# S4 - Online lot auction

An online marketplace sells one lot per round by **first-price sealed-bid auction**. In each round, every participating bidder submits one bid. The highest bid at or above the reserve price wins, and the winner pays its own bid. If no bid reaches the reserve, the lot is unsold. The same population of independent buyers ("bidders") takes part round after round, and bidders may join and leave the market over time. Bidders value the lots differently, and each bidder operates under a spending allowance. Rounds are daily, and round 0 is a Monday. Each **episode** is an independent 250-round replicate starting from the market's typical state. **Baseline reserve price: 20.**

## Files
- `history.csv` - 40 baseline episodes (no interventions): 10,000 rows.
- `experiments.csv` - 20 sample paths from the fixed pilot experiment menu in `experiments.json` (columns `experiment`, `replicate`, then as in history). Every path is a full 250-round episode.
- `experiments.json` - the experiment menu and each intervention type's no-change value.

## Columns (per round)
| column | meaning |
|---|---|
| `episode` | replicate id |
| `round` | 0-249 |
| `reserve` | reserve price in force |
| `sold` | 1 if the lot sold, else 0 |
| `price` | winning bid (blank if unsold) |
| `revenue` | price if sold, else 0 |
| `n_bids` | number of bids at or above the reserve |
| `active_bidders` | number of bidders currently present in the market |

## Interventions
Interventions act at the start of round `start`, before bidding.

| type | meaning | no-change value |
|---|---|---|
| `reserve` | from round `start` onward, the reserve price is `size` | 20 |
| `entrants` | at round `start`, `size` new bidders join the market. They are drawn from the same population of buyers as the existing bidders and can bid in that round. | 0 |
| `budget` | from round `start` onward, every bidder's spending allowance is multiplied by `size` | 1 |
