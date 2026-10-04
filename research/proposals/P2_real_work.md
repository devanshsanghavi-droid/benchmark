# P2 (real-work-value lens): STRAIT — Straight-Through Rulebook Adjudication In Text

*Proposal, 2026-09-29.*

**Citation conventions.**
- Keys in `[brackets]` resolve in `research/refs/*.json`.
- `[C:offg]` is the ECI-refit analysis in `notes/gap_offg_construct_evidence.md`.
- † marks works verified this session but not in `refs/` (Appendix B).
- `[I]` marks interpretation; `[computed here]` marks own arithmetic or simulation.

---

## 1. Name and thesis

**STRAIT.** A surface search found no LLM benchmark with this name; a full collision check is still needed before launch.

**Thesis: exactness at volume is the unit of deployable value.** Much paid back-office work, and much of what enterprise agent pipelines do daily, is *casework*. Someone applies an organisation's written rules, line by line, to an expense claim, benefit claim, timesheet, refund or invoice. Operations teams call a case finished with no human correction "straight-through processing" (STP) [I: industry usage]. The deployment question is therefore:

> **How large a case can the model process straight through, from a rulebook it has never seen?**

**The headline is the casework horizon (H50):** the case size, in *decision steps*, at which a model gets the whole case exactly right half the time. This follows METR's move of making the difficulty axis the unit [metr2025horizon]. The axis is open-ended, so headroom is structural.

**Philosophy: the "clerk's standard".** A clerk is judged on applying *this* organisation's rules, odd ones included, to *every* line, not on eloquence or on knowing the tax code by heart.

## 2. Construct definition

**Construct: procedural fidelity at volume.** This is the ability to execute a novel, written, internally consistent rule system over structured case data, exactly and exhaustively. In every rule system:

- (i) the rules are unseen in training;
- (ii) some provisions deliberately contradict common real-world defaults;
- (iii) provisions interact through precedence, exceptions, amendments, definitions and cross-line accumulators.

**Components**, each tagged per item and diagnosed exactly (§5):

1. rule identification;
2. precedence and exception handling;
3. state tracking;
4. **prior override** (the document beats what "usually" happens);
5. exhaustive coverage;
6. exact computation.

**What it is not:** domain knowledge (every rule is supplied), long-context retrieval (core items are under 8k tokens), arithmetic prowess (numbers are kept simple and arithmetic is measured separately), or writing.

**Pre-registered network:**

| Measure | Predicted relation with H50 | Role |
|---|---|---|
| τ²-bench pass^k [barres2025tau2], TaxCalcBench†, RuleArena†, IFBench [pyatkin2025ifbench] | High | Convergent |
| Knowledge QA (SimpleQA, GPQA) | Lower | Discriminant |
| Prior-override penalty (a sub-score) | Weak with general capability | Candidate off-g component |

## 3. Why it is not a game (C1)

STRAIT has no opponent, no win or lose, no moves, board or turns, and no sender and receiver. An item is a work artefact: a policy, a claim form and a required adjudication. It has exactly one correct output fixed by a written specification, like a tax return.

Difficulty comes from the volume and interaction of provisions, not from recreational puzzle structure or adversarial search. Nothing is played; a case is processed.

## 4. Worked example (one complete item)

This is a Travel & Expense pack item at tier T2. It was rendered from a formal specification through human-written clause templates. The gold answer and step count come from the reference engine, and a scratch re-implementation reproduced both [computed here].

**Harness instruction (fixed):**

> You are processing an expense claim for Halvorsen Freight Ltd. Apply the company's Travel and Expense Policy below exactly as written, including amendments. Where it differs from common practice, this policy governs. Do not use tools. For every line give its status (PAID, REDUCED, DENIED or PENDED) and the payable amount in US dollars to the cent. End with one JSON block in the format shown.

**HALVORSEN FREIGHT LTD. — TRAVEL AND EXPENSE POLICY (Rev. 7)**

