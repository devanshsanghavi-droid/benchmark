#!/usr/bin/env python3
"""F5 Self-Knowledge Exam -- pilot item generator (SEALED; not for solvers).

Usage: python3 generate.py SEED OUT_PUBLIC_DIR OUT_KEY_DIR

Six families x five difficulty levels x two items = 60 items.
Every answer is computed by code here and re-checked by an independent path
(uniqueness solver for logic grids, grammar enumeration for rule inference,
symbolic reader for documents, exec for programs).
"""
import io, json, math, os, random, sys, itertools, contextlib
from fractions import Fraction
from functools import lru_cache

LEVELS = [1, 2, 3, 4, 5]

# --------------------------------------------------------------------------
# Family 1: exact computation (arithmetic, number theory, counting)
# --------------------------------------------------------------------------
PRIMES_SMALL = [2, 3, 5, 7, 11, 13]
PRIMES_2D = [37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def ndig(rng, n):
    while True:
        x = rng.randint(10 ** (n - 1), 10 ** n - 1)
        if x % 10 != 0:
            return x


def lattice_paths(M, N, forb, below_diag=False):
    forb = set(forb)
    f = {}
    for i in range(M + 1):
        for j in range(N + 1):
            if (i, j) in forb or (below_diag and j > i):
                f[(i, j)] = 0
            elif i == 0 and j == 0:
                f[(i, j)] = 1
            else:
                f[(i, j)] = f.get((i - 1, j), 0) + f.get((i, j - 1), 0)
    return f[(M, N)]


def lattice_paths_bruteforce(M, N, forb, below_diag=False):
    # independent check: enumerate step sequences (fine for small grids)
    forb = set(forb)
    cnt = 0
    for xs in itertools.combinations(range(M + N), M):
        xs = set(xs)
        x = y = 0
        ok = True
        for s in range(M + N):
            if s in xs:
                x += 1
            else:
                y += 1
            if (x, y) in forb or (below_diag and y > x):
                ok = False
                break
        cnt += ok
    return cnt


def sigma(n):
    s = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            s += d
            if d * d != n:
                s += n // d
        d += 1
    return s


def gen_compute(rng, level, sub):
    fmt = "a single integer (digits only)"
    if level == 1 and sub == 0:
        a, b = ndig(rng, 3), ndig(rng, 3)
        return f"Compute {a} × {b}.", a * b, "int", fmt, {"kind": "mul3x3"}
    if level == 1 and sub == 1:
        while True:
            g = rng.randint(12, 99)
            x, y = rng.randint(20, 150), rng.randint(20, 150)
            if math.gcd(x, y) == 1:
                break
        a, b = g * x, g * y
        assert math.gcd(a, b) == g
        return f"Compute the greatest common divisor of {a} and {b}.", g, "int", fmt, {"kind": "gcd"}
    if level == 2 and sub == 0:
        a, b = ndig(rng, 5), ndig(rng, 4)
        return f"Compute {a} × {b}.", a * b, "int", fmt, {"kind": "mul5x4"}
    if level == 2 and sub == 1:
        p = rng.choice(PRIMES_2D)
        while True:
            a = rng.randint(11, 99)
            if a % p:
                break
        e = rng.randint(30, 90)
        return (f"Compute the remainder when {a}^{e} (that is, {a} raised to the power {e}) is divided by {p}.",
                pow(a, e, p), "int", fmt, {"kind": "powmod"})
    if level == 3 and sub == 0:
        ps = sorted(rng.sample([3, 5, 7, 11, 13], 3))
        N = rng.randint(20000, 99999)
        ans = sum(1 for n in range(1, N + 1) if all(n % q for q in ps))
        return (f"How many integers n with 1 ≤ n ≤ {N} are divisible by none of {ps[0]}, {ps[1]} and {ps[2]}?",
                ans, "int", fmt, {"kind": "incl_excl"})
    if level == 3 and sub == 1:
        M, N = rng.randint(6, 7), rng.randint(6, 7)
        cells = [(i, j) for i in range(M + 1) for j in range(N + 1) if (i, j) not in [(0, 0), (M, N)]]
        while True:
            fb = sorted(rng.sample(cells, 3))
            ans = lattice_paths(M, N, fb)
            if ans > 0 and ans < lattice_paths(M, N, []) * 0.7:
                break
        assert ans == lattice_paths_bruteforce(M, N, fb)
        pts = ", ".join(f"({x},{y})" for x, y in fb)
        return (f"A path goes from (0,0) to ({M},{N}) using unit steps, each of which increases either the x-coordinate "
                f"or the y-coordinate by 1. How many such paths pass through none of the points {pts}?",
                ans, "int", fmt, {"kind": "lattice"})
    if level == 4 and sub == 0:
        a, b = ndig(rng, 8), ndig(rng, 7)
        return f"Compute {a} × {b}.", a * b, "int", fmt, {"kind": "mul8x7"}
    if level == 4 and sub == 1:
        while True:
            n = 2 ** rng.randint(1, 4) * 3 ** rng.randint(0, 2)
            for q in rng.sample([5, 7, 11, 13, 17, 19, 23, 29, 31, 37], 3):
                n *= q ** rng.randint(1, 2)
            if 200000 <= n <= 9999999:
                break
        return (f"Compute the sum of all positive divisors of {n} (including 1 and {n} itself).",
                sigma(n), "int", fmt, {"kind": "sigma"})
    if level == 5 and sub == 0:
        a, b = ndig(rng, 13), ndig(rng, 12)
        return f"Compute {a} × {b}.", a * b, "int", fmt, {"kind": "mul13x12"}
    if level == 5 and sub == 1:
        n = 10
        cells = [(i, j) for i in range(1, n + 1) for j in range(0, i + 1) if (i, j) not in [(n, n)] and i + j > 1]
        while True:
            fb = sorted(rng.sample(cells, 4))
            ans = lattice_paths(n, n, fb, below_diag=True)
            if 0 < ans < 0.5 * lattice_paths(n, n, [], below_diag=True):
                break
        assert ans == lattice_paths_bruteforce(n, n, fb, below_diag=True)
        pts = ", ".join(f"({x},{y})" for x, y in fb)
        return (f"A path goes from (0,0) to ({n},{n}) using unit steps, each of which increases either the x-coordinate "
                f"or the y-coordinate by 1, and it never visits a point with y > x. How many such paths pass through "
                f"none of the points {pts}?", ans, "int", fmt, {"kind": "lattice_diag"})
    raise ValueError


# --------------------------------------------------------------------------
# Family 2: logic grid puzzles (unique solution checked by a CSP solver)
# --------------------------------------------------------------------------
ATTRS = {
    "name": ["Ada", "Bram", "Cleo", "Dov", "Esme", "Fitz", "Gus", "Hana", "Ivo", "Juno"],
    "pet": ["cat", "dog", "fox", "owl", "hare", "newt", "goat", "crow"],
    "drink": ["tea", "coffee", "milk", "juice", "water", "cocoa", "cider", "kefir"],
    "colour": ["red", "blue", "green", "white", "yellow", "black", "grey", "orange"],
    "instrument": ["violin", "cello", "flute", "harp", "drums", "piano", "oboe", "banjo"],
}
PLAYER = {"violin": "violinist", "cello": "cellist", "flute": "flautist", "harp": "harpist",
          "drums": "drummer", "piano": "pianist", "oboe": "oboist", "banjo": "banjo player"}


def np_(attr, v):
    if attr == "name":
        return v
    if attr == "pet":
        return f"the {v} owner"
    if attr == "drink":
        return f"the {v} drinker"
    if attr == "colour":
        return f"the resident of the {v} house"
    if attr == "instrument":
        return f"the {PLAYER[v]}"


def vp_(attr, v, neg=False):
    if attr == "name":
        return f"is {'not ' if neg else ''}{v}"
    if attr == "pet":
        return f"{'does not own' if neg else 'owns'} the {v}"
    if attr == "drink":
        return f"{'does not drink' if neg else 'drinks'} {v}"
    if attr == "colour":
        return f"{'does not live' if neg else 'lives'} in the {v} house"
    if attr == "instrument":
        return f"{'does not play' if neg else 'plays'} the {v}"


def cap(s):
    return s[0].upper() + s[1:]


def clue_holds(c, pos):
    t = c[0]
    if t in ("pos", "notpos", "ends"):
        h = pos[c[1]]
        if t == "pos":
            return h == c[2]
        if t == "notpos":
            return h != c[2]
        return h in (1, c[2])
    x, y = pos[c[1]], pos[c[2]]
    return {"same": x == y, "notsame": x != y, "leftimm": x + 1 == y, "left": x < y,
            "next": abs(x - y) == 1, "notnext": abs(x - y) != 1}[t]


def csp_count(N, attrs, vals, clues, limit=2):
    """Count solutions (up to limit) by backtracking with forward checking."""
    vars_ = [(a, v) for a in attrs for v in vals[a]]
    dom = {x: set(range(1, N + 1)) for x in vars_}
    for c in clues:
        if c[0] == "pos":
            dom[c[1]] &= {c[2]}
        elif c[0] == "notpos":
            dom[c[1]] -= {c[2]}
        elif c[0] == "ends":
            dom[c[1]] &= {1, c[2]}
    binary = [c for c in clues if c[0] not in ("pos", "notpos", "ends")]
    by_var = {x: [] for x in vars_}
    for c in binary:
        by_var[c[1]].append(c)
        by_var[c[2]].append(c)
    count = [0]

    def ok_partial(assign, x):
        for c in by_var[x]:
            if c[1] in assign and c[2] in assign:
                if not clue_holds(c, assign):
                    return False
        return True

    def rec(assign, dom):
        if count[0] >= limit:
            return
        un = [x for x in vars_ if x not in assign]
        if not un:
            count[0] += 1
            return
        x = min(un, key=lambda z: len(dom[z]))
        for h in sorted(dom[x]):
            assign[x] = h
            if ok_partial(assign, x):
                nd = {}
                bad = False
                for z in un:
                    if z == x:
                        continue
                    d = dom[z]
                    if z[0] == x[0]:
                        d = d - {h}
                    # forward check binary constraints with x
                    for c in by_var[x]:
                        other = c[2] if c[1] == x else c[1]
                        if other == z:
                            d = {hz for hz in d if clue_holds(c, {x: h, z: hz})}
                    if not d:
                        bad = True
                        break
                    nd[z] = d
                if not bad:
                    rec(assign, nd)
            del assign[x]

    rec({}, dom)
    return count[0]


def gen_logic(rng, level, sub):
    # reject puzzles whose asked order equals the (sorted) listing of values or its reverse: a free guess
    while True:
        r = _gen_logic_once(rng, level, sub)
        if r[1] != sorted(r[1]) and r[1] != sorted(r[1], reverse=True):
            return r


def _gen_logic_once(rng, level, sub):
    N, K, types, minimise = {
        1: (3, 2, ["same", "pos", "leftimm", "next", "notsame"], False),
        2: (4, 2, ["same", "pos", "leftimm", "next", "notsame", "notpos"], True),
        3: (4, 3, ["same", "pos", "leftimm", "next", "notsame", "left", "notpos"], True),
        4: (5, 3, ["same", "leftimm", "next", "notsame", "left", "notpos", "notnext", "ends"], True),
        5: (5, 4, ["same", "leftimm", "next", "notsame", "left", "notpos", "notnext", "ends"], True),
    }[level]
    attrs = ["name"] + rng.sample(["pet", "drink", "colour", "instrument"], K - 1)
    vals = {a: rng.sample(ATTRS[a], N) for a in attrs}
    sol = {}
    for a in attrs:
        perm = list(range(1, N + 1))
        rng.shuffle(perm)
        for v, h in zip(vals[a], perm):
            sol[(a, v)] = h
    vars_ = list(sol)

    def rand_clue():
        t = rng.choice(types)
        if t in ("pos", "notpos", "ends"):
            x = rng.choice(vars_)
            if t == "pos":
                return ("pos", x, sol[x])
            if t == "notpos":
                hs = [h for h in range(1, N + 1) if h != sol[x]]
                return ("notpos", x, rng.choice(hs))
            if sol[x] in (1, N):
                return ("ends", x, N)
            return None
        x, y = rng.sample(vars_, 2)
        if t in ("same", "notsame") and x[0] == y[0]:
            return None
        c = (t, x, y)
        return c if clue_holds(c, sol) else None

    for _ in range(200):
        clues = []
        while csp_count(N, attrs, vals, clues) > 1:
            c = rand_clue()
            if c and c not in clues:
                clues.append(c)
        if minimise:
            order = list(range(len(clues)))
            rng.shuffle(order)
            keep = list(clues)
            for i in order:
                trial = [c for c in keep if c != clues[i]]
                if csp_count(N, attrs, vals, trial) == 1:
                    keep = trial
            clues = keep
        if len(clues) >= {1: 3, 2: 4, 3: 7, 4: 9, 5: 12}[level]:
            break
    assert csp_count(N, attrs, vals, clues) == 1
    assert all(clue_holds(c, sol) for c in clues)
    rng.shuffle(clues)
    ask = rng.choice(attrs[1:]) if sub == 0 else "name"
    lines = []
    for c in clues:
        t = c[0]
        if t == "pos":
            lines.append(f"{cap(np_(*c[1]))} lives in house {c[2]}.")
        elif t == "notpos":
            lines.append(f"{cap(np_(*c[1]))} does not live in house {c[2]}.")
        elif t == "ends":
            lines.append(f"{cap(np_(*c[1]))} lives in one of the two end houses.")
        elif t == "same":
            lines.append(f"{cap(np_(*c[1]))} {vp_(*c[2])}.")
        elif t == "notsame":
            lines.append(f"{cap(np_(*c[1]))} {vp_(*c[2], neg=True)}.")
        elif t == "leftimm":
            lines.append(f"{cap(np_(*c[1]))} lives directly to the left of {np_(*c[2])}.")
        elif t == "left":
            lines.append(f"{cap(np_(*c[1]))} lives somewhere to the left of {np_(*c[2])}.")
        elif t == "next":
            lines.append(f"{cap(np_(*c[1]))} lives next to {np_(*c[2])}.")
        elif t == "notnext":
            lines.append(f"{cap(np_(*c[1]))} does not live next to {np_(*c[2])}.")
    attr_desc = {"name": "a different name", "pet": "a different pet", "drink": "a different drink",
                 "colour": "a house of a different colour", "instrument": "a different instrument"}
    intro = (f"{N} people live in a row of {N} houses, numbered 1 to {N} from left to right. "
             + "Each person has " + ", ".join(attr_desc[a] for a in attrs[:-1]) + " and " + attr_desc[attrs[-1]] + ". "
             + "The possible values are: " + "; ".join(f"{a}s: {', '.join(sorted(vals[a]))}" for a in attrs) + ". "
             + "\"Directly to the left of\" means in the house numbered one lower; \"next to\" means in an adjacent house.")
    clue_txt = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(lines))
    inv = {h: v for (a, v), h in sol.items() if a == ask}
    answer = [inv[h] for h in range(1, N + 1)]
    q = f"Question: list the {ask}s in house order, from house 1 to house {N}."
    prompt = intro + "\n\nClues:\n" + clue_txt + "\n\n" + q
    fmt = f"the {N} {ask}s separated by commas, in house order 1 to {N}"
    return prompt, answer, "wordlist", fmt, {"N": N, "K": K, "n_clues": len(clues)}


