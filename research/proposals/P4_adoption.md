# P4 (adoption-and-appeal lens): SECOND READER — how long a document can an AI check?

*Proposal, 2026-09-29.*

**Citation conventions.**
- `[key]` resolves in `research/refs/*.json`.
- `[C:offg]` is the ECI-refit analysis in `notes/gap_offg_construct_evidence.md`; `[D:MCA]` is the headline-table count in `notes/model_cards_adoption.md`.
- † marks works checked this session by web or GitHub search, at abstract or README level (confidence M). They are listed in Appendix B.
- `[I]` marks interpretation; `[computed here]` marks my own arithmetic or simulation.

---

## 1. Name and thesis

**SECOND READER.** A repository and web search found no LLM benchmark with this name; the only hit is a 1-star note-taking repo. A full collision check is still due before launch (F12).

**Thesis: trust scales with checking.** Models now write more than people can read, and their output is worth only as much as the errors someone catches in it. Professional work already runs on the *four-eyes principle* (code review, audit, copy-editing). The question buyers and labs keep asking is:

> **How long a document can this model check and still catch the one wrong line, without crying wolf when there is none?**

**Headline: the catch horizon (CH50), in pages.** CH50 is the length of a never-seen document at which the model's *net catch* reaches 50%. Net catch is planted errors pinpointed minus false alarms on the error-free twin. A page is 40 numbered lines. As with METR's time horizon [metr2025horizon], the axis is open-ended, so headroom is structural.

**The line a journalist can repeat:** "Model X is a coin-flip second reader at 12 pages. Professional checkers working at 2 minutes a page reach N."

**Philosophy.** ARC asks "can it learn?" [chollet2019measure]. Arena asks "which answer do people prefer?" [zheng2023arenablog]. Second Reader asks **"can you trust it to check?"** Credit requires both halves: *catch it* and *don't cry wolf*.

**What made benchmarks sticky, and this design's version of each:**

| Sticky feature | Evidence | Second Reader |
|---|---|---|
| Thesis-bearing name | ARC→ARC-AGI; HLE (`notes/virality_consumer.md` §2.1, §2.6) | names the role, not the task |
| Legible, unbounded unit | METR's horizon spans about 4,600× [metr2025horizon; metrEvalAnalysis2026] | pages; a doubling-time chart |
| One ladder | Arena's CI-backed single score [lmarena2025twoyear] | one CH50 with CI and cost per catch |
| Lab-adoption loop | a neutral runner is the top adoption predictor [D:MCA; google2025gemini3eval] | neutral runner; symmetric pre-release runs; Inspect and lm-eval at launch |
| Shareable artifacts | pelican; Vending-Bench stories [willison2025yearinllms; willison2025gemini3] | deterministic "miss cards"; release-day diff cards |
| Try-it layer | ARC's playable tasks (`virality_consumer.md` §2.1) | "Be the second reader" public pages |

## 2. Construct definition

**Construct: document vigilance.** The ability to locate, in a long, never-seen, internally structured document, the single line (if any) that contradicts the rest of it. The contradiction can be with the document's figures, its stated rules or its cross-references. The model must also declare a clean document clean.

**Components** (each tagged per item and reported as diagnostics):
1. Exhaustive coverage: there is no cue about where to look.
2. Binding at a distance: a rule on line 4 governs line 290.
3. Derived checking: 1–3 computations, such as time-zone offsets, running balances or date arithmetic.
4. Premise scepticism: the supplied document may be wrong.
5. Specificity: surprising-but-correct lines must not be flagged.

**What it is not:**
- knowledge (every needed fact, including offsets and rates, is in the document);
- arithmetic prowess (numbers are small, and G4 items need no arithmetic);
- retrieval (there is no query and no lexical cue);
- writing.

**Pre-registered network** (relation to the log CH50 residual after partialling out ECI):
- *Convergent* (residual ρ ≥ 0.3): FIND†, FinED-Bench†, ProcessBench†, BIG-Bench Mistake†. These use different formats and human-inserted or natural errors.
- *Discriminant*: the relation should be weaker for RULER, MRCR and NIAH (same long-context format, retrieval construct) [hsieh2024ruler; kamradt2023niah], and near zero for knowledge QA.

