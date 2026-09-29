# Prior Art for Novel Non-Game LLM Evaluation Methods (2023-2026)

Compiled 2026-09-29 by the prior-art research subagent.

**Fact-check status (added 2026-09-29).** An adversarial fact-check pass re-verified the 16 load-bearing claims and all 65 references against independent GitHub-hosted sources: official repos, arXiv-listing mirrors, and daily arXiv digests. WebSearch was also exhausted for that pass. Corrections are marked inline with "[corrected by fact-check]". The full record is in "## Verification log" at the end of this file.

**Tooling caveat.** The session's shared WebSearch budget ran out before this subagent's first query (0 of about 30 planned searches ran). All evidence below comes from three sources:

1. WebFetch of GitHub READMEs (primary repos).
2. GitHub repository search.
3. GitHub code search. This surfaced paper abstracts, BibTeX, curated paper lists and third-party paper notes that quote arXiv IDs and numbers.

The limits of that evidence:

- arXiv, OpenReview, ACL Anthology and lab blogs could not be opened directly.
- Every arXiv ID below was seen written in a GitHub-hosted page, and the page is recorded as `seen_url` in the JSON file.
- Numbers seen only in third-party notes or digests are tagged **[S]** (secondary). Numbers seen in an official repo, or in a paper's own abstract or BibTeX, are tagged **[P]** (primary or near-primary).
- Anything not seen this session is labelled "unverified" or left out.

Confidence levels:

- **H** = seen in a primary source, or in two or more independent sources.
- **M** = one reliable secondary source, or a primary source summarised by the fetch model.
- **L** = a single weak source, or conflicting sources.

---

## Summary

Between 2023 and 2026 the field produced at least twelve families of non-game evaluation methods. Each was meant to escape the three failure modes of static QA benchmarks: contamination, saturation, and weak links to real-world value.

1. **Procedural and dynamic generation.** Examples: DyVal, DyVal 2, NPHardEval, NPPC, KOR-Bench, CHASE, Skill-Mix, GSM-Symbolic, functional MATH(), Benchmark Self-Evolving, Reasoning Gym.
2. **Live/temporal benchmarks.** Examples: LiveBench, LiveCodeBench, ForecastBench, FutureX, Prophet Arena, KalshiBench, and Uncheatable Eval (compression on fresh text).
3. **Economic-value benchmarks.** Examples: GDPval, SWE-Lancer, Remote Labor Index.
4. **In-context learning of genuinely novel material.** Examples: MTOB, LINGOLY, CodeUpdateArena, EvaLearn.
5. **Model-as-examiner and peer evaluation.** Examples: LM-as-Examiner, KIEval, TreeEval, LLM-as-an-Interviewer, Auto-Arena, Language Model Council, peer prediction, and debate.
6. **Teaching and tutoring.** Examples: Saha et al. 2023, EducationQ, MathTutorBench, and two different benchmarks both named TutorBench.
7. **Compression-as-intelligence.** Huang et al. 2024 and Uncheatable Eval.
8. **Consistency and metamorphic testing.** Examples: consistency checks for superhuman models and for forecasters, generator-validator (GV) consistency, the Reversal Curse, and DyCodeEval.
9. **Calibration and abstention.** Examples: AbstentionBench and KalshiBench.
10. **Scientific discovery.** Examples: ScienceAgentBench, MLE-bench, PaperBench, BrainBench, AI Scientist v1/v2, the ideation-execution studies, and LAB-Bench.
11. **Long-horizon memory and state tracking.** Examples: LongMemEval, BABILong, Michelangelo.
12. **Verification-generation asymmetry.** Examples: GV-consistency, the Generative AI Paradox, BrowseComp's "hard to find, easy to verify" design, and a 2026 factual GV-gap paper.

Four patterns show up across the families:

- **Renewability and cheap, objective grading are rarely achieved together.**
  - Symbolic procedural generators (NPHardEval, NPPC, DyVal, Reasoning Gym) are infinite and exactly verifiable. But they test narrow algorithmic or puzzle skills, and the field treats them as RL training environments more than as flagship leaderboards.
  - LLM-generated evolving benchmarks (Benchmark Self-Evolving, CHASE, BenchAgents) scale better. But they inherit generator bias, which is the user's "echo chamber" objection to item 10.
  - Temporal benchmarks (LiveBench, FutureX, ForecastBench, Prophet Arena) are contamination-proof. But they need resolution delays or continuous human curation.
  - Economic benchmarks (GDPval, RLI) have the highest face validity. But they are expensive, rely on expert or LLM graders, and have small public sets.
- **"Learning" is almost never the measured construct.** The frontier is shifting from what a model knows to how well it learns from new material or teaches it. Examples: MTOB, EvaLearn, EducationQ, Saha et al. Each existing instance has a serious validity hole:
  - MTOB is one language. Aycock et al. showed the gains come from the book's parallel examples, not its grammar explanations.
  - EducationQ reuses contaminated GPQA and MMLU-Pro questions.
  - EvaLearn uses fixed problems.
  - MathTutorBench scores pedagogy with a reward model, not learning gain.
- **Ground-truth-free methods are maturing but have no leaderboard.** Consistency checks, peer prediction (ICLR 2026), debate and GV-consistency all show that evaluation without labels can work, including for models stronger than the grader. None has become a maintained, widely cited leaderboard.
- **Calibration is a separate capability that most leaderboards ignore.** AbstentionBench and KalshiBench show that reasoning models are over-confident. Only the forecasting benchmarks score with proper scoring rules.

**Most promising unfilled niche (interpretation).** No benchmark combines four properties:

- (a) procedurally generated, never-seen material (a synthetic language, formal system or API);
- (b) learning or teaching gain as the headline metric, with the student's post-test graded by an exact verifier rather than an LLM judge;
- (c) proper-scoring calibration;
- (d) one comparable scale across components.

Details are in "Implications" below.

---

## Detailed findings

Format of each entry: what it measures / strengths / weaknesses / adoption evidence seen / gap left. Source tags: [P] = primary or near-primary, [S] = secondary.

### 1. Procedural and dynamic generation (contamination resistance by construction)

