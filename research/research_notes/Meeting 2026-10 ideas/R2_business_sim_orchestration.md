# R2: Business-simulation benchmarks and model-orchestration arenas

Brief for the 7 Oct 2026 meeting. Idea A: agents run unequal companies, scenarios rotated. Idea B: Design-Arena-style votes between setups (big model alone vs. small model guided by a big one).

**How to read the source tags.**
- **[P]**: primary source, read directly.
- **[P\*]**: primary text seen only through a verbatim GitHub copy or a search-engine excerpt.
- **[S]**: secondary source.

**Access.** arxiv, andonlabs, designarena, arena.ai and Semantic Scholar were blocked. No proxy services were used; prior repo notes were leads only.

## TL;DR

- **Idea A fills a gap.** Every AI business benchmark found gives all agents the same start: Vending-Bench ($500), YC-Bench ($200K), CEO-Bench ($1M), E-Commerce Bench (¥100k). None rotates unequal starts. The closest precedent is a human game: Markstrat gives firms different starting positions by default.
- **Variance is the main risk for Idea A.** Leaderboards run about 5 episodes per model, and single runs derail. Duplicate (paired) scoring is the standard fix.
- **Small model + big advisor works only under conditions.** In Anthropic's own measurements the advisor helps when the capability gap is large *and* the executor actually asks for advice. On a frontier executor the gain is about what extra reasoning effort buys. When the executor stops asking, the pairing scores *below* the executor alone.
- **No public arena compares orchestration as a controlled variable.** Design Arena ranks models and finished products. The closest precedents are Aider and Gorilla's 2024 Agent Arena. This gap is Idea B's opening.

## 1. Existing AI business and economy benchmarks

| Benchmark (date) | Setup / starts / runs | Key findings |
|---|---|---|
| **Vending-Bench 2** (Andon; board 29 Sep 2026) | One simulated year; adversarial suppliers. Identical $500 start; 5 runs per model [S, Epoch] | GPT-6 Astra $15,515 ±1,074 · Opus 5 $11,182 ±2,094 · Opus 5.5 $9,235 ±785. Andon puts a "good" strategy at about $63k. Andon admits supplier LLMs "can be jailbroken" and sales equations "can be gamed" [P\*]. In Vending-Bench 1, "even … Claude 3.5 Sonnet has runs that fail spectacularly" [P\*]. |
| **Vending-Bench Arena** | 3–4 agents share one location; trading allowed; symmetric seats; scored individually | Fable 5 started every cartel in 5 runs. In 24 extra same-model runs, cartels formed in 9/12 Fable 5 runs vs 4/12 Opus 4.8 runs [P\*]. Opus 5 proposed cartels in all 6 of its runs [S]. |
| **Project Vend 2** (Anthropic, Dec 2025) | Real shop, plus a "CEO" agent on the same model | The shop turned profitable "in spite of the CEO, rather than because of it". Enforcing procedures helped most [P]. |
| **YC-Bench** (Collinear, Apr 2026) | Agent is CEO of a startup for 1 year; deterministic simulation. $200K start; 12 models × 3 seeds | Opus 4.6 averaged $1.27M; GLM-5 $1.21M at 11× lower inference cost. Scratchpad use was the strongest predictor of success. Adversarial clients caused 47% of bankruptcies [P]. |
| **CEO-Bench** (Princeton, Jun 2026) | 500 days; agent sets pricing, marketing, R&D, sales. $1M start; one run per scenario; no confidence intervals [S] | 3 of 14 models finished above $1M. All scored below a rule-based baseline [S]. Secondary dollar figures conflict with each other. |
| **"Can LLMs Be CEOs?"** (2606.17459) | Agent allocates capital using advice from CFO/CTO/COO/CMO advisor agents; 13 scenarios | Failure modes: "single-advisor capture" and a "conservative default under ambiguity" [S]. |
| **E-Commerce Bench** (Qwen, Aug 2026) | **Deterministic** demand and supplier-negotiation kernel (the LLM only writes dialogue). ¥100k start; 5 episodes | GPT-5.6 Sol: ¥1,431k ±314k, but 18.5% of its spend went to fraudulent suppliers. GPT-5.5: ¥702k ±616k, bankrupt in 2 of 5 runs [P]. |
| **Business Arena** (Alibaba/Yale, 2026) | Shop, 15 models | 9× net-worth spread; best model trails human strategies [S]. |
| **TheAgentCompany** (CMU, 2024) | Agent is an employee; 175 tasks | Best agent about 30% [S]. |

