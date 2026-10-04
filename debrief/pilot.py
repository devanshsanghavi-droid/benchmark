"""Live pilot driver for DEBRIEF (v0). Prompts go to files; model agents write replies to files; this scores them.

Layout under results/pilot_v0/:
  prompts/<stage>/item_<k>.txt   prompt shown to the agent for item k
  replies/<stage>/item_<k>.txt   the agent's full reply (working + final answer lines / <note>)
  notes/<arm>.json               the note text per item for each arm
  items/item_<k>.json            items with keys (copied in only at scoring time)

Stages: practice (junior on practice cases), control_r1, control_r2, placebo, template, coach_<label>,
post_<label> (junior with that coach's notes).

Usage:
  python -m debrief.pilot prepare  --keys KEYDIR
  python -m debrief.pilot coaches  --keys KEYDIR             # after replies/practice exist
  python -m debrief.pilot post     --keys KEYDIR --coach haiku sonnet ...   # after replies/coach_<label> exist
  python -m debrief.pilot score    --keys KEYDIR
"""
import argparse
import json
import os
import shutil
import statistics

from .core import (PLACEBO_NOTE, Case, Item, System, coach_prompt, diagnose, junior_prompt, make_item, nfr, nfr_ci,
                   parse_answers, parse_note, template_coach_note)

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "pilot_v0")
ITEMS = [(201, 2), (202, 2), (203, 2), (204, 3), (205, 3), (206, 3)]
BUDGET = 150


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text)


def _r(path):
    return open(path).read() if os.path.exists(path) else ""


def load_item(keys, k):
    d = json.load(open(os.path.join(keys, f"item_{k}.json")))
    sysd = d["system"]
    s = System(**sysd)
    mk = lambda c: Case(**{**c, "dims": tuple(c["dims"])})
    return Item(s, d["spec"], [mk(c) for c in d["practice"]], [mk(c) for c in d["fresh"]], d["practice_key"], d["fresh_key"])


def prepare(keys):
    os.makedirs(keys, exist_ok=True)
    for k, (seed, level) in enumerate(ITEMS, 1):
        it = make_item(seed, level)
        _w(os.path.join(keys, f"item_{k}.json"), it.to_json())
        _w(os.path.join(ROOT, "prompts", "practice", f"item_{k}.txt"), junior_prompt(it, it.practice, None))
        for st in ("control_r1", "control_r2"):
            _w(os.path.join(ROOT, "prompts", st, f"item_{k}.txt"), junior_prompt(it, it.fresh, None))
        _w(os.path.join(ROOT, "prompts", "placebo", f"item_{k}.txt"), junior_prompt(it, it.fresh, PLACEBO_NOTE))
    _w(os.path.join(ROOT, "notes", "placebo.json"), json.dumps({str(k): PLACEBO_NOTE for k in range(1, len(ITEMS) + 1)}, indent=1))
    print("prepared", len(ITEMS), "items")


def coaches(keys):
    tmpl = {}
    for k in range(1, len(ITEMS) + 1):
        it = load_item(keys, k)
        reply = _r(os.path.join(ROOT, "replies", "practice", f"item_{k}.txt"))
        ans = parse_answers(reply)
        working = reply.strip()
        p = coach_prompt(it, ans, BUDGET)
        p = p.replace("\n\nReply with the note only",
                      f"\n\nJUNIOR'S WORKING (verbatim):\n<<<\n{working}\n>>>\n\nReply with the note only")
        _w(os.path.join(ROOT, "prompts", "coach", f"item_{k}.txt"), p)
        tmpl[str(k)] = template_coach_note(it, ans, BUDGET)
        _w(os.path.join(ROOT, "prompts", "template", f"item_{k}.txt"), junior_prompt(it, it.fresh, tmpl[str(k)]))
    _w(os.path.join(ROOT, "notes", "template.json"), json.dumps(tmpl, indent=1))
    print("coach prompts + template arm written")


def post(keys, labels):
    for lab in labels:
        notes = {}
        for k in range(1, len(ITEMS) + 1):
            it = load_item(keys, k)
            note = parse_note(_r(os.path.join(ROOT, "replies", f"coach_{lab}", f"item_{k}.txt")), BUDGET)
            notes[str(k)] = note
            _w(os.path.join(ROOT, "prompts", f"post_{lab}", f"item_{k}.txt"), junior_prompt(it, it.fresh, note))
        _w(os.path.join(ROOT, "notes", f"coach_{lab}.json"), json.dumps(notes, indent=1))
    print("post-test prompts written for", labels)


