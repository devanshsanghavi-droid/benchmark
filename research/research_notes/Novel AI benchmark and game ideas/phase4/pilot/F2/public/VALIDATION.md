# F2 Hidden-Rule Lab static pilot: validation (organiser file; contains no answers)

Built 30 Sep 2026. The pilot has 8 problems with 8 test panels each, 64 test labels in all. The solver sees 16 PNG sheets:

- 8 example sheets of 668×892 px, each with 12 labelled panels (6 fit, 6 do not);
- 8 test sheets of 886×456 px, each with 8 unlabelled panels.

Each panel's drawing area is 200×150 px. The answer key, the rules, the generator, the seeds, and the reference and baseline answer files are in `../sealed.tar.gz.enc`.

## Engineering checks

| Check | Result |
|---|---|
| Reference solution: owner oracle using a pixel parser and the private-grammar enumerator on the PNGs | **64/64 = 100.0%**; 8/8 problems fully correct |
| Pixel-to-scene-graph parse fidelity: 160 panels vs generator ground truth | 160/160 exact |
| Test labels determined at δ = 0 (every grammar rule with cost ≤ the true rule's cost that fits all 12 examples gives the key's labels) | 8/8 problems; exactly 1 semantic class survives in every problem |
| Test labels determined at δ = +1 (rules one symbol costlier also checked) | 8/8 problems (0 surviving rules disagree on any test) |
| True-rule cost, in grammar symbols (range over problems) | 2–5 |
| Distinct rules enumerated per problem (up to the true cost + 1) | 562 – 99,508 |

## Baselines (single run each; 95% CI = bootstrap over problems)

| Solver | Correct | Accuracy | 95% CI | Problems 8/8 |
|---|---|---|---|---|
| Reference (oracle, knows the grammar) | 64/64 | 100.0% | [100.0, 100.0] | 8 |
| Always "fits" | 29/64 | 45.3% | [39.1, 53.1] | 0 |
| Always "does not fit" | 35/64 | 54.7% | [46.9, 60.9] | 0 |
| Random: expectation (analytic or simulated) | 32/64 | 50.0% | [37.5, 62.5] (central 95% of draws) | 0.03 expected |
| Random, seeded draw 0 | 32/64 | 50.0% | [40.6, 57.8] | 0 |
| Random, seeded draw 1 | 33/64 | 51.6% | [37.5, 65.6] | 0 |
| Random, seeded draw 2 | 31/64 | 48.4% | [40.6, 57.8] | 0 |
| Count-feature decision stump (≤200 lines; **used as a construction filter**, see note) | 35/64 | 54.7% | [48.4, 60.9] | 0 |
| Count-feature 1-NN (≤200 lines; held out) | 38/64 | 59.4% | [42.2, 73.4] | 0 |
| Pixel colour-histogram 1-NN (≤200 lines; held out) | 35/64 | 54.7% | [37.5, 70.3] | 0 |

**Note on the construction filter.**
- Test and example sets were rejected when the count-feature stump, trained on the 12 examples, got 6 or more of the 8 tests right. This mirrors the spec's shortcut-separating probes. It was triggered on 1 problem, where 2 draws were rejected.
- The stump's score is therefore low partly by construction. The two 1-NN baselines were not used during construction.
- In an earlier, discarded build without the filter, the stump scored 70.3% and the histogram 1-NN scored 65.6%.

## What this pilot can and cannot show

- **No human baseline.** No humans were available, so the A1 question from the spec (do humans beat frontier models?) is **not measured here**. Nor are the human pre-launch gates: at least 60 humans, and at least 2 humans solving every family.
- **Static, not interactive.**
  - The owner chose the examples by greedy set cover against the grammar, so the subject runs no experiments.
  - The bounded adversary is approximated by uniqueness at δ = 0 and δ = +1 with respect to the owner's grammar. Rules outside that grammar are not covered by the check.
  - The spec's headline metric, experiments to success, is not measured.
- **Small n.** There are 8 problems × 8 tests and one attempt per model, so 95% CIs are about ±10–15 pp. Treat tier differences under about 15 pp as noise.
- **Perception confound.** The rendered scenes are simple, flat, 2D and settled, with none of the spec's physics ambiguity (lean, contact). The render is lossless: the parser recovers 160/160 panels exactly.

## How to score (organisers)

```
openssl enc -d -aes-256-cbc -pbkdf2 -in sealed.tar.gz.enc -out /tmp/f2s.tgz   # prompts for the passphrase
mkdir -p /tmp/f2s && tar xzf /tmp/f2s.tgz -C /tmp/f2s
python3 public/score.py /tmp/f2s/sealed/key answers/ --show-rules
rm -rf /tmp/f2s /tmp/f2s.tgz
```
