"""Rung L3 - operator bot.
L2 plus operator knowledge of the tide waveform family (filters all (period, phase) hypotheses,
plans stakes by exact dry windows, waits for basins to drain, multi-turn escape check),
memory of enemy stakes outside vision, and a marginal-income recruiting rule."""
from ladder_common import Planner


class Bot(Planner):
    OPTS = dict(tide="exact", threat=True, defend=True, enemy_tg=True, memory=True, recruit="value", wait_drain=True)
