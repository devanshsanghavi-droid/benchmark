# Central synthesis: why benchmarks succeed or fail, and what a new non-game method must do

Compiled 2026-09-29 from the four cluster briefs (`briefs/A`–`D`), the four gap dossiers (`notes/gap_*.md`) and, for lookups, the underlying dossiers in `notes/`. Where a dossier carries "[corrected by fact-check]" or a verification log, the corrected version is used.

**Citation conventions.**
- `[key]` resolves in `research/refs/*.json`. Several works have more than one key across files (for example `akhtar2026plateau` = `akhtar2026saturation`; `openai2026noVerified` = `openai2026swebvretire` = `openai2026swebv`); one is used per sentence.
- `[D:MCA]` is a count derived in `notes/model_cards_adoption.md` §A: headline results tables of 34 model releases from 7 developers, Dec 2024–Sep 2026. Counts are exact for that sample only.
- `[C:offg]` is a correlation computed in `notes/gap_offg_construct_evidence.md` by refitting Epoch's ECI code on a mirror of Epoch's data [eciBayesian2026; epoch2026ecipublic]. It is not Epoch's published ECI.
- `(M)` marks a claim resting on one mirror or a secondary source; `(L)` a weak or unverified one. `[I]` marks this synthesis's interpretation; `[computed here]` marks arithmetic done in this document.

---

## Executive summary

1. **Most benchmarks fail, and the ecosystem around a benchmark, not its paper, decides adoption.**
   - About 445 LLM benchmark papers appeared at six top venues in 2018–2024 [bean2025measuring]. Yet 34 major model releases in 2025–26 named 110 benchmark families, 44% of them only once [D:MCA].
   - Citations correlate *negatively* with headline adoption (ρ = −0.34, exploratory; L-M) [D:MCA].
   - The strongest measured predictors are a trusted third-party runner whose competitor numbers labs can cite, and alignment with what labs sell [google2025gemini3eval; D:MCA].

2. **Everything saturates; brands survive by renewal.**
   - A static benchmark now stays in headline tables for about 7–30 months [D:MCA].
   - The hardest 2025 sets went from single digits to near ceiling in 13–18 months [petrov2025proofbluff; dekoninck2026beyond; epoch2026tier4saturated; alloevil2026tracker].
   - Every family with a long 2026 headline presence except HLE is a versioned brand [D:MCA].

3. **Validity collapse kills more often than a capability ceiling.**
   - 42% of FrontierMath problems had errors [epoch2026frontiermathv2].
   - Only 641 of 2,500 HLE items were certified correct [zhai2026hleverified].
   - At least 59.4% of audited hard SWE-bench Verified items were flawed [openai2026noVerified].
   - A do-nothing agent scores 38% on τ-bench [zhu2025abc].

4. **Winners share six traits:**
   - a legible, anchored unit;
   - cheap exact verification;
   - real-work tasks;
   - launch headroom against humans;
   - a distribution channel;
   - versioned maintenance.

   Evidence: [anthropic2025swebenchSonnet; metr2025horizon; rein2024gpqa; D:MCA]. Winners are mostly *not* unique. HLE, METR's time horizon, GPQA and ARC-AGI all correlate 0.95–0.97 with a refitted general-capability index [C:offg]. "Nothing unique" is a scientific weakness, not an adoption killer.

5. **The lead's diagnosis of the ten benchmarks is half right.**
   - *Supported:* fragmented scores, install friction, pre-emption, too few items, and the vetting burden of generated items.
   - *Contradicted:* memorisation (MastermindEval is procedural; its flaw is brute-forceability), "no philosophy", "solved games max out", "very simple" (TopoBench: 0.15 on hard puzzles), "Chutes and Ladders" (Concept: humans >90% vs evaluated models <40%), and "not fun" as an adoption cause.
   - *Missed:* empty repositories, frontier-model exclusion, maintenance cliffs and name collisions.
   - Evidence: [golde2025mastermindeval; topsakal2024grid; topobench2026projectpage; gevers2026concept; mayug2026topobenchrepo].

6. **Games rarely stick for structural reasons.** They appear in 0 of 34 headline tables, including Google's despite Kaggle Game Arena [D:MCA]. The format invites pool-relative scores, tool-solvable tasks, oversupply and weak product links [anthropic2025pokemon].

7. **The open niche is measurement quality.** No benchmark yet combines all of:
   - procedurally generated, never-seen material;
   - an exact verifier;
   - a difficulty knob;
   - built-in shortcut controls;
   - a linked, human-anchored scale.

   The best-evidenced construct for such a benchmark, learning a novel system from supplied material, is probably mostly general-factor-loaded (CL-bench 0.71; ARC 0.95–0.97) [C:offg]. Its distinctness must therefore be tested, not assumed.

---

## The benchmark lifecycle

The survey supports a five-stage life cycle: **birth → adoption → saturation and contamination → validity collapse → retirement or successor**. Every stage has compressed from years to months.

**Birth.** Supply vastly exceeds demand:
- Ott et al. curated 3,765 benchmarks and found that "many benchmarks fail to find widespread utilization" [ott2022mapping].
- 61 developer reports (Jan 2022–Nov 2025) mention 190 benchmarks [akhtar2026plateau].

| Benchmark (launch) | Launch score | Human reference | Source |
|---|---|---|---|
| MMLU (2020) | GPT-3 43.9% | 89.8% expert estimate | [hendrycks2021mmlu; gemini2023] |
| GPQA (Nov 2023) | GPT-4 39% | experts 65%; non-experts with web 34% | [rein2024gpqa] |
| SWE-bench (Oct 2023) | 1.96% | — | [jimenez2024swebench] |
| OSWorld (Apr 2024) | 12.24% | 72.36% | [xie2024osworld] |
| FrontierMath (Nov 2024) | <2% | — | [epoch2024frontiermath] |
| HLE (Jan 2025) | 3.3–9.4% | — | [phan2025hle] |

**Adoption.** Lags are short when channels exist [D:MCA]:
- *Weeks* for a new version of an adopted brand. Terminal-Bench 2.0 was released 7 Nov 2025 and appeared in Claude Opus 4.5 on 24 Nov 2025.
- *About 2–3 months* for an independent benchmark with headroom and a leaderboard: τ²-bench → GPT-5; HLE → o3.
- *5–10 months* for a competitor's benchmark or near-zero launch scores. ARC-AGI-2 launched in Mar 2025 and was adopted in Nov 2025, at 31–38%.

Triggers were institutional rather than academic:
- OpenAI's Preparedness team co-built SWE-bench Verified in Aug 2024 [openai2024sweverified].
- ARC ran five quiet years until o3 scored 75.7% on 20 Dec 2024 [chollet2024o3arc].
- GDPval went from 1/14 to 12/13 frontier tables after Artificial Analysis rebuilt it as GDPval-AA [D:MCA; aaGdpvalAA2025].

**Saturation and contamination.** Time to human parity fell from about 15–20 years (MNIST, Switchboard) to about a year (GLUE) [kiela2021dynabench]. In the LLM era:
- MMLU needed about 3.25 years to pass its expert estimate [hendrycks2021mmlu; gemini2023].
- SWE-bench Verified went from 40% to over 80% in one year [anthropic2026demystifyingEvals].
- ARC-AGI-2 went from single digits to 95.0% in about 18 months [kamradt2025arcagi2launch; alloevil2026tracker].
- ARC-AGI-3 went from under 1% (Mar 2026) to 99.9% under a provider harness six months later [latere2026field; kamradt2026astra].
- In the long-context family, NIAH saturated in about 3 months and OpenAI-MRCR's 2-needle 128K setting in 4 months [kamradt2023niah; gemini2024gemini15; openai2025gpt5dev].

Of 60 widely reported benchmarks, 29 are highly saturated. Age and test-set size are the most consistent predictors, and private test sets showed no reliable protection (N = 4) [akhtar2026plateau].

