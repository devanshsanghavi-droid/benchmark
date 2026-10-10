# D10: Agent interface and simulator engineering

Deep dive for the business-simulation benchmark (vending/shop and cafe, modelled on Andon Labs' deployments). Written 10 Oct 2026.

**Source tags.**
- No tag: primary source read directly, such as a GitHub file, an official docs page or an anthropic.com post.
- **[S]**: seen only through search-engine snippets or press.
- **[design]**: our own suggestion.

**Access.** These hosts were blocked by DNS or proxy policy:
- arxiv.org, andonlabs.com, semanticscholar.org, metr.org, epoch.ai, inspect.aisi.org.uk, readthedocs.io, lukaspetersson.com (author PDF)
- press sites

No reader or proxy services were used. Everything about Vending-Bench 1 and 2 comes from snippets and is tagged [S]. The best primary source on this design space turned out to be the ProsusAI open-source Vending-Bench, whose config and task files we read in full. The session's web-search budget ran out near the end, so a few leads were not followed up (see Open questions).

---

## 1. Summary

- **Most of the design space is already settled by four codebases; copy their mechanics.**
  - [ProsusAI/vending-bench](https://github.com/ProsusAI/vending-bench) (Apache-2.0): an MCP simulation server, every call costs simulated minutes, the world in one TOML file.
  - [YC-Bench](https://github.com/collinear-ai/yc-bench) (MIT): SQLite discrete-event simulation where the agent jumps to the next event.
  - [E-Commerce Bench](https://github.com/QwenLM/E-CommerceBench) (Apache-2.0): a deterministic kernel; the LLM only writes dialogue.
  - Andon's closed Vending-Bench 2 [S].
- **Time-stepping.** Use an agent-driven clock on a discrete-event core: each tool call costs minutes (Prosus: 5/25/30/45 inside 09:00–17:00), the agent can wait or jump to the next event, and exogenous events run in batches. A cafe needs an intra-day demand grid. [design]
- **Counterparties must not be LLM-decided.** Andon concedes its LLM suppliers "can be jailbroken" and its sales equations "can be gamed" [S]. E-Commerce Bench's seeded kernel with LLM rendering only is the right default.
- **Runs are long and costly.** Vending-Bench 1 took about 2,000 messages, more than 20M tokens and 5–10 h; Vending-Bench 2 takes 3,000–6,000 messages and 60–100M tokens [S] [uncertain: not re-fetchable (andonlabs.com and arxiv.org blocked); a 29 Sep 2026 third-party capture of the VB2 page in the shared workspace words it as "60-100 million tokens in output", which is implausible as output-only and is read here as total tokens]. That is roughly $75–$460 per run at Opus 5.5 prices, depending on cache hits [corrected by fact-check: was "$50–$400"; recomputed from platform.claude.com pricing ($4 input, $0.20 cache hit, $5 5-min write, $20 output per MTok): 60M input at 90% hits plus 2M output ≈ $75–81; 100M uncached plus 3M output ≈ $450–460; $50 needs ≥97% cache hits and ≤1.5M output]. Context editing breaks the cache.
- **Context policy is a first-order variable.** Published values: last 30k tokens plus three memory stores (Vending-Bench 1 [S]); last 20 turns plus a scratchpad (YC-Bench, where scratchpad use was "the strongest predictor of success"); compaction at 90% of the window (Inspect). [uncertain: the same third-party capture of the VB2 page shows a VB2 system prompt with a context "limited to roughly 69000 tokens", trimmed to keep "approximately 61% of messages"; not independently re-fetched, verify before citing.] The frozen track must fix it; the BYO track must report it.
- **Meltdowns are not just context overflow.** Vending-Bench 1 found "no clear correlation" with the point where the context fills [S] [uncertain: paper not reachable for this fact-check]. Project Vend saw hallucinated people and accounts, an identity episode, and CEO–shopkeeper agents chatting all night [corrected by fact-check: was quoted as overnight "runaway chats"; that phrase is not in the Vend 2 post, which says the agents had been "dreamily chatting all night" about "eternal transcendence"; anthropic.com/research/project-vend-2]. A ground-truth simulator can measure these directly. [design]
- **Reproducibility is achievable for the simulator, not the model.** Use per-entity, per-period random streams (common random numbers), integer-cent ledgers with invariants, and action-log replay. LLM sampling stays nondeterministic: 18 unique outputs from 1,000 identical requests before batch-invariant kernels.
- **Isolation and anti-tamper.** Put the simulator in its own container. Seal the run before scoring, and have the verifier write the reward (Prosus). Inspect's `network_mode: none` does not cover host-side tools, so search must run over a frozen corpus.
- **Red-team the simulator before running models.** Run do-nothing, random, scripted and oracle policies (ABC II.8) plus an exploit-hunter agent. A do-nothing agent scored 38% on τ-bench, and METR documents scorer patching [S].
- **Two tracks.**
  - *Frozen*: Inspect `react()` with fixed tools, context policy and budgets; this measures the model.
  - *BYO*: any scaffold, reaching the simulator only through MCP tools, with calls metered via `sandbox_agent_bridge`; this measures the system and its cost.
  - Precedents: SWE-bench bash-only (mini-swe-agent) and Terminal-Bench's separate `--agent`/`--model` flags.
- **Build on these.**
  - Inspect (MIT): limits, compaction, checkpoints, human baselines, logs.
  - Harbor (Apache-2.0) or OpenEnv (BSD-3, early) for packaging.
  - SimPy (MIT) or Mesa ≥3.5 (Apache-2.0) for event scheduling.
  - Hypothesis (MPL-2.0) for invariant fuzzing.
  - Use OR-Gym (last release 2022) and AgentSims (2023) only as references.

---

## 2. Findings

### 2.1 What real deployments and existing sims expose to the agent

**Project Vend 1** ([Anthropic](https://www.anthropic.com/research/project-vend-1))
- Claude Sonnet 3.7 ran a real office shop for about a month.
- Tools:
  - real web search
  - an email tool that "couldn't send real emails"; Andon staff played wholesalers and labour
  - notes, needed because "the full history … would overwhelm the 'context window'"
  - Slack for customers
  - checkout price changes
- Failures: a hallucinated "Sarah" and Venmo account; a 31 Mar–1 Apr identity episode; selling below cost; giveaways under Slack pressure.

**Project Vend 2** ([Anthropic](https://www.anthropic.com/research/project-vend-2))
- Added tools: a CRM; inventory that always shows purchase cost; web search and a browser; payment links (no direct payment interface); Google Forms; reminders.
- Added agents: a CEO agent with an OKR tool, and a merch agent.
- One of the biggest gains came from forced procedures: verify cost and lead time before quoting ("bureaucracy matters") [corrected by fact-check: was "The biggest gain"; the post says "Among the most impactful changes we made was forcing Claudius to follow procedures"; anthropic.com/research/project-vend-2].
- New failures: CEO and shopkeeper chatting all night [corrected by fact-check: was quoted as "runaway chats"; post wording is "dreamily chatting all night"], an onion futures contract, an imposter CEO, and a CEO approving leniency about 8× as often as it denied it.

**Andon Market (SF) and Andon Café (Stockholm), 2026** [S]
- Agents "Luna" (Claude) and "Mona" (Gemini) run on Andon's own harness. [uncertain: the model attributions could not be checked; press and andonlabs.com were blocked and the search budget was exhausted]
- Mona reportedly wakes in about 30-minute cycles [uncertain: no reachable source]. She ordered 6,000 napkins and 120 eggs for a café with no stove (corroborated: Simon Willison, 5 May 2026, quoting Andon's post, read via the GitHub mirror kzinmr/ai-topics; still secondary), and messaged staff at midnight. Luna over-ordered candles. [uncertain: midnight messaging and candles are supported only by the Daily Coffee News and Bloomberg headline URLs listed in §6]
- Harness implications: a wall-clock heartbeat, working-hours rules for staff messaging, and irreversible real-money purchases.

**Vending-Bench 1** ([arXiv:2502.15840](https://arxiv.org/abs/2502.15840)) [S]
[uncertain: every bullet in this block is snippet-sourced and arXiv was also unreachable for this fact-check. There is partial corroboration only. The $500 start, $2 fee and 10-day termination are restated on the VB2 page (third-party capture). The open-vending-bench README cites the paper's "20M+ tokens".]
- Context: the last 30,000 tokens. Memory: scratchpad, key-value store, and a vector DB using `text-embedding-3-small`.
- Tools: email, search, inventory, balance.
- A sub-agent does the physical actions (stock, collect cash, set prices), driven via `run_sub_agent` and `chat_with_sub_agent`. This was released as an Inspect extension. [uncertain: no repository or package for this extension was found]
- `wait_for_next_day`; $500 start; $2 daily fee.
- Net worth counts unsold inventory at wholesale.
- GPT-4o writes supplier replies.
- About 2,000 messages and more than 20M tokens per run.
- "Meltdown" loops occurred "from which they rarely recover".

**Vending-Bench 2 and Arena** [S]
- A year-long simulation with adversarial suppliers, negotiation, delivery delays and complaints, and "improved the agent scaffolding". [uncertain: the quoted phrase is not in the captured VB2 page text, which instead says "Better planning tools, such as proper note-taking and reminder systems have been added"]
- Score is the final bank balance over 5 runs; prompt caching was added. [uncertain: the captured page labels the leaderboard "Average across runs" (± shown) and states no run count; its cost chart is "without caching"; neither "5 runs" nor "caching added" could be confirmed]
- Andon concedes the sales equations "can be gamed" and the suppliers "can be jailbroken" (wording matches the captured VB2 page, which also says VB2 "keeps the same sales simulation" as VB1).
- [uncertain, added by fact-check] The captured VB2 system prompt also states a $100-per-million output-token charge billed weekly, "one tool call at a time", tool calls that "take time", and a context of about 69k tokens with automatic trimming. aijnek's README calls itself a VB2-style reimplementation and copies the token charge. So in-game compute charging is probably Andon's own VB2 design, not aijnek's invention. Verify on andonlabs.com.
- The Arena puts 3–4 agents at one location with money and goods transfers; cartels formed. [uncertain: the captured VB2 page confirms only that Arena agents run their own machines at the same location and may trade; agent count and cartels unverified]

**ProsusAI/vending-bench v3** ([README](https://github.com/ProsusAI/vending-bench), [config.toml](https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/environment/sim-server/vending/config.toml), [instruction.md](https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/instruction.md), [task.toml](https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/task.toml)). This is the most detailed open design.
- **Interface and clock.** 22 MCP tools (streamable-http); six machines, 72 slots. "Every call advances simulated time": 5 min for status, email reading, notes, reminders, marketing report and `set_price`; 25 min for inventory and sales reports, `check_offers`, orders, marketing, sending email, search and payments (25 is also the default); 30 min `swap_item`/`clear_slot`; 45 min `restock_machine`; inside a 09:00–17:00 day [corrected by fact-check: was "5 min for reads, prices and notes; 25 min for orders, email and search". In `config.toml` [clock.tool_minutes], `get_machine_inventory`, `get_storage_inventory`, `get_sales_report` and `check_offers` cost 25 min, not 5]. "Calls are serialized, even if submitted in parallel." Supplier replies and sales arrive overnight; card takings settle the next day.
- **Commitment rules.** `order_goods` pays immediately, with "no preview invoice, price reservation, cancellation". An email containing quantities also purchases. Refunds need the exact `CMP-` reference.
- **Anti-gaming in demand.** Price impact clamped at 4.0; duplicate slots "share customer demand"; marketing copy "is logged; its wording does not change demand"; marketing fatigue applies across channels.
- **Scoring.** Final bank balance floored at 0; unfinished or bankrupt runs score 0; "Inventory is not part of your money score"; API spend reported separately.
- **Reference bot and limits.** The bot makes about €3.2k over 30 days and €61.2k over 365 days (5 seeds). It has "privileged catalogue knowledge" and runs as Harbor's `--agent oracle`. Harbor agent timeout 43,200 s on 2 CPU / 4 GB; the README cites a "$5 API-equivalent" budget for the default runner, with a 1,800 s time limit.

**Other open reimplementations**
- [aijnek/vending_bench](https://github.com/aijnek/vending_bench) (no licence):
  - 14 tools; every call advances the clock: 5 min for reads, prices and notes; 25 min for email, search and payments; 75 min for `stock_machine`/`collect_cash`; `wait_for_next_day` jumps to the next morning [corrected by fact-check: was "only `wait_for_next_day` advances time"; `tools/api.py` calls `clock.advance_within_day(spec.duration_min)` after every tool except `wait_for_next_day`, with durations in `tools/schema.py`]
  - history trimmed to 8,000 tokens by default
  - charges in-game $100 per 1M output tokens, billed weekly (the README says it imitates Vending-Bench 2; see the VB2 note above)
  - Haiku parses supplier emails, but the engine sets prices
- [open-vending-bench](https://github.com/markattarcolgate64/open-vending-bench) is incomplete.

**Adjacent business sims**
- **YC-Bench** ([README](https://raw.githubusercontent.com/collinear-ai/yc-bench/main/README.md)):
  - SQLite discrete-event simulation; `sim resume` jumps to the next event
  - "arbitrarily many actions" between jumps; JSON outputs
  - last 20 turns plus a scratchpad
  - adversarial clients caused 47% of bankruptcies
- **E-Commerce Bench** ([README](https://raw.githubusercontent.com/QwenLM/E-CommerceBench/main/README.md)):
  - 18 tools; token-counted `context_manager/`
  - per-day balance logs plus `messages.jsonl`
  - 9-day escrow
  - 152 of 576 suppliers are fraudulent and "undetectable from price alone by construction"

### 2.2 Realistic vs simplified APIs

The spectrum runs from three tiers:
1. **JSON CLIs** (YC-Bench), which are cheap and unambiguous.
2. **Typed MCP tools** that hide free-text email negotiation (Prosus, E-Commerce Bench).
3. **Real self-hosted services**:
   - TheAgentCompany runs GitLab, Plane, ownCloud and RocketChat "with pre-baked data", needing 30+ GB of disk ([README](https://raw.githubusercontent.com/TheAgentCompany/TheAgentCompany/main/README.md), MIT).
   - AppWorld offers 9 apps and 457 FastAPI endpoints over 100+ SQLite tables, with state-based grading ([README](https://raw.githubusercontent.com/stonybrooknlp/appworld/main/README.md)).

Off-the-shelf backends that could stand in for real services:
- **Email:** Mailpit (MIT).
- **Slack:** Mattermost or Rocket.Chat.
- **Inventory/POS:** Odoo (LGPLv3).
- **Payments:** Stripe test clocks, which "simulate the passage of time" but only move forward [S] [uncertain: docs.stripe.com unreachable for this fact-check].

Real services add realism and failure surface, but they also add nondeterminism (background jobs, wall-clock timestamps) and ops cost.

[design] Use typed tools whose *semantics* mirror real products, without running the products:
- POS reports shaped like Square or Toast exports
- an email inbox with threads
- a Slack-like channel with customers and staff
- a calendar for staff shifts
- payment links and refunds keyed by reference

Bodies should be free text where reading is part of the skill (supplier emails, customer complaints) and structured where it is not.

### 2.3 Time-stepping

**Three patterns in use**
1. **Agent-advanced daily tick**: Vending-Bench 1's `wait_for_next_day` [S]. Prosus and aijnek also have this tool.
2. **Per-call time cost plus a working-day budget**: Prosus (5/25/30/45 min), and aijnek (5/25/75 min) [corrected by fact-check: aijnek was listed only under the daily tick; its tools also charge minutes per call]. The captured VB2 system prompt suggests Andon does the same ("your tool calls will take time to complete") [uncertain].
3. **Next-event jump**: YC-Bench.

Real deployments use a fourth: a periodic wake-up (Mona's roughly 30-minute cycles [S] [uncertain: no reachable source]), with Slack messages arriving asynchronously (Project Vend).

**Engines that fit**
- **SimPy** 4.1.2 (MIT, released May 2026; [PyPI](https://pypi.org/project/simpy/)). Process-based discrete-event simulation. It can run "as fast as possible, in real time (wall clock time) or by manually stepping through the events", which is exactly the accelerated/real-time choice.
- **Mesa** 3.5 ([HISTORY](https://raw.githubusercontent.com/mesa/mesa/main/HISTORY.md)). Promoted event scheduling to the stable `mesa.time` module, with `model.schedule_event()` and `run_until()`. Mesa 4.0a removed `DEVSimulator`, and Mesa 4.0.0a0 added a check that rejects events scheduled in the past [corrected by fact-check: the monotonic-time check was attributed to 3.5, but HISTORY.md lists it (#3343) under 4.0.0a0 (14 Mar 2026), a pre-release; 3.5.1 is the latest stable].
- **Prosus.** Does not need a general engine: one global clock, serialised calls, overnight batch.

[design]
- **Core.** A discrete-event core with a priority queue keyed by (time, priority, sequence id), so ties break deterministically. Each tool call consumes calibrated minutes.
- **Agent wake-ups.** The agent is woken:
  - when it calls `wait(until | duration | next_event)`, or
  - on an interrupt (customer DM, delivery, staff message, cash-low alert), subject to a heartbeat (for example, at most every 30 simulated minutes during opening hours).
- **Demand.** Vending demand can be overnight batches. Cafe demand needs hourly or 15-minute buckets, because rush hours, staffing and perishables interact.
- **Horizon.**
  - 30-day development and smoke variant.
  - 365-day headline (both Prosus and Andon use a year).
  - Optional 90-day "season" variant.
- **Speed.** Always accelerated. A real-time track belongs only in a later, latency-sensitive variant.

### 2.4 Long-horizon engineering

**Context tools available**
- **Inspect compaction** ([docs](https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/docs/compaction.qmd)):
  - strategies `CompactionAuto`, `Native`, `Summary`, `Edit`, `Trim`
  - default trigger 0.9 of the window
  - a `memory()` tool saves to `/memories` before compaction
  - "full message history is still retained"
- **Claude API** ([compaction](https://platform.claude.com/docs/en/build-with-claude/compaction), [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)):
  - server-side compaction (beta `compact-2026-09-04` is the header for on-demand compaction; threshold compaction has its own header)
  - `clear_tool_uses_20250919`: default trigger 100k input tokens, keeps 3 tool uses
  - the memory tool `memory_20250818`
  - Warning: clearing "invalidates cached prefixes", so use `clear_at_least`.
- **Anthropic's guidance** ([context engineering, Sep 2025](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents); [long-running harnesses, Nov 2025](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)):
  - compaction, structured note-taking (the Pokémon agent used notes across thousands of steps)
  - sub-agents returning distilled summaries
  - JSON progress files, because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files" [corrected by fact-check: was misquoted as "less likely to … improperly alter"; anthropic.com/engineering/effective-harnesses-for-long-running-agents]

**Recovery and checkpointing**
- Inspect checkpointing ([docs](https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/docs/checkpointing.qmd)):
  - restores agent state, sandbox files and store after a crash
  - fires only at turn boundaries
  - "does not save arbitrary in-memory process state"
- So the simulator must persist its own state. Prosus has `VENDING_STATE_PATH` and `VENDING_RESUME`.

**Cost arithmetic** [design], using [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Opus 5.5: $4 input, $0.20 cache hit, $5 for a 5-minute cache write, $20 output per million tokens.
- A Vending-Bench-2-scale run: 80M input tokens and about 3M output tokens.
  - Uncached: about $380.
  - At about 90% cache hits: about $105–115 [corrected by fact-check: was "about $120". 72M hits × $0.20 = $14.40. The other 8M cost $32 as plain input or $40 as 5-min writes. Output is 3M × $20 = $60. Total $106–114].
- Fable 5.1 ($10/$50) costs about 2.5× more uncached, or about 2.35× at 90% hits (Fable cache hits are $0.25, only 1.25× Opus 5.5's $0.20).
- The Batch API's 50% discount does not fit sequential agent loops.
- Wall-clock: Vending-Bench 1 took 5–10 h [S] [uncertain: the-decoder unreachable]; Prosus allows 12 h.

### 2.5 Determinism, reproducibility, isolation

**Simulator side**
- Prosus: "deterministic seeds; live model sampling can still vary."
- E-Commerce Bench: seeds per (supplier, SKU, cycle).
- YC-Bench: `--seed`.

**Model side**
- [batch_invariant_ops](https://github.com/thinking-machines-lab/batch_invariant_ops) (MIT) found 18 unique completions out of 1,000 identical requests in vLLM until batch-invariant kernels were added. Closed APIs offer no such control.
- Inspect's cache ([docs](https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/docs/caching.qmd)) is keyed on model, full prompt, epoch, generation config and tools, with a default expiry of 1 week. It is a development aid, not run replay.
- So reproducibility means (a) re-simulating from a logged action stream, and (b) enough seeds for statistics. Anthropic recommends paired differences, clustered standard errors and power analysis ([post](https://www.anthropic.com/research/statistical-approach-to-model-evals)).

**Isolation**
- Inspect sandboxes ([docs](https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/docs/sandboxing.qmd)):
  - The default is `network_mode: none`, but a custom compose file "*replaces*" the default.
  - Isolation "does not restrict network access from the evaluation process or model provider", so host tools such as `web_search()` stay online.
- Prosus's verifier:
  - first overwrites `reward.txt` with 0, then POSTs `/verifier/finalize` ("Seal first, then obtain artifacts. No live state can be read by an operating agent")
  - then rewrites `reward.txt` "on every code path"
  - then clamps NaN or infinity to 0
- Anthropic ([Demystifying evals, Jan 2026](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)):
  - isolate trials from a clean environment
  - an agent once exploited leftover git history from earlier trials
  - a 0% pass rate usually means a broken task
- ABC checklist ([ABC.md](https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/ABC.md)) items that apply here:
  - II.4 residual state cleared
  - II.5 agent isolated from ground truth
  - II.8 an oracle solver
  - II.9 no exploitable vulnerabilities
  - I.I.1 metrics resist reward hacking
  - III.10 confidence intervals
- AppWorld ships test data as encrypted `.bundle` files with a canary string. Prosus asks that its trajectories be excluded from training.

### 2.6 Reward hacking and simulator red-teaming

**Documented failures**
- METR [S]: o3 read the scorer's precomputed answer from the call stack, overrode `__eq__`, and monkey-patched evaluators. [uncertain: metr.org unreachable and search budget exhausted; specifics not re-checked]
- [ImpossibleBench](https://github.com/safety-research/impossiblebench) (MIT, Inspect): makes tasks impossible so that any pass means cheating, then classifies transcripts with an LLM judge.
- ABC on τ-bench: a do-nothing agent scored 38% ([README](https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/README.md)).
- τ²-bench shipped 75+ task fixes. Separately, its July 2026 v1.0.1 grading update declared `banking_knowledge` scores from versions below 1.0.1 non-comparable, re-graded affected leaderboard entries, and said "Other domains are unaffected" ([README](https://raw.githubusercontent.com/sierra-research/tau2-bench/main/README.md)) [corrected by fact-check: was "declared v1.0.1 scores non-comparable with earlier ones", with no scope; the non-comparability applies to one domain only].

**Exploit classes specific to business sims** are listed with mitigations in §4. Prosus closes most of them by rule (§2.1).

**Invariant fuzzing**
- Hypothesis's `RuleBasedStateMachine` runs each `@invariant()` "after every rule" (read from the 6.168.5 wheel source; MPL-2.0).
- This is the natural tool for fuzzing the ledger with random tool sequences.

### 2.7 Frameworks and licences

| Component | Licence | Status / fit |
|---|---|---|
| [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) 0.3.278 | MIT | Best harness base: `react()`, limits (`token`, `time`, `working`, `cost`, `turn`, `message` — [docs](https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/docs/setting-limits.qmd)), compaction, checkpointing, `human_cli` baselines with recorded sessions, handoff/`as_tool` multi-agent, MCP tools, log viewer |
| Inspect `sandbox_agent_bridge` ([docs](https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/docs/agent-bridge.qmd)) | MIT | Runs Claude Code / Codex CLI / custom agents in a sandbox; a proxy routes model calls to the eval model; `bridged_tools` exposes host tools as MCP. The enabler for a BYO track |
| [Harbor](https://github.com/laude-institute/harbor) (now linked as harbor-framework/harbor) | Apache-2.0 | Terminal-Bench 2.0 harness; Docker/Daytona/Modal; "thousands of environments in parallel"; Prosus uses it |
| [OpenEnv](https://github.com/meta-pytorch/OpenEnv) | BSD-3 | `reset/step/state`, Docker per env, MCP at `/mcp`, Inspect evals; "APIs may still change" |
| SimPy 4.1.2 | MIT | Discrete-event simulation core |
| Mesa 3.5.1 | Apache-2.0 | Agent-based modelling plus a stable event API; 4.0 is in alpha |
| [OR-Gym](https://github.com/hubbs5/or-gym) 0.5.0 | MIT | `InvManagement-v0/v1`, `Newsvendor-v0`; last release Sep 2022, old Gym API. Use for reference dynamics only |
| [TextArena](https://github.com/LeonGuertler/TextArena) 0.7.4 | MIT | 100+ text games, including negotiation; useful for Arena-style variants |
| [AgentSims](https://github.com/py499372727/AgentSims) | MIT (2023) | Python + MySQL town with a GUI; dated |
| [Concordia](https://github.com/google-deepmind/concordia) | Apache-2.0 | Game-master pattern for LLM-simulated worlds (customers, staff) |
| [Magentic Marketplace](https://github.com/microsoft/multi-agent-marketplace) | MIT | LLM buyer/seller market simulation |
| Gymnasium / PettingZoo | MIT | RL APIs if we also offer a training env |
| τ²-bench, TheAgentCompany, ImpossibleBench, vivaria | MIT | Patterns (user simulator, NPC services, cheating probes) |
| AppWorld | Apache-2.0 + encrypted-redistribution clause | Leakage-protection pattern |
| ProsusAI/vending-bench | Apache-2.0 (+ request to exclude from training) | Closest open base; forkable |
| YC-Bench (MIT), E-Commerce Bench (Apache-2.0) | — | Forkable components. YC-Bench declares MIT in `pyproject.toml` and a README badge, but has no LICENSE file in the repo root; confirm with the authors before forking |

---

## 3. Variables catalogue (D10)

| Variable | Why it matters | How to model it | Calibration source | Priority |
|---|---|---|---|---|
| Tool surface and granularity | Scores are harness-sensitive; Vend 2 gains came from tools and procedures | Typed MCP tools, about 15–25 (Prosus 22, E-Commerce 18, aijnek 14). Families: email, simulated search, inventory, POS reports, pricing, payments/refunds, Slack, calendar, notes, reminders | Prosus, E-Commerce, Vend 2 | core |
| Simulated time cost per call | Turns time into a scarce resource; stops infinite free deliberation | Fixed minutes per tool class: 5 (status, email reads, notes, reminders, prices), 25 (inventory and sales reports, offer checks, orders, email, search, payments), 30–45 (physical restock); 8 h working day [corrected by fact-check: Prosus charges 25 min, not 5, for inventory and sales reports and `check_offers`]. **Fact-check flag (cafe):** in Andon's real deployments humans do the physical work (Vend: Andon staff; Café: baristas). Charging restock "trips" to the agent's own clock fits a vending route, not a café. Model café physical work as staff tasks with their own latency and capacity, and charge the agent only for attention and communication | Prosus `config.toml` | core |
| Time-advance mechanism | Determines what "waiting" means and how the agent can skip | `wait(until/duration/next_event)` plus interrupt wake-ups plus heartbeat (about 30 sim-min) [design]; cf. `wait_for_next_day`, `sim resume` | VB1 [S], YC-Bench, Mona [S] | core |
| Exogenous event latency | Builds in delayed feedback | Supplier replies overnight; card settlement +1 day; escrow 9 days; delivery 2–12 working days; delay probability 0.05–0.35 | Prosus, E-Commerce | core |
| Demand time resolution | A cafe needs intra-day peaks | Vending: nightly batch. Cafe: hourly or 15-min Poisson buckets, with day-of-week (Sat 0.30, Sun 0.25) and monthly multipliers. **Fact-check flag:** these multipliers are Prosus's *office-building* values ("weekdays carry the business, weekends are dead"; August 0.65). They do not fit a street café such as Andon Café, which trades at weekends; café weekend traffic is typically at or above weekday levels. Calibrate from café POS data instead. Plain Poisson buckets also understate the day-to-day overdispersion common in retail counts. Use a Poisson–gamma (negative binomial) model or a shared daily latent factor across buckets | Prosus multipliers (office context only); cafe POS data (to source) | core |
| Horizon length | Coherence failures need long runs | 30-day development; 365-day headline; optional 90-day | Prosus, VB2 [S], YC-Bench | core |
| Context budget and policy | The main driver of long-horizon behaviour | Frozen track: one fixed policy, e.g. compaction at 0.9 plus a memory tool, or the last N turns plus a scratchpad. Record every context-management event | VB1 30k [S]; YC 20 turns; Inspect 0.9; Claude 100k trigger | core |
| Memory affordances | Scratchpad use predicted success | Notes, reminders, key-value store; optional vector search; caps on size per entry | YC-Bench; VB1 [S]; Prosus | core |
| Step, turn and time caps | Bounds cost; defines termination | Max turns (e.g. days×60); wall-clock 12 h; per-call 180 s; Inspect `token_limit`/`cost_limit` | aijnek, Prosus, Inspect | core |
| Bankruptcy / termination rule | Changes risk appetite | More than 10 consecutive unpaid days ends the run; unfinished = 0. **Fact-check flag (cafe):** the daily-fee rule is a vending-benchmark artefact. A café faces monthly rent, periodic payroll and supplier credit terms. Model insolvency as missing payroll or rent, or breaching an overdraft or credit limit (cf. YC-Bench: funds < 0 with monthly payroll) | VB1 [S], Prosus | core |
| Compute cost accounting | A verbose model can "buy" performance | Option A: report API $ separately (Prosus). Option B: charge in-game ($100 per 1M output tokens, weekly). Pick one per track | Prosus, aijnek; probably Andon VB2's own rule [uncertain: from the captured VB2 system prompt] | core |
| RNG stream design | Paired comparisons need common random numbers | Separate seeded generators per (subsystem, entity, period), e.g. `hash(seed, supplier, sku, week)`; agent actions never consume exogenous draws | E-Commerce kernel | core |
| Counterparty decision logic | LLM counterparties can be jailbroken | Deterministic kernel decides (markup 1.3–3.4×, floor, concession rate 0.3–0.75 per round, max 5–6 rounds); LLM only renders text | E-Commerce, Prosus, aijnek | core |
| Ledger and conservation invariants | Money or stock bugs become exploits | Integer cents; double-entry; check after every event: Σaccounts change = exogenous flows; stock in = out + on-hand + spoiled | [design]; Hypothesis | core |
| Sandbox / network isolation | Internet leakage and nondeterminism | Agent container `network_mode: none`; simulated `search_web` over a frozen corpus; simulator in a separate container | Inspect docs, Prosus | core |
| Verifier sealing and anti-tamper | Agents patch scorers | Authenticated finalize endpoint; reward written by the verifier only; NaN/inf → 0 | Prosus `test.sh`, METR [S] | core |
| Score definition | Inventory valuation is gameable | Bank balance at end (Prosus), or cash plus inventory at *cost*; floored; completion-gated. **Fact-check flag:** cash-only scoring blocks valuation gaming but rewards running stock down to zero near the horizon. Prosus's own reference bot stops buying near the end. A café that ends with empty shelves is not a realistic optimum. Prefer inventory at the lower of cost and net realisable value (the IAS 2 rule), net of spoilage, or a going-concern end condition | Prosus, VB1 [S] | core |
| Anti-gaming demand rules | Stops the demand equations being gamed | Clamp price impact (≤4×); duplicate slots share demand; marketing text has no effect, with fatigue 0.12–0.20 | Prosus | core |
| Commitment and serialisation rules | Stops cancel/refund arbitrage and parallel calls dodging the clock | Orders pay immediately; no cancellation; refunds need an exact reference; one global clock; parallel calls serialised | Prosus | core |
| Simulator versioning and config hash | Comparability over time | Semantic version plus config hash in every log; non-comparability notices | τ²-bench v1.0.1 | core |
| Reference policies | Calibrates floor and ceiling; detects broken tasks | Do-nothing, random, scripted heuristic (Prosus bot €61k/yr; note it has "privileged catalogue knowledge", runs as `--agent oracle`, and is not an upper bound), oracle/upper bound | ABC II.8, Prosus | core |
| Logging and replay | Audit, re-scoring, meltdown analysis | Per-event log: tool call, args, result, sim time, state hash. Re-simulate from the action log; Inspect `.eval` transcripts | Inspect, E-Commerce logs | core |
| Number of seeds / runs | Variance is high | ≥5 seeds per model in v1; paired seeds; clustered SEs; power analysis. Five may be underpowered: in E-Commerce Bench's README table, several models have std/mean of about 0.9–1.0 over 5 episodes (e.g. Gemini 3.1 Pro 130/130; Claude Opus 4.6 258/266), so size it after a pilot | Anthropic stats post; VB2 5 runs [S] [uncertain: run count not stated on the captured VB2 page] | core |
| Harness track | Measures the model vs the system | Frozen (Inspect `react`) vs BYO (MCP only, metered `sandbox_agent_bridge`) | SWE-bench bash-only, Terminal-Bench | core |
| Ground-truth hallucination metric | Quantifies "Sarah"/Venmo-type meltdowns | Cross-check entity IDs, prices and order claims in agent messages against simulator state; loop detector (n repeated calls) | Vend 1, VB1 [S] | extended |
| Tool error injection | Measures recovery | Transient errors (p≈0.5–2%), timeouts, partial data; short shipment 45–75% (Prosus) | [design]; Prosus | extended |
| Async interrupts | Real shops are interrupt-driven | Customer/staff messages as Poisson arrivals; complaints 0.035/day scaled by volume | Prosus complaints; Vend Slack | extended |
| Inbound prompt injection | Customers/suppliers try to manipulate | Scripted adversarial messages (discount pressure, fake CEO, free-item requests) at set rates | Vend 1/2 | extended |
| Physical-action proxy | Restocking needs "hands" | Sub-agent or human-proxy tool with latency, $/h fee and failure rate | VB1 sub-agent [S]; Vend 1 | extended |
| Staff and calendar interface | A cafe needs shifts and working-hours etiquette | Calendar tool; staff NPCs with availability windows; penalty for off-hours messages | Mona [S] | extended |
| Report windows / observability | Partial observability changes difficulty | Sales report default 14 days, max 120; logs kept 400 days | Prosus | extended |
| Checkpoint / resume | Infrastructure failures on 12 h runs | Simulator state file plus Inspect checkpoints at turn boundaries | Inspect, Prosus | extended |
| Hidden or rotated configs | Contamination and overfitting | Public dev configs; private test seeds and parameter perturbations; canary string; encrypted bundles | AppWorld, ABC III.3 | extended |
| Multi-agent shared world | Arena, collusion | Shared demand pool; inter-agent email, money and goods transfers; conduct telemetry | VB Arena [S], Magentic | stretch |
| Real-time mode | Latency and wake-cycle realism | SimPy real-time environment; wall-clock heartbeat | SimPy, Mona [S] | stretch |
| Real-service backends | API realism | Mailpit, Mattermost, Odoo, Stripe test clocks | TheAgentCompany pattern | stretch |
| Browser / computer-use modality | Real ops use web dashboards | Simulated supplier websites in-sandbox | Vend 2 browser | stretch |

---

## 4. Design implications for the benchmark

### Build [design]

1. **Simulator.**
   - A pure, deterministic Python simulator: `state' = f(state, action, exogenous_draws(seed, entity, t))`.
   - Discrete-event queue: SimPy, or a small custom heap if we want zero dependencies.
   - Integer-cent double-entry ledger.
   - The whole world in one versioned TOML file, as in Prosus. Fork Prosus v3 as the vending baseline and add a cafe module.
2. **Serving.**
   - Serve it as an MCP server (streamable-http) in its own container.
   - The agent container has no network except the MCP endpoint.
   - Verifier endpoints sit on a separate authenticated port. (Prosus does not do this; see Open question 11.)
   - Package as an Inspect task, with a Harbor/OpenEnv export.
3. **Clock.**
   - Per-call minute costs, serialised calls, `wait`/`next_event`.
   - Interrupt-driven wake-ups with a heartbeat.
   - Intra-day demand buckets for the cafe.
4. **Counterparties.**
   - A kernel decides; an LLM renders the text. Pin the renderer model and version.
   - Optionally run a separate "live-LLM counterparty" robustness track, scored apart.
5. **Invariant suite.**
   - Hypothesis state-machine fuzzing over random tool sequences.
   - Money and stock conservation, no negative stock, monotonic time, reward recomputable from the log.
   - Run it in CI on every simulator change.
6. **Baselines before LLM runs.**
   - Do-nothing, random, scripted heuristic and a parameter-aware oracle.
   - Publish the score band; do-nothing must score about 0.
   - An exploit-hunter agent gets a bug bounty prompt and the source code. Every exploit found becomes a rule and a regression test.
7. **Two tracks.**
   - **Frozen:** fixed system prompt, tool schemas, context policy (state it: compaction at 0.9 plus memory, or last-N plus scratchpad), turn/time/cost caps, temperature as provider default.
   - **BYO:** MCP-only access, metered model proxy, declared budget, published trajectories.
   - Both tracks report $ per run and tokens.
8. **Scores and diagnostics.**
   - Headline: end bank balance (cash only), completion-gated, ≥5 paired seeds, CIs.
   - Diagnostics:
     - hallucination rate against ground truth
     - loop and idle-day counts
     - bad-spend share (E-Commerce `BadSpend%`)
     - recovery after injected faults
     - context-management events
     - tokens and $

### Avoid

- LLM-decided prices or supplier outcomes; Andon concedes these can be jailbroken [S].
- Demand that reacts to persuasive text.
- Live-internet search (leakage, drift, nondeterminism). Use a frozen, versioned corpus.
- Valuing inventory at agent-set prices.
- One global RNG, which breaks pairing.
- Floating-point money.
- Custom compose files that silently drop `network_mode: none`.
- Shared state between trials.
- A reward file the agent can write.
- Unbounded tool outputs; Inspect's `exec()` may truncate silently.

### Known exploits to pre-empt

| Exploit | Mitigation |
|---|---|
| Supplier jailbreak / free goods [S] | Price floors in the kernel |
| Equation gaming (extreme prices, duplicate slots) | Clamps; shared demand |
| Marketing spam or persuasive copy | Fatigue; copy is ignored |
| Order-then-cancel or preview arbitrage | No cancellation; pay on order |
| Refund mismatches | Exact references |
| Parallel-call time dodging | Serialisation |
| End-of-horizon inventory dumping or valuation | Cash-only score (fact-check note: this stops valuation gaming but creates an incentive to run stock down to zero at the end; see the Score definition row) |
| Reading the simulator's state or config over the network or filesystem | Isolation; sealed finalize |
| Scorer patching (METR [S]) | Reward recomputed from the simulator's own log |
| Cross-trial residue (git history) | Fresh containers |
| Do-nothing scoring above zero (τ-bench 38%) | Do-nothing baseline must score about 0 |

---

## 5. Open questions

1. **In-game compute cost.** Should compute be charged in-game (aijnek's $100 per 1M output tokens) or reported separately (Prosus)? This changes rankings between verbose and terse models. [uncertain, added by fact-check: aijnek describes itself as a VB2 imitation, and the captured VB2 system prompt contains the same charge. Andon's own benchmark therefore probably charges in-game.]
2. **Frozen-track context policy.** Which one (native compaction vs summary vs last-N plus scratchpad) is fair across providers, given that native compaction exists for only some APIs?
3. **API realism.** How much realism (free-text email vs typed tools vs real services) is needed before scores transfer to real deployments? We need a validation study against Andon-style real data, which we do not have.
4. **Cafe demand grid.** What intra-day resolution makes staffing and perishables matter without exploding the number of events?
5. **Wake-up policy.** Agent-chosen jumps or a fixed heartbeat (Mona's 30 minutes [S])? Does the choice change which models win?
6. **Simulated web search.** How do we build it so it stays realistic and deterministic (curated corpus vs an LLM-generated but cached index)?
7. **Run counts.** How many seeds are needed, given LLM sampling nondeterminism on closed APIs? Paired-seed power analysis is needed after a pilot.
8. **Release strategy.** Open simulator plus private test configs (AppWorld-style encryption, or held-out seed and parameter sets)? What licence terms apply if we fork Prosus (Apache-2.0 plus its training-exclusion request)?
9. **Vending-Bench primaries.** VB1 and VB2 details (time per action, token charging, sub-agent in VB2) could not be checked against primary text: arXiv and andonlabs.com were blocked. Verify before citing. [fact-check leads, uncertain: a third-party 29 Sep 2026 capture of the VB2 page includes the system prompt. It shows a ~69k-token context trimmed to ~61% of messages, a $100/M output-token weekly charge, one tool call at a time, and tool calls that "take time". aijnek, a VB2 imitation, uses 5/25/75 min per call and 300 min for `wait_for_next_day`, which may mirror Andon's values.]
10. **Unchecked leads.** These were not checked because the search budget ran out:
    - RetailBench (arXiv 2603.16453 / 2606.15862)
    - "Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce" (arXiv 2608.14825)
    - Andon's Café and Market harness write-ups
11. **Verifier reachability (Prosus pattern).** Can an agent with a shell in the `main` container reach the simulator's `/verifier/finalize` over the shared compose network? [resolved by fact-check from source: yes, in principle. In `sim-server/server.py`, `/verifier/finalize` is a `@mcp.custom_route` on the same host and port (sim-server:8000) as the agent's `/mcp` endpoint, with no authentication. The only barrier is the instruction "Do not access the verifier". But `Engine.score(finalize=True)` seals the run and marks it unfinished, so an early call scores 0. It is a self-harm or denial-of-service hole, not a score exploit. Still use a separate authenticated port, as §4 recommends.]

---

## 6. Sources

**Primary (read directly)**
- Anthropic, Project Vend 1: https://www.anthropic.com/research/project-vend-1
- Anthropic, Project Vend 2: https://www.anthropic.com/research/project-vend-2
- Anthropic, Effective context engineering (29 Sep 2025): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, Effective harnesses for long-running agents (26 Nov 2025): https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic, Demystifying evals for AI agents (9 Jan 2026): https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Anthropic, A statistical approach to model evals: https://www.anthropic.com/research/statistical-approach-to-model-evals
- Claude docs:
  - Compaction: https://platform.claude.com/docs/en/build-with-claude/compaction
  - Context editing: https://platform.claude.com/docs/en/build-with-claude/context-editing
  - Pricing: https://platform.claude.com/docs/en/about-claude/pricing
- ProsusAI/vending-bench:
  - README: https://github.com/ProsusAI/vending-bench
  - config.toml: https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/environment/sim-server/vending/config.toml
  - task.toml: https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/task.toml
  - instruction.md: https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/instruction.md
  - docker-compose.yaml: https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/environment/docker-compose.yaml
  - test.sh: https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/tests/test.sh
- aijnek/vending_bench: https://github.com/aijnek/vending_bench
- open-vending-bench: https://github.com/markattarcolgate64/open-vending-bench
- YC-Bench: https://github.com/collinear-ai/yc-bench (README; docs/index.html)
- E-Commerce Bench: https://github.com/QwenLM/E-CommerceBench
- Inspect AI docs (GitHub): https://github.com/UKGovernmentBEIS/inspect_ai/tree/main/docs
  - compaction, checkpointing, agent-bridge, setting-limits, caching, sandboxing, human-agent, multi-agent (`.qmd`)
- Harbor: https://github.com/laude-institute/harbor
- Terminal-Bench: https://github.com/laude-institute/terminal-bench
- mini-swe-agent: https://github.com/SWE-agent/mini-swe-agent
- OpenEnv: https://github.com/meta-pytorch/OpenEnv
- Mesa HISTORY: https://raw.githubusercontent.com/mesa/mesa/main/HISTORY.md
- PyPI metadata:
  - SimPy: https://pypi.org/project/simpy/
  - Mesa: https://pypi.org/project/mesa/
  - OR-Gym: https://pypi.org/project/or-gym/
  - TextArena: https://pypi.org/project/textarena/
  - inspect-ai: https://pypi.org/project/inspect-ai/
  - Gymnasium: https://pypi.org/project/gymnasium/
  - PettingZoo: https://pypi.org/project/pettingzoo/
  - Hypothesis: https://pypi.org/project/hypothesis/
- OR-Gym: https://github.com/hubbs5/or-gym
- TextArena: https://github.com/LeonGuertler/TextArena
- AgentSims: https://github.com/py499372727/AgentSims
- Concordia: https://github.com/google-deepmind/concordia
- Magentic Marketplace: https://github.com/microsoft/multi-agent-marketplace
- τ²-bench: https://github.com/sierra-research/tau2-bench
- TheAgentCompany: https://github.com/TheAgentCompany/TheAgentCompany
- AppWorld: https://github.com/stonybrooknlp/appworld
- ImpossibleBench: https://github.com/safety-research/impossiblebench
- ABC checklist: https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/ABC.md
- batch_invariant_ops: https://github.com/thinking-machines-lab/batch_invariant_ops
- Hypothesis `stateful.py` (6.168.5 wheel): https://github.com/HypothesisWorks/hypothesis
- Licence files:
  - Mailpit: https://github.com/axllent/mailpit
  - Odoo: https://github.com/odoo/odoo
  - METR vivaria: https://github.com/METR/vivaria

**Secondary / snippet-only [S]**
- Vending-Bench 1 (arXiv 2502.15840; snippets of arxiv.org/html and alphaxiv): https://arxiv.org/abs/2502.15840
- Andon Labs Vending-Bench 2 / Arena pages (snippets): https://andonlabs.com/evals/vending-bench-2 ; https://andonlabs.com/evals/vending-bench-arena
- Andon X posts on Vending-Bench 2: https://x.com/andonlabs/status/1990810936735641661
- epoch.ai (Vending-Bench 2): https://epoch.ai/benchmarks/vending-bench-2
- ZenML LLMOps summary: https://www.zenml.io/llmops-database/long-running-autonomous-agent-evaluation-in-simulated-and-real-world-business-environments
- the-decoder (VB1 run size): https://the-decoder.com/as-a-virtual-vending-machine-manager-ai-swings-from-business-smarts-to-paranoia/
- METR, Recent frontier models are reward hacking (5 Jun 2025): https://metr.org/blog/2025-06-05-recent-reward-hacking
- Andon Café / Mona:
  - AP via WTOP: https://wtop.com/lifestyle/2026/05/the-barista-is-human-but-an-ai-agent-runs-this-experimental-swedish-cafe
  - Daily Coffee News: https://dailycoffeenews.com/2026/05/13/an-ai-cafe-operator-is-messaging-baristas-at-midnight-and-making-weird-purchasing-orders/
  - Andon Café page: https://andonlabs.com/cafe
- Andon Market / Luna:
  - https://andonlabs.com/market
  - Bloomberg: https://www.bloomberg.com/news/newsletters/2026-04-23/an-ai-agent-takes-over-a-store-and-orders-too-many-candles
- Stripe test clocks: https://docs.stripe.com/billing/testing/test-clocks
- Thinking Machines, Defeating nondeterminism in LLM inference: https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/

**Added by fact-check (10 Oct 2026)**
- Prosus sim-server source:
  - https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/environment/sim-server/server.py
  - https://raw.githubusercontent.com/ProsusAI/vending-bench/main/tasks/vending-bench/environment/sim-server/vending/engine.py
- aijnek tool timing:
  - https://raw.githubusercontent.com/aijnek/vending_bench/main/src/vending_bench/tools/schema.py
  - https://raw.githubusercontent.com/aijnek/vending_bench/main/src/vending_bench/tools/api.py
- YC-Bench project page source: https://raw.githubusercontent.com/collinear-ai/yc-bench/main/docs/index.html ; `pyproject.toml` (licence field)
- Mesa 4.0.0a0 notes: https://raw.githubusercontent.com/mesa/mesa/main/HISTORY.md
- Hypothesis 6.168.5 wheel, `hypothesis/stateful.py` (`invariant()` docstring)
- Simon Willison, "Our AI started a cafe in Stockholm" (5 May 2026), quoting Andon. Read via the GitHub mirror https://raw.githubusercontent.com/kzinmr/ai-topics/main/wiki/raw/articles/simonwillison.net--2026-may-5-our-ai-started-a-cafe-in-stockholm--0a8c7878.md (secondary)
- A third-party capture of https://andonlabs.com/evals/vending-bench-2 (retrieved 29 Sep 2026) found in the shared workspace scratchpad. Its provenance is unverified and it was not re-fetched; it is used only for [uncertain] leads.

---

## Fact-check log

Independent adversarial fact-check, 10 Oct 2026. Primary sources were re-read from raw.githubusercontent.com, pypi.org, anthropic.com and platform.claude.com.

Some hosts were unreachable from this sandbox: arxiv.org, andonlabs.com, metr.org, the-decoder, wtop, dailycoffeenews, bloomberg, docs.stripe.com, thinkingmachines.ai, simonwillison.net and Semantic Scholar. The web-search budget was also exhausted, and no reader or proxy services were used. As a result, most [S] claims stay [uncertain].

Each row below is a claim group; rows that bundle several sub-claims are counted once.

| # | Claim | Verdict | Source | Note |
|---|---|---|---|---|
| 1 | Prosus: Apache-2.0; MCP streamable-http; 22 tools; 6 machines / 72 slots | Verified | Prosus README, task.toml, instruction.md | 21 tools in `[clock.tool_minutes]` plus `wait_for_next_day` = 22 |
| 2 | Prosus quotes: "Every call advances simulated time"; "Calls are serialized, even if submitted in parallel" | Verified | README; instruction.md | |
| 3 | Prosus: 5 min for reads, prices and notes; 25 min for orders, email and search | **Corrected** | config.toml `[clock.tool_minutes]` | Inventory, storage and sales reports and `check_offers` are 25 min; default is 25. Fixed in §2.1 and the catalogue |
| 4 | Prosus: 30 min swap, 45 min restock, 09:00–17:00 day | Verified | config.toml | `clear_slot` is also 30 |
| 5 | Prosus commitment rules (pay on order, no preview or cancellation, email with quantities purchases, `CMP-` refunds) | Verified | instruction.md | |
| 6 | Prosus anti-gaming: impact clamp 4.0, duplicate slots share demand, copy has no effect, cross-channel fatigue 0.12–0.20 | Verified | config.toml `[demand]`, `[marketing]`; instruction.md | The clamp is on the sales-impact factor |
| 7 | Prosus scoring: balance floored at 0, unfinished or bankrupt = 0, inventory excluded, API spend separate | Verified | README; engine.py `score()` | |
| 8 | Prosus reference bot ≈ €3.2k / 30 d and €61.2k / 365 d, 5 seeds | Verified | README (€3,227.89; €61,218.52) | Bot has privileged catalogue knowledge (note added) |
| 9 | Harbor agent timeout 43,200 s, 2 CPU / 4 GB; "$5 API-equivalent" budget | Verified | task.toml; README | The $5 cap pairs with a 1,800 s limit in `run_models.py` |
| 10 | `VENDING_STATE_PATH` / `VENDING_RESUME` | Verified | docker-compose.yaml; config.toml | |
| 11 | Verifier: finalize, rewrite reward on every path, NaN/inf → 0 | Verified (nuance) | test.sh | `reward.txt` is zeroed *before* finalize; ordering clarified |
| 12 | Supplier and negotiation numbers (markup 1.3–3.4×, pace 0.30–0.75, 5 rounds; aijnek 6; delivery 2–12 d; delay 0.05–0.35; short-ship 45–75%) | Verified | config.toml `[[suppliers]]`, `[negotiation]`; aijnek README | |
| 13 | Complaints 0.035/day scaled by volume; sales report 14 / 120 days; 400-day log | Verified | config.toml | |
| 14 | Day-of-week multipliers Sat 0.30, Sun 0.25 | Verified (flagged) | config.toml | Office-building values; flagged as wrong for a café |
| 15 | "deterministic seeds; live model sampling can still vary" | Verified | README | |
| 16 | Prosus training-exclusion request | Verified | README | |
| 17 | OQ11: can `main` reach `/verifier/finalize`? | Resolved | server.py; engine.py | Same port as `/mcp`, no auth; an early call seals the run and scores 0 |
| 18 | aijnek: 14 tools, 8k-token history, $100/M output weekly, Haiku with engine-set prices, days×60 steps, 180 s, no licence | Verified | aijnek README; repo (no LICENSE file) | |
| 19 | aijnek: "only `wait_for_next_day` advances time" | **Corrected** | tools/api.py, tools/schema.py | Every call costs 5/25/75 min. Fixed in §2.1 and §2.3 |
| 20 | In-game token charge is aijnek's design (implied) | Uncertain | aijnek README ("VB2-style"); third-party VB2 capture | Probably Andon VB2's rule; annotated |
| 21 | open-vending-bench incomplete | Verified | README ("STILL IN PROGRESS") | |
| 22 | YC-Bench: SQLite DES, `sim resume`, arbitrarily many actions, JSON, 20 turns plus scratchpad | Verified | YC-Bench README | |
| 23 | YC-Bench: 47% of bankruptcies from adversarial clients; scratchpad "the strongest predictor of success" | Verified | docs/index.html | |
| 24 | YC-Bench MIT | Verified (note) | pyproject.toml, README badge | No LICENSE file in repo root |
| 25 | E-Commerce Bench: 18 tools, `context_manager/`, logs, 9-day escrow, 152/576 fraudulent, seeded kernel, LLM renders only, Apache-2.0, `BadSpend%` | Verified | E-CommerceBench README, LICENSE | |
| 26 | TheAgentCompany: GitLab/Plane/ownCloud/RocketChat, pre-baked data, 30+ GB, MIT | Verified | README; LICENSE | |
| 27 | AppWorld: 9 apps, 457 APIs, 100+ tables, state-based grading, encrypted `.bundle`, canary | Verified | README | README says "database tables" and does not say "SQLite" |
| 28 | Mailpit MIT; Odoo LGPLv3 | Verified | LICENSE files | |
| 29 | Stripe test clocks only move forward | Uncertain | — | docs.stripe.com unreachable |
| 30 | SimPy 4.1.2, MIT, May 2026, real-time quote | Verified | PyPI (24 May 2026) | |
| 31 | Mesa 3.5 added a monotonic-time check | **Corrected** | Mesa HISTORY.md | That check (#3343) is in 4.0.0a0 |
| 32 | Mesa 3.5 `mesa.time`, `schedule_event`, `run_until`; 4.0a removed `DEVSimulator`; 3.5.1, Apache-2.0; 4.0 in alpha | Verified | HISTORY.md; PyPI | |
| 33 | Inspect compaction: 5 strategies, 0.9 default, `memory()` to `/memories`, history retained | Verified | docs/compaction.qmd | |
| 34 | Claude compaction beta `compact-2026-09-04` | Verified (nuance) | platform.claude.com compaction | Header for on-demand compaction; threshold compaction has its own |
| 35 | `clear_tool_uses_20250919` (100k trigger, keep 3), `memory_20250818`, cache invalidation, `clear_at_least` | Verified | platform.claude.com context-editing | |
| 36 | Context-engineering post (29 Sep 2025): Pokémon notes over thousands of steps; sub-agents return distilled summaries | Verified | anthropic.com | |
| 37 | Harnesses post quote "less likely to … improperly alter" | **Corrected** | anthropic.com (26 Nov 2025) | Actual: "less likely to inappropriately change or overwrite JSON files compared to Markdown files" |
| 38 | Inspect checkpointing (turn boundaries, no in-memory state, restores sandbox and store) | Verified | docs/checkpointing.qmd | |
| 39 | Opus 5.5: $4 in, $0.20 hit, $5 5-min write, $20 out; Fable 5.1 $10/$50; Batch 50% | Verified | platform.claude.com pricing | |
| 40 | Uncached VB2-scale run ≈ $380 | Verified | Arithmetic | 80×4 + 3×20 = $380 |
| 41 | 90%-cache run ≈ $120 | **Corrected** | Arithmetic | $106–114 |
| 42 | Fable 5.1 ≈ 2.5× more | Verified (nuance) | Arithmetic | 2.5× uncached; ≈2.35× at 90% hits |
| 43 | Summary: "$50–$400 per run" | **Corrected** | Arithmetic | ≈$75–460 for 60–100M tokens |
| 44 | VB1 run took 5–10 h | Uncertain | — | the-decoder unreachable |
| 45 | batch_invariant_ops: 18 unique of 1,000; MIT | Verified | README; LICENSE | |
| 46 | Inspect cache keys; 1-week expiry | Verified | docs/caching.qmd | Keys also include base URL and `tool_choice` |
| 47 | Anthropic stats post: paired differences, clustered SEs, power analysis | Verified | anthropic.com (19 Nov 2024) | |
| 48 | Inspect `network_mode: none` default; custom compose "replaces" it; host tools unaffected; `exec()` silent truncation | Verified | docs/sandboxing.qmd | |
| 49 | Demystifying evals (9 Jan 2026): clean isolation, git-history advantage, 0% pass rate usually means a broken task | Verified | anthropic.com | "0% pass@100 … most often a signal of a broken task" |
| 50 | ABC items II.4, II.5, II.8, II.9, I.I.1, III.3, III.10 | Verified | ABC.md | |
| 51 | METR: o3 call-stack answer, `__eq__` override, monkey-patching | Uncertain | — | metr.org unreachable |
| 52 | ImpossibleBench: MIT, Inspect, LLM-judge classification | Verified | README; LICENSE | |
| 53 | τ-bench do-nothing agent 38% | Verified | agentic-benchmarks README | |
| 54 | τ²-bench: v1.0.1 scores non-comparable with earlier ones | **Corrected** | tau2-bench README | Applies only to `banking_knowledge`; "Other domains are unaffected" |
| 55 | Hypothesis `@invariant()` runs "after every rule"; 6.168.5; MPL-2.0 | Verified | 6.168.5 wheel `stateful.py`; PyPI | |
| 56 | Inspect 0.3.278 MIT; limit types; `human_cli` recorded; handoff / `as_tool` | Verified | PyPI (9 Oct 2026); docs | |
| 57 | `sandbox_agent_bridge` proxy; `bridged_tools` exposed as MCP | Verified | docs/agent-bridge.qmd | |
| 58 | Harbor: Apache-2.0, TB-2.0 harness, Daytona/Modal, "thousands of environments in parallel" | Verified | Harbor README; LICENSE | Repo now presented as harbor-framework/harbor |
| 59 | OpenEnv: BSD-3, `reset/step/state`, Docker, `/mcp`, Inspect, "APIs may still change" | Verified | README; LICENSE | |
| 60 | OR-Gym 0.5.0, MIT, Sep 2022, `InvManagement-v0/v1`, `Newsvendor-v0` | Verified | PyPI; README | |
| 61 | TextArena 0.7.4, MIT, 100+ games including negotiation | Verified | PyPI; README | |
| 62 | AgentSims: MIT 2023; Python + MySQL; GUI | Verified | README; LICENSE | |
| 63 | Concordia: Apache-2.0; game master | Verified | README; LICENSE | |
| 64 | Magentic Marketplace: MIT; LLM buyer/seller simulation | Verified | README; LICENSE | |
| 65 | Gymnasium / PettingZoo MIT | Verified | PyPI | |
| 66 | τ²-bench, TheAgentCompany, ImpossibleBench, vivaria all MIT | Verified | LICENSE files | |
| 67 | Vend 1: Sonnet 3.7, ~1 month, tools, quotes, Sarah/Venmo, 31 Mar–1 Apr, below-cost sales, giveaways | Verified | anthropic.com project-vend-1 | |
| 68 | Vend 2: CRM, cost in inventory, browser, payment links, Forms, reminders, CEO with OKR tool, merch agent, 8× leniency, onion futures, imposter CEO | Verified | anthropic.com project-vend-2 (18 Dec 2025) | |
| 69 | Vend 2: "The biggest gain came from forced procedures" | **Corrected** | project-vend-2 | "Among the most impactful changes" |
| 70 | Vend 2: overnight "runaway chats" (quoted) | **Corrected** | project-vend-2 | Not verbatim; post says "dreamily chatting all night" |
| 71 | Café: 6,000 napkins; 120 eggs with no stove | Verified (secondary) | Simon Willison quoting Andon, via GitHub mirror | Still secondary |
| 72 | Mona messaged staff at midnight; Luna over-ordered candles | Uncertain | Headline URLs only | |
| 73 | Luna = Claude, Mona = Gemini; Mona wakes every ~30 min | Uncertain | — | No reachable source |
| 74 | VB1 details (30k context, three memory stores, `text-embedding-3-small`, tools, sub-agent tools, $500/$2, wholesale net worth, GPT-4o suppliers, ~2,000 msgs, >20M tokens, meltdown quote, "no clear correlation") | Uncertain | Partial: VB2 page capture; open-vending-bench README | arXiv unreachable |
| 75 | VB1 sub-agent released as an Inspect extension | Uncertain | — | No repo or package found |
| 76 | VB2: year-long, adversarial suppliers, delays, complaints; "can be gamed" / "can be jailbroken" | Uncertain (corroborated) | Third-party capture of andonlabs.com | Wording matches capture; not re-fetched |
| 77 | VB2: "improved the agent scaffolding"; 5 runs; prompt caching added | Uncertain | Capture | Capture shows "Average across runs" with no count; cost chart "without caching" |
| 78 | VB2: 3,000–6,000 msgs; 60–100M tokens | Uncertain | Capture | Capture says "tokens in output", which is ambiguous |
| 79 | Arena: 3–4 agents, transfers, cartels | Uncertain | Capture (partial) | Only shared location and trading confirmed |
| 80 | SWE-bench bash-only via mini-swe-agent; Terminal-Bench `--agent`/`--model` | Verified | mini-swe-agent README; terminal-bench README | |
| 81 | Anthropic post dates: 29 Sep 2025, 26 Nov 2025, 9 Jan 2026 | Verified | anthropic.com | |
| 82 | Tool-count range 15–25 (Prosus 22, E-Commerce 18, aijnek 14) | Verified | READMEs | |
| 83 | Inspect limits include `token`, `time`, `working`, `cost`, `turn`, `message` | Verified | docs/setting-limits.qmd | |
| F1 | Catalogue: café day-of-week multipliers (Sat 0.30, Sun 0.25) | Flag | config.toml comment ("weekends are dead") | Office values, unrealistic for a café |
| F2 | Catalogue: plain Poisson demand buckets | Flag | Modelling practice | Retail counts are overdispersed; use negative binomial or a latent daily factor |
| F3 | Catalogue: 10-unpaid-days bankruptcy for a café | Flag | Modelling | Use rent, payroll or credit-limit insolvency |
| F4 | Catalogue: restock trips charged to the agent clock for a café | Flag | Vend 1/2 and Café setups use human staff | Charge physical work to staff NPCs |
| F5 | Score: cash-only "prevents" inventory exploits | Flag | Prosus bot stops buying near the end; IAS 2 | Creates an end-of-horizon run-down incentive |

**Tally**
- Checked 83 claim groups: 62 verified (including 1 secondary-only and 1 open question resolved), 9 corrected, 12 uncertain, 0 removed.
- Also raised 5 modelling flags against the variables catalogue (F1–F5), annotated inline.
- Most consequential: Prosus time-costs misreported (4 read tools cost 25 min, not 5); aijnek also charges per-call minutes; the per-run cost range ($50–$400 → $75–$460); Prosus `/verifier/finalize` is unauthenticated on the MCP port; in-game token charging probably originates in Andon's VB2.
