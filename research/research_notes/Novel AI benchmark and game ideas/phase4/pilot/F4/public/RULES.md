# Brackwater — rules (v1.0)

Brackwater is a two-player, simultaneous-move territory and economy game played on a small
tidal marsh under fog of war. Each player commands crews that plant **stakes** on cells. Staked
cells produce **grain** every turn. Low-lying **fens** are rich, but a tide floods them on a
rhythm you are not told. Flooding washes stakes away and drowns crews. The player with more
grain after 200 turns wins.

## 1. Board

- A rectangular grid (16 × 16 on all maps so far). Cell `c` has coordinates `x = c % width` and `y = c // width`. North is `y − 1`.
- Every map is point-symmetric: cell `c` corresponds to cell `N − 1 − c`. Player 0's hub corresponds to player 1's hub.
- The whole map (terrain and both hub locations) is known to both players from the start.

| Char | Terrain | Elevation | Yield per turn when staked by you |
|---|---|---|---|
| `#` | rock | — | impassable |
| `.` | land | 3 (never floods) | 1 |
| `2` | high fen | 2 | 2 |
| `1` | fen | 1 | 3 |
| `0` | low fen | 0 | 5 |
| `A` / `B` | hub of player 0 / player 1 (land) | 3 | hub income, see §6 |

## 2. Pieces and starting position

- **Hub.** Each player has one hub. It cannot be attacked, staked or destroyed. Enemy crews may never enter it.
- **Crews.** Each player starts with 3 crews on its hub, with ids 0, 1 and 2. Ids are per player, increase by one for each new crew and are never reused. Any number of crews, of either player, may stand on one cell; only crews of both players on the same cell fight.
- **Stakes.** A cell holds at most one stake, owned by one player. Hubs and rock never hold stakes.
- **Grain.** Each player starts with 20.

## 3. Orders

Each turn both players act simultaneously. Each player gives every one of its crews one order:

| Order | Effect |
|---|---|
| `N`, `E`, `S`, `W` | Move one cell in that direction. |
| `H` | Hold (stay). |
| `K` | Stake: stay, and plant your stake on the current cell (§5, step 4). |

A player may also **recruit** at most one new crew per turn.

**Illegal actions:**
- a move off the board, into rock, or into the enemy hub;
- an unknown crew id;
- an order other than the six above;
- recruiting when you cannot afford it or already have 24 crews;
- a malformed action (see API.md).

An illegal action forfeits the game.

**Legal but useless actions:** staking your own hub or a cell you already own does nothing. Crews without an order hold. Moving into a flooded cell is legal (see step 5).

## 4. Recruiting

- The cost is `floor(12 × 1.2^n)` grain, where `n` is the number of crews you have when the turn starts. With 3 crews it costs 20; with 10 crews, 74; with 20 crews, 460.
- You may have at most **24 crews**.
- The new crew appears on your hub at the start of the turn (step 1), takes the next id, and receives its first order next turn.

## 5. Turn sequence

Both players' actions resolve together in this order:

1. **Recruit.** Pay for and place new crews.
2. **Move.** All moves happen at once. Crews may pass through each other; only crews that end up on the same cell interact.
3. **Combat.** On every cell holding crews of both players, each side loses crews equal to the **number of enemy crews on that cell**. That loss is reduced by 1 if **the cell carries that side's stake** (the defender's bulwark). Losses are capped at the number of crews the side has there, and each side loses its highest-id crews first. At most one side survives. Examples:
   - 1 vs 1 on a neutral cell: both die.
   - 2 vs 1 on a neutral cell: one of the two survives.
   - 1 attacker vs 1 defender on the defender's stake: the attacker dies and the defender survives.
   - 2 attackers vs 1 defender on the defender's stake: the defender dies and one attacker survives.
4. **Stake.** Every surviving crew with order `K` plants its owner's stake on its cell. Any enemy stake there is replaced.
5. **Tide.** The turn counter advances and the water level is updated (§7). Then:
   - every stake on a flooded cell is washed away;
   - every crew on a flooded cell drowns.

   A crew therefore survives on a fen only if that fen is dry at the end of the turn.
6. **Income.** Each player gains 2 grain (hub income) plus the yield of every stake it owns.

## 6. Scoring and end of game

- The game lasts **200 turns** (turns 0–199).
- Only final grain counts. Grain spent on recruiting is gone.
- The player with more grain wins. Equal grain is a draw.
- A player that forfeits loses. If both players forfeit on the same turn, the game is a draw. A player forfeits by:
  - making an illegal action;
  - crashing;
  - producing malformed output;
  - exceeding the compute limits in API.md.

## 7. The tide (partly hidden)

- The water level is an integer from 0 to 3. A fen of elevation `e` is **flooded** while the level is greater than `e`. At level 1 only low fens (`0`) are flooded; at level 3 every fen is flooded. Land never floods.
- The level follows a **strictly periodic** cycle that is fixed for the whole match. In each cycle it climbs from 0 to 3 and falls back to 0. It changes by at most 1 per turn.
- The **period is between 20 and 40 turns**. The period, the phase and the time spent at each level are **not disclosed**. The period and phase are drawn afresh for every match.
- You see flooding only on cells you can see. Nothing else is announced. Anything you learn about the tide must come from your own observations.

## 8. Fog of war

- **What you always know:**
  - the map;
  - your own crews, stakes, grain and income;
  - which of your crews and stakes you lost last turn.
- **What you see:** every cell within Chebyshev distance 2 of any of your crews (a 5 × 5 square), within 3 of your hub, and within 1 of any of your stakes.
- **What vision shows:**
  - enemy crews on visible cells (as a count per cell, without ids);
  - enemy stakes on visible cells;
  - which visible cells are flooded.
- **What you are never shown:**
  - the enemy's grain;
  - the enemy's crew count;
  - anything on cells you cannot see.
- A lost stake is reported without saying whether it was washed away or taken by the enemy.

## 9. Maps

The public `maps/` directory holds five maps. Evaluation uses fresh private maps from the same generator, with a fresh tide for every map. Every map is played twice, with the players swapping seats.