## 3. Why it is not a game (C1)

- **No opponent.** Errors are planted by a fixed stochastic program whose distribution never adapts to the model.
- **No play.** There is no win or loss, no turns, moves or board. The model reads one document and returns one line number or NONE.
- **Not a puzzle.** The items are documents people are paid to check (itineraries, stock ledgers, leases, run-sheets), and the errors follow a real clerical-error taxonomy.
- **No referential or signalling framing.** There is no partner, and nothing is decoded except by the scorer.
- **The try-it page is an assessment, not a game.** It has no points, streaks or human rankings.

## 4. Worked example: one complete item

This is an itinerary item: 0.5 pages (22 lines), grade G3 (derived), shown verbatim. The bracketed notes are **not** part of the prompt.

```
You are acting as the second reader of the document below. Its lines are numbered.
Either exactly one line is inconsistent with the rest of the document (its figures,
its stated rules, or its cross-references), or the document is fully consistent.
Everything needed is in the document. Do not use any tools.
Think as long as you like, then end with exactly one line:  LINE: <number>  or  LINE: NONE
Optionally add:  BECAUSE: <numbers of the lines it conflicts with>

 1  ITINERARY KX-4471 · Traveller: Imogen Adeyemi · Issued 12 Oct 2026
 2  Travel policy (Halvorsen & Pike, rev. 3):
 3  P1  Minimum connection: 60 min within one country; 90 min otherwise.
 4  P2  Each hotel stay runs from the arrival date in that city to the next departure from it.
 5  P3  All times are local. The offsets below apply on all travel dates.
 6  Airport  City       UTC offset
 7  LIS      Lisbon     +0
 8  FRA      Frankfurt  +1
 9  YYZ      Toronto    -5
10  ORD      Chicago    -6
11  Flights (flight · date · from dep → to arr · block time)
12  F1  NV 572  Tue 03 Nov  LIS 07:10 → FRA 11:05  2h55
13  F2  NV 470  Tue 03 Nov  FRA 13:05 → YYZ 16:40  8h35      [ERROR: generator value 15:40]
14  F3  QA 505  Fri 06 Nov  YYZ 09:15 → ORD 10:05  1h50      [decoy: "lands 50 min after take-off"]
15  F4  QA 958  Sun 08 Nov  ORD 17:30 → LIS 08:35 (Mon 09 Nov)  9h05   [decoy: next-day arrival]
16  Hotels
17  H1  Toronto, Front Street  in Tue 03 Nov  out Fri 06 Nov  3 nights
18  H2  Chicago, Wabash Ave    in Fri 06 Nov  out Sun 08 Nov  2 nights
19  Totals
20  T1  Block time, all flights: 22h25
21  T2  Hotel nights: 5
22  T3  Days away (departure to return, inclusive): 7
```

**Grounding.** The airports and their November 2026 offsets are real (checked with Python `zoneinfo` against the IANA tz database), and the weekdays match the 2026 calendar. Airlines and flight numbers are fictional, so only the document itself can be checked.

**Key.** `LINE: 13`. The template-generated oracle sentence, which also becomes the public miss card, reads: *"13:05 at FRA (UTC+1, line 8) is 12:05 UTC; plus 8h35 is 20:40 UTC = 15:40 at YYZ (UTC−5, line 9). Line 13 says 16:40."*

**Uniqueness, checked automatically.** The only violated constraint is F2's timing, whose scope is lines {8, 9, 13}. The oracle tries a fix at each line in scope:
- Setting FRA to +0 fixes F2 but breaks F1.
- Setting YYZ to −4 fixes F2 but breaks F3.
- Only line 13 repairs the document.

A 30-line script confirms this [computed here].

**Scoring.**
- `LINE: 13` is a hit.
- `LINE: 14` is a miss: the model took the decoy.
- The clean twin (line 13 = 15:40) runs in a separate call. There, `LINE: NONE` is a correct rejection and any number is a false alarm.

