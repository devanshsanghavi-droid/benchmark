"""F2 pilot -- compositional rule grammar over block-world scenes, vectorised with numpy.

Cost = description length in grammar symbols (a proxy for the spec's 'depth'/prior bits):
  concepts: any=0, atom=1 (shape / colour / size / on-ground / top-of-stack),
            negated atom=2, conjunction of two atoms from different categories=2
  count templates: exists/none U: c+1 ; count(U) =k, >=k, <=k, even/odd: c+2
  count(U1) > count(U2), count(U1) = count(U2): c1+c2+2
  every U1 is U2: c1+c2+1
  relational (R in on, under, above, below, touches, left, right, same-stack):
     forall x in U1 exists y in U2 R(x,y); exists-exists; none; forall-forall : c1+c2+2
  stack-level: every stack contains U: c+2; stack homogeneity/distinctness of an attribute: 2;
     neighbour (touching) sameness/difference of an attribute: 2; all stacks same/different height: 2;
     max stack height =,>=,<= k: 3; heights strictly increasing/decreasing left-to-right: 3;
     leftmost/rightmost stack is (weakly) tallest: 3
  Boolean: NOT r: c+1 ; r1 AND r2, r1 OR r2 (one level, over base rules): c1+c2+1
"""
import numpy as np
from world import SHAPES, COLOURS, SIZES, NSLOTS

M = 12
RELS = ["on", "under", "above", "below", "touches", "left_of", "right_of", "same_stack"]


def arrays(scenes):
    N = len(scenes)
    shape = np.full((N, M), -1, np.int8); col = np.full((N, M), -1, np.int8)
    size = np.full((N, M), -1, np.int8); slot = np.full((N, M), -1, np.int8)
    level = np.full((N, M), -1, np.int8); top = np.zeros((N, M), bool)
    for i, sc in enumerate(scenes):
        j = 0
        for st in sorted(sc, key=lambda s: s["slot"]):
            h = len(st["objs"])
            for lv, (s, c, z) in enumerate(st["objs"]):
                shape[i, j] = SHAPES.index(s); col[i, j] = COLOURS.index(c); size[i, j] = SIZES.index(z)
                slot[i, j] = st["slot"]; level[i, j] = lv; top[i, j] = (lv == h - 1)
                j += 1
    valid = shape >= 0
    A = dict(N=N, shape=shape, col=col, size=size, slot=slot, level=level, top=top, valid=valid)
    vp = valid[:, :, None] & valid[:, None, :] & ~np.eye(M, dtype=bool)[None]
    same = vp & (slot[:, :, None] == slot[:, None, :])
    on = same & (level[:, :, None] == level[:, None, :] + 1)
    above = same & (level[:, :, None] > level[:, None, :])
    left = vp & (slot[:, :, None] < slot[:, None, :])
    tr = lambda X: X.transpose(0, 2, 1)
    A["R"] = {"on": on, "under": tr(on), "above": above, "below": tr(above), "touches": on | tr(on),
              "left_of": left, "right_of": tr(left), "same_stack": same}
    # per-stack info
    has = np.zeros((N, NSLOTS), bool); height = np.zeros((N, NSLOTS), np.int8)
    for s in range(NSLOTS):
        m = valid & (slot == s)
        has[:, s] = m.any(1); height[:, s] = m.sum(1)
    A["has"], A["height"] = has, height
    return A


def concepts(A):
    v = A["valid"]
    atoms = []   # (category, name, mask)
    for k, s in enumerate(SHAPES):
        atoms.append(("shape", s, v & (A["shape"] == k)))
    for k, c in enumerate(COLOURS):
        atoms.append(("colour", c, v & (A["col"] == k)))
    for k, z in enumerate(SIZES):
        atoms.append(("size", z, v & (A["size"] == k)))
    atoms.append(("ground", "on-ground", v & (A["level"] == 0)))
    atoms.append(("top", "top-of-stack", v & A["top"]))
    C = [("object", 0, v)]
    for cat, n, m in atoms:
        C.append((n, 1, m))
    for cat, n, m in atoms:
        C.append(("non-" + n, 2, v & ~m))
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            if atoms[i][0] != atoms[j][0]:
                C.append((atoms[i][1] + "&" + atoms[j][1], 2, atoms[i][2] & atoms[j][2]))
    return C


