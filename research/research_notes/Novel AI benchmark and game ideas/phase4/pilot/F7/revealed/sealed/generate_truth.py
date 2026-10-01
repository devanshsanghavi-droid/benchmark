"""Sealed rollouts: truth (10k), oracle reference (independent 10k) and no-change (10k) per question. SEALED."""
import os, sys, time
import numpy as np
from config import QUESTIONS, N_TRUTH
from common import seed_for, load_sim, rounded, outcome

sim = sys.argv[1]
KEY = sys.argv[2]
CH = 2500


def outcomes(ivs, seed, outs):
    mod = load_sim(sim)
    res = [[] for _ in outs]
    ss = np.random.SeedSequence(seed)
    for child in ss.spawn(N_TRUTH // CH):
        o = rounded(sim, mod.run(CH, int(child.generate_state(1, np.uint64)[0]), ivs))
        for k, out in enumerate(outs):
            res[k].append(outcome(o, out))
    return [np.concatenate(r) for r in res]


qs = [q for q in QUESTIONS if q["sim"] == sim]
arrs = {}
t0 = time.time()
nc = outcomes([], seed_for("nochange", sim), [q["out"] for q in qs])
for q, y in zip(qs, nc):
    arrs["nochange__" + q["id"]] = y
print(sim, "nochange done", round(time.time() - t0), flush=True)
for q in qs:
    arrs["truth__" + q["id"]] = outcomes(q["iv"], seed_for("truth", q["id"]), [q["out"]])[0]
    arrs["oracle__" + q["id"]] = outcomes(q["iv"], seed_for("oracle", q["id"]), [q["out"]])[0]
    print(sim, q["id"], "done", round(time.time() - t0), flush=True)
np.savez_compressed(os.path.join(KEY, "samples_%s.npz" % sim), **arrs)
print(sim, "saved", flush=True)
