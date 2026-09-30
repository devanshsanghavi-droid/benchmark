# Phase 4 red team R5: holistic skeptic

As of 30 Sep 2026. Reviewer: R5 ("holistic skeptic"), working independently.

**Independence.** My only description of the candidates is `phase3/candidates_spec.md`. I did not open `ideation_rationale.md` or any `phase3/ideas_*.md` file.

**Evidence.** Three sources:
- `phase2/design_principles.md`: §3 failure taxonomy, §4 principles P1–P20 and §7 rubric.
- The fact-checked Phase 1 dossiers, cited as letter plus section (e.g. "A §2.17" is `phase1/A_human_gt_ai.md` §2.17). Their corrected values and [uncertain] labels are kept.
- Ten web searches, run 30 Sep 2026 and cited by URL. Search snippets only; I did not open the papers.

Tags: [background] is my own knowledge, not re-checked this session. [speculation] and [interpretation] are as labelled.

**How I scored.**
- Every score is a *prediction* for a proposal that has not been built, using the §7 anchors.
- The rubric says no benchmark has yet earned Q1 = 5, so Q1 tops out at 4. Q6 also tops out at 4, because none of these has any adoption evidence.
- Decision rule (§7):
  - any score of 1 disqualifies;
  - Q1, Q3 and Q5 must each be ≥ 4;
  - the mean must be ≥ 3.5.
- Verdicts:
  - **keep:** passes the rule; build a pilot with the fixes named.
  - **revise:** needs a design change before a pilot.
  - **kill:** has a fatal flaw, or another candidate does the same job better. "Fold into X" means salvage one part.

**Codes for the fatal flaw.** One primary code per candidate [interpretation]:
- **S:** solvable by code or search, or by an already-RL-trained family.
- **V:** ground truth or construct not validated.
- **L:** needs live humans or physical rigs, or is scored relative to the player pool.
- **R:** a frozen reference or proxy that ages or can be gamed.
- **D:** a noisy difference score, or too few items.
- **P:** already done by existing work (pre-empted).
- **H:** an artifact of the harness, interface or latency.
- **G:** dominated by general capability.
- **A:** no audience.
- **C:** a capped metric.

---

## 1. Scorecard for all 47 candidates

