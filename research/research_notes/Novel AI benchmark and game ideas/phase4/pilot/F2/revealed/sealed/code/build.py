"""F2 Hidden-Rule Lab static pilot -- problem builder.

For each hidden rule R* (cost c*):
  1. build a label-balanced pool of random scenes + single-edit 'near-miss' mutants;
  2. enumerate the grammar (dedup on the pool) up to cost c*+1;
  3. pick 8 test scenes: 3 'shortcut-separating' (R* disagrees with many simple rules that agree with R*
     on >=75% of the pool), 2 near-miss mutants, 3 random; 3-5 of them fit;
  4. pick 12 examples (6 fit / 6 not) by greedy set cover so that EVERY grammar rule of cost <= c*
     that fits all 12 examples gives the same labels as R* on the 8 tests (bounded adversary, delta=0);
     leftover slots greedily remove cost c*+1 rules that disagree on tests (delta=+1 robustness);
  5. shortcut filter: reject the attempt if a generic count-feature decision stump (baselines.COUNT_STUMP),
     trained on the 12 examples, gets >= 6 of the 8 tests right (declared construction filter);
  6. record the consistency report.
Usage: python3 build.py <master_seed> <public_dir> <sealed_dir>
"""
import sys, os, json, random, time
import numpy as np
from world import (random_scene, mutate, canon, copy_scene, render_examples_sheet, render_tests_sheet)
from grammar import arrays, RuleSet
from baselines import feats, stump

STUMP_MAX = 5   # construction filter: reject test/example sets on which the count-feature stump gets >= 6/8

# ---------------------------------------------------------------- hidden rules (independent direct implementations)
def objs(sc):
    for st in sc:
        for lv, o in enumerate(st["objs"]):
            yield st, lv, o


def r_large_yellow(sc):
    return any(o[2] == "large" and o[1] == "yellow" for _, _, o in objs(sc))


def r_more_red_than_blue(sc):
    cols = [o[1] for _, _, o in objs(sc)]
    return cols.count("red") > cols.count("blue")


def r_circles_left_of_triangles(sc):
    cs = [st["slot"] for st, _, o in objs(sc) if o[0] == "circle"]
    ts = [st["slot"] for st, _, o in objs(sc) if o[0] == "triangle"]
    return all(c < t for c in cs for t in ts)


def r_odd_total(sc):
    return sum(len(st["objs"]) for st in sc) % 2 == 1


def r_triangle_on_blue(sc):
    return all(lv >= 1 and st["objs"][lv - 1][1] == "blue" for st, lv, o in objs(sc) if o[0] == "triangle")


def r_no_large_on_small(sc):
    return not any(lv >= 1 and o[2] == "large" and st["objs"][lv - 1][2] == "small" for st, lv, o in objs(sc))


def r_every_stack_yellow(sc):
    return all(any(o[1] == "yellow" for o in st["objs"]) for st in sc)


def r_large_square_supports_small(sc):
    return all(lv + 1 < len(st["objs"]) and st["objs"][lv + 1][2] == "small"
               for st, lv, o in objs(sc) if o[0] == "square" and o[2] == "large")


