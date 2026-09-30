# Self-Knowledge Exam (pilot): instructions for solvers

This exam measures two things:
1. how many of 60 freshly generated problems you solve;
2. how well you know, item by item, which of your own answers will be correct and which will not.

Both count. Read this whole file before you start.

Your **solver label** (written `<SOLVER_LABEL>` below) is given in the message that assigned you this task. Use it exactly as given.

---

## 1. Rules

**Files you may read.** Read only files inside this `public/` directory, which is `/home/user/benchmark/research/research_notes/Novel AI benchmark and game ideas/phase4/pilot/F5/public/`:
- `INSTRUCTIONS.md` (this file);
- `items.md`, or `items.json`, which has identical content in JSON.

`score.py` and `VALIDATION.md` are also here; you may read them, but you do not need them.

Do not open, list or search anything outside `public/`. That includes the rest of the repository, the encrypted archive next to this directory, and other solvers' files in `answers/`.

**Files you may write.** Write exactly two files, both in this directory (create it if it does not exist):

`/home/user/benchmark/research/research_notes/Novel AI benchmark and game ideas/phase4/pilot/F5/answers/`

- `<SOLVER_LABEL>.phase1.json`, written at the end of Phase 1;
- `<SOLVER_LABEL>.json`, your final answers, written in Phase 2.

Create no other files, including scratch or notes files.

**Tool policy (headline track: no tools).** Do all problem solving in your own reasoning. Do not use any of the following:
- code, interpreters, shells or shell arithmetic;
- calculators or spreadsheets;
- web search or any other retrieval;
- other models, agents or subagents.

The only tools you may use are:
- reading the files listed above;
- writing your two answer files.

Many items would be trivial for a program; running one defeats the exam.

**Budget.** There is no time limit. In Phase 2, think as long as you need. Phase 1 is deliberately quick.

**Honesty.** Your stated probabilities should be your real beliefs. They are scored with proper scoring rules, so honest probabilities maximise your expected score.

---

## 2. What to do

### Phase 1: forecast and triage (quick; do not solve anything)

At the top of `items.md` (and under `phase1` in `items.json`), **45 forecast items** are listed in three **triage blocks**, A, B and C, each of 15 items.

**Forecast q.** For each of the 45 forecast items:
1. Read the item.
2. Judge it briefly: at most a few sentences of thought, about 300 tokens of reasoning at most. Do **not** solve it, partly solve it, or start computing it.
3. State **q**: your probability, from 0 to 1, that the answer you give to this item in Phase 2 will be exactly correct.

**Triage.** In each block, choose **exactly 5** of its 15 items. Choose the ones you would take on if you could take only 5 from that block and were credited for each one you solve.

Every item is still attempted in Phase 2 either way. Your triage score compares how many of your 5 picks you solve with your success rate on the whole block.

**Commit.** Write `answers/<SOLVER_LABEL>.phase1.json` (schema in section 3) **before** you start Phase 2. Do not change it afterwards.

### Phase 2: attempt all 60 items

Attempt **every** item, Q01 to Q60. That includes the 15 items that were not in any Phase-1 block.

**Effort.** Make a genuine, full-effort attempt on each item, whatever you forecast in Phase 1. Do not skip items or give token attempts.

**Record three things for each item:**
- `answer`: your answer, in the item's stated **Answer format**.
- `p`: your probability, from 0 to 1, that this answer is exactly correct.
- `work`: a short note of at most 200 characters, such as a key intermediate result or the main step. This is the attempt artefact; it is required.

**Declining an item.** If you decline an item, set `answer` to `null` and `p` to `0`. A declined item counts as not solved.

**Order.** You may attempt items in any order.

**Final file.** Write `answers/<SOLVER_LABEL>.json` with:
- all 60 attempts;
- your Phase-1 `forecasts` and `triage`, copied **unchanged**.

**Answer checking.** Answers are checked automatically for exact correctness after light normalisation:
- surrounding whitespace is ignored;
- digit-group separators are ignored;
- letter case is ignored where the format has no meaningful case;
- a list may be written as a JSON list or as a comma-separated string.

Give only the answer in `answer`, with no explanation. For printed program output, give exactly the line printed.

---

## 3. Output schema

Both files must be valid JSON: no comments and no trailing commas. The item IDs are `Q01` to `Q60`.

The blocks below are templates. Replace every `<...>` with a real value:
- `<id>` is an item ID string such as `"Q01"`;
- `<q>` and `<p>` are numbers from 0 to 1;
- `<answer>` is a string or integer, or `null` if you decline;
- `<note>` is a short string.

**Phase 1: `answers/<SOLVER_LABEL>.phase1.json`**

```text
{
  "solver_label": "<SOLVER_LABEL>",
  "forecasts": { <id>: <q>, <id>: <q>, ... },
  "triage": {
    "A": [<id>, <id>, <id>, <id>, <id>],
    "B": [<id>, <id>, <id>, <id>, <id>],
    "C": [<id>, <id>, <id>, <id>, <id>]
  }
}
```

- `forecasts` has exactly 45 entries: one for each forecast item and no others.
- Each triage list holds exactly 5 distinct IDs taken from that block.

**Final: `answers/<SOLVER_LABEL>.json`**

```text
{
  "solver_label": "<SOLVER_LABEL>",
  "forecasts": { ...identical to the Phase-1 file... },
  "triage": { ...identical to the Phase-1 file... },
  "attempts": {
    <id>: {"answer": <answer>, "p": <p>, "work": <note>},
    ...one entry for every item, Q01 to Q60...
  },
  "notes": "optional free text"
}
```

List answers may be written as a JSON list or as a string.

---

## 4. How you are scored

- **Accuracy:** the share of the 60 items answered exactly correctly.
- **Your confidence p:** scored with the log score and the Brier score. Log scores clip probabilities to [0.01, 0.99]. p is also scored on how well it separates your correct answers from your incorrect ones.
- **Your forecasts q:** scored the same way, on the forecast items.
- **Triage value:** how many of your 5 picks per block you solve, compared with your success rate on the whole block.

Probabilities of 0 or 1 are penalised heavily when they are wrong.

---

## 5. Checklist before you finish

- [ ] The Phase-1 file was written before any Phase-2 work, with 45 forecasts and 3 × 5 triage picks.
- [ ] The final file has 60 attempts, each with `answer`, `p` and `work`.
- [ ] `forecasts` and `triage` in the final file are identical to the Phase-1 file.
- [ ] Both files parse as valid JSON and are in the `answers/` directory under the exact names above.
- [ ] You used no tools other than reading `public/` files and writing your two answer files, and you read nothing outside `public/`.
