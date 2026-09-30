from common import Exps, Invalid, exact, is_int, nargs, need

COUPONS = {"SAVE5": (5000, 500), "SAVE20": (20000, 2000)}
BIG = 10 ** 9


def _cart_ok(cart):
    if not isinstance(cart, list) or len(cart) > 20:
        return False
    for ln in cart:
        if not (isinstance(ln, list) and len(ln) == 3 and isinstance(ln[0], str)
                and len(ln[0]) <= 20 and is_int(ln[1], -10 ** 6, 10 ** 6)
                and is_int(ln[2], -1000, 1000)):
            return False
    return True


def validate(ops):
    try:
        for op in ops:
            m, a = op[0], op[1:]
            if m == "checkout":
                nargs(op, 1, 2)
                need(_cart_ok(a[0]), "cart outside domain")
                need(len(a) == 1 or a[1] is None or (isinstance(a[1], str) and len(a[1]) <= 20),
                     "coupon")
            elif m == "line_total":
                nargs(op, 2)
                need(is_int(a[0], 0, 10 ** 6) and is_int(a[1], 1, 1000),
                     "line_total defined for unit_price>=0, qty>=1")
            elif m == "tax_on":
                nargs(op, 1)
                need(is_int(a[0], 0, BIG), "tax_on defined for amount>=0")
            elif m == "split_payment":
                nargs(op, 2)
                need(is_int(a[0], 0, BIG) and is_int(a[1], -1000, 1000), "split_payment args")
        return None
    except Invalid as e:
        return str(e)


def line_disc(p, q):
    return (p * q * 10) // 100 if q >= 10 else 0


def tax(x):
    return (x * 825 + 5000) // 10000


def checkout(cart, coupon):
    skus = [ln[0] for ln in cart]
    if not cart or len(set(skus)) != len(skus) or any(p < 0 or q < 1 for _, p, q in cart):
        return None
    if coupon is not None and coupon not in COUPONS:
        return None
    sub = sum(p * q for _, p, q in cart)
    disc = sum(line_disc(p, q) for _, p, q in cart)
    off = 0
    if coupon is not None and sub - disc >= COUPONS[coupon][0]:
        off = COUPONS[coupon][1]
    net = sub - disc - off
    ship = 0 if net >= 5000 else 599
    tx = tax(net)
    return {"subtotal": sub, "discount": disc, "coupon": off, "net": net, "tax": tx,
            "shipping": ship, "total": net + tx + ship}


def expected(ops):
    out = Exps()
    out.no_mutation = True
    for op in ops:
        m, a = op[0], op[1:]
        if m == "checkout":
            r = checkout(a[0], a[1] if len(a) > 1 else None)
            out.append(("exc", {"PricingError"}) if r is None else ("ok", r, exact))
        elif m == "line_total":
            out.append(("ok", a[0] * a[1] - line_disc(a[0], a[1]), exact))
        elif m == "tax_on":
            out.append(("ok", tax(a[0]), exact))
        elif m == "split_payment":
            t, n = a
            if n < 1:
                out.append(("exc", {"PricingError"}))
            else:
                q, r = divmod(t, n)
                out.append(("ok", [q + 1] * r + [q] * (n - r), exact))
    return out


def fuzz(rng):
    ops = []
    for _ in range(rng.randint(1, 6)):
        k = rng.random()
        if k < 0.6:
            cart = []
            for i in range(rng.randint(1, 3)):
                cart.append(["s%d" % i, rng.choice([rng.randint(0, 999), rng.randint(0, 9000)]),
                             rng.choice([1, 2, 3, 9, 10, 11, 12, 15, 20, 25])])
            ops.append(["checkout", cart, rng.choice([None, None, "SAVE5", "SAVE20", "BOGUS"])])
        elif k < 0.75:
            ops.append(["line_total", rng.randint(0, 999), rng.randint(1, 30)])
        elif k < 0.9:
            ops.append(["tax_on", rng.randint(0, 20000)])
        else:
            ops.append(["split_payment", rng.randint(0, 5000), rng.randint(0, 7)])
    return ops