- **1.1** "Trip" means the period from the departure date to the return date on the claim form, inclusive. The first and last travel days are the departure and return dates.
- **1.2** "Claimed amount" means the amount on the claim line, converted to US dollars under 2.3 where required.
- **2.1** A line whose expense date is more than 45 calendar days before the claim submission date is DENIED.
- **2.2** (a) A line with a claimed amount of $80.00 or more must be supported by an itemised receipt. A line lacking a required receipt is PENDED. (b) Mileage lines are exempt from 2.2(a).
- **2.3** Foreign-currency amounts are converted to US dollars at the rate printed on the line, rounded to the nearest cent, before any rule in §3 or §4 is applied.
- **3.1** Meals are reimbursed at the claimed amount, subject to a daily meal limit of $64.00 that applies to the total of all meal lines with the same expense date.
- **3.2** On the first and last travel days of a trip, the daily meal limit is 60% of the amount in 3.1.
- **3.3** Where the meal lines for one date together exceed the daily limit, the limit is allocated in the order the lines appear on the claim form. Each line receives the lesser of its eligible amount and the unallocated part of the limit.
- **3.4** Alcoholic drinks are not reimbursable. The alcohol amount shown on a meal line is deducted before 3.1–3.3 are applied.
- **4.1** Lodging is reimbursed up to $180.00 per night for the room charge. Lodging taxes shown on the line are reimbursed in full.
- **4.2** Use of a personal car is reimbursed at $0.52 per mile stated on the line, regardless of the amount the claimant entered.
- **4.3** Taxi and rideshare fares are reimbursed at the claimed amount.
- **5.1** Rules apply in this order: 2.1, then 2.3, then 2.2, then §3 or §4. A DENIED or PENDED line receives $0.00 and does not count towards any limit.
- **5.2** A line is PAID if its payable amount equals its claimed amount. It is REDUCED if the payable amount is lower, including $0.00 because a limit is used up.

**MEMO — Finance, 14 February 2026.** From 1 March 2026 the room-charge limit in 4.1 is $210.00 per night for stays in Northgate. Other locations are unchanged.

**CLAIM.** Claimant: Marta Oyelaran. Trip: Northgate, departing 3 March 2026 and returning 5 March 2026. Submitted: 10 April 2026.

| Line | Date | Category | Description | Amount | Receipt | Notes |
|---|---|---|---|---|---|---|
| L1 | 2026-03-03 | Meal | Dinner, Harbour Grill | $41.50 | Yes | Alcohol $9.00 |
| L2 | 2026-03-03 | Meal | Lunch, Station Deli | $14.20 | Yes | |
| L3 | 2026-03-03 | Lodging | Brightwater Inn, Northgate, 2 nights | $481.60 | Yes | Room $430.00; tax $51.60 |
| L4 | 2026-03-04 | Meal | Lunch, Le Petit Quai, Kingsport (Canada) | CAD 44.80 | Yes | 1 CAD = 0.7286 USD |
| L5 | 2026-03-04 | Meal | Dinner, Northgate Steakhouse | $52.00 | No | |
| L6 | 2026-03-05 | Mileage | Northgate to head office, 212 miles | $148.40 | No | |
| L7 | 2026-01-29 | Taxi | Airport taxi (January client visit) | $38.00 | Yes | |
| L8 | 2026-03-05 | Meal | Breakfast, Airport Café | $22.00 | No | |

**Output format:** `{"lines":[{"id":"L1","status":"...","payable":"0.00"}, ...]}`

**Gold:**

| Line | Status | Payable | Derivation |
|---|---|---|---|
| L1 | REDUCED | 32.50 | 41.50 − 9.00 alcohol; first-day limit 38.40 (60% of 64.00) |
| L2 | REDUCED | 5.90 | Remaining first-day limit, allocated in claim order |
| L3 | REDUCED | 471.60 | Amended limit 2 × 210 = 420.00, plus tax 51.60 |
| L4 | PAID | 32.64 | 44.80 × 0.7286 |
| L5 | REDUCED | 31.36 | 64.00 − 32.64 |
| L6 | REDUCED | 110.24 | 212 × 0.52; exempt from the receipt rule |
| L7 | DENIED | 0.00 | 71 days old |
| L8 | PAID | 22.00 | Last-day limit 38.40 |

The total payable is $706.24.

