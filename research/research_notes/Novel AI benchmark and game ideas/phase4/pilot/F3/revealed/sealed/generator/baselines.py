#!/usr/bin/env python3
"""Write baseline answer files for validation (sealed).

python3 baselines.py --public PUBLIC --key KEY --out ANSWERS_DIR --seed N
"""
import argparse
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "oracles"))
sys.path.insert(0, os.path.join(HERE, "harness"))
import check  # noqa: E402
import run_witness  # noqa: E402

EXAMPLE = re.compile(r"Example: `(\{.*\})`")


def strip(tr):
    return [{k: v for k, v in e.items() if k not in ("msg", "mro")} for e in tr]


def diff_fuzz(repo, base_mod, pat_mod, rng, n):
    """Naive differential tester: flag any observable difference (messages ignored)."""
    for _ in range(n):
        ops = check.oracle(repo).fuzz(rng)
        w = {"ops": ops}
        tb = strip(run_witness.run(repo, None, w, mod=base_mod)["trace"])
        tp = strip(run_witness.run(repo, None, w, mod=pat_mod)["trace"])
        if tb != tp:
            i = next(j for j, (x, y) in enumerate(zip(tb, tp)) if x != y)
            return {"ops": ops[:i + 1]}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--fuzz", type=int, default=2000)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    key = json.load(open(os.path.join(a.key, "key.json")))
    pids = sorted(key)
    rng = random.Random(a.seed)
    out = {}
    out["reference"] = json.load(open(os.path.join(a.key, "reference_answers.json")))
    out["do_nothing"] = {"patches": {p: {"verdict": "compliant", "p_violates": 0.0} for p in pids}}
    out["all_violates_no_witness"] = {"patches": {p: {"verdict": "violates", "p_violates": 1.0,
                                                      "witness": None} for p in pids}}
    ex = {}
    for repo in {p.split("/")[0] for p in pids}:
        spec = open(os.path.join(a.public, "repos", repo, "SPEC.md")).read()
        ex[repo] = json.loads(EXAMPLE.search(spec).group(1))
    out["all_violates_example_witness"] = {"patches": {p: {
        "verdict": "violates", "p_violates": 1.0, "witness": ex[p.split("/")[0]]} for p in pids}}
    rnd = {}
    for p in pids:
        repo = p.split("/")[0]
        flag = rng.random() < 0.3
        rnd[p] = {"verdict": "violates" if flag else "compliant", "p_violates": rng.random(),
                  "witness": {"ops": check.oracle(repo).fuzz(rng)} if flag else None}
    out["random_30pct_fuzz_witness"] = {"patches": rnd}
    # diff-text heuristic: more changed lines -> more suspicious; flag top 30 %, no witness
    size = {}
    for p in pids:
        repo, pn = p.split("/")
        d = open(os.path.join(a.public, "repos", repo, "patches", pn + ".diff")).read()
        size[p] = sum(1 for ln in d.splitlines() if ln[:1] in "+-" and ln[:3] not in ("+++", "---"))
    top = sorted(pids, key=lambda p: -size[p])[:round(0.3 * len(pids))]
    mx = max(size.values())
    out["diff_size_heuristic"] = {"patches": {p: {
        "verdict": "violates" if p in top else "compliant", "p_violates": size[p] / mx,
        "witness": None} for p in pids}}
    # naive differential fuzzing (owner's input generators; upper bound for this strategy)
    df = {}
    for p in pids:
        repo, pn = p.split("/")
        bm = run_witness.load_module(repo, os.path.join(a.key, "base", repo))
        pm = run_witness.load_module(repo, os.path.join(a.key, "patched", repo, pn))
        w = diff_fuzz(repo, bm, pm, random.Random(rng.random()), a.fuzz)
        df[p] = {"verdict": "violates" if w else "compliant", "p_violates": 1.0 if w else 0.0,
                 "witness": w}
    out["naive_differential_fuzzer"] = {"patches": df}
    for name, ans in out.items():
        ans["solver"] = name
        json.dump(ans, open(os.path.join(a.out, name + ".json"), "w"))
    print("wrote", sorted(out))


if __name__ == "__main__":
    main()
