# Spec: `intervals`

`intervals.IntervalSet` represents a finite set S of integers. A pair `(a, b)` denotes the half-open range of integers x with `a <= x < b`. Exceptions are named by class; any subclass also satisfies a rule. Messages are unspecified.

**Domain.** All bounds and points are ints in -1000..1000. Behaviour on other argument types is unspecified.

| Rule | Statement |
|---|---|
| I1 | A new set is empty. |
| I2 | `add(a, b)`: S becomes S ∪ [a, b). `remove(a, b)`: S becomes S \ [a, b). Both raise `ValueError` if `a > b` and leave S unchanged; `a == b` is a no-op. |
| I3 | `contains(x)` returns whether x ∈ S. |
| I4 | `intervals()` returns the canonical form of S: a list of `(start, end)` tuples, sorted by `start`, with `start < end` for every pair and `end_i < start_{i+1}` for consecutive pairs (no overlapping, touching or empty pairs). The canonical form of a set is unique. |
| I5 | `measure()` returns the number of integers in S. |
| I6 | `gaps(lo, hi)` returns the canonical form (as in I4) of [lo, hi) \ S. Raises `ValueError` if `lo > hi`. |
| I7 | `overlaps(a, b)` returns whether [a, b) ∩ S is non-empty. Raises `ValueError` if `a > b`. |
| I8 | Only `add` and `remove` change S. |

## Witness format

A witness is a JSON object `{"ops": [...]}` with at most 60 operations. A fresh `IntervalSet()` is created, then each operation `[method, arg1, ...]` is called in order, with `method` one of `add`, `remove`, `contains`, `intervals`, `measure`, `gaps`, `overlaps`. Exceptions are recorded and execution continues. Tuples are reported as JSON lists. Example: `{"ops": [["add", 1, 4], ["remove", 2, 3], ["intervals"]]}`.
