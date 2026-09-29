# Adoption signals: which benchmarks frontier labs actually report, how long they last, and what makes one universal (as of 2026-09-29)

Scope:
- (a) Which benchmarks frontier and major open-weight labs actually put in the headline tables of their 2025–2026 releases.
- (b) Quantitative lifecycle data: time from benchmark release to saturation, and how that time has shrunk.
- (c) Which benchmarks went from obscure to universal, and what triggered it.
- The dossier closes with the empirically strongest predictors of adoption.

**How the evidence was gathered, and what that means for confidence.**
- The session-wide WebSearch budget (200 calls) was exhausted before this subagent started, so no WebSearch call succeeded.
- WebFetch/curl to openai.com, blog.google, deepmind.google, x.ai, ai.meta.com, arxiv.org, huggingface.co, hai.stanford.edu and epoch.ai was blocked.
- The evidence therefore comes from the following source types.

| Tag | Meaning |
|---|---|
| **[P]** | Primary, fetched by me. |
| **[Mi]** | Faithful mirror of a blocked primary page. |
| **[Sib]** | Fact verified by a sibling subagent in `research/notes/*.md`. Carried over with its URL; not re-fetched by me unless stated. |
| **[S]** | Secondary: LLM-written summaries or community datasets. |
| **[D]** | Derived: numbers I computed from [P]/[Mi] data. The method is described in §A.1. |

What each tag covers in practice:
- **[P]**
  - Anthropic launch posts on anthropic.com. HTML text was parsed, and benchmark tables (which are images) were downloaded through anthropic.com's image proxy and read visually.
  - Google DeepMind model cards and reports on storage.googleapis.com. PDFs were rendered to images where tables were images.
  - GitHub READMEs and model cards (DeepSeek, Moonshot, MiniMax, Meta, Zhipu, OpenAI simple-evals).
  - The ICML 2026 PMLR PDF of Akhtar et al. and its companion data repository.
  - The ARC-AGI-2 changelog.
- **[Mi]** OpenAI and DeepMind blog pages mirrored as cleaned markdown in `visual-snow/seshat/web-research/…`.
  - Each file carries its original `source_url` and date.
  - Figures are stripped, but chart titles, data labels and markdown tables survive.
  - I treat these as faithful copies (medium-high confidence).
  - Other mirrors: the ARC Prize 2025 technical report (UNIR-TUC mirror of arXiv:2601.10904), the AI Index 2025 page (an r.jina scrape stored on GitHub), and the Dynabench Figure 1 image reproduced in a university course repository.
- **[S]** examples: AI Index 2026 chapter summaries on GitHub, and the community "Killed by LLM" dataset.

Confidence tags: **[H]** high, **[M]** medium, **[L]** low.

---

## Summary

1. **Lab adoption is extremely concentrated, and the concentrated set turns over fast.** [D from P/Mi] I built a release × benchmark matrix from the headline benchmark tables of **34 releases by 7 developers** (Dec 2024 to Sep 2026): Anthropic 14, OpenAI 9, Google 4, Meta 1, DeepSeek 3, Moonshot 1, MiniMax 2.
   - They name **110 benchmark families**, or 121 distinct names before collapsing versions.
   - **48 families (44%) appear in exactly one release**, and 21 more appear in only two.
   - Only **11 families appear in at least one-third of releases**:

     | Benchmark | Releases (of 34) |
     |---|---|
     | GPQA Diamond | 27 |
     | SWE-bench Verified | 23 |
     | Humanity's Last Exam | 22 |
     | Terminal-Bench (all versions) | 21 |
     | AIME (2024/2025) | 19 |
     | τ-/τ²-bench | 19 |
     | OSWorld (all versions) | 15 |
     | MMMLU | 14 |
     | GDPval / GDPval-AA | 13 |
     | MMMU | 12 |
     | BrowseComp | 12 |

   - Akhtar et al. (ICML 2026) found the same long tail independently: 190 benchmarks across 61 developer reports (Jan 2022 to Nov 2025), filtered to those used in at least 5 reports. [P, H]
2. **The 2025 core set is gone from 2026 headline tables.** [D]
   - Across OpenAI, Anthropic and Google headline tables, the four 2025 staples fell as follows:

     | Benchmark | 2025 | 2026 |
     |---|---|---|
     | AIME | 13/14 | 0/13 |
     | MMMU (original) | 11/14 | 0/13 |
     | GPQA Diamond | 14/14 | 6/13 (0 after April 2026) |
     | SWE-bench Verified | 13/14 | 4/13 (0 after April 2026) |

   - **None of the 8 benchmark families in Claude 3.7 Sonnet's table (Feb 2025) remains in any Anthropic headline table from Claude Opus 4.8 (May 2026) onward.**
   - Consecutive-release retention in Anthropic tables fell from 0.75–1.00 (2025) to 0.33–0.42 (mid/late 2026).
3. **The replacement set is agentic, economic and versioned.** [D]
   - Agentic or interactive benchmarks made up this share of frontier-lab headline rows:

     | Period | Agentic share |
     |---|---|
     | 2025H1 | 23% |
     | 2025H2 | 35% |
     | 2026H1 | 61% |
     | 2026H2 | 76% (Anthropic only, n = 2 releases) |

   - The long-lived 2026 entries are **versioned brands**:
     - Terminal-Bench 1.0 → 2.0 → 2.1 → 4.0
     - OSWorld → OSWorld-Verified → 2.0 → 2.1
     - ARC-AGI-1 → 2 → 3
     - GDPval → GDPval-AA → v2 → v2.1
     - Finance Agent → v1.1 → v2
     - τ-bench → τ²-bench
     - SWE-bench → Verified → Pro
   - Humanity's Last Exam (HLE) is the only unversioned benchmark present in essentially every 2026 frontier table (12/13). [P/Mi]
4. **Retirement is now explicit and lab-driven.** [Mi, H]
   - OpenAI stopped reporting SWE-bench Verified on 23 Feb 2026. It said the benchmark "became a standard metric reported in frontier model releases" but was now contaminated and flawed: 59.4% of 138 audited hard problems were flawed, and "all frontier models we tested" reproduced gold patches.
   - OpenAI recommended SWE-bench Pro instead. SWE-bench Pro went from 1/14 frontier tables in 2025 to 9/11 in 2026H1. [D]
   - OpenAI had already frozen its classic `simple-evals` table (MMLU/GPQA/MATH/HumanEval/MGSM/DROP) in July 2025. [P, H]
   - Anthropic's Opus 5.5 post (22 Sep 2026) states that "benchmark margins have become a less reliable guide to real-world differences." [P, H]
5. **Saturation time has collapsed from decades to months.**
   - Kiela et al. (2021, Fig. 1) plot time-to-human-normalized parity. Reading approximately from the figure [P-figure, M]:

     | Benchmark | Approximate time to parity |
     |---|---|
     | MNIST, Switchboard | about 15–20 years |
     | ImageNet | about 6 years |
     | SQuAD 1.1 | about 2 years |
     | SQuAD 2.0, GLUE | about 1 year |

   - AI Index 2025: MMMU, GPQA and SWE-bench rose 18.8, 48.9 and 67.3 points within a year of their 2023 introduction. [Mi-scrape, M-H]
   - In 2025–26, headline benchmarks were driven to ceiling or retired within roughly 6–20 months:
     - AIME 2025 hit 100% (no tools, GPT-5.2) about 10 months after the exam.
     - τ²-bench telecom reached 98–99% within about 8 months.
     - SWE-bench Verified lasted about 18 months from creation to OpenAI's retirement.
     - Terminal-Bench needed a new major version roughly every 4–6 months. [P/Mi/D]
6. **What predicts adoption (strongest evidence first).**
   1. A **trusted third-party leaderboard** that labs can cite for competitor numbers. Examples: ARC Prize "Verified", Scale's HLE leaderboard, Artificial Analysis (GDPval-AA), the Terminal-Bench and OSWorld-Verified leaderboards, Kaggle, Andon Labs and Zapier. Labs explicitly source competitor columns from these. [P, H]
   2. **Alignment with the capability a lab is selling right now**: agentic coding, computer use, knowledge work. [D, H]
   3. **Measurable headroom at the moment of adoption.** Labs add a benchmark once their model shows non-trivial, improving scores and drop it near ceiling. ARC-AGI-2 was adopted about 8 months after launch, when scores reached 31–38%. AIME was dropped after 100%. [D, M-H]
   4. **Co-development with, or verification by, labs**: SWE-bench Verified with OpenAI Preparedness; lab participation in OSWorld-Verified fixes; lab task contributions to Terminal-Bench; ARC Prize verification. [P/Sib, M-H]
   5. **Brand continuity through versioning.** [P, H]
   6. **Cheap, automatic, legible scoring**, for example an Elo, a dollar value, or a single percentage. [Sib/P, M]
