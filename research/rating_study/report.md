# Retrospective rating study: results

3 independent LLM raters (session-default, sonnet, fable) scored 39 benchmarks on 14 rubric factors (0-3 each; max total 42), outcome-blind by instruction.

## Reliability

- Krippendorff's alpha (interval), total score: **0.89**
- Pairwise Pearson r between raters' totals: 0.92, 0.92, 0.92
- Per-factor alpha: F1 0.92, F2 0.91, F3 0.66, F4 0.66, F5 0.75, F6 0.83, F7 0.84, F8 0.73, F9 0.90, F10 0.89, F11 0.82, F12 0.85, F13 0.68, F14 0.79

## Association with adoption outcome

- Mean total by outcome: not_adopted 14.4, partial 19.3, adopted 22.1
- Spearman rho (mean total vs outcome 0/1/2): **0.68** (95% bootstrap CI 0.45 to 0.82)
- AUC adopted vs not adopted: **0.93** (95% CI 0.83 to 1.00)

| Factor | AUC | mean (adopted) | mean (not adopted) | alpha |
|---|---|---|---|---|
| F14 Thesis, brand and story | 0.99 | 2.13 | 0.79 | 0.79 |
| F12 Differentiation and timing | 0.98 | 2.52 | 1.00 | 0.85 |
| F11 Product and decision relevance | 0.89 | 1.70 | 0.61 | 0.82 |
| F13 Single headline score in a human-legible, comparable unit | 0.84 | 1.53 | 0.79 | 0.68 |
| F9 Distribution and friction | 0.82 | 1.78 | 0.94 | 0.90 |
| F10 Maintained, independent, citable leaderboard with governance | 0.80 | 1.28 | 0.33 | 0.89 |
| F5 Launch headroom against a human anchor | 0.71 | 1.67 | 1.21 | 0.75 |
| F3 Statistical resolution | 0.65 | 1.07 | 0.82 | 0.66 |
| F4 Shortcut, tool and harness robustness | 0.64 | 1.38 | 1.12 | 0.66 |
| F2 Exact, automatic verification | 0.58 | 1.78 | 1.73 | 0.91 |
| F1 Construct definition and incremental validity | 0.53 | 1.52 | 1.39 | 0.92 |
| F6 Renewal mechanism and difficulty knob | 0.49 | 1.00 | 0.88 | 0.83 |
| F8 Item-quality assurance | 0.47 | 1.30 | 1.33 | 0.73 |
| F7 Contamination resistance (training-time and run-time) | 0.47 | 1.43 | 1.42 | 0.84 |

## Composite analysis

- measurement_and_longevity (F1, F2, F3, F4, F5, F6, F7, F8): AUC 0.61 (95% CI 0.38 to 0.81), Spearman 0.13
- ecosystem_and_narrative (F9, F10, F11, F12, F13, F14): AUC 1.00 (95% CI 0.98 to 1.00), Spearman 0.84

## Sensitivity analyses

- Ratings where the rater did not claim to know the outcome: 49 rater-benchmark pairs over 20 benchmarks (1 adopted, 11 not adopted); AUC 1.00, Spearman 0.68. (Uninformative for AUC when the blind subset contains very few adopted benchmarks.)
- Excluding the lead's ten benchmarks (n=29): AUC 0.79, Spearman 0.38.
- Game-based benchmarks (n=11) mean total 16.2 vs non-game 20.6; game outcomes {'not_adopted': 7, 'partial': 4, 'adopted': 0}.

## Per-benchmark mean totals