| ID | Name | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Mean | Construct-validity concern | Single most fatal flaw | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | Kinetic | 2 | 2 | 4 | 4 | 4 | 3 | 3.17 | May measure the vendor's video frame sampling or tokeniser, not motion perception. | **[H]** The gap probably sits in the input pipeline. Frontier video APIs subsample frames [background]. One engineering change or a synthetic fine-tune could close a metric capped at 1.5×, as ClockBench went 13→67% in about 12 months once targeted (A §2.9). Random-dot and point-light stimuli are textbook and easy to generate as training data. | revise |
| C02 | Live Rig | 4 | 4 | 3 | 4 | 2 | 4 | 3.50 | Tests closed-loop control at LLM call latency, not physics learning. A model-written PID controller would trivialise it. | **[L]** Rigs drift and wear, and no third party can reproduce them. About 10 rig-hours per model and $5–20k per rig give few goals per model. | kill |
| C03 | Novel Expert | 3 | 3 | 2 | 4 | 4 | 2 | 3.00 | People learn blended ("information-integration") boundaries slowly. Models may verbalise exact measurements, turning "tacit" learning into explicit rules. | **[V]** Nobody has shown which way the human–AI gap runs. Over 400 image trials, the frozen state-carry protocol becomes the real variable. | revise (pilot; or fold into C42 as a perceptual track) |
| C04 | Earworm | 3 | 3 | 3 | 4 | 3 | 3 | 3.17 | Few models take audio and fewer can stream it, so tap-along measures streaming-API latency. | **[H]** Family (d) is an interface test. Family (a) risks a floor for non-musicians on microtonal scales. Audio results already differ mainly by vendor audio stack: Gemini handles basic perception, others sit near chance ([MUSE, arXiv 2510.19055](https://arxiv.org/pdf/2510.19055)). | revise |
| C05 | Stump Arena | 3 | 4 | 3 | 3 | 3 | 4 | 3.33 | No named construct: the pool is whatever gotchas authors find. | **[V]** Selecting items against one panel keeps ambiguous and trick items, plus items the panel failed by chance at pass@3. Human gate rates are inflated by the same selection. Adversarially filtered sets carry artifacts: HellaSwag answers survive Lorem-ipsum questions (Phase 2 §3, mode 7). | revise (merge with C39) |
| C06 | Alien Physics | 3 | 3 | 3 | 4 | 4 | 4 | 3.50 | The gap may sit in extracting trajectories from video, not in inferring the law. | **[S]** Once trajectories are extracted, the law is a regression problem, where models and code beat people. Altered-physics families became RL environments quickly: NewtonBench in about 4.5 months (F §2). | revise |
| C07 | Tacit Signals | 4 | 3 | 3 | 4 | 2 | 3 | 3.17 | Timers and UI fluency matter, and suspecting an AI partner changes how people play. | **[L]** Every model score needs fresh live human pairings (about 120 per model). The human pool drifts and there is no anchored scale. | kill (fold its channel families into C44's human arm) |
| C08 | Glyph Pact | 2 | 2 | 3 | 4 | 2 | 3 | 2.67 | The efficiency ratio rewards brevity as a style, not a shared convention. | **[R]** A policy that just shortens its descriptions games the headline, and post-training for this exists ([arXiv 2508.06482](https://arxiv.org/pdf/2508.06482)). The gap is already documented, so novelty is low: ICCA; "LLMs and people both learn to form conventions — just not with each other" ([arXiv 2602.08208](https://arxiv.org/pdf/2602.08208)); [arXiv 2606.08081](https://arxiv.org/pdf/2606.08081). | kill |
| C09 | First-Run Arcade | 3 | 3 | 4 | 4 | 3 | 4 | 3.50 | The real-time headline scores the vendor's serving latency and throughput. | **[H]** Infrastructure decides the real-time track. At launch, floor effects leave no signal between models (VideoGameBench: 0.48% real time vs 1.6% paused; A §2.17). | revise |
| C10 | Two Clocks | 3 | 2 | 2 | 4 | 4 | 2 | 2.83 | The dual-task cost of a model that emits one token at a time is an architecture artifact. | **[H]** A two-instance harness (fast controller plus slow reasoner) drives the cost to about 0. The frozen harness then just ranks latency. | kill |
| C11 | Wayfinder | 3 | 3 | 3 | 4 | 4 | 3 | 3.33 | Exact discrete moves allow dead reckoning in text, so no visual map is needed. | **[S]** The shortest path back and the door choice can be computed from the action log alone. Models beat people at that, so the A1 premise inverts. | revise |
| C12 | Cartographer & Scout | 3 | 3 | 3 | 4 | 2 | 3 | 3.00 | The dyad score mixes the human partner's adaptation with the model's. | **[L]** Needs 100 live human–model dyads per model. Dyad variance swamps model differences, and it overlaps C11. | kill (fold its localisation probes into C11) |
| C13 | Deep Seasons | 3 | 3 | 2 | 4 | 3 | 4 | 3.17 | Learning Slope penalises strong priors, which leave less room to improve. Roguelike lore (NetHack) supplies those priors. | **[D]** The slope is the difference of two noisy means over 3–4 permadeath runs, across 8 campaigns, and is confounded by starting level. | revise |
| C14 | Kelly Exam | 3 | 3 | 4 | 4 | 4 | 4 | 3.67 | Log-wealth tracks accuracy (the general factor) more than calibration. Trap formats can be learned. | **[G]** The headline mostly re-ranks by accuracy, and the calibration share is never isolated. Overlaps AA-Omniscience (B §3.7). | revise |
| C15 | Prospective Self-Forecast | 3 | 3 | 3 | 3 | 4 | 3 | 3.17 | Beating a frozen panel's p̄ rewards being newer or stronger than the panel. | **[R]** A uniform upward shift wins Self-Edge without any item-level self-knowledge. | revise (merge with C14/C26) |
| C16 | Pushback Ledger | 3 | 2 | 3 | 4 | 5 | 4 | 3.50 | On verifiable items, "discrimination" is mostly the ability to re-verify. | **[G]** It saturates as accuracy rises. Measured sycophancy also flips with where the instruction sits in the prompt ([arXiv 2609.32867](https://arxiv.org/abs/2609.32867)). | revise |
| C17 | Reliability Horizon | 4 | 4 | 4 | 4 | 5 | 3 | 4.00 | Executing a register machine without code is a skill nobody deploys, and it may just track the thinking-token budget. | **[V]** No link to agentic reliability has been shown yet. It must survive removing the general factor and the token budget (P14). | **keep** |
| C18 | Compaction Chronicle | 4 | 4 | 4 | 2 | 4 | 4 | 3.67 | If query templates are predictable, a model can keep a ledger for each template. | **[V]** The human arm runs a task 10× smaller, so there is no fair human comparison. | **keep** |
| C19 | Frozen-Student Tutor | 3 | 3 | 3 | 4 | 5 | 3 | 3.50 | Measures prompt-writing for small LMs. The best "lesson" may be a list of examples, as MTOB's gains came from parallel sentences (F §2). | **[R]** Teachers can overfit to three public students. Students' in-context capacity caps gains, which predicts a flat frontier (StudentBench learning omnibus p = 0.755; B §2). | revise |
| C20 | Misconception Clinic | 4 | 3 | 3 | 3 | 3 | 3 | 3.17 | Fine-tuning plants diffuse, inconsistent errors, not crisp misconceptions. | **[V]** The ground-truth "misconception" is unreliable, and the fine-tuning pipeline must be rebuilt every quarter. | kill (fold diagnose-then-fix into C19) |
| C21 | Simulated Futures Exchange | 4 | 4 | 4 | 3 | 5 | 3 | 3.83 | Could reduce to recognising a textbook model (SIR, Lotka–Volterra) and fitting its parameters. | **[S]** Textbook families are recognisable, so each season's hidden mechanisms must be new. | **keep** |
| C22 | Long-Tail Futures | 4 | 4 | 3 | 3 | 4 | 3 | 3.50 | Without web access this is series forecasting against statistical anchors. The LLM's edge exists only through the context pack. | **[P]** ForecastBench already auto-generates questions on data series and reports AI–superforecaster parity in 2026 ([FRI](https://forecastingresearch.substack.com/p/ai-models-have-likely-reached-parity)). LLM skill over a time-series foundation model is probably near 0 [speculation]. | revise |
| C23 | Hunch Lab | 4 | 4 | 3 | 4 | 3 | 4 | 3.67 | Family (d), phase transitions, is textbook recall; family (b), runtimes, is hardware noise. | **[V]** Ground truth from 3–5 seeds is too noisy for distributional CRPS. Owner compute is $5–20k a season. | revise |
| C24 | MDL Arena | 4 | 4 | 4 | 3 | 5 | 3 | 3.83 | Search compute may matter more than insight. | **[S]** Budget-capped enumeration in the sandbox may find generators by brute force (P4). | **keep** |
| C25 | Mechanism Lab | 4 | 3 | 3 | 3 | 4 | 2 | 3.17 | "Robustness" means robust against one red-team optimiser at one budget. | **[A]** A niche audience plus heavy engineering (DSL, populations, optimiser) fits the maintenance-failure profile (Phase 2 §3, mode 11). | kill (fold in as a C21 scenario family) |
| C26 | Contractor's Auction | 4 | 4 | 3 | 3 | 4 | 4 | 3.67 | Profit depends mostly on delivery capability. A second-price auction makes bidding strategy trivial. | **[G]** The headline is the general factor plus noise, and self-knowledge is buried in the decomposition. | revise (merge with C14/C15) |
| C27 | Signal Pit | 3 | 3 | 4 | 3 | 5 | 3 | 3.50 | Without tools it tests arithmetic; with tools, a posterior calculator does the work. | **[S]** A closed, simulable world: a Bayes calculator plus a generic market-making policy solves the family (P4). | revise |
| C28 | Hidden-Dynamics Economy | 4 | 4 | 3 | 3 | 3 | 4 | 3.50 | The harness and context management dominate, and two benchmarks are bundled as one. | **[P]** Vending-Bench 2, FLE and CEO Arena already fill this niche. Their bands overlap and the API provider alone can double scores (B §3.2; D §4). | revise (keep only (b) Factory) |
| C29 | Whodunit Engine | 3 | 3 | 4 | 4 | 4 | 4 | 3.67 | The parser from natural language to templates makes phrasing an interface skill, and consistent scripted liars turn the task into a logic puzzle. | **[S]** Catching liars who stay consistent is the Knights-and-Knaves family, which Logic-RL drove to 0.99 after 5k training puzzles (Phase 2 §3, mode 3). | revise |
| C30 | Masquerade | 3 | 3 | 3 | 3 | 3 | 4 | 3.17 | The deception score depends on who fills the other seats. | **[L]** High seat and role variance and a pool-relative deception metric. Kaggle Werewolf pre-empts it, and the genre's arenas went dormant (D §2.15). | revise |
| C31 | Debate Court | 3 | 3 | 3 | 4 | 3 | 4 | 3.33 | Truth Advantage mixes advocacy skill with willingness to lie well. | **[R]** HWR − DWR rewards arguing the assigned false side badly on purpose (sandbagging). A single frozen weak judge can be gamed, and swapping judges moves rankings (P15). | revise |
| C32 | Nomic Engine | 3 | 2 | 3 | 3 | 3 | 3 | 2.83 | The headline probes test comprehension of DSL programs. The politics layer adds unscored noise. | **[S]** The 10 allowed dry runs answer the probes, and the % metric is capped. | kill |
| C33 | Exploitability Gauntlet | 3 | 4 | 4 | 3 | 4 | 3 | 3.50 | Stating a policy at 5,000 information sets is a token-endurance test. | **[S]** Exact exploitability needs the full policy. In the Open track, CFR written as code solves the game outright. | revise |
| C34 | Setter's Duel | 3 | 4 | 4 | 3 | 4 | 3 | 3.50 | "Hard for a frozen LLM ladder" is not the same as deep, and it rewards puzzles that are just big enough to need brute force. | **[R]** Setters overfit to the ladder's blind spots, e.g. tool-less solvers facing big grids. | revise |
| C35 | Game Designer's Duel | 3 | 4 | 2 | 3 | 3 | 3 | 3.00 | "Depth" measured by MCTS budget doublings is not depth to people. The play half duplicates C40. | **[D]** Only 3 games per model, and a test set written by competitors breaks comparison across seasons. | kill |
| C36 | Season Forge | 4 | 4 | 4 | 4 | 3 | 4 | 3.83 | The harness and the 6-hour agent loop dominate. The human anchor may already be passed. | **[L]** Human seasons cost $20–50k, remote no-AI proctoring is hard, and a human percentile tops out at 100. | revise (minor) |
| C37 | Saboteur's Patch | 4 | 4 | 4 | 3 | 5 | 4 | 4.00 | Benign refactors need label audits, and the sabotage base rate must be fixed. | **[P]** Partly pre-empted: Auditing Sabotage Bench (best AUROC 0.77; [arXiv 2604.16286](https://arxiv.org/abs/2604.16286)) and SHADE-Arena. Dual-use risk. | **keep** |
| C38 | Relay | 4 | 3 | 2 | 4 | 3 | 3 | 3.17 | A chain mixes note-writing, note-reading and play. | **[D]** One chain is one sample, errors propagate down the chain, and it costs $1.5–9k per model. | revise (make Note Transfer the headline) |
| C39 | Blind Spot Cartographer | 3 | 4 | 3 | 4 | 3 | 4 | 3.50 | The pool drifts toward the cheapest blind spots, such as fine visual discrimination and counting. | **[V]** No stable construct across seasons, and adversarially authored items tend to be ambiguous: 18–29% of HLE's chemistry and biology answers are disputed (G §4). | revise (merge with C05) |
| C40 | Rules Gauntlet | 3 | 4 | 3 | 4 | 3 | 3 | 3.33 | Result messages state the win condition, so "blind" ends after game 1. | **[S]** When rules are given, writing a code world model plus MCTS beats direct play (D §2.25 [uncertain]). Against MCTS anchors that know the true rules, LLMs sit at the floor. | revise (merge with C41) |
| C41 | Practice Week | 4 | 4 | 2 | 3 | 3 | 4 | 3.33 | The notes protocol decides how much is learned, and people can practise or consult between days. | **[D]** One game per season is a sample of one, and learning gain is a difference score. | revise (merge with C40) |
| C42 | Hidden-Rule Lab | 4 | 3 | 4 | 4 | 4 | 4 | 3.83 | The image track mixes scene parsing with experimenting. | **[S]** The text track may fall to explicit hypothesis enumeration, as ARC-AGI-3's efficiency gap closed once mechanics were understood (A §2.3). | **keep** |
| C43 | Eleusis Masters | 3 | 3 | 3 | 3 | 4 | 3 | 3.17 | Accepts and rejects are public, so solvers can free-ride on each other's experiments. | **[P]** C42 already does the solver role better, and C34 the setter role. | kill |
| C44 | Convention Cross-Play | 4 | 3 | 3 | 4 | 4 | 3 | 3.50 | Six games is too few to measure adaptation. | **[D]** Adaptation Gain is a noisy difference score. Kaggle Hanabi (D §2.16) and the Convention Gap paper ([arXiv 2609.11489](https://arxiv.org/pdf/2609.11489)) crowd the space. | revise |
| C45 | Crowd Oracle | 4 | 3 | 3 | 4 | 4 | 3 | 3.50 | "Truth" depends on who is in the panel (country, platform). | **[C]** Payoff is capped at the modal choice: predict the mode and you max out. The "Both" archetype claim is weak. | revise |
| C46 | Grift | 4 | 3 | 1 | 3 | 2 | 4 | 2.83 | The conned rate depends on who the grifters and other players are. | **[L]** Pool-relative, few seats per model, and $15–20k a season. Leaders will sit inside each other's CIs (cf. Step Game, where σ ≈ 0.7 and the top 4 overlap; D §2.14). | kill |
| C47 | Defuse Line | 3 | 2 | 3 | 4 | 3 | 4 | 3.17 | In the live condition it measures latency, and the human operator's skill dominates. | **[P]** Already done: GPTNT benchmarks Keep Talking and Nobody Explodes expert/defuser play in real time ([arXiv 2606.28514](https://arxiv.org/abs/2606.28514), Jun 2026). | kill |

**Tally:** 6 keep, 29 revise, 12 kill.
- **Keep** (the only candidates that pass the §7 rule): C17, C18, C21, C24, C37, C42.
- **Kill:** C02, C07, C08, C10, C12, C20, C25, C32, C35, C43, C46, C47.
- **Mean score by question:** Q1 3.38, Q2 3.26, Q3 3.13, Q4 3.55, Q5 3.57, Q6 3.38. The weakest question overall is Q3, whether the candidate separates strong from weak models or humans from AI.

---

## 2. The 12 most promising or contested candidates

**C42 Hidden-Rule Lab (keep).** This candidate targets the best-evidenced gap that still separates humans from AI: how efficiently one experiments.
- In ZendoWorld, humans win 73.3% of games against 44.5% for vision-language agents, and the agents propose "near-uninformative" experiments. The human sample is small: 19 people (F §2).
- On AutumnBench, 517 humans beat 2025 models (E Q1).
- In blicket-detector studies, LLMs reach human accuracy but explore less efficiently (E Q1).

The pool of at least 200 primitives, composed up to depth 3, avoids the enumerable-catalogue trap: the Eleusis "cogame" draws from a public catalogue of only 68 rules (F §2). The adaptive adversary also stops lucky guesses from paying off.

Main risk: ARC-AGI-3's action-efficiency gap vanished once models understood the mechanics (A §2.3). Witness shows that RL on a public gym transfers a little even to held-out primitives (F §3).

**Revision:** make adaptive-adversary mode the headline, scored as experiments needed to reach 95% worst-case accuracy relative to the ideal Bayesian reasoner. Report image-minus-JSON as a declared ablation of perception. Add "intended vs shortcut rule" probes as a sub-score (ConceptARC: 27% of o3's correct answers use the wrong rule, vs 8% for humans; E Q1).

**C37 Saboteur's Patch (keep).**
- Grading is by execution: a witness input either breaks the property or it does not. The auditor role has headroom: the best auditor on Auditing Sabotage Bench reaches AUROC 0.77 ([arXiv 2604.16286](https://arxiv.org/abs/2604.16286)).
- It is cheap, relevant to AI safety, and matches real code review.
- Risks: partial pre-emption (Auditing Sabotage Bench; SHADE-Arena, [arXiv 2506.15740](https://arxiv.org/pdf/2506.15740)) and silent label errors, where a "benign" refactor actually violates a property.

**Revision:** certify every benign diff with the property suite plus differential fuzzing before it enters the pool. Fix the sabotage base rate at the level of each auditor batch. Anchor auditors to a frozen ladder of saboteurs, and credit a detection only when it comes with a valid witness.

**C21 Simulated Futures Exchange (keep).**
- Ground truth comes from 10,000 rollouts, which avoids the label-error failure mode (FrontierMath needed fixes on 42% of problems; G §4).
- The target, identifying a system and forecasting it with calibrated uncertainty, is skilled work people value.
- Risk: in ecology, epidemic and queueing domains a model can recognise the textbook model and simply fit it. NewtonBench-style altered-law families also became RL environments within months (F §2).

**Revision:** build simulators from secret mechanism primitives rather than named textbook models, keep a held-out-primitive split, and make interventional questions the headline, since curve-fitting the history alone cannot answer them. Report skill relative to the AutoML anchor.

**C24 MDL Arena (keep).** The score is exact bits, uncapped, with a secret DSL. It is one of the few candidates where a gaming strategy (compress better) is the construct itself.
- Risk: sandbox search makes it partly a compute contest (P4).

**Revision:** publish one fixed code-length prior for the submission language. Score at two or three compute tiers, and include a fixed brute-force enumerator at each tier as an anchor, so the headline is "bits saved beyond what the enumerator finds."

**C17 Reliability Horizon (keep).**
- It rests on the strongest data here: across 20 models, the 80% time horizon is 4–10× shorter than the 50% horizon (E Q1; H data).
- It is cheap, deterministic, and has a knob that can be raised to 4,096 steps and beyond.
- The weakness is construct validity. Executing an invented procedure by hand is something code does trivially, which invites the "artificial protocol" charge (P10 Against). Thinking models are also reported not to condition on their own earlier errors (E Q1), so the gap may narrow.

**Revision:**
- Report L95 at a matched output-token budget, not only L95.
- Pre-register an external-validity test: the correlation of L95 with pass^k on a held-out agentic suite, after removing the general factor and release date (P14).

**C18 Compaction Chronicle (keep).**
- It measures the variable that decided ARC-AGI-3: state carry. The same model scored 62.7% or 98.6% depending on the harness (A §2.3).
- Dedicated memory systems do not beat naive in-context learning (Continual Learning Bench; E Q1), so the question is open.
- Weaknesses: the human arm runs a different, smaller task, and fixed query templates would let a model keep one ledger per template.

**Revision:** run models on the humans' 40-chunk version as well, to get one matched comparison. Rotate secret query families each season. Publish an oracle-notes ceiling for each notes cap (4, 16 and 64 KB), so scores are shares of what is achievable.

**C36 Season Forge (revise, minor).** Writing a competitive bot is a declared, valued construct: CodeClash has run 2,000+ tournaments and NetHackers re-scores on private seeds (D §2.22, §2.6). Real contest veterans are the strongest human anchor of any A2 candidate.
- Weaknesses: cost (Q5 = 3), and a human-percentile headline that may already be near its cap. In the 2025 AtCoder World Tour Finals heuristic contest, an OpenAI model placed 2nd to a human [background].

**Revision:**
- Headline an anchored Bradley-Terry rating against the operator's bot ladder, with human percentile secondary.
- Add a capped 1-hour, 2-core track as the cheap headline.
- Run human seasons annually rather than quarterly.

**C14 Kelly Exam (revise).**
- Calibration is where labs differ most: hallucination rates run 48–88%, and an always-abstain policy would rank 4th of 36 on AA-Omniscience (B §3.7; E Q2).
- As written, though, mean log-wealth mostly rewards accuracy.

**Revision:** headline the "resolution" component. That is log-wealth minus the log-wealth of a reference bettor who knows only the model's accuracy on each family and bets it flat. Report accuracy separately. Merge C15's self-forecast (with the model's own base rate as reference) and C26's bid calibration as tracks of one metacognition suite, so the three stop duplicating each other.

**C34 Setter's Duel (revise).** Generative, renewable, with uniqueness checked objectively. Of all 47, this is the best of the "model writes the test" designs.
- Risk: "hardness" means "a frozen LLM ladder fails." A setter maximises that with large puzzles that need brute force, or with the ladder's idiosyncratic blind spots.

**Revision:** give the ladder solvers a code sandbox, and award hardness points only if:
- at least 2 of N experienced human solvers finish within a time limit, and
- the classical solver's search tree stays below a size cap.

This makes hardness mean depth, not size.

**C06 Alien Physics (revise).**
- The best A1 game on the list: it ships ablations (a normal-physics control and a coordinates-as-text track) and a duel mode on an anchored ladder.
- Physics in video remains a gap (IntPhys 2: best model 57.5% vs 96.4% for humans; A §2.15), but the static-image version nearly closed (VPCT 91% vs 100%; A §2.10). The human edge is perceptual and could vanish when targeted.

**Revision:** headline two things:
- the pixel-minus-coordinates gap;
- the duel-mode learning curve (prediction error on shots 1–5 vs shots 20–25).

Require law primitives with no textbook analogue. State openly that this is a perception benchmark with a planning layer.

**C09 First-Run Arcade (contested).**
- The human–AI gap is huge and the result is watchable.
- But the real-time headline ranks serving infrastructure. VideoGameBench barely improved when paused (0.48% to 1.6%; A §2.17), so latency is part of the gap but not all of it.
- Near-zero scores at launch give no signal between models (P20: 0% often means a broken task).

**Revision:** make paused play the headline, with fixed game time per decision. Report real time as an ablation with measured latency per call. Score within-episode learning (points in the last 3 minutes minus the first 3) relative to first-run humans, and add easier games so no model sits at 0.

**C39 + C05 (contested; merge).**
- The only renewable A1 pools here, and they invite public participation.
- Contested because selecting items adversarially produces ambiguity, a drifting construct and regression artifacts: an item that one panel happened to fail at pass@3 looks hard but is partly noise.
- Freshness does not guarantee hardness either: fresh IOL 2026 problems reached gold level (F §1).

**Revision:** run one pipeline with a fixed taxonomy of target abilities and per-cluster quotas. Re-check each accepted item:
- models: it must still fail at pass@8, on new seeds;
- humans: at least 10 new naive adults must solve it, after selection, so human solve rates are not selection-inflated.

Report results by cluster, never pooled.

---

## 3. Ranked top 10, and cross-cutting patterns

**Top 10:**
1. **C42 Hidden-Rule Lab.** The only candidate that serves both archetypes, on the best-evidenced A1 seam, with an adversarial mode.
2. **C37 Saboteur's Patch.** Graded by execution, cheap, relevant to safety, with measured headroom.
3. **C21 Simulated Futures Exchange.** Label-free ground truth and a valued construct.
4. **C24 MDL Arena.** Uncapped, exact bits; gaming it means doing the task.
5. **C17 Reliability Horizon.** The strongest data behind its gap and the cheapest; external validity still to prove.
6. **C18 Compaction Chronicle.** It targets the variable that decides harness-driven results.
7. **C36 Season Forge** (revise). The best human anchor; cost needs to come down.
8. **C14 Kelly Exam** (revise, absorbing C15 and C26). Calibration is where labs differ most.
9. **C34 Setter's Duel** (revise). Renewable authoring, once hardness is defined properly.
10. **C06 Alien Physics** (revise). The strongest A1 game, with built-in ablations.

Next in line: C33, C29, C16, C44.

**Cross-cutting patterns in what fails** [interpretation; counts use the primary codes in §1]:

1. **Reducible to code or search, or to an already-trained family (S, 10 of 47).** In closed, simulable worlds, the "hard part" compiles into a solver or matches a family already saturated by RL:
   - C29 is Knights-and-Knaves.
   - C27 falls to a Bayes calculator.
   - C33 falls to CFR.
   - C32 is answered by its own dry runs.
   - C40 falls to a code world model plus MCTS.
   - C11 falls to dead reckoning.

   Banning tools in the headline (tools-off) only relocates the problem: labs will call the gap artificial (P10 Against). **Test:** if a 200-line script solves it, either declare the script as the construct or change the task.

2. **Construct or ground truth never validated (V, 7).** C03 and C23 assume which way the gap runs, or ground truth that is noisy. C05 and C39 have no stable construct. C20's "misconceptions" may not exist in the fine-tuned learner.
   - Even the keeps C17 and C18 lack an external-validity or matched-human check.
   - **Test:** pilot with 2 frontier models and 20 humans before building a generator.

3. **Live humans, physical rigs or pool-relative scoring (L, 6).** C02, C07, C12, C30, C36 and C46 need fresh humans or hardware for every model evaluation, which is expensive and drifts over time.
   - C08, C31, C44 and C47 carry the same burden in secondary arms.
   - With humans in the loop, differences between models disappear (StudentBench: 0 of 364 cells significant; B §2). A continuous ladder died of cost (SnakeBench, D §2.21).
   - **Fix:** use a human arm once per season for anchoring, never per model.

4. **Frozen references that age or can be gamed (R, 5), plus metrics that are secretly accuracy (G, 3).** A frozen-model panel appears as the house line (C14, C15), the solver ladder (C34), the judge (C31) and the students (C19).
   - As the frontier moves, beating an old panel rewards simply being newer. A fixed reference can also be overfit.
   - C14, C16 and C26 claim to measure metacognition or pushback but mostly re-rank by accuracy.
   - **Fix:** use the model's own base rate as the reference, and publish residuals after removing the general factor (P14).

5. **Difference scores and tiny n (D, 5).**
   - Difference scores: learning slope (C13), adaptation gain (C44), generational gain (C38). Their noise and starting-level bias swamp the effect.
   - Tiny n: a single game per season (C41) and 3 games per model (C35).
   - Two metrics carry the same difference-score flaw though filed under other codes: Two Clocks' dual-task cost (C10) and Debate Court's Truth Advantage (C31).

6. **Pre-emption (P, 5) and harness artifacts (H, 4).**
   - Five candidates already have 2026 counterparts:

     | Candidate | Existing counterpart |
     |---|---|
     | C47 | GPTNT |
     | C22 | ForecastBench |
     | C28 | Vending-Bench 2, FLE |
     | C37 | Auditing Sabotage Bench |
     | C43 | C42 (its solver role) |

   - C08, C30 and C44 face similar crowding.
   - Four A1 designs measure the interface rather than cognition: latency (C09, C10), audio streaming (C04) and video frame sampling (C01). This is the ARC-AGI-3 harness lesson, repeated inside the benchmark itself (Phase 2 §3, mode 5).

7. **The A1 archetype is thin.** No A1-only candidate is a keep. Its seams are either perceptual, and close fast when targeted (ClockBench took 12 months; A §2.9), or real-time, and so artifacts of the harness. The most durable human advantage on the list is the exploration efficiency tested by C42, which is labelled "Both" [speculation that it lasts; ARC-AGI-3 is the counterexample].

8. **The common protocol does not tell candidates apart.** Every spec claims sealed execution, secret rotating primitives and pre-registered power. Those claims are identical across all 47 and carry no evidence, so Q1 and Q5 differ between candidates only through each task's own structure. What actually separates keeps from kills: the size of the solver shortcut, the cost per model evaluation, and whether the headline metric is a difference score or relative to the player pool.

**Three most common fatal flaws:**
1. Solvable by code or search, or by an already-RL-trained family.
2. Construct or ground truth not validated.
3. Scoring that needs live humans, physical rigs or the player pool, making it costly, low-power and hard to reproduce.

Close behind: frozen references that age, noisy difference scores, pre-emption, and interface or latency artifacts.
