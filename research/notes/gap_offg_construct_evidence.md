# Gap dossier: are learning, teaching, calibration and multi-turn communication off the general factor?

Date: 2026-09-29. Scope: a quantitative test of the design bet in Brief D (S6; Implications 1-3 and 7) and of niche #1 in `prior_art_novel_methods.md`. The bet is that learning from novel material, teaching it, and calibration carry reliable variance beyond general capability ("g"; ECI or PC1). This dossier also collects the counter-evidence the survey had not gathered.

Confidence labels:
- **H**: primary source, or two agreeing copies.
- **M**: a single mirror, or a consistent secondary source.
- **L**: unverified.
- **[C]**: a number I computed in this session from public data. The label after [C] rates the input data.

---

## Summary

- **Bottom line.** The claim "learning ability is off the general factor" is **not supported as stated**. When learning or teaching is scored as *performance after learning*, it is mostly g-loaded among 2024-26 models. The candidates that do keep sizeable reliable variance beyond ECI are different ones:
  - forecasting accuracy among frontier models;
  - calibration error, but not Brier score;
  - honesty and sycophancy propensities;
  - knowledge/factuality.
  
  The design must therefore test the residual rather than assume it. It must also be sized and made reliable enough to *falsify* the off-g claim.

- **ARC-AGI is the strongest counter-evidence.** ARC was built to measure skill-acquisition efficiency [chollet2019measure], yet it is among the most g-loaded benchmarks in the whole Epoch data set [C, H]:
  - Leave-one-benchmark-out ECI-refit correlations: ARC-AGI-1 ρ = 0.966 [0.934, 0.980] (n = 69); ARC-AGI-2 ρ = 0.953 [0.906, 0.972] (n = 66).
  - ARC-AGI-2's disattenuated r is about 0.97, and its discriminability is third-highest of 96 benchmarks.
  - Direct checks agree: ARC-AGI-2 vs GPQA Diamond ρ = 0.92 (n = 53, mirror data); ARC-AGI-1 vs GPQA Diamond ρ = 0.88 (n = 21, Epoch's own repo).
  - Among frontier models (ECI-refit ≥ 150), ARC still correlates 0.80-0.84, compared with 0.51 for GPQA Diamond.

- **Learning from novel material in context.** CL-bench [dou2026clbench] is the closest existing instance of the lead construct. It correlates ρ = 0.71 [0.40, 0.89] with the ECI-refit (n = 19, all 2025-26 frontier models; disattenuated about 0.76) [C, M]. That is similar to SWE-bench Verified in the same restricted population, and far from zero. The verdict is indeterminate: at most moderately off-g.

- **Teaching.**
  - MathTutorBench, recomputed on all 17 leaderboard models: problem-solving vs the pedagogy composite gives Spearman **0.76 [0.34, 0.92]** but Pearson **0.43 [0.07, 0.83]** [C, H]. The published 8-model 0.421 is reproduced only as a Pearson, and that Pearson is driven by two specialised fine-tunes. On ranks, teaching tracks solving.
  - TutorBench vs ECI-refit: ρ = 0.66 [0.21, 0.89] (n = 19). Its residual co-varies with other rubric-judged Scale benchmarks, which points to a method factor [C, M].
  - EducationQ gain vs ECI-refit: ρ = 0.12 [-0.74, 0.84] (n = 8). This is uninformative [C, M].

- **EvaLearn** (11 models in the repo's Table 2, not the 9 stated in the abstract):
  - Feedback-learning *accuracy* correlates ρ = 0.90 with zero-shot accuracy.
  - The *gain* correlates ρ = -0.61 [-0.92, 0.02] with zero-shot accuracy. That is a difference score, prone to regression to the mean and ceiling effects [C, H].
  - The paper's "not strongly correlated" claim rests on worked examples, not on a coefficient [H].

- **Forecasting is the clearest off-g signal** [C, H]. On ForecastBench's baseline leaderboard (70 models matched to ECI), ρ = 0.63 overall. Among ECI-refit ≥ 140 models it is **ρ = 0.05 [-0.26, 0.35]** (n = 36), even though score reliability is about 0.89 (estimated from the published CIs). This may, however, reflect a no-retrieval ceiling (frontier models sit at 58.6-62.0; superforecasters score 67.7), not a distinct ability.

- **Calibration.** In the Safetywashing data (2024 open models) [C, H]:
  - 1-RMS calibration error correlates -0.02 (base models) and 0.41 / 0.05 temperature-tuned (chat models) with capability PC1.
  - 1-Brier correlates **0.84-0.92**.
  
  A proper-scoring overlay is therefore g-loaded unless it is decomposed into its calibration and resolution components.

- **Power.** Suppose the true disattenuated r with ECI is about 0.75, benchmark reliability is at least 0.9, and ECI reliability is 0.95. Rejecting "collapse" (ρ ≥ 0.9) then needs about **57 models** (one-sided α = 0.05, power 0.8). At ρ = 0.8 it needs about 106; at reliability 0.8, about 85 or 166. Family clustering reduces the effective N further [C].

---

## Findings

### 1. Re-analysis on the Epoch/ECI data (task 1a)

**Data.** Epoch's `benchmark_data.zip` could not be fetched: epoch.ai is blocked by the proxy with a CONNECT 403, and the `eci-public` repo contains code only. I used three substitutes:
- **Mirror.** A third-party mirror of the zip: `linkofrivia/ECI_Bayesian`, `data/processed/benchmarks_merged.csv` [eciBayesian2026].
  - Snapshot 2026-08-07; ZIP sha256 `591b9f32…` per its `pipeline_report.md`.
  - 5,064 rows, 100 benchmarks, 835 model versions.
  - It merges Epoch's ZIP and live feed with Scale SEAL, RAND and Kaggle rows.
- **Cross-check against Epoch's own repo** (`epoch-research/benchmark-stitching`, Dec 2025) [epoch2025stitching]:
  - ARC-AGI: 51 overlapping rows, maximum absolute difference 0.005.
  - GPQA Diamond: 132 rows, 96% within 0.01.
  - The mirror is faithful where checked (H for Epoch-sourced rows; M for SEAL-sourced rows, which were not cross-checked).
- **Fit.** The official `epoch-research/eci-public` `fit_eci_model` code [epoch2026ecipublic; ho2025rosetta]: a least-squares sigmoid IRT, anchored at Claude 3.5 Sonnet (20241022) = 130 and GPT-5 = 150.
  - I call the result the **ECI-refit**. It is *not* Epoch's published ECI.
  - It uses more benchmarks (SEAL etc.), a different identification anchor (GPQA Diamond instead of Winogrande), and model groups built by stripping effort suffixes, taking the maximum across effort variants as Epoch does.
  - Result: 276 model groups with at least 4 benchmarks each, and 96 benchmarks.

**Method.** For each benchmark B with at least 15 models:
- The ECI-refit is re-fitted *leaving B out* (LOO), to avoid part-whole inflation.
- I report:
  - Spearman ρ between B's normalised score and the LOO ECI-refit, with a 2,000-sample bootstrap CI;
  - R, the Pearson correlation between observed scores and a per-benchmark logistic curve fitted on the LOO ECI;
  - the residual SD;
  - a KR-21-style binomial reliability, rel = 1 - mean[p(1-p)/n_items] / var(p), using n_items from the mirror's `benchmark_n_items.csv`;
  - ECI-refit reliability from 100 bootstrap refits;
  - disattenuated R = R / sqrt(rel_B × rel_ECI);
  - "reliable specific" share = rel_B - R².

**Caveats on these statistics.**
- Binomial reliability ignores judge noise and run-to-run noise. For LLM-judged benchmarks it *overstates* reliability. That makes the disattenuated R here a lower bound and the specific share an upper bound.
- Values above 1 (SciCode, WeirdML, GDP.pdf) show that the binomial approximation can also fail the other way.

**Selected results.** Scope is all model groups; the 2024+ subset differs by at most 0.07 for these rows. Source: [C] from [eciBayesian2026] + [epoch2026ecipublic].

| Benchmark (construct) | n | ρ with LOO ECI-refit [95% CI] | R (curve) | rel_B (binom.) | R disatt. | reliable specific share | Fitted discriminability (rank of 96) |
|---|---|---|---|---|---|---|---|
| Humanity's Last Exam | 39 | 0.968 [0.93, 0.98] | 0.956 | 0.997 | 0.971 | 0.08 | 0.097 |
| ARC-AGI-1 (skill acquisition) | 69 | **0.966 [0.93, 0.98]** | 0.963 | n/a | n/a | n/a | 0.192 (6th highest) |
| METR Time Horizons (agentic) | 36 | 0.965 [0.91, 0.98] | 0.975 | 0.951 | 1.01 | 0.00 | 0.049 |
| OTIS Mock AIME | 124 | 0.960 [0.93, 0.97] | 0.975 | 0.985 | 0.993 | 0.04 | 0.179 |
| ARC-AGI-2 (skill acquisition) | 66 | **0.953 [0.91, 0.97]** | 0.950 | 0.991 | **0.971** | 0.09 | **0.268 (3rd highest)** |
| SEAL Tool Use (Enterprise) | 29 | 0.884 [0.72, 0.97] | 0.831 | 0.950 | 0.884 | 0.26 | 0.042 |
| MultiChallenge (multi-turn) | 28 | 0.820 [0.58, 0.95] | 0.864 | 0.915 | 0.928 | 0.17 | 0.052 |
| BALROG (agentic games) | 23 | 0.807 [0.54, 0.92] | 0.865 | n/a | n/a | n/a | 0.040 |
| SWE-bench Verified | 31 | 0.804 [0.61, 0.92] | 0.870 | 0.966 | 0.903 | 0.21 | 0.058 |
| MCP Atlas (tool use) | 29 | 0.795 [0.61, 0.90] | 0.805 | 0.976 | 0.842 | 0.33 | 0.093 |
| Chess Puzzles | 73 | 0.737 [0.59, 0.83] | 0.765 | 0.926 | 0.807 | 0.34 | 0.076 |
| SimpleQA Verified (factuality) | 78 | 0.736 [0.60, 0.83] | 0.733 | 0.995 | 0.744 | 0.46 | 0.058 |
| Fiction.LiveBench (long context) | 33 | 0.729 [0.47, 0.86] | 0.690 | 0.886 | 0.775 | 0.41 | 0.126 |
| **CL-bench (context learning of new knowledge)** | 19 | **0.711 [0.40, 0.89]** | 0.650 | 0.953 | **0.761** | 0.53 | 0.042 |
| **TutorBench (tutoring)** | 19 | **0.660 [0.21, 0.89]** | 0.718 | 0.943 | **0.757** | 0.43 | 0.022 (7th lowest) |
| SEAL Instruction Following | 16 | 0.638 [0.21, 0.90] | 0.729 | 0.888 | 0.837 | 0.36 | 0.031 |
| Lech Mazur Writing | 40 | 0.621 [0.37, 0.80] | 0.601 | 0.938 | 0.642 | 0.58 | 0.029 |
| DeepResearchBench | 23 | 0.500 [0.04, 0.79] | 0.480 | 0.633 | 0.616 | 0.40 | 0.024 |
| **ForecastBench (Epoch-ingested)** | 63 | **0.446 [0.20, 0.65]** | 0.540 | n/a | n/a | n/a | **0.015 (2nd lowest)** |

Additional rows:
- GPQA Diamond: n = 137, ρ = 0.974 [0.959, 0.981].
- CL-bench Life: n = 13, ρ = 0.82 [0.49, 0.98].

**Lowest fitted discriminability** (full fit): Video-MME (0.008), ForecastBench (0.015), PIQA, TriviaQA, LAMBADA, MMLU-Biology, TutorBench (0.022), LAB-Bench LitQA2, DeepResearchBench, VISTA.

**Highest fitted discriminability:** GBAEval (0.318), VPCT (0.269), **ARC-AGI-2 (0.268)**, FrontierMath Tier 4 (0.237), ProofBench (0.235), **ARC-AGI (0.192)**, Remote Labor Index (0.191).

Discriminability confounds construct with score range. ForecastBench's normalised scores span only 0-0.25 and TutorBench's span 0.36-0.69, so correlation is the better statistic.

**Largest residual SD** (normalised-score units): GBAEval 0.21, Fiction.LiveBench 0.16, GSM8K 0.16, GeoBench 0.14, VPCT 0.14, SimpleQA Verified 0.13. ARC-AGI-2 is 0.10.

**Range restriction.** Correlations fall in frontier-only populations, and they fall for *every* benchmark, not only candidate off-g ones. Spearman with the LOO ECI-refit (n in parentheses):

| Benchmark | ECI-refit ≥ 140 | ECI-refit ≥ 150 |
|---|---|---|
| ARC-AGI-1 | 0.93 (47) | **0.84 (25)** |
| ARC-AGI-2 | 0.92 (47) | **0.80 (25)** |
| GPQA Diamond | 0.86 (67) | 0.51 (33) |
| Humanity's Last Exam | 0.93 (25) | 0.54 (10) |
| OTIS AIME | 0.81 (61) | 0.66 (32) |
| SWE-bench Verified | 0.74 (28) | 0.67 (17) |
| CL-bench | 0.71 (19) | - |
| MultiChallenge | 0.67 (22) | - |
| TutorBench | 0.53 (17) | - |
| SimpleQA Verified | 0.48 (58) | 0.27 (34) |
| ForecastBench (Epoch) | **-0.27 (32)** | -0.19 (13) |

ECI-refit reliability itself also falls with the range: 0.97 for all models, 0.91 at ECI ≥ 140, 0.86 at ECI ≥ 150 [C]. A low correlation among frontier-only models is therefore **not** evidence of distinctness unless it is benchmarked against yardstick benchmarks (GPQA, ARC) in the same sample [C, M].

**Residual structure.** I took Spearman correlations of residuals from the LOO curve fits [C, M]:
- **ARC-AGI-1 vs ARC-AGI-2 residuals: ρ = 0.45 (n = 63, p < 0.001).** There is a reliable ARC-specific factor. It is small, though: R² ≈ 0.90 with the ECI-refit, so ARC-specific reliable variance is about 0.1 × 0.45 ≈ 4-5% of total variance.
- ARC residuals also correlate with METR time-horizon residuals (0.58-0.65, n = 18-20), which suggests a shared reasoning/agentic sub-factor.
- **TutorBench's residual correlates with the residuals of MultiChallenge (0.66, n = 16), PRBench-Legal (0.56, n = 13) and PRBench-Finance (0.57, n = 13).** All four are rubric-judged conversational leaderboards from Scale. This looks like a judge or format method factor, not a teaching construct.
- TutorBench's residual is negatively correlated with ARC-AGI-2's (-0.70, n = 16).
- ForecastBench's residual is negatively correlated with OTIS-AIME's (-0.46, n = 55).

**Developer-family effects.** In a one-way ANOVA of the residuals, model family explains a large share of residual variance [C, M]:

| Benchmark | η² | permutation p |
|---|---|---|
| MCP Atlas | 0.75 | < 0.001 |
| PRBench Finance | 0.51 | 0.02 |
| SWE-bench Verified | 0.50 | 0.01 |
| SEAL Tool Use | 0.48 | 0.015 |
| Chess Puzzles | 0.47 | < 0.001 |
| METR | 0.41 | 0.015 |
| SimpleQA Verified | 0.24 | 0.016 |
| ARC-AGI-2 | 0.23 | 0.14 (n.s.) |
| ForecastBench | 0.10 | 0.80 (n.s.) |

On SimpleQA Verified, the Gemini family's mean residual is +0.18. Much "off-g" variance in public data is lab-specific post-training emphasis. That is reliable, but it is not a cognitive construct, and it reduces the effective N.

**Third-party K = 3 Bayesian MIRT (`ECI_Bayesian`, exploratory).**
- ForecastBench loads 0.99 on a second axis, as do Chess (0.90), SEAL Tool Use (0.83), CL-bench (0.69) and GPQA Diamond (0.66).
- ARC-AGI-1 and 2, TutorBench, MultiChallenge and METR load 0.94-0.98 on axis 1.
- The axes intercorrelate 0.69-0.78, and the repo documents mode or bimodality issues. Treat this as suggestive only [M/L; eciBayesian2026].

### 2. ARC-AGI vs general capability (task 1b)

- **Design intent:** ARC measures "skill-acquisition efficiency" [chollet2019measure] (H, existing dossier).
- **Trajectory:** ARC-AGI-2 went from single digits at launch to 95.0% by Sep 2026 [kamradt2025arcagi2launch; alloevil2026tracker] (S/H per `arc_agi.md`).
- **Empirical g-loading** [C]:
  - LOO ECI-refit ρ = 0.966 (ARC-AGI-1) and 0.953 (ARC-AGI-2). ARC-AGI-2's disattenuated R is 0.971. Both are in the top ~15% of 78 benchmarks (ARC-AGI-1 ranks 2nd, ARC-AGI-2 about 10th).
  - ARC-AGI-1 vs ARC-AGI-2: ρ = 0.977 (n = 68).
  - ARC-AGI-2 vs GPQA Diamond: 0.917 (n = 53). vs OTIS AIME: 0.914 (n = 51). vs FrontierMath: 0.913 (n = 30). vs SWE-bench Verified: 0.907 (n = 22).
  - vs ForecastBench: **-0.19** (n = 35).
  - On Epoch's primary Dec-2025 files alone: ARC-AGI-1 vs GPQA Diamond ρ = 0.883 (n = 21, p = 1e-7) [C, H; epoch2025stitching].
- **Answer: no.** In 2024-26, "skill-acquisition efficiency" as ARC operationalises it is **not distinguishable from g in practice**. Its specific variance is about 4-5% of the total (see the residual analysis above). It is g-loaded (H).

### 3. MathTutorBench (task 1c)

**Data.** The README leaderboard [macina2025mathtutorbench] lists **17 models**, parsed from https://raw.githubusercontent.com/eth-lre/mathtutorbench/main/README.md. "Pedagogy" is my composite: the mean of Scaffolding Win Rate, Pedagogy-IF Win Rate, Scaffolding (Hard) and Pedagogy-IF (Hard). Its Cronbach α across these four columns is 0.95 over 17 models, and 0.91 for the 12 general-purpose models. Bootstrap uses 10,000 resamples [C, H].

| Pair | n | Spearman [95% CI] | Pearson [95% CI] |
|---|---|---|---|
| Problem Solving vs Pedagogy composite | 17 | **0.756 [0.34, 0.92]** | **0.426 [0.07, 0.83]** |
| PS vs Scaffolding Win Rate | 17 | 0.477 [-0.07, 0.83] | 0.282 [-0.14, 0.75] |
| PS vs Pedagogy-IF (Hard) | 17 | 0.741 [0.40, 0.90] | 0.521 [0.20, 0.83] |
| Expertise composite (5 solving/diagnosis columns) vs Pedagogy | 17 | 0.892 [0.60, 0.99] | 0.687 [0.44, 0.93] |
| PS vs Pedagogy, excluding 5 specialised tutors or fine-tunes | 12 | 0.839 [0.48, 0.96] | 0.563 [0.32, 0.93] |

**Comparison with the published 0.421** (8 models) [tutordiag2026]. That figure matches my 17-model *Pearson* of 0.426, but it is the wrong statistic here:
- The Pearson is driven by Qwen2.5-Math-7B-Instruct (PS 0.88, pedagogy 0.06) and Apertus-8B (0.76, 0.14). Both are specialisation or instruction-following failures.
- Problem Solving is near ceiling (0.88-0.98) for the strongest 9 models.

On ranks, pedagogy tracks solving (0.76), and it tracks the broader expertise composite even more closely (0.89). The verdict is **g-loaded, with specialisation outliers**. The claim "strong problem solvers are not automatically strong tutors" is true for specialised fine-tunes. It is not a general dissociation among general-purpose models.

### 4. EvaLearn (task 1d)

**Source:** the official repo's `EvaLearn-paper.pdf` and README [evalearn2025] (H).

**Exact claims:**
- Abstract: "we observe that current LLMs with stronger static abilities do not show a clear advantage in learning capability across all tasks".
- Finding (d): the metrics "are not strongly correlated with static model capability".
- §3.4: "learning capability is not strongly correlated with a model's inherent static ability".

No correlation coefficient appears anywhere in the extracted text. The claim rests on examples, e.g. "DeepSeek-R1 … experiences a 9% drop … while Claude-3.7-Sonnet achieves a 7.2% gain".

**N.**
- The abstract and §3.1 say **nine** models.
- Table 2 in the repo PDF lists **11**: the nine plus Gemini-2.5-Pro and Gemini-2.5-Flash.
- The sequence file has 182 sequences × 7 problems = 1,274 slots over 648 problems, so **problems are reused across sequences**. This confirms a previously unverified note [C, H].

**My computation** (overall accuracy, Table 2, zero-shot vs feedback learning) [C, H]:

| Pair | n | Spearman [95% CI] | Pearson |
|---|---|---|---|
| Zero-shot vs feedback-learning accuracy | 11 | **0.90 [0.60, 1.0]** | 0.92 |
| Zero-shot vs gain (FB - ZS) | 11 | **-0.61 [-0.92, 0.02]** | -0.39 |
| Zero-shot vs gain | 9 (excl. Gemini) | -0.57 [-0.98, 0.23] | -0.40 |
| Zero-shot vs P_offset (Table 4) | 11 | -0.20 [-0.77, 0.64] | - |

- Gains range from -9.3 to +10.5 pp (SD 5.7).

**Interpretation:**
- Post-learning accuracy is g-dominated.
- The gain is a difference score. Its negative relation to baseline is what regression to the mean and ceiling effects would produce. For example, Gemini-2.5-Pro starts at 68.5% and gains -1.3; o3-mini starts at 54.3% and gains +10.5.
- The paper reports no reliability for the gain.
- **Verdict: indeterminate.** The gain looks off-g, but its reliability is unknown and it is confounded with baseline.

### 5. EducationQ (task 1e)

**Source:** the official repo PDF (ACL 2025), Table 4: 14 teachers, fixed student Llama 3.1 70B Instruct, 1,498 questions [educationq2025] (H).

**Results.** Absolute learning gain (ALG) ranges from 1.20 (Phi-3.5-mini) to 11.01 (Llama 3.1 70B = the student). I matched 8 teachers to ECI-refit scores [C, M]:
- All 8: ρ(ALG, ECI-refit) = **0.12 [-0.74, 0.84]**.
- Excluding teacher = student: ρ = 0.50 [-0.41, 0.96] (n = 7).
- Excluding all Llama-family teachers: ρ = 0.80 (n = 5; CI not estimable).

**Confounds.**
- The top teacher is the student model itself. Llama-derived teachers also rank 1st, 3rd, 6th and 7th, which suggests a family-similarity advantage.
- Test-retest was run for only 3 teachers on GPQA-main (ALG R1/R2: 6.92/6.92, 5.58/5.80, 4.69/4.91).
- The paper reports cross-dataset ranking consistency r = 0.871 (GPQA-Diamond vs MMLU-Pro-Stratified) (H).

**Verdict: indeterminate**, and confounded.

### 6. Forecasting and calibration (task 1f)

**ForecastBench baseline leaderboard** (`forecastbench-datasets`, `leaderboards/csv/leaderboard_baseline.csv`, updated 2026-09-29) [karger2025forecastbench; fri2026forecastbenchdata].
- The ForecastBench team ran 121 LLM configurations. The score is the "Overall" difficulty-adjusted Brier index (higher is better) with 95% CIs.
- I matched 70 model groups to the ECI-refit, taking the maximum over prompt variants [C, H].

| Subset | n | Spearman with ECI-refit [95% CI] | Pearson | Reliability (from CIs) | Disattenuated Pearson |
|---|---|---|---|---|---|
| All matched | 70 | 0.625 [0.44, 0.76] | 0.728 | 0.95 | 0.77 |
| ECI-refit ≥ 140 | 36 | **0.049 [-0.26, 0.35]** | 0.13 | **0.885** | **0.14** |
| ECI-refit ≥ 150 | 14 | 0.21 [-0.34, 0.67] | 0.18 | 0.645 | 0.23 |

- Frontier scores are flat:
  - Claude Opus 4.8: 59.8. GPT-5.5: 60.7. GPT-5.4: 58.6. Gemini 3.1 Pro: 59.1. o3 (scratchpad): 61.7. Claude Sonnet 4.6 (adaptive thinking): 62.0.
  - Superforecaster median: 67.7. Public median: 62.6.
- Among ECI ≥ 140 models, the score is not related to release date either (ρ = -0.11), so knowledge recency does not explain it.
- The Epoch-ingested ForecastBench column gives LOO ρ = 0.45 (all) and **-0.27 at ECI ≥ 140** (n = 32).
- ForecastBench's own README calls it "a valuable proxy for general intelligence" (H), which the frontier data contradict.
- **Verdict: off-g likely among frontier models** (M; the no-retrieval ceiling is an alternative explanation).

**Calibration vs proper scores (Safetywashing data, 2024 open models)** [ren2024safetywashing]. I recomputed capability PC1 exactly as in the repo's `analysis.py`: Spearman PC1 over 12 capability benchmarks. PC1 explains 78.3% of variance (base) and 70.8% (chat) [C, H].

| Metric (higher = better) | Base models, n = 27 | Chat models, n = 26 |
|---|---|---|
| 1-RMS calibration error, MMLU | **-0.02** | **0.41** |
| 1-RMS calibration error, MMLU (temperature-tuned) | -0.36 | **0.05** |
| 1-Brier, MMLU | **0.92** | **0.84** |
| TruthfulQA MC1 | 0.70 | 0.81 |
| MWE sycophancy (non-sycophantic rate) | **-0.66** | **-0.67** |
| EQ-Bench | 0.57 | 0.71 |

- Brier mixes accuracy (resolution) with calibration, so it is g-loaded. Pure calibration error is not.
- **KalshiBench** [nel2025kalshibench]: 5 frontier models, so no correlation is possible. The GPT-5.2-XHigh vs Claude Opus 4.5 ECE contrast is an anecdote (M-H, existing dossier).
- **AbstentionBench** [kirichenko2025abstention]: "scaling is of little use" is an abstract claim, and I found no coefficient (S, existing dossier).

### 7. Literature sweep (task 2)

- **Honesty (MASK)** [ren2025mask]. The official README says "scaling pre-training does not improve model honesty" (H). Search extracts of the arXiv HTML give Spearman(compute, honesty) = **-0.599** and Spearman(compute, accuracy) = **+0.873** (M: two consistent search extracts of one source; the full text was not fetched). The number of models is "a diverse set" and I did not verify the count. Verdict: **off-g likely**, or even negatively related to capability. It is a propensity, not an ability.

- **Multi-turn underspecified conversation** [laban2025lost]. I transcribed Table 1 from the official README image (15 models, 6 tasks, FULL / CONCAT / SHARDED) and computed on the 5 tasks with complete data [C, H]:
  - Sharded (multi-turn) vs full (single-turn) mean: Spearman **0.90 [0.62, 0.99]**, Pearson **0.98**.
  - Retention (sharded/full, the paper's column) ranges 50.5-66.1% (SD 4.8). It correlates ρ = **0.50 [-0.03, 0.84]** with single-turn performance. Top-half models retain 63.4% and bottom-half 58.3%.
  - Answer: **the degradation is similar across strong and weak models**, with only a weak tendency for stronger models to degrade less. The absolute multi-turn score is g-loaded.
  - Headline figures: "average drop of 39%"; aptitude "-15%" and unreliability "+112%" (M, search extracts of the paper and an author post).
  - MultiChallenge (above): ρ = 0.82, disattenuated about 0.93.
  - Verdict: **g-loaded** (absolute); retention is indeterminate (narrow range).

- **Learning from feedback (MINT)** [wang2024mint]. 20 LLMs, all 2023-era. "Better single-turn performance does not guarantee better multi-turn performance"; SIFT and RLHF "generally hurt multi-turn capabilities"; +2-17% gains from language feedback (M-H: official README plus search extracts; the leaderboard website was blocked, so I computed no coefficient). Verdict: **indeterminate**, and not frontier.

- **Demonstration-scaling curves.**
  - Many-shot ICL [agarwal2024manyshot]: mostly Gemini 1.5 Pro, with GPT-4-Turbo and Claude-3-Opus only on low-resource MT (M, search extracts). Too few models for individual differences. The NeurIPS 2024 venue was not checked.
  - LMAct [ruoss2025lmact], ICML 2025: 8 models (Claude 3.5 Sonnet, Gemini 1.5 Flash/Pro, Gemini 2.0 Flash Exp, GPT-4o, o1-mini, o1-preview, o1). "Often, presenting more demonstrations has little effect. Some models steadily improve with more demonstrations on a few tasks" (H, README).
  - Flat curves leave little between-model variance in slope, so slope reliability will be low.
  - Verdict: **indeterminate**. A slope is a weak individual-difference measure.

- **Overriding semantic priors** [wei2023larger]. Overriding flipped labels "is an emergent ability of model scale"; instruction tuning strengthens reliance on priors more than input-label learning (M, search extracts; GPT-3, InstructGPT, Codex, PaLM and Flan-PaLM). Verdict: **g-loaded / scale-dependent**.

- **Sycophancy.**
  - Safetywashing data: ρ = -0.66 / -0.67 with capability (H, computed above).
  - Wei et al. 2023 [wei2023sycophancy]: "both model scaling and instruction tuning significantly increase sycophancy for PaLM models up to 540B parameters" (M, search extracts).
  - Verdict: **negatively g-related** (|ρ| about 0.67). There is specific variance, but it is not independent of capability.

- **Delegation, orchestration and collaboration.**
  - CooperBench [khatua2026cooperbench]: 5 models (full-text mirror, H). Solo/Coop success: GPT-5 0.48/0.28; Claude Sonnet 4.5 0.47/0.26; MiniMax-M2 0.36/0.14; Qwen3-Coder 0.22/0.13; Qwen3 0.06/0.05. **Coop ranks equal Solo ranks** (ρ = 1.0, n = 5) [C]. Retention (0.58, 0.55, 0.39, 0.59, 0.83) is non-monotone. "Agents achieve on average 30% lower success rates when working together".
  - Kim et al. [kim2025scalingagents]: 260 configurations, 3 families, 9 models. Multi-agent performance "improves consistently with increasing model Intelligence Index" under every architecture. Coordination returns turn negative once single-agent baselines exceed about 45% (β = -0.408, per search extracts) (H for the full-text quotes; M for β).
  - The Collaboration Gap [davidson2025collabgap]: 32 models. "Models that perform well solo often degrade substantially when required to collaborate" (M). I found no solo-vs-collaboration coefficient.
  - Verdict: absolute delegation performance is **g-loaded**. The coordination *gain* is negatively related to capability, so it is indeterminate as a construct.

- **ADeLe** [zhou2025generalscales]: 15 LLMs, full-text mirror (H).
  - CL (conceptualisation, learning and abstraction) "looks quite central in the manifold". The two demand correlations above 0.8 both involve CL, with MC and QLl.
  - Reasoning (chain-of-thought) models boost "quantitative and logical reasoning, learning and abstraction, and perhaps surprisingly, mind modelling and social capabilities". Knowledge abilities track model size.
  - MCu (calibrating knowns and unknowns) has "steep" curves "with low variability across models".
  - Verdict: learning/abstraction and social cognition follow the reasoning (g-like) axis. They are **g-loaded**, but in a population of only 15 models.

- **Agentic predictability** [ruan2024observational]: "the agent performance of models such as GPT-4 can be precisely predicted from simpler non-agentic benchmarks" (H, full-text mirror). In the ECI-refit table, METR time horizon has LOO ρ = 0.965 and disattenuated R about 1.0 [C].

### 8. One row per candidate (task 3)

Notes on the columns:
- "Frontier" means that at least one 2025-26 frontier model is included.
- ρ is Spearman unless stated.
- rel = reliability (binomial KR-21-style unless stated).
- "disatt." = disattenuated.

| Construct | Study | N (frontier?) | Capability proxy | r [95% CI] | Reliability | Disatt. r | Verdict | Conf. | Source |
|---|---|---|---|---|---|---|---|---|---|
| Skill-acquisition efficiency (static puzzles) | ARC-AGI-2 (Epoch data) [C] | 66 (yes) | LOO ECI-refit | 0.953 [0.91, 0.97] | 0.99 | 0.97 | **g-loaded** | H | https://github.com/linkofrivia/ECI_Bayesian ; https://github.com/epoch-research/benchmark-stitching |
| Same | ARC-AGI-1 [C] | 69 (yes) | LOO ECI-refit | 0.966 [0.93, 0.98] | n/a | n/a | **g-loaded** | H | same |
| Learning new knowledge from context | CL-bench [C] | 19 (all 2025-26) | LOO ECI-refit | 0.71 [0.40, 0.89] | 0.95 (LLM-rubric; upper bound) | 0.76 | indeterminate (moderately off-g at most) | M | https://github.com/Tencent-Hunyuan/CL-bench + ECI_Bayesian |
| Same, real-life contexts | CL-bench Life [C] | 13 (all 2025-26) | LOO ECI-refit | 0.82 [0.49, 0.98] | n/a | n/a | g-loaded (small N) | L-M | same |
| Sequential learning from feedback | EvaLearn [C] | 11 (2025, incl. Gemini-2.5-Pro) | Zero-shot accuracy, same items | FB accuracy 0.90 [0.60, 1.0]; gain -0.61 [-0.92, 0.02] | not reported | n/a | accuracy g-loaded; gain indeterminate | M | https://github.com/ByteDance-Seed/EvaLearn (EvaLearn-paper.pdf) |
| Learning from feedback | MINT | 20 (no; 2023) | Single-turn accuracy | not extracted | n/a | n/a | indeterminate | M | https://github.com/xingyaoww/mint-bench |
| Demonstration scaling | LMAct | 8 (partly; o1 era) | n/a | not computable | low (flat curves) | n/a | indeterminate | M | https://github.com/google-deepmind/lm_act |
| Demonstration scaling | Many-shot ICL | about 3 families (no) | n/a | n/a | n/a | n/a | indeterminate | L-M | arXiv:2404.11018 (search) |
| Overriding priors in ICL | Wei et al. 2023 | GPT-3/PaLM families (no) | Scale | qualitative: emerges with scale | n/a | n/a | g-loaded | M | arXiv:2303.03846 (search) |
| Teaching (pedagogy, reward model) | MathTutorBench [C] | 17 (yes: Gemini 3.1 Pro, 3.6 Flash, Sonnet 4.6) | Problem-solving column | ρ 0.76 [0.34, 0.92]; Pearson 0.43 [0.07, 0.83] | pedagogy α = 0.95 | ≈0.78 (ρ/√0.95) | **g-loaded** on ranks; specialisation outliers | M-H | https://raw.githubusercontent.com/eth-lre/mathtutorbench/main/README.md |
| Teaching (rubric) | TutorBench (SEAL) [C] | 19 (yes) | LOO ECI-refit | 0.66 [0.21, 0.89] | 0.94 (upper bound) | 0.76 | indeterminate; residual shared with other Scale rubric boards | M | ECI_Bayesian (Scale SEAL rows) |
| Teaching (student learning gain) | EducationQ [C] | 8 of 14 matched (no; 2024) | ECI-refit | 0.12 [-0.74, 0.84]; 0.50 excluding self-teaching | 3-model retest only | n/a | indeterminate (confounded) | L-M | https://github.com/SunriserFuture/EducationQ (paper PDF) |
| Forecasting accuracy | ForecastBench baseline [C] | 70; 36 at ECI ≥ 140 (yes) | ECI-refit | all 0.63 [0.44, 0.76]; frontier 0.05 [-0.26, 0.35] | 0.95 all; 0.885 frontier (from CIs) | 0.77 all; **0.14 frontier** | **off-g likely (frontier)** | M-H | https://github.com/forecastingresearch/forecastbench-datasets |
| Forecasting accuracy (Epoch-ingested) | ForecastBench (Epoch) [C] | 63 (yes) | LOO ECI-refit | 0.45 [0.20, 0.65]; -0.27 at ≥ 140 | n/a | n/a | off-g likely | M | ECI_Bayesian |
| Calibration error | Safetywashing data [C] | 26 chat / 27 base (no; 2024 open) | Capability PC1 | 1-RMSCE: 0.41 chat, -0.02 base; temperature-tuned 0.05 | n/a | n/a | **off-g likely** | M-H | https://github.com/centerforaisafety/safetywashing |
| Proper score (Brier) | Safetywashing data [C] | 26 / 27 (no) | Capability PC1 | 0.84 / 0.92 | n/a | n/a | **g-loaded** | M-H | same |
| Calibration (markets) | KalshiBench | 5 (yes) | Accuracy | not computable | n/a | n/a | indeterminate | M | existing dossier |
| Abstention | AbstentionBench | 20 (yes, 2025) | Scale / reasoning | "scaling is of little use" (no coefficient) | n/a | n/a | indeterminate | L-M | existing dossier |
| Honesty under pressure | MASK | "diverse set" (count unverified) | Training compute | honesty -0.599; accuracy +0.873 | n/a | n/a | **off-g likely** (negative) | M | https://github.com/centerforaisafety/mask ; arXiv:2503.03750 |
| Sycophancy | Safetywashing MWE-sycophancy [C] | 26 / 27 (no) | Capability PC1 | -0.67 / -0.66 | n/a | n/a | negatively g-related | M-H | https://github.com/centerforaisafety/safetywashing |
| Sycophancy | Wei et al. 2023 | PaLM ≤ 540B (no) | Scale | increases with scale | n/a | n/a | g-related (positive for sycophancy) | M | arXiv:2308.03958 (search) |
| Multi-turn underspecified conversation | Lost in Conversation [C] | 15 (yes: o3, R1, Gemini-2.5) | Single-turn (FULL) | absolute 0.90 [0.62, 0.99]; retention 0.50 [-0.03, 0.84] | n/a | n/a | absolute **g-loaded**; retention indeterminate | H (table) | https://github.com/microsoft/lost_in_conversation |
| Multi-turn instruction retention | MultiChallenge [C] | 28 (yes) | LOO ECI-refit | 0.82 [0.58, 0.95] | 0.92 | 0.93 | **g-loaded** | M | ECI_Bayesian |
| Long-context comprehension | Fiction.LiveBench [C] | 33 (yes) | LOO ECI-refit | 0.73 [0.47, 0.86] | 0.89 | 0.78 | indeterminate | M | ECI_Bayesian |
| Knowledge / factuality | SimpleQA Verified [C] | 78 (yes) | LOO ECI-refit | 0.74 [0.60, 0.83] | 0.995 | 0.74 | off-g likely (knowledge / family effect) | M-H | ECI_Bayesian |
| Tool use | SEAL Tool Use / MCP Atlas [C] | 29 / 29 (yes) | LOO ECI-refit | 0.88 / 0.80 | 0.95 / 0.98 | 0.88 / 0.84 | g-loaded (strong family effects) | M | ECI_Bayesian |
| Agentic long-horizon | METR time horizon [C] | 36 (yes) | LOO ECI-refit | 0.965 [0.91, 0.98] | 0.95 | ≈1.0 | **g-loaded** | M-H | ECI_Bayesian; [ruan2024observational] |
| Collaboration / delegation | CooperBench [C] | 5 (yes) | Solo success | ρ = 1.0 (ranks identical) | n/a | n/a | absolute g-loaded; gap indeterminate | M | arXiv:2601.13295 (full-text mirror) |
| Orchestration gain | Kim et al. 2025 | 9 models, 3 families (yes) | Intelligence Index | MAS performance rises with the index; gain β = -0.408 above about 45% | n/a | n/a | g-loaded; gain negatively related | M | arXiv:2512.08296 (full-text mirror) |
| Learning/abstraction; social | ADeLe | 15 (partly; o1 era) | Model family and size | qualitative: CL central; reasoning boosts CL and MS | n/a | n/a | g-loaded (reasoning axis) | M | full-text mirror of arXiv:2503.06378 |

### 9. Strongest counter-evidence to "learning ability is off the general factor" (task 4)

1. **ARC-AGI.** The field's flagship "skill-acquisition efficiency" benchmark:
   - is among the most g-loaded of 78 benchmarks (LOO ρ 0.95-0.97; disattenuated 0.97; third-highest discriminability);
   - saturated alongside general frontier progress (95% on ARC-AGI-2 within about 18 months);
   - keeps a higher g-correlation among frontier models (0.80-0.84) than GPQA does (0.51) [C, H].
   
   Its reliable specific variance is only about 4-5% of the total.
2. **Whenever learning is scored as performance after learning, g dominates:**
   - EvaLearn feedback-learning accuracy vs zero-shot: ρ = 0.90.
   - Lost-in-Conversation multi-turn vs single-turn: ρ = 0.90, Pearson 0.98.
   - MathTutorBench pedagogy vs problem solving: ρ = 0.76, and 0.89 against the expertise composite.
   - CL-bench vs ECI-refit, even inside a range-restricted frontier sample: 0.71.
   - ADeLe finds the learning/abstraction demand "central in the manifold".
   
   Off-g signals appear only in *difference scores* (EvaLearn gain, conversation retention, coordination gap). These have narrow ranges and unreported reliability, and they are prone to regression to the mean.
3. **Complex capabilities are predictable from simple ones:** agentic performance [ruan2024observational]; multi-agent performance rising with the Intelligence Index under every architecture [kim2025scalingagents].
4. **T5 is borne out.** The lowest correlations in the Epoch set come from:
   - benchmarks with the lowest reliability (DeepResearchBench, rel 0.63);
   - near-ceiling or compressed ranges (LAMBADA, TriviaQA, PIQA, SEAL IF);
   - benchmarks whose residuals are explained by developer family (MCP Atlas η² 0.75; SWE-bench Verified 0.50).
   
   A low correlation is not evidence of a construct.
5. **Where published "off-g" teaching or learning claims were tested, they weakened:**
   - MathTutorBench: Pearson 0.43 but Spearman 0.76.
   - EducationQ: self-teaching confound.
   - EvaLearn: no coefficient; N is 9 or 11.

### 10. Minimum N and reliability to demonstrate a residual (task 4)

The Fisher-z SE of r is about 1/sqrt(n-3). Assume a one-sided α = 0.05, power 0.8, and ECI reliability 0.95 (it drops to 0.86 at ECI ≥ 150). The table gives the number of models needed to reject a disattenuated ρ0 when the true value is ρ1 [C]:

| Null ρ0 | rel_B | ρ1 = 0.60 | 0.70 | 0.75 | 0.80 | 0.85 |
|---|---|---|---|---|---|---|
| 0.90 ("collapse") | 0.70 | 42 | 78 | 125 | 252 | 897 |
| 0.90 | 0.80 | 31 | 55 | 85 | 166 | 570 |
| 0.90 | 0.90 | 23 | 38 | **57** | **106** | 346 |
| 0.90 | 0.95 | 19 | 31 | 46 | 83 | 262 |
| 1.00 ("pure g + noise") | 0.90 | 10 | 12 | 14 | 17 | 23 |

**Residual-reliability test.** Correlate the ECI-residuals of two parallel halves of the new benchmark. Detecting a split-half residual correlation of at least 0.5, 0.4 or 0.3 (vs 0) needs N = 24, 38 or 68 [C].

**95% CI widths for r:**
- n = 30: r = 0.7 → [0.45, 0.85]; r = 0.9 → [0.80, 0.95].
- n = 50: r = 0.7 → [0.52, 0.82].
- n = 80: r = 0.7 → [0.57, 0.80].

**Constraints** [C, M]:
- *Model supply.* As of the Aug-2026 snapshot, Epoch data hold only **43 model groups at ECI-refit ≥ 150**, 94 at ≥ 140 and 160 at ≥ 120. A frontier-only design cannot reach N ≈ 100, so the sample must span about ECI 120-165.
- *Clustering.* Models cluster in about 11 families, and family explains up to 50-75% of residual variance on some benchmarks. The effective N is closer to the number of families than the number of models unless family is modelled as a random effect.

**Recommendation** [I]:
- At least 60 models (target 100) from at least 10 families.
- Headline-score reliability of at least 0.9 on the item/run-sampling definition, estimated by split halves with an LLM-judge component if a judge is used.
- Split-half *residual* reliability of at least 0.5.
- Pre-register the falsifier: if the disattenuated LOO-ECI r is 0.9 or more, the construct collapses into g.

---

## Implications for designing a new benchmark

All items are [I], grounded in the findings above.

1. **Demote "learning is off-g" from premise to pre-registered hypothesis.** The best existing evidence points the other way:
   - ARC (H): ρ = 0.95-0.97.
   - CL-bench (M): 0.71 in a restricted range.
   - Performance after learning is g-dominated across EvaLearn, MathTutorBench and Lost in Conversation.
   
   Brief D S6 should be downgraded from "moderate" to "weak / contested" for learning and teaching. It stays "moderate" for forecasting and calibration error.
2. **Headline two numbers, but let the data decide which one is the construct.**
   - (a) Position on the linked ECI-style scale. A loading of about 0.8-0.95 should be expected, and that is fine for linking.
   - (b) A residual, *only if* it passes three tests: split-half residual reliability of at least 0.5; a disattenuated LOO-ECI r significantly below 0.9; and convergent correlation with a different-format measure of the same construct that exceeds its correlation with same-format measures of other constructs (MTMM).
   
   If the residual fails, report the benchmark as a contamination-proof, renewable g-measure with a learning *format*. That is still useful, but it is a different paper.
3. **Score learning as a within-model effect, not a between-model difference score.**
   - Use a parallel-form pre/post or a no-material control condition per item family, and estimate the learning effect hierarchically (items × models) so that its reliability can be computed.
   - Report the reliability of the learning score. For a difference score this can be computed with Lord's formula; the Brief treats it as unknown.
   - Correct for regression to the mean by modelling the gain conditional on the baseline.
4. **The calibration overlay must be decomposed.**
   - Brier and log scores are g-loaded (0.84-0.92). Calibration error is not (-0.02 to 0.41).
   - Report the Murphy decomposition (reliability / resolution / uncertainty) or ECE alongside the proper score. Put the calibration component, not the proper score, in the residual claim.
5. **Prioritise constructs with better off-g evidence if the goal is unique signal:**
   - forecasting and calibration error (frontier ρ ≈ 0.05; reliability 0.885);
   - honesty and sycophancy propensities (MASK compute-honesty -0.60; sycophancy ≈ -0.67).
   
   The latter are propensities; their "off-g" status partly reflects training choices.
6. **Sample design.** At least 60-100 models from at least 10 families, spanning ECI about 120-165.
   - Family enters as a random effect, with a family-clustered bootstrap.
   - Re-score two yardstick benchmarks (e.g. ARC-AGI-2 and GPQA Diamond) on the *same* sample, so that the new benchmark's g-loading is read relative to them under identical range restriction.
   - Use leave-one-out ECI when the new benchmark enters the scale.
7. **Teaching arm.**
   - Never let the teacher and student share a family (EducationQ's top teacher *was* the student).
   - Score student gain on held-out generated material with an exact verifier, not a reward model.
   - Test whether pedagogy residuals co-vary with other rubric-judged chat benchmarks; TutorBench's residual does (0.56-0.66), which signals a method factor.
8. **Keep ARC as the cautionary tale in the paper's related work.** A benchmark designed around skill acquisition became a high-discrimination g-measure. This supports designing *for* measurement quality (renewability, linking, reliability) as the primary contribution, with off-g as a tested secondary claim.

---

## Claims ledger

| # | Claim | Source URL(s) | Confidence |
|---|---|---|---|
| 1 | The ECI-refit (official `eci-public` code on a mirror of Epoch's 2026-08-07 benchmark ZIP) gives 276 model groups and 96 benchmarks | https://github.com/epoch-research/eci-public ; https://github.com/linkofrivia/ECI_Bayesian (data/processed/benchmarks_merged.csv; data/pipeline/output/pipeline_report.md) | M (mirror) [C] |
| 2 | The mirror matches Epoch's primary repo: ARC-AGI 51 rows, max abs diff 0.005; GPQA Diamond 132 rows, 96% within 0.01 | https://github.com/epoch-research/benchmark-stitching (data/external_benchmark_arc_agi.csv; data/benchmarks_runs.csv) | H [C] |
| 3 | ARC-AGI-1 LOO ECI-refit ρ = 0.966 [0.934, 0.980], n = 69; ARC-AGI-2 ρ = 0.953 [0.906, 0.972], n = 66; ARC-AGI-2 disattenuated R = 0.971 | as #1, #2 | H [C] |
| 4 | ARC-AGI-2 has the 3rd-highest fitted discriminability (0.268) of 96 benchmarks; ARC-AGI-1 0.192 | as #1 | M [C] |
| 5 | ARC-AGI-2 vs GPQA Diamond ρ = 0.917 (n = 53); ARC-AGI-1 vs GPQA ρ = 0.883 (n = 21) on Epoch primary files | as #1, #2 | H [C] |
| 6 | Among ECI-refit ≥ 150: ARC-AGI-1 0.84, ARC-AGI-2 0.80 (n = 25) vs GPQA 0.51 (n = 33) | as #1 | M [C] |
| 7 | ARC-AGI-1 and ARC-AGI-2 ECI-residuals correlate 0.45 (n = 63) | as #1 | M [C] |
| 8 | CL-bench tests learning of new knowledge from context: 1,899 tasks, 500 contexts (search), 31,607 rubrics (search) / avg 63.2 rubrics per context (README) | https://github.com/Tencent-Hunyuan/CL-bench | H |
| 9 | CL-bench vs LOO ECI-refit ρ = 0.711 [0.40, 0.89], n = 19 (ECI 143-157); disattenuated 0.76 | as #1 | M [C] |
| 10 | TutorBench vs LOO ECI-refit ρ = 0.660 [0.21, 0.89], n = 19; its residual correlates with MultiChallenge (0.66, n = 16) and PRBench (0.56-0.57, n = 13) | as #1 | M [C] |
| 11 | MathTutorBench README lists 17 models; PS vs pedagogy composite Spearman 0.756 [0.34, 0.92], Pearson 0.426 [0.07, 0.83] | https://raw.githubusercontent.com/eth-lre/mathtutorbench/main/README.md | H [C] |
| 12 | The 8-model 0.421 solving-pedagogy correlation | https://github.com/qhduan/cn-chat-arxiv (via prior_art dossier) | M |
| 13 | The EvaLearn abstract says nine models, but Table 2 of the repo PDF lists 11 (adds Gemini-2.5-Pro/Flash); no correlation coefficient is reported | https://github.com/ByteDance-Seed/EvaLearn (EvaLearn-paper.pdf, readme.md) | H |
| 14 | EvaLearn: 182 sequences × 7 problems over 648 problems (problems reused) | https://github.com/ByteDance-Seed/EvaLearn (Dataset/EvaLearn_Sequence.json) | H [C] |
| 15 | EvaLearn: ZS vs FB accuracy ρ = 0.90; ZS vs gain ρ = -0.61 [-0.92, 0.02] (n = 11) | as #13 | H [C] |
| 16 | EducationQ: 14 teachers, student Llama 3.1 70B, ALG 1.20-11.01; ALG vs ECI-refit ρ = 0.12 (n = 8), 0.50 excluding self-teaching | https://github.com/SunriserFuture/EducationQ (docs/2025.acl-long.1576.pdf) | H (table); M [C] (ECI match) |
| 17 | ForecastBench baseline: 70 matched models, ρ = 0.625; at ECI ≥ 140, ρ = 0.049 [-0.26, 0.35] (n = 36), reliability 0.885 from published CIs | https://github.com/forecastingresearch/forecastbench-datasets (leaderboards/csv/leaderboard_baseline.csv) | H (data); M (ECI match) [C] |
| 18 | Superforecaster median 67.7 and public median 62.6 on ForecastBench baseline Overall | same | H |
| 19 | ForecastBench README: "serving as a valuable proxy for general intelligence" | https://raw.githubusercontent.com/forecastingresearch/forecastbench/main/README.md | H |
| 20 | Safetywashing data: 1-RMSCE(MMLU) vs capability PC1 -0.02 (base) and 0.41 (chat); 1-Brier 0.92 / 0.84; sycophancy -0.66 / -0.67 | https://github.com/centerforaisafety/safetywashing (data/*.csv, analysis.py) | H [C] |
| 21 | MASK: "scaling pre-training does not improve model honesty" | https://github.com/centerforaisafety/mask | H |
| 22 | MASK: Spearman(compute, honesty) = -0.599; Spearman(compute, accuracy) = +0.873 | arXiv HTML via search extracts (https://arxiv.org/html/2503.03750) | M |
| 23 | Lost in Conversation Table 1 (15 models): sharded vs full ρ = 0.90, Pearson 0.98; retention 50.5-66.1%, ρ with single-turn 0.50 | https://github.com/microsoft/lost_in_conversation (README; images/Lost_in_Conv_Main_Table.png) | H [C] |
| 24 | Lost in Conversation: average 39% drop; aptitude -15%, unreliability +112% | search extracts of arXiv:2505.06120 and an author post | M |
| 25 | MINT: 20 LLMs; "Better single-turn performance does not guarantee better multi-turn performance"; SIFT/RLHF hurt multi-turn | https://github.com/xingyaoww/mint-bench ; search extracts (ICLR 2024 proceedings) | M-H |
| 26 | LMAct: 8 models; "often, presenting more demonstrations has little effect" | https://github.com/google-deepmind/lm_act | H |
| 27 | Many-shot ICL: Gemini 1.5 Pro up to 1M tokens; GPT-4-Turbo and Claude-3-Opus on low-resource MT | search extracts of arXiv:2404.11018 | M |
| 28 | Wei et al. 2023: overriding flipped-label priors is emergent with scale | search extracts (Google Research blog; arXiv:2303.03846) | M |
| 29 | Wei et al. 2023b: scaling and instruction tuning increase sycophancy (PaLM ≤ 540B) | search extracts of arXiv:2308.03958 | M |
| 30 | CooperBench Solo/Coop per-model success rates (5 models); "30% lower success rates when working together" | https://github.com/elasticity-ai/stylized-facts (references/text/khatua2026cooperbench.txt) | H |
| 31 | Kim et al.: MAS performance rises with Intelligence Index; capability-saturation effect; β = -0.408 above about 45% | https://github.com/elasticity-ai/stylized-facts (references/text/kim2025scalingagents.txt); β via search extracts | H (quotes) / M (β) |
| 32 | Collaboration Gap: 32 models; solo-capable models degrade when collaborating | search extracts (arXiv:2511.02687; Microsoft Research page); cited in CooperBench full text | M |
| 33 | ADeLe: CL "quite central in the manifold"; reasoning models boost CL and MS | https://github.com/elasticity-ai/stylized-facts (references/text/zhou2025generalscales.txt) | H |
| 34 | Ruan et al.: agent performance "can be precisely predicted from simpler non-agentic benchmarks" | https://github.com/elasticity-ai/stylized-facts (references/text/ruan2024observational.txt) | H |
| 35 | Developer family explains a large share of residual variance: MCP Atlas η² 0.75, SWE-bench Verified 0.50, SimpleQA 0.24 (p = 0.016) | as #1 | M [C] |
| 36 | ECI-refit reliability: 0.97 (all), 0.91 (≥ 140), 0.86 (≥ 150); 43 model groups at ≥ 150 | as #1 | M [C] |
| 37 | Power table (Fisher z) and required N | computed | H (arithmetic) [C] |
| 38 | Third-party K = 3 MIRT puts ForecastBench (0.99), Chess, SEAL Tool Use and CL-bench on a second axis | https://github.com/linkofrivia/ECI_Bayesian (results/mirt_humanmerge_…/mirt_loadings.csv) | L-M |

---

## References

Existing keys (reused): ruan2024observational; zhang2025trainbeforetest; zhou2025generalscales; ren2024safetywashing; desai2026whatbenchmarks; heineman2025signal; ho2025rosetta; epoch2026ecipublic; epoch2025stitching; eciBayesian2026; chollet2019measure; kamradt2025arcagi2launch; alloevil2026tracker; evalearn2025; macina2025mathtutorbench; tutordiag2026; educationq2025; tutorbench2025; karger2025forecastbench; nel2025kalshibench; kirichenko2025abstention; yang2025prophetarena.

New keys (see refs/gap_offg_construct_evidence.json):

1. [ren2025mask] Ren, R., Agarwal, A., Mazeika, M., et al. (16 authors). The MASK Benchmark: Disentangling Honesty From Accuracy in AI Systems. arXiv:2503.03750, 2025. https://github.com/centerforaisafety/mask
2. [laban2025lost] Laban, P., Hayashi, H., Zhou, Y., Neville, J. LLMs Get Lost In Multi-Turn Conversation. arXiv:2505.06120, 2025. https://github.com/microsoft/lost_in_conversation
3. [wang2024mint] Wang, X., Wang, Z., Liu, J., Chen, Y., Yuan, L., Peng, H., Ji, H. MINT: Evaluating LLMs in Multi-turn Interaction with Tools and Language Feedback. arXiv:2309.10691; ICLR 2024. https://github.com/xingyaoww/mint-bench
4. [agarwal2024manyshot] Agarwal, R., Singh, A., Zhang, L. M., et al. Many-Shot In-Context Learning. arXiv:2404.11018, 2024 (venue per brief: NeurIPS 2024; unverified).
5. [ruoss2025lmact] Ruoss, A., Pardo, F., Chan, H., Li, B., Mnih, V., Genewein, T. LMAct: A Benchmark for In-Context Imitation Learning with Long Multimodal Demonstrations. arXiv:2412.01441; ICML 2025. https://github.com/google-deepmind/lm_act
6. [wei2023larger] Wei, J. W., Wei, J., Tay, Y., et al. Larger language models do in-context learning differently. arXiv:2303.03846, 2023.
7. [wei2023sycophancy] Wei, J., et al. Simple synthetic data reduces sycophancy in large language models. arXiv:2308.03958, 2023.
8. [dou2026clbench] Dou, S., Zhang, M., Yin, Z., et al. (27 authors). CL-bench: A Benchmark for Context Learning. arXiv:2602.03587, 2026. https://github.com/Tencent-Hunyuan/CL-bench
9. [dou2026clbenchlife] Dou, S., Shen, Y., Huang, C., et al. CL-bench Life: Can Language Models Learn from Real-Life Context? arXiv:2604.27043, 2026. https://github.com/Tencent-Hunyuan/CL-bench
10. [khatua2026cooperbench] Khatua, A., Zhu, H., Tran, P., et al. CooperBench: Why Coding Agents Cannot be Your Teammates Yet. arXiv:2601.13295, 2026.
11. [kim2025scalingagents] Kim, Y., Gu, K., Park, C., et al. Towards a Science of Scaling Agent Systems. arXiv:2512.08296, 2025.
12. [davidson2025collabgap] Davidson, T. R., Fourney, A., Amershi, S., West, R., Horvitz, E., Kamar, E. The Collaboration Gap. arXiv:2511.02687, 2025.
13. [fri2026forecastbenchdata] Forecasting Research Institute. forecastbench-datasets (leaderboards and datasets, nightly). https://github.com/forecastingresearch/forecastbench-datasets (accessed 2026-09-29).
14. [stylizedfacts2026mirror] elasticity-ai. stylized-facts: references/text full-text mirrors (used as seen_url for Ruan, ADeLe, Kim, Khatua). https://github.com/elasticity-ai/stylized-facts
