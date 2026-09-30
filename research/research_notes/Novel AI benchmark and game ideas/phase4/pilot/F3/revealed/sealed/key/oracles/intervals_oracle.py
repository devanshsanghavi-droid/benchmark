from common import Exps, Invalid, exact, is_int, nargs, need

LIM = 1000


def validate(ops):
    try:
        for op in ops:
            m, a = op[0], op[1:]
            if m in ("add", "remove", "gaps", "overlaps"):
                nargs(op, 2)
            elif m == "contains":
                nargs(op, 1)
            else:
                nargs(op, 0)
            need(all(is_int(x, -LIM, LIM) for x in a), "ints in -1000..1000")
        return None
    except Invalid as e:
        return str(e)


def canon(points):
    out = []
    for x in sorted(points):
        if out and out[-1][1] == x:
            out[-1][1] = x + 1
        else:
            out.append([x, x + 1])
    return out


def expected(ops):
    S = set()
    out = Exps()
    for op in ops:
        m, a = op[0], op[1:]
        if m in ("add", "remove", "gaps", "overlaps") and a[0] > a[1]:
            out.append(("exc", {"ValueError"}))
        elif m == "add":
            S |= set(range(a[0], a[1]))
            out.append(("ok", None, exact))
        elif m == "remove":
            S -= set(range(a[0], a[1]))
            out.append(("ok", None, exact))
        elif m == "contains":
            out.append(("ok", a[0] in S, exact))
        elif m == "intervals":
            out.append(("ok", canon(S), exact))
        elif m == "measure":
            out.append(("ok", len(S), exact))
        elif m == "gaps":
            out.append(("ok", canon(set(range(a[0], a[1])) - S), exact))
        elif m == "overlaps":
            out.append(("ok", any(x in S for x in range(a[0], a[1])), exact))
    return out


def fuzz(rng):
    ops = []
    for _ in range(rng.randint(3, 16)):
        k = rng.random()
        lo = rng.randint(-12, 12)
        hi = lo + rng.randint(-1, 9)
        if k < 0.4:
            ops.append(["add", lo, hi])
        elif k < 0.65:
            ops.append(["remove", lo, hi])
        elif k < 0.75:
            ops.append(["contains", rng.randint(-12, 14)])
        elif k < 0.85:
            ops.append(["gaps", lo, hi])
        elif k < 0.95:
            ops.append(["overlaps", lo, hi])
        else:
            ops.append(["measure"])
    ops.append(["intervals"])
    return ops
