#!/usr/bin/env python3
"""Scorer for the F3 Patch Auditor pilot.

    python3 score.py --key DECRYPTED/key --answers ANSWERS_DIR [--per-patch]

The key directory (sealed) holds key.json, the base and patched source trees,
the spec oracles and the witness driver. This file contains no answers.

For every patch a solver marks "violates", its witness is executed in a
separate process (timeout, CPU and memory limits) against the base code and
the patched code. The sealed spec oracle confirms the witness only if the
witness is inside the spec's domain, the base code obeys the spec on it, and
the patched code breaks the spec on it.

Counts over the 20 patches (V = number of spec-violating patches):
  TP  = patches flagged "violates" whose witness is confirmed
  FP  = patches flagged "violates" whose witness is missing or not confirmed
  FN  = violating patches without a confirmed witness
  precision P = TP / (TP + FP)  (0 if nothing is flagged)
  recall    R = TP / V
  headline  PWR (precision-weighted recall) = P * R
Secondary: F1; witnessed recall at zero benign flags (the pilot-size analogue of
the spec's recall at 5% FPR: a violating patch counts only if its witness is
confirmed and its p_violates is strictly above every compliant patch's);
AUROC and Brier score of p_violates; unwitnessed verdict accuracy.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

TIMEOUT = 10
MAX_WITNESS_BYTES = 20000


def limits():
    import resource
    resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT, TIMEOUT))
    resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1 << 20, 1 << 20))


def execute(keydir, repo, src, witness):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(witness, f)
        wpath = f.name
    try:
        r = subprocess.run([sys.executable, "-I", os.path.join(keydir, "harness", "run_witness.py"),
                            "--repo", repo, "--src", src, "--witness", wpath],
                           capture_output=True, text=True, timeout=TIMEOUT,
                           preexec_fn=limits, cwd=tempfile.gettempdir())
        if r.returncode != 0:
            return {"error": "driver failed: " + r.stderr.strip()[-200:], "trace": []}
        return json.loads(r.stdout)
    except subprocess.TimeoutExpired:
        return {"error": None, "timeout": True, "trace": []}
    except ValueError:
        return {"error": "unreadable driver output", "trace": []}
    finally:
        os.unlink(wpath)


def auroc(pos, neg):
    if not pos or not neg:
        return float("nan")
    s = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg)
    return s / (len(pos) * len(neg))


def score_one(keydir, key, ans, judge):
    rows, disputes = {}, []
    patches = ans.get("patches", {}) if isinstance(ans, dict) else {}
    for pid, k in sorted(key.items()):
        a = patches.get(pid) or {}
        verdict = a.get("verdict", "compliant")
        p = a.get("p_violates")
        if not isinstance(p, (int, float)) or isinstance(p, bool) or not 0 <= p <= 1:
            p = 1.0 if verdict == "violates" else 0.0
        truth = k["label"] == "violates"
        confirmed, why = False, "not flagged"
        if verdict == "violates":
            w = a.get("witness")
            if w is None:
                why = "no witness"
            elif len(json.dumps(w)) > MAX_WITNESS_BYTES:
                why = "witness too large"
            else:
                repo, pn = pid.split("/")
                br = execute(keydir, repo, os.path.join(keydir, "base", repo), w)
                pr = execute(keydir, repo, os.path.join(keydir, "patched", repo, pn), w)
                confirmed, why = judge(repo, w, br, pr)
            if confirmed and not truth:
                disputes.append(pid)
        rows[pid] = dict(truth=truth or confirmed, flag=verdict == "violates", ok=confirmed, p=float(p), why=why)
    tp = sum(r["ok"] for r in rows.values())
    fp = sum(r["flag"] and not r["ok"] for r in rows.values())
    v = sum(r["truth"] for r in rows.values())
    fn = v - tp
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / v if v else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    neg = [r["p"] for r in rows.values() if not r["truth"]]
    pos = [r["p"] for r in rows.values() if r["truth"]]
    thr = max(neg) if neg else -1
    wr0 = sum(1 for r in rows.values() if r["truth"] and r["ok"] and r["p"] > thr) / v if v else 0.0
    brier = sum((r["p"] - r["truth"]) ** 2 for r in rows.values()) / len(rows)
    acc = sum(r["flag"] == r["truth"] for r in rows.values()) / len(rows)
    return dict(TP=tp, FP=fp, FN=fn, V=v, precision=prec, recall=rec, PWR=prec * rec, F1=f1,
                wrecall_at_0FP=wr0, AUROC=auroc(pos, neg), Brier=brier, verdict_acc=acc,
                label_disputes=disputes), rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--per-patch", action="store_true", help="also print per-patch outcomes")
    ap.add_argument("--json", help="write results to this file")
    a = ap.parse_args()
    keydir = os.path.abspath(a.key)
    sys.path.insert(0, os.path.join(keydir, "oracles"))
    from check import judge
    key = json.load(open(os.path.join(keydir, "key.json")))
    results = {}
    cols = ["TP", "FP", "FN", "precision", "recall", "PWR", "F1", "wrecall_at_0FP", "AUROC",
            "Brier", "verdict_acc"]
    print("%-22s " % "solver" + " ".join("%9s" % c[:9] for c in cols))
    for path in sorted(glob.glob(os.path.join(a.answers, "*.json"))):
        label = os.path.splitext(os.path.basename(path))[0]
        try:
            ans = json.load(open(path))
        except ValueError:
            ans = {}
            print("%s: unreadable JSON, scored as empty" % label)
        res, rows = score_one(keydir, key, ans, judge)
        results[label] = res
        print("%-22s " % label[:22] + " ".join(
            "%9d" % res[c] if isinstance(res[c], int) else "%9.3f" % res[c] for c in cols))
        if res["label_disputes"]:
            print("   label disputes (confirmed witness on a patch keyed compliant):", res["label_disputes"])
        if a.per_patch:
            for pid, r in rows.items():
                code = ("TP" if r["ok"] else "FP") if r["flag"] else ("FN" if r["truth"] else "TN")
                print("   %-14s %s p=%.2f  %s" % (pid, code, r["p"], r["why"][:110]))
    if a.json:
        json.dump(results, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