## 5. Generator design (C4, C5)

**Families are human-authored.** Each family is written by a paid practitioner (travel coordinator, stock controller, paralegal, events manager) together with an engineer, and reviewed by a second author. A family has four parts:
- (a) a typed data model;
- (b) **constraints as code**: sums, running balances, time arithmetic with stated offsets, date arithmetic from a stated anchor, capacities, no double-booking, reference integrity, and *house rules* that deliberately depart from common defaults (e.g. overtime after 37.5 h) so that memorised norms mislead;
- (c) samplers grounded in real structure: IANA time zones, real airports, public-domain name-frequency lists, ISO currency codes, realistic value ranges;
- (d) several hand-written templates per field, mixing tables and prose.

v1 has 8 families: itinerary, stock ledger, lease schedule, event run-sheet, purchase ledger, timesheet, lab solution-prep sheet and production batch sheet. At least 3 further families are private each season.

**Mutations** follow the clerical-error taxonomy: transposition (54→45), decimal slide, off-by-one hour/day/unit, neighbour copy, stale value (rent before escalation), sibling-reference swap, and a small threshold breach. Every mutated value keeps its field's format, precision and range.

**Oracle.** After mutation, the checker lists the violated constraints and their line scopes. Each line in the intersection of those scopes is a candidate. For each candidate, the checker solves for the implied value and re-runs every constraint. An item survives only if **exactly one line** repairs it and its clean twin passes every constraint. The reference checker therefore scores 100% by construction, enforced by CI on each release (F2, F8).

**Decoys.** Each page carries *d* surprising-but-consistent lines: "arrivals before departure" across time zones, zero quantities, refunds, leap days, amendments that lawfully override earlier clauses.

**Length by "core + padding".**
- A *core* is the error line, its witnesses and decoys, at most one page long, and human-validated (§12).
- The core is embedded at a random position in consistent padding from the same family. The padding has live constraints of its own, so it must be checked too.
- The same core can appear anywhere from 0.5 to 512 pages. The length effect is thus estimated within the core, and the core stays solvable at every length.

**Freshness.** Items are generated at evaluation time from private seeds, with new entities, values and positions in every window. No LLM authors, mutates or paraphrases anything in v1. If paraphrase is added later, each paraphrased line must re-parse to identical field values or it is discarded (C4).

## 6. Scoring and headline unit (C3, C6)

For model *m*:
- Fit two logistic curves in log₂ℓ, where ℓ is length in pages. One is for hits on error documents: logit H = α_m + β_m·log₂ℓ. The other is for flags on clean documents: logit F = γ_m + δ·log₂ℓ, with δ shared across models and per-model δ as a robustness check.
- Net catch is N_m(ℓ) = H_m(ℓ) − F_m(ℓ), the standard corrected hit rate [I].
- **CH50_m** is the smallest ℓ with N_m(ℓ) = 0.5.
- The 95% CI comes from a cluster bootstrap over cores (2,000 resamples).
- If N stays above 0.5 at the longest tested length, the result is reported as "> ℓ_max" and the ladder is extended.

**Parsing.** Only the final `LINE:` field is read.
- Unparseable output and multi-number answers are wrong on both document types: a miss on an error document, a false alarm on a clean one. Hedging therefore never pays.

**Shipped null baselines:**
- Always NONE: exactly 0.
- Random line: negative.
- Position prior: about 0.
- A "local checker" script (within-line arithmetic only): at most the G1 share.

**Diagnostics only:** CH80, H, F, witness accuracy, per-family and per-grade horizons, the search gap (§11), tokens and cost per catch.

**Precision** [computed here; simulation with logit slopes of −0.8 to −1.2 per doubling]:
- The pilot design (40 error and 20 clean documents per model) gives a 95% CI of about ×0.5–×2.
- About 300 error and 60 clean documents, placed adaptively within ±1 doubling of each model's horizon, give about ×0.75–×1.35.
- Adjacent models are separated by paired, item-level comparisons on identical documents.

