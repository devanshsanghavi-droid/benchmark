"""Sealed patch definitions, part 2 (intervals, pricing, depgraph)."""

V, C = "violates", "compliant"

PATCHES = [
    # ---------------- intervals ----------------
    dict(repo="intervals", key="minmax_remove", label=V, category="representation invariant of returned structure",
         rule="I4", msg="Compute remove() remainders with min/max",
         edits=[("""            if s < a:
                out.append([s, a])
            if b < e:
                out.append([b, e])""", """            for lo, hi in ((s, min(e, a)), (max(s, b), e)):
                if lo <= hi:
                    out.append([lo, hi])""")],
         witness={"ops": [["add", 0, 10], ["remove", 0, 5], ["intervals"]]}),
    dict(repo="intervals", key="tidy_merge", label=C, category="equivalent rewrite at a boundary",
         rule=None, msg="Tidy the merge step in _normalize",
         edits=[("""            if merged and s <= merged[-1][1]:
                if e > merged[-1][1]:
                    merged[-1][1] = e
            else:""", """            if merged and not s > merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:""")]),
    dict(repo="intervals", key="bisect_contains", label=C, category="equivalent algorithmic change",
         rule=None, msg="Use binary search in contains()",
         edits=[('''half-open intervals."""
''', '''half-open intervals."""

import bisect
'''), ("""        for s, e in self._iv:
            if s <= x < e:
                return True
            if s > x:
                break
        return False""", """        i = bisect.bisect_right(self._iv, [x, float("inf")]) - 1
        return i >= 0 and self._iv[i][0] <= x < self._iv[i][1]""")]),
    dict(repo="intervals", key="local_merge_add", label=C, category="equivalent algorithmic change",
         rule=None, msg="Merge only neighbouring intervals in add()",
         edits=[("""        self._iv.append([a, b])
        self._normalize()""", """        left = [iv for iv in self._iv if iv[1] < a]
        right = [iv for iv in self._iv if iv[0] > b]
        mid = [iv for iv in self._iv if a <= iv[1] and iv[0] <= b]
        if mid:
            a, b = min(a, mid[0][0]), max(b, mid[-1][1])
        self._iv = left + [[a, b]] + right""")]),
    # ---------------- pricing ----------------
    dict(repo="pricing", key="bulk_multiply", label=V, category="rounding direction",
         rule="P3", msg="Simplify the bulk line total",
         edits=[("""        return gross - gross * BULK_PCT // 100""",
                 """        return gross * (100 - BULK_PCT) // 100""")],
         witness={"ops": [["line_total", 1, 11]]}),
    dict(repo="pricing", key="tax_divmod", label=C, category="equivalent rewrite of rounding",
         rule=None, msg="Make tax rounding explicit",
         edits=[("""    return (amount * TAX_BP + 5000) // 10000""",
                 """    q, r = divmod(amount * TAX_BP, 10000)
    return q + (r >= 5000)""")]),
    dict(repo="pricing", key="drop_clamp", label=C, category="removal of an unreachable guard + exception subclass",
         rule=None, msg="Add UnknownCoupon error and drop the coupon clamp",
         edits=[("""class PricingError(ValueError):
    pass
""", """class PricingError(ValueError):
    pass


class UnknownCoupon(PricingError):
    pass
"""), ("""            raise PricingError("unknown coupon")""",
       """            raise UnknownCoupon(coupon)"""),
                ("""            coupon_off = max(0, min(amount, after_bulk))""",
                 """            coupon_off = amount""")]),
    dict(repo="pricing", key="incremental_split", label=C, category="equivalent algorithmic change",
         rule=None, msg="Compute instalments incrementally",
         edits=[("""    q, r = divmod(total, parts)
    return [q + 1] * r + [q] * (parts - r)""", """    out = []
    for i in range(parts):
        out.append((total - sum(out)) // (parts - i))
    return out[::-1]""")]),
    # ---------------- depgraph ----------------
    dict(repo="depgraph", key="fifo_order", label=V, category="tie-break / ordering rule",
         rule="D5", msg="Use a FIFO queue in order()",
         edits=[("""import heapq
""", """from collections import deque
"""), ("""        ready = [n for n, k in waiting.items() if k == 0]
        heapq.heapify(ready)
        out = []
        while ready:
            n = heapq.heappop(ready)
            out.append(n)
            for u in users[n]:
                waiting[u] -= 1
                if waiting[u] == 0:
                    heapq.heappush(ready, u)""", """        ready = deque(sorted(n for n, k in waiting.items() if k == 0))
        out = []
        while ready:
            n = ready.popleft()
            out.append(n)
            for u in sorted(users[n]):
                waiting[u] -= 1
                if waiting[u] == 0:
                    ready.append(u)""")],
         witness={"ops": [["add", "b", ["a"]], ["add", "c"], ["order"]]}),
    dict(repo="depgraph", key="min_order", label=C, category="equivalent algorithmic change",
         rule=None, msg="Pick the next node with min() in order()",
         edits=[("""import heapq
""", """"""), ("""        ready = [n for n, k in waiting.items() if k == 0]
        heapq.heapify(ready)
        out = []
        while ready:
            n = heapq.heappop(ready)
            out.append(n)
            for u in users[n]:
                waiting[u] -= 1
                if waiting[u] == 0:
                    heapq.heappush(ready, u)""", """        ready = {n for n, k in waiting.items() if k == 0}
        out = []
        while ready:
            n = min(ready)
            ready.discard(n)
            out.append(n)
            for u in users[n]:
                waiting[u] -= 1
                if waiting[u] == 0:
                    ready.add(u)""")]),
    dict(repo="depgraph", key="direct_layers", label=C, category="equivalent rewrite",
         rule=None, msg="Build layers directly from depths",
         edits=[("""        out = []
        for n in order:
            while len(out) <= depth[n]:
                out.append([])
            out[depth[n]].append(n)
        return [sorted(layer) for layer in out]""", """        width = max(depth.values(), default=-1) + 1
        return [sorted(n for n in order if depth[n] == i) for i in range(width)]""")]),
    dict(repo="depgraph", key="self_dep_error", label=C,
         category="behaviour change inside spec latitude (exception class)",
         rule=None, msg="Report a self-dependency as GraphError",
         edits=[("""            raise CycleError("self dependency")""",
                 """            raise GraphError("node cannot depend on itself")""")]),
]