def base_rules(A, cmax):
    """yield (cost, description, bool[N])"""
    C = concepts(A)
    N = A["N"]
    cnt = {n: m.sum(1) for n, c, m in C}
    Cn = [(n, c, m) for n, c, m in C if n != "object"]
    for n, c, m in C:
        k = cnt[n]
        if c + 1 <= cmax:
            yield c + 1, f"exists {n}", k >= 1
            yield c + 1, f"no {n}", k == 0
        if c + 2 <= cmax:
            top_k = 8 if n == "object" else 5
            for q in range(1, top_k + 1):
                yield c + 2, f"count({n})=={q}", k == q
                yield c + 2, f"count({n})>={q+1}", k >= q + 1
                yield c + 2, f"count({n})<={q}", k <= q
            yield c + 2, f"count({n}) even", k % 2 == 0
            yield c + 2, f"count({n}) odd", k % 2 == 1
    for i, (n1, c1, m1) in enumerate(Cn):
        for j, (n2, c2, m2) in enumerate(Cn):
            if i == j:
                continue
            if c1 + c2 + 2 <= cmax:
                yield c1 + c2 + 2, f"count({n1})>count({n2})", cnt[n1] > cnt[n2]
                if i < j:
                    yield c1 + c2 + 2, f"count({n1})==count({n2})", cnt[n1] == cnt[n2]
            if c1 + c2 + 1 <= cmax:
                yield c1 + c2 + 1, f"every {n1} is {n2}", ~(m1 & ~m2).any(1)
    # relational quantifiers
    NOTEYE = ~np.eye(M, dtype=bool)[None]
    for r in RELS:
        Rm = A["R"][r]
        for n2, c2, m2 in C:
            E = (Rm & m2[:, None, :]).any(2)                      # x has some R-partner in U2
            AL = ~(~Rm & m2[:, None, :] & NOTEYE).any(2)          # x is R-related to all (other) U2
            for n1, c1, m1 in C:
                c = c1 + c2 + 2
                if c > cmax:
                    continue
                yield c, f"every {n1} {r} some {n2}", ~(m1 & ~E).any(1)
                yield c, f"some {n1} {r} some {n2}", (m1 & E).any(1)
                yield c, f"no {n1} {r} any {n2}", ~(m1 & E).any(1)
                yield c, f"every {n1} {r} every {n2}", ~(m1 & ~AL).any(1)
    # stack-level
    has, height = A["has"], A["height"]
    slot, valid = A["slot"], A["valid"]
    for n, c, m in C:
        if c + 2 <= cmax:
            cont = np.stack([(m & (slot == s)).any(1) for s in range(NSLOTS)], 1)
            yield c + 2, f"every stack contains {n}", ~(has & ~cont).any(1)
    if cmax >= 2:
        same = A["R"]["same_stack"]; on = A["R"]["on"]
        for an, key in (("colour", "col"), ("shape", "shape"), ("size", "size")):
            eq = A[key][:, :, None] == A[key][:, None, :]
            yield 2, f"within each stack all share {an}", ~(same & ~eq).any((1, 2))
            yield 2, f"within each stack no two share {an}", ~(same & eq).any((1, 2))
            yield 2, f"touching objects always share {an}", ~(on & ~eq).any((1, 2))
            yield 2, f"touching objects never share {an}", ~(on & eq).any((1, 2))
        hmax = np.where(has, height, -1).max(1)
        hmin = np.where(has, height, 99).min(1)
        yield 2, "all stacks same height", hmax == hmin
        hs = [sorted([h for h, e in zip(height[i], has[i]) if e]) for i in range(len(height))]
        yield 2, "all stacks different heights", np.array([len(set(x)) == len(x) for x in hs])
    if cmax >= 3:
        for q in (1, 2, 3):
            yield 3, f"max height=={q}", hmax == q
            yield 3, f"max height>={q}", hmax >= q
            yield 3, f"max height<={q}", hmax <= q
        seq = [[h for h, e in zip(height[i], has[i]) if e] for i in range(len(height))]
        yield 3, "heights strictly increase left->right", np.array([all(a < b for a, b in zip(x, x[1:])) for x in seq])
        yield 3, "heights strictly decrease left->right", np.array([all(a > b for a, b in zip(x, x[1:])) for x in seq])
        yield 3, "leftmost stack is (weakly) tallest", np.array([x[0] == max(x) for x in seq])
        yield 3, "rightmost stack is (weakly) tallest", np.array([x[-1] == max(x) for x in seq])


class RuleSet:
    """Deduplicated rules (semantic equivalence on the given scene set), min-cost representative kept."""

    def __init__(self, A, cmax, with_bool=True, verbose=False):
        self.N = A["N"]
        idx = {}
        costs, descs, rows = [], [], []

        def add(c, d, packed):
            key = packed.tobytes()
            j = idx.get(key)
            if j is None:
                idx[key] = len(costs); costs.append(c); descs.append(d); rows.append(packed)
            elif c < costs[j]:
                costs[j] = c; descs[j] = d

        for c, d, v in base_rules(A, cmax):
            add(c, d, np.packbits(np.asarray(v, bool)))
        nbase = len(costs)
        if with_bool:
            P = np.array(rows)
            bc = np.array(costs)
            for j in range(nbase):
                if bc[j] + 1 <= cmax:
                    add(bc[j] + 1, f"NOT[{descs[j]}]", np.packbits(~np.unpackbits(P[j], count=self.N).astype(bool)))
            for a in range(2, cmax):
                for b in range(a, cmax):
                    if a + b + 1 > cmax:
                        continue
                    ia = np.where(bc == a)[0]; ib = np.where(bc == b)[0]
                    Pb = P[ib]
                    for t, i in enumerate(ia):
                        sel = slice(t + 1, None) if a == b else slice(None)
                        ibs = ib[sel]
                        if len(ibs) == 0:
                            continue
                        Pbs = Pb[sel]
                        for op, R in (("AND", Pbs & P[i]), ("OR", Pbs | P[i])):
                            for k in range(len(ibs)):
                                key = R[k].tobytes()
                                if key not in idx:
                                    add(a + b + 1, f"[{descs[i]}] {op} [{descs[ibs[k]]}]", R[k].copy())
                                else:
                                    jj = idx[key]
                                    if a + b + 1 < costs[jj]:
                                        costs[jj] = a + b + 1; descs[jj] = f"[{descs[i]}] {op} [{descs[ibs[k]]}]"
        self.costs = np.array(costs, np.int16)
        self.descs = descs
        self.P = np.array(rows)
        self.idx = idx
        if verbose:
            print(f"  rules: {len(costs)} unique (base {nbase}); by cost:",
                  {int(c): int((self.costs == c).sum()) for c in np.unique(self.costs)})

    def matrix(self, sel=None, cols=None):
        P = self.P if sel is None else self.P[sel]
        X = np.unpackbits(P, axis=1, count=self.N).astype(bool)
        return X if cols is None else X[:, cols]

    def cost_of(self, vec):
        j = self.idx.get(np.packbits(np.asarray(vec, bool)).tobytes())
        return None if j is None else (int(self.costs[j]), self.descs[j])
