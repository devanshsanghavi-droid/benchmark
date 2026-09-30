# Panel C: Benchmarks that failed, saturated, leaked or stopped discriminating, and a test of the "novel critical thinking" hypothesis (as of 30 Sep 2026)

**Method and limits.** The research date is 2026-09-30. The session's shared web-search budget ran out after about 35 searches. arxiv.org, openai.com, epoch.ai, arcprize.org, zapier.com, aclanthology.org and matharena.ai were blocked for direct fetch, so primary papers were checked another way:
- verbatim abstract mirrors found with GitHub code search, such as arXiv daily-digest repositories and the ACL Anthology XML;
- GitHub repository pages fetched directly;
- anthropic.com fetched directly;
- search-result summaries of primary pages.

The earlier dossiers in `research/notes/` and `briefs/C_failures_attention.md` were used only as leads. Numbers carried over from them without being re-checked this session are marked **(not re-verified)**.

Confidence: **H** means a primary source or a verbatim mirror of one. **M** means a single secondary source, a search summary of a primary page, or a figure not re-verified. **L** means an aggregator only. Speculation is marked [speculation].

---

## 1. Summary and hypothesis verdict

### Takeaway
The hypothesis is **refuted as a "one common factor" claim and partly confirmed as a claim about one failure mode.** Leaked or familiar items explain contamination failures (AIME 2024, HumanEval, SWE-bench Verified, GSM8K for some model families). They do not explain the other four failure modes, and several benchmarks built on genuinely novel items or skills still saturated fast.

