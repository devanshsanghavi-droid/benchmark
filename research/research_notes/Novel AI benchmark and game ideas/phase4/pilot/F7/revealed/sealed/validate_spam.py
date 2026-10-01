"""Mean skill of 20 independent spam (random-quantile) forecasts, using public/score.py functions. SEALED."""
import json, sys
import numpy as np
sys.path.insert(0, sys.argv[1])
import score
key, ref = score.load_key("key")
qids = sorted(ref)
clim = json.load(open("validation_answers/history_climatology.json"))["forecasts"]
spam = json.load(open("validation_answers/spam_random.json"))["forecasts"]
# the history min/max range is recovered from the public baseline builder's convention: re-derive from public data
import baselines_public as bp
rng = np.random.default_rng(99)
vals = []
import csv, os
pub = sys.argv[2]
qdoc = json.load(open(os.path.join(pub, "questions.json")))
rngs = {}
cache = {}
for q in qdoc["questions"]:
    bp.TIME_CUR = bp.TIME_COL[q["simulator"]]
    if q["simulator"] not in cache:
        cache[q["simulator"]] = bp.load(os.path.join(pub, q["folder"], "history.csv"), ["episode"])
    b = np.array([bp.outcome(r, q["outcome"]) for r in cache[q["simulator"]].values()])
    rngs[q["id"]] = (b.min(), b.max())
for k in range(20):
    ans = {qid: sorted(rng.uniform(*rngs[qid], 5).tolist()) for qid in qids}
    L = score.losses(ans, ref, qids)
    vals.append(score.skill(L, ref, qids))
print("spam mean %.1f  sd %.1f  min %.1f  max %.1f" % (np.mean(vals), np.std(vals), np.min(vals), np.max(vals)))