Contamination runs in parallel through two channels:
- *At training time.* GPT-4o scores 88.0% on MMLU but 73.4% on the closed MMLU-CF [zhao2025mmlucf].
- *At run time.* Claude Opus 4.6 decrypted BrowseComp's canary-keyed answer key [anthropic2026browsecomp].

**Validity collapse.** Near the top of the scale, broken items dominate what is left to solve (see Executive summary, item 3). Further cases:
- about 30% of SWE-bench Pro public tasks were broken [openai2026signalNoise];
- 27 of 50 τ-bench airline tasks were corrected [sierra2026tau2changelog].

Configuration confounds grow to the size of model gaps. Step budget moved one model on OSWorld-Verified from 42.88% to 62.88% [osworldVerifiedData2026], and Anthropic now advises skepticism toward gaps under 3 points [anthropic2026infraNoise].

**Retirement.** Seven dated modes appear:

| Mode | Example | Source |
|---|---|---|
| Lab-issued retirement | OpenAI stopped reporting SWE-bench Verified on 23 Feb 2026 | [openai2026noVerified] |
| Silent drop at ceiling | AIME 13/14 → 0/13 frontier tables; MMMU 11/14 → 0/13 (2025 → 2026) | [D:MCA] |
| Self-retirement | Open LLM Leaderboard (13 Mar 2025); HELM maintenance mode (1 Jun 2026); MathArena's farewell to final-answer contests (May 2026) (M/L) | [fourrier2025ollretire; crfm2026helmmaint; sun2026farewell] |
| Dormancy | EvalPlus, Aider Polyglot, TheAgentCompany; BFCL data unchanged since 16 Dec 2025 | [liu2023evalplus; aider2024polyglot; tacExperiments2025; bfclLeaderboardData] |
| Environment rot | 55.6% of ToolBench APIs unstable (M); 13 of 46 OSWorld Chrome tasks broken by site changes | [guo2024stabletoolbench; zhu2025abc] |
| Family exit | No multilingual row in any 2026H2 frontier table | [D:MCA] |
| Successor under the same brand | Verified/Pro/v2; Terminal-Bench ships a major version about every 4–6 months | [D:MCA] |

The turnover is visible in one lab's tables. None of the 8 benchmark families in Claude 3.7 Sonnet's table (Feb 2025) appears in any Anthropic headline table from Opus 4.8 (May 2026) onward [anthropic2025claude37; anthropic2026opus48; D:MCA].

**Field divergence closes the loop.** Scores and real-world value have come apart:
- Experienced developers were 19% *slower* with early-2025 AI tools [becker2025metrRCT].
- About half of test-passing SWE-bench Verified patches would not be merged [metr2026mergeability].
- Anthropic's Sep 2026 launch says benchmark margins "have become a less reliable guide to real-world differences" [anthropic2026opus55].

---

## A framework of benchmark success and failure

Fourteen factors in four groups. Each has a definition, a mechanism, evidence from successes (S) and failures (F), a strength rating, and a 0–3 anchored rubric. **Strength** is the factor's link to the outcome named, using the briefs' H/M/L grading.

### Group I: Measurement validity

**F1. Construct definition and incremental validity.**
- *Definition:* a written account of what the score measures and what it should and should not correlate with, plus evidence of reliable variance beyond general capability.
- *Mechanism:* a stated construct guides evolution and resists relabelling. Incremental validity is the scientific reason for a new benchmark.
- *S:*
  - ARC's theory of skill-acquisition efficiency, published with candid limits ("Test validity is not established"), told it how to evolve [chollet2019measure; chollet2024o3blog].
  - MASK separated honesty from accuracy: ρ −0.60 vs +0.87 with compute (M) [ren2025mask].
- *F:*
  - Reviewers of 445 papers found definitions and scoring that "undermine the validity" of claims [bean2025measuring].
  - BBQ-accuracy behaves like a reasoning benchmark [desai2026whatbenchmarks], and safety benchmarks track capability [ren2024safetywashing].
  - ARC's theory did not make it distinct from the general factor: ρ = 0.953–0.966 [C:offg].
- *Strength:* moderate for scientific value; **weak for adoption**. Adopted benchmarks are g-loaded: HLE 0.968, METR 0.965, GPQA 0.974 [C:offg].
- *Rubric:*
  - 0 = no stated construct, or unrelated constructs in the headline;
  - 1 = construct named, no validity evidence;
  - 2 = construct plus at least one validity check (external criterion, controlled manipulation or human gap);
  - 3 = construct theory with convergent, discriminant and incremental evidence over a general factor.

**F2. Exact, automatic verification.**
- *Definition:* deterministic, specification-traceable scoring; no LLM judge in the headline.
- *Mechanism:* cheap, repeatable scoring enables many runs and reproduction, and removes the judge as an attack surface.
- *S:*
  - Winners used multiple choice, hidden tests, execution checkers, CTF flags, database-state checks and Lean proofs [rein2024gpqa; jimenez2024swebench; xie2024osworld; zhang2025cybench; yao2024tau; tsoukalas2024putnambench].
  - WebArena-Verified *removed* LLM judging [hattami2025webarenaverified].
- *F:*
  - A constant "null model" gets an 86.5% length-controlled win rate on AlpacaEval 2.0 [zheng2025cheating].
  - Changing the judge moves one model from 79.0 to 49.1 [arenahardauto2025repo].
  - 31.08% of passing SWE-bench patches passed only because tests were weak [swebenchplus2024].
- *Counter-evidence:* judged, product-aligned sets are adopted: HealthBench 4/34, Finance Agent 8/34 [D:MCA]. But their graders change silently [openaiSimpleEvalsHBPro2026], and rubrics miss clinical hallucinations (M) [farrow2026rubricsfail].
- *Strength:* strong for validity and longevity; moderate for adoption.
- *Rubric:*
  - 0 = scoring requires human judgement;
  - 1 = LLM judge, rubric or self-report in the headline;
  - 2 = deterministic but untested for defects;
  - 3 = deterministic, with an oracle solution and a null baseline shipped.

**F3. Statistical resolution.**
- *Definition:* enough independent items and trials to separate adjacent frontier models, with uncertainty reported.
- *Mechanism:* unresolvable gaps yield noise-driven ranks and early "saturation".
- *S:*
  - With 95% CIs, Arena-Hard separates 87.4% of model pairs, against 22.6% for MT-Bench's 80 questions [li2024arenahardblog].
  - Test-set size is one of the two most consistent saturation predictors [akhtar2026plateau].
- *F:*
  - Detecting a 3-point gap needs about 969 items [miller2024errorbars].
  - One AIME item is worth 3.33 points, and seed-to-seed SD is 5–15 points [hochlehnert2025sober].
  - Terminal-Bench 2.0 (n = 82) was flagged very highly saturated at one month [evaleval2026saturationdata].
  - 14 of 24 benchmarks report no uncertainty [reuel2024betterbench].
- *Tension:* small sets were adopted *because* they were cheap [I].
- *Strength:* strong for validity; moderate for adoption.
- *Rubric:*
  - 0 = under about 100 units, or no uncertainty reported;
  - 1 = a few hundred units, no CIs;
  - 2 = CIs of ±3–5 points reported;
  - 3 = pre-registered power analysis, about 1,000 or more independent clusters (or adaptive IRT), and paired clustered SEs.

**F4. Shortcut, tool and harness robustness.**
- *Definition:* the score cannot be reached through format heuristics, lookup, brute-force code, do-nothing actions or harness tricks; the tool policy is declared.
- *Mechanism:* shortcuts inflate scores and turn rankings into harness contests.
- *S:*
  - MMMU-Pro filtered out text-answerable items [yue2025mmmupro].
  - NoLiMa removed lexical overlap, shrinking "effective context" by 16× to more than 128× [modarressi2025nolima].
  - SWE-bench Pro V2 re-grades in a pristine offline sandbox [scale2026sweproV2].
