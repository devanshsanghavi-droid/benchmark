#!/usr/bin/env python3
"""Build synthetic answer files from the sealed key, score them with public/score.py, emit the VALIDATION table.

Usage: python3 make_validation.py KEY_DIR SCORE_PY WORK_DIR OUT_TABLE_JSON
WORK_DIR receives synthetic answer files (they contain key answers: delete after use).
"""
import json, os, random, subprocess, sys

key_dir, score_py, work, out_json = sys.argv[1:5]
key = json.load(open(os.path.join(key_dir, "key.json")))
items = key["items"]
ids = sorted(items)
blocks = key["blocks"]
rng = random.Random(777)
os.makedirs(work, exist_ok=True)


def right(i, variant=False):
    it = items[i]
    a = it["answer"]
    t = it["atype"]
    if not variant:
        return a if t != "wordlist" else ", ".join(a)
    # format variants a solver might plausibly produce
    if t == "int":
        return f"{a:,}"
    if t == "doc":
        return a.lower() if isinstance(a, str) else f" {a} "
    if t == "wordlist":
        return [x.upper() for x in a]
    if t == "str":
        return " " + a.upper() + " "
    if t == "printed":
        return "  " + a.replace(" ", "   ") + " "
    if t == "intlist":
        return " ".join(map(str, a))


def wrong(i):
    it = items[i]
    a, t = it["answer"], it["atype"]
    if t == "int":
        return a + 1
    if t == "doc":
        return "NOT DETERMINABLE" if not (isinstance(a, str) and a.startswith("NOT")) else "CONTRADICTORY"
    if t == "wordlist":
        return ", ".join(reversed(a))
    if t == "str":
        return "zz" + a
    if t == "printed":
        return a + "0"
    if t == "intlist":
        return str(a + [0])


LVL = {1: 0.95, 2: 0.8, 3: 0.55, 4: 0.3, 5: 0.1}
P50 = {i: int(rng.random() < 0.5) for i in ids}
PLV = {i: int(rng.random() < LVL[items[i]["level"]]) for i in ids}


def write(label, pattern, pfun, qfun, triage, answer_override=None, variant=False, phase1=False):
    att = {}
    for i in ids:
        y = pattern[i]
        ans = (right(i, variant) if y else wrong(i)) if answer_override is None else answer_override
        att[i] = {"answer": ans, "p": pfun(i, y), "work": "synthetic"}
    fc = {i: qfun(i, pattern[i]) for i in ids if items[i]["set"] == "forecast"}
    tri = {b: triage(b, pattern) for b in blocks}
    data = {"solver_label": label, "forecasts": fc, "triage": tri, "attempts": att}
    with open(os.path.join(work, label + ".json"), "w") as f:
        json.dump(data, f)
    if phase1:
        with open(os.path.join(work, label + ".phase1.json"), "w") as f:
            json.dump({"solver_label": label, "forecasts": fc, "triage": tri}, f)
        os.utime(os.path.join(work, label + ".phase1.json"), (1, 1))


def acc(pat):
    return sum(pat.values()) / len(pat)


def first5(b, pat):
    return blocks[b][:5]


def best5(b, pat):
    return sorted(blocks[b], key=lambda i: -pat[i])[:5]


def worst5(b, pat):
    return sorted(blocks[b], key=lambda i: pat[i])[:5]


def rand5(b, pat):
    return rng.sample(blocks[b], 5)


def by_level5(b, pat):
    return sorted(blocks[b], key=lambda i: (items[i]["level"], rng.random()))[:5]


a50, alv = acc(P50), acc(PLV)
write("B01_const_own_acc", P50, lambda i, y: a50, lambda i, y: a50, first5, phase1=True)
write("B02_oracle", P50, lambda i, y: float(y), lambda i, y: float(y), best5)
write("B03_anti_oracle", P50, lambda i, y: float(1 - y), lambda i, y: float(1 - y), worst5)
write("B04_random_conf", P50, lambda i, y: rng.random(), lambda i, y: rng.random(), rand5)
write("B05_noisy_signal", P50, lambda i, y: min(1, max(0, 0.5 + 0.2 * (2 * y - 1) + rng.gauss(0, 0.2))),
      lambda i, y: min(1, max(0, 0.5 + 0.2 * (2 * y - 1) + rng.gauss(0, 0.2))), best5)
