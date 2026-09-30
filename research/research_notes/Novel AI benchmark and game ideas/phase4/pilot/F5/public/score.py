#!/usr/bin/env python3
"""F5 Self-Knowledge Exam (pilot) -- scorer.

Usage:
    python3 score.py KEY_DIR ANSWERS_DIR [--json OUT.json] [--boot 2000] [--seed 20260930]

KEY_DIR      directory containing key.json (searched recursively), i.e. the decrypted sealed archive.
ANSWERS_DIR  directory holding <LABEL>.json (final answers) and optionally <LABEL>.phase1.json
             (the Phase-1 commitment). Every *.json that is not *.phase1.json is scored as one solver.

This file contains no answers; it reads them from KEY_DIR. Standard library only.

Metrics (per solver)
  accuracy            share of all items answered correctly (abstentions and invalid answers count as wrong)
  Brier               mean (p - y)^2 over all items, with Murphy decomposition (10 equal-width bins)
  ECE                 expected calibration error, 10 equal-width bins
  AUROC(p)            P(p_correct_item > p_wrong_item), ties 1/2; insensitive to base accuracy
  AUROC within level  same, counting only pairs of items at the same hidden design-difficulty level
  SR_twin  [headline 1, spec form]  mean over forecast items of LS(p) - LS(b_f), where b_f is the solver's own
                      per-family success rate on blind-twin items (shrunk to the pooled twin rate, prior weight 2).
                      With only 2-3 twins per family the reference is noisy and SR_twin is biased upward; the
                      scorer therefore also prints the SR_twin that "p = own accuracy" would get on the same items.
  SR_glob             mean over all items of LS(p) - LS(own overall accuracy); exactly 0 for a solver that
                      reports its own accuracy as a constant
  SR_fam              as SR_glob but against own per-family accuracy (hindsight; conservative)
                      LS = natural-log score, probabilities clipped to [0.01, 0.99]; units: nats per item
  Triage value [headline 2]  (sum_blocks succ(chosen k) - k * r_b) / (sum_blocks min(k, succ_b) - k * r_b)
  Prospective (q)     AUROC(q), SR_twin(q), Brier(q) on forecast items
  Cross-solver        leave-one-out peer success rate as a difficulty predictor, AUROC(p) on contested items,
                      and AUROC of two cue-only predictors (hidden level; visible prompt length)
"""
import argparse, json, math, os, random, re, sys

CLIP = (0.01, 0.99)


# ------------------------------------------------------------------ loading
def load_key(key_dir):
    for root, _, files in os.walk(key_dir):
        if "key.json" in files:
            with open(os.path.join(root, "key.json")) as f:
                return json.load(f)
    sys.exit(f"key.json not found under {key_dir}")


def load_answers(ans_dir):
    out = {}
    for fn in sorted(os.listdir(ans_dir)):
        if not fn.endswith(".json") or fn.endswith(".phase1.json"):
            continue
        label = fn[:-5]
        path = os.path.join(ans_dir, fn)
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:  # unreadable file = do-nothing solver, flagged
            data = {"_load_error": str(e)}
        if not isinstance(data, dict):
            data = {"_load_error": "top-level JSON is not an object"}
        p1 = os.path.join(ans_dir, label + ".phase1.json")
        ph1 = None
        if os.path.exists(p1):
            try:
                with open(p1) as f:
                    ph1 = json.load(f)
            except Exception as e:
                ph1 = {"_load_error": str(e)}
        out[label] = {"data": data, "phase1": ph1, "mtime": os.path.getmtime(path),
                      "phase1_mtime": os.path.getmtime(p1) if ph1 is not None else None}
    return out


# ------------------------------------------------------------------ normalisation
ABSTAIN = object()
INVALID = object()


def _is_abstain(a):
    return a is None or (isinstance(a, str) and a.strip().upper() in ("", "ABSTAIN", "NULL", "NONE", "SKIP"))


