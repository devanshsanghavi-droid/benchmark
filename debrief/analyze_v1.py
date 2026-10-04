"""Post-hoc analysis of DEBRIEF pilot v1 (L4-L5 parcel tariffs, Haiku junior, four Claude coaches).

Writes results/pilot_v1/analysis.json and prints a summary. Two analyses:
  raw      - every run, every item cell (the pre-specified analysis);
  screened - POST HOC: drops (run, item) cells that show a harness artefact. Items k and k+3 share a seed, so the
             L4 and L5 tariffs are near-identical twins and junior agents that read all six prompts in one context
             sometimes applied the twin's amendments or wrote the twin's answers. A cell is dropped when the reply
             answers case ids the item does not have, or when >= 2 of its errors equal the twin tariff's price.
Usage: python -m debrief.analyze_v1 --keys KEYDIR
"""
import argparse
import json
import os
import random
import statistics

from . import pilot
from .core import diagnose, nfr, parse_answers, price

TWIN = {1: 4, 2: 5, 3: 6, 4: 1, 5: 2, 6: 3}
COACHES = ["haiku", "sonnet", "opus", "fable"]


def cells(keys):
    pilot.ROOT = pilot.ROOT.replace("pilot_v0", "pilot_v1")
    items = {k: pilot.load_item(keys, k) for k in range(1, 7)}
    out = {}
    for st in sorted(os.listdir(os.path.join(pilot.ROOT, "replies"))):
        if st.startswith("coach_") or st == "practice":
            continue
        out[st] = {}
        for k, it in items.items():
            a = parse_answers(open(os.path.join(pilot.ROOT, "replies", st, f"item_{k}.txt")).read())
            ids = {c.cid for c in it.fresh}
            corr = [1.0 if a.get(c.cid) == it.fresh_key[c.cid] else 0.0 for c in it.fresh]
            twin = items[TWIN[k]].system
            twin_errs = sum(1 for c in it.fresh if a.get(c.cid) != it.fresh_key[c.cid] and a.get(c.cid) == price(twin, c))
            flagged = bool(set(a) - ids) or twin_errs >= 2
            out[st][k] = {"corr": corr, "flagged": flagged, "twin_errors": twin_errs}
    return items, out


def arm_rows(c, names, keep):
    """Per-item correctness averaged over the given replicate runs, using only unflagged cells (if keep)."""
    rows = {}
    for k in range(1, 7):
        runs = [c[n][k]["corr"] for n in names if n in c and (not keep or not c[n][k]["flagged"])]
        if runs:
            rows[k] = [statistics.mean(x) for x in zip(*runs)]
    return rows


def nfr_on(ctrl, post, ks):
    return nfr([ctrl[k] for k in ks], [post[k] for k in ks])


def boot(ctrl, post, ks, B=4000, seed=1):
    r = random.Random(seed)
    v = []
    for _ in range(B):
        s = [r.choice(ks) for _ in ks]
        x = nfr_on(ctrl, post, s)
        if x == x:
            v.append(x)
    v.sort()
    return v[int(0.025 * len(v))], v[int(0.975 * len(v)) - 1]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", required=True)
    a = ap.parse_args(argv)
    items, c = cells(a.keys)
    res = {"flagged_cells": {st: [k for k, v in d.items() if v["flagged"]] for st, d in c.items()}}
    for mode, keep in (("raw", False), ("screened", True)):
        ctrl = arm_rows(c, ["control_r1", "control_r2"], keep)
        arms = {"placebo": ["placebo"], "template": ["template"]}
        arms.update({f"coach_{m}": [f"post_{m}", f"post_{m}_r2"] for m in COACHES})
        arms.update({f"coach_{m}_r1": [f"post_{m}"] for m in COACHES})
        arms.update({f"coach_{m}_r2": [f"post_{m}_r2"] for m in COACHES})
        tab = {}
        for arm, names in arms.items():
            post = arm_rows(c, names, keep)
            ks = sorted(set(ctrl) & set(post))
            n_err = sum(1 - x for k in ks for x in ctrl[k])
            acc = sum(map(sum, (post[k] for k in ks))) / sum(len(post[k]) for k in ks)
            tab[arm] = {"items": len(ks), "control_errors": round(n_err, 1), "accuracy": round(acc, 3),
                        "NFR": round(nfr_on(ctrl, post, ks), 1), "CI95": [round(x, 1) for x in boot(ctrl, post, ks)]}
        ks = sorted(ctrl)
        tab["_control_accuracy"] = round(sum(map(sum, (ctrl[k] for k in ks))) / sum(len(ctrl[k]) for k in ks), 3)
        r1, r2 = arm_rows(c, ["control_r1"], keep), arm_rows(c, ["control_r2"], keep)
        ks2 = sorted(set(r1) & set(r2))
        tab["_noise_floor_NFR_r2_vs_r1"] = round(nfr_on(r1, r2, ks2), 1)
        res[mode] = tab
    # practice diagnosability, pre-registered library vs with the coach-discovered misconception
    pr = {"library": 0, "with_posthoc": 0, "errors": 0}
    for k, it in items.items():
        ans = parse_answers(open(os.path.join(pilot.ROOT, "replies", "practice", f"item_{k}.txt")).read())
        _, _, l1 = diagnose(it, ans)
        _, _, l2 = diagnose(it, ans, posthoc=True)
        pr["errors"] += sum(v != "correct" for v in l1.values())
        pr["library"] += sum(v == "diagnosable" for v in l1.values())
        pr["with_posthoc"] += sum(v == "diagnosable" for v in l2.values())
    res["practice_diagnosability"] = pr
    json.dump(res, open(os.path.join(pilot.ROOT, "analysis.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
