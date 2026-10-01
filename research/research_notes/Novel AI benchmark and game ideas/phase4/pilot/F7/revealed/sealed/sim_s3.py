"""S3 -- Habit adoption on a hidden social network (contagion family). SEALED.

Hidden mechanisms:
  * fixed hidden graph: 3 communities (A,B,C), heavy-tailed degrees, asymmetric cross-links
  * COMPLEX CONTAGION: a susceptible person adopts with high prob. only when the fraction of
    active neighbours exceeds a personal THRESHOLD (heterogeneous, hidden)
  * small spontaneous adoption plus heavy-tailed media shocks hitting one community
  * FATIGUE: adopters stay active >= a minimum period (delay), then lapse;
    lapsed people are refractory for a while before they can re-adopt
Observed daily per community: new_adopters, active.
"""
import numpy as np

T = 120
N_COMM = 3
COMM_SIZE = 100
N = N_COMM * COMM_SIZE
COLUMNS = ["new_adopters", "active"]
GRAPH_SEED = 90731

P = dict(
    beta=0.35, width=0.04, th_a=5.0, th_b=9.0,
    eps0=0.0015, comm_eps=[1.0, 1.0, 1.4],
    shock_p=0.03, shock_scale=0.012, shock_alpha=1.3, shock_cap=0.25, shock_decay=0.5,
    min_active=12, lapse=0.10, recover=0.015, burn=200, min_count=2,
    k_in=8.0, k_out=[[0, 0.6, 0.4], [0.6, 0, 1.6], [0.4, 1.6, 0]], deg_alpha=2.5,
)


def build_graph(p):
    g = np.random.default_rng(GRAPH_SEED)
    comm = np.repeat(np.arange(N_COMM), COMM_SIZE)
    w = (1 - g.random(N)) ** (-1 / (p["deg_alpha"] - 1))  # Pareto weights, min 1
    w = np.minimum(w, 15.0)
    adj = np.zeros((N, N), np.float32)
    for a in range(N_COMM):
        for b in range(a, N_COMM):
            ia = np.where(comm == a)[0]
            ib = np.where(comm == b)[0]
            wa, wb = w[ia], w[ib]
            target = p["k_in"] if a == b else p["k_out"][a][b]
            if target <= 0:
                continue
            prob = np.outer(wa, wb)
            prob = prob * (target * COMM_SIZE / (2 if a == b else 1)) / prob.sum() * (2 if a == b else 1)
            prob = np.minimum(prob, 1.0)
            e = g.random(prob.shape) < prob
            if a == b:
                e = np.triu(e, 1)
                e = e | e.T
            adj[np.ix_(ia, ib)] = np.maximum(adj[np.ix_(ia, ib)], e)
            adj[np.ix_(ib, ia)] = np.maximum(adj[np.ix_(ib, ia)], e.T)
    np.fill_diagonal(adj, 0)
    theta = g.beta(p["th_a"], p["th_b"], N)
    return comm, adj, theta


def run(R, seed, interventions=(), params=None):
    p = dict(P)
    if params:
        p.update(params)
    comm, adj, theta = build_graph(p)
    deg = np.maximum(adj.sum(1), 1.0)
    rng = np.random.default_rng(seed)
    state = np.zeros((R, N), np.int8)   # 0 susceptible, 1 active, 2 lapsed
    age = np.zeros((R, N), np.int16)
    init = rng.random((R, N)).argsort(1)[:, :2]
    state[np.arange(R)[:, None], init] = 1
    age[np.arange(R)[:, None], init] = rng.integers(0, 10, (R, 2))
    shock = np.zeros((R, N_COMM))
    comm_eps = np.array(p["comm_eps"]) * p["eps0"]
    obs = {c: np.zeros((R, T, N_COMM)) for c in COLUMNS}
    beta = np.full(R, p["beta"])
    for day in range(-p["burn"], T):
        extra = np.zeros(N_COMM)
        for iv in interventions:
            if iv["type"] == "seed" and iv["start"] == day:
                cs = [{"A": 0, "B": 1, "C": 2}[iv["community"]]] if iv["community"] in ("A", "B", "C") else [0, 1, 2]
                idx = np.where(np.isin(comm, cs))[0]
                key = rng.random((R, len(idx)))
                key[state[:, idx] != 0] = 2.0
                order = key.argsort(1)[:, :iv["size"]]
                chosen = idx[order]
                ok = np.take_along_axis(key, order, 1) < 1.5
                rows = np.broadcast_to(np.arange(R)[:, None], chosen.shape)
                state[rows[ok], chosen[ok]] = 1
                age[rows[ok], chosen[ok]] = 0
            elif iv["type"] == "friction" and iv["start"] == day:
                beta[:] = p["beta"] * iv["size"]
            elif iv["type"] == "broadcast" and iv["start"] <= day < iv["start"] + iv["duration"]:
                extra += iv["size"]
        # media shocks
        hit = rng.random(R) < p["shock_p"]
        which = rng.integers(0, N_COMM, R)
        mag = np.minimum(p["shock_scale"] * rng.random(R) ** (-1 / p["shock_alpha"]), p["shock_cap"])
        shock *= p["shock_decay"]
        shock[np.arange(R)[hit], which[hit]] += mag[hit]
        act = (state == 1).astype(np.float32)
        cnt = act @ adj
        frac = cnt / deg
        eps = comm_eps[comm][None, :] + shock[:, comm] + extra[comm][None, :]
        z = np.clip((frac - theta[None, :]) / p["width"], -30, 30)
        padopt = beta[:, None] / (1 + np.exp(-z)) * (cnt >= p["min_count"]) + eps
        u = rng.random((R, N))
        adopt = (state == 0) & (u < padopt)
        # fatigue / lapse
        lapse = (state == 1) & (age >= p["min_active"]) & (rng.random((R, N)) < p["lapse"])
        rec = (state == 2) & (rng.random((R, N)) < p["recover"])
        age[state == 1] += 1
        state[lapse] = 2
        state[rec] = 0
        state[adopt] = 1
        age[adopt] = 0
        if day >= 0:
            for c in range(N_COMM):
                sl = slice(c * COMM_SIZE, (c + 1) * COMM_SIZE)
                obs["new_adopters"][:, day, c] = adopt[:, sl].sum(1)
                obs["active"][:, day, c] = (state[:, sl] == 1).sum(1)
    return obs
