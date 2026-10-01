"""Print full-information renders of one game every k turns (SEALED dev tool).
usage: trace.py botA.py botB.py seed every"""
import os, sys
SEALED = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.environ["F4_PUBLIC"]
sys.path[:0] = [PUBLIC, SEALED, os.path.join(SEALED, "ladder")]
import harness, mapgen, brackwater_engine as bw
a, b, seed, every = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
m = bw.parse_map(mapgen.generate(seed))
def tr(match):
    if match.turn % every == 0:
        print(match.render()); print("level", match._level, "P", match._Match__p, "stats", match._stats); print()
r = harness.play_game(m, seed, [("inproc", a), ("inproc", b)], trace=tr)
print(r)
