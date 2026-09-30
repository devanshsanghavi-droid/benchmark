# Validation (pilot build)

Scores from `score.py` against the sealed key. 20 patches, of which V = 6 violate.

| Answer set | TP | FP | FN | Precision | Recall | **PWR** | F1 | Witnessed recall @ 0 FP | AUROC | Brier |
|---|---|---|---|---|---|---|---|---|---|---|
| Reference solution | 6 | 0 | 0 | 1.000 | 1.000 | **1.000** | 1.000 | 1.000 | 1.000 | 0.000 |
| Do-nothing (all compliant) | 0 | 0 | 6 | 0.000 | 0.000 | **0.000** | 0.000 | 0.000 | 0.500 | 0.300 |
| All violates, no witness | 0 | 20 | 6 | 0.000 | 0.000 | **0.000** | 0.000 | 0.000 | 0.500 | 0.700 |
| All violates, spec-example witness | 0 | 20 | 6 | 0.000 | 0.000 | **0.000** | 0.000 | 0.000 | 0.500 | 0.700 |

## Build certification

| Check | Result |
|---|---|
| Visible tests pass (5 base + 20 patched trees) | 25 / 25 |
| Reference witnesses confirmed by the oracle | 6 / 6 |
| Oracle violations on base code, 3,000 random cases per repo | 0 / 15,000 |
| Oracle violations on the 14 compliant patches, 3,000 cases each | 0 / 42,000 |
| Human baseline | none (no humans available for this pilot) |