| ID | Benchmark | Year | Outcome | Mean total | Rater totals |
|---|---|---|---|---|---|
| B16 | ForecastBench | 2024 | adopted | 30.0 | 29, 32, 29 |
| B13 | LiveCodeBench | 2024 | adopted | 27.7 | 26, 28, 29 |
| B19 | MathArena | 2025 | adopted | 27.0 | 26, 28, 27 |
| B20 | GDPval | 2025 | adopted | 26.0 | 24, 28, 26 |
| B18 | Terminal-Bench | 2025 | adopted | 24.3 | 24, 25, 24 |
| B14 | FrontierMath | 2024 | adopted | 23.7 | 22, 26, 23 |
| B17 | Humanity's Last Exam | 2025 | adopted | 23.7 | 21, 24, 26 |
| B24 | Kaggle Game Arena | 2025 | partial | 23.7 | 21, 26, 24 |
| B12 | OSWorld | 2024 | adopted | 23.3 | 24, 23, 23 |
| B7 | MMMU | 2023 | adopted | 23.0 | 22, 24, 23 |
| B4 | GPQA | 2023 | adopted | 22.0 | 22, 22, 22 |
| B5 | SWE-bench | 2023 | adopted | 22.0 | 22, 24, 20 |
| B6 | Chatbot Arena | 2023 | adopted | 21.7 | 22, 21, 22 |
| B27 | IFBench | 2025 | partial | 20.7 | 19, 22, 21 |
| B11 | tau-bench | 2024 | adopted | 20.3 | 19, 21, 21 |
| B15 | BFCL (Berkeley Function Calling Leaderboard) | 2024 | adopted | 20.3 | 18, 22, 21 |
| B22 | Codenames ad-hoc concept forming | 2025 | partial | 20.3 | 18, 21, 22 |
| B25 | MTOB (Machine Translation from One Book) | 2023 | partial | 20.0 | 19, 19, 22 |
| B2 | HumanEval | 2021 | adopted | 19.7 | 18, 21, 20 |
| B37 | GTBench | 2024 | not_adopted | 19.0 | 17, 22, 18 |
| B38 | lmgame-Bench | 2025 | not_adopted | 19.0 | 18, 21, 18 |
| B1 | MMLU | 2020 | adopted | 18.7 | 19, 17, 20 |
| B23 | LLM Chess | 2025 | partial | 18.7 | 17, 19, 20 |
| B10 | ARC (Abstraction and Reasoning Corpus) | 2019 | adopted | 18.3 | 17, 20, 18 |
| B28 | ConceptARC | 2023 | partial | 18.0 | 15, 21, 18 |
| B3 | BIG-Bench Hard | 2022 | adopted | 17.7 | 17, 18, 18 |
| B39 | EducationQ | 2025 | not_adopted | 17.7 | 17, 20, 16 |
| B8 | IFEval | 2023 | adopted | 17.3 | 18, 16, 18 |
| B21 | MastermindEval | 2025 | partial | 17.0 | 17, 17, 17 |
| B34 | TopoBench | 2026 | not_adopted | 17.0 | 17, 18, 16 |
| B26 | MathTutorBench | 2025 | partial | 16.3 | 15, 18, 16 |
| B31 | Concept (Do You Get the Hint?) | 2025 | not_adopted | 15.7 | 15, 17, 15 |
| B9 | Needle-in-a-Haystack | 2023 | adopted | 15.3 | 18, 15, 13 |
| B33 | Grid-based game competitions | 2024 | not_adopted | 14.7 | 14, 14, 16 |
| B35 | From Raw Corpora to Domain Benchmarks | 2025 | not_adopted | 13.3 | 12, 13, 15 |
| B36 | BloomQA (Bloom's-taxonomy guideline benchmarks) | 2026 | not_adopted | 12.0 | 11, 11, 14 |
| B30 | Game Reasoning Arena | 2025 | not_adopted | 11.7 | 12, 11, 12 |
| B32 | Boardwalk | 2025 | not_adopted | 10.0 | 10, 11, 9 |
| B29 | Qi Town (Who is a Better Player: LLM against LLM) | 2025 | not_adopted | 8.0 | 8, 9, 7 |

## Caveats

- The rubric was derived from the same literature that describes these benchmarks, so this is a consistency check, not an out-of-sample validation.
- Raters are LLMs and most reported already knowing the outcome for most benchmarks; outcome leakage into design ratings cannot be excluded (see blind-subset analysis).
- Outcome labels were assigned by the synthesis agent from documented adoption evidence; 'partial' is heterogeneous.
