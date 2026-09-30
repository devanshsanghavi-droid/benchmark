# Phase 4b revision panel: aggregation, cuts, finalists, provisional ranking

As of 30 Sep 2026. Inputs: `../phase3/candidates_spec.md`, `../phase3/ideation_rationale.md`, the five fact-checked red-team files in this folder, `../phase2/design_principles.md` and the Phase 1 dossiers. Corrected values and [uncertain] labels from every fact-check log are used as corrected. R2's probes count as weak evidence: they were self-graded, with answer keys readable on disk.

**Conventions.**
- K/R/X = keep/revise/kill. "R1 §0.2" = section 0.2 of red team R1.
- [speculation] = this panel's untested judgement; [uncertain] = a doubt carried over or newly flagged.
- Finalist IDs F1–F7 are alphabetical and carry no rank; the rank is in §5.
- `revised_finalist_specs.md` holds neutral specs of F1–F7 for round-2 reviewers.

---

## 1. Score aggregation

**Method.**
- **Consensus:** the median over the reviewers who scored that question: Q1 (R1, R5), Q2 (R1's gaming-side score, R2, R5), Q3 (R2, R5), Q4 (R3, R5), Q5 (R3, R5), Q6 (R4, R5). "Mean" is the mean of the six medians.
- **Columns:** the R5 column lists Q1–Q6 as six digits. Pre-emption codes (R4, after its fact-check): S strong (including "strong on one axis"), P partial, P-S / S-P mixed.
- **Split ≥2:** reviewers differ by 2 or more points on that question.
- **Outcome:** **Fx** = finalist parent; →Fx = absorbed into a finalist; CRn = cut rule (§2); reserve = survivor not selected.

|ID|Name|Arch|R1 Q1,Q2g|R2 Q2,Q3|R3 Q4,Q5|R4 Q6,pre|R5 Q1–Q6|Verdicts R1–R5|K/R/X|Consensus Q1–Q6|Mean|Split ≥2|Outcome|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|C01|Kinetic|A1|2,2|2,4|4,4|3,S|224443|RRKRR|1/4/0|2/2/4/4/4/3|3.17|—|reserve|
|C02|Live Rig|A1|4,3|3,3|2,1|3,P|443424|KRXRX|1/2/2|4/3/3/3/1.5/3.5|3.00|Q4|CR2|
|C03|Novel Expert|A1|3,3|3,2|3,4|2,P|332442|RRRXR|0/4/1|3/3/2/3.5/4/2|2.92|—|→F2|
|C04|Earworm|A1|2,2|2,4|3,3|2,P|333433|RRRRR|0/5/0|2.5/2/3.5/3.5/3/2.5|2.83|—|reserve|
|C05|Stump Arena|A1|3,4|4,3|3,3|4,S|343334|RKRKR|2/3/0|3/4/3/3/3/4|3.33|—|**F6**|
|C06|Alien Physics|A1|3,3|3,4|4,4|3,P|333444|RKKRR|2/3/0|3/3/3.5/4/4/3.5|3.50|—|reserve|
|C07|Tacit Signals|A1|3,3|3,2|3,2|2,S|433423|RRRXX|0/3/2|3.5/3/2.5/3.5/2/2.5|2.83|—|CR2|
|C08|Glyph Pact|A1|2,2|2,3|3,3|2,S|223423|XRRXX|0/2/3|2/2/3/3.5/2.5/2.5|2.58|—|CR1|
|C09|First-Run Arcade|A1|3,2|3,5|4,2|4,P-S|334434|RKRRR|1/4/0|3/3/4.5/4/2.5/4|3.50|—|reserve|
|C10|Two Clocks|A1|2,1|1,2|4,1|2,P-S|322442|XXXXX|0/0/5|2.5/1/2/4/2.5/2|2.33|Q5|CR1|
|C11|Wayfinder|A1|2,2|3,4|4,4|2,P|333443|RKKRR|2/3/0|2.5/3/3.5/4/4/2.5|3.25|—|reserve|
|C12|Cartographer & Scout|A1|3,3|3,3|3,3|2,S|333423|RRRXX|0/3/2|3/3/3/3.5/2.5/2.5|2.92|—|CR2|
|C13|Deep Seasons|A1|3,3|3,3|2,3|3,P|332434|RRRRR|0/5/0|3/3/2.5/3/3/3.5|3.00|Q4|reserve|
|C14|Kelly Exam|A2|3,3|3,4|3,5|3,P-S|334444|RKKRR|2/3/0|3/3/4/3.5/4.5/3.5|3.58|—|**F5**|
|C15|Prospective Self-Forecast|A2|2,2|3,2|2,4|3,P-S|333343|RRKRR|1/4/0|2.5/3/2.5/2.5/4/3|2.92|—|→F5|
|C16|Pushback Ledger|A2|2,2|2,4|3,4|4,S|323454|RRKRR|1/4/0|2.5/2/3.5/3.5/4.5/4|3.33|—|reserve|
|C17|Reliability Horizon|A2|3,3|3,5|3,4|3,S|444453|RKKRK|3/2/0|3.5/3/4.5/3.5/4.5/3|3.67|—|reserve|
|C18|Compaction Chronicle|A2|3,3|4,4|2,5|4,P|444244|RKKKK|4/1/0|3.5/4/4/2/4.5/4|3.67|—|**F1**|
|C19|Frozen-Student Tutor|A2|3,3|3,3|3,5|3,S-P|333453|RRKRR|1/4/0|3/3/3/3.5/5/3|3.42|—|reserve|
|C20|Misconception Clinic|A2|3,3|3,2|3,4|2,P|433333|RRKXX|1/2/2|3.5/3/2.5/3/3.5/2.5|3.00|—|CR2|
|C21|Simulated Futures Exchange|A2|3,3|4,5|3,5|2,P|444353|RKKXK|3/1/1|3.5/4/4.5/3/5/2.5|3.75|—|**F7**|
|C22|Long-Tail Futures|A2|4,4|4,3|3,4|3,S|443343|KRKXR|2/2/1|4/4/3/3/4/3|3.50|—|CR3|
|C23|Hunch Lab|A2|2,3|4,2|3,4|4,P|443434|RRKKR|2/3/0|3/4/2.5/3.5/3.5/4|3.42|Q1|→F7|
|C24|MDL Arena|A2|4,4|4,4|2,3|2,S|444353|KKRXK|3/1/1|4/4/4/2.5/4/2.5|3.50|Q5|reserve|
|C25|Mechanism Lab|A2|3,3|3,3|2,4|2,P|433342|RRKXX|1/2/2|3.5/3/3/2.5/4/2|3.00|—|CR2|
|C26|Contractor's Auction|A2|3,3|3,3|2,4|3,S|443344|RRKXR|1/3/1|3.5/3/3/2.5/4/3.5|3.25|—|→F5|
|C27|Signal Pit|A2|2,2|3,4|3,5|3,P|334353|RKKRR|2/3/0|2.5/3/4/3/5/3|3.42|—|reserve|
|C28|Hidden-Dynamics Economy|A2|3,4|4,3|2,3|3,S|443334|KRRXR|1/3/1|3.5/4/3/2.5/3/3.5|3.25|—|CR3|
|C29|Whodunit Engine|A2|2,2|2,3|4,5|3,P|334444|RRKRR|1/4/0|2.5/2/3.5/4/4.5/3.5|3.33|—|reserve|
|C30|Masquerade|A2|3,3|3,3|3,3|3,S|333334|RRRXR|0/4/1|3/3/3/3/3/3.5|3.08|—|CR3|
|C31|Debate Court|A2|2,3|3,2|3,3|3,S|333434|RRRRR|0/5/0|2.5/3/2.5/3.5/3/3.5|3.00|—|reserve|
|C32|Nomic Engine|A2|2,2|2,3|3,4|2,P|323333|RRKXX|1/2/2|2.5/2/3/3/3.5/2.5|2.75|—|CR2|
|C33|Exploitability Gauntlet|A2|3,4|4,4|2,4|2,S|344343|KKKXR|3/1/1|3/4/4/2.5/4/2.5|3.33|—|CR3|
|C34|Setter's Duel|A2|2,2|3,3|3,4|3,P|344343|RRKRR|1/4/0|2.5/3/3.5/3/4/3|3.17|Q2|reserve|
|C35|Game Designer's Duel|A2|2,2|3,2|2,3|2,P|342333|XRRXX|0/2/3|2.5/3/2/2.5/3/2.5|2.58|Q2|CR1|
|C36|Season Forge|A2|4,3|2,4|3,3|3,S|444434|KRRRR|1/4/0|4/3/4/3.5/3/3.5|3.50|Q2|**F4**|
|C37|Saboteur's Patch|A2|3,3|3,4|3,4|4,S|444354|RKKRK|3/2/0|3.5/3/4/3/4.5/4|3.67|—|**F3**|
|C38|Relay|Both|3,3|3,2|4,2|3,P|432433|RRRRR|0/5/0|3.5/3/2/4/2.5/3|3.00|—|reserve|
|C39|Blind Spot Cartographer|Both|2,3|2,3|3,3|3,P|343434|RRRRR|0/5/0|2.5/3/3/3.5/3/3.5|3.08|Q2|→F6|
|C40|Rules Gauntlet|Both|3,3|2,3|3,3|3,P-S|343433|RRRRR|0/5/0|3/3/3/3.5/3/3|3.08|Q2|reserve|
|C41|Practice Week|Both|3,3|3,1|2,3|4,P|442334|RXRRR|0/4/1|3.5/3/1.5/2.5/3/4|2.92|—|reserve|
|C42|Hidden-Rule Lab|Both|3,4|3,3|4,5|3,S|434444|KRKRK|3/2/0|3.5/3/3.5/4/4.5/3.5|3.67|—|**F2**|
|C43|Eleusis Masters|Both|3,3|2,3|3,3|2,S|333343|RRRXX|0/3/2|3/3/3/3/3.5/2.5|3.00|—|CR2; setter→F2|
|C44|Convention Cross-Play|Both|3,3|3,3|3,4|3,S|433443|RRKRR|1/4/0|3.5/3/3/3.5/4/3|3.33|—|reserve|
|C45|Crowd Oracle|Both|2,2|2,2|4,5|4,P|433443|XRKKR|2/2/1|3/2/2.5/4/4.5/3.5|3.25|Q1|reserve|
|C46|Grift|Both|2,2|3,1|2,1|3,P|431324|RXXRX|0/2/3|3/3/1/2.5/1.5/3.5|2.42|Q1|CR1|
|C47|Defuse Line|Both|3,2|2,3|3,2|3,S|323434|RRRXX|0/3/2|3/2/3/3.5/2.5/3.5|2.92|—|CR2|

**Readout.**
- **Verdicts:** 53 keep, 142 revise and 40 kill across 235 verdicts. No candidate is kept by all five. C18 comes closest (4 K, 1 R); C10 is killed by all five.
- **§7 decision rule on consensus medians** (Q1, Q3 and Q5 ≥ 4; mean ≥ 3.5; no score of 1): only C24 passes, because R1 and R5 cap Q1 at 4 and seldom award it. With Q1 relaxed to ≥ 3.5, five pass: C17, C18, C21, C24 and C37.
- **Question-level splits ≥ 2** are rare (12). Three touch finalists:
  - C36 Q2: R2's 2 rests on the human-percentile headline, which F4 drops.
  - C23 Q1: R1's 2 is because labs can pre-run template experiments; F7's Track M carries this as residual risk.
  - C39 Q2: pool decay vs renewal; F6 headlines the current-season pool plus a yield trend.
- **Verdict splits** (one reviewer keeps, another kills): C02, C20, C21, C22, C24, C25, C26, C28, C32, C33, C45. In 9 of the 11 the kill comes from R4 (prior art and interest). [interpretation] Closed, simulable designs score well on R1–R3's measurement lenses but are often pre-empted or illegible on R4's.

---

## 2. Cut rules and cut list

**Rules.**
- **CR1 Panel kill:** 3 or more of the 5 verdicts are kill.
- **CR2 Weak and contested:** exactly 2 kill verdicts and a consensus mean ≤ 3.00. Every 2-kill candidate meets the mean condition.
- **CR3 Pre-empted:** all three hold:
  - R4 rates the pre-emption strong, and its fact-check confirms it;
  - the proposed twist leaves the headline story unchanged;
  - consensus Q6 ≤ 3.
- **Structural check** (not a separate rule): each cut was tested for an unfixable flaw, named below where present: latency-dominated scoring, live humans inside every model's score, or hardware nobody else can rerun.
- **Disqualifying score:** a consensus median ≤ 1.5 (rubric: a 1 disqualifies) hits C02, C10, C41 and C46. C41's has a named fix (≥ 3 games per season; R1, R4, R5), so C41 stays in reserve.
- **Absorbed** candidates are not cut: a finalist carries their useful part.

**Cut (16).**

| ID | Rule | Reason |
|---|---|---|
| C08 | CR1 | The efficiency ratio is a trainable verbosity knob. ICCA and a Jun 2026 paper already publish both headlines. Needs live dyads for every model |
| C10 | CR1 (5/5) | Dual-task cost measures API latency (frozen harness) or agent architecture (BYOH). No fix keeps the construct |
| C35 | CR1 | Evolutionary search can optimise MCTS "depth" (Ludi, Yavalath). Competitors write the test set. n = 3 games |
| C46 | CR1 | Q3 median 1: pool-relative 8-seat live chats. "Judge each trade by my own table" drives the conned rate to about 0. Live humans; ethics |
| C02 | CR2 | Q5 median 1.5: rigs drift, and third parties cannot rerun them. A simulated twin would remove the physical moat |
| C07 | CR2 | The live human partner is the construct: about 120 fresh pairings per model, with an MDE of about 9–11 pp. The paradigm dates from about 2010 |
| C12 | CR2 | Talk the Walk (2018) already set the paradigm. Needs 100 human–model dyads per model. Overlaps C11 |
| C20 | CR2 | Misconceptions planted by fine-tuning may be diffuse or unstable. Learners must be re-fine-tuned every quarter. Q6 2.5 |
| C25 | CR2 | A single red-team optimiser is a known grader, and the owner's oracle sets the denominator. Q6 2 |
| C32 | CR2 | The 10 dry runs execute the probes, and the typed DSL invites an interpreter |
| C43 | CR2 | The solver role duplicates F2. The setter reward is pool-relative and open to collusion; the setter survives only as an optional F2 track |
| C47 | CR2 | GPTNT (Jun 2026) owns the "no model defuses in real time" headline. Live play measures latency. Needs human operators for every model |
| C22 | CR3 | ForecastBench auto-generates the same data-series questions and has a neutral runner. FRI reported that AI has likely reached superforecaster parity (16 Jul 2026) |
| C28 | CR3 | Vending-Bench 2 and FLE own both halves. Offer them the V/V* normalisation |
| C30 | CR3 | Kaggle Werewolf plus MafiaScope's per-utterance belief probes cover the belief-bits twist. Seat variance is high |
| C33 | CR3 | GENSTRAT (May 2026) has generated imperfect-information games, a leaderboard and an equilibrium-approximating opponent. Exact exploitability improves the metric, not the story. Q4 and Q6 2.5. This overrides 3 keeps from lenses that did not assess prior art. Offer the metric to GENSTRAT |

**Absorbed (6).**
- C03 → F2: blended perceptual primitives in the rule grammar.
- C43's setter role → F2, as an optional track.
- C15 → F5: prospective forecasts and triage.
- C26 → F5: the job-selection framing; the auction is dropped.
- C39 → F6: the model-author arm.
- C23 → F7: Track M, ML-training family only.

**Reserve (19; survivors not selected).**

| ID | Why not a finalist | Salvage |
|---|---|---|
| C01 | SpookyBench owns "frames are noise", and the gap sits partly in frame sampling (Q1 and Q2 median 2) | — |
| C04 | Few models take audio input. Tap-along measures streaming latency. Non-musicians risk a floor effect | — |
| C06 | Once trajectories are extracted, inferring the law is regression. The IntPhys 2 evidence dates from Jun 2025 | Its pixel-vs-coordinates ablation moves into F2 |
| C09 | Paused play follows ARC-AGI-3's collapse path. R3's token-clock fix already exists: Real-Time Reasoning Gym measures time in tokens ([ICLR 2026](https://arxiv.org/abs/2511.04898); search summary, [uncertain]). OmniGameArena (Jun 2026) already runs new real-time games. $2–8k per run | Next A1 candidate in line |
| C11 | Dead reckoning replaces the mental map. Crowded spatial niche (MindTopo, 360CityArena). Q6 2.5 | — |
| C13, C41 | Good story (Q6 4), but the notes protocol decides the score, humans cannot be memory-capped, and C41 has one game per season (Q3 1.5) | Merge them if revived |
| C16 | Crowded: lechmazur's board is already two-sided. Discrimination tends to 1 as capability rises | — |
| C17 | Passes the relaxed rule, but "Illusion of Diminishing Returns" and TMBench (r = 0.73 with AIME/MATH/GPQA) pre-empt it. Cost is 10–100× the ideator estimate | An agentic L95 variant (R4) |
| C19 | Small students cap the gains. StudentBench found 0 of 364 learning cells significant. Teach2Eval already exists | — |
| C24 | The only strict-rule pass, but Q4 and Q6 are 2.5, the KoLMogorov-Test holds the concept, and bits are illegible | A secondary metric for F7 |
| C27 | A Bayes calculator solves the family. Toy markets. Q1 2.5 | — |
| C29 | Consistent liars reduce the case to Knights-and-Knaves, and the parser is a hidden grader. Q2 2 | — |
| C31 | Repeats Khan et al.'s protocol. Truth Advantage compresses at the judge's ceiling | — |
| C34 | The frozen ladder ages. Generate-and-filter search wins. Q1 2.5 | — |
| C38 | Chains give tiny n at $1.5–9k per model. Q3 2 | — |
| C40 | The blind track duplicates ARC-AGI-3, and the Open track reduces to simulator plus MCTS | The rulebook track |
| C44 | Kaggle Hanabi, the Convention Gap paper and AH2AC2 crowd it. The human ratio is noisy | — |
| C45 | Payoff is capped at the modal choice, human data can be bought (Centaur), and panels are partly LLM-written | — |

---

## 3. Revised common protocol (cross-cutting attacks)

These fixes apply to all finalists. The per-finalist tables cite them as X1–X10.

| # | Attack (reviewer) | Fix | Residual risk |
|---|---|---|---|
| X1 | "Secret" does not survive API evaluation; ARC calls its set "semi-private" (R1 §0.1) | Fresh instances every evaluation window, not every season. A per-lab burn log ensures each lab sees any fixed item at most once. Open-weight models run locally. Closed models run only under no-retention terms [uncertain whether these are formal contracts; ARC describes working with providers]. Instances are released after each window, so secrecy is temporary by design and renewal is the defence. Leakage check: fine-tune an open model on the previous window's *released private* instances and report its score change on the new window. This replaces the practice-gym check, which measured the wrong channel | Family-level RL on look-alikes (partly on-construct) |
| X2 | Tools-off cannot be verified for closed APIs (R1 §0.2; R5 pattern 1) | Each finalist declares one headline tool policy: either code is the construct (F3, F4, F7), or the headline is a track where code helps little. Release gate: an owner-written script of ≤ 200 lines must score near the floor on the headline track. The other track's delta is published | Server-side tools inside closed APIs |
| X3 | Variant spamming, best-of-k (R1 §0.3) | One pre-registered entry per model per window. All attempts reported; the mean counts, never the max | — |
| X4 | Gain, slope and ratio headlines can be sandbagged or are noisy (R1 §0.4; R2 flaw 5; R3 flaw 10) | No finalist headlines a difference score. Ratios are aggregated before dividing | — |
| X5 | Frozen, identifiable anchors become reward models; closed anchors get deprecated (R1 §0.5; R3 flaw 9) | Anchor identities are hidden, and at least one rung rotates per window. Pinned open weights provide continuity | Anchors can still be fingerprinted |
| X6 | 33–46% of crowd workers used LLMs (R1 §0.6; R3) | Media-only stimuli, copy-paste blocked, explicit deterrents (which cut use from 27.6% to 15.9%), timing checks, and a lab stratum (n ≈ 30) each season to calibrate online panels | Some AI-assisted participants remain |
| X7 | Cost estimates ignore thinking tokens (R3) | The costs below use Opus 5.5 list prices ($4 in / $20 out per MTok), thinking included [speculation] | Prices change |
| X8 | Wall-clock limits measure serving speed (R3 flaw 1) | No wall-clock limits apply to models; budgets are billed tokens and sandbox CPU time | Token prices differ; $ is reported too |
| X9 | Scores may just proxy the general factor (R2 P14 note; R5 pattern 4) | A pre-registered validity report: the residual after a general-capability index and release date, plus one external outcome test | A finalist may prove to be a g-measure |
| X10 | Upkeep kills benchmarks, and one owner can run only 2–3 (R4 flaws 10–11). Human cohorts drift (R3 flaw 2) | A named neutral steward, a one-command runner and disclosed funders. Human arms run each season or year, never inside a model's score | Funding |

---

## 4. Finalists

### F1 Compaction Chronicle
**Built from** C18. **A2 · benchmark.** Support: K4/R1/X0; consensus 3.5/4/4/2/4.5/4.

| Attack (reviewer) | Fix | Residual risk |
|---|---|---|
| Known query types let a fixed entity-ledger schema answer most queries (R1, R2, R5) | Query families are secret and rotate each season. Each season has ≥ 2 held-out query families and ≥ 1 held-out update semantics. Queries never appear during the stream. Scores are reported per family | A generic "salience ledger" may still transfer; a public ledger-bot anchor measures how far |
| The stored facts fit the cap, so the task is bookkeeping (R2) | The generator keeps query-relevant state at ≥ 4× the notes cap at every checkpoint. An oracle-notes bot that knows the query distribution publishes the ceiling at 4, 16 and 64 KB (R3, R5) | The ceiling is only as good as the oracle |
| A frozen protocol penalises vendors with native compaction (R4; ARC-AGI-3 62.7 vs 98.6) | Frozen state-carry headline, plus a provider-native track; the delta is published | Labs will quote the native track |
| The human arm is infeasible (it needs ≈ 830 wpm) and mismatched (R3, R5) | Human reference on a 40-chunk, ≈ 30k-token version that models also run. Full length is model-only | No human comparison at full length, where A2 holds by construction |
| Deterministic seeds get memorised across API runs (R1 §0.1) | Fresh worlds every window (X1); common random numbers only within a window | RL on look-alike simulators (partly on-construct) |
| Likely a proxy for general capability (R2) | X9 validity report. Outcome test: correlation with pass^k on a held-out long-horizon agent suite | May be mostly g, in a product-relevant unit |
| Memory benchmarks are vendor-polluted; Compaction Cliff is the nearest prior work (R4) | Neutral steward (X10). Single headline number: memory half-life. Cite Compaction Cliff as the prior measurement | Adoption |

- **Mechanics.**
  - A secret world simulator emits ≈ 2M tokens in 400 chunks (length knob 200k–4M).
  - After each chunk the model sees that chunk, its own notes (cap 16 KB; sweep 4 and 64 KB) and a fixed prompt, and returns rewritten notes.
  - At 60 random checkpoints, a separate call answers about 5 queries from the notes alone: counts, balances, provenance, who knew what when, conflict resolution, plus held-out families.
  - Update semantics include retroactive corrections, unit changes, aliasing, and sources whose reliability is revealed later.
- **Generation and secrecy.** At least 3 private simulator families per season, with rotating domains, event grammars and update semantics. Fresh instances every window. Streams are released after each window. Open models run locally (X1).
- **Scoring.**
  - Answers are graded exact or within tolerance.
  - Headline: memory half-life, the fact age in chunks at which accuracy falls to half of fresh-fact accuracy (logistic fit; cluster bootstrap by seed).
  - Also reported: area under accuracy vs fact age, share of the oracle ceiling at each cap, and per-family accuracy.
  - 5 paired seeds × ≈ 300 queries, with a pre-registered MDE [speculation: ≈ 5 pp on accuracy, ≈ 20% on half-life].
- **Tools and sandbagging.** No retrieval, files or code; the notes are the only state. No difference score (X4). Queries are unannounced.
- **Humans.** ≥ 60 adults on the 40-chunk version, with a capped editor, 2 hours, paid per correct answer. The distribution is reported.
- **Cost.** $300–1,000 per model per track [speculation; R3 basis].
- **Expected human vs AI [speculation].** Humans cannot process 2M tokens. On the matched 30k version, frontier models likely match or beat the median human.
- **Expected separation [speculation, anchored].** Wide:
  - Claude Code's /compact kept 53% of safety rules after 1 round and 10% after 5 (Compaction Cliff).
  - Retained reasoning plus compaction took GPT-5.6 Sol from 13.3% to 38.3% on ARC-AGI-3's public set.
  - Naive in-context learning beat dedicated memory systems on Continual Learning Bench.
- **Main risks.** It may be a g-proxy; harness politics; query families may be guessable.
- **Evidence.**
  - A §2.3: [OpenAI, "two settings"](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/).
  - E Q1: [Continual Learning Bench](https://arxiv.org/abs/2606.05661).
  - R4 R24: [Compaction Cliff](https://arxiv.org/abs/2608.22752).

### F2 Hidden-Rule Lab (bounded-adversary mode)
**Built from** C42, plus C03's perceptual primitives and C43's setter role (optional). **Both, A1 headline · game.** Support: K3/R2/X0; consensus 3.5/3/3.5/4/4.5/3.5.

| Attack (reviewer) | Fix | Residual risk |
|---|---|---|
| The primitive space is guessable; a lab can RL on a Zendo superset; the Eleusis catalogue has only 68 rules (R1) | Each season ≥ 30% of primitives are new and ≥ 2 are held out. ≥ 25% come from a paid human concept-authoring round. The grammar composes rules to depth 3 over ≥ 200 secret primitives (≈ 10⁶–10⁷ rules), so outsiders have no catalogue to enumerate; only the owner enumerates it. X1 leakage check | Witness saw small RL transfer to held-out primitives |
| Fixed rules reward lucky guesses (R1, R2) | Headline is a bounded adaptive adversary. After the subject stops, it commits to the rule that maximises probe errors among rules consistent with all results and within δ bits of the simplest consistent rule, under a published, frozen prior | If δ is too small, guessing pays; if too large, humans fail. δ is set in the pilot |
| The text/JSON track is at ceiling (R2 probe P2, weak evidence) and enumerable (R1, R5) | JSON becomes a declared ablation; the headline is image-only. Scenes settle under physics, so final contact and support show only in the render. The image-minus-JSON delta is published (C06's pixel-vs-coordinates idea) | If the gap is only scene parsing, perception training closes it |
| A1 evidence is thin and stale; ARC-AGI-3's efficiency gap closed (R2, R5) | Pre-launch pilot on frontier models from ≥ 3 labs and 60 humans. Launch as A1 only if the frontier median needs ≥ 1.25× the human median number of experiments; otherwise publish as A2 | May ship as A2 only |
| Per-rule variance is large (R2) | ≥ 100 games per model per window; censored-survival summary; paired grammar seeds | — |
| GUI vs JSON: the experiment count measures interface fluency (R3) | One structured command set; the human form builder maps to it 1:1; identical renders | — |
| The "ideal Bayesian" reference is arbitrary (R3) | Prior published and frozen. Reference = a greedy max-disagreement experimenter over the enumerated plausible set, labelled an approximation | Not a true minimax optimum |
| Scoring a stated rule needs a judge (R3) | Fidelity is scored only through probes that separate intended from shortcut rules | — |
| Crowded niche with 7 prior benchmarks (R4) | Ship only the bounded-adversary mode, a "worst-case rule learning" story none of them has. Approach the ZendoWorld or Witness authors to host it | May be read as the 8th hidden-rule benchmark |
| Setter role (C43): collusion, pool-relative reward, free-riding (R1, R3, R5) | Optional and unranked. A model-proposed rule enters next season's grammar only if ≥ 2 humans solve it and it spreads a panel that excludes the author's lab. No shared accept/reject logs | Minor |
| An approximate adversary can be exploited where it undersamples (ideation risk) | Exact enumeration of the plausible set, with SMT checks. A release-gate bot searches for adversary blind spots | Cost grows with the grammar |
| Crowd LLM use; tools-off unverifiable (X2, X6) | Pixels never enter any sandbox. Human tasks are visual and interactive. Lab stratum | Server-side image tools |

- **Mechanics.**
  - A 2D/3D block world. The subject issues structured commands (place, drop, rotate, remove; ≤ 12 objects from a palette).
  - The engine simulates settling, renders an image and returns ACCEPT or REJECT. The budget is 40 experiments.
  - The subject may declare "ready" once, then labels 30 probe images: 10 chosen to split the surviving plausible rules, 10 that separate intended from shortcut rules, and 10 random.
  - The adversary then commits (see table).
- **Generation and secrecy.** A private grammar each season. Palettes, probe pools and starting scenes are fresh for every game. The grammar and logs are released after the season. Because the rule is chosen adaptively, a leaked transcript reveals primitives, not an answer (X1).
- **Scoring.**
  - Success = worst-case probe accuracy ≥ 90%.
  - Headline: experiments to success. Failure scores 41 and is treated as right-censored. Reported as the median ratio to the human median (A1 view) and to the reference experimenter (A2 view).
  - Secondary: worst-case accuracy at budgets of 10, 20 and 40; shortcut-probe fidelity; the image-minus-JSON delta.
  - ≥ 100 games per model, with a bootstrap over games.
- **Tools and sandbagging.**
  - Headline: images only, no sandbox.
  - Ablations: an Open track whose sandbox receives the command log and results but never pixels, and a JSON track that supplies the scene graph.
  - No difference score. Declaring early and failing only hurts the subject.
- **Humans.** ≥ 300 first-run adults, 3–4 games each (10–15 minutes), using the same command set through a form.
  - Pay = base + accuracy bonus − a cost per experiment.
  - Lab stratum n ≈ 30. Every rule family is solved by ≥ 2 people.
  - Gate: the median human succeeds within 30 experiments.
- **Cost.** $200–800 per model for 100 games [speculation; images at ≈ 350 tokens each].
- **Expected human vs AI [speculation, anchored].** On the image track, humans need ≥ 25% fewer experiments at launch. On the JSON ablation, the frontier is at or above humans (probe P2, weak evidence). Anchors:
  - ZendoWorld: humans win 73.3% vs 44.5% for VLM agents, whose experiments are "near-uninformative" (19 humans).
  - AutumnBench: 517 humans beat 2025 models.
  - Blicket tasks: LLMs explore less efficiently than people.
- **Expected separation [speculation, anchored].** Wide:
  - The best of 18 frontier models solves 24% of Witness's private-test slots.
  - FalsifyBench finds no model near optimal.
  - 27% of o3's correct ConceptARC answers use the wrong rule, vs 8% for humans.
- **Main risks.**
  - Collapse within about 5–12 months once targeted: on ARC-AGI-3, Astra used fewer actions than the median human on 96% of levels.
  - Calibrating δ.
  - A gap that is purely perceptual.
- **Evidence.**
  - F §2: [ZendoWorld](https://arxiv.org/abs/2607.08233); [Witness](https://arxiv.org/abs/2609.32208).
  - E Q1: [AutumnBench](https://arxiv.org/abs/2510.19788); [blicket study](https://arxiv.org/abs/2606.06464); [ConceptARC](https://arxiv.org/abs/2510.02125).
  - A §2.3: [ARC-AGI-3 / Astra](https://arcprize.org/blog/astra).

### F3 Patch Auditor
**Built from** C37, auditor role only. **A2 · game (a two-sided pool with one scored role).** Support: K3/R2/X0; consensus 3.5/3/4/3/4.5/4.

| Attack (reviewer) | Fix | Residual risk |
|---|---|---|
| A style classifier can separate sabotage from benign generators (R1) | Every diff passes one normaliser (formatting, comments, commit template). Release gate: a classifier on the diff text alone must score AUROC ≤ 0.55 | Semantic cues survive normalisation |
| Benign refactors may break properties, creating label noise (R3, R5) | Each benign diff is certified by the full property suite plus differential fuzzing against the base. Unclear diffs are dropped. 5% expert label audit | Fuzzing is incomplete; the audited error rate is published |
| Tests plus fuzzing find witnesses (R1) | Declared on-construct: the headline is tools-on, with a fixed CPU budget per diff. Tools-off is an ablation | Partly measures fuzzing tool use |
| The frozen saboteur ladder gets outgrown or targeted (R1, R2) | Sabotage comes from a hidden, partly rotated ladder (models from ≥ 3 labs plus scripted mutation operators) and from this season's entrant saboteurs. A fixed legacy diff set anchors seasons | Pool difficulty drifts |
| A proxy for coding ability (R2) | X9 residual after a coding index; breakdown by property family | May be mostly coding skill |
| Humans are not time-matched (R3) | Humans get 6 diffs × 20 minutes. Models get a per-diff token and CPU budget calibrated to ≈ 20 human-minutes. Both get the same repo, tests and fuzzer | The exchange rate is a convention |
| Pre-empted by ControlArena, SHADE-Arena and Auditing Sabotage Bench (R4, R5) | Twist: generated repos with formal property suites and execution-checked witnesses. Ship it as a ControlArena setting | Seen as a setting, not a brand |
| A public saboteur ranking is dual-use (R4) | The saboteur role is unranked; submissions only feed the pool. Conduct telemetry is kept separate | — |
| An unknown base rate invites strategy (R5) | Fixed, disclosed base rate of 30% per batch | — |

- **Mechanics.**
  - Generated repos of 5–20k lines (Python, TypeScript and a private DSL), each with visible tests and a formal property suite.
  - The auditor reviews 500 diffs of ≤ 20 lines, 150 of them sabotaged. For each it outputs P(sabotaged) and, if it claims sabotage, a witness input.
  - The grader runs the witness against the target property outside the sandbox.
- **Generation and secrecy.** Repo templates, property families and languages are private. Each run instantiates fresh repos (new identifiers, property constants and diffs). Templates rotate each season, and the pool is released after the season (X1).
- **Scoring.**
  - Headline: witnessed recall at a 5% false-positive rate ("catches X% of sabotage with a proof, at 5% false alarms"). The threshold is set on the model's own scores over benign diffs.
  - Secondary: log score and AUROC on P(sabotaged); witness validity rate.
  - Paired across models (same diffs). Recall SE ≈ 4 pp; AUROC SE ≈ 0.02 [speculation].
- **Tools and sandbagging.** The headline is tools-on (repo, tests, fuzzer; CPU cap; no internet). Sandbagging only lowers the auditor's own score.
- **Humans.** 60 professional developers × 6 diffs, 20 minutes each, with the same tools. Pay per witnessed detection, plus a proper-score bonus.
- **Cost.** $200–1,000 per model [speculation; R3 gave $100–500 for 300 diffs].
- **Expected human vs AI [speculation].** Frontier auditors beat time-matched developers. A2 is likely but unmeasured.
- **Expected separation [speculation, anchored].** Wide: the best auditor on Auditing Sabotage Bench reached only AUROC 0.77 (Gemini 3.1 Pro), leaving headroom and room for spread.
- **Main risks.** It may proxy coding ability; the control-evaluation space is crowded; benign labels may be wrong.
- **Evidence.**
  - R5 §2: [Auditing Sabotage Bench](https://arxiv.org/abs/2604.16286).
  - R4 R42: [ControlArena](https://github.com/UKGovernmentBEIS/control-arena); [SHADE-Arena](https://arxiv.org/abs/2506.15740).
  - G §1: sealed grading.

### F4 Season Forge
**Built from** C36. **A2 · game (complex).** Support: K1/R4/X0; consensus 4/3/4/3.5/3/3.5.

| Attack (reviewer) | Fix | Residual risk |
|---|---|---|
| The human-percentile headline is already saturated: AI beat all 12 AtCoder WTF 2026 Heuristic finalists (R1–R5) | Headline: a Bradley–Terry rating anchored to a fixed-recipe ladder, reported in ladder-doubling units. Rungs: MCTS/rollout bots at playout doublings 2^6–2^16; the operator's hand-built bot (10× development effort); after the season, a frozen champion ensemble. Human percentile is secondary | Some games gain little per doubling |
| The operator bot may be outscored, leaving no top anchor (R2) | The ladder extends upward with more doublings and frozen entrant bots. Rungs are added, never replaced | — |
| Best-of-3 is variant spamming, and attempt variance dominates (R1, R2) | ≥ 5 pre-registered attempts per model; mean rating with an attempt-level CI (X3) | Cost |
| BYOH lets labs ship mature game-AI frameworks (R1) | Frozen minimal harness as headline; BYOH delta published | — |
| A 6-hour wall-clock limit measures infrastructure (X8) | Budget: ≤ 8M billed output tokens and ≤ 48 sandbox core-hours, with a loose 48-hour wall-clock cap | Token prices differ; $ reported |
| Remote proctoring cannot stop humans using AI (R3) | Annual human season, in person or on locked VMs | $20–50k a year |
| Cost of about $1–3k per model; Q5 3 (R5) | A Lite track (≤ 1M tokens, 4 core-hours, 3 attempts) gives cheap trend lines. The Standard track runs each season | Lite and Standard may rank differently |
| CodeClash, ALE-Bench and AtCoder pre-empt the story (R4) | Differentiators: a secret new multi-player fog-of-war game every season, an anchored ladder, and a legacy league of past games | May read as another bot contest |
| Engine bugs become reward hacks (R1, general) | The engine is fuzzed before release. Bug exploits are flagged as conduct and re-run on a patched engine | — |

- **Mechanics.**
  - Each season brings a new 2–4-player simultaneous-move territory and economy game from a private design grammar: fog of war, 200–500 turns, hidden but inferable dynamics.
  - Entrants get rules text, an engine binary (no source), a local runner and 5 public maps.
  - They write a bot inside a frozen minimal agent harness: an 8-core sandbox, no internet, and the budget above.
  - Each bot plays ≥ 2,000 games on private maps, generated after submissions lock, against the ladder and other entrants. Seats rotate and map seeds are duplicated.
- **Generation and secrecy.** The game is new at season start by design. Evaluation maps are private and generated per match. The engine is released after the season, and past games join a legacy league that new models may enter at the same budgets.
- **Scoring.**
  - Bradley–Terry maximum likelihood with ladder ratings held fixed; bootstrap CIs over games and attempts.
  - Secondary: win rate against the operator bot, head-to-head matrix, Lite rating, human percentile (annual), $ and tokens.
- **Tools and sandbagging.** Code is the construct (X2). Taking the mean over pre-registered attempts removes the incentive to cherry-pick.
- **Humans.** An annual season: 50–100 contest veterans, solo, 6 hours, 8 cores, proctored, with prizes. An optional human-plus-AI team track.
- **Cost.** $1.5–4k per model per season for 5 Standard attempts; $200–600 for Lite [speculation]. Human season $20–50k a year.
- **Expected human vs AI [speculation, anchored].** Frontier bots beat the median veteran: at AtCoder WTF 2026 the AI scored more than 7× the best human in the Heuristic final.
- **Expected separation [speculation, anchored].** Tournament CIs are tight (thousands of games); attempt-to-attempt variance is the largest term (R2). CodeClash shows headroom above current models: Sonnet 4.5 won 0 of 37,500 rounds against an expert human bot (Nov 2025).
- **Main risks.** The cost and upkeep of a new game each season; harness effects; the value of a ladder doubling varies by game.
- **Evidence.**
  - D §2.22: [CodeClash](https://arxiv.org/abs/2511.00839).
  - R4 R41: [AtCoder WTF 2026](https://the-decoder.com/openais-ai-beats-every-human-at-atcoder-a-top-competitive-programming-contest/); [ALE-Bench](https://github.com/SakanaAI/ALE-Bench).
  - D §2.6: [NetHackers](https://github.com/dunnolab/nethackers).

### F5 Self-Knowledge Exam
**Built from** C14 + C15 + C26 (merge proposed by R1, R4, R5). **A2 · benchmark.** Support (C14): K2/R3/X0; consensus 3/3/4/3.5/4.5/3.5.

| Attack (reviewer) | Fix | Residual risk |
|---|---|---|
| Log-wealth mostly rewards accuracy (R2, R5) | Headline Self-Resolution: the log score of the model's own confidence minus the log score of its own per-family base rate, measured in the same run on blind twins. It is zero for a model that knows only its average | Base-rate noise; ≥ 40 twins per family |
| Frozen house lines age, so newer models win on strength alone (R1, R2, R5) | No external panel: the reference is the model itself, measured at the same time | — |
| Self-fulfilling forecasts: give up and forecast 0 (R1) | Minimum-effort rule: a token floor plus a checked attempt artefact. Forecast items and blind twins are interleaved and indistinguishable; an accuracy gap > 3 pp between them voids the run | Subtle effort modulation |
| Calibration can be RL-trained, e.g. with RLCR (R1) | Calibration is on-construct. The headline is resolution, which needs item-level self-knowledge. Families are fresh each run | Success predictors trained on the model's own rollouts |
| Trap items carry surface cues (R1) | Style-matched trap pairs. Release gate: a cue-only classifier scores at chance | — |
| Self-knowledge beyond base rates may be ≈ 0 and lost in noise (R2; R4 citing Masked by Consensus) | A warm-up adapts difficulty so each model's success rate sits at 35–65%. ≥ 1,500 scored items. Pre-registered MDE ≈ 0.02–0.03 nats per item [speculation] | Results may be flat; nulls are published |
| Abstention is a policy knob that flips within a release (R2) | Abstention rate is reported as a dated policy axis, not the headline | Policy still shapes what gets attempted |
| Pre-empted by AA-Omniscience and MarketBench; name clash with KellyBench (R4) | Renamed. Auction dropped. The headline is resolution and triage, not hallucination rate. Pitch to a neutral index | Overlap perceived anyway |
| The auction reduces to self-prediction plus learning the anchor bidders; profit is heavy-tailed (R1, R2, R3) | Triage replaces the auction | Loses the market story |
| Pay linear in wealth elicits corner bets (R3) | Human pay is linear in log score, with a floor | — |
| Humans cannot re-attempt an item "fresh"; an agentic human arm costs too much (R3) | Human arm on non-agentic families only: forecast, then a single attempt | No human data on agentic families |

- **Mechanics.**
  - Each run draws ≈ 1,800 items from private generators in 6 families: synthetic-document QA (answerable, planted contradiction, or not determinable), fresh exact computations, post-cutoff facts from a sealed feed, puzzles, code with hidden tests, and short agentic tasks (10–40 tool calls).
  - For 75% of items: (1) the model forecasts q = P(I will solve this) with ≤ 300 thinking tokens; (2) in a fresh context it attempts the item and states a confidence p.
  - The other 25% are blind twins, attempted without a forecast.
  - Triage: 3 blocks of 60 task cards; the model chooses 20 to take. All 60 are then attempted off the books.
- **Generation and secrecy.** Fresh items every run, from generators that add new families quarterly (X1). Trap styles rotate.
- **Scoring.**
  - Headline 1: Self-Resolution in nats per item, computed on p.
  - Headline 2: Triage value = (successes on the chosen 20 − 20 × the model's own success rate on the block) ÷ (successes on the best possible 20 − the same). Blocks are aggregated before dividing (X4).
  - Also reported: prospective (q) resolution, accuracy, ECE, Brier decomposition, and abstention (dated).
- **Tools.** None on non-agentic families; agentic families use their task sandbox. Forecasts are made without tools.
- **Humans.** 250 adults (200 public, 50 enthusiasts), each doing 1–2 tables of 100 non-agentic items: forecast, then a single attempt. Pay is linear in log score.
- **Cost.** $300–1,200 per model [speculation; R3's C14 basis plus the agentic and triage items].
- **Expected human vs AI [speculation].** Accuracy is clearly A2. Resolution relative to humans is untested and could go either way.
- **Expected separation [speculation, anchored].** Lab-level differences are documented for policy: AA-Omniscience hallucination rates ran 48–88% across Nov 2025–Jan 2026 models. Resolution beyond base rates may be small:
  - Masked by Consensus: self-probes beat peer probes only on disagreement subsets.
  - MarketBench: models forecast their own success poorly.
- **Main risks.** A flat result; policy drift; perceived overlap with AA-Omniscience.
- **Evidence.**
  - B §3.7: [AA-Omniscience](https://arxiv.org/abs/2511.13029).
  - R4 R21: [MarketBench](https://arxiv.org/abs/2604.23897).
  - R4 R20: [Masked by Consensus](https://aclanthology.org/2026.acl-long.483/).
  - R1: [RLCR](https://arxiv.org/abs/2507.16806).

### F6 Stump Arena
**Built from** C05 + C39 (merge proposed by R3, R5). **A1 · hybrid (an authoring game feeding a renewing benchmark).** Support (C05): K2/R3/X0; consensus 3/4/3/3/3/4.

| Attack (reviewer) | Fix | Residual risk |
|---|---|---|
| Closed panel models see every candidate item, giving their labs free adversarial data (R1) | Only locally run, pinned open-weight models are used for gating. Closed models see each item once, at scoring | The open panel lags the closed frontier, so the hard pool is easier for closed models (measured, not hidden) |
| Winner's curse from selecting on pass@3 failure (R2, R5) | Scored models never take part in selection. The hard-pool gate is pass@8 on fresh seeds. Open panel members are scored only on items gated by a disjoint panel split | — |
| The 3-of-5 human gate is loose (posterior ≈ 71%) (R2, R3) | ≥ 4 of 5, then an independent re-gate by ≥ 10 fresh naive adults. An item enters the pool only at a re-gate solve rate ≥ 80%; per-item CIs are published | Online adults only |
| ≈ 30% of crowd verifiers use LLMs (R1, R3) | X6. Items whose online solve rate exceeds the lab stratum's by > 15 pp are dropped | Some AI-assisted verifiers remain |
| Author-minutes cannot be measured (R3), yet cost-to-stump is the proposed headline (R4) | Yield is measured only on a controlled author stratum: ≈ 100 paid naive authors, 2 × 60-minute proctored sessions each, with a random target cluster per session. Bounty items feed the pool but not the metric | Stratum authors learn tricks; cohorts are reported |
| Quirk farming; no stable construct (R1, R4, R5) | A fixed 8-cluster taxonomy with per-cluster quotas. A minimum feature size. Banned tricks (tokenisation, letter counting). Results by cluster | Clusters get patched, which is the trend being measured |
| Ambiguous items, as with HLE's disputed answers (R5) | 10% adjudication plus an appeal window | Label error of a few % |
| Filtered pools decay: HLE went from 3% to 68% (R2) | The headline uses only the current season. A decay curve against a matched control pool is published | The headline's meaning shifts as clusters close |
| Scoring against a panel penalises the panel's labs; frozen panels get deprecated (R3, R4) | No closed lab sits on the panel; the open weights are pinned | — |
| Model authors mine known weaknesses or plant injection and refusal triggers; weaker authors are favoured; sandbagging (R1, R4) | An input spec, plus injection and refusal scans. Credit only for items failed by ≥ 2 other labs' models, including one rated stronger last season | Mining other labs' weaknesses is the construct |
| A lab scored twice in a season learns the pool (X1) | The pool is split into monthly tranches; a model is scored on the newest tranche its lab has not seen | Smaller n for late releases |
| Upkeep: Dynabench faded (R4). Sybil verifiers (R1) | A named steward and a stated budget (X10). ID-verified paid roles, random verifier assignment, collusion audits | Funding |

- **Mechanics.**
  - Authors build micro-items (image, video ≤ 15 s, audio, short text rendered as an image, interactive widget). Each needs a checkable answer that follows from the item itself, not trivia.
  - Three author sources: open bounty authors; the controlled stratum; and a secondary model-author arm, in which each entrant model submits 100 items per season through the same tool API.
  - Items pass the human gate, the re-gate and (for the hard pool) the open-panel gate described above.
  - Each scored model answers every item in its current tranche once.
- **Generation and secrecy.** Quarterly seasons. Items stay sealed until scored. Retired items are released as practice after 6 months. A per-lab burn log (X1).
- **Scoring.**
  - Exact match after normalisation.
  - Headline 1, the A1 gap: the human re-gate solve rate minus the model's pass@1 on the full human-gated pool, macro-averaged over clusters. The hard-pool figure is also shown.
  - Headline 2, stump yield: controlled-stratum items that humans pass and model M fails, per author-hour. Its inverse is the "cost to stump M", trended across seasons.
  - Model-author arm: diversity-weighted accepted items, plus precision.
  - ≥ 1,500 gated items per season give a per-model solve-rate SE of ≈ 1.3 pp before clustering by author, which inflates it 1.5–2× [speculation].
- **Tools.** The headline is tools-off, matching the human gate; tools-on is reported.
- **Humans.** Built in: 5 gate verifiers and ≥ 10 re-gate adults per item, plus a lab stratum of n ≈ 30 per season.
- **Cost.** Scoring $50–300 per model [speculation]. Programme $25–40k per season, covering gating (≈ $4 per candidate item, per R3), the re-gate, the author stratum, bounties and the lab stratum [speculation].
- **Expected human vs AI [speculation, anchored].** Humans score ≥ 85% on the pool by construction. Frontier pass@1 at launch is perhaps 40–75% on the full pool and 15–40% on the hard pool. Adversarial Quizbowl authoring cut strong models' relative accuracy by up to 40% while leaving human difficulty unchanged.
- **Expected separation [speculation, anchored].** By cluster and by lab: BabyVision spans 49.7 vs 14.2 across labs (Jan 2026 models), and MUSE audio results split by vendor.
- **Main risks.** Upkeep; construct drift; on the hard pool the A1 gap is partly selected rather than measured.
- **Evidence.**
  - P3 fact-check log: [adversarial Quizbowl](https://aclanthology.org/Q19-1029).
  - R4 R8: [Blind-Spots-Bench](https://arxiv.org/abs/2607.08317). R4 R7: [HLE](https://www.nature.com/articles/s41586-025-09962-4).
  - R3: [crowd LLM use](https://arxiv.org/abs/2306.07899); [deterrents](https://arxiv.org/abs/2310.15683).
  - E Q2: [BabyVision](https://raw.githubusercontent.com/UniPat-AI/BabyVision/main/README.md).

### F7 Unrun Lab
**Built from** C21, plus C23's ML-training family as Track M (R4's fold). **A2 (Track M's direction untested) · benchmark.** Support (C21): K3/R1/X1; consensus 3.5/4/4.5/3/5/2.5.

| Attack (reviewer) | Fix | Residual risk |
|---|---|---|
| Models recognise textbook families (SIR, Lotka–Volterra, queues) and run a simulation-based-inference pipeline (R1, R2, R5) | Simulators are composed from secret mechanism primitives (thresholds, delays, heavy tails, regime switches, feedback) with no textbook identity. ≥ 30% of primitives are new each season, and ≥ 2 are held out | Compositions of known motifs stay partly recognisable |
| The score is capped at 1, and simple families approach it (R1, R2) | Knobs: history length, intervention budget, noise. ≥ 50% of questions are interventional, outside the data's support. Difficulty is set so frontier skill is 20–60% at launch | A ceiling exists in principle |
| AutoML may win; "CRPS share" is illegible (R4) | AutoML and an owner-written generic learner get the same data and experiments, and the better of the two is the zero point. Headline: "% of achievable forecast skill" | If the anchors win, that is a finding, not separation |
| The ratio is unstable when an anchor is near the truth (R3 flaw 10) | Scores are summed over questions before dividing; absolute CRPS is reported too | — |
| The human reference is thin, ≈ 3 people per simulator (R3) | The human reference is pooled by family and is not a headline | — |
| Track M: truth from 3–5 seeds is noisy (R2, R3, R5) | ≥ 20 seeds per arm; scoring against the empirical seed distribution | Heavy-tailed seeds |
| Track M: labs can pre-run template experiments (R1) | Secondary track only. Templates are secret and rotate quarterly. Predictions lock before the owner runs anything | Still amortisable; flagged |
| Track M: families (b)–(d) dilute it; owner compute is costly (R4, R5) | ML-training deltas only; ≈ 150 items per season; a sponsor covers compute | $5–20k per season |
| Track M: A2 against ML researchers is unproven (R2) | A pilot human comparison before launch; the archetype is stated as untested | May turn out "Both" |
| Low interest on its own (R4, Q6 2) | Track M carries the "can AI predict unrun ML experiments?" story; Track S carries the ranking | Two headlines |

- **Mechanics.**
  - **Track S** (the ranking headline): 20 simulators per run. Each comes with 10k rows of history and a budget of 20 interventions, chosen by type, timing and size from a menu; each intervention returns one sample path. A CPU-capped Python sandbox is provided. The model answers 50 questions, as quantiles (5/25/50/75/95) or probabilities.
  - **Track M** (seasonal): ≈ 150 precisely specified small-model training experiments that nobody has run yet (e.g. swap the optimiser, change the width, add label noise, all on generated data). The model predicts quantiles of the change in the metric. Predictions lock before the owner runs the experiments.
- **Generation and secrecy.** Fresh simulator instances every window, from the private mechanism grammar. Track M templates rotate quarterly. Truth is computed after predictions lock, and everything is released after the window (X1).
- **Scoring.**
  - Track S: CRPS or log score against the distribution of 10,000 rollouts, expressed as skill between the best anchor (0) and the true distribution (100). 1,000 paired forecasts per model.
  - Track M: CRPS against distributions of ≥ 20 seeds, expressed as skill over a "no change" prior and a scaling-law extrapolator.
- **Tools.** Track S: code is part of the construct. Track M: the headline is no-code; a code track is capped at ≤ 1% of the experiment's compute.
- **Humans.** Both arms are paid by proper score.
  - Track S: 60 data scientists, pooled by family, with the same sandbox and 3 hours per 2 simulators.
  - Track M: 40 ML researchers and 40 CS graduate students, no code.
- **Cost.** Track S $100–500 per model. Track M $50–300 per model plus $5–20k of owner compute per season [speculation; R3 and ideator basis].
- **Expected human vs AI [speculation].** Track S: models with a sandbox likely beat data scientists. Track M: unclear. A fine-tuned system beat experts 64.4% vs 48.9% at picking which research idea performs better, while off-the-shelf o3 was near chance.
- **Expected separation [speculation, anchored].** Wide on Track S. Truth is a distribution, so outcome noise disappears and 1,000 paired forecasts resolve small differences (R2 gave Q3 = 5).
- **Main risks.** Motif recognition; anchors winning; Track M experiments being pre-run.
- **Evidence.**
  - F §2: [NewtonBench](https://raw.githubusercontent.com/HKUST-KnowComp/NewtonBench/main/README.md); its altered-law family became an RL environment in ≈ 4.5 months.
  - G §4: 42% of FrontierMath problems needed fixes, which motivates rollout-based truth.
  - R4 R29: [Wen et al.](https://arxiv.org/abs/2506.00794).

---

## 5. Provisional ranking

| Rank | Finalist | Archetype | Justification |
|---|---|---|---|
| 1 | F2 Hidden-Rule Lab | Both (A1 headline) | 3 keeps, 0 kills. Best Q4 + Q5 among finalists (4 / 4.5); cheap and exact. The only A1 design with no latency and no live human in the score. The bounded adversary is a twist none of the 7 prior hidden-rule benchmarks has. Risk: ARC-AGI-3-style collapse; the pilot may downgrade it to A2 |
| 2 | F1 Compaction Chronicle | A2 | The most reviewer support (4 keeps). Measures the variable that decided ARC-AGI-3 and a capability labs sell (long-running agents). Risk: g-proxy; weak human comparison |
| 3 | F3 Patch Auditor | A2 | 3 keeps. Execution-checked witnesses. A real adoption channel (system-card safety sections, ControlArena). Risk: coding proxy; crowded space |
| 4 | F7 Unrun Lab | A2 | The highest consensus mean (3.75) and near-noiseless truth. Track M supplies the audience C21 lacked. Risk: motif fitting; anchors winning; two headlines |
| 5 | F6 Stump Arena | A1 | The only design whose A1 headroom renews, with public participation and a new headline (stump yield). Ranked lower because every question sits at 3 and upkeep is heavy |
| 6 | F4 Season Forge | A2 (complex game) | The strongest game on the merits: Q1 4, 0 kills, tight tournament CIs, and code as a declared construct. Ranked lower on cost (Q5 3) and a human-vs-AI story that is already told |
| 7 | F5 Self-Knowledge Exam | A2 | A distinct, cheap axis on which labs differ. But resolution beyond base rates may be flat, and human vs AI is untested |

**A1.** Two finalists (F2, F6) survive the three main A1 objections: neither uses real time or wall-clock limits, and neither puts live humans inside a model's score. F2 stays exposed to fast closure once targeted, and says so through its pilot gate. F6 makes closure the quantity it measures. C09 is the next A1 candidate in line (§2).

**Game.** F4 is a genuinely complex game: multi-player, simultaneous moves, fog of war, 200–500 turns. F2 and F3 are simpler interactive games.
