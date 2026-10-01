# F4 Season Forge pilot: sealed design notes (Brackwater v1.0)

Built on 30 Sep 2026. This file is SEALED and ships only inside `sealed.tar.gz.enc`.

## Contents of the sealed archive

| path | what |
|---|---|
| `engine_src/brackwater_engine.py` | engine source (public copy is `optimize=2` bytecode without docstrings) |
| `mapgen.py` | private map generator (16×16, point-symmetric; basins, rocks, connectivity and quality checks) |
| `seeds.json` | seeds for the 5 public maps, the calibration maps (400), eval maps per rung (4 × 200) and h2h maps (100). A map seed `s` is also the match (tide) seed |
| `ladder/ladder_common.py`, `ladder/rung1..3.py` | reference bots L1–L3 (L0 is the public `random_bot.py`) |
| `ladder_ratings.json` | fixed BT ratings (logits, L0 = 0) from calibration, plus the pairwise matrix |
| `public_manifest.json` | sha256 of the public files at seal time; `score.py` checks it |
| `tools/` | `build_public.py` (compiles the engine and writes public maps), `calibrate.py`, `arena.py` and `trace.py` (development tools) |

## Game design

**Brackwater** is a 2-player simultaneous-move territory and economy game with fog of war and 200 turns. It is not a reskin of a known game. Its closest relatives are painting/territory games such as Paper.io and the Generals.io family, and harvest games such as Halite. It differs from them in five ways:

- income comes from **stakes**, not from carrying resources;
- a **defender's bulwark** (+1 on your own stake) makes raiding a timing and positioning problem;
- **territory is a sensor network** (stakes see radius 1);
- **exponential recruit cost** creates a bank-versus-invest tempo trade-off;
- a **hidden periodic tide** periodically erases the richest territory and kills crews caught on it.

### Strategic dimensions

These are the axes a good bot must handle:

1. **Economy tempo.** Every crew recruited lowers final grain directly, so a recruit must pay back. The cost grows ×1.2 per crew.
2. **Land versus fen valuation.** Land stakes are permanent (1 per turn for the rest of the game). Fens pay 2, 3 or 5 per turn, but only until the next flood of their elevation and must then be re-staked. Early game favours land; fens gain relative value as the game goes on.
3. **Tide inference (hidden but inferable).** Staking and standing on fens profitably requires predicting floods. Low fens give no visual warning before they flood.
4. **Combat.** 1-for-1 attrition on neutral cells and a +1 bulwark on your own stake. Walking into defended stakes is suicide; raiding undefended enemy stakes gives a double swing.
5. **Information.** Fog; the enemy's grain and crew count are never shown; lost stakes are reported without saying whether they were washed or taken; stakes give vision radius 1.
6. **Endgame.** Recruiting and far-away staking stop paying near turn 200.

### Hidden tide

This is the secret part of the engine:

- Per match, from the match seed: period `P ~ U{20..40}` and phase `φ ~ U{0..P−1}`.
- `f = ((t + φ) mod P) / P`; triangle wave `h = 1 − |2f − 1|`.
- `level = [h > 0.55] + [h > 0.72] + [h > 0.88]`.
- Flooded fraction of time: elevation 0 → 45%, elevation 1 → 28%, elevation 2 → 12%.
- For `P ≥ 20` the level changes by at most 1 per turn.
- The public rules disclose only the qualitative facts: periodic, 0→3→0 each cycle, at most one step per turn, period in [20, 40]. The thresholds, dwell times and waveform are hidden.
- An exact-knowledge filter over the 630 (P, φ) hypotheses pins the tide by about turns 27–43 in test games.

### Engine speed

About 5 ms per 200-turn game with idle bots, and about 19 ms with two in-process random bots (well within the 50 ms target). A full evaluation game (subprocess bot plus in-process ladder bot) costs about 0.1–0.5 s wall, dominated by the bots and process start-up.

## Reference ladder

All three non-random rungs are one crew-to-target planner with different feature switches (`ladder/ladder_common.py`). The planner:

1. Values each unowned cell as yield × expected income turns (enemy stakes ×2).
2. Assigns crews to targets greedily by value / (arrival delay + 1.5).
3. Steps along shortest paths, skipping cells judged unsafe (tide) or losing (combat threat).

| rung | tide model | combat | recruiting | other |
|---|---|---|---|---|
| L0 | — (random legal orders) | — | 25% chance when legal | public `random_bot.py` |
| L1 | crude: stay off fens up to the highest flooded elevation currently seen | avoids cells where visible enemies can win; no defence | whenever affordable until 30 turns left | fens valued by a fixed 8-turn guess |
| L2 | approximate: level bounds + rising/falling trend + period from observed flood onsets | + intercepts raiders standing on own stakes | payback rule (cost ≤ 2 × turns left) | — |
| L3 ("operator bot") | exact waveform family (filters (P, φ)), exact dry windows, waits for basins to drain, 8-turn escape check | same as L2 | marginal-income rule | memory of enemy stakes outside vision |

### Ablation findings from development

Each result is 60–100 games.

- **Threat awareness is the biggest discontinuity.** Bots that walk into visible enemies or defended stakes lose about 100% to bots that do not.
- **The approximate tide model adds almost nothing over the crude rule** (about 45:55).
- **Exact tide knowledge is worth about 80%** against L2.
- **Chasing raiders hurts** (23–30%).
- **Enemy-stake memory helps slightly.**
- **Raid multiplier, distance exponent and fen bias** tweaks were all within noise.

### Calibration

