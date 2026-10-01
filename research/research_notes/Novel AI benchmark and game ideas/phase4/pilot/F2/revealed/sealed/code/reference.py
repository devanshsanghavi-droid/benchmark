"""F2 pilot -- reference solution (owner oracle) and pixel parser.

Pipeline (image-only input, i.e. the headline track's PNG sheets):
  1. parse every panel of every sheet back into a scene graph (colour segmentation + shape by fill ratio);
  2. check the parsed scene graphs against the generator's ground truth (render fidelity check);
  3. solve each problem with the owner's private grammar: enumerate rules in order of cost (up to 7),
     keep the cheapest rules consistent with the 12 labelled examples, label tests by their (unanimous) vote.
This is an oracle: it knows the private grammar. It is NOT a blind baseline.
Usage: python3 reference.py <public_dir> <sealed_dir>
"""
import sys, os, json
from collections import deque
import numpy as np
from PIL import Image
from world import (RGB, PW, PH, SLOT_X, panel_boxes_examples, panel_boxes_tests, panel_origin, canon)
from grammar import arrays, RuleSet

COLS = ["red", "blue", "green", "yellow"]


def components(mask):
    H, W = mask.shape
    seen = np.zeros_like(mask)
    out = []
    for y0, x0 in zip(*np.nonzero(mask)):
        if seen[y0, x0]:
            continue
        q = deque([(y0, x0)]); seen[y0, x0] = True; pts = []
        while q:
            y, x = q.popleft(); pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and mask[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True; q.append((yy, xx))
        out.append(np.array(pts))
    return out


def parse_panel(img):
    a = np.asarray(img).astype(int)
    objs = []
    for c in COLS:
        d = np.abs(a - np.array(RGB[c])).max(2)
        for pts in components(d < 45):
            if len(pts) < 25:
                continue
            y0, x0 = pts.min(0); y1, x1 = pts.max(0)
            w, h = x1 - x0 + 1, y1 - y0 + 1
            fill = len(pts) / (w * h)
            shape = "square" if fill > 0.9 else ("circle" if fill > 0.62 else "triangle")
            size = "large" if max(w, h) > 26 else "small"
            cx = (x0 + x1) / 2
            slot = int(np.argmin([abs(cx - s) for s in SLOT_X]))
            objs.append((slot, -y1, [shape, c, size]))
    stacks = {}
    for slot, negy, o in sorted(objs):
        stacks.setdefault(slot, []).append(o)
    return [{"slot": s, "objs": stacks[s]} for s in sorted(stacks)]


def crop(sheet, box):
    ox, oy = panel_origin(box)
    return sheet.crop((ox, oy, ox + PW, oy + PH))


def parse_problem(public, pid):
    ex = Image.open(os.path.join(public, f"{pid}_examples.png")).convert("RGB")
    te = Image.open(os.path.join(public, f"{pid}_tests.png")).convert("RGB")
    bex, _ = panel_boxes_examples(); bte, _ = panel_boxes_tests()
    exs = [parse_panel(crop(ex, b)) for b in bex]
    tes = [parse_panel(crop(te, b)) for b in bte]
    return exs[:6], exs[6:], tes


def solve(fits, nots, tests, cmax=7):
    scenes = fits + nots + tests
    A = arrays(scenes)
    RS = RuleSet(A, cmax)
    X = RS.matrix()
    y = np.array([True] * len(fits) + [False] * len(nots))
    cons = np.where((X[:, :12] == y[None]).all(1))[0]
    cmin = RS.costs[cons].min()
    best = cons[RS.costs[cons] == cmin]
    votes = X[best][:, 12:].mean(0)
    labels = ["Y" if v > 0.5 else "N" for v in votes]
    unanimous = bool(((votes == 0) | (votes == 1)).all())
    return labels, RS.descs[best[0]], int(cmin), len(best), unanimous


def main():
    public, sealed = sys.argv[1], sys.argv[2]
    truth = json.load(open(os.path.join(sealed, "scenes.json")))
    out = {"solver_label": "REFERENCE", "problems": {}}
    fidelity = {"panels": 0, "exact_match": 0}
    diag = {}
    for pid in sorted(truth):
        fits, nots, tests = parse_problem(public, pid)
        T = truth[pid]
        for got, want in zip(fits + nots + tests, T["examples_fit"] + T["examples_not"] + T["tests"]):
            fidelity["panels"] += 1
            fidelity["exact_match"] += int(canon(got) == canon(want))
        labels, desc, cmin, nbest, unan = solve(fits, nots, tests)
        out["problems"][pid] = {"labels": labels, "rule": f"(grammar, cost {cmin}) {desc}"}
        diag[pid] = dict(min_cost=cmin, n_min_cost_classes=nbest, unanimous=unan)
        print(pid, diag[pid], flush=True)
    print("parse fidelity:", fidelity)
    os.makedirs(os.path.join(sealed, "answers_validation"), exist_ok=True)
    json.dump(out, open(os.path.join(sealed, "answers_validation", "REFERENCE.json"), "w"), indent=1)
    json.dump({"parse_fidelity": fidelity, "per_problem": diag},
              open(os.path.join(sealed, "reference_diagnostics.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
