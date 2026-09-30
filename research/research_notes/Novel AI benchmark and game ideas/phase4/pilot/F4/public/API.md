# Brackwater — bot API

## Your bot

Your bot is one Python 3.11 file, `bot.py`, that defines:

```python
class Bot:
    def __init__(self, player: int, game_info: dict):
        ...   # called once per game
    def act(self, obs: dict) -> dict:
        ...   # called once per turn (200 times), returns your action
```

- **Libraries:** the Python standard library and `numpy` only. You may `import bot_api` (helpers in this directory). You may also `import brackwater_engine` to run your own simulations (see "Engine" below).
- **Isolation:** every game runs your file in a **fresh process** that sees only `game_info` and the observations. No state survives from one game to the next. Do not read or write files, open sockets, start threads or processes, or inspect the harness.
- **Output:** anything you `print` goes to stderr and is discarded during evaluation. Use `run_local.py --show-stderr` to see it.

## `game_info` (passed to `__init__`)

| key | value |
|---|---|
| `player` | 0 or 1 (0 is hub `A`, 1 is hub `B`) |
| `width`, `height` | 16, 16 |
| `terrain` | string of length `width*height`; char per cell, one of `#`, `.`, `0`, `1`, `2`, `A`, `B` (see RULES.md) |
| `hubs` | `[hub_cell_of_player0, hub_cell_of_player1]` |
| `turns` | 200 |
| `yields` | `{".": 1, "2": 2, "1": 3, "0": 5}` |
| `hub_income` | 2 |
| `crew_cap` | 24 |
| `start_crews`, `start_grain` | 3, 20 |
| `vision` | `{"crew": 2, "hub": 3, "stake": 1}` (Chebyshev radii) |
| `version` | engine version string |

Cells are integers `c = y * width + x`.

## Observation (`obs`, passed to `act` every turn)

| key | type | meaning |
|---|---|---|
| `turn` | int | 0..199, the turn about to be played |
| `grain` | int | your grain |
| `income` | int | grain you gained at the end of the previous turn (0 on turn 0) |
| `recruit_cost` | int | what recruiting costs this turn |
| `crews` | dict `{crew_id: cell}` | all your living crews |
| `stakes` | sorted list of cells | all your stakes |
| `visible` | sorted list of cells | cells you currently see |
| `flooded` | sorted list of cells | visible cells that are flooded now |
| `enemy_crews` | dict `{cell: count}` | enemy crews on visible cells |
| `enemy_stakes` | sorted list of cells | enemy stakes on visible cells |
| `lost_crews` | dict `{crew_id: "combat" or "drowned"}` | your crews lost during the previous turn |
| `lost_stakes` | sorted list of cells | your stakes lost during the previous turn (washed away or taken, not distinguished) |
| `new_crew` | int or None | id of the crew you recruited last turn |

The observation always describes the state at the start of the turn you are about to play.

## Action (return value of `act`)

```python
{"orders": {crew_id: "N" | "E" | "S" | "W" | "H" | "K", ...}, "recruit": False}
```

- **`orders`:** keys are your crew ids as ints (strings of ints are also accepted). Crews you leave out hold. `"K"` means stake.
- **`recruit`:** `True`/`False` (or 1/0). You may leave it out; the default is `False`.
- **Types:** the action must be JSON-serialisable. Numpy integer and bool scalars are converted automatically.
- **Extra keys:** unknown top-level keys are ignored.
- **Illegal actions:** any of the following forfeits the game:
  - an unknown crew id;
  - a bad order string;
  - a move off the board, into rock or into the enemy hub;
  - an unaffordable or over-cap recruit;
  - an action that is not a dict.

`bot_api.Grid(game_info).legal_orders(cell)` lists the legal orders for a crew on `cell`.

## Compute limits (enforced by `harness.py`)

| limit | value |
|---|---|
| CPU time of your process per game (start-up, imports, `__init__`, all `act` calls) | **3.0 s** |
| CPU time per `act()` call | **0.25 s** |
| wall-clock per `act()` round trip | 3 s |
| wall-clock for start-up and `__init__` | 20 s |
| memory (address space) | 2 GB |

Interpreter start-up costs about 0.03 s of the per-game budget; importing numpy costs about 0.1 s more. Exceeding any limit forfeits the game. Evaluation runs up to four games in parallel on a 4-core machine. The limits are CPU time, so machine load does not matter.

## Helpers (`bot_api.py`, source provided)

`Grid(game_info)` provides:

- `W`, `H`, `N`, `terrain`;
- `elev` (−1 for rock, 0–2 for fens, 3 for land and hubs);
- `yld`, `my_hub`, `enemy_hub`;
- `moves[c]`: a list of `(order, target_cell)` for legal moves;
- `neighbors(c)`, `legal_orders(c)`, `xy(c)`, `cell(x, y)`, `chebyshev(a, b)`;
- `bfs(sources, avoid=None)`: distances as a list, −1 where unreachable;
- `step_toward(c, dist_map)`.

`recruit_cost(n)` is also provided.

## Engine (compiled; no source)

`brackwater_engine.pyc` is the official engine. It is the same file used in evaluation. Documented API:

```python
import brackwater_engine as bw
m = bw.load_map("maps/map1.json")        # or bw.parse_map({"rows": [...]})
match = bw.Match(m, seed)                # seed (int) fixes the tide for this match
info = match.game_info(p)                # p = 0 or 1
obs = match.observe(p)
a = match.validate(p, action)            # normalised action, or raises bw.IllegalAction
match.step([a0, a1])                     # validated actions of both players
match.done, match.turn, match.grain      # state flags / final grain
match.result()                           # {"grain": [..], "winner": 0/1/None, "stats": {...}}
print(match.render())                    # full-information ASCII board (debugging only)
```

In `render()`, each cell shows two characters: the terrain (`~` for flooded, `@` for a hub), then its occupant:
- `A` or `B`: crews of that player;
- `a` or `b`: that player's stake;
- a blank: empty.

Use only this documented API. Do not decompile, disassemble or introspect the engine (for example with `dis`, `marshal` or decompilers, or by reading private attributes). Treat it as a binary.

## Tools

- `harness.py`: runs games exactly as evaluation does.
- `run_local.py`: plays your bot against the random bot or another bot file on the public maps. Run it from this directory.
- `random_bot.py`: the only reference bot you are given.
