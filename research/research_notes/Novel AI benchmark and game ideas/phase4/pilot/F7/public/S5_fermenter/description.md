# S5 - Continuous fermenter

A continuous stirred-tank fermenter with a fixed liquid volume. Fresh medium containing a growth substrate flows in continuously, and culture broth flows out at the same rate. That rate is the dilution rate D, per hour. Microorganisms grow on the substrate and make a product. An automatic cooling controller regulates the reactor temperature, tracking a temperature setpoint. Feed medium arrives in lots from a supplier with a nominal substrate concentration of 20 g/L. Actual lot strength may vary and is not recorded. Each **episode** is an independent 400-hour replicate starting from typical running conditions. **Baseline:** D = 0.10 per hour, setpoint 34.0 C.

## Files
- `history.csv` - 25 baseline episodes (no interventions): 10,000 rows.
- `experiments.csv` - 20 sample paths from the fixed pilot experiment menu in `experiments.json` (columns `experiment`, `replicate`, then as in history). Every path is a full 400-hour episode.
- `experiments.json` - the experiment menu and each intervention type's no-change value.

## Columns (hourly; values recorded at the end of each hour, with measurement error)
| column | meaning |
|---|---|
| `episode` | replicate id |
| `hour` | 0-399 |
| `biomass` | cell concentration (g/L) |
| `substrate` | residual substrate concentration in the broth (g/L) |
| `product` | product concentration (g/L) |
| `temperature` | reactor temperature (C) |
| `cooling_duty` | fraction of maximum cooling power in use, averaged over the hour (0-1) |

## Interventions
Interventions act from the start of hour `start`.

| type | meaning | no-change value |
|---|---|---|
| `feed_conc` | from hour `start` onward, the substrate concentration of the feed is multiplied by `size` | 1 |
| `dilution` | from hour `start` onward, the dilution rate is set to `size` per hour | 0.10 |
| `setpoint` | from hour `start` onward, the controller's temperature setpoint is set to `size` C | 34.0 |
