#!/usr/bin/env python3
"""F5 pilot: supplementary analysis behind RESULTS.md (format-normalised re-grade, extra bootstrap CIs, cross-solver
checks, phase-1 consistency, cross-reading checks, deliberate-failure counterfactual).

Usage (from anywhere; needs revealed/ decrypted next to this file):
    python3 analysis_supplementary.py [OUT.json]
Imports public/score.py; standard library only; writes nothing unless OUT.json is given."""
import json, math, os, random, sys, difflib, itertools, re

F5 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(F5, "public"))
import score as sc

key = json.load(open(os.path.join(F5, "revealed/sealed/key/key.json")))
items = key["items"]
ids = sorted(items)
S = ["haiku", "sonnet", "opus", "fable"]
data = {s: json.load(open(os.path.join(F5, f"answers/{s}.json"))) for s in S}
ph1 = {s: json.load(open(os.path.join(F5, f"answers/{s}.phase1.json"))) for s in S}
B = 2000
SEED = 20261001

fam = [items[i]["family"] for i in ids]
lvl = [items[i]["level"] for i in ids]
twin = [items[i]["set"] == "twin" for i in ids]
fidx = [k for k in range(60) if not twin[k]]


# ---------------- format normalisation (type/format only, never semantic) ----------------
def variants(a):
    """Alternative encodings of the same answer: JSON-list string <-> list, int <-> digit string."""
    out = []
    if isinstance(a, str):
        s = a.strip()
        try:
            v = json.loads(s)
            if isinstance(v, (list, int)) and not isinstance(v, bool):
                out.append(v)
        except Exception:
            pass
    if isinstance(a, list):
        out.append(", ".join(str(x) for x in a))
        out.append(json.dumps(a))
    if isinstance(a, int) and not isinstance(a, bool):
        out.append(str(a))
    return out


Y, Yn, P, Q, fmt_changes = {}, {}, {}, {}, {}
for s in S:
    att = data[s]["attempts"]
    y, yn, p, ch = [], [], [], []
    for k, i in enumerate(ids):
        a = att[i]["answer"]
        ok, _ = sc.is_correct(items[i], a)
        okn = ok
        if not ok:
            for v in variants(a):
                if sc.is_correct(items[i], v)[0]:
                    okn = True
                    ch.append(i)
                    break
        y.append(int(ok)); yn.append(int(okn)); p.append(float(att[i]["p"]))
    Y[s], Yn[s], P[s], fmt_changes[s] = y, yn, p, ch
    fc = data[s]["forecasts"]
    Q[s] = [fc.get(i) for i in ids]

# answer-type usage (for the report)
types = {}
for s in S:
    t = {}
    for i in ids:
        a = data[s]["attempts"][i]["answer"]
        at = items[i]["atype"]
        t.setdefault(at, set()).add(type(a).__name__)
    types[s] = {k: sorted(v) for k, v in sorted(t.items())}


# ---------------- helpers ----------------
def clopper_pearson(x, n, a=0.05):
    # exact binomial CI via bisection on the regularised incomplete beta (use simple binomial sums)
    def cdf(k, n, p):
        return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k + 1))
    lo = 0.0 if x == 0 else _bis(lambda p: 1 - cdf(x - 1, n, p) - a / 2)
    hi = 1.0 if x == n else _bis(lambda p: cdf(x, n, p) - a / 2, inc=False)
    return lo, hi