**Decision steps: 27.** Steps are rule firings in the engine trace plus one base determination per line: 8 base, 5 for 3.1, 4 for 3.3, 3 for 3.2, and 1 each for 2.1, 2.2(b), 2.3, 3.4, 4.1, the memo and 4.2. Provisions 2.2(a) and 4.3 fire on no line; they are distractors.

**Catalogued misreadings**, each giving a distinct wrong output:

| Misreading | Wrong output |
|---|---|
| Meal-time order instead of claim order (the day total is unchanged, which is why grading is line-level) | L2 PAID 14.20, L1 24.20 |
| The U.S. Federal Travel Regulation's 75% first/last-day default (to be re-verified by the pack author) | L2 PAID 14.20 |
| Missing the memo | L3 411.60 |
| Accepting the claimant's per-mile rate | L6 PAID 148.40 |
| Receipt rule applied to mileage | L6 PENDED |
| Alcohol deducted after the limit | L1 29.40 |

Provisions 3.2 and 4.2 are tagged *prior-conflict*.

## 5. Generator design (no LLM anywhere)

**Domain packs** are human-authored software. Each pack has:
- a typed case schema;
- **provision families**, each with formal antecedent and consequent code, precedence declarations, parameter ranges and a sourced *real-world default*;
- 4–8 **human-written prose templates** per family.

A practitioner and an engineer build the families from public documents: government travel regulations, public university expense policies, public health-plan benefit summaries, wage-and-hour rules and carrier rate cards. The real-world grounding is *structural*: which provisions exist and how they interact. Examples are deductible → coinsurance → out-of-pocket maximum, per-diem with first/last-day reductions, daily vs weekly overtime, and three-way-match tolerances.

The v1 packs are Travel & Expense, Benefit Claims (EOB-style), Payroll, Returns & Refunds and Freight Quotes. Accounts-Payable Match and one further pack stay private.

**Rulebook sampler.** For each item it:

1. draws 12–30 provision families, 30–40% of them distractors;
2. samples parameters;
3. flips a set share (reference: 25%) of prior-bearing parameters to counterfactual values;
4. adds definitions, cross-references, 0–2 dated amendment memos and a precedence clause;
5. renders each provision through a random template;
6. takes names from public census name-frequency lists and fictional place lists.

A static checker rejects any rulebook in which provisions have overlapping antecedents, incompatible consequents and no declared precedence.

**Case sampler.** Lines are drawn from per-category amount and date distributions, fitted to public statistics where available. A *constructive coverage* step then hits the target step count and forces the requested provision firings. From T2 up, every item has at least one non-PAID line and one binding prior-conflict provision, so "pay as claimed" scores 0.

**Reference engine.** It executes the formal specification, not the prose. Its outputs are the gold answer, the firing trace (the step count) and component tags.

**Misreading engine.** Each pack carries a human-written catalogue of plausible misreadings, such as wrong order, inclusive vs exclusive thresholds, the real-world default, and a skipped amendment. Every item is re-run under each misreading. The results serve two purposes:
- wrong model outputs are **attributed exactly**, with no judge;
- an item is rejected if any misreading reproduces the gold, because it has no diagnostic power.

**Unambiguity safeguards.** Ambiguity is the classic killer: τ³-bench corrected 27 of 50 airline tasks [sierra2026tau2changelog], and policy "loopholes" masquerade as agent errors (Cao 2026†). STRAIT uses five safeguards:

- **(a)** Every template ships with 5–10 human-adjudicated minimal cases that two practitioners must solve identically.
- **(b)** Every catalogued misreading must be excluded by explicit wording: "or more", stated orders, defined statuses.
- **(c)** Any item where at least 3 models agree on the same non-gold output is re-derived by hand.
- **(d)** Each release gets a 100-item expert audit with a published error rate (target ≤2%).
- **(e)** A template implicated in a key error is retired.

**Freshness.** Each window uses new seeds over family subsets, parameters, counterfactual flips and templates, so repeats are negligible. 30% of families and 50% of templates are private and rotate each version. LLMs never write or paraphrase items (C4, strictly).

## 6. Scoring and headline unit

**Item score (exact, binary).** The last fenced JSON block is parsed. An item passes (STP = 1) only if the line IDs match and every line's status and decimal payable equal the gold to the cent. A parse failure scores 0 and is reported separately.

