#!/usr/bin/env python3
"""Independent verification of the F5 pilot answer key (SEALED).

Re-derives every answer by parsing the PUBLIC item text only (no generator internals) with
different algorithms from generate.py, then compares with key.json.
Usage: python3 verify.py PUBLIC_ITEMS_JSON KEY_JSON
"""
import io, itertools, json, math, re, sys, contextlib


def v_compute(p):
    m = re.fullmatch(r"Compute (\d+) × (\d+)\.", p)
    if m:
        return int(m[1]) * int(m[2])
    m = re.fullmatch(r"Compute the greatest common divisor of (\d+) and (\d+)\.", p)
    if m:
        a, b = int(m[1]), int(m[2])
        while b:
            a, b = b, a % b
        return a
    m = re.match(r"Compute the remainder when (\d+)\^(\d+) .* divided by (\d+)\.", p)
    if m:
        return (int(m[1]) ** int(m[2])) % int(m[3])
    m = re.fullmatch(r"How many integers n with 1 ≤ n ≤ (\d+) are divisible by none of (\d+), (\d+) and (\d+)\?", p)
    if m:
        N, ps = int(m[1]), [int(m[2]), int(m[3]), int(m[4])]
        tot = 0
        for r in range(4):
            for c in itertools.combinations(ps, r):
                tot += (-1) ** r * (N // math.prod(c))
        return tot
    m = re.match(r"Compute the sum of all positive divisors of (\d+) ", p)
    if m:
        n, s, d = int(m[1]), 1, 2
        while d * d <= n:
            if n % d == 0:
                e = 0
                while n % d == 0:
                    n //= d
                    e += 1
                s *= (d ** (e + 1) - 1) // (d - 1)
            d += 1
        if n > 1:
            s *= n + 1
        return s
    m = re.match(r"A path goes from \(0,0\) to \((\d+),(\d+)\)", p)
    if m:
        M, N = int(m[1]), int(m[2])
        diag = "never visits a point with y > x" in p
        pts = re.search(r"none of the points (.*)\?", p)[1]
        forb = {(int(a), int(b)) for a, b in re.findall(r"\((\d+),(\d+)\)", pts)}
        # recursive count with memo (different from the generator's table DP)
        from functools import lru_cache

        @lru_cache(None)
        def f(x, y):
            if (x, y) in forb or x > M or y > N or (diag and y > x):
                return 0
            if (x, y) == (M, N):
                return 1
            return f(x + 1, y) + f(x, y + 1)
        return f(0, 0)
    raise ValueError("unparsed compute: " + p)


def v_trace(p):
    if p.startswith("Start with the string"):
        s = list(re.match(r"Start with the string (\w+)\.", p)[1])
        for line in re.findall(r"^\d+\. (.*)$", p, re.M):
            m = re.fullmatch(r"Swap the letters in positions (\d+) and (\d+)\.", line)
            if m:
                i, j = int(m[1]) - 1, int(m[2]) - 1
                s[i], s[j] = s[j], s[i]
                continue
            m = re.fullmatch(r"Swap the letters (\w) and (\w) \(wherever they currently are\)\.", line)
            if m:
                s = [m[2] if c == m[1] else m[1] if c == m[2] else c for c in s]
                continue
            m = re.fullmatch(r"Rotate (left|right) by (\d+) steps?\.", line)
            if m:
                for _ in range(int(m[2])):
                    s = s[1:] + s[:1] if m[1] == "left" else s[-1:] + s[:-1]
                continue
            m = re.fullmatch(r"Reverse the letters in positions (\d+) through (\d+)\.", line)
            if m:
                i, j = int(m[1]) - 1, int(m[2]) - 1
                while i < j:
                    s[i], s[j] = s[j], s[i]
                    i, j = i + 1, j - 1
                continue
            m = re.fullmatch(r"Remove the letter in position (\d+) and reinsert it so that it ends up in position (\d+)\.",
                             line)
            if m:
                i, j = int(m[1]) - 1, int(m[2]) - 1
                c = s[i]
                del s[i]
                s = s[:j] + [c] + s[j:]
                assert s[j] == c
                continue
            raise ValueError(line)
        return "".join(s)
    s = re.search(r"starts from the string (\w+) ", p)[1]
    rules = []
    for l, r in re.findall(r"^Rule \d+: (\w+) → (.*)$", p, re.M):
        rules.append((l, "" if r == "(empty string)" else r))
    T = int(re.search(r"after exactly (\d+) steps", p)[1])
    for _ in range(T):
        for l, r in rules:
            m = re.search(re.escape(l), s)
            if m:
                s = s[:m.start()] + r + s[m.end():]
                break
        else:
            raise ValueError("halted")
    return s


def v_prog(p):
    code = re.search(r"```python\n(.*)```", p, re.S)[1]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})
    return buf.getvalue().strip()