def norm(atype, a):
    if _is_abstain(a):
        return ABSTAIN
    try:
        if atype == "int":
            if isinstance(a, bool):
                return INVALID
            if isinstance(a, int):
                return a
            s = re.sub(r"[\s,_]", "", str(a))
            return int(s) if re.fullmatch(r"[+-]?\d+", s) else INVALID
        if atype == "doc":
            if isinstance(a, int) and not isinstance(a, bool):
                return a
            s = re.sub(r"[\s,_]", "", str(a))
            if re.fullmatch(r"[+-]?\d+", s):
                return int(s)
            t = re.sub(r"[^A-Z]", "", str(a).upper())
            return t if t in ("CONTRADICTORY", "NOTDETERMINABLE") else INVALID
        if atype == "wordlist":
            if isinstance(a, list):
                parts = [str(x) for x in a]
            else:
                s = str(a).strip().strip("[]")
                parts = s.split(",") if "," in s else s.split()
            return [re.sub(r"[\"'`\s]", "", x).lower() for x in parts if x.strip()]
        if atype == "str":
            return re.sub(r"[\"'`\s]", "", str(a)).lower()
        if atype == "printed":
            return re.sub(r"[\"'`\s]", "", str(a))
        if atype == "intlist":
            if isinstance(a, list):
                return [int(x) for x in a]
            return [int(x) for x in re.findall(r"-?\d+", str(a))]
    except Exception:
        return INVALID
    raise ValueError(atype)


def is_correct(item, a):
    got = norm(item["atype"], a)
    if got is ABSTAIN or got is INVALID:
        return False, got
    want = item["answer"]
    if item["atype"] == "doc" and isinstance(want, str):
        want = re.sub(r"[^A-Z]", "", want.upper())
    else:
        want = norm(item["atype"], want)
    return got == want, got


def prob(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if math.isnan(v) or v < 0 or v > 1:
        return None
    return v


# ------------------------------------------------------------------ metrics
def auroc(scores, ys):
    pos = [s for s, y in zip(scores, ys) if y]
    neg = [s for s, y in zip(scores, ys) if not y]
    if not pos or not neg:
        return None
    w = 0.0
    for a in pos:
        for b in neg:
            w += 1.0 if a > b else 0.5 if a == b else 0.0
    return w / (len(pos) * len(neg))


def auroc_strat(scores, ys, strata):
    w = n = 0.0
    for s in set(strata):
        idx = [i for i, t in enumerate(strata) if t == s]
        pos = [scores[i] for i in idx if ys[i]]
        neg = [scores[i] for i in idx if not ys[i]]
        for a in pos:
            for b in neg:
                w += 1.0 if a > b else 0.5 if a == b else 0.0
        n += len(pos) * len(neg)
    return (w / n if n else None), int(n)


def ls(p, y):
    p = min(max(p, CLIP[0]), CLIP[1])
    return math.log(p) if y else math.log(1 - p)


def brier(ps, ys):
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps) if ps else None


def murphy(ps, ys, nb=10):
    n = len(ps)
    if not n:
        return None
    ob = sum(ys) / n
    bins = {}
    for p, y in zip(ps, ys):
        b = min(int(p * nb), nb - 1)
        bins.setdefault(b, []).append((p, y))
    rel = res = ece = 0.0
    for v in bins.values():
        pb = sum(p for p, _ in v) / len(v)
        yb = sum(y for _, y in v) / len(v)
        rel += len(v) * (pb - yb) ** 2 / n
        res += len(v) * (yb - ob) ** 2 / n
        ece += len(v) * abs(pb - yb) / n
    return {"reliability": rel, "resolution": res, "uncertainty": ob * (1 - ob), "ece": ece}


def twin_rates(fams, ys, is_twin):
    tw = [(f, y) for f, y, t in zip(fams, ys, is_twin) if t]
    s, n = sum(y for _, y in tw), len(tw)
    b0 = (s + 1) / (n + 2)
    rates = {}
    for f in set(fams):
        sf = sum(y for g, y in tw if g == f)
        nf = sum(1 for g, _ in tw if g == f)
        rates[f] = (sf + 2 * b0) / (nf + 2)
    return rates


def sr_twin(ps, ys, fams, is_twin):
    """Spec headline: forecast items scored against the solver's own twin-estimated family base rate."""
    rates = twin_rates(fams, ys, is_twin)
    d = [ls(p, y) - ls(rates[f], y) for p, y, f, t in zip(ps, ys, fams, is_twin) if not t and p is not None]
    return sum(d) / len(d) if d else None