**Headline: casework horizon H50, in decision steps.** For each model *m*, fit P(STP) = σ(α_m − β·log₂ s), where *s* is the item's step count and the slope β is shared across models (per-model slopes are a robustness check). Then H50_m = 2^(α_m/β).

- The 95% CI comes from a cluster bootstrap over rulebooks (2,000 resamples).
- A model that passes everything is reported as "> max", which triggers ladder extension.
- *Reading:* "Half the time, this model processes a 40-rule-application case with zero errors."
- The human study (§11) fits clerk time against steps, so H50 is *also displayed* as "≈ N clerk-minutes". This is the same score in an external unit, not a second score.

**Resolution** [computed here]. In a simulation with β = 1–1.5 and items spread over five log₂ tiers:

| Items per model | 95% range of estimated H50 |
|---|---|
| 60 | ×0.6 to ×1.5 of the true value |
| 400 (leaderboard) | ×0.85 to ×1.2 |

Paired items and adaptive tier selection near each model's H50 tighten this.

**Diagnostics, never the headline:**
- STP at the 32-step reference tier;
- H80;
- pass^3;
- line accuracy;
- dollar error ("leakage");
- per-step error;
- misreading shares;
- prior-override penalty;
- arithmetic-floor error;
- cost per item.

## 7. Difficulty knob and expected curve

**Primary knob: decision steps.** Every core prompt stays at or under about 7k tokens.

| Tier | Decision steps | Lines | Provisions |
|---|---|---|---|
| T1 | 8–15 | 3–4 | about 12 |
| T2 | 16–31 | 5–8 | about 16 |
| T3 | 32–63 | 8–14 | about 20 |
| T4 | 64–127 | 15–25 | about 25 |
| T5 | 128–255 | 30–50 | about 30 |

**Secondary knobs** are fixed for the headline and varied in diagnostic panels: distractor share, prior-conflict rate, amendments, accumulator depth, and template register.

**Full release only:** tiers T6 and above batch several claims with shared annual accumulators (32k–200k tokens).

**Expected curve.** STP should fall logistically in log₂ steps. With independent per-step errors, P ≈ (1 − e)^s, so H50 ≈ 0.69/e: 1% per-step error gives H50 ≈ 69 [computed here].

**Pre-registered pilot guesses [I]:**
- Haiku: 8–20.
- Sonnet: 20–60.
- Opus and Fable: 40–200.
- The best model scores ≤50% STP at T5.

Censoring above T5 would mean the ladder must extend before launch. Headroom comes from the open axis, not from "stump today's model" filtering.

## 8. Contamination, gaming and tool regime (C10)

**Memorisation.** Rulebooks are new each window. Counterfactual parameters make memorised real rules *harmful*: the federal 75% rule gives the wrong answer in §4, and TaxCalcBench† found models substituting bracket percentages for the provided tax tables.

**Curriculum.** Public generators become RL environments [stojanovski2025reasoninggym; pyatkin2025ifbench; primeintellect2026longcontext]. The defences:
- private families and templates;
- a **contamination index**: the public-template vs private-template gap on the same specifications (a parallel-form method, as in [zhang2024gsm1k]);
- a curriculum stress test: fine-tune an open model on public items and measure transfer to private packs.

**Shortcuts.**
- Null baselines ship with every release: pay-as-claimed, deny-all, random, and caps-only. The target is ≤2% STP.
- The answer is a vector of cent amounts, so guessing fails.
- No correctness feedback is ever returned, so search and brute force have nothing to climb.
- One pinned single-turn harness with no retries; shipped models only [singh2025leaderboardillusion].

**Tool regime.**
- **Core track (headline): no tools and no browsing.** The pilot enforces this by instruction plus a transcript audit, excluding any tool-using response. In production, no tools are declared.
- **Tool track (separate board):** an offline Python sandbox. Code helps with bookkeeping, and "policy-as-code" is legitimate work, but reading the policy correctly remains the hard part. The core-to-tool gap is reported.
- **Web lookup** cannot help: rulebooks are fictional, and real-world lookups return exactly the defaults that prior-conflict provisions contradict. This is measured through the prior-override penalty. Keys never leave the grader, which avoids BrowseComp-style key retrieval [anthropic2026browsecomp].

