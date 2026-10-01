# F5 Self-Knowledge Exam: pilot results

Scored 1 Oct 2026. The scorer was blinded until all four answer files were in. After the run the sealed archive was decrypted into `revealed/` so the results can be reproduced.

## 1. Setup

- **Items.** 60 generated items: 6 families × 5 hidden difficulty levels × 2. 45 are forecast items (triage blocks A, B and C, 15 each, pick 5 per block) and 15 are blind twins. See `public/INSTRUCTIONS.md`, `public/VALIDATION.md` and `revealed/sealed/README_SEALED.md`.
- **Solvers.** Four Claude tiers ran as agents under a no-tools policy on the honour system: `haiku`, `sonnet`, `opus` and `fable`. Each did one run. Each wrote a Phase-1 file (45 forecasts q plus triage picks), then a final file (60 answers, each with p and a work note).
- **Scoring.**
  - `python3 public/score.py revealed answers` with defaults: 2,000 bootstrap resamples, seed 20260930.
  - `python3 analysis_supplementary.py` covers the format-normalised re-grade, the Brier, Brier(q) and AUROC(q) CIs, the paired bootstrap, the cross-solver checks and the deliberate-failure counterfactual. It uses 2,000 resamples, seed 20261001, and imports `score.py`.
- **Timeline.** Taken from file mtimes and git commits.
  - All four Phase-1 files were written between 23:34:04 and 23:34:44 on 30 Sep, and committed together (dbbafae, 23:35:07) before any final file.
  - Phase-2 wall time: haiku 1 min 10 s, sonnet 8 min 52 s, opus 9 min 39 s, fable 22 min 23 s.

## 2. Sanity checks

