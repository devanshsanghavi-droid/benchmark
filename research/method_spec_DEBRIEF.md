# P6 (contrarian lens): DEBRIEF. Grade the ripple, not the stone

*Proposal, 2026-09-29.*

**Conventions.** `[key]` resolves in `research/refs/*.json`; `[C:offg]` = `notes/gap_offg_construct_evidence.md`; `[TB]` = `notes/gap_teachback_instrument_validity.md`; † = checked this session, not in `refs/` (Appendix B); *(hypothesis)* = a prediction. All model outputs shown are **illustrative, written by hand**; none is pilot data.

---

## 1. Name and thesis

**DEBRIEF.** GitHub repository searches for "debrief llm benchmark" (0 hits) and "debrief" in LLM repository names (1 unrelated tool) found no collision. A full check is due before launch (F12).

**Thesis.** Every benchmark grades the model's own answer. DEBRIEF never does. It grades what changes in *someone else* because of the model.

**The task.**
1. A fixed, cheaper "junior" model attempts practice cases under a rulebook it has never seen, and gets some wrong.
2. The model under test reads the rulebook, the junior's worked attempts and the answer key.
3. It writes **one debrief note of at most 150 words**.
4. The junior, given the note, answers **fresh cases the model never saw**.

**Headline: the DEBRIEF score, a Net Fix Rate (NFR) in %.** It is the share of the junior's errors on never-seen cases that the note removes, net of the correct answers the note breaks. In one line: *"Model X's debrief fixes 38% of a junior model's mistakes on cases it never saw."*

**Philosophy.** ARC asks "can it learn?" [chollet2019measure]; Arena asks "do people prefer it?"; DEBRIEF asks **"can it make someone else better?"** Understanding shows in the errors it removes in another mind. Orchestrators, reviewers, mentors and tutors are judged this way in practice.

## 2. Construct definition

**Construct: diagnostic coaching (corrective transfer).** Given a written rule system, a fixed learner's worked attempts at practice cases, and their correct answers, write a short note that moves the learner's behaviour on *unseen* cases of the same system toward correctness.

**Components** (tagged per item; diagnostics only):
1. **Attribution:** find which rule the learner misread, from its working.
2. **Generalisation:** fix the rule, not the instance.
3. **Prioritisation:** choose what to address within the budget.
4. **Non-interference:** do not break correct behaviour, e.g. by over-generalising a fix past its exception.
5. **Reader fit:** write for the learner's actual capacity.

**What it is not:**
- solving: the key is supplied, and scored cases are hidden;
- rewriting the manual: the budget is far below the spec length;
- generic prompting tips: priced by a placebo arm (§6);
- dialogue tutoring: it is one-shot;
- knowledge: the system is novel.

**Predicted nomological network** *(hypotheses, pre-registered)*:

| Measure | Predicted relation | Role |
|---|---|---|
| Human-learner gain from the same notes (§10) | r > 0.7 across engineered arms | external criterion |
| Teaching-gain measures (EducationQ, Teach2Eval) [educationq2025; teach2eval2025] | moderate–high | convergent, different method |
| The model's own solo accuracy on the fresh cases | moderate | key partial-out |
| ECI / capability PC1 | disattenuated 0.6–0.85; **falsifier ≥ 0.9** | discriminant |
| Knowledge QA (SimpleQA) | low | discriminant |

## 3. Why it is not a game (C1)

There is no opponent, no win or lose, and no moves, board, turns or environment. The score is an absolute effect, and nobody competes.

It is not a referential or signalling game either:
- **The junior is a frozen instrument.** It gets no payoff, learns nothing across items and never replies.
- **No convention can form.** There is one note, one reading and no feedback to either party.
- **The content is fixed by the world.** What is conveyed is an external rule system graded against programmatic ground truth, not a referent chosen from a shared set.
- **A human can replace the junior** without changing the task (§10).

Structurally, DEBRIEF is an A/B usability test of corrective documentation with a standardised reader.

## 4. Worked example: one complete item

**Setup:** parcel-tariff family, level L2, budget B = 150 words.

**Spec (excerpt).** The rendered document runs to about 1,000 words, including definitions, a claims section and a delivery-times table that are irrelevant to price.