## 9. Real-world relevance

**The score sets a routing policy** [I]: auto-process cases below the model's H80 or H90 and send the rest to humans. A lab can state "processes 60-step claims straight through".

The packs mirror work bought at volume (claims examination, expense audit, payroll, AP matching, refunds). They also mirror daily agent work: applying the policy in the system prompt to the record in hand. CC-Gen† is motivated by the same need.

Labs headline work-shaped evaluations: the agentic share of frontier headline rows went from 23% to 76% (synthesis, [D:MCA]), and GDPval sells occupational value [openai2025gdpval]. STRAIT adds exact grading and unlimited fresh items.

**Consumer hook:** "Would you let this model do your expense report?", shareable trap stories, and a horizon-doubling chart.

## 10. Incremental validity (C7)

**Argument.** Casework errors are omission, prior substitution, accumulator state and precedence errors. These are fidelity properties shaped by post-training (self-checking, deference to context), not only by scale. Related constructs keep residual variance:

- SEAL Instruction Following: ρ = 0.638 with the leave-one-out ECI-refit (disattenuated 0.837; reliable specific share 0.36) [C:offg].
- MCP Atlas: ρ = 0.795 [C:offg].
- TaxCalcBench's table-substitution failures, RuleArena's confusion between similar rules†, and pass^k reliability gaps [yao2024tau] are all failure modes distinct from "can solve".

**Honest prior.** ARC-AGI, built on a distinctness thesis, sits at 0.95–0.97 [C:offg]. We predict a disattenuated leave-one-out ECI correlation of 0.75–0.90. The primary claim is measurement quality plus a work-anchored unit; distinctness is a falsifiable secondary claim.

**Test (full study):**

1. **Sample.** At least 60 models from at least 10 families, with GPQA and ARC-AGI-2 re-scored on the same sample. About 57 models suffice if the true r is about 0.75 [C:offg].
2. **Falsifier.** A disattenuated r ≥ 0.9 means collapse into g. The construct claim also needs split-half residual reliability ≥ 0.5.
3. **External criterion: FieldCase.** About 200 private cases on 3–4 *real public* policies (a government travel regulation, a university expense policy, a health-plan benefit summary). The cases are human-authored and double-adjudicated by certified practitioners.
   - Regression: FieldCase STP ~ ECI + log compute + H50, with a pre-registered ΔR² ≥ 0.05, bootstrapped.
   - An optional industry partner adds shadow-mode STP against QA-audited production decisions (rubric F11 = 3).
4. **MTMM check** [campbell1959convergent]. H50 correlates more with τ² and TaxCalcBench than with exact-match knowledge QA.
5. **Sub-score prediction.** The prior-override penalty has |ρ| < 0.4 with ECI and predicts the FieldCase items where real policies depart from national defaults.
6. **Prospective replication.** Predictions are frozen for models released after publication.

## 11. Human baseline

**Participants:** 30–40 practitioners (claims examiners, AP specialists, T&E auditors, payroll administrators) with at least 2 years' experience, recruited through a vetted freelance platform with 3 qualification items.

**Procedure:**
- Participants get the same text and a basic calculator; an optional spreadsheet condition mirrors the tool track.
- Each person does 15–20 items across T1–T5, timed.
- Pay is hourly plus an exactness bonus, which mirrors STP.
- Each frozen-split item gets at least 3 attempts.

**Outputs:**
- human H50, per individual and pooled;
- per-tier STP;
- the clerk-minutes mapping;
- a panel audit of items solved by no one.

**Cost:** about $5k plus bonuses (35 people × 3 h × $50/h) [computed here]. Whether careful humans beat frontier models at T4–T5 is an empirical launch result, not an assumption.

## 12. Leaderboard and governance

**Install:** `pip install strait-bench`, then `strait run --model <provider/model> --window 2026Q4`.
- Text in, text out, through any chat API; no Docker and no logits.
- Inspect and lm-eval tasks at launch (cf. [lmevalMastermind]).

