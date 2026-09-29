# Gap dossier: do the survey's success and failure laws hold for the uncovered benchmark families?

Date: 2026-09-29. Scope: lifecycle fact sheets for two representative benchmarks in each of six families that the survey had not covered:
- instruction following;
- function and tool calling;
- honesty and safety;
- domain (medical, finance; legal and MedQA as one-line context);
- multilingual;
- multimodal.

Each family is then tested against five general claims from the briefs:
- **(a)** the benchmark lifecycle (Brief A, headlines 1-2);
- **(b)** LLM judges as a liability (Brief A F9; Brief B F5);
- **(c)** family learnability (Brief D T2);
- **(d)** adoption follows third-party runners and product alignment (Brief B, headline 1 and S1-S2);
- **(e)** academic leaderboards survive through maintenance (Brief C S2).

Conventions:
- **H**: primary source (a repo file, code, a commit, a model-card image read in this session), or two agreeing copies.
- **M**: a single mirror, a search-engine extract of a primary paper, or a consistent secondary source.
- **L**: unverified, or secondary aggregator only.
- **[C]**: a number I computed in this session from public data. The label after it rates the input data.
- **[I]**: my interpretation.
- **[D:MCA]**: a headline-table count from `notes/model_cards_adoption.md`. That sample has 34 releases from Dec 2024 to Sep 2026, and its counts are sample-specific.

