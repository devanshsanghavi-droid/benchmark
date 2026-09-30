# Hidden-Rule Lab: static pilot, solver instructions

You are taking part in a small blind pilot of a visual rule-induction task. There are **8 problems (P1 to P8)**. Each problem has its own **hidden rule**. The rule decides whether a whole scene **fits** or **does not fit**.

For each problem:

1. Look at the labelled examples and work out the hidden rule.
2. Decide whether each of 8 new, unlabelled test scenes fits that rule.
3. Write down the rule you inferred as one sentence.

## Files (all in this `public/` folder)

| File | Contents |
|---|---|
| `P1_examples.png` … `P8_examples.png` | 12 labelled example scenes per problem. The **top block** (captions `YES-1` … `YES-6`) shows 6 scenes that **fit** the rule. The **bottom block** (captions `NO-1` … `NO-6`, dark caption bars) shows 6 scenes that **do not fit**. |
| `P1_tests.png` … `P8_tests.png` | 8 unlabelled test scenes per problem, captioned `T1` … `T8` (left to right, top row first). |
| `INSTRUCTIONS.md` | This file. |

`score.py` and `VALIDATION.md` are for the organisers. Do not open them. You don't need them.

## What a scene shows

- A side view of objects standing on a ground line (the brown line with the beige band below it).
- There are up to **4 stacks**, in four fixed positions from left to right. Each stack holds **1 to 3 objects**, and each object rests directly on the one below it.
- Every object has three attributes:
  - a **shape**: square, circle or triangle;
  - a **colour**: red, blue, green or yellow;
  - a **size**: small or large. The two sizes are clearly different.
- Only squares ever have something resting on top of them. Circles and triangles are always at the top of their stack.
- Captions, caption bars, panel borders and the ground band are **not** part of the scene.

## About the rules

- Each problem has exactly one rule. The same rule labels both that problem's examples and its tests. Rules in different problems are unrelated.
- A rule is deterministic and depends only on what is visible in the scene. It can involve any combination of the following:
  - object attributes;
  - how many objects of some kind there are;
  - where objects are;
  - how objects relate to each other.
- The words in a rule have their usual logical meaning. For example, a statement about "every X" is true of a scene that contains no X.
- Each rule can be stated in one plain sentence. The examples were chosen so that **every sufficiently simple rule consistent with all 12 examples gives the same labels on the 8 tests**. A correct rule must fit all 6 YES scenes and none of the 6 NO scenes. If several rules fit, prefer the simplest one. Do not rely on convoluted rules that only happen to fit.

## Tool policy (headline track: images only, no code)

**Allowed:**
- Viewing the PNG files in this folder with your image-viewing or file-reading tool (for example, `Read`). You may view each image as many times as you like.
- Reading this file.
- Writing your single answer file (see below) with a file-writing tool. If a shell command is your only way to write a file, you may use exactly one command whose only effect is to write the JSON, for example `cat > … <<'EOF'`.

**Not allowed:**
- Running any code, scripts, notebooks or shell commands, apart from the single write above.
- Any programmatic image analysis, such as cropping, zooming, pixel reading, colour picking or OCR done by code or tools. Use your own vision only.
- Reading anything outside this `public/` folder. That includes the encrypted archive next to it, other research files, git history and other solvers' answers.
- Web access.
- Asking other agents or models for help.

## Effort guidance

- There is no time limit, so work carefully.
- A good procedure for each problem:
  1. Look closely at every example panel, and note each object's shape, colour, size, stack and height.
  2. Propose candidate rules.
  3. Check each candidate against **all 12** examples.
  4. Only then label the tests.
- Spend roughly equal effort on each problem.
- Answer every problem. If you are unsure, give your best guess, because a blank label scores zero.

## Output (exact format)

Write **one JSON file** to:

```
/home/user/benchmark/research/research_notes/Novel AI benchmark and game ideas/phase4/pilot/F2/answers/<SOLVER_LABEL>.json
```

- `<SOLVER_LABEL>` is the label given to you in your prompt. Use only letters, digits, `-` and `_`. If no label was given, use `solver`.
- Create the `answers/` folder if it does not exist.
- Do not write anything else anywhere.

Schema:

```json
{
  "solver_label": "<SOLVER_LABEL>",
  "problems": {
    "P1": {"labels": ["?", "?", "?", "?", "?", "?", "?", "?"], "rule": "<one sentence stating the rule you inferred>"},
    "P2": {"labels": ["?", "?", "?", "?", "?", "?", "?", "?"], "rule": "<one sentence>"},
    "P3": {"labels": ["?", "?", "?", "?", "?", "?", "?", "?"], "rule": "<one sentence>"},
    "P4": {"labels": ["?", "?", "?", "?", "?", "?", "?", "?"], "rule": "<one sentence>"},
    "P5": {"labels": ["?", "?", "?", "?", "?", "?", "?", "?"], "rule": "<one sentence>"},
    "P6": {"labels": ["?", "?", "?", "?", "?", "?", "?", "?"], "rule": "<one sentence>"},
    "P7": {"labels": ["?", "?", "?", "?", "?", "?", "?", "?"], "rule": "<one sentence>"},
    "P8": {"labels": ["?", "?", "?", "?", "?", "?", "?", "?"], "rule": "<one sentence>"}
  }
}
```

- `labels`: exactly 8 strings, in the order T1, T2, …, T8. Each is `"Y"` (the scene fits the rule) or `"N"` (it does not). The `"?"` above are placeholders only.
- `rule`: one sentence stating the rule you inferred. It is recorded but not scored.
- The file must be valid JSON with no comments or trailing commas.

## Scoring

- Each test label that matches the answer key scores 1 point. There are 64 points in total.
- Missing or invalid labels score 0.
- Results are reported as:
  - accuracy per problem;
  - overall accuracy;
  - the number of problems with all 8 labels correct.
- Your stated rules are kept for analysis but do not affect the score.
