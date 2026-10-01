# F5 Self-Knowledge Exam pilot: sealed material

Contents:
- `key/key.json`: the answer key. For each item it gives the family, the hidden difficulty level (1–5), the sub-generator, the set (forecast or twin), the triage block, the answer type, the answer, the stock-log label, the prompt length and the generator metadata.
- `gen/generate.py`: the item generator. Usage: `python3 gen/generate.py $(cat gen/seed.txt) OUT_PUBLIC OUT_KEY`. It is deterministic, and the output is byte-identical to `public/items.*` and `key.json` under any PYTHONHASHSEED.
- `gen/seed.txt`: the master seed, a 64-bit value drawn from os.urandom at build time.
- `gen/verify.py`: an independent checker. It re-derives every answer from the PUBLIC item text only, using different algorithms: regex parsing, brute-force logic search, re-implemented rule grammar, enumeration of unrecorded stock quantities with non-negativity, and exec of the printed code. `gen/verify_log.txt` holds the result: 0 mismatches out of 60.
- `gen/make_validation.py` and `gen/write_validation_md.py` build the synthetic baselines and the null simulations and render `public/VALIDATION.md`. `validation_aggregates.json` holds the raw aggregate numbers, with no answers.

## Design

Six families, each with 5 levels × 2 sub-generators, give 60 items. Levels form a ladder intended to span Haiku to Fable, with no tools:

| Family | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
|---|---|---|---|---|---|
| exact-computation | 3×3-digit product; gcd | 5×4-digit product; a^e mod p | inclusion–exclusion count; lattice paths avoiding 3 points | 8×7-digit product; divisor sum σ(n) | 13×12-digit product; sub-diagonal lattice paths to (10,10) avoiding 4 points |
| logic-grid (unique solution, minimal clue set from level 2) | 3 houses × 2 attributes | 4 × 2 | 4 × 3 | 5 × 3 | 5 × 4 |
| string-trace: scramble ops / rewriting steps | 5 letters, 3 ops / 3 steps | 6, 6 / 6 | 8, 10 / 10 | 10, 16 / 16 | 12, 26 / 26 |
| program-output (Python) | loop sum; vowel shuffle | filter/sort; dict of word lengths | 3n+b loop; stack pairing | 11-cell automaton; swap/rotate | LCG queue; 3-branch while loop |
| rule-inference (list rule, unique within a grammar of 26 primitives up to depth 3) | 1 simple primitive | 1 medium primitive | 2 primitives | 2 medium | 3 primitives |
| stock-log (answer is a number, CONTRADICTORY or NOT DETERMINABLE) | 1 good × 1 warehouse, about 10 entries | 2 × 2, about 15 | 2 × 2 with a correction, about 22 | 3 × 3 with corrections and an alias, about 30 | 3 × 3 with pallets, an alias and corrections, about 40 |

Other structure:
- **Stock-log labels.** There are 4 answerable, 3 contradictory and 3 not-determinable logs. Within each level, every log has the same number of unrecorded deliveries and stocktakes (style matching). Corrections may appear after the query day.
- **Blind twins.** 15 items (25%), 2–3 per family, on distinct levels.
- **Forecast items.** 45, split at random into triage blocks A, B and C of 15; the solver picks 5 per block.
- **Presentation.** Presentation order and IDs Q01–Q60 are random.

## Tool policy

The headline track is no tools, as in the spec for non-agentic families; forecasts are made without tools. Solvers are told not to run code, use calculators or web search, or delegate to agents.

## Known limitations

These are also listed in `public/VALIDATION.md` §5:
- the pilot runs at small scale;
- there is no warm-up;
- the fixed item set spans a wide difficulty range;
- "fresh context" is replaced by a two-phase honour protocol;
- SR_twin is biased at 2–3 twins per family, so SR_glob and AUROC are used instead;
- the 200-line script gate fails by construction;
- there is no human arm, because no humans were available.

One generator bug was found by `verify.py` during stress testing and fixed: a converted shipment was dropped from the log. After the fix, 30 stress seeds verified clean. Logic puzzles whose answer equals the alphabetical listing of values (or its reverse) are rejected.
