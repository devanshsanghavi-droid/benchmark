# P1 (psychometric lens): PREMORTEM — can a model see its own mistakes coming?

Draft, 2026-09-29. Lens: psychometrics first. `[keys]` resolve in `research/refs/*.json`; `[C:offg]` = computed in `notes/gap_offg_construct_evidence.md`; **[new]** = checked this session via web search (abstract-level, M), listed at the end. *(hypothesis)* marks predictions, not results.

## 1. Name and thesis

**Premortem** measures **foresight**: whether a model can tell, *before* attempting a batch of fresh tasks, which ones it will get wrong.

**Thesis.** A model that knows in advance which of its answers will fail is more useful than one a few points more accurate that cannot tell. Routing, abstention, escalation and "should I double-check this?" all run on that self-knowledge, which accuracy benchmarks do not measure and which the evidence suggests is not simply general capability renamed. Premortem measures it at **matched accuracy**, on **freshly generated real-work tasks**, with **one exact score**.

Philosophy: ARC asks "can it learn?", Arena "do people prefer it?", **Premortem "does it know its limits?"**

## 2. Construct definition

**Construct: prospective metacognitive sensitivity ("foresight").** This is the ability of model *M*, under a declared tool regime *R*, to rank fresh tasks by its own probability of answering them exactly right. It does so in a context where it has not attempted them, at a difficulty where *M* succeeds about half the time.

- **Sensitivity, not bias.** Foresight is a rank association between stated probability and outcome, as in type-2 signal detection theory (SDT) [new: Maniscalco & Lau 2012; Fleming & Lau 2014]. Overall over- or under-confidence is reported but kept out of the headline; temperature scaling cannot change a rank score.
- **Prospective and separate-context.** The prediction call never sees the model's solution, and the solving call never mentions confidence. This blocks *strategic errors* (deliberately missing items already flagged).
- **Matched first-order accuracy.** Type-2 measures rise mechanically with type-1 accuracy, so SDT research equates first-order performance before comparing people [new: Rahnev & Fleming 2019]. In LLM data this is how g gets in: Brier score correlates 0.84–0.92 with capability PC1, calibration error −0.02 to 0.41 [C:offg; ren2024safetywashing].

**What it is not:** accuracy (held near 50% by design); knowing what is *generally* hard, such as long tables (removed by the cue-validity knob, §7); verbal hedging style (only ranks are scored).

**Measurement model.** For model *m* and item *i* in family *f*:

- **Correctness** Y_mi ∈ {0,1} (exact); **stated probability** p_mi ∈ [0,100] (separate prediction call).
- **First-order model:** logit Pr(Y_mi = 1) = θ_mf − β_f·d_i − γ_f·h_i + u_i + e_mi, with θ_mf capability on family *f*; d_i the generator's size/depth level; h_i random hazard flags (known failure triggers); u_i item idiosyncrasy shared across models; e_mi the model-specific item effect.
- **Foresight (FS)** is the within-stratum rank association between p and Y. Within a stratum d is fixed, so FS can only come from tracking h ("hazard awareness"), u ("class-level" knowledge) or e ("individuated" self-knowledge).
  A *checklist baseline* (§6) estimates h-tracking; *shared-item blocks* (§14, P4) estimate e, the component a 2026 study found absent in retrospective confidence [new: Moran & Whiting 2026].

