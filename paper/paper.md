---
title: "Grade the Ripple, Not the Stone"
subtitle: "Why AI benchmarks die, what survived a red-teamed search for new ones, and a live pilot of DEBRIEF, a benchmark that scores what a model's note changes in another model"
author: "Benchmark research project (multi-agent study coordinated with Claude Code)"
date: "October 2026"
abstract: |
  We asked what makes an AI benchmark durable and discriminative, then searched for a new one. Seven evidence panels (about 465 fact-checked claims) covered benchmarks humans still win, benchmarks AI wins that still separate models, dead and saturated benchmarks, games, capability gaps, test-time learning and evaluation methodology. The common hypothesis that failed benchmarks "lack novel thinking a model could not have trained on" is only partly right: novelty prevents item contamination, but novel benchmarks such as ARC-AGI-3 (under 1% to 99.9% in about five months) and FrontierMath Tier 4 (5% to 98% in under 14 months) still fell. What failed benchmarks share is a cheap path to a higher score that bypasses the named ability, plus no owner renewing the task faster than labs optimise against it. We generated 47 candidates, attacked them with seven independent red teams, and ran blinded pilots on five finalists with four Claude model tiers. Pilots killed three finalists outright: clean visual rule induction, patch auditing and self-knowledge quizzes all saturated at the mid tier. A bot-writing league on a secret new game (Season Forge) produced the widest separation (0.41 to 5.08 ladder rungs). We then built and piloted DEBRIEF, which scores the share of a fixed junior model's errors that a 150-word note from the model under test removes on unseen cases. Version 0 failed its first gate: the Haiku junior priced generated tariffs at 98.6% accuracy, leaving nothing to coach. We report the v0.2 redesign and its pilot below. The broad lesson is that durable benchmarks need renewal as the mechanism, an outcome measured on something other than the model's own answer, and pre-registered gates that are allowed to fail.
---

# Introduction

Benchmarks are how the field decides which models are good. Most of them stop working within two years. Static sets now stay in lab headline tables for roughly 7 to 30 months, and the hardest 2025 sets went from single digits to near ceiling in 13 to 18 months. This paper has three parts:

1. **Why benchmarks succeed or fail**, from fact-checked evidence (Section 2).
2. **A red-teamed search for a new benchmark or game**, with blinded pilots that killed most of the shortlist (Section 3).
3. **DEBRIEF**, a non-game benchmark that grades the effect of a model's explanation on another model, and its live pilots, including a failed first version (Sections 4 and 5).

We use two archetypes throughout. In **A1**, humans clearly outperform AI (the ARC-AGI pattern). In **A2**, AI clearly outperforms typical humans but the results still separate strong from weak models, ideally in informative ways such as cheap models beating expensive ones (the StudentBench pattern [@northcutt2026studentbench]).

All evidence files, fact-check logs, pilot materials and decrypted answer keys are in the repository under `research/research_notes/Novel AI benchmark and game ideas/` and `results/`. Claims we could see only through search-engine summaries, because the environment blocked several primary hosts, are marked [S].

# Why benchmarks succeed or fail

## The novelty hypothesis

The working hypothesis was that failed benchmarks "lack novel critical thinking that a model can't have been trained on beforehand". Panel C coded 36 benchmark histories. Under the reading "unseen instances", 5 cases support it, 10 contradict it and 21 are neutral. Under the reading "novel skills", it is about 9 / 6 / 21. The counts depend on coding, so the verdict rests on counterexamples that hold under every reading:

- **ARC-AGI-3**, a novel interactive family with no item leakage, went from under 1% at launch (25 Mar 2026) to 62.7% on ARC's standard harness and 98.6% on a state-preserving harness for the same model at the same effort, and 99.9% at higher effort, in about five months [@arc2026astra].
- **FrontierMath Tier 4**, built from unpublished problems, went from 5% to 98% in under 14 months, on an error-corrected v2 set [@epoch2026tier4].
- **ARC-AGI-1** had 49% of its private set solved by a 2020 ensemble of brute-force program searches [@chollet2024arcprize].

The converse also fails: GPQA [@rein2024gpqa], SWE-bench and AutomationBench [@zapier2026automationbench] stayed useful without novel skills. The kernel of the hypothesis is real for static public items. AIME 2024 scores run above what AIME 2025 predicts [@balunovic2025matharena], and OpenAI retired SWE-bench Verified after models reproduced gold patches [@openai2026swebv].

**Refined statement.** A benchmark fails when the cheapest way to raise its score stops running through the named capability, and no owner renews items, families and protocol faster than labs optimise against them.

## Failure modes, and which ones novelty prevents