def sr_const(ps, ys, groups):
    acc = {}
    for g in set(groups):
        v = [y for y, h in zip(ys, groups) if h == g]
        acc[g] = sum(v) / len(v)
    d = [ls(p, y) - ls(acc[g], y) for p, y, g in zip(ps, ys, groups)]
    return sum(d) / len(d) if d else None


def boot_ci(fn, n, B, rng, strata=None):
    vals = []
    for _ in range(B):
        if strata is None:
            idx = [rng.randrange(n) for _ in range(n)]
        else:
            idx = []
            for s in set(strata):
                pool = [i for i in range(n) if strata[i] == s]
                idx += [rng.choice(pool) for _ in pool]
        v = fn(idx)
        if v is not None:
            vals.append(v)
    if len(vals) < B * 0.5:
        return None
    vals.sort()
    return (vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1])


# ------------------------------------------------------------------ per-solver scoring
def score_solver(label, rec, key, B, seed):
    items = key["items"]
    ids = sorted(items)
    data = rec["data"]
    flags = []
    if "_load_error" in data:
        flags.append("answer file unreadable: " + data["_load_error"])
    att = data.get("attempts", {})
    if isinstance(att, list):
        att = {str(a.get("id")): a for a in att if isinstance(a, dict)}
    if not isinstance(att, dict):
        att = {}
    fc = data.get("forecasts")
    tri = data.get("triage")
    ph1 = rec["phase1"] if isinstance(rec["phase1"], dict) else None
    if not isinstance(fc, dict) or not fc:
        fc = (ph1 or {}).get("forecasts") or {}
        if fc:
            flags.append("forecasts taken from phase1 file")
    if not isinstance(tri, dict) or not tri:
        tri = (ph1 or {}).get("triage") or {}
        if tri:
            flags.append("triage taken from phase1 file")

    ys, ps, fams, lvls, twin, chars, qs, ids_used = [], [], [], [], [], [], [], []
    n_abst = n_inv = n_p_missing = n_q_missing = n_work = 0
    work_len = 0
    for i in ids:
        it = items[i]
        a = att.get(i, {}) if isinstance(att.get(i, {}), dict) else {"answer": att.get(i)}
        ok, got = is_correct(it, a.get("answer"))
        n_abst += got is ABSTAIN
        n_inv += got is INVALID
        p = prob(a.get("p"))
        if p is None:
            n_p_missing += 1
            p = 0.5
        w = a.get("work")
        if isinstance(w, str) and w.strip():
            n_work += 1
            work_len += len(w.strip())
        q = None
        if it["set"] == "forecast":
            q = prob(fc.get(i)) if isinstance(fc, dict) else None
            if q is None:
                n_q_missing += 1
                q = 0.5
        ys.append(1 if ok else 0)
        ps.append(p)
        fams.append(it["family"])
        lvls.append(it["level"])
        twin.append(it["set"] == "twin")
        chars.append(it["prompt_chars"])
        qs.append(q)
        ids_used.append(i)
    n = len(ids)
    acc = sum(ys) / n
    fidx = [k for k in range(n) if not twin[k]]
    tidx = [k for k in range(n) if twin[k]]
    acc_f = sum(ys[k] for k in fidx) / len(fidx)
    acc_t = sum(ys[k] for k in tidx) / len(tidx)
    se_gap = math.sqrt(max(acc_f * (1 - acc_f), 1e-9) / len(fidx) + max(acc_t * (1 - acc_t), 1e-9) / len(tidx))

    m = murphy(ps, ys)
    r = {"solver": label, "n_items": n, "flags": flags,
         "accuracy": acc, "n_correct": sum(ys), "acc_forecast_items": acc_f, "acc_twin_items": acc_t,
         "forecast_minus_twin_acc": acc_f - acc_t, "forecast_minus_twin_se": se_gap,
         "spec_void_rule_triggered(>3pp; not applied in pilot)": abs(acc_f - acc_t) > 0.03,
         "abstention_rate": n_abst / n, "invalid_answers": n_inv, "p_missing": n_p_missing,
         "q_missing": n_q_missing, "work_artefact_rate": n_work / n,
         "mean_work_chars": (work_len / n_work) if n_work else 0,
         "mean_p": sum(ps) / n, "overconfidence_p": sum(ps) / n - acc,
         "brier_p": brier(ps, ys), "murphy_p": m, "ece_p": m["ece"],
         "mean_logscore_p": sum(ls(p, y) for p, y in zip(ps, ys)) / n}
    r["auroc_p"] = auroc(ps, ys)
    r["auroc_p_within_level"], r["pairs_within_level"] = auroc_strat(ps, ys, lvls)
    r["auroc_p_within_family_level"], r["pairs_within_family_level"] = auroc_strat(
        ps, ys, [f"{f}|{l}" for f, l in zip(fams, lvls)])
    r["SR_twin_p"] = sr_twin(ps, ys, fams, twin)
    r["SR_twin_p_const_reference"] = sr_twin([acc] * n, ys, fams, twin)  # what "p = own accuracy" would score
    r["SR_glob_p"] = sr_const(ps, ys, ["all"] * n)
    r["SR_fam_p"] = sr_const(ps, ys, fams)
    # prospective q on forecast items
    qf = [qs[k] for k in fidx]
    yf = [ys[k] for k in fidx]
    r["mean_q"] = sum(qf) / len(qf)
    r["overconfidence_q"] = r["mean_q"] - acc_f
    r["brier_q"] = brier(qf, yf)
    r["auroc_q"] = auroc(qf, yf)
    r["auroc_q_within_level"], _ = auroc_strat(qf, yf, [lvls[k] for k in fidx])
    qfull = [qs[k] if qs[k] is not None else 0.5 for k in range(n)]
    r["SR_twin_q"] = sr_twin(qfull, ys, fams, twin)
    r["corr_p_q"] = _pearson([ps[k] for k in fidx], qf)
    # triage
    k_pick = key.get("triage_k", 5)
    num = den = 0.0
    tri_flags = []
    tri_detail = {}
    y_of = dict(zip(ids_used, ys))
    for b, bids in key["blocks"].items():
        picks = tri.get(b, []) if isinstance(tri, dict) else []
        if not isinstance(picks, list):
            picks = []
        valid = []
        for x in picks:
            x = str(x).strip()
            if x in bids and x not in valid:
                valid.append(x)
        if len(valid) != k_pick or len(picks) != k_pick:
            tri_flags.append(f"block {b}: {len(picks)} picks, {len(valid)} valid")
        valid = valid[:k_pick]
        sb = sum(y_of[x] for x in bids)
        rb = sb / len(bids)
        got = sum(y_of[x] for x in valid)
        num += got - k_pick * rb
        den += min(k_pick, sb) - k_pick * rb
        tri_detail[b] = {"chosen_successes": got, "block_successes": sb, "block_size": len(bids)}
    r["triage_value"] = num / den if den > 1e-12 else None
    r["triage_detail"] = tri_detail
    if tri_flags:
        flags.extend(tri_flags)
    # phase-1 commitment check
    if ph1 is None:
        r["phase1_check"] = "no phase1 file"
    else:
        fc1 = ph1.get("forecasts", {}) if isinstance(ph1, dict) else {}
        tr1 = ph1.get("triage", {}) if isinstance(ph1, dict) else {}
        dq = sum(1 for i in fc1 if prob(fc1.get(i)) != prob(fc.get(i)))
        dq += sum(1 for i in fc if i not in fc1)
        same_tri = all(sorted(map(str, tr1.get(b, []))) == sorted(map(str, tri.get(b, []))) for b in key["blocks"])
        r["phase1_check"] = {"q_differences": dq, "triage_identical": same_tri,
                             "phase1_written_before_final": rec["phase1_mtime"] <= rec["mtime"]}
    # per-family / per-level / doc-label accuracy
    r["acc_by_family"] = {f: _mean([y for y, g in zip(ys, fams) if g == f]) for f in sorted(set(fams))}
    r["acc_by_level"] = {str(l): _mean([y for y, h in zip(ys, lvls) if h == l]) for l in sorted(set(lvls))}
    dl = {}
    for i, y in zip(ids_used, ys):
        lab = items[i].get("doc_label")
        if lab:
            dl.setdefault(lab, []).append(y)
    r["acc_by_doc_label"] = {k: _mean(v) for k, v in sorted(dl.items())}
    r["mean_p_by_level"] = {str(l): _mean([p for p, h in zip(ps, lvls) if h == l]) for l in sorted(set(lvls))}
    # bootstrap CIs
    rng = random.Random(seed)
    r["ci95_auroc_p"] = boot_ci(lambda ix: auroc([ps[k] for k in ix], [ys[k] for k in ix]), n, B, rng)
    r["ci95_auroc_p_within_level"] = boot_ci(
        lambda ix: auroc_strat([ps[k] for k in ix], [ys[k] for k in ix], [lvls[k] for k in ix])[0], n, B, rng)
    r["ci95_SR_twin_p"] = boot_ci(
        lambda ix: sr_twin([ps[k] for k in ix], [ys[k] for k in ix], [fams[k] for k in ix], [twin[k] for k in ix]),
        n, B, rng, strata=twin)
    r["ci95_SR_glob_p"] = boot_ci(lambda ix: sr_const([ps[k] for k in ix], [ys[k] for k in ix], ["all"] * len(ix)),
                                  n, B, rng)
    r["_vectors"] = {"ids": ids_used, "y": ys, "p": ps, "level": lvls, "chars": chars}
    return r