## 7. Difficulty knob and expected curve (C5)

| Knob | Levels |
|---|---|
| **Length ℓ** (the headline axis) | 0.5, 1, 2 … 512 pages |
| **Grade** (standard mix 25% each) | G1 local (witness within 3 lines); G2 distant (witness ≥ 25% of the document away); G3 derived; G4 house rule, no arithmetic |
| **Decoy density d** | 0, 1 (standard), 2 per page |
| **Clean-twin share** | fixed at 1/3 |

**Expected curve (hypotheses).**
- Net catch falls logistically in log₂ pages, a vigilance decrement.
- Mid-document errors are missed most; the randomised core position makes this testable.
- G3 and G4 are hardest without tools; G1 becomes trivial with tools.

**Pre-declared tiers.** *Standard* (the headline), *Hard* (G3 and G4 only) and *Long* (64 pages or more).
- Launch requires frontier net catch at 64 pages to be at most 30% on the Standard mix.
- The Standard mix is revised (d = 2, more G3) only after the frontier CH50 passes 256 pages.
- Versions are linked through a frozen anchor set of 200 cores with fixed-parameter IRT [habba2026growingpains; ho2025rosetta].

## 8. Contamination and gaming defences (F4, F7)

- **Training-time contamination.** Instances are new each window, and private families and seeds rotate each season. Public families ship with their generator for practice. The public–private gap in CH50 is published as a parallel-form estimate [zhang2024gsm1k].
- **Generator-as-curriculum.** Public generators become RL tasksets [primeintellect2026longcontext]. Each version therefore fine-tunes an open model on the public families and reports its transfer to private families as a contamination index.
- **Heuristic defences:**
  - clean twins defeat always-flag;
  - decoys defeat "flag the odd-looking line";
  - uniform core positions defeat position priors;
  - randomised table or prose rendering defeats template keying;
  - the one-line answer defeats multi-guessing.
- **Do-nothing** scores exactly 0 [zhu2025abc].
- **Run-time leakage.** Content is fictional, and private keys never leave the runner, so there is nothing to look up [anthropic2026browsecomp].
- **Harness.** The prompt and settings are pinned, and provider-harness numbers are listed separately [kamradt2026astra].

## 9. Tool regime (C10)

- **Sealed track (headline).**
  - One text call per document.
  - No code execution, retrieval or web.
  - Reasoning is allowed and its tokens are reported.
  - Pinned temperature and output cap.
  - Any tool call invalidates the transcript.
- **Tool track (separate board).**
  - Sandboxed Python with the document as a file, and no network.
  - It measures per-family **tool uplift** on purpose: brute-force by code is measured, not banned.
  - Hypothesis: ledgers become near-trivial with parsing, while prose house rules resist it.
- **Web lookup** is banned in the sealed track and useless in both, because the content is fictional.

## 10. Real-world relevance (F11)

**The decision it informs.** CH50 answers a deployment question directly: *at what chunk size can I rely on this model as reviewer?* It maps onto products labs sell: AI code review, contract and document review, accounts-payable checks, and agents auditing their own long transcripts.

**Evidence of the need:**
- About half of test-passing SWE-bench Verified patches would not be merged [metr2026mergeability].
- Benchmark audits found errors that reviewers had missed:
  - 42% of FrontierMath problems had errors [epoch2026frontiermathv2];
  - only 641 of 2,500 HLE items were certified [zhai2026hleverified];
  - at least 59.4% of audited hard SWE-bench Verified items were flawed [openai2026noVerified].
- Error-detection benchmarks are appearing at 2026 venues (FIND† and FinED-Bench† at ACL 2026 Findings).
- FinED-Bench† reports that performance falls with document length, which supports length as the axis.

## 11. Incremental-validity argument and test (C7)