- *F:*
  - Question-blind heuristics score 66.6–79.6% on TruthfulQA [turner2025gamingtruthfulqa].
  - A do-nothing agent scores 38% on τ-bench [zhu2025abc].
  - Mastermind's 1,296 possible codes (4 positions, 6 colours) can be brute-forced [golde2025mastermindeval].
  - Harness choice moves ARC-AGI-3 by 36 points [kamradt2026astra] and BFCL by 44 [bfclLeaderboardData].
- *Strength:* strong.
- *Rubric:*
  - 0 = solvable by a short program, lookup or heuristic, with no tool policy;
  - 1 = no demonstrated shortcut, but no controls;
  - 2 = tool policy plus at least one control (blind baseline, ablation, mutation or harness comparison);
  - 3 = full battery: blind, do-nothing and brute-force baselines, a sealed runtime and harness sensitivity.

### Group II: Longevity and integrity

**F5. Launch headroom against a human anchor.**
- *Definition:* the frontier is far below ceiling at launch, against a measured human reference.
- *Mechanism:* this opens the window in which labs adopt a benchmark, and supplies a "beat the expert" story.
- *S:*
  - On ARC-AGI-2, every task was solved by at least 2 people in at most 2 attempts, while "Pure LLMs score 0%" [kamradt2025arcagi2].
  - Labs adopt at roughly 10–40%: ARC-AGI-2 at 31–38%, ARC-AGI-3 at 30.2% [D:MCA; anthropic2026opus5].
- *F:*
  - BrowseComp Long Context launched at 80–90% and was dropped after two releases [openai2025gpt5dev].
  - LongBench v2 passed its human baseline at launch [bai2024longbench2].
- *Counter-evidence:*
  - HealthBench Professional (a system above physicians, 59.0 vs 43.7; M) and MMMLU (o1 at 87.7%) were adopted anyway [openai2026healthbenchpro; openai2024mmmlu].
  - Headroom created by a "must stump today's model" filter selects bad items [phan2025hle; zhai2026hleverified].
- *Strength:* strong for legitimacy and timing; not necessary under strong product alignment.
- *Rubric:*
  - 0 = near ceiling, or trivially solvable;
  - 1 = headroom claimed, but frontier untested or no reference;
  - 2 = frontier at or below 50% on current frontier-class models, or a large gap to a measured human baseline;
  - 3 = both, with frontier at or below 30% and far below the human baseline.

**F6. Renewal mechanism and difficulty knob.**
- *Definition:* the item pool can be refreshed and made harder under one name, with a frozen split kept for comparability.
- *Mechanism:* renewal turns inevitable saturation into a new version rather than a death.
- *S:*
  - All long-lived 2026 families except HLE are versioned [D:MCA].
  - MRCR survived by going from 2 to 8 needles and from 128K to 1M tokens [openai2025gpt52; openai2026gpt54; gemini2025gemini25].
- *F:*
  - Fixed configurations died fast: NIAH in about 3 months, BrowseComp Long Context at launch, LOFT after one release [kamradt2023niah; openai2025gpt5dev; lee2024loft].
  - Frozen pools went dormant [liu2023evalplus; openai2025paperbench].
- *Caveat:* public generators become curricula. IFBench's held-out constraints bought about a year [pyatkin2025ifbench; aa2026method], and Prime Intellect packaged six long-context evaluations as RL tasksets [primeintellect2026longcontext].
- *Strength:* strong.
- *Rubric:*
  - 0 = static pool;
  - 1 = regenerable, but no plan;
  - 2 = difficulty knob or scheduled fresh items;
  - 3 = knob plus published cadence plus stable name plus frozen split.

**F7. Contamination resistance (training-time and run-time).**
- *Definition:* scores cannot reflect memorised items or answers retrieved during evaluation, and leakage is measured.
- *Mechanism:* contamination inflates public scores and destroys trust.
- *S:*
  - MathArena exposed 10–20-point AIME 2024 inflation [balunovic2025matharena].
  - GSM1k's parallel form turned an accusation into an estimate: drops of up to 8% [zhang2024gsm1k].
- *F:*
  - Masked MMLU options are reproduced at 57% [deng2024contamination].
  - 63% of one model's SWE-bench Pro successes retrieved the known fix [jain2026cursorRewardHacking].
  - Detection is losing: membership inference is near random [duan2024mia], and brief GRPO training conceals contamination [wang2025fragility].
- *Tension:* private sets do not slow saturation (N = 4) [akhtar2026plateau]. Hygiene keeps scores honest; renewal extends life [I].
- *Strength:* strong for validity; moderate for longevity.
- *Rubric:*
  - 0 = public static web-sourced items;
  - 1 = canary strings or surface renaming only;
  - 2 = procedural, post-cutoff or private-holdout items;
  - 3 = a fresh live window, run-time leak controls and a measured contamination gap.

**F8. Item-quality assurance.**
- *Definition:* answer keys are validated redundantly, and an audited error rate is published and re-audited.
- *Mechanism:* near the ceiling, rankings measure agreement with wrong keys.
- *S:*
  - GPQA kept items only where two experts agreed and non-experts failed [rein2024gpqa].
  - SWE-bench Verified screened 1,699 samples with 93 developers and discarded 68.3% [openai2024sweverified].
- *F:*
  - The audits listed in the lifecycle section.
  - 57% of analysed MMLU Virology items are erroneous [gema2025mmluredux].
  - Even exact-graded synthetic MRCR had about 5% wrong ground truth [openai2025gpt52].
- *Strength:* strong.
- *Rubric:*
  - 0 = no audit, or unaudited generated keys;
  - 1 = informal checks;
  - 2 = redundant expert validation, or keys computed by a verified rule engine or generator;
  - 3 = a published audited error rate per release, a 100% oracle and a planned re-audit.

### Group III: Ecosystem and adoption

**F9. Distribution and friction.**
- *Definition:* text-in, text-out scoring that runs on closed APIs; one-command install; harness integration; low cost per run.
- *Mechanism:* people run what is cheap and already wired in.
- *S:*
  - MastermindEval survives because its author merged 6 tasks into lm-evaluation-harness 11 days after release [lmevalMastermind].
  - OpenAI co-built SWE-bench's Docker harness [openai2024sweverified].
- *F:*
  - Game Reasoning Arena needs conda, an OpenSpiel build and four API keys, and carries a non-commercial licence [graRepo2025].
  - TopoBench's repo is empty [mayug2026topobenchrepo].
  - The raw-corpora metric needs logits, so only open models of 8B parameters or fewer were scored [sharma2025rawcorpora].
  - Kimi K2 omitted results over "prohibitively expensive evaluation costs" [moonshot2025kimik2].
- *Counter-evidence:* BFCL shipped on PyPI and in Inspect, yet appears in 0/34 frontier tables [bfclLeaderboardData; D:MCA].
- *Strength:* strong as a necessary condition; weak as a sufficient one.
- *Rubric:*
  - 0 = no public code or data, or needs model internals;
  - 1 = incomplete release (data only, no evaluator), heavy setup or a restrictive licence;
  - 2 = pip or API-only, with a permissive licence;
  - 3 = in a major harness at launch, one command, low cost.

**F10. Maintained, independent, citable leaderboard with governance.**
- *Definition:* a runner adds every frontier model within weeks under a written policy (fixed harness, verified entries, disclosed funding), so labs can cite competitor numbers.
- *Mechanism:* labs need competitor columns, so the benchmark with a trusted runner is the one they report.
- *S:*
  - Gemini 3 Pro sources competitor numbers from ARC Prize Verified, Scale's HLE board, Artificial Analysis and matharena.ai [google2025gemini3eval].
  - GDPval went from 1/14 to 12/13 frontier tables once it had a third-party runner [D:MCA].
- *F:*
  - The grid-games board froze with no outside submissions [researchoutcome2024llmgamebenchmark].
  - GTBench's submission path never shipped [duan2024gtbench].
  - FrontierMath, tied to one sponsor, appears only in OpenAI's tables [D:MCA; besiroglu2025clarifying].
  - Meta privately tested 27 Arena variants [singh2025leaderboardillusion].
