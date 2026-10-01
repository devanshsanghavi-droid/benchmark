"""Quick in-process arena for reference bots (SEALED dev tool).
usage: arena.py botA.py botB.py [n_maps] [seed_offset]"""
import os, sys, statistics as st
SEALED = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.environ["F4_PUBLIC"]
sys.path[:0] = [PUBLIC, SEALED, os.path.join(SEALED, "ladder")]
import harness, mapgen, brackwater_engine as bw
a, b = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 50
off = int(sys.argv[4]) if len(sys.argv) > 4 else 100000
jobs = []
for i in range(n):
    s = off + i
    m = bw.parse_map(mapgen.generate(s))
    jobs.append(((i, 0), m, s, [("inproc", a), ("inproc", b)], None))
    jobs.append(((i, 1), m, s, [("inproc", b), ("inproc", a)], None))
rs = harness.run_jobs(jobs, workers=4, progress=False)
wa = 0.0; ga = []; gb = []; cpua = []; cpub = []; stats = {"A": {}, "B": {}}
for (jid, _, _, _, _), r in zip(jobs, rs):
    pa = 0 if jid[1] == 0 else 1
    if r["winner"] == pa: wa += 1
    elif r["winner"] is None: wa += 0.5
    ga.append(r["grain"][pa]); gb.append(r["grain"][1 - pa])
    cpua.append(r["cpu"][pa]); cpub.append(r["cpu"][1 - pa])
    for k, v in r["stats"].items():
        stats["A"][k] = stats["A"].get(k, 0) + v[pa]; stats["B"][k] = stats["B"].get(k, 0) + v[1 - pa]
    if r["forfeit"] != [None, None]: print("FORFEIT", r["forfeit"])
N = len(rs)
print("%s vs %s: A winrate %.3f over %d games | grain A %.0f B %.0f | cpu/game A %.3f (max %.3f) B %.3f (max %.3f)" % (
    os.path.basename(a), os.path.basename(b), wa / N, N, st.mean(ga), st.mean(gb), st.mean(cpua), max(cpua), st.mean(cpub), max(cpub)))
print("  A stats/game:", {k: round(v / N, 1) for k, v in stats["A"].items()})
print("  B stats/game:", {k: round(v / N, 1) for k, v in stats["B"].items()})
