"""Sealed patch definitions, part 1 (ledger, ratelimit)."""

V, C = "violates", "compliant"

PATCHES = [
    # ---------------- ledger ----------------
    dict(repo="ledger", key="merge_loops", label=V, category="atomicity / partial update on failure",
         rule="L7", msg="Merge the validation and debit loops in split_fee",
         edits=[("""            if self._bal[name] < share:
                raise InsufficientFunds(name)
        for name, share in shares.items():
            self._bal[name] -= share""", """            if self._bal[name] < share:
                raise InsufficientFunds(name)
            self._bal[name] -= share""")],
         witness={"ops": [["open", "a", 10], ["open", "b", 0], ["split_fee", ["a", "b"], 4],
                          ["balance", "a"]]}),
    dict(repo="ledger", key="even_spread", label=V, category="arithmetic distribution rule",
         rule="L5", msg="Compute fee shares without a separate remainder pass",
         edits=[("""        n = len(payers)
        base, rem = fee // n, fee % n
        shares = {}
        for i, name in enumerate(payers):
            shares[name] = base + (1 if i < rem else 0)""", """        n = len(payers)
        shares = {}
        for i, name in enumerate(payers):
            shares[name] = fee * (i + 1) // n - fee * i // n""")],
         witness={"ops": [["fee_shares", ["a", "b"], 1]]}),
    dict(repo="ledger", key="divmod_shares", label=C, category="equivalent rewrite of arithmetic",
         rule=None, msg="Simplify fee_shares with divmod",
         edits=[("""        n = len(payers)
        base, rem = fee // n, fee % n
        shares = {}
        for i, name in enumerate(payers):
            shares[name] = base + (1 if i < rem else 0)
        return shares""", """        q, r = divmod(fee, len(payers))
        return {name: q + (i < r) for i, name in enumerate(payers)}""")]),
    dict(repo="ledger", key="transfer_reorder", label=C,
         category="behaviour change inside spec latitude (exception choice)",
         rule=None, msg="Check accounts and funds before other transfer validation",
         edits=[("""        if src == dst:
            raise LedgerError("self transfer")
        bal = self._get(src)
        self._get(dst)
        if bal < cents:
            raise InsufficientFunds(src)""", """        bal = self._get(src)
        self._get(dst)
        if cents > bal:
            raise InsufficientFunds(src)
        if src == dst:
            raise LedgerError("self transfer")""")]),
    # ---------------- ratelimit ----------------
    dict(repo="ratelimit", key="bisect_prune", label=V, category="boundary condition at exact threshold",
         rule="R3", msg="Use binary search to prune expired requests",
         edits=[('''timestamps."""
''', '''timestamps."""

import bisect
'''), ("""        i = 0
        while i < len(q) and q[i] <= cutoff:
            i += 1
        if i:""", """        i = bisect.bisect_left(q, cutoff)
        if i:""")],
         witness={"ops": [["init", 1, 10], ["allow", "k", 0], ["allow", "k", 10]]}),
    dict(repo="ratelimit", key="comprehension_prune", label=C, category="equivalent rewrite at a boundary",
         rule=None, msg="Prune expired requests with a comprehension",
         edits=[("""        i = 0
        while i < len(q) and q[i] <= cutoff:
            i += 1
        if i:""", """        kept = [s for s in q if s > cutoff]
        i = len(q) - len(kept)
        if i:""")]),
    dict(repo="ratelimit", key="allow_via_remaining", label=C, category="equivalent refactor",
         rule=None, msg="Implement allow() on top of remaining()",
         edits=[("""    def allow(self, key, t):
        self._tick(t)
        q = self._prune(key, t)
        if len(q) >= self.capacity:
            return False""", """    def allow(self, key, t):
        if self.remaining(key, t) <= 0:
            return False""")]),
    dict(repo="ratelimit", key="sorted_keys", label=C,
         category="behaviour change inside spec latitude (unspecified order)",
         rule=None, msg="Return keys in sorted order",
         edits=[("""                live.append(key)
        return live""", """                live.append(key)
        return sorted(live)""")]),
]
