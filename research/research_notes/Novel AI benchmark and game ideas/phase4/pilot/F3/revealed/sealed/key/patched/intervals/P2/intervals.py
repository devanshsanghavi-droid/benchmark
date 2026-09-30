"""A set of integers stored as sorted, disjoint half-open intervals."""


def _check(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("bounds must be ints")
    if a > b:
        raise ValueError("empty range with a > b")


class IntervalSet:
    def __init__(self):
        self._iv = []

    def _normalize(self):
        self._iv.sort()
        merged = []
        for s, e in self._iv:
            if merged and not s > merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        self._iv = merged

    def add(self, a, b):
        _check(a, b)
        if a == b:
            return
        self._iv.append([a, b])
        self._normalize()

    def remove(self, a, b):
        _check(a, b)
        if a == b:
            return
        out = []
        for s, e in self._iv:
            if e <= a or s >= b:
                out.append([s, e])
                continue
            if s < a:
                out.append([s, a])
            if b < e:
                out.append([b, e])
        self._iv = out

    def contains(self, x):
        for s, e in self._iv:
            if s <= x < e:
                return True
            if s > x:
                break
        return False

    def intervals(self):
        return [(s, e) for s, e in self._iv]

    def measure(self):
        return sum(e - s for s, e in self._iv)

    def gaps(self, lo, hi):
        """Maximal uncovered pieces of [lo, hi)."""
        _check(lo, hi)
        out = []
        cur = lo
        for s, e in self._iv:
            if e <= cur:
                continue
            if s >= hi:
                break
            if s > cur:
                out.append((cur, s))
            cur = max(cur, e)
        if cur < hi:
            out.append((cur, hi))
        return out

    def overlaps(self, a, b):
        _check(a, b)
        if a == b:
            return False
        for s, e in self._iv:
            if s < b and a < e:
                return True
        return False