- *Strength:* strong. This is the top-ranked measured predictor [D:MCA].
- *Rubric:*
  - 0 = none;
  - 1 = stale or personal board;
  - 2 = creator-maintained, with frontier models added;
  - 3 = a neutral runner covering all frontier models within weeks, with a written policy and verified entries.

**F11. Product and decision relevance.**
- *Definition:* the score informs a decision people actually make, ideally validated against a field outcome.
- *Mechanism:* labs headline what they sell.
- *S:*
  - The agentic share of frontier headline rows went 23% → 76% (2025H1 → 2026H2) [D:MCA].
  - SWE-bench was chosen for its "real engineering tasks from actual projects" [anthropic2025swebenchSonnet].
  - HealthBench and Finance Agent match health and finance products [arora2025healthbench; bigeard2025financeagent].
- *F:*
  - Games appear in 0/34 tables. On Pokémon: "I don't think anybody's making their buying decision" on it [anthropic2025pokemon].
  - Multilingual rows exited once the capability became table stakes [D:MCA].
- *Tension:* the highest-face-validity sets are the least renewable; GDPval exposes only a 220-task subset [openai2025gdpval].
- *Strength:* strong for adoption.
- *Rubric:*
  - 0 = no identifiable decision;
  - 1 = plausible but undemonstrated;
  - 2 = a capability labs sell or practitioners recognise as real work;
  - 3 = as 2, plus validation against a field outcome.

**F12. Differentiation and timing.**
- *Definition:* no near-duplicate from a better-resourced group exists or is imminent; prior art is surveyed; the name is unique.
- *Mechanism:* in crowded niches, the incumbent's distribution decides.
- *S:* versioned successors of established brands won their niches: MMLU-Pro, SWE-bench Verified, τ² [wang2024mmlupro; openai2024sweverified; barres2025tau2].
- *F:*
  - Kaggle Game Arena launched the day Game Reasoning Arena's repo was created, on the same engine [google2025gamearena; graRepo2025].
  - GTBench preceded the grid-games paper by five months [gtbench2024].
  - Another Codenames benchmark preceded Hakimov et al. by two months [stephenson2024codenames].
  - PUZZLES held five of TopoBench's six puzzle families [puzzles2024], and TopoBench's name collides with a 256-star library [topobenchTDL2024].
- *Counter-evidence:* MastermindEval's repo predates its supposed pre-emptor [bullsCowsRepo].
- *Strength:* moderate (case-based); strong in hot niches.
- *Rubric:*
  - 0 = near-duplicate of an existing or simultaneous better-resourced benchmark;
  - 1 = crowded niche;
  - 2 = differentiated construct, surveyed prior art, unique name;
  - 3 = first credible entrant, or an evidenced gap.

### Group IV: Narrative and legibility

**F13. Single headline score in a human-legible, comparable unit.**
- *Definition:* one number with a CI, on an absolute or externally anchored scale that extends or links to other benchmarks. Sub-scores are diagnostic only.
- *Mechanism:* rankings are the "primary scientific export" of benchmarks [hardt2025siam].
- *S:*
  - METR's human-minute horizon spans about 4,600× on one curve [metr2025horizon; metrEvalAnalysis2026].
  - The 23-task BBH outlived the 204-task BIG-bench [suzgun2023bbh; srivastava2023bigbench].
  - IRT linking exists: the ECI [ho2025rosetta], and 100 items estimate MMLU within about 2 points [polo2024tinybenchmarks].
- *F:*
  - Qi Town reports three unrelated scores [zhou2025qitown].
  - Grid-game results split into 3 × 3 × 2 cells [topsakal2024grid].
  - HELM fragmented [crfm2026helmmaint].
  - "Effective context length" differs 16× to more than 128× between RULER and NoLiMa for the same models [hsieh2024ruler; modarressi2025nolima].
- *Strength:* strong.
- *Rubric:*
  - 0 = several unrelated scores;
  - 1 = one score, but pool-relative, opaque or not framed as the headline;
  - 2 = one absolute score with CIs;
  - 3 = one score in an externally anchored, extensible, linkable unit.

**F14. Thesis, brand and story.**
- *Definition:* a thesis-bearing, collision-free, stable name; a steward; recurring "moments" (prizes, launch-day results); shareable artifacts.
- *Mechanism:* drives attention and legitimacy. "Fun" is better stated as "stakes plus story": HLE and METR are not fun, but they carry high stakes and dramatic framing [cais2026hle; kwa2025metr].
- *S:*
  - ARC kept one thesis through three versions and drew 1,430 prize teams [chollet2025arcprize2024].
  - HLE got a Nature paper [cais2026hlenature].
  - The pelican test reached a Google I/O keynote with no leaderboard [willison2025yearinllms].
- *F:*
  - Retitled or colliding names [cipolinakun2025gra; sharma2025rawcorpora; topobenchTDL2024].
  - ConceptARC, same format without ARC's institutions, stayed niche [moskvichev2023conceptarc].
  - A strong brand did not prevent HLE's audit failures [zhai2026hleverified].
- *Strength:* moderate for adoption; strong for attention.
- *Rubric:*
  - 0 = no thesis, a generic or colliding name, or retitled;
  - 1 = generic motivation;
  - 2 = distinctive thesis and stable unique name;
  - 3 = plus a steward and recurring moments or prizes.

---

## The lead's ten benchmarks through the framework

**Provisional ratings.** The scores below are this synthesis's own [I] ratings, drawn from `notes/user_failed_a.md` and `notes/user_failed_b.md` and scored with the anchors above. They are *not* blind, and the section 8 study is designed to replace them. Three adopted benchmarks are rated at their launch as calibration rows.

| Benchmark | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 | F14 | Σ/42 | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Qi Town [zhou2025qitown] | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 6 | not adopted |
| 2 Game Reasoning Arena [graRepo2025] | 1 | 2 | 1 | 0 | 0 | 1 | 1 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 10 | not adopted |
| 3 MastermindEval [golde2025mastermindeval] | 2 | 2 | 1 | 0 | 1 | 2 | 2 | 2 | 3 | 0 | 0 | 1 | 2 | 1 | 19 | partial (harness) |
| 4 Concept [gevers2026concept] | 2 | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 0 | 1 | 1 | 2 | 1 | 18 | too young |
| 5 Codenames [hakimov2025codenames] | 2 | 2 | 1 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 0 | 2 | 1 | 21 | partial (clembench) |
| 6 Boardwalk [becker2025boardwalk] | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 11 | not adopted |
| 7 Grid games [topsakal2024grid] | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 0 | 0 | 0 | 1 | 14 | not adopted |
| 8 TopoBench [maniparambil2026topobench] | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 16 | too young; empty repo |
| 9 Raw corpora [sharma2025rawcorpora] | 2 | 2 | 1 | 1 | 1 | 2 | 2 | 1 | 0 | 0 | 1 | 2 | 1 | 0 | 16 | not adopted |
| 10 BloomQA [chen2026bloomqa] | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 0 | 0 | 0 | 1 | 2 | 1 | 1 | 14 | too young |
| *Calibration:* GPQA (2023) [rein2024gpqa] | 2 | 2 | 1 | 2 | 3 | 0 | 1 | 3 | 2 | 1 | 1 | 2 | 2 | 2 | 24 | adopted |
| *Calibration:* SWE-bench Verified (2024) [openai2024sweverified] | 2 | 2 | 2 | 1 | 2 | 1 | 0 | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 25 | adopted |
| *Calibration:* ARC-AGI-2 (2025) [kamradt2025arcagi2launch] | 3 | 3 | 1 | 2 | 3 | 3 | 2 | 3 | 2 | 3 | 1 | 3 | 2 | 3 | 34 | adopted |

**Reading the table [I].**
- The two clear failures (Qi Town and Game Reasoning Arena) score 0–1 on every ecosystem and narrative factor (F9–F14).
- The two survivors plugged into channels that someone else maintains. MastermindEval has the only F9 of 3, and Codenames the only F10 of 2.
- More headroom did not save TopoBench or Concept.
- The calibration rows do not beat the lead's items on F1 or F7. GPQA's edge is item quality and headroom (F5 = F8 = 3); SWE-bench Verified's is relevance and first-mover position (F11 = 2, F12 = 3).

