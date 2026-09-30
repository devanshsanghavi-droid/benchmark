# Spec: `pricing`

Checkout pricing. All money values are `int` cents. Exceptions are named by class; any subclass also satisfies a rule. Messages are unspecified. "floor" means rounding toward negative infinity.

**Domain.** A cart is a list of 0..20 lines; each line is a list `[sku, unit_price, qty]` with `sku` a string of at most 20 characters, `unit_price` an int in -10**6..10**6 and `qty` an int in -1000..1000. `coupon` is `None` or a string of at most 20 characters. Other ints passed to module functions are in -10**9..10**9, except that `parts` in `split_payment` is in -1000..1000. Behaviour outside this domain is unspecified.

| Rule | Statement |
|---|---|
| P1 | `checkout(cart, coupon=None)` raises `PricingError` if the cart is empty, two lines share a `sku`, any `unit_price < 0`, any `qty < 1`, or `coupon` is not `None` and not a known code. |
| P2 | `subtotal` is the sum over lines of `unit_price * qty`. |
| P3 | Bulk discount: a line with `qty >= 10` gets a line discount of `floor(unit_price * qty * 10 / 100)` cents (10 % off, rounded down to a whole cent). Other lines get 0. `discount` is the sum of line discounts. `line_total(unit_price, qty)` (for `unit_price >= 0`, `qty >= 1`) returns `unit_price * qty` minus that line's discount. |
| P4 | Coupons: `"SAVE5"` takes 500 off when `subtotal - discount >= 5000`; `"SAVE20"` takes 2000 off when `subtotal - discount >= 20000`. A known coupon below its minimum is accepted and takes 0 off. `coupon` in the result is the amount taken off. |
| P5 | `net = subtotal - discount - coupon`. |
| P6 | `shipping` is 0 when `net >= 5000`, otherwise 599. |
| P7 | `tax` is `net * 8.25 / 100` rounded to the nearest cent, with exact halves rounded up; equivalently `floor((net * 825 + 5000) / 10000)`. `tax_on(amount)` returns this value for any int `amount >= 0`. |
| P8 | `checkout` returns a dict with exactly the keys `subtotal`, `discount`, `coupon`, `net`, `tax`, `shipping`, `total`, where `total = net + tax + shipping`. |
| P9 | `split_payment(total, parts)`, for `total >= 0`: raises `PricingError` if `parts < 1`; otherwise returns a list of `parts` ints in non-increasing order that sum to `total` and differ from each other by at most 1. |
| P10 | No function modifies its arguments. |

## Witness format

A witness is a JSON object `{"ops": [...]}` with at most 20 operations. Each operation is `[function, arg1, ...]` with `function` one of `checkout` (args: `cart`, `coupon`), `line_total`, `tax_on`, `split_payment`. Operations are independent. Exceptions are recorded and execution continues. Example: `{"ops": [["checkout", [["pen", 150, 2]], null], ["tax_on", 999]]}`.
