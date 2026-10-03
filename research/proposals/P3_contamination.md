# P3 (longevity lens): WEDGE. Does this change change anything? Show me the case.

Draft, 2026-09-29.

**Conventions.**
- `[keys]` resolve in `research/refs/*.json`.
- `[C:offg]` refers to `notes/gap_offg_construct_evidence.md`; `[D:MCA]` refers to `notes/model_cards_adoption.md`.
- † marks a source verified this session that is not in `refs/` (Appendix B).
- `[I]` marks interpretation, `[computed here]` marks my own computation, and *(hypothesis)* marks a prediction.

---

## 1. Name and thesis

**WEDGE** stands for *Witnesses for Edits, Divergence Graded by Execution*. A wedge is one concrete input that splits two versions of a rule system apart.

**Name check.** A GitHub search for "wedge llm benchmark" returned no results; the only near-collision is an unrelated 0-star firmware repository. I dropped three other names after checking: "DiffWit" (already a diff tool), "FaultLine" (taken by ten LLM-tooling repositories) and "Exhibit A" (a code-evidence engine).

**Thesis.** Benchmarks die of their answer keys:
- keys leak into training data: GPT-4o scores 88.0% on MMLU but 73.4% on the closed MMLU-CF [zhao2025mmlucf];
- keys are decrypted at run time: Claude Opus 4.6 decrypted BrowseComp's key [anthropic2026browsecomp];
- keys are wrong: 42% of FrontierMath items had errors, and at least 59.4% of audited hard SWE-bench Verified items were flawed [epoch2026frontiermathv2; openai2026noVerified];
- keys cap at 100%: static sets stay in headline tables for only 7–30 months [D:MCA].

WEDGE has **no answer key**. Each item is a fresh edit to a real-world kind of rule artefact: an access policy, a dependency constraint, a checkout promotion or a function. The model answers the question that reviewers of code, security and policy ask every day: *does this change change anything?* It answers either by giving **one concrete case** on which the two versions disagree, with both outcomes, or by answering NONE. A program checks the case by running both versions. The answer exists nowhere until the model writes it, so it cannot be memorised, looked up or mis-keyed.

**Philosophy.** ARC asks "can it learn?" and Arena asks "do people prefer it?". WEDGE asks "**can it show you exactly where a change bites?**" Evidence, not matching strings.

**Headline: the wedge horizon, W50.** W50 is the number of conditions that must hold at once for a change to show, at which the model finds a valid wedge half the time. This axis is computed from each item's structure, not from how models perform on it. It is open-ended, so it can be extended rather than reset, as METR's time horizon is [metr2025horizon].

---

## 2. Construct definition

**Construct: change-impact reasoning.** The model is given two versions, A and B, of a deterministic rule system and a declared finite input space. It must decide whether A and B behave differently. If they do, it must construct an input that exposes the difference and state the outcome under each version.

