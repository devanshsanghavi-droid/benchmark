# VALIDATION (Brackwater pilot v1.0, 30 Sep 2026)

## Ladder self-consistency

200 maps x 2 seats = 400 games per pair; 0 forfeits. Row score rate vs column.

| | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| L0 | – | 0.000 | 0.000 | 0.000 |
| L1 | 1.000 | – | 0.145 | 0.128 |
| L2 | 1.000 | 0.855 | – | 0.235 |
| L3 | 1.000 | 0.873 | 0.765 | – |

Fixed BT ratings (logit, L1 = 0; pseudo-count 0.5/0.5 per pair): L0 -5.87, L1 +0.00, L2 +1.44, L3 +2.38.

Ladder CPU per game, mean/max (s): L0 0.00/0.03, L1 0.14/0.18, L2 0.13/0.20, L3 0.17/0.29.

## Reference bots scored as submissions (score.py, subprocess harness)

400 games per rung on the evaluation maps.

| submission | vs L0 | vs L1 | vs L2 | vs L3 | forfeits | rung position [95% CI] | logit vs L1 [95% CI] | CPU/game mean/max (s) |
|---|---|---|---|---|---|---|---|---|
| strongest reference bot (= L3) | 1.000 [1.000, 1.000] | 0.887 [0.860, 0.917] | 0.765 [0.730, 0.805] | 0.500 [0.500, 0.500] | 0 | 3.03* [2.94, 3.12] | +2.41 [+2.32, +2.50] | 0.24/0.32 |
| random bot (= L0) | 0.500 [0.500, 0.500] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0 | -0.00 [-0.00, -0.00] | -5.87 [-5.87, -5.87] | 0.03/0.06 |

Head-to-head: L3_vs_RANDOM 1.000.

\* = outside the ladder range (extrapolated).

Human baseline: none (no humans available for this pilot).
