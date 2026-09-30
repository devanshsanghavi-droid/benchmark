#!/usr/bin/env python3
"""Generator for the F3 Patch Auditor pilot (sealed).

python3 build.py --seed N --public OUT/public --key OUT/key [--fuzz 1500]

Writes the public repos/specs/tests/patches, the answer key, patched trees,
reference answers, and runs certification (visible tests, reference
witnesses, differential fuzzing against the spec oracle).
"""
import argparse
import difflib
import json
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "oracles"))
sys.path.insert(0, os.path.join(HERE, "harness"))
sys.path.insert(0, HERE)

import check  # noqa: E402
import run_witness  # noqa: E402
from patches_r1r2 import PATCHES as P12  # noqa: E402
from patches_r3r5 import PATCHES as P35  # noqa: E402

REPOS = ["ledger", "ratelimit", "intervals", "pricing", "depgraph"]
PATCHES = P12 + P35


def apply_edits(src, edits):
    for old, new in edits:
        assert src.count(old) == 1, "edit anchor not unique: %r" % old[:60]
        src = src.replace(old, new)
    return src


def make_diff(repo, base, patched, msg):
    fn = repo + ".py"
    body = "".join(difflib.unified_diff(base.splitlines(True), patched.splitlines(True),
                                        "a/" + fn, "b/" + fn, n=3))
    return "Subject: %s\n\n%s" % (msg, body)


def run_tests(d):
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
                       cwd=d, capture_output=True, text=True, timeout=120)
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--public", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--fuzz", type=int, default=1500)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    key, ref = {}, {"solver": "reference", "patches": {}}
    cert = {"visible_tests": {}, "fuzz": {}, "reference_witness": {}}
    for repo in REPOS:
        tdir = os.path.join(HERE, "templates", repo)
        pub = os.path.join(a.public, "repos", repo)
        os.makedirs(os.path.join(pub, "tests"), exist_ok=True)
        os.makedirs(os.path.join(pub, "patches"), exist_ok=True)
        base = open(os.path.join(tdir, repo + ".py")).read()
        for f, dst in ((repo + ".py", repo + ".py"), ("SPEC.md", "SPEC.md"),
                       ("test_%s.py" % repo, "tests/test_%s.py" % repo)):
            shutil.copy(os.path.join(tdir, f), os.path.join(pub, dst))
        kb = os.path.join(a.key, "base", repo)
        os.makedirs(os.path.join(kb, "tests"), exist_ok=True)
        shutil.copy(os.path.join(tdir, repo + ".py"), kb)
        shutil.copy(os.path.join(tdir, "test_%s.py" % repo), os.path.join(kb, "tests"))
        cert["visible_tests"][repo + "/base"] = run_tests(kb)
        plist = [p for p in PATCHES if p["repo"] == repo]
        rng.shuffle(plist)
        for i, p in enumerate(plist, 1):
            pid = "%s/P%d" % (repo, i)
            patched = apply_edits(base, p["edits"])
            with open(os.path.join(pub, "patches", "P%d.diff" % i), "w") as f:
                f.write(make_diff(repo, base, patched, p["msg"]))
            kp = os.path.join(a.key, "patched", repo, "P%d" % i)
            os.makedirs(os.path.join(kp, "tests"), exist_ok=True)
            with open(os.path.join(kp, repo + ".py"), "w") as f:
                f.write(patched)
            shutil.copy(os.path.join(tdir, "test_%s.py" % repo), os.path.join(kp, "tests"))
            cert["visible_tests"][pid] = run_tests(kp)
            key[pid] = {k: p.get(k) for k in ("label", "key", "category", "rule", "witness", "msg")}
            v = p["label"] == "violates"
            ref["patches"][pid] = {"verdict": p["label"], "p_violates": 1.0 if v else 0.0,
                                   "witness": p.get("witness")}
            if v:
                br = run_witness.run(repo, kb, p["witness"])
                pr = run_witness.run(repo, kp, p["witness"])
                cert["reference_witness"][pid] = check.judge(repo, p["witness"], br, pr)
        # differential fuzzing against the spec oracle
        frng = random.Random(a.seed * 7919 + REPOS.index(repo))
        cases = [{"ops": check.oracle(repo).fuzz(frng)} for _ in range(a.fuzz)]
        mods = {"base": run_witness.load_module(repo, kb)}
        for i in range(1, len(plist) + 1):
            mods["P%d" % i] = run_witness.load_module(repo, os.path.join(a.key, "patched", repo, "P%d" % i))
        for name, mod in mods.items():
            bad = 0
            for w in cases:
                assert check.oracle(repo).validate(w["ops"]) is None, w
                tr = run_witness.run(repo, None, w, mod=mod)
                if check.violations(repo, w["ops"], tr["trace"]):
                    bad += 1
            cert["fuzz"]["%s/%s" % (repo, name)] = bad
    os.makedirs(a.key, exist_ok=True)
    json.dump(key, open(os.path.join(a.key, "key.json"), "w"), indent=1)
    json.dump(ref, open(os.path.join(a.key, "reference_answers.json"), "w"), indent=1)
    json.dump(cert, open(os.path.join(a.key, "certification.json"), "w"), indent=1, default=str)
    for sub in ("oracles", "harness"):
        dst = os.path.join(a.key, sub)
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(os.path.join(HERE, sub), dst,
                        ignore=shutil.ignore_patterns("__pycache__"))
    os.makedirs(os.path.join(a.public, "harness"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "harness", "run_witness.py"), os.path.join(a.public, "harness"))
    for f in ("INSTRUCTIONS.md", "score.py", "check_answers.py"):
        shutil.copy(os.path.join(HERE, f), os.path.join(a.public, f))
    with open(os.path.join(a.key, "seed.txt"), "w") as f:
        f.write("build seed: %d\nfuzz cases per module: %d\n" % (a.seed, a.fuzz))
    print(json.dumps(cert, indent=1, default=str))


if __name__ == "__main__":
    main()
