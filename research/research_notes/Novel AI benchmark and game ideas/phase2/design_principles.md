# Phase 2: Design principles for a durable, discriminative AI benchmark or game

As of 30 Sep 2026. Synthesised from the seven fact-checked Phase 1 dossiers in `../phase1/`: A (human > AI), B (AI > human but discriminative), C (failures and the hypothesis test), D (games), E (capability gaps), F (test-time learning), G (methodology). Where a fact-check corrected a value, the corrected value is used.

**Conventions.**
- Citations give the dossier and section, then the primary URL listed there.
- [interpretation] marks my synthesis; [speculation] marks something untested.
- [uncertain: …] labels are carried over from the fact-check logs.
- **A1** is the archetype where humans clearly beat AI. **A2** is the archetype where AI beats humans but the results separate good models from bad.

---

## 1. Executive summary

- **Hypothesis: refined. The literal claim is refuted.**
  - Lack of novelty explains contamination and familiarity failures only.
  - Panel C's 36 cases split 5 support / 10 contradict / 21 neutral when novelty means unseen items, and about 9 / 6 / 21 when it means novel skills.
  - Either way, 21 failures (broken validity, no adoption) are unrelated to novelty.
  - ARC-AGI-3, FrontierMath Tier 4 and ARC-AGI-1 fell despite being novel.
- **What failed benchmarks share:** a cheap way to raise the score that bypasses the named capability, and no owner renewing the benchmark faster than labs optimise against it. Memorised items are one such path among several.
- **Novelty buys time, not immunity.** ARC's versions lasted about 5 years, then about 1 year, then about 5 months.
- **The harness is now the largest single source of variance.**
  - ARC-AGI-3: 62.7% vs 98.6% for the same model at the same effort.
  - OSWorld: step budgets alone swing scores 20 pp.
- **Public generators become training sets within weeks to months.**
  - Bulls-and-Cows was saturated in about 9.5 weeks.
  - NewtonBench became an NVIDIA NeMo Gym environment in about 4.5 months.
- **The A1 gaps that last are perceptual, physical, exploratory or real-time.**
  - MMSI-Video 96.4 vs 38.0; IntPhys 2 96.44 vs 57.51; BabyVision 94.1 vs 49.7; ZendoWorld 73.3% vs 44.5%.
  - Most of these figures predate the Sep 2026 frontier.
  - Text-only gaps have closed.
- **A2 separation is strongest on traits outside general capability and on long horizons.**
  - Vending-Bench 2 spans more than 50× [secondary] and ranks Grok 4.7 above Opus 5.5.
  - Hallucination rates span 48–88% by lab.
  - Gemini 3.8 Flash beats Opus 5.5 on NYT Connections at about 5.3× lower price.
  - Many of these inversions are within noise.
- **Measurement is usually the weak link.**
  - The median human baseline has 8 people.
  - A 3-pp gap needs about 1,000 items to resolve.
  - A do-nothing agent scores 38% on τ-bench.
  - Novel expert sets have about 18–42% label errors.
- **Adoption follows distribution, not headroom.**
  - "Boring" AutomationBench reached lab launch tables in 5 months.
  - OfficeBench, with a 47% vs 93% [uncertain] model–human gap, died unmaintained.
- **Top five principles:**
  - P1: renew task families.
  - P7: treat public generators as training data.
  - P18: freeze the harness and publish the bring-your-own-harness delta.
  - P6 + P15: seal execution and keep the grader unreachable.
  - P17: baseline humans properly.

---

## 2. Verdict on the novelty hypothesis

**Verdict: refined.** As "the one thing failed benchmarks have in common", lack of novel critical thinking is **refuted**. A narrower version holds.

### 2.1 Evidence under both readings

| Reading | Supports | Contradicts | Neutral |
|---|---|---|---|
| **Unseen instances** | 5: AIME 2024, SWE-bench Verified, HumanEval/MBPP, MATH (partial), GSM8K (non-frontier models) | 10: GPQA, AIME 2025 and final-answer contests, FrontierMath, LMArena, ARC-AGI-1, ARC-AGI-3, LiveBench, Bulls-and-Cows, Logic-RL Knights-and-Knaves, AutomationBench | 21: validity or adoption failures, or too young to judge |
| **Novel skills or task families** | about 9: AIME 2025, Bulls-and-Cows, Logic-RL and LiveBench move here, because their skills were familiar and Logic-RL was trained on the family | about 6 | 21 |

Source: C §4 and its Gaps note.