def _bis(f, inc=True):
    lo, hi = 0.0, 1.0
    for _ in range(100):
        m = (lo + hi) / 2
        v = f(m)
        if (v < 0) == inc:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def boot(fn, idx_pool, rng, B=B):
    vals = []
    n = len(idx_pool)
    for _ in range(B):
        ix = [idx_pool[rng.randrange(n)] for _ in range(n)]
        v = fn(ix)
        if v is not None:
            vals.append(v)
    if len(vals) < 0.5 * B:
        return None
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def spearman(a, b):
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]:
                j += 1
            for k in range(i, j + 1):
                r[o[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    return sc._pearson(rank(a), rank(b))


def logscore_mean(ps, ys):
    return sum(sc.ls(p, y) for p, y in zip(ps, ys)) / len(ps)


def triage(s, ys):
    tri = data[s]["triage"]
    pos = {i: k for k, i in enumerate(ids)}
    num = den = 0.0
    det = {}
    for b, bids in key["blocks"].items():
        sb = sum(ys[pos[x]] for x in bids)
        got = sum(ys[pos[x]] for x in tri[b])
        num += got - 5 * sb / 15
        den += min(5, sb) - 5 * sb / 15
        det[b] = f"{got}/{sb}"
    return (num / den if den > 1e-12 else None), det


R = {}
for s in S:
    rng = random.Random(SEED)
    y, p = Y[s], P[s]
    n = 60
    allidx = list(range(60))
    r = {}
    r["n_correct"] = sum(y)
    r["n_correct_fmt_norm"] = sum(Yn[s])
    r["fmt_changes"] = fmt_changes[s]
    r["acc"] = sum(y) / n
    r["acc_cp95"] = clopper_pearson(sum(y), n)
    r["mean_p"] = sum(p) / n
    r["sum_p"] = sum(p)
    r["brier"] = sc.brier(p, y)
    r["brier_ci"] = boot(lambda ix: sc.brier([p[k] for k in ix], [y[k] for k in ix]), allidx, rng)
    r["ece"] = sc.murphy(p, y)["ece"]
    r["logscore"] = logscore_mean(p, y)
    r["auroc"] = sc.auroc(p, y)
    r["auroc_ci"] = boot(lambda ix: sc.auroc([p[k] for k in ix], [y[k] for k in ix]), allidx, rng)
    r["auroc_lvl"] = sc.auroc_strat(p, y, lvl)[0]
    r["auroc_lvl_ci"] = boot(lambda ix: sc.auroc_strat([p[k] for k in ix], [y[k] for k in ix],
                                                        [lvl[k] for k in ix])[0], allidx, rng)
    r["auroc_cue_level"] = sc.auroc([-l for l in lvl], y)
    r["SR_glob"] = sc.sr_const(p, y, ["all"] * n)
    r["SR_glob_ci"] = boot(lambda ix: sc.sr_const([p[k] for k in ix], [y[k] for k in ix], ["all"] * len(ix)),
                           allidx, rng)
    r["SR_twin"] = sc.sr_twin(p, y, fam, twin)
    r["SR_twin_const"] = sc.sr_twin([r["acc"]] * n, y, fam, twin)
    r["SR_twin_ci"] = sc.boot_ci(lambda ix: sc.sr_twin([p[k] for k in ix], [y[k] for k in ix], [fam[k] for k in ix],
                                                       [twin[k] for k in ix]), n, B, rng, strata=twin)
    r["triage"], r["triage_detail"] = triage(s, y)
    # prospective q on forecast items
    q = [Q[s][k] for k in fidx]
    yf = [y[k] for k in fidx]
    r["acc_f"] = sum(yf) / len(yf)
    r["mean_q"] = sum(q) / len(q)
    r["sum_q"] = sum(q)
    r["n_correct_f"] = sum(yf)
    r["brier_q"] = sc.brier(q, yf)
    r["brier_q_ci"] = boot(lambda ix: sc.brier([Q[s][k] for k in ix], [y[k] for k in ix]), fidx, rng)
    r["logscore_q"] = logscore_mean(q, yf)
    r["auroc_q"] = sc.auroc(q, yf)
    r["auroc_q_ci"] = boot(lambda ix: sc.auroc([Q[s][k] for k in ix], [y[k] for k in ix]), fidx, rng)
    r["SR_glob_q"] = sc.sr_const(q, yf, ["all"] * len(q))
    r["corr_pq"] = sc._pearson([p[k] for k in fidx], q)
    r["spearman_p_level"] = spearman(p, lvl)
    r["spearman_q_level"] = spearman(q, [lvl[k] for k in fidx])
    r["acc_by_level"] = {l: sum(y[k] for k in range(60) if lvl[k] == l) / 12 for l in range(1, 6)}
    r["meanp_by_level"] = {l: sum(p[k] for k in range(60) if lvl[k] == l) / 12 for l in range(1, 6)}
    fams = sorted(set(fam))
    r["acc_by_family"] = {f: sum(y[k] for k in range(60) if fam[k] == f) / 10 for f in fams}
    r["acc_twin"] = sum(y[k] for k in range(60) if twin[k]) / 15
    R[s] = r

# ---------------- cross-solver ----------------
X = {}
# rank correlation across the 4 solvers: accuracy vs each self-knowledge metric (higher = better)
acc4 = [R[s]["acc"] for s in S]
for m, sign in [("SR_glob", 1), ("SR_twin", 1), ("brier", -1), ("ece", -1), ("logscore", 1), ("brier_q", -1),
                ("logscore_q", 1)]:
    X["spearman_acc_vs_" + m] = spearman(acc4, [sign * R[s][m] for s in S])
# paired bootstrap of differences among ceiling solvers
rng = random.Random(SEED + 1)
pairs = {}
for a, b in itertools.combinations(["sonnet", "opus", "fable"], 2):
    for m, fn in [("SR_glob", lambda s, ix: sc.sr_const([P[s][k] for k in ix], [Y[s][k] for k in ix], ["all"] * len(ix))),
                  ("brier", lambda s, ix: sc.brier([P[s][k] for k in ix], [Y[s][k] for k in ix]))]:
        d = fn(a, range(60)) - fn(b, range(60))
        ci = boot(lambda ix: fn(a, ix) - fn(b, ix), list(range(60)), rng)
        pairs[f"{m}:{a}-{b}"] = (d, ci)
X["paired_diffs"] = pairs
# do peers' confidences (apparent difficulty) predict haiku's correctness?
peer_p = [sum(P[s][k] for s in ["sonnet", "opus", "fable"]) / 3 for k in range(60)]
X["auroc_peer_meanp_for_haiku"] = sc.auroc(peer_p, Y["haiku"])
X["auroc_peer_meanp_for_haiku_within_level"] = sc.auroc_strat(peer_p, Y["haiku"], lvl)[0]
X["auroc_peer_meanp_for_haiku_ci"] = boot(lambda ix: sc.auroc([peer_p[k] for k in ix], [Y["haiku"][k] for k in ix]),
                                         list(range(60)), random.Random(SEED + 2))
for s in ["sonnet", "opus", "fable"]:
    X[f"auroc_{s}_p_for_haiku"] = sc.auroc(P[s], Y["haiku"])
X["spearman_p_between"] = {f"{a}-{b}": spearman(P[a], P[b]) for a, b in itertools.combinations(S, 2)}
X["spearman_q_between"] = {f"{a}-{b}": spearman([Q[a][k] for k in fidx], [Q[b][k] for k in fidx])
                           for a, b in itertools.combinations(S, 2)}
# haiku: p of correct vs wrong
X["haiku_meanp_correct"] = sum(p for p, y in zip(P["haiku"], Y["haiku"]) if y) / sum(Y["haiku"])
X["haiku_meanp_wrong"] = sum(p for p, y in zip(P["haiku"], Y["haiku"]) if not y) / (60 - sum(Y["haiku"]))

# ---------------- cross-reading checks ----------------
work = {s: [data[s]["attempts"][i]["work"] for i in ids] for s in S}
ans = {s: [data[s]["attempts"][i]["answer"] for i in ids] for s in S}
sim = {}
for a, b in itertools.combinations(S, 2):
    r_ = [difflib.SequenceMatcher(None, work[a][k].lower(), work[b][k].lower()).ratio() for k in range(60)]
    sim[f"{a}-{b}"] = {"mean": sum(r_) / 60, "max": max(r_), "argmax": ids[r_.index(max(r_))],
                       "n_ge_0.8": sum(x >= 0.8 for x in r_), "identical": sum(work[a][k] == work[b][k] for k in range(60))}
X["work_similarity"] = sim
# identical wrong answers between any two solvers
idw = []
for a, b in itertools.combinations(S, 2):
    for k, i in enumerate(ids):
        if not Y[a][k] and not Y[b][k]:
            na = sc.norm(items[i]["atype"], ans[a][k]); nb = sc.norm(items[i]["atype"], ans[b][k])
            if na == nb:
                idw.append((a, b, i))
X["identical_wrong_answers"] = idw
# phase-1 consistency
pc = {}
for s in S:
    f1, t1 = ph1[s]["forecasts"], ph1[s]["triage"]
    f2, t2 = data[s]["forecasts"], data[s]["triage"]
    pc[s] = {"n_forecasts": len(f1), "forecasts_identical": f1 == f2, "triage_identical": t1 == t2,
             "triage_sizes": {b: len(v) for b, v in t1.items()},
             "picks_in_block": all(x in key["blocks"][b] for b, v in t1.items() for x in v),
             "forecast_ids_match": sorted(f1) == sorted(i for i in ids if items[i]["set"] == "forecast")}
X["phase1"] = pc
# haiku triage picks: levels and outcomes
pos = {i: k for k, i in enumerate(ids)}
X["haiku_picks"] = {b: [(x, items[x]["level"], Y["haiku"][pos[x]]) for x in v] for b, v in data["haiku"]["triage"].items()}
X["answer_types_used"] = types
# deliberate-failure counterfactual for ceiling solvers: in each block fail the unpicked item with the lowest stated p
# and state p = 0.01 for it (3 items in all); everything else as submitted
cf = {}
for s in ["sonnet", "opus", "fable"]:
    tri = data[s]["triage"]
    y, p2 = list(Y[s]), list(P[s])
    for b, bids in key["blocks"].items():
        j = min((x for x in bids if x not in tri[b]), key=lambda x: P[s][pos[x]])
        y[pos[j]], p2[pos[j]] = 0, 0.01
    cf[s] = {"acc": sum(y) / 60, "auroc": sc.auroc(p2, y), "SR_glob": sc.sr_const(p2, y, ["all"] * 60),
             "brier": sc.brier(p2, y), "triage": triage(s, y)[0]}
X["deliberate_failure_counterfactual"] = cf

out = {"R": R, "X": X}
if len(sys.argv) > 1:
    json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