def _mean(v):
    return sum(v) / len(v) if v else None


def _pearson(a, b):
    n = len(a)
    if n < 3:
        return None
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if va == 0 or vb == 0:
        return None
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(va * vb)


def cross_solver(results):
    """Peer-difficulty and cue-only baselines; needs >= 2 solvers for the peer part."""
    labs = list(results)
    ids = results[labs[0]]["_vectors"]["ids"]
    Y = {l: results[l]["_vectors"]["y"] for l in labs}
    for l in labs:
        v = results[l]["_vectors"]
        ys = v["y"]
        results[l]["auroc_cue_level"] = auroc([-x for x in v["level"]], ys)
        results[l]["auroc_cue_prompt_length"] = auroc([-x for x in v["chars"]], ys)
        if len(labs) >= 2:
            peer = [sum(Y[o][k] for o in labs if o != l) / (len(labs) - 1) for k in range(len(ids))]
            results[l]["auroc_peer_loo"] = auroc(peer, ys)
            contested = [k for k in range(len(ids)) if 0 < sum(Y[o][k] for o in labs) < len(labs)]
            results[l]["n_contested_items"] = len(contested)
            results[l]["auroc_p_contested"] = auroc([v["p"][k] for k in contested], [ys[k] for k in contested])


# ------------------------------------------------------------------ output
def f(x, d=3):
    if x is None:
        return "n/a"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return f"{x:.{d}f}"
    return str(x)


