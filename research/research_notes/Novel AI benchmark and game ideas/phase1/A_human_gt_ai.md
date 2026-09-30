# Panel A: Benchmarks and games where humans still beat frontier AI (as of 30 Sep 2026)

**Evidence access (read first).** The egress proxy blocked most primary hosts (arcprize.org, arxiv.org, huggingface.co, simple-bench.com, epoch.ai, scale.com, `*.github.io`, lesswrong.com), and the shared search budget ran out after about 33 queries. Evidence tags:

- **[P]** primary, read directly: GitHub READMEs and data files via raw.githubusercontent.com, including the OSWorld-Verified spreadsheet, which I parsed myself.
- **[P-m]** primary text via a verbatim mirror or capture: arcprize.org pages captured 29 Sep 2026, ARC reports and posts, a translation of ARC's Astra post, and the Claude Opus 5 system card.
- **[S]** secondary: search-engine extracts of pages I could not open. Treat as medium or low confidence.
- **[I]** my inference; **[speculation]** as labelled.

Prior repo dossiers were used as leads only. Every number carried over was re-checked against [P]/[P-m], or is tagged [S] with its own URL.

---

## 1. Summary

- **The famous "human > AI" gaps in reasoning and agentic benchmarks have mostly flipped by Sep 2026.**
  - **ARC-AGI-1.** Frontier models match the human panel: Claude Opus 5 scores 97.5% against a 98% panel.
  - **ARC-AGI-2.** Claude Opus 5 scores 90.42% [P-m]. GPT-6 Astra is reported at 95.0% for $1.12/task [S]. The human panel solves 100%; the average test-taker scores 60%.
  - **ARC-AGI-3.** GPT-6 Astra scores 99.9% under the provider harness, taking fewer actions than the median human on 96% of levels [P-m].
  - **OSWorld.** Agents passed the 72.36% human rate on 11 Dec 2025, and the best agent reached 90.19% on 25 Jul 2026 [P].
  - **GAIA.** Top test-set entries of 93–95% sit above the 92% human baseline [S].
- **Near-parity, likely inside noise:**
  - SimpleBench: 81.9% (Claude Fable 5) against 83.7% for 9 humans [S].
  - WebArena: 74.3% against 78.24% [S].
  - VPCT: 91% against 100% [S].
- **Gaps that still hold, and hold by a lot, are perceptual, spatial, physical or real-time. Three clusters:**
  - **Fine-grained vision and spatial reasoning:**
    - VisFactor: humans 78.8% vs Gemini-3.1-Pro 54.0% [S].
    - MMSI-Video-Bench: 96.4% vs 38.0% [S].
    - MindCube: about 95% vs 61.3% after purpose-built training [P/S].
    - ClockBench: 89.1% vs 66.7% [S].
  - **Intuitive physics from video:** IntPhys 2 humans score about 96% while the best model scores about 57.5%, with chance at 50% [S].
  - **Real-time and long-horizon games under a fixed protocol:**
    - VideoGameBench: 0.48% completion [S].
    - BALROG NetHack progression: about 13% for GPT-6 Astra-Max [S].
- **Gaps with no clean human anchor but large headroom.**
  - EnigmaEval: best model about 39–44% [S], but there is no formal human baseline.
  - Concept (Gevers & Daelemans): humans >90% vs LLMs <40% [S], but the benchmark has not been re-run on 2026 frontier models.
- **What flipped each gap (strongest evidence first):**
  1. Test-time compute and RL-trained reasoning (o3 on ARC-AGI-1).
  2. Application-layer refinement loops and harnesses. Poetiq took Gemini 3 Pro on ARC-AGI-2 from 31% to 54% [P-m]. On ARC-AGI-3, the Provider Adapter harness took Astra from 62.7% to 98.6% at the same effort [P-m].
  3. Test-time training and program synthesis in the Kaggle track.
  4. Knowledge or format familiarity, which ARC calls "knowledge overfitting" [P-m].
  5. Agent scaffolds with step budgets and multiple rollouts (OSWorld) [P].
- **Harnesses and tools can decide a benchmark even when the model is unchanged.**
  - ARC-AGI-3: 62.7% vs 98.6% for the same model at the same effort [P-m].
  - OSWorld: Sonnet 4.5 scores 42.88%, 58.08% and 62.88% at 15, 50 and 100 steps [P].
  - NetHack: GPT-6 Astra *ascended* on 21 Sep 2026 using a harness it built itself, with web and wiki access, on its third attempt [P]. The protocol-constrained BALROG progression is still about 13% [S].
- **Speed of closure.**
  - ARC-AGI-1 took about 5 years to pass the average human.
  - ARC-AGI-2 took about 15 months to pass its 60% human average.
  - ARC-AGI-3 took 6 months to go from under 1% to human-level under a provider harness.
  - ClockBench went from 13.3% to 66.7% in about 12 months.
  - Durability is shrinking for anything with a verifiable, text-renderable state.
- **What still makes items hard, by mechanism:**
  - Backed by ablations:
    - Fine spatial detail is lost between vision encoder and language model: BlindTest linear probes succeed where the VLM fails, and accuracy nears 100% once shapes are spaced apart [S].
    - Removing lexical priors breaks planning: Mystery Blocksworld drops LLMs to 0–4% while a classical planner scores 100% [P].
    - Carrying state across long interactions: the ARC-AGI-3 harness ablation [P-m].
    - Parsing raw multimodal inputs: EnigmaEval drops from transcribed puzzles to raw PDFs [S].
  - Author claims only: sequential hypothesis revision and reading others' intent (Concept).
- **Weak human anchors are common.**
  - BlindTest's "100%" is an *expected* human accuracy, not a measured one [P].
  - SimpleBench rests on 9 people [S]; ClockBench on 5 [S]; VPCT on 3 volunteers [S].
  - ARC's "human panel" counts a task as solved if at least 2 people solved it. The *average* test-taker scores 60–64% on ARC-AGI-1/2 [P-m] and about 48% on ARC-AGI-3 [S].
- **New 2025–26 benchmarks with large gaps are mostly video, spatial or perceptual** (MMSI-Video-Bench, VisFactor v4, MindTopo, CityCube, SpatiaLab). None is yet a leaderboard that labs track.

---

## 2. Per-benchmark entries

### 2.1 ARC-AGI-1 (Chollet, Nov 2019)

#### Takeaway
ARC-AGI-1 is flipped and saturated. It took about 5 years to beat the *average* human (Dec 2024) and about 6.7 years to match the human *panel* (2026). The flip came from test-time compute plus RL-trained reasoning, with some tuning on ARC data.

#### Cited Findings
- **Human baselines.** The human panel (at least 2 humans solve each task) scores 98%, and the average human 64.2%, at $17/task. The table is in the ARC-AGI-2 launch post [P-m](https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md).
- **Kaggle history.**
  - An ensemble of all 2020 Kaggle entries reached 49%, a "brute-force" existence proof [P-m](https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2024/2412.04604v2_arc_prize_2024.md).
  - ARC Prize 2024 raised the private-set state of the art "from 33% to 55.5%", driven by "deep learning-guided program synthesis and test-time training". The ARChitects won the open-source prize at 53.5%. 1,430 teams submitted 17,789 entries [P-m](https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2024/2412.04604v2_arc_prize_2024.md).
- **o3-preview (Dec 2024).**
  - It scored 75.7% on the semi-private set within the $10k limit, and 87.5% with 172× compute.
  - OpenAI "trained the o3 we tested on 75% of the Public Training set" [P-m](https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/sources/o3_announcement.html).
- **Latest.** Claude Opus 5 scored 97.50% (verified by ARC Prize, max effort, Jul 2026) [P-m](https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md).
- **ARC's own framing.** ARC-AGI-1 "stayed unbeaten for so long, despite a 50,000x scaleup of base LLM pretraining" [P-m](https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-1/packet-r1.md).

#### Inferences
- Pretraining scale alone never flipped ARC-AGI-1. Four things did: test-time search and refinement, RL reasoning, test-time training, and familiarity with the ARC format.
- The "human 98%" figure is a *panel* ceiling. Against individual people, AI passed the median in Dec 2024.