**Argument.** Four pieces of evidence make a distinct construct plausible, though none proves it:
1. **Finding dissociates from fixing.** BIG-Bench Mistake†: LLMs "cannot find reasoning errors, but can correct them given the error location", with GPT-4 best at 52.87. Generator–validator agreement is 76% for GPT-4 [li2024gvconsistency].
2. **The specificity half loads on propensities that do not rise with capability.** Premise-deference propensities are not monotone in capability. In the Safetywashing data, the *non*-sycophantic rate correlates −0.66/−0.67 with capability PC1 [C:offg; ren2024safetywashing]. MASK finds that honesty does not improve with scale [ren2025mask]. Reasoning fine-tuning *degrades* abstention by 24% on average [kirichenko2025abstention], and a correct NONE is a form of abstention.
3. **Uncued long-document processing is a separate bottleneck.** Removing lexical cues shrinks effective context 16× to more than 128× [modarressi2025nolima]. Fiction.LiveBench keeps more specific variance (ρ = 0.73 with the ECI refit; reliable specific share 0.41) than ARC or GPQA [C:offg].
4. **The counterweight.** Novel-sounding constructs usually collapse onto g: ARC correlates 0.95–0.97 with the ECI refit, CL-bench 0.71 [C:offg]. So distinctness is a secondary, falsifiable claim, and the unit's product value does not depend on it.

**Pre-registered test.**
1. **Sample.** At least 60 models (target 100) from at least 10 families, with GPQA and ARC-AGI-2 re-scored as yardsticks. About 57 models give 80% power against collapse at a true disattenuated r of 0.75 [C:offg].
2. **Falsifier.** A disattenuated leave-one-out ECI-refit correlation ≥ 0.9 counts as collapse. The benchmark would then be marketed as a product measure only.
3. **Residual reliability.** Split-half by family and seed must be ≥ 0.5.
4. **In-instrument manipulation: the search gap.** Hit rate with the error's one-page window disclosed, minus hit rate uncued, at the same length. Prediction: the gap varies beyond ECI.
5. **Specific prediction.** The false-alarm rate is higher for reasoning-tuned models at matched ECI.
6. **MTMM** [campbell1959convergent]. Residual correlations with FIND, FinED-Bench and ProcessBench exceed those with RULER and MRCR.
7. **Incremental validity** [sechrest1963incremental].
   - Criteria: catch rate on real documents (the FIND test split and FinED-Bench-Hard), then a field study of professionals reviewing real audit files with model assistance.
   - Test: ΔR² ≥ 0.05 over ECI plus log compute, bootstrapped.

## 12. Human baseline plan

- **A. Item validation.** Three trained checkers work untimed on each calibration core (1–4 pages).
  - A core is kept if at least 2 of 3 find the error, the ARC criterion [kamradt2025arcagi2].
  - A decoy template is revised if at least 2 of 3 flag it on the clean twin.
  - An audited key-error rate is published per release, with a target of ≤ 2%.
- **B. Human horizon.** 40 professionals (accountants, paralegals, copy editors, operations staff, QA engineers) and 40 lay adults.
  - Pay is hourly, plus a bonus per correct catch *and* per correct NONE.
  - Length follows an adaptive staircase, like an eye test.
  - Arms: 2 minutes per page (the value is frozen after a timing pre-study), plus an untimed arm up to 4 pages.
  - Outputs: human CH50, and minutes per page, which gives a secondary link to METR-style human-minutes.
- **C. Public "Be the second reader" page.** Opt-in; reported separately and never the headline.

## 13. Leaderboard, governance and attention channel

- **Board.** One CH50 per model with CI, cost per catch, date and a verified badge, plus a separate tool-track column. A doubling-time chart is published with its fit assumptions.
- **Policy** [arcprize2026policy; singh2025leaderboardillusion]:
  - a named neutral steward, with funding disclosed;
  - every frontier model added within 14 days of API availability;
  - the scored model is the shipped model;
  - one sealed run per version, with K = 2 samples per item;
  - symmetric pre-release testing, with no retractions and no private variants;
  - retirement triggers declared in advance (e.g. a family whose public–private gap exceeds 20%).