RULES = [
    dict(id="R1", family="attribute conjunction (existential)", cost=3, fn=r_large_yellow,
         text="There is at least one large yellow object.", grammar="exists large&yellow"),
    dict(id="R2", family="count comparison", cost=4, fn=r_more_red_than_blue,
         text="There are more red objects than blue objects.", grammar="count(red)>count(blue)"),
    dict(id="R3", family="relative position (universal, pairwise)", cost=4, fn=r_circles_left_of_triangles,
         text="Every circle is in a stack to the left of every triangle (vacuously true if there are no circles or no triangles).",
         grammar="every circle left_of every triangle"),
    dict(id="R4", family="parity of a count", cost=2, fn=r_odd_total,
         text="The total number of objects is odd.", grammar="count(object) odd"),
    dict(id="R5", family="universal support relation", cost=4, fn=r_triangle_on_blue,
         text="Every triangle rests directly on a blue object (vacuously true if there are no triangles).",
         grammar="every triangle on some blue"),
    dict(id="R6", family="forbidden support relation (size)", cost=4, fn=r_no_large_on_small,
         text="No large object rests directly on a small object.", grammar="no large on any small"),
    dict(id="R7", family="per-stack quantification", cost=3, fn=r_every_stack_yellow,
         text="Every stack contains at least one yellow object.", grammar="every stack contains yellow"),
    dict(id="R8", family="compositional relational (conjunctive concept + support)", cost=5, fn=r_large_square_supports_small,
         text="Every large square has a small object resting directly on top of it (vacuously true if there are no large squares).",
         grammar="every large&square under some small"),
]


# ---------------------------------------------------------------- pool
def make_pool(fn, rng, n_each=900, max_draw=400000):
    seen = set()
    rand = {True: [], False: []}
    draws = 0
    while (len(rand[True]) < n_each or len(rand[False]) < n_each) and draws < max_draw:
        sc = random_scene(rng); draws += 1
        k = canon(sc)
        if k in seen:
            continue
        lab = fn(sc)
        if len(rand[lab]) < n_each:
            rand[lab].append(sc); seen.add(k)
    mut = {True: [], False: []}
    base = rand[True] + rand[False]
    draws = 0
    while (len(mut[True]) < n_each or len(mut[False]) < n_each) and draws < max_draw:
        sc = rng.choice(base); draws += 1
        for _ in range(rng.choice([1, 1, 2])):
            m = mutate(sc, rng)
            if m is None:
                break
            sc = m
        k = canon(sc)
        if k in seen:
            continue
        lab = fn(sc)
        if len(mut[lab]) < n_each:
            mut[lab].append(sc); seen.add(k)
    pool = rand[True] + rand[False] + mut[True] + mut[False]
    kind = ["random"] * (len(rand[True]) + len(rand[False])) + ["mutant"] * (len(mut[True]) + len(mut[False]))
    return pool, np.array(kind)


def colsums(RS, rows, t, cols):
    """number of rules in `rows` that disagree with truth t on each scene in cols"""
    out = np.zeros(len(cols), np.int64)
    for s in range(0, len(rows), 20000):
        X = RS.matrix(rows[s:s + 20000])
        out += (X[:, cols] != t[cols][None]).sum(0)
    return out


def disagree_rows(RS, rows, t, cols):
    """subset of rows that disagree with t on at least one of cols"""
    keep = []
    for s in range(0, len(rows), 20000):
        X = RS.matrix(rows[s:s + 20000])
        keep.append(rows[s:s + 20000][(X[:, cols] != t[cols][None]).any(1)])
    return np.concatenate(keep) if keep else np.array([], int)


