# S1 - Pond community

A small pond is monitored once a day. Each **episode** is an independent 400-day replicate of the same pond, starting from the pond's typical state on the same calendar date (day 0 is the same date in every episode; a year has 365 days). The pond receives dissolved nutrients from its catchment. Its community includes free-floating algae, small grazing invertebrates ("grazers") that feed on algae, and fish that feed on the grazers. Not every state variable of the pond is measured.

## Files
- `history.csv` - 25 baseline episodes (no interventions), 400 days each: 10,000 rows.
- `experiments.csv` - 20 sample paths from the fixed pilot experiment menu in `experiments.json` (columns `experiment`, `replicate`, then as in history). Every path is a full 400-day episode.
- `experiments.json` - the experiment menu (interventions and replicate counts) and each intervention type's no-change value.

## Columns (daily; all values are measured with error)
| column | meaning |
|---|---|
| `episode` | replicate id |
| `day` | 0-399 |
| `nutrient` | dissolved nutrient concentration (arbitrary units) |
| `algae` | algal biomass index |
| `grazers` | estimated number of adult grazers in the pond |
| `fish` | fish caught in a standardised daily survey (an index of fish abundance) |

## Interventions
Interventions act at the start of day `start`, before that day's measurements.

| type | size means | no-change value |
|---|---|---|
| `nutrient_load` | from day `start` onward, all external nutrient input to the pond is multiplied by `size` | 1 |
| `fish_removal` | on day `start`, the fraction `size` (0-1) of the fish is removed | 0 |
| `grazer_stocking` | on day `start`, `size` adult grazers are added to the pond | 0 |