**Where the evidence supports and contradicts the lead's diagnoses.**

| Lead diagnosis (item) | Verdict | Evidence |
|---|---|---|
| No single comparable score (Qi Town, grid games) | **Supported**. Comparing scores *across* benchmarks is solvable by IRT linking | [zhou2025qitown; topsakal2024grid; ho2025rosetta] |
| Simple, well-known games, nothing unique (Qi Town, GRA, grid games) | **Supported** for Qi Town and GRA: Tic-Tac-Toe is solved, and chess already had maintained ladders. **Contradicted** for TopoBench (hard tier 0.15) and Concept (>50-point human gap). "Unique" is rare everywhere: BALROG correlates 0.807 with the ECI refit | [saplin2025llmchess; kelly2026gamearena; topobench2026projectpage; gevers2026concept; C:offg] |
| Heavy install friction (GRA) | **Supported**. The raw-corpora logit requirement is a worse form of the same problem. A sponsor can absorb friction | [graRepo2025; sharma2025rawcorpora; jimenez2024swebench] |
| Framework, not a ladder (GRA, Boardwalk) | **Supported**. Partly a category error for Boardwalk, titled "Towards a Framework". Frameworks survive as harnesses | [becker2025boardwalk; gao2024harness] |
| Possible memorisation (MastermindEval) | **Contradicted**: instances are generated from random codes. The real flaws are a known strategy and brute-force solvability | [golde2025mastermindeval] |
| No underlying philosophy (MastermindEval) | **Contradicted**: it states "simple, scalable, interpretable". Philosophy also predicts adoption weakly (ConceptARC) | [golde2025mastermindeval; moskvichev2023conceptarc] |
| No measurable leaderboard | **Supported**: the strongest measured adoption predictor. Yet MastermindEval survives via the harness | [D:MCA; lmevalMastermind] |
| Not fun for consumers | **Contradicted** as an adoption cause. Arena Elo appears in 0/34 tables, and Cybench won through labs and AISIs | [D:MCA; zhang2025cybench] |
| Skill no product needs (Concept) | **Supported for games generally**. **Weak for Concept**, whose intent inference maps to clarification dialogue (`notes/user_failed_a.md`, interpretation) | [anthropic2025pokemon; gevers2026concept] |
| Pre-empted by a near-duplicate (Codenames; Qi Town, GRA) | **Supported**: a Codenames benchmark came two months earlier, and Kaggle Game Arena launched the same week. **Weak** for MastermindEval | [stephenson2024codenames; google2025gamearena; bullsCowsRepo] |
| Too few items (Boardwalk) | **Supported**: roughly ±16 points [computed in `notes/user_failed_b.md`] | [becker2025boardwalk] |
| Renaming doesn't change concepts (Boardwalk) | **Partly**. Anonymisation is weak, so results are inflated rather than "false"; rule mutation is the strong control | [becker2025boardwalk; becker2025variacoes] |
| Solved games max out (grid games) | **Contradicted** for 2024 models: disqualification rates reached 46.67% and 53.33% with image prompts. Novel Tic-Tac-Toe-style games leave reasoning models 41% below their MATH 500 scores. The real flaw was not using the solver as the yardstick | [topsakal2024grid; mishra2025tttbench] |
| AI-generated items: echo chamber and vetting burden (BloomQA) | **Partly**. The vetting burden is real (no audited sample was published). But grounding in expert guidelines and deterministic keys mitigate the echo chamber, and human-authored keys also fail audits (59.4%, 42%). "Audited vs unaudited" matters more than who wrote the items | [chen2026bloomqa; openai2026noVerified; epoch2026frontiermathv2; vendrow2025platinum] |
| TopoBench "very simple"; raw corpora "main words ≠ adept model" | **Contradicted** for TopoBench (0.15 on the hard tier). **Partly** for raw corpora: it measures knowledge recall, but it was validated against an expert benchmark (r = 0.99, N = 6) | [topobench2026projectpage; sharma2025rawcorpora] |

**Causes the lead missed:**
- **Empty or partial artifacts:** TopoBench's repo is empty; no code was found for Qi Town; Boardwalk released no evaluator [mayug2026topobenchrepo; zhou2025qitown; labcraig2025boardwalkrepo].
- **Frontier exclusion:** TopoBench's best closed model was GPT-5-mini; the raw-corpora pipeline tested only models of 8B or fewer [maniparambil2026topobench; sharma2025rawcorpora].
- **Maintenance cliffs** [graRepo2025; researchoutcome2024llmgamebenchmark].
- **Renamed or colliding names** [cipolinakun2025gra; topobenchTDL2024].
- **Premature verdicts:** Concept, TopoBench and BloomQA were under a year old [gevers2026concept; chen2026bloomqa].

---

## What the successful benchmarks share

Across exams, math, coding, agentic tasks, arenas and ARC, the adopted benchmarks share six traits:

1. **A legible, externally anchored unit and one headline number.** Examples: human-minutes, Elo, expert parity, dollars, "% of real issues resolved" [metr2025horizon; zheng2023arenablog; openai2025gdpval; jimenez2024swebench].
2. **Cheap, automatic, mostly exact verification.** This is what allowed many runs and third-party reproduction [rein2024gpqa; xie2024osworld; white2025livebench].
3. **A headroom window at adoption:** launch far below a human anchor, adopted at roughly 10–40% [D:MCA; kamradt2025arcagi2].
4. **A channel:** a lab sponsor (SWE-bench Verified), a neutral verifier (ARC Prize Verified, Artificial Analysis), government use (Cybench in AISI tests) or a harness (lm-eval) [openai2024sweverified; google2025gemini3eval; zhang2025cybench; gao2024harness].
5. **Product alignment**, which explains the 23% → 76% agentic shift in headline rows [D:MCA].
6. **Maintenance with versioning under a stable name**, or freshness by construction [D:MCA; balunovic2025matharena; jain2024livecodebench].

What they did **not** reliably share:
- citations (ρ = −0.34 with adoption; L-M) [D:MCA];
- a particular venue (MMLU at ICLR, BIG-bench in TMLR, GPQA at COLM) [hendrycks2021mmlu; srivastava2023bigbench; rein2024gpqa];
- a unique signal off the general factor [C:offg];
- consumer fun (Arena Elo appears in 0/34 tables) [D:MCA];
- validity: 42–59% flawed items turned up in audits [epoch2026frontiermathv2; openai2026noVerified].

Two exceptions bound these laws (`notes/gap_uncovered_families_generality.md`):
- **Product alignment can override headroom and exactness.** Two benchmarks were adopted anyway:
  - HealthBench Professional, which is LLM-graded and launched with a system already above physicians (59.0 vs 43.7; M) [openai2026healthbenchpro];
  - MMMLU, on which o1 already scored 87.7% [openai2024mmmlu].
- **A runner is neither sufficient nor necessary.** BFCL had one and appears in 0/34 frontier tables, though it is a headline in Llama and Qwen reports. HealthBench had none [bfclLeaderboardData; meta2024llama33card; qwen2025qwen3].

Adoption is also audience-specific: open-weight developers headline harness-packaged boards that frontier labs ignore [I].

---

## Why game-based benchmarks rarely stick

The evidence gives seven reasons, with counter-evidence at the end.

1. **No reporting channel.**
   - There are 0 conventional game benchmarks in 34 headline tables, including Google's own tables despite Kaggle Game Arena [D:MCA].
   - None of Akhtar's 60 widely reported benchmarks is game-based, though its text-only filters may have screened some out [akhtar2026plateau].
   - Lab game showcases are demos: "this is really for our own understanding" [anthropic2025pokemon].
