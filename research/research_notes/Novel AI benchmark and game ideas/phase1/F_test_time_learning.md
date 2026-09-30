# Panel F: Test-time learning of new systems, and procedural generators vs training on them (as of 30 Sep 2026)

**How this was verified.** The egress proxy blocked arxiv.org, arcprize.org, huggingface.co, openreview.net, kaggle.com and most blogs. Only raw.githubusercontent.com and anthropic.com were reachable. The web-search quota ran out after about 40 queries. Each claim is therefore tagged:

- **[P]** Primary source fetched in full: an official GitHub README or doc, or the ARC docs repo.
- **[P-m]** A verbatim mirror or capture of a primary page, hosted on GitHub.
- **[S]** A search-engine excerpt of a primary page that could not be fetched. At most medium confidence.
- **[Sec]** A secondary or aggregator source.

Confidence is H, M or L. Speculation is marked [speculation] and inferences [I].

**Fact-check pass (30 Sep 2026).** An independent check re-fetched every cited raw.githubusercontent.com source and ran web searches for the [S] claims; arcprize.org and arxiv.org were still blocked. Inline marks are "[corrected by fact-check …]", "[uncertain: …]" and "[added by fact-check]". See the log at the end.

---

## 1. Summary

- **Every "learn a new closed system" benchmark with a public format has fallen fast once labs targeted it. "Novel instances of a known family" is not durable.**
  - **ARC-AGI-3** (interactive; learn the game by playing) went from **under 1%** for every frontier model at the 25 Mar 2026 launch (best about 0.37%, Gemini 3.1 Pro Preview) [S], to 7.78% (GPT-5.6 Sol, the best leaderboard score before Opus 5), to 30.16% (Claude Opus 5, released 24 Jul 2026, per its system card), to **99.9%** on the semi-private set with GPT-6 Astra on 3 Sep 2026. That is about 5 months after launch. [corrected by fact-check: was "went from a best of 7.78% (GPT-5.6 Sol)", which reads as the starting point; 7.78% was the pre-Opus-5 leaderboard best, and the launch-time best was below 1%; sources: ARC-AGI-3 paper arXiv 2603.24621 (digest) and arcprize.org/blog/arc-agi-3-launch via search excerpts; anthropic.com/news/claude-opus-5]
  - The 99.9% (Astra, high effort) needed a harness that keeps reasoning state between calls; ARC's standard harness gives 62.7% (Astra, max effort). At the same (max) effort the two harnesses give 62.7% vs 98.6% [P-m][P].
  - Astra (max effort, Provider Adapter harness) used fewer actions than the median human on 96.0% of levels [P-m].
- **ARC itself says its static sets were "overfit" at the family level.** Its report says this is happening to ARC-AGI-1 and ARC-AGI-2 "accidentally or intentionally". The cause is IID public and private sets plus heavy public-data training. Evidence: Gemini 3 Deep Think used ARC colour mappings that the harness never mentioned [P-m, ARC Prize 2025 report, Jan 2026]. ARC adds that it "cannot determine which" (accident or intent) and "cannot precisely quantify the magnitude of this effect". "At the family level" is this dossier's gloss, not ARC's wording.
- **Fresh human-made items are contamination-proof but not difficulty-proof.** On unseen IOL 2026 problems, Claude Opus 4.8 got a jury score equal to a gold medal (79.5/100 against a 70.0 gold threshold), which would have placed 4th of 255 human contestants (Aug 2026) [S].
- **Per-run randomised semantics (obfuscation, symbol remapping) removes memorisation, not the reasoning advance.**
  - Mystery Blocksworld: every LLM scored about 0%. Then o1-preview scored 52.8%, and 37.3% on fully randomised names (Sep 2024) [P].
  - LingOly-TOO: obfuscation cuts frontier scores by about 0.1, yet leaderboard scores keep rising [S/Sec].
- **What still looks hard in 2026 is novel *skills*: new primitives, rare formal systems, genuine experiments, expert-authored new knowledge.**
  - **EsoLang-Bench:** best 11.2% on one language and about 3.8% overall, against 100% on the same problems in Python (Mar–May 2026) [P].
  - **CL-bench:** best 23.7% (Feb 2026); CL-bench Life best 22.2% (Apr 2026) [S]. [uncertain: not verified — no CL-bench results for Jul–Sep 2026 models (Opus 5, GPT-6 Astra) were found, so "still ~23%" may be stale]
  - **ZendoWorld:** humans win 73.3% of games against 44.5% for vision-language model (VLM) agents (Jul 2026) [S].
  - **Witness:** reinforcement learning (RL) on hidden-rule games moved a 27B open model (Qwen3.8-27B) from only 2.1 to 5.4 RHAE-L5 on a private test (Sep 2026) [S]. Frontier context: the best of 18 frontier models solves only 24% of private-test level slots, and Opus 5 scores 59.9 RHAE-L5 on validation (97.8 when given the ground-truth rules), so rule *acquisition* is the bottleneck [S]. [context added by fact-check; source: arXiv 2609.32208 via search excerpts]
  - Most of these are months old and have been tested on few frontier models. Their durability is unproven.
- **Public generators become training corpora within months.**
  - Reasoning Gym (100+ generators), Enigmata (36 tasks), SynLogic (35) and InternBootcamp are built for reinforcement learning with verifiable rewards (RLVR) [P].
  - NewtonBench, an ICLR 2026 benchmark, was integrated into NVIDIA NeMo Gym as an RL environment on 26 Feb 2026, about 4.5 months after its arXiv release [P].
- **RL on procedural families transfers somewhat across nearby families. Transfer to new primitives is mixed: near zero for "qualitatively new" dynamics (RL Grokking), small but positive on Witness's held-out primitives.** [corrected by fact-check: was "but weakly to new primitives"]
  - Reasoning Gym reports cross-domain gains, e.g. algorithmic training gives +29.1% on algebra [S].
  - Enigmata claims gains on ARC-AGI-1 and -2 and AIME [P, author claim].
  - "RL Grokking" finds "qualitatively new dynamics" stay near zero after RL [S].
  - HardcoreLogic shows large drops on long-tail rule variants of familiar puzzles, even for GPT-5 [S].
  - Mixed evidence: in Witness, RL on WitnessGym raised validation scores on *both* held-out compositions and held-out primitives, plus a mean +4.1 on four external discovery benchmarks. The authors read this as RL transfer to new rules; the absolute private-test gain was small (2.1 → 5.4) [S]. [corrected by fact-check: "weakly to new primitives" was stated without this counter-evidence; source: arXiv 2609.32208 via search excerpts]
- **How the novelty designs were beaten, as a recurring recipe [I]:**
  1. Training on the task family: its data and generators, or RL environments.
  2. Refinement loops at test time: test-time training, or program search with a verifier. Examples are ARC Prize 2024 test-time training (TTT) and the Poetiq harness (31% → 54% on ARC-AGI-2).
  3. Compiling the environment into code: code world models (e.g. the community "Tycho" agent's executable world model on the ARC-AGI-3 public set), and Astra writing `maze_solver.py` in the separate PRO-LONG sandbox harness. [corrected by fact-check: Astra's scored 62.7%/99.9% runs used no code execution; ARC says it kept compact symbolic notes, "not a complete programming language". The solver files come from a separate PRO-LONG evaluation that ARC says reflects "model plus tools". Source: arcprize.org/blog/astra (translation mirror)]
  4. Persistent reasoning state and memory: the ARC-AGI-3 Provider Adapter harness.
- **Action-efficiency metrics do not stay discriminative.** ARC expected that AI would need many more actions even after solving an environment. Instead, frontier AI is "binary": once it understands the mechanics, it executes within the human range [P-m]. Per-level efficiency caps (1.15×) limit the metric's upside [P].
- **Harness dependence is now the largest source of variance on test-time-learning benchmarks.** It was 62.7% vs 99.9% for the same model (max vs high effort), or 62.7% vs 98.6% at the same max effort [P-m]. EsoLang-Bench's self-scaffolding with interpreter feedback is its best regime [P]. [I] Any new design must fix or report the harness.
- **Human baselines are best in the ARC series:**
  - 458 first-run participants in 90-minute sessions; every environment beaten by at least two people; the per-level baseline is the upper median of human action counts [P-m][P].
  - Olympiad jury grading (IOL-AI) [S].
  - Most other benchmarks (gg-bench, EsoLang, KOR, CL-bench, Reasoning Gym) have no human baseline [P, I].

---

## 2. Benchmarks that require learning a new system at test time

### Takeaway

Benchmarks built on a closed, rule-bounded world (ARC-AGI-3, Blocksworld variants, olympiad puzzles, MTOB en→kgv) reached or approached human parity within about 5–24 months of being targeted. Mastering a new formal system or new knowledge from supplied material is still largely unsaturated (EsoLang-Bench, CL-bench, active rule-discovery environments). But those benchmarks are mostly 2025–2026 vintage and have limited frontier coverage.

### Cited findings: per-benchmark entries

Each entry gives the task, AI vs human results, the trend, and what beat it (if beaten).

**ARC-AGI-3 (ARC Prize Foundation; launched 25 Mar 2026 [S])**
- **Task.** Turn-based game environments "with no instructions, rules, or stated goals". Agents must explore, infer mechanics and goals, and carry learning across levels [P-m, Opus 5 card §8.14.2]. [corrected by fact-check: quote was "no instructions, no rules, and no stated goals"; verbatim wording restored from the system-card mirror]
- **Scoring (RHAE, Relative Human Action Efficiency)** [P, ARC docs]:
  - Per level: (human_baseline_actions / ai_actions)², capped at 1.15.
  - A game score is the level-index-weighted average; completing only the first 4 of 5 levels caps it at 66.7%. The total is the mean over games.
  - Only actions that change the environment count. Tool calls, reasoning and retries do not.
  - Changed 14 Apr 2026: the baseline moved from the 2nd-best human to the median, and the cap from 1.0 to 1.15 [P changelog].
