"""Analyse the retrospective benchmark-viability rating study.

Inputs : research/rating_study/framework.json, research/rating_study/ratings.json
Outputs: research/rating_study/results.json, research/rating_study/report.md

Statistics:
- Krippendorff's alpha (interval) per factor and for the total score (3 raters x 39 benchmarks).
- Association of the mean total rubric score with the adoption outcome (Spearman rho; AUC adopted vs not_adopted),
  with percentile bootstrap CIs over benchmarks.
- Per-factor AUCs.
- Sensitivity analyses: ratings where the rater did NOT claim to know the outcome; excluding the lead's ten
  benchmarks; game vs non-game.
"""

import json
import os

import numpy as np
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "research", "rating_study")
RNG = np.random.default_rng(20260929)

LEAD_TEN = {
    "Qi Town (Who is a Better Player: LLM against LLM)",
    "Game Reasoning Arena",
    "MastermindEval",
    "Concept (Do You Get the Hint?)",
    "Codenames ad-hoc concept forming",
    "Boardwalk",
    "Grid-based game competitions",
    "TopoBench",
    "From Raw Corpora to Domain Benchmarks",
    "BloomQA (Bloom's-taxonomy guideline benchmarks)",
}
GAME = {
    "Qi Town (Who is a Better Player: LLM against LLM)", "Game Reasoning Arena", "MastermindEval",
    "Concept (Do You Get the Hint?)", "Codenames ad-hoc concept forming", "Boardwalk",
    "Grid-based game competitions", "GTBench", "lmgame-Bench", "LLM Chess", "Kaggle Game Arena",
}
OUTCOME_CODE = {"not_adopted": 0, "partial": 1, "adopted": 2}


def krippendorff_alpha_interval(data):
    """data: raters x units array with np.nan for missing. Interval metric."""
    data = np.asarray(data, dtype=float)
    units = [data[:, u][~np.isnan(data[:, u])] for u in range(data.shape[1])]
    units = [v for v in units if len(v) >= 2]
    n = sum(len(v) for v in units)
    if n <= 1:
        return float("nan")
    d_o = 0.0
    for v in units:
        m = len(v)
        diffs = (v[:, None] - v[None, :]) ** 2
        d_o += diffs.sum() / (m - 1)
    d_o /= n
    allv = np.concatenate(units)
    d_e = ((allv[:, None] - allv[None, :]) ** 2).sum() / (n * (n - 1))
    if d_e == 0:
        return float("nan")
    return 1.0 - d_o / d_e


def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    gt = (pos[:, None] > neg[None, :]).sum()
    eq = (pos[:, None] == neg[None, :]).sum()
    return (gt + 0.5 * eq) / (len(pos) * len(neg))