**Multi-agent markets.**
- GPT-4 pricing agents "quickly and autonomously reach supracompetitive prices", and small wording changes in prompts change how much they collude (Fish, Gonczarowski & Shorrer) [P\*].
- Microsoft's Magentic Marketplace found strong first-proposal bias: replying fast beat replying well by "10–30x" [P\*].

**Human MBA games.**
- **Capstone (Capsim):** all firms start identical [S].
- **Markstrat:** "In most cases, each firm starts in a different situation"; instructors can configure identical starts [P\*].
- **Skill vs. luck:**
  - Gamlath (2009) found students performed consistently across rounds, i.e. "skill rather than… luck" [S].
  - Teach & Patel (2007) reported Capstone standings were settled early. A replication on 1,164 firms in 194 competitions did *not* confirm this [S].
  - So "the richest start never lost" depends on game design. Idea A should measure it.

## 2. Fair comparison when starts are unequal

- **Duplicate format (bridge).** Every table plays the same deals, and you are scored only against others who held the same cards. Matchpoints count rank; IMPs count margin [S].
  - For Idea A, each scenario is a "board". An agent's score is its result minus the mean of all agents on that scenario.
- **Seat swap / mirror.**
  - *Duplicate poker:* each pair plays the same cards from both seats. Kaggle used about 900k hands [S].
  - *AIVAT:* this control-variate method cut the standard deviation of a poker match by 85%, so it needed 44× fewer hands [P\*].
  - *Stockfish fishtest:* games are paired by opening with colours reversed and scored as pairs ("pentanomial" model). Fishtest says this saves "substantial" testing resources and estimates opening bias [P].
- **Rotation.** In a shared market, use a Latin square: each agent plays each seat once against balanced opponents. Report results with seat fixed effects.
- **Handicap-adjusted scoring.** Normalise each scenario against references: (agent − weak reference) / (strong reference − weak reference).
  - References already in use: CEO-Bench's rule-based baseline, Business Arena's human strategies.
- **Determinism.** E-Commerce Bench fixes demand and negotiation so outcome differences are "attributable to the agent" [P].
- **How many runs (illustrative arithmetic, α = 0.05, 80% power).**
  - With 5 unpaired runs, the smallest detectable difference is about 1.8 SD. Run-to-run spread in E-Commerce Bench is 40–90% of the mean.
  - To detect a 0.5 SD difference: about 63 runs per agent unpaired, about 31 paired scenarios if within-scenario correlation ρ = 0.5, and about 13 if ρ = 0.8.
  - Unequal starts *raise* ρ, so pairing is especially efficient for Idea A.
- **Statistical practice.** Anthropic recommends clustered standard errors ("over three times as large as naive"), paired differences and a power analysis [P].

## 3. Does a small model guided by a big one match the big model alone?

| Pattern | Evidence | Verdict / cost |
|---|---|---|
| **Advisor tool** (Anthropic, Apr 2026) | Sonnet 4.6 + Opus advisor: +2.7 pts on SWE-bench Multilingual vs Sonnet alone. Haiku 4.5 + Opus: 41.2% vs 19.7% on BrowseComp [P] | 11.9% cheaper per task than Sonnet alone. The launch post has no comparison with Opus alone. |
| **Anthropic cost guide** (Sep 2026) | When the executor kept asking, the advisor "closed at least half the gap"; one coding pairing "beat the stronger model outright". On GPQA, Haiku gained "a great deal", Sonnet 5 "a few points", a frontier executor "almost nothing" [P] | Opus 5.5 + Fable 5.1 advisor: +1.7 pts for about 2.1× the cost, "about what more effort does". On a chart-reading benchmark, Opus 5.5 at low effort asked for advice on 1 of 300 tasks and scored **7 pts below** Opus 5.5 alone. "If the executor asks on most of its tasks… running the advisor's model itself is the cheaper way" [P]. |
| **Orchestrator / workers** (same guide) | Fable 5.1 lead + 25 Sonnet 5 workers on a 21.6M-token corpus | About half the cost but 10–12 pts lower. On full BrowseComp, Fable 5 alone matched the coordinator at 22–30% lower cost [P]. |
| **Multi-agent research system** (Jun 2025) | Opus 4 lead + Sonnet 4 subagents scored 90.2% higher than Opus 4 alone | Used about 15× the tokens of a chat; token usage alone explains 80% of BrowseComp variance [P]. |
| **Aider architect/editor** | o1-preview + DeepSeek: 85.0% vs o1-preview alone 79.7%. R1 + Sonnet 3.5: 64.0% at $13 vs o1: 61.7% at $186. But o3-high + GPT-4.1: 78.2% vs o3-high alone 81.3% [P] | Mixed; usually cheaper |
| **Mixture-of-Agents** | Open models combined: 65.1% vs GPT-4o 57.5% on AlpacaEval 2 [P]. Self-MoA (one strong model sampled several times) beat the mixed version by 6.6 pts [S] | Mixing in weaker models hurts |
| **Routers / cascades** | RouteLLM: "costs down up to 85%… 95% GPT-4 performance" [P]. Minions: 97.9% of quality at 5.7× lower cost [S] | Close to parity, much cheaper |
| **Negative** | Kim et al., 180 configurations: multi-agent setups lose 39–70% on sequential tasks [S]. Project Vend's CEO agent; the MAST failure taxonomy [P] | Single-chain tasks favour one model |