- **Seasons (quarterly).** Each adds at least 2 human-authored families and releases the oldest private family to the public practice pool. The anchor set keeps CH50 linked.
- **Distribution.** `pip install secondreader`, then `secondreader run --model provider/name`: API-only (C9), with a declared cost. Inspect and lm-eval tasks ship at launch [aisi2024inspect; lmevalMastermind].
- **Artifacts** are rendered from item plus oracle, with no LLM:
  - *miss cards*: the wrong line in red, the model's flag in blue, and the oracle sentence;
  - *release-day diff cards*: newly caught and newly missed items;
  - a *Wall of wrong lines*: public pages every frontier model missed but humans caught.

  Showcase items come only from the public pool (`virality_consumer.md` implications 9–10).

## 14. Pilot plan within C8

- **Models.** `haiku`, `sonnet`, `opus` and `fable`, run as subagents told to use no tools. Transcripts are audited, and any response that used a tool is excluded and replaced from the reserve.
- **Items.** 4 families (itinerary, stock ledger, lease schedule, run-sheet) and 20 error cores: 5 per family, balanced over G1–G4. The design is crossed: every model sees identical documents.
- **Size.** The longest document is 8 pages: about 320 lines, or roughly 5k tokens plus a 250-token instruction, within the ~8k limit.

| Block | Per model | ×4 |
|---|---|---|
| Error documents: 20 cores × 2 lengths, so each of 0.5/1/2/4/8 pages gets 8 | 40 | 160 |
| Clean twins: 4 per length | 20 | 80 |
| Retest: 3 per length, fresh call | 15 | 60 |
| Cued control: the 8 eight-page error documents, with "if present, it is within lines a–b" | 8 | 32 |
| **Planned** | **83** | **332** |
| Reserve for excluded or unparseable calls | | ≤ 48 |
| **Maximum** | | **≤ 380** |

The generator, oracle, parser, fits and bootstrap are all Python.

**Pre-registered criteria:**
1. 100% of items pass the oracle and uniqueness checks, and the null baselines behave as stated.
2. Hit rate falls with log₂ℓ and from G1 to G4, with CIs excluding 0.
3. CH50(haiku) < CH50(opus) with non-overlapping CIs. Other pairs are exploratory, and opus vs fable may not separate.
4. The best model's net catch is ≤ 0.6 at some tested length. Otherwise v1 adopts the Hard mix as its headline, and we record that the 8k window cannot bound the frontier.
5. Item-level test–retest κ ≥ 0.6.
6. The search gap is > 0 for at least 2 models.
7. At least 95% of answers parse, and retained transcripts show zero tool uses.

**Limit.** Four same-family models test the instrument, not incremental validity.

## 15. Risks

1. **g-collapse.** Likely in part. The falsifier and a product-only fallback are declared in advance.
2. **A young, crowded niche.** FIND† has a well-resourced sponsor (Kensho). The differentiation is renewal, exact generated keys, clean twins and an unbounded unit. Incumbents are invited as convergent-validity partners.
3. **Synthetic documents are cleaner than real ones.** Mitigated by practitioner templates and the real-document criterion.
4. **Tool dominance on structured families.** Reported separately; prose and rule families limit it.
5. **Page portability.** Lines are held to a fixed token band; per-family horizons are published.
6. **Long-document cost.** Adaptive placement keeps it to a few million input tokens per model [I].
7. **Decoy disputes.** Resolved by panel A.
8. **Less consumer appeal than visual arenas.** The survey finds "fun" does not drive adoption.

## 16. Closest prior work and how this differs

