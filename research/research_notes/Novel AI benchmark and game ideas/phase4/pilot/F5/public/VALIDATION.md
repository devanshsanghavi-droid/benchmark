# F5 Self-Knowledge Exam pilot: validation numbers

Synthetic answer files were built against the sealed answer key and scored with `score.py` from this directory (1,000 bootstrap resamples, fixed seed). No real solver is involved. Two synthetic correctness patterns are used: **coin** (each item right independently with probability 0.5; realised accuracy 0.450) and **ladder** (success probability falls with a hidden per-item difficulty variable; realised accuracy 0.567). Metric definitions are in the `score.py` docstring. SR values are nats per item.

**Human baseline: none.** No human participants were available for this pilot, so the spec's human arm was not run and no human numbers exist.

## 1. Reference baselines

| ID | Pattern | Baseline | Acc | Mean p | Brier | ECE | AUROC(p) | AUROC(p) within difficulty | SR_twin (spec) | SR_glob | SR_fam | Triage | AUROC(q) | Abstain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B01 | coin | Constant confidence = own accuracy (p = q = realised accuracy; triage = first 5 listed) | 0.450 | 0.450 | 0.248 | 0.000 | 0.500 | 0.500 | 0.143 | 0.000 | -0.026 | 0.250 | 0.500 | 0.000 |
| B02 | coin | Oracle: perfect self-knowledge at the same accuracy (p = q = 1 if correct else 0; best 5) | 0.450 | 0.450 | 0.000 | 0.000 | 1.000 | 1.000 | 0.829 | 0.678 | 0.652 | 1.000 | 1.000 | 0.000 |
| B03 | coin | Anti-oracle (p = q = 1 if wrong else 0; worst 5) | 0.450 | 0.550 | 1.000 | 1.000 | 0.000 | 0.000 | -3.766 | -3.917 | -3.943 | -1.100 | 0.000 | 0.000 |
| B04 | coin | Random confidence (p, q uniform on [0,1]; random 5) | 0.450 | 0.495 | 0.316 | 0.228 | 0.527 | 0.520 | -0.096 | -0.249 | -0.274 | -0.200 | 0.504 | 0.000 |
| B05 | coin | Partial self-knowledge (p = 0.5 +/- 0.2 + N(0, 0.2) noise; q likewise) | 0.450 | 0.473 | 0.128 | 0.129 | 0.929 | 0.936 | 0.458 | 0.283 | 0.257 | 1.000 | 0.941 | 0.000 |
| B06 | ladder | Constant confidence = own accuracy | 0.567 | 0.567 | 0.246 | 0.000 | 0.500 | 0.500 | 0.359 | 0.000 | -0.012 | -0.174 | 0.500 | 0.000 |
| B07 | ladder | Difficulty-only knowledge (p = q = true success probability of the item's hidden difficulty; easiest 5) | 0.567 | 0.540 | 0.106 | 0.087 | 0.934 | 0.500 | 0.717 | 0.341 | 0.329 | 1.000 | 0.930 | 0.000 |
| B08 | ladder | Oracle at the same accuracy | 0.567 | 0.567 | 0.000 | 0.000 | 1.000 | 1.000 | 1.055 | 0.674 | 0.663 | 1.000 | 1.000 | 0.000 |
| B09 | - | Abstain on everything (answer null, p = q = 0) | 0.000 | 0.000 | 0.000 | 0.000 | n/a | n/a | 0.017 | 0.000 | 0.000 | n/a | n/a | 1.000 |
| B10 | - | Do-nothing: empty answer file (all defaults: wrong, p = q = 0.5) | 0.000 | 0.500 | 0.250 | 0.500 | n/a | n/a | -0.666 | -0.683 | -0.683 | n/a | n/a | 1.000 |
| B11 | - | Every answer correct, p = q = 0.99 (no errors to discriminate) | 1.000 | 0.990 | 0.000 | 0.010 | n/a | n/a | 0.017 | 0.000 | 0.000 | n/a | n/a | 0.000 |
| B12 | - | Every answer wrong, p = q = 0.9 | 0.000 | 0.900 | 0.810 | 0.900 | n/a | n/a | -2.276 | -2.293 | -2.293 | n/a | n/a | 0.000 |

## 2. Null distributions on this item set

2,000 simulated solvers on the real item structure (families, blind twins, triage blocks, difficulty strata) with no self-knowledge. The table shows mean [2.5%, 97.5%].

| Statistic under the null | coin pattern | ladder pattern |
|---|---|---|
| SR_twin of a constant p = own-accuracy forecaster | 0.113 [-0.023, 0.355] | 0.183 [0.010, 0.514] |
| AUROC(p), random p | 0.496 [0.352, 0.647] | 0.500 [0.360, 0.646] |
| AUROC(p) within difficulty strata, random p | 0.495 [0.340, 0.657] | 0.500 [0.298, 0.718] |
| Triage value, random picks | -0.004 [-0.435, 0.423] | -0.002 [-0.421, 0.429] |

## 3. Scorer self-tests (all passed)

- Correct answers in alternative formats (digit separators, letter case, list vs string, extra whitespace): 60/60 scored correct.
- Synthetic correctness patterns recovered exactly (the accuracy of B01, B02, B06, B08, B09, B11 and B12 equals the designed pattern).
- The Phase-1 commitment check detects identical forecasts and triage, and the write order.
- Every answer in the key was re-derived by an independent checker that parses the public item text only. There were 0 mismatches on this item set, and 0 on 30 further stress seeds after one generator bug was fixed.

## 4. Reading the numbers

- **Base-rate insensitivity.** A constant forecaster at its own accuracy gets AUROC 0.500 and SR_glob 0.000, whatever its accuracy (B01, B06). An oracle gets AUROC 1.000 at any accuracy (B02, B08).
- **SR_twin (spec headline 1) is biased upward at pilot scale.** There are only 2–3 blind twins per family, where the spec asks for at least 40, so the reference base rate is noisy. A constant forecaster then scores well above 0 (section 2). `score.py` prints, for each solver, the SR_twin that "p = own accuracy" would get on the same items. The difference between the two equals SR_glob on forecast items. Use SR_glob and AUROC as the pilot's resolution read-outs.
- **Difficulty-only knowledge.** B07 knows only how hard each item is. It gets a high overall AUROC and triage value, but its AUROC within difficulty strata is 0.500. The within-strata AUROC, the peer-difficulty baseline and the cue-only AUROCs printed by `score.py` separate item-level self-knowledge from knowledge of visible difficulty.
- **Brier and ECE reward abstaining on everything** (B09: Brier 0, ECE 0 at accuracy 0). Always read them next to accuracy.
- **Noise.** With 60 items, one solver's AUROC must be above about 0.65 to differ from chance at 95%. Triage (3 blocks of 15, pick 5) has a null range of about ±0.43. Differences between tiers smaller than these ranges are not evidence.

## 5. Deviations from the F5 spec

- 60 items rather than about 1,800, in 6 pilot families: exact computation, logic grids, string tracing, program-output prediction, rule inference, and stock logs. The stock logs are synthetic documents whose answer is a number, CONTRADICTORY or NOT DETERMINABLE. There are no post-cutoff-fact items (no sealed feed exists) and no agentic sandbox items. Program-output prediction stands in for code with hidden tests.
- There is no per-model warm-up. One fixed item set spans a wide difficulty range instead, so every tier gets some items right and some wrong. As a result, visible difficulty carries part of the signal (see B07).
- Split: 45 forecast items and 15 blind twins (25%). Triage uses 3 blocks of 15 forecast items, pick 5 (the same 1/3 ratio as 20 of 60). The triage cards are the forecast items themselves, not a separate set.
- The spec's "fresh context" is not enforced. Forecasts and attempts happen in one session, with a Phase-1 file written first. The ≤300-token forecast budget, the tool ban and the minimum-effort rule rely on the honour system; each attempt must record a short work note as its artefact. Solvers know which items are twins.
- The void rule (forecast-vs-twin accuracy gap above 3 pp) is reported but not applied: with 15 twins the gap's standard error is about 0.14.
- Release gates: the gate that a script of 200 lines or fewer must score near the floor would fail by construction, because every family is mechanically solvable by a short program. The no-tools policy therefore carries the construct and cannot be verified. The gate that a cue-only classifier score at chance cannot be tested with 10 stock logs. The logs are style-matched by construction: every log of a given size has the same number of unrecorded deliveries and stocktakes whatever its label.