write("B06_const_own_acc_ladder", PLV, lambda i, y: alv, lambda i, y: alv, first5)
write("B07_difficulty_only", PLV, lambda i, y: LVL[items[i]["level"]], lambda i, y: LVL[items[i]["level"]],
      by_level5)
write("B08_oracle_ladder", PLV, lambda i, y: float(y), lambda i, y: float(y), best5)
write("B09_abstain_all", {i: 0 for i in ids}, lambda i, y: 0.0, lambda i, y: 0.0, first5, answer_override=None)
# abstain: overwrite answers with null
d = json.load(open(os.path.join(work, "B09_abstain_all.json")))
for i in ids:
    d["attempts"][i]["answer"] = None
json.dump(d, open(os.path.join(work, "B09_abstain_all.json"), "w"))
with open(os.path.join(work, "B10_empty_file.json"), "w") as f:
    json.dump({}, f)
write("B11_all_correct_const", {i: 1 for i in ids}, lambda i, y: 0.99, lambda i, y: 0.99, first5)
write("B12_confident_wrong", {i: 0 for i in ids}, lambda i, y: 0.9, lambda i, y: 0.9, first5)
write("T01_format_variants_all_correct", {i: 1 for i in ids}, lambda i, y: 0.9, lambda i, y: 0.9, first5,
      variant=True)

jpath = os.path.join(work, "_scores.json")
subprocess.run([sys.executable, score_py, key_dir, work, "--json", jpath, "--boot", "1000", "--quiet"],
               check=True, stdout=subprocess.DEVNULL)
S = json.load(open(jpath))
# scorer self-tests
exp = {"B01_const_own_acc": a50, "B02_oracle": a50, "B06_const_own_acc_ladder": alv, "B08_oracle_ladder": alv,
       "B11_all_correct_const": 1.0, "B12_confident_wrong": 0.0, "B09_abstain_all": 0.0,
       "T01_format_variants_all_correct": 1.0}
for k, v in exp.items():
    assert abs(S[k]["accuracy"] - v) < 1e-9, (k, S[k]["accuracy"], v)
assert S["B01_const_own_acc"]["phase1_check"]["q_differences"] == 0
assert S["B01_const_own_acc"]["phase1_check"]["phase1_written_before_final"] is True
json.dump({"P50_acc": a50, "PLV_acc": alv, "scores": S}, open(out_json, "w"), indent=1)
print("self-tests passed; P50 acc", a50, "ladder acc", alv)

# ---------------- null distributions on the real item structure (no answers involved) ----------------
import importlib.util
spec = importlib.util.spec_from_file_location("score", score_py)
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)
fams = [items[i]["family"] for i in ids]
lvls = [items[i]["level"] for i in ids]
twin = [items[i]["set"] == "twin" for i in ids]
pos = {i: k for k, i in enumerate(ids)}
nrng = random.Random(4242)
null = {}
for name, gen in [("rate50", lambda: [int(nrng.random() < 0.5) for _ in ids]),
                  ("ladder", lambda: [int(nrng.random() < LVL[l]) for l in lvls])]:
    srt, au, auw, tv = [], [], [], []
    for _ in range(2000):
        ys = gen()
        a = sum(ys) / len(ys)
        if 0 < a < 1:
            srt.append(sc.sr_twin([a] * len(ys), ys, fams, twin))
            rp = [nrng.random() for _ in ys]
            au.append(sc.auroc(rp, ys))
            w = sc.auroc_strat(rp, ys, lvls)[0]
            if w is not None:
                auw.append(w)
        num = den = 0.0
        for b, bids in blocks.items():
            yb = [ys[pos[i]] for i in bids]
            sb = sum(yb)
            pick = nrng.sample(bids, 5)
            num += sum(ys[pos[i]] for i in pick) - 5 * sb / len(bids)
            den += min(5, sb) - 5 * sb / len(bids)
        if den > 1e-12:
            tv.append(num / den)

    def summ(v):
        v = sorted(v)
        return {"mean": sum(v) / len(v), "lo": v[int(0.025 * len(v))], "hi": v[int(0.975 * len(v)) - 1]}
    null[name] = {"SR_twin_const_own_acc": summ(srt), "AUROC_random_p": summ(au),
                  "AUROC_within_level_random_p": summ(auw), "triage_random_picks": summ(tv)}
T = json.load(open(out_json))
T["null"] = null
json.dump(T, open(out_json, "w"), indent=1)
print(json.dumps(null, indent=1))
