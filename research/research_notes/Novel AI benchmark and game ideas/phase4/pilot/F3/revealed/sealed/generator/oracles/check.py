"""Sealed judge: decides whether a witness demonstrates a spec violation."""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import compare  # noqa: E402


def oracle(repo):
    return importlib.import_module(repo + "_oracle")


def violations(repo, ops, trace):
    o = oracle(repo)
    return compare(ops, trace, o.expected(ops))


def judge(repo, witness, base_run, patched_run):
    """Return (confirmed: bool, reason: str)."""
    o = oracle(repo)
    ops = witness.get("ops") if isinstance(witness, dict) else None
    if base_run.get("error") or patched_run.get("error"):
        return False, "malformed witness: %s" % (base_run.get("error") or patched_run.get("error"))
    why = o.validate(ops)
    if why:
        return False, "witness outside spec domain: " + why
    if patched_run.get("timeout") or base_run.get("timeout"):
        return False, "timeout"
    vb = compare(ops, base_run["trace"], o.expected(ops))
    if vb:
        return False, "base also violates (oracle problem): " + vb[0]
    vp = compare(ops, patched_run["trace"], o.expected(ops))
    if not vp:
        return False, "patched code obeys the spec on this witness"
    return True, vp[0]