# ---- rule inference: re-implemented primitive library, uniqueness re-checked ----
def _p(xs):
    return [sum(xs[:i + 1]) for i in range(len(xs))]


LIB = {
    "reverse": lambda x: list(reversed(x)), "sort_asc": lambda x: sorted(x),
    "sort_desc": lambda x: sorted(x)[::-1], "rotl1": lambda x: x[1:] + x[:1], "rotr1": lambda x: x[-1:] + x[:-1],
    "rotl2": lambda x: x[2:] + x[:2], "add1": lambda x: [v + 1 for v in x], "add2": lambda x: [v + 2 for v in x],
    "add3": lambda x: [v + 3 for v in x], "mul2": lambda x: [v * 2 for v in x], "mul3": lambda x: [v * 3 for v in x],
    "add_index": lambda x: [v + i for i, v in enumerate(x)], "prefix_sum": _p,
    "running_max": lambda x: [max(x[:i + 1]) for i in range(len(x))],
    "diffs": lambda x: [b - a for a, b in zip(x, x[1:])],
    "swap_pairs": lambda x: [x[i ^ 1] if (i ^ 1) < len(x) else x[i] for i in range(len(x))],
    "next_sum": lambda x: [x[i] + x[(i + 1) % len(x)] for i in range(len(x))] if x else [],
    "mod10": lambda x: [v % 10 for v in x], "drop_first": lambda x: x[1:], "drop_last": lambda x: x[:-1],
    "even_pos": lambda x: [v for i, v in enumerate(x) if i % 2 == 0],
    "keep_even": lambda x: [v for v in x if v % 2 == 0], "keep_odd": lambda x: [v for v in x if v % 2],
    "dedupe": lambda x: [v for i, v in enumerate(x) if v not in x[:i]],
    "double_odds": lambda x: [v * 2 if v % 2 else v for v in x], "square": lambda x: [v * v for v in x],
}


def v_rule(p):
    exs = [(json.loads(a), json.loads(b)) for a, b in re.findall(r"^(\[.*?\]) → (\[.*?\])$", p, re.M)]
    test = json.loads(re.search(r"for the input (\[.*?\])\?", p)[1])
    answers = set()
    for d in (1, 2, 3):
        for chain in itertools.product(LIB, repeat=d):
            ok = True
            for a, b in exs:
                x = a
                for f in chain:
                    x = LIB[f](x)
                if x != b:
                    ok = False
                    break
            if ok:
                x = test
                for f in chain:
                    x = LIB[f](x)
                answers.add(tuple(x))
    assert len(answers) == 1, ("rule not unique", len(answers))
    return list(answers.pop())


