#!/usr/bin/env python3
"""Render public/VALIDATION.md from the validation JSON (aggregate numbers only)."""
import json, sys
T = json.load(open(sys.argv[1]))
out = sys.argv[2]
S = T["scores"]


def f(x, d=3):
    return "n/a" if x is None else f"{x:.{d}f}"


rows = [
    ("B01_const_own_acc", "coin", "Constant confidence = own accuracy (p = q = realised accuracy; triage = first 5 listed)"),
    ("B02_oracle", "coin", "Oracle: perfect self-knowledge at the same accuracy (p = q = 1 if correct else 0; best 5)"),
    ("B03_anti_oracle", "coin", "Anti-oracle (p = q = 1 if wrong else 0; worst 5)"),
    ("B04_random_conf", "coin", "Random confidence (p, q uniform on [0,1]; random 5)"),
    ("B05_noisy_signal", "coin", "Partial self-knowledge (p = 0.5 +/- 0.2 + N(0, 0.2) noise; q likewise)"),
    ("B06_const_own_acc_ladder", "ladder", "Constant confidence = own accuracy"),
    ("B07_difficulty_only", "ladder", "Difficulty-only knowledge (p = q = true success probability of the item's hidden difficulty; easiest 5)"),
    ("B08_oracle_ladder", "ladder", "Oracle at the same accuracy"),
    ("B09_abstain_all", "-", "Abstain on everything (answer null, p = q = 0)"),
    ("B10_empty_file", "-", "Do-nothing: empty answer file (all defaults: wrong, p = q = 0.5)"),
    ("B11_all_correct_const", "-", "Every answer correct, p = q = 0.99 (no errors to discriminate)"),
    ("B12_confident_wrong", "-", "Every answer wrong, p = q = 0.9"),
]
L = []
L.append("# F5 Self-Knowledge Exam pilot: validation numbers")
L.append("")
L.append("Synthetic answer files were built against the sealed answer key and scored with `score.py` from this "
         "directory (1,000 bootstrap resamples, fixed seed). No real solver is involved. Two synthetic correctness "
         f"patterns are used: **coin** (each item right independently with probability 0.5; realised accuracy "
         f"{T['P50_acc']:.3f}) and **ladder** (success probability falls with a hidden per-item difficulty variable; "
         f"realised accuracy {T['PLV_acc']:.3f}). Metric definitions are in the `score.py` docstring. "
         "SR values are nats per item.")
L.append("")
L.append("**Human baseline: none.** No human participants were available for this pilot, so the spec's human arm "
         "was not run and no human numbers exist.")