- **AI results:**
  - At launch (25 Mar 2026) every frontier model scored below 1%: Gemini 3.1 Pro Preview 0.37%, GPT-5.4 0.26%, Opus 4.6 0.25%, Grok 4.20 0% [S, arcprize.org/blog/arc-agi-3-launch and arXiv 2603.24621 via search excerpts]. [added by fact-check; resolves the "7.78% vs <1%" conflict with dossiers A and E]
  - Opus 5 (high): 30.16%, "roughly four times the best previously reported score on the official leaderboard". GPT-5.6 Sol (max): 7.78%. Opus 4.8: 1.52% [P-m, Opus 5 system card; Opus 5 released 24 Jul 2026 per anthropic.com/news/claude-opus-5].
  - GPT-6 Astra, semi-private, 3 Sep 2026: **62.7%** on the Standard harness (max, $26,098) and **99.9%** on the Provider Adapter harness (high, $18,817). At max effort the Provider Adapter gave 98.6% ($17,332) [P-m ARC blog translation; S arcprize.org/blog/astra].
  - Community leaderboard: the "Tycho" agent scored 100.0% on the *public demo* set (29 Jul 2026). Public-set scores there are self-reported [S].
  - Kaggle Milestone #1 (30 Jun 2026) was won by Tufa Labs' "The Duck", a small open LLM (Qwen 3.6 27B FP8) writing Python in a REPL; its score was not captured [S; P duck-harness README for the tool-using design].
- **Human results.** 100% of environments were solved by at least two first-run humans (details in §2 Human baselines below) [P-m].
- **What beat it:**
  - *Persistent opaque reasoning state and compaction.* The Standard harness keeps "visible notes"; the Provider Adapter keeps "native conversation and reasoning state" [P arc-agi-3-benchmarking README].
  - *Compressing the environment into a symbolic world model.* ARC's summary says Astra's key behaviour was to compress unfamiliar environments into compact symbolic world models, write game mechanics as logical rules, and invent DSL shorthand to track state and plan [P-m; paraphrase back-translated from the Chinese mirror, so not verbatim English]. ARC calls this "on-the-fly algebraic shorthand", not a full programming language.
  - *Tool building.* With a sandbox (PRO-LONG harness) it built per-game solvers (`maze_solver.py`, `combat_solver.py`, `patrol_solver.py`) [P-m]. This was a separate evaluation, not the scored 62.7%/99.9% runs. ARC says it measures model plus tools, since human testers had no code interpreter.
- **ARC's own caveat (paraphrase):** scope and format are tightly bounded; environment mechanics and goals are deterministic and closed; it does not represent real-world complexity [P-m; back-translated, not verbatim].
- **Confidence.** H for the scores (primary text via mirror, consistent with search excerpts); M–H for the launch date and launch-time scores (several consistent search excerpts of arcprize.org and the ARC-AGI-3 paper).

**ARC-AGI-1 and ARC-AGI-2 (static few-shot grid rule induction). Included for how they were beaten.**
- **ARC-AGI-1, ARC Prize 2024:**
  - Private-set state of the art (SOTA) went from 33% to 55.5% (MindsAI, not open-sourced) [S, ARC 2024 report].
  - TTT, the approach of Akyürek et al., scored 47.5% on the semi-private set [P-m, ARC Prize 2024 report mirror; was S].
  - re-ARC supplies procedural generators for all 400 ARC-1 training tasks, with 1,000 verified examples per task [P].
