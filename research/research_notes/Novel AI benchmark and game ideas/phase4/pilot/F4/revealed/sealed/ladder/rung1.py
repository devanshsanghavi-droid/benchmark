"""Rung L1 - greedy staker with combat caution.
Crews go for the best unclaimed cell by value/distance (land valued by turns left, fens by a
fixed 8-turn guess, enemy stakes x2), avoid ending turns where visible enemy crews could beat
them, and use only a crude tide rule (stay off fens up to the highest flooded elevation seen
right now).  No defence of its own stakes; recruits whenever it can until 30 turns remain."""
from ladder_common import Planner


class Bot(Planner):
    OPTS = dict(tide="crude", threat=True, defend=False, enemy_tg=True, memory=False, recruit="always")
