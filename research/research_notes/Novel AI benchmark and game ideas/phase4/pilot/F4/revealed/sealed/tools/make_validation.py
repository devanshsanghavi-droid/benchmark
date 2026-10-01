import json, sys
B = sys.argv[1]; OUT = sys.argv[2]
lad = json.load(open(B + "/sealed/ladder_ratings.json"))
val = json.load(open(B + "/val_results.json"))
R = ["L0", "L1", "L2", "L3"]
pw = lad["pairwise_score_rate"]
def rate(a, b):
    if a == b: return None
    k = "%s_vs_%s" % (a, b)
    return pw[k] if k in pw else 1 - pw["%s_vs_%s" % (b, a)]
rt = lad["ratings_logit"]
L = []
L.append("# VALIDATION (Brackwater pilot v1.0, 30 Sep 2026)\n")
L.append("## Ladder self-consistency\n")
L.append("%d maps x 2 seats = %d games per pair; %d forfeits. Row score rate vs column.\n" % (lad["maps"], lad["games_per_pair"], lad["forfeit_games"]))
L.append("| | " + " | ".join(R) + " |")
L.append("|---" * 5 + "|")
for a in R:
    L.append("| %s | " % a + " | ".join("–" if a == b else "%.3f" % rate(a, b) for b in R) + " |")
L.append("")
L.append("Fixed BT ratings (logit, L1 = 0; pseudo-count 0.5/0.5 per pair): " + ", ".join("%s %+.2f" % (k, rt[k] - rt["L1"]) for k in R) + ".\n")
L.append("Ladder CPU per game, mean/max (s): " + ", ".join("%s %.2f/%.2f" % (k, lad["cpu_per_game_mean"][k], lad["cpu_per_game_max"][k]) for k in R) + ".\n")
L.append("## Reference bots scored as submissions (score.py, subprocess harness)\n")
L.append("%d games per rung on the evaluation maps.\n" % val["games_per_rung"])
L.append("| submission | vs L0 | vs L1 | vs L2 | vs L3 | forfeits | rung position [95% CI] | logit vs L1 [95% CI] | CPU/game mean/max (s) |")
L.append("|---|---|---|---|---|---|---|---|---|")
names = {"VAL_RANDOM": "random bot (= L0)", "VAL_L3": "strongest reference bot (= L3)"}
for lab, s in val["solvers"].items():
    cells = ["%.3f [%.3f, %.3f]" % (s["vs"][k]["score_rate"], *s["vs"][k]["ci95"]) for k in R]
    L.append("| %s | " % names.get(lab, lab) + " | ".join(cells) + " | %d | %.2f%s [%.2f, %.2f] | %+.2f [%+.2f, %+.2f] | %.2f/%.2f |" % (
        s["forfeits"], s["rung_position"], "*" if s["extrapolated"] else "", *s["rung_position_ci95"],
        s["bt_logit_rel_L1"], *s["bt_logit_ci95_rel_L1"], s["cpu_per_game_mean"], s["cpu_per_game_max"]))
L.append("")
if val.get("h2h"):
    L.append("Head-to-head: " + ", ".join("%s %.3f" % (k.replace("VAL_", ""), v) for k, v in val["h2h"].items()) + ".\n")
L.append("\\* = outside the ladder range (extrapolated).\n")
L.append("Human baseline: none (no humans available for this pilot).")
open(OUT, "w").write("\n".join(L) + "\n")
print("\n".join(L))
