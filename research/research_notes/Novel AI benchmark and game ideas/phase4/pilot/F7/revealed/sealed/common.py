"""Shared helpers for the sealed generator. SEALED."""
import json, os, zlib, importlib
import numpy as np
from config import SIMS

ROUND = {
    "S1": dict(nutrient=3, algae=3, grazers=0, fish=0),
    "S2": dict(offered=0, answered=0, abandoned=0, queue_end=0, avg_wait_min=2, scheduled_agents=0),
    "S3": dict(new_adopters=0, active=0),
    "S4": dict(reserve=2, sold=0, price=3, revenue=3, n_bids=0, active_bidders=0),
    "S5": dict(biomass=4, substrate=4, product=4, temperature=3, cooling_duty=4),
}
HERE = os.path.dirname(os.path.abspath(__file__))


def master_seed():
    with open(os.path.join(HERE, "seeds.json")) as f:
        return json.load(f)["master_seed"]


def seed_for(*keys):
    ints = [zlib.crc32(str(k).encode()) for k in keys]
    ss = np.random.SeedSequence(entropy=master_seed(), spawn_key=ints)
    return int(ss.generate_state(1, np.uint64)[0])


def load_sim(sim):
    return importlib.import_module(SIMS[sim]["module"])


def rounded(sim, obs):
    out = {}
    for c, a in obs.items():
        nd = ROUND[sim][c]
        out[c] = np.round(a, nd)
    return out


def outcome(obs, out):
    a = obs[out["col"]]
    if a.ndim == 3:
        a = a[:, :, out["group"]] if "group" in out else a.sum(2)
    if "step" in out:
        return a[:, out["step"]].astype(float)
    seg = a[:, out["from"]:out["to"] + 1]
    if out["agg"] == "mean":
        return seg.mean(1)
    if out["agg"] == "sum":
        return seg.sum(1)
    raise ValueError(out)


def run_chunked(sim, R, seed, ivs, chunk=2500):
    """Run R rollouts in chunks (independent sub-seeds) and return rounded observations."""
    mod = load_sim(sim)
    parts = []
    ss = np.random.SeedSequence(seed)
    for i, child in enumerate(ss.spawn((R + chunk - 1) // chunk)):
        r = min(chunk, R - i * chunk)
        parts.append(rounded(sim, mod.run(r, int(child.generate_state(1, np.uint64)[0]), ivs)))
    return {c: np.concatenate([p[c] for p in parts], 0) for c in parts[0]}