7. **Academic citations do not predict lab adoption.**
   - Akhtar et al. find that inclusion in technical reports is not associated with saturation once age is controlled (ρ = 0.05, p = 0.73). [P, H]
   - In my matrix, citation counts from Akhtar's dataset correlate *negatively* with 2025–26 headline adoption across 39 benchmarks (Spearman ρ = −0.34, permutation p ≈ 0.03). This is exploratory and confounded by age. [D, L-M]
   - HellaSwag (2,836 citations), TriviaQA (3,491) and GLUE (9,064) appear in zero 2025–26 headline tables. τ-bench (7 citations in Akhtar's dataset) appears in 19.
8. **Games are absent from headline tables.**
   - In all 34 releases, no conventional board-game or video-game benchmark appears as a headline row.
   - Pokémon play appears only as a qualitative demo (Claude 4 post; Gemini 2.5 report). Google did not put its own Kaggle Game Arena (launched Aug 2025, Sib) in the Gemini 3, 3.1 or 3.5 tables.
   - The only game-like rows are ARC-AGI-3 (novel, purpose-built interactive environments; in the Opus 5 table) and Vending-Bench 2 (a business simulation; in the Gemini 3 Pro table). [P, H] This supports the user's diagnosis that off-the-shelf game benchmarks lack lab uptake.

**Design takeaway for our non-game benchmark (interpretation):**
- Launch with a verified third-party leaderboard that runs every frontier model.
- Target a capability labs are selling.
- Ship with a difficulty knob and a version roadmap under one stable name, so the brand survives saturation.
- Report a single legible headline number with standard errors.
- Keep per-run cost low enough that open-weight labs do not omit it. Kimi K2 omitted results because of "prohibitively expensive evaluation costs" [Sib].

---

## A. Adoption matrix: which benchmarks labs actually reported (2025–2026)

### A.1 Method

- **Unit.** One row per release. A benchmark is counted if it appears as a row in the release's **headline results table**, or in the launch post's results charts or appendix. System-card-only evaluations are *not* counted. Headline tables are what the market sees, but they understate what labs actually run.
- **Normalisation.** Versions of one brand are collapsed into a family, marked "\*": Terminal-Bench 1.0/2.0/2.1/4.0, OSWorld/-Verified/2.0/2.1, ARC-AGI-1/2/3, GDPval/GDPval-AA/v2/v2.1, AIME 2024/2025, τ-/τ²-bench, FrontierCode Diamond/v1.1, HealthBench/Professional.
  - OpenAI-MRCR and Google's MRCR v2 are kept separate because they are different datasets.
  - "Agentic" means the model acts through tools or an environment: SWE-bench\*, Terminal-Bench\*, τ-bench\*, OSWorld\*, BrowseComp, MCP Atlas, GDPval\*, Finance Agent, Toolathlon, CyberGym, SWE-Lancer, Vending-Bench, and similar.
- **Scripts.** Computed in the scratchpad (`matrix.py`, `period.py`, `tables.py`). All data are listed in A.2 and A.3, so the analysis can be re-derived.
- **Caveats.**
  - The Anthropic sample is denser (14 releases) than Google's (4). The 2026H2 bucket has only Anthropic's Opus 5 and Opus 5.5, because no later OpenAI or Google launch page was reachable.
  - xAI (Grok 4) and Alibaba (Qwen3) are **not in the matrix**. Their launch pages and model cards were unreachable (see A.5).
  - Open-weight READMEs list more benchmarks per release (median about 20) than frontier launch tables (median about 12). Table-size effects are therefore large, and cross-lab comparisons should use shares.

### A.2 Release key (sources in References; all [P] or [Mi])

| ID | Org | Release | Date | Headline benchmarks (n) | Agentic share | Source |
|---|---|---|---|---|---|---|
| A1 | Anthropic | Claude 3.7 Sonnet | 2025-02-24 | 8 | 0.25 | anthropic.com/news/claude-3-7-sonnet (table image) |
| A2 | Anthropic | Claude Opus 4 / Sonnet 4 | 2025-05-22 | 7 | 0.43 | anthropic.com/news/claude-4 (text and footnotes) |
| A3 | Anthropic | Claude Opus 4.1 | 2025-08-05 | 7 | 0.43 | anthropic.com/news/claude-opus-4-1 |
| A4 | Anthropic | Claude Sonnet 4.5 | 2025-09-29 | 9 | 0.56 | anthropic.com/news/claude-sonnet-4-5 |
| A5 | Anthropic | Claude Haiku 4.5 | 2025-10-15 | 8 | 0.50 | anthropic.com/news/claude-haiku-4-5 |
| A6 | Anthropic | Claude Opus 4.5 | 2025-11-24 | 9 | 0.56 | anthropic.com/news/claude-opus-4-5 |
| A7 | Anthropic | Claude Opus 4.6 | 2026-02-05 | 13 | 0.62 | anthropic.com/news/claude-opus-4-6 |
| A8 | Anthropic | Claude Sonnet 4.6 | 2026-02-17 | 13 | 0.62 | anthropic.com/news/claude-sonnet-4-6 |
| A9 | Anthropic | Claude Opus 4.7 | 2026-04-16 | 12 | 0.67 | anthropic.com/news/claude-opus-4-7 |
| A10 | Anthropic | Claude Opus 4.8 | 2026-05-28 | 6 | 0.83 | anthropic.com/news/claude-opus-4-8 |
| A10b | Anthropic | Claude Fable 5 / Mythos 5 | 2026-06-09 | 13 | 0.77 | anthropic.com/news/claude-fable-5-mythos-5 |
| A10c | Anthropic | Claude Sonnet 5 | 2026-06-30 | 5 | 0.80 | anthropic.com/news/claude-sonnet-5 |
| A11 | Anthropic | Claude Opus 5 | 2026-07-24 | 12 | 0.75 | anthropic.com/news/claude-opus-5 |
| A12 | Anthropic | Claude Opus 5.5 | 2026-09-22 | 9 | 0.78 | anthropic.com/news/claude-opus-5-5 (HTML table) |
| O1 | OpenAI | GPT-4.5 | 2025-02-27 | 7 | 0.29 | openai.com/index/introducing-gpt-4-5 [Mi] |
| O2 | OpenAI | GPT-4.1 | 2025-04-14 | 18 | 0.22 | openai.com/index/gpt-4-1 [Mi] |
| O3 | OpenAI | o3 / o4-mini | 2025-04-16 | 14 | 0.29 | openai.com/index/introducing-o3-and-o4-mini [Mi] |
| O4 | OpenAI | gpt-oss-120b/20b | 2025-08-05 | 8 | 0.12 | openai.com/index/introducing-gpt-oss [Mi] |
| O5 | OpenAI | GPT-5 | 2025-08-07 | 17 | 0.18 | openai.com/index/introducing-gpt-5 [Mi] |
| O6 | OpenAI | GPT-5.2 | 2025-12-11 | 22 | 0.41 | openai.com/index/introducing-gpt-5-2 [Mi] |
| O7 | OpenAI | GPT-5.3-Codex | 2026-02-05 | 5 | 1.00 | openai.com/index/introducing-gpt-5-3-codex [Mi] |
| O8 | OpenAI | GPT-5.4 | 2026-03-05 | 20 | 0.50 | openai.com/index/introducing-gpt-5-4 [Mi] |
| O9 | OpenAI | GPT-5.5 | 2026-04-23 | 20 | 0.50 | openai.com/index/introducing-gpt-5-5 [Mi] |
| G1 | Google | Gemini 2.5 (tech report Tables 3–4) | 2025-06 | 17 | 0.06 | storage.googleapis.com …/gemini_v2_5_report.pdf |
| G2 | Google | Gemini 3 Pro | 2025-11 | 20 | 0.25 | …/gemini_3_pro_model_evaluation.pdf |
| G3 | Google | Gemini 3.1 Pro | 2026-02 | 16 | 0.50 | …/Model-Cards/Gemini-3-1-Pro-Model-Card.pdf |
| G4 | Google | Gemini 3.5 Flash | 2026-05 | 13 | 0.54 | …/Model-Cards/Gemini-3-5-Flash-Model-Card.pdf |
| M1 | Meta | Llama 4 Scout / Maverick | 2025-04-05 | 14 | 0.00 | github meta-llama/llama-models …/llama4/MODEL_CARD.md |
| D1 | DeepSeek | DeepSeek-V3 | 2024-12 | 22 | 0.05 | github deepseek-ai/DeepSeek-V3 |
| D2 | DeepSeek | DeepSeek-R1 | 2025-01 | 20 | 0.05 | github deepseek-ai/DeepSeek-R1 |
| D3 | DeepSeek | DeepSeek-V3.2-Exp | 2025-09 (month unverified) | 14 | 0.36 | github deepseek-ai/DeepSeek-V3.2-Exp |
| K1 | Moonshot | Kimi K2 | 2025-07 (from arXiv:2507.20534) | 27 | 0.19 | github MoonshotAI/Kimi-K2 |
| X1 | MiniMax | MiniMax-M1 | 2025-06 (from arXiv:2506.13585) | 15 | 0.13 | github MiniMax-AI/MiniMax-M1 |
| X2 | MiniMax | MiniMax-M2 | 2025-10 [Sib] | 21 | 0.57 | github MiniMax-AI/MiniMax-M2 |

The benchmark lists behind the counts are as follows.

**Anthropic**
- A1: GPQA Diamond, SWE-bench Verified, TAU-bench, MMMLU, MMMU, IFEval, MATH 500, AIME 2024.
- A2: SWE-bench Verified, Terminal-bench, TAU-bench, GPQA Diamond, MMMLU, MMMU, AIME.
- A3: A2's set, with "AIME 2025" named.
- A4: A3's set, plus τ2-bench (replacing TAU-bench), OSWorld and Finance Agent.
- A5: A4's set minus Finance Agent.
- A6: SWE-bench Verified, Terminal-bench 2.0, τ2-bench, MCP Atlas, OSWorld, ARC-AGI-2 (Verified), GPQA Diamond, MMMU, MMMLU.
- A7: Terminal-Bench 2.0, SWE-bench Verified, OSWorld, τ2-bench, MCP Atlas, BrowseComp, HLE, Finance Agent, GDPval-AA, ARC-AGI-2, GPQA Diamond, MMMU Pro, MMMLU.
- A8: as A7, with OSWorld-Verified and Finance Agent v1.1.
- A9: SWE-bench Pro, SWE-bench Verified, Terminal-Bench 2.0, HLE, BrowseComp, MCP-Atlas, OSWorld-Verified, Finance Agent v1.1, CyberGym, GPQA Diamond, CharXiv Reasoning, MMMLU.
- A10: SWE-Bench Pro, Terminal-Bench 2.1, HLE, OSWorld-Verified, GDPval-AA, Finance Agent v2.
- A10b: SWE-Bench Pro, FrontierCode (Diamond), GDPval-AA, GDP.pdf, Blueprint-Bench 2, AutomationBench, OSWorld-Verified, Legal Agent Benchmark, HLE, BioMysteryBench, Terminal-Bench 2.1, ExploitBench, HealthBench Professional.
- A10c: SWE-bench Pro, Terminal-Bench 2.1, HLE, OSWorld-Verified, GDPval-AA v2.
- A11: Frontier-Bench v0.1, GDPval-AA v2, ARC-AGI-3, BrowseComp, HLE, OSWorld 2.0, DeepSWE v1.1, FrontierCode v1.1, AutomationBench, Legal Agent Benchmark (held-out), HealthBench Professional, BioMysteryBench.
- A12: Terminal-Bench 4.0, FrontierCode v1.1, CursorBench 4.0, GDPval-AA v2.1, AutomationBench, HLE, Terminal-Bench-Science 0.1, OSWorld 2.1, Chartography. WANDR appears as a chart only.

**OpenAI**
- O1: GPQA, AIME '24, MMMLU, MMMU, SWE-Lancer Diamond, SWE-Bench Verified, SimpleQA.
- O2: AIME '24, GPQA Diamond, MMLU, Multilingual MMLU, SWE-bench Verified, SWE-Lancer, Aider polyglot, MultiChallenge, COLLIE, IFEval, Multi-IF, OpenAI-MRCR, Graphwalks, MMMU, MathVista, CharXiv, ComplexFuncBench, Taubench. An internal instruction-following eval was also reported and is not counted.
- O3: AIME 2024, AIME 2025, Codeforces, GPQA Diamond, HLE, MMMU, MathVista, CharXiv-Reasoning, SWE-Lancer, SWE-Bench Verified (n = 477), Aider Polyglot, Scale MultiChallenge, BrowseComp, Tau-bench.
- O4: Codeforces, HLE, HealthBench (+Hard), AIME 2024, AIME 2025, GPQA Diamond, MMLU, Tau-Bench Retail.
- O5: AIME 2025, FrontierMath Tier 1–3, HMMT, GPQA Diamond, HLE, SWE-bench Verified (n = 477), Aider Polyglot, Scale MultiChallenge, BrowseComp, COLLIE, Tau2-bench, MMMU, MMMU Pro, VideoMMMU, CharXiv-Reasoning, ERQA, HealthBench (+Hard, Hallucinations). "Economically important tasks" was an internal metric, not counted.
- O6: GDPval, SWE-Bench Pro, SWE-bench Verified, SWE-Lancer, GPQA Diamond, CharXiv, AIME 2025, HMMT, FrontierMath T1–3 and T4, ARC-AGI-1 and -2 (Verified), HLE, MMMLU, OpenAI MRCRv2, Graphwalks, BrowseComp Long Context, MMMU Pro, Video MMMU, Screenspot Pro, Tau2-bench, BrowseComp, Scale MCP-Atlas, Toolathlon.
- O7: SWE-Bench Pro, Terminal-Bench 2.0, OSWorld-Verified, GDPval, Cybersecurity CTF, SWE-Lancer.
- O8: GDPval, FinanceAgent v1.1, OfficeQA, SWE-Bench Pro, Terminal-Bench 2.0, OSWorld-Verified, MMMU Pro, OmniDocBench, BrowseComp, MCP Atlas, Toolathlon, Tau2 Telecom, Frontier Science Research, FrontierMath, GPQA Diamond, HLE, Graphwalks, MRCR v2, ARC-AGI-1 and -2. WebArena-Verified and Online-Mind2Web appear in text only.
- O9: Terminal-Bench 2.0, GDPval, OSWorld-Verified, Toolathlon, BrowseComp, FrontierMath, CyberGym, SWE-Bench Pro, FinanceAgent v1.1, OfficeQA Pro, MMMU Pro, MCP Atlas, GeneBench, BixBench, GPQA Diamond, HLE, Graphwalks, MRCR v2, ARC-AGI-1 and -2. Internal evals (Expert-SWE, investment banking, CTF) were also reported and are not counted.

**Google**
- G1: LiveCodeBench, Aider Polyglot, SWE-bench Verified, GPQA, HLE, SimpleQA, FACTS Grounding, Global MMLU (Lite), ECLeKTic, AIME 2025, HiddenMath-Hard, LOFT, MRCR-V2, MMMU, Vibe-Eval, ZeroBench, BetterChartQA.
- G2: HLE, ARC-AGI-2, GPQA Diamond, AIME 2025, MathArena Apex, MMMU-Pro, ScreenSpot-Pro, CharXiv Reasoning, OmniDocBench 1.5, Video-MMMU, LiveCodeBench Pro, Terminal-Bench 2.0, SWE-Bench Verified, τ2-bench, Vending-Bench 2, FACTS Benchmark Suite, SimpleQA Verified, MMMLU, Global PIQA, MRCR v2.
- G3: HLE, ARC-AGI-2, GPQA Diamond, Terminal-Bench 2.0, SWE-Bench Verified, SWE-Bench Pro (Public), LiveCodeBench Pro, SciCode, APEX-Agents, GDPval-AA, τ2-bench, MCP Atlas, BrowseComp, MMMU Pro, MMMLU, MRCR v2.
- G4: Terminal-bench 2.1, SWE-Bench Pro, MCP Atlas, Toolathlon, OSWorld-Verified, Finance Agent v2, GDPval-AA, CharXiv Reasoning, MMMU-Pro, Blueprint-Bench 2, MRCR v2, HLE, ARC-AGI-2.

**Others**
- M1:
  - Pre-trained: MMLU, MMLU-Pro, MATH, MBPP, TydiQA, ChartQA, DocVQA.
  - Instruct: MMMU, MMMU Pro, MathVista, ChartQA, DocVQA, LiveCodeBench, MMLU Pro, GPQA Diamond, MGSM, MTOB.
- D1: MMLU, MMLU-Redux, MMLU-Pro, DROP, IF-Eval, GPQA-Diamond, SimpleQA, FRAMES, LongBench v2, HumanEval-Mul, LiveCodeBench, Codeforces, SWE Verified, Aider-Edit/Polyglot, AIME 2024, MATH-500, CNMO 2024, CLUEWSC, C-Eval, C-SimpleQA, Arena-Hard, AlpacaEval 2.0.
- D2: D1's set minus LongBench v2, HumanEval-Mul and Aider-Edit.
- D3: MMLU-Pro, GPQA-Diamond, HLE, LiveCodeBench, AIME 2025, HMMT 2025, Codeforces, Aider-Polyglot, BrowseComp, BrowseComp-zh, SimpleQA, SWE Verified, SWE-bench Multilingual, Terminal-bench.
- K1: LiveCodeBench v6, OJBench, MultiPL-E, SWE-bench Verified, SWE-bench Multilingual, TerminalBench, Aider-Polyglot, Tau2, AceBench, AIME 2024, AIME 2025, MATH-500, HMMT 2025, CNMO 2024, PolyMath-en, ZebraLogic, AutoLogi, GPQA-Diamond, SuperGPQA, HLE, MMLU, MMLU-Redux, MMLU-Pro, IFEval, Multi-Challenge, SimpleQA, LiveBench. Base-model tables were not counted.
- X1: AIME 2024, AIME 2025, MATH-500, LiveCodeBench, FullStackBench, GPQA Diamond, HLE, ZebraLogic, MMLU-Pro, SWE-bench Verified, OpenAI-MRCR, LongBench-v2, TAU-bench, SimpleQA, MultiChallenge.
- X2: SWE-bench Verified, Multi-SWE-Bench, SWE-bench Multilingual, Terminal-Bench, ArtifactsBench, BrowseComp, BrowseComp-zh, GAIA (text only), xbench-DeepSearch, HLE, τ²-Bench, FinSearchComp-global, AgentCompany. It also reports an "Artificial Analysis" block: AIME25, MMLU-Pro, GPQA-Diamond, HLE, LiveCodeBench, SciCode, IFBench, AA-LCR, τ²-Bench-Telecom, Terminal-Bench-Hard, and the AA Intelligence index.

### A.3 Benchmark → releases (families in ≥ 3 releases) [D]

The half-year columns count only OpenAI, Anthropic and Google (frontier-3) releases: 6 in 2025H1, 8 in 2025H2, 11 in 2026H1 and 2 in 2026H2.

| Benchmark family | Releases (of 34) | Orgs | 2025H1 | 2025H2 | 2026H1 | 2026H2 | Release IDs |
|---|---|---|---|---|---|---|---|
| GPQA Diamond | 27 | 7 | 6/6 | 8/8 | 6/11 | 0/2 | A1–A9, O1–O6, O8, O9, G1–G3, M1, D1–D3, K1, X1, X2 |
| SWE-bench Verified | 23 | 6 | 6/6 | 7/8 | 4/11 | 0/2 | A1–A9, O1–O3, O5, O6, G1–G3, D1–D3, K1, X1, X2 |
| Humanity's Last Exam | 22 | 6 | 2/6 | 4/8 | 10/11 | 2/2 | A7–A12, O3–O6, O8, O9, G1–G4, D3, K1, X1, X2 |
| Terminal-Bench\* | 21 | 6 | 1/6 | 5/8 | 11/11 | 1/2 | A2–A10c, A12, O7–O9, G2–G4, D3, K1, X2 |
| AIME\* | 19 | 6 | 6/6 | 7/8 | 0/11 | 0/2 | A1–A5, O1–O6, G1, G2, D1–D3, K1, X1, X2 |
| τ-/τ²-bench\* | 19 | 5 | 4/6 | 8/8 | 4/11 | 0/2 | A1–A8, O2–O6, O8, G2, G3, K1, X1, X2 |
| OSWorld\* | 15 | 3 | 0/6 | 3/8 | 10/11 | 2/2 | A4–A12, O7–O9, G4 |
| MMMLU | 14 | 3 | 4/6 | 6/8 | 4/11 | 0/2 | A1–A9, O1, O2, O6, G2, G3 |
| GDPval\* (incl. GDPval-AA) | 13 | 3 | 0/6 | 1/8 | 10/11 | 2/2 | A7, A8, A10–A12, O6–O9, G3, G4 |
| MMMU (original) | 12 | 4 | 6/6 | 5/8 | 0/11 | 0/2 | A1–A6, O1–O3, O5, G1, M1 |
| BrowseComp | 12 | 5 | 1/6 | 2/8 | 6/11 | 1/2 | A7–A9, A11, O3, O5, O6, O8, O9, G3, D3, X2 |
| ARC-AGI\* | 10 | 3 | 0/6 | 3/8 | 6/11 | 1/2 | A6–A8, A11, O6, O8, O9, G2–G4 |
| MMMU-Pro | 10 | 4 | 0/6 | 3/8 | 6/11 | 0/2 | A7, A8, O5, O6, O8, O9, G2–G4, M1 |
| SWE-bench Pro | 10 | 3 | 0/6 | 1/8 | 9/11 | 0/2 | A9–A10c, O6–O9, G3, G4 |
| MCP Atlas | 9 | 3 | 0/6 | 2/8 | 7/11 | 0/2 | A6–A9, O6, O8, O9, G3, G4 |
| Finance Agent\* | 8 | 3 | 0/6 | 1/8 | 7/11 | 0/2 | A4, A7–A10, O8, O9, G4 |
| SimpleQA (incl. Verified) | 8 | 5 | 2/6 | 1/8 | 0/11 | 0/2 | O1, G1, G2, D1–D3, K1, X1 |
| Aider Polyglot | 8 | 4 | 3/6 | 1/8 | 0/11 | 0/2 | O2, O3, O5, G1, D1–D3, K1 |
| LiveCodeBench | 8 | 5 | 1/6 | 0/8 | 0/11 | 0/2 | G1, M1, D1–D3, K1, X1, X2 |
| CharXiv Reasoning | 7 | 3 | 2/6 | 3/8 | 2/11 | 0/2 | A9, O2, O3, O5, O6, G2, G4 |
| MMLU-Pro | 7 | 4 | 0/6 | 0/8 | 0/11 | 0/2 | M1, D1–D3, K1, X1, X2 (open-weight only) |
| MMLU | 6 | 4 | 1/6 | 1/8 | 0/11 | 0/2 | O2, O4, M1, D1, D2, K1 |
| IFEval | 5 | 4 | 2/6 | 0/8 | 0/11 | 0/2 | A1, O2, D1, D2, K1 |
| MATH-500 | 5 | 4 | 1/6 | 0/8 | 0/11 | 0/2 | A1, D1, D2, K1, X1 |
| SWE-Lancer | 5 | 1 | 3/6 | 1/8 | 1/11 | 0/2 | O1–O3, O6, O7 (creator only) |
| MultiChallenge | 5 | 3 | 2/6 | 1/8 | 0/11 | 0/2 | O2, O3, O5, K1, X1 |
| OpenAI-MRCR | 5 | 2 | 1/6 | 1/8 | 2/11 | 0/2 | O2, O6, O8, O9, X1 |
| Codeforces (Elo) | 5 | 2 | 1/6 | 1/8 | 0/11 | 0/2 | O3, O4, D1–D3 |
| FrontierMath | 4 | 1 | 0/6 | 2/8 | 2/11 | 0/2 | O5, O6, O8, O9 (OpenAI only) |
| Graphwalks | 4 | 1 | 1/6 | 1/8 | 2/11 | 0/2 | O2, O6, O8, O9 (OpenAI only) |
| MRCR v2 (Google) | 4 | 1 | 1/6 | 1/8 | 2/11 | 0/2 | G1–G4 (Google only) |
| HealthBench\* | 4 | 2 | 0/6 | 2/8 | 1/11 | 1/2 | O4, O5, A10b, A11 |
| Toolathlon | 4 | 2 | 0/6 | 1/8 | 3/11 | 0/2 | O6, O8, O9, G4 |
| HMMT | 4 | 3 | 0/6 | 2/8 | 0/11 | 0/2 | O5, O6, D3, K1 |
| AutomationBench | 3 | 1 | 0/6 | 0/8 | 1/11 | 2/2 | A10b, A11, A12 |
| FrontierCode\* | 3 | 1 | 0/6 | 0/8 | 1/11 | 2/2 | A10b, A11, A12 |

**Single-release families (48).** AA-LCR, APEX-Agents, AceBench, ArtifactsBench, AutoLogi, BetterChartQA, BixBench, ChartQA, Chartography, ComplexFuncBench, CursorBench 4.0, DeepSWE v1.1, DocVQA, ECLeKTic, ERQA, ExploitBench, FinSearchComp, Frontier-Bench v0.1, FrontierScience, FullStackBench, GAIA, GDP.pdf, GeneBench, Global MMLU, Global PIQA, HiddenMath, HumanEval, IFBench, LOFT, LiveBench, MATH, MBPP, MGSM, MTOB, MathArena Apex, Multi-IF, Multi-SWE-Bench, MultiPL-E, OJBench, PolyMath, SuperGPQA, Terminal-Bench-Science 0.1, TheAgentCompany, TydiQA, Vending-Bench 2, Vibe-Eval, ZeroBench, xbench-DeepSearch. [D]

### A.4 Table churn (consecutive releases of the same lab) [D]

"Retained" means the share of the earlier release's benchmark families that appear in the next release.

| Lab | Transition | Jaccard | Retained |
|---|---|---|---|
| Anthropic | 3.7 Sonnet → Claude 4 | 0.67 | 0.75 |
| Anthropic | Claude 4 → Opus 4.1 | 1.00 | 1.00 |
| Anthropic | Opus 4.1 → Sonnet 4.5 | 0.78 | 1.00 |
| Anthropic | Sonnet 4.5 → Haiku 4.5 | 0.89 | 0.89 |
| Anthropic | Haiku 4.5 → Opus 4.5 | 0.70 | 0.88 |
| Anthropic | Opus 4.5 → Opus 4.6 | 0.57 | 0.89 |
| Anthropic | Opus 4.6 → Sonnet 4.6 | 1.00 | 1.00 |
| Anthropic | Sonnet 4.6 → Opus 4.7 | 0.56 | 0.69 |
| Anthropic | Opus 4.7 → Opus 4.8 | 0.38 | 0.42 |
| Anthropic | Opus 4.8 → Fable 5 | 0.36 | 0.83 |
| Anthropic | Fable 5 → Sonnet 5 | 0.38 | 0.38 |
| Anthropic | Sonnet 5 → Opus 5 | 0.21 | 0.60 |
| Anthropic | Opus 5 → Opus 5.5 | 0.31 | 0.42 |
| OpenAI | GPT-5 → GPT-5.2 | 0.41 | 0.65 |
| OpenAI | GPT-5.2 → GPT-5.3-Codex | 0.13 | 0.14 |
| OpenAI | GPT-5.3-Codex → GPT-5.4 | 0.20 | 0.80 |
| OpenAI | GPT-5.4 → GPT-5.5 | 0.73 | 0.84 |
| Google | Gemini 2.5 → 3 Pro | 0.23 | 0.41 |
| Google | Gemini 3 Pro → 3.1 Pro | 0.38 | 0.50 |
| Google | Gemini 3.1 Pro → 3.5 Flash | 0.38 | 0.50 |

- **Anthropic long-run overlap.** Families from Claude 3.7 Sonnet's table still present in each later Anthropic table:

  | Release | Overlap with Claude 3.7 Sonnet families |
  |---|---|
  | Claude 4 | 6/7 |
  | Sonnet 4.5 | 6/9 |
  | Opus 4.5 | 5/9 |
  | Opus 4.6 | 4/13 |
  | Opus 4.7 | 3/12 |
  | Opus 4.8, Fable 5, Sonnet 5, Opus 5, Opus 5.5 | **0** |

- **Google.** Only about half of each Gemini table survives into the next.
  - Gemini 3 Pro (Nov 2025) → 3.1 Pro (Feb 2026) dropped AIME 2025, MathArena Apex, ScreenSpot-Pro, CharXiv, OmniDocBench, Video-MMMU, Vending-Bench 2, FACTS, SimpleQA Verified and Global PIQA.
  - It added SWE-Bench Pro, SciCode, APEX-Agents, GDPval-AA, MCP Atlas and BrowseComp.
  - Gemini 3.5 Flash (May 2026) then dropped GPQA Diamond, SWE-Bench Verified, MMMLU, τ2-bench, BrowseComp, LiveCodeBench Pro, SciCode and APEX-Agents. [P]

### A.5 Coverage gaps (not in the matrix)

- **xAI Grok 4** (July 2025). x.ai was blocked.
  - Sibling evidence: "Grok 4 Heavy scored 44.4% on HLE with tools". [Sib: knowledge_exams.md, via TechCrunch search summary; M]
  - ARC Prize's 2025 report names xAI among four labs that "reported ARC-AGI performance in public model cards in 2025". [Mi, H]
  - Competitors' tables show xAI-reported numbers: Anthropic's Feb 2025 table has Grok 3 Beta scores on GPQA, MMMU and AIME 2024. [P]
  - The Akhtar dataset lists Grok-4 in top-5 entries for GPQA (87.7), MATH-500 (99.0), ARC-AGI (66.7), Global MMLU (91.1) and LegalBench (83.4). [P]
- **Alibaba Qwen3** (April 2025; 2507 updates July–Aug 2025).
  - The QwenLM/Qwen3 README contains no tables; it points to blogs (blocked) and the technical report. [P]
  - A sibling reports that MMLU-Redux is in the Qwen3 technical report. [Sib: knowledge_exams.md, M]
  - The Akhtar dataset lists Qwen3-235B top-5 entries on MCLM (80.8), C-Eval (89.6) and MMLU-Redux (93.8, Thinking-2507). [P]
- **Zhipu GLM.** The README text for GLM-4.7 names SWE-bench, SWE-bench Multilingual, Terminal Bench 2.0, τ²-Bench, BrowseComp and HLE. The tables are images and were not counted. [P]
  - The GLM-4.5 README says it was evaluated "across 12 industry-standard benchmarks" (arXiv:2508.06471). [P]

---

## B. Lifecycle data: release → saturation, and the shrinking window

### B.1 Pre-LLM baseline: Kiela et al. 2021 (Dynabench), Figure 1 [P-figure, M]

- Caption: "Benchmark saturation over time for popular benchmarks, normalized with initial performance at minus one and human performance at zero." Reproduced with this caption in the KAUST course repository.
- My approximate readings of when each series first reaches 0 (human parity):

| Benchmark | First point | ≈ Reaches human parity | ≈ Years |
|---|---|---|---|
| MNIST | 1998 | about 2013–2015 | about 15–17 |
| Switchboard | 1998 | about 2017 | about 19 |
| ImageNet | 2009 | about 2015 | about 6 |
| SQuAD 1.1 | 2016 | about 2018 | about 2 |
| SQuAD 2.0 | 2018 | about 2019 | about 1 |
| GLUE | 2018 | about 2019 | about 1 |

- These are visual readings of a plotted figure. Cite the figure, not my numbers.

### B.2 Community "time-to-kill" dataset [S, L-M]

The Killed-by-LLM `data.ts` (R0bk/killedbyllm) lists creation and "defeat" months. The "defeat" criteria vary (human baseline versus near-ceiling), and there are internal inconsistencies. For example, IFEval is "defeated" in 2024-03 by Llama 3.3 70B, a model released later.

| Benchmark | Created | Defeated | Months |
|---|---|---|---|
| GLUE | 2018-05 | 2019-06 | 13 |
| SuperGLUE | 2019-05 | 2019-10 | 5 |
| SQuAD v2.0 | 2018-05 | 2019-04 | 11 |
| BIG-Bench | 2021-06 | 2022-04 | 10 |
| BIG-Bench-Hard | 2022-10 | 2024-06 | 20 |
| GSM8K | 2021-10 | 2023-11 | 25 |
| MMLU | 2020-09 | 2023-03 | 30 |
| HumanEval | 2021-07 | 2024-05 | 34 |
| MATH | 2021-03 | 2024-09 | 42 |
| HellaSwag | 2019-05 | 2023-03 | 46 |
| ARC-AGI (v1) | 2019-11 | 2024-12 | 61 |

The Esposito & Zhang (2026) working paper states that SuperGLUE reached superhuman performance "within eighteen months", citing Srivastava et al. (2023). This conflicts with the 5-month entry above. The definitions differ: T5 at 89.3 against 89.8 human counts as "defeat" in one source, and later models passing the human baseline count in the other. [Mi, M]

### B.3 LLM-era rates from official sources

- **AI Index 2025** [Mi-scrape of hai.stanford.edu, M-H]:
  - "In 2023, researchers introduced new benchmarks—MMMU, GPQA, and SWE-bench… Just a year later, performance sharply increased: scores rose by 18.8, 48.9, and 67.3 percentage points".
  - "the score difference between the top and 10th-ranked models fell from 11.9% to 5.4% in a year, and the top two are now separated by just 0.7%."
- **AI Index 2026** [S, chapter summaries on GitHub; M]:
  - HLE: "frontier models gained 30 percentage points in a single year".
  - OSWorld: accuracy "rose from 12% to 66.3%".
  - The top 15 MMLU-Pro models are all above 87% with about a 4-point spread.
  - "developer-reported results sometimes outperform independent third-party evaluations".
- **Anthropic engineering (9 Jan 2026)** [P, H]:
  - "LLMs have progressed from 40% to >80% on this eval in just one year" (SWE-bench Verified).
  - "SWE-Bench Verified scores started at 30% this year, and frontier models are now nearing saturation at >80%." The two statements are inconsistent about the starting point; quote the specific sentence used.
- **OpenAI (23 Feb 2026)** [Mi, H]: SWE-bench Verified SOTA was "improving from 74.9% to 80.9% in the last 6 months".

### B.4 Headline-benchmark lifetimes measured from lab tables [D from P/Mi]

| Benchmark | Public release | Adopted in headline tables | Ceiling / last frontier headline appearance | Headline lifetime |
|---|---|---|---|---|
| AIME 2025 | Feb 2025 exam [Sib] | o3, Apr 2025 (88.9%) | Sonnet 4.5 100% w/ python (Sep 2025); Gemini 3 Pro 100% w/ code (Nov 2025); **GPT-5.2 100% no tools (11 Dec 2025)**; 0/13 frontier tables in 2026 | about 8 months |
| τ²-bench | 10–12 Jun 2025 [P Akhtar data; Sib] | GPT-5 Aug 2025 (telecom 96.7%) | Opus 4.6 99.3% telecom (Feb 2026); last GPT-5.4, Mar 2026 (98.9%) | about 7 months |
| MMMU (val) | 2023 (AI Index) | throughout 2025 | GPT-5.1 85.4% (Opus 4.5 table, Nov 2025); last Opus 4.5, 24 Nov 2025 | replaced by MMMU-Pro / CharXiv |
| SWE-bench Verified | 13 Aug 2024 [Sib] | Claude 3.5 Sonnet (new), Oct 2024 [Sib] | OpenAI stopped Feb 2026; last Opus 4.7 at 87.6%, Apr 2026 (Mythos Preview 93.9%) | about 18–20 months |
| GPQA Diamond | Nov 2023 [Sib] | 2024 (Claude 3, o1) [Sib] | about 94% (GPT-5.4 Pro 94.4%, Mythos Preview 94.6%, Gemini 3.1 Pro 94.3%); last Apr 2026 | about 29 months |
| MMMLU | Sep 2024 [P Akhtar data] | Claude 3.7 Sonnet, Feb 2025 | about 89–92% plateau; last Apr 2026 | about 19 months |
| ARC-AGI-2 | 24 Mar 2025 [P changelog; Sib] | Gemini 3 Pro 31.1% / Opus 4.5 37.6% (Nov 2025) | GPT-5.5 85.0% (Apr 2026); Anthropic replaced it with ARC-AGI-3 in Jul 2026 | 8 months to adoption; about 16 months to replacement |
| Terminal-Bench (per version) | TB1 about Apr–May 2025; TB2.0 7 Nov 2025; TB2.1 by May 2026; TB4.0 by Sep 2026 | same month as each release | TB2.0 82.7% (GPT-5.5); TB2.1 88.0% (Fable 5) | **a new major version about every 4–6 months** |

Pattern [I, M-H]:
- The LLM-era headline lifetime of a *static* benchmark is now **about 7–30 months**.
- Math-competition and τ²-style benchmarks die fastest; expert multiple-choice (GPQA) lasts longest.
- Benchmarks survive past saturation only by **re-versioning under the same brand**.

### B.5 Akhtar et al. (ICML 2026): systematic saturation evidence [P, H]

- **Data.** 60 text benchmarks (ages 1–114 months). The candidate pool was 190 benchmarks named in 61 official developer reports (Jan 2022 to Nov 2025) from OpenAI, Anthropic, Google, Meta, Alibaba and others. Benchmarks were kept if they appeared in at least 5 reports.
- **Findings.**
  - "nearly half of our benchmarks exhibit saturation, with rates increasing with age".
  - After controlling for age, citation counts are not associated with saturation (ρ = 0.22, p = 0.12), nor are citation growth (ρ = 0.13, p = 0.37) or "frequency of appearance in technical reports (ρ = 0.05, p = 0.73)".
  - In the joint Bayesian model, "benchmark age and test set size show the most consistent effects".
  - Private test sets (N = 4), output format and templating show no reliable effect.
  - "expert-curated benchmarks show lower saturation at comparable ages".
- **Companion data (evaleval/benchmark-saturation, `data/manual_annotation_data.csv`)** gives launch SOTA against the top model in late 2025:

  | Benchmark | SOTA at release | Top model, late 2025 | Months since release |
  |---|---|---|---|
  | MATH-500 | 6.9 (GPT-2) | 99.2 (o3) | 57 |
  | GPQA | 38.8 (GPT-4) | 87.7 (Grok 4) | 25 |
  | MMLU | 43.9 (GPT-3) | 93.5 (GPT-5) | 63 |
  | GSM8K | 55 (GPT-3) | 97.3 | 50 |
  | HumanEval | 28.81 (Codex-12B) | 94.5 | 53 |
  | LiveCodeBench | 29.1 | 91.7 (Gemini 3 Pro) | 21 |
  | HLE | 13.4 (o3-mini-high) | 37.72 (Gemini 3 Pro preview) | 11 |
  | AIME 2025 | 26 | 99.0 (GPT-5.2) | 10 |
  | τ²-bench | 55 (GPT-4.1) | 85.4 (Gemini 3 Pro) | 6 |
  | FrontierMath | 2 (o1) | 29.2 (GPT-5.2 Pro) | 16 |

  - Terminal-Bench 2.0 is rated "Very high" saturation (S = 0.97) at age 1 month, with n = 82. This shows that the S-index also flags **small test sets on which the top models tie**, not only ceilings.
  - Caveat: some rows mix variants. The SWE-bench row lists Verified-style scores against the full-set paper.

---

## C. From obscure to universal: case studies and triggers

| Benchmark | Obscure phase | Trigger(s) | Universal phase (evidence) |
|---|---|---|---|
| **ARC-AGI** | 2019 release. Small Kaggle and ARCathon prizes 2020–23 [Sib] | **ARC Prize 2024** (launched 11 Jun 2024; $600K Grand Prize; 1,430 teams) [Sib]. **o3-preview 75.7% / 87.5%**, co-announced with ARC on 20 Dec 2024 [Sib]. ARC then verified lab scores | "four frontier AI labs (Anthropic, Google DeepMind, OpenAI, and xAI) reported ARC-AGI performance on model cards" in 2025, "establishing ARC-AGI as an industry standard" [Mi, H]. 10/34 releases in my matrix, all verified runs ("ARC Prize Verified") [P] |
| **SWE-bench** | Oct 2023 (ICLR 2024). Early scores were in single digits [Sib] | **OpenAI Preparedness co-built SWE-bench Verified** (13 Aug 2024). The agentic-coding product race | OpenAI: it "became a standard metric reported in frontier model releases" [Mi, H]. 23/34 releases [D]. Retired Feb 2026 |
| **Terminal-Bench** | Repo created Jan 2025 [Sib] | **Anthropic headline adoption on day one** (Claude 4, 22 May 2025: 43.2%) [P]. Terminal coding agents (Claude Code, Codex CLI). Lab task contributions and a public harness (Terminus) [Sib] | 11/11 frontier releases in 2026H1 [D]. "used by virtually all frontier labs" (README, self-report) [Sib] |
| **τ-bench / τ²-bench** | Jun 2024, Sierra (a startup) [Sib] | **Early Anthropic adoption** (Claude 3.5 Sonnet new / 3.7 Sonnet tables) [P/Sib]. The telecom dual-control domain in τ² (Jun 2025) | 19/34 releases across 5 orgs [D]. Died by 2026H2 at 98–99% telecom |
| **Humanity's Last Exam** | Never obscure: launched 24 Jan 2025 with branding [Sib] | Name ("Last Exam"), launch headroom (<10%), **CAIS + Scale + a Scale leaderboard** that labs cite for competitors [P: Gemini 2.5/3 notes], a Nature paper [Sib] | 22/34 releases; 12/13 frontier tables in 2026 [D] |
| **GDPval** | OpenAI, Sep–Oct 2025, expert-graded [Sib] | **Artificial Analysis turned it into GDPval-AA**: an automated LLM-judge Elo leaderboard [Sib]. The "economic value" narrative | 0/14 frontier tables in 2025 → 12/13 in 2026 [D] (as GDPval or GDPval-AA v2/v2.1) |
| **OSWorld** | Apr 2024 (NeurIPS 2024); launch best 12.24% vs human 72.36% [Sib] | Anthropic computer-use products. **OSWorld-Verified (Jul 2025), fixed with participation from Moonshot, OpenAI, Anthropic, ByteDance and others** [Sib] | 0/6 → 3/8 → 10/11 → 2/2 frontier tables by half-year [D]. Re-versioned as 2.0 and 2.1 |
| **BrowseComp** | OpenAI, Apr 2025 [Sib] | Open-sourced in simple-evals (still maintained after the Jul 2025 freeze) [P]. The rise of deep-research products | Open-weight labs adopted it first (DeepSeek V3.2-Exp, MiniMax-M2, GLM). Anthropic and Google followed in Feb 2026 [P/D] |
| **SWE-bench Pro** | Scale, 21 Sep 2025 [Sib] | **OpenAI's Feb 2026 recommendation** as the Verified replacement [Mi] | 1/14 → 9/11 frontier tables (2025 → 2026H1) [D] |
| **AIME** | A long-standing exam | **OpenAI o1 (Sep 2024)** made it the "reasoning-model" headline [Sib] | 13/14 frontier tables in 2025. Dead in 2026 after 100% [D/P] |

**Lag from public release to first headline adoption** [D]:
- **Weeks** for new versions of an already-adopted brand, or for lab co-developed sets:
  - Terminal-Bench 2.0: 7 Nov 2025 → Opus 4.5 on 24 Nov 2025 and Gemini 3 Pro in Nov 2025.
  - OSWorld 2.0: 26 Jun 2026 → Opus 5 on 24 Jul 2026.
  - Terminal-Bench 1.0 → Claude 4.
- **About 2–3 months** for new independent benchmarks with headroom and a leaderboard:
  - τ²-bench → GPT-5.
  - HLE → o3.
  - SWE-bench Verified → Claude 3.5 Sonnet (new).
  - SWE-bench Pro → GPT-5.2.
- **About 5–10 months** when the benchmark was created by a competitor (BrowseComp: OpenAI Apr 2025 → Anthropic and Google Feb 2026), or when launch scores were near zero (ARC-AGI-2: Mar → Nov 2025).

---

## Benchmark-by-benchmark

### 1. GPQA Diamond
- **Measures:** graduate-level, "Google-proof" multiple-choice science questions (biology, physics, chemistry). [Sib]
- **Release / creators:**
  - arXiv:2311.12022 (Nov 2023), COLM 2024.
  - Rein, Hou, Stickland, Petty, Pang, Dirani, Michael, Bowman. [Sib: knowledge_exams.md]
- **Items / format:** Diamond is 198 four-option multiple-choice items. [Sib]
- **Launch vs. latest:**
  - GPT-4 39% (Nov 2023). [Sib]
  - Latest frontier scores:
    - GPT-5.4 Pro 94.4% (Mar 2026) [Mi]
    - Claude Mythos Preview 94.6% and Opus 4.7 94.2% (Apr 2026) [P]
    - Gemini 3.1 Pro 94.3% (Feb 2026) [P]
    - GPT-5.5 93.6% (Apr 2026) [Mi]
- **Adoption:**
  - The most-reported benchmark in the matrix: 27/34 releases, all 7 orgs. [D]
  - It was in every frontier table in 2025 (14/14) and in none after Apr 2026:
    - Anthropic dropped it at Opus 4.8.
    - Google dropped it at Gemini 3.5 Flash.
    - OpenAI still had it in GPT-5.5. [D]
  - Epoch found that labs' self-reports fall within its confidence intervals. [Sib]
- **Status:** saturated at about 94%, near the estimated valid-item ceiling of about 90–95%. [Sib]
- **Why it succeeded:**
  - Expert validation plus a non-expert failure filter.
  - Cheap to run (198 items).
  - Arrived just before reasoning models.
  - Gated distribution. [Sib, I]
- **Why it is failing:**
  - The ceiling has been reached.
  - The small n (198) cannot resolve 1–2 point frontier gaps. [Sib]
- **Sources:**
  - Anthropic and Google tables (References 7–20, 33–37).
  - OpenAI GPT-5.4 and GPT-5.5 mirrors.
  - knowledge_exams.md.

### 2. SWE-bench Verified (→ SWE-bench Pro)
- **Measures:** resolving real GitHub issues in 12 Python repositories, checked by hidden tests. The set is a 500-task human-screened subset. [Mi; Sib]
- **Release / creators:**
  - SWE-bench: Jimenez et al., ICLR 2024.
  - Verified: OpenAI Preparedness together with the SWE-bench authors, 13 Aug 2024.
  - 93 developers screened 1,699 samples. [Sib; Mi]
- **Launch vs. latest:**
  - GPT-4o 33.2% at Verified launch. [Sib]
  - Latest: Opus 4.7 87.6% and Mythos Preview 93.9% (Apr 2026). [P]
  - OpenAI reported on a fixed n = 477 subset (o3 69.1%, GPT-5 74.9%). Anthropic reported on all 500 ("Scores for OpenAI models are reported out of a 477 problem subset"). [P, Mi]
- **Adoption:** 23/34 releases. OpenAI: it "became a standard metric reported in frontier model releases". [Mi, H]
- **Status:** **contaminated / retired.** OpenAI's audit:
  - "at least 59.4% of the audited problems have flawed test cases".
  - "all frontier models we tested were able to reproduce the original, human-written bug fix".
  - "we have stopped reporting SWE-bench Verified scores, and we recommend that other model developers do so too… OpenAI recommends reporting results for SWE-bench Pro." [Mi, H]
  - Anthropic kept it through Opus 4.7, with a memorization screen footnote: "Our memorization screens flag a subset of problems… Excluding any problems that show signs of memorization, Opus 4.7's margin of improvement over Opus 4.6 holds." [P]
- **Why it succeeded:**
  - A real-world task.
  - Human validation.
  - Lab (Preparedness) sponsorship.
  - The cheap 500-task size.
  - It rode the agentic-coding product wave. [Sib, I]
- **Why it failed:**
  - Public GitHub provenance, so contamination.
  - Flawed tests.
  - Python-only.
  - Scaffold and subset (477 vs 500) differences made cross-lab numbers non-comparable. [Mi; P]
- **Successor:** SWE-bench Pro (Scale; 1,865 problems, 731 public). [Sib]
  - Adopted by 9/11 frontier releases in 2026H1. [D]
  - Latest headline: Claude Mythos 5 / Fable 5 at 80.3% (Jun 2026). [P]
  - Launch-era frontier: GPT-5.2 55.6% (Dec 2025). [Mi]

### 3. Humanity's Last Exam (HLE)
- **Measures:** frontier expert-level, closed-ended academic questions; about 14% multimodal. [Sib]
- **Release / creators:**
  - arXiv:2501.14249 (24 Jan 2025).
  - CAIS, Scale AI and a contributor consortium.
  - Nature 649 (2026). [Sib]
- **Items:** 2,500 public questions. [Sib]
- **Launch vs. latest:**
  - o1 8.0% at launch [Sib]; 13.4 (o3-mini-high) as SOTA-at-release in the Akhtar data. [P]
  - Latest, no tools: Claude Mythos 5 / Fable 5 59.0% (Jun 2026). [P]
  - Latest, with tools: Claude Opus 5.5 67.7% (Sep 2026). [P]
- **Adoption:**
  - 22/34 releases. [D]
  - Present in 10/11 frontier tables in 2026H1 and 2/2 in 2026H2. [D]
  - Labs cite **Scale's leaderboard** for competitor numbers: "Humanity's Last Exam results for Gemini 2.5 Pro and Claude Sonnet 4.5 are from ScaleAI leaderboard & GPT-5.1 from Artificial Analysis" (Gemini 3 Pro PDF). [P]
- **Status:** **thriving but contested.** Epoch rated it "Flawed" (Sep 2026) [Sib], and CAIS responded with HLE-Rolling and HLE-Diamond. [Sib]
  - With-tools and no-tools variants diverge by 8–15 points. Labs now use domain blocklists: "A domain blocklist was used to decontaminate eval results" (Anthropic Opus 4.6); "a blocklist … to avoid results that could include benchmark numbers like huggingface.com" (Gemini 3). [P]
- **Why it succeeded:**
  - Branding.
  - Launch headroom.
  - Prize-funded expert crowdsourcing.
  - A third-party leaderboard.
  - A Nature paper.
  - Active maintenance. [Sib, I]
- **Why it is failing:**
  - The adversarial filter admits wrong items (29–46% suspect in audits).
  - Search-time contamination.
  - Tool-variant ambiguity. [Sib]

### 4. AIME (2024, 2025)
- **Measures:** 30 integer-answer competition math problems per year. [Sib]
- **Launch vs. latest:**
  - o3 88.9% and o4-mini 92.7% on AIME 2025 (Apr 2025). [Mi]
  - 100% for GPT-5.2 (no tools, Dec 2025) [Mi], Gemini 3 Pro (with code execution, Nov 2025) [P] and Sonnet 4.5 (python, Sep 2025). [P]
- **Adoption:**
  - 19/34 releases.
  - 13/14 frontier tables in 2025 → **0/13 in 2026**. [D]
- **Status:** **saturated / contaminated.** AIME 2024 is "significantly contaminated" (MathArena) [Sib]; the successors (HMMT, MathArena Apex, FrontierMath) are themselves niche in lab tables. [D]
- **Why it succeeded:**
  - Human anchoring and prestige.
  - Trivially gradable.
  - A new edition every year.
  - The o1 "reasoning moment". [Sib]
- **Why it failed:**
  - n = 30.
  - Guessable integer answers.
  - Near-duplicates online.
  - It hit 100%. [Sib; P]

### 5. τ-bench / τ²-bench (Sierra)
- **Measures:** a tool-agent-user loop with policy documents, judged on final database state. Also reports pass^k reliability. [Sib]
- **Release:**
  - τ-bench arXiv:2406.12045 (Jun 2024).
  - τ²-bench arXiv:2506.07982 (Jun 2025, adds the telecom domain).
  - Yao, Shinn, Razavi, Narasimhan; Barres et al. [Sib]
- **Launch vs. latest:**
  - Claude 3.5 Sonnet (1022) retail 69.2% at τ-bench launch. [Sib]
  - Telecom: Opus 4.6 99.3% (Feb 2026) and GPT-5.4 98.9% (Mar 2026). [P, Mi]
- **Adoption:**
  - 19/34 releases, 5 orgs.
  - Last frontier appearance Mar 2026 (GPT-5.4). [D]
- **Status:** saturated (telecom and retail). τ³ (banking_knowledge, voice) exists but has not appeared in headline tables. [Sib; D]
- **Why it succeeded:**
  - Realistic customer-service agent setting.
  - Cheap simulated user.
  - Reliability metric.
  - Early lab adoption.
  - Domain expansion. [Sib, I]
- **Why it failed:**
  - A small task count per domain (50–114).
  - Saturated within about 8 months of τ².
  - Judged through simulated users. [Sib]

### 6. Terminal-Bench (1.0 → 2.0 → 2.1 → 4.0)
- **Measures:** end-to-end tasks in a sandboxed terminal, checked by test scripts. [Sib]
- **Release / creators:**
  - Stanford and the Laude Institute; TB2.0 paper arXiv:2601.11868.
  - TB2.0 has 89 tasks.
  - TB2.1 modified 26 tasks, partly from Z.ai's "Terminal-Bench 2.0 Verified". [Sib]
- **Launch vs. latest:**
  - TB1: Opus 4 43.2% (May 2025). [P]
  - TB2.0: Opus 4.5 59.3% (Nov 2025) → GPT-5.5 82.7% (Apr 2026). [P, Mi]
  - TB2.1: Fable 5 88.0% (Jun 2026). [P]
  - TB4.0: Opus 5.5 66.4% (SE ±2.6), GPT-6 Astra 57.9% (Sep 2026). [P]
- **Adoption:** 21/34 releases, 6 orgs; 11/11 frontier tables in 2026H1. [D]
- **Status:** **thriving through versioning.**
- **Why it succeeded:**
  - It matches the terminal-agent products.
  - Lab task contributions.
  - Maintainer-run leaderboard with public trajectories.
  - Rapid re-versioning keeps headroom. [Sib, P]
- **Risks:**
  - Harness dependence. "self-reported harness" labels appear in competitor columns, e.g. GPT-5.4 at 75.1%. [P]
  - Anthropic reports that container resources move scores by about 6 points. [Sib]
  - Scores across versions are not comparable.

### 7. OSWorld (→ Verified → 2.0 → 2.1)
- **Measures:** computer-use agents in real VMs, graded by execution checkers. [Sib]
- **Release:**
  - arXiv:2404.07972 (Apr 2024, NeurIPS 2024).
  - Verified 28 Jul 2025; 2.0 26 Jun 2026; 2.1 16 Sep 2026. [Sib]
- **Launch vs. latest:**
  - At launch, best model 12.24% against humans 72.36%. [Sib]
  - Claude Sonnet 4.5 61.4% (Sep 2025) → Opus 4.8 83.4% (Verified, May 2026). [P]
  - OSWorld 2.0: Opus 5 70.6% (Jul 2026). [P]
  - OSWorld 2.1: Opus 5.5 81.8% "partial" (Sep 2026). [P]
- **Adoption:** 15/34 releases; 0/6 → 10/11 → 2/2 frontier tables by half-year. [D]
- **Status:** v1/Verified is saturated above the human baseline [Sib]; 2.x is active.
- **Why it succeeded:**
  - A real OS.
  - Human baseline.
  - Lab participation in the Verified fixes.
  - The computer-use product race.
- **Risks:**
  - Step budgets and harness choices.
  - "partial" scoring conventions.
  - Version churn.

### 8. MMMLU (OpenAI multilingual MMLU)
- **Measures:** MMLU translated into 14 languages. Anthropic: "Claude scores on MMMLU are the average over 14 non-English languages". [P]
- **Release:** OpenAI, Sep 2024 (Akhtar dataset release date; "(OpenAI, 2024)"). [P]
- **Launch vs. latest:**
  - Claude 3.7 Sonnet 86.1% (Feb 2025). [P]
  - Gemini 3.1 Pro 92.6% (Feb 2026). [P]
- **Adoption:** 14/34 releases, Anthropic, Google and OpenAI only; last in Opus 4.7 (Apr 2026). [D]
- **Status:** saturated (a flat 89–92% band).
- **Why it succeeded:**
  - A cheap multilingual line item from a familiar brand.
  - OpenAI released it.
- **Why it failed:** it inherits MMLU's label noise and the ceiling. [Sib]

### 9. MMMU (→ MMMU-Pro, CharXiv)
- **Measures:** college-level multimodal questions.
- **Launch vs. latest:** o3 82.9% (Apr 2025) → GPT-5 84.2% (Aug 2025) → GPT-5.1 85.4% (Opus 4.5 table, Nov 2025). [Mi, P]
- **Adoption:** 12/34 releases; **0/13 frontier tables in 2026**. Replaced by MMMU-Pro (10 releases) and CharXiv Reasoning. [D]
- **Status:** saturated / replaced.
- **Release / creators:** not verified this session beyond "introduced 2023" (AI Index 2025). [Mi]

### 10. BrowseComp (OpenAI)
- **Measures:** hard-to-find, easy-to-verify web facts, answered by browsing agents. [Sib]
- **Release:** arXiv:2504.12516 (Apr 2025), Wei et al. [Sib]
- **Launch vs. latest:**
  - Deep Research 51.5% at launch. [S via Sib]
  - Opus 5 90.8% and GPT-5.6 Sol 90.4% (Jul 2026). [P]
  - GPT-5.5 Pro 90.1% (Apr 2026). [Mi]
- **Adoption:**
  - 12/34 releases, 5 orgs. Open-weight labs adopted it before Anthropic and Google (Feb 2026). [D]
  - It survived OpenAI's Jul 2025 simple-evals freeze as a maintained reference implementation. [P]
- **Status:** active, approaching saturation (about 90%).
- **Contamination:** Claude Opus 4.6 found the source and decrypted the XOR-protected answer key. [Sib: contamination_saturation_stats.md]

### 11. GDPval / GDPval-AA
- **Measures:** economically valuable knowledge-work deliverables across 44 occupations. The OpenAI original uses blinded expert pairwise grading; the Artificial Analysis variant uses LLM-judge Bradley-Terry Elo. [Sib]
- **Release:** OpenAI, arXiv:2510.04374 (Sep–Oct 2025). [Sib]
- **Latest:**
  - GDPval (wins or ties): GPT-5.2 70.9% (Dec 2025) → GPT-5.5 84.9% (Apr 2026). [Mi]
  - GDPval-AA Elo:

    | Release | Version | Elo |
    |---|---|---|
    | Opus 4.6 (Feb 2026) | GDPval-AA | 1606 |
    | Opus 4.8 (May 2026) | GDPval-AA | 1890 |
    | Fable 5 (Jun 2026) | GDPval-AA | 1932 |
    | Opus 5 | v2 | 1861 |
    | Opus 5.5 | v2.1 | 1846 |

    [P] The Elo scale is relative and version-specific.
- **Adoption:** 0 frontier tables in 2025H1 → 12 of the 13 frontier releases in 2026. [D] Anthropic's Opus 5.5 post: "Artificial Analysis's GDPval-AA v2.1 evaluates agents on real-world professional work across 44 occupations." [P]
- **Status:** thriving; contested on grading validity. [Sib]
- **Why it succeeded:**
  - Economic framing.
  - No hard ceiling.
  - A third party (Artificial Analysis) made it cheap to run on every model.

### 12. ARC-AGI (1 → 2 → 3)
- **Measures:** few-shot abstraction on novel grid tasks. ARC-AGI-3 uses novel interactive environments. [Sib]
- **Release:** ARC-AGI-1 2019; ARC-AGI-2 24 Mar 2025 [P changelog; Sib]; ARC-AGI-3 25 Mar 2026. [Sib]
- **Launch vs. latest:**
  - ARC-AGI-2: single digits at launch [Sib] → 85.0% for GPT-5.5 (Apr 2026). [Mi]
  - ARC-AGI-3 (Opus 5 table, Jul 2026): Opus 5 30.2%, GPT-5.6 Sol 7.8%, Opus 4.8 1.5%. [P]
- **Adoption:**
  - 4 frontier labs in 2025 model cards (ARC Prize report). [Mi, H]
  - 10/34 releases in my matrix. [D]
  - Numbers are "ARC Prize Verified" on the semi-private set. [P]
- **Status:** v2 is near-saturated; v3 is active.
- **Why it succeeded:**
  - A prize and philosophy (fluid intelligence).
  - Verified testing partnership with labs.
  - A cost axis.
  - Re-versioning. [Sib]
- **Why it is failing:** ARC says "knowledge overfitting" now affects ARC-AGI-1/2 (IID public/private sets). [Sib]

### 13. MCP Atlas (Scale AI)
- **Measures:** multi-step tool workflows over MCP servers. Google: "Multi-step workflows using MCP". [P]
- **Creator:** Scale AI (OpenAI labels it "Scale MCP-Atlas"; "results from Scale AI after the latest 2026 April update"). [Mi] Release date not verified.
- **Scores:** Opus 4.5 62.3% (Nov 2025) → Gemini 3.5 Flash 83.6% (May 2026). [P]
- **Adoption:** 9/34 releases, 3 orgs, all between Nov 2025 and May 2026. It is absent from Anthropic tables after Opus 4.7. [D]
- **Status:** active; possibly already fading.

### 14. Finance Agent (v1 → v1.1 → v2)
- **Measures:** agentic financial analysis (label used in the Anthropic, Google and OpenAI tables). [P]
- **Creator:** not verified this session.
- **Scores:** Sonnet 4.5 55.3% (Sep 2025) → Opus 4.7 64.4% (v1.1) → Opus 4.8 53.9% (v2) → Gemini 3.5 Flash 57.9% (v2). [P]
- **Adoption:** 8/34 releases, 3 orgs. [D]
- **Status:** active, versioned.
- **Significance:** an example of vendor or customer-domain benchmarks entering headline tables. Other examples in 2026 Anthropic tables are AutomationBench (Zapier), CursorBench (Cursor), FrontierCode (Cognition, per Sib), WANDR (Perplexity) and Legal Agent Benchmark. Anthropic's footnote: "AutomationBench results were run and reported by Zapier." [P]

### 15. MMLU and MMLU-Pro (declining classics)
- **MMLU:** 6/34 releases, all by mid-2025.
  - The last frontier appearances are GPT-4.1 (Apr 2025) and gpt-oss (Aug 2025).
  - OpenAI's simple-evals table (MMLU, GPQA, MATH, HumanEval, MGSM, DROP, SimpleQA) was frozen in Jul 2025: "simple-evals will no longer be updated for new models or benchmark results". [P, H]
- **MMLU-Pro:** 7/34 releases, **all open-weight** (Meta, DeepSeek, Moonshot, MiniMax). It never appeared in a frontier-3 headline table in the sample. [D]
  - AI Index 2026: the top 15 are within about 4 points above 87%. [S]
- **Status:** saturated. Retained as "entry-standard" checks by open-weight labs. [I]

### 16. SimpleQA / SimpleQA Verified
- **Measures:** short-form parametric factuality. [Sib]
- **Adoption:** 8/34 releases:
  - OpenAI GPT-4.5 only among OpenAI releases.
  - Google Gemini 2.5 and 3 Pro (Verified, "from the official Kaggle leaderboard").
  - DeepSeek, Moonshot, MiniMax.
  - 0 frontier tables in 2026. [D, P]
- **Scores:** Gemini 3 Pro 72.1% (SimpleQA Verified, Nov 2025). [P] The Akhtar data list 97.1 for DeepSeek-V3.2-Exp, which is likely a tool-augmented variant (unverified). [P data, L]
- **Status:** niche / tool-contaminated. Search agents trivially retrieve answers. [Sib]

### 17. LiveCodeBench (and LiveCodeBench Pro)
- **Measures:** contamination-controlled coding problems, windowed by date. [Sib]
- **Release:** arXiv:2403.07974 (Mar 2024). [Sib]
- **Adoption:**
  - 8/34 releases, mostly open-weight: DeepSeek, Moonshot, MiniMax, Meta, Gemini 2.5.
  - The frontier labs moved to agentic coding. Google uses LiveCodeBench **Pro** Elo: Gemini 3 Pro 2,439 → 3.1 Pro 2,887. [P]
- **Status:** active in open-weight reports; absent from 2026 frontier tables. [D]
  - Akhtar S-index 0.77 ("High"). [P]

### 18. Aider Polyglot
- **Adoption:** 8/34 releases, last in Sep 2025 (DeepSeek-V3.2-Exp). [D]
- **Scores:** GPT-5 88% (Aug 2025). [Mi]
- **Citation practice:** Gemini 2.5 sourced competitors' numbers "from the Aider leaderboard". [P]
- **Status:** saturated / abandoned by frontier labs.

### 19. FrontierMath (Epoch AI; OpenAI-funded per Sib)
- **Adoption:** 4/34 releases, **all OpenAI**. [D]
- **Scores:**
  - Tier 1–3: GPT-5.2 40.3% (Dec 2025) → GPT-5.5 Pro 52.4% (Apr 2026).
  - Tier 4: GPT-5.5 Pro 39.6%. [Mi]
- **Status:** active but single-lab in headline tables, despite third-party hosting. This shows that a third-party host is not sufficient when the sponsor relationship is lab-specific. [I, M]

### 20. Lab-specific / internal benchmarks
Examples:
- OpenAI: Graphwalks, OpenAI-MRCR, SWE-Lancer, Expert-SWE (internal), investment-banking modeling (internal), and GDPval before Artificial Analysis took it up.
- Google: HiddenMath, ECLeKTic, FACTS, MRCR v2 (Google).
- Anthropic: BioMysteryBench.

Observations:
- Each appears in releases of **one lab only** (single-lab rows in A.3). [D]
- Google's MRCR v2 is described as "not publicly available yet" (Gemini 3 Pro PDF). [P]
- OpenAI created the most cross-lab successes: SWE-bench Verified (co-created), BrowseComp, MMMLU and SimpleQA. **In each case the data or an open harness was public, and third parties ran leaderboards.** [I, M]

### 21. LMArena / Arena Elo (as a launch-claim channel)
- **Adoption signal:**
  - Labs announce Arena ranks at launch. Meta Llama 4 is the notorious case: the "Llama-4-Maverick-03-26-Experimental" variant was ranked, and the public release model was later ranked 32nd. [Sib: arenas_preference.md, S]
  - AI Index 2026 uses Arena Elo for its "Big Four convergence" figure (Anthropic 1,503, xAI 1,495, Google 1,494, OpenAI 1,481 in March 2026). [S]
- **Not in headline tables:** Arena Elo does not appear as a row in any of the 34 headline tables I read. [D]
- **Status:** thriving as marketing and aggregate signal; contested (The Leaderboard Illusion). [Sib]

### 22. Game benchmarks (user's list context)
- **In the headline tables:**
  - Zero conventional game benchmarks in 34 headline tables. [D]
  - Pokémon appears only as a qualitative demo:
    - Claude 4 post: "Claude Opus 4 records key information to help improve its game play".
    - Gemini 2.5 report: "Gemini Plays Pokémon" progress timeline. [P]
  - ARC-AGI-3's "novel, turn-based game environments" (Sib quoting the Opus 5 system card) is the lone exception. It succeeded as a new version of an established, philosophy-driven brand with a prize and verification, not as a game benchmark per se. [I]
- **Status:** niche / abandoned by labs.

---

## Cross-cutting success factors

1. **A citable third-party leaderboard that covers competitors (strongest).** [P, H]
   - Labs need competitor columns, and they get them from self-reports or neutral leaderboards.
   - Gemini 3 Pro: "All the results for non-Gemini models are sourced from providers' self reported numbers unless mentioned otherwise." It cites sources for:
     - ARC-AGI-2: "ARC Prize Verified"
     - HLE: Scale leaderboard / Artificial Analysis
     - MathArena Apex: matharena.ai
     - LiveCodeBench Pro, Terminal-Bench 2.0: public leaderboards
     - Vending-Bench 2: andonlabs.com
     - SimpleQA Verified: Kaggle
   - Gemini 2.5 did the same for Aider, SimpleQA and FACTS.
   - Anthropic Opus 5.5 did the same for Terminal-Bench 4.0, AutomationBench and GDPval-AA.
   - OpenAI GPT-5.5 did the same for MCP Atlas.
   - Benchmarks without such a source have to be re-run by the reporting lab. Google names the ones it ran itself (MMMU-Pro, ScreenSpot-Pro, CharXiv, OmniDocBench, Video-MMMU, MMMLU, Global PIQA), which raises cost and dispute risk.
2. **Product alignment.** [D, H] The agentic share of frontier headline rows went 23% → 35% → 61% → 76% (2025H1 → 2026H2) as labs sold coding agents, computer use and enterprise work. Benchmarks that measure what is being sold get adopted.
3. **A headroom window.** [D, M-H]
   - Labs add a benchmark when their model posts a non-trivial, improving number. ARC-AGI-2 was adopted at 31–38% (8 months after its 0–5% launch). ARC-AGI-3 was adopted when Opus 5 scored 30.2% against 1.5% for its predecessor.
   - Labs drop a benchmark at ceiling: AIME at 100%, τ² telecom at 99%, GPQA at 94%.
4. **Brand continuity through versioning.** [P, H] Every family with more than 12 months of 2026 headline presence is a versioned brand (Terminal-Bench, OSWorld, ARC-AGI, GDPval-AA, Finance Agent), with HLE as the exception.
5. **Lab co-development or verification.** [P/Sib/Mi, M-H]
   - OpenAI Preparedness and SWE-bench Verified.
   - Lab participation in OSWorld-Verified fixes.
   - Terminal-Bench task contributions.
   - ARC's pre-release verification.
   - Customers running benchmarks for labs (Zapier for AutomationBench).
   - Adoption lag drops to weeks.
6. **Legible units and names.** [Sib/P, M] "Humanity's Last Exam", "Verified", "Diamond", Elo (GDPval-AA, LiveCodeBench Pro), dollars (Vending-Bench net worth).
7. **Low cost to run.** [Sib, M]
   - Small sets (GPQA 198, SWE-bench Verified 500) were cheap to run many times.
   - Expensive suites are skipped. Kimi K2: "Some data points have been omitted due to prohibitively expensive evaluation costs". TheAgentCompany had no submissions after Nov 2025. [Sib]

## Cross-cutting failure factors

1. **Ceiling saturation removes the benchmark from headline tables within months.** Examples: AIME, MMMU, τ², GPQA, MMLU (§B.4). [D, H]
2. **Public-source provenance plus RL-era training leads to contamination and retirement.** SWE-bench Verified is the canonical case. [Mi, H] HLE and BrowseComp now need domain blocklists at evaluation time. [P]
3. **Item-quality ceilings.** Flawed tests (59.4% of audited hard SWE-bench Verified tasks) and wrong answers (HLE "Flawed" per Epoch) make the last points unattainable, so saturation arrives early. [Mi; Sib]
4. **No third-party runner, or a creator-only benchmark, keeps adoption single-lab.** Examples: FrontierMath (OpenAI-only in headline tables despite Epoch hosting), Graphwalks, HiddenMath, FACTS, MRCR v2 (Google), SWE-Lancer. [D, M]
5. **Academic citations do not create lab adoption.** Highly cited classics (GLUE 9,064; HellaSwag 2,836; TriviaQA 3,491) are absent, while τ-bench (7 citations in Akhtar's data) is in 19/34 releases. Exploratory ρ = −0.34. [D, L-M]
6. **Harness and variant ambiguity reduces comparability, which fuels replacement:**
   - n = 477 vs 500 (SWE-bench).
   - "self-reported harness" (Terminal-Bench).
   - With-tools vs no-tools (HLE, AIME).
   - "partial" scoring (OSWorld 2.1).
   - Deep Think / Pro variants.
   - [P]
7. **Small n limits discrimination late in life.** Akhtar: test-set size is one of the two most consistent saturation predictors. Terminal-Bench 2.0 was flagged at 1 month because the top models tied on 82 tasks. [P, H]
8. **Games are ignored by labs** in headline reporting, including Google's own Kaggle Game Arena. [D/Sib, H]

## Strongest empirically supported predictors of adoption (ranked)

| Rank | Predictor | Evidence strength | Key evidence |
|---|---|---|---|
| 1 | A trusted third-party leaderboard that runs or verifies frontier models, so competitors' numbers are citable | High | Explicit sourcing notes in Gemini 2.5, Gemini 3 Pro, Opus 5.5 and GPT-5.5 [P/Mi]; ARC Prize Verified; GDPval-AA uptake 0 → 12/13 frontier tables after Artificial Analysis [D] |
| 2 | Measures the capability category labs are currently marketing (2025–26: agentic coding, computer use, knowledge work) | High | Agentic share 23% → 76% [D]; SWE-bench Pro / Terminal-Bench / OSWorld / GDPval surge [D] |
| 3 | A headroom window: non-trivial but improving scores for the adopting lab's model | Medium-high | ARC-AGI-2 lag of 8 months; ARC-AGI-3 adopted at 30%; drops at ceiling (AIME, τ², GPQA) [D/P] |
| 4 | Versioned brand continuity (a difficulty knob and renewals under one name) | High | All long-lived 2026 families except HLE are versioned [P/D] |
| 5 | Lab co-development, verification or recommendation | Medium-high | SWE-bench Verified (OpenAI), SWE-bench Pro (OpenAI recommendation → 9/11) [Mi/D]; OSWorld-Verified [Sib] |
| 6 | Low cost and automatic scoring | Medium | Kimi K2 omissions; small-n staples [Sib] |
| 7 | Memorable branding / legible units | Medium (qualitative) | HLE, "Verified", Elo, $ [Sib/P] |
| — | Academic citations / venue prestige | Not predictive, or negative | Akhtar ρ = 0.05 for report frequency vs saturation [P]; my ρ = −0.34 citations vs adoption [D] |

**Implications for our non-game benchmark (interpretation).**
- Launch with an independent, maintainer-run leaderboard that evaluates all frontier models under a fixed harness and publishes standard errors (as Anthropic now does: "The standard error is ±2.6 pts").
- Frame it around a capability labs sell, such as agentic knowledge work with verifiable outputs.
- Ship v1 at about 10–40% frontier accuracy.
- Pre-announce a versioning scheme (difficulty knob; fresh item pools every 4–6 months).
- Keep cost per model run low.
- Give it a memorable, stable name.
- Invite labs to verify, but never let one lab own it (the FrontierMath lesson).

---

## Claims ledger

| # | Claim | Sources | Confidence |
|---|---|---|---|
| 1 | Headline tables of 34 releases (Dec 2024–Sep 2026; 7 developers) name 110 benchmark families; 48 (44%) appear in exactly one release; only 11 appear in ≥ 1/3 of releases (GPQA Diamond 27, SWE-bench Verified 23, HLE 22, Terminal-Bench 21, AIME 19, τ-bench 19, OSWorld 15, MMMLU 14, GDPval 13, MMMU 12, BrowseComp 12). | Derived from the release sources in A.2 (Refs 7–20, 22–30, 33–44) | H for the counts, given the A.1 inclusion rule |
| 2 | Across OpenAI, Anthropic and Google headline tables, AIME appeared in 13/14 releases in 2025 and 0/13 in 2026; MMMU 11/14 → 0/13; GPQA Diamond 14/14 → 6/13 (none after April 2026); SWE-bench Verified 13/14 → 4/13. | Refs 7–20, 22–30, 33–37 | H |
| 3 | The agentic share of frontier-3 headline rows was 23% (2025H1), 35% (2025H2), 61% (2026H1) and 76% (2026H2, Anthropic only). | Derived; Refs 7–20, 22–30, 33–37 | M-H (the category boundary is a judgment call) |
| 4 | None of the 8 benchmark families in Claude 3.7 Sonnet's table (24 Feb 2025) appears in any Anthropic headline table from Opus 4.8 (28 May 2026) onward. | https://www.anthropic.com/news/claude-3-7-sonnet ; https://www.anthropic.com/news/claude-opus-4-8 ; …/claude-fable-5-mythos-5 ; …/claude-sonnet-5 ; …/claude-opus-5 ; …/claude-opus-5-5 | H |
| 5 | OpenAI (23 Feb 2026) said SWE-bench Verified "became a standard metric reported in frontier model releases". It found ≥59.4% of 138 audited hard problems had flawed tests and that all frontier models tested could reproduce gold patches. It stopped reporting the benchmark and recommended SWE-bench Pro; SOTA had moved 74.9% → 80.9% in the prior 6 months. | https://raw.githubusercontent.com/visual-snow/seshat/main/web-research/openai/why-we-no-longer-evaluate-swe-bench-verified.md (mirror of https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified) | M-H (mirror) |
| 6 | Labs source competitor numbers from providers' self-reports and third-party leaderboards: ARC Prize Verified, Scale's HLE leaderboard, Artificial Analysis, matharena.ai, the public LiveCodeBench Pro and Terminal-Bench 2.0 leaderboards, Andon Labs (Vending-Bench 2), Kaggle (SimpleQA Verified). | https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_model_evaluation.pdf ; https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf ; https://www.anthropic.com/news/claude-opus-5-5 | H |
| 7 | ARC Prize's 2025 technical report states that four frontier labs (Anthropic, Google DeepMind, OpenAI, xAI) reported ARC-AGI performance in public model cards in 2025, "establishing ARC-AGI as an industry standard benchmark for AI reasoning". | https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md (arXiv:2601.10904) | H |
| 8 | Akhtar et al. (ICML 2026) reviewed 61 developer reports (Jan 2022–Nov 2025) naming 190 benchmarks, and analysed 60. Nearly half are saturated. Frequency of appearance in technical reports is not associated with saturation (ρ = 0.05, p = 0.73). Age and test-set size are the most consistent predictors. | https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf ; https://github.com/evaleval/benchmark-saturation | H |
| 9 | Kiela et al. (2021) Fig. 1 shows time-to-human-parity shrinking from about 15–20 years (MNIST, Switchboard) to about 1–2 years (SQuAD, GLUE). The year values are approximate readings of the figure. | https://raw.githubusercontent.com/KAUST-Academy/Artificial-Intelligence-Courses/HEAD/LaTeX/sections/llm-evaluation/motivation.tex ; figure at …/LaTeX/images/llm-evaluation/dynabench_fig1_benchmark_saturation.png | M |
| 10 | AI Index 2025: MMMU, GPQA and SWE-bench scores rose 18.8, 48.9 and 67.3 points within a year of their 2023 introduction; the top-vs-10th gap fell from 11.9% to 5.4%. | https://raw.githubusercontent.com/petroslamb/autonomy-tax-enterprise-agents/HEAD/sources/raw/031_stanford_ai_index_2025_rjina.md (scrape of hai.stanford.edu/ai-index/2025-ai-index-report) | M-H |
| 11 | Anthropic (9 Jan 2026): "LLMs have progressed from 40% to >80% on this eval in just one year" (SWE-bench Verified). Anthropic Opus 5.5 (22 Sep 2026): "benchmark margins have become a less reliable guide to real-world differences". | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents ; https://www.anthropic.com/news/claude-opus-5-5 | H |
| 12 | GPT-5.2 reported 100.0% on AIME 2025 without tools (11 Dec 2025). Gemini 3 Pro reported 100% with code execution (Nov 2025). No frontier-3 headline table in 2026 reports AIME. | seshat mirror introducing-gpt-5-2.md ; gemini_3_pro_model_evaluation.pdf ; derived | H |
| 13 | OpenAI froze simple-evals in July 2025 ("will no longer be updated for new models or benchmark results"), keeping only HealthBench, BrowseComp and SimpleQA reference implementations. | https://github.com/openai/simple-evals (README) | H |
| 14 | GDPval (incl. GDPval-AA) went from 1/14 frontier-3 headline tables in 2025 to 12/13 in 2026. Anthropic's tables cite "Artificial Analysis's GDPval-AA". | Refs 13–20, 27–30, 36–37; https://www.anthropic.com/news/claude-opus-5-5 | H |
| 15 | SWE-bench Pro went from 1/14 frontier-3 tables in 2025 (GPT-5.2) to 9/11 in 2026H1. | Refs 15–18, 27–30, 36–37 | H |
| 16 | Across 39 benchmarks with citation counts in Akhtar's dataset, citations correlate negatively with 2025–26 headline adoption (Spearman ρ = −0.34, permutation p ≈ 0.03). This is exploratory and confounded by age. | Derived from evaleval/benchmark-saturation CSV and the A.2 matrix | L-M |
| 17 | Zero conventional game benchmarks appear in the 34 headline tables. Pokémon appears only as a demo (Claude 4; Gemini 2.5). ARC-AGI-3 (novel interactive environments) is the lone game-like row (Opus 5). | Refs 8, 19, 33 | H |
| 18 | Terminal-Bench was in Anthropic's headline table on day one (Claude Opus 4, 22 May 2025: 43.2%) and in 11/11 frontier-3 releases in 2026H1. Versions went 2.0 → 2.1 → 4.0 within about 10 months. | https://www.anthropic.com/news/claude-4 ; Refs 8, 13–20, 28–30, 34–37 | H |
| 19 | Kimi K2's README says some data points were omitted "due to prohibitively expensive evaluation costs". | Sib agentic.md; https://github.com/MoonshotAI/Kimi-K2 | M-H |
| 20 | OSWorld at launch: best model 12.24% vs humans 72.36%. Claude Opus 4.8 reports 83.4% on OSWorld-Verified (May 2026). | Sib agentic.md (arXiv:2404.07972); https://www.anthropic.com/news/claude-opus-4-8 | H |

## References

Full entries with seen-URLs are in `research/refs/model_cards_adoption.json`. [P] means fetched directly by me; [Mi] means a mirror.

**Meta-research and lifecycle**
1. Akhtar, M., Reuel, A., et al. (2026). *When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation.* ICML 2026, PMLR 306. arXiv:2602.16763. [P] https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf
2. EvalEval Coalition (2026). *benchmark-saturation* repository (companion data, `data/manual_annotation_data.csv`). [P] https://github.com/evaleval/benchmark-saturation
3. Kiela, D., Bartolo, M., Nie, Y., et al. (2021). *Dynabench: Rethinking Benchmarking in NLP.* NAACL 2021. arXiv:2104.14337. [P-figure via course repo] https://github.com/KAUST-Academy/Artificial-Intelligence-Courses
4. Ott, S., Barbosa-Silva, A., Blagec, K., Brauner, J., Samwald, M. (2022). *Mapping global dynamics of benchmark creation and saturation in artificial intelligence.* Nature Communications 13:6793. doi:10.1038/s41467-022-34591-0. [Mi abstract] https://github.com/TTXS123OK/CVPapers
5. Stanford HAI (2025). *AI Index Report 2025.* [Mi-scrape] https://hai.stanford.edu/ai-index/2025-ai-index-report
6. Stanford HAI (2026). *AI Index Report 2026, Technical Performance chapter* (secondary summaries). [S] https://hai.stanford.edu/ai-index/2026-ai-index-report/technical-performance

**Anthropic launch posts (all [P], anthropic.com)**
7. Claude 3.7 Sonnet and Claude Code (24 Feb 2025).
8. Introducing Claude 4 (22 May 2025).
9. Claude Opus 4.1 (5 Aug 2025).
10. Introducing Claude Sonnet 4.5 (29 Sep 2025).
11. Introducing Claude Haiku 4.5 (15 Oct 2025).
12. Introducing Claude Opus 4.5 (24 Nov 2025).
13. Introducing Claude Opus 4.6 (5 Feb 2026).
14. Introducing Claude Sonnet 4.6 (17 Feb 2026).
15. Introducing Claude Opus 4.7 (16 Apr 2026).
16. Introducing Claude Opus 4.8 (28 May 2026).
17. Claude Fable 5 and Claude Mythos 5 (9 Jun 2026).
18. Introducing Claude Sonnet 5 (30 Jun 2026).
19. Introducing Claude Opus 5 (24 Jul 2026).
20. Introducing Claude Opus 5.5 (22 Sep 2026).
21. Demystifying evals for AI agents (Anthropic Engineering, 9 Jan 2026).

**OpenAI (launch posts via [Mi] visual-snow/seshat; simple-evals [P])**
22. Introducing GPT-4.5 (27 Feb 2025).
23. Introducing GPT-4.1 in the API (14 Apr 2025).
24. Introducing OpenAI o3 and o4-mini (16 Apr 2025).
25. Introducing gpt-oss (5 Aug 2025).
26. Introducing GPT-5 (7 Aug 2025).
27. Introducing GPT-5.2 (11 Dec 2025).
28. Introducing GPT-5.3-Codex (5 Feb 2026).
29. Introducing GPT-5.4 (5 Mar 2026).
30. Introducing GPT-5.5 (23 Apr 2026).
31. Why SWE-bench Verified no longer measures frontier coding capabilities (23 Feb 2026).
32. openai/simple-evals README (deprecation notice, July 2025). [P]

**Google DeepMind ([P], storage.googleapis.com)**
33. Gemini Team (2025). *Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities.* Technical report.
34. Gemini 3 Pro: Model Evaluation – Approach, Methodology & Results (Nov 2025).
35. Gemini 3 Pro Model Card (Nov 2025).
36. Gemini 3.1 Pro Model Card (Feb 2026).
37. Gemini 3.5 Flash Model Card (May 2026).

**Open-weight developers ([P], GitHub)**
38. Meta. Llama 4 Model Card (Apr 2025).
39. DeepSeek-AI. DeepSeek-V3 README (arXiv:2412.19437).
40. DeepSeek-AI. DeepSeek-R1 README (arXiv:2501.12948).
41. DeepSeek-AI. DeepSeek-V3.2-Exp README.
42. Moonshot AI. Kimi K2 README (arXiv:2507.20534).
43. MiniMax. MiniMax-M1 README (arXiv:2506.13585).
44. MiniMax. MiniMax-M2 README.
45. Z.ai. GLM-4.5 / 4.6 / 4.7 README (GLM-4.5 tech report arXiv:2508.06471).

**Other**
46. Chollet, F., Knoop, M., Kamradt, G., Landers, B. (2026). *ARC Prize 2025: Technical Report.* arXiv:2601.10904. [Mi]
47. arcprize/ARC-AGI-2 changelog. [P]
48. Kopel, R. *Killed by LLM* (data.ts). [S] https://github.com/R0bk/killedbyllm
49. Esposito, M., Zhang, L. (2026). *The Benchmark Ceiling: Human Judgment, Evaluation Scarcity, and the Political Economy of AI Capability Measurement.* arXiv:2607.01254 (working paper). [Mi]

**Sibling dossiers relied on (not re-fetched unless stated):**
- knowledge_exams.md: GPQA and HLE metadata, Grok 4 HLE, Epoch reviews.
- coding.md: SWE-bench Verified history, SWE-bench Pro, Terminal-Bench versions.
- agentic.md: OSWorld, τ-bench, BrowseComp, GDPval / GDPval-AA, the Kimi K2 cost omission.
- arc_agi.md: ARC Prize history. I re-verified the four-labs statement and the ARC-AGI-2 changelog.
- math.md: AIME contamination, FrontierMath.
- arenas_preference.md: the Llama 4 Arena episode.
- contamination_saturation_stats.md: BrowseComp decryption, harness effects.
