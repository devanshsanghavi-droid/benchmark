"""Ladder calibration (SEALED tool): round robin among L0..L3 on the calibration maps
(each map twice, seats swapped), BT fit with 0.5/0.5 pseudo-counts per pair, L0 anchored at 0.
Writes ladder_ratings.json next to seeds.json and prints the pairwise matrix."""
import json, math, os, sys, time
SEALED = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.environ["F4_PUBLIC"]
sys.path[:0] = [PUBLIC, SEALED, os.path.join(SEALED, "ladder")]
import harness, mapgen, brackwater_engine as bw
n_maps = int(sys.argv[1]) if len(sys.argv) > 1 else 200
R = ["L0", "L1", "L2", "L3"]
files = {"L1": "ladder/rung1.py", "L2": "ladder/rung2.py", "L3": "ladder/rung3.py"}
path = {"L0": os.path.join(PUBLIC, "random_bot.py")}
path.update({k: os.path.join(SEALED, v) for k, v in files.items()})
seeds = json.load(open(os.path.join(SEALED, "seeds.json")))["calibration"][:n_maps]
maps = {s: bw.parse_map(mapgen.generate(s)) for s in seeds}
jobs = []
for i in range(4):
    for j in range(i + 1, 4):
        a, b = R[i], R[j]
        for s in seeds:
            jobs.append(((a, b, s, 0), maps[s], s, [("inproc", path[a]), ("inproc", path[b])], None))
            jobs.append(((a, b, s, 1), maps[s], s, [("inproc", path[b]), ("inproc", path[a])], None))
t0 = time.time()
res = harness.run_jobs(jobs, workers=4)
W = {}; N = {}; cpu = {k: [] for k in R}; forf = 0
for (jid, *_), r in zip(jobs, res):
    a, b, s, seat = jid
    pa = seat
    sc = 1.0 if r["winner"] == pa else (0.5 if r["winner"] is None else 0.0)
    W[(a, b)] = W.get((a, b), 0) + sc; N[(a, b)] = N.get((a, b), 0) + 1
    cpu[a].append(r["cpu"][pa]); cpu[b].append(r["cpu"][1 - pa])
    if r["forfeit"] != [None, None]: forf += 1
# BT by MM with pseudo-counts
PS = 0.5
wins = {k: 0.0 for k in R}
n = {}
for (a, b), w in W.items():
    wins[a] += w + PS; wins[b] += N[(a, b)] - w + PS
    n[(a, b)] = n[(b, a)] = N[(a, b)] + 2 * PS
g = {k: 1.0 for k in R}
for _ in range(20000):
    new = {}
    for i in R:
        den = sum(n[(i, j)] / (g[i] + g[j]) for j in R if j != i)
        new[i] = wins[i] / den
    z = new["L0"]
    new = {k: v / z for k, v in new.items()}
    if max(abs(math.log(new[k]) - math.log(g[k])) for k in R) < 1e-12:
        g = new; break
    g = new
rat = {k: math.log(g[k]) for k in R}
out = {"ratings_logit": rat, "files": files, "anchor": "L0 = 0 (scores are reported relative to L1)",
       "pseudo_count": PS, "maps": n_maps, "games_per_pair": 2 * n_maps,
       "pairwise_score_rate": {"%s_vs_%s" % k: W[k] / N[k] for k in W},
       "cpu_per_game_mean": {k: sum(v) / len(v) for k, v in cpu.items()},
       "cpu_per_game_max": {k: max(v) for k, v in cpu.items()}, "forfeit_games": forf}
json.dump(out, open(os.path.join(SEALED, "ladder_ratings.json"), "w"), indent=1)
print("elapsed %.0fs, forfeits %d" % (time.time() - t0, forf))
for (a, b) in W:
    p = W[(a, b)] / N[(a, b)]
    se = math.sqrt(p * (1 - p) / N[(a, b)])
    pred = 1 / (1 + math.exp(-(rat[a] - rat[b])))
    print("%s vs %s: %.3f (+-%.3f, n=%d)  BT-pred %.3f" % (a, b, p, 1.96 * se, N[(a, b)], pred))
print("ratings (L0=0):", {k: round(v, 3) for k, v in rat.items()})
print("ratings (L1=0):", {k: round(v - rat["L1"], 3) for k, v in rat.items()})
print("cpu/game mean:", {k: round(v, 3) for k, v in out["cpu_per_game_mean"].items()}, "max:", {k: round(v, 3) for k, v in out["cpu_per_game_max"].items()})