2. **Oversupply and incumbents.** GitHub has 173 "llm game benchmark" repos and 49 "codenames llm" repos (`notes/user_failed_a.md`, ledger C13). Kaggle Game Arena launched the same day as Game Reasoning Arena, on the same engine [google2025gamearena; graRepo2025].
3. **Pool-relative, fragmented scores.**
   - Qi Town reports Elo, a cycle graph and a sentiment score [zhou2025qitown].
   - Grid games report win rates within a changing pool [topsakal2024grid].
   - Even Kaggle reportedly had to build a unified leaderboard (single source) [gigazine2026gamearena].
   - Solved games offer a perfect yardstick, and the benchmarks did not use it [topsakal2024grid].
4. **Tool-solvability and harness dominance.**
   - Mastermind's 1,296 codes are brute-forceable [golde2025mastermindeval].
   - On ARC-AGI-3, one model scored 62.7% under the standard harness and 98.6% under a provider harness, having "built its own tools for each game" [kamradt2026astra].
   - A harness change plus a newer checkpoint halved the Gemini Pokémon run from 813 to 406.5 hours [gemini2025report].
5. **Fast saturation of fixed configurations.** The Bulls-and-Cows ladder's last commit reads "o3-mini saturated the benchmark" [bullsCowsRepo]. LLM Chess had to add an engine after reasoning models saturated random opponents [saplin2025llmchess].
6. **Maintenance cliffs at the end of the paper cycle.**
   - GTBench: last commit 6 Sep 2024 [duan2024gtbench].
   - GameBench: last commit 27 Jun 2024 [costarelli2024gamebench].
   - SmartPlay: archived [wu2024smartplay].
   - lmgame-Bench: no commits since 12 Sep 2025, despite 983 stars [hu2025lmgame].
7. **Weak product link, and no unique signal either.** Game results track general capability: BALROG ρ = 0.807 and Chess Puzzles 0.737 with the ECI refit [C:offg]. So games neither inform buying decisions nor add construct-level information.

**Counter-evidence the lead should weigh.**
- Games are not intrinsically easy. Novel Tic-Tac-Toe-style games leave reasoning models 41% below their MATH 500 scores [mishra2025tttbench], and Concept shows a >50-point human–model gap [gevers2026concept].
- Game-like formats can be adopted when they ride an established brand with a steward, or report a legible unit. ARC-AGI-3 is in Anthropic's Opus 5 table, and Vending-Bench 2's dollars appear in Google's Gemini 3 table [anthropic2026opus5; willison2025gemini3].
- Community game ladders win attention, not adoption (AI Diplomacy: 707 stars) [aiDiplomacyRepo].

The verdict [I]: games fail mostly for ecosystem reasons (F9–F12) and legibility reasons (F13). The format makes those failures likely. The lead's instinct to leave games is supported, but for these reasons rather than "boring".

---

## Open niches

Ranked by evidence of a gap, net of incumbents and risks (`notes/prior_art_novel_methods.md` and the gap dossiers).

1. **Renewable, exactly graded learning of a novel system from supplied material**, for example a synthetic formal language, API or rule system specified in a document.
   - *Incumbents and their holes:*
     - CL-bench is expert-authored at about 20 hours per context and judged by GPT-5.1 [dou2026clbench].
     - MIR-Bench publishes its generators, which makes it curriculum-ready [yan2025mirbench].
     - MTOB covers one language, and its gains come from copying parallel examples [tanzer2023mtob; aycock2024grammarbook].
     - Many-shot classification in-context learning collapses to similar-exemplar retrieval [zou2025manyiclbench].
   - *Gap:* no benchmark combines all of these:
     - a symbolic generator with an oracle;
     - a closed-book floor at chance;
     - literal-overlap and similar-exemplar controls;
     - separate complexity and length knobs;
     - a human learner baseline.
   - *Risk:* probably g-loaded. CL-bench correlates 0.71 with the ECI refit and ARC 0.95–0.97 [C:offg]. Public generators also become RL curricula [primeintellect2026longcontext].
2. **Teach-back: a model teaches a fixed student, which is post-tested exactly on generated material.**
   - *Incumbents and their holes:* EducationQ, Teach2Eval and TeachBench reuse known items. MathTutorBench scores pedagogy with a reward model [educationq2025; teach2eval2025; teachbench2026; macina2025mathtutorbench].
   - *Risks:*
     - The student is 35% of gain variance in EducationQ's 3×3 [educationq2025] (recomputed in `notes/gap_teachback_instrument_validity.md`).
     - Prompted students cannot "stay ignorant" (M) [validsim2026; sycophanticsim2026].
     - Telling beats teaching on immediate tests [bastani2025guardrails].
     - Human gains barely separate frontier tutors: 0 of 364 significant cells [northcutt2026studentbench].
3. **A calibration overlay decomposed from accuracy.** Calibration error is off-g (1−RMS error vs capability PC1: −0.02 in base models, 0.41 in chat models), while Brier score is not (0.84–0.92) [C:offg; ren2024safetywashing].
4. **Spec-to-executable tasks.** Regulations or protocols become executable checkers, verified by differential testing and rule mutation. This generalises Boardwalk and Code World Models [becker2025boardwalk; lehrach2025cwm]. It is product-relevant and exactly verifiable [I].
5. **Forecasting.** It is off-g among frontier models (ρ = 0.05 at ECI-refit ≥140) [C:offg; fri2026forecastbenchdata]. However, ForecastBench already occupies the niche.
6. **Other gaps without maintained leaderboards:**
   - verification–generation-gap and ground-truth-free consistency boards [li2024gvconsistency; qiu2026peerprediction];
   - discovery in synthetic worlds with hidden laws (`notes/prior_art_novel_methods.md`, niche 6);
   - human-anchored validation of simulated students and users [zhou2026sim2real; northcutt2026studentbench].

The niche that survives the evidence [I]: the contribution should be **measurement quality** first. That means renewable, contamination-proof, exact, linked and human-anchored measurement. **Distinctness** should be a pre-registered, falsifiable secondary claim.

---

## Design requirements for a new non-game method

Each requirement names the factor it serves and a test that can be run before launch.

1. **Single headline score in a human-legible unit (F13).**
   - One number with a 95% CI; sub-scores are diagnostic only.
   - The unit can be stated in one sentence, for example "share of a never-seen system mastered".
   - *Test:* a lay comprehension check passes [metr2025horizon; zhou2025qitown].
2. **A linked, extensible scale (F13, F6).** Scores are placed on an IRT scale with fixed anchor items and anchor models, so new tiers extend rather than reset it. *Test:* linking error ≤2 points on held-out anchors [ho2025rosetta; habba2026growingpains].
3. **Exact automatic grading with oracle and null baselines (F2).** No LLM judge in the headline. A reference oracle scores 100% on every generated item; empty and do-nothing baselines score at the published chance floor. *Test:* continuous-integration checks on every release [scale2026sweproV2; zhu2025abc].
4. **Contamination resistance without LLM-generated items (F7).** Items come from a symbolic generator or from human experts, never from an evaluated model family. LLMs are subjects only. *Test:* a generator-provenance log; a parallel-form gap below 2 points. Evidence: examiner and self-evolving designs are circular [bai2023lmexaminer; selfevolving2025]; parallel forms estimate contamination [zhang2024gsm1k].
5. **Fresh private windows and a curriculum stress test (F7, F6).**
   - Live-window seeds and some item families stay private, and families rotate on a schedule.
   - *Test:* fine-tune a model on the public generator; report its transfer to private families as a contamination index [pyatkin2025ifbench; primeintellect2026longcontext].
6. **A difficulty knob and version cadence (F6, F5).** Separate complexity and length knobs, pre-declared harder tiers, a frozen canonical split, and a new version every 4–6 months under one name. *Test:* v1 includes at least two untouched harder tiers [vodrahalli2024michelangelo; D:MCA].
7. **Launch headroom (F5).** The best frontier model scores 10–40% on the v1 headline, and under 10% on the hardest tier. *Test:* a pre-launch frontier run [D:MCA].
8. **A measured human baseline (F5).** Report both the panel criterion (each item solved by at least 2 people) and the individual average, with paid human cost per item and a definition frozen before launch. *Test:* a human study report [kamradt2025arcagi2launch; legris2024harc; wei2025humanbaselines].
9. **Power analysis (F3).**
   - Resolve 3-point gaps among the top 10 models.
   - This needs roughly 1,000 or more independent clusters, K ≥ 4 samples per item, and paired, clustered SEs.
   - *Test:* a pre-registered power report [miller2024errorbars; hochlehnert2025sober; kotawala2026resolution].