def boot_ci(fn, n, B=5000):
    vals = []
    for _ in range(B):
        idx = RNG.integers(0, n, n)
        v = fn(idx)
        if not np.isnan(v):
            vals.append(v)
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def main():
    fw = json.load(open(os.path.join(DIR, "framework.json")))
    ratings = json.load(open(os.path.join(DIR, "ratings.json")))
    factors = fw["factors"]
    benches = fw["benchmarks"]
    F, N, R = len(factors), len(benches), len(ratings)

    X = np.full((R, N, F), np.nan)
    fam = np.full((R, N), "", dtype=object)
    for r, rr in enumerate(ratings):
        for item in rr["ratings"]:
            b = int(item["benchmark_id"].lstrip("B")) - 1
            X[r, b, :] = item["scores"][:F]
            fam[r, b] = item["familiarity"]

    y = np.array([OUTCOME_CODE[b["outcome"]] for b in benches])
    names = [b["name"] for b in benches]
    total = X.sum(axis=2)  # R x N
    mean_total = np.nanmean(total, axis=0)

    res = {"n_benchmarks": N, "n_factors": F, "n_raters": R,
           "raters": [{"rater": r["rater"], "model": r["model"]} for r in ratings]}

    # Reliability
    res["alpha_total"] = krippendorff_alpha_interval(total)
    res["alpha_per_factor"] = {f["id"]: krippendorff_alpha_interval(X[:, :, i]) for i, f in enumerate(factors)}
    pair_r = []
    for a in range(R):
        for b in range(a + 1, R):
            pair_r.append(stats.pearsonr(total[a], total[b])[0])
    res["pairwise_pearson_total"] = [float(v) for v in pair_r]

    # Association with outcome
    adopted, notad = y == 2, y == 0
    res["spearman_total_vs_outcome"] = float(stats.spearmanr(mean_total, y)[0])
    res["spearman_ci"] = boot_ci(lambda idx: stats.spearmanr(mean_total[idx], y[idx])[0] if len(set(y[idx])) > 1 else np.nan, N)
    res["auc_adopted_vs_not"] = float(auc(mean_total[adopted], mean_total[notad]))
    res["auc_ci"] = boot_ci(lambda idx: auc(mean_total[idx][y[idx] == 2], mean_total[idx][y[idx] == 0]), N)
    res["mean_total_by_outcome"] = {k: float(mean_total[y == v].mean()) for k, v in OUTCOME_CODE.items()}
    res["max_total"] = 3 * F

    per_factor = {}
    for i, f in enumerate(factors):
        m = np.nanmean(X[:, :, i], axis=0)
        per_factor[f["id"]] = {
            "name": f["name"],
            "auc": float(auc(m[adopted], m[notad])),
            "mean_adopted": float(m[adopted].mean()),
            "mean_not_adopted": float(m[notad].mean()),
        }
    res["per_factor"] = per_factor

    # Composite analysis: measurement-quality factors vs ecosystem/narrative factors
    groups = {}
    for i, f in enumerate(factors):
        groups.setdefault(f["group"], []).append(i)
    validity_idx = [i for g, ix in groups.items() if g.startswith("Measurement") or g.startswith("Longevity") for i in ix]
    eco_idx = [i for g, ix in groups.items() if g.startswith("Ecosystem") or g.startswith("Narrative") for i in ix]
    comp = {}
    for label, ix in (("measurement_and_longevity", validity_idx), ("ecosystem_and_narrative", eco_idx)):
        m = np.nanmean(X[:, :, ix].sum(axis=2), axis=0)
        comp[label] = {
            "factors": [factors[i]["id"] for i in ix],
            "auc": float(auc(m[adopted], m[notad])),
            "auc_ci": boot_ci(lambda idx, m=m: auc(m[idx][y[idx] == 2], m[idx][y[idx] == 0]), N),
            "spearman": float(stats.spearmanr(m, y)[0]),
        }
    res["composites"] = comp

    # Sensitivity 1: ratings where rater did not claim to know the outcome
    blind_mask = fam != "knew_outcome"
    Xb = np.where(blind_mask[:, :, None], X, np.nan)
    tb = np.nansum(Xb, axis=2)
    tb[~blind_mask] = np.nan
    with np.errstate(all="ignore"):
        mb = np.array([np.nanmean(col) if np.any(~np.isnan(col)) else np.nan for col in tb.T])
    ok = ~np.isnan(mb)
    res["blind_subset"] = {
        "n_rater_benchmark_pairs": int(blind_mask.sum()),
        "n_benchmarks_with_any_blind_rating": int(ok.sum()),
        "n_adopted": int((ok & adopted).sum()),
        "n_not_adopted": int((ok & notad).sum()),
        "auc": float(auc(mb[ok & adopted], mb[ok & notad])),
        "spearman": float(stats.spearmanr(mb[ok], y[ok])[0]) if ok.sum() > 3 else float("nan"),
    }

    # Sensitivity 2: excluding the lead's ten
    keep = np.array([n not in LEAD_TEN for n in names])
    res["excluding_lead_ten"] = {
        "n": int(keep.sum()),
        "auc": float(auc(mean_total[keep & adopted], mean_total[keep & notad])),
        "spearman": float(stats.spearmanr(mean_total[keep], y[keep])[0]),
    }

    # Game vs non-game
    game = np.array([n in GAME for n in names])
    res["game_vs_nongame"] = {
        "n_game": int(game.sum()),
        "mean_total_game": float(mean_total[game].mean()),
        "mean_total_nongame": float(mean_total[~game].mean()),
        "game_outcomes": {k: int(((y == v) & game).sum()) for k, v in OUTCOME_CODE.items()},
    }

    res["per_benchmark"] = [
        {"id": f"B{i+1}", "name": names[i], "year": benches[i]["year"], "outcome": benches[i]["outcome"],
         "mean_total": float(mean_total[i]), "rater_totals": [float(t) for t in total[:, i]],
         "factor_means": [float(v) for v in np.nanmean(X[:, i, :], axis=0)]}
        for i in range(N)
    ]
    json.dump(res, open(os.path.join(DIR, "results.json"), "w"), indent=1)

    # Markdown report
    L = []
    L.append("# Retrospective rating study: results\n")
    L.append(f"{R} independent LLM raters ({', '.join(r['model'] for r in ratings)}) scored {N} benchmarks on {F} rubric factors (0-3 each; max total {3*F}), outcome-blind by instruction.\n")
    L.append("## Reliability\n")
    L.append(f"- Krippendorff's alpha (interval), total score: **{res['alpha_total']:.2f}**")
    L.append(f"- Pairwise Pearson r between raters' totals: {', '.join(f'{v:.2f}' for v in pair_r)}")
    L.append("- Per-factor alpha: " + ", ".join(f"{k} {v:.2f}" for k, v in res["alpha_per_factor"].items()) + "\n")
    L.append("## Association with adoption outcome\n")
    L.append(f"- Mean total by outcome: " + ", ".join(f"{k} {v:.1f}" for k, v in res["mean_total_by_outcome"].items()))
    L.append(f"- Spearman rho (mean total vs outcome 0/1/2): **{res['spearman_total_vs_outcome']:.2f}** (95% bootstrap CI {res['spearman_ci'][0]:.2f} to {res['spearman_ci'][1]:.2f})")
    L.append(f"- AUC adopted vs not adopted: **{res['auc_adopted_vs_not']:.2f}** (95% CI {res['auc_ci'][0]:.2f} to {res['auc_ci'][1]:.2f})\n")
    L.append("| Factor | AUC | mean (adopted) | mean (not adopted) | alpha |")
    L.append("|---|---|---|---|---|")
    for fid, v in sorted(per_factor.items(), key=lambda kv: -kv[1]["auc"]):
        L.append(f"| {fid} {v['name']} | {v['auc']:.2f} | {v['mean_adopted']:.2f} | {v['mean_not_adopted']:.2f} | {res['alpha_per_factor'][fid]:.2f} |")
    L.append("\n## Composite analysis\n")
    for k, v in res["composites"].items():
        L.append(f"- {k} ({', '.join(v['factors'])}): AUC {v['auc']:.2f} (95% CI {v['auc_ci'][0]:.2f} to {v['auc_ci'][1]:.2f}), Spearman {v['spearman']:.2f}")
    L.append("\n## Sensitivity analyses\n")
    bs = res["blind_subset"]
    L.append(f"- Ratings where the rater did not claim to know the outcome: {bs['n_rater_benchmark_pairs']} rater-benchmark pairs over {bs['n_benchmarks_with_any_blind_rating']} benchmarks ({bs['n_adopted']} adopted, {bs['n_not_adopted']} not adopted); AUC {bs['auc']:.2f}, Spearman {bs['spearman']:.2f}. (Uninformative for AUC when the blind subset contains very few adopted benchmarks.)")
    ex = res["excluding_lead_ten"]
    L.append(f"- Excluding the lead's ten benchmarks (n={ex['n']}): AUC {ex['auc']:.2f}, Spearman {ex['spearman']:.2f}.")
    g = res["game_vs_nongame"]
    L.append(f"- Game-based benchmarks (n={g['n_game']}) mean total {g['mean_total_game']:.1f} vs non-game {g['mean_total_nongame']:.1f}; game outcomes {g['game_outcomes']}.\n")
    L.append("## Per-benchmark mean totals\n")
    L.append("| ID | Benchmark | Year | Outcome | Mean total | Rater totals |")
    L.append("|---|---|---|---|---|---|")
    for pb in sorted(res["per_benchmark"], key=lambda d: -d["mean_total"]):
        L.append(f"| {pb['id']} | {pb['name']} | {pb['year']} | {pb['outcome']} | {pb['mean_total']:.1f} | {', '.join(f'{t:.0f}' for t in pb['rater_totals'])} |")
    L.append("\n## Caveats\n")
    L.append("- The rubric was derived from the same literature that describes these benchmarks, so this is a consistency check, not an out-of-sample validation.")
    L.append("- Raters are LLMs and most reported already knowing the outcome for most benchmarks; outcome leakage into design ratings cannot be excluded (see blind-subset analysis).")
    L.append("- Outcome labels were assigned by the synthesis agent from documented adoption evidence; 'partial' is heterogeneous.")
    open(os.path.join(DIR, "report.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L[:30]))


if __name__ == "__main__":
    main()
