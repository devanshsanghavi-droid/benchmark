"""Assemble key/key.json + key/truth_samples.npz from sealed rollouts; write reference answer files. SEALED."""
import glob, json, os
import numpy as np
from config import QUESTIONS, QKEYS, QUANTILES

KEY = "key"
arr = {}
for f in glob.glob(os.path.join(KEY, "samples_*.npz")):
    z = np.load(f)
    arr.update({k: z[k] for k in z.files})
naive = json.load(open("validation_answers/naive_extrapolator.json"))["forecasts"]
key = {"version": "F7-UnrunLab-pilot-2026-09-30", "quantile_levels": QUANTILES,
       "scale_rule": "std of pooled (truth rollouts, no-change rollouts)", "questions": {}}
truth = {}
refs = {"nochange_true_model": {}, "oracle_true_model": {}, "ideal_insample_truth": {}}
for q in QUESTIONS:
    qid = q["id"]
    y = arr["truth__" + qid]; nc = arr["nochange__" + qid]; orc = arr["oracle__" + qid]
    assert len(y) == 10000 and len(nc) == 10000 and len(orc) == 10000, qid
    scale = float(np.std(np.concatenate([y, nc])))
    qn = [float(v) for v in np.quantile(nc, QUANTILES)]
    qo = [float(v) for v in np.quantile(orc, QUANTILES)]
    qi = [float(v) for v in np.quantile(y, QUANTILES)]
    key["questions"][qid] = {"simulator": q["sim"], "scale": scale, "nochange": qn, "oracle": qo,
                             "naive": [naive[qid][k] for k in QKEYS]}
    truth[qid] = y.astype(np.float64)
    refs["nochange_true_model"][qid] = dict(zip(QKEYS, qn))
    refs["oracle_true_model"][qid] = dict(zip(QKEYS, qo))
    refs["ideal_insample_truth"][qid] = dict(zip(QKEYS, qi))
json.dump(key, open(os.path.join(KEY, "key.json"), "w"), indent=1)
np.savez_compressed(os.path.join(KEY, "truth_samples.npz"), **truth)
for name, fc in refs.items():
    json.dump({"solver_label": name, "forecasts": fc}, open(os.path.join("validation_answers", name + ".json"), "w"), indent=1)
print("key built:", len(key["questions"]), "questions")