**Components** (adapted from mutation testing's reachability–infection–propagation account; background knowledge, not re-verified):
1. **Reach:** the input makes the edited clause matter.
2. **Infect:** the clause's local result changes.
3. **Propagate:** the difference survives the rules that could mask it.
4. **Certify:** both outcomes are stated correctly.
5. **Recognise equivalence:** the model answers NONE when nothing changes.

**What it is not:**
- *domain knowledge*: all rules are supplied, and families based on real languages get a reference card excerpted from the governing specification;
- *forward execution*: measured separately with forward twins (§6);
- *enumeration*: the headline regime is tool-free, and items must meet a rarity floor;
- *writing quality*: only the final line is scored.

**Pre-registered network *(hypotheses)*:**

| Measure | Predicted relation with W50 |
|---|---|
| SWT-bench fail-to-pass†; TestGenEval mutation score† | High: convergent evidence from a different format (agentic, repository-scale) |
| Forward-twin accuracy on the same items | High, but below 1 after disattenuation |
| ECI [ho2025rosetta] | High (0.8–0.9) |
| Knowledge QA (SimpleQA, GPQA) | Lower |
| False-NONE and false-wedge rates vs calibration error | Positive. This is the candidate off-g component [C:offg]. |

---

## 3. Why it is not a game (C1)

WEDGE has no opponent, no win or lose, no moves, board, turns or environment, and no sender or receiver. An item is a change-review ticket with one criterion: do the two versions disagree on the case the model wrote?

The task is ordinary professional work:
- AWS exposes it as an API that "checks whether new access is allowed for an updated policy when compared to the existing policy"†;
- SWT-bench poses its code version as a test that "fails in the original state … and passes after a patch"†.

Nothing is played. A change is reviewed.

---

## 4. Worked example: one complete item

**Item `ACCESS-d7-0042`**: family ACCESS; tier d = 7; edit operator *scope narrowing of a deny statement*; rendered from human-written statement templates; about 650 tokens.

> **Change review: access policy for the Northwind Records document store.**
>
> How decisions are made: a request is ALLOWED only if at least one ALLOW rule matches it and no DENY rule matches it. Otherwise it is DENIED. Rule order does not matter.
>
> **Version A (current)**
> A1 ALLOW finance-team employees and managers to read or edit files in *ledgers* or *forecasts*.
> A2 ALLOW managers (any team) to share files in *forecasts*, when on the office or VPN network.
> A3 ALLOW audit-team members (any role) to read files in any folder for years 2024 and 2025.
> D1 DENY edit and delete from the home network.
> D2 DENY contractors any action on *payroll* or *ledgers*.
> D3 DENY any action other than read on files for 2024 or earlier.
> D4 DENY any request made before 07:00 or at or after 20:00, unless the user signed in with MFA.
> D5 DENY contractors any request not made from the office network.
>
> **Version B (proposed)** is identical to Version A except:
> D2 DENY contractors any action on *payroll*.
>
> **Request space.** A request has exactly these fields: team ∈ {finance, engineering, sales, audit}; role ∈ {employee, manager, contractor}; action ∈ {read, edit, delete, share}; folder ∈ {ledgers, forecasts, payroll, archive}; year ∈ {2023, 2024, 2025, 2026}; network ∈ {office, vpn, home}; hour ∈ {0,…,23} (whole hours, local time); mfa ∈ {yes, no}.
>
> **Task.** Does Version B decide any request in the request space differently from Version A? If so, give ONE such request and the decision under each version. If no request is decided differently, answer NONE. Do not use tools. End with exactly one line in one of these forms:
> `WEDGE {"team": …, "role": …, "action": …, "folder": …, "year": …, "network": …, "hour": …, "mfa": …} A=ALLOW|DENY B=ALLOW|DENY`
> `WEDGE NONE`

**A correct answer:**

`WEDGE {"team": "audit", "role": "contractor", "action": "read", "folder": "ledgers", "year": 2025, "network": "office", "hour": 10, "mfa": "no"} A=DENY B=ALLOW`

**Why the item is deep.** The edit looks as if it lets contractors work on ledgers. It does nothing for finance contractors, because A1 covers only employees and managers. Its only effect is to open closed-year ledgers to *audit* contractors, and only when they:
- read (A3),
- files from 2024 or 2025 (A3),
- from the office (D5),
- during business hours or with MFA (D4).

Each tempting answer is killed by exactly one rule:

| Tempting answer | Killed by |
|---|---|
| Finance contractor reading ledgers | A1 |
| Audit contractor on 2026 files | A3 |
| Request over VPN | D5 |
| 21:00 without MFA | D4 |

**Generator metadata [computed here]:**

| Quantity | Value |
|---|---|
| Size of request space | 110,592 |
| Requests decided differently | 74 (all DENY→ALLOW) |
| Rarity | 1 in 1,494 |
| Depth | 7: the fewest fields that must be pinned so that every completion is a wedge |
| Minimal cubes | 28 |
| Oracle agreement | Two independently written evaluators agree on all 110,592 requests |
| Uniform random guess | 0.07% |
| Edit-anchored guess (contractor and ledgers; other fields random) | 0.8% |
| "Permissive defaults" heuristic (read, office, MFA, current year, any team) | 0% |

**NONE variant.** If A3 is limited to employees and managers in both versions, the same edit changes nothing. Enumeration certifies that variant as a NONE item [computed here].

---

## 5. Generator design

Each family is a real-world *kind* of rule artefact with deterministic semantics. Public families ship a development generator. Private families rotate and are released only when retired.

| Family (v1) | Real-world grounding | Two independent oracles |
|---|---|---|
| ACCESS (security) | Deny-overrides / default-deny attribute policies, as in cloud IAM. Statement and edit catalogues are distilled by people from public policy examples. | Two engines |
| VERSIONS (developers) | PEP 440 specifiers plus environment markers. Base lines are sampled from real `requires_dist` metadata. | `packaging` (the implementation pip uses) + an own subset implementation |
| CHECKOUT (consumers) | Real storefront promotion types: percentage, threshold shipping, member pricing, exclusions, stacking order | Two engines + an audit of the rendered text |
| IGNORE (developers) | Real `.gitignore` files | `git check-ignore` + `pathspec` |
| CODE (developers) | Permissively licensed human-written functions + a mutation-operator catalogue | CPython on a declared finite domain |
| Private pool | Calendar recurrence (RFC 5545), shop opening hours (OSM syntax), first-match firewall rules, cron, SQL `WHERE`, shipping-rate tables | Two per family |

**Pipeline.** No LLM is used anywhere (C4).
1. **Sample a base artefact.** It comes from a real corpus, or from a human-authored template catalogue fitted to real corpora.
2. **Apply edit operators.** They are drawn from a human-written catalogue of real change types: threshold shifts, scope widening or narrowing, exceptions, precedence swaps, boundary and rounding changes, first-match reordering, and behaviour-preserving refactors.
3. **Check the oracles.** Enumerate the declared space under both oracles. Discard the item on any disagreement.
4. **Measure the item.** Compute:
   - the difference region Δ;
   - the depth *d*: the minimal number of pinned fields such that every completion lies in Δ;
   - the rarity ρ = |Δ| / |space|;
   - the success rate of the heuristic suite.
5. **Accept or reject.** Accept only if:
   - *d* hits the target tier;
   - ρ ≤ 10⁻² for d ≥ 3;
   - the heuristic suite succeeds ≤ 5% of the time for d ≥ 4;
   - the prompt fits the token budget.

   Deep tiers are reached by *planting*: the edit is placed behind guards and masks. Items are re-tiered by their measured depth.
6. **Add NONE items.** About 20% of items are NONE items: masked edits or refactors, certified by enumeration.
7. **Render deterministically** from human-written templates.

**Real-diff track.** Real before/after pairs are drawn from public version histories committed after the window opens: requirement lines, ignore files, infrastructure-as-code policies. No generator produces them, and they are tiered after the fact.

**Freshness and cost.** Every window uses new private seeds. For the worked example, both oracles and the depth search ran in under a minute [computed here]. Larger spaces use decision diagrams or SAT counting.

---

## 6. Scoring and the headline unit

**Item success** requires all four of:
1. exactly one parsable `WEDGE` line;
2. the request lies in the declared space;
3. oracle_A(w) ≠ oracle_B(w);
4. both stated outcomes are correct.

On a NONE item, success means answering `WEDGE NONE`. Answering NONE on an item that does differ is a failure. No stored answer is ever consulted.

**Headline: W50 under the tool-free regime T0.** For each model, fit a logistic regression of success on *d* with equally weighted family effects. W50 is the *d* at which fitted success is 0.5, with a 95% cluster-bootstrap CI over calls and base artefacts.

**Unit: conditions.** A W50 of 5.2 reads: *"When a change only shows up if five things are true at once, the model finds such a case half the time."* For consumer audiences, each tier also carries a rarity gloss ("about 1 case in N").

**Diagnostics** (never in the headline):
- bare validity, with outcomes not required;
- forward-twin horizon F50 (same items; a request is given and both outcomes must be stated);
- NONE accuracy and false-NONE rate;
- per-family W50;
- tool-track W50-T1;
- dollar cost.

**Precision [computed here].** Simulation assumptions: slope −0.9 logits per condition; item SD 0.8; call SD 0.5. Under these, 1,200 items per model give W50 ± 0.27 conditions, and 150–170 pilot items give ± 0.6–0.8.

---

## 7. Difficulty knob and expected score curve

**Primary knob: depth *d*.** These secondary knobs vary independently:
- length (distractor statements);
- number of masks;
- breadth of the input space;
- edit multiplicity, including edits that cancel each other;
- share of NONE items.

v1 declares tiers d = 1–16.

**Expected curve *(hypothesis)*:** a logistic decline in *d*. Success should be near ceiling at d = 1–2, where the edited clause alone decides, and frontier success should be below 30% at the top v1 tier. An explanatory item-response model, from the linear-logistic-test family, checks that *d* rather than length drives difficulty.

**Extension rule.** When any model's W50 reaches the top tier minus 3, the next version adds deeper tiers under the same name and unit. MRCR survived this way; fixed configurations such as NIAH died in months [openai2025gpt52; kamradt2023niah].

Because depth is a property of the item, the scale does not shift as the model population changes, which answers the population-dependence critique of factor scales [zhou2025generalscales]. Generator-specific training could still flatten the curve. Frozen anchors watch for this (§13).

---

## 8. Contamination and gaming defences (the lens)

| Fast killer | Evidence | WEDGE mechanism | Test shipped each window |
|---|---|---|---|
| Saturation in months | Hardest 2025 sets reached near ceiling in 13–18 months [dekoninck2026beyond; epoch2026tier4saturated]; NIAH saturated in about 3 months [kamradt2023niah] | Open-ended *d*; pre-declared tiers; extension rule | Headroom report |
| Training-time contamination | Drops of up to 8% on GSM1k [zhang2024gsm1k]; a single replica lowers loss [schaeffer2026generative] | Fresh private seeds; no key to memorise; items published only after the window closes | Dev-vs-live parallel-form gap ≤ 0.3 conditions |
| Run-time lookup or decryption | BrowseComp key decrypted [anthropic2026browsecomp]; 63% of one model's successes retrieved known fixes [jain2026cursorRewardHacking] | **Keyless**: the package ships verifiers, not answers; each rule system is invented per item | Web-enabled control run (expect no gain) |
| Generator becomes an RL curriculum | Reasoning Gym is aimed at RL [stojanovski2025reasoninggym]; six evaluations were packaged as RL tasksets [primeintellect2026longcontext]; IFBench's hold-out bought about a year [pyatkin2025ifbench] | Dev generators for public families only; ≥40% of items from private families that rotate; real-diff track | **Contamination indices**: CI_gen = W50(public) − W50(private); CI_real = W50(generated) − W50(real-diff); flag > 1.0. One fine-tune on the public generator per version, with its transfer reported. |
| Label noise | HLE: 641 of 2,500 items certified correct [zhai2026hleverified]; MRCR had about 5% wrong ground truth [openai2025gpt52] | Nothing is keyed; dual oracles; exhaustive checks; the deployed implementation (git, `packaging`, CPython) is normative | Oracle-disagreement log; human solvability audit of 100 items per window, ≤ 1% ambiguous |
| Shortcuts and brute force | Mastermind brute-forceable [golde2025mastermindeval]; do-nothing agent scores 38% on τ-bench [zhu2025abc] | Heuristic floors; acceptance filter; rarity floor; one answer line | Published floors: random, edit-anchored, permissive defaults, boundary values, always-NONE |
| Leaderboard gaming | 27 private Llama 4 variants tested [singh2025leaderboardillusion] | One scored run per shipped model; live seeds never exposed | Written policy (§13) |
| Harness noise | Harness moved ARC-AGI-3 by 36 points [kamradt2026astra] | One text turn, no environment | Two human-written paraphrases |

**Goodhart alignment [I].** Training on WEDGE-style items trains edge-case search over real rule systems, which buyers want. If that training does not transfer, the indices expose it.

---

## 9. Tool regime (C10)

- **T0 (headline): sealed and tool-free.**
  - One prompt, one response; no tools, code or web.
  - The steward calls APIs with tools disabled.
  - In the pilot, transcripts are audited, and any response that used a tool is excluded.
- **T1 (reported separately): stdlib-only Python sandbox.**
  - 10 CPU-minutes, no network, and the family libraries removed.
  - Items come from spaces ≥ 2⁴⁰, so enumeration fails. T1 deliberately measures formalisation plus solver-writing.
  - Two baselines are published: a formalise-and-enumerate agent that uses the true oracle (the ceiling), and random fuzzing at budgets of 10³–10⁶.
- **Web:** never scored. A control run tests that nothing can be found.

---

## 10. Real-world and product relevance

"Will this change break or open anything?" is a daily decision in:
- code review and regression testing, where mutant-killing tests are the metric in TestGenEval†;
- cloud security, where AWS's `CheckNoNewAccess` makes exactly this judgement†;
- dependency upgrades;
- pricing and promotion QA;
- consumers asking "does this terms, price or opening-hours update affect me?"

In all of these, one concrete counterexample is the unit of work: a bug report, a test, a legal hypothetical. Each window's hardest solved item becomes a shareable "wedge card": the change, the case and a one-line story, as in §4.

---

## 11. Incremental validity: argument and test (C7)

**Honest prior.** Performance after reasoning is usually g-loaded: ARC correlates 0.95–0.97 with the ECI refit, and CL-bench 0.71 [C:offg]. WEDGE's main contribution is measurement quality. Distinctness is a secondary, falsifiable claim.

**Why a residual is plausible *(hypotheses)*:**
1. **Wedge-writing inverts execution.** Forward and reverse competence already come apart: the reversal curse [berglund2023reversal], and GPT-4's 76% generator-validator consistency [li2024gvconsistency]. Post-training rewards mostly forward-verifiable outputs.
2. **False-NONE and false-wedge rates are over-claiming propensities.** They sit next to calibration error and honesty, the best-evidenced off-g candidates [C:offg; ren2024safetywashing].

**Test.**
- **Sample:** 60–100 models from ≥ 10 families, spanning ECI about 120–165, with family as a random effect [C:offg]. GPQA Diamond and ARC-AGI-2 are re-scored on the same sample as yardsticks.
- **Falsifier:** the construct claim is dropped if the disattenuated leave-one-out ECI correlation is ≥ 0.9, or if the split-half reliability of the ECI residual is < 0.5.
- **Incremental validity** [sechrest1963incremental; hunsley2003incremental]: ΔR² ≥ 0.05 over ECI plus log compute, when predicting SWT-bench fail-to-pass† and TestGenEval mutation score†. Both are different-format criteria.
- **Multitrait-multimethod (MTMM)** [campbell1959convergent; desai2026whatbenchmarks]:
  - traits: witness and forward;
  - methods: natural-language families (ACCESS, CHECKOUT) and formal-language families (VERSIONS, IGNORE, CODE);
  - prediction: corr(W_NL, W_formal) > corr(W_NL, F_NL).
- **Stability:** a time split by release date.

If the falsifier fires, WEDGE is reported as a renewable, contamination-proof g-measure presented as change review [I].

---

## 12. Human baseline plan

**Panels:**
- 60 general adults (CHECKOUT, ACCESS);
- 40 professional developers (VERSIONS, IGNORE, CODE);
- 10 security or QA professionals as an expert anchor.

**Protocol.** Each person attempts 30 items across d = 2–12, without tools (paper allowed), at up to 12 minutes per item. Pay is hourly plus a bonus for answers the oracle verifies.

**Reported:**
- individual W50 (median and IQR);
- the panel criterion: the highest tier at which each item is solved by at least 2 of 3 people [kamradt2025arcagi2; legris2024harc];
- time per tier, which gives an optional human-minutes gloss;
- NONE accuracy.

Definitions are frozen before launch [wei2025humanbaselines]. Estimated cost: 110 people × 3 h × $40 ≈ $13k.

---

## 13. Leaderboard and governance

- **Steward:** a neutral academic or non-profit body with disclosed funding and a written policy, modelled on ARC Prize Verified [arcprize2026policy].
  - Every frontier model is added within 14 days.
  - The scored model is the shipped model, with one run per version.
- **Windows:** quarterly.
  - Each window has ≥ 1,200 T0 items per model: 60% from public families, 40% from private families, plus the real-diff track.
  - Results are published as rank bands with multiplicity control [kotawala2026resolution].
  - Cost per run is disclosed.
- **Linking:** 300 frozen anchor items, never released, are re-run each window on three pinned open-weight models. Linking error must stay ≤ 0.3 conditions [habba2026growingpains].
- **Openness:**
  - the harness and verifiers (Apache-2.0) and the dev generators are public;
  - retired windows' items and all model outputs are released under CC-BY;
  - a private family's generator is released when the family retires, after at least two windows.
- **Install:** `pip install wedge-bench`, then `wedge run --model provider:model --window dev`.
  - The oracles are pure Python; the git check for IGNORE is optional.
  - Inspect and lm-eval adapters ship at launch [gao2024harness].
- **Retirement triggers:** a family is retired if its contamination index exceeds 1.0 for two or more frontier models, or if a shortcut above the published floors is found. Versions are extended under the §7 rule.

---

## 14. Pilot plan (fits C8)

**Families and oracles:**
- ACCESS: two engines;
- VERSIONS: `packaging` 24.0 (present in the sandbox) plus an own subset implementation;
- CHECKOUT: two engines.

**Design.** Tiers d ∈ {2, 3, 4, 5, 6, 8, 10, 12}. The design is paired: all four models get identical items.
- Per model: 144 items that differ (3 families × 8 tiers × 6) plus 24 NONE items.
- Items are packed three per call, all unrelated, each answered on its own `WEDGE[id]` line.
- Every prompt is ≤ 8k tokens. Items at d ≥ 10 are packed two per call if needed.

| Block | Calls per model | Total (haiku, sonnet, opus, fable) |
|---|---|---|
| Main items (168; 3 per call) | 56 | 224 |
| Forward twins (45 items; 5 per call) | 9 | 36 |
| Test–retest (6 calls re-issued verbatim) | 6 | 24 |
| Unpacked check (6 items alone) | 6 | 24 |
| **Planned total** | **77** | **308** |
| Reserve (tool-flagged or truncated calls) | ≤ 23 | ≤ 92 (hard cap 400) |

Every call instructs the model not to use tools, and flagged responses are excluded. No auxiliary model roles are needed. All scoring and baselines run in Python.

**Go/no-go criteria (pre-registered):**
1. 100% dual-oracle agreement and a 100% reference solver; every NONE item certified.
2. A negative slope in *d* with a CI that excludes 0, for at least 3 of the 4 models.
3. Headroom: the best model scores ≤ 30% at d = 12, with W50 at least 2 conditions below 12; the weakest model scores ≥ 50% at d = 2.
4. W50 CI half-width ≤ 1.0 condition.
5. The heuristic suite scores ≤ 5% on items with d ≥ 4.
6. Parse failures ≤ 3%; tool exclusions ≤ 5%.

**Exploratory:**
- the gap between witness and forward twins *(hypothesis: witness < forward for all four models)*;
- false-NONE vs false-wedge rates;
- packing and retest effects;
- family × model interaction.

With four models, the pilot cannot test C7. It tests feasibility, reliability, headroom and the unit.

---

## 15. Risks

1. **g-collapse** is likely (§11). Mitigation: a measurement-quality framing and a pre-registered falsifier.
2. **Depth may not drive difficulty.** The explanatory item-response check tests this. The fallback is an IRT theta anchored on depth.
3. **Knowledge confound** in real-language families, such as PEP 440's pre-release rules. Mitigations: reference cards, a card ablation and invented-semantics families.
4. **Rendering ambiguity** in natural-language families. Mitigations: two-person template review and the solvability audit.
5. **The acceptance filter makes items adversarial to fixed heuristics.** This is declared, like MMMU-Pro's text-only filter [yue2025mmmupro], and the rejection rate is reported.
6. **Hidden server-side tools** weaken T0. Mitigations: provider attestation and latency or token anomaly flags.
7. **Real-diff items may be shallow.** They are re-tiered after the fact and down-weighted if narrow.
8. **Consumer appeal may be niche.** Mitigations: wedge cards, and the CHECKOUT and opening-hours families.
9. **Steward load** of about one new private family per quarter. The oracle-plus-template design keeps each family to days of work.

---

## 16. Closest prior work, and how WEDGE differs

| Work | What it shares with WEDGE | How WEDGE differs |
|---|---|---|
| **CRUXEval**† | Input prediction graded by execution (a witness format) | CRUXEval has 800 functions *generated by Code Llama 34B*, one version, a static set and no knob. WEDGE is differential, human-grounded, fresh and depth-scaled. |
| **SWT-bench**† | A test that distinguishes two code versions | SWT-bench is static, repository-scale, agentic and Docker-bound. WEDGE is compact, text-only and tool-free, with a knob. |
| **TestGenEval**† | Mutation score | TestGenEval is static: 1,210 file pairs from 11 repositories. |
| **Reasoning Gym, NPPC** [stojanovski2025reasoninggym; nppc2025] | Generator plus verifier | Their generators target algorithmic puzzle families and are public, aimed at RL. WEDGE uses real-world rule artefacts, private rotation and a measured capture index. |
| **BrowseComp** [wei2025browsecomp] | Hard to find, easy to verify | BrowseComp stores a decryptable key. WEDGE stores none. |
| **Counterfactual tasks, CodeUpdateArena, KOR-Bench** [wu2023reasoningreciting; liu2024codeupdatearena; ma2024korbench] | Altered rules | They evaluate forward, on fixed sets. |
| **Boardwalk, Code World Models** [becker2025boardwalk; lehrach2025cwm] | Inspired WEDGE's differential oracles | Neither is a change-impact benchmark. |
| **STRAIT (P2)** | Rule-based items; shared generator infrastructure is possible | STRAIT is forward adjudication; WEDGE is its inverse. P2 items can serve as WEDGE forward twins. |

---

## Appendix A. Candidates brainstormed through the longevity lens

1. **WEDGE (chosen).** It is keyless, has an open-ended structural unit, and measures curriculum capture.
2. **Day-Zero Docs.** Predict the behaviour of real packages released after the model's cutoff, reading only their docs.
   - *Rejected, on C10 and label noise.* With tools, installing the package solves the item.
   - Sealed, the docs underdetermine behaviour, so every item needs human vetting.
   - Many 2026 docs are LLM-written, which comes close to C4's echo chamber.
3. **Live forecasting of real data streams.**
   - *Rejected on C8*: nothing resolves inside the pilot.
   - Other problems: the niche is occupied [karger2025forecastbench], and retrieval confounds scores (C10).
4. **Teach-back to a fixed worker.**
   - *Rejected on longevity*: a closed worker model gets deprecated, and headroom is capped by what the worker can do.
   - The student accounts for about 35% of gain variance [educationq2025].
   - In the pilot, Claude would be teaching Claude.
5. **Black-box next-word prediction on fresh text.**
   - *Rejected*: the text is online once published (C10), and the task is knowledge-loaded and heavily g-loaded.
   - "Bits per word" is not a legible unit, and a guessing framing drifts toward C1.
6. **Hidden-rule identification from input–output traces.**
   - *Rejected on C1 and C10*: it is Mastermind-style code-breaking, the lead's own critique of MastermindEval [golde2025mastermindeval], and hypothesis enumeration brute-forces it.
7. **Novel formal-language learning with private families.**
   - No hard violation, but *not chosen*: it is keyed, so a leaked generator yields the answers.
   - It carries the example-copying confound [aycock2024grammarbook], and sibling proposals likely cover it.
   - It is folded into WEDGE as the invented-semantics families.

## Appendix B. Sources verified this session, not in `refs/`

- **gu2024cruxeval**: Gu, Rozière, Leather, Solar-Lezama, Synnaeve, Wang. *CRUXEval: A Benchmark for Code Reasoning, Understanding and Execution.* arXiv:2401.03065. The README states that the 800 functions were generated with Code Llama 34B, and that output prediction and input prediction are scored by execution. https://github.com/facebookresearch/cruxeval
- **mundler2024swtbench**: Mündler, Müller, He, Vechev. *SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents.* NeurIPS 2024; arXiv:2406.12952. https://github.com/logic-star-ai/swt-bench
- **TestGenEval** (repository): 1,210 code–test file pairs from 11 repositories, with mutation score as a metric. https://github.com/facebookresearch/testgeneval
- **AWS IAM Access Analyzer `CheckNoNewAccess`** (botocore service model): "Checks whether new access is allowed for an updated policy when compared to the existing policy." https://raw.githubusercontent.com/boto/botocore/develop/botocore/data/accessanalyzer/2019-11-01/service-2.json