def build_problem(rule, rng, log):
    t0 = time.time()
    pool, kind = make_pool(rule["fn"], rng)
    t = np.array([rule["fn"](s) for s in pool])
    A = arrays(pool)
    cstar = rule["cost"]
    RS = RuleSet(A, cstar + 1)
    found = RS.cost_of(t)
    assert found is not None and found[0] <= cstar, (rule["id"], found)
    le = np.where(RS.costs <= cstar)[0]
    nxt = np.where(RS.costs == cstar + 1)[0]
    # agreement of every cost<=c* rule with truth, for shortcut selection
    agree = np.zeros(len(le))
    for s in range(0, len(le), 20000):
        X = RS.matrix(le[s:s + 20000]); agree[s:s + 20000] = (X == t[None]).mean(1)
    short = le[(agree >= 0.75) & (agree < 1.0)]
    allcols = np.arange(len(pool))
    sc_short = colsums(RS, short, t, allcols) if len(short) else np.zeros(len(pool))
    best = None
    for attempt in range(150):
        n_fit = rng.choice([3, 4, 5])
        cats = ["short"] * 3 + ["near"] * 2 + ["rand"] * 3
        labs = [True] * n_fit + [False] * (8 - n_fit)
        rng.shuffle(labs)
        tests = []
        for cat, lab in zip(cats, labs):
            if cat == "short":
                cand = np.where((t == lab))[0]
                cand = cand[np.argsort(-sc_short[cand])][:max(20, len(cand) // 25)]
            elif cat == "near":
                cand = np.where((t == lab) & (kind == "mutant"))[0]
            else:
                cand = np.where((t == lab) & (kind == "random"))[0]
            cand = [c for c in cand if c not in tests]
            tests.append(int(rng.choice(cand)))
        tests_arr = np.array(tests)
        K = disagree_rows(RS, le, t, tests_arr)
        K1 = disagree_rows(RS, nxt, t, tests_arr)
        tset = set(tests)
        cand_cols = np.array([i for i in allcols if i not in tset])
        quota = {True: 6, False: 6}
        ex = []
        rem, rem1 = K, K1
        for step in range(12):
            allowed = np.array([quota[bool(t[c])] > 0 for c in cand_cols])
            cols = cand_cols[allowed]
            if len(rem):
                score = colsums(RS, rem, t, cols).astype(float)
                if len(rem1):
                    score += 1e-6 * colsums(RS, rem1, t, cols)
            elif len(rem1):
                score = colsums(RS, rem1, t, cols).astype(float)
            else:
                score = (kind[cols] == "random").astype(float)   # nothing left to kill: add a typical scene
            score += np.array([rng.random() for _ in cols]) * 1e-9
            j = int(cols[np.argmax(score)])
            ex.append(j); quota[bool(t[j])] -= 1
            cand_cols = cand_cols[cand_cols != j]
            if len(rem):
                X = RS.matrix(rem); rem = rem[X[:, j] == t[j]]
            if len(rem1):
                X = RS.matrix(rem1); rem1 = rem1[X[:, j] == t[j]]
        # shortcut-learner filter: a generic count-feature stump trained on the 12 examples
        exf = [pool[i] for i in ex]
        Fx = np.array([feats(sc) for sc in exf]); ytr = np.array([bool(t[i]) for i in ex])
        Ft = np.array([feats(pool[i]) for i in tests])
        stump_correct = int((stump(Fx, ytr, Ft) == t[tests_arr]).sum())
        res = dict(tests=tests, examples=ex, n_fit=n_fit, left0=len(rem), left1=len(rem1), K=len(K), K1=len(K1),
                   stump_correct=stump_correct, attempts=attempt + 1)
        keyf = lambda r: (r["left0"], r["stump_correct"] > STUMP_MAX, r["left1"])
        if best is None or keyf(res) < keyf(best):
            best = res
        if res["left0"] == 0 and res["stump_correct"] <= STUMP_MAX and res["left1"] == 0:
            break
        if best["left0"] == 0 and best["stump_correct"] <= STUMP_MAX and attempt >= 30:
            break
    # ----- consistency report on the final choice
    ex, tests = np.array(best["examples"]), np.array(best["tests"])
    report = {}
    for label, rows in (("delta0_cost_le_cstar", le), ("delta1_cost_eq_cstar_plus1", nxt)):
        X = RS.matrix(rows)
        cons = rows[(X[:, ex] == t[ex][None]).all(1)]
        Xc = RS.matrix(cons)
        errs = (Xc[:, tests] != t[tests][None]).sum(1) if len(cons) else np.zeros(0, int)
        report[label] = dict(consistent_rules=int(len(cons)),
                             consistent_rules_disagreeing_on_tests=int((errs > 0).sum()),
                             max_test_errors_any_consistent_rule=int(errs.max()) if len(errs) else 0,
                             examples_of_disagreeing=[RS.descs[r] for r in cons[errs > 0][:5]])
    X = RS.matrix(le); cons = le[(X[:, ex] == t[ex][None]).all(1)]
    report["min_cost_consistent"] = int(RS.costs[cons].min())
    report["simplest_consistent_rules"] = [RS.descs[r] for r in cons[RS.costs[cons] == RS.costs[cons].min()][:10]]
    report["true_rule_min_cost_on_pool"] = found[0]
    report["true_rule_equivalent_desc"] = found[1]
    report["n_rules_enumerated"] = int(len(RS.costs))
    report["n_shortcut_rules"] = int(len(short))
    report["attempt_result"] = {k: best[k] for k in ("n_fit", "left0", "left1", "K", "K1", "stump_correct", "attempts")}
    report["build_seconds"] = round(time.time() - t0, 1)
    fits = [pool[i] for i in ex if t[i]]
    nots = [pool[i] for i in ex if not t[i]]
    rng.shuffle(fits); rng.shuffle(nots)
    test_scenes = [pool[i] for i in tests]
    test_kinds = ["shortcut", "shortcut", "shortcut", "near-miss", "near-miss", "random", "random", "random"]
    order = list(range(8)); rng.shuffle(order)
    test_scenes = [test_scenes[i] for i in order]
    test_kinds = [test_kinds[i] for i in order]
    test_labels = [bool(rule["fn"](s)) for s in test_scenes]
    assert all(rule["fn"](s) for s in fits) and not any(rule["fn"](s) for s in nots)
    return dict(fits=fits, nots=nots, tests=test_scenes, test_labels=test_labels, test_kinds=test_kinds,
                report=report)


def main():
    seed, public, sealed = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    os.makedirs(public, exist_ok=True); os.makedirs(os.path.join(sealed, "key"), exist_ok=True)
    master = random.Random(seed)
    order = list(range(len(RULES))); master.shuffle(order)
    key, rules_out, scenes_out, reports = {}, {}, {}, {}
    for p, ri in enumerate(order):
        pid = f"P{p+1}"
        rule = RULES[ri]
        pseed = master.randrange(2**31)
        rng = random.Random(pseed)
        print(f"{pid} <- {rule['id']} (cost {rule['cost']}), seed {pseed}", flush=True)
        prob = build_problem(rule, rng, None)
        print("   ", json.dumps(prob["report"]["attempt_result"]), prob["report"]["delta0_cost_le_cstar"]["consistent_rules_disagreeing_on_tests"],
              prob["report"]["delta1_cost_eq_cstar_plus1"]["consistent_rules_disagreeing_on_tests"], flush=True)
        render_examples_sheet(pid, prob["fits"], prob["nots"], os.path.join(public, f"{pid}_examples.png"))
        render_tests_sheet(pid, prob["tests"], os.path.join(public, f"{pid}_tests.png"))
        key[pid] = ["Y" if x else "N" for x in prob["test_labels"]]
        rules_out[pid] = {k: v for k, v in rule.items() if k != "fn"} | {"problem_seed": pseed}
        scenes_out[pid] = dict(examples_fit=prob["fits"], examples_not=prob["nots"], tests=prob["tests"],
                               test_labels=key[pid], test_kinds=prob["test_kinds"])
        reports[pid] = prob["report"]
    json.dump({"format": "f2-pilot-key-v1", "problems": key}, open(os.path.join(sealed, "key", "key.json"), "w"), indent=1)
    json.dump(rules_out, open(os.path.join(sealed, "rules.json"), "w"), indent=1)
    json.dump(scenes_out, open(os.path.join(sealed, "scenes.json"), "w"))
    json.dump(reports, open(os.path.join(sealed, "consistency_report.json"), "w"), indent=1)
    json.dump({"master_seed": seed, "problem_order": [RULES[i]["id"] for i in order]},
              open(os.path.join(sealed, "seeds.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
