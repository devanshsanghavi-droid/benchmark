"""Owner baselines computed ONLY from public/ files (no simulator access). SEALED (owner-side).

naive_extrapolator : history quantiles of the outcome + linear extrapolation of the effect seen in
                     single-intervention pilot experiments of the same type (slope per unit size vs
                     the no-change value), summed over the question's interventions; timing ignored.
history_climatology: history quantiles of the outcome (a data-estimated no-change forecast).
spam_random        : sorted uniform random numbers between the min and max of the history outcome.
"""
import csv, json, os, sys
from collections import defaultdict
import numpy as np

PUB = sys.argv[1]
OUT = sys.argv[2]
TAUS = [0.05, 0.25, 0.5, 0.75, 0.95]
QKEYS = ["q05", "q25", "q50", "q75", "q95"]
TIME_COL = {"S1": "day", "S2": "hour", "S3": "day", "S4": "round", "S5": "hour"}


def load(path, idcols):
    """-> dict run_key -> dict column -> array over time (S3: summed or per community)."""
    runs = defaultdict(lambda: defaultdict(dict))
    with open(path) as f:
        for row in csv.DictReader(f):
            k = tuple(row[c] for c in idcols)
            t = int(row[TIME_CUR])
            grp = row.get("community")
            for c, v in row.items():
                if c in idcols or c in ("hour", "day", "round", "hour_of_day", "community"):
                    continue
                val = float(v) if v != "" else np.nan
                runs[k][(c, grp)][t] = val
    out = {}
    for k, cols in runs.items():
        d = {}
        for (c, g), m in cols.items():
            T = max(m) + 1
            a = np.array([m[t] for t in range(T)])
            d[(c, g)] = a
        out[k] = d
    return out


def outcome(run, spec):
    col = spec["column"]
    comm = spec.get("community")
    if comm is None:
        a = run[(col, None)]
    elif comm in ("A", "B", "C"):
        a = run[(col, comm)]
    else:
        a = run[(col, "A")] + run[(col, "B")] + run[(col, "C")]
    if "time_index" in spec:
        return a[spec["time_index"]]
    seg = a[spec["from"]:spec["to"] + 1]
    return seg.mean() if spec["aggregate"] == "mean" else seg.sum()


def ivsize(iv):
    return iv["duration"] if iv["type"] == "outage" else iv["size"]


def main():
    global TIME_CUR
    qdoc = json.load(open(os.path.join(PUB, "questions.json")))
    naive, clim, spam = {}, {}, {}
    rng = np.random.default_rng(2026)
    cache = {}
    for q in qdoc["questions"]:
        sim, folder = q["simulator"], q["folder"]
        TIME_CUR = TIME_COL[sim]
        if sim not in cache:
            hist = load(os.path.join(PUB, folder, "history.csv"), ["episode"])
            exps = load(os.path.join(PUB, folder, "experiments.csv"), ["experiment", "replicate"])
            menu = json.load(open(os.path.join(PUB, folder, "experiments.json")))
            cache[sim] = (hist, exps, menu)
        hist, exps, menu = cache[sim]
        spec = q["outcome"]
        b = np.array([outcome(r, spec) for r in hist.values()])
        bq = np.quantile(b, TAUS)
        effect = 0.0
        for iv in q["interventions"]:
            null = menu["intervention_types"][iv["type"]]["no_change_value"]
            slopes = []
            cands = [e for e in menu["experiments"] if len(e["interventions"]) == 1 and e["interventions"][0]["type"] == iv["type"]]
            if iv["type"] == "seed":
                same = [e for e in cands if e["interventions"][0].get("community") == iv.get("community")]
                cands = same or cands
            for e in cands:
                ys = [outcome(r, spec) for k, r in exps.items() if k[0] == e["experiment"]]
                d = ivsize(e["interventions"][0]) - null
                if d != 0:
                    slopes.append((np.mean(ys) - b.mean()) / d)
            if slopes:
                effect += float(np.mean(slopes)) * (ivsize(iv) - null)
        nq = np.maximum(bq + effect, 0.0)
        naive[q["id"]] = dict(zip(QKEYS, [float(x) for x in nq]))
        clim[q["id"]] = dict(zip(QKEYS, [float(x) for x in bq]))
        sq = np.sort(rng.uniform(b.min(), b.max(), 5))
        spam[q["id"]] = dict(zip(QKEYS, [float(x) for x in sq]))
    os.makedirs(OUT, exist_ok=True)
    for name, fc in (("naive_extrapolator", naive), ("history_climatology", clim), ("spam_random", spam)):
        json.dump({"solver_label": name, "forecasts": fc}, open(os.path.join(OUT, name + ".json"), "w"), indent=1)
    print("baselines written to", OUT)


TIME_CUR = None
if __name__ == "__main__":
    main()