- **ARC-AGI-2** [P, ARC-AGI-2 readme]:
  - Average human test-taker scored 66% on the public eval.
  - Each eval task was solved by ≥2 people in ≤2 attempts [S, arcprize.org/arc-agi/2]. [corrected by fact-check: tagged as from the readme, which does not contain it; the claim itself is confirmed by ARC's site via search excerpts]
- **ARC Prize 2025 (Jan 2026 report)** [P-m]:
  - The top Kaggle score was 24%.
  - The Poetiq refinement harness raised Gemini 3 Pro from 31% ($0.81/task) to 54% ($31/task).
- **2026 frontier claims:**
  - Gemini 3 Deep Think 84.6% at $13.62/task (Feb 2026), verified by ARC Prize per its X post [S/Sec, M].
  - [uncertain: not verified — sibling dossier A reports GPT-6 Astra at 95.0% ($1.12/task, Sep 2026) from an ARC Prize X post and arcprize.org/results; arcprize.org was unreachable]
- **What beat it.** ARC names two causes: refinement loops, and "knowledge overfitting" when the "public training and private test sets are too similar (e.g., IID) and the model has been trained on substantial public domain data" [P-m].

**MTOB, Machine Translation from One Book (Kalamang; Sep 2023; ICLR 2024)**
- **Task.** Translate English↔Kalamang (fewer than 200 speakers) from a grammar of about 500 pages, a wordlist and about 400 parallel sentences. The data ships encrypted, with the BIG-bench canary [P].
- **Results over time:**
  - 2023 baseline: 44.7 chrF (kgv→en) and 45.8 (en→kgv), against 51.6 and 57.0 for a human who learned from the same materials [P].
  - Gemini 1.5 Pro (Feb–Mar 2024): 58.3 chrF en→kgv, reported as above the 57.0 human score [S].
  - Llama 4 Maverick (Apr 2025), filed under "Long Context" [P]:
    - half book: 54.0 / 46.4 chrF (en→kgv / kgv→en);
    - full book: 50.8 / 46.7;
    - both below the human scores.
- **Trend.** Human parity in one direction within about 5 months, with long context as the driver. It has since become a long-context line item, not a learning benchmark [P, I].
- **Validity problem.** Aycock et al. (arXiv 2409.19151; ICLR 2025) report that almost all gains come from the book's parallel examples, not its grammar explanations [S]. [I] "Learning a language" collapsed into retrieval over examples.
- **Successors:**
  - ConlangBench (Aug 2026) covers 21 constructed languages with 21M parallel pairs. Fine-tuned models "can learn all eight conlangs" that have enough parallel data. It is a training and evaluation resource, not a test of learning in context [S].
  - No MTOB-style successor with a fresh, unpublished language was found (Gap).

**Linguistics-olympiad "Rosetta stone" puzzles**
- **LingOly (Jun 2024).**
  - 1,133 UKLO problems in 90+ mostly low-resource languages. On the *harder* problems the best model (Claude 3 Opus) scored 38.7%, 24.7 points above its no-context baseline [S]. [corrected by fact-check: was "the best model scored 38.7% exact match" with no difficulty qualifier; the paper abstract gives 38.7% for harder problems; source: arXiv 2406.06196 / NeurIPS 2024 via search excerpts] [uncertain: not verified — "average exact match 21.7%" not found in excerpts]
  - Data is in a password zip [P].
  - There is a no-context control for memorisation [P].
- **LingOly-TOO (Mar 2025; later revisions).**
  - Obfuscated versions of 82 UKLO problems, giving 6,995 question-answer pairs (paper v3) [S]. [corrected by fact-check: was "over 1,200 QA pairs"; source: arXiv 2503.02972v3 via search excerpt] [uncertain: not verified — "up to 6 obfuscations per problem"]
  - Paper v3: Claude 3.7 Sonnet 0.43 obfuscated, o1-preview 0.32, o3-mini 0.31 [S].
  - Leaderboard snapshot: GPT-5 0.467 and Claude Opus 4.1 0.458 obfuscated [Sec, benchmarklist]. Best reasoning models dropped from about 0.59 to 0.48 [S].
  - Auditors confirmed solvability. Obfuscation causes a small drop in human performance: about 5.7% for humans vs about 12.8% on average for models [S].
- **Linguini (Meta, Sep 2024).** Password-protected to avoid crawling [P]. Scores not verified (Gap).
- **modeLing.** Not verified (Gap).
- **"Could language models win the International Linguistics Olympiad?" (CoNLL 2026).**
  - A domain-specific inference-time scaling framework adds 4.9 pp (DeepSeek-R1), 13.1 pp (Gemini 2.5 Flash) and 4.9 pp (Llama 3.3 70B) [S].
  - The repo ships obfuscated splits behind a password zip; revised 26 Aug 2026 [P].
- **IOL-AI Challenge (arXiv 2608.18011, Aug 2026)** [S]:
  - Run on the *unseen* IOL 2026 Individual Contest problems.
  - Automatic scoring, plus grading by the official IOL jury under human rubrics.
  - 731 submissions from 46 teams, under a 1×T4, 30-minute budget. The two compute-limited systems sent for jury grading scored in the bottom 5% of contestants.
  - Claude Opus 4.8, evaluated outside that compute budget, scored the equivalent of a gold medal (79.5 vs a 70.0 gold threshold), which would have ranked 4th of 255 humans.
- **Trend.** Fresh human-authored puzzles (the IOL cadence) are now at gold-medal level for frontier models (Aug 2026). They remain unsaturated for compute-limited open systems.

**Invented and esoteric programming languages: EsoLang-Bench (Lossfunk; arXiv 2603.09678, Mar 2026)**
- **Task.**
  - 80 algorithmic problems in 4 tiers, written in Brainfuck, Befunge-98, Whitespace, Unlambda and Shakespeare.
  - 6 hidden I/O tests per problem.
  - Language docs are in the prompt; iterative regimes get up to 5 attempts with interpreter feedback [P].
- **Results (README, fetched 30 Sep 2026; GitHub counts "verified May 2026")** [P]:
  - Peak 11.2% (GPT-5.4 xhigh, self-scaffolding, Befunge-98), about 3.8% overall.
  - Other best overall scores: o4-mini-high about 3.4%, Gemini 3.1 Pro about 2.6%. Whitespace peaks at 0%.
  - The same problems in Python or JavaScript reach 100%.
  - Few-shot adds only 0.8 pp over zero-shot (Wilcoxon p=0.505).
- **Trend.** Unsaturated at release. Only one generation of frontier models has been tested.
- **Caveat [I].** These languages are rare but *public* (e.g. 2,028 GitHub repos tagged Brainfuck [P]). The benchmark measures learning a hostile syntax under tight budgets (8,192 tokens, 5 attempts). [speculation] It may fall quickly to agentic harnesses that build tooling, e.g. compilers from a friendlier language into Brainfuck, as Astra did with per-game solvers.

**KOR-Bench (knowledge-orthogonal reasoning; Oct 2024) and KORGym (May 2025; NeurIPS 2025)**
- **KOR-Bench** [P]:
  - Rules independent of prior knowledge, in five categories: Operation, Logic, Cipher, Puzzle, Counterfactual.
  - Claude-3.5-Sonnet and GPT-4o scored about 58% at release.
  - Later reasoning-model scores not verified (Gap).
- **KORGym** [S]:
  - A parameterised game platform; 19 LLMs and 8 VLMs evaluated.
  - o3-mini scored highest overall; Doubao-1.5-thinking-pro had a 0.72 mean and 0.84 on puzzles. [uncertain: not verified — the Doubao figures were not in the excerpts found]
  - The authors attribute gains to "RL-driven enhancements".

**CL-bench and CL-bench Life (Tencent Hunyuan; Feb 2026, Apr 2026)**
- **Task.** Learn new knowledge from supplied context: domain knowledge, rule systems, procedures, and empirical discovery or simulation [P].
- **Construction** [P]:
  - 500 contexts, 1,899 tasks, 31,607 rubrics. The README gives 1,899 tasks and an average of 63.2 rubrics per context; the 500 and 31,607 figures come from search excerpts [S] and agree with that average.
  - About 20 expert-hours per context.
  - Graded by a GPT-5.1 judge (low reasoning effort; high for CL-bench Life). A task counts as solved only if every rubric passes.
- **Results** [S]:
  - Frontier average 17.2%; best GPT-5.1 at 23.7% (Feb 2026).
  - CL-bench Life (405 tasks): best GPT-5.5 (High) at 22.2% (Apr 2026).
- **Trend.** Unsaturated. It is expensive to build and depends on an LLM judge.

**Learning a new game from its rules**
- **gg-bench (Berkeley; May 2025)** [P]:
  - An LLM writes descriptions of novel two-player games and implements them as Gym environments. RL agents are trained by self-play and filtered for quality. The model under test plays 30 games per environment against those agents.
  - 126 games. The authors call it "a data generating process" that can be regenerated at will.
  - Win rates: GPT-4o 8.94%, Claude 3.7 Sonnet 9.53%, o3-mini 31.08%, DeepSeek-R1 32.50%, o1 36.28%.
  - No 2026 results found (Gap).
- **Code World Models for General Game Playing (DeepMind; Oct 2025)** [S]:
  - The LLM turns natural-language rules plus trajectories into Python (`apply_action`, `get_legal_actions`, rewards, etc.) for MCTS, verified by unit tests generated from trajectories.
  - It also writes value heuristics and inference functions for hidden information.
  - Win-rate numbers not verified (Gap).
  - Follow-ups (titles only): "When a Verified World Model Still Loses" (Jul 2026) and "Distilling Game CWM Generation into Lightweight LLMs" (May 2026) [S].
- **Boardwalk (Aug 2025)** [S]:
  - LLMs code 12 anonymised board games, to avoid evoking pretrained knowledge.
  - Best: Claude 3.7 Sonnet, with 55.6% of games error-free. [uncertain: not verified — the 55.6% figure was not in the excerpts found; the 12 anonymised games and the three models tested were confirmed]
- **Trend [I].** Rule-to-code compilation (CWM) is one approach that worked on ARC-AGI-3: community public-set agents such as Tycho use executable world models, and Astra built solvers in the PRO-LONG sandbox. It was not what produced Astra's scored 99.9%, which came from symbolic notes plus preserved reasoning state. [corrected by fact-check: was "Rule-to-code compilation (CWM) is the approach that won ARC-AGI-3"; source: arcprize.org/blog/astra (translation mirror); Tycho description via arcprize.org/leaderboard/community search excerpt] Games with written rules are now largely a code-synthesis problem, and weak play (gg-bench) reflects multi-turn strategy, not rule learning.

**Counterfactual worlds (altered arithmetic bases, physics, rules)**
- **"Reasoning or Reciting?" (Wu et al.; NAACL 2024)** [S]:
  - Default vs counterfactual variants, e.g. base-10 vs base-9 arithmetic, modified chess, and more.
  - Performance often drops from near-perfect to near-zero. Chain of thought (CoT) narrows but does not close the gap. Bases 8 and 16 do better (frequency effect).
  - No 2025–26 reasoning-model re-run found (Gap).
- **PlanBench Mystery Blocksworld (obfuscated domain), leaderboard** [P]:
  - Claude 3.5 Sonnet, GPT-4o, Claude 3 Opus and GPT-4: 0%. LLaMA-3.1 405B: 0.8%.
  - o1-preview (Sep 2024): 97.8% Blocksworld, **52.8%** Mystery, **37.3%** Randomized Mystery.
  - DeepSeek-R1 (2025): 99.1 / 43.3 / 25.8.
- **NewtonBench (HKUST; arXiv Oct 2025; ICLR 2026)** [P]:
  - 324 law-discovery tasks in 12 physics domains built from "metaphysical shifts" (altered canonical laws). Agents run interactive experiments.
  - Frontier models (GPT-5, Gemini-2.5-pro) show "clear but fragile" discovery.
  - Noise of 0.0001 costs 13–15% accuracy. "Code assistance helps weaker models but hinders stronger ones".
  - **Integrated as an RL environment in NVIDIA NeMo Gym on 26 Feb 2026.**
- **HardcoreLogic (Oct 2025)** [S]:
  - More than 5,000 long-tail variants of 10 familiar puzzle games.
  - Top models, including GPT-5, "suffer significant performance degradation". Subtle rule variations hurt even without extra difficulty, "indicating heavy reliance on memorized stereotypes".

**Hidden-rule inference and scientific discovery**
- **WILT (Riot Games; Oct 2024)** [S; P for design]:
  - Wason 2-4-6 style: up to 30 test triples, then submit a lambda.
  - Best 28% (Claude 3.5 Sonnet).
- **InductionBench (Feb 2025; ACL 2025)** [S]:
  - String functions from the subregular hierarchy.
  - Even o3-mini "struggle[s]". Models get confused by more data and fail to find minimal rules.
- **Eleusis and Zendo:**
  - Hugging Face "Can LLMs Play the Game of Science?" space [S]. Scores not verified.
  - The Metta "cogame-eleusis" environment draws its hidden rule from a **68-rule public catalogue** ("a search, not a guess") [P]. [I] That rule space is small enough to enumerate.
- **ZendoWorld (Jul 2026)** [S]:
  - Visual rule induction by active experimentation.
  - Humans (19 participants) win 73.3% of games in 8.0±0.7 turns; VLM agents win 44.5%.
  - VLM agents "propose near-uninformative experiments". Humans recover complex and out-of-distribution rules "where no visual agent succeeds".
- **FalsifyBench (Jun 2026)** [S]:
  - A semantic 2-4-6 variant; 12 LLMs tested; "no model comes close to optimal".
  - Negative testing (trying to falsify) predicts success.
- **Hero's Journey (UT Austin; Jun 2026)** [S]:
  - 8 text-game rule-induction tasks, scored by efficiency-calibrated success (ECSR) and by whether the model can state the rule.
  - Procedural induction remains "an open challenge". Surface semantics matter little.
- **DiscoveryWorld (AI2; Jun 2024; NeurIPS 2024 D&B Spotlight)** [S; P for design]:
  - Human scientists averaged 66% completion and 55% knowledge on 16 normal and challenge tasks.
  - The best GPT-4o agents reached about 18% completion on normal and challenge tasks. [uncertain: not verified — the excerpt found attributes 18% to *challenge* tasks (ReAct agent, 38% on easy); the normal-task figure was not seen]
  - Seeds 0–4 are official; higher seeds are "outside of the benchmark" [P].
- **BoxingGym (2025)** [P]:
  - 10+ simulated environments for experimental design, scored with expected information gain (EIG) regret.
  - Numbers not verified.
- **AutumnBench / WorldTest (Oct 2025)** [S]:
  - 43 grid-world environments in a DSL; 129 tasks: masked-frame prediction, planning, and predicting changed dynamics.
  - A reward-free exploration phase comes before scored tests in derived environments.
  - 517 humans outperform 3 frontier models. Extra compute helps only in some environments.
- **Witness (Sep 2026)** [S]:
  - An agentic pipeline generates hidden-rule puzzle games. WitnessGym is for RL; WitnessBench has a public validation set and a *private* test set.
  - Validation is split into held-out *compositions* and held-out *primitives*.
  - RL raised Qwen3.8-27B from 2.1 to 5.4 RHAE-L5 on the private test, with validation gains on both splits and a mean +4.1 on four external discovery benchmarks.
  - Frontier baseline: under a shared harness, the best of 18 frontier models solves only 24% of private-test level slots. Opus 5 reaches 59.9 RHAE-L5 on validation, and 97.8 when given the ground-truth rules. [added by fact-check; source: arXiv 2609.32208 via search excerpts]

### Human baselines: how they are measured

- **ARC-AGI-3** [P-m, arcprize.org/blog/arc-agi-3-human-dataset, captured 29 Sep 2026; P docs]:
  - 458 members of the public, not selected for any demographic, in 90-minute sessions paid about $130 plus $5 per solved environment. (ARC's later Astra post gives $115 per session and "about 500" people tested.)
  - "First-run": each participant saw an environment once, with one attempt.
  - Humans got the same system prompt and information as the AI.
  - Every environment was beaten by at least 2 independent participants from a panel of about 10.
  - Public demo: 342 replays and 145 solves across 25 environments, open-sourced. Solve rates vary (10/10 on one, 6/12 on another).
  - The baseline is the **upper median** of human action counts per level.
  - ARC changed the baseline because of a "luck factor" in some levels and because "first place doesn't always get 100%" [P-m].
- **ARC-AGI-2** [P]:
  - Each eval task was solved by ≥2 people in ≤2 attempts; average test-taker 66%.
  - The scoring rule is 2 trials per test input, although the README also says 3 in one place.
- **Olympiads (IOL-AI)** [S]:
  - Official jury grading with human rubrics, compared with medal cut-offs.
  - The strongest baseline type [I], but only once a year.
- **MTOB** [P]. A single human learner (an author) worked from the same materials. N=1.
- **DiscoveryWorld** [S]. Human scientists with advanced degrees on 16 tasks: completion, procedure and knowledge scores.
- **ZendoWorld** [S]. 19 participants, 10 plays per game; reports win rate and turns to solve.
- **AutumnBench** [S]. 517 participants.
- **None found** for gg-bench, EsoLang-Bench, KOR-Bench, Reasoning Gym, Enigmata or HardcoreLogic. CL-bench is unverified.

### Inferences

- [I] A benchmark survives only while (a) it needs a genuinely new *primitive* or a hard-to-simulate environment, and (b) no one has turned the family into an RL environment.
  - Closed, deterministic, cheaply simulable worlds get compiled into code and searched: ARC-AGI-3, games, Blocksworld.
- [I] Measuring efficiency in actions per level has not stopped saturation. It measures post-understanding execution, where AI is already at human level. Exploration cost and hypothesis efficiency would need separate metrics, e.g. the number of experiments before the rule is correctly stated.
- [I] Olympiad-style fresh items test whether a skill *family* generalises. That family (linguistic rule induction) is now within frontier reach.

### Gaps

- The ARC-AGI-3 environment counts per split (public, semi-private, private) were not re-verified from primary sources. The launch-time frontier scores (all below 1%, best 0.37%) are now confirmed by search excerpts of arcprize.org and the ARC-AGI-3 paper, not by a full fetch. [updated by fact-check]
- The September 2026 Kaggle milestone results were not available.
- No 2026 frontier results were found for gg-bench, KOR-Bench, WILT, InductionBench, the Wu et al. counterfactual tasks, Linguini or modeLing.
- Code World Models win rates and Enigmata's ARC numbers were not verified.
- CL-bench numbers come from search excerpts; the paper and leaderboard were blocked.

---

## 3. Novel instances vs novel skills: what the evidence shows

**Definitions used here.**
- *Novel instance*: a new sample from a task family whose format and meta-skill are known. Examples: new seed, new level, new obfuscation, new month's problems, new olympiad paper.
- *Novel skill*: success needs a rule primitive, formal system or body of knowledge absent from training, and a transfer that cannot be reduced to recombining known family moves.

### Takeaway

Almost every documented defeat is a defeat of instance novelty by *family-level* learning. The model had never seen the item but had seen, or been trained on, the family. The few settings that remain hard in 2026 need new primitives, active experimentation under uncertainty, or learning of real knowledge from long expert material. None has yet faced a lab-scale push.

### Cited findings

**Instance novelty beaten by family-level learning:**
- **ARC-AGI-1 and -2.** Private tasks were unseen, yet ARC asserts "overfitting" via IID public and private sets plus public-data training. The evidence is Gemini 3 Deep Think using ARC colour conventions the harness never mentioned [P-m].
- **ARC-AGI-3 (a new family in Mar 2026).** It moved from under 1% at launch (25 Mar), to 7.78% (GPT-5.6 Sol, pre-Opus-5 leaderboard best), to 30.16% (Opus 5, 24 Jul), to 99.9% (Astra, 3 Sep, harness-dependent), within about 5 months [S][P-m]. [corrected by fact-check: was "from a single-digit best (7.78%)"; the launch-time best was below 1%; see §2]
  - [I] The family's meta-skill (explore → infer mechanics → plan in 2D grid games) proved learnable. After that, private environments are just instances.
  - A community agent reached 100% on the 25 public environments by 29 Jul 2026 (self-reported) [S].
- **Mystery and Randomized Mystery Blocksworld.** Symbol obfuscation kept LLMs at 0% until reasoning models (o1-preview: 52.8% / 37.3%) [P].
  - [I] Remapping defeats memorisation, not a planning skill once acquired.
- **Linguistic olympiads.** Fresh IOL 2026 problems reached gold level (Opus 4.8) [S]. Obfuscated LingOly-TOO scores rose from 0.43 (Claude 3.7) to 0.467 (GPT-5) [S/Sec].
- **LiveCodeBench.** Time-split fresh problems exposed contamination: DeepSeek models drop on LeetCode problems released after Aug–Sep 2023 [S]. Fresh instances still get solved as coding skill improves [I].
- **Procedural puzzle families.** Once a family is an RL corpus (Enigmata, SynLogic, Reasoning Gym), held-out *instances* within it are expected to be near-solved [I]. MastermindEval, for example, had o3-mini above 0.85 solve rate even at code length 5 with 7 colours [S].

**Skill novelty still hard (as of Sep 2026):**
- **EsoLang-Bench.** 100% in Python vs about 3.8% overall in esoteric languages for the same algorithms, and few-shot examples do not help [P]. This is the cleanest separation of an algorithmic skill already held from a new formal system that must be learned.
- **HardcoreLogic.** "Subtle rule variations that do not necessarily increase puzzle difficulty" cause failures; performance rests on "memorized stereotypes" [S].
- **"RL Grokking Recipe".** After RL, models transfer to easier and harder variants with diminishing gains, but "qualitatively new dynamics remain near zero" [S].
- **Witness.** The design explicitly separates held-out compositions from held-out primitives. RL on the generator gave a 27B open model only 2.1 → 5.4 on the private test, though with gains on both held-out splits [S]. Frontier models are much higher but not saturated: the best of 18 solves 24% of private-test level slots, and Opus 5 scores 59.9 RHAE-L5 on validation [S]. This is the only 2026 benchmark found that operationalises this study's distinction.
- **Active experimentation:**
  - ZendoWorld agents' experiments are "near-uninformative" [S].
  - FalsifyBench: success depends on negative testing, and no model is near optimal [S].
  - AutumnBench: humans are better at experimental design and belief updating [S].
  - NewtonBench: 13–15% drop at 0.0001 noise [P].
- **Learning new knowledge from supplied material.** CL-bench is at about 23%, with context ignored in many failures [S; the "55–66% ignored" figure was not re-verified].

**Contrary or complicating evidence:**
- **Transfer across families is real but modest and mostly near-domain.**
  - Reasoning Gym reports gains in held-out domains after RLVR on one domain: algorithmic training gives algebra +29.1% and geometry +22.3%; logic gives cognition +13.3%; games give algebra +21.8% [S]. (Fact-check confirmed the +29.1% and +22.3% in excerpts; +13.3% and +21.8% were not seen.)
  - Witness: RL on WitnessGym improved held-out primitives as well as held-out compositions, plus +4.1 on external discovery benchmarks [S].
  - Enigmata's 32B model "surpasses o3-mini-high and o1" on ARC-AGI-1 and -2, and puzzle data improved Seed1.5-Thinking on AIME and GPQA [P, author claim].
  - [I] So training on the generator does inflate scores on *other* reasoning benchmarks. Held-out families are not immune.
- **The strongest "novel skill" results are young.** EsoLang (Mar 2026), CL-bench (Feb 2026), ZendoWorld (Jul 2026) and Witness (Sep 2026) have each been evaluated on one model generation. ARC-AGI-3 was under 1% at launch and under 8% until Opus 5 (24 Jul 2026), then reached 99.9% about six weeks later.

### Inferences

- [I] **A working test for "novel skill" in the new benchmark's design:**
  1. Performance must not improve when the model is RL-trained on the public generator's other families. Measure this directly, as Witness does with held-out primitives.
  2. Few-shot or public exemplars must not help (the EsoLang test).
  3. Obfuscation or remapping must not change the score (the LingOly-TOO / Mystery Blocksworld test; a *drop* signals memorisation).
  4. Score should rise with the amount of genuine interaction needed, not with generic compute.
- [I] **"Novel instance" durability is set by how fast the family's meta-skill becomes an RL target.** Evidence puts this at months for high-profile families: ARC-AGI-3 about 5 months; NewtonBench to NeMo Gym about 4.5 months.
- [speculation] Designs that keep the *primitive set* secret and rotating (Witness-style held-out primitives, refreshed each season) are the most promising, but no durability data exists yet.

### Gaps

- No controlled study was found in which a lab trained on a public generator and was then evaluated on a secret generator with new primitives at frontier scale.
- The Reasoning Gym transfer numbers come from a search excerpt; the model sizes and baselines behind them were not verified.

---

## 4. Durability of novelty-generation approaches

### Takeaway

No approach has shown more than about 2 years of durability against frontier progress once the family was known. The most durable property is *contamination resistance*: private sets, fresh cadence and encryption all work for that. *Difficulty resistance* depends on whether the family's skill has been targeted.

### Cited findings (table)

| Approach | Example(s) | Evidence of durability or defeat | Confidence |
|---|---|---|---|
| Private or held-out instance sets from a public family | ARC-AGI-1/2/3 semi-private and private sets | Defeated by family-level "overfitting" when splits are IID [P-m]. ARC-AGI-2 went from 24% (open Kaggle) and 54% (refinement harness) in 2025 to 84.6% (Deep Think, Feb 2026, [Sec]). ARC-AGI-3 reached 99.9% about 5 months after launch [P-m]. | H (mechanism); M (ARC-AGI-2 2026 figure) |
| Public procedural generator (unbounded instances) | Reasoning Gym, Enigmata, SynLogic, InternBootcamp, PUZZLES, re-ARC, MastermindEval | Designed as RLVR training data [P]. They transfer to other benchmarks (+13–29% cross-domain; ARC and AIME gains claimed) [S][P]. Instances are trivially refreshed, but that does not protect the family [I]. | H (training use); M (transfer size) |
| Benchmark → RL environment pipeline | NewtonBench → NVIDIA NeMo Gym (Feb 2026); CL-bench packaged by Prime Intellect [lead, not re-verified] | NewtonBench became an RL environment about 4.5 months after arXiv [P]. | H (NewtonBench) |
| Per-run randomised semantics (symbol remap, obfuscation) | Mystery / Randomized Mystery Blocksworld; LingOly-TOO; KOR-Bench cipher and operation | Removes memorisation (a large drop for older LLMs). Reasoning models reached 52.8% / 37.3% on Mystery / Randomized [P]. LingOly-TOO costs frontier models about 0.1, and scores keep rising [S/Sec]. | H (Blocksworld); M (LingOly-TOO) |
| Rare-but-real systems (esolangs, endangered languages) | MTOB; EsoLang-Bench; LingOly | MTOB en→kgv reached human level (Gemini 1.5 Pro, 58.3 vs 57.0 chrF) about 5 months after release [S]. Its gains came from parallel examples [S]. EsoLang is still at 3.8% overall (2026) [P]. Contamination risk rises over time, so both use encrypted or password-zipped data [P]. | M |
| Counterfactual variants of known systems | Wu et al. counterfactual tasks; NewtonBench "metaphysical shifts"; HardcoreLogic long-tail variants | Large gaps for 2023-era models [S]. Subtle-variant fragility persists for GPT-5 (Oct 2025) [S]. NewtonBench is "fragile" but now an RL target [P]. [I] Durable only while the space of variants is too large to train on. | M |
| Fresh human-created items on a cadence | LiveCodeBench (v1→v6, May 2023 to Apr 2025, 400→1,055 problems); LiveBench (monthly by design); annual IOL problems (IOL-AI) | Contamination-proof: LiveCodeBench detected DeepSeek contamination [S][P]. Not difficulty-proof: IOL 2026 was at gold level [S]. LiveBench's README still names 2025-04-25 as the "current release", suggesting cadence lapses [P]. | H (contamination); M (cadence) |
| Rule space too large to train on (generated games or worlds) | gg-bench (LLM-generated games); AutumnBench DSL worlds; KORGym parameterised games; WitnessGym | gg-bench reasoning models at 31–36% (May 2025), with no later data [P]. AutumnBench shows a human > model gap (Oct 2025) [S]. Counterexample: the Eleusis cogame uses a 68-rule public catalogue, small enough to enumerate [P]. | L–M (young, sparse follow-up) |
| Secret generators or held-out primitives | WitnessBench private test with held-out primitives | RL on the public gym gives a 27B model only 2.1→5.4 RHAE-L5 on the private test, though with gains on both held-out splits (Sep 2026). The best of 18 frontier models solves 24% of private level slots [S]. Too new to judge durability. | L |
| Interactive, efficiency-scored learning | ARC-AGI-3 RHAE | Discriminative at launch (all frontier models <1%). Saturated once models "understood" mechanics: Astra (max, Provider Adapter) used fewer actions than the median human on 96.0% of levels. The 1.15 cap and the scoring change in week 3 add non-stationarity [P][P-m]. | H |
| Expert-authored novel knowledge contexts | CL-bench (about 20 expert-hours per context); CL-bench Life | Best about 23% (Feb 2026) and 22.2% (Apr 2026) [S]. Durable so far, but costly and LLM-judge graded [P]. | M |
| Adversarial or evolving benchmark versions | ARC v1→v2→v3 "refinement loop" of benchmark design | ARC frames adaptation as the method ("iteratively improving benchmarks in response to AI progress") [P-m]. Each version lasted roughly 5 years (v1, 2019 to about 2024), about 1 year (v2) and about 5 months (v3) against frontier models [I; dates from P-m/S]. | M |

### Inferences

- [I] The versions' life spans are shrinking: ARC v1 lasted about 5 years, v2 about 1 year, v3 about 5 months. A new benchmark should plan for planned rotation of task *families*, not only instances, on a cadence of months.
- [I] The most promising combination, untested at frontier scale:
  1. Secret, rotating *primitive sets* (Witness-style).
  2. Per-run semantic randomisation to kill memorisation (Mystery / LingOly-TOO).
  3. Scoring on hypothesis and experiment efficiency, not execution efficiency (ZendoWorld, FalsifyBench, AutumnBench).
  4. A fixed, reported harness (the ARC-AGI-3 lesson).

### Gaps

- No durability data was found for automated *adversarial* generators (e.g. Dynabench-style) in test-time-learning settings.
- No data on how long a secret generator stays secret when labs can probe it through submissions.

---

## 5. Claims table

| # | Claim | Value | Date | Source URL | Type | Conf. |
|---|---|---|---|---|---|---|
| 1 | ARC-AGI-3 RHAE per-level formula and cap | (h/a)², cap 1.15; level-index weighted; only env-changing actions count | docs, current 30 Sep 2026 | https://raw.githubusercontent.com/arcprize/docs/main/methodology.mdx | P | H |
| 2 | ARC-AGI-3 scoring change | 2nd-best → median human; cap 1.0→1.15 | 14 Apr 2026 | https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx | P | H |
| 3 | ARC-AGI-3 human study | 458 participants, 90 min, ~$130 + $5/solve, first-run, ≥2 solvers per env | captured 29 Sep 2026 | https://arcprize.org/blog/arc-agi-3-human-dataset (capture: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md) | P-m | H |
| 4 | ARC-AGI-3 public demo human data | 342 replays, 145 solves, 25 envs | 2026 | same as #3 | P-m | H |
| 5 | Opus 5 on ARC-AGI-3 (semi-private, verified) | 30.16% (high); GPT-5.6 Sol 7.78% (pre-Opus-5 best, *not* the launch-time best, which was <1%) | 24 Jul 2026 system card | https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md | P-m | H |
| 6 | GPT-6 Astra on ARC-AGI-3 | 62.7% Standard (max) / 99.9% Provider Adapter (high) | 3 Sep 2026 | https://arcprize.org/blog/astra (translation mirror: https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md) | P-m + S | H |
| 7 | Astra's action efficiency | Astra (max, Provider Adapter): fewer actions than median human on 96.0% of levels; 51.7% fewer on average | 3 Sep 2026 | same as #6 | P-m | H |
| 8 | Harness difference | Standard = visible notes, `manual_rolling`; Provider Adapter = native reasoning state + compaction | current | https://raw.githubusercontent.com/arcprize/arc-agi-3-benchmarking/main/README.md | P | H |
| 9 | ARC-AGI-3 community leaderboard, public demo | Tycho 100.0% | 29 Jul 2026 | https://arcprize.org/leaderboard/community | S | M |
| 10 | ARC "knowledge overfitting" assertion for ARC-AGI-1/2 | "accidentally or intentionally" | Jan 2026 | https://arxiv.org/abs/2601.10904 (mirror: https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md) | P-m | H |
| 11 | Poetiq refinement harness on ARC-AGI-2 | 31% ($0.81) → 54% ($31) | late 2025 | same as #10 | P-m | H |
| 12 | ARC Prize 2025 top Kaggle ARC-AGI-2 score | 24% | Nov 2025 (report Jan 2026) | same as #10 | P-m | H |
| 13 | ARC Prize 2024: ARC-AGI-1 private SOTA | 33% → 55.5% (MindsAI); TTT 47.5% semi-private | Dec 2024 | https://arcprize.org/blog/arc-prize-2024-winners-technical-report | S | M |
| 14 | ARC-AGI-2 human calibration | avg test-taker 66% (readme); each task solved by ≥2 people in ≤2 attempts (arcprize.org, not the readme) | 2025 | https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/readme.md ; https://arcprize.org/arc-agi/2 | P / S | H |
| 15 | Gemini 3 Deep Think on ARC-AGI-2 | 84.6% | Feb 2026 | https://labs.adaline.ai/p/what-is-the-arc-agi-benchmark-and (aggregator excerpt) | Sec | L–M |
| 16 | MTOB 2023 baselines vs human | 44.7/45.8 vs 51.6/57.0 chrF | Sep 2023 | https://raw.githubusercontent.com/lukemelas/mtob/main/README.md | P | H |
| 17 | Gemini 1.5 Pro MTOB en→kgv | 58.3 chrF (> 57.0 human) | Feb–Mar 2024 | https://arxiv.org/abs/2403.05530 | S | M |
| 18 | Llama 4 Maverick MTOB | half book 54.0/46.4; full 50.8/46.7 (en→kgv / kgv→en) | Apr 2025 | https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama4/MODEL_CARD.md | P | H |
| 19 | MTOB gains come from parallel examples | "almost all" improvement | Sep 2024 | https://arxiv.org/abs/2409.19151 | S | M |
| 20 | LingOly baseline | best 38.7% on *harder* problems (Claude 3 Opus; +24.7 over no-context) [corrected]; avg EM 21.7% [uncertain] | Jun 2024 | https://arxiv.org/abs/2406.06196 | S | M |
| 21 | LingOly-TOO obfuscated top scores | GPT-5 0.467; Opus 4.1 0.458; Claude 3.7 0.43 | 2025 | https://benchmarklist.com/benchmarks/lingoly_too/ ; https://arxiv.org/abs/2503.02972 | Sec/S | M–L |
| 22 | IOL-AI Challenge | Opus 4.8 gold-equivalent (79.5 vs min gold 70.0), would place 4th of 255; 731 submissions, 46 teams, T4 × 30 min (budget applies to challenge entries, not Opus 4.8) | Aug 2026 | https://arxiv.org/abs/2608.18011 | S | M |
| 23 | Olympiad inference-time scaling gains | +4.9 / +13.1 / +4.9 pp (R1 / Gemini 2.5 Flash / Llama 3.3) | CoNLL 2026 | https://aclanthology.org/2026.conll-main.28/ | S | M |
| 24 | EsoLang-Bench peak and overall | 11.2% peak; ~3.8% overall; Python/JS 100%; few-shot +0.8 pp (p=0.505) | Mar–May 2026 | https://raw.githubusercontent.com/Lossfunk/EsolangBench/main/README.md | P | H |
| 25 | KOR-Bench at release | ~58% (Claude-3.5-Sonnet, GPT-4o) | Oct 2024 | https://raw.githubusercontent.com/KOR-Bench/KOR-Bench/main/README.md | P | H |
| 26 | KORGym top performers | o3-mini best overall; Doubao-1.5-thinking-pro 0.72 mean | May 2025 | https://arxiv.org/abs/2505.14552 | S | M |
| 27 | CL-bench design | 500 contexts, 1,899 tasks, 31,607 rubrics; ~20 expert-h/context; GPT-5.1 judge | Feb 2026 | https://raw.githubusercontent.com/Tencent-Hunyuan/CL-bench/main/README.md | P | H |
| 28 | CL-bench scores | avg 17.2%; best GPT-5.1 23.7%; Life best GPT-5.5 (High) 22.2% | Feb / Apr 2026 | https://arxiv.org/abs/2602.03587 ; https://hy.tencent.com/research/100039?langVersion=en | S | M |
| 29 | gg-bench win rates | GPT-4o 8.94; Claude 3.7 9.53; o3-mini 31.08; R1 32.50; o1 36.28 | May 2025 | https://raw.githubusercontent.com/vivek3141/gg-bench/master/README.md | P | H |
| 30 | Boardwalk | Claude 3.7 Sonnet 55.6% of 12 anonymised games error-free (55.6% uncertain) | Aug 2025 | https://arxiv.org/abs/2508.16447 | S | L–M |
| 31 | PlanBench Mystery Blocksworld | older LLMs ~0%; o1-preview 52.8% (Randomized 37.3%); R1 43.3% (25.8%) | Sep 2024 / 2025 | https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md | P | H |
| 32 | NewtonBench | 324 tasks, 12 domains; 0.0001 noise → 13–15% drop; NeMo Gym RL env 26 Feb 2026 | Oct 2025 – Feb 2026 | https://raw.githubusercontent.com/HKUST-KnowComp/NewtonBench/main/README.md | P | H |
| 33 | HardcoreLogic | >5,000 puzzles, 10 games; GPT-5 degrades significantly | Oct 2025 | https://arxiv.org/abs/2510.12563 | S | M |
| 34 | WILT | best 28% (Claude 3.5 Sonnet) | Oct 2024 | https://arxiv.org/abs/2410.10998 | S | M |
| 35 | ZendoWorld | humans 73.3% win, 8.0±0.7 turns; VLM agents 44.5% | Jul 2026 | https://arxiv.org/abs/2607.08233 | S | M |
| 36 | DiscoveryWorld | humans 66% completion / 55% knowledge; best agent ~18% (excerpt: challenge tasks only; normal uncertain) | Jun 2024 | https://arxiv.org/abs/2406.06769 | S | M |
| 37 | AutumnBench | 43 envs, 129 tasks, 517 humans > 3 frontier models | Oct 2025 | https://arxiv.org/abs/2510.19788 | S | M |
| 38 | Witness RL transfer | Qwen3.8-27B: 2.1 → 5.4 RHAE-L5 on private test; best of 18 frontier models 24% of private level slots; Opus 5 59.9 validation RHAE-L5 | Sep 2026 | https://arxiv.org/abs/2609.32208 | S | M |
| 39 | Reasoning Gym cross-domain RLVR transfer | algorithmic→algebra +29.1%, geometry +22.3%; logic→cognition +13.3%; games→algebra +21.8% | May 2025 | https://arxiv.org/abs/2505.24760 | S | M |
| 40 | Reasoning Gym size and purpose | >100 generators; RL training | current | https://raw.githubusercontent.com/open-thought/reasoning-gym/main/README.md | P | H |
| 41 | Enigmata transfer claims | 36 tasks / 7 categories; 32B model > o3-mini-high and o1 on Enigmata-Eval, ARC-AGI-1/2; AIME and GPQA gains in Seed1.5 | May 2025 | https://raw.githubusercontent.com/BytedTsinghua-SIA/Enigmata/main/README.md | P (author claim) | M |
| 42 | SynLogic | 35 tasks; +6 BBEH over R1-Distill-Qwen-32B | May 2025 | https://raw.githubusercontent.com/MiniMax-AI/SynLogic/main/README.md | P (author claim) | M |
| 43 | RL Grokking Recipe | qualitatively new dynamics ~0 after RL | Sep 2025 | https://arxiv.org/abs/2509.21016 | S | M–L |
| 44 | MastermindEval | o3-mini >0.85 solve at c=5, n=7; perfect-game rate >0.78 | Mar 2025 | https://arxiv.org/abs/2503.05891 | S | M |
| 45 | re-ARC | generators for all 400 ARC-1 training tasks; 1,000 verified examples each | Apr 2024 | https://raw.githubusercontent.com/michaelhodel/re-arc/main/README.md | P | H |
| 46 | LiveCodeBench versions | v1 400 → v6 1,055 problems (May 2023 – Apr 2025) | Apr 2025 | https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/main/README.md | P | H |
| 47 | LiveCodeBench contamination detection | DeepSeek drops on problems after Aug–Sep 2023 | 2024 | https://arxiv.org/abs/2403.07974 | S | M |
| 48 | LiveBench "current release" in README | 2025-04-25 (not all public) | README fetched 30 Sep 2026 | https://raw.githubusercontent.com/LiveBench/LiveBench/main/README.md | P | H |
| 49 | Eleusis cogame rule space | 68-rule public catalogue | current | https://raw.githubusercontent.com/Metta-AI/cogame-eleusis/main/README.md | P | H |
| 50 | ARC-AGI-3 Kaggle Milestone #1 winner | Tufa Labs "The Duck" (small open LLM + Python REPL) | 30 Jun 2026 | https://arcprize.org/blog/arc-prize-2026-milestone-1 | S | M |
| 51 | ARC-AGI-3 launch-time frontier scores [added by fact-check] | all <1%: Gemini 3.1 Pro Preview 0.37%, GPT-5.4 0.26%, Opus 4.6 0.25%, Grok 4.20 0% | 25 Mar 2026 | https://arcprize.org/blog/arc-agi-3-launch ; https://arxiv.org/abs/2603.24621 | S | M–H |

---

## 6. Sources

**Primary, fetched (official repos and docs):**
- ARC docs, methodology: https://raw.githubusercontent.com/arcprize/docs/main/methodology.mdx
- ARC docs, changelog: https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx
- ARC-AGI-3 benchmarking harness README: https://raw.githubusercontent.com/arcprize/arc-agi-3-benchmarking/main/README.md
- ARC-AGI-2 readme: https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/readme.md
- EsoLang-Bench: https://raw.githubusercontent.com/Lossfunk/EsolangBench/main/README.md
- gg-bench: https://raw.githubusercontent.com/vivek3141/gg-bench/master/README.md
- KOR-Bench: https://raw.githubusercontent.com/KOR-Bench/KOR-Bench/main/README.md
- CL-bench: https://raw.githubusercontent.com/Tencent-Hunyuan/CL-bench/main/README.md
- Reasoning Gym: https://raw.githubusercontent.com/open-thought/reasoning-gym/main/README.md
- Enigmata: https://raw.githubusercontent.com/BytedTsinghua-SIA/Enigmata/main/README.md
- SynLogic: https://raw.githubusercontent.com/MiniMax-AI/SynLogic/main/README.md
- PUZZLES (RLP): https://raw.githubusercontent.com/ETH-DISCO/rlp/main/README.md
- re-ARC: https://raw.githubusercontent.com/michaelhodel/re-arc/main/README.md
- MARC (TTT): https://raw.githubusercontent.com/ekinakyurek/marc/main/README.md
- MastermindEval: https://raw.githubusercontent.com/flairNLP/mastermind/main/README.md
- DiscoveryWorld: https://raw.githubusercontent.com/allenai/discoveryworld/main/README.md
- NewtonBench: https://raw.githubusercontent.com/HKUST-KnowComp/NewtonBench/main/README.md
- BoxingGym: https://raw.githubusercontent.com/kanishkg/boxing-gym/main/README.md
- Counterfactual evaluation: https://raw.githubusercontent.com/ZhaofengWu/counterfactual-evaluation/master/README.md
- MTOB: https://raw.githubusercontent.com/lukemelas/mtob/main/README.md
- Llama 4 model card: https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama4/MODEL_CARD.md
- LingOly: https://raw.githubusercontent.com/am-bean/lingOly/main/README.md
- LingOly-TOO: https://raw.githubusercontent.com/jkhouja/LingOly-TOO/main/README.md
- Could LMs win the IOL? (repo): https://raw.githubusercontent.com/JamieGarnham/lingoly-team/main/README.md
- Linguini: https://raw.githubusercontent.com/facebookresearch/linguini/main/README.md
- PlanBench: https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md
- WILT: https://raw.githubusercontent.com/RiotGames/WILT/main/README.md
- Eleusis cogame: https://raw.githubusercontent.com/Metta-AI/cogame-eleusis/main/README.md
- HardcoreLogic: https://raw.githubusercontent.com/ljcleo/hardcore-logic/master/README.md
- LiveBench: https://raw.githubusercontent.com/LiveBench/LiveBench/main/README.md
- LiveCodeBench: https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/main/README.md
- InternBootcamp: https://raw.githubusercontent.com/InternLM/InternBootcamp/main/README.md

**Mirrors and captures of primary pages:**
- ARC Prize 2025 Technical Report (arXiv 2601.10904): https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md
- ARC-AGI-3 human dataset blog (capture of arcprize.org/blog/arc-agi-3-human-dataset): https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md
- "OpenAI's GPT-6 Astra on ARC-AGI-3" (translation of arcprize.org/blog/astra): https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md
- Claude Opus 5 system card §8 (mirror): https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md

**Primary pages seen only as search excerpts (not fetched; egress-blocked):**
- https://arcprize.org/blog/astra ; https://arcprize.org/leaderboard/community ; https://arcprize.org/blog/arc-prize-2026-milestone-1 ; https://arcprize.org/blog/arc-prize-2024-winners-technical-report ; https://arxiv.org/abs/2603.24621 (ARC-AGI-3 paper)
- MTOB / Gemini 1.5: https://arxiv.org/abs/2309.16575 ; https://arxiv.org/abs/2403.05530 ; Aycock et al.: https://arxiv.org/abs/2409.19151
- LingOly: https://arxiv.org/abs/2406.06196 ; LingOly-TOO: https://arxiv.org/abs/2503.02972 ; IOL-AI: https://arxiv.org/abs/2608.18011 ; CoNLL 2026: https://aclanthology.org/2026.conll-main.28/ ; ConlangBench: https://arxiv.org/abs/2608.03505
- EsoLang-Bench: https://arxiv.org/abs/2603.09678 ; KORGym: https://arxiv.org/abs/2505.14552 ; CL-bench: https://arxiv.org/abs/2602.03587 ; CL-bench Life blog: https://hy.tencent.com/research/100039?langVersion=en
- gg-bench: https://arxiv.org/abs/2505.07215 ; Code World Models: https://arxiv.org/abs/2510.04542 ; Boardwalk: https://arxiv.org/abs/2508.16447
- Counterfactual tasks: https://arxiv.org/abs/2307.02477 ; o1 on PlanBench: https://arxiv.org/abs/2409.13373 ; NewtonBench: https://arxiv.org/abs/2510.07172 ; HardcoreLogic: https://arxiv.org/abs/2510.12563
- WILT: https://arxiv.org/abs/2410.10998 ; InductionBench: https://arxiv.org/abs/2502.15823 ; ZendoWorld: https://arxiv.org/abs/2607.08233 ; FalsifyBench: https://arxiv.org/abs/2606.04751 ; Hero's Journey: https://arxiv.org/abs/2606.02556 ; DiscoveryWorld: https://arxiv.org/abs/2406.06769 ; AutumnBench: https://arxiv.org/abs/2510.19788 ; Witness: https://arxiv.org/abs/2609.32208
- Reasoning Gym: https://arxiv.org/abs/2505.24760 ; RL Grokking Recipe: https://arxiv.org/abs/2509.21016 ; MastermindEval: https://arxiv.org/abs/2503.05891 ; LiveCodeBench: https://arxiv.org/abs/2403.07974 ; InternBootcamp: https://arxiv.org/abs/2508.08636

**Secondary or aggregator (low weight):**
- LingOly-TOO leaderboard mirror: https://benchmarklist.com/benchmarks/lingoly_too/
- ARC-AGI-2 2026 score aggregation: https://labs.adaline.ai/p/what-is-the-arc-agi-benchmark-and
- ARC-AGI-3 leaderboard aggregation: https://benchlm.ai/benchmarks/arcagi3

---

## Fact-check log (Phase 1)

**Tally:** 78 claims checked: 62 verified, 8 corrected, 8 uncertain, 0 removed.
**Access:** arcprize.org, arxiv.org, huggingface.co, openreview.net, aclanthology.org and semanticscholar.org were blocked (proxy 403/000). raw.githubusercontent.com and anthropic.com were fetched in full; WebSearch worked and gave excerpts of the blocked primary pages ([S]).
**Most consequential:** (1) The ARC-AGI-3 launch-time best was <1% (Gemini 3.1 Pro Preview 0.37%), not 7.78%. 7.78% (GPT-5.6 Sol) was the leaderboard best just before Opus 5 (24 Jul 2026), so dossiers A/E and F are all right once dated. (2) Code world models did not produce Astra's scored 99.9%. (3) Witness needed frontier context, and it partly contradicts "near-zero transfer to new primitives".

| # | Claim | Verdict | Source URL | Note |
|---|---|---|---|---|
| 1 | ARC-AGI-3 launched 25 Mar 2026 | verified | https://arcprize.org/blog/arc-agi-3-launch (search excerpt); https://arxiv.org/abs/2603.24621 | Several excerpts agree (launched at Y Combinator, SF). |
| 2 | ARC-AGI-3 best score at launch = 7.78% (implied by "went from a best of 7.78%") | corrected | https://arcprize.org/blog/arc-agi-3-launch (excerpt); https://raw.githubusercontent.com/memgrafter/research-digests/491d1e597ee1384396057fbe72e2bdec9f11c2c6/ml_research_analysis_2026/2603.24621_arc-agi-3-a-new-challenge-for-frontier-agentic-intelligence_20260331_185732.md | Launch: all frontier <1% (Gemini 3.1 Pro Prev 0.37, GPT-5.4 0.26, Opus 4.6 0.25, Grok 4.20 0). The 7.78% was the pre-Opus-5 best. Resolves the conflict with A/E ("<1%"; E: "best 0.37%"). |
| 3 | Opus 5 30.16% (high), "roughly four times the best previously reported score"; GPT-5.6 Sol 7.78% (max); Opus 4.8 1.52% | verified | https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md | Verbatim in card §8.14.2 ("…on the official leaderboard"). |
| 4 | Opus 5 system card "mid-2026" | verified | https://www.anthropic.com/news/claude-opus-5 | Precise date: released 24 Jul 2026. |
| 5 | GPT-6 Astra 62.7% Standard (max, $26,098) / 99.9% Provider Adapter (high, $18,817), 3 Sep 2026 | verified | https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md | Chinese translation of arcprize.org/blog/astra (Kamradt, 3 Sep 2026); full effort table present. |
| 6 | "62.7% vs 99.9% for the same model" | verified | same as #5 | Clarified: different effort (max vs high). Same-effort (max) gap is 62.7% vs 98.6%. |
| 7 | Astra fewer actions than median human on 96.0% of levels; 51.7% fewer on average | verified | same as #5 | Clarified: this is Astra (max) on the Provider Adapter (the 98.6% run), not the 99.9% run. |
| 8 | ~5 months from launch to 99.9% | verified | #1, #5 | 25 Mar → 3 Sep = 5.3 months (dossier A's "6 months" is looser). |
| 9 | "Rule-to-code compilation (CWM) is the approach that won ARC-AGI-3"; recipe item "Astra writing maze_solver.py" | corrected | same as #5 | Scored Astra runs used symbolic notes ("not a complete programming language") and preserved reasoning state. Solver files came from the separate PRO-LONG sandbox harness (model plus tools). Executable world models were used by community public-set agents (Tycho). |
| 10 | Opus 5 card quote "no instructions, no rules, and no stated goals" | corrected | same as #3 | Verbatim: "with no instructions, rules, or stated goals". |
| 11 | ARC quotes on Astra ("compress unfamiliar environments…") and on ARC-AGI-3's limits ("scope and format are tightly bounded…") | corrected | same as #5 | Content matches, but the only source is a Chinese translation. Recast as back-translated paraphrase, not verbatim. |
| 12 | ARC expected AI to need more actions; frontier AI is "binary" once mechanics are understood | verified | same as #5 | "更像二元模式" in the translation. |
| 13 | Harnesses: Standard = visible notes, `manual_rolling`; Provider Adapter = native reasoning state + compaction | verified | https://raw.githubusercontent.com/arcprize/arc-agi-3-benchmarking/main/README.md | |
| 14 | RHAE: (h/a)², cap 1.15, level-index weighting, 4-of-5 levels → 66.7% cap, only env-changing actions count, upper median | verified | https://raw.githubusercontent.com/arcprize/docs/main/methodology.mdx | |
| 15 | 14 Apr 2026: baseline 2nd-best → median; cap 1.0 → 1.15 | verified | https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx | |
| 16 | Human study: 458 people, 90 min, ~$130 + $5/solve, first-run, same system prompt, every env beaten by ≥2 of ~10 | verified | https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md | Capture of the 14 Apr 2026 post. ARC's Astra post says $115/session and "about 500" people, so ARC's own figures differ slightly. |
| 17 | Public demo: 342 replays, 145 solves, 25 envs; 10/10 (r11l) vs 6/12 (tr87); "luck factor"; "first place doesn't always get 100%" | verified | same as #16 | |
| 18 | Tycho 100.0% on public demo, 29 Jul 2026 | verified | https://arcprize.org/leaderboard/community (search excerpt) | Public-set scores are self-reported; others (e.g. VISTA) also reached 100%. |
| 19 | Kaggle Milestone #1 (30 Jun 2026) won by Tufa Labs' "The Duck" (small open LLM + Python REPL) | verified | https://arcprize.org/blog/arc-prize-2026-milestone-1 (excerpt); https://raw.githubusercontent.com/Tufalabs/duck-harness/main/README.md | Model: Qwen 3.6 27B FP8 [S]. Score still not captured. |
| 20 | ARC: ARC-AGI-1/2 "overfit", "accidentally or intentionally"; IID splits + public-data training; Gemini 3 Deep Think colour mappings | verified | https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md | Added ARC's caveats: "cannot determine which" and "cannot precisely quantify the magnitude". "At the family level" is the dossier's gloss. |
| 21 | ARC Prize 2024: private SOTA 33% → 55.5% (MindsAI); TTT (Akyürek et al.) 47.5% semi-private | verified | https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2024/2412.04604v2_arc_prize_2024.md | TTT figure upgraded from [S] to [P-m]. |
| 22 | ARC Prize 2025 top Kaggle score 24%; Poetiq 31% ($0.81) → 54% ($31) | verified | same as #20 | |
| 23 | ARC-AGI-2 average test-taker 66%; 2 trials (readme also says 3 in one place) | verified | https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/readme.md | |
| 24 | ARC-AGI-2 each task solved by ≥2 people in ≤2 attempts, tagged [P, readme] | verified | https://arcprize.org/arc-agi/2 (search excerpt) | The claim is true, but it is not in the readme; source tag fixed. |
| 25 | Gemini 3 Deep Think 84.6% on ARC-AGI-2 (Feb 2026) | verified | https://x.com/arcprize/status/2021985585066652039 (search excerpt) | ARC-verified, $13.62/task; secondary-grade evidence. |
| 26 | ARC-AGI-2 ~95% by Sep 2026 | uncertain | https://arcprize.org/results/openai-gpt-6-astra (blocked) | Dossier A cites Astra 95.0% [S]; not fetched. |
| 27 | re-ARC: generators for all 400 ARC-1 training tasks, 1,000 verified examples each | verified | https://raw.githubusercontent.com/michaelhodel/re-arc/main/README.md | |
| 28 | MTOB: <200 speakers; 400 parallel train sentences; encrypted + BIG-bench canary; 44.7/45.8 vs human 51.6/57.0 chrF; Sep 2023; ICLR 2024 | verified | https://raw.githubusercontent.com/lukemelas/mtob/main/README.md ; https://iclr.cc/virtual/2024/poster/17609 | README says "several hundred pages" (dossier: "about 500"). |
| 29 | Gemini 1.5 Pro 58.3 chrF en→kgv > 57.0 human; parity ~5 months after MTOB | verified | https://arxiv.org/abs/2403.05530 (search excerpt) | Sep 2023 → Feb 2024 ≈ 5 months. |
| 30 | Llama 4 Maverick MTOB half 54.0/46.4, full 50.8/46.7 (under "Long Context") | verified | https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama4/MODEL_CARD.md | |
| 31 | Aycock et al.: almost all improvement comes from parallel examples; ICLR 2025 | verified | https://proceedings.iclr.cc/paper_files/paper/2025/hash/20f44da80080d76bbc35bca0027f14e6-Abstract-Conference.html (excerpt) | |
| 32 | ConlangBench: 21 conlangs, 21M pairs, fine-tuned models learn all eight well-resourced conlangs | verified | https://arxiv.org/abs/2608.03505 (excerpt) | |
| 33 | LingOly: best model (Claude 3 Opus) 38.7% exact match | corrected | https://arxiv.org/abs/2406.06196 (excerpt, NeurIPS 2024 abstract) | 38.7% is on *harder* problems (+24.7 over no-context). |
| 34 | LingOly average exact match 21.7% | uncertain | https://arxiv.org/abs/2406.06196 | Not found in excerpts. |
| 35 | LingOly data in password zip; no-context control | verified | https://raw.githubusercontent.com/am-bean/lingOly/main/README.md | |
| 36 | LingOly-TOO: 82 problems, "over 1,200 QA pairs", up to 6 obfuscations | corrected | https://arxiv.org/html/2503.02972v3 (excerpt) | 6,995 QA pairs (v3). "Up to 6 obfuscations" still unverified. |
| 37 | LingOly-TOO v3: Claude 3.7 Sonnet 0.43, o1-preview 0.32, o3-mini 0.31; best 0.59 → 0.48 with obfuscation; small human drop | verified | https://arxiv.org/abs/2503.02972 (excerpts) | Human drop ~5.7% vs models ~12.8%. |
| 38 | LingOly-TOO leaderboard: GPT-5 0.467, Opus 4.1 0.458 | uncertain | https://benchmarklist.com/benchmarks/lingoly_too/ | Aggregator only; HF leaderboard blocked. |
| 39 | Linguini password-protected against crawling | verified | https://raw.githubusercontent.com/facebookresearch/linguini/main/README.md | |
| 40 | CoNLL 2026 olympiad paper: +4.9 / +13.1 / +4.9 pp; repo revised 26 Aug 2026; password zips | verified | https://aclanthology.org/2026.conll-main.28/ (excerpt); https://raw.githubusercontent.com/JamieGarnham/lingoly-team/main/README.md | |
| 41 | IOL-AI: Opus 4.8 gold-equivalent on unseen IOL 2026, would place 4th; min gold 70.0; 731 submissions, 46 teams, 1×T4 30 min | verified | https://arxiv.org/abs/2608.18011 (excerpts) | 79.5/100, 4th of 255. The T4 budget applied to challenge entries (the two graded were in the bottom 5%), not to Opus 4.8. |
| 42 | EsoLang-Bench: 80 problems / 4 tiers / 5 langs; 6 hidden tests; docs in prompt; 5 attempts; 8,192 tokens | verified | https://raw.githubusercontent.com/Lossfunk/EsolangBench/main/README.md | |
| 43 | EsoLang: peak 11.2% (GPT-5.4 xhigh, Befunge-98); ~3.8% overall; o4-mini-high ~3.4%; Gemini 3.1 Pro ~2.6%; Whitespace 0%; Python/JS 100%; few-shot +0.8 pp (p=0.505); Brainfuck 2,028 repos | verified | same as #42 | |
| 44 | KOR-Bench five categories; Claude-3.5-Sonnet / GPT-4o ~58% | verified | https://raw.githubusercontent.com/KOR-Bench/KOR-Bench/main/README.md | |
| 45 | KORGym: 19 LLMs + 8 VLMs; o3-mini top; RL-driven gains | verified | https://arxiv.org/abs/2505.14552 (excerpt) | |
| 46 | KORGym: Doubao-1.5-thinking-pro 0.72 mean, 0.84 puzzles | uncertain | https://arxiv.org/abs/2505.14552 | Not in excerpts. |
| 47 | CL-bench design: 500 contexts, 1,899 tasks, 31,607 rubrics, ~20 expert-h/context, GPT-5.1 judge | verified | https://raw.githubusercontent.com/Tencent-Hunyuan/CL-bench/main/README.md ; https://hyper.ai/en/datasets/49190 (excerpt) | README: 1,899 tasks, 63.2 rubrics/context, 20 h, GPT-5.1 (low) judge. 500 contexts and 31,607 rubrics come from an excerpt. |
| 48 | CL-bench avg 17.2%, best GPT-5.1 23.7% (Feb 2026) | verified | https://arxiv.org/abs/2602.03587 (excerpt) | |
| 49 | CL-bench Life: 405 tasks; best GPT-5.5 (High) 22.2% (Apr 2026) | verified | README (#47); https://hy.tencent.com/research/100039?langVersion=en (excerpt) | |
| 50 | CL-bench still ~23% as of Sep 2026 | uncertain | https://www.clbench.com (not fetched) | No results found for Jul–Sep 2026 frontier models. |
| 51 | gg-bench: 126 games, "data generating process", 30 games/env; GPT-4o 8.94, Claude 3.7 9.53, o3-mini 31.08, R1 32.50, o1 36.28 | verified | https://raw.githubusercontent.com/vivek3141/gg-bench/master/README.md ; https://arxiv.org/abs/2505.07215 (excerpt for 126) | |
| 52 | Code World Models (DeepMind, Oct 2025): rules + trajectories → Python for MCTS; value heuristics; hidden-info inference | verified | https://arxiv.org/abs/2510.04542 (excerpt) | Also ICLR 2026 (OpenReview). |
| 53 | Boardwalk: Claude 3.7 Sonnet 55.6% of 12 anonymised games error-free | uncertain | https://arxiv.org/abs/2508.16447 (excerpt) | 12 anonymised games confirmed; 55.6% not seen. |
| 54 | Mystery Blocksworld: older LLMs 0% (LLaMA-3.1 405B 0.8%); o1-preview 97.8 / 52.8 / 37.3; R1 99.1 / 43.3 / 25.8 | verified | https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md | Zero-shot, 600 instances each. |
| 55 | NewtonBench: 324 tasks / 12 domains; "clear but fragile"; 0.0001 noise → 13–15% drop; code helps weaker, hinders stronger; arXiv 9 Oct 2025; ICLR 2026; NeMo Gym RL env 26 Feb 2026 (~4.5 months) | verified | https://raw.githubusercontent.com/HKUST-KnowComp/NewtonBench/main/README.md ; https://raw.githubusercontent.com/NVIDIA-NeMo/Gym/main/README.md | The NeMo Gym README lists "Newton Bench". |
| 56 | HardcoreLogic: >5,000 puzzles, 10 games; large drops, "memorized stereotypes" | verified | https://arxiv.org/abs/2510.12563 (excerpt) | ICLR 2026. |
| 57 | WILT: ≤30 test triples; best 28% (Claude 3.5 Sonnet) | verified | https://arxiv.org/abs/2410.10998 (excerpt); https://raw.githubusercontent.com/RiotGames/WILT/main/README.md | 14/50. |
| 58 | InductionBench (Feb 2025; ACL 2025): subregular string functions; o3-mini struggles | verified | https://aclanthology.org/2025.acl-long.1287/ (excerpt) | |
| 59 | Eleusis cogame: 68-rule public catalogue, "a search, not a guess" | verified | https://raw.githubusercontent.com/Metta-AI/cogame-eleusis/main/README.md | |
| 60 | ZendoWorld: humans (19) 73.3% win in 8.0±0.7 turns vs VLM agents 44.5%; near-uninformative experiments | verified | https://arxiv.org/abs/2607.08233 (excerpt) | VLM turns 8.1±0.4. |
| 61 | FalsifyBench (Jun 2026): 12 LLMs; no model near optimal; negative testing predicts success | verified | https://arxiv.org/abs/2606.04751 (excerpt) | |
| 62 | Hero's Journey (UT Austin, Jun 2026): 8 tasks; ECSR + rule verbalisation; procedural induction open | verified | https://arxiv.org/abs/2606.02556 (excerpt) | |
| 63 | DiscoveryWorld: humans 66% completion / 55% knowledge; official seeds 0–4 | verified | https://arxiv.org/abs/2406.06769 (excerpt); https://raw.githubusercontent.com/allenai/discoveryworld/main/README.md | |
| 64 | DiscoveryWorld best agents ~18% on normal and challenge | uncertain | https://arxiv.org/abs/2406.06769 (excerpt) | Excerpt: ReAct 18% on challenge, 38% on easy. |
| 65 | BoxingGym: 10+ environments; EIG regret | verified | https://raw.githubusercontent.com/kanishkg/boxing-gym/main/README.md | |
| 66 | AutumnBench: 43 envs, 129 tasks, 517 humans > 3 frontier models | verified | https://arxiv.org/abs/2510.19788 (excerpt) | Models: Claude 4 Sonnet, o3, Gemini 2.5 Pro. |
| 67 | Witness: Qwen3.8-27B 2.1 → 5.4 RHAE-L5 on private test; gains on both held-out splits | verified | https://arxiv.org/abs/2609.32208 (excerpts) | Also a mean +4.1 on 4 external discovery benchmarks. |
| 68 | Witness presented as "novel skill still hard" with only the 27B RL result | corrected | same as #67 | Added frontier context: best of 18 frontier models 24% of private level slots; Opus 5 59.9 validation RHAE-L5 (97.8 with ground-truth rules). |
| 69 | Summary: RL transfers "weakly to new primitives" / near-zero transfer | corrected | https://arxiv.org/abs/2509.21016 ; https://arxiv.org/abs/2609.32208 (excerpts) | RL Grokking's near-zero on "qualitatively new dynamics" is verified, but Witness reports RL gains on held-out primitives. Bullet now marked as mixed evidence. |
| 70 | RL Grokking: "qualitatively new dynamics remain near zero" after RL | verified | https://arxiv.org/abs/2509.21016 (excerpt) | |
| 71 | Reasoning Gym: algorithmic → algebra +29.1%, geometry +22.3% | verified | https://arxiv.org/abs/2505.24760 (excerpt) | |
| 72 | Reasoning Gym: logic → cognition +13.3%, games → algebra +21.8% | uncertain | https://arxiv.org/abs/2505.24760 | Not in excerpts. |
| 73 | Reasoning Gym >100 generators, for RL training | verified | https://raw.githubusercontent.com/open-thought/reasoning-gym/main/README.md | |
| 74 | Enigmata: 36 tasks / 7 categories; 32B > o3-mini-high and o1 on Enigmata-Eval, ARC-AGI-1/2; AIME/GPQA gains in Seed1.5 | verified | https://raw.githubusercontent.com/BytedTsinghua-SIA/Enigmata/main/README.md | Author claim. |
| 75 | SynLogic: 35 tasks; +6 BBEH over R1-Distill-Qwen-32B | verified | https://raw.githubusercontent.com/MiniMax-AI/SynLogic/main/README.md | Author claim. |
| 76 | MastermindEval: o3-mini >0.85 solve at c=5, n=7; perfect-game >0.78 | verified | https://arxiv.org/abs/2503.05891 (excerpt) | 0.92 at c=5, n=7. |
| 77 | LiveCodeBench v1 400 → v6 1,055 problems (May 2023–Apr 2025); DeepSeek contamination → results after Aug 2023 | verified | https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/main/README.md | |
| 78 | LiveBench README "current release" 2025-04-25 | verified | https://raw.githubusercontent.com/LiveBench/LiveBench/main/README.md | |

No claims were removed: none of the load-bearing claims looked fabricated. Every 2026 paper the dossier cites (IOL-AI, ZendoWorld, Witness, FalsifyBench, Hero's Journey, ConlangBench, CoNLL 2026, EsoLang, CL-bench Life) turned up in search results with matching figures.
