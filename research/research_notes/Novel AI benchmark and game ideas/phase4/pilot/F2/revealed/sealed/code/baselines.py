"""F2 pilot -- trivial / shallow baselines, all operating on the public PNG sheets only.
  ALWAYS_FITS, ALWAYS_NOT      constant answers
  RANDOM_s<k>                  uniform random labels (seeded draws; the expectation is 50%)
  PIXEL_HIST_1NN               per-panel colour-pixel histogram, 1-nearest-neighbour to the 12 examples
  COUNT_STUMP                  generic count features (per shape/colour/size, #objects, #stacks, max height)
                               from the pixel parser; best single-threshold stump on the 12 examples.
                               NOTE: used as a construction filter in build.py (attempts where it scored >=6/8
                               on a problem were rejected), so its score is low partly by construction.
  COUNT_1NN                    same count features, 1-nearest-neighbour (L1) to the 12 examples (held out)
None of these knows the private rule grammar (the <=200-line 'owner script' gate of the common protocol).
PIXEL_HIST_1NN and COUNT_1NN were NOT used during construction (held-out shallow baselines).
Usage: python3 baselines.py <public_dir> <sealed_dir>
"""
import sys, os, json, random
import numpy as np
from PIL import Image
from world import RGB, SHAPES, COLOURS, SIZES, panel_boxes_examples, panel_boxes_tests
from reference import parse_problem, crop

PIDS = [f"P{i}" for i in range(1, 9)]


def write(sealed, label, probs):
    d = os.path.join(sealed, "answers_validation"); os.makedirs(d, exist_ok=True)
    json.dump({"solver_label": label, "problems": probs}, open(os.path.join(d, f"{label}.json"), "w"), indent=1)


def hist(img):
    a = np.asarray(img).astype(int)
    f = [(np.abs(a - np.array(RGB[c])).max(2) < 45).mean() for c in COLOURS]
    f.append((a.sum(2) < 200).mean())      # dark outline pixels ~ object count/perimeter
    return np.array(f)


def feats(sc):
    objs = [o for st in sc for o in st["objs"]]
    f = [sum(o[0] == s for o in objs) for s in SHAPES] + [sum(o[1] == c for o in objs) for c in COLOURS]
    f += [sum(o[2] == z for o in objs) for z in SIZES]
    f += [len(objs), len(sc), max(len(st["objs"]) for st in sc)]
    return np.array(f, float)


def stump(Xtr, ytr, Xte):
    best = (-1, None)
    for j in range(Xtr.shape[1]):
        for thr in np.unique(Xtr[:, j]):
            for sign in (1, -1):
                pred = (sign * (Xtr[:, j] - thr) >= 0)
                acc = (pred == ytr).mean()
                if acc > best[0]:
                    best = (acc, (j, thr, sign))
    j, thr, sign = best[1]
    return sign * (Xte[:, j] - thr) >= 0


def main():
    public, sealed = sys.argv[1], sys.argv[2]
    write(sealed, "ALWAYS_FITS", {p: {"labels": ["Y"] * 8, "rule": "always fits"} for p in PIDS})
    write(sealed, "ALWAYS_NOT", {p: {"labels": ["N"] * 8, "rule": "never fits"} for p in PIDS})
    for k in range(3):
        rng = random.Random(1000 + k)
        write(sealed, f"RANDOM_s{k}", {p: {"labels": [rng.choice("YN") for _ in range(8)], "rule": "random"} for p in PIDS})
    bex, _ = panel_boxes_examples(); bte, _ = panel_boxes_tests()
    nn, st, cnn = {}, {}, {}
    for p in PIDS:
        ex = Image.open(os.path.join(public, f"{p}_examples.png")).convert("RGB")
        te = Image.open(os.path.join(public, f"{p}_tests.png")).convert("RGB")
        Hx = np.array([hist(crop(ex, b)) for b in bex]); Ht = np.array([hist(crop(te, b)) for b in bte])
        y = np.array([True] * 6 + [False] * 6)
        lab = [y[np.argmin(np.abs(Hx - h).sum(1))] for h in Ht]
        nn[p] = {"labels": ["Y" if v else "N" for v in lab], "rule": "colour histogram 1-NN"}
        fits, nots, tests = parse_problem(public, p)
        Fx = np.array([feats(s) for s in fits + nots]); Ft = np.array([feats(s) for s in tests])
        pr = stump(Fx, y, Ft)
        st[p] = {"labels": ["Y" if v else "N" for v in pr], "rule": "count-feature stump"}
        lab = [y[np.argmin(np.abs(Fx - f).sum(1))] for f in Ft]
        cnn[p] = {"labels": ["Y" if v else "N" for v in lab], "rule": "count-feature 1-NN"}
    write(sealed, "PIXEL_HIST_1NN", nn)
    write(sealed, "COUNT_STUMP", st)
    write(sealed, "COUNT_1NN", cnn)


if __name__ == "__main__":
    main()