def _correct(it, stage):
    ans = parse_answers(_r(os.path.join(ROOT, "replies", stage, f"item_{_correct.k}.txt")))
    return [1.0 if ans.get(c.cid) == it.fresh_key[c.cid] else 0.0 for c in it.fresh]


def score(keys):
    n = len(ITEMS)
    items = [load_item(keys, k) for k in range(1, n + 1)]
    os.makedirs(os.path.join(ROOT, "items"), exist_ok=True)
    for k in range(1, n + 1):
        shutil.copy(os.path.join(keys, f"item_{k}.json"), os.path.join(ROOT, "items", f"item_{k}.json"))
    stages = sorted(d for d in os.listdir(os.path.join(ROOT, "replies")))
    corr = {}
    for st in stages:
        rows = []
        for k, it in enumerate(items, 1):
            _correct.k = k
            rows.append(_correct(it, st))
        corr[st] = rows
    reps = [s for s in ("control_r1", "control_r2") if s in corr]
    control = [[statistics.mean(corr[s][i][j] for s in reps) for j in range(len(items[i].fresh))] for i in range(n)]
    out = {"items": [{"seed": s, "level": l} for s, l in ITEMS], "arms": {}}
    # practice diagnostics
    pr = []
    for k, it in enumerate(items, 1):
        ans = parse_answers(_r(os.path.join(ROOT, "replies", "practice", f"item_{k}.txt")))
        s, _, labels = diagnose(it, ans)
        pr.append({"item": k, "practice_correct": sum(v == "correct" for v in labels.values()),
                   "diagnosable": sum(v == "diagnosable" for v in labels.values()),
                   "slip": sum(v == "slip" for v in labels.values()), "blamed": sorted(s)})
    out["practice"] = pr
    acc = lambda rows: sum(map(sum, rows)) / sum(map(len, rows))
    out["control_accuracy"] = {s: acc(corr[s]) for s in reps}
    out["control_accuracy_mean"] = acc(control)
    if len(reps) == 2:
        out["control_test_retest_agreement"] = (sum(a == b for i in range(n) for a, b in zip(corr[reps[0]][i], corr[reps[1]][i]))
                                                / sum(len(r) for r in corr[reps[0]]))
        # replicate-vs-replicate NFR: pure noise floor
        out["noise_floor_nfr_r2_vs_r1"] = nfr(corr[reps[0]], corr[reps[1]])
    arms = [s for s in stages if s not in ("practice",) + tuple(reps)]
    for a in arms:
        post_rows = corr[a]
        fixed = sum(1 for i in range(n) for c, p in zip(control[i], post_rows[i]) if p > c)
        lo, hi = nfr_ci(control, post_rows)
        by_level = {}
        for lvl in sorted({l for _, l in ITEMS}):
            idx = [i for i, (_, l) in enumerate(ITEMS) if l == lvl]
            by_level[f"L{lvl}"] = nfr([control[i] for i in idx], [post_rows[i] for i in idx])
        gains = sum(max(0.0, p - c) for i in range(n) for c, p in zip(control[i], post_rows[i]))
        breaks = sum(max(0.0, c - p) for i in range(n) for c, p in zip(control[i], post_rows[i]))
        out["arms"][a] = {"accuracy": acc(post_rows), "NFR": nfr(control, post_rows), "CI95": [lo, hi],
                          "by_level": by_level, "fix_mass": gains, "break_mass": breaks, "cases_improved": fixed}
    notes_dir = os.path.join(ROOT, "notes")
    out["note_words"] = {f[:-5]: [len(v.split()) for v in json.load(open(os.path.join(notes_dir, f))).values()]
                         for f in sorted(os.listdir(notes_dir))}
    _w(os.path.join(ROOT, "scores.json"), json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="debrief.pilot")
    ap.add_argument("cmd", choices=["prepare", "coaches", "post", "score"])
    ap.add_argument("--keys", required=True)
    ap.add_argument("--coach", nargs="*", default=[])
    a = ap.parse_args(argv)
    {"prepare": lambda: prepare(a.keys), "coaches": lambda: coaches(a.keys),
     "post": lambda: post(a.keys, a.coach), "score": lambda: score(a.keys)}[a.cmd]()


if __name__ == "__main__":
    main()