| Failure mode | Does novelty prevent it? | Example |
|---|---|---|
| Item contamination | Yes | AIME 2024; SWE-bench Verified |
| Training on the task family | Only while the generator stays secret | Logic-RL reached 0.99 after about 5k synthetic puzzles [@xie2025logicrl] |
| Brute force or writing a solver | No | ARC-AGI-1's 49% ensemble |
| Harness capture | No | ARC-AGI-3: 62.7% vs 98.6%, same model and effort |
| Broken validity | No; novel expert sets are more error-prone | A do-nothing agent scores 38% on τ-bench [@zhu2025abc]; 42% of FrontierMath problems needed fixes |
| Gaming and selective submission | No | 27 private Llama 4 variants on LMArena [@singh2025leaderboard] |
| Noise and thin baselines | No | Median human baseline is 8 people [@wei2025humanbaselines]; a 3-point gap needs about 1,000 items [@miller2024errorbars] |
| Adoption failure | No | OfficeBench [@wang2024officebench]: big gap at launch, no maintainer |

## What durable benchmarks have in common

Twenty design principles came out of the synthesis (`phase2/design_principles.md`). The five with the most support:

1. **Renew task families, not just items**, on a cadence, under a named owner. ARC's benchmark lifetimes fell from about five years to about one year to about five months.
2. **Treat any public generator as future training data.** Keep scored seeds and rule sets secret and rotating.
3. **Freeze and version one harness**, and publish the gap to a bring-your-own-harness track.
4. **Seal execution**: no network during the run, grader outside the agent's reach, and release gates where a reference solution passes and a do-nothing agent fails.
5. **Baseline humans properly**: a defined population, matched interface and effort, and a sample sized by power analysis.

Where the field still has signal (Panels A, B, E):