Access notes. arXiv, OpenReview, ACL Anthology, Hugging Face, NeurIPS/PMLR proceedings, cdn.openai.com, alignmentforum/lesswrong, vals.ai and gorilla.cs.berkeley.edu were all blocked. Primary evidence therefore comes from GitHub clones:
- `ShishirPatil/gorilla`, including its `gh-pages` leaderboard data;
- `allenai/IFBench`, which ships the paper PDF;
- `openai/simple-evals`;
- `MMMU-Benchmark/MMMU`;
- `sylinrl/TruthfulQA` and `centerforaisafety/mask`;
- `alexander-turner/TurnTrout.com`, the source of the "Gaming TruthfulQA" post;
- `evaleval/benchmark-saturation` (Akhtar et al.'s annotation data);
- `UKGovernmentBEIS/inspect_evals` and `EleutherAI/lm-evaluation-harness`.

Anthropic's Fable 5 benchmark table image was fetched through anthropic.com's image proxy and read directly.

---

## Summary

- **Bottom line.** The survey's laws mostly generalise, but three of the five need rewording before they can be stated as general. The instruction-following, domain, honesty and multilingual families each contradict at least one brief claim as currently worded.

- **(a) Lifecycle: partially holds.** The launch → rapid gain → ceiling *shape* recurs in 9 of the 12 fact-sheet benchmarks. The exceptions are MASK (a propensity measure), StableToolBench (dormant before it saturated) and Global-MMLU (adopted once, with no arc). But the third stage is often not a *label-noise* ceiling. It is a family-specific validity ceiling:
  - IFEval: overfitting to 25 constraint templates.
  - StableToolBench: environment rot; 55.6% of ToolBench APIs were unstable (M).
  - TruthfulQA: answer-format shortcuts. A question-blind decision tree reaches 79.6% in theory and 66.6% in practice (H). The original generation metric also depended on a fine-tuned GPT-3 judge that the authors cannot share (H).
  - HealthBench: rubric and physician-disagreement ceilings (M).
  - MMMU: modality shortcuts. GeminiPro scores 42.9% on MMMU with no images (M).
  
  The "successor" stage is not guaranteed either. **Multilingual rows left frontier headline tables entirely** in 2026 without a successor: MMMLU's last appearance was April 2026, and Global-MMLU and MGSM each appear in one release [D:MCA] (H).

- **(b) LLM judges: contradicted descriptively, confirmed as a liability.**
  - LLM-rubric-graded benchmarks are routinely in headline tables: Finance Agent 8/34, MultiChallenge 5/34 and HealthBench 4/34, across OpenAI and Anthropic [D:MCA] (H).
  - Anthropic headlined OpenAI-built, rubric-graded **HealthBench Professional** in June 2026: Mythos 5 scored 66.0% against GPT-5.5's 51.8% [anthropic2026fable5] (H, table image).
  - The liabilities are visible, though. OpenAI silently changed the grader between versions: HealthBench uses `gpt-4.1-2025-04-14`, while HealthBench Professional mode requires a "GPT-5.4 low grader" plus a response-length penalty [openaiSimpleEvalsHBPro2026] (H).
  - Rubrics miss clinically relevant hallucinations, "often leaving scores unchanged" [farrow2026rubricsfail] (M).
  - Rewrite F9: judged scores are adoptable, but only as a versioned (rubric, grader, length-policy) triple with published meta-evaluation.

- **(c) Family learnability: confirmed, and sharpened.**
  - IFEval "quickly saturated, with many leading models scoring 80+% at as small as 2B parameters". Model builders generated targeted synthetic data "from the IFEval taxonomy", and on IFBench's 58 unseen constraints GPT-4.1, Claude 3.7 Sonnet, Qwen3-32B and Claude 4 Sonnet all score below 50% [pyatkin2025ifbench] (H).
  - The successor then went the same way. IFBench's authors released a 29-constraint RLVR curriculum that lifts Tülu-3-8B on IFBench from 28.9 to 45.9 (H). Artificial Analysis added IFBench to its index in August 2025 and removed it in June 2026 [aa2026method] (M-H).
  - The held-out-constraint defence bought roughly one year.

- **(d) Adoption: holds only in a refined form.**
  - Product alignment is the most consistent predictor. HealthBench fits Claude for Healthcare (January 2026) and ChatGPT for Clinicians; Finance Agent fits financial services; MCP Atlas and Toolathlon fit agent products.
  - A third-party runner is **not sufficient**. BFCL runs 108 model configurations (44 proprietary), is packaged on PyPI and implemented in Inspect Evals, yet appears in 0/34 headline tables [C, H].
  - A third-party runner is **not necessary** either. HealthBench is lab-built and lab-graded, and was adopted anyway.
  - Sponsorship beats validity: MMMLU (OpenAI) appears 14 times, while the better-validated, culturally annotated Global-MMLU appears once [D:MCA] (H).
  - Headline adoption is also audience-specific. BFCL *is* a headline metric for open-weight developers outside the sample: the Llama 3.1 and 3.3 cards and the Qwen3 technical report (H).

- **(e) Maintenance: necessary but not sufficient, and it decays.** BFCL is the test case.
  - It was maintained as intended: four versions (February 2024 → July 2025), a 168-entry changelog, 13 data checkpoints in 2025, and hundreds of ground-truth fixes (H).
  - Its maintenance then decayed. Leaderboard data has not changed since 16 December 2025, and there have been no commits since 23 March 2026. GPT-5.4/5.5, Claude Opus 4.6 and later, and Gemini 3.1 Pro are all missing [C, H].
  - Other academic cases add further endings: StableToolBench dormant since April 2025, the MASK repo frozen at launch, Toolathlon's declared "final version" (June 2026), and MMMU releasing its hidden test answers (February 2026) (H).

- **Additional contradiction: Brief A S1.** Benchmarks were adopted without launch headroom against a human anchor.
  - HealthBench Professional launched with the best system at 59.0 against a physician baseline of 43.7 (M).
  - MMMLU launched with o1 already at 87.7% (H).
  
  When product alignment is strong, headroom is not necessary for adoption.

---

## Findings

### 1. Instruction following: IFEval → IFBench (MultiChallenge as context)

| Field | IFEval | IFBench |
|---|---|---|
| Creator, date | Google (Zhou, Lu, Mishra, Brahma, Basu, Luan, Zhou, Hou); arXiv:2311.07911, 15 Nov 2023 [zhou2023ifeval; evaleval2026saturationdata] (H) | AI2 + UW (Pyatkin, Malik, Graf, Ivison, Huang, Dasigi, Lambert, Hajishirzi). Repo's first commit 10 Jun 2025; arXiv:2507.02833; NeurIPS 2025 D&B [pyatkin2025ifbench] (H) |
| Construct | "Verifiable instructions" such as "write in more than 400 words" [lm-eval README] (H) | *Generalisation* of precise instruction following to unseen, out-of-domain verifiable constraints (H) |
| Item source | 541 prompts (counted from `input_data.jsonl`) [C, H]. 25 constraint types (H). Prompts are LLM-generated with few-shot filtering (Akhtar annotation, quoting the paper) (H-data) | 58 new constraints, "created manually" with feedback from LM users, attached to held-out WildChat prompts. The constraint taxonomy is split into train and test "to prevent contamination". An optional two-turn "constraint isolation" setting is included (H) |
| Grader | Code: Python verifiers, reporting strict/loose accuracy at prompt and instruction level (H) | Code verifiers. The paper reports prompt-level loose accuracy (H) |
| Headroom, human anchor | GPT-4: 76.9% prompt-strict and 83.6% instruction-strict (M, search extract). Akhtar records "SOTA at release 83.57 (GPT-4)" (H-data). No human anchor | GPT-4.1, Claude 3.7 Sonnet, Qwen3-32B and Claude 4 Sonnet all score below 50%; o3 is the exception (H). No human anchor |
| Saturation timeline | Llama 3.3 70B: 92.1 (Dec 2024) [meta2024llama33card] (H). Akhtar's top 5: o3-mini 93.9, Claude 3.7 Sonnet 93.2, Nova Pro 92.1 (spread 3.5 points). Saturation index 0.82, "High" (H-data). The IFBench paper says IFEval "has quickly saturated, with many leading models scoring 80+% at as small as 2B parameters" (H) | Added to the Artificial Analysis Intelligence Index in v2.1 (Aug 2025). Removed in v4.1 (Jun 2026): "we continue to run it" [aa2026method, via aggregators_indices.md captured changelog] (M-H). By Sep 2026 the top AA IFBench scores are about 83% (Grok 4.3 at 83.3%) (L, search extract) |
| Contamination, shortcuts, label errors | Akhtar annotators tag it "Contamination": prompts and solutions have been public since 2023 (H-data; M interpretation). Models "strongly overfit" to the 25 templates; Nemotron-4 340B generated targeted IF data "combining synthetic instructions with constraints from the IFEval taxonomy" (quoted in the IFBench paper, H). No label-error audit was found this session | Over-optimisation under IF-RLVR: trained models "prioritize the constraint over the full instruction", and GPT-4.1-as-judge scores base-policy completions higher on the task itself (H) |
| Versions, successors | No official versions. Successors come from other groups (IFBench; Multi-IF; MultiChallenge covers multi-turn) (H/M) | Multi-turn variant; pip package (`ifbench`) that also ships the classic IFEval verifiers (H) |
| Maintainer, last update | google-research monorepo, not versioned (M) | AI2; last commit 9 Sep 2026 (H) |
| Distribution channel | lm-evaluation-harness task [gao2024harness]; Open LLM Leaderboard v2 (Jun 2024 to Mar 2025) [hf2024ollv2]; Inspect Evals [inspectevals] (H) | Artificial Analysis index, a third-party runner (H via dossier). Ai2 blog "Why Artificial Analysis uses Ai2's IFBench" [ai2025ifbenchAA] (L, title only) |
| Headline tables | 5/34 (A1, O2, D1, D2, K1). None in frontier tables after 2025H1 [D:MCA] (H). Outside the sample: Llama 3.3 card (H) | 1/34 (X2, only inside MiniMax's "Artificial Analysis" block) [D:MCA] (H) |

**Family learnability, directly observed (H).** From IFBench's own contributions list:
- "we improve the IFeval scores of a TÜLU-3-8B model from 82.4 to 92.2, and the IFBENCH scores from 28.9 to 45.9";
- "IF-RLVR increases a Qwen 2.5 7b base model to scores of 87.8 (IFEval) and 54.7 (IFBENCH)".

The authors also publish the training constraints ("IFTrain", 29 constraints), RLVR prompts and code in `allenai/open-instruct`. The benchmark ships with its own curriculum, the pattern Brief D T2 predicts [stojanovski2025reasoninggym].

**MultiChallenge (context only).**
- Scale AI; arXiv:2501.17399; Findings of ACL 2025 [sirdeshmukh2025multichallenge].
- Grader: "LLM as judge with instance-level rubrics", with up to 93% agreement with human raters. All frontier models scored below 50% at launch (M, search extracts).
- Headline tables: 5/34 (O2, O3, O5, K1, X1) [D:MCA] (H). This is a second LLM-judged instruction-following benchmark in headline tables.

### 2. Function and tool calling: BFCL and StableToolBench (MCP Atlas and Toolathlon as contrast)

| Field | BFCL (v1 → v4) | StableToolBench |
|---|---|---|
| Creator, date | UC Berkeley Gorilla team (Patil, Mao, Yan, Ji, Suresh, Stoica, Gonzalez). Leaderboard "is live" on 26 Feb 2024; paper at ICML 2025 [patil2025bfcl; gorillaBfclRepo] (H) | Tsinghua THUNLP-MT et al. (Guo, Cheng, Wang, Liang, Qin, Li, Liu, Sun, Liu); arXiv:2403.07714; Findings of ACL 2024 [guo2024stabletoolbench] (H) |
| Construct | Whether an LLM can "invoke functions": selecting and parameterising calls (simple, multiple, parallel), relevance and irrelevance detection, multi-turn state (v3), and agentic web search, memory and format sensitivity (v4) (H) | Multi-step tool use over ToolBench's large real-API environment (H) |
| Item source | v1: 2,000 question-function-answer pairs (1,680 Python, 100 Java, 50 JavaScript, 70 REST, 100 SQL) (H). v2 "Live": 2,251 pairs from "live, user-contributed function documentation and queries", from "large banks, tech-corporations, agent developers … hobbyists and enterprises", deduplicated and filtered (H). v3: 800 multi-turn entries (200 base + 600 augmented) (H). v4: web search 200, memory 465, format sensitivity 26 configurations × 200. Overall score: 5,088 entries (H) | ToolBench queries, filtered for solvability by majority vote of gpt-4-turbo, gemini-pro and claude-2 (H) |
| Grader | **Deterministic.** AST matching against possible answers (v1-v2), executable checks, and for multi-turn "state-based" plus "response-based" checks after every turn (v3) (H). The v4 web-search category calls a live search API (SerpAPI by default), so that part is not hermetic (H) | **LLM judge.** GPT-4 computes Solvable Pass Rate and Win Rate. In Jun 2024 the judge moved from `gpt-4-turbo-preview`, "which we found may produce unstable evaluations", to `gpt-4-turbo-2024-04-09` (H). The environment is also LLM-simulated: a cache plus GPT-4-turbo simulators for unavailable APIs, later "MirrorAPI", trained to mirror more than 7k APIs (H) |
| Headroom, human anchor | GPT-4 led at v1 launch (H). Top overall on v4 is 77.47% (Claude Opus 4.5 FC, Dec 2025 checkpoint) [C, H]. No human anchor | No human anchor. Launch rationale: the API status of 55.6% of ToolBench tools was "inconsistent" (M, search extract) |
| Saturation timeline | v4 changelog (17 Jul 2025): "As single-turn tasks approach saturation, weighting now favors complex, multi-step agentic tasks". Live and non-live weights cut from 33% to 10% each; agentic set at 40% (H). Top-10 non-live AST in the final data: 81.9-90.7%; multi-turn 33.9-68.4% [C, H] | Never saturated in public; it went dormant instead (see below) |
| Contamination, shortcuts, label errors | **Label churn.** A 16 Oct 2024 "bug fix in the dataset and possible answers" touched 104 Live Simple, 547 Live Multiple, 11 Live Parallel and 17 Live Parallel Multiple entries: 679 of the 1,351 scored live AST entries, about 50% [C, H]. An 11 Dec 2024 enum fix touched 256 more. At least 27 of 168 changelog entries concern dataset or ground-truth fixes (keyword count) [C, M]. **Harness sensitivity.** Opus 4.5 scores 77.47% (FC) against 33.47% (Prompt); GPT-5.2 scores 55.87% (FC, rank 16) against 45.27% (Prompt) [C, H]. The v4 blog reports "significant performance drops" for Claude models with XML return formats (H). The roadmap item "BFCL metrics to evaluate contamination" is still unchecked (H) | Environment decay was the failure mode. Stability is bought with LLM simulation, which trades realism and adds a second LLM dependency (H; [I]) |
| Versions, successors | v1 (Feb 2024) → v2 Live (20 Aug 2024) → v3 Multi-Turn (21 Sep 2024) → v4 Agentic (17 Jul 2025) (H). In frontier tables the successors are *other groups'* benchmarks: MCP Atlas (Scale), Toolathlon (HKUST) and τ²-bench (Sierra) [D:MCA] | MirrorAPI update (2025) (H) |
| Maintainer, last update | 108 model rows, 44 proprietary. Data checkpoints roughly monthly Jan-Apr 2025, then Jun, Aug, Nov and 16 Dec 2025. **Data unchanged since 16 Dec 2025.** On 12 Apr 2026 a commit only bumped the "Last Updated" string. Last code commit 23 Mar 2026. BFCL commits per month fell from 29 (Jun 2025) to 1-5 (Jan-Mar 2026), then zero [C, H] | Last commit 15 Apr 2025 (H) |
| Distribution channel | Own leaderboard, with model handlers contributed by model builders. `bfcl-eval` on PyPI; Inspect Evals implementation (H). Open-weight reports source baselines from it: Qwen3, "Some baselines are derived from the BFCL leaderboard" [qwen2025qwen3] (H) | GitHub, a public virtual-API server and Docker image (H). No Inspect Evals implementation (checked) (H) |
| Headline tables | 0/34 [D:MCA] (H). Outside the sample: Llama 3.1 card (BFCL), Llama 3.3 card (BFCL v2: 77.3 for 70B), Qwen3 technical report (BFCL v3: 70.8 for the flagship) [meta2024llama31card; meta2024llama33card; qwen2025qwen3] (H). OpenAI's GPT-4.1 table used ComplexFuncBench instead [D:MCA] | 0/34 [D:MCA] (H) |

**Why BFCL is absent from frontier headline tables while MCP Atlas (9), Toolathlon (4) and τ²-bench (19) appear.** These are evidence-backed candidate causes, not a proven decomposition:
1. **Construct currency.** BFCL's scored weight moved to agentic tasks only in July 2025 (H). By then MCP Atlas ("multi-step workflows using MCP") and Toolathlon (600+ tools in real software environments, long-horizon, task-specific evaluators) matched the agent products labs were selling (H; [I], cf. Brief B S2).
2. **Saturation of the scored core.** Single-turn AST tops out at about 82-91% [C, H], so it separates frontier models poorly.
3. **Harness-dominated rankings.** Format choice alone moves a frontier model by 44 points, and OpenAI's flagship ranks 16th [C, H]. A lab has little incentive to headline a board whose rank reflects handler and format choices (Brief B F4, F7; [I]).
4. **Coverage lag.** No GPT-5.4/5.5, Claude Opus 4.6 or later, or Gemini 3.1 Pro rows exist [C, H]. The board cannot serve as the "citable source for competitor numbers" that Brief B S1 requires.
5. **Audience.** 64 of 108 rows are non-proprietary, and many are specialised tool-calling fine-tunes such as xLAM, Hammer and watt-tool (H). BFCL functions as the open-weight community's standard, and Meta and Qwen headlined it (H).

The runner contrast:
- MCP Atlas numbers are reported as "results from Scale AI" [D:MCA] (M).
- Toolathlon offers a hosted public evaluation service (Nov 2025) and released "Toolathlon-Verified", "the verified final version", on 30 Jun 2026 [li2025toolathlon] (H).

Citation counts for BFCL could not be verified: Semantic Scholar is blocked. The paper calls itself "the defacto standard for evaluating function-calls" (M, search extract).

### 3. Honesty and safety: TruthfulQA and MASK

| Field | TruthfulQA | MASK |
|---|---|---|
| Creator, date | Lin, Hilton, Evans; Sep 2021; ACL 2022 [lin2022truthfulqa] (H) | CAIS + Scale AI (Ren, Agarwal, Mazeika, … Yue, Hendrycks); arXiv:2503.03750, Mar 2025 [ren2025mask] (H) |
| Construct | Avoiding imitative falsehoods and misconceptions (H) | Honesty as consistency between a model's elicited beliefs and its statements under pressure to lie, "disentangled from accuracy" (H) |
| Item source | 817 author-written questions in 38 categories (H) | About 1,000 public questions (M). Multiple "archetypes", such as binary and statistics (H) |
| Grader | The generation metric is a fine-tuned GPT-3 "GPT-judge"/"GPT-info" (about 90-95% validation accuracy against humans). The authors "are not currently able to provide external access to the fine-tuned models" (H). MC1 and MC2 use log-probability scoring (H) | LLM judges: `o3-mini` and `gpt-4o` in `evaluate.py` (H) |
| Headroom, human anchor | Best model 58% against a human 94% (H) | Launch-era dishonesty rates: P(lie) 33.4% for Claude 3.5 Sonnet and 26.6% for Claude 3.7 Sonnet (M). "Scaling pre-training does not improve model honesty" (H) |
| Saturation timeline | MC1 SOTA 80.8% by 21 Nov 2024 (Turner's table, H). On the Jan 2025 binary version, Akhtar's top 5 are Claude 3.5 91.1, GPT-4o 88.5, Grok 2 87.2 and Llama 3.3 70B 84.4, sourced from the authors' post. Saturation index 0.55 ("Moderate"); "Recent models evaluated: No" (H-data) | xAI model cards report MASK dishonesty of 0.43% (Grok 4), 0.49%/0.46% (Grok 4.1) and 1.90% "MASK-Rectified" (Grok 4.6) (L-M, search extracts of xAI PDFs). This is suggestive of a floor, but conditions such as system prompts are unverified |
| Contamination, shortcuts, label errors | **Shortcut.** On 256 analysed MC1 questions: "always selecting the odd answer out" scores 73%; a decision tree scores 79.6% in theory and 66.6% as implemented, with Gemini never seeing the question; only 37/256 (14.5%) are immune to both tricks [turner2025gamingtruthfulqa] (H, author's source). The author flags 79.6% as "possibly … a slight overestimate". **Counterpoint.** The TruthfulQA authors found LLMs "probably not exploiting these shortcuts when zero-shot prompted" and that binary scores "correlate tightly" with the original MC (H). **Label churn.** Jan 2025 dropped invalid questions (for example, browsing) and removed the "Indexical Error: Time" category, but "we have not completed a full validation of the remaining questions" (H). **Capability confound.** MC1 correlates 0.812 with a capabilities score [ren2024safetywashing] (H, quoted) | Honesty is g-negative: Spearman ρ with compute −0.599, while accuracy is +0.873 [ren2025mask via gap_offg_construct_evidence.md] (M) |
| Versions, successors | v0 (2021) → Oct 2021 (about 300 extra reference answers) → Jan 2025 binary MC [truthfulqa2025newmc; truthfulqaReadme] (H) | None; xAI's "MASK-Rectified" variant (L) |
| Maintainer, last update | Repo last commit 15 Jan 2025 (H) | Repo last commit 6 Mar 2025, i.e. frozen at launch (H) |
| Distribution channel | Open LLM Leaderboard v1 (to Jun 2024) [hf_openllm_archive]; lm-eval-harness; Inspect Evals (H) | HF dataset; Inspect Evals (H) |
| Headline tables | 0/34 [D:MCA] (H) | 0/34 [D:MCA] (H). Appears in model-card safety sections (xAI) (M) |

**Link to safetywashing.** The two benchmarks bracket the problem:
- TruthfulQA's multiple-choice score is largely a capability proxy: r = 0.812 [ren2024safetywashing]. On top of that it is shortcut-exposed.
- MASK was built to separate the propensity (honesty) from the capability (accuracy), and the separation holds (−0.60 against +0.87) (M).
- The survey's adoption laws do not describe safety benchmarks well, because these are published through a different channel: system and model cards, not launch headline tables. Brief B's headline-table outcome measure scores every safety benchmark as a "failure" [I].
- Sycophancy measures are similarly anti-correlated with capability in the Safetywashing data (−0.66/−0.67) [ren2024safetywashing via gap_offg_construct_evidence.md] (H [C]). Inspect Evals ships a `sycophancy` task (H).

### 4. Domain: HealthBench → HealthBench Professional, and Vals Finance Agent

| Field | HealthBench (May 2025) → HealthBench Professional (Apr 2026) | Finance Agent (Vals AI) v1 → v1.1 → v2 |
|---|---|---|
| Creator, date | OpenAI (first author Arora per the lead; the author list was not verified this session); code merged into `simple-evals` on 12 May 2025 [arora2025healthbench] (H for the date, M for the authors). HealthBench Professional: arXiv:2604.27470; `simple-evals` options added 22 Apr 2026 [openai2026healthbenchpro; openaiSimpleEvalsHBPro2026] (H) | Vals AI with Stanford (Bigeard, Krishnan, Wu, Nashold); arXiv:2508.00828, 2025 [bigeard2025financeagent] (M). v2 released May 2026 [valsFabV2] (M) |
| Construct | Open-ended health conversations across contexts (emergencies, global health, data transformation) and behaviour dimensions (M). HB-Pro: clinician tasks (care consult, writing and documentation, medical research) (M) | Agentic financial-analyst research over recent SEC filings (M) |
| Item source | 5,000 conversations; 48,562 rubric criteria written by 262 physicians from 60 countries (M, search extracts of the paper and launch page). Hard and Consensus subsets exist (H, code). Physicians were shown "reference completions … from Apr 2025 models (o3, gpt-4.1)" (H, code metadata). HB-Pro: 525 tasks from real clinician chats, with rubric items written and adjudicated by three or more physicians over three rounds (M) | 537 expert-authored questions in a nine-category taxonomy built with bank, hedge-fund and PE experts. Filings are from after 2024, "to prevent … pre-training memorization" (M) |
| Grader | **LLM rubric.** `gpt-4.1-2025-04-14` grades each criterion (H). Reported meta-evaluation: grader-physician macro F1 ≈ 0.71, "comparable to" physician-physician agreement (M). **HB-Pro mode requires "GPT-5.4 low grader, and length adjustment"**, a score penalty per 500 response characters (H, code) | **LLM rubric.** LLM-as-judge per key point from the expert answers, plus a "contradiction rubric" (M) |
| Headroom, human anchor | HealthBench: GPT-3.5 Turbo 0.16 to o3 0.60; HealthBench Hard: o3 0.32 (M). **HB-Pro launched with models above the human anchor**: physician-written responses 43.7, GPT-5.4 base 48.1, "GPT-5.4 in ChatGPT for Clinicians" 59.0 (M) | Best model 46.8% (class-balanced); no model above 50% (M). No human anchor found |
| Saturation timeline | HealthBench Hard: o3 31.6% → GPT-5 46.2% (Aug 2025) (M). HB-Pro (Anthropic table, Jun 2026): Mythos 5/Fable 5 66.0%\*, Mythos Preview 64.7%, Opus 4.8 56.9%, GPT-5.5 51.8% [anthropic2026fable5] (H) | Sonnet 4.5 55.3% (v1, Sep 2025) → Opus 4.7 64.4% (v1.1) → **v2 resets**: Opus 4.8 53.9%, Gemini 3.5 Flash 57.9% [D:MCA] (H). GPT-5.5 about 52% on v2 (L, secondary) |
| Contamination, shortcuts, label errors | **Disagreement ceiling.** 81.8% of physician-disagreement variance is at case level; rubric identity explains 15.8% of met/not-met variance but 3.6-6.9% of disagreement; physician identity 2.4% [borgohain2026disagreement] (M; repo exists, H). **Rubric blind spots.** Clinically relevant hallucinations "are missed by rubrics, often leaving scores unchanged" across HealthBench, HB-Pro and LiveMedBench [farrow2026rubricsfail] (M; project page H). **Length gaming.** HB-Pro's built-in length adjustment implies verbosity was rewarded (H for the mechanism; [I] for the motive) | v2 adds a held-out private split "to limit contamination". Scores fell about 14 points on average against v1.1 (L-M, secondary summary of Vals) |
| Versions, successors | HealthBench (main/Hard/Consensus) → HB-Pro. Same brand, **different grader** (H) | v1 → v1.1 → v2, a versioned brand (H) |
| Maintainer, last update | OpenAI. `simple-evals` keeps HealthBench as a maintained reference implementation after the Jul 2025 freeze; last commit 22 Apr 2026 [openai2025simpleevals] (H) | Vals AI, a commercial evaluator; leaderboard at vals.ai (M) |
| Distribution channel | Lab sponsor, open reference implementation, Inspect Evals implementation (H). **Product alignment**: HB-Pro built on ChatGPT for Clinicians conversations (M); Anthropic launched "Claude for Healthcare" on 11 Jan 2026 [claudeHealthcare2026] (M) | Third-party runner (Vals) and vendor-domain alignment with financial-services products [I] |
| Headline tables | 4/34 (O4, O5; A10b, A11) [D:MCA] (H). The A10b row was read from the table image this session (H). OpenAI stopped headlining it after GPT-5 (O6-O9 lack it) [D:MCA] | 8/34 (A4, A7-A10, O8, O9, G4) [D:MCA] (H) |

**Context (one line each, no fact sheet).**
- **MedQA.**
  - Top 5 in Akhtar's data: o1 96.52, GPT-5.1 96.38, GPT-5 96.32 (spread 0.46). Saturation index 0.99, "Very high". Launch SOTA: BioBERT-large 36.7 (H-data).
  - The Med-Gemini team relabelled the test set with at least 3 primary-care physicians per question after finding "label errors or … missing information" [saab2024medgemini] (H, repo README).
- **LegalBench.**
  - 162 tasks "gathered from 40 contributors" via legal-community crowdsourcing [guha2023legalbench] (H).
  - Akhtar's top 5: GPT-5 84.5, Gemini 2.5 Pro 83.6, Grok 4 83.4 (spread 1.7). Saturation index 0.72 "High" (H-data).
  - Still maintained (commit 29 Mar 2026) (H). 0/34 headline tables (H).
- **Legal Agent Benchmark.** It appears in Anthropic's A10b table (Fable 5 13.3%, Opus 4.8 10.4%, GPT-5.5 2.1%, Gemini 3.1 Pro 0.0%) (H, image) and in A11. It is therefore a 2-release family in the dossier's own lists, not a single-release family as the task brief states. Its creator was not verified.

### 5. Multilingual: MMMLU and Global-MMLU (MGSM as context)

| Field | MMMLU (OpenAI) | Global-MMLU (Cohere For AI et al.) |
|---|---|---|
| Creator, date | OpenAI; 13 Sep 2024 (Akhtar) [openai2024mmmlu] (H-data) | Singh, Romanou, Fourrier, Adelani, … (Cohere For AI and collaborators); 5 Dec 2024; ACL 2025 [singh2024globalmmlu] (H) |
| Construct | MMLU knowledge in 14 non-English languages (H) | Multilingual MMLU with *cultural-sensitivity* annotation (H) |
| Item source | MMLU test set translated "using professional human translators", including low-resource Yoruba and Swahili (H) | 42 languages. Machine translation plus professional translations and community post-edits. Culturally Sensitive/Agnostic (CS/CA) labels on 2,850 questions per language. A 15-language Lite version (H, lm-eval README) |
| Grader | Exact (multiple choice) (H) | Exact (H) |
| Headroom, human anchor | Little at release: o1 averaged 0.877, with Yoruba lowest at 0.754 (H). MMLU's expert anchor is inherited | The top models were already high: Gemini 2.5 Pro 94.8, Grok 4 91.1 (Akhtar top 5) (H-data) |
| Saturation timeline | o3-high 0.888 average (Apr 2025) (H). Headline plateau from Claude 3.7 Sonnet 86.1% to Gemini 3.1 Pro 92.6% [D:MCA] (H). **Tension**: Akhtar's saturation index calls MMMLU "Very low" (0.00004), because its top-5 snapshot mixes models from 81 to 89 (H-data) | Akhtar: "Very low" (spread 5.1) (H-data) |
| Contamination, shortcuts, label errors | Inherits MMLU's contamination and mislabelling, per Akhtar's annotators (M). Translation carries over Western-centric content (M, via Global-MMLU) | 28% of MMLU questions need culturally sensitive knowledge, and 84.9% of geography questions concern North America or Europe. Rankings shift more on CS subsets (5.7 rank changes on average) than on CA subsets (3.4) (M, search extracts) |
| Versions, successors | None. The brand stayed frozen (H) | Lite version (H) |
| Maintainer, last update | OpenAI `simple-evals`; results frozen since Jul 2025 (H) | Cohere Labs (HF dataset) (M) |
| Distribution channel | Lab sponsor, HF dataset, `simple-evals` runner (H) | HF, lm-eval-harness (H) |
| Headline tables | 14/34, Anthropic, Google and OpenAI only; last in Opus 4.7 (Apr 2026). Gemini 3.5 Flash dropped it [D:MCA] (H) | 1/34 (G1, "Global MMLU (Lite)") [D:MCA] (H) |

**MGSM (context).**
- Launch: Google (Shi et al.), Oct 2022. 250 GSM8K problems translated by paid professional translators [shi2022mgsm] (H-data). Launch SOTA: PaLM, 55.
- Saturation:
  - `simple-evals`: "We believe these evals are saturated for our newer models"; o3-high scores 92.0 [openai2025simpleevals] (H).
  - Akhtar's top 5: Claude Opus 4.1 94.4 to 93.0; saturation index 0.92 (H-data).
- Translation errors are reported in arXiv:2511.05162 (L, not read).
- The multilingual clustering penalty is real: MGSM's 2,500 items behave like about 707 independent ones (design effect 3.5) [miller2024errorbars via contamination_saturation_stats.md] (H).
- Headline tables: 1/34 (M1).

**Family-level fact (H, [D:MCA]).** No multilingual row appears in any 2026H2 frontier table in the sample (A11, A12, G4). The family exited without a successor: the capability became table stakes, not a differentiator [I].

### 6. Multimodal: MMMU → MMMU-Pro

| Field | MMMU | MMMU-Pro |
|---|---|---|
| Creator, date | Yue et al.; Nov 2023; CVPR 2024 [yue2024mmmu] (H) | Yue et al.; 5 Sep 2024; ACL 2025 [yue2025mmmupro] (H) |
| Construct | College-level multi-discipline multimodal understanding and reasoning (H) | The same construct, made "robust" (H) |
| Item source | 11.5K questions from college exams, quizzes and textbooks; 30 subjects, 183 subfields, 32 image types (H) | Three steps (H): (1) filter out text-only-answerable questions, using four text-only LLMs (Llama3-70B-Instruct, Qwen2-72B-Instruct, Yi-1.5-34B-Chat, Mixtral-8×22B-Instruct) with ten tries each (M); (2) expand from 4 to 10 options; (3) add a vision-only setting with the question embedded in a screenshot. 1,730 items per setting [C, H] |
| Grader | Exact (H) | Exact (H) |
| Headroom, human anchor | GPT-4V 56% (H); 56.8 val and 55.7 test (M). Human experts on 900 val questions: 76.2 (worst), 82.6 (medium), 88.6 (best) (M) | README: "significantly lower than on MMMU, with accuracies ranging from 16.8% to 26.9%". The paper's abstract frames this as how much lower scores are, i.e. a drop (M; the README wording is ambiguous). GPT-4o, recomputed from the released outputs [C, H]: standard-10 CoT 55.0%, direct 40.1%; vision CoT 50.1%, direct 42.4% |
| Saturation timeline | o3 82.9% (Apr 2025) → GPT-5.1 85.4% (Nov 2025); 0/13 frontier tables in 2026 [D:MCA] (M-H) | Still reported in May 2026 (G4) [D:MCA] (H) |
| Contamination, shortcuts, label errors | **Blind baselines.** GeminiPro scores 42.9% on MMMU "without any visual input". Sphinx-X-MoE scores 43.6% without images, against 17.9% for its LLM backbone, which points to leakage [chen2024mmstar] (M, search extract; the problem statement is in the MMStar README, H) | This benchmark *is* the shortcut fix (H) |
| Versions, successors | MMMU-Pro. Hidden test answers **released 12 Feb 2026**, ending the EvalAI server. EvalScope third-party workflow added 28 Jul 2026 [mmmuRepo] (H) | CharXiv and other chart and document sets take over in some tables [D:MCA] |
| Maintainer, last update | MMMU team; commits through Jul 2026 (H) | Same repo (H) |
| Distribution channel | EvalAI (retired), lm-eval, Inspect Evals, EvalScope (H) | Labs re-run it themselves; Google names it among the benchmarks it ran [D:MCA] (H) |
| Headline tables | 12/34 [D:MCA] (H) | 10/34 [D:MCA] (H) |

MMMU is the textbook case for Brief A's lifecycle:
1. launch far below an expert anchor;
2. saturation;
3. a shortcut audit;
4. a filtered "Pro" successor;
5. retirement of the hidden test set.

### 7. Verdicts on the survey's claims

| Claim | IF | Tool calling | Honesty/safety | Domain | Multilingual | Multimodal | Verdict |
|---|---|---|---|---|---|---|---|
| (a) Launch → saturation → label-noise ceiling → successor | Shape holds. The ceiling is **overfitting to templates**, not label noise | BFCL holds, with a label-churn ceiling. **StableToolBench contradicts it**: death by environment rot before saturation | **Contradicts it**: TruthfulQA died of shortcuts and judge obsolescence, not saturation. MASK is a propensity measure that does not follow a capability arc | Holds. The ceiling is **expert disagreement and rubric blindness** | **Contradicts it**: saturation followed by *family exit*, with no successor | Holds (textbook) | **Partially holds.** Restate as "launch → rapid gain → validity ceiling (family-specific) → successor *or family exit*" |
| (b) LLM judges are a liability; keep them out of headlines | MultiChallenge (judged) is in 5/34 | StableToolBench's judge instability | TruthfulQA's judge became unshareable | **HealthBench and Finance Agent are adopted**, but the grader changed between versions and rubrics miss hallucinations | n/a | n/a | **Descriptively contradicted; normatively confirmed.** Judged scores reach headlines; their failure mode is version fragility, not non-adoption |
| (c) Public verifiable generators become curricula | **Strongly confirmed** (IFEval → IFBench → IFBench removed from AA within about 10 months) | Consistent: BFCL's templated single-turn core saturated and was down-weighted | n/a | n/a | n/a | n/a | **Confirmed.** A held-out constraint family bought roughly one year |
| (d) Adoption follows third-party runners and product alignment, not citations | IFBench spread via AA (runner) | **The runner is not sufficient** (BFCL 0/34). Product-aligned MCP Atlas and Toolathlon win | Wrong outcome measure: safety spreads via system cards | **The runner is not necessary** (HealthBench). Product alignment is decisive | **Sponsorship beats validity** (MMMLU 14 against Global-MMLU 1) | Lab-run MMMU-Pro | **Holds in refined form.** Product alignment dominates; a runner helps but is neither necessary nor sufficient; audience matters (open-weight vs frontier) |
| (e) Academic versioned leaderboards survive through maintenance | n/a | **BFCL: maintained but never frontier-adopted, and its maintenance decayed** (data frozen Dec 2025) | MASK frozen at launch | n/a | n/a | MMMU maintained, then retired its hidden test set | **Necessary for survival as a research standard; not sufficient for frontier adoption; decays after publication** |

### 8. Families that contradict a brief claim (flags)

| Family | Contradicted claim | Evidence (confidence) |
|---|---|---|
| Instruction following | Brief A (a): the "label-noise ceiling" stage | No IFEval label audit was found. The binding constraint was overfitting to 25 templates (H) |
| Function calling | Brief C S2 / (e), as a route to frontier adoption; Brief B S1 (a runner is sufficient) | BFCL: 108 model rows, v1-v4, pip and Inspect packaging, yet 0/34; data frozen since 16 Dec 2025 (H) |
| Function calling | Brief A (a) | StableToolBench: 55.6% unstable APIs (M), an LLM-simulated environment (H), dormant since Apr 2025 (H) |
| Honesty and safety | Brief A (a); Brief B's headline-adoption metric | TruthfulQA: a question-blind 66.6-79.6% (H) and an unshareable GPT-judge (H). 0/34 for both safety benchmarks, which appear in model cards instead (M) |
| Domain | Brief A F9 / Brief B F5 (descriptive reading); Brief A S1 (headroom against a human anchor) | HealthBench 4/34 and Finance Agent 8/34 (H). HB-Pro launched with a model at 59.0 against physicians at 43.7 (M) |
| Multilingual | Brief A (a) "then a successor"; Brief A S1 | Multilingual rows are absent from all 2026H2 frontier tables (H). MMMLU was adopted with o1 already at 87.7% (H) |
| Multimodal | None | Fits (a) and F5 exactly (H/M) |

### 9. Cross-checks against `model_cards_adoption.md`

- All counts quoted in the task brief match the dossier's table: IFEval 5, MultiChallenge 5, HealthBench\* 4, Finance Agent\* 8, MCP Atlas 9, Toolathlon 4, MMMU 12, MMMU-Pro 10, MMMLU 14, BFCL 0 (H).
- **One discrepancy.** The task brief lists the "Legal Agent Benchmark" as single-release. The dossier's own release lists put it in A10b and A11, and I confirmed the A10b row from the table image (H).
- The "BFCL never appears" result is **sample-scoped**. The 34-release sample has no Qwen or Zhipu releases and no Llama 3.x releases, and all of these used BFCL (H).

---

## Implications for designing a new benchmark

1. **Hold out families, not items, and plan for about a one-year half-life for each held-out family.**
   - IFBench's unseen constraints held for about a year before RLVR recipes and public verifiers closed the gap (H/M).
   - Publish in-family against out-of-family performance as a first-class metric.
   - Rotate generator families on a published schedule.
   - Never release the test-family generator with the benchmark: IFBench shipped its training curriculum on day one.
2. **If any score is judged, version the whole grading triple.**
   - Put the rubric, the grader model and the length policy in the version string.
   - Publish grader-expert agreement for each release.
   - Keep a deterministic sub-score as the headline anchor.
   - HealthBench → HB-Pro changed the grader and added a length penalty under one brand (H). Rubric-blind error probes should be part of every release (M).
3. **Use hermetic environments with state-based checks.** BFCL v3 compares backend state after each turn (H). Avoid live third-party APIs, which caused StableToolBench's decay (M). Avoid LLM-simulated environments, which add a second model dependency (H).
4. **Lock and report the harness.** A 44-point FC-versus-Prompt swing for the same model on BFCL (H) is larger than most frontier gaps. Fix the call format, or report the sensitivity as a separate axis, as BFCL v4 does with 26 format configurations.
5. **Ship blind and ablation baselines at launch and in every version.** Examples: question-hidden (TruthfulQA, 66.6-79.6%), modality-removed (MMMU, 42.9%), and answer-format-only. Filter or re-weight items that such baselines solve (MMMU-Pro).
6. **Separate propensities from capabilities and test for safetywashing.**
   - Report each construct's correlation with a capability composite [ren2024safetywashing].
   - For honesty-like constructs, elicit beliefs separately (MASK).
   - If the construct is a propensity, expect adoption through system cards, not headline tables.
7. **Choose the audience deliberately.**
   - Frontier-lab headlines follow product alignment (health, finance, MCP agents) and a runner the labs trust.
   - The open-weight and research standard follows harness packaging and an open leaderboard (BFCL, IFEval).
   - A benchmark optimised for one audience may not reach the other.
8. **Budget maintenance beyond the paper cycle, and write the end of life down.** BFCL's cadence fell from about monthly to nothing within about 9 months of its ICML publication (H). Toolathlon's explicit "final version" and MMMU's release of its test answers are graceful exits worth copying.
9. **For expert-judged domains, estimate and publish the disagreement ceiling.** HealthBench's disagreement is 81.8% case-level (M). Near that ceiling, score gains are noise.
10. **If multilingual, use human translation, cultural-sensitivity tags and cluster-aware standard errors.** MGSM's design effect is 3.5 (H). Expect the family to leave frontier headlines once it saturates, so do not make multilinguality the headline construct.
11. **Keep custody independent of any product being evaluated.** HB-Pro's top system is its sponsor's product, and Anthropic headlines a competitor's benchmark on which it leads (H/M). Both are selective-disclosure risks (Brief B F4).

---

## Claims ledger

| # | Claim | Source URL(s) | Confidence |
|---|---|---|---|
| 1 | IFEval has 541 prompts and 25 verifiable constraint types; grading is by Python verifiers | https://github.com/google-research/google-research/tree/master/instruction_following_eval ; https://github.com/allenai/IFBench (README: "25 classic IFEval keys") | H [C] |
| 2 | IFEval "quickly saturated, with many leading models scoring 80+% at as small as 2B parameters"; "most models strongly overfit to this small set of constraints" | https://github.com/allenai/IFBench/blob/main/Precise_IF_Generalization_Abilities.pdf | H |
| 3 | Nemotron-4 340B generated targeted IF data "combining synthetic instructions with constraints from the IFEval taxonomy" (as stated in the IFBench paper) | same PDF | H (secondary statement inside a primary paper) |
| 4 | On IFBench's 58 OOD constraints, GPT-4.1, Claude 3.7 Sonnet, Qwen3-32B and Claude 4 Sonnet score below 50%; IF-RLVR models beat all but o3 | same PDF | H |
| 5 | IF-RLVR: Tülu-3-8B IFEval 82.4→92.2 and IFBench 28.9→45.9; Qwen2.5-7B base 87.8/54.7; authors release 29 training constraints and RLVR code | same PDF; https://github.com/allenai/IFBench | H |
| 6 | IFEval top 5 (Akhtar data): 93.9, 93.2, 92.1, 92.1, 90.4; saturation index 0.82; launch SOTA 83.57 (GPT-4) | https://github.com/evaleval/benchmark-saturation/blob/main/data/manual_annotation_data.csv | H |
| 7 | GPT-4 at IFEval launch: 76.9% prompt-strict | https://arxiv.org/abs/2311.07911 (search extract) | M |
| 8 | Llama 3.3 70B card: IFEval 92.1, MGSM 91.1, BFCL v2 77.3 | https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md | H |
| 9 | AA added IFBench in index v2.1 (Aug 2025) and removed it in v4.1 (Jun 2026) | research/notes/aggregators_indices.md (captured AA changelog; fact-check "Confirmed (captured copy)") | M-H |
| 10 | AA IFBench top about 83% by Sep 2026 | https://artificialanalysis.ai/evaluations/ifbench (search extract); https://benchlm.ai/benchmarks/aaifbench | L |
| 11 | MultiChallenge uses an LLM judge with instance-level rubrics, with up to 93% agreement with human raters; frontier models under 50% at launch | https://aclanthology.org/2025.findings-acl.958.pdf ; https://scale.com/research/multichallenge (search extracts) | M |
| 12 | BFCL leaderboard live 26 Feb 2024; v2 Live 20 Aug 2024; v3 21 Sep 2024; v4 17 Jul 2025 | https://github.com/ShishirPatil/gorilla (README news; CHANGELOG) | H |
| 13 | BFCL v1: 2,000 pairs (1,680 Python, 100 Java, 50 JavaScript, 70 REST, 100 SQL); AST and executable evaluation | https://github.com/ShishirPatil/gorilla/blob/gh-pages/blogs/8_berkeley_function_calling_leaderboard.html | H |
| 14 | BFCL v2 Live: 2,251 live, user-contributed pairs "avoiding the drawbacks of dataset contamination" | https://github.com/ShishirPatil/gorilla/blob/gh-pages/blogs/12_bfcl_v2_live.html | H |
| 15 | BFCL v3: state-based and response-based multi-turn checking | https://github.com/ShishirPatil/gorilla/blob/gh-pages/blogs/13_bfcl_v3_multi_turn.html | H |
| 16 | BFCL v4: "As single-turn tasks approach saturation, weighting now favors complex, multi-step agentic tasks" (Live/Non-Live 33%→10%, Agentic 40%) | https://github.com/ShishirPatil/gorilla/blob/main/berkeley-function-call-leaderboard/CHANGELOG.md | H |
| 17 | 16 Oct 2024 dataset fix touched 679 of 1,351 scored live AST entries (about 50%); 11 Dec 2024 enum fix touched 256 | same CHANGELOG; https://github.com/ShishirPatil/gorilla/blob/gh-pages/blogs/15_bfcl_v4_web_search.html (composition) | H [C] |
| 18 | BFCL final data (16 Dec 2025): 108 rows, 44 proprietary; top Opus 4.5 FC 77.47%; Opus 4.5 Prompt 33.47%; GPT-5.2 FC 55.87% (rank 16) | https://github.com/ShishirPatil/gorilla/blob/gh-pages/data_overall.csv | H [C] |
| 19 | BFCL data unchanged since 16 Dec 2025; 12 Apr 2026 commit only bumped the date; last repo commit 23 Mar 2026; monthly commits fell from 29 (Jun 2025) to 1-5 (2026) | https://github.com/ShishirPatil/gorilla (git history of main and gh-pages) | H [C] |
| 20 | Qwen3 technical report uses BFCL v3 (flagship 70.8) and "Some baselines are derived from the BFCL leaderboard" | https://github.com/yanfeng98/paper-is-all-you-need/blob/main/papers/00069-Qwen3_Technical_Report.pdf ; https://arxiv.org/abs/2505.09388 | H |
| 21 | Llama 3.1 card lists BFCL under Tool Use | https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md | H |
| 22 | BFCL is implemented in Inspect Evals and packaged as `bfcl-eval` | https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals ; BFCL README | H |
| 23 | BFCL, MCP Atlas, Toolathlon and τ²-bench headline counts 0/9/4/19 in 34 releases | research/notes/model_cards_adoption.md | H (sample-specific) |
| 24 | StableToolBench: cache + GPT-4-turbo API simulator; GPT-4 evaluator; evaluator switched because the preview "may produce unstable evaluations"; MirrorAPI mirrors more than 7k APIs; last commit 15 Apr 2025 | https://github.com/THUNLP-MT/StableToolBench | H |
| 25 | 55.6% of ToolBench tools had inconsistent API status | https://arxiv.org/abs/2403.07714 (search extract) | M |
| 26 | Toolathlon-Verified released 30 Jun 2026 as "the verified final version"; public eval service from Nov 2025 | https://github.com/hkust-nlp/Toolathlon | H |
| 27 | TruthfulQA MC1 heuristics: odd-one-out 73%; decision tree 79.6% (theory) and 66.6% (implemented, question hidden); only 37/256 immune; SOTA 80.8% (Nov 2024) | https://github.com/alexander-turner/TurnTrout.com/blob/main/website_content/truthfulqa.md ; https://www.lesswrong.com/posts/57k6xNcWtAtsSTcor/gaming-truthfulqa-simple-heuristics-exposed-dataset | H |
| 28 | TruthfulQA authors: binary MC (Jan 2025); MC1/MC2 "still valid"; not a full validation of the remaining questions; GPT-judge not externally accessible | https://github.com/sylinrl/TruthfulQA | H |
| 29 | TruthfulQA MC1 correlates 0.812 with capabilities | https://arxiv.org/abs/2407.21792 (quoted in the Turner post source) | H |
| 30 | MASK: "scaling pre-training does not improve model honesty"; judges are o3-mini and gpt-4o; repo last commit 6 Mar 2025 | https://github.com/centerforaisafety/mask | H |
| 31 | MASK honesty vs compute ρ = −0.599; accuracy +0.873 | research/notes/gap_offg_construct_evidence.md (arXiv HTML extracts) | M |
| 32 | xAI cards report MASK dishonesty of 0.43-1.90% for Grok 4.x | https://data.x.ai/2025-11-17-grok-4-1-model-card.pdf ; https://media.x.ai/v1/website/card-4p6-4cd2dc57.pdf (search extracts) | L-M |
| 33 | HealthBench: 5,000 conversations, 48,562 criteria, 262 physicians from 60 countries; o3 0.60, GPT-3.5 Turbo 0.16; Hard o3 0.32 | https://openai.com/index/healthbench/ ; https://arxiv.org/abs/2505.08775 (search extracts) | M |
| 34 | HealthBench grader is `gpt-4.1-2025-04-14`; Hard and Consensus subsets; physicians given Apr-2025 model references | https://github.com/openai/simple-evals/blob/main/healthbench_eval.py | H |
| 35 | HB-Pro mode requires "GPT-5.4 low grader, and length adjustment" (22 Apr 2026) | https://github.com/openai/simple-evals (commit "Add HealthBench Professional options") | H |
| 36 | HB-Pro: 525 tasks; rubrics by 3 or more physicians over 3 rounds; physicians 43.7, GPT-5.4 base 48.1, ChatGPT for Clinicians 59.0 | https://arxiv.org/abs/2604.27470 ; https://cdn.openai.com/dd128428-0184-4e25-b155-3a7686c7d744/HealthBench-Professional.pdf (search extracts) | M |
| 37 | Grader-physician macro F1 about 0.71, "comparable to" inter-physician agreement | https://arxiv.org/abs/2505.08775 (search extract) | M |
| 38 | Anthropic Fable 5 table: HealthBench Professional 66.0%\*/64.7/56.9/51.8; Legal Agent Benchmark 13.3/10.4/2.1/0.0 | https://www.anthropic.com/news/claude-fable-5-mythos-5 (table image) | H |
| 39 | Physician disagreement: 81.8% case-level; rubric 15.8% of label variance; physician 2.4% | https://arxiv.org/abs/2602.22758 (search extract); https://github.com/satyaborg/healthbench-physician-disagreement | M |
| 40 | Rubrics miss clinically relevant hallucinations, often leaving scores unchanged (HealthBench, HB-Pro, LiveMedBench) | https://arxiv.org/abs/2609.12718 (search extract); https://github.com/FJFehr/when-rubrics-fail | M |
| 41 | GPT-5 HealthBench Hard 46.2% vs o3 31.6% | https://openai.com/index/introducing-gpt-5/ ; https://cdn.openai.com/gpt-5-system-card.pdf (search extracts) | M |
| 42 | Claude for Healthcare launched 11 Jan 2026 | https://www.mobihealthnews.com/news/jpm-anthropic-launches-claude-healthcare ; https://www.fiercehealthcare.com/ai-and-machine-learning/jpm26-anthropic-launches-claude-healthcare-targeting-health-systems-payers | M |
| 43 | Finance Agent v1: 537 expert questions, post-2024 SEC filings, LLM-judge rubric with contradiction check, best 46.8% | https://arxiv.org/abs/2508.00828 ; https://zenodo.org/records/15428639 (search extracts) | M |
| 44 | Finance Agent v2 (May 2026): private held-out split, about 14-point average drop vs v1.1 | https://www.vals.ai/benchmarks/fabv2 ; https://www.kucoin.com/blog/can-ai-replace-financial-analysts-in-2026-vals-ai-finance-agent-v2-reveals-gpt-5-5-hits-just-52-percent-accuracy | L-M |
| 45 | Finance Agent scores 55.3 → 64.4 (v1.1) → 53.9/57.9 (v2); 8/34 headline | research/notes/model_cards_adoption.md | H |
| 46 | MedQA top 5 about 96.1-96.5 (o1, GPT-5.1, GPT-5); saturation index 0.99; relabelled by 3 or more PCPs per question | https://github.com/evaleval/benchmark-saturation ; https://github.com/Google-Health/med-gemini-medqa-relabelling | H |
| 47 | LegalBench: 162 tasks from 40 contributors; Akhtar top 84.5 (GPT-5); last commit 29 Mar 2026 | https://github.com/HazyResearch/legalbench ; Akhtar CSV | H |
| 48 | MMMLU: professional human translators, 14 languages; o3-high 0.888 average; Yoruba lowest | https://github.com/openai/simple-evals/blob/main/multilingual_mmlu_benchmark_results.md | H |
| 49 | Global-MMLU: 42 languages; CS/CA annotation on 2,850 questions per language; Lite 15 languages | https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/global_mmlu | H |
| 50 | Global-MMLU: 28% culturally sensitive; 84.9% of geography questions about NA/EU; CS rank changes 5.7 vs CA 3.4 | https://aclanthology.org/2025.acl-long.919/ ; https://arxiv.org/abs/2412.03304 (search extracts) | M |
| 51 | MGSM "saturated for our newer models"; o3-high 92.0 | https://github.com/openai/simple-evals | H |
| 52 | MGSM design effect 3.5 (2,500 items ≈ 707 independent) | research/notes/contamination_saturation_stats.md (Miller et al.) | H |
| 53 | No multilingual row in any 2026H2 frontier headline table in the sample; MMMLU last in Apr 2026 | research/notes/model_cards_adoption.md (A11, A12, G4 lists) | H (sample-specific) |
| 54 | MMMU: 11.5K questions, 30 subjects, 183 subfields; GPT-4V 56% | https://github.com/MMMU-Benchmark/MMMU | H |
| 55 | MMMU human experts 76.2/82.6/88.6 | https://mmmu-benchmark.github.io/ ; https://arxiv.org/abs/2311.16502 (search extracts) | M |
| 56 | MMMU-Pro: text-only filter with four LLMs × 10 tries; 10 options; vision-only; "16.8% to 26.9%" lower | https://github.com/MMMU-Benchmark/MMMU ; https://arxiv.org/abs/2409.02813 (search extract) | H (steps) / M (filter detail and the meaning of the range) |
| 57 | GPT-4o on MMMU-Pro: standard-10 CoT 55.0, vision CoT 50.1 (n = 1,730) | https://github.com/MMMU-Benchmark/MMMU/tree/main/mmmu-pro/output | H [C] |
| 58 | MMMU test answers released 12 Feb 2026; EvalScope added 28 Jul 2026 | https://github.com/MMMU-Benchmark/MMMU | H |
| 59 | GeminiPro 42.9% on MMMU without images; Sphinx-X-MoE 43.6% vs 17.9% backbone | https://arxiv.org/abs/2403.20330 (search extract); https://github.com/MMStar-Benchmark/MMStar | M |
| 60 | Inspect Evals includes bfcl, healthbench, ifeval, mask, medqa, mgsm, mmmu, sycophancy, tau2 and truthfulqa; not IFBench or StableToolBench | https://github.com/UKGovernmentBEIS/inspect_evals | H |

---

## References

Keys marked (existing) are reused from other refs files. New keys are in `refs/gap_uncovered_families_generality.json`.

1. [zhou2023ifeval] Zhou, J., Lu, T., Mishra, S., Brahma, S., Basu, S., Luan, Y., Zhou, D., Hou, L. *Instruction-Following Evaluation for Large Language Models.* arXiv:2311.07911, 2023. https://github.com/google-research/google-research/tree/master/instruction_following_eval
2. [pyatkin2025ifbench] Pyatkin, V., Malik, S., Graf, V., Ivison, H., Huang, S., Dasigi, P., Lambert, N., Hajishirzi, H. *Generalizing Verifiable Instruction Following.* NeurIPS 2025 D&B; arXiv:2507.02833. https://github.com/allenai/IFBench
3. [sirdeshmukh2025multichallenge] Sirdeshmukh, V., et al. *MultiChallenge: A Realistic Multi-Turn Conversation Evaluation Benchmark Challenging to Frontier LLMs.* Findings of ACL 2025; arXiv:2501.17399.
4. [patil2025bfcl] Patil, S. G., Mao, H., Yan, F., Ji, C. C.-J., Suresh, V., Stoica, I., Gonzalez, J. E. *The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models.* ICML 2025 (PMLR 267). https://proceedings.mlr.press/v267/patil25a.html
5. [gorillaBfclRepo] Gorilla team. *Berkeley Function Calling Leaderboard: README, CHANGELOG, commit history.* https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard
6. [bfclLeaderboardData] Gorilla team. *BFCL leaderboard data and blogs (gh-pages; checkpoint 2025-12-16).* https://github.com/ShishirPatil/gorilla/tree/gh-pages
7. [guo2024stabletoolbench] Guo, Z., Cheng, S., Wang, H., Liang, S., Qin, Y., Li, P., Liu, Z., Sun, M., Liu, Y. *StableToolBench: Towards Stable Large-Scale Benchmarking on Tool Learning of Large Language Models.* Findings of ACL 2024; arXiv:2403.07714. https://github.com/THUNLP-MT/StableToolBench
8. [li2025toolathlon] Li, J., et al. (21 authors, including Neubig, G. and He, J.). *The Tool Decathlon: Benchmarking Language Agents for Diverse, Realistic, and Long-Horizon Task Execution.* arXiv:2510.25726, 2025. https://github.com/hkust-nlp/Toolathlon
9. [lin2022truthfulqa] (existing) Lin, S., Hilton, J., Evans, O. *TruthfulQA.* ACL 2022.
10. [truthfulqa2025newmc] (existing) *New, improved multiple-choice TruthfulQA.* Jan 2025.
11. [truthfulqaReadme] Lin, S., et al. *TruthfulQA repository README (Updates: Oct 2021, Jan 2025).* https://github.com/sylinrl/TruthfulQA
12. [turner2025gamingtruthfulqa] (existing; now verified) Turner, A., Kurzeja, M. *Gaming TruthfulQA: Simple Heuristics Exposed Dataset Weaknesses.* 15 Jan 2025. Source: https://github.com/alexander-turner/TurnTrout.com/blob/main/website_content/truthfulqa.md
13. [ren2024safetywashing] (existing) Ren, R., et al. *Safetywashing: Do AI Safety Benchmarks Actually Measure Safety Progress?* arXiv:2407.21792.
14. [ren2025mask] (existing) Ren, R., Agarwal, A., Mazeika, M., et al. *The MASK Benchmark.* arXiv:2503.03750. https://github.com/centerforaisafety/mask
15. [xai2025grok41card] xAI. *Grok 4.1 Model Card.* 17 Nov 2025. https://data.x.ai/2025-11-17-grok-4-1-model-card.pdf (search extract only)
16. [arora2025healthbench] OpenAI (first author Arora per the lead; author list not verified). *HealthBench: Evaluating Large Language Models Towards Improved Human Health.* arXiv:2505.08775, 2025. Reference implementation: https://github.com/openai/simple-evals/blob/main/healthbench_eval.py
17. [openai2026healthbenchpro] OpenAI. *HealthBench Professional: Evaluating Large Language Models on Real Clinician Chats.* arXiv:2604.27470, 2026.
18. [openaiSimpleEvalsHBPro2026] OpenAI. *simple-evals: "Add HealthBench Professional options" (PR #108, 22 Apr 2026).* https://github.com/openai/simple-evals
19. [openai2025simpleevals] (existing) OpenAI. *simple-evals.* https://github.com/openai/simple-evals
20. [borgohain2026disagreement] Borgohain, S., Mariathas. *Decomposing Physician Disagreement in HealthBench.* arXiv:2602.22758, 2026. https://github.com/satyaborg/healthbench-physician-disagreement
21. [farrow2026rubricsfail] Farrow, G., Li, L. S., Johnson, J., Wang, T., Torr, P., Bolton, W., Fehr, F. J. *When Rubrics Fail: Hallucinations Reveal Blind Spots in Medical AI Evaluation.* arXiv:2609.12718, 2026. https://github.com/FJFehr/when-rubrics-fail
22. [claudeHealthcare2026] MobiHealthNews / Fierce Healthcare. *JPM26: Anthropic launches Claude for Healthcare.* Jan 2026.
23. [anthropic2026fable5] (existing) Anthropic. *Claude Fable 5 and Claude Mythos 5.* 9 Jun 2026.
24. [anthropic2026opus5] (existing) Anthropic. *Introducing Claude Opus 5.*
25. [bigeard2025financeagent] Bigeard, A., Krishnan, R., Wu, S., Nashold, L. *Finance Agent Benchmark: Benchmarking LLMs on Real-world Financial Research Tasks.* arXiv:2508.00828, 2025.
26. [valsFabV2] Vals AI. *Finance Agent v2.* https://www.vals.ai/benchmarks/fabv2 (May 2026)
27. [guha2023legalbench] Guha, N., et al. (first author per the lead). *LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models.* NeurIPS 2023 D&B; arXiv:2308.11462. https://github.com/HazyResearch/legalbench
28. [saab2024medgemini] Saab, K., Tu, T., et al. *Capabilities of Gemini Models in Medicine.* arXiv:2404.18416, 2024. MedQA relabelling: https://github.com/Google-Health/med-gemini-medqa-relabelling
29. [shi2022mgsm] Shi, F., et al. (first author per the lead). *Language Models are Multilingual Chain-of-Thought Reasoners.* arXiv:2210.03057, 2022 (title and ID from the simple-evals README).
30. [openai2024mmmlu] OpenAI. *Multilingual MMLU (MMMLU) benchmark results.* https://github.com/openai/simple-evals/blob/main/multilingual_mmlu_benchmark_results.md
31. [singh2024globalmmlu] Singh, S., Romanou, A., Fourrier, C., Adelani, D. I., et al. *Global MMLU: Understanding and Addressing Cultural and Linguistic Biases in Multilingual Evaluation.* ACL 2025; arXiv:2412.03304.
32. [miller2024errorbars] (existing) Miller, E. *Adding Error Bars to Evals.* arXiv:2411.00640.
33. [yue2024mmmu] Yue, X., et al. *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI.* CVPR 2024; arXiv:2311.16502.
34. [yue2025mmmupro] Yue, X., et al. *MMMU-Pro: A More Robust Multi-discipline Multimodal Understanding Benchmark.* ACL 2025; arXiv:2409.02813.
35. [mmmuRepo] MMMU team. *MMMU repository (news: MMMU-Pro 2024-09-05; test answers released 2026-02-12).* https://github.com/MMMU-Benchmark/MMMU
36. [chen2024mmstar] Chen, L., Li, J., et al. *Are We on the Right Way for Evaluating Large Vision-Language Models?* NeurIPS 2024; arXiv:2403.20330. https://github.com/MMStar-Benchmark/MMStar
37. [qwen2025qwen3] Qwen Team. *Qwen3 Technical Report.* arXiv:2505.09388, 2025.
38. [meta2024llama31card] Meta. *Llama 3.1 Model Card.* https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md
39. [meta2024llama33card] Meta. *Llama 3.3 Model Card.* https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md
40. [inspectevals] (existing) UK AISI. *Inspect Evals.* https://github.com/UKGovernmentBEIS/inspect_evals
41. [gao2024harness] (existing) EleutherAI. *lm-evaluation-harness.* https://github.com/EleutherAI/lm-evaluation-harness
42. [hf2024ollv2] (existing) and [hf_openllm_archive] (existing). Open LLM Leaderboard v2 blog and archive.
43. [evaleval2026saturationdata] (existing) evaleval. *benchmark-saturation (manual annotation data).* https://github.com/evaleval/benchmark-saturation
44. [akhtar2026plateau] (existing) Akhtar, M., et al. *When AI Benchmarks Plateau.*
45. [aa2026method] (existing) Artificial Analysis. *Intelligence Benchmarking methodology and changelog.*
46. [stojanovski2025reasoninggym] (existing) *Reasoning Gym.*
47. [ai2025ifbenchAA] Ai2. *Why Artificial Analysis uses Ai2's IFBench instruction-following benchmark.* https://allenai.org/blog/ifbench-artificial-analysis (title seen in search only; L)
48. [benchlm2026] BenchLM.ai. *IFBench / AA-IFBench / LegalBench leaderboard snapshots, Sep 2026.* (secondary aggregator; L)
