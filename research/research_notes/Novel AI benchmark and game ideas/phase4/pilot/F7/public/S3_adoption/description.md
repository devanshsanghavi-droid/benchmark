# S3 - Habit adoption in a small town

A town has 300 residents in three neighbourhoods, A, B and C, with 100 residents each. A daily habit (for example a fitness routine) spreads among the residents. On any day, each resident either practises the habit ("active") or does not. Residents start and stop practising over time. They are connected by a social network that is **not observed**. Each **episode** is an independent 120-day replicate starting from the town's typical state.

## Files
- `history.csv` - 28 baseline episodes (no interventions), one row per episode x day x neighbourhood: 10,080 rows.
- `experiments.csv` - 20 sample paths from the fixed pilot experiment menu in `experiments.json` (columns `experiment`, `replicate`, then as in history). Every path is a full 120-day episode.
- `experiments.json` - the experiment menu and each intervention type's no-change value.

## Columns (daily, per neighbourhood)
| column | meaning |
|---|---|
| `episode` | replicate id |
| `day` | 0-119 |
| `community` | neighbourhood `A`, `B` or `C` |
| `new_adopters` | residents of that neighbourhood who started practising that day on their own (recruits from a `seed` intervention are not counted here) |
| `active` | residents of that neighbourhood practising at the end of that day |

## Interventions
| type | meaning | no-change value |
|---|---|---|
| `seed` | on day `start`, `size` residents who are not currently active are recruited and become active that day. They are chosen uniformly at random from neighbourhood `community` (`A`, `B` or `C`), or from the whole town if `community` is `all`. | 0 |
| `friction` | from day `start` onward, the strength of social influence between residents is multiplied by `size` | 1 |
| `broadcast` | on days `start` to `start+duration-1`, each non-active resident has an extra daily probability `size` of starting the habit | 0 |