def ci(c, d=2):
    return f"[{c[0]:.{d}f}, {c[1]:.{d}f}]" if c else "[n/a]"


def print_solver(r):
    print(f"\n=== {r['solver']} ===")
    if r["flags"]:
        print("  flags: " + "; ".join(r["flags"]))
    print(f"  accuracy {f(r['accuracy'])} ({r['n_correct']}/{r['n_items']}); forecast items {f(r['acc_forecast_items'])}"
          f", blind twins {f(r['acc_twin_items'])} (gap {r['forecast_minus_twin_acc']:+.3f} +/- {r['forecast_minus_twin_se']:.3f} SE)")
    print(f"  abstention {f(r['abstention_rate'])}, invalid answers {r['invalid_answers']}, p missing {r['p_missing']}"
          f", q missing {r['q_missing']}, work artefacts {f(r['work_artefact_rate'])}")
    mu = r["murphy_p"]
    print(f"  p: mean {f(r['mean_p'])} (overconf {r['overconfidence_p']:+.3f}), Brier {f(r['brier_p'])} "
          f"[REL {f(mu['reliability'])} RES {f(mu['resolution'])} UNC {f(mu['uncertainty'])}], ECE {f(r['ece_p'])}")
    print(f"  AUROC(p) {f(r['auroc_p'])} {ci(r['ci95_auroc_p'])}; within level {f(r['auroc_p_within_level'])} "
          f"{ci(r['ci95_auroc_p_within_level'])} ({r['pairs_within_level']} pairs); within family x level "
          f"{f(r['auroc_p_within_family_level'])} ({r['pairs_within_family_level']} pairs)")
    print(f"  Self-Resolution (nats/item): SR_twin {f(r['SR_twin_p'], 4)} {ci(r['ci95_SR_twin_p'], 3)} "
          f"(constant p = own accuracy would score {f(r['SR_twin_p_const_reference'], 4)}) | "
          f"SR_glob {f(r['SR_glob_p'], 4)} {ci(r['ci95_SR_glob_p'], 3)} | SR_fam {f(r['SR_fam_p'], 4)}")
    print(f"  Triage value {f(r['triage_value'])}  " +
          " ".join(f"{b}:{d['chosen_successes']}/{d['block_successes']}" for b, d in r["triage_detail"].items()))
    print(f"  q (prospective): mean {f(r['mean_q'])} (overconf {r['overconfidence_q']:+.3f}), Brier {f(r['brier_q'])},"
          f" AUROC {f(r['auroc_q'])}, within level {f(r['auroc_q_within_level'])}, SR_twin {f(r['SR_twin_q'], 4)},"
          f" corr(p,q) {f(r['corr_p_q'])}")
    print("  acc by family: " + ", ".join(f"{k} {f(v, 2)}" for k, v in r["acc_by_family"].items()))
    print("  acc by level:  " + ", ".join(f"L{k} {f(v, 2)}" for k, v in r["acc_by_level"].items())
          + " | mean p by level: " + ", ".join(f"L{k} {f(v, 2)}" for k, v in r["mean_p_by_level"].items()))
    print("  stock-log acc by true label: " + ", ".join(f"{k} {f(v, 2)}" for k, v in r["acc_by_doc_label"].items()))
    if "auroc_peer_loo" in r:
        print(f"  baselines for this solver's correctness: peer LOO AUROC {f(r['auroc_peer_loo'])}, "
              f"hidden-level AUROC {f(r['auroc_cue_level'])}, prompt-length AUROC {f(r['auroc_cue_prompt_length'])}; "
              f"AUROC(p) on {r['n_contested_items']} contested items {f(r['auroc_p_contested'])}")
    else:
        print(f"  cue-only baselines: hidden-level AUROC {f(r['auroc_cue_level'])}, "
              f"prompt-length AUROC {f(r['auroc_cue_prompt_length'])}")
    print(f"  phase-1 commitment: {r['phase1_check']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("key_dir")
    ap.add_argument("answers_dir")
    ap.add_argument("--json", help="write all metrics to this JSON file")
    ap.add_argument("--boot", type=int, default=2000, help="bootstrap resamples (0 = none)")
    ap.add_argument("--seed", type=int, default=20260930)
    ap.add_argument("--quiet", action="store_true", help="summary table only")
    a = ap.parse_args()
    key = load_key(a.key_dir)
    recs = load_answers(a.answers_dir)
    if not recs:
        sys.exit("no answer files found")
    res = {l: score_solver(l, rec, key, a.boot, a.seed) for l, rec in recs.items()}
    cross_solver(res)
    if not a.quiet:
        for r in res.values():
            print_solver(r)
    print("\n=== summary (headlines: SR_twin, Triage) ===")
    hdr = ["solver", "acc", "mean_p", "Brier", "ECE", "AUROC_p", "AUROC_p|lvl", "SR_twin", "SR_glob", "Triage",
           "AUROC_q", "abstain"]
    print(" | ".join(hdr))
    for r in res.values():
        print(" | ".join([r["solver"], f(r["accuracy"]), f(r["mean_p"]), f(r["brier_p"]), f(r["ece_p"]),
                          f(r["auroc_p"]), f(r["auroc_p_within_level"]), f(r["SR_twin_p"], 4),
                          f(r["SR_glob_p"], 4), f(r["triage_value"]), f(r["auroc_q"]), f(r["abstention_rate"])]))
    if a.json:
        out = {l: {k: v for k, v in r.items() if k != "_vectors"} for l, r in res.items()}
        with open(a.json, "w") as fh:
            json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