### Cited Findings (summary bullets)
1. **Novel items do not prevent saturation.** FrontierMath Tier 4 used unpublished, expert-written problems. Its top score went from 5% to 98% in less than 14 months, and Epoch now considers it saturated — [Epoch AI on X](https://x.com/EpochAIResearch/status/2098103831502708864); [AlphaSignal](https://alphasignal.ai/news/openai-s-gpt-6-astra-cracks-epoch-s-hardest-math-benchmark-in-14-months). MathArena says final-answer contest benchmarks, which use fresh and uncontaminated problems each year, "have become saturated in just one year" — [MathArena platform paper](https://arxiv.org/abs/2605.00674); [MathArena "Farewell"](https://matharena.ai/no_final_answer/).
2. **Novel *skills* do not prevent saturation either; they delay it.**
   - ARC-AGI-1 took about 4 years to go from 0% (GPT-3) to 5% (GPT-4o). Then o3 reached 75.7%, or 87.5% at high compute (Dec 2024).
   - 49% of ARC-AGI-1's private set had already fallen to an ensemble of brute-force program searches in 2020.
   - ARC-AGI-3 reached 62.7% with the standard harness and 99.9% with a provider-built harness about six months after launch.
   - Sources: [ARC Prize 2024 report](https://arxiv.org/abs/2412.04604); [ARC Prize Astra post](https://arcprize.org/blog/astra).
3. **Contamination is real where it occurs, but it is uneven.**
   - AIME 2024 scores run 10–20 points above what AIME 2025 predicts [MathArena](https://arxiv.org/abs/2505.23281).
   - OpenAI stopped reporting SWE-bench Verified after "all frontier models we tested" reproduced gold patches [OpenAI via mirror](https://github.com/BobYeger/state-of-agents/blob/main/raw/articles/openai-retires-swe-bench-verified.md).
   - On GSM1k, Phi and Mistral drop by up to 13%, while frontier models show "minimal" overfitting [GSM1k](https://arxiv.org/abs/2405.00332).
4. **Validity collapse is common and independent of novelty.** Novel expert items are, if anything, *more* error-prone:
   - FrontierMath v2 fixed errors in 42% of problems [Epoch](https://epoch.ai/benchmarks/frontiermath-tier-4-v2).
   - About 29% of HLE's chemistry and biology answers conflict with the literature [FutureHouse](https://www.futurehouse.org/research/hle-exam).
   - On τ-bench, a do-nothing agent scores 38% [ABC repo](https://github.com/uiuc-kang-lab/agentic-benchmarks).
   - On HellaSwag, more than 65% of predictions are unchanged when the question is replaced with "Lorem ipsum" [Chizhov et al.](https://arxiv.org/abs/2504.07825).
5. **Gaming does not depend on novelty.** LMArena draws fresh user prompts continuously, yet Meta privately tested 27 variants before Llama 4 [Leaderboard Illusion](https://arxiv.org/abs/2504.20879).
6. **Most of the user's own "failed" list failed on adoption, not measurement.** Several were explicitly designed around novelty or contamination resistance:
   - Qi Town was motivated by "the limitation of data dependency" of Q&A benchmarks.
   - The raw-corpora pipeline "avoids benchmark contamination".
   - TopoBench and MastermindEval are procedurally generated.

   They stalled through empty repositories, no leaderboard, pre-emption or white-box metrics (§3.3).
7. **Benchmarks with no novelty often stayed useful for years.**
   - SWE-bench discriminated for about 2.3 years although its issues come from public GitHub.
   - GPQA Diamond went from 39% to above 90% over about 2 years.
   - AutomationBench tests no novel skill, yet it entered frontier launch tables within 5 months (§2).
8. **Benchmark lifetimes are shrinking.**
   - AI Index 2026: evaluations "intended to be challenging for years are saturated in months" [AI Index 2026 ch. 2](https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf).
   - Of 60 widely used benchmarks, about half are saturated. Age and test-set size predict saturation; private test sets show no protective effect [Akhtar et al.](https://arxiv.org/abs/2602.16763).
9. **Procedural novelty plus automatic verification turns a benchmark into a training environment.** Reasoning Gym ships more than 100 such generators for reinforcement learning with verifiable rewards (RLVR). Logic-RL reached 0.99–0.89 on Knights-and-Knaves puzzles from fewer than 5,000 synthetic samples. A community Mastermind-style ladder was "saturated" by o3-mini about 9 weeks after launch — [Reasoning Gym](https://arxiv.org/abs/2505.24760); [Logic-RL](https://arxiv.org/abs/2502.14768); [Bulls-and-Cows commits](https://github.com/stalkermustang/llm-bulls-and-cows-benchmark/commits/main).
10. **The user's "boring professional benchmarks":**
    - "Automation Bench" is almost certainly **Zapier's AutomationBench** (H).
    - "Office Bench" is **OfficeBench**, arXiv 2407.19056 (H).
    - "DC Bench" is **unresolved**. The best fit is **DCA-Bench**, arXiv 2406.07275 (low-medium). DC-BENCH (dataset condensation, NeurIPS 2022) is a non-LLM name-match.

### Hypothesis verdict (one paragraph)
Taken literally, "failed benchmarks lack novel critical thinking the model can't have been trained on" is **refuted**, for three reasons:
- **Counterexamples with novelty that still failed or saturated.** FrontierMath Tier 4 (novel items), AIME 2025 and the MathArena final-answer contests (novel items), ARC-AGI-1 and ARC-AGI-3 (novel skills), Bulls-and-Cows and MastermindEval (procedural items), and LMArena (novel prompts, gamed anyway).
- **Counterexamples without novelty that stayed useful.** SWE-bench, GPQA Diamond, chess ladders and AutomationBench.
- **Many failures have nothing to do with training exposure.** These are validity collapse (τ-bench, HellaSwag, HLE, FrontierMath errors) and adoption or infrastructure failure (most of the user's list, OfficeBench, DCA-Bench, BIG-bench, HELM).

The hypothesis **survives in narrower form**:
- For **static public instances**, contamination is a real and common killer (AIME 2024, SWE-bench Verified, HumanEval, GSM8K for some families).
- **Novel skills buy time.** ARC-AGI-1 held for about 5 years, against 1–3 years for exam benchmarks.

The better statement (§5) is that failed benchmarks share a **static, finite, cheaply optimisable target with no renewal owner**. Novelty removes one cheap path (memorisation). Brute force, trainable task families, artifacts, broken graders, harness engineering and selective submission remain.

### Inferences
- For benchmark design, novelty should be treated as necessary for contamination resistance but not sufficient for longevity or adoption.

### Gaps
- "DC Bench" could not be resolved with certainty. The user should confirm which benchmark they meant.

---

## 2. Resolving "Automation Bench", "Office Bench" and "DC Bench"

### Takeaway
Two of the three names resolve cleanly: Zapier's AutomationBench and OfficeBench. "DC Bench" has no exact LLM-benchmark referent. DCA-Bench is the closest "professional data work" match.

### Cited Findings

**A. "Automation Bench" = Zapier AutomationBench (confidence that this is the referent: H)**
- **Identity.** "AutomationBench" by Daniel Shepard and Robin Salimans (Zapier), arXiv 2604.18934, posted about 21 Apr 2026 — [arXiv](https://arxiv.org/abs/2604.18934); abstract mirror [DailyAgentPapers](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/21/automationbench.md) (H).
- **Task format.**
  - Cross-application workflow orchestration through REST APIs, across Sales, Marketing, Operations, Support, Finance and HR. The patterns are drawn from real workflows on Zapier's platform.
  - Agents must "discover relevant endpoints themselves, follow layered business rules, and navigate environments with irrelevant and sometimes misleading records".
  - "Grading is programmatic and end-state only." — [abstract mirror](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/21/automationbench.md) (H)
  - The repo has 600 public tasks (100 per domain) across 47 simulated SaaS tools, plus 200 "simple" tasks that are excluded from the score. The official leaderboard uses "a separate, held-out private task set per domain" that is "purposely harder and is not released" — [GitHub](https://github.com/zapier/AutomationBench) (H).
- **Results.**
  - At launch: "Even the best frontier models currently score below 10%" (Apr 2026) [abstract](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/21/automationbench.md) (H).
  - By 22 Sep 2026, Zapier-run scores in Anthropic's launch table were: GPT-6 Astra 41.4%, Claude Opus 5.5 40.0%, Fable 5.1 31.4%, GPT-5.6 Sol 28.8% and Opus 5 26.9%. Footnote: "AutomationBench results were run and reported by Zapier" [Anthropic](https://www.anthropic.com/news/claude-opus-5-5) (H).
  - **Conflict:** the GitHub README leaderboard lists Opus 5 at 50.3%, Kimi K3 at 46.67% and Fable 5 at 46.17% [GitHub](https://github.com/zapier/AutomationBench). This is incompatible with Anthropic's 26.9% for Opus 5. The cause may be a different split, version or scoring; it is unresolved.
- **Adoption.**
  - It is in Anthropic's Opus 5.5 headline table [Anthropic](https://www.anthropic.com/news/claude-opus-5-5) (H).
  - Artificial Analysis runs "AutomationBench-AA" on "a private 657-task held-out split" (v1.0.6) with guardrail-aware scoring. It is part of the Agents category of the AA Intelligence Index (AA methodology text captured 2026-09-21, mirrored at [fstandhartinger/model-market-comparison](https://github.com/fstandhartinger/model-market-comparison); [AA announcement](https://artificialanalysis.ai/articles/announcing-zapier-automationbench-aa)) (M).
  - The repo has 314 stars and 49 forks [GitHub](https://github.com/zapier/AutomationBench) (H).
- **Lesson.** It is a "boring", non-novel skill (API calls plus business rules). It was adopted within months for four reasons:
  1. It maps onto buying decisions.
  2. It is graded deterministically on end state, with no LLM judge.
  3. It keeps a harder private split.
  4. A neutral runner (Zapier, and AA) produces the numbers labs cite.

  Its risks are vendor ownership and a public split that can be trained on. The climb from under 10% to about 41% in 5 months suggests a lifetime of 1–2 years [speculation].

**B. "Office Bench" = OfficeBench (confidence: H)**
- **Identity.** "OfficeBench: Benchmarking Language Agents across Multiple Applications for Office Automation" by Zilong Wang, Yuedong Cui, Li Zhong, Zimin Zhang, Da Yin, Bill Yuchen Lin and Jingbo Shang. arXiv 2407.19056, July 2024 — [arXiv](https://arxiv.org/abs/2407.19056); [GitHub](https://github.com/zlwang-cs/OfficeBench) (H).
- **Task format.**
  - 300 tasks: 93 single-app, 95 two-app and 112 three-app.
  - The apps are office tools (Word, Excel, PDF, email, calendar and so on) in a simulated environment.
  - Evaluation uses "Exact Matching, Fuzzy Matching, and Execution-based Evaluation" [GitHub](https://github.com/zlwang-cs/OfficeBench) (H).
- **Results.**
  - GPT-4o 47.00%, GPT-4 Turbo 38.00%, Llama 3 70B 27.33% and Gemini 1.5 Pro 26.00% [GitHub](https://github.com/zlwang-cs/OfficeBench) (H).
  - Humans 93.33%. GPT-4o by app count: single 64.52%, two 60.00%, three 21.43% [search summary of arXiv](https://arxiv.org/abs/2407.19056) (M).
- **Adoption.**
  - 47 stars and 16 commits; no maintained leaderboard found [GitHub](https://github.com/zlwang-cs/OfficeBench) (H).
  - Its main afterlife is as raw material. Microsoft's OdysseyBench+ turned OfficeBench's 300 tasks "from their original atomic form into rich, multi-interaction dialogue scenarios that span multiple days" [OdysseyBench](https://arxiv.org/abs/2508.09124) (M).
- **Lesson.** It had a realistic construct with a large human–model gap. It still did not become a standard because it had no maintainer or leaderboard, and because a better-resourced successor re-framed atomic tasks as long-horizon ones. Headroom is not adoption.

**C. "DC Bench" = unresolved. Candidates:**

| Candidate | What it is | Fit |
|---|---|---|
| **DCA-Bench** (Benhao Huang et al., arXiv 2406.07275; ACM DOI 10.1145/3711896.3737422, the KDD 2025 proceedings series) | LLM agents detect data-quality issues on dataset platforms. It has 221 real cases from 8 platforms in 4 types with 18 tags, 4 hint levels and a GPT-4(o) automatic evaluator. Without hints, the best curator finds about 30% of issues — [search summary](https://arxiv.org/abs/2406.07275); [GitHub](https://github.com/TRAIS-Lab/dca-bench) (M-H). Repo: 11 stars, no leaderboard (H). | **Best fit (low-medium, about 50%)**: a "boring professional" LLM-agent benchmark whose name contains "DC" |
| **DC-BENCH** (Cui, Wang, Si, Hsieh; NeurIPS 2022 D&B) | Dataset condensation methods (image classification) — [NeurIPS PDF](https://proceedings.neurips.cc/paper_files/paper/2022/file/052e22cfdd344c79634f7ec76fa03e22-Paper-Datasets_and_Benchmarks.pdf) (H) | Exact name match, but not an LLM or professional-task benchmark |
| "DCBench" / "DC Bench" (2026 LLM agents) | Two searches found no such benchmark (see the queries in the search log) | none found |

- **DCA-Bench lesson** (if it is the referent): a realistic professional task with an LLM-judge grader and 221 items, and no leaderboard. It was adopted about as widely as OfficeBench.

### Inferences
- What unites the "boring professional" trio is not novelty. AutomationBench succeeded where OfficeBench and DCA-Bench did not through **distribution plus a trusted, deterministic, private-split grader plus a sponsor with a reason to keep it running.**

### Gaps
- AutomationBench's public/private scoring conflict (50.3% vs 26.9% for Opus 5) is unresolved.
- OfficeBench's venue was not verified.
- The user should confirm the "DC Bench" referent. [speculation] They may be misremembering DSBench, DA-Code or GDPval.

---

## 3. Per-benchmark failure entries

### Takeaway
Failure modes cluster into five types: contamination, saturation, validity collapse, adoption/infrastructure and gaming. Most benchmarks have two or more. Time-to-saturation has fallen from about 3–5 years (2019–2021 benchmarks) to about 6–14 months (2025–2026 "hard" ones).

### Cited Findings

#### 3.1 Knowledge and exam benchmarks
- **MMLU (2020).** Failure modes: saturation, validity, contamination.
  - Validity: 6.49% of questions contain errors; Virology is 57% erroneous [MMLU-Redux](https://arxiv.org/abs/2406.04127) (H, via abstract summary).
  - Saturation: from 43.9% (GPT-3, 2020) to about 90% (Gemini Ultra, CoT@32, Dec 2023). That is about 3.3 years (not re-verified; M).
  - AI Index 2026 reports frontier models "topping 88%" [AI Index 2026](https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf) (M).
  - Contamination probe: GPT-4 guessed masked MMLU options 57% of the time (TS-Guessing, Deng et al.; not re-verified; M).
- **MMLU-Pro (2024).** Failure mode: saturation. It was retained mainly by open-weight labs (not re-verified). I did not verify the size of its top-model spread this session → Gaps.
- **HellaSwag (2019).** Failure modes: validity collapse, contamination, saturation.
  - "Severe construct validity issues".
  - With "Lorem ipsum dolor..." in place of the question, "more than 65% of model predictions remain the same, and this cannot be attributed merely to contamination" [Chizhov et al. abstract mirror](https://github.com/Luvata/arxive/blob/main/pages/2025-04-11-cs-cl.html) (H).
  - Launch: BERT 47.3% vs humans 95.6%. GPT-4 95.3% (Mar 2023), about 4 years later (not re-verified; M).
- **BIG-bench and BBH.** Failure modes: adoption (BIG-bench) and saturation (BBH).
  - The BIG-bench repo (>200 tasks) was archived on 17 Apr 2026 [GitHub](https://github.com/google/BIG-bench) (H).
  - BBH was deemed saturated, "with models scoring over 90%", which motivated BBEH. On BBEH, o3-mini-high scores 44.8% (harmonic mean) [BBEH](https://arxiv.org/abs/2502.19187) (M).
  - **Conflict:** Akhtar et al. classed BBH as unsaturated by their separability index (not re-verified). Their metric (top-5 separability on leaderboard data) differs from "near ceiling".
- **GPQA Diamond (Nov 2023).** Failure mode: saturation by capability.
  - Experts score about 65% on full GPQA; skilled non-experts with web access about 34% (GPQA paper; not re-verified; M).
  - Top scores rose from GPT-4's about 39% to 94.3% (Gemini 3.1 Pro).
  - Epoch fits a logistic with an asymptote of about 92%, meaning it is "approaching saturation" [Epoch search summary](https://epoch.ai/gradient-updates/gpqa-diamond-whats-left) (M).
  - 198 items limit resolution (prior note; not re-verified).
  - Useful for about 2 years despite static items.
- **Humanity's Last Exam (Jan 2025).** Failure modes: validity (label errors). **Not saturated.**
  - "29 ± 3.7% (95% CI)" of text-only chemistry and biology answers conflict with peer-reviewed evidence (FutureHouse). An HLE-team follow-up found about 18% problematic in a subset [FutureHouse](https://www.futurehouse.org/research/hle-exam); [search summary](https://the-decoder.com/nearly-29-percent-of-humanitys-last-exam-questions-are-wrong-or-misleading/) (M-H).
  - Responses: HLE-Rolling and HLE-Verified [HLE-Verified](https://arxiv.org/abs/2602.13964) (M).
  - Progress: under 10% at launch, then +30 points in one year [AI Index 2026](https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf). Public-leaderboard top was 46.44% on 16 Aug 2026 (search summary; M).

#### 3.2 Math and code
- **GSM8K (2021) and GSM1k.** Failure modes: saturation, plus contamination for some families.
  - GSM1k found drops of up to 13% (Phi, Mistral). There is a positive relation between the probability of generating GSM8K items and the gap (r² = 0.36, NeurIPS version).
  - Frontier models showed "minimal overfitting" [GSM1k](https://arxiv.org/abs/2405.00332); [Scale](https://labs.scale.com/papers/llm-performance-grade-school-arithmetic) (H).
- **MATH (2021).** Failure mode: saturation (with some memorised technique).
  - Launch: 3.0–6.9%, with the authors extrapolating that scaling alone would be "impractical" [MATH search summary](https://arxiv.org/abs/2103.03874) (M).
  - o1: 94.8% (Sep 2024; likely MATH-500), about 3.5 years later (not re-verified; M).
- **HumanEval and MBPP (2021).** Failure modes: saturation, contamination, weak tests.
  - Codex 28.8% at launch; o4-mini-high 99.3% by Apr 2025 (not re-verified; M).
  - EvoEval: 19.6–47.7-point drops on transformed tasks, with "drastic ranking changes" [EvoEval](https://arxiv.org/abs/2403.19114) (M).
  - LiveCodeBench: some models do well on HumanEval but not on fresh problems [LiveCodeBench](https://arxiv.org/abs/2403.07974) (M).
- **AIME (yearly).**
  - AIME 2024 is contaminated: models score 10–20% above expectations derived from AIME 2025, and QwQ-Preview about 60% above [MathArena](https://arxiv.org/abs/2505.23281) (H-M).
  - The *novel* AIME 2025 and HMMT sets saturated too. MathArena: final-answer benchmarks "saturated in just one year", so it moved to proofs, Apex and research questions [MathArena platform](https://arxiv.org/abs/2605.00674); [Farewell post](https://matharena.ai/no_final_answer/) (M-H).
- **FrontierMath (Nov 2024).** Failure modes: saturation (Tier 4), validity, conflict of interest.
  - Tier 4 went from 5% (11 Jul 2025) to 98% (GPT-6 Astra, Sep 2026), "less than 14 months", and is saturated [Epoch X](https://x.com/EpochAIResearch/status/2098103831502708864) (M; the X post was seen via search).
  - Errors: an AI-assisted audit "flagged fatal errors in about a third of problems" [Epoch X](https://x.com/EpochAIResearch/status/2053995435870892048) (M). v2 (12 Jun 2026) addressed errors in 42% of problems (123 + 12 corrected; 5 + 7 removed; 338 remain), and models scored about 12 points higher on the corrected set [Epoch](https://epoch.ai/benchmarks/frontiermath-tier-4-v2); [Digital Applied](https://www.digitalapplied.com/blog/epoch-frontiermath-v2-error-corrected-ai-benchmark-analysis) (M).
  - Funding and access: OpenAI commissioned the problems and has access except for a holdout. This was disclosed around o3's launch (Dec 2024). o3's claimed 25% compares with about 10% in Epoch's independent run (Apr 2025) (not re-verified; M) [Epoch](https://epoch.ai/latest/openai-and-frontiermath).
- **SWE-bench Verified (Aug 2024).** Failure modes: contamination, validity collapse, gaming.
  - OpenAI (23 Feb 2026): "at least 59.4% of the audited problems have flawed test cases that reject functionally correct submissions" (a 27.6% subset that models often failed).
  - Also: "all frontier models we tested were able to reproduce the original, human-written bug fix … or verbatim problem statement specifics."
  - "We have stopped reporting SWE-bench Verified scores" [OpenAI via verbatim mirror](https://github.com/BobYeger/state-of-agents/blob/main/raw/articles/openai-retires-swe-bench-verified.md) (H).
  - SWE-Bench Illusion: buggy-file identification from the issue text alone reached "up to 76%" on SWE-bench Verified, against "up to 53%" outside it [abstract mirror](https://github.com/ATOM00blue/machine-learning-library/blob/main/corpus/papers/2506.12286.md) (H).
  - Progress: SWE-bench went from 4.4% (2023) to 71.7% (2024) [AI Index 2025 via IBM](https://www.ibm.com/think/news/stanford-hai-2025-ai-index-report) (M).
  - Useful life about 18 months (Verified) to 2.3 years (SWE-bench).

#### 3.3 The user's "failed" list

Identity and abstracts were re-verified through mirrors; repos were checked on 2026-09-30.

- **Qi Town** (arXiv 2508.04720). Failure mode: adoption.
  - It was explicitly motivated by "compensating the limitation of data dependency of the mainstream Question-and-Answer (Q&A) based benchmark method".
  - Design: 5 widely played games, 20 LLM players, and three metrics (Elo, a Performance Loop Graph, and a "Positive Sentiment Score" for "mental fitness") [abstract mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/main/8-Aug-2025/AI/README.md) (H).
  - No public code was found (prior dossier; not re-verified).
  - Launched the day after Kaggle Game Arena (4 Aug 2025; not re-verified; M).
- **Game Reasoning Arena** (arXiv 2508.03368). Failure mode: adoption/maintenance. The last commit was 11 Sep 2025, about 5 weeks after launch [GitHub commits](https://github.com/SLAMPAI/game_reasoning_arena/commits/main) (H). Pre-empted by Kaggle Game Arena on the same OpenSpiel engine (M).
- **MastermindEval** (arXiv 2503.05891). Failure modes: shortcut (brute force) and narrow construct. **Survived as a component.**
  - The lm-eval harness has 6 tasks: code length and colours of 2/4, 3/5 and 4/6. Games are "pre-played … using Knuth's algorithm", and the hard variant uses distractors one symbol away [lm-eval](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mastermind) (H).
  - Hypothesis spaces are at most 6⁴ = 1,296 codes (arithmetic), so a short program enumerates them.
- **Concept** (Findings of ACL 2026). **Not failed; too young.** "Easily solved by humans (with a success rate of over 90%) … no model exceeds 40%" [ACL abstract mirror](https://github.com/smallflyingpig/ai-conference-overview) (H). The roster was mid-2025 models (prior dossier; L).
- **Codenames ad-hoc concept forming** (GEM² at ACL 2025). **Survived inside clembench.** It varies frequency, ambiguity, concreteness, assassins and opponent difficulty [clembench/codenames](https://github.com/clp-research/clembench/tree/main/codenames) (H). It was pre-empted by Stephenson et al. (Dec 2024; M).
- **Boardwalk** (arXiv 2508.16447). A framework, not a benchmark; small N.
  - 12 games and 3 LLMs. "We anonymize the games … to avoid evoking pre-trained LLM knowledge." Best result: 55.6% error-free (Claude 3.7 Sonnet) [abstract mirror](https://github.com/Kedreamix/Talk2Paper) (H).
  - Anonymising names hides surface form, not structure (inference).
- **Grid-based game competitions** (arXiv 2407.07796). Failure mode: abandonment.
  - 2,310 matches [BenchmarkCards](https://github.com/SokolAnn/BenchmarkCards) (H).
  - The last model was added 19 Jul 2024 (gpt-4o-mini) and the last commit was 14 Dec 2024 [commits](https://github.com/research-outcome/LLM-Game-Benchmark/commits/main) (H).
  - Not maxed out: invalid moves and disqualifications were frequent with image prompts (prior dossier; M).
- **TopoBench** (arXiv 2603.12133). Failure mode: missing artifacts.
  - "Even frontier models solve fewer than one quarter of hard instances" [abstract mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/main/13-Mar-2026/NLP/README.md) (H).
  - The code repo named in the abstract is **empty** [GitHub](https://github.com/mayug/topobench-benchmark) (H).
- **Raw corpora → domain benchmarks** (arXiv 2506.07658). Failure modes: white-box metric and construct.
  - Its pipeline "avoids benchmark contamination, enables automated updates with new domain data" [abstract mirror](https://github.com/Luvata/arxive/blob/main/pages/2026-03-09-cs-cl.html) (H).
  - It scores by target-token rank and needs logits, and every evaluated model is open-weight and ≤8B (prior dossier; M).
- **BloomQA** (arXiv 2601.20253). Failure modes: validity risk and no release.
  - Generated MCQs and dialogues from expert guidelines. "LLMs sometimes perform relatively better on higher-order reasoning (Analyze) but fail more frequently on lower-level items (Remember)" [abstract mirror](https://github.com/advanced-cs/arXiv_daily/blob/main/daily_papers/20260129_Thu/text.md) (H).
  - The inversion may be an artifact of generated difficulty labels (prior dossier's interpretation; [speculation]).
- **Bulls-and-Cows** (added as a counterexample). Procedurally novel codes. Created 26 Nov 2024; last commit 31 Jan 2025: "o3-mini saturated the benchmark...." [commits](https://github.com/stalkermustang/llm-bulls-and-cows-benchmark/commits/main) (H). That is about 9.5 weeks to saturation.

#### 3.4 Agentic, arena and multimodal
- **τ-bench.** Failure mode: validity collapse. "A trivial do-nothing agent scores 38% pass@k and pass^k"; "a spamming agent that dumps database content scores 40%" [ABC repo](https://github.com/uiuc-kang-lab/agentic-benchmarks) (H).
- **WebArena, KernelBench, SWE-Lancer, OSWorld.**
  - WebArena has outcome-validity flaws (string matching and a naive LLM judge; 1.6–5.2% absolute misestimation, search summary).
  - KernelBench overestimates capability by 31%.
  - SWE-Lancer tests can be bypassed through password-protected zips.
  - The Agentic Benchmark Checklist (ABC) reports "up to 100% in relative terms" misestimation and a 33% reduction on CVE-Bench [ABC repo](https://github.com/uiuc-kang-lab/agentic-benchmarks) (H); [ABC paper](https://arxiv.org/abs/2507.02825) (M for the 100% and 33% figures, via secondary mirror).
  - WebArena progress: 14.41% (GPT-4 agent) vs 78.24% human in 2023, to about 71–74% on a 2026 third-party leaderboard [WebArena](https://arxiv.org/abs/2307.13854) (H); [Steel leaderboard](https://leaderboard.steel.dev/leaderboards/webarena/) (L).
- **LMArena.** Failure mode: gaming.
  - "27 private LLM variants tested by Meta in the lead-up to the Llama-4 release".
  - Google and OpenAI received about 19.2% and 20.4% of all Arena data.
  - Arena data yields "relative performance gains of up to 112%" on the Arena distribution [abstract mirror](https://github.com/aishwaryanr/awesome-generative-ai-guide/blob/main/research_updates/2025_papers/april_list.md) (H).
  - Meta's "Llama-4-Maverick-03-26-Experimental" topped the board. LMArena: "Meta's interpretation of our policy did not match what we expect from model providers" [The Register](https://www.theregister.com/2025/04/08/meta_llama4_cheating/); [Willison](https://simonwillison.net/2025/Apr/8/lmaren/) (M-H).
- **MMMU (Nov 2023).** Failure modes: validity (text-only solvability) and saturation.
  - MMMU-Pro filtered out "questions answerable by text-only models", and performance fell by 16.8–26.9% [MMMU README](https://github.com/MMMU-Benchmark/MMMU) (H).
  - +18.8 points within a year [AI Index 2025 via IBM](https://www.ibm.com/think/news/stanford-hai-2025-ai-index-report) (M).
  - 2026 frontier is about 80% vs an 88.6% expert ceiling [aggregator](https://benchmarkingagents.com/mmmu-benchmark/) (L).
- **ARC-AGI-1 (2019).** Failure modes: shortcut (search), test-time training, compute.
  - "ARC-AGI-1 took 4 years to go from 0% with GPT-3 in 2020 to 5% in 2024 with GPT-4o" [ARC Prize, quoted in AINews mirror](https://github.com/smol-ai/ainews-web-2025) (H).
  - In 2020 the top single entry scored 20%, but an ensemble of all 2020 Kaggle entries solved 49% of the private set, mostly by brute-force program search [ARC Prize 2024 report](https://arxiv.org/abs/2412.04604) (M-H).
  - In 2024 test-time training won: ARChitects 53.5% and MindsAI 55.5% (ineligible) [ARC Prize 2024 report](https://arxiv.org/abs/2412.04604) (M-H).
  - o3-preview: 75.7% within the $10k limit and 87.5% at about 172× compute (20 Dec 2024). It was trained on 75% of the public training set [ARC Prize blog](https://arcprize.org/blog/oai-o3-pub-breakthrough) (M; mirrored quote).
- **ARC-AGI-3 (Mar 2026).** Failure mode: harness saturation. GPT-6 Astra scored 62.7% ($26K) with the standard harness and 99.9% ($19K) with a provider adapter that keeps reasoning state and builds per-game tools such as a board parser (about 3 Sep 2026) [ARC Prize](https://arcprize.org/blog/astra); [Techmeme](https://www.techmeme.com/260903/p40) (M).
- **Infrastructure deaths.** HELM entered maintenance mode on 1 Jun 2026, with no new evaluations [HELM](https://github.com/stanford-crfm/helm/blob/main/docs/maintenance_mode.md) (H). The Open LLM Leaderboard was retired in Mar 2025 (prior dossier; M).

#### 3.5 Shrinking lifetimes (statistics)
- AI Index 2025: within a year of introduction, MMMU, GPQA and SWE-bench rose by 18.8, 48.9 and 67.3 points respectively [IBM summary](https://www.ibm.com/think/news/stanford-hai-2025-ai-index-report) (M).
- AI Index 2026: evaluations "intended to be challenging for years are saturated in months"; "nearly half of the 60 most-cited benchmarks are now saturated" [AI Index 2026](https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf) (M).
- Akhtar et al. (ICML 2026):
  - 60 benchmarks; "nearly half" saturated (29 highly saturated; count not re-verified).
  - "Benchmark age and scale are strong predictors, while … private test sets or closed-ended formats show limited effects."
  - "Expert-curated benchmarks resist saturation better than crowdsourced ones."
  - Sources: [arXiv](https://arxiv.org/abs/2602.16763); [ICML](https://icml.cc/virtual/2026/poster/63311) (H for the qualitative claims via search summary).
  - LiveBench, although refreshed, has a saturation index of 0.99 at about 79% accuracy (not re-verified; M).
- Rough time-to-saturation, derived from the entries above:

| Benchmark (era) | Time to saturation or retirement |
|---|---|
| HellaSwag (2019) | ~4 yr |
| ARC-AGI-1 (2019) | ~5 yr |
| MMLU (2020) | ~3.3 yr |
| MATH (2021) | ~3.5 yr |
| HumanEval (2021) | ~3 yr |
| GPQA (2023) | ~2 yr |
| SWE-bench Verified (2024) | ~1.5 yr |
| AIME 2025 / final-answer (2025) | ~1 yr |
| FrontierMath T4 (2025) | ~14 mo |
| ARC-AGI-3 (2026) | ~6 mo (harness) |
| Bulls-and-Cows (2024) | ~9.5 wk |

### Inferences
- The shortest lifetimes (Bulls-and-Cows, ARC-AGI-3, FrontierMath T4) belong to benchmarks that were **contamination-free by construction**. Speed of saturation is driven by how cheaply the target can be optimised (verifiable reward, searchable space, harness engineering, a lab-funded push), not by item exposure.
- Expert-curated novel items (HLE, FrontierMath) trade contamination risk for verification risk. Errors run at about 18–42%, well above the roughly 5% FrontierMath originally self-estimated ([Epoch, via mirror](https://github.com/benchflow-ai/awesome-evals)).

### Gaps
- MMLU-Pro spread, GLUE/SuperGLUE timings and Ott et al.'s 3,765-benchmark statistics were not re-verified this session (search budget exhausted).
- The exact Akhtar per-benchmark S-index values were not re-fetched.

---

## 4. Hypothesis test table

### Takeaway
Of 36 cases:
- **Supports (7):** AIME 2024, SWE-bench Verified, HumanEval/MBPP, MATH, GSM8K (non-frontier only), and weakly Boardwalk and Codenames. All but Codenames are contamination or structural-familiarity failures; Codenames rests on a skill LLMs are natively trained for.
- **Contradicts (17):** these either had novelty and failed or saturated, or lacked novelty and stayed useful (GPQA, AutomationBench).
- **Neutral (12):** failures that are orthogonal to novelty (validity or adoption).

### Cited Findings (evidence per row is in §3 and §6)

| Benchmark | Novel items? | Novel skill? | Failure mode(s) | S / C / N | Why |
|---|---|---|---|---|---|
| MMLU | No | No | Saturation, validity (6.49% errors), some contamination | N | Died of ceiling plus label noise. Still discriminated for ~3 yr without novelty |
| MMLU-Pro | No | No | Saturation | N | Harder items bought time; novelty irrelevant |
| GSM8K / GSM1k | No / yes | No | Contamination (Phi, Mistral); frontier capability caught up | S (non-frontier) / C (frontier) | Frontier models did as well on novel GSM1k; saturation was real capability |
| HumanEval / MBPP | No | No | Contamination, saturation, weak tests | S | EvoEval drops of 19.6–47.7 pp show memorisation |
| HellaSwag | No | No | Validity (answer-only shortcut), contamination | N | >65% of predictions unchanged with Lorem ipsum: a shortcut, not memorised items |
| BIG-bench | Partly | Partly | Adoption (archived) | N | 200+ tasks, many novel; breadth without a ladder |
| BBH | No | No | Saturation (>90% per BBEH) | N | BBEH, with *novel* replacement tasks, restored headroom: novelty as renewal (see §5) |
| MATH | No | No | Saturation; some memorised technique | S (partial) | Long life (~3.5 yr) despite public items |
| GPQA Diamond | No (static) | No | Saturation by capability | C | Non-novel yet discriminative ~2 yr |
| AIME 2024 | No (leaked) | No | Contamination | S | 10–20 pts above AIME-2025 expectation |
| AIME 2025 / final-answer contests | **Yes** | No | Saturation within ~1 yr | C | Fresh, uncontaminated, still saturated |
| FrontierMath T1–3 / T4 | **Yes** (unpublished) | No | Saturation (T4, 14 mo), 42% item errors, funder access | C | Novel instances did not prevent a 5→98% run |
| HLE | **Yes** | No | Validity (29% bio/chem) | N | Not saturated; problem is label quality |
| SWE-bench Verified | No (public GitHub) | No | Contamination, 59.4% flawed tests | S (C for longevity) | Leakage helped kill it, but it discriminated for 18+ mo despite contamination |
| WebArena | Yes (self-hosted sites) | Partly | Validity (grader flaws); climbing | N | Grader, not novelty |
| τ-bench | Yes | No | Validity (do-nothing 38%) | N | Broken success criterion |
| LMArena | **Yes** (live prompts) | No | Gaming (27 variants; Llama 4) | C | Continuous novelty did not stop selective submission |
| MMMU | No | No | Validity (text-only answerable), saturation | N | Shortcut, not leakage |
| ARC-AGI-1 | **Yes** (private) | **Yes** | Brute force (49% ensemble), TTT, compute | C | Flagship "novel skill" benchmark; fell anyway |
| ARC-AGI-3 | **Yes** | **Yes** | Harness saturation (62.7% → 99.9%) | C | Novel interactive games, ~6 mo |
| LiveBench | **Yes** (rolling) | No | Saturation by separability (S = 0.99; not re-verified) | C | Refresh alone did not keep separation |
| Bulls-and-Cows | **Yes** (procedural) | No | Saturation in ~9.5 wk | C | Procedural novelty; o3-mini saturated it |
| Logic-RL K&K (as eval) | **Yes** (procedural) | No | Trained to 0.99–0.89 with <5k samples | C | Verifiable generators become RL curricula |
| Qi Town | Yes (fresh games) | No | Adoption, pre-emption, mixed metrics | C | Explicitly built to escape "data dependency"; failed anyway |
| Game Reasoning Arena | Yes | No | Adoption, friction, pre-emption | C | Novel play did not help |
| MastermindEval | **Yes** (procedural) | No | Brute-forceable (≤1,296 codes), narrow; survived in lm-eval | C | Memorisation was never the threat |
| Concept | Partly (human logs) | Partly (abduction) | Too young; no leaderboard | N | Headroom high; outcome pending |
| Codenames (Hakimov) | Yes (sampled boards) | No | Pre-emption, crowding; survived in clembench | S (weak) | Skill (association) is native to LLMs, but it failed on crowding |
| Boardwalk | Attempted (renamed) | No | Framework not benchmark; small N; partial artifacts | S (weak) | Renaming hides surface, not structure |
| Grid games | Yes (matches) | No (solved games) | Abandonment | C | Not saturated; died of maintenance |
| TopoBench | **Yes** (generated) | No | Empty repo, name collision | C | Hard (<25%) yet unused |
| Raw corpora → domain | **Yes** (fresh corpora) | No | White-box metric; construct | C | Contamination-free by design; unusable on closed models |
| BloomQA | **Yes** (generated) | No | Validity risk; no release | C | Novel items; weak labels |
| OfficeBench | Yes | No | Adoption (no ladder); absorbed by OdysseyBench | N | Headroom (47% vs 93%) not enough |
| DCA-Bench (if referent) | Yes (real cases) | No | Adoption; LLM-judge grading | N | Realistic, unmaintained |
| AutomationBench | Yes (private split) | **No** | Not failed; rising fast (<10% → ~41%) | C | "Boring" and non-novel, yet adopted into launch tables |

### Inferences
- **Novel instances** (items not in training) predict immunity to *contamination* only. They are uncorrelated with lifetime in this sample: the novel-instance benchmarks FrontierMath T4, AIME 2025 and Bulls-and-Cows all saturated in 14 months or less.
- **Novel skills** (task families absent from training) predict a *slower start*: ARC-AGI-1 took about 4 years to go from 0% to 5%. They offer no protection once the family becomes a training or harness target. Examples:
  - ARC-AGI-1's public training set was used for o3-preview.
  - ARC-AGI-3 was beaten through harness engineering.
- The strongest predictor of a *failed* (unused) benchmark in the user's list is infrastructure: missing code, no leaderboard, frontier models excluded, pre-emption. Both novelty dimensions have no predictive value there.

### Gaps
- The sample is not random; it is weighted towards notable failures.
- No systematic dataset links "novelty" labels to lifetime. Akhtar et al. coded 14 properties, but "novel skill" was not among them (inference from their abstract).

---

## 5. Refined hypothesis

### Takeaway
**Refined statement:** *A benchmark stops discriminating when the cheapest way to raise its score no longer runs through the capability it names, and nobody renews it.* Items the model was trained on (contamination) are one such cheap path. There are five others:
1. **Trainable task families.** Verifiable, procedurally generatable tasks become RL curricula.
2. **Search, tools or compute.** Brute force, test-time training, harnesses.
3. **Artifacts and broken graders.** Answer-only cues, do-nothing passes, wrong keys.
4. **Selective submission.** Private variants, best-of-N.
5. **Adoption failure.** The benchmark is never run on frontier models, so it never discriminates for anyone.

Novel instances close path 0 (contamination). Novel skills close paths 0 and 1 only until the skill becomes a training or harness target.

### Cited Findings
- **Path 1 (trainable family):**
  - Reasoning Gym provides 100+ generators "for reinforcement learning with verifiable rewards" [Reasoning Gym](https://arxiv.org/abs/2505.24760) (M).
  - Logic-RL reached 0.99–0.89 on 3–7-person Knights and Knaves from fewer than 5,000 samples and generalised to 8-person puzzles [Logic-RL](https://arxiv.org/abs/2502.14768) (M).
  - Bulls-and-Cows was saturated in about 9.5 weeks [commits](https://github.com/stalkermustang/llm-bulls-and-cows-benchmark/commits/main) (H).
- **Path 2 (search, tools, harness):**
  - A 2020 brute-force ensemble solved 49% of ARC-AGI-1 [ARC Prize 2024](https://arxiv.org/abs/2412.04604) (M-H).
  - Mastermind's hypothesis spaces are at most 1,296 codes [lm-eval](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mastermind) (H).
  - ARC-AGI-3 moved from 62.7% to 99.9% through the harness alone [ARC Prize](https://arcprize.org/blog/astra) (M).
  - LLM Chess: reasoning models "saturated random-based evaluations", so the maintainers added the Komodo Dragon engine [LLM Chess](https://github.com/maxim-saplin/llm_chess) (H).
- **Path 3 (artifacts and graders):** HellaSwag (>65% of predictions unchanged); τ-bench (38%); SWE-bench Verified (59.4%); FrontierMath (42%); HLE (29%). See §3.
- **Path 4 (selection):** 27 Llama 4 variants on Arena, and gains of up to 112% from Arena data [Leaderboard Illusion](https://arxiv.org/abs/2504.20879) (H).
- **Path 5 (adoption):**
  - TopoBench's repo is empty; Game Reasoning Arena went quiet after 5 weeks; grid games froze in Jul 2024 (§3.3, H).
  - HELM froze [HELM](https://github.com/stanford-crfm/helm/blob/main/docs/maintenance_mode.md) (H).
  - BIG-bench was archived [GitHub](https://github.com/google/BIG-bench) (H).
- **Counterevidence to "novelty is irrelevant":**
  - Replacing saturated tasks with *novel* ones restores headroom: BBEH, where the best model scored 44.8% against BBH's >90% [BBEH](https://arxiv.org/abs/2502.19187) (M).
  - TTT-Bench's novel TTT-style games leave reasoning models 41% below their MATH-500 scores [TTT-Bench](https://arxiv.org/abs/2506.10209) (M-H).
  - MathArena's fresh contests exposed AIME 2024 inflation [MathArena](https://arxiv.org/abs/2505.23281) (H-M).
  - So novelty works as a **renewal mechanism and a contamination audit**, not as a permanent moat.

### Inferences
- **What successful long-lived instruments share** (ARC across versions, MathArena, FrontierMath's tier ladder, LLM Chess, clembench):
  - a **maintainer who renews items or difficulty on a cadence**;
  - **a stable brand across versions**;
  - **verified labels**;
  - **a declared tool and harness policy**.

  The novelty they have is *renewed* novelty, not one-off novelty.
- **Predictions from the refined hypothesis** [speculation, but testable]:
  1. Any benchmark whose instances are procedurally generated **and** automatically verified will saturate faster than a comparably hard static one, because it doubles as an RL environment. Unless its difficulty knob scales faster than training, expect under 12 months.
  2. Benchmarks graded on real-world end states with private splits and neutral runners (AutomationBench) will be adopted faster than novel-reasoning games, but will also climb fast.
  3. The design target for a new benchmark or game should be: an **unbounded difficulty knob**, a **declared tool policy**, **redundantly verified labels**, a **sealed evaluation with submission logging**, a **refresh cadence with a named owner**, and a **distribution channel** (harness plus leaderboard plus lab tables).

### Gaps
- No study directly measures whether RLVR availability shortens benchmark life. Prediction 1 is untested.

---

## 6. Claims table

| # | Claim | Value | Date | Source URL | Primary/secondary | Conf. |
|---|---|---|---|---|---|---|
| 1 | AutomationBench best frontier score at launch | <10% | Apr 2026 | https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/21/automationbench.md (abstract of arXiv 2604.18934) | Primary (mirror) | H |
| 2 | AutomationBench public set | 600 tasks (6×100), 47 simulated tools, private harder leaderboard split | 2026 | https://github.com/zapier/AutomationBench | Primary | H |
| 3 | AutomationBench Zapier-run scores | GPT-6 Astra 41.4; Opus 5.5 40.0; Fable 5.1 31.4; GPT-5.6 Sol 28.8; Opus 5 26.9 | 22 Sep 2026 | https://www.anthropic.com/news/claude-opus-5-5 | Primary | H |
| 4 | AutomationBench README leaderboard (conflicts with #3) | Opus 5 50.3; Kimi K3 46.67; Fable 5 46.17 | Sep 2026 | https://github.com/zapier/AutomationBench | Primary | M (conflict) |
| 5 | AutomationBench-AA split | 657 private tasks, v1.0.6 | Sep 2026 | https://github.com/fstandhartinger/model-market-comparison (AA page capture) | Secondary | M |
| 6 | OfficeBench results | GPT-4o 47.00%; Llama 3 70B 27.33%; 300 tasks (93/95/112) | Jul 2024 | https://github.com/zlwang-cs/OfficeBench | Primary | H |
| 7 | OfficeBench human | 93.33% | Jul 2024 | https://arxiv.org/abs/2407.19056 | Primary (search summary) | M |
| 8 | DCA-Bench | 221 cases, 8 platforms; ~30% issues found without hints | 2024–25 | https://arxiv.org/abs/2406.07275 ; https://github.com/TRAIS-Lab/dca-bench | Primary | M-H |
| 9 | SWE-bench Verified audit | ≥59.4% of audited (27.6% subset) flawed; all tested frontier models reproduced gold patches or problem specifics | 23 Feb 2026 | https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ (mirror: github.com/BobYeger/state-of-agents) | Primary (mirror) | H |
| 10 | SWE-Bench Illusion | File-path ID up to 76% vs up to 53% | Jun 2025 | https://arxiv.org/abs/2506.12286 | Primary (mirror) | H |
| 11 | τ-bench do-nothing agent | 38%; spamming agent 40% | 2025 | https://github.com/uiuc-kang-lab/agentic-benchmarks | Primary | H |
| 12 | ABC misestimation | Up to 100% relative; CVE-Bench −33% | 2025 | https://arxiv.org/abs/2507.02825 | Secondary quote | M |
| 13 | AIME 2024 contamination | +10–20 pts vs AIME-2025 expectation; QwQ ~60 | May 2025 | https://arxiv.org/abs/2505.23281 | Primary (search summary) | M-H |
| 14 | Final-answer contests saturated | "in just one year" | 2026 | https://arxiv.org/abs/2605.00674 ; https://matharena.ai/no_final_answer/ | Primary (search summary) | M |
| 15 | FrontierMath T4 | 5% → 98% in <14 months; saturated | Jul 2025 → Sep 2026 | https://x.com/EpochAIResearch/status/2098103831502708864 | Primary (via search) | M |
| 16 | FrontierMath v2 | Errors in 42% of problems; ~+12 pts on corrected set; 338 problems | 12 Jun 2026 | https://epoch.ai/benchmarks/frontiermath-tier-4-v2 | Primary (search summary) | M |
| 17 | GSM1k | Drops up to 13% (Phi, Mistral); r² = 0.36 | May 2024 | https://arxiv.org/abs/2405.00332 | Primary (search summary) | H |
| 18 | HLE bio/chem errors | 29 ± 3.7%; HLE team ~18% on subset | Jul 2025 | https://www.futurehouse.org/research/hle-exam | Primary (search summary) | M-H |
| 19 | HLE progress | +30 pts in one year; 46.44% top (16 Aug 2026) | 2026 | https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf | Primary (search summary) | M |
| 20 | MMLU errors | 6.49%; Virology 57% | 2024 | https://arxiv.org/abs/2406.04127 | Primary (search summary) | H |
| 21 | HellaSwag shortcut | >65% of predictions unchanged with Lorem ipsum | Apr 2025 | https://arxiv.org/abs/2504.07825 | Primary (mirror) | H |
| 22 | BBH saturated; BBEH top | >90% on BBH; o3-mini-high 44.8% on BBEH | Feb 2025 | https://arxiv.org/abs/2502.19187 | Primary (search summary) | M |
| 23 | MMMU-Pro drop | −16.8% to −26.9% vs MMMU | 2024 | https://github.com/MMMU-Benchmark/MMMU | Primary | H |
| 24 | GPQA Diamond | ~39% → 94.3%; logistic asymptote ~92% | 2023 → 2026 | https://epoch.ai/gradient-updates/gpqa-diamond-whats-left | Secondary (search summary) | M |
| 25 | ARC-AGI-1 early progress | 0% (GPT-3, 2020) → 5% (GPT-4o, 2024) | Dec 2024 | https://arcprize.org/blog/oai-o3-pub-breakthrough (quoted in github.com/smol-ai/ainews-web-2025) | Primary (quoted) | H |
| 26 | ARC-AGI-1 brute-force ensemble | 49% of private set (2020 entries); top single 20% | Dec 2024 | https://arxiv.org/abs/2412.04604 | Primary (search summary) | M-H |
| 27 | ARC Prize 2024 TTT | ARChitects 53.5%; MindsAI 55.5% | Dec 2024 | https://arxiv.org/abs/2412.04604 | Primary (search summary) | M-H |
| 28 | o3-preview ARC-AGI-1 | 75.7% ($10k limit); 87.5% (~172×) | 20 Dec 2024 | https://arcprize.org/blog/oai-o3-pub-breakthrough | Primary (not re-fetched) | M |
| 29 | ARC-AGI-3 harness gap | 62.7% standard vs 99.9% provider adapter (GPT-6 Astra) | ~3 Sep 2026 | https://arcprize.org/blog/astra ; https://www.techmeme.com/260903/p40 | Primary (search summary) | M |
| 30 | Leaderboard Illusion | 27 Meta variants; 19.2% / 20.4% data share; up to 112% gain | Apr 2025 | https://arxiv.org/abs/2504.20879 | Primary (mirror) | H |
| 31 | LMArena on Meta | "interpretation of our policy did not match…" | 7 Apr 2025 | https://simonwillison.net/2025/Apr/8/lmaren/ | Secondary quoting primary | M-H |
| 32 | Saturation study | 60 benchmarks; ~half saturated; age and scale predict; private sets no protective effect | 2026 (ICML) | https://arxiv.org/abs/2602.16763 | Primary (search summary) | H |
| 33 | AI Index 2025 one-year gains | MMMU +18.8, GPQA +48.9, SWE-bench +67.3 pts | Apr 2025 | https://www.ibm.com/think/news/stanford-hai-2025-ai-index-report | Secondary | M |
| 34 | AI Index 2026 | "saturated in months"; ~half of 60 most-cited saturated | Apr 2026 | https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf | Primary (search summary) | M |
| 35 | Bulls-and-Cows saturation | Commit "o3-mini saturated the benchmark...." | 31 Jan 2025 | https://github.com/stalkermustang/llm-bulls-and-cows-benchmark/commits/main | Primary | H |
| 36 | Logic-RL | 0.99 → 0.89 accuracy (3–7 persons), <5k synthetic samples | Feb 2025 | https://arxiv.org/abs/2502.14768 | Primary (search summary) | M |
| 37 | TTT-Bench | Reasoning models 41% below MATH-500; 5% below AIME 2024 | 2025 | https://arxiv.org/abs/2506.10209 | Primary (search summary) | M-H |
| 38 | LLM Chess | Random-opponent tier saturated in 2025; Dragon engine added | 2025–26 | https://github.com/maxim-saplin/llm_chess | Primary | H |
| 39 | Qi Town motivation | Built to compensate for "data dependency" of Q&A benchmarks | Aug 2025 | https://arxiv.org/abs/2508.04720 (mirror: CSQianDong/Awesome-arXiv-Daily-Reporter) | Primary (mirror) | H |
| 40 | Game Reasoning Arena | Last commit 11 Sep 2025 | 2025 | https://github.com/SLAMPAI/game_reasoning_arena/commits/main | Primary | H |
| 41 | MastermindEval in lm-eval | 6 tasks (2/4, 3/5, 4/6); Knuth pre-play | 2025 | https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mastermind | Primary | H |
| 42 | Concept | Humans >90%; no model >40% | Oct 2025 / ACL 2026 | https://aclanthology.org/2026.findings-acl.1219/ | Primary (mirror) | H |
| 43 | Boardwalk | 12 games; best 55.6% error-free | Aug 2025 | https://arxiv.org/abs/2508.16447 | Primary (mirror) | H |
| 44 | Grid games leaderboard frozen | Last model 19 Jul 2024; last commit 14 Dec 2024; 2,310 matches | 2024 | https://github.com/research-outcome/LLM-Game-Benchmark/commits/main | Primary | H |
| 45 | TopoBench | <25% of hard solved; code repo empty | Mar 2026 / Sep 2026 | https://arxiv.org/abs/2603.12133 ; https://github.com/mayug/topobench-benchmark | Primary | H |
| 46 | Raw-corpora pipeline | "avoids benchmark contamination" | 2025–26 | https://arxiv.org/abs/2506.07658 | Primary (mirror) | H |
| 47 | BloomQA | Analyze > Remember inversion | Jan 2026 | https://arxiv.org/abs/2601.20253 | Primary (mirror) | H |
| 48 | BIG-bench archived | 17 Apr 2026; >200 tasks | 2026 | https://github.com/google/BIG-bench | Primary | H |
| 49 | HELM maintenance mode | From 1 Jun 2026; no new evaluations | 2026 | https://github.com/stanford-crfm/helm/blob/main/docs/maintenance_mode.md | Primary | H |
| 50 | WebArena launch gap | GPT-4 agent 14.41% vs human 78.24% | 2023 | https://arxiv.org/abs/2307.13854 | Primary (search summary) | H |
| 51 | OdysseyBench+ reuses OfficeBench | 300 tasks turned into multi-day dialogues | Aug 2025 | https://arxiv.org/abs/2508.09124 | Primary (search summary) | M |

---

## 7. Sources

**Step 1 referents**
- Zapier AutomationBench: https://github.com/zapier/AutomationBench ; https://arxiv.org/abs/2604.18934 ; abstract mirror https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/21/automationbench.md ; https://artificialanalysis.ai/articles/announcing-zapier-automationbench-aa
- Anthropic, Claude Opus 5.5 (22 Sep 2026): https://www.anthropic.com/news/claude-opus-5-5
- OfficeBench: https://arxiv.org/abs/2407.19056 ; https://github.com/zlwang-cs/OfficeBench
- OdysseyBench: https://arxiv.org/abs/2508.09124
- DCA-Bench: https://arxiv.org/abs/2406.07275 ; https://github.com/TRAIS-Lab/dca-bench ; https://dl.acm.org/doi/10.1145/3711896.3737422
- DC-BENCH: https://proceedings.neurips.cc/paper_files/paper/2022/file/052e22cfdd344c79634f7ec76fa03e22-Paper-Datasets_and_Benchmarks.pdf

**Contamination, validity and gaming**
- OpenAI, "Why we no longer evaluate SWE-bench Verified": https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ (verbatim mirror: https://github.com/BobYeger/state-of-agents/blob/main/raw/articles/openai-retires-swe-bench-verified.md)
- SWE-Bench Illusion: https://arxiv.org/abs/2506.12286
- Agentic Benchmark Checklist: https://arxiv.org/abs/2507.02825 ; https://github.com/uiuc-kang-lab/agentic-benchmarks
- GSM1k: https://arxiv.org/abs/2405.00332 ; https://labs.scale.com/papers/llm-performance-grade-school-arithmetic
- MMLU-Redux: https://arxiv.org/abs/2406.04127
- What the HellaSwag?: https://arxiv.org/abs/2504.07825
- MMMU-Pro: https://arxiv.org/abs/2409.02813 ; https://github.com/MMMU-Benchmark/MMMU
- EvoEval: https://arxiv.org/abs/2403.19114 ; LiveCodeBench: https://arxiv.org/abs/2403.07974
- The Leaderboard Illusion: https://arxiv.org/abs/2504.20879 ; https://www.theregister.com/2025/04/08/meta_llama4_cheating/ ; https://simonwillison.net/2025/Apr/8/lmaren/
- FutureHouse on HLE: https://www.futurehouse.org/research/hle-exam ; HLE-Verified: https://arxiv.org/abs/2602.13964 ; HLE (Nature): https://www.nature.com/articles/s41586-025-09962-4

**Saturation and lifetimes**
- Akhtar et al., "When AI Benchmarks Plateau": https://arxiv.org/abs/2602.16763 ; https://icml.cc/virtual/2026/poster/63311 ; https://github.com/evaleval/benchmark-saturation
- AI Index 2025 (IBM summary): https://www.ibm.com/think/news/stanford-hai-2025-ai-index-report ; AI Index 2026 ch. 2: https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf
- MathArena: https://arxiv.org/abs/2505.23281 ; https://arxiv.org/abs/2605.00674 ; https://matharena.ai/no_final_answer/
- FrontierMath: https://x.com/EpochAIResearch/status/2098103831502708864 ; https://alphasignal.ai/news/openai-s-gpt-6-astra-cracks-epoch-s-hardest-math-benchmark-in-14-months ; https://epoch.ai/benchmarks/frontiermath-tier-4-v2 ; https://x.com/EpochAIResearch/status/2065488154086568445 ; https://x.com/EpochAIResearch/status/2053995435870892048 ; https://www.digitalapplied.com/blog/epoch-frontiermath-v2-error-corrected-ai-benchmark-analysis ; https://epoch.ai/latest/openai-and-frontiermath ; label-error compendium https://github.com/benchflow-ai/awesome-evals
- GPQA Diamond: https://epoch.ai/gradient-updates/gpqa-diamond-whats-left ; https://epoch.ai/benchmarks/gpqa-diamond
- BBEH: https://arxiv.org/abs/2502.19187
- MATH: https://arxiv.org/abs/2103.03874
- WebArena: https://arxiv.org/abs/2307.13854 ; https://leaderboard.steel.dev/leaderboards/webarena/
- MMMU (aggregator): https://benchmarkingagents.com/mmmu-benchmark/

**Novel-skill and procedural counterexamples**
- ARC Prize 2024 report: https://arxiv.org/abs/2412.04604 ; o3 post: https://arcprize.org/blog/oai-o3-pub-breakthrough (quoted in https://github.com/smol-ai/ainews-web-2025) ; ARC-AGI-2: https://arxiv.org/abs/2505.11831 ; ARC-AGI-3 Astra: https://arcprize.org/blog/astra ; https://www.techmeme.com/260903/p40
- Reasoning Gym: https://arxiv.org/abs/2505.24760 ; Logic-RL: https://arxiv.org/abs/2502.14768 ; TTT-Bench: https://arxiv.org/abs/2506.10209
- Bulls-and-Cows: https://github.com/stalkermustang/llm-bulls-and-cows-benchmark ; LLM Chess: https://github.com/maxim-saplin/llm_chess

**The user's list**
- Qi Town: https://arxiv.org/abs/2508.04720 (mirror https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/main/8-Aug-2025/AI/README.md)
- Game Reasoning Arena: https://arxiv.org/abs/2508.03368 ; https://github.com/SLAMPAI/game_reasoning_arena
- MastermindEval: https://arxiv.org/abs/2503.05891 ; https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mastermind
- Concept: https://aclanthology.org/2026.findings-acl.1219/ (mirror https://github.com/smallflyingpig/ai-conference-overview)
- Codenames: https://aclanthology.org/2025.gem-1.63/ ; https://github.com/clp-research/clembench/tree/main/codenames
- Boardwalk: https://arxiv.org/abs/2508.16447
- Grid games: https://arxiv.org/abs/2407.07796 ; https://github.com/research-outcome/LLM-Game-Benchmark
- TopoBench: https://arxiv.org/abs/2603.12133 ; https://github.com/mayug/topobench-benchmark
- Raw corpora: https://arxiv.org/abs/2506.07658 (mirror https://github.com/Luvata/arxive/blob/main/pages/2026-03-09-cs-cl.html)
- BloomQA: https://arxiv.org/abs/2601.20253 (mirror https://github.com/advanced-cs/arXiv_daily/blob/main/daily_papers/20260129_Thu/text.md)

**Infrastructure**
- BIG-bench (archived): https://github.com/google/BIG-bench ; HELM maintenance mode: https://github.com/stanford-crfm/helm/blob/main/docs/maintenance_mode.md

**Could not verify this session** (blocked hosts or exhausted search budget):
- the Llama 3 contamination table (HellaSwag, BBH, AGIEval gains);
- Ott et al. (2022) 3,765-benchmark statistics;
- GLUE/SuperGLUE saturation timings;
- MMLU-Pro top-model spread;
- LiveBench S-index value;
- the Kaggle Game Arena launch date (4 Aug 2025; carried over as M);
- GPQA paper baselines (65% experts, 34% non-experts);
- o1 MATH 94.8%;
- HumanEval 28.8% → 99.3%;
- the o3 FrontierMath 25% vs 10% comparison.