**DyVal** (Zhu, Chen, Wang, Gong, Yang, Xie; arXiv:2309.17167)
- The promptbench BibTeX titles it "DyVal: Graph-informed Dynamic Evaluation of Large Language Models" [P, https://github.com/microsoft/promptbench]. A third-party reference list gives the arXiv title as "DyVal: Dynamic Evaluation of Large Language Models for Reasoning Tasks" [S].
- The EMNLP 2025 contamination survey's list gives the venue as ICLR 2024 [S, https://github.com/SeekingDream/Static-to-Dynamic-LLMEval].
- Measures: reasoning on items generated "on-the-fly with controlled complexity" from DAGs (arithmetic, logic, algorithmic tasks) [P].
- Strengths: infinite items, and difficulty is a tunable graph parameter.
- Weaknesses: synthetic templates are far from real use. Models can be trained on the generator itself.
- Adoption: integrated into Microsoft's promptbench library [P].

**DyVal 2 / Meta Probing Agents (MPA)** (Zhu, Wang, Zhao, Xu, Xie; arXiv:2402.14865; ICML 2024 per the promptbench news)
- Uses LLM "probing agents" to transform existing benchmark items along psychometric dimensions (language understanding, problem solving, domain knowledge) [S, https://github.com/lyy1994/awesome-data-contamination; P for the venue, promptbench].
- Weakness: the transformations are generated by an LLM, so they carry generator bias.

**NPHardEval** (Fan, Hua, Li, Ling, Zhang; arXiv:2312.14890; ACL 2024 per the survey list)
- Algorithmic problem types (the repo lists BSP, EDP, GCP, KSP, MSP, SPP, TSP and variants) across P, NP-complete and NP-hard. The data is versioned (V0/V1/V2), and "replaced all data" in the Jan 2024 V1 release [P, https://github.com/casmlab/NPHardEval].
- Early README leaderboard: GPT-4 at about 0.72 (P), 0.35 (NP-complete) and 0.057 (NP-hard). Accuracy falls with complexity class [P via fetch summary; M].
- Strengths: difficulty is anchored in complexity theory, and grading is exact.
- Weaknesses: classic textbook problems (TSP, knapsack, graph colouring) are heavily represented in training data. The refresh cadence is not documented.
- Adoption: 66 GitHub stars, repo updated 2026-08-22 [P, GitHub search], plus a multimodal spin-off, NPHardEval4V.

**NPPC, the "Nondeterministic Polynomial Problem Challenge: An Ever-Scaling Reasoning Benchmark for LLMs"** (repo SMU-DIGA/nppc)
- 25 NP-complete problems (12 core, 13 extension), including 3-SAT, TSP and Vertex Cover.
- Modules: `npgym` generates and verifies instances, `npsolver` runs models, `npeval` analyses results.
- Stated design goals: "uncrushable", "unhackable" (infinite instances), "auto-verifiable" and "general" [P, https://github.com/SMU-DIGA/nppc].
- arXiv ID, authors and results not captured this session.
- Weakness: same as NPHardEval. Difficulty scales, but the task family is narrow and well known.

**KOR-Bench: "Benchmarking Language Models on Knowledge-Orthogonal Reasoning Tasks"** (Ma, Du, Wang, Zhang, Wen, Qu, Yang, Liu, Liu, Yue, Huang, Zhang; arXiv:2410.06526)
- Tests novel, knowledge-independent rules given in the prompt, in five categories: Operation, Logic, Cipher, Puzzle, Counterfactual [P, https://github.com/KOR-Bench/KOR-Bench].
- Claude-3.5-Sonnet and GPT-4o reached about 58% [P via fetch summary; M].
- Strength: this is the closest prior art to "learn a new rule system in context".
- Weaknesses: static item set. Rules are short, one-shot and puzzle-like, and there is no learning curve. 19 stars [P, GitHub search].
- Venue not captured.

**CHASE: "How to Get Your LLM to Generate Challenging Problems for Evaluation"** (Patel, Reddy, Bahdanau; arXiv:2502.14678)
- Builds hard items bottom-up from simpler components. It "decomposes the generation process into independently verifiable sub-tasks".
- Domains: document QA, repository-level code completion, math.
- State-of-the-art models score 40-60% [P, https://github.com/McGill-NLP/CHASE].
- Strength: a principled recipe for LLM-generated items with verification.
- Weakness: items still come from an LLM, so there is a risk of shared blind spots with the models being tested.

**Skill-Mix: "a Flexible and Expandable Family of Evaluations for AI models"** (Yu, Kaur, Gupta, Brown-Cohen, Goyal, Arora; arXiv:2310.17567; ICLR 2024)
- The model must write text that combines k randomly sampled skills (a pool of about 101) on a random topic (a pool of about 100).
- Because the number of combinations grows like N^k, outputs must differ from anything in the training data. The digest reports that "GPT-4's reasonable performance on k=5 is suggestive of going beyond 'stochastic parrot' behavior".
- Grading is by GPT-4 and LLaMA-2-70B-Chat with human spot-checks.
- Only about 10% of the skill and topic lists are public.
- Sources: [S, https://github.com/memgrafter/research-digests; ICLR 2024 per https://github.com/MLNLP-World/Top-AI-Conferences-Paper-with-Code].
- Weakness: relies on LLM judges. Hiding 90% of the lists hurts reproducibility.
- Follow-up: Instruct-SkillMix (Kaur, Park, Goyal, Arora; arXiv:2408.14774; ICLR 2025) reused the idea for training data, not evaluation [P, https://github.com/princeton-pli/Instruct-SkillMix].

**"Reasoning or Reciting? Exploring the Capabilities and Limitations of Language Models Through Counterfactual Tasks"** (Z. Wu et al.; arXiv:2307.02477) [corrected by fact-check: the title ends "Counterfactual Tasks", not "Counterfactual Evaluations", per the arXiv listing mirror qhduan/cn-chat-arxiv 2307.02477v2]
- Pairs default tasks with counterfactual variants. Task directories: arithmetic (modified number systems), programming, syntax, spatial, drawing, music, chess (modified rules), SET, logic [P, https://github.com/ZhaofengWu/counterfactual-evaluation].
- Full author list and venue not captured this session.
- Strength: separates reasoning from recall.
- Weakness: a fixed handful of variants, which can now be learned.

**GSM-Symbolic** (Mirzadeh, Alizadeh, Shahrokhi, Tuzel, Bengio, Farajtabar; arXiv:2410.05229; ICLR 2025 per the survey list)
- Templated regeneration of GSM8K with 50 instances per template, plus harder variants P1/P2. Performance varies across instantiations of equivalent problems and drops when an irrelevant clause is added [P, https://github.com/apple/ml-gsm-symbolic].

**Functional benchmarks, MATH()** (Srivastava et al.; arXiv:2402.19450)
- A new instance of the whole benchmark is snapshotted each month. The "reasoning gap" is defined as the percentage drop from static to functional accuracy [P, https://github.com/ConsequentAI/fneval].

**Benchmark Self-Evolving: "A Multi-Agent Framework for Dynamic LLM Evaluation"** (arXiv:2402.11443; COLING 2025, aclanthology 2025.coling-main.223)
- LLM agents rewrite GSM8K, CLUTRR, StrategyQA and BoolQ items using eight modes: paraphrase, add noise, reverse polarity, alternative, complex, retrieval, planning, knowledge [P, https://github.com/nanshine/Self-Evolving-Benchmark; venue per https://github.com/MLNLP-World/Top-AI-Conferences-Paper-with-Code].
- 26 stars [P].
- Weakness: this is exactly the "LLM-generated scenarios" pattern the user flagged as an echo chamber.

**Reasoning Gym: "Reasoning Environments for Reinforcement Learning with Verifiable Rewards"** (Stojanovski et al.; arXiv:2505.24760; NeurIPS 2025 Spotlight)
- More than 100 procedural generators with verifiers, covering algebra, arithmetic, logic, graphs, geometry, cognition and games [P, https://github.com/open-thought/reasoning-gym].
- It is positioned mainly for RLVR training. This is a signal that procedural generators are now training infrastructure, so any benchmark built on the same generator families will be trained on.

**DyCodeEval** (ICML 2025)
- Uses metamorphic testing. Four LLM agents rewrite programming problems into semantically equivalent but textually different variants. Evaluated on 18 models [S, https://github.com/zhaoyang97/Paper-Notes-en].
- [added by fact-check] The survey README lists it as "DyCodeEval: Dynamic Benchmarking of Reasoning Capabilities in Code Large Language Models Under Data Contamination", ICML 2025, arXiv:2503.04149 [S, https://github.com/SeekingDream/Static-to-Dynamic-LLMEval].

**Survey anchor.** Chen et al., "Recent advances in large language model benchmarks against data contamination: From static to dynamic evaluation" (EMNLP 2025; arXiv:2502.17521). Its taxonomy:

- **Temporal cutoff:** LiveBench, LiveCodeBench, ForecastBench, AntiLeak-Bench, AcademicEval, RealMath.
- **Rule-based generation:**
  - Template-based: GSM-Symbolic, Mathador-LM, MMLU-CF.
  - Table-based: S3Eval.
  - Graph-based: DyVal, NPHardEval.
- **LLM-based generation:**
  - Benchmark rewriting: DyCodeEval, StructEval, VarBench.
  - Interactive evaluation: LLM-as-an-Interviewer, TreeEval, KIEval.
  - Multi-agent evaluation: Benchmark Self-Evolving, BenchAgents.
- **Hybrid:** LatestEval, DARG, C2LEVA.

Source: [P, https://github.com/SeekingDream/Static-to-Dynamic-LLMEval].

**Gap in family 1.** Existing generators produce either narrow algorithmic puzzles, with exact verifiers but low ecological validity, or LLM-rewritten natural items, with ecological validity but generator bias. None generates a whole coherent new domain (a language, API or formal science) whose mastery must be acquired and then transferred.

### 2. Live/temporal benchmarks

**LiveBench: "A Challenging, Contamination-Free LLM Benchmark"** (White, Dooley, Roberts, Pal, Feuer, ... LeCun, Goldstein, Neiswanger, Goldblum; arXiv:2406.19314; ICLR 2025 Spotlight)
- 18 tasks in 6 categories: reasoning, math, coding, language, data analysis, instruction following.
- "Each question has verifiable, objective ground-truth answers ... without the use of an LLM judge."
- New questions are released monthly and public release is delayed: "the current LiveBench release is 2025-04-25; however, not all questions for this release are public" [P, https://github.com/LiveBench/LiveBench].
  - [corrected by fact-check] Two clarifications, both from the same README. The most recent *fully public* release is 2024-11-25: users are told to pass `--livebench-release-option 2024-11-25` to evaluate all categories. "Monthly" is the stated design goal. The latest release the README names is 2025-04-25, so the monthly cadence is not evidenced after that date. The "18 tasks" count is described as "currently".
- Strengths: objective grading combined with freshness.
- Weaknesses: it depends on continuous human curation, and the items are still conventional QA.

**LiveCodeBench** (Jain, Han, Gu, Li, Yan, Zhang, Wang, Solar-Lezama, Sen, Stoica)
- Collects LeetCode, AtCoder and Codeforces problems by release date and evaluates only on windows after a model's training cutoff. Four scenarios: generation, self-repair, code execution, test-output prediction.
- Releases grew from v1 (400 problems, May 2023-Mar 2024) to v6 (1,055 problems, May 2023-Apr 2025) [P, https://github.com/LiveCodeBench/LiveCodeBench].
- arXiv:2403.07974 [corrected by fact-check: the ID was previously "not captured". It was confirmed via the arXiv-listing mirror qhduan/cn-chat-arxiv papers/24/03/2403.07974.json and a DeepSeek-R1 bibliography entry, CoRR abs/2403.07974]. The survey lists ICLR 2025.

**ForecastBench: "A Dynamic Benchmark of AI Forecasting Capabilities"** (Karger, Bastani, Chen, Jacobs, Halawi, Zhang, Tetlock; arXiv:2409.19839; ICLR 2025)
- A "dynamic, contamination-free benchmark of LLM forecasting accuracy with human comparison groups". Leaderboards and datasets are updated nightly [P, https://github.com/forecastingresearch/forecastbench].

**FutureX: "An Advanced Live Benchmark for LLM Agents in Future Prediction"** (arXiv:2508.11987; ICLR 2026 per third-party notes)
- Collects not-yet-resolved events daily from 195 sources, has agents predict, then automatically fetches the resolved answers.
- Four difficulty levels, weighted 10/20/30/40%.
- 25 models were evaluated. Grok-4 ranked first. A panel of 40 industry experts "lead[s] significantly in L1, L3, and L4".
- Answer retrieval succeeds more than 97% of the time.
- Stated limitations: long-horizon events are excluded, anti-crawling needs manual review, and metrics differ across levels.
- Sources: [S, https://github.com/zhaoyang97/Paper-Notes-en; arXiv ID also in https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series].
- Adoption: used as an evaluation target by MiroMindAI/MiroFlow [S]. Follow-up FutureX-Pro (arXiv:2601.12259) extends to vertical domains [S].

**Prophet Arena: "LLM-as-a-Prophet: Understanding Predictive Intelligence with Prophet Arena"** (Yang, Mahns, Li, Gu, Wu, Xu; arXiv:2510.17638)
- Continuously collects live forecasting tasks, largely Kalshi prediction markets per tagging [S], and splits each task into pipeline stages.
- Scored on Brier and calibration error, and on market returns.
- Findings: small calibration errors and "promising market returns". Bottlenecks are "inaccurate event recalls, misunderstanding of data sources and slower information aggregation compared to markets when resolution nears".
- Sources: [P abstract as indexed in https://github.com/Hypogenic-AI/news-from-future-ai-aed4-claude; ID in https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series].
- Adoption:
  - Used as the testbed for Live-Evo (arXiv:2602.02369; 10 weeks, 500 tasks) and ForeDreamer (arXiv:2608.20920) [S].
  - A 1,200-question subset is used in Thinking Machines' tinker-cookbook forecasting recipe [S, code search].
  - A GitHub repo named `prophet-arena-iclr-poster` exists, which suggests an ICLR presentation [unverified].

**KalshiBench: "Do Large Language Models Know What They Don't Know?"** (L. Nel; arXiv:2512.16030)
- 300 Kalshi questions that resolve after the models' training cutoffs.
- "Systematic overconfidence across all models". Best ECE was Claude Opus 4.5 at 0.120. GPT-5.2-XHigh had worse calibration (ECE 0.395) "despite comparable accuracy". "Only one model achieves a positive Brier Skill Score" [P abstract as indexed in https://github.com/Hypogenic-AI/news-from-future-ai-aed4-claude].

**"Pitfalls in Evaluating Language Model Forecasters"** (Paleka, Goel, Geiping, Tramèr, 2025)
- Warns about "many forms of temporal leakage" and about the difficulty of extrapolating from evaluation performance to real-world forecasting [P abstract as indexed, same source]. arXiv:2506.00723 [corrected by fact-check: the ID was previously "not captured". It is confirmed in shunta0213/daily-paper cs.AI/20250607/arxiv.csv and the memgrafter/research-digests header]. A daily digest also reports that at least 3.8% of one forecasting dataset's questions had resolved early [S, https://github.com/gabrielchua/daily-ai-papers].

**Gap in family 2.** Live benchmarks guarantee freshness only for knowledge and prediction questions. Forecasting needs days to months before questions resolve, and the scores depend on search tooling. No live benchmark measures learning of fresh structured material with immediate, exact grading.

### 3. Economic and labor value

**GDPval** (OpenAI; arXiv:2510.04374)
- 1,320 tasks across 44 occupations in the 9 sectors that each contribute more than 5% of US GDP. Tasks are built from real work products of professionals with an average of 14 years' experience.
- Graded by blind pairwise comparison by experts [S, https://github.com/memgrafter/research-digests; https://github.com/howard86/howardism].
- Win-or-tie rates vs experts on the 220-task gold subset, paper Fig. 5 [corrected by fact-check]:

  | Model | Wins + ties |
  |---|---|
  | Claude Opus 4.1 | 47.6% |
  | GPT-5 high | 38.8% |
  | o3 high | 34.1% |
  | o4-mini high | 27.9% |
  | Gemini 2.5 Pro | 25.5% |
  | Grok 4 | 24.3% |
  | GPT-4o | 12.4% |

  Sources: the parsed paper text (https://github.com/visual-snow/seshat, parsed/openai/gdpval-...md) and the OpenAI blog chart text mirrored in the same repo (web-research/openai/gdpval.md). howard86/howardism independently gives GPT-4o 12.4%, o3 high 34.1% and GPT-5 high 38.8%. The Grok 4, Gemini 2.5 Pro and o4-mini assignments rely on one parse of the figure (confidence M).
  - The table previously here came from the EnvCommons README (GPT-5 39.0%, o3 35.2%, o4-mini 29.1%, GPT-4o 12.5%). Its numbers do not match the paper; only the 47.6% figure matches.
  - Paper authors: Patwardhan, Dias, Proehl, Kim, Wang, Watkins, et al. (OpenAI).
  - The paper's "roughly linear" improvement claim (Fig. 6) is fitted to three OpenAI models only (GPT-4o, o3 high, GPT-5 high) [S, https://github.com/howard86/howardism; consistent with the parsed Fig. 6].
  - The experimental automated grader agrees with human experts 66% of the time, against 71% human inter-rater agreement [P, parsed paper].
- A later blog discusses a "70.9% win rate" (model not captured) [S, https://github.com/amaarora/amaarora.github.io].
- Adoption: very high. GitHub repository search for "gdpval" returned 60 repos, most of them third-party reimplementations [P, GitHub search].
- Weaknesses:
  - Expert grading is costly, so third parties substitute LLM graders (for example, the EnvCommons/OpenReward environment uses rubric scoring by an LLM grader with tool access [S]). The construct shifts as a result.
  - Only a 220-task gold subset is public [S].

**SWE-Lancer: "Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?"** (arXiv:2502.12115)
- The repo was archived on 18 July 2025 and consolidated into openai/preparedness [P, https://github.com/openai/SWELancer-Benchmark; https://github.com/openai/preparedness]. Task counts were not verified this session.
  - [fact-check note] GitHub metadata shows `archived: true` with a last push on 2025-07-18. The exact archive date is not exposed.
  - Authors, per the GDPval paper's reference list: Miserendino, Wang, Patwardhan, Heidecke.
- Strength: dollar-denominated scores.
- Weakness: one domain (software).

**Remote Labor Index (RLI): "Measuring AI Automation of Remote Work"** (Mazeika et al., CAIS and Scale AI; arXiv:2510.26787)
- Real, paid freelance projects across 3D/CAD, architecture, design, video, audio, data analysis and web.
- **Metric, automation rate:** the share of projects where the AI deliverable is judged at least as good as the human deliverable, i.e. a "reasonable client would accept it" [S, https://github.com/ruvnet/metaharness].
- **Scores:**
  - "The highest-performing agent achiev[ed] an automation rate of 2.5%" at launch [P abstract as indexed in https://github.com/Doragd/Algorithm-Practice-in-Industry].
  - A July 2026 update reportedly reached 16.1% (Fable 5), with GPT-5.5 at 6.3% and Claude Opus 4.8 at 8.3% [S, https://github.com/knomit/cyberai-kb, citing a safe.ai blog].
  - Another secondary source gives the best as 15.8% [S, https://github.com/vadimchernets/papers], so the exact 2026 number is L.
  - [corrected by fact-check] Four independent secondary sources agree on **16.10% (Fable 5)** on the Scale AI × CAIS leaderboard as of 1-2 July 2026, with Opus 4.8 at 8.33% and Codex GPT-5.5 at 6.25%, out of 240 projects:
    - https://github.com/ruvnet/metaharness (leaderboard snapshot);
    - https://github.com/guzus/ai-research-arm (citing @ScaleAILabs);
    - a Latent Space AINews digest (https://github.com/steveash/hitchhikers-guide-to-ai-native-engineering);
    - a ZDNET article mirror (https://github.com/kishorebr/aivibe-blog).

    The 15.8% figure is an outlier; use 16.1% (confidence M).
  - The top agent at launch (2.5%) was Manus [S, ruvnet/metaharness].
- The public evaluation platform repo exists [P, https://github.com/centerforaisafety/rli_evaluation_platform].

**Gap in family 3.** These benchmarks are high-validity, low-renewability, high-cost and subjectively graded. Economic benchmarks cannot be regenerated weekly, and their items leak once published.

### 4. In-context learning of genuinely novel material

**MTOB: "A Benchmark for Learning to Translate a New Language from One Grammar Book"** (Tanzer, Suzgun, Visser, Jurafsky, Melas-Kyriazi; arXiv:2309.16575)
- The language is Kalamang, with fewer than 200 speakers.
- Materials: a field grammar, a 2,531-entry word list, and 400 train / 100 test parallel sentences.
- A human learning from the same materials scored 51.6 chrF (kgv→en) and 57.0 chrF (en→kgv), against a model baseline of 44.7 and 45.8 [P, https://github.com/lukemelas/mtob].
- **Adoption:** a frontier lab used it. The Gemini 1.5 report's source says that in the best setting Gemini 1.5 Pro reached human-rated translation quality of 4.14 vs the human learner's 5.52 (kgv→en), and 5.46 vs 5.58 (en→kgv) [P-ish, report LaTeX mirrored at https://github.com/Toudsour/ArxivLearning].
  - [corrected by fact-check] The report is internally inconsistent: its prose says 5.58 for the human en→kgv score, but its own tables (main body and appendix) give **5.60**.
  - The 4.14 kgv→en "best setting" is the **half-book** setting. The full-book score is 4.00, and the original-report version of the model scored 4.36 with the full book.
  - Scores are single-rater, 0-6, from a non-native rater who could recognise their own translations. The report itself warns that the ratings "are obviously biased".
- **Critical validity finding:** Aycock, Stap, Wu, Monz, Sima'an (arXiv:2409.19151; ICLR 2025 per accepted-paper lists, Spotlight per one list [added by fact-check]) found "almost all improvements stem from the book's parallel examples rather than its grammatical explanations". A fine-tuned encoder-decoder matched the LLM-with-grammar-book result [P abstract as indexed in https://github.com/Yikai-Liao/paper_machine].
- **Lesson for design:** a "learn from material" benchmark must control whether success comes from examples or from explanations.

**LINGOLY** (Bean, Hellsten, Mayne, Magomere, Chi, Chi, Hale, Kirk; arXiv:2406.06196)
- UK Linguistics Olympiad puzzles in low-resource and extinct languages, with a `--no_context` baseline to detect memorisation [P, https://github.com/am-bean/lingOly].
- Weakness: the olympiad puzzles are public and finite.

**CodeUpdateArena: "Benchmarking Knowledge Editing on API Updates"** (Liu, Pandit, Ye, Choi, Durrett; arXiv:2407.06249)
- The model must absorb fictional, executable updates to API functions, then solve program-synthesis tasks that use them [P, https://github.com/leo-liuzy/CodeUpdateArena]. This is the novel-API-learning precedent.

**EvaLearn: "Quantifying the Learning Capability and Efficiency of LLMs via Sequential Problem Solving"** (NeurIPS 2025)
- 648 problems, 6 task types, 182 sequences, 9 frontier models. Problems are solved sequentially so that models can use earlier experience. Five automated metrics.
- Findings: "models with stronger static abilities do not show a clear advantage in learning capability across all tasks". Some models show negative transfer [P abstract as indexed in https://github.com/HuggingAGI/HuggingArxivLLM; venue per https://github.com/zhaoyang97/Paper-Notes].
- arXiv:2506.02672; Dou, Zhang, Huang, et al. (ByteDance Seed / Fudan). NeurIPS 2025 proceedings, poster [corrected by fact-check: the ID and authors were previously "not captured". Both are confirmed in the official repo README and BibTeX at https://github.com/ByteDance-Seed/EvaLearn]. A third-party note says each sequence holds 7 problems. That would require reusing problems across sequences (182 × 7 > 648), so treat it as unverified [S, zhaoyang97/Paper-Notes].

**KOR-Bench** (see §1) is the rule-learning precedent.

**Gap in family 4.** Every existing instance uses a fixed, finite, human-curated corpus: one language, one set of olympiad puzzles, one set of API edits. None generates new languages or formal systems procedurally, and none separates learning from examples vs learning from explanations as a controlled factor.

### 5. Model-as-examiner, interviewer, council and peer evaluation

**Language-Model-as-an-Examiner** (Bai et al.; arXiv:2306.04181)
- A model acts as examiner: it formulates questions and evaluates answers reference-free. Dataset: LMExamQA [S, https://github.com/THU-KEG/EvaluationPapers4ChatGPT].

**KIEval** (Yu, Gao, Yao, Wang, Ye, Wang, Xie, Zhang, Zhang; arXiv:2402.15043; ACL 2024)
- An "LLM-powered interactor" runs multi-round dialogues grounded in benchmark questions, to tell recall apart from comprehension [P, https://github.com/zhuohaoyu/KIEval].

**TreeEval: "Benchmark-Free Evaluation of Large Language Models through Tree Planning"** (arXiv:2402.13125)
- An examiner LLM plans a tree of questions. It reportedly achieved the highest correlation with AlpacaEval 2.0 "using only around 45 questions" across 6 models [S, https://github.com/lyy1994/awesome-data-contamination].
- The venue is listed as NeurIPS 2024 in the survey list [S, unverified].

**LLM-as-an-Interviewer: "Beyond Static Testing Through Dynamic LLM Evaluation"** (Kim, Suk, Kim, ..., Oh; arXiv:2412.10424)
- Multi-turn interview that includes feedback and follow-up questions [S, https://github.com/SeekingDream/Static-to-Dynamic-LLMEval; https://github.com/metame-ai/awesome-llm-plaza].

**Auto-Arena: "Automating LLM Evaluations with Agent Peer-battles and Committee Discussions"** (Zhao, Zhang, Chia, Zhao, Bing; arXiv:2405.20267)
- An examiner LLM writes queries, two candidate models hold a multi-round peer battle, and a committee of LLM judges discusses and decides the winner.
- On 17 LLMs it "shows the highest correlation with human preferences" [P abstract as indexed in https://github.com/Luvata/arxive; repo https://github.com/DAMO-NLP-SG/Auto-Arena-LLMs].

**Language Model Council** (Zhao, Plaza-del-Arco, Genchel, Cercas Curry; arXiv:2406.08598; NAACL 2025; DOI 10.18653/v1/2025.naacl-long.617)
- 20 LLMs democratically write the test, respond to it and judge each other on emotional-intelligence / interpersonal tasks [P, https://github.com/llm-council/llm-council].

**Peer prediction: "Truthfulness Despite Weak Supervision: Evaluating and Training LLMs Using Peer Prediction"** (Qiu, Carroll, Allen; arXiv:2601.20299; ICLR 2026)
- Uses mechanism design: a mutual-predictability metric scores answers without ground truth.
- "LLM-as-a-Judge become worse than random guess when facing deceptive models 5-20x the judge's size, while peer prediction thrives when such gaps are large, including ... over 100x size difference" [P abstract as indexed in https://github.com/2shin0/arxiv-ai-mailing; venue per https://github.com/Thang1703hrsh/Awesome-Human-AI-Alignment].

**Debate:** "Debating with More Persuasive LLMs Leads to More Truthful Answers" (Khan et al.; arXiv:2402.06782; ICML 2024, listed as Best Paper) [S, https://github.com/huggingface/blog]. Weaker judges can assess stronger debaters, which establishes debate as a scalable-oversight evaluation protocol.

**Gap in family 5.**
- Examiner, interviewer and council methods all make LLMs both the item source and the grader. That is circular: models share training data and failure modes, which is the "echo chamber" problem again.
- Peer prediction and debate have theoretical guarantees but no public leaderboard.
- No method grades with an objective downstream outcome (for example, whether a student's post-test answer is exactly correct).

### 6. Teaching and tutoring as evaluation

**Saha, Hase, Bansal, "Can Language Models Teach Weaker Agents? Teacher Explanations Improve Students via Personalization"** (NeurIPS 2023; arXiv:2306.09299)
- A teacher LLM intervenes with explanations, and quality is measured by the change in a student model's accuracy [P, https://github.com/swarnaHub/ExplanationIntervention]. [corrected by fact-check] The repo README does not use the "Theory of Mind" title.
  - README heading: "Can Language Models Teach? Teacher Explanations Improve Student Performance via Personalization".
  - README BibTeX: "Can Language Models Teach Weaker Agents? Teacher Explanations Improve Students via Personalization" (NeurIPS 2023).
  - The "... via Theory of Mind" ending is the arXiv v1 title [S, https://github.com/taesiri/ArXivQA papers/2306.09299.md].
- This is the conceptual origin of "student learning gain as a metric".

**EducationQ** (ACL 2025; arXiv:2504.14928)
- Setup: a teacher agent (the model under test), a fixed student (Llama 3.1 70B Instruct) and an evaluator. Protocol: pre-test, then 5 dialogue rounds, then post-test. The teacher cannot see the answer options.
- Metric: absolute learning gain (ALG) = post-test minus pre-test accuracy.
- Scale: 14 LLMs, 1,498 questions drawn from GPQA and MMLU-Pro.
- Results:
  - "Teaching capability is not proportional to model size". Llama 3.1 70B had the highest ALG (+11.01%).
  - Human experts agreed 78% with the automated qualitative analysis.
- Source: [S, https://github.com/zhaoyang97/Paper-Notes-en].
- [added by fact-check] Authors, from the official README BibTeX (https://github.com/SunriserFuture/EducationQ): Yao Shi, Rongkeng Liang, Yong Xu. ACL 2025 Long, doi:10.18653/v1/2025.acl-long.1576.
- [added by fact-check] Validity caveat: the top-ranked teacher, Llama 3.1 70B Instruct (pre-test 47.73, post-test 58.74, ALG +11.01), is the **same model** as the fixed student. Its win may partly reflect teacher-student model affinity rather than general teaching skill.
  - The paper's ablation reports that teacher rankings hold with Qwen 72B and Mistral Nemo students.
  - But the Llama-70B teacher's gain on the GPQA Diamond subset drops from +12.63% (Llama 70B student) to +8.08% (Qwen 72B) and +4.55% (Mistral Nemo) [S, zhaoyang97/Paper-Notes-en].
- Weaknesses: the items come from public, contaminated benchmarks. The student is an LLM whose prior knowledge is uncontrolled.

**MathTutorBench** (Macina, Daheim, Hakimi, Kapur, Gurevych, Sachan; arXiv:2502.18940; EMNLP 2025 main conference, doi:10.18653/v1/2025.emnlp-main.11) [corrected by fact-check: the official README BibTeX confirms EMNLP 2025 main, but "Oral" status was not found in any source checked]
- Three skills (math expertise, student understanding, pedagogy) across seven tasks. Pedagogy is scored by a 1.5B "scaffolding" reward model as a win rate against the teacher utterance.
- Finding: "strong problem solvers are not automatically strong tutors" [P, https://github.com/eth-lre/mathtutorbench].
- A 2026 diagnostic (arXiv:2606.16206) found the correlation between solving and pedagogy composites on MathTutorBench's public leaderboard is 0.421 across eight models [P abstract as indexed in https://github.com/rxmna8502/vybe-intelligence-vault].
  - [added by fact-check] Title and authors: Yao, Zheng, Li, "Measuring Whether LLM Tutors Teach or Solve: A Diagnostic for Educational Impact". v2 was retitled "Beyond Helpfulness: A Teaching-over-Solving Diagnostic for Measuring Educational Impact in LLM Tutors". The abstract was re-read in three arXiv digests.
  - The current MathTutorBench README leaderboard lists 17 models, so 0.421 describes an earlier eight-model snapshot.

**TutorBench** (arXiv:2510.02663, "A Benchmark to Assess Tutoring Capabilities of Large Language Models") [S, https://github.com/memgrafter/research-digests]
- Name collision: a different "TutorBench" appears in DeepTutor (arXiv:2604.26962). It uses a profile-driven simulated student [S, https://github.com/rxmna8502/vybe-intelligence-vault].
- MMTutorBench (arXiv:2510.23477) covers multimodal tutoring [S].

**Gap in family 6.**
- Most tutoring benchmarks score tutor utterances with rubrics or reward models, not realised student learning.
- The one learning-gain benchmark (EducationQ) uses contaminated items and an uncontrolled student prior.
- No benchmark has a candidate teach a student material neither has seen, with the student's post-test graded exactly. That is the cleanest version of "teaching as evaluation".

### 7. Compression as intelligence

**"Compression Represents Intelligence Linearly"** (Huang, Zhang, Shan, He; arXiv:2404.09937; COLM 2024)
- Bits-per-character on Common Crawl, Python and arXiv-math corpora predicts average benchmark score almost linearly. The repo leaderboard lists 29 models [P, https://github.com/hkust-nlp/llm-compression-intelligence].
- A digest reports Pearson r of about -0.95 across 31 LLMs [S, https://github.com/memgrafter/research-digests], so the exact r and N are M.

**Uncheatable Eval: "Dynamic Compression-Based Evaluation of Language Models"** (Tan, Li, Shen; arXiv:2609.27510; posted 2026-09-23; code at https://github.com/Jellyfish042/uncheatable_eval) [full title added by fact-check, from the arXiv mirror qhduan/cn-chat-arxiv and the official repo]
- Measures compression rate on regularly collected, newly published text: 80 models, 14 text categories. Lower compression rate is "strongly associated with higher zero-shot MMLU accuracy" [P abstract as indexed in https://github.com/Luvata/arxive and https://github.com/Rook1eChan/daily-arxiv].
- Aimed at base models. A third-party note says the method is not for chat-tuned models [S, https://github.com/turbobeest/modelspec].

**Gap in family 7.** Compression needs log-probabilities, so it does not work for closed or chat models. Its content is also opaque to consumers: a BPC number is not "fun" or legible.

### 8. Consistency and metamorphic testing (evaluation without ground truth)

**"Evaluating Superhuman Models with Consistency Checks"** (Fluri, Paleka, Tramèr; arXiv:2306.09983)
- "While the correctness of superhuman decisions may be impossible to evaluate, we can still surface mistakes if the model's decisions fail to satisfy certain logical, human-interpretable rules."
- Domains: chess (Leela), forecasting (GPT-4 / GPT-3.5), legal bail decisions [P, https://github.com/ethz-spylab/superhuman-ai-consistency].

**"Consistency Checks for Language Model Forecasters"** (Paleka et al.; arXiv:2412.18544) [S, https://github.com/elicit/machine-learning-list; https://github.com/memgrafter/research-digests].

**Generator-Validator (GV) consistency** (Li, Shrivastava, Li, Hashimoto, Liang; arXiv:2310.01846; ICLR 2024)
- "Even GPT-4 ... is GV-consistent only 76% of the time". Consistency fine-tuning raised Alpaca-30B from 60% to 93% [P abstract as indexed in https://github.com/victorialslocum/frontpage; venue per https://github.com/will-rice/llm-self-improvement-papers].

**The Reversal Curse** (arXiv:2309.12288)
- A secondary note: GPT-4 answers about 80% of forward-direction questions but about 35% of the reversed questions [S, https://github.com/jaebradley/notes].

**Metamorphic Testing of Large Language Models for Natural Language Processing** (Cho et al.; arXiv:2511.02108) [S, https://github.com/isLinXu/paper-list]. DyCodeEval (§1) applies metamorphic relations to code.

**Gap in family 8.** Consistency methods are powerful for superhuman regimes but exist only as papers. There is no maintained multi-model consistency leaderboard, and violations have not been combined with accuracy on one scale.

### 9. Calibration and abstention

**AbstentionBench: "Reasoning LLMs Fail on Unanswerable Questions"** (Kirichenko, Ibrahim, Chaudhuri, Bell; arXiv:2506.09038)
- 20 datasets across 6 abstention scenarios, including underspecified, unanswerable, stale-data and false-premise questions.
- "Reasoning fine-tuning hurts abstention" [P, https://github.com/facebookresearch/AbstentionBench].
- [added by fact-check] The abstract quantifies this: reasoning fine-tuning "degrades abstention (by 24% on average)" across 20 frontier LLMs, and scaling "is of little use" [S, abstract copied in https://github.com/ProfSynapse/Epistemic-Humility-Research and the memgrafter/research-digests header].
- Note that AbstentionBench grades with an LLM judge, reported at 88% agreement with human labels [S, memgrafter]. It is not a judge-free benchmark.

KalshiBench, Prophet Arena and ForecastBench (§2) are the proper-scoring calibration benchmarks.

**Gap in family 9.** Calibration is measured almost only on forecasting or unanswerable-question sets. It is not a first-class dimension of capability benchmarks, where every answer could carry a confidence scored by a proper scoring rule.

### 10. Scientific discovery and research ability

**ScienceAgentBench** (Chen et al., OSU; arXiv:2410.05080; ICLR 2025)
- 102 tasks taken from 44 peer-reviewed publications in 4 disciplines, evaluated on generated programs, execution results and cost [P, https://github.com/OSU-NLP-Group/ScienceAgentBench].

**MLE-bench** (Chan et al.; arXiv:2410.07095)
- 75 Kaggle competitions graded against human leaderboard medals. A "lite" low-complexity split has 22 competitions.
- The live leaderboard top as of fetch was Famou-Agent 2.0 (Gemini-3-Pro-Preview) with 64.44 ± 1.18% any-medal, dated 2026-02-23. It is followed by AIBuildAI (Claude-Opus-4.6) at 63.11% [P, https://github.com/openai/mle-bench].
- **Adoption:** very high. This is an active 2026 agent leaderboard.

**PaperBench** (arXiv:2504.01848)
- Agents replicate 20 ICML 2024 Spotlight and Oral papers from scratch. Grading is by an LLM judge against author-co-developed rubrics.
- Best agent: 21.0% ± 0.8 (BasicAgent with Claude-3.5-Sonnet). Code-Dev variant cuts grading cost by about 85% [P, https://github.com/openai/preparedness].
  - [corrected by fact-check] 21.0% is the abstract's "best-performing tested agent" (Claude 3.5 Sonnet (New) with open-source scaffolding) in the headline BasicAgent comparison.
  - It is **not** the top of the official repo leaderboard. There, IterativeAgent o1-high scores 26.0 ± 0.3% with a 36 h limit and 24.4 ± 0.7% with a 24 h limit, both above BasicAgent claude-3.5-sonnet at 21.0 ± 0.8%. All runs are dated 2025-04-02.
  - The Code-Dev ~85% figure is specifically the reduction in o3-mini SimpleJudge grading cost per average submission.
  - Authors: Starace, Jaffe, Sherburn, Aung, Chan, Maksin, Dias, Mays, Kinsella, Thompson, Heidecke, Glaese, Patwardhan. ICML 2025 per the cspapers.org index [S].
- Secondary details [S, https://github.com/turbobeest/modelspec]:
  - 8,316 leaf rubric criteria.
  - Human baseline: ML PhDs reached 41.4% on a 3-paper subset (best of 3, 48 h), vs o1 at 26.6% on that subset.
  - Judge: o3-mini, with F1 0.83 against human labels on JudgeEval.

**BrainBench** (Luo et al., "Large language models surpass human experts in predicting neuroscience results", *Nature Human Behaviour* 2024, DOI 10.1038/s41562-024-02046-9)
- Two-alternative choice between an original and an altered abstract.
- LLMs averaged 81.4% vs human experts' 63.4% (171 of 202 experts passed the screening checks). Restricting to the top 20% of self-rated expertise raised the human score to 66.2% [P, https://github.com/braingpt-lovelab/BrainBench; numbers seen in paper text mirrored at https://github.com/tegorman13/lit_git and https://github.com/cognitivetech/llm-research-summaries].

**The AI Scientist** (Lu, Lu, Lange, Foerster, Clune, Ha; arXiv:2408.06292)
- "Typically less than $15 per paper". The repo warns that it executes LLM-written code [P, https://github.com/SakanaAI/AI-Scientist].

**The AI Scientist-v2** (Yamada et al.; arXiv:2504.08066)
- Claims "the first workshop paper written entirely by AI and accepted through peer review", at an ICLR 2025 workshop [P, https://github.com/SakanaAI/AI-Scientist-v2].
- Note that this is a system demonstration, not a benchmark.

**Research-idea studies** (Si, Yang, Hashimoto, ICLR 2025, arXiv:2409.04109; and "The Ideation-Execution Gap")
- LLM ideas were rated more novel than expert ideas.
- After execution (43 ideas), LLM ideas' scores "decrease significantly more" than expert ideas' [P, https://github.com/NoviScl/AI-Researcher].

**LAB-Bench** (FutureHouse; arXiv:2407.10362)
- More than 2,400 multiple-choice questions on practical biology research: literature, figures, databases, sequences, cloning [P abstract as indexed in https://github.com/HuggingAGI/HuggingArxiv].

**Gap in family 10.**
- Outcome-prediction benchmarks (BrainBench) are clever and cheap but can be learned from the literature.
- Replication and ML-engineering benchmarks (PaperBench, MLE-bench) are costly (GPUs, LLM judges) and drift toward agent scaffolding contests.
- None tests discovery of a hidden law in a synthetic world whose ground truth the benchmark designer knows exactly.

### 11. Long-horizon memory and state tracking

**LongMemEval** (Wu, Wang, Yu, Zhang, Chang, Yu; arXiv:2410.10813; ICLR 2025)
- 500 questions testing information extraction, multi-session reasoning, knowledge updates, temporal reasoning and abstention. The S variant has about 40 sessions (about 115k tokens); the M variant about 500 sessions [P, https://github.com/xiaowu0162/LongMemEval].

**BABILong** (Kuratov et al.; NeurIPS 2024; arXiv:2406.10149 [ID added by fact-check, from the official README])
- 20 bAbI-style tasks hidden in contexts up to 10M tokens. "Even models that claim to support 128K tokens, such as GPT-4 ... experience degradation beyond 10% of their input capacity" [P, https://github.com/booydar/babilong].

**Michelangelo: "Long Context Evaluations Beyond Haystacks via Latent Structure Queries"** (Vodrahalli et al., Google; arXiv:2409.12640)
- Synthetic, unleaked tasks that require inferring latent structure rather than retrieving a needle [S, https://github.com/Xnhyacinth/Awesome-LLM-Long-Context-Modeling].

**Gap in family 11.** Memory benchmarks test retrieval and tracking of given facts. They do not test cumulative learning, where knowledge from session k must be used to master session k+1 (EvaLearn comes closest).

### 12. The verification-generation gap

- **GV-consistency** (above): the first systematic generator-vs-validator metric (GPT-4 at 76%).
- **"The Generative AI Paradox: What It Can Create, It May Not Understand"** (West et al.; arXiv:2311.00059). Models can generate better than they understand, the reverse of humans [S, https://github.com/taesiri/ArXivQA; https://github.com/metame-ai/awesome-llm-plaza].
- **BrowseComp** (OpenAI, Wei et al.; arXiv:2504.12516): 1,266 "inverted" questions that are "hard to find but easy to verify" [S, https://github.com/kzinmr/ai-topics]. It deliberately exploits the asymmetry to get cheap, exact grading.
- **"The Future of Facts: Tracing the Factual Generation-Verification Gap"** (2026). The abstract says language models "often verify outputs more reliably than they generate them". The same feed shows ID arXiv:2605.27564 next to that abstract, so the title-to-ID link is M [S, https://github.com/sifted-network/sifted-awesome-ai-agents].
  - [corrected by fact-check] The title-to-ID link is now **H**. The official repo https://github.com/anjasurina/factgap carries an arXiv badge for 2605.27564 and BibTeX. Authors: Tim R. Davidson, Anja Surina, Caglar Gulcehre.
  - Key findings: verification is learned before generation, and it is more robust to continual learning. Factual updates can leave a "multi-verse" state where old and new answers are both verified as correct.
- **Counter-evidence:** an ICLR 2026 paper on implicit reward models (arXiv:2507.07981) "refutes the popular 'generation-verification gap' hypothesis" as an explanation for why implicit reward models generalise worse [S, https://github.com/zhaoyang97/Paper-Notes-en].
- **Gap in family 12.** No leaderboard reports each model's generation score, verification score and gap on the same items.

### Cross-family comparison (interpretation)

| Family | Renewable? | Objective grading? | Real-world link | Cost | Adoption signal seen | Main failure risk |
|---|---|---|---|---|---|---|
| Symbolic procedural (NPHardEval, NPPC, DyVal, Reasoning Gym) | Infinite | Exact | Low | Low | Moderate (stars; RL use) | Trained on and saturated; narrow |
| LLM-generated evolving (Self-Evolving, CHASE, DyVal2) | High | LLM or partial | Medium | Low-med | Low (26-star repo) | Generator bias ("echo chamber") |
| Live temporal (LiveBench, LiveCodeBench) | Monthly | Exact | Medium | Curation labour | High | Curation burden; conventional QA |
| Forecasting (ForecastBench, FutureX, Prophet, KalshiBench) | Daily | Exact after delay | High | Low-med | High (2025-26 follow-ups) | Leakage; resolution delay; search-tool confound |
| Economic (GDPval, RLI, SWE-Lancer) | No | Expert or LLM | Very high | Very high | Very high (60 GDPval repos) | Grader substitution; small public sets |
| Novel-material ICL (MTOB, LINGOLY, KOR, CodeUpdateArena) | No (fixed corpora) | Exact or metric | Medium | Low | Medium (MTOB in Gemini 1.5 report) | Finite; example-copying confound |
| Examiner / council / interviewer | High | LLM | Low-med | Low | Low-med | Circularity |
| Peer prediction / debate / consistency | High | No ground truth needed | Medium | Low | Research only | No leaderboard; hard to explain |
| Teaching / tutoring | Low | Reward model or student test | High | Medium | Medium (MathTutorBench leaderboard) | Contaminated items; uncontrolled student |
| Compression | Continuous | Exact | Low (legibility) | Low | Medium | Needs logprobs; opaque to consumers |
| Science (PaperBench, MLE-bench, BrainBench) | No | Rubric, medal or exact | High | High | High (MLE-bench 2026 leaderboard) | Cost; judge drift |
| Memory (LongMemEval, BABILong) | Semi | Exact or LLM | Medium | Low | Medium | Retrieval ≠ learning |

---

## Implications for designing a new benchmark

All of this section is interpretation, grounded in the findings above and in the user's failure diagnoses.

1. **Do not rely on LLM-generated items or LLM grading as the core.**
   - The user's diagnosis of item 10 (Bloom's taxonomy, 60k LLM-generated items as an echo chamber) is echoed by the circularity of examiner and council methods, and by the grader-substitution drift seen for GDPval.
   - Prefer symbolic generators with exact verifiers (the NPPC, DyVal and Reasoning Gym design principles) for the item source and the final score.
   - LLMs can take part only as subjects: teacher, student or verifier.
2. **Beat "memorised well-known task" failures by generating whole new domains, not new instances of known problems.**
   - NPHardEval and NPPC scale instances of textbook problems. Counterfactual tasks and KOR-Bench show that novel rules expose recitation, but their rule sets are static.
   - A generator of fresh synthetic systems (a mini-language with a grammar and lexicon, a fictional API, or a toy physics or chemistry with hidden laws), sampled per evaluation round, removes the "models may have memorised it" objection (the user's item 3) at the root.
3. **Control for the MTOB confound.** Aycock et al. show that "learning from a book" can collapse into copying parallel examples. A new design should vary explanation vs examples as independent factors, and include items unsolvable by nearest-example copying (novel compositions).
4. **Measure learning and teaching, not just knowing.** EvaLearn and EducationQ show that learning and teaching ability do not track static benchmark rank. This is a new, discriminative dimension, which answers the "nothing unique" objection (the user's items 1, 2, 8).
   - The cleanest version is a teach-back protocol: candidate model reads novel material, then teaches a fixed student, then the student takes an exactly graded post-test. The metric is the student's learning gain.
   - This yields a grounded, judge-free outcome and has direct product relevance (tutoring, documentation, onboarding), which answers the "no product needs it" objection (the user's item 4).
5. **Put everything on one scale.** The user's item 1 complaint (three non-comparable scores) argues for IRT or Bradley-Terry aggregation across sub-tasks, with per-item difficulty parameters from the generator.
6. **Build in calibration.** KalshiBench and AbstentionBench show that over-confidence is widespread and not fixed by reasoning. Having every answer carry a probability scored with a log or Brier rule costs almost nothing and adds a dimension most leaderboards lack.
7. **Exploit verification-generation asymmetry for cheap grading, and report the gap.** A cross-examination matrix (every model's outputs verified by every other model, scored against exact generator ground truth) would give a live verification-gap leaderboard. None exists yet. It could also borrow peer-prediction scoring for the subjective parts.
8. **Keep it light and legible.** Game Reasoning Arena failed partly on heavy installs (the user's item 2). Compression failed on consumer legibility. The new benchmark should run as API calls only, and its headline number should be interpretable, for example "the student learned X% of a new language from this model".
9. **Plan for the procedural-generator-becomes-training-set problem.** Reasoning Gym shows that public generators become RLVR curricula.
   - Mitigations: keep generator seeds and parameter ranges partly private, rotate domain families, and version releases as LiveBench does (delayed public release).
   - Scoring rules should reward transfer to held-out generator families.

### Under-explored niches (ranked by novelty × feasibility; interpretation)

1. **Teach-back with learning gain on procedurally generated novel material.** Nearest prior art: Saha et al. 2023, EducationQ, MTOB. What is missing: novel generated material, an exact post-test, and a controlled student prior.
2. **Procedurally generated "new language or formal system from a textbook" learning curves.** This generalises MTOB, KOR-Bench and EvaLearn and measures sample efficiency as material is added. The explanation-vs-example ablation is built in.
3. **A live verification-generation-gap leaderboard with a cross-model audit matrix.** Nearest prior art: GV-consistency (2023, 6 tasks), the factual GV-gap paper (2026), BrowseComp's asymmetry, peer prediction.
4. **Ground-truth-free consistency leaderboards for superhuman regimes.** Nearest prior art: Fluri et al. and Paleka et al. There is no maintained leaderboard.
5. **Proper-scoring calibration as a universal overlay** on capability items, not only on forecasting.
6. **Discovery in synthetic worlds with known hidden laws.** A contamination-proof analogue of BrainBench, ScienceAgentBench and AI Scientist evaluations, where the ground-truth law is known exactly.
7. **Cumulative cross-session learning** (use what you learned in session k to master session k+1). This combines LongMemEval-style memory with EvaLearn-style learning.
8. **Human-anchored validation of simulated students.** A small human study checking that learning gains of LLM students predict gains of human learners. No tutoring benchmark seen reports this link.

---

## Claims ledger

1. DyVal (arXiv:2309.17167) generates evaluation samples on the fly with controlled complexity, to mitigate contamination. DyVal 2 was presented at ICML 2024. Sources: https://github.com/microsoft/promptbench ; https://github.com/lyy1994/awesome-data-contamination. Confidence: H (DyVal), M (DyVal 2 venue).
2. NPHardEval (arXiv:2312.14890) evaluates reasoning across P, NP-complete and NP-hard problem classes with versioned data. GPT-4's early accuracy fell from about 0.72 (P) to about 0.057 (NP-hard). Source: https://github.com/casmlab/NPHardEval. Confidence: H (design), M (numbers).
3. NPPC is an "ever-scaling" benchmark of 25 NP-complete problems with generator and verifier modules. Source: https://github.com/SMU-DIGA/nppc. Confidence: H.
4. KOR-Bench (arXiv:2410.06526) tests knowledge-orthogonal rules in 5 categories. Top models were at about 58%. Source: https://github.com/KOR-Bench/KOR-Bench. Confidence: H (design), M (score).
5. CHASE (arXiv:2502.14678) builds synthetic evaluation problems bottom-up from verifiable sub-tasks. State-of-the-art LLMs score 40-60%. Source: https://github.com/McGill-NLP/CHASE. Confidence: H.
6. Skill-Mix (arXiv:2310.17567, ICLR 2024) samples k-skill combinations. Only about 10% of the skill and topic lists are public. Sources: https://github.com/memgrafter/research-digests ; https://github.com/MLNLP-World/Top-AI-Conferences-Paper-with-Code. Confidence: M.
7. Benchmark Self-Evolving (arXiv:2402.11443) was published at COLING 2025 and uses 8 LLM-driven evolution modes. Sources: https://github.com/nanshine/Self-Evolving-Benchmark ; https://github.com/MLNLP-World/Top-AI-Conferences-Paper-with-Code. Confidence: H.
8. LiveBench (arXiv:2406.19314, ICLR 2025 Spotlight) has 18 tasks in 6 categories, is scored with objective ground truth without LLM judges, releases monthly and delays public release. Source: https://github.com/LiveBench/LiveBench. Confidence: H.
9. LiveCodeBench (arXiv:2403.07974 [corrected by fact-check]) release_v6 contains 1,055 problems dated May 2023-Apr 2025, collected from LeetCode, AtCoder and Codeforces. Source: https://github.com/LiveCodeBench/LiveCodeBench. Confidence: H.
10. ForecastBench (arXiv:2409.19839, ICLR 2025) is a dynamic, contamination-free forecasting benchmark with human comparison groups and nightly updates. Source: https://github.com/forecastingresearch/forecastbench. Confidence: H.
11. FutureX (arXiv:2508.11987) collects events daily from 195 sources and evaluated 25 models. Grok-4 ranked first, and 40 human experts still led on several levels. Sources: https://github.com/zhaoyang97/Paper-Notes-en ; https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series. Confidence: M.
12. Prophet Arena (arXiv:2510.17638) reports small LLM calibration errors and promising market returns. LLMs aggregate information more slowly than markets near resolution. Sources: https://github.com/Hypogenic-AI/news-from-future-ai-aed4-claude ; https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series. Confidence: M-H.
13. KalshiBench (arXiv:2512.16030): 300 Kalshi questions and 5 frontier models, all overconfident. Best ECE was 0.120 (Claude Opus 4.5). GPT-5.2-XHigh had ECE 0.395. Only one model had a positive Brier Skill Score. Source: https://github.com/Hypogenic-AI/news-from-future-ai-aed4-claude. Confidence: M-H.
14. Uncheatable Eval (arXiv:2609.27510, Sep 2026) measures compression on newly published text across 80 models and 14 categories, and finds lower compression rate associates with higher MMLU. Sources: https://github.com/Luvata/arxive ; https://github.com/Rook1eChan/daily-arxiv. Confidence: M-H.
15. "Compression Represents Intelligence Linearly" (arXiv:2404.09937, COLM 2024) finds a near-linear BPC-to-benchmark relationship. A digest reports r ≈ -0.95. Sources: https://github.com/hkust-nlp/llm-compression-intelligence ; https://github.com/memgrafter/research-digests. Confidence: H (finding), M (r value).
16. GDPval (arXiv:2510.04374): 1,320 tasks, 44 occupations, 9 sectors, professionals averaging 14 years' experience, blind expert pairwise grading. Claude Opus 4.1 won or tied 47.6%. [corrected by fact-check] The other models' paper Fig. 5 values are GPT-5 high 38.8%, o3 high 34.1%, o4-mini high 27.9%, GPT-4o 12.4%; the EnvCommons numbers were wrong. Sources: https://github.com/memgrafter/research-digests ; https://github.com/visual-snow/seshat (parsed paper) ; https://github.com/howard86/howardism. Confidence: H (47.6% and task counts), M-H (other rates).
17. RLI (arXiv:2510.26787): the top agent's automation rate at launch was 2.5% (Manus). [corrected by fact-check] The July 2026 leaderboard top is 16.10% (Fable 5), per four independent secondary sources; the 15.8% figure is an outlier. Sources: https://github.com/Doragd/Algorithm-Practice-in-Industry ; https://github.com/ruvnet/metaharness ; https://github.com/guzus/ai-research-arm ; https://github.com/knomit/cyberai-kb. Confidence: H (2.5%), M (16.1%).
18. MTOB (arXiv:2309.16575): Kalamang has fewer than 200 speakers. The human learner scored 51.6 and 57.0 chrF, against model baselines of 44.7 and 45.8. Source: https://github.com/lukemelas/mtob. Confidence: H.
19. Aycock et al. (arXiv:2409.19151) found that almost all MTOB-style gains come from parallel examples, not grammatical explanations. Source: https://github.com/Yikai-Liao/paper_machine. Confidence: H.
20. The Gemini 1.5 report's MTOB evaluation found near-human en→kgv quality (5.46 vs 5.58 human learner) but a gap for kgv→en (4.14 vs 5.52). [corrected by fact-check] The report's tables give the human en→kgv score as 5.60 (its prose says 5.58), and 4.14 is the half-book setting. Source: https://github.com/Toudsour/ArxivLearning. Confidence: M.
21. EvaLearn (arXiv:2506.02672 [corrected by fact-check]; NeurIPS 2025): 648 problems in 182 sequences. Stronger static ability does not imply stronger learning ability. Sources: https://github.com/HuggingAGI/HuggingArxivLLM ; https://github.com/zhaoyang97/Paper-Notes. Confidence: M-H.
22. EducationQ (arXiv:2504.14928, ACL 2025) measures teaching by the student's absolute learning gain. Llama 3.1 70B had the highest gain (+11.01%), above larger models. [added by fact-check] The fixed student is also Llama 3.1 70B Instruct, a same-model confound. Sources: https://github.com/zhaoyang97/Paper-Notes-en ; https://github.com/SunriserFuture/EducationQ. Confidence: M-H.
23. MathTutorBench (arXiv:2502.18940, EMNLP 2025 main; "Oral" unverified) finds that "strong problem solvers are not automatically strong tutors". The solving-pedagogy correlation across 8 leaderboard models is 0.421. Sources: https://github.com/eth-lre/mathtutorbench ; https://github.com/rxmna8502/vybe-intelligence-vault. Confidence: H (finding), M (0.421).
24. Saha, Hase, Bansal (NeurIPS 2023, arXiv:2306.09299) measure a teacher LLM by the student's accuracy gain after explanations. Source: https://github.com/swarnaHub/ExplanationIntervention. Confidence: H.
25. Peer prediction (arXiv:2601.20299, ICLR 2026): LLM-as-a-Judge becomes worse than random against deceptive models 5-20x the judge's size, while peer prediction works at gaps above 100x. Sources: https://github.com/2shin0/arxiv-ai-mailing ; https://github.com/Thang1703hrsh/Awesome-Human-AI-Alignment. Confidence: M-H.
26. Auto-Arena (arXiv:2405.20267) uses an examiner, peer battles and a judge committee, and correlated best with human preferences across 17 LLMs. Source: https://github.com/Luvata/arxive. Confidence: M-H.
27. The Language Model Council (arXiv:2406.08598, NAACL 2025) had 20 LLMs democratically benchmark each other on emotional-intelligence tasks. Source: https://github.com/llm-council/llm-council. Confidence: H.
28. GV-consistency (arXiv:2310.01846, ICLR 2024): GPT-4 is generator-validator consistent only 76% of the time. Sources: https://github.com/victorialslocum/frontpage ; https://github.com/will-rice/llm-self-improvement-papers. Confidence: H.
29. Fluri, Paleka, Tramèr (arXiv:2306.09983) evaluate superhuman models via logical consistency violations in chess, forecasting and legal decisions. Source: https://github.com/ethz-spylab/superhuman-ai-consistency. Confidence: H.
30. AbstentionBench (arXiv:2506.09038): 20 datasets and 6 scenarios. Reasoning fine-tuning hurts abstention. Source: https://github.com/facebookresearch/AbstentionBench. Confidence: H.
31. MLE-bench (arXiv:2410.07095) has 75 Kaggle competitions. The leaderboard top in 2026 was 64.44% any-medal (Famou-Agent 2.0 with Gemini-3-Pro-Preview, 2026-02-23). Source: https://github.com/openai/mle-bench. Confidence: H.
32. PaperBench (arXiv:2504.01848) replicates 20 ICML 2024 papers. The best agent scored 21.0%. [corrected by fact-check] That is the abstract's headline result (Claude 3.5 Sonnet New, BasicAgent). The repo leaderboard's top is IterativeAgent o1-high at 26.0% (36 h). ML PhDs scored 41.4% on a 3-paper subset. Sources: https://github.com/openai/preparedness ; https://github.com/turbobeest/modelspec. Confidence: H (21.0%), M (human baseline).
33. BrainBench (*Nature Human Behaviour* 2024): LLMs averaged 81.4% vs human experts' 63.4%. Sources: https://github.com/braingpt-lovelab/BrainBench ; https://github.com/tegorman13/lit_git ; https://github.com/cognitivetech/llm-research-summaries. Confidence: H.
34. ScienceAgentBench (arXiv:2410.05080, ICLR 2025) has 102 tasks from 44 publications in 4 disciplines. Source: https://github.com/OSU-NLP-Group/ScienceAgentBench. Confidence: H.
35. The AI Scientist-v2 (arXiv:2504.08066) claims the first fully AI-written paper accepted through peer review at an ICLR 2025 workshop. Source: https://github.com/SakanaAI/AI-Scientist-v2. Confidence: H (that the claim is made).
36. LLM research ideas were rated more novel than experts' (arXiv:2409.04109, ICLR 2025), but they lost more score after execution (the ideation-execution gap). Source: https://github.com/NoviScl/AI-Researcher. Confidence: H.
37. LongMemEval (arXiv:2410.10813, ICLR 2025): 500 questions over 5 memory abilities. Source: https://github.com/xiaowu0162/LongMemEval. Confidence: H.
38. BABILong (NeurIPS 2024): GPT-4 degrades beyond about 10% of its 128K context. Source: https://github.com/booydar/babilong. Confidence: H.
39. BrowseComp (arXiv:2504.12516) has 1,266 questions designed to be hard to find but easy to verify. Sources: https://github.com/kzinmr/ai-topics ; https://github.com/knarayanareddy/AI-Arsenal. Confidence: M-H.
40. Reasoning Gym (arXiv:2505.24760, NeurIPS 2025 Spotlight) provides more than 100 procedural generators with verifiers, aimed at RL training. Source: https://github.com/open-thought/reasoning-gym. Confidence: H.
41. The Chen et al. EMNLP 2025 survey (arXiv:2502.17521) splits dynamic evaluation into temporal-cutoff, rule-based, LLM-based and hybrid generation. Source: https://github.com/SeekingDream/Static-to-Dynamic-LLMEval. Confidence: H.

---

## References

Each entry gives the paper, then [URL where it was seen]. Full author lists are given where they were captured.

1. Zhu, K., Chen, J., Wang, J., Gong, N. Z., Yang, D., Xie, X. DyVal: Graph-informed Dynamic Evaluation of Large Language Models (arXiv title: "DyVal: Dynamic Evaluation of Large Language Models for Reasoning Tasks"). arXiv:2309.17167, 2023. ICLR 2024 per the survey list. [https://github.com/microsoft/promptbench]
2. Zhu, K., Wang, J., Zhao, Q., Xu, R., Xie, X. DyVal 2: Dynamic Evaluation of Large Language Models by Meta Probing Agents. arXiv:2402.14865, 2024. ICML 2024. [https://github.com/lyy1994/awesome-data-contamination]
3. Fan, L., Hua, W., Li, L., Ling, H., Zhang, Y. NPHardEval: Dynamic Benchmark on Reasoning Ability of Large Language Models via Complexity Classes. arXiv:2312.14890, 2023. [https://github.com/casmlab/NPHardEval]
4. NPPC: Nondeterministic Polynomial Problem Challenge: An Ever-Scaling Reasoning Benchmark for LLMs. GitHub repo; paper ID not captured. [https://github.com/SMU-DIGA/nppc]
5. Ma, K., Du, X., Wang, Y., et al. KOR-Bench: Benchmarking Language Models on Knowledge-Orthogonal Reasoning Tasks. arXiv:2410.06526, 2024. [https://github.com/KOR-Bench/KOR-Bench]
6. Patel, A., Reddy, S., Bahdanau, D. How to Get Your LLM to Generate Challenging Problems for Evaluation (CHASE). arXiv:2502.14678, 2025. [https://github.com/McGill-NLP/CHASE]
7. Yu, D., Kaur, S., Gupta, A., Brown-Cohen, J., Goyal, A., Arora, S. Skill-Mix: a Flexible and Expandable Family of Evaluations for AI Models. arXiv:2310.17567; ICLR 2024. [https://github.com/memgrafter/research-digests]
8. Kaur, S., Park, S., Goyal, A., Arora, S. Instruct-SkillMix. arXiv:2408.14774; ICLR 2025. [https://github.com/princeton-pli/Instruct-SkillMix]
9. Wu, Z., et al. Reasoning or Reciting? Exploring the Capabilities and Limitations of Language Models Through Counterfactual Tasks. arXiv:2307.02477, 2023. [title corrected by fact-check] [https://github.com/ZhaofengWu/counterfactual-evaluation]
10. Mirzadeh, I., Alizadeh, K., Shahrokhi, H., Tuzel, O., Bengio, S., Farajtabar, M. GSM-Symbolic. arXiv:2410.05229, 2024. [https://github.com/apple/ml-gsm-symbolic]
11. Srivastava, S., et al. Functional Benchmarks for Robust Evaluation of Reasoning Performance, and the Reasoning Gap. arXiv:2402.19450, 2024. [https://github.com/ConsequentAI/fneval]
12. Benchmark Self-Evolving: A Multi-Agent Framework for Dynamic LLM Evaluation. arXiv:2402.11443; COLING 2025. [https://github.com/AGI-Edgerunners/LLM-Agents-Papers ; https://github.com/nanshine/Self-Evolving-Benchmark]
13. Stojanovski, Z., Stanley, O., Sharratt, J., Jones, R., Adefioye, A., Kaddour, J., Köpf, A. Reasoning Gym. arXiv:2505.24760; NeurIPS 2025 Spotlight. [https://github.com/open-thought/reasoning-gym]
14. Chen, S., Chen, Y., Li, Z., Jiang, Y., Wan, Z., He, Y., Ran, D., Gu, T., Li, H., Xie, T., Ray, B. Recent Advances in Large Language Model Benchmarks against Data Contamination: From Static to Dynamic Evaluation. arXiv:2502.17521; EMNLP 2025. [https://github.com/SeekingDream/Static-to-Dynamic-LLMEval]
15. White, C., Dooley, S., Roberts, M., Pal, A., Feuer, B., et al. LiveBench: A Challenging, Contamination-Free LLM Benchmark. arXiv:2406.19314; ICLR 2025. [https://github.com/LiveBench/LiveBench]
16. Jain, N., Han, K., Gu, A., Li, W.-D., Yan, F., Zhang, T., Wang, S., Solar-Lezama, A., Sen, K., Stoica, I. LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code. arXiv:2403.07974, 2024. [ID added by fact-check] [https://github.com/LiveCodeBench/LiveCodeBench]
17. Karger, E., Bastani, H., Chen, Y.-H., Jacobs, Z., Halawi, D., Zhang, F., Tetlock, P. E. ForecastBench. arXiv:2409.19839; ICLR 2025. [https://github.com/forecastingresearch/forecastbench]
18. FutureX: An Advanced Live Benchmark for LLM Agents in Future Prediction. arXiv:2508.11987; ICLR 2026 (per third-party notes). [https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series ; https://github.com/zhaoyang97/Paper-Notes-en]
19. Yang, Q., Mahns, S., Li, S., Gu, A., Wu, J., Xu, H. LLM-as-a-Prophet: Understanding Predictive Intelligence with Prophet Arena. arXiv:2510.17638, 2025. [https://github.com/Hypogenic-AI/news-from-future-ai-aed4-claude]
20. Nel, L. Do Large Language Models Know What They Don't Know? KalshiBench. arXiv:2512.16030, 2025. [https://github.com/Hypogenic-AI/news-from-future-ai-aed4-claude]
21. Paleka, D., Goel, S., Geiping, J., Tramèr, F. Pitfalls in Evaluating Language Model Forecasters. arXiv:2506.00723, 2025. [ID added by fact-check] [https://github.com/Hypogenic-AI/news-from-future-ai-aed4-claude]
22. Tan, K., Li, Y., Shen, L. Uncheatable Eval: Dynamic Compression-Based Evaluation of Language Models. arXiv:2609.27510, 2026. [full title added by fact-check] [https://github.com/Luvata/arxive]
23. Huang, Y., Zhang, J., Shan, Z., He, J. Compression Represents Intelligence Linearly. arXiv:2404.09937; COLM 2024. [https://github.com/hkust-nlp/llm-compression-intelligence]
24. Patwardhan, T., Dias, R., Proehl, E., Kim, G., Wang, M., Watkins, O., et al. (OpenAI). GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks. arXiv:2510.04374, 2025. [https://github.com/memgrafter/research-digests ; https://github.com/visual-snow/seshat] [authors added by fact-check; do not cite the EnvCommons README for win rates]
25. Miserendino, S., Wang, M., Patwardhan, T., Heidecke, J. (OpenAI). SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering? arXiv:2502.12115, 2025. [https://github.com/openai/preparedness]
26. Mazeika, M., Gatti, A., Menghini, C., et al. (incl. Hendrycks, D.). Remote Labor Index: Measuring AI Automation of Remote Work. arXiv:2510.26787, 2025. [https://github.com/Doragd/Algorithm-Practice-in-Industry ; https://github.com/ruvnet/metaharness]
27. Tanzer, G., Suzgun, M., Visser, E., Jurafsky, D., Melas-Kyriazi, L. A Benchmark for Learning to Translate a New Language from One Grammar Book (MTOB). arXiv:2309.16575, 2023; ICLR 2024. [venue added by fact-check] [https://github.com/lukemelas/mtob]
28. Aycock, S., Stap, D., Wu, D., Monz, C., Sima'an, K. Can LLMs Really Learn to Translate a Low-Resource Language from One Grammar Book? arXiv:2409.19151, 2024; ICLR 2025. [venue added by fact-check] [https://github.com/Yikai-Liao/paper_machine]
29. Gemini Team, Google. Gemini 1.5 technical report, in-context language learning section (report LaTeX mirror). 2024. [https://github.com/Toudsour/ArxivLearning]
30. Bean, A. M., Hellsten, S., Mayne, H., Magomere, J., Chi, E. A., Chi, R., Hale, S. A., Kirk, H. R. LINGOLY. arXiv:2406.06196, 2024. [https://github.com/am-bean/lingOly]
31. Liu, Z. L., Pandit, S., Ye, X., Choi, E., Durrett, G. CodeUpdateArena. arXiv:2407.06249, 2024. [https://github.com/leo-liuzy/CodeUpdateArena]
32. Dou, S., Zhang, M., Huang, C., et al. EvaLearn: Quantifying the Learning Capability and Efficiency of LLMs via Sequential Problem Solving. arXiv:2506.02672; NeurIPS 2025. [ID and authors added by fact-check; https://github.com/ByteDance-Seed/EvaLearn] [https://github.com/HuggingAGI/HuggingArxivLLM ; https://github.com/zhaoyang97/Paper-Notes]
33. Bai, Y., et al. Benchmarking Foundation Models with Language-Model-as-an-Examiner. arXiv:2306.04181, 2023. [https://github.com/THU-KEG/EvaluationPapers4ChatGPT]
34. Yu, Z., Gao, C., Yao, W., Wang, Y., Ye, W., Wang, J., Xie, X., Zhang, Y., Zhang, S. KIEval. arXiv:2402.15043; ACL 2024. [https://github.com/zhuohaoyu/KIEval]
35. TreeEval: Benchmark-Free Evaluation of Large Language Models through Tree Planning. arXiv:2402.13125. [https://github.com/SeekingDream/Static-to-Dynamic-LLMEval]
36. Kim, E., Suk, J., Kim, S., Muennighoff, N., Kim, D., Oh, A. LLM-as-an-Interviewer: Beyond Static Testing Through Dynamic LLM Evaluation. arXiv:2412.10424, 2024. [https://github.com/metame-ai/awesome-llm-plaza]
37. Zhao, R., Zhang, W., Chia, Y. K., Zhao, D., Bing, L. Auto-Arena of LLMs. arXiv:2405.20267, 2024. [https://github.com/Luvata/arxive]
38. Zhao, J., Plaza-del-Arco, F. M., Genchel, B., Cercas Curry, A. Language Model Council. arXiv:2406.08598; NAACL 2025; doi:10.18653/v1/2025.naacl-long.617. [https://github.com/llm-council/llm-council]
39. Qiu, T. A., Carroll, M., Allen, C. Truthfulness Despite Weak Supervision: Evaluating and Training LLMs Using Peer Prediction. arXiv:2601.20299; ICLR 2026. [https://github.com/2shin0/arxiv-ai-mailing]
40. Khan, A., Hughes, J., Valentine, D., et al. Debating with More Persuasive LLMs Leads to More Truthful Answers. arXiv:2402.06782; ICML 2024. [https://github.com/huggingface/blog]
41. Saha, S., Hase, P., Bansal, M. Can Language Models Teach Weaker Agents? Teacher Explanations Improve Students via Personalization. arXiv:2306.09299; NeurIPS 2023. [https://github.com/swarnaHub/ExplanationIntervention]
42. Shi, Y., Liang, R., Xu, Y. EducationQ: Evaluating LLMs' Teaching Capabilities Through Multi-Agent Dialogue Framework. arXiv:2504.14928; ACL 2025; doi:10.18653/v1/2025.acl-long.1576. [https://github.com/zhaoyang97/Paper-Notes-en ; https://github.com/SunriserFuture/EducationQ] [authors added by fact-check]
43. Macina, J., Daheim, N., Hakimi, I., Kapur, M., Gurevych, I., Sachan, M. MathTutorBench: A Benchmark for Measuring Open-ended Pedagogical Capabilities of LLM Tutors. arXiv:2502.18940; EMNLP 2025; doi:10.18653/v1/2025.emnlp-main.11. [https://github.com/eth-lre/mathtutorbench]
44. TutorBench: A Benchmark to Assess Tutoring Capabilities of Large Language Models. arXiv:2510.02663, 2025. [https://github.com/memgrafter/research-digests]
45. Yao, J., Zheng, Z., Li, B. Measuring Whether LLM Tutors Teach or Solve: A Diagnostic for Educational Impact (v2: Beyond Helpfulness: A Teaching-over-Solving Diagnostic for Measuring Educational Impact in LLM Tutors). arXiv:2606.16206, 2026. [title and authors added by fact-check] [https://github.com/rxmna8502/vybe-intelligence-vault]
46. Fluri, L., Paleka, D., Tramèr, F. Evaluating Superhuman Models with Consistency Checks. arXiv:2306.09983, 2023. [https://github.com/ethz-spylab/superhuman-ai-consistency]
47. Paleka, D., Sudhir, A. P., Alvarez, A., Bhat, V., Shen, A., Wang, E., Tramèr, F. Consistency Checks for Language Model Forecasters. arXiv:2412.18544, 2024. [https://github.com/elicit/machine-learning-list]
48. Li, X. L., Shrivastava, V., Li, S., Hashimoto, T., Liang, P. Benchmarking and Improving Generator-Validator Consistency of Language Models. arXiv:2310.01846; ICLR 2024. [https://github.com/victorialslocum/frontpage ; https://github.com/will-rice/llm-self-improvement-papers]
49. West, P., Lu, X., Dziri, N., Brahman, F., Li, L., Hwang, J. D., Jiang, L., Fisher, J., Ravichander, A., Chandu, K., et al. The Generative AI Paradox: "What It Can Create, It May Not Understand". arXiv:2311.00059, 2023. [https://github.com/metame-ai/awesome-llm-plaza]
50. Berglund, L., Tong, M., Kaufmann, M., Balesni, M., Stickland, A. C., Korbak, T., Evans, O. The Reversal Curse: LLMs trained on "A is B" fail to learn "B is A". arXiv:2309.12288, 2023. [https://github.com/jaebradley/notes]
51. Cho, S., et al. Metamorphic Testing of Large Language Models for Natural Language Processing. arXiv:2511.02108, 2025. [https://github.com/isLinXu/paper-list]
52. Davidson, T. R., Surina, A., Gulcehre, C. The Future of Facts: Tracing the Factual Generation-Verification Gap. arXiv:2605.27564, 2026. [title-to-ID link upgraded to H by fact-check; https://github.com/anjasurina/factgap] [https://github.com/sifted-network/sifted-awesome-ai-agents]
53. Kirichenko, P., Ibrahim, M., Chaudhuri, K., Bell, S. J. AbstentionBench. arXiv:2506.09038, 2025. [https://github.com/facebookresearch/AbstentionBench]
54. Chen, Z., et al. ScienceAgentBench. arXiv:2410.05080; ICLR 2025. [https://github.com/OSU-NLP-Group/ScienceAgentBench]
55. Chan, J. S., Chowdhury, N., Jaffe, O., Aung, J., Sherburn, D., Mays, E., Starace, G., Liu, K., Maksin, L., Patwardhan, T., Weng, L., Mądry, A. MLE-bench. arXiv:2410.07095, 2024. [https://github.com/openai/mle-bench]
56. Starace, G., Jaffe, O., Sherburn, D., Aung, J., Chan, J. S., Maksin, L., Dias, R., Mays, E., Kinsella, B., Thompson, W., Heidecke, J., Glaese, A., Patwardhan, T. PaperBench: Evaluating AI's Ability to Replicate AI Research. arXiv:2504.01848, 2025. [authors added by fact-check] [https://github.com/openai/preparedness]
57. Luo, X., Rechardt, A., Sun, G., et al. Large language models surpass human experts in predicting neuroscience results. *Nature Human Behaviour*, 2024. doi:10.1038/s41562-024-02046-9. [https://github.com/braingpt-lovelab/BrainBench]
58. Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., Ha, D. The AI Scientist. arXiv:2408.06292, 2024. [https://github.com/SakanaAI/AI-Scientist]
59. Yamada, Y., Lange, R. T., Lu, C., Hu, S., Lu, C., Foerster, J., Clune, J., Ha, D. The AI Scientist-v2. arXiv:2504.08066, 2025. [https://github.com/SakanaAI/AI-Scientist-v2]
60. Si, C., Yang, D., Hashimoto, T. Can LLMs Generate Novel Research Ideas? arXiv:2409.04109; ICLR 2025. Also Si, Hashimoto, Yang, The Ideation-Execution Gap, 2025. [https://github.com/NoviScl/AI-Researcher]
61. FutureHouse. LAB-Bench: Measuring Capabilities of Language Models for Biology Research. arXiv:2407.10362, 2024. [https://github.com/HuggingAGI/HuggingArxiv]
62. Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., Yu, D. LongMemEval. arXiv:2410.10813; ICLR 2025. [https://github.com/xiaowu0162/LongMemEval]
63. Kuratov, Y., et al. BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack. arXiv:2406.10149; NeurIPS 2024. [ID added by fact-check] [https://github.com/booydar/babilong]
64. Vodrahalli, K., et al. Michelangelo: Long Context Evaluations Beyond Haystacks via Latent Structure Queries. arXiv:2409.12640, 2024. [https://github.com/Xnhyacinth/Awesome-LLM-Long-Context-Modeling]
65. Wei, J., et al. (OpenAI). BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents. arXiv:2504.12516, 2025. [https://github.com/kzinmr/ai-topics]

---

## Verification log

Adversarial fact-check pass, 2026-09-29.

**Method and limits.**

- WebSearch was unavailable: the session's search budget was already spent, and all attempts returned "budget used".
- arXiv, export.arxiv.org, HuggingFace, OpenReview and the ACL Anthology were blocked (arXiv API CONNECT rejected by the proxy).
- The GitHub REST API was restricted to this project's repo.
- Verification therefore used four channels:
  1. Official benchmark READMEs, fetched raw from raw.githubusercontent.com.
  2. Cross-repository GitHub code search. This surfaced arXiv-listing mirrors and digests (qhduan/cn-chat-arxiv, CSQianDong/Awesome-arXiv-Daily-Reporter, 2shin0/arxiv-ai-mailing, MystenLabs/snowreads arXiv metadata, memgrafter/research-digests), accepted-paper lists, and parsed paper text.
  3. GitHub repository metadata.
  4. One WebFetch of a github.com page (NPPC).
- For every claim, at least one source other than the dossier's cited URL was consulted.
- A limitation remains: many confirmations rest on third-party copies of arXiv abstracts, not the arXiv page itself.

### Claim verdicts

| ID | Verdict | Evidence (what was checked) | Sources |
|---|---|---|---|
| C1 LiveBench | **Confirmed** (clarified) | README: "18 diverse tasks across 6 categories"; "verifiable, objective ground-truth answers ... without the use of an LLM judge"; "releasing new questions monthly"; "current LiveBench release is 2025-04-25; however, not all questions for this release are public"; ICLR 2025 Spotlight; arXiv 2406.19314. Clarifications: the most recent fully public release is 2024-11-25; "monthly" is the stated design, with no release after 2025-04-25 named in the README; "18 tasks" is described as "currently". | https://raw.githubusercontent.com/LiveBench/LiveBench/main/README.md |
| C2 LiveCodeBench | **Confirmed** (+ID) | README: "release_v6 ... problems released between May 2023 and Apr 2025 containing 1055 problems"; v1 = 400 problems (May 2023-Mar 2024); LeetCode/AtCoder/CodeForces and 4 scenarios. arXiv ID added: 2403.07974. | https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/main/README.md ; https://github.com/qhduan/cn-chat-arxiv (papers/24/03/2403.07974.json) ; https://github.com/NiuTrans/LaTeXTrans (DeepSeek-R1 .bbl) |
| C3 MTOB | **Confirmed** | README abstract: "less than 200 speakers", "44.7 chrF on Kalamang to English ... and 45.8 chrF on English to Kalamang ... compared to 51.6 and 57.0 chrF by a human"; wordlist "2,531 Kalamang words"; 400/100 split. The abstract does not name the baseline model. A WebFetch summariser's "GPT-3.5-turbo" was an artefact of a CLI default, so do not attribute these scores to a model without the paper. ICLR 2024 (Spotlight per one list). | https://raw.githubusercontent.com/lukemelas/mtob/main/README.md ; https://github.com/MLNLP-World/Top-AI-Conferences-Paper-with-Code (ICLR2024 list) ; https://github.com/AmberLJC/Sci-Reasoning |
| C4 Aycock et al. | **Confirmed** (+venue) | Abstract: "almost all improvements stem from the book's parallel examples rather than its grammatical explanations"; an encoder-decoder fine-tune is comparable. Venue: ICLR 2025, Spotlight per one list. | https://github.com/Luvata/arxive (pages/2025-04-25-cs-cl.html) ; https://github.com/sailfish009/paper (2024.10.01.txt) ; https://github.com/freezed-corpse-143/topaperlist (ICLR 2025 list) ; https://github.com/AmberLJC/Sci-Reasoning |
| C5 GV-consistency | **Confirmed** | Abstract: "even GPT-4 ... is GV-consistent only 76% of the time"; Alpaca-30B 60%→93%. ICLR 2024 via a cspapers.org index path. | https://github.com/qhduan/cn-chat-arxiv (2310.01846) ; https://github.com/stanford-cs336/spring2025-lectures (cached arXiv API response) ; https://github.com/swkim101/cspapers.org (index2/2024/iclr) |
| C6 Peer prediction | **Confirmed** | Full abstract read, authors Qiu, Carroll, Allen: "LLM-as-a-Judge become worse than random guess when facing deceptive models 5-20x the judge's size, while peer prediction thrives when such gaps are large, including in cases with over 100x size difference". ICLR 2026 per two independent venue lists (secondary). | https://raw.githubusercontent.com/CSQianDong/Awesome-arXiv-Daily-Reporter/main/29-Jan-2026/AI/README.md ; https://github.com/Doragd/Algorithm-Practice-in-Industry ; https://github.com/zhaoyang97/Paper-Notes ; https://github.com/zhihengli-casia/AI-Paper-Trends |
| C7 KalshiBench | **Confirmed** | An independent project's verification log reports a first-hand arXiv-abstract check: single author Lukas Nel; v1 2025-12-17; 300 questions; five frontier models; systematic overconfidence; ECE 0.120 (Claude Opus 4.5) and 0.395 (GPT-5.2-XHigh); only one positive Brier Skill Score. Caveats: single-author preprint, not peer-reviewed. Interpretation: the "resolves after training cutoff" property decays as newer models are released. One third-party re-run notes that all its KalshiBench questions resolved inside its models' cutoffs. | https://github.com/ZhangRui987/agent-oversight-framework (VERIFICATION-LOG.md, REFERENCES.md) ; https://github.com/memgrafter/research-digests ; https://github.com/AKarode/parallax-markets |
| C8 EducationQ | **Confirmed** (+caveat) | Paper note table: Llama 3.1 70B Instruct teacher, pre 47.73, post 58.74, ALG 11.01; 14 LLMs; 1,498 questions; 78% expert agreement. Official README confirms ACL 2025 (doi 10.18653/v1/2025.acl-long.1576), authors Shi, Liang, Xu, and student config `llama-3.1-70b-instruct`. Caveat added: the top teacher is the same model as the fixed student. | https://raw.githubusercontent.com/SunriserFuture/EducationQ/main/README.md ; https://raw.githubusercontent.com/zhaoyang97/Paper-Notes-en/main/docs/ACL2025/llm_evaluation/educationq_evaluating_llms_teaching_capabilities_through_multi-agent_dialogue_fr.md ; https://github.com/iwangjian/Paper-Reading-ConvAI |
| C9 MathTutorBench + diagnostic | **Confirmed** (minor correction) | README: "strong problem solvers are not automatically strong tutors"; 1.5B scaffolding reward model; EMNLP 2025 main (doi 10.18653/v1/2025.emnlp-main.11). "Oral" was not found. Diagnostic arXiv:2606.16206 (Yao, Zheng, Li): "across eight publicly reported models, the correlation between solving and pedagogy composites is 0.421". The live leaderboard now has 17 models. | https://raw.githubusercontent.com/eth-lre/mathtutorbench/main/README.md ; https://github.com/qhduan/cn-chat-arxiv (2606.16206) ; https://github.com/2shin0/arxiv-ai-mailing (LLM/2026-06-16.md) ; https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (16-Jun-2026) |
| C10 EvaLearn | **Confirmed** (+ID, authors) | Abstract: 648 problems, six task types, 182 sequences, nine frontier models; "current LLMs with stronger static abilities do not show a clear advantage in learning capability across all tasks". Official repo: arXiv 2506.02672; NeurIPS 2025 proceedings (poster); authors Dou, Zhang, et al. | https://raw.githubusercontent.com/ByteDance-Seed/EvaLearn/main/readme.md ; https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (4-Jun-2025) |
| C11 GDPval | **Corrected** | Confirmed: 1,320 tasks, 44 occupations, 9 sectors (>5% of GDP), 220-task gold subset, blind expert pairwise comparison, Claude Opus 4.1 47.6% wins+ties. The dossier's other win rates, taken from the EnvCommons README, were **wrong**. Paper Fig. 5 and the OpenAI blog chart give GPT-5 high 38.8%, o3 high 34.1%, o4-mini high 27.9%, Gemini 2.5 Pro 25.5%, Grok 4 24.3%, GPT-4o 12.4%. Also: the automated grader agrees with experts 66% of the time vs 71% human inter-rater agreement; the "linear" trend uses three OpenAI models only. | https://github.com/visual-snow/seshat (parsed/openai/gdpval-...md; web-research/openai/gdpval.md) ; https://github.com/UKGovernmentBEIS/inspect_evals (src/inspect_evals/gdpval/README.md) ; https://github.com/howard86/howardism ; https://github.com/turbobeest/modelspec |
| C12 Remote Labor Index | **Corrected** (resolved) | The 2.5% launch figure is confirmed verbatim in 4 arXiv digests; the top agent was Manus. For 2026, four independent secondary sources give **16.10% (Fable 5)** on the Scale AI × CAIS leaderboard as of 1-2 July 2026 (Opus 4.8 8.33%, Codex GPT-5.5 6.25%; 240 projects). The 15.8% figure is an outlier. No primary leaderboard page could be opened, so confidence is M. | https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (31-Oct-2025) ; https://github.com/2shin0/arxiv-ai-mailing ; https://github.com/ruvnet/metaharness (docs/research/rli-remote-labor-index.md) ; https://github.com/guzus/ai-research-arm ; https://github.com/steveash/hitchhikers-guide-to-ai-native-engineering ; https://github.com/kishorebr/aivibe-blog |
| C13 BrainBench | **Confirmed** | 81.4% vs 63.4% (t(14)=25.8); 171 experts passed screening; top-20% experts 66.2%. Official BibTeX: Nature Human Behaviour, Nov 2024, doi 10.1038/s41562-024-02046-9. Some lists date it 2025 (issue date); preprint arXiv:2403.03230. | https://raw.githubusercontent.com/braingpt-lovelab/BrainBench/main/README.md ; https://github.com/cognitivetech/llm-research-summaries ; https://github.com/taesiri/ArXivQA (papers/2403.03230.md) ; https://github.com/pclark425/pclark425.github.io ; https://github.com/LukasWallrich/ai_metascience_replications |
| C14 PaperBench | **Corrected** | Confirmed: 20 ICML 2024 Spotlight/Oral papers; 8,316 gradable tasks; abstract "best-performing tested agent, Claude 3.5 Sonnet (New) ... 21.0%"; Code-Dev "around an 85% reduction in o3-mini SimpleJudge costs". Correction: the official leaderboard's best reported agent is **IterativeAgent o1-high at 26.0 ± 0.3% (36 h limit)**, then 24.4% (24 h), then BasicAgent claude-3.5-sonnet at 21.0%. So "best reported agent = Claude BasicAgent 21.0%" holds only for the abstract's headline comparison. | https://raw.githubusercontent.com/openai/preparedness/main/project/paperbench/README.md ; https://github.com/swkim101/cspapers.org (index2/2025/icml) ; https://github.com/visual-snow/seshat (web-research/openai/paperbench.md) |
| C15 Uncheatable Eval | **Confirmed** | Full title "Uncheatable Eval: Dynamic Compression-Based Evaluation of Language Models"; abstract: 80 models, 14 text categories, "lower compression rates are strongly associated with higher zero-shot MMLU accuracy"; aimed at base models. Authors Tan, Li, Shen; 2026-09-23. Official code repo carries the arXiv badge. | https://github.com/qhduan/cn-chat-arxiv (papers/26/09/2609.27510.json) ; https://github.com/Jellyfish042/uncheatable_eval ; https://github.com/zhaolin-amd/llm-paper-radar ; https://github.com/rxmna8502/vybe-intelligence-vault |
| C16 AbstentionBench | **Confirmed** (+detail) | README: 20 datasets, 6 abstention scenarios, "reasoning fine-tuning hurts abstention". The abstract adds "by 24% on average" across 20 frontier LLMs. Grading uses an LLM judge (88% agreement per a digest). | https://raw.githubusercontent.com/facebookresearch/AbstentionBench/main/README.md ; https://github.com/ProfSynapse/Epistemic-Humility-Research ; https://github.com/memgrafter/research-digests |

**Totals:**

- **13 confirmed:** C1-C10, C13, C15 and C16. Several gained added detail or caveats; C9 had a minor venue-label correction.
- **3 corrected:** C11, C12 and C14.
- **0 refuted.**
- **0 unverifiable.**

### Other corrections made in the body (outside the 16 claims)

1. **Reasoning or Reciting? (arXiv:2307.02477).** The title ends "Counterfactual Tasks", not "Counterfactual Evaluations".
2. **Gemini 1.5 MTOB.** The human en→kgv score is 5.60 in the report's tables; its prose says 5.58. The 4.14 kgv→en "best setting" is the half-book setting (full book 4.00). The ratings come from a single, self-aware rater.
3. **Saha et al.** The repo README heading does *not* use the "Theory of Mind" title; that is the arXiv v1 title.
4. **MathTutorBench.** "EMNLP 2025 Oral" was downgraded to "EMNLP 2025 main"; Oral is unverified.
5. **IDs added:**
   - LiveCodeBench: arXiv:2403.07974
   - EvaLearn: arXiv:2506.02672
   - Pitfalls in Evaluating LM Forecasters: arXiv:2506.00723
   - BABILong: arXiv:2406.10149
   - DyCodeEval: arXiv:2503.04149 (per survey README)
6. **Authors added:** GDPval, SWE-Lancer, PaperBench, EducationQ, EvaLearn, arXiv:2606.16206, Future of Facts, Reversal Curse, Paleka et al. forecasters, LLM-as-an-Interviewer.
7. **Venues added:** MTOB (ICLR 2024); Aycock et al. (ICLR 2025); NPHardEval (ACL 2024 anthology link).
8. **Future of Facts (arXiv:2605.27564).** The title-to-ID link was upgraded from M to H via the official repo.
9. **AbstentionBench.** Uses an LLM judge, so it should not be cited as judge-free.

### Reference-check summary (refs JSON)

- **References checked:** 65 of 65; none skipped.
- **`verified: true` (paper/repo exists with that title and ID):** 65.
- **Entries with a problem found and fixed (title, ID, authors, venue, or conflicting numbers):** 21.
  - 6 were substantively wrong or misleading: wu2023reasoningreciting (title), envcommons2025gdpval (win rates), gemini2024gemini15 (5.58 vs 5.60; half-book), openai2025paperbench (the "best agent" framing), saha2023teach (dossier text about the README title), macina2025mathtutorbench ("Oral" in the dossier text).
  - The rest were incomplete metadata.
  - Title corrected: wu2023reasoningreciting, tutordiag2026, tan2026uncheatable (title completed).
  - ID added: jain2024livecodebench, evalearn2025, paleka2025pitfalls, kuratov2024babilong; factualgvgap2026 (ID normalised).
  - Authors added or completed: openai2025gdpval, openai2025swelancer, openai2025paperbench, educationq2025, kim2024interviewer, paleka2024forecasterconsistency, berglund2023reversal.
  - Venue added or refined: tanzer2023mtob, aycock2024grammarbook, macina2025mathtutorbench (Oral not verified), fan2023nphardeval.
  - Content conflict flagged: envcommons2025gdpval (win rates do not match the paper); gemini2024gemini15 (5.58 vs 5.60; half-book).
- **Venue claims that remain secondary or unverified** (flagged in `verify_note`):
  - DyVal (ICLR 2024), DyVal 2 (ICML 2024), Skill-Mix (ICLR 2024), TreeEval (NeurIPS 2024), FutureX (ICLR 2026), GDPval (ICLR 2026), ScienceAgentBench (ICLR 2025: the README BibTeX is @misc 2024), Debate (ICML 2024 and Best Paper), Reasoning Gym (Spotlight), Auto-Arena (a later "ACL'25" version under a different title), Future of Facts (NeurIPS 2026 per an author homepage only).
- **Fabricated or non-existent references found:** none. Every arXiv ID in the file resolved to a paper whose title matches the dossier in at least one independent listing.
