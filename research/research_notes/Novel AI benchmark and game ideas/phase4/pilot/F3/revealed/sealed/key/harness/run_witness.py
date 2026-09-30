#!/usr/bin/env python3
"""Execute a witness against one copy of a repo and print the trace as JSON.

Usage:
  python3 run_witness.py --repo ledger --src PATH/TO/REPO_DIR --witness w.json
  python3 run_witness.py --repo ledger --src PATH/TO/REPO_DIR --witness-json '{"ops": [...]}'

PATH/TO/REPO_DIR is the directory holding the module file (e.g. ledger.py).
The trace has one entry per operation: {"ok": result} or
{"exc": class_name, "mro": [class names], "msg": message}.
This tool only executes; it does not judge whether a trace obeys the spec.
"""
import argparse
import copy
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True

REPOS = {
    "ledger": {"module": "ledger", "cls": "Ledger", "max_ops": 60,
               "methods": ["open", "deposit", "transfer", "split_fee", "fee_shares",
                           "balance", "total", "history"]},
    "ratelimit": {"module": "ratelimit", "cls": "Limiter", "max_ops": 60, "init_op": True,
                  "methods": ["allow", "remaining", "retry_after", "keys", "reset"]},
    "intervals": {"module": "intervals", "cls": "IntervalSet", "max_ops": 60,
                  "methods": ["add", "remove", "contains", "intervals", "measure", "gaps",
                              "overlaps"]},
    "pricing": {"module": "pricing", "cls": None, "max_ops": 20,
                "methods": ["checkout", "line_total", "tax_on", "split_payment"]},
    "depgraph": {"module": "depgraph", "cls": "DepGraph", "max_ops": 60,
                 "methods": ["add", "remove", "nodes", "deps_of", "order", "layers",
                             "affected"]},
}


def to_json(v, depth=0):
    if depth > 50:
        return {"__repr__": "<too deep>"}
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    if isinstance(v, (list, tuple)):
        return [to_json(x, depth + 1) for x in v]
    if isinstance(v, dict):
        return {str(k): to_json(x, depth + 1) for k, x in v.items()}
    if isinstance(v, (set, frozenset)):
        return {"__set__": sorted((to_json(x, depth + 1) for x in v), key=repr)}
    return {"__repr__": repr(v)[:200]}


def exc_entry(e):
    return {"exc": type(e).__name__, "mro": [c.__name__ for c in type(e).__mro__],
            "msg": str(e)[:200]}


def check_shape(repo, witness):
    cfg = REPOS[repo]
    if not isinstance(witness, dict) or not isinstance(witness.get("ops"), list):
        return "witness must be an object with an 'ops' list"
    ops = witness["ops"]
    if not ops or len(ops) > cfg["max_ops"]:
        return "ops must hold 1..%d operations" % cfg["max_ops"]
    for i, op in enumerate(ops):
        if not isinstance(op, list) or not op or not isinstance(op[0], str):
            return "op %d must be a non-empty list starting with a method name" % i
        allowed = cfg["methods"] + (["init"] if cfg.get("init_op") and i == 0 else [])
        if op[0] not in allowed:
            return "op %d: method %r not allowed here" % (i, op[0])
    if cfg.get("init_op") and ops[0][0] != "init":
        return "first op must be init"
    return None


def load_module(repo, src):
    cfg = REPOS[repo]
    path = os.path.join(src, cfg["module"] + ".py")
    spec = importlib.util.spec_from_file_location("_audited_" + cfg["module"], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(repo, src, witness, mod=None):
    err = check_shape(repo, witness)
    if err:
        return {"error": err, "trace": []}
    cfg = REPOS[repo]
    if mod is None:
        mod = load_module(repo, src)
    obj = mod if cfg["cls"] is None else None
    trace = []
    for i, op in enumerate(witness["ops"]):
        name, args = op[0], copy.deepcopy(op[1:])
        before = copy.deepcopy(args)
        try:
            if name == "init":
                obj = getattr(mod, cfg["cls"])(*args)
                res = None
            else:
                if obj is None:
                    obj = getattr(mod, cfg["cls"])()
                res = getattr(obj, name)(*args)
            entry = {"ok": to_json(res)}
        except Exception as e:  # recorded, execution continues
            entry = exc_entry(e)
        if to_json(args) != to_json(before):
            entry["args_after"] = to_json(args)
        trace.append(entry)
    return {"error": None, "trace": trace}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, choices=sorted(REPOS))
    ap.add_argument("--src", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--witness")
    g.add_argument("--witness-json")
    a = ap.parse_args()
    if a.witness:
        with open(a.witness) as f:
            witness = json.load(f)
    else:
        witness = json.loads(a.witness_json)
    sys.setrecursionlimit(5000)
    out = run(a.repo, a.src, witness)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
