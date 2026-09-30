# VALIDATION - reference forecasters (numbers only)

Overall skill over 15 questions (0 = no-change forecast, 100 = oracle forecast), computed by `score.py` against the sealed key.

| forecaster | overall skill | 90% bootstrap CI (over questions) |
|---|---|---|
| no-change (true-model distribution with no intervention) | 0.0 | [0.0, 0.0] |
| oracle (true model, independent 10,000 rollouts) | 100.0 | [100.0, 100.0] |
| ideal (in-sample quantiles of the truth rollouts) | 100.0 | [100.0, 100.0] |
| naive "extrapolate the experiments" (public data only) | 16.0 | [-8.1, 35.8] |
| history climatology (public data only) | -1.7 | [-5.1, 1.6] |
| spam: random quantiles within the history range (mean of 20 draws) | 3.8 (sd 9.4) | - |

Reference mean quantile score (scale units): no-change 0.5768; oracle 0.1651.