# --------------------------------------------------------------------------
# Family 3: string transformation tracing
# --------------------------------------------------------------------------
def apply_op(s, op):
    s = list(s)
    t = op[0]
    if t == "swap_pos":
        i, j = op[1] - 1, op[2] - 1
        s[i], s[j] = s[j], s[i]
    elif t == "swap_let":
        i, j = s.index(op[1]), s.index(op[2])
        s[i], s[j] = s[j], s[i]
    elif t == "rot_l":
        k = op[1] % len(s)
        s = s[k:] + s[:k]
    elif t == "rot_r":
        k = op[1] % len(s)
        s = s[-k:] + s[:-k] if k else s
    elif t == "rev":
        i, j = op[1] - 1, op[2] - 1
        s[i:j + 1] = s[i:j + 1][::-1]
    elif t == "move":
        i, j = op[1] - 1, op[2] - 1
        ch = s.pop(i)
        s.insert(j, ch)
    return "".join(s)


def apply_op_alt(s, op):
    # independent re-implementation for cross-checking
    n = len(s)
    t = op[0]
    if t == "swap_pos":
        i, j = op[1] - 1, op[2] - 1
        return "".join(s[j] if k == i else s[i] if k == j else s[k] for k in range(n))
    if t == "swap_let":
        a, b = op[1], op[2]
        return "".join(b if c == a else a if c == b else c for c in s)
    if t == "rot_l":
        return "".join(s[(k + op[1]) % n] for k in range(n))
    if t == "rot_r":
        return "".join(s[(k - op[1]) % n] for k in range(n))
    if t == "rev":
        i, j = op[1] - 1, op[2] - 1
        return s[:i] + s[i:j + 1][::-1] + s[j + 1:]
    if t == "move":
        i, j = op[1] - 1, op[2] - 1
        ch = s[i]
        rest = s[:i] + s[i + 1:]
        return rest[:j] + ch + rest[j:]