**Leaderboards that rank *systems*.**
- Aider's leaderboard lists architect/editor pairs [P].
- Gorilla/LMSYS Agent Arena (2024) ranks model + framework + tools combinations and rates each component separately [S].
- arena.ai's Agent Arena added cost per task and a Pareto view in Aug 2026 [S].
- HAL runs cost-aware agent evals; its leaderboard is paused [P].
- None varies orchestration as a controlled factor under crowd votes.

**Check on the team's example.** Sonnet 5.5 as executor with Opus 5 as advisor is a supported pairing [P].
- List prices per million input/output tokens: Opus 5.5 $4/$20, Opus 5 $5/$25, Sonnet 5.5 $2/$10 [P].
- So the advisor costs *more* than the one-shot baseline, and Opus 5.5 is only 2× Sonnet 5.5.
- Anthropic says advisors pay "best when the advisor's model is priced well above the executor's". Expect any cost advantage to be thin.

## 4. Design Arena

- **What it is.** A crowdsourced, YC-backed benchmark of AI-generated design, run by Arcada Labs, which raised $7.9M [S].
  - Categories: web, UI, games, 3D, SVG, image, video, audio.
  - Claims "millions of votes" from 190+ countries [S].
- **How it scores** [P\*, methodology page]:
  - 4 hidden models answer the same prompt.
  - A 5-battle bracket produces a full 1st–4th ranking.
  - Votes are fitted with Bradley–Terry, converted as rating = 400·log10(strength).
- **Does it compare pipelines?** Only opaque products.
  - A Builder arena ranks v0, Bolt and Lovable.
  - An Agent Arena (since Oct 2025) ranks Cursor Agent (Auto), Devin, Jules and Factory Droids [S].
  - None of these are controlled model combinations.
- **Caveats** [S]:
  - It measures user preference from a technical user base, and vendors can tune prompts to it.
  - "The Leaderboard Illusion" documents private variant testing on Chatbot Arena (27 private Meta variants) and unequal sampling between providers.

## 5. Talking points

### Idea A: unequal-start company simulation

1. **Novelty.** No AI business benchmark rotates unequal starts. Ours would measure *skill relative to position*.
2. **Score value added, not money.** Use duplicate scoring (result minus the scenario mean), a matchpoint-style rank, and normalisation against reference policies. A rich start then cannot "win" on its own.
3. **Calibrate before running LLMs.**
   - Sweep scripted policies (random, all-in on marketing, all-in on R&D, balanced) across scenarios.
   - Confirm a good policy from a poor start can beat a bad policy from a rich one.
   - Publish a variance decomposition (scenario vs. agent vs. agent×scenario). If the scenario dominates, we are measuring the dealer, not the player.
4. **Two formats.**
   - *Solo duplicate:* each agent plays its own copy with the same seed. Clean and cheap.
   - *Shared market with Latin-square seats:* richer, but agents will collude. Report conduct telemetry next to profit.
