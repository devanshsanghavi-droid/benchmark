#!/usr/bin/env python3
"""Scorer for the F2 Hidden-Rule Lab static pilot. This file contains no answers.

Usage:
    python3 score.py KEY_DIR ANSWERS_DIR [--show-rules] [--json OUT.json]

KEY_DIR      directory holding key.json (found in the decrypted sealed archive, under sealed/key/).
             key.json format: {"format": "f2-pilot-key-v1", "problems": {"P1": ["Y"|"N", x8], ...}}
ANSWERS_DIR  directory of solver answer files <SOLVER_LABEL>.json (schema in INSTRUCTIONS.md).

Scoring: each test panel is worth 1 point if the solver's label matches the key. A missing,
malformed or non-Y/N label scores 0. The per-problem rule sentence is recorded but not scored.
Reported per solver: per-problem correct/8, overall accuracy (pooled over all test labels),
problems fully correct (8/8), a 95% bootstrap CI over problems, and the count of invalid labels.
"""
import sys, os, json, glob, random, argparse

NORMALISE = {"Y": "Y", "YES": "Y", "FITS": "Y", "FIT": "Y", "TRUE": "Y",
             "N": "N", "NO": "N", "NOT": "N", "DOES NOT FIT": "N", "FALSE": "N"}


def norm(v):
    if isinstance(v, bool):
        return "Y" if v else "N"
    if isinstance(v, str):
        return NORMALISE.get(v.strip().upper())
    return None


def load_key(key_dir):
    with open(os.path.join(key_dir, "key.json")) as f:
        k = json.load(f)
    return k["problems"]


def score_file(path, key):
    res = {"file": os.path.basename(path), "per_problem": {}, "invalid": 0, "error": None, "rules": {}}
    try:
        with open(path) as f:
            ans = json.load(f)
        probs = ans.get("problems", {})
        res["label"] = str(ans.get("solver_label", os.path.splitext(os.path.basename(path))[0]))
    except Exception as e:  # unreadable file: every label counts as wrong
        probs, res["error"] = {}, f"{type(e).__name__}: {e}"
        res["label"] = os.path.splitext(os.path.basename(path))[0]
    for pid, truth in key.items():
        entry = probs.get(pid, {}) if isinstance(probs, dict) else {}
        labels = entry.get("labels", []) if isinstance(entry, dict) else []
        if not isinstance(labels, list):
            labels = []
        correct = 0
        for i, t in enumerate(truth):
            v = norm(labels[i]) if i < len(labels) else None
            if v is None:
                res["invalid"] += 1
            elif v == t:
                correct += 1
        res["per_problem"][pid] = correct
        res["rules"][pid] = entry.get("rule", "") if isinstance(entry, dict) else ""
    n = sum(len(t) for t in key.values())
    res["correct"] = sum(res["per_problem"].values())
    res["n"] = n
    res["accuracy"] = res["correct"] / n
    res["fully_correct"] = sum(res["per_problem"][p] == len(key[p]) for p in key)
    # 95% bootstrap CI over problems (ratio of pooled totals)
    rng = random.Random(0)
    pids = list(key)
    stats = []
    for _ in range(10000):
        s = [rng.choice(pids) for _ in pids]
        stats.append(sum(res["per_problem"][p] for p in s) / sum(len(key[p]) for p in s))
    stats.sort()
    res["ci95"] = (stats[249], stats[9749])
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("key_dir"); ap.add_argument("answers_dir")
    ap.add_argument("--show-rules", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    key = load_key(a.key_dir)
    files = sorted(glob.glob(os.path.join(a.answers_dir, "*.json")))
    if not files:
        sys.exit(f"no *.json answer files in {a.answers_dir}")
    results = [score_file(f, key) for f in files]
    pids = list(key)
    head = f"{'solver':<18}" + "".join(f"{p:>5}" for p in pids) + f"{'total':>9}{'acc':>8}{'95% CI':>15}{'8/8':>5}{'inval':>6}"
    print(head); print("-" * len(head))
    for r in results:
        row = f"{r['label'][:18]:<18}" + "".join(f"{r['per_problem'][p]:>5}" for p in pids)
        row += f"{r['correct']:>5}/{r['n']:<3}{100*r['accuracy']:>7.1f}%"
        row += f"  [{100*r['ci95'][0]:4.1f},{100*r['ci95'][1]:5.1f}]{r['fully_correct']:>5}{r['invalid']:>6}"
        print(row)
        if r["error"]:
            print(f"    !! {r['file']}: {r['error']}")
    print(f"\nper-problem columns: correct test labels out of {len(key[pids[0]])}; "
          f"'8/8' = problems with every test label correct; 'inval' = missing/invalid labels (scored wrong).")
    if a.show_rules:
        for r in results:
            print(f"\n== {r['label']} stated rules (not scored)")
            for p in pids:
                print(f"  {p} [{r['per_problem'][p]}/{len(key[p])}]: {r['rules'][p]}")
    if a.json:
        with open(a.json, "w") as f:
            json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