# ---- logic grids: parse the English clues, brute-force all assignments ----
def v_logic(p):
    N = int(re.match(r"(\d+) people", p)[1])
    vals = {}
    for a, vs in re.findall(r"(\w+)s: ([\w ,]+?)(?:;|\. )", p.split("The possible values are: ")[1].split('"')[0]):
        vals[a] = [v.strip() for v in vs.split(",")]
    attrs = list(vals)
    player = {"violinist": "violin", "cellist": "cello", "flautist": "flute", "harpist": "harp", "drummer": "drums",
              "pianist": "piano", "oboist": "oboe", "banjo player": "banjo"}

    def parse_np(s):
        s = s.strip()
        s = s[0].lower() + s[1:] if not s.startswith(tuple(vals.get("name", []))) else s
        if s in vals.get("name", []):
            return ("name", s)
        m = re.fullmatch(r"the (\w+) owner", s)
        if m:
            return ("pet", m[1])
        m = re.fullmatch(r"the (\w+) drinker", s)
        if m:
            return ("drink", m[1])
        m = re.fullmatch(r"the resident of the (\w+) house", s)
        if m:
            return ("colour", m[1])
        m = re.fullmatch(r"the (.+)", s)
        if m and m[1] in player:
            return ("instrument", player[m[1]])
        raise ValueError("np: " + s)

    def parse_vp(s):
        for pat, attr in [(r"is (not )?(\w+)", "name"), (r"(does not own|owns) the (\w+)", "pet"),
                          (r"(does not drink|drinks) (\w+)", "drink"),
                          (r"(does not live|lives) in the (\w+) house", "colour"),
                          (r"(does not play|plays) the (\w+)", "instrument")]:
            m = re.fullmatch(pat, s)
            if m:
                neg = bool(m[1]) and m[1].startswith(("not", "does not"))
                return (attr, m[2]), neg
        raise ValueError("vp: " + s)

    clues = []
    for line in re.findall(r"^\d+\. (.*)\.$", p, re.M):
        m = re.fullmatch(r"(.+?) lives in house (\d+)", line)
        if m:
            clues.append(("pos", parse_np(m[1]), int(m[2])))
            continue
        m = re.fullmatch(r"(.+?) does not live in house (\d+)", line)
        if m:
            clues.append(("notpos", parse_np(m[1]), int(m[2])))
            continue
        m = re.fullmatch(r"(.+?) lives in one of the two end houses", line)
        if m:
            clues.append(("ends", parse_np(m[1])))
            continue
        m = re.fullmatch(r"(.+?) lives directly to the left of (.+)", line)
        if m:
            clues.append(("leftimm", parse_np(m[1]), parse_np(m[2])))
            continue
        m = re.fullmatch(r"(.+?) lives somewhere to the left of (.+)", line)
        if m:
            clues.append(("left", parse_np(m[1]), parse_np(m[2])))
            continue
        m = re.fullmatch(r"(.+?) does not live next to (.+)", line)
        if m:
            clues.append(("notnext", parse_np(m[1]), parse_np(m[2])))
            continue
        m = re.fullmatch(r"(.+?) lives next to (.+)", line)
        if m:
            clues.append(("next", parse_np(m[1]), parse_np(m[2])))
            continue
        # same / notsame: split NP and VP at the first verb
        m = re.fullmatch(r"(.+?) ((?:is|owns|drinks|lives|plays|does not) .+)", line)
        if m:
            x = parse_np(m[1])
            y, neg = parse_vp(m[2])
            clues.append(("notsame" if neg else "same", x, y))
            continue
        raise ValueError("clue: " + line)

    def holds(c, pos):
        t = c[0]
        if t == "pos":
            return pos[c[1]] == c[2]
        if t == "notpos":
            return pos[c[1]] != c[2]
        if t == "ends":
            return pos[c[1]] in (1, N)
        x, y = pos[c[1]], pos[c[2]]
        return {"same": x == y, "notsame": x != y, "leftimm": x + 1 == y, "left": x < y,
                "next": abs(x - y) == 1, "notnext": abs(x - y) != 1}[t]

    def attrs_of(c):
        return {c[1][0]} | ({c[2][0]} if len(c) > 2 and isinstance(c[2], tuple) else set())

    sols = []
    perms = list(itertools.permutations(range(1, N + 1)))

    def rec(k, pos):
        if k == len(attrs):
            sols.append(dict(pos))
            return
        a = attrs[k]
        done = set(attrs[:k + 1])
        relevant = [c for c in clues if a in attrs_of(c) and attrs_of(c) <= done]
        for pm in perms:
            for v, h in zip(vals[a], pm):
                pos[(a, v)] = h
            if all(holds(c, pos) for c in relevant):
                rec(k + 1, pos)
        for v in vals[a]:
            pos.pop((a, v), None)

    rec(0, {})
    assert len(sols) == 1, len(sols)
    ask = re.search(r"list the (\w+)s in house order", p)[1]
    inv = {h: v for (a, v), h in sols[0].items() if a == ask}
    return [inv[h] for h in range(1, N + 1)]


