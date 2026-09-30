"""Brackwater pilot scorer (public source; needs the decrypted sealed directory).

    python3 score.py --sealed /path/to/decrypted/sealed --answers /path/to/answers \
        [--solvers S1,S2] [--games-per-rung 400] [--h2h-games 200] [--workers 4] [--out results.json]

For every solver directory <answers>/<LABEL>/bot.py the submitted bot plays --games-per-rung
games against each ladder rung L0..L3 on fresh private maps (each map played twice with seats
swapped; identical maps for every solver).  Crashes, illegal actions and budget breaches forfeit
the game.  Headline: Bradley-Terry rating with the ladder ratings held fixed, reported as
  * rung position: 0 = L0 ... 3 = L3, piecewise-linear between rungs, >3 extrapolated at the
    L2->L3 gap (flagged), and
  * BT logit relative to L1 (and its Elo equivalent, x 400/ln 10).
CIs: percentile bootstrap over maps (both seat-games of a map resampled together).
"""
import argparse
import hashlib
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness  # noqa: E402
import brackwater_engine as bw  # noqa: E402

RUNGS = ["L0", "L1", "L2", "L3"]
PSEUDO = 0.5  # pseudo-wins and pseudo-losses added per (bot, opponent) pair


def sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def fit_rating(data, ladder):
    """data: list of (rung, score, n).  ML rating with ladder ratings fixed (1-D Newton)."""
    r = 0.0
    for _ in range(100):
        g = 0.0
        h = 0.0
        for k, s, n in data:
            s2, n2 = s + PSEUDO, n + 2 * PSEUDO
            p = sigmoid(r - ladder[k])
            g += s2 - n2 * p
            h += n2 * p * (1 - p)
        if h <= 0:
            break
        step = max(-2.0, min(2.0, g / h))
        r += step
        if abs(step) < 1e-9:
            break
    return r


def rung_position(r, ladder):
    xs = [ladder[k] for k in RUNGS]
    if r <= xs[0]:
        return (r - xs[0]) / (xs[1] - xs[0]), r < xs[0]
    for i in range(len(xs) - 1):
        if r <= xs[i + 1]:
            return i + (r - xs[i]) / (xs[i + 1] - xs[i]), False
    return len(xs) - 1 + (r - xs[-1]) / (xs[-1] - xs[-2]), True