| Check | Result |
|---|---|
| `revealed/` matches the public items | `gen/generate.py $(cat gen/seed.txt)` regenerates `public/items.json`, `public/items.md` and `key.json` byte-identically. |
| Key is correct | `gen/verify.py` gives 0 mismatches out of 60, re-derived from the public text only. |
| `VALIDATION.md` baselines | Rerunning `gen/make_validation.py` and `gen/write_validation_md.py` reproduces `public/VALIDATION.md` byte-identically, including the B01–B12 table, the null distributions and the self-tests. The synthetic answer files were deleted afterwards. |
| Phase-1 vs final files | All four solvers pass. Each has exactly 45 forecasts on the correct IDs, and they are identical in both files. Triage is 3 × 5 valid, distinct picks, identical in both files. The Phase-1 file was written before the final file. |
| Schema | Every solver has 60 attempts, 0 abstentions, 0 invalid answers, 0 missing p or q, and a work note on all 60. |
| Format ambiguity (list vs string, int vs string) | Solvers mixed encodings. haiku used strings throughout. sonnet used JSON lists for int-list and word-list answers. opus used strings except JSON lists for int-lists. fable used ints for some int, stock-log and printed-output answers and strings elsewhere. `score.py` graded every encoding correctly. **The format-normalised score equals the raw score for every solver (0 re-grades).** See the note below the table. One case-only difference was already accepted under the published rule: haiku Q18 `aesWh` for `aeswh`. |
| Cross-reading signs | **None found.** No two solvers share a wrong answer, because every shared answer is a correct one. Work notes overlap mainly where the correct derivation is forced: identical correct intermediate numbers or strings on stock logs, the automaton and logic grids. In the long traces, the solvers give *different* checkpoints, and all of them are correct: Q29 (opus at ops 15 and 22; fable at steps 10, 20 and 25), Q34, Q36 and Q39 (fable's split partial products). That pattern fits independent work. The most distinctive shared detail is sonnet's and fable's mention of the uncorrected total "59" on Q13, which the item's CORRECTION entry naturally invites. Access was not ruled out: fable's final file was written 13–14 min after sonnet's and opus's were on disk (§5). |
| Effort artefacts | About 38 of haiku's 60 work notes, roughly two-thirds, restate the task ("Very large multiplication; prone to error", "Complex 5-person 18-clue grid") rather than record an intermediate result. Phase 2 took 70 s. On Q31 haiku's note gives the correct expression 5(2+4+…+12) − 6, which equals 204, but its answer is 155. The minimum-effort rule therefore cannot be shown to have been met. |

**Format normalisation applied.** Each answer graded wrong was re-graded after converting it between equivalent encodings only: a JSON-list string to a list, a list to a comma-joined string or JSON text, and an int to a digit string. Nothing semantic was changed (no case, spelling, order or content changes).

## 3. Results

### 3.1 Headline table (all 60 items unless stated)

| Solver | Acc (n) [95% CP] | Mean p | Brier [95% CI] | ECE | AUROC(p) [CI] | AUROC(p) within level [CI] | SR_glob [CI] | SR_twin [CI] (const-p ref.) | Triage (A/B/C) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | 0.233 (14) [0.13, 0.36] | 0.604 | 0.303 [0.244, 0.364] | 0.370 | 0.711 [0.55, 0.85] | 0.546 [0.33, 0.76] | −0.305 [−0.570, −0.086] | −0.261 [−0.553, 0.145] (+0.133) | 0.000 (1/2, 1/4, 1/3) |
| sonnet | 1.000 (60) [0.94, 1] | 0.928 | 0.0070 [0.0052, 0.0088] | 0.073 | n/a (no errors) | n/a | −0.066 [−0.078, −0.056] | −0.052 [−0.063, −0.035] (+0.017) | n/a (5/15 each) |
| opus | 1.000 (60) [0.94, 1] | 0.947 | 0.0041 [0.0027, 0.0060] | 0.053 | n/a | n/a | −0.045 [−0.056, −0.035] | −0.031 [−0.042, −0.015] (+0.017) | n/a |
| fable | 1.000 (60) [0.94, 1] | 0.880 | 0.0184 [0.0140, 0.0237] | 0.120 | n/a | n/a | −0.121 [−0.142, −0.104] | −0.111 [−0.131, −0.087] (+0.017) | n/a |

How to read the table:
- **Units.** SR values are nats per item.
- **Accuracy CIs** are exact Clopper–Pearson intervals. A bootstrap interval would collapse to a single point at 60/60.
- **AUROC and SR CIs** come from `score.py`.
- **SR_twin** is the spec's headline. It is **biased upward by +0.11 to +0.18 under the null** at 2–3 twins per family (VALIDATION §2). The bracketed reference is what a constant "p = own accuracy" forecaster would score on the same items. Use SR_glob and AUROC as the resolution read-outs.
- **Triage** is undefined when every item in a block is solved (denominator 0). Its null 95% range is about ±0.43.
- **Chance level for AUROC(p).** With random p on this item set, the null range is [0.35, 0.65].

### 3.2 Phase-1 forecasts q (45 forecast items)

| Solver | Mean q vs acc on forecast items | Σq vs solved | Brier(q) [95% CI] | Log score(q) | AUROC(q) [CI] | SR_glob(q) | corr(p, q) |
|---|---|---|---|---|---|---|---|
| haiku | 0.578 vs 0.200 (+0.378) | 26.0 vs 9 | 0.311 [0.251, 0.375] | −0.851 | 0.622 [0.40, 0.82]; within level 0.333 | −0.350 | 0.970 |
| sonnet | 0.762 vs 1.000 (−0.238) | 34.3 vs 45 | 0.081 [0.055, 0.109] | −0.296 | n/a | −0.286 | 0.643 |
| opus | 0.754 vs 1.000 (−0.246) | 33.9 vs 45 | 0.095 [0.061, 0.134] | −0.322 | n/a | −0.312 | 0.726 |
| fable | 0.754 vs 1.000 (−0.246) | 33.9 vs 45 | 0.096 [0.060, 0.137] | −0.324 | n/a | −0.314 | 0.836 |

In its final notes haiku predicted 35–40 correct; it solved 14.

### 3.3 Accuracy, with mean p, by hidden level and by family

| | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| haiku acc (mean p) | 0.42 (0.84) | 0.42 (0.74) | 0.25 (0.59) | 0.00 (0.44) | 0.08 (0.42) |
| sonnet acc (mean p) | 1.00 (0.97) | 1.00 (0.95) | 1.00 (0.93) | 1.00 (0.90) | 1.00 (0.89) |
| opus acc (mean p) | 1.00 (0.98) | 1.00 (0.96) | 1.00 (0.95) | 1.00 (0.93) | 1.00 (0.92) |
| fable acc (mean p) | 1.00 (0.94) | 1.00 (0.92) | 1.00 (0.89) | 1.00 (0.84) | 1.00 (0.81) |

Accuracy by family (10 items each):

| Solver | Exact computation | Logic grid | Program output | Rule inference | Stock log | String trace |
|---|---|---|---|---|---|---|
| haiku | 0.20 | 0.10 | 0.10 | 0.40 | 0.40 | 0.20 |
| sonnet, opus, fable | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

Other per-solver figures:
- haiku's stock-log accuracy by true label: answerable 0.50, contradictory 0.00, not determinable 0.67.
- haiku's accuracy on forecast items vs twins: 0.20 vs 0.33 (gap −0.13 ± 0.14 SE). The spec's void rule is triggered but, as pre-registered, not applied.
- Spearman correlation of p with hidden level: haiku −0.77, sonnet −0.68, opus −0.66, fable −0.79.

### 3.4 Do the self-knowledge metrics just track accuracy?

- **Rank correlation across the 4 solvers.** Spearman(accuracy, metric) is **0.77 for every metric**: Brier, ECE, log score, SR_glob, SR_twin, Brier(q) and log score(q). The value comes entirely from haiku being last on everything. With n = 4 and three solvers tied on accuracy, it carries no evidential weight.
- **Ordering of the three ceiling solvers.** On every proper-score metric the order is opus > sonnet > fable, which is exactly the order of mean p (0.947 > 0.928 > 0.880).
  - Paired bootstrap differences in SR_glob all exclude 0. Opus − fable is +0.076 [+0.065, +0.088], sonnet − fable is +0.055 [+0.043, +0.066], and sonnet − opus is −0.021 [−0.030, −0.012]. The same holds for Brier.
  - At 100% accuracy these metrics measure only how close p is to 1, not discrimination: SR_glob ≤ 0, with 0 reached at p ≥ 0.99.
- **AUROC.** It is defined only for haiku, so differences between tiers cannot be tested.
  - haiku's 0.711 [0.55, 0.85] exceeds the random-p null of [0.35, 0.65].
  - Within level it is 0.546 [0.33, 0.76], which is consistent with chance.
  - It is below the cue-only hidden-level AUROC of 0.742.
  - The other solvers' p, which encodes only *apparent* difficulty because they got everything right, predicts haiku's correctness at AUROC 0.676 (mean of the three) and 0.724 (fable's p alone).
  - Between-solver Spearman correlation of p is 0.83–0.89 among the top three and 0.62–0.66 between haiku and the others. For Phase-1 q the corresponding figures are 0.89–0.97 and 0.57–0.60.

### 3.5 Deliberate-failure counterfactual

Each ceiling solver was given a hypothetical failure: in each block, the unpicked item with its lowest stated p was failed, with p set to 0.01 for it. That is 3 items in all; everything else was left as submitted.

| Solver | Accuracy | AUROC(p) | SR_glob (actual) | Brier (actual) | Triage |
|---|---|---|---|---|---|
| sonnet | 1.00 → 0.95 | n/a → 1.000 | −0.066 → **+0.129** | 0.0070 → 0.0060 | n/a → 1.000 |
| opus | 1.00 → 0.95 | n/a → 1.000 | −0.045 → **+0.151** | 0.0041 → 0.0031 | n/a → 1.000 |
| fable | 1.00 → 0.95 | n/a → 1.000 | −0.121 → **+0.082** | 0.0184 → 0.0152 | n/a → 1.000 |

Every self-knowledge metric improves, and each solver ends up beating any honest ceiling solver. Triage reaches 1.000 as soon as all 5 picks are solved and one unpicked item in the block is failed.

## 4. Interpretation

- **Ceiling effect: the pilot cannot answer its main question.** Sonnet, opus and fable each scored 60/60, including all 12 L5 items (a 13 × 12-digit product, sub-diagonal lattice paths, a 26-op string trace, 5 × 4 logic grids). Their exact lower bound is 0.94. For these three, AUROC, within-level AUROC and triage are undefined, so whether self-knowledge separates tiers *beyond* accuracy cannot be tested. The difficulty ladder was intended to span Haiku to Fable without tools and failed above Haiku. Either no-tools performance is far above the builder's estimate, or the honour-system tool ban did not hold. The data cannot tell these apart. The correct, solver-specific intermediate states and the 9–22 min wall times fit genuine hand work, but they do not prove it.
- **At the ceiling, the metrics reward confidence, not self-knowledge, and this produces an inversion.** Among the three perfect solvers, Brier, ECE, SR_glob and SR_twin rank opus > sonnet > fable. The differences are "significant" under paired bootstrap, but they reflect only how far each solver hedged below 1. Fable, nominally the top tier, ranks last of the three, and only because it was the most cautious. Across all four solvers each metric's rank correlation with accuracy is 0.77, all of it from haiku. Nothing in this pilot shows self-knowledge adding information beyond accuracy.
- **haiku: overconfident, and its discrimination is explained by visible difficulty.** Its p is too high by 0.37 and its q by 0.38. SR_glob is −0.31, CI excluding 0, which is worse than stating its own accuracy as a constant. Triage is 0.00, inside the null range. Its AUROC of 0.71 vanishes within level (0.55), sits below the level cue alone (0.74), and is matched by *other* models' confidences (0.68–0.72). This supports the round-2 critique that confidence tracks apparent difficulty.
- **Confidence tracks apparent difficulty for every tier, even where difficulty did not matter.** All four solvers' p falls monotonically from L1 to L5 (Spearman −0.66 to −0.79), although the top three were right on every L5 item. Phase-1 q is shared heavily across tiers (Spearman 0.89–0.97 among the top three), which points to a common perception of difficulty rather than a model-specific self-model.
- **Phase-1 forecasting is poorly calibrated in both directions.** The top three under-forecast by about 0.24 (mean q of about 0.75 against 1.00 realised). haiku over-forecast by 0.38. Brier(q) for the top three is 0.08–0.10. That is far from the 0.0001 a perfect forecaster would get here, and these models plainly could not anticipate their own ceiling.
- **The gaming critique is confirmed concretely.** Failing three unpicked items on purpose and labelling them p = 0.01 costs 5 pp of accuracy. It turns undefined AUROC and triage into 1.000 and lifts SR_glob from negative to +0.08 to +0.15, above anything an honest perfect solver can score. haiku's work-note-free attempts show that the minimum-effort rule, the only defence here, cannot be verified.
- **Implications for F5.**
  1. Restore the spec's per-model warm-up, or use adaptive difficulty that targets roughly 40–60% accuracy for each tier. A fixed ladder cannot serve four tiers.
  2. Enforce the tool ban in the harness (no tool access) instead of relying on honour.
  3. Make within-difficulty discrimination the headline: within-level AUROC, AUROC relative to the peer-difficulty baseline, or SR against a difficulty-conditioned reference. Report it only when a solver has enough errors.
  4. Gate or combine self-knowledge scores with accuracy, for example a single reward-weighted answer-or-abstain score, so that deliberate failure does not pay.
  5. Drop SR_twin as the headline until there are 40 or more twins per family.

## 5. Limitations

- **Single lab.** All solvers are Claude tiers, and the same team built the items, the key, the scorer and this analysis. Nothing here generalises across developers.
- **Agent harness not frozen.** Model versions, system prompts, thinking budgets and the agent scaffold were not pinned or recorded. Wall times come only from file mtimes and git commits.
- **Small sample.** n = 60 with one run per solver: wide CIs (haiku AUROC CI width about 0.30; triage null about ±0.43), 2–3 twins per family, and only n = 4 solvers for any across-tier correlation.
- **No humans.** The spec's human arm was not run.
- **Tool ban not verifiable.** The no-tools policy, the 300-token forecast budget and the full-effort rule were all on the honour system. Ceiling performance on L5 cannot be attributed to unaided reasoning.
- **Shared filesystem.** Solvers could in principle read each other's files: they ran concurrently in a shared directory, and fable's final file was written after sonnet's and opus's were on disk. No sign of cross-reading was found (§2), but it is not ruled out.
- **Other deviations from the spec.**
  - There was no fresh context between forecasting and solving.
  - Twins were known to the solvers.
  - The cue-only release gate could not be tested.
  - The 200-line-script gate fails by construction.