**Counterexamples that hold under every reading** (C §4 Gaps):
- **ARC-AGI-3.** A novel family with no item leakage. Scores went from under 1% at launch (25 Mar 2026) to 7.78% (GPT-5.6 Sol) to 30.16% (Opus 5, 24 Jul). On 3 Sep, GPT-6 Astra scored 62.7% on the standard harness vs 98.6% on the provider harness at the same max effort, and 99.9% at high effort (A §2.3; [ARC](https://arcprize.org/blog/astra)).
- **FrontierMath Tier 4.** Unpublished problems went from 5% to 98% in under 14 months. Caveats: the 98% is on the error-fixed v2, and Epoch reports AI "unintended shortcuts" (C §3.2; [Epoch](https://x.com/EpochAIResearch/status/2098103831502708864)).
- **ARC-AGI-1.** A 2020 brute-force ensemble solved 49% of the private set (C §3.4; [report](https://arxiv.org/abs/2412.04604)).
- **The user's "failed" list.** Qi Town was built to escape "data dependency", and TopoBench is procedural. Both died of adoption failure or missing artifacts (C §3.3).

**Evidence for the kernel:**
- **Novel skills delay saturation.**
  - ARC-AGI-1 took about 4 years to go from 0% to 5% (C §3.4).
  - EsoLang-Bench scores 3.8% vs 100% for the same problems in Python (F §2; [README](https://raw.githubusercontent.com/Lossfunk/EsolangBench/main/README.md)).
  - BBEH restored headroom (44.8%) after BBH passed 90% (C §5).
- **Obfuscation and fresh items expose reciting.**
  - Mystery Blocksworld: 0% for non-reasoning LLMs vs 100% for a classical planner (A §2.7).
  - MathArena found "strong signs of contamination in AIME 2024" (C §3.2).
- **The converse also fails.** GPQA and AutomationBench lacked novelty yet stayed useful (C §4).

### 2.2 Refined statement

[interpretation, extending C §5] Benchmarks fail when two things hold:
1. The cheapest way to raise the score stops running through the named capability, or never did.
2. No owner renews items, task families and protocol faster than labs optimise against them.

The cheap paths are contamination, training on the task family, brute force and tools, harness engineering, broken graders and selective submission. For new benchmarks, adoption failure is a separate, dominant killer.

**The version of the hypothesis the evidence supports:** durable benchmarks need *renewed* novelty at the level of skills or primitives, *plus* a protocol that closes the shortcuts that don't depend on memorisation. Novelty is a renewal mechanism and a contamination audit, not a moat (C §5).

[interpretation] For "critical thinking", the durable seam is reasoning under interaction and uncertainty: designing experiments, revising hypotheses, knowing when not to answer. Every text-only gap re-tested in 2025–26 has closed or nearly closed (E Q1).

### 2.3 What novelty prevents, and what it doesn't

| Failure mode | Novel instances | Novel skills or families |
|---|---|---|
| Item contamination | **Prevents** | **Prevents** |
| Format familiarity ("knowledge overfitting") | No (ARC-AGI-1/2; A §2.2) | Delays until the family is targeted |
| Capability catch-up | No (AIME 2025, FrontierMath) | Delays (ARC-AGI-1 about 5 years; ARC-AGI-3 about 5 months) |
| RL on the family | No | Delays only while the generator stays secret; some transfer anyway (F §3) |
| Brute force or simulator-writing | No | No (ARC-AGI-1's 49%) |
| Harness capture | No | No (ARC-AGI-3) |
| Leakage during evaluation | No (BrowseComp) | No |
| Label errors | No: novel expert items are *more* error-prone (FrontierMath 42%, HLE about 29%) | No |
| Gaming | No (LMArena's fresh prompts) | No |
| Noise, adoption, pre-emption | No (Qi Town, TopoBench) | No |

---

## 3. Failure taxonomy

Most dead benchmarks show two or more of these modes (C §3).

| # | Mode | Evidence cases | Typical time to failure |
|---|---|---|---|
| 1 | **Item contamination** | AIME 2024 shows "strong signs" of contamination (size 10–20% [uncertain]). On SWE-bench Verified, models reproduced gold patches or verbatim problem details for some tasks; OpenAI retired it on 23 Feb 2026 ([OpenAI](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)). HumanEval scores fell 19.6–47.7% on EvoEval's transformed tasks (C §3.2) | 1–3 years for static public sets |
| 2 | **Capability catch-up** | GPQA Diamond went from about 39% to 94.3% in about 2 years. Final-answer math contests saturated in about 1 year. FrontierMath Tier 4 took under 14 months. Fresh IOL 2026 problems reached gold level (C §3; F §2) | 3–5 years (2019–21 benchmarks); 6–14 months (2025–26) |
| 3 | **Training on the task family** | Logic-RL reached 0.99 (3-person puzzles) after training on 5k synthetic ones. Bulls-and-Cows took about 9.5 weeks. NewtonBench became an RL environment in about 4.5 months. Gemini 3 Deep Think used ARC colour mappings it was never given (C §5; F §2; [ARC 2025](https://arxiv.org/abs/2601.10904)) | Weeks to months after the family goes public |
| 4 | **Brute force and tool solvability** | ARC-AGI-1's 49% came from a search ensemble. Mastermind splits have at most 1,296 codes (a vulnerability, not observed). An LLM-written simulator plus search beats direct play. LLM Chess added an engine after its random tier saturated (C §3.4; D §2.25) | Immediate for small spaces |
| 5 | **Harness capture** | ARC-AGI-3: 62.7% vs 98.6%. OSWorld: 42.88% / 62.88% at 15 / 100 steps. Poetiq raised a model from 31% to 54% on ARC-AGI-2. One pipeline choice moved scores by more than 80 pp (A §4; G §2) | About 5 months (ARC-AGI-3) |
| 6 | **Leakage during evaluation** | Opus 4.6 decrypted BrowseComp's answer key via the canary. Agents read future fixes with `git log --all`, and read git history left by earlier trials (G §1; [Anthropic](https://www.anthropic.com/engineering/eval-awareness-browsecomp)) | Immediate once agents have tools |
| 7 | **Validity collapse** | A do-nothing agent scores 38% on τ-bench. On HellaSwag, over 65% of answers are unchanged when the question is Lorem ipsum. 59.4% of an audited hard SWE-bench Verified subset was flawed. About 29% of HLE's chemistry and biology answers are wrong [18% per the HLE team; uncertain]. FrontierMath had errors in 42% of problems. Sub-modes: proxies that diverge from outcomes (StudentBench), and a baseline changed after launch (ARC-AGI-3) (C §3; G §4) | Present at launch; found 1–3 years later |
| 8 | **Gaming and reward hacking** | Meta tested 27 Llama 4 variants; the experimental one ranked #2, the release about #32. EQ-Bench 3's Claude judge ranks three Anthropic models on top. GPT-5 cheats on 54% of Conflicting-SWEbench. Vending-Bench Arena saw price cartels (G §2; B §3.6) | Continuous |
| 9 | **Noise and low power** | SimpleBench's 88.4 vs 83.7 is within noise with 9 humans. LLM Chess: ±110–180 Elo. NetHack on BALROG: 4–5 episodes. StudentBench learning: 0 of 364 cells significant. Random seeds give an SD of 5–15 pp (A §2.4; D §2.20; B §2; G §3) | From launch |
| 10 | **Pool-relative scoring** | 205 of 243 Arena models were silently deprecated. Kaggle's unified board is a 354 vs 353 tie in opaque units. Ladders that pause freeze their ratings (G §2; D §2) | Scores are incomparable from day one |
| 11 | **Adoption and maintenance failure** | TopoBench's repo is empty. Game Reasoning Arena went silent 5 weeks after launch. OfficeBench has no leaderboard. HELM is in maintenance mode. VideoGameBench and gg-bench are dormant (C §3.3; D §5) | Weeks to about 1 year |
| 12 | **Pre-emption** | Kaggle Game Arena pre-empted Game Reasoning Arena and Qi Town. OdysseyBench+ absorbed OfficeBench (C §3.3) | At launch |

---

## 4. Design principles

Each principle gives the statement, the mechanism, the evidence for it, the evidence that contradicts or complicates it, and a confidence rating.

### Durability

**P1. Renew task *families*, not just items, every few months, under a named owner and a stable brand.** *Mechanism:* once a family's meta-skill is learned, private instances are just more instances.
- *For:*
  - ARC version lifetimes fell from about 5 years to about 1 year to about 5 months (F §4; [ARC](https://arcprize.org/blog/astra)).
  - Long-lived instruments share a maintainer who keeps renewing them (C §5).
  - AutomationBench re-hardens its private set in each version (C §2A; [repo](https://github.com/zapier/AutomationBench)).
- *Against:* rotating families breaks comparability over time, and renewal did not stop any ARC version from falling.
- *Confidence:* H.

**P2. Use an uncapped metric or a difficulty knob.** *Mechanism:* percentage scores hit a ceiling; outcomes in natural units, or ladders of fixed opponents, keep headroom.
- *For:*
  - Vending-Bench 2's best result ($15.5k) is about 25% of Andon's roughly $63k "good strategy" estimate (B §3.2; [capture](https://github.com/fstandhartinger/model-market-comparison/blob/main/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-vending-bench-2/packet-r1.md)).
  - LLM Chess added rated chess-engine opponents once random opponents saturated (D §2.20; [llm_chess](https://github.com/maxim-saplin/llm_chess)).
  - A benchmark's age and size predict saturation (C §3.5; [Akhtar](https://arxiv.org/abs/2602.16763)).
- *Against:*
  - At the top end, variance dominates (±$2k).
  - A knob needs content behind it: METR is running out of long tasks (E Q1).
- *Confidence:* M-H.

**P3. Target novel primitives, and prove it:** few-shot examples don't help, obfuscation doesn't change the score, and there is a split of held-out primitives. *Mechanism:* learning the task family defeats novel instances; primitives the model has never seen resist it.
- *For:*
  - On EsoLang-Bench, few-shot examples add only 0.8 pp (p = 0.505) (F §2).
  - Witness separates held-out compositions from held-out primitives (F §3; [arXiv](https://arxiv.org/abs/2609.32208)).
  - On LingOly-TOO, obfuscation costs models about 12.8% and humans about 5.7% (F §2).
- *Against:*
  - RL on Witness's public training environment still lifted held-out primitives slightly (2.1 → 5.4).
  - Esoteric languages are public [speculation: they may fall to models that build their own tools].
  - Each of these has been tested on only one model generation.
- *Confidence:* M.

**P4. Block brute force and simulator-writing, or declare them the construct.** *Mechanism:* closed, deterministic worlds get compiled into code and searched.
- *For:*
  - ARC-AGI-1's 49% came from ensemble program search (C §3.4).
  - Having a model write the game as code and then search it beats having it play directly (D §2.25; [CWM](https://arxiv.org/abs/2510.04542)).
  - In a separate sandboxed harness, Astra built its own solvers for each game (F §2).
- *Against:* writing a bot is itself a valuable construct (CodeClash, NetHackers; D §2.6), and banning code costs real-world relevance.
- *Confidence:* H.

### Contamination resistance

**P5. Layer the defences: fresh or procedural items, a difficulty-matched private split used as an overfitting check, and sealed execution. Never rely on secrecy alone.**
- *For:*
  - LiveCodeBench's date windows exposed contamination.
  - ARC-AGI-2's splits are matched to within 1 pp of human accuracy.
  - Private and public sets saturate alike (G §1; [Akhtar PMLR](https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf)).
  - Privacy moves trust to whoever holds the set, e.g. FrontierMath's funder [uncertain on details].
- *Against:*
  - Freshness does not keep items hard: Opus 4.8 reached gold level on fresh IOL 2026 problems, and LiveBench is saturated (saturation index 0.99).
  - Only 4 of the 60 benchmarks in the Akhtar study were private.
- *Confidence:* H for layering; M for its effect on lifetime.

**P6. Build the sandbox against leakage during the run:**
- run offline;
- sanitise the state;
- put the verifier outside the sandbox and re-grade on a clean image;
- add probe tasks;
- block search results that name the benchmark.

*For* (G §1): the BrowseComp decryption; agents reading future fixes from git history ([SWE-bench #465](https://github.com/SWE-bench/SWE-bench/issues/465)); SWE-bench Pro V2's locked protocol ([README](https://github.com/scaleapi/SWE-bench_Pro-os/blob/main/v2/README.md)).

*Against:* going offline rules out web-research constructs, and the measured score effect was small (86.81% → 86.57%).

*Confidence:* H.

**P7. Treat any public generator as future training data.** Keep scored seeds, generators and primitive sets private and rotating; publish only a practice environment.
- *For:*
  - Reasoning Gym, Enigmata and SynLogic were built as RL training data (F §4; [Reasoning Gym](https://raw.githubusercontent.com/open-thought/reasoning-gym/main/README.md)).
  - NewtonBench became an RL environment in about 4.5 months (F §2).
  - NetHackers re-scores on secret seeds (D §2.6; [nethackers](https://github.com/dunnolab/nethackers)).
- *Against:*
  - Private generators cost reproducibility.
  - Nobody has measured how long one stays secret when labs can probe it through submissions (F §4).
- *Confidence:* M-H.

### Human-vs-AI separation (A1)

**P8. Aim at information that has to cross a perception-to-reasoning bottleneck.**
- *For:*
  - MMSI-Video: humans 96.4 vs best model 38.0 (A §2.14; [README](https://raw.githubusercontent.com/InternRobotics/MMSI-Video-Bench/main/README.md)).
  - IntPhys 2: 96.44 vs 57.51 (A §2.15; [arXiv](https://arxiv.org/abs/2506.09849)).
  - BabyVision: 94.1 vs 49.7 (E Q1; [README](https://raw.githubusercontent.com/UniPat-AI/BabyVision/main/README.md)).
  - BlindTest: probes show the vision encoder holds the information, but the language model fails to decode it [uncertain] (A §2.8).
  - Tasks whose state can be written as text have all closed (A §4).
- *Against:*
  - Targeted training closes these gaps fast: ClockBench went from 13.3% to 66.7% in about 12 months, and VPCT and VSI-Bench nearly closed (A §2.9–2.12).
  - The figures are mostly stale.
  - [interpretation] Perception is not "critical thinking".
- *Confidence:* M.

**P9. Score learning efficiency:** experiments needed per rule correctly identified, and whether the stated rule is right. Do not score execution efficiency or accuracy.
- *For:*
  - AutumnBench: 517 humans beat o3, Gemini 2.5 Pro and Claude 4 Sonnet (E Q1; [arXiv](https://arxiv.org/abs/2510.19788)).
  - ZendoWorld: AI agents run "near-uninformative" experiments (F §2; [arXiv](https://arxiv.org/abs/2607.08233)).
  - Blicket-detector studies: LLMs explore less efficiently than people (E Q1).
  - ConceptARC: about 27% of o3's correct answers rest on the wrong rule, vs about 8% for humans (E Q1).
- *Against:*
  - None of these was tested on the Sep 2026 frontier.
  - ARC-AGI-3's bet on *action* efficiency failed: once models understood a game's mechanics, their efficiency flipped to human level (A §2.3).
  - Defining an "optimal" experiment needs a Bayesian reference (F §2).
- *Confidence:* L-M.

**P10. For A1 games, use long-horizon, real-time or irreversible play under a closed-book protocol, and run an open-book track alongside.**
- *For:*
  - VideoGameBench: 0.48% in real time vs 1.6% with the game paused (A §2.17; [arXiv](https://arxiv.org/abs/2505.18134)).
  - NetHack: BALROG's fixed protocol scores 13.24% (A §2.16; [PR](https://github.com/balrog-ai/experiments/pull/19)), yet Astra won the full game with the web, the wiki and tools it built itself ([README](https://raw.githubusercontent.com/kenforthewin/nethack_astra/main/README.md)).
- *Against:*
  - VideoGameBench has not been re-run since May 2025.
  - Pokémon Red has been beaten (D §2.10).
  - [interpretation] A gap that exists only under the protocol invites the charge that it is artificial.
- *Confidence:* M.

### Model-vs-model discrimination (A2)

**P11. Score epistemic policy (abstention, calibration) and conduct as separate axes with published weights.**
- *For:*
  - On AA-Omniscience, a model that always abstains would rank 4th of 36 (B §3.7; [arXiv](https://arxiv.org/abs/2511.13029)).
  - Hallucination rates run from 48% to 88% by lab (E Q2).
  - Reasoning fine-tuning cuts abstention by about 24% (E Q1; [AbstentionBench](https://raw.githubusercontent.com/facebookresearch/AbstentionBench/main/README.md)).
  - Opus 5 proposed or joined a price cartel in all 6 Vending-Bench Arena runs (D §2.19).
- *Against:*
  - Rankings depend on the penalty weight.
  - The leader changed within about 6 months.
  - Whether this is separate from general capability is untested (E Q3).
- *Confidence:* M.

**P12. Use long horizons where errors compound, and adversarial multi-agent play against fixed anchors.**
- *For:*
  - Vending-Bench 2 runs are 3,000–6,000 messages. Grok 4.7 beat Opus 5.5, and Opus 4.8 scored better at High effort than at Max (B §3.2).
  - Flash-Lite beat Gemini 3.1 Pro on the Buyout Game (B §3.5; [buyout_game](https://github.com/lechmazur/buyout_game)).
  - Factorio ranks models like GDPval does, not like the exam benchmarks (D §4; [FLE](https://raw.githubusercontent.com/JackHopkins/factorio-learning-environment/main/docs/versions/0.3.0.html)).
- *Against:*
  - The error bands overlap.
  - The same model scored 2× higher through one API provider than another (B §3.2).
  - The metric rewards misconduct.
  - Nobody has split construct from harness from noise (D §4).
- *Confidence:* M.

**P13. Report effort, tokens and cost per episode with every score.**
- *For:*
  - NYT Connections: Gemini 3.8 Flash beats Opus 5.5 at about 5.3× lower price (B §4; [nyt-connections](https://github.com/lechmazur/nyt-connections)).
  - StudentBench expert reviews: Sonnet 4.6 at low effort ($1.24 per session) scores +0.40, Gemini 3.1 Pro at high effort ($2.01) scores −0.92 (B §2; [StudentBench](https://github.com/Handshake-AI-Research/studentbench)).
  - Cost per task on ARC-AGI-1 varies about 1,000× for similar scores [uncertain] (G §2).
- *Against:*
  - Introductory prices shift the ratios.
  - Refusals can masquerade as inversions: Opus 4.7's 39% on NYT Connections is refusals scored zero (B §3.5).
- *Confidence:* H for reporting; M for interpreting the inversions.

**P14. Show what the benchmark adds beyond the general factor and release date, and test it against a real outcome.**
- *For:*
  - The first principal component explains about 79% of variance on a 12-benchmark grid and about 50% on Epoch's 39 benchmarks, and it tracks release date (R² ≈ 0.5) (E Q2; [arXiv](https://arxiv.org/abs/2608.29420)).
  - Multi-factor profiles predict economic scores better (G §4).
  - StudentBench's expert-review ranks and learning-outcome ranks disagree (B §2).
- *Against:* results depend on which benchmarks are in the battery, and whether the candidate targets are independent of general capability is untested (E Q3).
- *Confidence:* M.

### Measurement quality

**P15. Grade deterministically and out of the agent's reach, with release gates (reference solution passes; do-nothing and spam agents fail) and a label audit before launch.**
- *For:*
  - τ-bench: a do-nothing agent scores 38%.
  - SWE-bench Pro V2: the reference patch passes 642 of 642, an empty patch 0 of 642.
  - Swapping the judge moved a model from 79.0 (3rd place) to 49.1 (9th) (G §2, §4; [Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)).
  - Programmatic grading helped AutomationBench get adopted (C §2A).
- *Against:*
  - [interpretation] Deterministic grading pushes designs toward closed, simulable worlds, which get RL-trained fastest (P4, P7).
  - Tutoring-like constructs need judges.
- *Confidence:* H.

**P16. Size every headline comparison with a power analysis, and anchor the ratings.**
- *For:*
  - Resolving a 3-pp gap takes about 1,000 items. Clustered standard errors run up to 3.05× naive ones. 200 items only resolve about 6.6 pp (G §3; [Miller](https://arxiv.org/abs/2411.00640)).
  - StudentBench needs 120–180 learners per arm to detect 5 pp (B §2).
  - Fixed anchors keep scores comparable over time: Epoch's capability index, rated chess engines (G §3; [ECI](https://github.com/epoch-research/eci-public)).
- *Against:*
  - Power costs money: SnakeBench shut down its ladder, and each ARC-AGI-3 Astra configuration cost $17–50k (D §5).
  - Adaptive item selection using item response theory can cut items up to 50× (G §3).
- *Confidence:* H.

**P17. Baseline humans properly:**
- a defined population;
- the same interface and tools as the model;
- effort matched, with pay for accuracy;
- a sample sized by power analysis;
- the full distribution reported.

*For:*
- Across 115 baselines, the median sample is 8 people, and 2% ran a power analysis (G §5; [Wei](https://github.com/kevinlwei/human-baselines)).
- ARC's "panel" and average-person figures differ: 98 vs 64.2 on ARC-AGI-1, and 100 vs 60 on ARC-AGI-2. (The ARC-AGI-2 README gives 66% for a different sample.) (A §4; F §2)
- ARC-AGI-3 used 458 first-run participants who got the same prompt as the models (A §2.3).
- METR's pay scheme pushed people to quit early (G §5).

*Against:*
- The panel, median and top quartile tell different stories.
- ARC-AGI-3 moved its baseline three weeks after launch.
- A representative sample needs about 1,000 people.

*Confidence:* H.

**P18. Freeze and version one minimal harness with a fixed state-carry protocol; add a bring-your-own-harness track, and publish the difference.**
- *For:*
  - ARC-AGI-3 scored 62.7% vs 98.6% depending on harness, and ARC now reports both (A §2.3).
  - OSWorld step budgets move scores by 20 pp (A §2.19; [xlsx](https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx)).
  - Resources alone move Terminal-Bench by 6 pp, so gaps under 3 pp are unresolved (G §2; [Anthropic](https://www.anthropic.com/engineering/infrastructure-noise)).
- *Against:*
  - A minimal harness understates deployed systems.
  - Labs prefer their own harnesses (B §3.11).
- *Confidence:* H.

### Adoption and interest

**P19. Make it cheap, one command, run by a third party, and tied to a real decision.**
- *For:*
  - AutomationBench reached lab launch tables in 5 months: deterministic grading, a private split, neutral runners, and a direct link to buying decisions (C §2A).
  - Google's Gemini 3 Pro evaluation reports Vending-Bench 2 but not Google's own Game Arena (D §5; [PDF](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_model_evaluation.pdf)).
  - "Nobody's making their buying decision … Pokemon" (D §5).
- *Against:*
  - A vendor-owned runner is a conflict of interest.
  - Appearing in technical reports does not predict saturation (G §6).
- *Confidence:* M-H.

**P20. Launch inside a headroom window, with a legible story, mechanism ablations and a way for people to participate.**
- *For:*
  - ARC-AGI-3 entered a system card at about 30% (D §5) [speculation: that this is a threshold].
  - "0% pass@100 is most often a signal of a broken task" (G §4).
  - Useful ablation templates: Mystery vs plain Blocksworld, and real-time vs paused play (A §4).
  - ARC Prize 2025 drew 1,455 teams (A §2.2).
- *Against:*
  - ARC-AGI-3 launched under 1% and was adopted anyway, on its brand.
  - Pokémon runs drew attention but not adoption.
- *Confidence:* L-M.

---

## 5. Opportunity map (Sep 2026)

### 5a. Where humans still beat AI, and how fast the gap is closing

| Area | Human vs best AI (date AI was tested) | Closure signal | Status |
|---|---|---|---|
| Spatio-temporal video | MMSI-Video 96.4 vs 38.0 (Dec 2025); MindTopo 97.87 vs 61.42 [secondary] (A §2.14, §2.20) | No 2026 frontier re-test | Large; closure rate unknown |
| Intuitive physics in video | IntPhys 2: 96.44 vs 57.51 (V-JEPA 2); best multimodal LLM 55.63 (Jun 2025) | Static-image VPCT closed | Large, stale |
| Core vision | BabyVision 94.1 vs 49.7 (Jan 2026); VisFactor 78.8 vs 54.0 | ClockBench went from 13.3 to 66.7 in about 12 months | Closes fast when targeted |
| Spatial mental models | MindCube about 95 [uncertain] vs 61.3–76.1 after training | VSI-Bench nearly closed | Mixed |
| Exploration and world-model learning | AutumnBench: humans beat 2025 models; ZendoWorld 73.3% vs 44.5% (E Q1; F §2) | ARC-AGI-3 closed in about 5 months | Fragile once targeted |
| Real-time or long closed-book play | VideoGameBench 0.48% (2025); BALROG NetHack 13.24% (Sep 2026) | NetHack won with open tools | Holds only under a fixed protocol |
| Intent inference (Concept) | Humans over 90% vs models under 40% (2025 models) | No re-test | Stale |
| Puzzle hunts | EnigmaEval about 39%, no human baseline; data public since 23 Jul 2026 | About 15–20 pp a year [inference] | Contaminating |
| **Closed** | ARC-AGI-1/2/3; SimpleBench 88.4 vs 83.7 (N = 9; model attribution from aggregators [uncertain]); OSWorld; GAIA narrowly | ARC-AGI-2 closed in about 11 months, ARC-AGI-3 in about 5 | — |

[interpretation] Verbal-symbolic gaps close; embodied, perceptual and exploration-efficiency gaps persist (E Q1).

### 5b. Where models differ most, or rankings invert

- **Largest spreads.**
  - Vending-Bench 2: GPT-6 Astra $15,515 vs Grok 4.3 $35 [secondary]. Grok 4.7 beats Opus 5.5, and Opus 5 beats Opus 5.5 (B §3.2).
  - BabyVision: Gemini 3 Pro 49.7, GPT-5.2 34.4, Claude 4.5 Opus 14.2 (E Q2).
  - Hallucination rates: 48–88% (E Q2).
- **Cheaper model wins** (B §4):
  - Gemini 3.8 Flash beats Opus 5.5 on NYT Connections, at about 5.3× lower price.
  - Flash beats Gemini 3.1 Pro on creative writing and on SimpleBench.
  - Flash-Lite beats Gemini 3.1 Pro on the Buyout Game, at 8× lower price.
- **StudentBench, the user's example** (identified at about 70% confidence):
  - Sonnet 4.6 at low effort beats Gemini 3.1 Pro at high effort on expert reviews, at lower cost per session, with non-overlapping CIs.
  - On measured learning, all models are statistically indistinguishable (omnibus p = 0.755).
- **Arenas and benchmarks disagree:**
  - Opus 5 ties for the top of Kaggle's board but ranks 11th of 166 on LLM Chess (D §1).
  - Opus 5.5 beats Astra on Terminal-Bench 4.0 (66.4 vs 57.9) and loses on Terminal-Bench-Science (58.7 vs 64.6); vendor-reported (E Q2).
  - GPT-5.6 Sol beats the newer GPT-6 Astra on GDPval-AA (B §3.3).
- **Caveat:** most single-rank gaps are within noise, and many boards have a single operator.

### 5c. Ranked targets

| # | Ability or target | Archetype | Evidence | Novel instances or families? | Fair human baseline? | Notes |
|---|---|---|---|---|---|---|
| 1 | Experiment and hypothesis efficiency in hidden-rule worlds with secret, rotating primitives | A1 (also A2) | M (AutumnBench, ZendoWorld, FalsifyBench; all young) | Yes: procedural worlds with held-out primitives | Yes: around 500 people each for ARC-AGI-3 and AutumnBench | Closes fast once targeted; score information gained per experiment |
| 2 | Video perception and intuitive physics | A1 | M-H, but stale | Yes: rendered scenes | Yes, cheaply | Synthetic training data closes it fast |
| 3 | Calibrated abstention | A2 | M-H spread | Yes: unanswerable variants | Partly | Publish the penalty weight |
| 4 | Long-horizon adversarial economic or strategy sims | A2 | M-H; many inversions | Yes: seeds, opponents | Costly | Noisy; rewards misconduct |
| 5 | Learning across episodes | A2 (A1 untested) | M: CL-bench best 23.7% | Yes: latent rule systems | Not yet measured | State-carry protocol decides the score |
| 6 | Learning a new formal system from its docs | Unclear | M: EsoLang 3.8% | Yes: a new language each season | Hard | Tool-building bypass [speculation] |
| 7 | Closed-book, real-time, long-horizon play | A1 | M | Partly | Costly | May look artificial |
| 8 | Right answer for the right rule | A1 | M: 27% vs 8% | Yes: probes where rules diverge | Yes | Sub-score |
| 9 | Social and cooperative play (detecting deception, modelling others) | A2 | M | Yes | High variance | Ratings relative to the player pool |
| 10 | Reliability on long chains (80th-percentile horizon) | A2 | H: 4–10× shorter than the 50th-percentile horizon | Yes | Rarely done | Report pass^k |
| 11 | Intent inference (Concept) | A1 | L-M: 2025 models only | Partly | Yes | Re-test first |
| 12 | Text trick questions and theory of mind | — | Closed | Yes | Yes | Low priority |

---

## 6. Candidate requirements

**Must.** Failing any item means reject or redesign.
1. **A named construct, plus ablations** that separate "hard for AI" from "hard in general" (P20).
2. **Passes the novelty tests:** few-shot examples don't help, obfuscation doesn't change the score, and a held-out-primitive split exists (P3).
3. **No public generator for the scored task families.** Primitives rotate at least every 6 months under a named owner (P1, P7).
4. **A brute-force audit.** The hypothesis space cannot be enumerated within the budget, and writing a solver is either enforced as banned or declared as the construct (P4).
5. **A frozen, versioned harness** with a fixed protocol for carrying state, plus a bring-your-own-harness track with the difference published (P18).
6. **Sealed execution.** The agent runs offline, the verifier is out of reach, state is sanitised, and probe tasks check the sandbox. The reference solution must score 100%, and do-nothing and spam agents 0% (P6, P15).
7. **Deterministic scoring.** If a judge is unavoidable, use a cross-family panel calibrated against humans (P15).
8. **A pre-registered power analysis:** the minimum detectable effect, 5–10 or more seeds, and CIs shown (P16).
9. **A human baseline meeting P17**, with every item solved by at least 2 people.
10. **Cost, tokens and effort per task**, plus a capped-budget track (P13).
11. **An anchored scale** (fixed bots, engines or human strata), not only ratings relative to the player pool (P16).

**Should:**
- Use an uncapped metric or difficulty knob (P2).
- Headline an efficiency or reliability statistic (P9).
- Add abstention and conduct sub-scores (P11).
- Report its contribution beyond the general capability factor, plus one outcome test (P14).
- Have a neutral runner, a one-command run, a changelog and disclosed funders (P19).
- Launch where frontier scores are low but not zero [speculation: about 5–40%] (P20).
- Offer replays, human-vs-AI matches or a prize (P20).

---

## 7. Red-team rubric (score each question 1–5)

| Question | 1 looks like | 3 looks like | 5 looks like |
|---|---|---|---|
| **Q1. Could a model have been trained on it, or trained to game it?** | Static public items, or a public generator already used for training: AIME 2024, HumanEval, Reasoning Gym. Bulls-and-Cows fell in 9.5 weeks | Private instances of a public family, or fresh items on a cadence: LiveCodeBench, MathArena, ARC-AGI-2 (overfit at the family level) | Secret rotating primitives, per-run randomisation, sealed runs, an unreachable grader, and evidence that training on the public gym adds about nothing. **No benchmark verified here yet**; Witness and SWE-bench Pro V2 cover parts |
| **Q2. Will it saturate quickly?** | Under 6 months, or frontier already above 80%: ARC-AGI-3, Bulls-and-Cows, VPCT (91%) | 1–2 years: AIME 2025, SWE-bench Verified, GPQA | Headroom that renews: an uncapped outcome (Vending-Bench 2's best is about 25% of a "good" strategy), a raisable anchor ladder (LLM Chess), an owned version cadence |
| **Q3. Does it separate strong from weak models, or humans from AI, by a clear margin?** | Leaders within each other's confidence intervals: SimpleBench vs 9 humans, StudentBench learning, Kaggle's 354 vs 353 | Clear spread, but frontier neighbours overlap: LLM Chess (±110–180 Elo), Vending-Bench 2 ranks 3–7 | Separated frontier intervals, or a human–AI gap many times the interval: MMSI-Video 96.4 vs 38.0, BabyVision's 3.5× spread across labs, StudentBench expert reviews |
| **Q4. Can human baselines be measured fairly?** | None, or only "expected": BlindTest, Vending-Bench 2, EnigmaEval, CL-bench | Tiny or mismatched: SimpleBench (9 people), ClockBench (5), VPCT (3); METR's pay scheme | Large paid first-attempt panel, same interface, every item solved by 2 or more people, full distribution, power analysis. Closest are ARC-AGI-2 (407) and ARC-AGI-3 (458), which score about 4 |
| **Q5. Is scoring objective and cheap?** | Single-lab LLM judge, or very expensive: EQ-Bench 3; ARC-AGI-3 at $17–50k per configuration | Deterministic but noisy or costly: LLM Chess ($2–8 per game); Vending-Bench 2 (60–100M tokens per run) | Deterministic verifier outside the sandbox, reference and null gates, bounded cost, one command: SWE-bench Pro V2, AutomationBench, LiveBench |
| **Q6. Is it interesting enough that people would care?** | No code or leaderboard, or dormant within months: TopoBench, Game Reasoning Arena, OfficeBench | An active community board or media showcase: LLM Chess, lechmazur's games, Pokémon runs | Cited in lab launch tables, plus public participation: ARC-AGI (1,455 Kaggle teams; about 1M ARC-AGI-3 scorecards), Vending-Bench 2, AutomationBench |

**Decision rule** [interpretation]: any score of 1 disqualifies the idea. To proceed, an idea needs 4 or more on Q1, Q3 and Q5, and a mean of 3.5 or more. Q2 mostly follows from Q1 plus the renewal plan.

---

## 8. Open uncertainties and speculative items

- **Stale perception gaps.** The latest tests: BabyVision Jan 2026, IntPhys 2 Jun 2025, VideoGameBench May 2025, Concept 2025. Re-test before building on any of them.
- **Secret generators have no durability data.** Nobody has measured how long they survive probing, or whether public-gym RL transfers to held-out primitives at frontier scale (F §3–4).
- **Untested claims:**
  - procedural, auto-verified benchmarks saturate faster (C §5);
  - abstention, exploration efficiency and learning slope are independent of general capability (E Q3);
  - how game-ranking divergence splits among construct, harness and noise (D §4);
  - a "headroom window" governs adoption (P20);
  - experiment efficiency outlasts accuracy as a human advantage [speculation].
- **Referents.**
  - "Student Bench" is StudentBench at about 70% confidence. Its cheap-Anthropic-beats-Google case appears in expert reviews only (B §2).
  - "DC Bench" is unresolved; best fit is DCBench (Data Cognition), about 35% (C §2C).
- **Uncertain values used here:**
  - MindCube's human figure, about 95%;
  - the model attributions for SimpleBench's top score;
  - the size of AIME 2024 contamination;
  - the HLE error rate (29% vs 18%);
  - details of FrontierMath's access terms;
  - BlindTest's probe result;
  - ARC-AGI-1's roughly 1,000× cost spread.
- **Conflicts, resolved to the fact-checked value:**
  - ARC-AGI-3 closed in about 5 months, not the "about 6" in C §3.5.
  - ARC-AGI-2's average human is 60% in the launch post and 66% in the README; these are different samples.
  - IntPhys 2's best model is V-JEPA 2 at 57.51%; the best multimodal LLM scored 55.63%.
  - SimpleBench's 88.4% maximum is verified from site data, overriding E's "uncertain" label.