def op_text(op):
    t = op[0]
    if t == "swap_pos":
        return f"Swap the letters in positions {op[1]} and {op[2]}."
    if t == "swap_let":
        return f"Swap the letters {op[1]} and {op[2]} (wherever they currently are)."
    if t == "rot_l":
        return f"Rotate left by {op[1]} step{'s' if op[1] > 1 else ''}."
    if t == "rot_r":
        return f"Rotate right by {op[1]} step{'s' if op[1] > 1 else ''}."
    if t == "rev":
        return f"Reverse the letters in positions {op[1]} through {op[2]}."
    if t == "move":
        return f"Remove the letter in position {op[1]} and reinsert it so that it ends up in position {op[2]}."


def rewrite_step(s, rules):
    for lhs, rhs in rules:
        i = s.find(lhs)
        if i >= 0:
            return s[:i] + rhs + s[i + len(lhs):], True
    return s, False


def gen_trace(rng, level, sub):
    if sub == 0:
        n, nops = {1: (5, 3), 2: (6, 6), 3: (8, 10), 4: (10, 16), 5: (12, 26)}[level]
        s0 = "".join(rng.sample("abcdefghijklmnopqrstuvwxyz", n))
        kinds = ["swap_pos", "swap_let", "rot_l", "rot_r", "rev", "move"]
        ops = []
        for _ in range(nops):
            t = rng.choice(kinds)
            if t in ("swap_pos", "rev", "move"):
                i, j = rng.sample(range(1, n + 1), 2)
                if t == "rev" and i > j:
                    i, j = j, i
                ops.append((t, i, j))
            elif t == "swap_let":
                a, b = rng.sample(s0, 2)
                ops.append((t, a, b))
            else:
                ops.append((t, rng.randint(1, min(4, n - 1))))
        s = s1 = s0
        for op in ops:
            s = apply_op(s, op)
            s1 = apply_op_alt(s1, op)
            assert s == s1
        prompt = (f"Start with the string {s0}. Apply the following operations in order. Positions are numbered "
                  f"from 1 at the left. Rotating left by one step moves the first letter to the end; rotating right "
                  f"by one step moves the last letter to the front.\n"
                  + "\n".join(f"{k + 1}. {op_text(op)}" for k, op in enumerate(ops))
                  + "\n\nQuestion: what is the final string?")
        return prompt, s, "str", "the final string (letters only)", {"n": n, "nops": nops}
    # sub 1: string rewriting system
    T = {1: 3, 2: 6, 3: 10, 4: 16, 5: 26}[level]
    for _ in range(100000):
        alpha = "ABC"
        nr = rng.randint(2, 4)
        rules = []
        for _ in range(nr):
            lhs = "".join(rng.choice(alpha) for _ in range(rng.randint(1, 2)))
            rhs = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 3)))
            if lhs != rhs and lhs not in [r[0] for r in rules]:
                rules.append((lhs, rhs))
        if len(rules) < 2:
            continue
        s0 = "".join(rng.choice(alpha) for _ in range(rng.randint(4, 7)))
        s = s0
        used = set()
        good = True
        for step in range(T):
            before = s
            s, ok = rewrite_step(s, rules)
            if not ok or len(s) > 22:
                good = False
                break
            used.add(next(k for k, (l, r) in enumerate(rules) if before.find(l) >= 0))
        if not good or len(used) < min(len(rules), 3 if level >= 3 else 2) or len(s) < 4:
            continue
        # independent recomputation
        s2 = s0
        for _ in range(T):
            for lhs, rhs in rules:
                if lhs in s2:
                    s2 = s2.replace(lhs, rhs, 1)
                    break
        assert s2 == s
        break
    else:
        raise RuntimeError("rewrite gen failed")
    rules_txt = "\n".join(f"Rule {k + 1}: {l} → {r if r else '(empty string)'}" for k, (l, r) in enumerate(rules))
    prompt = (f"A rewriting process starts from the string {s0} and uses these rules:\n{rules_txt}\n\n"
              f"One step: find the lowest-numbered rule whose left-hand side occurs somewhere in the current string, "
              f"and replace the leftmost occurrence of that left-hand side with the rule's right-hand side. "
              f"(Only one replacement is made per step.)\n\n"
              f"Question: what is the string after exactly {T} steps?")
    return prompt, s, "str", "the resulting string (letters only)", {"T": T, "rules": len(rules)}