def cluster_ci(pairs, B, rng):
    """pairs: list of per-map total scores (0..2).  Returns (mean rate, lo, hi)."""
    n = len(pairs)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    m = sum(pairs) / (2 * n)
    bs = []
    for _ in range(B):
        s = 0.0
        for _ in range(n):
            s += pairs[rng.randrange(n)]
        bs.append(s / (2 * n))
    bs.sort()
    return m, bs[int(0.025 * B)], bs[min(B - 1, int(0.975 * B))]


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sealed", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--solvers", default="", help="comma-separated labels (default: every subdir with bot.py)")
    ap.add_argument("--games-per-rung", type=int, default=400)
    ap.add_argument("--h2h-games", type=int, default=200, help="games per solver pair (0 = skip)")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    sealed = os.path.abspath(a.sealed)
    sys.path.insert(0, sealed)
    import mapgen  # noqa: E402  (sealed map generator)
    seeds = json.load(open(os.path.join(sealed, "seeds.json")))
    lad = json.load(open(os.path.join(sealed, "ladder_ratings.json")))
    ladder = lad["ratings_logit"]
    rung_path = {"L0": os.path.join(HERE, "random_bot.py")}
    for k in ("L1", "L2", "L3"):
        rung_path[k] = os.path.join(sealed, lad["files"][k])

    man_path = os.path.join(sealed, "public_manifest.json")
    if os.path.exists(man_path):
        man = json.load(open(man_path))
        bad = [f for f, h in man.items() if not os.path.exists(os.path.join(HERE, f)) or _sha(os.path.join(HERE, f)) != h]
        if bad:
            print("WARNING: public files differ from the sealed manifest: %s" % ", ".join(bad))
        else:
            print("public files match the sealed manifest (%d files)" % len(man))

    answers = os.path.abspath(a.answers)
    if a.solvers:
        labels = [s.strip() for s in a.solvers.split(",") if s.strip()]
    else:
        labels = sorted(d for d in os.listdir(answers) if os.path.isfile(os.path.join(answers, d, "bot.py")))
    missing = [s for s in labels if not os.path.isfile(os.path.join(answers, s, "bot.py"))]
    if missing:
        print("missing bot.py for: %s (scored as all-forfeit)" % ", ".join(missing))
    if not labels:
        print("no solvers found")
        return

    n_maps = a.games_per_rung // 2
    maps = {}

    def get_map(s):
        if s not in maps:
            maps[s] = bw.parse_map(mapgen.generate(s))
        return maps[s]

    jobs = []
    for lab in labels:
        bot = os.path.join(answers, lab, "bot.py")
        for k in RUNGS:
            for s in seeds["eval"][k][:n_maps]:
                m = get_map(s)
                jobs.append(((lab, k, s, 0), m, s, [("subproc", bot), ("inproc", rung_path[k])], None))
                jobs.append(((lab, k, s, 1), m, s, [("inproc", rung_path[k]), ("subproc", bot)], None))
    h2h_pairs = []
    if a.h2h_games > 0 and len(labels) > 1:
        hm = a.h2h_games // 2
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                A, Bl = labels[i], labels[j]
                h2h_pairs.append((A, Bl))
                pa, pb = os.path.join(answers, A, "bot.py"), os.path.join(answers, Bl, "bot.py")
                for s in seeds["h2h"][:hm]:
                    m = get_map(s)
                    jobs.append((("H2H", A, Bl, s, 0), m, s, [("subproc", pa), ("subproc", pb)], None))
                    jobs.append((("H2H", A, Bl, s, 1), m, s, [("subproc", pb), ("subproc", pa)], None))
    print("running %d games on %d workers ..." % (len(jobs), a.workers))
    t0 = time.time()
    results = harness.run_jobs(jobs, workers=a.workers)
    print("done in %.0fs" % (time.time() - t0))

    rng = random.Random(12345)
    report = {"ladder_ratings_logit": ladder, "games_per_rung": 2 * n_maps, "pseudo_count": PSEUDO,
              "solvers": {}, "h2h": {}}
    per = {}
    for (jid, _m, _s, _sp, _l), r in zip(jobs, results):
        if jid[0] == "H2H":
            continue
        lab, k, s, seat = jid
        me = seat
        sc = 1.0 if r["winner"] == me else (0.5 if r["winner"] is None else 0.0)
        d = per.setdefault(lab, {}).setdefault(k, {"maps": {}, "W": 0, "D": 0, "L": 0, "forfeits": [],
                                                    "opp_forfeits": 0, "grain_diff": [], "cpu": []})
        d["maps"][s] = d["maps"].get(s, 0.0) + sc
        d["W" if sc == 1 else ("D" if sc == 0.5 else "L")] += 1
        if r["forfeit"][me]:
            d["forfeits"].append(r["forfeit"][me])
        if r["forfeit"][1 - me]:
            d["opp_forfeits"] += 1
        d["grain_diff"].append(r["grain"][me] - r["grain"][1 - me])
        if r["cpu"][me] is not None:
            d["cpu"].append(r["cpu"][me])

    print()
    print("Ladder (fixed BT logits): " + "  ".join("%s=%.2f" % (k, ladder[k] - ladder["L1"]) for k in RUNGS)
          + "   (shown relative to L1)")
    print()
    hdr = "%-10s " % "solver" + " ".join("%-22s" % ("vs " + k + " (rate, 95% CI)") for k in RUNGS) + \
          " %-8s %-20s %-14s %-9s %s" % ("forfeit", "rung pos (95% CI)", "logit vs L1", "Elo vs L1", "cpu/game mean/max")
    print(hdr)
    for lab in labels:
        dd = per.get(lab, {})
        data = []
        cells = []
        clusters = {}
        nf = 0
        cpus = []
        rep = {"vs": {}}
        for k in RUNGS:
            d = dd.get(k)
            if d is None:
                cells.append("%-22s" % "n/a")
                continue
            pairs = list(d["maps"].values())
            clusters[k] = pairs
            m, lo, hi = cluster_ci(pairs, a.boot, rng)
            n = 2 * len(pairs)
            data.append((k, sum(pairs), n))
            nf += len(d["forfeits"])
            cpus += d["cpu"]
            cells.append("%-22s" % ("%.3f [%.3f,%.3f]" % (m, lo, hi)))
            rep["vs"][k] = {"score_rate": m, "ci95": [lo, hi], "W": d["W"], "D": d["D"], "L": d["L"], "games": n,
                            "forfeits": len(d["forfeits"]), "forfeit_examples": d["forfeits"][:3],
                            "opponent_forfeits": d["opp_forfeits"],
                            "mean_grain_diff": sum(d["grain_diff"]) / max(1, len(d["grain_diff"]))}
        r = fit_rating(data, ladder)
        pos, extrap = rung_position(r, ladder)
        # bootstrap over maps within each rung
        bs_r = []
        for _ in range(a.boot):
            bd = []
            for k, pairs in clusters.items():
                n = len(pairs)
                s = sum(pairs[rng.randrange(n)] for _ in range(n))
                bd.append((k, s, 2 * n))
            bs_r.append(fit_rating(bd, ladder))
        bs_r.sort()
        rlo, rhi = bs_r[int(0.025 * a.boot)], bs_r[min(a.boot - 1, int(0.975 * a.boot))]
        plo, _ = rung_position(rlo, ladder)
        phi, _ = rung_position(rhi, ladder)
        rel = r - ladder["L1"]
        cpu_s = "%.2f/%.2f" % (sum(cpus) / len(cpus), max(cpus)) if cpus else "n/a"
        print("%-10s " % lab + " ".join(cells) + " %-8d %-20s %-14s %-9s %s" % (
            nf, "%.2f%s [%.2f,%.2f]" % (pos, "*" if extrap else "", plo, phi),
            "%+.2f [%+.2f,%+.2f]" % (rel, rlo - ladder["L1"], rhi - ladder["L1"]),
            "%+.0f" % (rel * 400 / math.log(10)), cpu_s))
        rep.update({"bt_logit_rel_L1": rel, "bt_logit_ci95_rel_L1": [rlo - ladder["L1"], rhi - ladder["L1"]],
                    "elo_rel_L1": rel * 400 / math.log(10), "rung_position": pos, "rung_position_ci95": [plo, phi],
                    "extrapolated": extrap, "forfeits": nf,
                    "cpu_per_game_mean": (sum(cpus) / len(cpus)) if cpus else None,
                    "cpu_per_game_max": max(cpus) if cpus else None})
        report["solvers"][lab] = rep
    print("(* = outside the ladder range; rung position extrapolated)")

    if h2h_pairs:
        print()
        print("Head-to-head (row's score rate vs column; secondary, not part of the rating)")
        tab = {}
        for (jid, _m, _s, _sp, _l), r in zip(jobs, results):
            if jid[0] != "H2H":
                continue
            _, A, Bl, s, seat = jid
            pa = 0 if seat == 0 else 1
            sc = 1.0 if r["winner"] == pa else (0.5 if r["winner"] is None else 0.0)
            t = tab.setdefault((A, Bl), [0.0, 0])
            t[0] += sc
            t[1] += 1
        print("%-10s " % "" + " ".join("%-8s" % l for l in labels))
        for A in labels:
            row = []
            for Bl in labels:
                if A == Bl:
                    row.append("%-8s" % "-")
                elif (A, Bl) in tab:
                    row.append("%-8.3f" % (tab[(A, Bl)][0] / tab[(A, Bl)][1]))
                else:
                    row.append("%-8.3f" % (1 - tab[(Bl, A)][0] / tab[(Bl, A)][1]))
            print("%-10s " % A + " ".join(row))
        report["h2h"] = {"%s_vs_%s" % k: v[0] / v[1] for k, v in tab.items()}

    if a.out:
        with open(a.out, "w") as fh:
            json.dump(report, fh, indent=1)
        print("\nwrote %s" % a.out)


if __name__ == "__main__":
    main()
