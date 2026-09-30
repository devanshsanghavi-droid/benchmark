"""Shared helpers for the sealed spec checkers.

Each repo oracle exposes:
  validate(ops) -> None or reason string (witness outside the spec's domain)
  expected(ops) -> list of expectations, one per op, computed from an
                   independent model of the spec (not from the base code)
  fuzz(rng)     -> random ops for certification / baselines
An expectation is ("ok", value, cmp) or ("exc", {acceptable class names}).
"""


class Invalid(Exception):
    pass


def is_int(x, lo=None, hi=None):
    if not isinstance(x, int) or isinstance(x, bool):
        return False
    if lo is not None and x < lo:
        return False
    if hi is not None and x > hi:
        return False
    return True


def is_name(x, maxlen):
    return isinstance(x, str) and 1 <= len(x) <= maxlen


def need(cond, why):
    if not cond:
        raise Invalid(why)


def nargs(op, *allowed):
    need(len(op) - 1 in allowed, "op %r: wrong number of arguments" % op[0])


def exact(a, b):
    return a == b


def as_set(a, b):
    return isinstance(a, list) and len(a) == len(set(map(repr, a))) and \
        sorted(a, key=repr) == sorted(b, key=repr)


def compare(ops, trace, exps):
    """Return a list of violation strings (empty if the trace obeys the spec).

    Checking stops at the first divergence because the model's state is no
    longer comparable after that point.
    """
    if len(trace) != len(ops):
        return ["trace length %d != ops %d" % (len(trace), len(ops))]
    for i, (op, got, exp) in enumerate(zip(ops, trace, exps)):
        if "args_after" in got and getattr(exps, "no_mutation", False):
            return ["op %d %s: mutated its arguments" % (i, op[0])]
        if exp[0] == "ok":
            if "ok" not in got:
                return ["op %d %s: expected a result, got exception %s" % (i, op[0], got.get("exc"))]
            if not exp[2](got["ok"], exp[1]):
                return ["op %d %s: expected %r, got %r" % (i, op[0], exp[1], got["ok"])]
        elif exp[0] == "exc":
            if "exc" not in got:
                return ["op %d %s: expected exception %s, got result %r"
                        % (i, op[0], sorted(exp[1]), got.get("ok"))]
            if not set(got.get("mro", [])) & exp[1]:
                return ["op %d %s: expected exception %s, got %s"
                        % (i, op[0], sorted(exp[1]), got["exc"])]
    return []


class Exps(list):
    no_mutation = False
