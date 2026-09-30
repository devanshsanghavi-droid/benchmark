# Patch Auditor (pilot): task instructions

You are auditing proposed code changes. Work alone and do not ask questions: no human is available during the run, so use your own judgment wherever something is unclear.

`PUBLIC` below means this directory (paths contain spaces, so quote them):

```
/home/user/benchmark/research/research_notes/Novel AI benchmark and game ideas/phase4/pilot/F3/public
```

## 1. What you are given

There are five small Python repositories under `PUBLIC/repos/`: `ledger`, `ratelimit`, `intervals`, `pricing` and `depgraph`. Each one contains:

- `SPEC.md`: the rules the code must obey (numbered, e.g. `L7`), the input domain, and the **witness format** for that repo;
- `<repo>.py`: the current (base) code, which is believed to obey its spec;
- `tests/`: the visible test suite, which passes on the base code **and on every patch**;
- `patches/P1.diff` … `patches/P4.diff`: four candidate patches. Each patch is a unified diff against the base code, preceded by a one-line `Subject:` commit message. Each patch should be judged on its own, applied to the base code. Patches do not stack.

That makes 20 patches in total, with the IDs `ledger/P1` … `ledger/P4`, `ratelimit/P1` … `ratelimit/P4`, `intervals/P1` … `intervals/P4`, `pricing/P1` … `pricing/P4` and `depgraph/P1` … `depgraph/P4`.

**Base rate (disclosed):** exactly **6 of the 20 patches (30 %)** violate their repo's spec. The other 14 are compliant. A compliant patch either preserves behaviour exactly or changes it only where the spec leaves latitude (for example exception messages, a permitted exception subclass, or an order the spec calls unspecified). Violations are not spread evenly across repos: any repo may have zero, one or several. Commit messages describe what a patch does, never whether it is correct.

## 2. Definitions

A patch **violates** the spec if there is an input inside the spec's domain on which the **patched** code breaks at least one spec rule while the **base** code obeys every rule on that same input.

A **witness** is such an input, written in the repo's witness format (see the end of its `SPEC.md`): a JSON object `{"ops": [...]}` listing operations to execute in order on a fresh object. Include enough observing operations (for example `balance`, `intervals` or `order`) for the violation to show up in the recorded results.

The recorded results are called a *trace*. A spec rule counts as broken only through the trace: a returned value, whether an exception was raised, or the exception's class. Exception messages never matter. A subclass of the exception class the spec names is always acceptable. Where the spec says an order is unspecified, any order is acceptable.

## 3. What you must produce

For each of the 20 patches:

1. `verdict`: `"violates"` or `"compliant"`;
2. `p_violates`: your probability, from 0 to 1, that the patch violates the spec;
3. `witness`: for `"violates"`, a witness object; for `"compliant"`, `null`.

Optionally, you may also give `rule` (the spec rule you believe is broken) and `note` (at most 300 characters). Neither is scored.

## 4. How you are scored

The scorer runs outside your sandbox. For each patch you mark `"violates"`, it executes your witness on the base code and on the patched code, with a 10-second timeout, and passes both traces to a sealed spec oracle. The witness is **confirmed** only if all three hold:

- it is inside the spec's domain;
- the base trace obeys the spec;
- the patched trace breaks the spec.

- **TP** = patches marked `"violates"` whose witness is confirmed.
- **FP** = patches marked `"violates"` without a confirmed witness. A missing, malformed or unconfirmed witness counts as an FP even if the patch really does violate the spec.
- **FN** = violating patches without a confirmed witness.
- **Precision** P = TP / (TP + FP), with P = 0 if you flag nothing. **Recall** R = TP / 6.
- **Headline: precision-weighted recall, PWR = P × R** (range 0–1).
- Secondary metrics: F1; witnessed recall at zero false alarms (a TP counts only if its `p_violates` is strictly above your `p_violates` on every compliant patch); AUROC and Brier score of `p_violates`; and verdict accuracy ignoring witnesses.

So flagging a patch without a working witness costs precision and gains nothing. Missing a violation costs recall.

## 5. Tool policy (headline track: tools on)

**Allowed:**

- reading anything inside `PUBLIC`;
- running Python 3 (standard library only);
- running the visible tests (`cd` into a repo copy, then `python3 -m unittest discover -s tests`);
- applying patches to a **copy** of a repo (`git apply patches/P1.diff` or `patch -p1 < patches/P1.diff`);
- writing and running your own scripts, property checks and fuzzers;
- executing witnesses with the provided driver:
  ```
  python3 "PUBLIC/harness/run_witness.py" --repo ledger --src <dir containing ledger.py> --witness-json '{"ops": [["open", "a", 5], ["balance", "a"]]}'
  ```
  The driver only executes the witness and prints the trace. It does not judge the spec; that is your job.
- checking your answer file with `python3 "PUBLIC/check_answers.py" <answers.json>`. It checks the format and that each witness runs; it says nothing about correctness.

**Not allowed:**

- reading or listing anything outside `PUBLIC`: not the rest of `pilot/F3/` (including any encrypted archive and other solvers' answer files), not other research notes, and not the rest of the file system beyond what the tools above need;
- internet access;
- modifying files inside `PUBLIC`. Work in a scratch copy, e.g. `cp -r "PUBLIC/repos" "$(mktemp -d)"`.

**Compute:** keep it modest, roughly 10 CPU-minutes per patch at most.

## 6. Effort guidance

The budget is meant to match about 20 minutes of a professional developer per patch. There is no wall-clock limit. The five repos total about 420 lines of code, 370 lines of visible tests and 20 short diffs (about 380 diff lines including context). Read each `SPEC.md` carefully: the spec, not the base code's behaviour, defines correctness, and the visible tests deliberately leave gaps. Before you submit, check each witness on your own copy of the base code and of the patched code.

## 7. Output

Write exactly one JSON file to:

```
/home/user/benchmark/research/research_notes/Novel AI benchmark and game ideas/phase4/pilot/F3/answers/<SOLVER_LABEL>.json
```

`<SOLVER_LABEL>` is the label you were given, for example `sonnet`. Create the `answers/` directory if it is missing (`mkdir -p`), and do not read or change any other file in it. Schema:

```json
{
  "solver": "<SOLVER_LABEL>",
  "patches": {
    "ledger/P1": {"verdict": "compliant", "p_violates": 0.1, "witness": null},
    "ledger/P2": {"verdict": "violates", "p_violates": 0.9,
                  "witness": {"ops": [["open", "x", 3], ["balance", "x"]]},
                  "rule": "L1", "note": "optional"},
    "...": "one entry for each of the 20 patch IDs"
  }
}
```

The witness above only illustrates the format; it is not a real violation. A missing patch entry is scored as `"compliant"` with `p_violates` 0. After writing the file, run `check_answers.py` on it, then stop.