- **Human-over-AI gaps** are now scarce and concentrated in perception, intuitive physics, exploration, real-time play and learning across episodes. Most text-only reasoning gaps have closed: ARC-AGI-1 and -2, SimpleBench and OSWorld are all at or above their human baselines.
- **Model-versus-model spread** is widest on long horizons, calibrated abstention, conduct, and outcomes that are uncapped (money earned) or measured on someone else (a student's learning). StudentBench is instructive: its expert reviews separated tutors and showed a cheap Sonnet configuration beating a pricier Gemini one, but measured learning did not separate them (0 of 364 cells significant) [@northcutt2026studentbench].

# A red-teamed search, and what the pilots killed

## Process

- Four ideation panels produced 52 ideas, merged into 47 neutral candidate specifications.
- Five independent red teams (trainability, separation, baselines and scoring, prior art and interest, holistic) scored every candidate without seeing the ideators' reasoning: 235 verdicts in total, 53 keep, 142 revise and 40 kill.
- A revision panel cut 16 candidates, merged 6 and redesigned 7 finalists.
- Two fresh reviewers then attacked the revised designs: one tried to game them, one judged measurement value.
- We built blinded pilots of five finalists. Each answer key was encrypted with a passphrase never written to the repository. Claude Haiku, Sonnet, Opus and Fable attempted each pilot as agents, and keys were decrypted only after solving.

## Pilot results

| Finalist | Archetype | Pilot | Result |
|---|---|---|---|
| Hidden-Rule Lab | A1 claim | 8 visual rule-induction problems, image only, no code | Sonnet and Opus 64/64, with every hidden rule stated exactly; Haiku 31/64 (chance) |
| Patch Auditor | A2 | 20 patches, 6 spec violations, tools on | Fable, Opus and Sonnet 1.000; Haiku 0.444; a fuzzing script also 1.000 |
| Self-Knowledge Exam | A2 | 60 items with self-forecasts | Sonnet, Opus and Fable 60/60, so calibration only rewarded confidence near 1; deliberate failure raised scores |
| Season Forge | A2, complex game | Write a bot for a new fog-of-war game; rated against a sealed 4-bot ladder | Haiku 0.41 rungs; Sonnet 0.81 and Fable 0.79 (interrupted snapshots); Opus 5.08, beating the strongest sealed bot 87% of the time |
| Unrun Lab | A2 | Forecast interventions in 5 secret simulators | Only Haiku finished: skill 9.6, below a naive extrapolator's 16.0 |

Three lessons follow:

- **Clean, static reasoning tasks saturate at the mid tier.** The provisional favourite, Hidden-Rule Lab, assumed a human advantage that no longer exists for rendered scenes.
- **"Tools on" turns many audits into script problems.** Whenever the benign class is "behaviour unchanged", differential fuzzing separates the classes without understanding.
- **Steep, novel, adversarial environments separate models widely.** Season Forge did so at modest scoring cost: 1,600 games ran in 163 seconds on four cores.

The final ranked shortlist from this search was:

1. Season Forge (A2, game).
2. Stump Arena (A1): crowd-authored items people solve and models fail, with a "cost to stump model X" headline.
3. Unrun Lab (A2).
4. Compaction Chronicle (A2): memory half-life over two-million-token streams, conditional.

Details are in `research/reports/Novel AI benchmark and game ideas.md`.

# DEBRIEF: grade the ripple, not the stone

A parallel design track looked for a non-game benchmark. It produced five proposals, all of which were then checked against the evidence above:

- **PREMORTEM:** predict your own failures.
- **STRAIT:** straight-through rule application.
- **WEDGE:** produce an input where two rulebooks differ.
- **SECOND READER:** find planted errors.
- **DEBRIEF:** coach a junior model with one note.

The pilots above weigh against PREMORTEM (the Self-Knowledge Exam failure), WEDGE and SECOND READER (Patch Auditor's saturation under tools), and STRAIT (static rule application saturates). DEBRIEF was chosen because it scores an outcome that is not the model's own answer.

## Task

1. A fixed, cheaper **junior** model attempts practice cases under a rulebook it has never seen, and gets some wrong.
2. The **model under test** reads the rulebook, the junior's worked attempts and the answer key, and writes **one note of at most 150 words**.
3. The junior, given the note, answers **fresh cases the model never saw**.

The headline is the **Net Fix Rate (NFR)**: the share of the junior's control errors on fresh cases that the note removes, net of correct answers it breaks:

$$\mathrm{NFR} = 100 \times \frac{\sum_{ij} (p_{ij} - c_{ij})}{\sum_{ij} (1 - c_{ij})}$$

Here $c_{ij}$ is the junior's control correctness on case $j$ of item $i$, averaged over replicates, and $p_{ij}$ is its correctness with the note. Two baselines price the cheap paths:

- a fixed **placebo** note ("re-read every rule");
- a programmatic **template coach** that restates, verbatim, the provisions a mutation search blames for the junior's errors.

Confidence intervals come from a cluster bootstrap over items.

Why it resists the failure modes above:

- **Items are generated by code from a private grammar.** Every answer comes from an exact interpreter, and no LLM writes test content.
- **Code cannot compute the score**, because scored cases are hidden from the model under test and the key to the practice cases is supplied.
- **Generic advice is priced** by the placebo arm.
- **Over-general fixes are penalised**, because broken correct answers are subtracted.

The closest prior work grades teaching by dialogue or by a teacher's explanation of single instances [@saha2023teach; @educationq2025; @teach2eval2025]. DEBRIEF differs in using one note, a programmatic world, fresh-case transfer and net-of-harm scoring.

## Generator

Version 0.1 generates courier tariffs at three levels. The traps are:

- weights rounded up;
- volumetric weight for parcels only;
- a weekend surcharge on the base price only;
- remote-area fees by postcode prefix;
- a GOLD discount with a zone exclusion;
- a document price cap.

Each trap doubles as a misconception in a mutation library. A mutation search labels each junior error as *diagnosable* (some set of misconceptions reproduces it) or a *slip*. Distractor sections pad the specification. An offline simulation with programmatic juniors checked the instrument: empty notes score about 0%, placebo about 3%, an over-general fix about 25%, and a strong coach 75 to 80%. Confidence intervals shrink from ±13 to ±5 points as items go from 24 to 200.

# DEBRIEF live pilots

PILOT_RESULTS_PLACEHOLDER

# Limitations

- **One lab's models.** All pilot solvers, coaches and juniors were Claude models, run as Claude Code agents with honour-system tool policies rather than a frozen harness.
- **Tiny samples:** 8 to 60 items per pilot.
- **No human participants.** DEBRIEF's human-coach and human-learner validation arms remain to be run.
- **Interrupted runs.** Usage limits cut several runs short, so the Season Forge snapshots for Sonnet, Fable and Opus and three Unrun Lab solvers are incomplete.
- **Weaker sourcing.** Several primary hosts (arxiv.org, arcprize.org, epoch.ai, openai.com and others) were blocked, so some claims rest on search summaries [S].
- **Imperfect blinding.** One Season Forge passphrase was written to a local tool-results file, so sealed-file access cannot be ruled out for that pilot.

# Conclusion

Looking for "a benchmark AI cannot have trained on" targets the wrong property. Every fixed target is trained on within months once it matters. What survives is renewal built into the mechanism: a new game every season, new human authors every month, new rule systems every window. Scores should be anchored to things that can be raised, and should be measured on outcomes other than the model's own answer. Equally important is willingness to fail one's own gates: three of five pilots in the search, and DEBRIEF's first version, failed theirs, and each failure showed where the real difficulty is.

# References
