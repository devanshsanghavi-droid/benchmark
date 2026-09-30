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
  - **ARC-AGI-1.** Frontier models have reached or passed the human panel: the top verified score is 98.5% (Claude Fable 5, reported by ARC Prize 5 Aug 2026; GPT-6 Astra tied it on 3 Sep 2026), against a 98% panel. Claude Opus 5 scores 97.5% [corrected by fact-check: was "match the human panel: Claude Opus 5 scores 97.5%", which omitted the higher 98.5% entries; source: ARC leaderboard capture of 29 Sep 2026 (highest served ARC-AGI-1 value 98.5) https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-1/packet-r1.md ; model attribution from search extracts of https://x.com/arcprize/status/2085115252035785168 and https://x.com/arcprize/status/2095597602545025138, secondary].
  - **ARC-AGI-2.** Claude Opus 5 scores 90.42% [P-m]. GPT-6 Astra is reported at 95.0% for $1.12/task [S]. The human panel solves 100%; the average test-taker scores 60%.
  - **ARC-AGI-3.** GPT-6 Astra scores 99.9% under the provider harness (high effort) [P-m] [verified]. In the max-effort provider run (98.6%) it took fewer actions than the median human on 96% of levels [P-m] [clarified by fact-check: the 96.0% figure belongs to the max-effort 98.6% run, not the 99.9% run].
  - **OSWorld.** Agents passed the 72.36% human rate on 11 Dec 2025, and the best agent reached 90.19% on 25 Jul 2026 [P] [verified]. [uncertain: comparability — the 72.36% human rate was measured on the original 2024 OSWorld tasks, while the agent scores are on the revised OSWorld-Verified set.]
  - **GAIA.** The top test-set entry, 93.36% (CustomGPT.ai Research Lab v44), sits just above the 92% human baseline [S] [corrected by fact-check: was "Top test-set entries of 93–95%"; the 95.1% figure (Agents-A1-4B) is a developer self-report, not a GAIA test-set leaderboard entry; source: https://raw.githubusercontent.com/InternScience/Agents-A1/main/README.md].
  - **SimpleBench.** SimpleBench's own leaderboard data (captured 29 Sep 2026) now tops out at 88.4%, above the 83.7% human baseline (9 people) [P-m]. Aggregators name Claude Opus 5.5 at 88.4% and Claude Fable 5.1 at 86.6% [S]. The ~4.7 pp margin is within noise for N=9 [I]. [corrected by fact-check: was listed under "near parity" as "81.9% (Claude Fable 5) against 83.7%"; the 81.9% is stale prose on simple-bench.com; source: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-simple-bench-snapshot-2026-09-10/producer-packet-r1.md (simple-bench.com/static/js/leaderboard-data.js, 104 values, max 88.4; 3 new model rows on 29 Sep)]
- **Near parity or nearly closed:**
  - WebArena: 74.3% against 78.24% [S].
  - VPCT: 91% against 100% [S].
- **Gaps that still hold, and hold by a lot, are perceptual, spatial, physical or real-time. Three clusters:**
  - **Fine-grained vision and spatial reasoning:**
    - VisFactor: humans 78.8% vs Gemini-3.1-Pro 54.0% [S].
    - MMSI-Video-Bench: 96.4% vs 38.0% [S].
    - MindCube: about 95% vs 61.3% after purpose-built training [P/S]. [uncertain: the ~95% human figure was not found in any source reachable here. The trained-model score varies by paper version (61.3% in the current README; 70.67% and 76.1% in earlier versions).]
    - ClockBench: 89.1% vs 66.7% [S].
  - **Intuitive physics from video:** IntPhys 2, humans about 96% vs best model about 57.5% (chance 50%) [S].
  - **Real-time and long-horizon games under a fixed protocol:**
    - VideoGameBench: 0.48% completion [S].
    - BALROG NetHack progression: about 13% for GPT-6 Astra at max effort (13.24 ± 2.66%) [P, balrog-ai/experiments PR #19].
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
  - NetHack: GPT-6 Astra *ascended* on 21 Sep 2026 using a harness it built itself, with web and wiki access, on its third attempt [P]. The protocol-constrained BALROG progression is still about 13% [P].
- **Speed of closure.**
  - ARC-AGI-1 took about 5 years to pass the average human.
  - ARC-AGI-2 took about 11 months to pass its 60% human average: Claude Opus 4.6 reported 68.8% (Feb 2026) and Gemini 3 Deep Think 84.6% (12 Feb 2026) [S] [corrected by fact-check: was "about 15 months"; source: search extracts of https://9to5google.com/2026/02/12/gemini-3-deep-think-upgrade/ and https://officechai.com/ai/gemini-3-deep-think-benchmarks-arc-agi/, secondary].
  - ARC-AGI-3 took about 5 months (25 Mar → 3 Sep 2026) to go from under 1% to human-level under a provider harness [corrected by fact-check: was "6 months"; dates from the ARC Astra post, see §2.3].
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
  - ARC's "human panel" counts a task as solved if at least 2 people solved it. The *average* test-taker scores 60–64% on ARC-AGI-1/2 [P-m] and about 48% on ARC-AGI-3 [S] [uncertain: the 48% figure appears only in search extracts that do not clearly attribute it; it was not found in the ARC-AGI-3 technical report extract].
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
- **Latest.** Claude Opus 5 scored 97.50% (verified by ARC Prize, max effort, Jul 2026) [P-m](https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md) [verified]. The top verified score is higher: 98.5%, by Claude Fable 5 (ARC post of 5 Aug 2026) and tied by GPT-6 Astra (3 Sep 2026) [S] [corrected by fact-check: Opus 5 was presented as the latest/best; the ARC leaderboard capture of 29 Sep 2026 gives a maximum of 98.5, https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-1/packet-r1.md].
- **ARC's own framing.** ARC-AGI-1 "stayed unbeaten for so long, despite a 50,000x scaleup of base LLM pretraining" [P-m](https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-1/packet-r1.md).

#### Inferences
- Pretraining scale alone never flipped ARC-AGI-1. Four things did: test-time search and refinement, RL reasoning, test-time training, and familiarity with the ARC format.
- The "human 98%" figure is a *panel* ceiling. Against individual people, AI passed the median in Dec 2024.

#### Gaps
- The released o3's performance without ARC training was never cleanly isolated.

### 2.2 ARC-AGI-2 (launched 24 Mar 2025)

#### Takeaway
ARC-AGI-2 is flipped against the average human (60%) and above the 85% prize threshold on the commercial leaderboard. It passed 60% within about 11 months (Feb 2026) and was above 85% by Jul 2026 at the latest (Opus 5, 90.42%), about 16 months after launch [corrected by fact-check: was "within about 15–18 months" for both; first >60% results were Claude Opus 4.6 at 68.8% and Gemini 3 Deep Think at 84.6% in Feb 2026, per search extracts, secondary]. The ARC Prize Kaggle track, with its compute limits, lagged far behind: 24% in Nov 2025.

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
  - GPT-6 Astra is reported at 95.0% for $1.12/task [S](https://x.com/arcprize/status/2095597602545025138); [S](https://arcprize.org/results/openai-gpt-6-astra). [verified: several independent search extracts agree, and the 29 Sep capture's maximum of 95 is consistent; the primary page was blocked.]
  - Note: Imbue's 95.1% (Gemini 3.1 Pro + code evolution, Feb 2026) is on the *public* eval set and is not comparable to the semi-private verified scores [S](https://imbue.com/blog/2026-02-27-arc-agi-2-evolution).
  - A 29 Sep 2026 capture of the official v2.json gives a maximum of 95 [P-m](https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-2/packet-r1.md) (via the prior dossier; the capture holds a summary, not the rows).

#### Inferences
- ARC's own diagnosis is that the *accuracy* gap became "primarily bottlenecked by engineering" while the *efficiency* gap remains science-limited [P-m, 2025 report].
- Accuracy-only human-gap claims have a short shelf life once a format is a lab target.

#### Gaps
- There is no independent per-task human-vs-AI error overlap analysis for 2026 models.
- Kaggle ARC-AGI-2 2026-track scores were not retrieved.

### 2.3 ARC-AGI-3 (interactive games; launched 25 Mar 2026) and ARC Prize 2026

#### Takeaway
ARC-AGI-3 is the only ARC version built on *action efficiency* against humans. It went from under 1% at launch (best 0.37%, Gemini 3.1 Pro, 25 Mar 2026) to 7.78% (GPT-5.6 Sol, Jul) to 30.16% (Claude Opus 5, 24 Jul) to 62.7% on ARC's Standard harness and 99.9% on the Provider Adapter harness (GPT-6 Astra, 3 Sep 2026) [verified; the timeline agrees with the Panel F check]. Under the provider harness, GPT-6 Astra is *more* action-efficient than the median human. The binding constraint was mostly the harness's handling of memory and state, not raw model capability.

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
  - **Conflict (largely resolved).** The technical report counts "486 unique participants … 2,893 total environment attempts", but *across 414 candidate environments* (the pre-selection pool), so it need not contradict the blog's 458 for the final set [S, search extract of https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf]. The "average human tester scored 48%" figure was not found in the report extract [uncertain: not verified — attribution unclear in search extracts].
- **Scoring change three weeks after launch.** The baseline moved from the 2nd-best human to the median human, and the per-level cap rose from 1.0× to 1.15× [P](https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx). ARC's reasons were a "luck factor" and a +0.5 pp effect for both humans and AI [P-m, blog capture].
- **Score trajectory.**
  - At launch (25 Mar 2026), frontier models scored below 1% [S, paper digest] [verified]. Launch coverage gives Gemini 3.1 Pro 0.37%, GPT-5.4 (high) 0.26%, Opus 4.6 0.25% and Grok 4.20 0% [S](https://officechai.com/ai/arc-agi-3/).
  - In Jul 2026 (Opus 5 released 24 Jul 2026), Claude Opus 5 (high) reached 30.16%, "roughly four times the best previously reported score". GPT-5.6 Sol (max; released 9 Jul 2026) scored 7.78%, and Opus 4.8 (high) 1.52% [verified; the 7.78% is the best *pre-Opus-5* score, not the launch score]. [P-m](https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md).
  - On 3 Sep 2026, GPT-6 Astra scored 62.7% on the Standard harness (max effort, about $26,098 per semi-private run) and 99.9% on the Provider Adapter harness (high effort, about $18,817). At max effort the two harnesses give 62.7% vs 98.6%.
    - Under the Provider Adapter, Astra (max effort, the 98.6% run) used fewer actions than the median human on 96.0% of levels, and 51.7% fewer actions on average [verified]. The 3.66× speed and 49% token figures compare the two harnesses across runs (tokens: 167 game–effort pairs solved in both).
    - The Provider Adapter "preserves opaque reasoning state between requests" and compacts context. It was about 3.66× faster and used 49% fewer tokens [P-m translation](https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md).
- **Mechanism evidence from ARC.**
  - ARC expected that action efficiency "would remain the dividing line". It found instead a "binary pattern": "once it 'understands' the mechanics, execution usually falls within the human efficiency range". Brute-force paths remain inefficient.
  - Astra wrote compact symbolic world models and built custom tools. ARC notes that humans had no code interpreter [P-m translation](https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md).
  - OpenAI separately reported that "enabling two settings tripled" its ARC-AGI-3 scores [S](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/). Per search extracts (late Jul 2026), the two settings were retained reasoning and compaction: GPT-5.6 Sol went from 13.3% to 38.3% on the *public* set [S].
- **ARC Prize 2026** (Kaggle, internet off) has ARC-AGI-3 and ARC-AGI-2 tracks, with milestone prizes on 30 Jun and 30 Sep 2026. Milestone 1 went to Tufa Labs' "The Duck", a REPL- and tool-using harness (Qwen 3.6 27B) that evicts old context, with **1.21%**; runners-up scored 0.867% and 0.864% [S](https://arcprize.org/blog/arc-prize-2026-milestone-1) (search extract); [P](https://raw.githubusercontent.com/Tufalabs/duck-harness/main/README.md) (the README confirms a tool-using ARC-AGI-3 solver but does not itself state the prize or the eviction policy). "Nearly one million scorecards" had been submitted on public environments by April [P-m].

#### Inferences
- Given persistent state, frontier models can form, test and compress hypotheses into a world model inside a text or code loop. The 36-point harness gap shows that state and memory plumbing was the bottleneck.
- The median-human efficiency bar fell once exploration stopped being brute force.
- "100% solvable" is a panel or existence claim; the average human scores about 48% RHAE [uncertain: 48% not verified, see Cited Findings].

#### Gaps
- Kaggle ARC-AGI-3 Milestone 2 numbers could not be retrieved. Milestone 1's top Kaggle score was 1.21% [S], which shows how far the offline, compute-limited track lags the API frontier (99.9%).
- The cost policy is unresolved: the leaderboard says "Only systems <$10,000 … shown", yet Astra's run costs about $19–26k per run.
- The "48% average human" figure could not be checked against the report text. The 458 vs 486 difference appears to be final-set vs candidate-pool counts [S].

### 2.4 SimpleBench (AI Explained; 2024)

#### Takeaway
SimpleBench is multiple-choice "trick" questions on everyday spatio-temporal, social and adversarial-wording reasoning. The human-over-AI gap has **flipped narrowly**: the site's leaderboard data (29 Sep 2026) tops out at 88.4% against the 83.7% human baseline, and aggregators attribute that score to Claude Opus 5.5 (released 22 Sep 2026). The margin is small, and with N=9 humans it is within noise. [corrected by fact-check: was "gap is now about 1.8 pp: humans 83.7% vs Claude Fable 5 at 81.9% (leaderboard of 10 Jun 2026) … effectively reached parity"; source: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-simple-bench-snapshot-2026-09-10/producer-packet-r1.md]

#### Cited Findings
- **Human baseline.** 83.7% "based on a sample of nine participants". Best model: Claude Fable 5 at 81.9%, then Gemini 3.1 Pro Preview 79.6% and GPT-5.5 Pro 76.9%. The leaderboard was updated 10 Jun 2026 [S](https://ai.miraheze.org/wiki/SimpleBench); [S](https://simple-bench.com/). [corrected by fact-check: this ranking is stale. On 29 Sep 2026 the served leaderboard data had a maximum of 88.4 and 3 newly added model rows, while the page prose still read "today's top model, Claude Fable, which scored 81.9%" [P-m](https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-simple-bench-snapshot-2026-09-10/producer-packet-r1.md). Aggregator search extracts give Claude Opus 5.5 88.4% and Claude Fable 5.1 86.6% [S](https://benchmarklist.com/benchmarks/simplebench/). A cross-panel report of GPT-6 Astra Pro at 86.5% was not verified here.]
- **What it tests.** Spatio-temporal reasoning, social intelligence and "linguistic adversarial robustness (trick questions)" [S](https://ai.miraheze.org/wiki/SimpleBench).
- **Code.** The public repo ships only a small public set and a runner [P](https://raw.githubusercontent.com/simple-bench/SimpleBench/main/README.md).

#### Inferences
- The hardness driver is distractor-laden wording that pulls toward the "textbook" answer. RL-trained reasoning models apparently learned to discount irrelevant detail [I; no ablation found].
- With about 200 private items and 9 humans, a gap under about 5 pp is not statistically meaningful [I].

#### Gaps
- Model-level rows for the Sep 2026 entries (Opus 5.5, Fable 5.1, GPT-6 Astra) were not read directly: simple-bench.com was blocked, and the capture gives only the value range.
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
  - The "CAIS dashboard" reports Claude Opus 5 at 43.9% (Jul 2026) [S, dashboard URL not retrieved] [uncertain: not verified — no source found for 43.9%; the SEAL figure 39.28 (Fable 5) was confirmed by search extract].
- **Dataset now public.** CAIS and Scale released the full EnigmaEval dataset (v2, gated, on Hugging Face) on 23 Jul 2026 [S](https://x.com/CAIS/status/2080344746699170214) (search extract; the date comes from the tweet ID). Scores from late 2026 on carry contamination risk; see design lesson 7.

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
- The human ceiling is about 95% [uncertain: not verified — not found in the README or in search extracts]. The v1 numbers were 60.76% for SFT and 70.67% for SFT plus RL, which differ from the updated README [S](https://www.emergentmind.com/topics/mindcube-benchmark). Another version reports 61.7% for SFT and 76.1% for SFT plus RL [S, search extract of arXiv 2506.21458]. The "trained model" number therefore depends on version (61.3–76.1%).

#### Inferences
- The scaffold ablation is mechanistic evidence: forcing an explicit allocentric map helps a lot. This implies that frontier VLMs lack a persistent internal spatial representation [I].

#### Gaps
- Scores for 2026 frontier models were not retrieved.

### 2.14 MMSI-Video-Bench (arXiv 2512.10863; Dec 2025)

#### Takeaway
MMSI-Video-Bench is a human-annotated video spatial-intelligence benchmark covering construction, motion, planning, prediction and cross-video reasoning. Humans score 96.4% and the best model (Gemini 3 Pro) 38.0%, one of the largest current gaps.

#### Cited Findings
- Humans score 96.4% and Gemini 3 Pro 38.0% [S](https://arxiv.org/pdf/2512.10863) [verified: the official README leaderboard lists Human 96.40 and Gemini 3 Pro 37.97, with 1,106 questions over 1,278 clips; [P](https://raw.githubusercontent.com/InternRobotics/MMSI-Video-Bench/main/README.md)].

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
  - Scores: humans 96.44% overall (92.44% on held-out). Most models are at 52–54% (chance is 50%). V-JEPA 2 is best at 57.51%. Gemini 2.5 Flash is near chance except about 64% on the easy set [verified (secondary): search extracts agree on humans 96.44/92.44 and V-JEPA 2 57.51; Gemini 2.5 Flash is 55.63% on the main set. Sibling dossier E gives the best model as Gemini 2.5 Flash at 55.63%, apparently counting MLLMs only.] [S](https://www.emergentmind.com/topics/intphys-2); [S](https://arxiv.org/html/2506.09849v1).
- **Physics-IQ Verified** (DeepMind), physical realism of video generation.
  - The ceiling of 100 is defined by physical variance.
  - Best scores are 58.2 (Magi-1 24B + GeoPhys best-of-N, v2v, Jun 2026) and 48.2 i2v (Physis-Lang/Cosmos3-Super, 28 Sep 2026). Veo 3.1 Fast scores 29.96 [P](https://raw.githubusercontent.com/google-deepmind/physics-IQ-benchmark/main/README.md).
- **Physion** (NeurIPS 2021) tests humans and models on identical stimuli [P](https://raw.githubusercontent.com/cogtoolslab/physics-benchmarking-neurips2021/master/README.md); **PHYRE** is an agent physics-puzzle set [P](https://raw.githubusercontent.com/facebookresearch/phyre/main/README.md). Neither has 2026 frontier-LLM numbers that I could find.

#### Inferences
- The hardness driver is temporal object tracking and violation detection, not static geometry. VPCT, a *static* image, closed; video VoE did not [I].
- The original IntPhys was saturated by V-JEPA at 98.3% [S], a reminder that synthetic-physics sets fall once targeted.

#### Gaps
- No 2026 IntPhys 2 held-out leaderboard values were retrieved (the HF space was blocked).
- Physics-IQ has no human baseline.
- No LLM or VLM numbers were re-verified for Physion or PHYRE.

### 2.16 BALROG / NetHack (UCL et al.; Nov 2024; ICLR 2025)

#### Takeaway
Under BALROG's fixed protocol, NetHack progression stayed near floor until 2026. GPT-6 Astra (max effort) reached 13.24 ± 2.66% [P]. Yet on 21 Sep 2026, Astra *ascended* (won) NetHack using a harness it built itself, with wiki and web access, on its third attempt. The protocol-constrained gap persists; the unconstrained gap closed.

#### Cited Findings
- BALROG evaluates agentic LLMs and VLMs "on long-horizon interactive tasks using reinforcement learning environments" [P](https://raw.githubusercontent.com/balrog-ai/BALROG/main/README.md).
- **NetHack progression scores.**
  - The BALROG leaderboard lists GPT-6-Astra-Max at 13.2 ± 2.7% (entry dated 18 Sep 2026) [S](https://www.sota2.com/research/sota/long-horizon-game-playing-on-balrog-nethack) [verified: the official results PR, merged 19 Sep 2026, gives GPT-6 Astra NetHack 13.24 ± 2.66%, GPT-5.6 Sol 3.22 ± 0.40% and overall BALROG averages Astra 68.26 ± 1.97%, Sol 59.97 ± 2.01%, all naive agent at max effort; [P](https://github.com/balrog-ai/experiments/pull/19)].
  - Earlier independent results: BRAID fork with Claude Opus 4.5 at 6.96%, and GPT-5.2 averaging 2.56% with a best run of 12.56% (reaching dungeon level 10) [S](https://kenforthewin.github.io/blog/posts/nethack-agent/) [corrected by fact-check: was "GPT-5.2 at 12.56%"; 12.56% is the maximum single run, per a search extract of the same blog post (secondary)].
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
VideoGameBench has VLMs play 1990s games from raw pixels in real time. The best model (Gemini 2.5 Pro) completed 0.48% (1.6% on the paused "Lite" variant) [verified (secondary)]. It is one of the most durable gaps on record, but no 2026 update was found.

#### Cited Findings
- The best-performing model, Gemini 2.5 Pro, "completes only 0.48% of VideoGameBench and 1.6% of VideoGameBench Lite" [corrected by fact-check: was attributed to "Gemini 2.5 Pro and Claude 3.7 Sonnet"; source: abstract via search extract of https://arxiv.org/abs/2505.18134, secondary]. [uncertain: the quote "the first checkpoint in a single game" was not re-verified.]
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
- Drivers: navigation from screenshots, memory over hundreds of hours, and correcting wrong beliefs. Harness differences make runs incomparable; it is a showcase, not a benchmark [I].

#### Gaps
- Gemini 2.5 Pro beat Pokémon Blue in May 2025 (per the LessWrong post, via search extract [S]); its harness details were not re-verified.
- There is no controlled human playtime baseline. The same LessWrong author cites an informal figure of about 26 hours for an average human to finish Red [S](https://www.lesswrong.com/posts/HyD3khBjnBhvsp8Gb/so-how-well-is-claude-playing-pokemon).

### 2.19 Computer use and web: OSWorld (and 2.0), WebArena, GAIA

#### Takeaway
- **OSWorld flipped.** Agents passed humans on 11 Dec 2025 (multi-rollout) and 25 Feb 2026 (single rollout), and reached 90.19% in Jul 2026.
- **GAIA flipped** narrowly on the test set: 93.36% vs 92% (secondary sources).
- **WebArena is within about 4 pp** of its human figure.
- **OSWorld 2.0** (Jun 2026) resets headroom with long tasks, but no human success rate was found. Headline OSWorld 2.0 numbers are *partial-credit* scores; strict (binary) completion rates are far lower, about 28–42% [S].

#### Cited Findings
- **OSWorld launch.** "Humans can accomplish over 72.36% of the tasks" [P](https://raw.githubusercontent.com/os-world/os-world.github.io/main/index.html).
- **Official OSWorld-Verified results** (my parse of the xlsx; 144 scored entries) [P](https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx): first above human was Agent S3 w/ Opus 4.5 + GPT-5 bBoN (N=10) at 72.58% (2025-12-11); first single-rollout was HIPPO Agent w/ Opus 4.5 at 74.48% (2026-02-25); best is Intelligence-Indeed Agent at 90.19% (2026-07-25). Claude Fable 5 scores 85.96%; 16 entries are at or above 72.36%. Step budget: Sonnet 4.5 scores 42.88%, 58.08% and 62.88% at 15, 50 and 100 steps.
- **OSWorld 2.0.** 108 long-horizon tasks; the median task takes a skilled human about 1.6 hours of active operation.
  - GPT-6 Astra scores 72.6% and Opus 5 70.6% [S](https://snorkel.ai/leaderboard/os-world-2-0/) [verified (secondary): both are self-reported *partial* scores. Astra's was measured on an offline subset under latency simulation.] [corrected by fact-check: these are not the top scores. Claude Fable 5.1 reports 77.9% partial (41.7% strict; its card says tasks and grading were modified), and Simular Sai reports 73.0% partial (28.25% binary). Snorkel's independent run of Opus 5 gives 68.31% partial and 31.43% binary. Source: https://raw.githubusercontent.com/steel-dev/leaderboard/main/src/data/osworld2.json (steel.dev data file, secondary). Anthropic reports Claude Opus 5.5 at 81.8% partial on a newer **OSWorld 2.1** [P](https://www.anthropic.com/claude-opus-5-5).]
  - Opus 5 scores 70.57% (500 steps, 5-run average) [P-m](https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md).
- **WebArena.** Humans 78.24%, GPT-4 14.41% at launch. Best in 2026: WebTactix (DeepSeek v3.2) at 74.3% (Feb 2026) [S](https://leaderboard.steel.dev/leaderboards/webarena/). The repo links a Google-Sheets leaderboard and human trajectories on about 170 tasks [P](https://raw.githubusercontent.com/web-arena-x/webarena/main/README.md).
- **GAIA.** Humans 92% vs GPT-4 with plugins 15% at launch.
  - Test-set leader: CustomGPT.ai Research Lab v44 at 93.36% (15 Jul 2026) [S](https://leaderboard.steel.dev/leaderboards/gaia/) [verified (secondary): search extracts give 93.36% (281/301 test tasks; L1 97.85, L2 91.82, L3 89.80), but with a submission date of 3 Jun 2026, not 15 Jul. The steel.dev data file on GitHub (last updated 27 May 2026) still shows 92.36% as the top score.]
  - Agents-A1-4B at 95.1% (10 Sep 2026) [S](https://benchlm.ai/benchmarks/gaia) [corrected by fact-check: this is a developer self-report for a model released 14 Jul 2026, not an entry on the official GAIA test leaderboard. The Agents-A1 README's GAIA column values (e.g. 96.04, 98.06, 87.38) are multiples of 1/103, which fits the 103-question text-only *validation* subset [I]. Source: https://raw.githubusercontent.com/InternScience/Agents-A1/main/README.md. It should not be compared with the 92% human baseline.]

#### Inferences
- The computer-use gap closed mainly through scaffolds (step budgets, best-of-N, hybrid planners); the step-budget effect alone is 20 pp. The 2023–24 human anchors are now stale [I].

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
| ARC-AGI-1 | Nov 2019 | 98% panel (≥2 solvers); 64.2% avg person | Claude Fable 5 98.5% (Aug 2026; tied by GPT-6 Astra, Sep 2026) [S; max 98.5 in P-m capture]; Opus 5 97.5% [P-m] [corrected by fact-check: was Opus 5 97.5% as best] | **Flipped** (avg person Dec 2024; panel passed Aug 2026) | Few-shot novel abstraction; fell to TTC/RL reasoning, TTT, format familiarity |
| ARC-AGI-2 | Mar 2025 | 100% panel; 60% avg person; $17/task | GPT-6 Astra 95.0% @ $1.12 (Sep 2026) [S]; Opus 5 90.42% [P-m] | **Flipped**: >60% in ~11 mo (Feb 2026), >85% by Jul 2026 [corrected by fact-check: was "~15–18 mo"] | Symbolic interpretation, compositional and contextual rules; fell to refinement harnesses and reasoning scale |
| ARC-AGI-3 | Mar 2026 | 100% of games solved by ≥2 of ~10 people; avg person ~48% RHAE [S; uncertain] | Astra 99.9% (Provider Adapter) / 62.7% (Standard) (3 Sep 2026) [P-m] | **Flipped under provider harness** in ~5 mo (25 Mar → 3 Sep 2026) [corrected by fact-check: was "6 mo"] | Exploration, goal inference, state/memory over long play; harness decided it |
| ARC Prize Kaggle | 2020– | – | 2024: 55.5%; 2025: 24.03% (ARC-AGI-2) [P-m] | Lags frontier APIs | Compute-limited, offline |
| SimpleBench | 2024 | 83.7% (9 people) [S] | 88.4% max on site data (29 Sep 2026) [P-m], attributed to Claude Opus 5.5 [S]; Fable 5.1 86.6% [S] | **Flipped narrowly** (within noise for N=9) [corrected by fact-check: was "Claude Fable 5 81.9% … Near parity"] | Trick wording and distractors; everyday physics and social reasoning |
| Concept | Oct 2025 | >90% [S] | <40% (2025 models) [S] | Unknown (no 2026 run) | Intent reading, sequential hypothesis revision |
| EnigmaEval | Feb 2025 | None formal (hunt teams) | Opus 5 43.9% (Jul 2026, CAIS) / Fable 5 39.3% (SEAL) [S] | Closing ~15–20 pp/yr | Goal discovery, raw multimodal parsing, long chains |
| PlanBench Mystery BW | 2022/2023 | 78% of 50 (plain BW only) [S] | o1-preview 52.8% (2024) [P] | Unknown after 2024 | Lexical-prior removal |
| BlindTest | Jul 2024 | "Expected" 100% (not measured) [P] | Sonnet-3.5 ~75–78% (2024) [P/S] | Unknown | Encoder-to-LLM loss of fine spatial detail; crowding |
| ClockBench | Sep 2025 | 89.1% (5 people) [S] | GPT-5.6 Sol Max 66.7% (~Sep 2026) [S] | Closing fast | Hand/angle localisation, style robustness |
| VPCT | 2025 | 100% (3 volunteers) [S] | Gemini 3 Pro 91% [S] | Near saturated | Trajectory simulation from one image |
| VisFactor | 2025 (v4 2026) | 78.8% (univ. participants) [S] | Gemini-3.1-Pro 54.0% [S] | Durable (so far) | Psychometric visual factors |
| VSI-Bench | Dec 2024 | 79% avg [S] | SSR-3D 73.9 (Mar 2026, specialised) [S] | Nearly closed via spatial training | Relational 3D from video; humans weak on metric estimates |
| MindCube | Jun 2025 | ~95% [S; uncertain] | 61.3% (trained, Mar 2026) [P]; other paper versions report up to 76.1% [S] | Durable | No persistent allocentric map |
| MMSI-Video-Bench | Dec 2025 | 96.4% [P] | Gemini 3 Pro 38.0% [P] | Large, new | Multi-video spatio-temporal integration |
| IntPhys 2 | Jun 2025 | 96.44% (92.44% held-out) [S] | V-JEPA 2 57.51% [S] | Durable | Violation-of-expectation physics in video |
| Physics-IQ | 2025 | No human (physical-variance ceiling 100) | 58.2 v2v (Jun 2026) [P] | Slow | Physical realism in generation |
| BALROG NetHack | Nov 2024 | Expert humans ascend (no % given) | Astra (max) 13.24% progression (Sep 2026) [P]; Astra *ascended* with self-built harness (21 Sep 2026) [P] | Protocol gap durable; open-tool gap closed | Tacit knowledge, 10⁴-turn state, irreversibility |
| VideoGameBench | May 2025 | Not measured | Gemini 2.5 Pro 0.48% (2025) [S] | Unknown in 2026 | Real-time pixels, long horizon |
| Pokémon Red/Blue | 2025 showcase | Casual players finish (no controlled N) | Opus 4.7 beat Red (May 2026) [S] | Flipped (slowly, harness-dependent) | Navigation, memory, self-correction |
| OSWorld (-Verified) | Apr 2024 | 72.36% [P] | 90.19% (25 Jul 2026) [P] | **Flipped** 11 Dec 2025 | Scaffolding and step budgets closed it |
| OSWorld 2.0 | Jun 2026 | No success-rate baseline; median task 1.6 h [S] | Partial-credit scores: Claude Fable 5.1 77.9% (self-reported, modified tasks; 41.7% strict) [S]; Astra 72.6% [S]; Opus 5 70.57% [P-m]. Strict completion about 28–42% [S]. Opus 5.5 81.8% partial on OSWorld 2.1 [P] [corrected by fact-check: Astra was presented as best, and the scores' partial-credit nature was not stated] | New | Long-horizon real tasks |
| WebArena | Jul 2023 | 78.24% [S] | WebTactix 74.3% (Feb 2026) [S] | Near parity | Multi-step web state |
| GAIA | Nov 2023 | 92% [S] | 93.36% test set (CustomGPT.ai v44, ~Jun 2026) [S] [corrected by fact-check: was "93.4–95.1%"; the 95.1% is a self-reported validation-style number] | **Flipped narrowly** (2026) | Tool use and retrieval chains |

---

## 4. Design lessons (with evidence tags)

1. **Pre-register the harness, or run two labelled tracks** (as ARC now does with Standard and Provider Adapter [P-m]). Otherwise the score measures the harness. Evidence: ARC-AGI-3 62.7% → 98.6% at the same model and effort [P-m]; a 20 pp step-budget effect on OSWorld [P]; NetHack 13% under protocol vs a win with a self-built harness [P].
2. **Measure human anchors properly and report distributions** (median person, top quartile, panel), not "≥2 solvers". Evidence: average vs panel is 64.2 vs 98 (ARC-AGI-1) and 60 vs 100 (ARC-AGI-2) [P-m]; the ARC-AGI-3 baseline was rewritten three weeks after launch [P]; BlindTest's human figure was never measured [P]; SimpleBench N=9, ClockBench N=5, VPCT N=3 [S].
3. **Efficiency is a measured axis, not a moat.** ARC-AGI-3's action efficiency was meant to be the "dividing line" but fell once models "understood" the mechanics [P-m]. Cost per task collapsed as well ($1.12 AI vs $17 human on ARC-AGI-2) [S/P-m].
4. **Durable gaps sit where information must survive a perception-to-reasoning bottleneck:** encoder-to-LLM spatial loss (BlindTest probes [S]), video object permanence (IntPhys 2 near chance [S]), allocentric maps (MindCube [P]), multi-video integration (MMSI-Video [S]). Text-renderable states (ARC grids, web DOM, terminal NetHack) were closed by reasoning plus tools [P/P-m].
5. **Ship mechanism ablations with the benchmark,** to separate "hard for AI" from "hard in general". Models to copy: Mystery vs plain Blocksworld with a classical-planner control [P]; transcribed vs raw PDF (EnigmaEval) [S]; spaced vs crowded shapes (BlindTest) [S]; real-time vs paused (VideoGameBench) [S]; the MindCube scaffold ablation [P].
6. **Expect "knowledge overfitting" without item leakage.** ARC found models using its colour encoding unprompted [P-m]. Private sets are necessary but not sufficient; the format family also needs replacing about yearly, as ARC does [P-m].
7. **Keep the full data private.** ClockBench publishes 10 of 180 clocks [P]; IntPhys 2 withholds held-out metadata [P]; ARC keeps private splits [P-m]. This did not stop ARC falling [I]. Counter-example: EnigmaEval's full dataset was made public on 23 Jul 2026 [S], so its later scores need contamination caveats.
8. **Real-time, irreversible, long-horizon settings are the least-closed agentic gaps:** VideoGameBench 0.48% [S]; NetHack protocol progression about 13% [S]. [Speculation] A game with wall-clock limits, no web access and required in-episode learning would keep headroom longer than turn-based puzzles.
9. **Anchors go stale; report ratio to a contemporaneous human re-baseline.** OSWorld's 72.36% now sits below 16 agent entries [P].
10. **Track closure speed as the durability metric.** ARC-AGI-1 took 5 years, ARC-AGI-2 about 11 months (to pass the 60% average), ARC-AGI-3 about 5 months (provider harness) [corrected by fact-check: were "about 15 months" and "6 months"]; ClockBench went from 13 to 67 in about 12 months [P-m/S]. A new "human > AI" benchmark should expect targeted post-training within 6–12 months of attention [I].

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
| ARC-AGI-3 avg human; participants per report | 48% [uncertain]; 486 participants across 414 candidate environments | 2026 | https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf | Secondary (search extract) | L (48%); M (486) |
| ARC-AGI-3 baseline change | 2nd-best → median human; cap 1.0 → 1.15 | 14 Apr 2026 | https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx | Primary | H |
| ARC Prize 2026 Milestone 1 winner | Tufa Labs "The Duck" | 30 Jun 2026 | https://arcprize.org/blog/arc-prize-2026-milestone-1 | Secondary | M |
| SimpleBench human vs best | 83.7% (N=9) vs max 88.4% (Claude Opus 5.5 per aggregators) [corrected by fact-check: was Claude Fable 5 81.9%, 10 Jun 2026] | 29 Sep 2026 | https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-simple-bench-snapshot-2026-09-10/producer-packet-r1.md | Primary (capture; value range only) + secondary (model names) | M |
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
| MMSI-Video-Bench | Humans 96.4% vs Gemini 3 Pro 38.0% | Dec 2025 | https://raw.githubusercontent.com/InternRobotics/MMSI-Video-Bench/main/README.md | Primary | H |
| IntPhys 2 | Humans 96.44%; V-JEPA 2 57.51%; MLLMs ~chance | Jun 2025 | https://www.emergentmind.com/topics/intphys-2 | Secondary | M |
| Physics-IQ Verified top | 58.2 (v2v), 48.2 (i2v) | Jun–Sep 2026 | https://raw.githubusercontent.com/google-deepmind/physics-IQ-benchmark/main/README.md | Primary | H |
| BALROG NetHack progression | GPT-6 Astra (max) 13.24 ± 2.66% | merged 19 Sep 2026 | https://github.com/balrog-ai/experiments/pull/19 | Primary | H |
| NetHack ascension by GPT-6 Astra | 37,140 turns; web/wiki/tools; 3rd try | 21 Sep 2026 | https://raw.githubusercontent.com/kenforthewin/nethack_astra/main/README.md | Primary | H |
| VideoGameBench | 0.48% (VGB), 1.6% (Lite) | May 2025 | https://arxiv.org/abs/2505.18134 | Secondary extract | M |
| Claude beats Pokémon Red | Opus 4.7 | May 2026 | https://www.lesswrong.com/posts/sehJYg5Yny9fvpbpt/a-year-late-claude-finally-beats-pokemon | Secondary | M |
| OSWorld human; flip; best | 72.36%; 72.58% (2025-12-11); 90.19% (2026-07-25) | 2024–26 | https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx | Primary | H |
| OSWorld step-budget effect | Sonnet 4.5: 42.88 / 58.08 / 62.88% | 2025 | same | Primary | H |
| OSWorld 2.0 | Partial scores: Fable 5.1 77.9%, Astra 72.6%, Opus 5 70.57%; strict about 28–42% | Jun–Sep 2026 | https://raw.githubusercontent.com/steel-dev/leaderboard/main/src/data/osworld2.json | Secondary (Opus: primary mirror) | M |
| WebArena | Human 78.24%; best 74.3% | Feb 2026 | https://leaderboard.steel.dev/leaderboards/webarena/ | Secondary | M |
| GAIA | Human 92%; test leader 93.36% (submitted ~3 Jun 2026) [corrected by fact-check: "95.1% (Sep)" is a self-reported, non-test-set figure] | 2026 | https://leaderboard.steel.dev/leaderboards/gaia/ | Secondary | M |

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

**Not verifiable this session:** blocked hosts (arcprize.org JSON rows, simple-bench.com, cbrower.dev, clockbench.ai, balrogai.com, vgbench.com, GAIA and IntPhys 2 HF leaderboards, arXiv full texts, lesswrong.com); search budget exhausted before the Gemini-Pokémon, VPCT-2026, MindTopo and SimpleBench-2026 checks.

---

## Fact-check log (Phase 1)

**Tally:** 36 verified · 11 corrected · 8 uncertain · 0 removed (55 claims or claim groups checked; every prioritized claim was checked).
**Most consequential:** SimpleBench has flipped narrowly (site data max 88.4 vs 83.7 human; the 81.9% was stale prose). GAIA's "95.1%" is not a test-set score. The OSWorld 2.0 leader and its partial-credit metric were misstated. ARC-AGI-1's best is 98.5%, above the panel. ARC-AGI-2 and -3 closure times were shorter than stated (about 11 and about 5 months).
**Access:** arcprize.org, arxiv.org, simple-bench.com, x.com, openai.com, huggingface.co, kaggle.com, scale.com and most aggregators were blocked. Primary evidence came via raw GitHub (READMEs, captures, the OSWorld xlsx, the balrog-ai PR) and anthropic.com; search extracts are marked secondary.

**ARC-AGI-3 launch-score conflict (A/E "under 1%" vs F "7.78%"): resolved; both are correct for different dates.** At launch (25 Mar 2026) every frontier model scored under 1%: Gemini 3.1 Pro 0.37%, GPT-5.4 0.26%, Opus 4.6 0.25% (paper digest [P-m] plus launch coverage [S]). The 7.78% is GPT-5.6 Sol (max), released 9 Jul 2026. It was the best *pre-Opus-5* score cited in the Opus 5 system card (30.16%, "roughly four times" the prior best; Opus 5 released 24 Jul 2026). The timeline is therefore <1% (Mar) → 7.78% (Jul) → 30.16% (24 Jul) → 62.7% Standard / 99.9% Provider Adapter (3 Sep). F's framing ("from a best of 7.78% … about 5 months after launch") omits the launch value but is not wrong.

**Other sibling conflicts:**
- E gives IntPhys 2's best model as Gemini 2.5 Flash at 55.63%; A gives V-JEPA 2 at 57.51%. Both numbers appear in search extracts, and E appears to count MLLMs only.
- F gives the ARC-AGI-2 average human as 66% (public-eval README [P]); A gives 60% (launch post [P-m]). Both are primary but describe different samples.
- E's SimpleBench claim (Opus 5.5 88.4%) is consistent with the correction here.

| Claim | Verdict | Source URL | Note |
|---|---|---|---|
| ARC-AGI-1/2 panel 98/100%, average 64.2/60%, $17/task, 400+ testers | verified | https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md | Mirror of the arcprize.org launch post (24 Mar 2025) |
| ARC-AGI-2 launch: pure LLMs 0%, o3-preview-low 4%, o1-pro 1%; three failure modes | verified | same | Quotes match |
| o3-preview 75.7% ($10k) / 87.5% (172×); trained on 75% of the public train set | verified | https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/sources/o3_announcement.html | 20 Dec 2024 |
| ARC Prize 2024: 33→55.5%, ARChitects 53.5%, 1,430 teams / 17,789 entries, 2020 ensemble 49% | verified | https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2024/2412.04604v2_arc_prize_2024.md | |
| ARC Prize 2025: 1,455 teams / 15,154 entries; NVARC 24.03, ARChitects 16.53, MindsAI 12.64 | verified | https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md | The top-3 split is also in the report itself |
| Poetiq: Gemini 3 Pro 31% @ $0.81 → 54% @ $31; "knowledge overfitting"; "bottlenecked by engineering" | verified | same | |
| Opus 5 ARC-AGI-1 97.50%, ARC-AGI-2 90.42%, ARC-AGI-3 30.16%; Opus 4.7 75.83%; GPT-5.6 Sol 7.78%; Opus 4.8 1.52% | verified | https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md | Mirror; www-cdn PDF blocked. anthropic.com/news/claude-opus-5 confirms the 24 Jul 2026 release and "three times … next-best" on ARC-AGI-3 |
| ARC-AGI-1 best is Opus 5 97.5% ("match the panel") | corrected | https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-1/packet-r1.md | Capture max 98.5. Search extracts: Claude Fable 5 98.5% (ARC post 5 Aug 2026), tied by GPT-6 Astra (3 Sep) |
| GPT-6 Astra ARC-AGI-2 95.0% @ $1.12/task | verified | https://x.com/arcprize/status/2095597602545025138 | Secondary (several extracts agree); capture max 95 [P-m] |
| ARC-AGI-2 "~15 months" to pass the 60% average | corrected | https://9to5google.com/2026/02/12/gemini-3-deep-think-upgrade/ | About 11 months: Deep Think 84.6% (12 Feb 2026) and Opus 4.6 68.8% (Feb 2026), secondary |
| Astra ARC-AGI-3: 62.7% Standard (max, $26,098), 99.9% Provider (high, $18,817), 98.6% Provider (max) | verified | https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md | Translation of arcprize.org/blog/astra (3 Sep 2026); full effort table matches |
| Astra fewer actions than median human on 96.0% of levels; −51.7% | corrected (clarified) | same | Figures come from the **max-effort 98.6%** run, not the 99.9% run. Summary bullet fixed |
| Provider Adapter keeps native reasoning state plus compaction; Standard keeps visible notes (`manual_rolling`) | verified | https://raw.githubusercontent.com/arcprize/arc-agi-3-benchmarking/main/README.md | |
| ARC-AGI-3: 135 environments, 25 public; 458 humans, 90 min; tr87 6/12; 342 replays; ~1M scorecards; <$10k display policy | verified | https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md | Capture of the 14 Apr 2026 blog |
| Scoring change: 2nd-best → median human; cap 1.0 → 1.15 (14 Apr 2026) | verified | https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx | |
| 64×64 grid, 5 moves + select + undo, 5× cutoff, RHAE (h/a)² | verified | https://raw.githubusercontent.com/memgrafter/research-digests/491d1e597ee1384396057fbe72e2bdec9f11c2c6/ml_research_analysis_2026/2603.24621_arc-agi-3-a-new-challenge-for-frontier-agentic-intelligence_20260331_185732.md | Paper digest |
| ARC-AGI-3 launch: frontier <1% | verified | https://officechai.com/ai/arc-agi-3/ | Best 0.37% (Gemini 3.1 Pro); secondary plus digest |
| ARC-AGI-3 "6 months" to human level | corrected | (dates above) | 25 Mar → 3 Sep 2026 ≈ 5 months |
| Tech report "486 participants" conflicts with 458 | corrected (clarified) | https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf | Search extract: 486 across **414 candidate** environments, so not a true conflict |
| ARC-AGI-3 average human 48% | uncertain | — | Seen only in unattributed search extracts; not in the report extract |
| OpenAI "two settings tripled" | verified | https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/ | Secondary: retained reasoning + compaction, GPT-5.6 Sol 13.3 → 38.3% on the public set (late Jul 2026) |
| ARC Prize 2026 Milestone 1: Tufa Labs "The Duck" | verified | https://arcprize.org/blog/arc-prize-2026-milestone-1 | Secondary; added score 1.21% (runners-up 0.867%, 0.864%) |
| SimpleBench: Fable 5 81.9% vs human 83.7% (N=9), "near parity" | corrected | https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-simple-bench-snapshot-2026-09-10/producer-packet-r1.md | simple-bench.com leaderboard-data.js on 29 Sep 2026: 104 values, max 88.4, 3 new rows. Page prose still says 81.9% (stale). Human 83.7%/N=9 verified. Flipped narrowly (confirms the Panel B cross-panel note) |
| SimpleBench model attributions: Opus 5.5 88.4%, Fable 5.1 86.6%, GPT-6 Astra Pro 86.5% | uncertain | https://benchmarklist.com/benchmarks/simplebench/ | Aggregator only; Astra Pro 86.5% not found in any source reachable here |
| OSWorld human 72.36% | verified | https://raw.githubusercontent.com/os-world/os-world.github.io/main/index.html | |
| OSWorld-Verified: 144 entries; first above human 72.58% (2025-12-11, bBoN N=10); HIPPO 74.48% (2026-02-25); best 90.19% (2026-07-25); Fable 5 85.96%; 16 ≥ 72.36; Sonnet 4.5 42.88/58.08/62.88 | verified | https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx | Re-parsed independently; Excel serial dates converted |
| OSWorld human-vs-agent comparability | uncertain | same | Human rate from the 2024 task set; agents on the revised Verified set |
| OSWorld 2.0: Astra 72.6%, Opus 5 70.6% (best) | corrected | https://raw.githubusercontent.com/steel-dev/leaderboard/main/src/data/osworld2.json | These are *partial* scores. Fable 5.1 77.9% partial (41.7% strict) is higher; strict rates are about 28–42%. Opus 5.5 81.8% partial on OSWorld 2.1 (https://www.anthropic.com/claude-opus-5-5) |
| WebArena human 78.24%, GPT-4 14.41%; WebTactix 74.3% (Feb 2026); ~170 human trajectories | verified | https://raw.githubusercontent.com/steel-dev/leaderboard/main/src/data/webarena.json | Aggregator data file (secondary); trajectories from the WebArena README [P]; WebTactix is self-reported |
| GAIA test leader CustomGPT.ai v44 93.36% (15 Jul 2026) | verified (date corrected) | https://customgpt.ai/gaia-state-of-the-art-agent-harness/ | Secondary: 281/301; submission dated ~3 Jun 2026 |
| GAIA Agents-A1-4B 95.1% (test set) | corrected | https://raw.githubusercontent.com/InternScience/Agents-A1/main/README.md | Self-reported; 4B model released 14 Jul 2026; the numbers fit the 103-question text-only validation subset [I]; not a test-set entry |
| GAIA human 92% | verified | https://arxiv.org/abs/2311.12983 | Paper abstract (known figure; arXiv blocked) |
| Concept >90% humans vs <40% LLMs; Findings of ACL 2026 | verified | https://aclanthology.org/2026.findings-acl.1219/ | Search extract of the abstract |
| EnigmaEval 1,184 puzzles / 8 sources; SEAL Fable 5 39.28±2.80 | verified | https://labs.scale.com/leaderboard | Secondary |
| EnigmaEval: Opus 5 43.9% on the "CAIS dashboard" | uncertain | — | No source found |
| EnigmaEval now public (23 Jul 2026) | added | https://x.com/CAIS/status/2080344746699170214 | Secondary; date from the tweet ID. Contamination caveat added to lesson 7 |
| PlanBench table (GPT-4o 0%, o1-preview 52.8/37.3, R1 43.3/25.8) | verified | https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md | |
| BlindTest 58.12% avg, Sonnet-3.5 74.94%, "expected" 100%; line intersections 48.67/77.33 | verified | https://raw.githubusercontent.com/anguyen8/vision-llms-are-blind/main/README.md | The line-intersection table is commented out in the README |
| BlindTest journal v6 (58.07%, 77.84%, linear probes) | uncertain | https://arxiv.org/abs/2407.06581 | arXiv blocked; not re-verified |
| ClockBench 10 of 180 public; 89.1% humans vs 13.3% at launch; 66.7% GPT-5.6 Sol Max | verified | https://raw.githubusercontent.com/aleksafar/clockbench/main/README.md | 10/180 [P]; scores secondary (theslowai extract). Human N=5 not re-verified |
| VPCT: 3 volunteers 100%; Gemini 3 Pro 91% | verified | https://llmlearner.com/rankings/vpct | Secondary (leaderboard update 6 May 2026) |
| VisFactor: 20 subtests, 39 MLLMs; humans 78.8% vs Gemini-3.1-Pro 54.0% | verified | https://raw.githubusercontent.com/CUHK-ARISE/VisFactor/main/README.md | Scores via search extract of v4 |
| VSI-Bench: 15 MLLMs, CVPR 2025 oral; SSR-3D 73.9 (+4.4 over InternVL3.5-241B) | verified | https://raw.githubusercontent.com/vision-x-nyu/thinking-in-space/main/README.md | SSR secondary |
| MindCube: 21,154 Q / 3,268 images; 37.8 → 57.8 → 61.3 | verified | https://raw.githubusercontent.com/mll-lab-nu/MindCube/main/README.md | Other versions report 70.67 / 76.1 |
| MindCube human ~95% | uncertain | — | Not found |
| MMSI-Video-Bench humans 96.4% vs Gemini 3 Pro 38.0% | verified | https://raw.githubusercontent.com/InternRobotics/MMSI-Video-Bench/main/README.md | Upgraded to [P] (96.40 vs 37.97) |
| IntPhys 2: 1,012 main + 344 held-out; humans 96.44/92.44; V-JEPA 2 57.51 | verified | https://raw.githubusercontent.com/facebookresearch/IntPhys2/main/README.md | Counts [P]; scores secondary; see the E conflict above |
| Physics-IQ Verified: 58.2 v2v (2026-06-19), 48.2 i2v (2026-09-28), Veo 3.1 Fast 29.96 | verified | https://raw.githubusercontent.com/google-deepmind/physics-IQ-benchmark/main/README.md | |
| BALROG NetHack: GPT-6 Astra-Max 13.2 ± 2.7% | verified | https://github.com/balrog-ai/experiments/pull/19 | Upgraded to [P]: 13.24 ± 2.66%, merged 19 Sep 2026 |
| BRAID: GPT-5.2 12.56% | corrected | https://kenforthewin.github.io/blog/posts/nethack-agent/ | Secondary extract: 2.56% average, 12.56% maximum |
| NetHack ascension by GPT-6 Astra (21 Sep 2026; 37,140 turns; 1,766,446 pts; 3rd attempt; web/wiki; not BALROG protocol) | verified | https://raw.githubusercontent.com/kenforthewin/nethack_astra/main/README.md | |
| VideoGameBench 0.48% / 1.6% by "Gemini 2.5 Pro and Claude 3.7 Sonnet" | corrected | https://arxiv.org/abs/2505.18134 | Best model is Gemini 2.5 Pro alone (abstract via search extract) |
| VideoGameBench "first checkpoint in a single game" quote | uncertain | — | Not re-verified |
| Pokémon: 140 h / 3 badges, 78 h in Mt. Moon; Opus 4.7 beat Red (May 2026); Jev Hall of Fame 23 Sep 2026 | verified | https://www.lesswrong.com/posts/sehJYg5Yny9fvpbpt/a-year-late-claude-finally-beats-pokemon | Secondary. jev-pokemon README [P] confirms Jev beat the game (stream 25–26 Sep) |
| MindTopo: GPT-5.6-Sol 61.42% vs humans 97.87% | verified | https://arxiv.org/html/2609.11900v1 | Search extract (secondary) |
| Model names: GPT-6 Astra, GPT-5.6 Sol, Claude Opus 5, Claude Fable 5 | verified | https://www.anthropic.com/news/claude-opus-5 | Opus 5 released 24 Jul 2026; Opus 5.5 22 Sep 2026 [P]. Astra launched 3 Sep 2026, GPT-5.6 on 9 Jul 2026 [S] |
| SpatialViz-Bench, SpatiaLab, CityCube leads | uncertain | — | Not checked (left as leads) |
