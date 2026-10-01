"""Write public data: history CSVs, pilot-experiment CSVs and menus, questions.json. SEALED."""
import csv, json, os, sys
import numpy as np
from config import SIMS, EXPERIMENTS, QUESTIONS, IV_TYPES
from common import seed_for, run_chunked, ROUND

PUB = sys.argv[1]
LETTER = {0: "A", 1: "B", 2: "C"}


def fmt(v, nd):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    if nd == 0:
        return str(int(round(v)))
    return ("%." + str(nd) + "f") % v


def time_cols(sim, t):
    if sim == "S2":
        return [t, t // 24, t % 24]
    return [t]


def time_header(sim):
    tu = SIMS[sim]["time"]
    if sim == "S2":
        return ["hour", "day", "hour_of_day"]
    return [tu]


def header(sim, obs, prefix_cols):
    cols = list(obs.keys())
    grouped = obs[cols[0]].ndim == 3
    return prefix_cols + time_header(sim) + (["community"] if grouped else []) + cols


def write_rows(w, sim, obs, prefix_vals_fn):
    cols = list(obs.keys())
    R, T = obs[cols[0]].shape[:2]
    grouped = obs[cols[0]].ndim == 3
    for r in range(R):
        pv = prefix_vals_fn(r)
        for t in range(T):
            if grouped:
                for g in range(obs[cols[0]].shape[2]):
                    w.writerow(pv + time_cols(sim, t) + [LETTER[g]] + [fmt(obs[c][r, t, g], ROUND[sim][c]) for c in cols])
            else:
                w.writerow(pv + time_cols(sim, t) + [fmt(float(obs[c][r, t]), ROUND[sim][c]) for c in cols])


def pub_iv(iv):
    d = {"type": iv["type"], "start": iv["start"]}
    for k in ("size", "duration", "community"):
        if k in iv:
            d[k] = iv[k]
    return d


def pub_out(sim, out):
    d = {"column": out["col"]}
    if "step" in out:
        d["time_index"] = out["step"]
    else:
        d["aggregate"] = out["agg"]
        d["from"] = out["from"]
        d["to"] = out["to"]
    if sim == "S3":
        d["community"] = LETTER[out["group"]] if "group" in out else "A+B+C (sum)"
    return d


def main():
    for sim, meta in SIMS.items():
        d = os.path.join(PUB, meta["folder"])
        os.makedirs(d, exist_ok=True)
        hist = run_chunked(sim, meta["n_hist"], seed_for("hist", sim), [])
        with open(os.path.join(d, "history.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header(sim, hist, ["episode"]))
            write_rows(w, sim, hist, lambda r: [r])
        menu = []
        with open(os.path.join(d, "experiments.csv"), "w", newline="") as f:
            w = csv.writer(f)
            for k, e in enumerate(EXPERIMENTS[sim]):
                o = run_chunked(sim, e["paths"], seed_for("exp", e["id"]), e["iv"])
                if k == 0:
                    w.writerow(header(sim, o, ["experiment", "replicate"]))
                write_rows(w, sim, o, lambda r, eid=e["id"]: [eid, r])
                menu.append({"experiment": e["id"], "interventions": [pub_iv(i) for i in e["iv"]], "replicates": e["paths"]})
        types = sorted({i["type"] for e in EXPERIMENTS[sim] for i in e["iv"]} | {i["type"] for q in QUESTIONS if q["sim"] == sim for i in q["iv"]})
        with open(os.path.join(d, "experiments.json"), "w") as f:
            json.dump({"simulator": sim, "time_unit": meta["time"],
                       "intervention_types": {t: {"kind": IV_TYPES[t]["mode"], "no_change_value": IV_TYPES[t]["null"]} for t in types},
                       "experiments": menu}, f, indent=1)
        print(sim, "public data written", flush=True)
    qs = []
    for q in QUESTIONS:
        qs.append({"id": q["id"], "simulator": q["sim"], "folder": SIMS[q["sim"]]["folder"],
                   "time_unit": SIMS[q["sim"]]["time"],
                   "interventions": [pub_iv(i) for i in q["iv"]],
                   "outcome": pub_out(q["sim"], q["out"]), "question": q["text"]})
    with open(os.path.join(PUB, "questions.json"), "w") as f:
        json.dump({"quantile_levels": [0.05, 0.25, 0.5, 0.75, 0.95], "questions": qs}, f, indent=1)


if __name__ == "__main__":
    main()
