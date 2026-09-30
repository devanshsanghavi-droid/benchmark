from common import Exps, Invalid, as_set, exact, is_int, is_name, nargs, need

TMAX = 10 ** 9


def validate(ops):
    try:
        need(ops and ops[0][0] == "init", "first op must be init")
        for i, op in enumerate(ops):
            m, a = op[0], op[1:]
            if m == "init":
                need(i == 0, "init only first")
                nargs(op, 2)
                need(is_int(a[0], 1, 1000) and is_int(a[1], 1, 1000), "capacity/window")
            elif m in ("allow", "remaining", "retry_after"):
                nargs(op, 2)
                need(is_name(a[0], 20) and is_int(a[1], 0, TMAX), "args")
            elif m == "keys":
                nargs(op, 1)
                need(is_int(a[0], 0, TMAX), "time")
            elif m == "reset":
                nargs(op, 1)
                need(is_name(a[0], 20), "key")
        return None
    except Invalid as e:
        return str(e)


def expected(ops):
    out = Exps()
    cap = win = None
    rec = {}
    now = None

    def live(key, t):
        return sorted(s for s in rec.get(key, []) if t - win < s <= t)

    for op in ops:
        m, a = op[0], op[1:]
        if m == "init":
            cap, win = a
            out.append(("ok", None, exact))
            continue
        if m == "reset":
            rec.pop(a[0], None)
            out.append(("ok", None, exact))
            continue
        t = a[-1]
        if now is not None and t < now:
            out.append(("exc", {"ClockError"}))
            continue
        now = t
        if m == "allow":
            lv = live(a[0], t)
            if len(lv) < cap:
                rec.setdefault(a[0], []).append(t)
                out.append(("ok", True, exact))
            else:
                out.append(("ok", False, exact))
        elif m == "remaining":
            out.append(("ok", cap - len(live(a[0], t)), exact))
        elif m == "retry_after":
            lv = live(a[0], t)
            if len(lv) < cap:
                d = 0
            else:
                d = max(0, lv[len(lv) - cap] + win - t)
            out.append(("ok", d, exact))
        elif m == "keys":
            ks = [k for k in rec if live(k, t)]
            out.append(("ok", ks, as_set))
    return out


def fuzz(rng):
    ops = [["init", rng.randint(1, 3), rng.randint(1, 6)]]
    t = rng.randint(0, 5)
    keys = ["k", "j"]
    for _ in range(rng.randint(4, 24)):
        t += rng.choice([0, 0, 1, 1, 2, 3, 5])
        tt = t if rng.random() > 0.05 else max(0, t - 2)
        k = rng.random()
        if k < 0.55:
            ops.append(["allow", rng.choice(keys), tt])
        elif k < 0.7:
            ops.append(["remaining", rng.choice(keys), tt])
        elif k < 0.82:
            ops.append(["retry_after", rng.choice(keys), tt])
        elif k < 0.94:
            ops.append(["keys", tt])
        else:
            ops.append(["reset", rng.choice(keys)])
    return ops