**Predicted nomological network (pre-registered, §11):** FS correlates at least moderately with *different-method* metacognition (retrospective type-2 AUROC on other content; accuracy of agents' success claims), only weakly to moderately with the Epoch Capabilities Index (ECI), GPQA and the model's own matched level d\*, and not with the sign of calibration bias.

## 3. Why it is not a game (C1)

There is no opponent, no win or lose, no board, puzzle or environment, and no signalling between agents. Each item is a practical computation of the kind assistants do daily: a time-zone conversion, an invoice total, a program trace, a shipping quote. In two separate calls the model is asked "How likely are you to get this exactly right?" and "Solve it." This is the confidence-rating paradigm of experimental psychology applied to work tasks; wagering or bet framings, used by some prior work, are avoided.

## 4. Worked example: one complete item

**Item `TZ-L2-0413`.** Family TZ (calendar and time-zone arithmetic, real IANA tz rules). Level d = 2 (one duration, one conversion). Hazards on:
- `dst_in_interval`: the United Kingdom leaves summer time during the window;
- `eu_us_mismatch_week`: the United States has not yet left summer time, so London–New York is 4 h, not 5 h.

**Rendered item text** (identical in both calls):

> A server maintenance window starts at 23:15 on Saturday 24 October 2026, Europe/London local time, and lasts 7 hours 50 minutes. At the moment it ends, what is the local date and time in America/New_York? Answer as YYYY-MM-DD HH:MM.

**Call A (prediction), one entry among 20 in a batch.** The header reads:

> You will later be asked to solve each problem below in a separate session, without tools, giving only the final answer in the stated format. For each problem, give the probability (integer 0–100) that your later final answer will be exactly correct. Do not solve them. List the IDs from most to least likely correct, one per line, as `ID: probability`.

**Call B (solving), one entry among 10 in a different, shuffled batch.** The header reads:

> Solve each problem. You may reason first. End with one line per problem: `ID: answer`.

The words "confidence" and "probability" never appear in call B.

**Oracle** (Python `zoneinfo`, tzdata 2025b; a second implementation must agree): 23:15 BST = 22:15 UTC; + 7 h 50 m = 06:05 UTC on 25 Oct. The UK changed clocks at 01:00 UTC that day; the US changes on 1 Nov, so New York is still UTC−4. **Gold: `2026-10-25 02:05`.** Diagnostic lure answers: `03:05` (London wall-clock arithmetic, converted at the new offset) and `01:05` (the usual 5 h gap).

**Scoring illustration.** Suppose the model states p = 85 for this item (a) and later answers `03:05`: a confident failure. In its stratum, items b (p 70) and c (p 40) succeed and d (p 20) fails. Of the four success–failure pairs, (b,d) and (c,d) are ordered correctly and (b,a) and (c,a) wrongly, so FS = (2 − 2)/4 × 100 = **0**, a coin flip.

## 5. Generator design (C4, C5)

Every item comes from a Python generator: a **real-world structure source**, a **parameter sampler** (level d plus independent random hazard flags), a **renderer** with at least 3 human-written templates per family, and an **oracle**. Items are text-only (C2); rendering tables as images is an optional multimodal extension. No LLM authors, paraphrases, edits or filters items.

**v1 public families (all four are used in the pilot):**

| Family | Real-world grounding | Level d scales | Example hazards | Oracle, second oracle |
|---|---|---|---|---|
| TZ: calendars and time zones | IANA tz database (pinned per window), business-day rules | legs, durations, zones | DST inside interval, offset-mismatch weeks, :30/:45 offsets, leap day, date line | `zoneinfo`; `dateutil` |
| LEDGER: invoice and table aggregation | ISO 4217/3166 codes, order-table schemas, stated FX and rounding rules | rows, filter clauses, joins | nulls, duplicate IDs, boundary dates, half-even rounding | `pandas`; SQLite |
| TRACE: program output | Python semantics (grammar-sampled programs) | statements, nesting | aliasing, negative modulo, slice ends, shadowing | CPython `exec` in a sandbox; restricted interpreter |
| RATECARD: policy application | real carrier rate-card structure (zones, weight brackets, dimensional weight, surcharges) | parcels, rules, exceptions | bracket boundaries, dimensional weight > actual weight, round-up rules | rules engine; independent re-implementation |

**Validation.** An item is kept only if the two oracles agree and a render → re-parse round trip reproduces the answer. A per-window human audit of 100 random items targets an error rate of ≤0.5%.

**Freshness.** Every window draws new 128-bit seeds. At least one-third of families are **private and rotate**: new human-designed rule systems and hazard types (e.g. holiday calendars, regulatory rate tables). tzdb and holiday-rule releases add real-world change on their own. The generator code is public; seeds and private families are not.

## 6. Scoring and headline unit (C3, C6)

**Correctness.** Exact string match in the stated format, after whitespace normalisation. Format errors are failures, so the model predicts them too.

**Headline: Foresight Score (FS).** Strata *s* = family × level. In each stratum, C_s and D_s count the (success, failure) pairs in which the success received the higher and the lower p, and n1_s, n0_s count successes and failures:

  **FS_m = 100 × Σ_s (C_s − D_s) / Σ_s (n1_s · n0_s)**

Ties within a batch are broken by the model's own list order; remaining ties score 0. FS is the stratified Somers' D (= 2·AUROC₂ − 1). The 95% CI comes from a stratified item bootstrap (2,000 resamples). AUROC₂ is preferred to the M-ratio, whose LLM profiles were reported unstable across inference formats (L; search extract [new: 2604.08976]).

**Human-legible sentence.** *"Of all pairs of one task the model later got right and one it got wrong, FS is the percentage it ranked correctly in advance minus the percentage it ranked wrongly."* 0 is a coin flip; 100 means never surprised by its own mistakes.

**Null baselines shipped with every release:** constant p (FS = 0 exactly), random p (≈ 0), and a size heuristic, p = −item length (≈ 0 at κ = 0 by construction). The **checklist baseline** is a logistic model predicting success from the visible hazard flags, fitted leave-one-model-out on *other* models' outcomes; its FS on model *m*'s items is the "generic checklist" floor.

**Diagnostics (never the headline):** d\* (matched level; a capability readout); accuracy at d\*; overconfidence gap (mean p − accuracy); ECE; **self-advantage** = FS − FS_checklist ("beats the checklist by X"); oracle ceiling from replicate solves; lure-tier FS.

**Resolution.** About 2,000 headline items per leaderboard run (≈ 1,000 successes, 1,000 failures) give an FS standard error of about 2.4 points (Hanley–McNeil, AUROC 0.6–0.7), so models about 7 points apart are separable at 95% [computed here].

## 7. Difficulty knobs and the expected score curve (C5)

1. **First-order level d (auto-matched).** A calibration phase fits each model's per-family threshold d\* (Pr(correct) ≈ 0.5) with a pooled logistic model. Headline items then run at a **constant** d\*, because running staircases inflate metacognitive estimates [new: Rahnev & Fleming 2019]. Generators scale without bound (more legs, rows, statements, rules), so first-order accuracy never saturates: the benchmark follows the model upward.
2. **Cue validity κ (headroom knob)** sets how far visible size predicts true difficulty, following the cue-utilisation account of metacognitive judgment [new: Koriat 1997].
   - **κ = +1 (Easy tier):** d varies over d\* ± 3, so surface size is informative.
   - **κ = 0 (Headline tier):** d is fixed; only hidden hazards vary.
   - **κ = −1 (Hard tier, "lures"):** long items are made trivial by a structural shortcut (for example, two zones with identical offsets, or a filter that matches no rows), and short items carry hazards. Surface size then *misleads*.
3. **Hazard novelty (the versioning knob).** This is the share of private, never-published hazard types.

**Expected curve** *(hypotheses)*, frontier models: FS 40–70 at κ = +1; 10–35 at κ = 0; −20 to +15 at κ = −1; own oracle ceiling (from replicate solves) 60–85.

Anchors: retrospective, unmatched type-2 AUROC on MMLU averaged 0.65–0.74 by domain across 33 models (FS 30–48) [new: Cacioli 2026c]; explicit difficulty estimates predicted models' own correctness near chance (about 0.55; search extract) [new: Li et al. 2026]. Headroom is large, and the κ = −1 tier should hold it for several versions. **Retirement trigger:** the top three models come within 5 points of their own oracle ceilings.

## 8. Contamination and gaming defences (C10, F4, F7)

Each threat is listed with its defence → published check.
- **Memorised items:** fresh seeds; no answer exists before the run → public-split vs live-window gap.
- **Training on the public generator:** private rotating families and hazards → transfer index FS_public − FS_private; retire a family if > 5.
- **Strategic errors:** separate contexts; call B never mentions confidence → accuracy with vs without confidence elicitation (§14, P5).
- **Size heuristics:** κ = 0 fixes size; lures invert it → size and checklist baselines; self-advantage.
- **Degenerate confidence** (constant, all 90s): FS = 0 by definition → tie rate.
- **Planted, flaggable failures:** only public hazards can be planted → FS_public ≫ FS_private.
- **Run-time lookup or key leak:** the oracle runs after responses return; canary in the frozen split → trajectory and tool-use audit.
- **Prompt and scale sensitivity** [new: 2603.09309]: pinned templates and 0–100 scale → two human-written paraphrases run on anchor models each window.
- **Wrong keys:** dual oracles → audited error rate per window.

## 9. Tool regime (C10)

- **Headline track, "sealed":** no tool definitions and no retrieval, identically in calls A and B; vendor-default reasoning settings, recorded, with tokens reported. Brute-force-by-code is impossible, and web lookup is useless because instances come from unpublished seeds at run time.
- **Tool track** (separate column, never the headline): a code interpreter in both calls. Arithmetic becomes free, so d\* rises until errors come from reading the specification. FS_tool then deliberately measures an agentic system's self-knowledge; d\*_tool − d\*_sealed is reported as "tool uplift".
- **Pilot:** subagents are told not to use tools; transcripts are audited; any response with a tool call is excluded and re-run once.

## 10. Real-world and product relevance (F11)

- **Routing and cascades:** a cheap model escalates to a stronger model or a human only when it predicts failure; cascade value rests on this construct.
- **Agents:** deciding whether to attempt, ask or stop, and not claiming success on failed work.
- **Hallucination and abstention:** reasoning fine-tuning degrades abstention by 24% on average [kirichenko2025abstention]; one frontier model was worse calibrated "despite comparable accuracy" [nel2025kalshibench].
- **Human–AI teaming:** users overestimate LLM accuracy, and model discrimination is poorly conveyed to them [new: Steyvers et al. 2025].

The first-order tasks are themselves assistant work.

**Consumer hook:** "Does your AI know when it's about to be wrong?" A public self-test page lets people measure their own FS on the same items (a test, not a game).

## 11. Incremental-validity argument and test plan (C7)

**Why foresight should carry variance beyond g:**
1. **Design.** Matched accuracy removes the main route by which g enters type-2 scores (first-order resolution: Brier 0.84–0.92 vs calibration error −0.02 to 0.41 with PC1 [C:offg]). Stratification and lures remove difficulty-tracking.
2. **Mechanism.** Self-reports are shaped by post-training (reward for confident answers; reasoning RL [kirichenko2025abstention]), largely independent of capability.
3. **Prior data:** accuracy rank and metacognitive-sensitivity rank were "largely inverted" across 20 frontier models [new: Cacioli 2026b]; one model had the highest d′ but the lowest M-ratio of four [new: Cacioli 2026a]; calibration error is off-g [C:offg].

**Counter-evidence taken seriously:** confidence across 20 frontier models is roughly rank-one shared difficulty, with no individuated self-knowledge [new: Moran & Whiting 2026]; ADeLe found low between-model variability in the metacognitive demand [zhou2025generalscales]; "learning" constructs, including ARC, collapsed into g (ρ 0.95–0.97) [C:offg].

**Prediction:** disattenuated r(FS, ECI) of 0.3–0.7 *(hypothesis)*, with a self-advantage that may be near zero.

**Test (full study, not the pilot):**

- **Sample:** ≥ 60 models (target 100) from ≥ 10 families, spanning ECI about 120–165; family as a random effect with a family-clustered bootstrap. About 57 models give 0.8 power to reject "collapse" (ρ ≥ 0.9) if the true value is 0.75 and reliability ≥ 0.9 [C:offg].
- **Pre-registered analyses:**
  1. *Parallel forms:* two independently seeded forms. Target r(FS_A, FS_B) ≥ 0.8 across models.
  2. *Discriminant:* disattenuated r(FS, ECI) < 0.9. **Falsifier: ≥ 0.9.** GPQA Diamond and ARC-AGI-2 are read in the same sample as yardsticks.
  3. *Residual reliability:* r(resid(FS_A | ECI), resid(FS_B | ECI)) ≥ 0.5. This is detectable with N ≈ 24 [C:offg].
  4. *Multitrait-multimethod (MTMM)* [campbell1959convergent]: FS correlates more with a different-method, same-trait measure (retrospective type-2 AUROC on SimpleQA Verified with verbal confidence) than with the same-method, different-trait measure d\*.
  5. *Incremental criterion validity* [sechrest1963incremental]: ΔR² of FS over [ECI, d\*] for (a) the accuracy of agents' end-of-task success claims on an external agentic suite; (b) cascade gain at a fixed escalation rate on held-out tasks; (c) a human–AI teaming study (12 models × 30 participants; final error rate under a fixed checking budget).
  6. *Individuation:* self-advantage > 0 across models.
- **If (2) fails:** Premortem is reported as a renewable, contamination-proof, decision-relevant foresight measure, and the off-g claim is withdrawn.

## 12. Human baseline plan

60 adults (online panel, numeracy screen) work with pen and paper only, matching the sealed track. A 12-item calibration sets each person's d\*; they then predict 48 items and later solve them, shuffled (two ~60-minute sessions, paid at least a living wage). 10 domain professionals (developers for TRACE, logistics staff for RATECARD) form an expert anchor. Per-person FS is noisy, so we report the median, IQR, top quartile and pooled human FS per tier. Protocol, exclusions and paid cost per item are frozen before launch. Leaderboard framing: "Model X's foresight is at the Y-th percentile of adults."

## 13. Leaderboard and governance (F10, F13, F14)

**Columns.** FS (headline, 95% CI); diagnostics (d\*, overconfidence gap, self-advantage, Hard-tier FS, tool-track FS, tokens and cost per run); human reference lines.

**Cadence.** Quarterly windows. The live score is on private seeds; a frozen public split supports replication. Three open-weight **anchor models** are re-run every window, and a window shift is removed if they move more than 2 FS points.

**Policy.** A named neutral steward with disclosed funding; every frontier model added within 14 days of API availability; the shipped model is scored, with no private variants; outputs published after each window closes; pinned harness; pre-declared retirement triggers (§7, §8).

**Distribution.** `pip install premortem` then `premortem run --model <provider/model> --window 2026Q4`, plus an Inspect task at launch. About 2,800 items per model (≈ 110 prediction and 230 solve calls); cost published per run.

**Name check** (GitHub, 2026-09-29): no benchmark is named Premortem, but about 13 LLM agent-skill repos use the term (e.g. MADEVAL/Pre-Mortem-Skill), a moderate collision. Fallback: *Prolepsis*.

## 14. Pilot plan within C8

**Setup.** Models `haiku`, `sonnet`, `opus` and `fable`, called as subagents told not to use tools; prompts ≤ 7k tokens (smaller batches for long items); all scoring in Python.

| Phase | Purpose | Items per model | Calls per model | Total calls |
|---|---|---|---|---|
| P0 Calibration | Fit d\* per family (2 adaptive rounds) | 48 | 4 solve | 16 |
| P1 Headline κ = 0 | FS at d\* | 240 (60 per family) | 12 predict (20 each) + 24 solve (10 each) | 144 |
| P2 Replicate | Test-retest of outcomes; oracle ceiling | 120 of P1, reshuffled | 12 solve | 48 |
| P3 Knob | κ = +1 and κ = −1 | 40 + 40 | 4 predict + 8 solve | 48 |
| P4 Shared block | Individuation: 4 × 4 cross-prediction matrix | 48 common items at the median d\* | 3 predict + 5 solve | 32 |
| P5 Retrospective | Different-method convergence; strategic-error check | 60 of P1 (answer + confidence in one call) | 6 | 24 |
| **Total** | | | **78** | **312** (+ ≤ 30 re-runs) |

The minimum viable pilot is P0 + P1 + P2 = 208 calls.

**Pre-registered success criteria:**
- **S1.** Accuracy at d\* within [0.35, 0.65] in ≥ 12 of the 16 model × family cells.
- **S2.** The FS 95% CI excludes 0 for ≥ 3 of the 4 models. Expected standard error is about 7 points with 240 items.
- **S3.** Median split-half FS reliability (Spearman–Brown) ≥ 0.6.
- **S4.** FS(κ = +1) > FS(κ = 0) > FS(κ = −1), pooled over models, with a one-sided bootstrap p < 0.05 for the end-points.
- **S5.** Exclusions for tool use or parse failure ≤ 5% of calls.
- **S6.** Generators reach d\* for `fable` without hitting their maximum level.

**Also reported:** self-advantage over the checklist baseline; the shared-block cross-prediction matrix; accuracy with vs without confidence elicitation; FS rank vs d\* rank (descriptive only).

**What the pilot cannot test:** four models from one family say nothing about incremental validity. The pilot establishes feasibility, reliability, knob behaviour and effect sizes for the power analysis.

## 15. Risks

1. **Collapse into g:** falsifiable (§11); the fallback is still a decision-relevant score.
2. **No individuated signal** [new: Moran & Whiting 2026]: FS may be mostly hazard awareness, still product-relevant and reported as such.
3. **Low between-model variance** [zhou2025generalscales]: needs many items; signal-to-noise is published [heineman2025signal].
4. **Crowded 2026 niche** (≥ 8 LLM-metacognition papers, one submitted to a Datasets & Benchmarks track): pre-emption is possible; differentiators in §16.
5. **Reasoning models may solve inside call A**, drifting the construct toward self-verification: tokens reported; the full study adds a capped-budget variant.
6. **Verbal-scale artefacts** (heavy discretisation) [new: 2603.09309]: mitigated by tie-breaking and a pinned scale.
7. **Pilot artefacts:** subagent system prompts; one model family.
8. **Consumer appeal weaker than games:** mitigated by the self-test page and a "beats the checklist" story.

## 16. Closest prior work and how Premortem differs

- **Kadavath et al. 2022** [new]: P(IK)/P(True), models predicting whether they know answers; partly white-box; static QA. *Premortem:* black-box, separate-context, fresh items, matched accuracy, leaderboard.
- **Cacioli 2026a/b/c** [new]: M-ratio on 4 open models; a 524-item battery with KEEP/WITHDRAW/BET probes (20 models); a 33-model MMLU AUROC₂ atlas. *All* retrospective, on static public items, at unmatched accuracy.
- **MIRROR** (Wang 2026) [new]: 8 experiments on 4 metacognitive levels, 16 models. Composite, static, not accuracy-matched.
- **Moran & Whiting 2026** [new]: confidence ≈ shared difficulty; an analysis, adopted here as the self-advantage test.
- **Bhattacharyya et al. 2026** [new]: appraisal-based self-assessment predicts performance (12 LLMs, 38 tasks). Static tasks; no matching or lures.
- **AbstentionBench, KalshiBench, ForecastBench, SimpleQA** [kirichenko2025abstention; nel2025kalshibench; karger2025forecastbench; wei2024simpleqa]: abstention or calibration on world knowledge. Knowledge- and tool-confounded; LLM judge or resolution delay.
- **Reasoning Gym, NPPC** [stojanovski2025reasoninggym; nppc2025]: accuracy generators; here only the substrate.

**The new combination:** prospective, separate-context prediction; per-model accuracy matching at a constant level; fresh real-work items with dual oracles; a cue-validity knob with lures; a checklist-relative individuation score; one pairwise headline with a human baseline on identical items; a governed, versioned leaderboard.

## Appendix A. Rejected candidates

- **Vigilance** (SDT on belief revision: keep a correct prior answer under invalid pushback; switch under a valid correction). *Runner-up;* passes C1–C10. Rejected: the "prior answer" is put in the model's mouth; recognising a valid correction requires solving (g-loaded), while the caving *bias* is an easily prompt-steered propensity [ren2025mask]; crowded sycophancy niche. Possible later module.
- **Sufficiency** (is a generated problem answerable, under-determined or contradictory?). Passes the constraints. Rejected: detecting insufficiency requires modelling the solution (likely g-loaded, like ARC [C:offg]), and generator artefacts (a "missing number" cue) invite surface heuristics.
- **Coherence** (Dutch-book coherence of probabilities over related propositions). **Weak on C10/F4:** degenerate strategies (always 50%, or a mechanical rule) are perfectly coherent. Adding accuracy to fix this re-imports g. Low legibility.
- **Nowcast intervals** (80% intervals for fresh real-world quantities). **Violates C10:** evaluation-time web lookup answers it. Knowledge-confounded; ForecastBench occupies the niche.
- **Teach-back** (a teacher model's student is post-tested exactly). Passes the constraints, but weak for this lens: tutoring is g-loaded (MathTutorBench ρ 0.76; TutorBench 0.66) and student-confounded [C:offg].
- **Novel-system learning** (learn a generated rule system from documentation). Passes the constraints; fails the lens: learning measured as post-learning accuracy collapses into g (ARC 0.95–0.97; CL-bench 0.71) [C:offg].
- **Describe-for-a-listener** (one model describes, another reconstructs). **Violates C1:** a referential or signalling game.

## New references (checked 2026-09-29 via web search; abstract-level, M)

- Maniscalco & Lau 2012, *Consciousness and Cognition* 21(1):422–430.
- Fleming & Lau 2014, *Frontiers in Human Neuroscience* 8:443.
- Rahnev & Fleming 2019, *Neuroscience of Consciousness* niz009.
- Koriat 1997, *Journal of Experimental Psychology: General* 126(4):349–370.
- Kadavath et al. 2022, arXiv:2207.05221.
- Steyvers et al. 2025, *Nature Machine Intelligence* (arXiv:2401.13835).
- Cacioli 2026a/b/c, arXiv:2603.25112, 2604.15702, 2605.06673. Wang 2026 (MIRROR), arXiv:2604.19809. Moran & Whiting 2026, arXiv:2605.24299. Bhattacharyya et al. 2026, arXiv:2605.07806. Li et al. 2026, arXiv:2512.18880.
- arXiv:2603.09309 (confidence scale design); arXiv:2604.08976 (quantisation and metacognition; attribution of the M-ratio finding is L).