10. **Demonstrable incremental validity over a general factor (F1).**
    - Sample: ≥60 models (target 100) from ≥10 families.
    - Pre-registered falsifier: a disattenuated leave-one-out ECI correlation ≥0.9 means the benchmark collapses into g.
    - The construct claim additionally requires split-half *residual* reliability ≥0.5.
    - Yardsticks (GPQA, ARC-AGI-2) are re-scored on the same sample.
    - *Test:* the validity report [C:offg; campbell1959convergent; sechrest1963incremental].
11. **Shortcut controls shipped with every release (F4).** Question-blind, material-removed, literal-overlap-twin and similar-exemplar-ablation baselines, plus composition items unsolvable by nearest-example copying. *Test:* the gaps are reported [modarressi2025nolima; aycock2024grammarbook; zou2025manyiclbench].
12. **Resistance to tool brute force and evaluation-time search (F4).**
    - Sealed offline sandbox; answers not on the web; tool track reported separately.
    - A published capped brute-force baseline.
    - Score reported against a token and dollar budget at pinned prices, one capped run per model.
    - *Test:* a trajectory retrieval audit [anthropic2026browsecomp; jain2026cursorRewardHacking; chollet2024o3blog; arcprize2026policy].
13. **Black-box, API-only, one-command install (F9).** Text in, text out. No logits and no native builds; runs on closed frontier APIs. `pip install` plus one command. Inspect and lm-eval tasks at launch. Declared cost per model run. *Test:* a clean-machine install in 10 minutes or less [sharma2025rawcorpora; graRepo2025; lmevalMastermind].
14. **A maintained, independent leaderboard with governance (F10).**
    - Every frontier model is added within 14 days of API availability.
    - A named steward, disclosed funding and a written testing policy.
    - The scored model is the shipped model; no private variants or retractions.
    - Retirement triggers are pre-declared.
    - *Test:* the policy is published before launch [arcprize2026policy; singh2025leaderboardillusion; akhtar2026plateau].
15. **Real product relevance with field validation (F11).** Map the construct to a named product capability, such as onboarding to a new API or specification from its documentation. Pre-register a correlation with an external criterion; for a teaching arm, a human-learner falsification study of about 8–10 arms with about 150 learners each. *Test:* the criterion study [metr2026mergeability; northcutt2026studentbench].
16. **An item audit (F8).** An expert-audited random sample per release, with a published error rate of ≤2%, and redundant solving of human-authored items. *Test:* the audit report [rein2024gpqa; epoch2026frontiermathv2].
17. **Differentiation and naming (F12, F14).** Survey incumbents on GitHub, arXiv and Hugging Face, and check the name for collisions. The name never changes after release. *Test:* a prior-art memo [google2025gamearena; topobenchTDL2024].
18. **Openness (F9, F14).**
    - A permissive licence, CC-BY data for retired windows, published outputs and a changelog.
    - *Test:* the licence file [graRepo2025; lmarena2025twoyear].

---

## Retrospective rating study design

**Purpose.** Before we design with the 14-factor rubric, test whether it predicts adoption when applied *blind* to launch-time descriptions.

**Outcome labels** (evidence cutoff 2026-09-29).
- **Adopted:** either of two routes.
  - Reported in at least 3 model reports (launch posts, model cards, technical reports) from frontier or major developers. Sources: the release matrix [D:MCA], and inclusion in Akhtar et al.'s sample, which requires at least 5 of 61 developer reports [akhtar2026plateau].
  - A maintained leaderboard with sustained third-party use for at least 12 months.
- **Partial:** niche but maintained use, or absorbed into a maintained suite, harness or index.
- **Not adopted:** neither.

Adoption is not longevity: several adopted benchmarks have since been retired.

**Sample.** 39 benchmarks.
- By outcome: 20 adopted and 19 not (8 partial, 11 not adopted).
- Coverage: all ten of the lead's items, 11 game benchmarks, 3 puzzle benchmarks and the major successes.
- Three items are right-censored at under 12 months old: Concept, TopoBench and BloomQA.

**Procedure.**
1. Non-raters write the descriptions from launch materials only, with names, brands and dates redacted. Two auditors strike wording that reveals the outcome.
2. At least 3 human raters, plus at least 2 LLM raters from different model families as a secondary arm, score F1–F14 on the 0–3 scale. They calibrate first on 4 practice items outside the sample.
3. Raters score the *launch-time plan*, not later history.
4. A recognition check flags items the rater identifies. Those items are analysed separately.

**Pre-registered analysis.**
1. *Reliability:* Krippendorff's α ≥ 0.67 per factor. Factors below that are merged or dropped before any outcome is examined.
2. *Primary test:* the rubric sum separates adopted from not-adopted benchmarks (AUC > 0.5, one-sided α = 0.05). With 20 vs 19 items, a single pre-specified composite has about 0.89 power at a true AUC of 0.75 and about 0.71 at 0.70 (Hanley–McNeil approximation). Dropping the 3 censored items leaves about 0.86 at 0.75 [computed here].
3. *Secondary tests:*
   - an ordinal logistic model on the three-level outcome;
   - group scores I–IV, with Holm correction;
   - a contrast of ecosystem factors (group III) against validity factors (group I).
4. *Exploratory:* individual factors, which are underpowered at n = 39.
5. *The lead's diagnoses:* each is mapped to a factor (e.g., "no leaderboard" to F10, "not fun" to F14) and tested against the outcome.
6. *Robustness checks:*
   - excluding the censored items;
   - excluding lab-owned benchmarks;
   - using the headline-table count as the outcome [D:MCA];
   - human raters only;
   - unrecognised items only.

