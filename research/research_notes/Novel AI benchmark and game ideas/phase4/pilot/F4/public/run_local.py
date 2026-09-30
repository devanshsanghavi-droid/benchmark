"""Local test runner for Brackwater bots (public).

Examples (run from this directory):
  python3 run_local.py --bot ../answers/MYLABEL/bot.py                   # vs random bot, 5 public maps x 2 seats x 2 tide seeds
  python3 run_local.py --bot ../answers/MYLABEL/bot.py --opponent other.py --games 40
  python3 run_local.py --bot mybot.py --watch 20 --map maps/map3.json    # print full-information boards every 20 turns
  python3 run_local.py --bot mybot.py --show-stderr --games 1            # see your bot's prints / tracebacks

Your bot always runs exactly as in evaluation: a fresh child process per game under the
compute limits in harness.LIMITS; crashes, illegal actions and limit breaches forfeit.
--opponent may be 'random' (in-process public random bot) or a path to another bot file
(run the same way as yours).
"""
import argparse
import glob
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness  # noqa: E402
import brackwater_engine as bw  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bot", required=True)
    ap.add_argument("--opponent", default="random")
    ap.add_argument("--games", type=int, default=20, help="total games (seats alternate)")
    ap.add_argument("--map", action="append", help="map json (repeatable); default: maps/*.json")
    ap.add_argument("--seed", type=int, default=1, help="first tide seed")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--show-stderr", action="store_true")
    ap.add_argument("--watch", type=int, default=0, help="play ONE game and print the board every N turns")
    a = ap.parse_args()

    map_files = a.map or sorted(glob.glob(os.path.join(HERE, "maps", "*.json")))
    maps = [bw.load_map(f) for f in map_files]
    me = ("subproc", os.path.abspath(a.bot))
    opp = ("inproc", os.path.join(HERE, "random_bot.py")) if a.opponent == "random" else ("subproc", os.path.abspath(a.opponent))

    if a.watch:
        def tr(m):
            if m.turn % a.watch == 0 or m.done:
                print(m.render())
                print()
        r = harness.play_game(maps[0], a.seed, [me, opp], show_stderr=True, trace=tr)
        print("result (you are A / player 0):", r)
        return

    jobs = []
    for i in range(a.games):
        m = maps[(i // 2) % len(maps)]
        seed = a.seed + i // (2 * len(maps)) * 1000 + (i // 2) % len(maps)
        seat = i % 2
        specs = [me, opp] if seat == 0 else [opp, me]
        jobs.append(((i, seat), m, seed, specs, None))
    if a.show_stderr:
        rs = [dict(harness.play_game(m, s, sp, show_stderr=True), job=j) for j, m, s, sp, _ in jobs]
    else:
        rs = harness.run_jobs(jobs, workers=a.workers)
    score = 0.0
    diffs, cpus, mmc, forf = [], [], [], []
    for (jid, *_), r in zip(jobs, rs):
        p = jid[1]
        score += 1.0 if r["winner"] == p else (0.5 if r["winner"] is None else 0.0)
        diffs.append(r["grain"][p] - r["grain"][1 - p])
        if r["cpu"][p] is not None:
            cpus.append(r["cpu"][p])
        if r["max_move_cpu"][p] is not None:
            mmc.append(r["max_move_cpu"][p])
        if r["forfeit"][p]:
            forf.append(r["forfeit"][p])
        if r["forfeit"][1 - p]:
            print("  opponent forfeited game %d: %s" % (jid[0], r["forfeit"][1 - p]))
    n = len(rs)
    print("games %d  score rate %.3f  mean grain diff %+.0f" % (n, score / n, statistics.mean(diffs)))
    if cpus:
        print("your CPU per game: mean %.2fs max %.2fs (limit %.1fs); max single move %.3fs (limit %.2fs)" % (
            statistics.mean(cpus), max(cpus), harness.LIMITS["game_cpu"], max(mmc) if mmc else 0.0,
            harness.LIMITS["move_cpu"]))
    print("your forfeits: %d" % len(forf))
    for f in forf[:5]:
        print("  ", f)


if __name__ == "__main__":
    main()