L.append("")
L.append("## 1. Reference baselines")
L.append("")
L.append("| ID | Pattern | Baseline | Acc | Mean p | Brier | ECE | AUROC(p) | AUROC(p) within difficulty | "
         "SR_twin (spec) | SR_glob | SR_fam | Triage | AUROC(q) | Abstain |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, pat, desc in rows:
    r = S[k]
    L.append(f"| {k.split('_')[0]} | {pat} | {desc} | {f(r['accuracy'])} | {f(r['mean_p'])} | {f(r['brier_p'])} | "
             f"{f(r['ece_p'])} | {f(r['auroc_p'])} | {f(r['auroc_p_within_level'])} | {f(r['SR_twin_p'])} | "
             f"{f(r['SR_glob_p'])} | {f(r['SR_fam_p'])} | {f(r['triage_value'])} | {f(r['auroc_q'])} | "
             f"{f(r['abstention_rate'])} |")
L.append("")
L.append("## 2. Null distributions on this item set")
L.append("")
L.append("2,000 simulated solvers on the real item structure (families, blind twins, triage blocks, difficulty "
         "strata) with no self-knowledge. The table shows mean [2.5%, 97.5%].")
L.append("")
L.append("| Statistic under the null | coin pattern | ladder pattern |")
L.append("|---|---|---|")
names = {"SR_twin_const_own_acc": "SR_twin of a constant p = own-accuracy forecaster",
         "AUROC_random_p": "AUROC(p), random p",
         "AUROC_within_level_random_p": "AUROC(p) within difficulty strata, random p",
         "triage_random_picks": "Triage value, random picks"}
for k, nm in names.items():
    a, b = T["null"]["rate50"][k], T["null"]["ladder"][k]
    L.append(f"| {nm} | {a['mean']:.3f} [{a['lo']:.3f}, {a['hi']:.3f}] | {b['mean']:.3f} [{b['lo']:.3f}, {b['hi']:.3f}] |")
L.append("")
L.append("## 3. Scorer self-tests (all passed)")
L.append("")
t = S["T01_format_variants_all_correct"]
L.append(f"- Correct answers in alternative formats (digit separators, letter case, list vs string, extra "
         f"whitespace): {t['n_correct']}/{t['n_items']} scored correct.")
L.append("- Synthetic correctness patterns recovered exactly (the accuracy of B01, B02, B06, B08, B09, B11 and B12 "
         "equals the designed pattern).")
L.append("- The Phase-1 commitment check detects identical forecasts and triage, and the write order.")
L.append("- Every answer in the key was re-derived by an independent checker that parses the public item text only. "
         "There were 0 mismatches on this item set, and 0 on 30 further stress seeds after one generator bug "
         "was fixed.")
L.append("")
L.append("## 4. Reading the numbers")
L.append("")
L.append("- **Base-rate insensitivity.** A constant forecaster at its own accuracy gets AUROC 0.500 and SR_glob "
         "0.000, whatever its accuracy (B01, B06). An oracle gets AUROC 1.000 at any accuracy (B02, B08).")
L.append("- **SR_twin (spec headline 1) is biased upward at pilot scale.** There are only 2–3 blind twins per "
         "family, where the spec asks for at least 40, so the reference base rate is noisy. A constant forecaster "
         "then scores well above 0 (section 2). `score.py` prints, for each solver, the SR_twin that "
         "\"p = own accuracy\" would get on the same items. The difference between the two equals SR_glob on "
         "forecast items. Use SR_glob and AUROC as the pilot's resolution read-outs.")
L.append("- **Difficulty-only knowledge.** B07 knows only how hard each item is. It gets a high overall AUROC and "
         "triage value, but its AUROC within difficulty strata is 0.500. The within-strata AUROC, the peer-difficulty "
         "baseline and the cue-only AUROCs printed by `score.py` separate item-level self-knowledge from "
         "knowledge of visible difficulty.")
L.append("- **Brier and ECE reward abstaining on everything** (B09: Brier 0, ECE 0 at accuracy 0). Always read "
         "them next to accuracy.")
L.append("- **Noise.** With 60 items, one solver's AUROC must be above about 0.65 to differ from chance at 95%. "
         "Triage (3 blocks of 15, pick 5) has a null range of about ±0.43. Differences between tiers smaller than "
         "these ranges are not evidence.")
L.append("")
L.append("## 5. Deviations from the F5 spec")
L.append("")
L.append("- 60 items rather than about 1,800, in 6 pilot families: exact computation, logic grids, string "
         "tracing, program-output prediction, rule inference, and stock logs. The stock logs are synthetic "
         "documents whose answer is a number, CONTRADICTORY or NOT DETERMINABLE. There are no post-cutoff-fact "
         "items (no sealed feed exists) and no agentic sandbox items. Program-output prediction stands in for "
         "code with hidden tests.")
L.append("- There is no per-model warm-up. One fixed item set spans a wide difficulty range instead, so every "
         "tier gets some items right and some wrong. As a result, visible difficulty carries part of the signal "
         "(see B07).")
L.append("- Split: 45 forecast items and 15 blind twins (25%). Triage uses 3 blocks of 15 forecast items, pick 5 "
         "(the same 1/3 ratio as 20 of 60). The triage cards are the forecast items themselves, not a separate "
         "set.")
L.append("- The spec's \"fresh context\" is not enforced. Forecasts and attempts happen in one session, with a "
         "Phase-1 file written first. The ≤300-token forecast budget, the tool ban and the minimum-effort rule "
         "rely on the honour system; each attempt must record a short work note as its artefact. Solvers know "
         "which items are twins.")
L.append("- The void rule (forecast-vs-twin accuracy gap above 3 pp) is reported but not applied: with 15 twins "
         "the gap's standard error is about 0.14.")
L.append("- Release gates: the gate that a script of 200 lines or fewer must score near the floor would fail by "
         "construction, because every family is mechanically solvable by a short program. The no-tools policy "
         "therefore carries the construct and cannot be verified. The gate that a cue-only classifier score at "
         "chance cannot be tested with 10 stock logs. The logs are style-matched by construction: every log of a "
         "given size has the same number of unrecorded deliveries and stocktakes whatever its label.")
open(out, "w").write("\n".join(L) + "\n")