| # | Benchmark (year) | At-launch description (rater-facing, name redacted) | Launch source | Outcome | Outcome evidence |
|---|---|---|---|---|---|
| 1 | MMLU (2020) | Four-option multiple-choice exam, 57 academic and professional subjects; static public set; best model 43.9%, expert estimate 89.8% | [hendrycks2021mmlu; gemini2023] | adopted | Akhtar ≥5-report sample; 6/34 [akhtar2026plateau; D:MCA] |
| 2 | HumanEval (2021) | 164 hand-written Python function problems with unit tests from a lab with a code model; execution-scored; 28.8% | [chen2021codex] | adopted | Akhtar sample [evaleval2026saturationdata] |
| 3 | BIG-Bench Hard (2022) | 23 tasks from a 204-task crowdsourced suite where models had not beaten average raters; exact match | [suzgun2023bbh] | adopted | Open LLM Leaderboard v2; Akhtar sample [hf2024ollv2; akhtar2026plateau] |
| 4 | GPQA (2023) | 448 expert-written graduate science MCQs (198-item high-agreement subset); experts 65%, non-experts with web 34%, best model 39% | [rein2024gpqa] | adopted | 27/34 [D:MCA] |
| 5 | SWE-bench (2023) | 2,294 real GitHub issues from 12 Python repos; patch must pass hidden tests; best model 1.96% | [jimenez2024swebench] | adopted | Verified 23/34; retired Feb 2026 [D:MCA; openai2026noVerified] |
| 6 | Chatbot Arena (2023) | Public site: users chat with two anonymous models and vote; Elo-style ratings; academic group; ~4.7K votes in week one | [zheng2023arenablog] | adopted | Maintained; 3M+ votes by 2025; 0/34 rows [lmarena2025twoyear; D:MCA] |
| 7 | MMMU (2023) | 11.5K college-level multimodal exam questions, 30 subjects; best model ~56%; experts 76–89% (M) | [yue2024mmmu] | adopted | 12/34 [D:MCA] |
| 8 | IFEval (2023) | 541 prompts with 25 kinds of code-verifiable constraints; best model ~77% (M) | [zhou2023ifeval] | adopted | 5/34; OLL v2 [D:MCA; hf2024ollv2] |
| 9 | Needle-in-a-Haystack (2023) | Individual's open test hiding one fact in long essay filler across lengths and depths; LLM-graded; a 128K model failed ≥73K tokens | [kamradt2023niah] | adopted | Launch figures of 4 lab releases [gemini2024gemini15; anthropic2024claude3; deepseek2024v3; openai2025gpt41] |
| 10 | ARC (2019) | One researcher's 1,000 hand-made grid puzzles (400 train, 600 eval), exact outputs, framed by a published theory of intelligence with stated limits | [chollet2019measure] | adopted | 10/34; 4 labs' 2025 cards [D:MCA; chollet2026arcprize2025] |
| 11 | τ-bench (2024) | Startup-built tool-use customer-service tasks with an LLM-simulated user; database-state success check; pass^k | [yao2024tau] | adopted | 19/34 [D:MCA] |
| 12 | OSWorld (2024) | 369 real-desktop computer-use tasks with execution checkers; humans 72.36%, best model 12.24% | [xie2024osworld] | adopted | 15/34 [D:MCA] |
| 13 | LiveCodeBench (2024) | Contest problems collected continuously and filtered by release date; executed tests; 400 at first release | [jain2024livecodebench] | adopted | 8/34, 5 orgs [D:MCA] |
| 14 | FrontierMath (2024) | Unpublished research-level math with auto-checkable answers, by a non-profit with 60+ mathematicians; mostly private; models <2% | [epoch2024frontiermath] | adopted | 4/34; hosted runs 2024–26 [D:MCA; epoch2026frontiermathv2] |
| 15 | BFCL (2024) | Academic live function-calling leaderboard; 2,000 query–function–answer pairs; AST and execution grading | [patil2025bfcl] | adopted | Llama 3.1/3.3, Qwen3 reports; 0/34 frontier [meta2024llama33card; qwen2025qwen3; bfclLeaderboardData] |
| 16 | ForecastBench (2024) | Auto-refreshed questions that resolve after evaluation; proper scores vs superforecaster and public groups | [karger2025forecastbench] | adopted | Nightly board; Epoch-ingested [fri2026forecastbenchdata; eciBayesian2026] |
| 17 | Humanity's Last Exam (2025) | ~3,000 expert questions kept only if frontier models failed; $500K prize pool; models 3–9% | [phan2025hle] | adopted | 22/34 [D:MCA] |
| 18 | Terminal-Bench (2025) | ~100 hand-written command-line agent tasks with test scripts; beta release with open harness | [tbench2025] | adopted | 21/34 [D:MCA] |
| 19 | MathArena (2025) | Academic platform scoring only competitions held after model release; 4 samples per problem; outputs published | [balunovic2025matharena] | adopted | Maintained 19 months; cited as competitor source [google2025gemini3eval] |
| 20 | GDPval (2025) | Lab-built work deliverables from 44 occupations; blinded expert pairwise grading; 220-task public subset; best 47.6% | [openai2025gdpval] | adopted | 13/34 [D:MCA] |
| 21 | MastermindEval (2025) | Workshop benchmark: procedural code-breaking in three paradigms; difficulty via code length and colours | [golde2025mastermindeval] | partial | 6 lm-eval tasks [lmevalMastermind] |
| 22 | Codenames concept forming (2025) | Workshop benchmark: clue-giving and guessing vs a programmed opponent, controlled word properties; from a game-suite group | [hakimov2025codenames] | partial | In clembench ladder [clembenchRepo] |
| 23 | LLM Chess (2025) | Community ladder: multi-turn chess vs a random opponent; wins plus instruction-following errors | [saplin2025llmchess] | partial | Maintained; 0/34 [llmChessRepo; D:MCA] |
| 24 | Kaggle Game Arena (2025) | Lab-and-platform arena of strategy games, opening with an 8-model chess exhibition; open harness | [google2025gamearena] | partial | Maintained; 0/34 incl. host [kelly2026gamearena; D:MCA] |
| 25 | MTOB (2023) | Learn to translate a <200-speaker language from one grammar book in context; chrF; human learner baseline | [tanzer2023mtob] | partial | 2 releases [gemini2024gemini15; meta2025llama4card] |
| 26 | MathTutorBench (2025) | Tutoring benchmark; pedagogy scored by a trained reward model; public leaderboard | [macina2025mathtutorbench] | partial | 17-model board; no lab tables [macina2025mathtutorbench] |
| 27 | IFBench (2025) | 58 held-out verifiable constraints on real prompts; most frontier models <50%; ships training constraints | [pyatkin2025ifbench] | partial | AA index for ~10 months; 1/34 [aa2026method; D:MCA] |
| 28 | ConceptARC (2023) | 160 puzzles in an existing grid format, 16 concept groups × 10 | [moskvichev2023conceptarc] | partial | Research use; no board [beger2025modalities] |
| 29 | Qi Town (2025) | 20 LLMs in round-robin board games incl. rule negotiation; Elo, win-cycle graph, self-reported sentiment | [zhou2025qitown] | not_adopted | No code or board found [zhou2025qitown] |
| 30 | Game Reasoning Arena (2025) | Framework wrapping a games library for LLM play; reasoning-trace analysis; conda, native build, provider keys | [cipolinakun2025gra] | not_adopted | Stopped 11 Sep 2025 [graRepo2025] |
| 31 | Concept (2025) | Abduction benchmark from human logs of a word-guessing board game, 4 languages; humans >90%, evaluated models <40% | [gevers2026concept] | not_adopted (censored) | No repo or board [gevers2026concept] |
| 32 | Boardwalk (2025) | 3 LLMs code 12 anonymised board games from rules; best 55.6% error-free | [becker2025boardwalk] | not_adopted | No evaluator released [labcraig2025boardwalkrepo] |
| 33 | Grid-game competitions (2024) | LLM-vs-LLM grid games with three prompt formats; 2,310 matches; board open to submissions | [topsakal2024grid] | not_adopted | Frozen Jul 2024 [researchoutcome2024llmgamebenchmark] |
| 34 | TopoBench (2026) | 900 topology puzzles, 6 families × 3 tiers, verifiers, no tools; frontier 0.58 easy, 0.15 hard | [topobench2026projectpage] | not_adopted (censored) | Repo empty [mayug2026topobenchrepo] |
| 35 | Raw corpora → domain benchmarks (2025) | LLM-free cloze pipeline from corpora; scores target-token rank; validated on 6 base models | [sharma2025rawcorpora] | not_adopted | No code; one guide citation [aialliance2025apptesting] |
| 36 | BloomQA (2026) | LLM-assisted pipeline turning expert guidelines into auto-graded MCQs and dialogues at 4 Bloom levels | [chen2026bloomqa] | not_adopted (censored) | No release [chen2026bloomqa] |
| 37 | GTBench (2024) | 10 game-theoretic tasks with LLM-vs-LLM play and a taxonomy; submission board announced | [gtbench2024] | not_adopted | Board never shipped [duan2024gtbench] |
| 38 | lmgame-Bench (2025) | Models play video and puzzle games through an agent harness; hosted board | [hu2025lmgame] | not_adopted | Stalled Sep 2025 [hu2025lmgame] |
| 39 | EducationQ (2025) | Teacher model tutors a fixed student on known exam questions; score is student post- minus pre-test | [educationq2025] | not_adopted | No board or report use found (`notes/prior_art_novel_methods.md`) |

**Threats to validity.** Recognisable details can leak outcomes. Failures are less well documented than successes. The D:MCA sample under-covers xAI and Alibaba [D:MCA]. "Adopted" mixes audiences: BFCL is adopted by open-weight developers but not by frontier labs [qwen2025qwen3].

If the rubric fails its primary test, that is a finding in itself. The design requirements would then be re-weighted toward the factor groups that did discriminate [I].