#### Gaps
- The released o3's performance without ARC training was never cleanly isolated.

### 2.2 ARC-AGI-2 (launched 24 Mar 2025)

#### Takeaway
ARC-AGI-2 is flipped against the average human (60%) and above the 85% prize threshold on the commercial leaderboard, within about 15–18 months. The ARC Prize Kaggle track, with its compute limits, lagged far behind: 24% in Nov 2025.

#### Cited Findings
- **Human baseline.** More than 400 humans were tested live. Every task was solved by at least 2 humans in 2 attempts or fewer. The panel scores 100%, the average test-taker 60%, at $17/task [P-m](https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md).
- **Scores at launch.** "Pure LLMs score 0%," and reasoning systems scored in single digits: o3-preview-low 4%, o1-pro 1% [P-m](https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md).
- **Mechanism: ARC's analysis of frontier failures.** Systems struggled with three things [P-m](https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md):
  - **symbolic interpretation** ("failed to assign semantic significance to the symbols");
  - **compositional reasoning** (multiple interacting rules; single global rules are "consistently" found);
  - **contextual rule application.**
- **ARC Prize 2025 (Kaggle, 26 Mar–3 Nov 2025).** 1,455 teams and 15,154 entries; top score 24.03% (NVARC). The Grand Prize was unclaimed [P-m](https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md). The top-5 split was NVARC 24.03, ARChitects 16.53, MindsAI 12.64 [S](https://arcprize.org/blog/arc-prize-2025-results-analysis).
- **Refinement harness.** Poetiq's harness raised Gemini 3 Pro from 31% ($0.81/task) to 54% ($31/task). ARC verified the result [P-m](https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md).
- **Knowledge overfitting.** ARC's verification harness never mentions ARC or its colour format, yet Gemini 3 Deep Think "employs correct ARC color mappings". ARC asserts that "overfitting" is "now occurring with ARC-AGI-1 and ARC-AGI-2" [P-m](https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md).
- **2026 scores.**
  - Claude Opus 4.7 scored 75.83% and Claude Opus 5 90.42%, both at max effort and verified [P-m](https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md).
  - GPT-6 Astra is reported at 95.0% for $1.12/task [S](https://x.com/arcprize/status/2095597602545025138); [S](https://arcprize.org/results/openai-gpt-6-astra).
  - A 29 Sep 2026 capture of the official v2.json gives a maximum of 95 [P-m](https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-2/packet-r1.md) (via the prior dossier; the capture holds a summary, not the rows).

#### Inferences
- ARC's own diagnosis is that the *accuracy* gap became "primarily bottlenecked by engineering" while the *efficiency* gap remains science-limited [P-m, 2025 report].
- Accuracy-only human-gap claims have a short shelf life once a format is a lab target.

#### Gaps
- There is no independent per-task human-vs-AI error overlap analysis for 2026 models.
- Kaggle ARC-AGI-2 2026-track scores were not retrieved.

### 2.3 ARC-AGI-3 (interactive games; launched 25 Mar 2026) and ARC Prize 2026

#### Takeaway
ARC-AGI-3 is the only ARC version built on *action efficiency* against humans. It went from under 1% at launch to 30% (Jul) to 62.7% on ARC's Standard harness and 99.9% on the Provider Adapter harness (3 Sep 2026). Under the provider harness, GPT-6 Astra is *more* action-efficient than the median human. The binding constraint was mostly the harness's handling of memory and state, not raw model capability.

#### Cited Findings
- **Format.** 135 environments: 25 public-demo, the rest semi-private and private. There are "no instructions"; test-takers must "explore, infer the rules … and come up with a strategy" [P-m](https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md).
  - The grids are 64×64 and the actions are five moves, select and undo.
  - The action cutoff is 5× the human count.
  - The scoring metric, RHAE = (human actions / AI actions)², makes brute force score "near zero" (paper digest) [S](https://raw.githubusercontent.com/memgrafter/research-digests/491d1e597ee1384396057fbe72e2bdec9f11c2c6/ml_research_analysis_2026/2603.24621_arc-agi-3-a-new-challenge-for-frontier-agentic-intelligence_20260331_185732.md).
- **Human baseline (blog, 14 Apr 2026).**
  - 458 members of the general public took part in 90-minute in-person sessions under "first-run" conditions, with the same system prompt as the AI.
  - Every environment was beaten by at least 2 participants, "typically five or more, out of … around ten".
  - Per-environment solve rates vary; tr87 was solved by 6 of 12.
  - 342 replays were open-sourced [P-m](https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md).
  - **Conflict.** The technical report reportedly counts "486 unique participants … 2,893 total environment attempts". It also says "the average human tester scored 48%" [S](https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf).
- **Scoring change three weeks after launch.** The baseline moved from the 2nd-best human to the median human, and the per-level cap rose from 1.0× to 1.15× [P](https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx). ARC's reasons were a "luck factor" and a +0.5 pp effect for both humans and AI [P-m, blog capture].
- **Score trajectory.**
  - At launch, frontier models scored below 1% on the private set [S, paper digest].
  - In Jul 2026, Claude Opus 5 (high) reached 30.16%, "roughly four times the best previously reported score". GPT-5.6 Sol (max) scored 7.78% [P-m](https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md).
  - On 3 Sep 2026, GPT-6 Astra scored 62.7% on the Standard harness (max effort, about $26,098 per semi-private run) and 99.9% on the Provider Adapter harness (high effort, about $18,817). At max effort the two harnesses give 62.7% vs 98.6%.
    - Under the Provider Adapter, Astra used fewer actions than the median human on 96.0% of levels, and 51.7% fewer actions on average.
    - The Provider Adapter "preserves opaque reasoning state between requests" and compacts context. It was about 3.66× faster and used 49% fewer tokens [P-m translation](https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md).
- **Mechanism evidence from ARC.**
  - ARC expected that action efficiency "would remain the dividing line". It found instead a "binary pattern": "once it 'understands' the mechanics, execution usually falls within the human efficiency range". Brute-force paths remain inefficient.
  - Astra wrote compact symbolic world models and built custom tools. ARC notes that humans had no code interpreter [P-m translation](https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md).
  - OpenAI separately reported that "enabling two settings tripled" its ARC-AGI-3 scores [S](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/).
- **ARC Prize 2026 (Kaggle, internet off).**
  - There is an ARC-AGI-3 track and an ARC-AGI-2 track.
  - Two milestone prizes: 30 Jun and 30 Sep 2026 [S](https://arcprize.org/blog/arc-prize-2026-milestone-1).
  - Milestone 1 was won by Tufa Labs' "The Duck". It is a REPL- and tool-using harness that evicts old context ("infinite play") [S](https://arcprize.org/blog/arc-prize-2026-milestone-1); [P](https://raw.githubusercontent.com/Tufalabs/duck-harness/main/README.md).
- **Scale of play.** "Nearly one million scorecards" had been submitted on public environments by April [P-m].

#### Inferences
- ARC-AGI-3 fell because frontier models, *given persistent state*, can do the essential steps inside a text or code loop: form a hypothesis, test it, and compress it into a world model. The 36-point gap between harnesses shows that state and memory plumbing was the bottleneck.
- The "median-human efficiency" bar was beaten once exploration stopped being brute force.
- The average human (about 48% RHAE) is far below the "100% solvable" framing. That framing is a panel or existence claim.

#### Gaps
- Kaggle ARC-AGI-3 scores (Milestone 1 and 2 numbers) could not be retrieved.
- The cost policy is unresolved: the leaderboard says "Only systems <$10,000 … shown", yet Astra's run costs about $19–26k per run.
- The human-count conflict (458 vs 486) and the "48% average human" figure could not be checked against the report text.

### 2.4 SimpleBench (AI Explained; 2024)

#### Takeaway
SimpleBench is multiple-choice "trick" questions on everyday spatio-temporal, social and adversarial-wording reasoning. Its human-over-AI gap is now about 1.8 pp: humans 83.7% vs Claude Fable 5 at 81.9% (leaderboard of 10 Jun 2026). That is almost certainly within noise; the benchmark has effectively reached parity.

#### Cited Findings
- **Human baseline.** 83.7% "based on a sample of nine participants". Best model: Claude Fable 5 at 81.9%, then Gemini 3.1 Pro Preview 79.6% and GPT-5.5 Pro 76.9%. The leaderboard was updated 10 Jun 2026 [S](https://ai.miraheze.org/wiki/SimpleBench); [S](https://simple-bench.com/).
- **What it tests.** Spatio-temporal reasoning, social intelligence and "linguistic adversarial robustness (trick questions)" [S](https://ai.miraheze.org/wiki/SimpleBench).
- **Code.** The public repo ships only a small public set and a runner [P](https://raw.githubusercontent.com/simple-bench/SimpleBench/main/README.md).

#### Inferences
- The hardness driver is distractor-laden wording that invites pattern-completion to the "textbook" answer, not the physically or socially obvious one.
- RL-trained reasoning models learned to discount irrelevant detail, which closed most of the gap. This is inferred; no ablation was found.
- With about 200 private items and 9 humans, a gap under about 5 pp is not statistically meaningful [I].

#### Gaps
- No 2026 scores for Claude Opus 5 or GPT-6 Astra were found; simple-bench.com was blocked.
- No item-level error analysis was found.

### 2.5 Concept (Gevers & Daelemans; arXiv 2510.13271, Oct 2025; Findings of ACL 2026)

#### Takeaway
Concept is a word-guessing board game that probes abductive reasoning from sequential icon hints. Humans succeed >90% of the time; no LLM tested exceeded 40%. It is one of the largest text-only human-over-AI gaps, but it has not been run on 2026 frontier models.

#### Cited Findings
- The authors describe the game as "easily solved by humans with a success rate of over 90%" yet hard for LLMs, "with no model exceeding 40% success rate" [S](https://aclanthology.org/2026.findings-acl.1219/); [S](https://arxiv.org/abs/2510.13271).
- **Failure modes (author claims).**
  - LLMs "struggle with interpreting other players' strategic intents" and "with correcting initial hypotheses given sequential information updates".
  - Performance drops further in Dutch, French and Spanish [S](https://aclanthology.org/2026.findings-acl.1219/).

#### Inferences
- The hardness drivers are theory-of-mind-style intent reading and belief revision under incremental evidence. Both resist "think longer" fixes more than deduction does [speculation until 2026 models are tested].

#### Gaps
- The model list, human N, item count and whether reasoning models were included were all not visible.
- There is no ablation separating hint grammar from world knowledge.

### 2.6 EnigmaEval (Scale AI / CAIS / MIT; Feb 2025)

#### Takeaway
EnigmaEval consists of 1,184 puzzle-hunt puzzles, long and multimodal, with no instructions. Its launch SOTA was 7% (normal split) and 0% (hard split). Mid-2026 SOTA is about 39–44%. There is **no formal human baseline**: the "human > AI" claim rests on puzzle-hunt teams solving these puzzles in competition.

#### Cited Findings
- The benchmark draws 1,184 puzzles from 8 competitions. At launch, o1 scored 7.0% on normal puzzles and 0% on hard ones, "far short of experienced human puzzle hunters" [S](https://arxiv.org/abs/2502.08859).
- **Mechanism evidence.** Performance "could drop dramatically from the transcribed puzzles to their original PDF versions", which the authors read as OCR and parsing limits [S](https://arxiv.org/abs/2502.08859).
- **Scale SEAL (current as of the search).** claude-fable-5-high 39.28±2.80, gpt-5.6-sol-high 37.12, gemini-3.1-pro-preview-high 36.78 [S](https://labs.scale.com/leaderboard).
  - As of 6 May 2026 the leader was gpt-5.4-pro at 23.82 [S](https://benchmarklist.com/benchmarks/enigma_eval/).
  - The "CAIS dashboard" reports Claude Opus 5 at 43.9% (Jul 2026) [S, dashboard URL not retrieved].

#### Inferences
- Two things drive the hardness:
  1. **Extracting the task itself.** No stated goal; an "aha" mapping must be discovered.
  2. **Raw multimodal parsing.**
- The benchmark is closing at roughly 15–20 pp a year [I from 7% → about 40% in about 17 months].

#### Gaps
- There is no team-hour-normalised human baseline, and no hard-split scores for 2026 models.

### 2.7 PlanBench / Mystery Blocksworld (Valmeekam et al., 2022–)

#### Takeaway
Obfuscating predicate names ("Mystery" Blocksworld) collapsed non-reasoning LLMs to about 0%, while a classical planner stays at 100%. Reasoning models recovered only partially: o1-preview 52.8%, DeepSeek R1 43.3%. Human evidence exists only for plain Blocksworld.

#### Cited Findings
- **Official leaderboard** (zero-shot, 600 instances each) [P](https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md):

  | Model | Blocksworld (NL) | Mystery Blocksworld | Randomized Mystery |
  |---|---|---|---|
  | GPT-4o | 35.5% | 0% | – |
  | Claude-3.5 Sonnet | 54.8% | 0% | – |
  | o1-preview | 97.8% | 52.8% | 37.3% |
  | DeepSeek R1 | 99.1% | 43.3% | 25.8% |

- **Humans.** In a study of 50 participants on a Blocksworld instance, 78% produced a valid plan. The classical planner Fast Downward solves 100% [S](https://www.emergentmind.com/topics/planbench); [S](https://arxiv.org/pdf/2305.15771).

#### Inferences
- The obfuscation ablation is clean mechanistic evidence: success depends on familiar surface forms, not on combinatorial difficulty (a solver finds it trivial).
- This is a "lexical-prior removal" hardness driver [I].

#### Gaps
- No leaderboard rows exist for o3, GPT-5.x or 2026 models, so the current status is unknown.
- There is no human baseline on the Mystery variants.

### 2.8 BlindTest, "VLMs are blind" (Auburn/Alberta; ACCV 2024; journal v6)

#### Takeaway
BlindTest is seven trivially easy geometric tasks: counting line intersections, touching circles, circled letters, counting nested squares and so on. VLMs averaged about 58% against an *expected* human 100%. The paper gives strong mechanistic evidence: the information is present in the vision encoder but lost when the language model decodes it.

#### Cited Findings
- Four state-of-the-art VLMs averaged 58.12%; Claude 3.5 Sonnet was best at 74.94%, "far from the human expected accuracy of 100%" [P](https://raw.githubusercontent.com/anguyen8/vision-llms-are-blind/main/README.md).
  - Models "consistently struggle with tasks that require precise spatial information and recognizing geometric primitives that overlap or are close together" [P](https://raw.githubusercontent.com/anguyen8/vision-llms-are-blind/main/README.md).
  - Line intersections: GPT-4o 48.67%, Sonnet-3.5 77.33% (README table).
- **Journal version** ("Failing to translate detailed visual features into words"):
  - The average is 58.07%, with the best (Sonnet-3.5) at 77.84%.
  - "Linear probing … show[s] that vision encoders contain sufficient visual information", but language models "fail to decode" it.
  - Accuracy is "near-100%" when "much more space is added to separate shapes" [S](https://arxiv.org/abs/2407.06581).

#### Inferences
- The hardness drivers are crowding and fine localisation at the encoder-to-LLM interface, not concept knowledge.
- Items where primitives are close together or overlap are the durable core [I].

#### Gaps
- The human baseline was not measured.
- No 2026 frontier scores on BlindTest were found. A follow-up, "VLMs are Biased" (arXiv 2505.23941), was seen but not read.

### 2.9 ClockBench (Alek Safar; Sep 2025)

#### Takeaway
ClockBench asks models to read analog clocks. Humans scored 89.1% (5 people). The best model was at 13.3% at launch and at 66.7% a year later (GPT-5.6 Sol Max). The gap is closing fast but is still about 22 pp.

#### Cited Findings
- The benchmark has 180 custom clocks and 720 questions. Humans scored 89.1%; Gemini 2.5 Pro 13.3% and Gemini 2.5 Flash 10.5% [S](https://the-decoder.com/even-the-best-ai-models-cant-reliably-read-the-clock/).
- **Error structure (launch).** Accuracy fell to 3.2% with Roman numerals and 4.5% with circular numerals. Second hands, coloured backgrounds and mirrored layouts also hurt. Hour-hand-only clocks were easiest at 23.6% [S](https://the-decoder.com/even-the-best-ai-models-cant-reliably-read-the-clock/).
- **2026.** "A year on it manages 66.7%. The top model, GPT-5.6 Sol Max" [S](https://theslowai.substack.com/p/ai-clock-benchmark-capacity).
- The public set is 10 of 180 clocks, and "Full dataset … intentionally kept private" [P](https://raw.githubusercontent.com/aleksafar/clockbench/main/README.md).

#### Inferences
- The hardness driver is precise angle and hand localisation plus robustness to style variation. Numeral style changes the score by about 4×.
- Fast improvement suggests that post-training on synthetic clock or gauge data works [speculation].

#### Gaps
- The human N is tiny (5).
- No 2026 per-condition error analysis was found.

### 2.10 VPCT, Visual Physics Comprehension Test (Chase Brower; 2025)

#### Takeaway
VPCT has 100 images; the task is to predict which bucket a ball rolling down ramps falls into. Humans (3 volunteers) scored 100%. Models went from about 66% (GPT-5 high) to 91% (Gemini 3 Pro). It is close to saturation.

#### Cited Findings
- The benchmark has 100 problems, and "a set of three volunteers all scored 100%". GPT-5 (high) scored 66% [S](https://epoch.ai/benchmarks/vpct).
- Gemini 3 Pro scores 91.0% and GPT-5.2 84.0% [S](https://llmlearner.com/rankings/vpct).
- The runner and leaderboard pointer are on GitHub [P](https://raw.githubusercontent.com/camelCase12/vpct-runner/main/README.md).

#### Inferences
- VPCT tests single-image trajectory simulation (collision and ramp geometry).
- It closed quickly, which is consistent with reasoning models doing explicit geometric simulation in chain of thought [I].

#### Gaps
- No 2026 scores (Opus 5, Astra) were retrieved, and cbrower.dev was blocked.

### 2.11 VisFactor (arXiv 2502.16435; v4 2026)

#### Takeaway
VisFactor digitises 20 vision-centric subtests from the FRCT psychometric battery. Humans (university participants) score 78.8% and the best of 39 MLLMs (Gemini-3.1-Pro) 54.0%, a 24.8 pp gap. Humans lead on nearly every subtest.

#### Cited Findings
- The 20 subtests span 4 domains. Humans score 78.8% and Gemini-3.1-Pro 54.0%.
- Humans win "nearly all subtests except RL2 (Diagramming Relationships)", where textual object knowledge helps [S](https://arxiv.org/html/2502.16435v4).

#### Inferences
- The psychometric factors (closure, spatial relations, visualisation, perceptual speed) isolate perception from knowledge. That is why the gap persists [I].

#### Gaps
- The human N and the per-factor gap sizes were not seen.

### 2.12 VSI-Bench, "Thinking in Space" (NYU; Dec 2024; CVPR 2025 oral)

#### Takeaway
VSI-Bench asks video-based 3D spatial questions: counts, distances, sizes, route plans and appearance order. Humans average 79%. At launch, humans beat the best model by about 33 pp. By 2026, spatially fine-tuned models reach about 74%. The gap is nearly closed, via domain training.

#### Cited Findings
- Humans score 79% on average, "outperforming the best model by 33%". Human accuracy on configuration and spatiotemporal tasks is 94–100%, but the gap is "much narrower on measurement tasks" (absolute distance and size) [S](https://arxiv.org/pdf/2412.14171).
- The launch evaluation covered 15 video MLLMs, including Gemini-1.5 and GPT-4o [P](https://raw.githubusercontent.com/vision-x-nyu/thinking-in-space/main/README.md).
- SSR-3D scores 73.9, beating InternVL3.5-241B by 4.4 points [S](https://arxiv.org/pdf/2603.00409).

#### Inferences
- Humans are imprecise at metric estimation, so the human ceiling is only 79%. That lets specialised models close the gap without human-like spatial models [I].
- The *relational and configurational* subsets (humans 94–100%) are the durable part.

#### Gaps
- No general frontier-model (Opus 5, Astra, Gemini 3.x) scores were found. Whether debiased or blind-baseline variants change the picture was not checked.

### 2.13 MindCube (Northwestern et al.; Jun 2025)

#### Takeaway
MindCube tests building a spatial mental model from a few views (perspective-taking and "what-if" movement). VLMs are "near-random". Purpose-built map-then-reason SFT plus RL reaches only 61.3%, against a human level of about 95%.

#### Cited Findings
- The benchmark has 21,154 questions over 3,268 images, and "existing VLMs show near-random performance".
- "Map-then-reason" (generate a cognitive map, then reason over it) improves accuracy from 37.8% to 57.8%, and RL raises it to 61.3%. These numbers are from the Mar 2026 code and data update [P](https://raw.githubusercontent.com/mll-lab-nu/MindCube/main/README.md).
- The human ceiling is about 95%. The v1 numbers were 60.76% for SFT and 70.67% for SFT plus RL, which differ from the updated README [S](https://www.emergentmind.com/topics/mindcube-benchmark).

#### Inferences
- The scaffold ablation is mechanistic evidence: forcing an explicit allocentric map helps a lot. This implies that frontier VLMs lack a persistent internal spatial representation [I].

#### Gaps
- Scores for 2026 frontier models were not retrieved.

### 2.14 MMSI-Video-Bench (arXiv 2512.10863; Dec 2025)

#### Takeaway
MMSI-Video-Bench is a human-annotated video spatial-intelligence benchmark covering construction, motion, planning, prediction and cross-video reasoning. Humans score 96.4% and the best model (Gemini 3 Pro) 38.0%, one of the largest current gaps.

#### Cited Findings
- Humans score 96.4% and Gemini 3 Pro 38.0% [S](https://arxiv.org/pdf/2512.10863).

#### Inferences
- Multi-video, temporal and spatial integration compounds the MindCube and VSI failure modes [I].

#### Gaps
- 2026 frontier scores and a per-category breakdown are missing.

### 2.15 Physical reasoning: IntPhys 2, Physics-IQ, Physion, PHYRE

#### Takeaway
Intuitive physics from video remains a large gap. On IntPhys 2, humans score about 96% while the best model scores about 57.5% and MLLMs sit near chance. Generative video models are far from physical realism on Physics-IQ.

#### Cited Findings
- **IntPhys 2** (Meta FAIR, Jun 2025).
  - Design: violation-of-expectation videos testing permanence, immutability, spatio-temporal continuity and solidity. Unreal Engine 5; 1,012-video main set plus a 344-video held-out set whose metadata is withheld [P](https://raw.githubusercontent.com/facebookresearch/IntPhys2/main/README.md).
  - Scores: humans 96.44% overall (92.44% on held-out). Most models are at 52–54% (chance is 50%). V-JEPA 2 is best at 57.51%. Gemini 2.5 Flash is near chance except about 64% on the easy set [S](https://www.emergentmind.com/topics/intphys-2); [S](https://arxiv.org/html/2506.09849v1).
- **Physics-IQ Verified** (DeepMind), physical realism of video generation.
  - The ceiling of 100 is defined by physical variance.
  - Best scores are 58.2 (Magi-1 24B + GeoPhys best-of-N, v2v, Jun 2026) and 48.2 i2v (Physis-Lang/Cosmos3-Super, 28 Sep 2026). Veo 3.1 Fast scores 29.96 [P](https://raw.githubusercontent.com/google-deepmind/physics-IQ-benchmark/main/README.md).
- **Physion** (NeurIPS 2021) compares humans and models on the same physical-prediction stimuli, with training protocols of "only", "all" and "all-but-one" scenarios [P](https://raw.githubusercontent.com/cogtoolslab/physics-benchmarking-neurips2021/master/README.md).
- **PHYRE** is an agent physics-puzzle benchmark; it points to the human-comparable "Virtual Tools" [P](https://raw.githubusercontent.com/facebookresearch/phyre/main/README.md).

#### Inferences
- The hardness driver is temporal object tracking and violation detection, not static geometry. VPCT, a *static* image, closed; video VoE did not [I].
- The original IntPhys was saturated by V-JEPA at 98.3% [S], a reminder that synthetic-physics sets fall once targeted.

#### Gaps
- No 2026 IntPhys 2 held-out leaderboard values were retrieved (the HF space was blocked).
- Physics-IQ has no human baseline.
- No LLM or VLM numbers were re-verified for Physion or PHYRE.

### 2.16 BALROG / NetHack (UCL et al.; Nov 2024; ICLR 2025)

#### Takeaway
Under BALROG's fixed protocol, NetHack progression stayed near floor until 2026. GPT-6 Astra-Max reached about 13.2%. Yet on 21 Sep 2026, Astra *ascended* (won) NetHack using a harness it built itself, with wiki and web access, on its third attempt. The protocol-constrained gap persists; the unconstrained gap closed.

#### Cited Findings
- BALROG evaluates agentic LLMs and VLMs "on long-horizon interactive tasks using reinforcement learning environments" [P](https://raw.githubusercontent.com/balrog-ai/BALROG/main/README.md).
- **NetHack progression scores.**
  - The BALROG leaderboard lists GPT-6-Astra-Max at 13.2 ± 2.7% (entry dated 18 Sep 2026) [S](https://www.sota2.com/research/sota/long-horizon-game-playing-on-balrog-nethack).
  - Earlier independent results: BRAID fork with Claude Opus 4.5 at 6.96%, and GPT-5.2 at 12.56% (reaching dungeon level 10) [S](https://kenforthewin.github.io/blog/posts/nethack-agent/).
- **The ascension.** CodexDelver, played by GPT-6 Astra via a remote terminal on Hardfought, ascended in NetHack 3.6.7 on 21 Sep 2026: 37,140 turns and 1,766,446 points.
  - Conditions: "The agent could consult the web, wiki and public source, write helpers, and keep persistent memory".
  - The authors state it "was not a BALROG-protocol evaluation or a win-rate study" [P](https://raw.githubusercontent.com/kenforthewin/nethack_astra/main/README.md).

#### Inferences
- NetHack's difficulty for LLMs came from three sources: (a) enormous tacit game knowledge; (b) state tracking over tens of thousands of turns; (c) irreversible death.
- Web or wiki access plus self-written tools and memory removes (a) and much of (b). The remaining gap is about *learning in-episode without external knowledge* [I].

#### Gaps
- The human-expert BALROG progression baseline was not found.
- The overall BALROG top scores for 2026 were not verified.

### 2.17 VideoGameBench (May 2025)

#### Takeaway
VideoGameBench has VLMs play 1990s games from raw pixels in real time. The best models completed 0.48% (1.6% on the paused "Lite" variant). It is one of the most durable gaps on record, but no 2026 update was found.

#### Cited Findings
- Gemini 2.5 Pro and Claude 3.7 Sonnet "complete only 0.48% of VideoGameBench and 1.6% of VideoGameBench Lite" and reach only "the first checkpoint in a single game".
- The Lite variant pauses the game while waiting for the model, and performance "improved slightly" [S](https://arxiv.org/abs/2505.18134).
- The harness supports checkpoint-image progress tracking [P](https://raw.githubusercontent.com/alexzhang13/videogamebench/main/README.md).

#### Inferences
- The latency ablation (real-time vs paused) shows that reaction time is *part* of the gap but not most of it. The rest is visual grounding and long-horizon credit assignment [I].

#### Gaps
- No 2026 scores and no formal human baseline were found (humans routinely finish these games).

### 2.18 Pokémon runs (Claude Plays Pokémon, Gemini Plays Pokémon)

#### Takeaway
Pokémon became an informal human-over-AI showcase. Claude needed about 140 hours for 3 badges in 2025. Claude Opus 4.7 finally beat Pokémon Red in May 2026. On 23 Sep 2026 a non-LLM decision model (Jev) beat Red "in under a week", with Claude Opus 5 as coach.

#### Cited Findings
- An early-2025 3-badge run took "perhaps 140 hours", with 78 hours spent escaping Mt. Moon in run #2.
- Claude Opus 4.7 beat Pokémon Red in May 2026; "the Elite 4 did take a couple tries" [S](https://www.lesswrong.com/posts/sehJYg5Yny9fvpbpt/a-year-late-claude-finally-beats-pokemon).
- TypeSafe AI's Jev "entered the Hall of Fame on September 23, 2026", with Claude Opus 5 "monitoring the game log and adjusting options" [S](https://www.tomshardware.com/tech-industry/artificial-intelligence/developer-says-jev-decision-model-beat-pokemon-red-in-under-a-week-non-llm-engine-succeeds-where-traditional-chatbots-stalled-for-months-but-claude-opus-5-coached-the-model-through-its-dead-ends).

#### Inferences
- The drivers are spatial navigation from screenshots, memory across hundreds of hours, and self-correction of wrong beliefs.
- Harness differences make runs incomparable. This is a showcase, not a benchmark [I].

#### Gaps
- Gemini's 2025 Pokémon Blue completion and its harness details were not re-verified this session.
- There is no controlled human playtime baseline.

### 2.19 Computer use and web: OSWorld (and 2.0), WebArena, GAIA

#### Takeaway
- **OSWorld flipped.** Agents passed humans on 11 Dec 2025 (multi-rollout) and 25 Feb 2026 (single rollout), and reached 90.19% in Jul 2026.
- **GAIA flipped** on the test set (secondary sources).
- **WebArena is within about 4 pp** of its human figure.
- **OSWorld 2.0** (Jun 2026) resets headroom with long tasks, but no human success rate was found.

#### Cited Findings
- **OSWorld launch.** "Humans can accomplish over 72.36% of the tasks" [P](https://raw.githubusercontent.com/os-world/os-world.github.io/main/index.html).
- **Official OSWorld-Verified results** (my parse of the xlsx; 144 scored entries) [P](https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx):
  - First above human: Agent S3 w/ Opus 4.5 + GPT-5 bBoN (N=10) at 72.58% (2025-12-11).
  - First single-rollout entry above human: HIPPO Agent w/ Opus 4.5 at 74.48% (2026-02-25).
  - Best: Intelligence-Indeed Agent at 90.19% (325.59/361, 2026-07-25).
  - Claude Fable 5 scores 85.96%.
  - 16 entries are at or above 72.36%.
  - Step budget: Sonnet 4.5 scores 42.88%, 58.08% and 62.88% at 15, 50 and 100 steps.
- **OSWorld 2.0.** 108 long-horizon tasks; the median task takes a skilled human about 1.6 hours of active operation.
  - GPT-6 Astra scores 72.6% and Opus 5 70.6% [S](https://snorkel.ai/leaderboard/os-world-2-0/).
  - Opus 5 scores 70.57% (500 steps, 5-run average) [P-m](https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md).
- **WebArena.** Humans 78.24%, GPT-4 14.41% at launch. Best in 2026: WebTactix (DeepSeek v3.2) at 74.3% (Feb 2026) [S](https://leaderboard.steel.dev/leaderboards/webarena/). The repo links a Google-Sheets leaderboard and human trajectories on about 170 tasks [P](https://raw.githubusercontent.com/web-arena-x/webarena/main/README.md).
- **GAIA.** Humans 92% vs GPT-4 with plugins 15% at launch.
  - Test-set leader: CustomGPT.ai Research Lab v44 at 93.36% (15 Jul 2026) [S](https://leaderboard.steel.dev/leaderboards/gaia/).
  - Agents-A1-4B at 95.1% (10 Sep 2026) [S](https://benchlm.ai/benchmarks/gaia).

#### Inferences
- The computer-use gap closed through scaffolds (step budgets, best-of-N, hybrid planners), not through a single model crossing a threshold. The step-budget effect alone is 20 pp.
- The human anchors, measured in 2023–24 by non-specialist annotators, are now stale [I].

#### Gaps
- There is no human success-rate baseline for OSWorld 2.0.
- The official GAIA HF leaderboard was blocked, so the [S] figures are unverified. An aggregator's "Qwen3.8 Max 86.1% leads OSWorld-Verified" conflicts with the official xlsx (90.19%).

### 2.20 Other new 2025–26 "large human > AI gap" benchmarks (leads)

These are leads only, found by search:
- **SpatialViz-Bench:** humans 90%+ vs Gemini-2.5 Pro 44.7% [S, from a search summary; the source paper was not identified].
- **CityCube** (ACL 2026; cross-view spatial reasoning, 5.0K QA over 59 tasks) [S](https://aclanthology.org/2026.acl-long.416.pdf).
- **SpatiaLab** (arXiv 2602.03916): models about 50–55% on multiple choice vs humans >85%, and about 40% vs about 65% open-ended [S](https://arxiv.org/pdf/2602.03916).
- **MindTopo** (arXiv 2609.11900, Sep 2026): a prior repo dossier reports GPT-5.6-Sol at 61.42% vs 97.87% for humans, from full-text mirrors. **Not re-verified here**; treat as L.

---

## 3. Summary table

| Benchmark | Launched | Human score (baseline type) | Best AI (model, date) | Trend | Main hardness driver |
|---|---|---|---|---|---|
| ARC-AGI-1 | Nov 2019 | 98% panel (≥2 solvers); 64.2% avg person | Claude Opus 5 97.5% (Jul 2026, verified) [P-m] | **Flipped** (avg person Dec 2024; panel parity 2026) | Few-shot novel abstraction; fell to TTC/RL reasoning, TTT, format familiarity |
| ARC-AGI-2 | Mar 2025 | 100% panel; 60% avg person; $17/task | GPT-6 Astra 95.0% @ $1.12 (Sep 2026) [S]; Opus 5 90.42% [P-m] | **Flipped** in ~15–18 mo | Symbolic interpretation, compositional and contextual rules; fell to refinement harnesses and reasoning scale |
| ARC-AGI-3 | Mar 2026 | 100% of games solved by ≥2 of ~10 people; avg person ~48% RHAE [S] | Astra 99.9% (Provider Adapter) / 62.7% (Standard) (3 Sep 2026) [P-m] | **Flipped under provider harness** in 6 mo | Exploration, goal inference, state/memory over long play; harness decided it |
| ARC Prize Kaggle | 2020– | – | 2024: 55.5%; 2025: 24.03% (ARC-AGI-2) [P-m] | Lags frontier APIs | Compute-limited, offline |
| SimpleBench | 2024 | 83.7% (9 people) [S] | Claude Fable 5 81.9% (Jun 2026) [S] | **Near parity** | Trick wording and distractors; everyday physics and social reasoning |
| Concept | Oct 2025 | >90% [S] | <40% (2025 models) [S] | Unknown (no 2026 run) | Intent reading, sequential hypothesis revision |
| EnigmaEval | Feb 2025 | None formal (hunt teams) | Opus 5 43.9% (Jul 2026, CAIS) / Fable 5 39.3% (SEAL) [S] | Closing ~15–20 pp/yr | Goal discovery, raw multimodal parsing, long chains |
| PlanBench Mystery BW | 2022/2023 | 78% of 50 (plain BW only) [S] | o1-preview 52.8% (2024) [P] | Unknown after 2024 | Lexical-prior removal |
| BlindTest | Jul 2024 | "Expected" 100% (not measured) [P] | Sonnet-3.5 ~75–78% (2024) [P/S] | Unknown | Encoder-to-LLM loss of fine spatial detail; crowding |
| ClockBench | Sep 2025 | 89.1% (5 people) [S] | GPT-5.6 Sol Max 66.7% (~Sep 2026) [S] | Closing fast | Hand/angle localisation, style robustness |
| VPCT | 2025 | 100% (3 volunteers) [S] | Gemini 3 Pro 91% [S] | Near saturated | Trajectory simulation from one image |
| VisFactor | 2025 (v4 2026) | 78.8% (univ. participants) [S] | Gemini-3.1-Pro 54.0% [S] | Durable (so far) | Psychometric visual factors |
| VSI-Bench | Dec 2024 | 79% avg [S] | SSR-3D 73.9 (Mar 2026, specialised) [S] | Nearly closed via spatial training | Relational 3D from video; humans weak on metric estimates |
| MindCube | Jun 2025 | ~95% [S] | 61.3% (trained, Mar 2026) [P] | Durable | No persistent allocentric map |
| MMSI-Video-Bench | Dec 2025 | 96.4% [S] | Gemini 3 Pro 38.0% [S] | Large, new | Multi-video spatio-temporal integration |
| IntPhys 2 | Jun 2025 | 96.44% (92.44% held-out) [S] | V-JEPA 2 57.51% [S] | Durable | Violation-of-expectation physics in video |
| Physics-IQ | 2025 | No human (physical-variance ceiling 100) | 58.2 v2v (Jun 2026) [P] | Slow | Physical realism in generation |
| BALROG NetHack | Nov 2024 | Expert humans ascend (no % given) | Astra-Max 13.2% progression (Sep 2026) [S]; Astra *ascended* with self-built harness (21 Sep 2026) [P] | Protocol gap durable; open-tool gap closed | Tacit knowledge, 10⁴-turn state, irreversibility |
| VideoGameBench | May 2025 | Not measured | Gemini 2.5 Pro 0.48% (2025) [S] | Unknown in 2026 | Real-time pixels, long horizon |
| Pokémon Red/Blue | 2025 showcase | Casual players finish (no controlled N) | Opus 4.7 beat Red (May 2026) [S] | Flipped (slowly, harness-dependent) | Navigation, memory, self-correction |
| OSWorld (-Verified) | Apr 2024 | 72.36% [P] | 90.19% (25 Jul 2026) [P] | **Flipped** 11 Dec 2025 | Scaffolding and step budgets closed it |
| OSWorld 2.0 | Jun 2026 | No success-rate baseline; median task 1.6 h [S] | Astra 72.6% [S]; Opus 5 70.57% [P-m] | New | Long-horizon real tasks |
| WebArena | Jul 2023 | 78.24% [S] | WebTactix 74.3% (Feb 2026) [S] | Near parity | Multi-step web state |
| GAIA | Nov 2023 | 92% [S] | 93.4–95.1% (Jul–Sep 2026) [S] | **Flipped** (2026) | Tool use and retrieval chains |

---

## 4. Design lessons (with evidence tags)

1. **Pre-register the harness, or measure two tracks.** A single score without a fixed harness measures the harness. Evidence:
   - 62.7% → 98.6% for the same model and effort on ARC-AGI-3 [P-m].
   - A 20 pp step-budget effect on OSWorld [P].
   - NetHack at 13% under protocol vs a win with a self-built harness [P/S].

   ARC now labels "Standard" and "Provider Adapter" results separately [P-m].
2. **Human anchors must be measured, sizeable and reported as distributions.** Report the median person, the top quartile and the panel, not "≥2 solvers". Evidence:
   - The average-vs-panel gaps: 64.2 vs 98 (ARC-AGI-1) and 60 vs 100 (ARC-AGI-2) [P-m].
   - The ARC-AGI-3 baseline was rewritten three weeks after launch [P].
   - BlindTest's human figure was not measured [P]; SimpleBench used N=9, ClockBench N=5, VPCT N=3 [S].
3. **Efficiency matters as much as accuracy, but it is not a moat.**
   - ARC-AGI-3's action-efficiency metric was supposed to be the "dividing line". It fell once models "understood" the mechanics [P-m].
   - Cost per task collapsed too: $1.12/task on ARC-AGI-2 vs a $17 human [S/P-m].
   - Treat efficiency as a *measured axis*, not as the source of durability [I].
4. **Durable gaps sit where information must survive a perception-to-reasoning bottleneck.** Examples:
   - encoder-to-LLM spatial loss (BlindTest linear probes [S]);
   - video object permanence (IntPhys 2 near chance [S]);
   - allocentric maps (MindCube [P]);
   - multi-video spatial integration (MMSI-Video [S]).

   Text-renderable states (ARC grids, web DOM, terminal NetHack) were closed by reasoning plus tools [P/P-m].
5. **Use ablations to prove the mechanism, and ship them with the benchmark.** Good examples:
   - Mystery vs plain Blocksworld, with a classical-planner control [P];
   - transcribed vs raw PDF in EnigmaEval [S];
   - spaced vs crowded shapes in BlindTest [S];
   - real-time vs paused in VideoGameBench [S];
   - the scaffold ablation in MindCube [P].

   These separate "hard for AI" from "hard in general".
6. **Expect "knowledge overfitting" without item leakage.**
   - ARC found models using ARC's colour encoding unprompted [P-m].
   - Private sets are necessary but not sufficient. The *format family* also needs periodic replacement, as ARC does roughly every year [P-m].
7. **Keep a fully private, rotating split and do not publish the full data.** ClockBench publishes 10 of 180 clocks [P]; IntPhys 2 withholds held-out metadata [P]; ARC uses private splits [P-m]. Durable sets rely on this, though it did not prevent ARC's fall [I].
8. **Real-time, irreversible, long-horizon settings are the least-closed agentic gaps.**
   - VideoGameBench was at 0.48% [S].
   - NetHack protocol progression is about 13% [S].
   - [Speculation] A game with enforced wall-clock limits, no web access and in-episode learning would keep headroom longer than turn-based puzzles.
9. **Beware stale anchors, and use ratio-to-human instead.** OSWorld's 72.36% now sits below 16 agent entries [P]. Report AI relative to a contemporaneous human re-baseline [I].
10. **Watch closure speed as the key durability metric.**
    - ARC-AGI-1 took 5 years, ARC-AGI-2 about 15 months and ARC-AGI-3 6 months (under the provider harness).
    - ClockBench went from 13 to 67 in about 12 months [P-m/S].

    Any new "human > AI" benchmark should expect targeted post-training within 6–12 months of attention [I].

---

## 5. Claims table

| Claim | Value | Date | Source URL | Primary/secondary | Confidence |
|---|---|---|---|---|---|
| ARC-AGI-1/2 human panel vs avg person; cost | 98%/64.2% (v1); 100%/60% (v2); $17/task | Mar 2025 | https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md | Primary (mirror) | H |
| o3-preview ARC-AGI-1; tuned on 75% of public train | 75.7% ($10k limit); 87.5% (172×) | Dec 2024 | https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/sources/o3_announcement.html | Primary (cache) | H |
| ARC Prize 2024 SOTA jump; 1,430 teams | 33% → 55.5%; ARChitects 53.5% | Dec 2024 | https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2024/2412.04604v2_arc_prize_2024.md | Primary (mirror) | H |
| ARC Prize 2025 Kaggle top | 24% (NVARC 24.03%); 1,455 teams | Nov 2025 | https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md | Primary (mirror) | H |
| Poetiq refinement on Gemini 3 Pro (ARC-AGI-2) | 31% @ $0.81 → 54% @ $31 | Dec 2025 | same as above | Primary (mirror) | H |
| Knowledge overfitting (ARC colour mappings) | Qualitative | Jan 2026 | same as above | Primary (mirror) | H |
| ARC-AGI-2 frontier failure modes | Symbolic, compositional, contextual | Mar 2025 | https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md | Primary (mirror) | H |
| Opus 5 ARC-AGI-1/2/3 (verified) | 97.50% / 90.42% / 30.16% | Jul 2026 | https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md | Primary (mirror) | M-H |
| GPT-6 Astra ARC-AGI-2 | 95.0% @ $1.12/task | Sep 2026 | https://x.com/arcprize/status/2095597602545025138 | Secondary | M |
| Astra ARC-AGI-3 Standard vs Provider Adapter | 62.7% (~$26k) vs 99.9% (~$18.8k); 98.6% at max | 3 Sep 2026 | https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md | Primary (translation) | M-H |
| Astra fewer actions than median human | 96.0% of levels; −51.7% actions | 3 Sep 2026 | same | Primary (translation) | M-H |
| ARC-AGI-3 human study | 458 participants; each game beaten by ≥2 of ~10 | 14 Apr 2026 | https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md | Primary (capture) | H |
| ARC-AGI-3 avg human; participants per report | 48%; 486 participants | 2026 | https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf | Secondary (search extract) | L-M |
| ARC-AGI-3 baseline change | 2nd-best → median human; cap 1.0 → 1.15 | 14 Apr 2026 | https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx | Primary | H |
| ARC Prize 2026 Milestone 1 winner | Tufa Labs "The Duck" | 30 Jun 2026 | https://arcprize.org/blog/arc-prize-2026-milestone-1 | Secondary | M |
| SimpleBench human vs best | 83.7% (N=9) vs Claude Fable 5 81.9% | 10 Jun 2026 | https://ai.miraheze.org/wiki/SimpleBench | Secondary | M |
| Concept human vs LLMs | >90% vs <40% | Oct 2025 / ACL 2026 | https://aclanthology.org/2026.findings-acl.1219/ | Primary abstract via search | M-H |
| EnigmaEval launch | o1 7.0% normal, 0% hard; 1,184 puzzles | Feb 2025 | https://arxiv.org/abs/2502.08859 | Secondary extract of primary | M |
| EnigmaEval SEAL top | Claude Fable 5 high 39.28±2.80 | 2026 | https://labs.scale.com/leaderboard | Secondary | M |
| PlanBench Mystery Blocksworld | GPT-4o 0%; o1-preview 52.8%; R1 43.3% | 2024–25 | https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md | Primary | H |
| PlanBench human Blocksworld | 78% of 50 valid plans | 2022 | https://www.emergentmind.com/topics/planbench | Secondary | M |
| BlindTest | 4-VLM avg 58.12%; best 74.94%; "expected" human 100% | 2024 | https://raw.githubusercontent.com/anguyen8/vision-llms-are-blind/main/README.md | Primary | H |
| BlindTest linear-probe mechanism | Encoder holds info; LLM fails to decode | v6 | https://arxiv.org/abs/2407.06581 | Secondary extract | M |
| ClockBench launch | Humans 89.1% (5); Gemini 2.5 Pro 13.3% | Sep 2025 | https://the-decoder.com/even-the-best-ai-models-cant-reliably-read-the-clock/ | Secondary | M |
| ClockBench 2026 | GPT-5.6 Sol Max 66.7% | ~Sep 2026 | https://theslowai.substack.com/p/ai-clock-benchmark-capacity | Secondary | L-M |
| VPCT | Humans 100% (3); Gemini 3 Pro 91% | 2025 | https://llmlearner.com/rankings/vpct | Secondary | L-M |
| VisFactor | Humans 78.8% vs Gemini-3.1-Pro 54.0% | 2026 (v4) | https://arxiv.org/html/2502.16435v4 | Secondary extract | M |
| VSI-Bench | Human 79%; SSR-3D 73.9 | Dec 2024 / Mar 2026 | https://arxiv.org/pdf/2412.14171 ; https://arxiv.org/pdf/2603.00409 | Secondary extract | M |
| MindCube | Near-random VLMs; 37.8 → 57.8 → 61.3% | Mar 2026 | https://raw.githubusercontent.com/mll-lab-nu/MindCube/main/README.md | Primary | H |
| MMSI-Video-Bench | Humans 96.4% vs Gemini 3 Pro 38.0% | Dec 2025 | https://arxiv.org/pdf/2512.10863 | Secondary extract | M |
| IntPhys 2 | Humans 96.44%; V-JEPA 2 57.51%; MLLMs ~chance | Jun 2025 | https://www.emergentmind.com/topics/intphys-2 | Secondary | M |
| Physics-IQ Verified top | 58.2 (v2v), 48.2 (i2v) | Jun–Sep 2026 | https://raw.githubusercontent.com/google-deepmind/physics-IQ-benchmark/main/README.md | Primary | H |
| BALROG NetHack progression | Astra-Max 13.2 ± 2.7% | 18 Sep 2026 | https://www.sota2.com/research/sota/long-horizon-game-playing-on-balrog-nethack | Secondary | L-M |
| NetHack ascension by GPT-6 Astra | 37,140 turns; web/wiki/tools; 3rd try | 21 Sep 2026 | https://raw.githubusercontent.com/kenforthewin/nethack_astra/main/README.md | Primary | H |
| VideoGameBench | 0.48% (VGB), 1.6% (Lite) | May 2025 | https://arxiv.org/abs/2505.18134 | Secondary extract | M |
| Claude beats Pokémon Red | Opus 4.7 | May 2026 | https://www.lesswrong.com/posts/sehJYg5Yny9fvpbpt/a-year-late-claude-finally-beats-pokemon | Secondary | M |
| OSWorld human; flip; best | 72.36%; 72.58% (2025-12-11); 90.19% (2026-07-25) | 2024–26 | https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx | Primary | H |
| OSWorld step-budget effect | Sonnet 4.5: 42.88 / 58.08 / 62.88% | 2025 | same | Primary | H |
| OSWorld 2.0 | Astra 72.6%; Opus 5 70.57% | Jun–Sep 2026 | https://snorkel.ai/leaderboard/os-world-2-0/ | Secondary (Opus: primary mirror) | M |
| WebArena | Human 78.24%; best 74.3% | Feb 2026 | https://leaderboard.steel.dev/leaderboards/webarena/ | Secondary | M |
| GAIA | Human 92%; test leader 93.36% (Jul), 95.1% (Sep) | 2026 | https://leaderboard.steel.dev/leaderboards/gaia/ | Secondary | M |

---

## 6. Sources

**Primary, read directly (raw GitHub):**
- ARC docs changelog — https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx
- ARC-AGI-3 Agents — https://raw.githubusercontent.com/arcprize/ARC-AGI-3-Agents/main/README.md
- Tufa Labs Duck harness — https://raw.githubusercontent.com/Tufalabs/duck-harness/main/README.md
- SimpleBench repo — https://raw.githubusercontent.com/simple-bench/SimpleBench/main/README.md
- BlindTest — https://raw.githubusercontent.com/anguyen8/vision-llms-are-blind/main/README.md
- ClockBench — https://raw.githubusercontent.com/aleksafar/clockbench/main/README.md
- VPCT runner — https://raw.githubusercontent.com/camelCase12/vpct-runner/main/README.md
- VSI-Bench — https://raw.githubusercontent.com/vision-x-nyu/thinking-in-space/main/README.md
- MindCube — https://raw.githubusercontent.com/mll-lab-nu/MindCube/main/README.md
- IntPhys 2 — https://raw.githubusercontent.com/facebookresearch/IntPhys2/main/README.md
- Physics-IQ — https://raw.githubusercontent.com/google-deepmind/physics-IQ-benchmark/main/README.md
- Physion — https://raw.githubusercontent.com/cogtoolslab/physics-benchmarking-neurips2021/master/README.md
- PHYRE — https://raw.githubusercontent.com/facebookresearch/phyre/main/README.md
- PlanBench — https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md
- BALROG — https://raw.githubusercontent.com/balrog-ai/BALROG/main/README.md
- nethack_astra — https://raw.githubusercontent.com/kenforthewin/nethack_astra/main/README.md
- VideoGameBench — https://raw.githubusercontent.com/alexzhang13/videogamebench/main/README.md
- OSWorld site — https://raw.githubusercontent.com/os-world/os-world.github.io/main/index.html
- OSWorld-Verified results — https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx
- OSWorld repo — https://raw.githubusercontent.com/xlang-ai/OSWorld/main/README.md
- WebArena — https://raw.githubusercontent.com/web-arena-x/webarena/main/README.md

**Primary via mirror, capture or translation:**
- ARC leaderboard/policy/blog captures (29 Sep 2026), one packet each for ARC-AGI-1, 2 and 3:
  - https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-1/packet-r1.md
  - https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-2/packet-r1.md
  - https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md
- ARC Astra post (Chinese translation of arcprize.org/blog/astra) — https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md
- Claude Opus 5 system card §8.12–8.14 mirror — https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md
- ARC Prize 2025 report (arXiv 2601.10904) — https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md
- ARC Prize 2024 report (arXiv 2412.04604) — https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2024/2412.04604v2_arc_prize_2024.md
- o3 ARC post cache — https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/sources/o3_announcement.html
- ARC-AGI-2 launch post cache — https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md
- ARC-AGI-3 paper digest (arXiv 2603.24621) — https://raw.githubusercontent.com/memgrafter/research-digests/491d1e597ee1384396057fbe72e2bdec9f11c2c6/ml_research_analysis_2026/2603.24621_arc-agi-3-a-new-challenge-for-frontier-agentic-intelligence_20260331_185732.md

**Secondary (search extracts; pages not opened):**
- ARC:
  - https://arcprize.org/blog/arc-prize-2025-results-analysis
  - https://arcprize.org/blog/arc-prize-2026-milestone-1
  - https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf
  - https://x.com/arcprize/status/2095597602545025138
  - https://arcprize.org/results/openai-gpt-6-astra
  - https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/
- SimpleBench:
  - https://ai.miraheze.org/wiki/SimpleBench
  - https://simple-bench.com/
- Concept:
  - https://aclanthology.org/2026.findings-acl.1219/
  - https://arxiv.org/abs/2510.13271
- EnigmaEval:
  - https://arxiv.org/abs/2502.08859
  - https://labs.scale.com/leaderboard
  - https://benchmarklist.com/benchmarks/enigma_eval/
- BlindTest (v6): https://arxiv.org/abs/2407.06581
- ClockBench:
  - https://the-decoder.com/even-the-best-ai-models-cant-reliably-read-the-clock/
  - https://theslowai.substack.com/p/ai-clock-benchmark-capacity
- VPCT:
  - https://epoch.ai/benchmarks/vpct
  - https://llmlearner.com/rankings/vpct
- VisFactor: https://arxiv.org/html/2502.16435v4
- VSI-Bench and SSR:
  - https://arxiv.org/pdf/2412.14171
  - https://arxiv.org/pdf/2603.00409
- MindCube: https://www.emergentmind.com/topics/mindcube-benchmark
- MMSI-Video-Bench: https://arxiv.org/pdf/2512.10863
- IntPhys 2:
  - https://arxiv.org/html/2506.09849v1
  - https://www.emergentmind.com/topics/intphys-2
- PlanBench:
  - https://www.emergentmind.com/topics/planbench
  - https://arxiv.org/pdf/2305.15771
- BALROG and NetHack:
  - https://www.sota2.com/research/sota/long-horizon-game-playing-on-balrog-nethack
  - https://kenforthewin.github.io/blog/posts/nethack-agent/
- VideoGameBench: https://arxiv.org/abs/2505.18134
- Pokémon:
  - https://www.lesswrong.com/posts/sehJYg5Yny9fvpbpt/a-year-late-claude-finally-beats-pokemon
  - https://www.tomshardware.com/tech-industry/artificial-intelligence/developer-says-jev-decision-model-beat-pokemon-red-in-under-a-week-non-llm-engine-succeeds-where-traditional-chatbots-stalled-for-months-but-claude-opus-5-coached-the-model-through-its-dead-ends
- OSWorld 2.0: https://snorkel.ai/leaderboard/os-world-2-0/
- WebArena: https://leaderboard.steel.dev/leaderboards/webarena/
- GAIA:
  - https://leaderboard.steel.dev/leaderboards/gaia/
  - https://benchlm.ai/benchmarks/gaia
- Other spatial benchmarks:
  - CityCube: https://aclanthology.org/2026.acl-long.416.pdf
  - SpatiaLab: https://arxiv.org/pdf/2602.03916

**Blocked or unverifiable this session** (recorded for the fact-checker):
- Blocked hosts: arcprize.org (leaderboard JSON rows), simple-bench.com, cbrower.dev (VPCT), clockbench.ai, balrogai.com, vgbench.com, the GAIA HF leaderboard, the IntPhys 2 HF leaderboard, all arXiv full texts, and lesswrong.com.
- The web-search budget was exhausted before the Pokémon (Gemini), VPCT-2026, MindTopo and SimpleBench-2026 checks.