# --------------------------------------------------------------------------
# Family 4: program output prediction
# --------------------------------------------------------------------------
def run_prog(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<item>", "exec"), {"__builtins__": __builtins__})
    out = buf.getvalue()
    assert out.count("\n") == 1 and out.endswith("\n"), repr(out)
    return out.strip()


def pseudo_word(rng, n):
    cons, vow = "bcdfghjklmnprstvwz", "aeiou"
    return "".join(rng.choice(vow if (k % 2 == 1) ^ (rng.random() < 0.25) else cons) for k in range(n))


def gen_prog(rng, level, sub):
    while True:
        code, chk = _gen_prog_once(rng, level, sub)
        if code is None:
            continue
        out = run_prog(code)
        if chk is not None:
            assert chk == out, (chk, out)
        return ("Predict exactly what this Python 3 program prints.\n\n```python\n" + code + "```",
                out, "printed", "exactly the one line the program prints", {"template": f"L{level}{'ab'[sub]}"})


def _gen_prog_once(rng, level, sub):
    if level == 1 and sub == 0:
        n, k, c = rng.randint(9, 14), rng.randint(2, 4), rng.randint(2, 6)
        code = (f"total = 0\nfor i in range(1, {n}):\n    if i % {k} == 0:\n        total += i * {c}\n"
                f"    else:\n        total -= 1\nprint(total)\n")
        tot = sum(i * c if i % k == 0 else -1 for i in range(1, n))
        return code, str(tot)
    if level == 1 and sub == 1:
        w = pseudo_word(rng, 8)
        if sum(ch in "aeiou" for ch in w) < 3:
            return None, None
        code = (f"word = \"{w}\"\nout = \"\"\nfor ch in word:\n    if ch in \"aeiou\":\n        out = ch + out\n"
                f"    else:\n        out = out + ch\nprint(out)\n")
        out = ""
        for ch in w:
            out = ch + out if ch in "aeiou" else out + ch
        return code, out
    if level == 2 and sub == 0:
        xs = [rng.randint(1, 40) for _ in range(10)]
        m, t = rng.randint(5, 9), rng.randint(8, 16)
        ys = sorted(x % m for x in xs if x > t)
        if len(ys) < 4:
            return None, None
        code = f"xs = {xs}\nys = sorted(x % {m} for x in xs if x > {t})\nprint(ys[1:-1], sum(ys))\n"
        return code, f"{ys[1:-1]} {sum(ys)}"
    if level == 2 and sub == 1:
        vocab = ["amber", "arch", "atlas", "birch", "bolt", "brine", "cobalt", "crest", "cairn", "dune", "delta",
                 "drift", "ember", "echo", "flint", "fjord", "gale", "grove"]
        words = [rng.choice(vocab) for _ in range(9)]
        code = (f"words = \"{' '.join(words)}\".split()\ncounts = {{}}\nfor w in words:\n"
                f"    counts[w[0]] = counts.get(w[0], 0) + len(w)\n"
                f"print(\",\".join(k + str(v) for k, v in sorted(counts.items())))\n")
        return code, None
    if level == 3 and sub == 0:
        n0, b = rng.randint(25, 250), rng.choice([1, 3, 5, 7])
        n, steps, peak = n0, 0, n0
        while n >= 10 and steps < 300:
            n = n // 2 if n % 2 == 0 else 3 * n + b
            peak = max(peak, n)
            steps += 1
        if not (12 <= steps <= 24):
            return None, None
        code = (f"n = {n0}\nsteps = 0\npeak = n\nwhile n >= 10:\n    if n % 2 == 0:\n        n = n // 2\n"
                f"    else:\n        n = 3 * n + {b}\n    peak = max(peak, n)\n    steps += 1\nprint(steps, peak, n)\n")
        return code, f"{steps} {peak} {n}"
    if level == 3 and sub == 1:
        xs = [rng.randint(1, 9) for _ in range(13)]
        k = rng.randint(3, 5)
        stack, out = [], []
        for x in xs:
            if stack and (stack[-1] + x) % k == 0:
                out.append(stack.pop() * x)
            else:
                stack.append(x)
        if len(out) < 3:
            return None, None
        code = (f"stack = []\nout = []\nfor x in {xs}:\n    if stack and (stack[-1] + x) % {k} == 0:\n"
                f"        out.append(stack.pop() * x)\n    else:\n        stack.append(x)\nprint(out, stack)\n")
        return code, f"{out} {stack}"
    if level == 4 and sub == 0:
        n = 11
        cells = [rng.randint(0, 1) for _ in range(n)]
        t = rng.randint(5, 6)
        rule = rng.choice([
            ("cells[i - 1] ^ (cells[i] | cells[(i + 1) % {n}])", lambda c, i: c[i - 1] ^ (c[i] | c[(i + 1) % n])),
            ("(cells[i - 1] & cells[i]) ^ cells[(i + 1) % {n}]", lambda c, i: (c[i - 1] & c[i]) ^ c[(i + 1) % n]),
            ("cells[i - 1] ^ cells[(i + 1) % {n}] ^ (cells[i] & cells[i - 1])",
             lambda c, i: c[i - 1] ^ c[(i + 1) % n] ^ (c[i] & c[i - 1])),
        ])
        c = list(cells)
        for _ in range(t):
            c = [rule[1](c, i) for i in range(n)]
        if sum(c) in (0, n):
            return None, None
        expr = rule[0].replace("{n}", str(n))
        code = (f"cells = {cells}\nfor step in range({t}):\n    cells = [{expr} for i in range({n})]\n"
                f"print(\"\".join(str(c) for c in cells))\n")
        return code, "".join(map(str, c))
    if level == 4 and sub == 1:
        n, K = rng.randint(9, 11), rng.randint(5, 6)
        a = list(range(1, n + 1))
        for k in range(2, K):
            for i in range(0, len(a), k):
                a[i], a[-1 - i] = a[-1 - i], a[i]
            a = a[1:] + a[:1]
        code = (f"a = list(range(1, {n} + 1))\nfor k in range(2, {K}):\n    for i in range(0, len(a), k):\n"
                f"        a[i], a[-1 - i] = a[-1 - i], a[i]\n    a = a[1:] + a[:1]\nprint(a)\n")
        return code, str(a)
    if level == 5 and sub == 0:
        M = rng.choice([97, 101, 103])
        A, C, seed, T = rng.randint(5, 40), rng.randint(1, 60), rng.randint(1, 90), rng.randint(15, 18)
        x, q, score, pushes, pops = seed, [], 0, 0, 0
        for t in range(T):
            x = (A * x + C) % M
            if x % 3 == 0:
                q.append(x)
                pushes += 1
            elif q:
                score += q.pop(0) * (t % 4 + 1)
                pops += 1
            else:
                score -= 1
        if pushes < 4 or pops < 3:
            return None, None
        code = (f"x = {seed}\nqueue = []\nscore = 0\nfor t in range({T}):\n    x = ({A} * x + {C}) % {M}\n"
                f"    if x % 3 == 0:\n        queue.append(x)\n    elif queue:\n"
                f"        score += queue.pop(0) * (t % 4 + 1)\n    else:\n        score -= 1\n"
                f"print(score, len(queue), x)\n")
        return code, f"{score} {len(q)} {x}"
    if level == 5 and sub == 1:
        a0, b0, c0 = rng.randint(18, 26), rng.randint(3, 15), rng.randint(0, 5)
        m1, m2 = rng.randint(3, 5), rng.randint(3, 4)
        r2, d1, d2, e = rng.randint(0, m2 - 1), rng.randint(2, 3), rng.randint(1, 2), rng.randint(2, 7)
        a, b, c, it, branches = a0, b0, c0, 0, set()
        while a > 0:
            if (a + b) % m1 == 0:
                b = b * 2 - c
                a -= d1
                branches.add(0)
            elif b % m2 == r2:
                c = c + a
                a -= 1
                branches.add(1)
            else:
                b = b + e
                c = c - 1
                a -= d2
                branches.add(2)
            it += 1
            if b < 0 or c < 0 or b > 10 ** 6:
                return None, None
        if len(branches) < 3 or it < 12:
            return None, None
        code = (f"a, b, c = {a0}, {b0}, {c0}\nwhile a > 0:\n    if (a + b) % {m1} == 0:\n        b = b * 2 - c\n"
                f"        a = a - {d1}\n    elif b % {m2} == {r2}:\n        c = c + a\n        a = a - 1\n    else:\n"
                f"        b = b + {e}\n        c = c - 1\n        a = a - {d2}\nprint(a, b, c)\n")
        return code, f"{a} {b} {c}"
    raise ValueError


# --------------------------------------------------------------------------
# Family 5: novel-rule inference (unique within a depth<=3 grammar)
# --------------------------------------------------------------------------
def _pref(xs):
    out, s = [], 0
    for x in xs:
        s += x
        out.append(s)
    return out


def _runmax(xs):
    out, m = [], None
    for x in xs:
        m = x if m is None else max(m, x)
        out.append(m)
    return out


def _dedupe(xs):
    seen, out = set(), []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _swap_pairs(xs):
    out = list(xs)
    for i in range(0, len(xs) - 1, 2):
        out[i], out[i + 1] = out[i + 1], out[i]
    return out


PRIMS = {
    "reverse": lambda xs: xs[::-1],
    "sort_asc": lambda xs: sorted(xs),
    "sort_desc": lambda xs: sorted(xs, reverse=True),
    "rotl1": lambda xs: xs[1:] + xs[:1],
    "rotr1": lambda xs: xs[-1:] + xs[:-1],
    "rotl2": lambda xs: xs[2:] + xs[:2],
    "add1": lambda xs: [x + 1 for x in xs],
    "add2": lambda xs: [x + 2 for x in xs],
    "add3": lambda xs: [x + 3 for x in xs],
    "mul2": lambda xs: [2 * x for x in xs],
    "mul3": lambda xs: [3 * x for x in xs],
    "add_index": lambda xs: [x + i for i, x in enumerate(xs)],
    "prefix_sum": _pref,
    "running_max": _runmax,
    "diffs": lambda xs: [xs[i + 1] - xs[i] for i in range(len(xs) - 1)],
    "swap_pairs": _swap_pairs,
    "next_sum": lambda xs: [xs[i] + xs[(i + 1) % len(xs)] for i in range(len(xs))],
    "mod10": lambda xs: [x % 10 for x in xs],
    "drop_first": lambda xs: xs[1:],
    "drop_last": lambda xs: xs[:-1],
    "even_pos": lambda xs: xs[::2],
    "keep_even": lambda xs: [x for x in xs if x % 2 == 0],
    "keep_odd": lambda xs: [x for x in xs if x % 2 == 1],
    "dedupe": _dedupe,
    "double_odds": lambda xs: [2 * x if x % 2 else x for x in xs],
    "square": lambda xs: [x * x for x in xs],
}
SIMPLE = ["reverse", "sort_asc", "sort_desc", "rotl1", "rotr1", "add1", "add2", "add3", "mul2", "mul3", "drop_first"]
MEDIUM = ["add_index", "prefix_sum", "running_max", "diffs", "swap_pairs", "next_sum", "mod10", "even_pos",
          "keep_even", "keep_odd", "dedupe", "double_odds", "square", "rotl2", "drop_last"]
PNAMES = list(PRIMS)


def apply_chain(chain, xs):
    for p in chain:
        xs = PRIMS[p](list(xs))
    return list(xs)


def all_outputs(inp, maxdepth=3):
    """Map chain(tuple) -> output for every chain of length 1..maxdepth (memoised by prefix)."""
    res = {(): tuple(inp)}
    frontier = {(): tuple(inp)}
    for _ in range(maxdepth):
        nf = {}
        for ch, out in frontier.items():
            for p in PNAMES:
                nf[ch + (p,)] = tuple(PRIMS[p](list(out)))
        res.update(nf)
        frontier = nf
    return res


def gen_rule(rng, level, sub):
    n_ex = {1: 4, 2: 5, 3: 5, 4: 6, 5: 6}[level]
    for _ in range(4000):
        if level == 1:
            chain = [rng.choice(SIMPLE)]
        elif level == 2:
            chain = [rng.choice(MEDIUM)]
        elif level == 3:
            chain = [rng.choice(SIMPLE), rng.choice(MEDIUM)]
            rng.shuffle(chain)
        elif level == 4:
            chain = [rng.choice(MEDIUM), rng.choice(MEDIUM)]
        else:
            chain = [rng.choice(MEDIUM), rng.choice(SIMPLE + MEDIUM), rng.choice(MEDIUM)]
            rng.shuffle(chain)
        chain = tuple(chain)
        exs = []
        for _ in range(n_ex + 1):
            L = rng.randint(5, 8)
            exs.append([rng.randint(0, 12) for _ in range(L)])
        outs = [apply_chain(chain, e) for e in exs]
        if any(len(o) < 2 for o in outs) or any(o == e for o, e in zip(outs, exs)):
            continue
        if max(abs(v) for o in outs for v in o) > 400:
            continue
        # enumerate the grammar: every chain consistent with the examples must agree on the test input
        tables = [all_outputs(e) for e in exs]
        consistent = [ch for ch in tables[0] if ch and all(tables[k][ch] == tuple(outs[k]) for k in range(n_ex))]
        if chain not in consistent:
            continue
        test_outs = {tables[n_ex][ch] for ch in consistent}
        if len(test_outs) != 1:
            continue
        min_len = min(len(ch) for ch in consistent)
        if min_len != len(chain):
            continue  # a shorter rule explains the data; keep the ladder honest
        break
    else:
        raise RuntimeError("rule generation failed")
    ex_txt = "\n".join(f"{exs[k]} → {outs[k]}" for k in range(n_ex))
    prompt = (f"Each line below shows an input list of integers and the output list that a hidden rule produces from "
              f"it. The same rule is used on every line.\n{ex_txt}\n\nQuestion: what output does the rule produce "
              f"for the input {exs[n_ex]}?")
    return prompt, outs[n_ex], "intlist", "a list of integers in square brackets", {"chain": list(chain),
                                                                                         "n_consistent": len(consistent)}


# --------------------------------------------------------------------------
# Family 6: synthetic documents (answerable / contradictory / not determinable)
# --------------------------------------------------------------------------
GOODS = ["salt", "lamp oil", "copper wire", "flour", "rope", "tea", "nails", "soap", "wool", "dye"]
WHS = ["North Yard", "Harbor Shed", "Mill Loft", "East Depot", "Canal Store", "Bell Barn"]
ALIASES = ["Depot 4", "Unit 12", "Store B", "Bay 7", "Shed 3"]
NOISE = ["the loading crane at {w} was repaired.", "an inspector visited {w}; no goods moved.",
         "the gate lock at {w} was replaced.", "{w} was closed for half a day for cleaning."]
PALLET = 12


def reader_label(doc):
    """Independent symbolic reader. Returns ('value', v) | ('ND',) | ('CONTRA',).
    Applies all corrections (wherever they appear), tracks each stock as const + sum(unknowns),
    collects stocktake equations over the whole log, then solves for the queried pair at end of day D."""
    entries = doc["entries"]
    corr = {}
    for e in entries:
        if e["kind"] == "CORR":
            corr[e["ref"]] = e["qty"]
    stock = {}
    for (g, w), v in doc["opening"].items():
        stock[(g, w)] = (Fraction(v), {})
    eqs = {k: [] for k in stock}
    nvar = [0]
    snap = None
    g0, w0, D = doc["query"]

    def qty(e):
        q = corr.get(e["no"], e["qty"])
        return q * (PALLET if e.get("unit") == "pallet" else 1)

    def add(key, c, var=None):
        const, co = stock[key]
        co = dict(co)
        if var is not None:
            co[var] = co.get(var, 0) + 1
        stock[key] = (const + c, co)

    for e in entries:
        if snap is None and e["day"] > D:
            snap = stock[(g0, w0)]
        k = e["kind"]
        if k == "IN":
            add((e["good"], e["wh"]), qty(e))
        elif k == "OUT":
            add((e["good"], e["wh"]), -qty(e))
        elif k == "MOVE":
            add((e["good"], e["wh"]), -qty(e))
            add((e["good"], e["wh2"]), qty(e))
        elif k == "VAGUE":
            nvar[0] += 1
            add((e["good"], e["wh"]), 0, var=nvar[0])
        elif k == "COUNT":
            const, co = stock[(e["good"], e["wh"])]
            eqs[(e["good"], e["wh"])].append((dict(co), Fraction(e["qty"]) - const))
    if snap is None:
        snap = stock[(g0, w0)]

    def solve(eqlist, target):
        vars_ = sorted({v for co, _ in eqlist for v in co} | set(target[1]))
        rows = [[Fraction(co.get(v, 0)) for v in vars_] + [rhs] for co, rhs in eqlist]
        # gaussian elimination
        piv_cols = []
        r = 0
        for c in range(len(vars_)):
            pr = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
            if pr is None:
                continue
            rows[r], rows[pr] = rows[pr], rows[r]
            pv = rows[r][c]
            rows[r] = [x / pv for x in rows[r]]
            for i in range(len(rows)):
                if i != r and rows[i][c] != 0:
                    f = rows[i][c]
                    rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
            piv_cols.append(c)
            r += 1
        for row in rows[r:]:
            if all(x == 0 for x in row[:-1]) and row[-1] != 0:
                return ("CONTRA",)
        t = [Fraction(target[1].get(v, 0)) for v in vars_]
        val = target[0]
        for i, c in enumerate(piv_cols):
            if t[c] != 0:
                f = t[c]
                t = [a - f * b for a, b in zip(t, rows[i][:-1])]
                val += f * rows[i][-1]
        if any(x != 0 for x in t):
            return ("ND",)
        return ("value", val)

    for key, eql in eqs.items():
        if key != (g0, w0):
            res = solve(eql, (Fraction(0), {}))
            if res[0] == "CONTRA":
                return ("OTHER_CONTRA",)
    res = solve(eqs[(g0, w0)], snap)
    if res[0] == "value":
        assert res[1].denominator == 1
        return ("value", int(res[1]))
    return res


def gen_doc_once(rng, level, target):
    ng, nw, days, per_day, ncorr, alias, pallets = {
        1: (1, 1, 5, (1, 2), 0, False, False),
        2: (2, 2, 6, (1, 3), 0, False, False),
        3: (2, 2, 7, (2, 3), 1, False, False),
        4: (3, 3, 8, (2, 4), 2, True, False),
        5: (3, 3, 9, (3, 4), 2, True, True),
    }[level]
    goods = rng.sample(GOODS, ng)
    whs = rng.sample(WHS, nw)
    alias_of = {}
    if alias:
        w = rng.choice(whs)
        alias_of[w] = rng.choice(ALIASES)
    pairs = [(g, w) for g in goods for w in whs]
    opening = {p: rng.choice([0] + list(range(5, 60))) for p in pairs}
    truth = dict(opening)
    D = rng.randint(max(2, days // 2), days - 1)
    qpair = rng.choice(pairs)
    events = []  # (day, dict)

    def wname(w):
        if w in alias_of and rng.random() < 0.5:
            return alias_of[w]
        return w

    # style matching: the number of unrecorded deliveries and stocktakes is fixed per level, whatever the label
    n_vague = {1: 1, 2: 1, 3: 2, 4: 2, 5: 2}[level]
    n_count = {1: 2, 2: 2, 3: 3, 4: 4, 5: 5}[level]
    vague_days = sorted(rng.randint(1, days) for _ in range(n_vague))
    count_slots = sorted((rng.randint(1, days), rng.choice(pairs)) for _ in range(n_count))
    if len(set(count_slots)) < n_count:
        return None
    for day in range(1, days + 1):
        n = rng.randint(*per_day)
        todays = []
        for _ in range(n):
            g, w = rng.choice(pairs)
            r = rng.random()
            if r < 0.45 or (nw == 1 and r < 0.60):
                q = rng.randint(3, 40)
                unit = None
                if pallets and rng.random() < 0.4:
                    unit = "pallet"
                    q = rng.randint(1, 4)
                todays.append({"day": day, "kind": "IN", "good": g, "wh": w, "qty": q, "unit": unit})
            elif r < 0.75 and nw > 1:
                w2 = rng.choice([x for x in whs if x != w])
                todays.append({"day": day, "kind": "MOVE", "good": g, "wh": w, "wh2": w2, "qty": None})
            elif r < 0.88:
                todays.append({"day": day, "kind": "OUT", "good": g, "wh": w, "qty": None})
            else:
                todays.append({"day": day, "kind": "NOISE", "wh": w, "text": rng.choice(NOISE)})
        for vd in vague_days:
            if vd == day:
                g, w = rng.choice(pairs)
                todays.insert(rng.randint(0, len(todays)), {"day": day, "kind": "VAGUE", "good": g, "wh": w,
                                                            "qty": rng.randint(2, 30)})
        for e in todays:
            k = e["kind"]
            if k in ("IN", "VAGUE"):
                truth[(e["good"], e["wh"])] += e["qty"] * (PALLET if e.get("unit") == "pallet" else 1)
            elif k in ("OUT", "MOVE"):
                have = truth[(e["good"], e["wh"])]
                if have < 4:
                    e = {"day": day, "kind": "IN", "good": e["good"], "wh": e["wh"], "qty": rng.randint(3, 40),
                         "unit": None}
                    truth[(e["good"], e["wh"])] += e["qty"]
                else:
                    e["qty"] = rng.randint(1, have - 1)
                    truth[(e["good"], e["wh"])] -= e["qty"]
                    if k == "MOVE":
                        truth[(e["good"], e["wh2"])] += e["qty"]
            events.append(e)
        # stocktakes at end of day
        for cd, p in count_slots:
            if cd == day:
                events.append({"day": day, "kind": "COUNT", "good": p[0], "wh": p[1], "qty": truth[p]})
    kinds = [e["kind"] for e in events]
    assert kinds.count("VAGUE") == n_vague and kinds.count("COUNT") == n_count
    rep = dict(opening)
    for e in events:
        k = e["kind"]
        if k in ("IN", "VAGUE"):
            rep[(e["good"], e["wh"])] += e["qty"] * (PALLET if e.get("unit") == "pallet" else 1)
        elif k in ("OUT", "MOVE"):
            rep[(e["good"], e["wh"])] -= e["qty"]
            if k == "MOVE":
                rep[(e["good"], e["wh2"])] += e["qty"]
        elif k == "COUNT":
            assert rep[(e["good"], e["wh"])] == e["qty"]
        assert min(rep.values()) >= 0
    assert rep == truth
    # corrections: the logged quantity is wrong; a later CORRECTION gives the true one
    cand = [i for i, e in enumerate(events) if e["kind"] in ("IN", "OUT", "MOVE")]
    if len(cand) < ncorr + 2:
        return None
    for i in rng.sample(cand, ncorr):
        e = events[i]
        true_q = e["qty"]
        wrong = true_q + rng.choice([-1, 1]) * rng.randint(1, max(2, true_q // 2 if e.get("unit") != "pallet" else 1))
        if wrong <= 0 or wrong == true_q:
            wrong = true_q + rng.randint(1, 5) * (1 if e.get("unit") != "pallet" else 1)
        e["logged"] = wrong
        e["true"] = true_q
    # falsify a stocktake for CONTRA target
    if target == "CONTRA":
        cc = [i for i, e in enumerate(events) if e["kind"] == "COUNT" and (e["good"], e["wh"]) == qpair
              and e["day"] <= D]
        if not cc:
            return None
        i = rng.choice(cc)
        delta = rng.choice([-1, 1]) * rng.randint(2, 12)
        if events[i]["qty"] + delta < 0:
            delta = abs(delta)
        events[i]["qty"] += delta
        events[i]["falsified"] = True
    # number entries, place corrections later in the log
    entries = []
    for e in events:
        e = dict(e)
        e["no"] = len(entries) + 1
        if "logged" in e:
            e["qty_true"] = e["qty"]
            e["qty"] = e["logged"]
        entries.append(e)
    for e in list(entries):
        if "logged" in e:
            # insert the correction at a random later position; it takes the day of the entry before it
            p = rng.randint(entries.index(e) + 1, len(entries))
            ce = {"day": entries[p - 1]["day"], "kind": "CORR", "ref": e["no"], "qty": e["qty_true"],
                  "old": e["qty"], "unit": e.get("unit")}
            entries.insert(p, ce)
    # renumber, fixing references
    old2new = {}
    for k, e in enumerate(entries):
        if "no" in e:
            old2new[e["no"]] = k + 1
    for k, e in enumerate(entries):
        e["no"] = k + 1
    for e in entries:
        if e["kind"] == "CORR":
            e["ref"] = old2new[e["ref"]]
    for e in entries:
        if e["kind"] == "CORR":
            assert entries[e["ref"] - 1]["no"] < e["no"]
    # days must be non-decreasing
    assert all(entries[k]["day"] <= entries[k + 1]["day"] for k in range(len(entries) - 1)), "day order"
    doc = {"entries": entries, "opening": opening, "query": (qpair[0], qpair[1], D), "goods": goods, "whs": whs,
           "alias": alias_of, "pallets": pallets, "days": days}
    lab = reader_label(doc)
    # truth at end of D (for ANSWERABLE cross-check)
    tq = dict(opening)
    for e in entries:
        if e["day"] > D:
            break
        k = e["kind"]
        q = e.get("qty_true", e.get("qty"))
        if k in ("IN", "VAGUE"):
            tq[(e["good"], e["wh"])] += q * (PALLET if e.get("unit") == "pallet" else 1)
        elif k == "OUT":
            tq[(e["good"], e["wh"])] -= q
        elif k == "MOVE":
            tq[(e["good"], e["wh"])] -= q
            tq[(e["good"], e["wh2"])] += q
    doc["truth_at_D"] = tq[qpair]
    want = {"ANSWERABLE": "value", "ND": "ND", "CONTRA": "CONTRA"}[target]
    if lab[0] != want:
        return None
    if target == "ANSWERABLE":
        assert lab[1] == tq[qpair], (lab, tq[qpair])
        # style matching: answerable docs must still contain a VAGUE entry (decoy)
    if target == "ND":
        # the queried pair must actually have an unrecorded delivery on or before day D
        if not any(e["kind"] == "VAGUE" and (e["good"], e["wh"]) == qpair and e["day"] <= D for e in entries):
            return None
    # nobody may see an impossible stock (known-and-negative) in truthful docs; checked via truth >= 0
    doc["label"] = lab
    doc["wname_seed"] = rng.random()
    return doc


def render_doc(rng, doc, level):
    alias_of = doc["alias"]
    r2 = random.Random(doc["wname_seed"])

    def wn(w):
        if w in alias_of and r2.random() < 0.5:
            return alias_of[w]
        return w

    def q_str(q, unit):
        if unit == "pallet":
            return f"{q} pallet{'s' if q != 1 else ''}"
        return f"{q} crate{'s' if q != 1 else ''}"

    rules = ["Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry "
             "it names (the correction applies wherever it appears in the log).",
             "Stock changes only through the deliveries, shipments and transfers recorded here.",
             "Entries are in time order. A stocktake states the exact stock at the end of that day."]
    if doc["pallets"]:
        rules.append(f"One pallet holds exactly {PALLET} crates.")
    for w, a in alias_of.items():
        rules.append(f"{w} is also referred to as {a}.")
    op = "; ".join(f"{w}: " + ", ".join(f"{doc['opening'][(g, w)]} crates of {g}" for g in doc["goods"])
                   for w in doc["whs"])
    lines = []
    for e in doc["entries"]:
        k = e["kind"]
        pre = f"#{e['no']} Day {e['day']}:"
        if k == "IN":
            lines.append(f"{pre} {q_str(e['qty'], e.get('unit'))} of {e['good']} delivered to {wn(e['wh'])}.")
        elif k == "OUT":
            lines.append(f"{pre} {q_str(e['qty'], None)} of {e['good']} shipped out from {wn(e['wh'])}.")
        elif k == "MOVE":
            lines.append(f"{pre} {q_str(e['qty'], None)} of {e['good']} moved from {wn(e['wh'])} to {wn(e['wh2'])}.")
        elif k == "VAGUE":
            lines.append(f"{pre} a delivery of {e['good']} arrived at {wn(e['wh'])}; the number of crates was not "
                         f"recorded.")
        elif k == "NOISE":
            lines.append(f"{pre} " + e["text"].format(w=wn(e["wh"])))
        elif k == "COUNT":
            lines.append(f"{pre} stocktake: {wn(e['wh'])} holds {q_str(e['qty'], None)} of {e['good']}.")
        elif k == "CORR":
            lines.append(f"{pre} CORRECTION to entry #{e['ref']}: the quantity was {q_str(e['qty'], e.get('unit'))}, "
                         f"not {q_str(e['old'], e.get('unit'))}.")
    g, w, D = doc["query"]
    prompt = ("Read this stock log and answer the question.\n\nRules for reading the log:\n"
              + "\n".join(f"- {r}" for r in rules)
              + f"\n\nOpening stock (start of Day 1): {op}.\n\n" + "\n".join(lines)
              + f"\n\nQuestion: how many crates of {g} were in {w} at the end of Day {D}?\n"
              + "Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this "
                "number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to "
                "fix the number.")
    return prompt


def gen_doc(rng, level, target):
    for _ in range(200000):
        doc = gen_doc_once(rng, level, target)
        if doc is not None:
            break
    else:
        raise RuntimeError("doc gen failed")
    prompt = render_doc(rng, doc, level)
    lab = doc["label"]
    ans = lab[1] if lab[0] == "value" else ("CONTRADICTORY" if lab[0] == "CONTRA" else "NOT DETERMINABLE")
    fmt = "a whole number, or CONTRADICTORY, or NOT DETERMINABLE"
    return prompt, ans, "doc", fmt, {"doc_label": target, "n_entries": len(doc["entries"])}


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------
FAMILIES = [("exact-computation", "COMPUTE"), ("logic-grid", "LOGIC"), ("string-trace", "TRACE"),
            ("program-output", "PROGRAM"), ("rule-inference", "RULE"), ("stock-log", "DOC")]


def main():
    seed = int(sys.argv[1])
    out_pub, out_key = sys.argv[2], sys.argv[3]
    rng = random.Random(seed)
    raw = []
    doc_targets = ["ANSWERABLE"] * 4 + ["CONTRA"] * 3 + ["ND"] * 3
    rng.shuffle(doc_targets)
    for fam, code in FAMILIES:
        k = 0
        for level in LEVELS:
            for sub in (0, 1):
                irng = random.Random(rng.getrandbits(64))
                if code == "COMPUTE":
                    r = gen_compute(irng, level, sub)
                elif code == "LOGIC":
                    r = gen_logic(irng, level, sub)
                elif code == "TRACE":
                    r = gen_trace(irng, level, sub)
                elif code == "PROGRAM":
                    r = gen_prog(irng, level, sub)
                elif code == "RULE":
                    r = gen_rule(irng, level, sub)
                elif code == "DOC":
                    r = gen_doc(irng, level, doc_targets[k])
                prompt, ans, atype, fmt, meta = r
                raw.append({"family": fam, "level": level, "sub": sub, "prompt": prompt, "answer": ans,
                            "atype": atype, "answer_format": fmt, "meta": meta})
                k += 1
                print(f"  {fam:18s} L{level}{'ab'[sub]} ok", file=sys.stderr)
    # blind twins: 15 of 60 (25%); 2-3 per family, on distinct levels
    fams = [f for f, _ in FAMILIES]
    n_tw = {f: 2 for f in fams}
    for f in rng.sample(fams, 3):
        n_tw[f] = 3
    for f in fams:
        lv = rng.sample(LEVELS, n_tw[f])
        for L in lv:
            cand = [it for it in raw if it["family"] == f and it["level"] == L]
            rng.choice(cand)["set"] = "twin"
    for it in raw:
        it.setdefault("set", "forecast")
    assert sum(it["set"] == "twin" for it in raw) == 15
    # presentation order and IDs
    rng.shuffle(raw)
    for i, it in enumerate(raw):
        it["id"] = f"Q{i + 1:02d}"
    fc = [it for it in raw if it["set"] == "forecast"]
    rng.shuffle(fc)
    blocks = {"A": sorted(it["id"] for it in fc[0:15]), "B": sorted(it["id"] for it in fc[15:30]),
              "C": sorted(it["id"] for it in fc[30:45])}
    for b, ids in blocks.items():
        for it in raw:
            if it["id"] in ids:
                it["block"] = b
    for it in raw:
        it.setdefault("block", None)

    # ---------------- public files ----------------
    pub_items = [{"id": it["id"], "family": it["family"], "prompt": it["prompt"],
                  "answer_format": it["answer_format"]} for it in raw]
    phase1 = {"triage_k": 5, "blocks": blocks,
              "forecast_items": sorted(i for ids in blocks.values() for i in ids)}
    with open(os.path.join(out_pub, "items.json"), "w") as f:
        json.dump({"pilot": "F5 Self-Knowledge Exam pilot", "n_items": len(raw), "phase1": phase1,
                   "items": pub_items}, f, indent=1, ensure_ascii=False)
    md = ["# F5 pilot: items", "",
          f"{len(raw)} items, Q01 to Q{len(raw)}. `items.json` holds the same content in machine-readable form.", "",
          "## Phase 1 lists", "",
          "Forecast items, grouped into three triage blocks of 15. In each block you will choose exactly 5.", ""]
    for b, ids in blocks.items():
        md.append(f"- **Block {b}:** " + ", ".join(ids))
    md += ["", "Items that appear in no block are not forecast in Phase 1. Every item (all "
           f"{len(raw)}) is attempted in Phase 2.", "", "---", ""]
    for it in raw:
        md.append(f"## {it['id']} · family: {it['family']}")
        md.append("")
        md.append(it["prompt"])
        md.append("")
        md.append(f"**Answer format:** {it['answer_format']}")
        md.append("")
        md.append("---")
        md.append("")
    with open(os.path.join(out_pub, "items.md"), "w") as f:
        f.write("\n".join(md))

    # ---------------- key ----------------
    key = {"pilot": "F5 Self-Knowledge Exam pilot", "seed": seed, "triage_k": 5, "blocks": blocks,
           "items": {it["id"]: {"family": it["family"], "level": it["level"], "sub": it["sub"], "set": it["set"],
                                "block": it["block"], "atype": it["atype"], "answer": it["answer"],
                                "doc_label": it["meta"].get("doc_label"), "prompt_chars": len(it["prompt"]),
                                "meta": it["meta"]} for it in raw}}
    with open(os.path.join(out_key, "key.json"), "w") as f:
        json.dump(key, f, indent=1, ensure_ascii=False)
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
