#!/usr/bin/env python3
"""Unrun Lab (F7) pilot scorer.  Standard library + numpy only.

Usage:
    python3 score.py --key KEY_DIR --answers ANSWERS_DIR [--per-question] [--pairs]

KEY_DIR is the `key/` folder obtained by decrypting sealed.tar.gz.enc. It holds
    key.json            per-question scale factor and reference forecasts (no-change, oracle, naive anchor)
    truth_samples.npz   10,000 sealed rollout outcomes per question (the ground-truth distribution)
ANSWERS_DIR holds one <SOLVER_LABEL>.json per solver (schema in INSTRUCTIONS.md).

Scoring
  * Quantile score (QS) of a forecast f = (f05, f25, f50, f75, f95) for question q:
        QS_q(f) = (1/5) * sum_tau mean_i rho_tau(y_i - f_tau) / scale_q
    where y_i are the 10,000 sealed rollouts, rho_tau(u) = u * (tau - 1[u < 0]) is the pinball
    loss, and scale_q (in key.json) makes questions unit-free. QS is a proper score for the
    stated quantiles and a discrete approximation to CRPS/2 (in scale units).
  * Skill (0 = no-change forecast, 100 = oracle forecast):
        per question:  100 * (QS_nochange - QS_solver) / (QS_nochange - QS_oracle)
        overall / per simulator: the same ratio computed on SUMS over questions
        (sums are taken before the ratio, as the spec requires).
    "no-change" = true-model quantiles with no intervention; "oracle" = true-model quantiles
    under the intervention from an independent set of 10,000 rollouts.
  * Anchored skill: same ratio with the naive "extrapolate the experiments" forecaster as 0.
  * Missing or invalid answers score QS = QS_nochange + (QS_nochange - QS_oracle), i.e. -100 on
    that question. Non-monotone quantiles are sorted before scoring and flagged.
  * CI: 90% bootstrap over questions (2,000 resamples, fixed seed) of the overall skill.
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

QKEYS = ["q05", "q25", "q50", "q75", "q95"]
TAUS = np.array([0.05, 0.25, 0.50, 0.75, 0.95])


def qscore(f, y, scale):
    f = np.asarray(f, float)
    u = y[None, :] - f[:, None]
    loss = np.mean(u * (TAUS[:, None] - (u < 0)), axis=1)
    return float(loss.mean() / scale)


def load_key(kdir):
    with open(os.path.join(kdir, "key.json")) as fh:
        key = json.load(fh)
    npz = np.load(os.path.join(kdir, "truth_samples.npz"))
    qs = key["questions"]
    ref = {}
    for qid, meta in qs.items():
        y = npz[qid]
        s = meta["scale"]
        ref[qid] = dict(sim=meta["simulator"], y=y, scale=s,
                        L_nc=qscore(meta["nochange"], y, s),
                        L_or=qscore(meta["oracle"], y, s),
                        L_nv=qscore(meta["naive"], y, s) if "naive" in meta else None)
    return key, ref


def parse_answers(path, qids):
    flags = []
    try:
        with open(path) as fh:
            data = json.load(fh)
        fc = data.get("forecasts", {})
        if not isinstance(fc, dict):
            raise ValueError("forecasts is not an object")
    except Exception as e:  # unreadable file -> everything missing
        return {}, ["unreadable file: %s" % e]
    out = {}
    for qid in qids:
        a = fc.get(qid)
        try:
            vals = [float(a[k]) for k in QKEYS]
            if not all(np.isfinite(vals)):
                raise ValueError("non-finite")
        except Exception:
            flags.append("%s missing/invalid" % qid)
            continue
        if any(vals[i] > vals[i + 1] for i in range(4)):
            flags.append("%s non-monotone (sorted)" % qid)
            vals = sorted(vals)
        out[qid] = vals
    extra = sorted(set(fc) - set(qids))
    if extra:
        flags.append("ignored unknown ids: %s" % ", ".join(extra))
    return out, flags


def losses(ans, ref, qids):
    L = {}
    for qid in qids:
        r = ref[qid]
        if qid in ans:
            L[qid] = qscore(ans[qid], r["y"], r["scale"])
        else:
            L[qid] = r["L_nc"] + (r["L_nc"] - r["L_or"])
    return L


def skill(L, ref, ids, zero="L_nc"):
    num = sum(ref[q][zero] - L[q] for q in ids)
    den = sum(ref[q][zero] - ref[q]["L_or"] for q in ids)
    return 100.0 * num / den


def boot_ci(L, ref, qids, n=2000, seed=12345):
    rng = np.random.default_rng(seed)
    q = np.array(qids)
    a = np.array([ref[k]["L_nc"] - L[k] for k in qids])
    b = np.array([ref[k]["L_nc"] - ref[k]["L_or"] for k in qids])
    idx = rng.integers(0, len(q), (n, len(q)))
    s = 100.0 * a[idx].sum(1) / b[idx].sum(1)
    return np.percentile(s, [5, 95]), idx


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--per-question", action="store_true")
    ap.add_argument("--pairs", action="store_true", help="paired bootstrap: share of resamples in which row beats column")
    args = ap.parse_args()
    key, ref = load_key(args.key)
    qids = sorted(ref)
    sims = sorted({ref[q]["sim"] for q in qids})
    files = sorted(glob.glob(os.path.join(args.answers, "*.json")))
    if not files:
        print("no answer files in", args.answers)
        sys.exit(1)
    results = {}
    for fpath in files:
        label = os.path.splitext(os.path.basename(fpath))[0]
        ans, flags = parse_answers(fpath, qids)
        L = losses(ans, ref, qids)
        results[label] = dict(L=L, flags=flags, n_ok=len(ans))
    hdr = "%-22s %8s %17s " % ("solver", "skill", "90% CI (boot)") + " ".join("%7s" % s for s in sims) + " %9s %8s %6s" % ("anchored", "mean QS", "valid")
    print("Unrun Lab pilot -- skill: 0 = no-change forecast, 100 = oracle (true-model) forecast")
    print(hdr)
    print("-" * len(hdr))
    idx_cache = None
    for label, r in results.items():
        L = r["L"]
        tot = skill(L, ref, qids)
        ci, idx_cache = boot_ci(L, ref, qids)
        per = [skill(L, ref, [q for q in qids if ref[q]["sim"] == s]) for s in sims]
        anch = skill(L, ref, qids, zero="L_nv") if all(ref[q]["L_nv"] is not None for q in qids) else float("nan")
        mqs = np.mean([L[q] for q in qids])
        print("%-22s %8.1f   [%6.1f, %6.1f] " % (label[:22], tot, ci[0], ci[1]) + " ".join("%7.1f" % v for v in per)
              + " %9.1f %8.4f %3d/%d" % (anch, mqs, r["n_ok"], len(qids)))
    print("\nreference QS (mean over questions): no-change %.4f, oracle %.4f" % (
        np.mean([ref[q]["L_nc"] for q in qids]), np.mean([ref[q]["L_or"] for q in qids])))
    for label, r in results.items():
        if r["flags"]:
            print("flags [%s]: %s" % (label, "; ".join(r["flags"])))
    if args.per_question:
        print("\nper-question skill (0 = no-change, 100 = oracle)")
        labels = list(results)
        print("%-7s " % "q" + " ".join("%12s" % l[:12] for l in labels))
        for q in qids:
            print("%-7s " % q + " ".join("%12.1f" % (100 * (ref[q]["L_nc"] - results[l]["L"][q]) / (ref[q]["L_nc"] - ref[q]["L_or"])) for l in labels))
    if args.pairs and len(results) > 1:
        labels = list(results)
        rng = np.random.default_rng(777)
        idx = rng.integers(0, len(qids), (2000, len(qids)))
        den = np.array([ref[q]["L_nc"] - ref[q]["L_or"] for q in qids])
        S = {}
        for l in labels:
            a = np.array([ref[q]["L_nc"] - results[l]["L"][q] for q in qids])
            S[l] = 100 * a[idx].sum(1) / den[idx].sum(1)
        print("\npaired bootstrap over questions: share of resamples where ROW skill > COLUMN skill")
        print("%-14s " % "" + " ".join("%10s" % l[:10] for l in labels))
        for a in labels:
            print("%-14s " % a[:14] + " ".join("%10s" % ("-" if a == b else "%.2f" % np.mean(S[a] > S[b])) for b in labels))


if __name__ == "__main__":
    main()