5. **Credibility.** Deterministic demand and negotiation (no counterparty to jailbreak), a frozen harness, logged cost, pre-registered hypotheses, and 15–30 paired scenarios per comparison rather than the field-norm 5 runs.
6. **Behaviour worth reporting.** Does the R&D vs. marketing split adapt to position? Do underdogs take more risk, or show CEO-Bench's "conservative default under ambiguity"?
7. **Why users care.** It answers "which model should I trust with a budget *from my position* (startup vs. incumbent)?", and whether a model is robust across positions rather than strong only in its best case.

### Idea B: arena of setups, including models working together

1. **The answer is genuinely open.**
   - Advisors close half or more of the capability gap when the executor consults.
   - On frontier executors they buy about what extra effort buys.
   - When consulting collapses, they hurt.
2. **Remove the confound.** "One-shot vs. long process" mixes orchestration with compute; token usage alone explained 80% of research-task variance.
   - Run a factorial design: {Sonnet 5.5, Opus 5.5} × {one-shot, iterative} × {no advisor, Opus 5 advisor}.
   - Add Opus 5.5 at low, medium and high effort. Anthropic says the advisor model alone at low effort is "the baseline to beat."
3. **Show the bill.** Display cost and latency per output, and rank setups on a quality × cost Pareto chart for each category.
4. **Attribute effects.** Fit Bradley–Terry with additive terms for executor, advisor and process, as Gorilla's arena did. "Advisor uplift" then becomes a published number with a confidence interval.
5. **Instrument the interaction.** Log consult rate, advice tokens, and whether the advice was followed. Gains track consult rate, and this is the "models interacting" angle no other arena offers.
6. **Credibility.**
   - The same prompt goes to every setup, so comparisons are paired.
   - Outputs are blind and randomised; use style control.
   - Fixed budgets; configs and logs are published.
   - No private variant testing; bootstrap confidence intervals.
   - Votes needed: about 200 per pair to detect 60/40, about 800 for 55/45.
7. **Why users care.** It answers "which setup for my task and budget?" with per-category Pareto winners, and should report negative results too.
8. **Bridge between A and B.** Enter orchestrated setups (for example, a Sonnet executor with an Opus advisor acting as CEO) into Idea A's simulation. Anthropic says long-horizon agentic work is where advisors fit.

## Sources

**[P]**
- claude.com/blog/the-advisor-strategy
- platform.claude.com/docs: advisor-tool; optimizing-for-cost-and-intelligence; pricing
- anthropic.com: engineering/multi-agent-research-system; research/project-vend-2; research/statistical-approach-to-model-evals
- GitHub:
  - collinear-ai/yc-bench (README, docs/index.html)
  - QwenLM/E-CommerceBench
  - Aider-AI/aider (architect post; polyglot_leaderboard.yml)
  - togethercomputer/MoA
  - lm-sys/RouteLLM
  - multi-agent-systems-failure-taxonomy/MAST
  - princeton-pli/hal-harness
  - official-stockfish/fishtest wiki (Fishtest-Mathematics)
  - TheAgentCompany/TheAgentCompany

**[P\*]**
- Vending-Bench 2 page capture (29 Sep 2026): github.com/fstandhartinger/model-market-comparison
- Andon Labs Fable 5 post (copy): github.com/kzinmr/ai-topics
- Vending-Bench 1: arXiv 2502.15840
- Fish, Gonczarowski & Shorrer: arXiv 2404.00806
- Magentic Marketplace: Microsoft Research, 2025
- AIVAT: AAAI 2018
- StratX Markstrat handbook
- notes.designarena.ai/methodology

**[S]**
- epoch.ai (Vending-Bench 2)
- shellypalmer.com (Opus 5 in the Arena)
- the-decoder.com, arXiv 2606.18543 (CEO-Bench)
- arXiv 2606.17459 ("Can LLMs Be CEOs?")
- arXiv 2608.08621 (Business Arena)
- rit.edu (Capsim)
- Gamlath 2009, doi 10.1108/10748120910998416
- ABSEL Teach & Patel replication
- Cornell bridge-scoring note; pokerlistings.com (Kaggle poker)
- arXiv 2502.00674 (Self-MoA)
- arXiv 2512.08296 (Kim et al.)
- docker.com (Minions)
- news.lmarena.ai/agent-arena
- alphasignal.ai (arena.ai Pareto view)
- Design Arena: ycombinator.com, remio.ai, designarena.ai/changelog
- arXiv 2504.20879 (The Leaderboard Illusion)
