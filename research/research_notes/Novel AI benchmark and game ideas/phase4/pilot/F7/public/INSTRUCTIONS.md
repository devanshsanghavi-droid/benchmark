# Unrun Lab - pilot task (F7, Track S miniature)

You are a solver in a blind pilot. There are five secret **stochastic simulators** (S1 to S5). For each one you get a partial description, baseline data and the results of a few pre-run experiments. Your job is to **forecast the distribution of stated outcomes under interventions that have not been run**, as quantiles. There are 15 questions, 3 per simulator. Do not try to be clever about the scoring: a proper scoring rule rewards honest, well-calibrated distributions.

## What you get (everything is inside this `public/` folder)
- `questions.json` - the 15 questions. Each has the interventions in machine-readable form, the outcome definition (`column`, plus either `time_index` or `aggregate` over `from`..`to` inclusive, and `community` for S3) and a plain-English statement.
- For each simulator, a folder `S1_pond/`, `S2_calldesk/`, `S3_adoption/`, `S4_auction/`, `S5_fermenter/` containing:
  - `description.md` - what the system is, what each column means, and what each intervention does. It is partial: the equations, parameters and some state variables are hidden.
  - `history.csv` - about 10,000 rows of observational data from independent baseline episodes with no interventions.
  - `experiments.csv` and `experiments.json` - 20 sample paths from a fixed menu of pilot experiments with interventions, and the menu itself.
- `score.py` - the scorer (it needs the sealed key, which you do not have). You may read it to understand the scoring.
- `VALIDATION.md` - scores of reference forecasters.

About the simulators: each is a mechanistic stochastic model built for this pilot, not a standard textbook model. It may contain features such as delays, thresholds, saturation, feedback loops, heavy-tailed shocks, regime switches and unobserved state variables. Descriptions do not say which. All time indices are 0-based. An intervention acts from the start of its `start` step, and everything not mentioned stays at baseline.

## What each question asks
Imagine a **fresh, independent episode** of the simulator, not one of the history episodes, with exactly the stated interventions applied. The outcome is a single number computed from that episode's **recorded** values: the same columns as in the CSVs, including measurement noise. Examples are the value of `grazers` on day 350, or the sum of `abandoned` over hours 216-335. Give the **5%, 25%, 50%, 75% and 95% quantiles** of that outcome's distribution across such episodes. The distribution covers all randomness: the starting state, the process noise and the measurement noise. Use the units of the outcome column.

## Tool policy (headline policy for this track: code is part of the construct)
- You **may** write and run code to analyse the provided data and to build and fit your own models or simulators. Python 3 with the standard library and numpy is recommended. You may use other packages that are already installed, but install nothing new.
- **No internet access** of any kind: no web search, no downloads and no external APIs.
- **Do not read anything outside this `public/` folder.** That includes the encrypted archive and any other files in parent folders, other solvers' answers, and other projects. Your prior knowledge is fine.
- You may create scratch files in a private temporary directory, for example under `/tmp`, and read your own scratch files back.
- Keep the total CPU time of your own code to about 30 minutes. There is no wall-clock limit.
- Work alone: no other people and no other AI systems.

## Output: exactly one JSON file
Write your answers to:

`/home/user/benchmark/research/research_notes/Novel AI benchmark and game ideas/phase4/pilot/F7/answers/<SOLVER_LABEL>.json`

`<SOLVER_LABEL>` is the label you were given. If you were not given one, use a short name for yourself with no spaces. Write only that one file in `answers/`; do not read or modify any other file there. The schema is:

```json
{
  "solver_label": "<SOLVER_LABEL>",
  "forecasts": {
    "S1-Q1": {"q05": 0.0, "q25": 0.0, "q50": 0.0, "q75": 0.0, "q95": 0.0},
    "S1-Q2": {"q05": 0.0, "q25": 0.0, "q50": 0.0, "q75": 0.0, "q95": 0.0},
    "...": "one entry for each of the 15 ids: S1-Q1..S1-Q3, S2-Q1..S2-Q3, S3-Q1..S3-Q3, S4-Q1..S4-Q3, S5-Q1..S5-Q3"
  },
  "notes": "optional, at most 200 words; not scored"
}
```

Rules for the file:
- Every value must be a finite JSON number.
- Within a question, quantiles must be non-decreasing (`q05 <= q25 <= q50 <= q75 <= q95`). Non-monotone sets are sorted and flagged.
- A missing or invalid question scores **-100** on that question.
- Validate the file with `python3 -c "import json; json.load(open('<path>'))"` before you finish.

## Scoring (for your information)
- **Ground truth** for each question is 10,000 sealed rollouts of the true simulator under the stated interventions.
- **Quantile score:** for each question, the pinball (quantile) loss of your five quantiles is averaged over the 10,000 rollouts and the 5 levels, then divided by a fixed per-question scale factor. This is a proper scoring rule and a discrete approximation to CRPS.
- **Skill** = 100 x (QS_no-change - QS_you) / (QS_no-change - QS_oracle), where:
  - "no-change" forecasts the true distribution of the outcome **without** the intervention;
  - "oracle" is the true model's forecast **with** the intervention.
  So 0 means no better than assuming the intervention does nothing, 100 means as good as knowing the true model, and scores can be negative.
- The overall and per-simulator skills are ratios of **sums** over questions.

## About this pilot (deviations from the full F7 spec)
This is a small blinded pilot of F7 "Unrun Lab", Track S. Compared with the full specification:
- It has 5 simulators and 15 questions, instead of 20 simulators and 50 questions per run.
- It has quantile questions only; there are no probability questions.
- **Experiments are pre-run from a fixed menu (20 sample paths per simulator).** In the full spec, solvers choose 20 interventions interactively from a menu through a live oracle; this pilot avoids needing a live oracle.
- The skill zero point is the no-change forecast. The spec uses the better of an AutoML pipeline and an owner-written generic learner as the zero point; here a naive extrapolator is reported only as a reference in `VALIDATION.md`.
- There is no frozen harness or sandbox: the tool policy above is enforced by instruction only.
- No human baseline was run, because no humans were available for this pilot.