| Work | What it does | Difference |
|---|---|---|
| FIND† (arXiv:2512.18601) | 375 test documents, each with one expert-inserted inconsistency; median 35k tokens; gpt-5 recovered 64% and also found *pre-existing* errors | static. Second Reader's documents are verified consistent, so no natural error escapes the key; adds renewal, clean twins and a horizon |
| FinED-Bench† (arXiv:2608.12342) | 973 expert-annotated financial documents; GPT-4o F1 48.34%; falls with length | static, F1-scored, one domain |
| ContraDoc† (NAACL 2024) | human-annotated self-contradictions in long documents | static; no localisation horizon |
| FLAWS† (arXiv:2511.21843) | 713 paper–error pairs *inserted by LLMs* | no LLM-made errors here (C4) |
| BIG-Bench Mistake†, ProcessBench†, ReaLMistake† | mistake location in reasoning chains and responses | those check model reasoning; this checks documents, with a length ladder |
| NIAH, RULER, NoLiMa, Michelangelo [kamradt2023niah; hsieh2024ruler; modarressi2025nolima; vodrahalli2024michelangelo] | retrieval and latent-structure queries | no query here: checking is self-directed, and NONE can be correct |
| METR horizon [metr2025horizon] | horizon unit | borrowed, but the axis is intrinsic, so no human timing is needed |
| Consistency checks [fluri2023consistency; li2024gvconsistency] | ground-truth-free consistency | exact ground truth |
| STRAIT (sibling P2) | *executing* a rulebook; horizon in decision steps | *verifies* finished documents; specificity is half the score |

---

## Appendix A: Rejected candidates

| Candidate | Idea | Verdict |
|---|---|---|
| Babel Season | learn a WALS-grounded generated language from a grammar sketch; exact translation | Meets the constraints and is shareable. Rejected: weak product link, the MTOB copying confound [aycock2024grammarbook], and learning constructs have proved g-loaded (CL-bench 0.71) [C:offg] |
| Ask First | answer when the context determines a unique answer, otherwise name the missing variable | Meets the constraints. Rejected: "a sensible default exists" is disputable, it overlaps P1, and its unit is less legible. A possible future track |
| Onboarding Day | learn a generated tool or DSL manual, then do tasks; horizon in manual pages | Overlaps P2 and CodeUpdateArena; it is "programming in a renamed language" (the lead's renaming objection) |
| Commute Planner | earliest-arrival queries on real GTFS timetables | **Fails C10** (a routing script solves it, and the feeds are online) and the "re-skinned known task" value (shortest path) |
| Black Box | infer a hidden rule from observations | **C1 risk** (puzzle framing); **C10** (program search brute-forces it); ARC or MIR-Bench in text [yan2025mirbench] |
| Explain it to Haiku | teach a fixed student; exact post-test | **C1 risk** (teacher–listener is close to a signalling game); the student explains 35% of gain variance [educationq2025]; human gains barely separate tutors [northcutt2026studentbench] |
| Live Numbers | compute answers from fresh public data releases | **Fails C10**: a pandas one-liner solves it, and the statistics are published online |
| Crowd Verdict | Arena-style votes on which answer is right | **Fails C3**: human judgement in the headline |

## Appendix B: Sources checked this session (not in `refs/`; M)

- Tyen et al., "LLMs cannot find reasoning errors, but can correct them given the error location", Findings of ACL 2024, arXiv:2311.08516 (README of github.com/WHGTyen/BIG-Bench-Mistake).
- Zheng et al., "ProcessBench: Identifying Process Errors in Mathematical Reasoning", ACL 2025, arXiv:2412.06559 (README of github.com/QwenLM/ProcessBench).
- Kamoi et al., "Evaluating LLMs at Detecting Errors in LLM Responses" (ReaLMistake), COLM 2024, arXiv:2404.03602 (README of github.com/psunlpgroup/ReaLMistake).
- Li, Raheja and Kumar, "ContraDoc: Understanding Self-Contradictions in Documents with Large Language Models", NAACL 2024, arXiv:2311.09182 (web search).
- Lovering et al., "On Finding Inconsistencies in Documents" (FIND), arXiv:2512.18601, ACL 2026 Findings (web search).
- "Are Large Language Models Reliable Reviewers? A Benchmark for Error Detection in Financial Documents" (FinED-Bench), arXiv:2608.12342, ACL 2026 Findings (web search).
- Xi, Rao, Payan and Shah, "FLAWS: A Benchmark for Error Identification and Localization in Scientific Papers", arXiv:2511.21843 (web search).