**Windows:**
- A quarterly fresh window.
- A private 400-item frozen split for longitudinal comparison.
- 20% anchor items for linking [ho2025rosetta].

**Policy:**
- A named steward with disclosed funding.
- Frontier models are added within 14 days.
- Provider-default reasoning settings, with tokens and cost reported.
- Retired windows and all outputs are released under CC-BY.

**Versioning** under a permanent name:
- A new tier is added when the frontier H50 exceeds half the top tier.
- Pre-declared retirement triggers: audited key error above 2%, or a contamination index above a published bound.

**Boards and outreach:** a separate tool-track board, plus a consumer page with the horizon chart and a trap gallery.

## 13. Pilot plan (C8)

**Models under test:** haiku, sonnet, opus and fable, called as workflow subagents told not to use tools. Transcripts are audited, and tool-using responses are excluded. No auxiliary role is needed.

**Items:** two packs (T&E and Benefit Claims). Each item has its own fresh rulebook, so items are independent clusters, and the four models see identical items. Prompts are at most about 7k tokens.

**Call budget:**

| Component | Calls (×4 models) |
|---|---|
| Main ladder: 2 packs × 5 tiers × 6 items = 60 items | 240 |
| Prior-conflict twins: 12 T3 items with every prior-conflict parameter reset to its real-world default | 48 |
| Test–retest: 12 main items repeated | 48 |
| **Total** | **336** |
| Reserve for excluded calls | ≤64 (cap 400) |

**Non-model baselines** are free.

**Pre-registered analyses** (Python):

| # | Analysis | Criterion |
|---|---|---|
| P1 | Knob works | β > 0 for every model; STP monotone over tiers |
| P2 | Ordering | H50 haiku < sonnet < opus, with paired cluster-bootstrap CIs; fable vs opus exploratory |
| P3 | Headroom | Best model's T5 STP ≤ 50%; not censored |
| P4 | Reliability | Split-half H50 (Spearman–Brown); test–retest κ ≥ 0.6 |
| P5 | Prior-override penalty | McNemar test on twins |
| P6 | Null baselines | ≤ 2% STP |
| P7 | Key audit | Consensus triage; 0 errors in 60 items bounds the rate at about 5% |
| P8 | Format | Parse failures < 2% |
| P9 | Attribution | Share of wrong lines explained by catalogued misreadings |
| P10 | Cost | Tokens per tier |

**Limit.** Four same-family models cannot test incremental validity; the pilot tests the *instrument*. With 60 items, H50 resolves to about ×0.6–×1.5, so the pilot may not separate opus from fable [computed here].

## 14. Risks

1. **g-collapse (likely).** Value then rests on exactness, freshness and the work unit.
2. **Prose–spec ambiguity**, the τ-bench failure mode. Handled by the §5 safeguards and a published residual error rate.
3. **Arithmetic confound.** Simple numbers, an arithmetic-floor control and the tool track.
4. **Ecological gap.** Synthetic rulebooks are cleaner than real ones; FieldCase measures transfer.
5. **Curriculum Goodhart.** Private packs, the contamination index and rotation.
6. **Step count mis-specifies difficulty.** Fall back to empirical IRT difficulty linked to steps.
7. **Pre-emption by adjacent work** (§15).
8. **"Expenses are boring."** Trap stories.
9. **Reasoning-budget confound.** A cost-matched view.
10. **Maintenance cliff.** Steward and cadence fixed before launch.

## 15. Closest prior work

