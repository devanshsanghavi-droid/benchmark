F3 Patch Auditor pilot - sealed material.
key/          answer key (key.json), base + patched trees, spec oracles, witness driver,
              reference answers, certification results, build seed (seed.txt).
generator/    templates, patch definitions, oracles, build.py, baselines.py (all sealed code).
validation/   baseline answer files and their scores (incl. naive differential fuzzer,
              diff-size heuristic, random), beyond the three rows published in VALIDATION.md.
Score solvers:  python3 public/score.py --key sealed/key --answers <answers dir> [--per-patch]
Rebuild:        python3 generator/build.py --seed <seed from key/seed.txt> --public OUT/public --key OUT/key --fuzz 3000
