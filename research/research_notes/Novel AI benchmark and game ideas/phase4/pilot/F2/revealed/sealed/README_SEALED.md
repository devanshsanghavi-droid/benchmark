# F2 Hidden-Rule Lab static pilot -- sealed material (built 30 Sep 2026)

Contents
- key/key.json                  answer key (input to public/score.py)
- rules.json                    hidden rule per problem: plain-English text, grammar form, cost, family, problem seed
- scenes.json                   scene graphs of every panel (examples fit / not, tests + labels + test kind:
                                shortcut / near-miss / random)
- consistency_report.json       per problem: delta=0 and delta=+1 uniqueness checks against the private grammar,
                                simplest consistent rules, #rules enumerated, construction attempts, stump score
- seeds.json, build_log.txt     master seed, problem order, per-problem seeds
- code/world.py                 block world, mutation operator, renderer, sheet layout
- code/grammar.py               private rule grammar (cost = description length in symbols), vectorised enumerator
- code/build.py                 problem builder (pool -> tests -> greedy set-cover examples -> checks -> PNGs, key)
- code/reference.py             reference solution: pixel parser + grammar enumerator (owner oracle)
- code/baselines.py             always-fits/not, random, count stump (construction filter), count 1-NN, pixel-hist 1-NN
- answers_validation/*.json     reference + baseline answer files
- validation_scores.txt/.json   output of public/score.py on answers_validation/
- reference_diagnostics.json    parse fidelity + reference min-cost/unanimity per problem

Reproduce: cd code && python3 build.py <master_seed from seeds.json> <public_dir> ..
           python3 reference.py <public_dir> .. && python3 baselines.py <public_dir> ..
           python3 <public_dir>/score.py ../key ../answers_validation
(Requires Pillow + numpy; build takes ~1.5 min on 4 cores.)
Note: an earlier build (different seed) without the count-stump construction filter was discarded before
any solver saw it; its images and key were deleted.
