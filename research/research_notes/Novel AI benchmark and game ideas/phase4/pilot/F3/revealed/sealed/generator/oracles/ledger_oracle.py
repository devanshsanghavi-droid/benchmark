from common import Exps, Invalid, exact, is_int, is_name, nargs, need

HOUSE = "__house__"
AMT = 10 ** 9


def validate(ops):
    try:
        for op in ops:
            m, a = op[0], op[1:]
            if m == "open":
                nargs(op, 1, 2)
                need(is_name(a[0], 20), "name")
                need(len(a) == 1 or is_int(a[1], -AMT, AMT), "amount")
            elif m == "deposit":
                nargs(op, 2)
                need(is_name(a[0], 20) and is_int(a[1], -AMT, AMT), "args")
            elif m == "transfer":
                nargs(op, 3)
                need(is_name(a[0], 20) and is_name(a[1], 20) and is_int(a[2], -AMT, AMT), "args")
            elif m in ("split_fee", "fee_shares"):
                nargs(op, 2)
                need(isinstance(a[0], list) and len(a[0]) <= 20
                     and all(is_name(x, 20) for x in a[0]), "names")
                need(is_int(a[1], -AMT, AMT), "fee")
                if m == "fee_shares":
                    need(a[0] and len(set(a[0])) == len(a[0]) and a[1] >= 0,
                         "fee_shares only defined for valid inputs")
            elif m == "balance":
                nargs(op, 1)
                need(is_name(a[0], 20), "name")
            elif m in ("total", "history"):
                nargs(op, 0)
        return None
    except Invalid as e:
        return str(e)


def shares(names, fee):
    q, r = divmod(fee, len(names))
    return {n: q + (1 if i < r else 0) for i, n in enumerate(sorted(names))}


def expected(ops):
    bal = {HOUSE: 0}
    hist = []
    out = Exps()
    known = lambda n: n in bal and n != HOUSE  # noqa: E731
    for op in ops:
        m, a = op[0], op[1:]
        if m == "open":
            name, cents = a[0], (a[1] if len(a) > 1 else 0)
            if name == HOUSE or cents < 0 or name in bal:
                out.append(("exc", {"LedgerError"}))
            else:
                bal[name] = cents
                hist.append(["open", name, cents])
                out.append(("ok", None, exact))
        elif m == "deposit":
            name, cents = a
            if cents <= 0:
                out.append(("exc", {"LedgerError"}))
            elif not known(name):
                out.append(("exc", {"UnknownAccount"}))
            else:
                bal[name] += cents
                hist.append(["deposit", name, cents])
                out.append(("ok", None, exact))
        elif m == "transfer":
            src, dst, cents = a
            if cents <= 0 or src == dst:
                out.append(("exc", {"LedgerError"}))
            elif not known(src) or not known(dst):
                acc = {"UnknownAccount"}
                if known(src) and bal[src] < cents:
                    acc.add("InsufficientFunds")
                out.append(("exc", acc))
            elif bal[src] < cents:
                out.append(("exc", {"InsufficientFunds"}))
            else:
                bal[src] -= cents
                bal[dst] += cents
                hist.append(["transfer", src, dst, cents])
                out.append(("ok", None, exact))
        elif m == "split_fee":
            names, fee = a
            if fee < 0 or not names or len(set(names)) != len(names):
                out.append(("exc", {"LedgerError"}))
            elif not all(known(n) for n in names):
                out.append(("exc", {"UnknownAccount"}))
            else:
                sh = shares(names, fee)
                if any(bal[n] < s for n, s in sh.items()):
                    out.append(("exc", {"InsufficientFunds"}))
                else:
                    for n, s in sh.items():
                        bal[n] -= s
                    bal[HOUSE] += fee
                    hist.append(["fee", sorted(names), fee])
                    out.append(("ok", sh, exact))
        elif m == "fee_shares":
            out.append(("ok", shares(a[0], a[1]), exact))
        elif m == "balance":
            name = a[0]
            if name == HOUSE:
                out.append(("ok", bal[HOUSE], exact))
            elif not known(name):
                out.append(("exc", {"UnknownAccount"}))
            else:
                out.append(("ok", bal[name], exact))
        elif m == "total":
            out.append(("ok", sum(bal.values()), exact))
        elif m == "history":
            out.append(("ok", [list(h) for h in hist], exact))
    return out


def fuzz(rng):
    names = ["a", "b", "c", "d"]
    ops = [["open", n, rng.randint(0, 12)] for n in rng.sample(names, rng.randint(2, 4))]
    for _ in range(rng.randint(3, 14)):
        k = rng.random()
        if k < 0.35:
            ps = rng.sample(names, rng.randint(1, 4))
            ops.append(["split_fee", ps, rng.randint(0, 25)])
        elif k < 0.5:
            ops.append(["transfer", rng.choice(names + [HOUSE]), rng.choice(names + [HOUSE]), rng.randint(-1, 15)])
        elif k < 0.6:
            ops.append(["deposit", rng.choice(names), rng.randint(-1, 10)])
        elif k < 0.7:
            ops.append(["fee_shares", rng.sample(names, rng.randint(1, 4)), rng.randint(0, 25)])
        else:
            ops.append(rng.choice([["balance", rng.choice(names + [HOUSE])], ["total"], ["history"]]))
    ops += [["balance", n] for n in names] + [["history"]]
    return ops
