#!/usr/bin/env python3
"""Format check for a Patch Auditor answer file (says nothing about correctness).

    python3 check_answers.py ANSWERS.json
"""
import json
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "harness"))
import run_witness  # noqa: E402

REPOS = ["ledger", "ratelimit", "intervals", "pricing", "depgraph"]
IDS = ["%s/P%d" % (r, i) for r in REPOS for i in range(1, 5)]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    try:
        ans = json.load(open(sys.argv[1]))
    except (OSError, ValueError) as e:
        sys.exit("cannot read JSON: %s" % e)
    problems = []
    if not isinstance(ans, dict) or not isinstance(ans.get("patches"), dict):
        sys.exit("top level must be an object with a 'patches' object")
    if not isinstance(ans.get("solver"), str):
        problems.append("missing 'solver' label")
    pats = ans["patches"]
    for pid in pats:
        if pid not in IDS:
            problems.append("unknown patch id %r" % pid)
    flagged = 0
    for pid in IDS:
        a = pats.get(pid)
        if a is None:
            problems.append("%s: missing (would be scored as compliant)" % pid)
            continue
        v = a.get("verdict")
        if v not in ("violates", "compliant"):
            problems.append("%s: verdict must be 'violates' or 'compliant'" % pid)
        p = a.get("p_violates")
        if not isinstance(p, (int, float)) or isinstance(p, bool) or not 0 <= p <= 1:
            problems.append("%s: p_violates must be a number in [0, 1]" % pid)
        if v == "violates":
            flagged += 1
            w = a.get("witness")
            if w is None:
                problems.append("%s: 'violates' without a witness counts as a false positive" % pid)
                continue
            repo = pid.split("/")[0]
            out = run_witness.run(repo, os.path.join(HERE, "repos", repo), w)
            if out["error"]:
                problems.append("%s: witness rejected by driver: %s" % (pid, out["error"]))
        elif a.get("witness") not in (None,):
            problems.append("%s: witness given for a 'compliant' verdict (ignored)" % pid)
    print("%d patches flagged as violating (disclosed base rate: 6 of 20)" % flagged)
    if problems:
        print("\n".join("- " + p for p in problems))
        sys.exit(1)
    print("format OK")


if __name__ == "__main__":
    main()
