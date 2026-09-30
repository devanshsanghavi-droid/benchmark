# Spec: `ratelimit`

`ratelimit.Limiter(capacity, window)` is a per-key sliding-window rate limiter. Time is supplied by the caller as an `int`. Exceptions are named by class; any subclass also satisfies a rule. Messages are unspecified.

**Domain.** `capacity` and `window` are ints in 1..1000. Times are ints in 0..10**9. Keys are non-empty strings of at most 20 characters. Behaviour on other argument types is unspecified.

| Rule | Statement |
|---|---|
| R1 | The constructor raises `ValueError` if `capacity < 1` or `window < 1`. |
| R2 | Clock: every call that takes `t` raises `ClockError` (a `ValueError`) if `t` is smaller than the largest `t` passed to any earlier successful call on the same limiter. Equal times are allowed. A call that raises changes no state. |
| R3 | Window: a request at time `s` is *live* at time `t` if and only if `t - window < s <= t`. |
| R4 | `allow(key, t)` returns `True` and records a request for `key` at time `t` if fewer than `capacity` requests for `key` are live at `t`; otherwise it returns `False` and records nothing. Only allowed requests are recorded. |
| R5 | `remaining(key, t)` returns `capacity` minus the number of recorded requests for `key` live at `t`. It records nothing. |
| R6 | `retry_after(key, t)` returns the smallest integer `d >= 0` such that `allow(key, t + d)` would return `True` if no other calls were made in between. It records nothing. |
| R7 | `keys(t)` returns a list of the distinct keys that have at least one recorded request live at `t`. List order is unspecified. |
| R8 | `reset(key)` forgets every recorded request for `key`. It does not take a time and never raises for an unknown key. |
| R9 | Keys are independent: calls for one key never change the results for another key, except through the clock rule R2. |

## Witness format

A witness is a JSON object `{"ops": [...]}` with at most 60 operations. The first operation must be `["init", capacity, window]`, which constructs the limiter. Each later operation is `[method, arg1, ...]` with `method` one of `allow`, `remaining`, `retry_after`, `keys`, `reset`. Exceptions are recorded and execution continues. Example: `{"ops": [["init", 2, 10], ["allow", "k", 0], ["remaining", "k", 3]]}`.
