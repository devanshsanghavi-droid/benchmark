"""Checkout pricing for a small shop. All money is in integer cents."""

TAX_BP = 825            # 8.25 % expressed in basis points
BULK_QTY = 10           # lines with at least this many units get a discount
BULK_PCT = 10           # percent off such lines
COUPONS = {"SAVE5": (5000, 500), "SAVE20": (20000, 2000)}  # code -> (minimum, amount)
FREE_SHIP_MIN = 5000
SHIPPING = 599


class PricingError(ValueError):
    pass


def _validate(cart):
    if not isinstance(cart, list) or not cart:
        raise PricingError("cart must be a non-empty list")
    seen = set()
    for line in cart:
        sku, price, qty = line
        if sku in seen:
            raise PricingError("duplicate sku")
        seen.add(sku)
        if price < 0 or qty < 1:
            raise PricingError("bad line")


def line_total(price, qty):
    gross = price * qty
    if qty >= BULK_QTY:
        return gross - gross * BULK_PCT // 100
    return gross


def tax_on(amount):
    return (amount * TAX_BP + 5000) // 10000


def checkout(cart, coupon=None):
    _validate(cart)
    subtotal = sum(price * qty for _, price, qty in cart)
    after_bulk = sum(line_total(price, qty) for _, price, qty in cart)
    discount = subtotal - after_bulk
    coupon_off = 0
    if coupon is not None:
        if coupon not in COUPONS:
            raise PricingError("unknown coupon")
        minimum, amount = COUPONS[coupon]
        if after_bulk >= minimum:
            coupon_off = max(0, min(amount, after_bulk))
    net = after_bulk - coupon_off
    shipping = 0 if net >= FREE_SHIP_MIN else SHIPPING
    tax = tax_on(net)
    return {
        "subtotal": subtotal,
        "discount": discount,
        "coupon": coupon_off,
        "net": net,
        "tax": tax,
        "shipping": shipping,
        "total": net + tax + shipping,
    }


def split_payment(total, parts):
    """Split `total` cents into `parts` instalments, largest first."""
    if parts < 1:
        raise PricingError("parts must be positive")
    q, r = divmod(total, parts)
    return [q + 1] * r + [q] * (parts - r)