Round robin on 200 calibration maps × 2 seats = 400 games per pair, 2,400 games in total, 0 forfeits. Values are the row bot's score rate against the column bot.

| | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| L0 | – | 0.000 | 0.000 | 0.000 |
| L1 | 1.000 | – | 0.145 | 0.128 |
| L2 | 1.000 | 0.855 | – | 0.235 |
| L3 | 1.000 | 0.873 | 0.765 | – |

**Fitted ratings.** BT fit by MM with 0.5 pseudo-wins and 0.5 pseudo-losses per pair. In logits, anchored at L0 = 0:

| rung | L0 = 0 | L1 = 0 |
|---|---|---|
| L0 | 0 | −5.87 |
| L1 | 5.87 | 0 |
| L2 | 7.31 | +1.44 |
| L3 | 8.25 | +2.38 |

**Fit quality.** The ladder is strictly ordered pairwise, but the BT fit is imperfect:

| pair | BT prediction | observed |
|---|---|---|
| L3 vs L1 | 0.915 | 0.872 |
| L2 vs L1 | 0.809 | 0.855 |
| L3 vs L2 | 0.719 | 0.765 |

L3's specific edge (exact tide) does not compound against L1's specific weakness (no defence).

**What the L0 rating means.** L0 loses every game, so its position is set only by the pseudo-count. Rung positions between 0 and 1 are therefore coarse: a bot there beats random and loses almost everything to L1.

**CPU per game** (mean / max): L1 0.14 / 0.18 s, L2 0.13 / 0.20 s, L3 0.17 / 0.29 s. That is about 17× below the solver budget of 3.0 s.

## Scoring (implemented in public `score.py`)

- Each solver plays 400 games against each rung: 200 fresh private maps × 2 seats. The maps differ per rung, but the same maps are used for every solver (paired). The 1,600 games per solver share 800 distinct maps.
- **Headline:** 1-D BT maximum-likelihood rating with ladder ratings fixed and 0.5/0.5 pseudo-counts per rung. It is reported as:
  - a **rung position** (piecewise linear between rungs; above L3, extrapolated at the L2→L3 gap and flagged);
  - a logit and Elo difference relative to L1.
- CIs come from a percentile bootstrap (1,000 resamples) over maps within each rung.
- **Secondary:**
  - per-rung score rate with a clustered bootstrap CI;
  - forfeits with example reasons;
  - mean grain difference;
  - CPU per game;
  - an optional solver-vs-solver h2h matrix (default 200 games per pair, not part of the rating).

## Deviations from the F4 spec (pilot simplifications)

- **Players:** 2, not 2–4, so the win rate and BT rating are clean.
- **Turns:** 200 (the bottom of the 200–500 range).
- **Ladder:** heuristic rungs, not MCTS playout doublings. "Rung units" stand in for "ladder-doubling units", and the value of a rung is game-specific. There is no rung rotation, no frozen-entrant rung and no anchors hidden between windows.
- **Engine "binary":** CPython 3.11 bytecode without docstrings. It is decompilable in principle, so this is enforced by the tool policy only.
- **Evaluation scale:** 1,600 games per solver, not 2,000 or more, and no tournament against other entrants in the headline.
- **Attempts:** one attempt per model (Lite-track analogue: about 1M output tokens and 4 core-hours, self-policed), not 5 or more pre-registered attempts. There is no attempt-level CI, so attempt variance, which the spec identifies as the largest error term, is not measured.
- **Humans:** none. No human baseline or human season is available for this pilot.
- **No BYOH track.**
- **Sandboxing:** process isolation with CPU, wall and memory limits. There is no filesystem or network sandbox; conduct rules and a manifest check stand in for them.

## Known risks

- **Harness escape.** In-process bots are trusted ladder bots only. Submitted bots run in a separate process that receives JSON observations and returns JSON actions, never pickle. The only engine state they can reach is what is in the observation.
- **Tide leak through bytecode.** A solver who ignored the tool policy and disassembled the `.pyc` could read the thresholds and the period range. The range is public anyway.
- **Saturation at the top.** Top solver bots may exceed L3, which is a 1–2 hour heuristic, not a 10×-budget operator bot. Rung positions above 3 are extrapolations.

## Validation (reference bots scored as submissions through public score.py, 400 games per rung)

| submission | vs L0 | vs L1 | vs L2 | vs L3 | forfeits | rung position [95% CI] |
|---|---|---|---|---|---|---|
| random bot (= L0) | 0.500 | 0.000 | 0.000 | 0.000 | 0 | 0.00 [0.00, 0.00] |
| L3 | 1.000 | 0.887 | 0.765 | 0.500 | 0 | 3.03 (extrapolated) [2.94, 3.12] |

- **Mirror matches.** L3 against itself gives exactly 0.500 because the bots are deterministic and the maps are symmetric.
- **Head-to-head.** L3 scores 1.000 against random.
- **Run time.** 3,400 games took about 5–9 min on 4 cores. Four solvers plus h2h is about 7,600 games, which is 20–40 min depending on solver CPU.

## How to score solvers

```
openssl enc -d -aes-256-cbc -pbkdf2 -in sealed.tar.gz.enc -pass pass:<PASSPHRASE> | tar xz -C /tmp/f4dec   # creates /tmp/f4dec/sealed
cd public && python3 score.py --sealed /tmp/f4dec/sealed --answers ../answers --out /tmp/f4_results.json
```

Wipe the decrypted directory afterwards. To rebuild the ladder ratings, run `F4_PUBLIC=<public dir> python3 tools/calibrate.py 200`. Do this only for a new ladder version, because the headline assumes fixed ratings.
