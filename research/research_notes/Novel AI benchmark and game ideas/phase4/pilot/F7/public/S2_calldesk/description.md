# S2 - Support call desk

A customer-support phone line that is open 24 hours a day. Each **episode** is an independent 14-day replicate (336 hourly rows). Every episode starts on a Monday at 00:00, so days 5, 6, 12 and 13 are Saturdays and Sundays. Calls wait in a single first-come-first-served line until an agent is free, and callers may hang up while they wait.

**Baseline rota:** from 08:00 to 20:00 there are 7 agents on weekdays and 4 on weekends; from 20:00 to 08:00 there are 2 agents every day. `scheduled_agents` shows the rota for each hour.

## Files
- `history.csv` - 30 baseline episodes (no interventions): 10,080 rows.
- `experiments.csv` - 20 sample paths from the fixed pilot experiment menu in `experiments.json` (columns `experiment`, `replicate`, then as in history). Every path is a full 14-day episode.
- `experiments.json` - the experiment menu and each intervention type's no-change value.

## Columns (hourly)
| column | meaning |
|---|---|
| `episode` | replicate id |
| `hour` | 0-335 (hour index within the episode) |
| `day`, `hour_of_day` | `hour // 24`, `hour % 24` |
| `offered` | calls that reached the line during the hour. The desk cannot tell first-time callers from people who have called before. |
| `answered` | calls picked up by an agent during the hour |
| `abandoned` | callers who hung up while waiting during the hour |
| `queue_end` | callers still waiting at the end of the hour |
| `avg_wait_min` | mean wait of the calls answered in that hour, in minutes. It is measured on a 5-minute grid (midpoint convention) and is 0 if no call was answered. |
| `scheduled_agents` | agents on the rota for that hour |

## Interventions
All `start` values are hour indices (0-335).

| type | meaning | no-change value |
|---|---|---|
| `demand` | from hour `start` onward, the rate at which customers with a new reason to call contact the desk is multiplied by `size` | 1 |
| `staff_day` | from hour `start` onward, `size` agents (an integer; negative removes agents) are added to every day-shift hour (08:00-20:00) on all days. `scheduled_agents` reflects the change. | 0 |
| `outage` | for `duration` hours starting at hour `start` (hours `start` to `start+duration-1`), the phone system cannot connect waiting callers to agents. Calls already in progress finish normally, and callers can still join the line. | 0 hours |
