"""Rung L2 - cautious planner.
L1 plus: an approximate tide model inferred only from observations (level bounds, rising /
falling trend, period from observed flood onsets), interception of enemy crews standing on its
own stakes, and a payback rule for recruiting."""
from ladder_common import Planner


class Bot(Planner):
    OPTS = dict(tide="approx", threat=True, defend=True, enemy_tg=True, memory=False, recruit="payback")
