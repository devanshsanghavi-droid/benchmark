"""Offline instrument check with SIMULATED programmatic juniors (no LLM calls).

Each simulated junior holds a set of misconceptions drawn from the live library plus a slip rate.
Each note arm has an ASSUMED effect on misconceptions. The point is to test the scoring pipeline,
not to estimate any model's ability: does NFR recover the known true effect, does the placebo sit
near 0, are over-general fixes penalised through breaks, and how wide are CIs at a given item count?
"""
import random

from .core import diagnose, live_misconceptions, make_item, nfr, nfr_ci, price

ARMS = {
    # name: (prob. each held misconception is fixed, misconceptions ADDED by the note)
    "empty": (0.0, ()),
    "placebo": (0.05, ()),
    "template_coach": (0.6, ()),
    "overgeneral_fix": (0.6, ("vol_on_docs",)),
    "strong_coach": (0.9, ()),
}


def junior_answers(item, mis, cases, slip, r):
    out = {}
    for c in cases:
        a = price(item.system, c, frozenset(mis))
        out[c.cid] = a + r.choice([-100, 100, 50]) if r.random() < slip else a
    return out


def run(n_items=60, levels=(1, 2, 3), slip=0.05, seed=1, reps=2):
    r = random.Random(seed)
    control, post = [], {a: [] for a in ARMS}
    diag_rates = []
    for k in range(n_items):
        item = make_item(1000 + k, levels[k % len(levels)])
        live = [m for m in live_misconceptions(item.system) if m != "vol_on_docs"]
        mis = set(r.sample(live, min(len(live), r.choice([2, 3]))))
        prac = junior_answers(item, mis, item.practice, slip, r)
        s, _, labels = diagnose(item, prac)
        wrong = [l for l in labels.values() if l != "correct"]
        if wrong:
            diag_rates.append(sum(l == "diagnosable" for l in wrong) / len(wrong))
        ctrl = [0.0] * len(item.fresh)
        for _ in range(reps):
            ans = junior_answers(item, mis, item.fresh, slip, r)
            for j, c in enumerate(item.fresh):
                ctrl[j] += (ans[c.cid] == item.fresh_key[c.cid]) / reps
        control.append(ctrl)
        for arm, (pfix, add) in ARMS.items():
            m2 = {m for m in mis if r.random() >= pfix} | {a for a in add if "vol" in item.system.provisions}
            ans = junior_answers(item, m2, item.fresh, slip, r)
            post[arm].append([float(ans[c.cid] == item.fresh_key[c.cid]) for c in item.fresh])
    rows = []
    for arm in ARMS:
        lo, hi = nfr_ci(control, post[arm], B=1000, seed=seed)
        rows.append((arm, nfr(control, post[arm]), lo, hi))
    ctrl_acc = sum(map(sum, control)) / sum(map(len, control))
    return rows, ctrl_acc, sum(diag_rates) / max(1, len(diag_rates))


def main():
    print("Simulated instrument check (programmatic juniors; assumed arm effects; not model data)")
    for n in (24, 60, 200):
        rows, acc, dr = run(n_items=n)
        print(f"\nitems={n}  junior control accuracy={acc:.2f}  practice errors diagnosable={dr:.2f}")
        for arm, v, lo, hi in rows:
            print(f"  {arm:16s} NFR={v:6.1f}%  95% CI [{lo:6.1f}, {hi:6.1f}]")


if __name__ == "__main__":
    main()