> NORTHVALE COURIERS: DOMESTIC TARIFF, EDITION 7.
> §2 Chargeable weight. For a PARCEL, chargeable weight is the greater of (a) actual weight and (b) volumetric weight = length × width × height (cm) ÷ 5,000. Both are rounded up to the next whole kilogram before comparing. A DOCUMENT is always charged on its actual weight, rounded up.
> §3 Base price. Zone A: 400 cents for the first kg, then 150 per further kg. Zone B: 600 then 200. Zone C: 900 then 250.
> §4 Surcharges. Collection on Saturday or Sunday: +20% of the base price. Postcodes beginning KX or ZL: a flat +350, added after any percentage surcharge. Percentages are rounded down to a whole cent.
> §5 Discounts. GOLD accounts: 10% off the total after surcharges. Not available on Zone C consignments.
> §6 Cap. A DOCUMENT never costs more than 1,500.

**Practice log shown to the model** (3 of 8 cases; the junior's working is illustrative):

| # | Case | Junior's working and answer | Key |
|---|---|---|---|
| P1 | Zone B, 2.3 kg, 40×30×20, PARCEL, Tue, MN4, STANDARD | "2.3→3 kg. 600+2×200 = **1000**" ✗ | 1400 |
| P2 | Zone A, 0.4 kg, 30×20×5, DOCUMENT, Sat, KX9, GOLD | "1 kg → 400; +80 = 480; +350 = 830; −83 = **747**" ✓ | 747 |
| P3 | Zone C, 6 kg, 50×40×30, PARCEL, Sun, ZL2, GOLD | "6 kg → 2150; +430; +350 = 2930; GOLD −293 = **2637**" ✗ | 4730 |

The generator's mutation search (§5) labels both errors exactly:
- **P1:** "no volumetric weight".
- **P3:** "no volumetric weight" plus "no Zone C exclusion".

**Hidden fresh set** (3 of 12 cases):
- **F1:** Zone B, 1.2 kg, 60×40×40, PARCEL, Mon, AB1, STANDARD → **4400**. The misconception gives 800.
- **F2:** Zone C, 3.1 kg, 10×10×10, PARCEL, Wed, CD3, GOLD → **1650**. The misconception gives 1485.
- **F3:** Zone A, 2.5 kg, 80×60×40, DOCUMENT, Sun, KX1, STANDARD → **1190**. This is an *exception guard*: the note "always use volumetric weight" breaks it to 1500.

**A good debrief** (illustrative, 72 words):

> Two fixes. (1) Weight: for PARCELS charge the larger of actual kg and L×W×H/5000, each rounded UP to a whole kg. In P1 the box's volumetric weight was 5 kg, not 3. DOCUMENTS are the exception: always actual weight. (2) The GOLD 10% discount never applies in Zone C (P3). Everything else you did right: weekend 20% is on the base only, remote 350 comes after it, and the discount comes last.

**Placebo note** (fixed, written once by the authors, same wrapper):

> Work through every rule in order. Re-read each surcharge, discount and exception before answering, and recompute your arithmetic.

**Scoring this item** (illustrative numbers):
- The junior's control accuracy is 5/12 (mean of 2 replicates), which leaves 7 errors.
- The good note gives 10/12: 5 errors fixed, none broken. Item NFR = 5/7 = 71%.
- The over-general note fixes 3 errors and breaks 2 document cases. Item NFR = 1/7 = 14%.

## 5. Generator design (C4, C5)

**Programmatic generation.** Every item is generated by code; no LLM writes test content. Families are grounded in real operational rule documents:
- parcel tariffs (dimensional weight is standard courier practice);
- transit fare capping;
- leave accrual;
- tiered utility tariffs;
- library loans;
- grading schemes;
- parking.

**Four parts per family:**
1. **Input schema:** realistic value ranges.
2. **Rule-template library:** base computations, conditional surcharges and discounts, exceptions, precedence, caps, rounding conventions and definitional overrides. Humans code rule *types* and parameter ranges from public documents; no source text is copied.
3. **Renderer:** writes the policy document from a *human-written phrase bank*, adding distractor sections.
4. **Interpreter:** computes every answer and its rule trace.

**Traps.** Each system carries k counter-default provisions drawn from a catalogue of known misapplication patterns:
- exceptions;
- order of operations;
- exclusion scope;
- rounding direction;
- threshold inclusivity;
- caps;
- definitional overrides.

**Mutation library.** The trap catalogue doubles as a mutation library in the tradition of procedural-bug diagnosis (Brown & Burton's BUGGY, [unverified]). Each single or double mutation of the system is a candidate misconception.

**Case sampling:**
- Practice (8 cases) covers every trap.
- Fresh (12 cases) covers every trap at least twice in new combinations, plus at least 3 trap-free cases and at least 2 exception guards.
- The input space is at least 10⁶ combinations.

**The practice log.** The pinned junior answers the practice cases once per window. The log is cached and ships with the item, so every model coaches the same errors.
- *Tension with C4:* the log is LLM output inside the item.
- *Our position:* questions, keys and error labels are all programmatic. Each error is labelled *diagnosable* when a mutation reproduces it, or *slip* otherwise. The log is a recorded specimen of the instrument's behaviour, not authored test content.
- *Fallback:* logs from human workers.

**Item quality (F8):**
- a second, independently written interpreter, differential-tested against the first;
- a one-off human audit of the phrase bank;
- an ambiguity lint that flags cases where a *plausible-reading* mutation changes the answer;
- an audited-sample error-rate target of 2% or less per release.

**Freshness.** New systems come from private seeds each window. Private families rotate, and the public generator covers practice families only.

## 6. Scoring and headline unit (C3, C6)

For item *i*, fresh case *j* and model *t*, the inputs are:
- *c_ij* ∈ [0, 1]: the junior's control correctness with the spec only, over R = 2 replicates;
- *p_ijt*: its correctness with spec plus note.

> **NFR_t = Σ_ij (p_ijt − c_ij) / Σ_ij (1 − c_ij) × 100.**

**Properties:**
- Answers are exact integers or labels, parsed from fixed answer lines and compared with the interpreter. There is no judge.
- Control is shared by every model, so differences between models are purely differences in post-note accuracy. This avoids the difference-score unreliability of EvaLearn-style gains [C:offg].
- NFR can be negative.
- Notes are hard-truncated at B words and wrapped identically in every arm.
- 95% CIs come from a cluster bootstrap over items and replicates.

**Shipped reference arms** (F2 level 3):
- empty note (0 by construction);
- **placebo** (the null baseline);
- **template coach:** a programmatic note restating, verbatim, the rules its mutation search blames. This is a no-LLM diagnosis baseline;
- **oracle procedure:** an unbudgeted, explicit decision procedure, giving the fixable ceiling.

**Diagnostics, not headline:**
- fix and break rates;
- NFR above the template coach;
- per-trap fix rates;
- NFR as a function of budget B.

**Headline setting:** B = 150 words, over the frozen L1–L4 mix, averaged over a worker panel excluding each model's own family (§12).

## 7. Difficulty knob and expected curve (C5)

| Level | Rules | Traps | Composition depth | Spec length |
|---|---|---|---|---|
| L1 | 5 | 2 | 2–3 | ~600 words |
| L2 | 8 | 3 | 3–4 | ~1,000 words |
| L3 | 12 | 5 | 4–5 | ~1,500 words |
| L4 | 16 | 7 | 5–6 | ~2,200 words |
| L5 | 22 | 10 | 6–8 | ~3,000 words |

**Secondary knobs:** budget B ∈ {50, 100, 150, 300} words, and junior tier.

**Headroom is structural.** 100% NFR needs every misconception fixed and nothing broken. Misconceptions multiply with level while the note stays at 150 words, so at L4–L5 the model must triage and compress interacting fixes.

**Expected curves** *(hypothesis)*:
- NFR falls roughly logistically with level: about 40–60% at L1 and 10–25% at L4 for frontier models.
- NFR(B) is concave and saturating, a rate–distortion curve.
- The placebo stays at 0–5% and the template coach at 10–25%.

New levels extend the scale. Anchor items and anchor notes link versions [habba2026growingpains].

## 8. Contamination and gaming defences

- **Memorisation.** Systems are fresh per window from private seeds; families rotate.
- **Telling.** The model never sees fresh cases or their seeds, so it cannot state their answers. This answers "telling beats teaching" [bastani2025guardrails; TB].
- **Lookup tables.** 10⁶ inputs cannot fit in 150 words.
- **Generic nudging.** Priced by the placebo arm. If the best models only match it, we report the construct as failed.
- **Sycophantic flips.** The junior is isolated, closed-book, and scored only on fresh cases [TB §1c]. Breaks are subtracted.
- **Worker-specific overfitting.** Defences:
  - a private, rotated worker panel;
  - a reported "unseen-worker NFR";
  - a leave-own-family-out headline, because single-student tutoring benchmarks crowned same-family teachers twice [educationq2025; teachbench2026].
- **Note injection.** Only answer lines are parsed. Injected instructions cannot produce correct integers.
- **Curriculum training** [stojanovski2025reasoninggym; primeintellect2026longcontext]. Training on public families trains real coaching. The gap between public and private families is published as a contamination index.
- **Instrument drift.** Fixed anchor notes are re-run each window. A shift beyond tolerance triggers a version bump.

## 9. Tool regime (C10)

- **Canonical track:** one text call, with no tools and no browsing. Reasoning tokens are reported.
- **The junior:** never has tools.
- **Why tools barely help.** Scored cases are hidden and the practice key is supplied, so code cannot compute the score. Re-implementing the mutation search reaches roughly the template-coach baseline. The web holds nothing about a novel system.
- **Tools track:** Python is allowed and reported separately, as a deliberate measure of computation-assisted diagnosis.
- **Pilot:** any call whose transcript shows tool use is excluded.

## 10. Real-world relevance and human baselines

**Relevance (F11).**
- **Who does this task today:**
  - an orchestrator rewriting a failing subagent's instructions;
  - a reviewer fixing a colleague's misreading of an API;
  - a trainer writing a "known mistakes" memo after QA;
  - a tutor whose feedback must carry over.
- **The buying decision:** which model sits in the orchestrator or reviewer seat above a cheap worker. One note improves every later case, so we report *fixes per dollar*.
- **Supporting evidence:** in the Eedi/LearnLM RCT, transfer, not immediate correction, separated tutors [learnlm2025eedirct].

**Human baselines (F5).**
1. **Human coaches.** About 30 experienced tutors, engineers and operations trainers each write about 10 debriefs, with a 15-minute limit and the same budget, scored on the same junior. This yields median and top-quartile human NFR: *"Model X coaches like a top-quartile human mentor."*
2. **Human juniors (instrument check).** About 8–10 arms of widely varying quality × about 150 learners each:
   - no note;
   - placebo;
   - template coach;
   - misleading note;
   - weak model;
   - strong model;
   - human coach;
   - oracle procedure.

   Pre-registered prediction: arm-level NFR on humans correlates above 0.7 with NFR on the LLM junior. This is a falsification design, because human learning gains barely separate frontier tutors: 0 of 364 cells were significant in StudentBench [northcutt2026studentbench; TB §4c].
3. **Human solve baseline** per level. All definitions are frozen before launch.

## 11. Incremental-validity argument and test (C7)

**Why DEBRIEF might carry variance beyond g** *(hypotheses)*:
1. **Solving is decoupled.** The key is supplied, which removes the most g-loaded component. Solo accuracy is also measured and partialled out.
2. **It requires modelling another agent's errors.** LLM tutors were near chance at labelling incorrect student actions [weitekamp2025tutorgym]. Higher general capability "does not necessarily yield more faithful user simulation" [zhou2026sim2real].
3. **Penalising breaks brings in propensities.** Over-generalisation is a propensity, and off-g variance has turned up in propensities; sycophancy correlates ρ ≈ −0.67 with capability [C:offg; ren2024safetywashing].
4. **It is a new method column for multitrait–multimethod analysis.** Format drives benchmark similarity [desai2026whatbenchmarks]. This is not construct evidence by itself.

**Counter-evidence:**
- Teaching tracks solving on ranks: MathTutorBench ρ = 0.76, and TutorBench 0.66 with the ECI-refit.
- ARC, built to measure learning, correlates 0.95–0.97 with the ECI-refit [C:offg].

**We expect substantial g-loading.**

**Test plan:**
- **Sample:** at least 60 models (target 100) from at least 10 families.
- **Falsifier:** a disattenuated leave-one-out ECI correlation of 0.9 or more.
- **Residual reliability:** split-half residual reliability of at least 0.5 is required [C:offg §10].
- **Yardsticks:** GPQA and ARC-AGI-2 are re-scored on the same models.
- **Hierarchical regression:** ΔR² of DEBRIEF over ECI + log-compute + solo accuracy, on held-out and newer models, for two criteria:
  - (i) human-learner NFR (§10);
  - (ii) a field task: orchestrator instruction-repair on held-out real subagent failures, scored by later subagent success.
- **Within-model manipulation (usable with few models):** an *informed* note (log shown) against a *blind* note (no log). The gap isolates use of diagnostic evidence.

## 12. Leaderboard and governance (F10, F14)

- **Runner and policy.** A named steward (an academic lab) and a neutral runner work under a written policy:
  - frontier models are added within 14 days;
  - the shipped model is the scored model;
  - funding is disclosed.
- **Windows.** Quarterly: 600 fresh systems × 12 cases, about 7,200 scored cases per worker, plus a frozen public anchor split.
  - *Power (hypothesis):* with about 50% control errors and a design effect of 2–3, SE is about 1.2–1.7 pp per model. It is pre-registered after the pilot's intraclass-correlation (ICC) estimate.
- **Worker panel.** At least 3 pinned open-weight juniors from different families, fixed decoding, K = 2. The panel changes only at major versions, linked by anchor notes.
- **Openness.** Notes and junior outputs are released under CC-BY after each window. Each run's cost is declared.
- **Retirement.** An NFR of 80% or more at the canonical mix promotes L5. A worker's deprecation bumps the version.
- **Install (C9).** `pip install debrief-bench`, then `debrief run --model <id> --window 2026Q4`. It works over black-box APIs; the junior needs one extra OpenAI-compatible key, or self-hosting. Inspect and lm-eval tasks ship at launch.
- **Consumer layer.** Before/after cards show the junior's wrong answers turning right beside the note. A try-it page lets visitors write their own debrief, which also collects human-coach data.

## 13. Pilot plan (C8)

**Roles.**
- **Junior:** `haiku`, in a fixed auxiliary role.
- **Models under test:** `haiku`, `sonnet`, `opus` and `fable`. The haiku→haiku self-debrief cell is reported separately.

**Items.** 24 systems from 3 families (parcel, fares, leave), 8 per level L1–L3. Each has 8 practice and 12 fresh cases.

**Constraints.**
- Prompts stay under 8k tokens: spec up to about 2.5k, log about 1k, cases about 0.8k.
- All scoring is done in Python.
- Every subagent is told to use no tools. Transcripts are audited, and flagged calls are re-run from the buffer.

| Arm | Calls |
|---|---|
| Junior practice attempt (builds the log) | 24 |
| Junior control on fresh set, 2 replicates | 48 |
| Informed debriefs (4 models × 24) | 96 |
| Junior post-test per debrief | 96 |
| Junior with placebo note / template-coach note | 24 + 24 |
| Junior with oracle procedure (8 L3 systems) | 8 |
| Blind debriefs (4 models × 6 systems) + junior post-tests | 24 + 24 |
| Model solo answers on fresh set (4 models × 6 systems) | 24 |
| **Total** (144 in the model-under-test role, 248 junior; 8 buffer) | **392** |

**Pre-registered go/no-go checks:**
- **G1:** junior control accuracy is 30–70% at each level.
- **G2:** at least 40% of practice errors are diagnosable by the mutation search.
- **G3:** template coach beats placebo (the 90% item-bootstrap CI excludes 0).
- **G4:** placebo is within ±5 pp of 0; otherwise the junior is note-sycophantic, and we report it.
- **G5:** the best NFR at L3 is at most 60% and below the oracle procedure.
- **G6:** the spread across models is at least 10 pp, or we report it as unresolved (per-model SE is about 4–5 pp).
- **G7:** parse rate is at least 95%, with 0 tool-using calls included.
- **G8:** informed notes beat blind notes, pooled over models.

**Also estimated:**
- the ICC, for power;
- per-trap fix and break rates;
- a mixed logistic model, *p_ijt* ~ model + *c_ij* + trap + solo-correct + (1 | system).

**Limits.** There is one junior, every model is a Claude model, and 4 models cannot support a correlation with g.

## 14. Risks

1. **Instrument dependence.** The student accounts for 35% of gain variance in EducationQ's 3×3 [TB §0]. Mitigated by the panel, pinning, leave-family-out and anchor notes; not removed.
2. **Unsystematic slips** compress NFR and blur ranks (checks G2, G6).
3. **Partial collapse into g** is likely. It is falsifiable. Even then, DEBRIEF remains fresh, exact and renewable, in a product unit.
4. **Generic nudges dominate** (priced by the placebo arm).
5. **C4 objection to LLM-written logs** (fallback: human logs).
6. **Spec ambiguity** makes a valid reading look like a misconception (addressed by the audit, the ambiguity lint and a published error rate).
7. **Less spectacle than games** (addressed by the before/after cards and the try-it page).
8. **Overlap with P2 STRAIT.** The rulebook generators could be shared. STRAIT scores the model's own adjudication; DEBRIEF never does.

## 15. Closest prior work and how DEBRIEF differs

- **Saha et al. 2023** [saha2023teach]. Teacher explanations raise student accuracy; its RQ4 tests "future unexplained data". *Differences:* public tasks, small students, per-instance explanations, no budgeted failure-log diagnosis, no leaderboard.
- **EducationQ, Teach2Eval, TeachBench** [educationq2025; teach2eval2025; teachbench2026]. *Differences:* public or contaminated items, pre/post on the same items, dialogue, single-family students.
- **MathTutorBench** [macina2025mathtutorbench]. A reward model scores pedagogy; there is no learner outcome.
- **Olausson et al. 2024†.** Self-repair is "bottlenecked by the model's ability to provide feedback". *Differences:* feedback targets the same program, so it can tell the fix; public HumanEval/APPS items.
- **MINT** [wang2024mint]. It evaluates *using* feedback, which GPT-4 provides by default. Whether it ranks feedback providers was not verified.
- **OPRO† and TextGrad†.** LLM critiques of failures improve downstream accuracy. They use the same mechanism, but as optimisers on public tasks, not as a measurement.
- **CL-bench, KOR-Bench, MTOB** [dou2026clbench; ma2024korbench; tanzer2023mtob]. Novel material, but graded on the model's own answers.

---

## Appendix A. Rejected candidates

1. **HANDOFF (cold-start brief).** The model condenses a verbose novel spec into a brief of at most B words; a junior without the spec answers fresh cases.
   - *Status:* compliant, and the strongest runner-up. Kept as a possible variant.
   - *Rejected because:* it is mostly "understand and restate". Learning-from-context scored as performance correlates 0.71 (CL-bench) and 0.95 (ARC) with the ECI-refit [C:offg]. It is also the synthesis's niche #2, so not contrarian.
2. **Hidden-law discovery lab.** *Rejected:* ARC-like and g-loaded; with tools it is brute-forceable by symbolic regression (C10).
3. **Active experimentation on a hidden system.** *Rejected:* Mastermind's structure (C1), brute-forceable [golde2025mastermindeval], and call-hungry (C8).
4. **Machine teaching to a deterministic learner.** Exact and free of LLMs. *Rejected:* it reduces to an enumerable combinatorial puzzle (C10, with C1 risk) and has weak relevance.
5. **Generation–verification-gap board.** *Rejected:* the headline is a difference of two scores (C6) and unreliable [C:offg].
6. **Consistency without ground truth.** *Rejected:* violates C3; constant answers are perfectly consistent.
7. **Examples-to-mastery curves.** *Rejected:* compliant, but it is the synthesis's niche #1, g-loaded and crowded [yan2025mirbench; agarwal2024manyshot].
8. **Reconstruct a hidden artifact from a description.** *Rejected:* a referential game (C1).
9. **Calibration overlay.** *Rejected:* taken by sibling proposal P1.

## Appendix B. Sources checked this session, not in `refs/`

- † Olausson, Inala, Wang, Gao, Solar-Lezama, "Is Self-Repair a Silver Bullet for Code Generation?", ICLR 2024, arXiv:2306.09896. The abstract was seen in two GitHub-hosted listings (MrUnreal/agent-rules; longyang998/fix-lazy-llms). Confidence M.
- † Yuksekgonul et al., "Optimizing generative AI by backpropagating language model feedback", *Nature* 639:609–616 (2025), arXiv:2406.07496 (TextGrad). Source: the official README, zou-group/textgrad. Confidence H.
- † "Large Language Models as Optimizers" (OPRO). Source: the official repository, google-deepmind/opro. Title only; confidence H for existence.
- [unverified] Brown & Burton, "Diagnostic models for procedural bugs in basic mathematical skills" (BUGGY), *Cognitive Science*, 1978. This comes from background knowledge and must be checked before citing.