# ---- stock logs: parse text, enumerate unrecorded quantities, enforce non-negativity ----
def v_doc(p):
    alias = dict((b, a) for a, b in re.findall(r"^- (.+) is also referred to as (.+)\.$", p, re.M))
    pallet = int(re.search(r"One pallet holds exactly (\d+) crates", p)[1]) if "pallet holds" in p else None

    def W(x):
        return alias.get(x, x)

    def Q(n, unit):
        return int(n) * (pallet if unit.startswith("pallet") else 1)

    opening = {}
    op = re.search(r"Opening stock \(start of Day 1\): (.*)\.\n", p)[1]
    for part in op.split("; "):
        w, rest = part.split(": ", 1)
        for n, g in re.findall(r"(\d+) crates of ([\w ]+)", rest):
            opening[(g.strip(), w)] = int(n)
    entries = []
    for no, day, body in re.findall(r"^#(\d+) Day (\d+): (.*)$", p, re.M):
        no, day = int(no), int(day)
        m = re.fullmatch(r"(\d+) (crates?|pallets?) of (.+) delivered to (.+)\.", body)
        if m:
            entries.append([no, day, "IN", m[3], W(m[4]), None, int(m[1]), m[2]])
            continue
        m = re.fullmatch(r"(\d+) (crates?) of (.+) shipped out from (.+)\.", body)
        if m:
            entries.append([no, day, "OUT", m[3], W(m[4]), None, int(m[1]), m[2]])
            continue
        m = re.fullmatch(r"(\d+) (crates?) of (.+) moved from (.+) to (.+)\.", body)
        if m:
            entries.append([no, day, "MOVE", m[3], W(m[4]), W(m[5]), int(m[1]), m[2]])
            continue
        m = re.fullmatch(r"a delivery of (.+) arrived at (.+); the number of crates was not recorded\.", body)
        if m:
            entries.append([no, day, "VAGUE", m[1], W(m[2]), None, None, "crates"])
            continue
        m = re.fullmatch(r"stocktake: (.+) holds (\d+) crates? of (.+)\.", body)
        if m:
            entries.append([no, day, "COUNT", m[3], W(m[1]), None, int(m[2]), "crates"])
            continue
        m = re.fullmatch(r"CORRECTION to entry #(\d+): the quantity was (\d+) (crates?|pallets?), not .*\.", body)
        if m:
            entries.append([no, day, "CORR", None, None, None, (int(m[1]), int(m[2])), m[3]])
            continue
        entries.append([no, day, "NOISE", None, None, None, None, None])
    for e in entries:
        if e[2] == "CORR":
            ref, q = e[6]
            tgt = next(x for x in entries if x[0] == ref)
            assert tgt[7].rstrip("s") == e[7].rstrip("s")
            tgt[6] = q
    g0, w0, D = re.search(r"how many crates of (.+) were in (.+) at the end of Day (\d+)\?", p).groups()
    D = int(D)
    vag = [e for e in entries if e[2] == "VAGUE"]
    results = set()
    for us in itertools.product(range(1, 81), repeat=len(vag)):
        uq = {id(e): u for e, u in zip(vag, us)}
        st = dict(opening)
        at_D = None
        ok = True
        for e in entries:
            if at_D is None and e[1] > D:
                at_D = st[(g0, w0)]
            k = e[2]
            if k == "IN":
                st[(e[3], e[4])] += Q(e[6], e[7])
            elif k == "VAGUE":
                st[(e[3], e[4])] += uq[id(e)]
            elif k == "OUT":
                st[(e[3], e[4])] -= e[6]
            elif k == "MOVE":
                st[(e[3], e[4])] -= e[6]
                st[(e[3], e[5])] += e[6]
            elif k == "COUNT":
                if st[(e[3], e[4])] != e[6]:
                    ok = False
                    break
            if any(v < 0 for v in st.values()):
                ok = False
                break
        if at_D is None:
            at_D = st[(g0, w0)]
        if ok:
            results.add(at_D)
    if not results:
        return "CONTRADICTORY"
    if len(results) == 1:
        return results.pop()
    return "NOT DETERMINABLE"


def main():
    items = json.load(open(sys.argv[1]))
    key = json.load(open(sys.argv[2]))["items"]
    bad = 0
    for it in items["items"]:
        fam, p = it["family"], it["prompt"]
        f = {"exact-computation": v_compute, "string-trace": v_trace, "program-output": v_prog,
             "rule-inference": v_rule, "logic-grid": v_logic, "stock-log": v_doc}[fam]
        got = f(p)
        want = key[it["id"]]["answer"]
        ok = got == want
        bad += not ok
        print(f"{it['id']} {fam:18s} L{key[it['id']]['level']} {'OK ' if ok else 'MISMATCH'}"
              + ("" if ok else f" got={got!r} key={want!r}"))
    print("MISMATCHES:", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
