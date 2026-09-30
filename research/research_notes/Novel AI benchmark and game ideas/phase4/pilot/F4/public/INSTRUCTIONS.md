# Task: write a competitive bot for a game you have never seen

You will write an AI bot for **Brackwater**. It is a new two-player, simultaneous-move territory and economy game with fog of war and a partly hidden tide. The game was designed for this exercise, so no strategy guides or existing bots exist. Your bot will play hundreds of games against a hidden ladder of reference bots of increasing strength. The goal is to win as many of those games as possible.

## What you get (all in this `public/` directory)

| file | purpose |
|---|---|
| `RULES.md` | complete game rules; read first |
| `API.md` | bot interface, observation and action formats, compute limits, engine API |
| `brackwater_engine.pyc` | the official engine, compiled (no source) — the same file used for evaluation |
| `bot_api.py` | optional helpers (grid geometry, BFS, legal orders) |
| `random_bot.py` | a random-legal bot; the **only** reference bot you are given |
| `harness.py`, `bot_runner.py` | the match harness used in evaluation (source provided) |
| `run_local.py` | local test runner (your bot vs. random or vs. another bot file) |
| `maps/map1.json` … `map5.json` | five public maps |
| `score.py`, `VALIDATION.md` | the organisers' scorer and its self-check; you cannot run the scorer (it needs sealed files) |

Requires CPython **3.11** (the engine is 3.11 bytecode). Run the tools from inside `public/`, for example: `python3 run_local.py --bot ../answers/<SOLVER_LABEL>/bot.py`.

## What to produce

A single file:

```
/home/user/benchmark/research/research_notes/Novel AI benchmark and game ideas/phase4/pilot/F4/answers/<SOLVER_LABEL>/bot.py
```

`<SOLVER_LABEL>` is the label given in your task prompt. The file defines `class Bot` with `__init__(self, player, game_info)` and `act(self, obs) -> dict` (see API.md).

Requirements for `bot.py`:
- It must be **self-contained**. It may import only the Python standard library, `numpy`, `bot_api` and `brackwater_engine`.
- It must not read or write files at run time.
- Scratch files in your answers directory are fine, but only `bot.py` is evaluated. Its last saved version when you stop is your one submission.

## How you will be scored

- Your bot plays **400 games against each of four hidden reference bots**, one of which is `random_bot.py`. The others are stronger bots whose identities are not disclosed.
- Games are on **fresh private maps from the same generator** as the public maps, with a fresh tide per map. Each map is played twice, with the players swapping seats.
- A win scores 1, a draw ½ and a loss 0. A crash, an exception, an illegal or malformed action, or a breach of a compute limit **forfeits that game** (it counts as a loss).
- **Headline:** a Bradley–Terry rating fitted to your results with the reference bots' ratings held fixed. It is reported as a position on the reference ladder, together with win rates and bootstrap confidence intervals.
- Every game counts equally. Robustness (never crashing, never timing out, never making an illegal move) matters as much as strength.

## Tool policy

- **Allowed:** you may use code execution freely to write, run, test and benchmark your bot. That includes running as many local games as you like, writing your own sparring bots and simulators, and analysing the logs.
- **No internet.** Do not use the web, and do not look up whether this game exists elsewhere. It does not.
- **Stay inside `public/`.** Do not read, list or search anything outside `public/`, apart from your own `answers/<SOLVER_LABEL>/` directory. In particular:
  - do not look at other solvers' directories;
  - do not look at any encrypted or sealed files;
  - do not look at the rest of the repository.
- **Do not modify files in `public/`.** Copy anything you want to change into your answers directory.
- **Engine is a binary.** Use it only through its documented API. Do not decompile, disassemble or introspect it: no `dis`, no `marshal`, no decompilers, no private attributes. Anything you learn by *playing* games and watching observations or `render()` output is fair game.
- **No exploits.** A bot that exploits an engine or harness bug, or tries to reach state outside its observations, is disqualified.

## Effort budget (single attempt)

This pilot mirrors the "Lite" track of the benchmark design:
- about **1M billed output tokens** (thinking included);
- at most **4 CPU core-hours** of sandbox compute for your testing and tuning (the machine has 4 cores);
- a suggested wall-clock ceiling of **about 3 hours** of work.

There is one submission and no retries. Manage your own budget. When you stop, make sure `bot.py` is your best working version. Also run `python3 run_local.py --bot ../answers/<SOLVER_LABEL>/bot.py --games 20` one last time and confirm it reports 0 forfeits.

The per-game compute limits apply at evaluation time:
- **3.0 CPU-seconds per game** in total;
- **0.25 CPU-seconds per move**;
- 2 GB memory.

See API.md.

## Hints on the task (not on strategy)

- The random bot is very weak. Beating it tells you little. You will need your own sparring partners, such as earlier versions of your own bot or deliberately different strategies.
- Some important dynamics are only described qualitatively in RULES.md. They are, however, observable during play.