| Work | What it does | How STRAIT differs |
|---|---|---|
| **RuleArena**† (ACL 2025; arXiv:2412.08972) | 95 real rules, 816 problems (airline baggage, NBA, tax), 3 levels; o1-preview below 50% on the hardest | Real public rules make it memorisable and fixed. STRAIT uses novel counterfactual rulebooks, fresh windows, an open-ended knob, a horizon unit and a human baseline |
| **TaxCalcBench**† (arXiv:2507.16126) | Engine-checked tax returns; best model 32% (2025) | One domain, real code, static. STRAIT keeps the strict whole-case grading |
| **SARA**† (arXiv:2005.05257) and Blair-Stanek et al.† (ICAIL 2023) | 376 hand-built statute cases; synthetic statutes exposed GPT-3 | Static. STRAIT turns the synthetic-statute insight into a renewable generator |
| **τ/τ²/τ³-bench** [yao2024tau; barres2025tau2] | Policy, tools and a simulated user | Small fixed sets, LLM user simulator, heavy label repair |
| **CC-Gen**† (arXiv:2510.11588; ACL 2026) | Controllable policy-complexity generator for policy *internalisation* | Training-oriented; mechanics unverified by us. STRAIT is judge-free, human-templated and leaderboard-anchored |
| **ClaimPilot**† (2026) | 150 synthetic veterinary claims from a policy grammar | A system paper's small single-domain set |
| **KOR-Bench** [ma2024korbench], **CodeUpdateArena** [liu2024codeupdatearena], **IFBench** | Novel rules and specifications, or verifiable constraints | Static, puzzle-like, or constraints on the output only |
| **METR horizon**, **GDPval** | Horizon unit (METR); occupational value (GDPval) | Borrowed: the unit and the value framing. STRAIT adds exact grading and unlimited renewal |

**Constraint check:**

| Constraint | How STRAIT meets it |
|---|---|
| C1 | Casework, not play |
| C2 | Text-only |
| C3 | Exact engine keys |
| C4 | Human templates plus sampling; no LLM text |
| C5 | Fresh seeds; open-ended step knob |
| C6 | H50, with construct stated |
| C7 | §10 |
| C8 | 336 calls |
| C9 | Pip package plus one command |
| C10 | §8 |

---

## Appendix A: Rejected candidates

1. **Ledger reconciliation** (bank vs ledger vs invoices; output the discrepancies).
   - *Assessment:* exact, but it reduces to fuzzy matching plus subset-sum (brute-forceable by code, F4) or, without tools, long-context lookup (the fast-saturating NIAH family).
   - *Outcome:* folded into STRAIT as the AP Match pack.
2. **Handoff fidelity** (the model writes a handoff note; a fixed worker model answers exact questions from it).
   - *Assessment:* a real multi-agent need.
   - *Rejected:* the sender–receiver structure is a signalling game in all but name (C1). The headline also depends on an LLM worker's reading, and the student effect was 35% of gain variance in EducationQ [educationq2025] (C3 spirit).
3. **Spec-to-transform ETL.**
   - *Assessment:* exact, but it collapses toward coding benchmarks, and serialisation errors dominate the signal.
   - *Outcome:* kept as a possible future pack.
4. **Live-filings extraction** (fresh 10-Q text; XBRL keys).
   - *Rejected:* answers are public on EDGAR within minutes (C10), filings exceed 8k tokens (C8), XBRL tagging errors corrupt keys, and there is little headroom.
5. **Incident root-cause from simulated logs.**
   - *Rejected:* one-of-N answers give a high chance floor, grep-style shortcuts work, and simulated logs lack realism (F4, F11).
6. **Calendar and travel constraint planning.**
   - *Rejected:* puzzle-like (C1 risk), brute-forceable (C10) and crowded.

## Appendix B: Sources verified in this session (not in `refs/`)

- **RuleArena.** Zhou, Hua, Pan, Cheng, Wu, Yu, Wang. ACL 2025, arXiv:2412.08972. Verified via the repository BibTeX (github.com/SkyRiver-2000/RuleArena) and search abstracts.
- **TaxCalcBench.** Column Tax. arXiv:2507.16126. Verified via github.com/column-tax/tax-calc-bench and search. Best result 32.35% strict (Gemini 2.5 Pro); table-substitution failures.
- **SARA.** Holzenberger, Blair-Stanek, Van Durme. arXiv:2005.05257.
- **Can GPT-3 Perform Statutory Reasoning?** Blair-Stanek, Holzenberger, Van Durme. ICAIL 2023, arXiv:2302.06100.
- **CC-Gen.** *Analyzing and Internalizing Complex Policy Documents for LLM Agents.* arXiv:2510.11588; ACL 2026 long paper 767. Verified via search; generator internals not read.
- **ClaimPilot.** Future Internet 18(9):465 (2026). Search snippet only (M).
- **Policy Loopholes.** Cao, H. arXiv:2609.14400. Search abstract (M).
