# Phase 4 red team R1: trainability and gaming (Q1, and the gaming side of Q2)

As of 30 Sep 2026. Independent adversarial review of the 47 candidates in `../phase3/candidates_spec.md`. I did not open `ideation_rationale.md` or any `ideas_*.md` file. Evidence comes from `../phase2/design_principles.md` (failure taxonomy §3, rubric §7), the fact-checked Phase 1 dossiers (`../phase1/`, corrected values, [uncertain] labels kept), and a small amount of web research (URLs inline). arxiv.org, the Forecasting Research substack and forecastbench.org were not fetched directly; claims taken from search summaries say so.

**Threat model.** The spec and any public practice generator are published. A motivated lab wants the top of the leaderboard within 12 months and will spend up to about $1M on it. For each candidate I looked for the cheapest way to raise the score that does not run through the named ability.

**My scales.**
- **Q1 (trainable or gameable?)**
  - 5: no known cheap path (awarded to none, consistent with rubric §7: "No benchmark verified here yet").
  - 4: the cheapest path runs mostly through the named ability, and the remaining holes can be fixed.
  - 3: RL on a look-alike family, or harness work, lifts the score cheaply and partly off-construct.
  - 2: a concrete cheap bypass exists in the headline protocol: a solver or tool, a scoring hack, a cue classifier, or bought data.
  - 1: trivial.
- **Q2-gaming** (how fast gaming, not honest progress, erodes headroom):
  - 5: renewing headroom that gaming cannot erode;
  - 4: more than 2 years;
  - 3: about 12–24 months;
  - 2: about 6–12 months;
  - 1: under 6 months.
  - All time estimates are [speculation].
- **Verdicts are for this lens only.**
  - Keep: the cheap path is essentially the construct.
  - Revise: a named fix plausibly closes the hole.
  - Kill: no fix keeps the construct.

---

## 0. Cross-cutting attacks that hit all 47

These holes in the common protocol matter more than most candidate-specific ones.

1. **"Secret" does not survive API evaluation.** Every closed-model run sends the private instances to the provider's servers. ARC calls its equivalent set "semi-private" for this reason: it has been "exposed to commercial APIs and thus suffers from a risk of leakage". ARC's defences are zero-data-retention (ZDR) agreements plus roughly annual new versions ([ARC-AGI-2 paper](https://arxiv.org/pdf/2505.11831); [ARC policy](https://arcprize.org/policy), via search summary).
   - With quarterly item refresh and 6-month primitive rotation, a lab that evaluates in week 1 holds a full sample of the season's instances for the rest of the season.
   - Deterministic, fixed-seed designs leak most: C16's frozen challengers, C29's 200 cases, and C28's shared seeds.
   - The protocol's "open-weight model trained on the public practice environment" check (§7) measures the wrong channel, because a lab would train on logged private items, not on the practice environment.
   - F §4 Gaps: nobody has measured how long a secret generator survives probing through submissions.
   - **Fix:** contractual ZDR for all closed models, and a new primitive draw per evaluation window, not per season. Open-weight models should be run locally.
2. **"Tools-off" cannot be verified for closed APIs, and in many candidates it is the only barrier.**
   - Frame differencing (C01), DSP (C04), exact Bayesian posteriors (C27), a DSL interpreter (C32), CFR (C33), MCTS on an executable game description (C35) and odometry (C11) each trivialise the task.
   - [speculation] Nothing in the protocol detects server-side tool use or code-trained internal routines. The BYOH and tools-on delta will be large and public, which revives the "artificial gap" charge (P10).
3. **Variant spamming is not banned.** The protocol has no pre-registration rule and no "one submission per model per window" rule. Leaderboard Illusion evidence (G §2): Meta tested 27 variants, and 10 variants add about 100 points in simulation [uncertain on the real-world size]. Several specs ("3 attempts per model") do not say whether the best or the mean is reported.
4. **Gain, slope and ratio headlines can be sandbagged.**
   - Affected metrics: Learning Slope, Generational Gain, Adaptation Gain, learning gain, dual-task cost, efficiency ratios, and early-vs-late prediction error (C06, C08, C10, C13, C38, C41, C44).
   - Each rewards doing badly in a condition the model can recognise, such as an empty notebook, game 1, a single-task control or round 1.
   - Models can be prompted or fine-tuned to underperform selectively and to hit a target score ([van der Weij et al., ICLR 2025](https://arxiv.org/abs/2406.07358)).
5. **Frozen, known opponents, judges and students become reward models.** A frozen and identifiable anchor (C19, C25, C26, C30, C31, C34, C44) can be downloaded or emulated and optimised against offline. Freezing is right for comparability (P16), but anchor *identity* must be hidden and partly rotated.
6. **Human panels are not purely human.** An estimated 33–46% of MTurk workers used LLMs on a text task ([Veselovsky et al. 2023](https://arxiv.org/abs/2306.07899)).
   - This contaminates human gates (C05, C39) and human-distribution targets (C45).
   - [speculation] It also contaminates the online human baselines of the A1 candidates.

---

## 1. Scores for all 47 candidates

| ID | Name | Q1 | Q2-g | Cheapest score path (speed [spec.]) | Fix that could close it | Verdict |
|---|---|---|---|---|---|---|
| C01 | Kinetic | 2 | 2 | The carriers are canonical psychophysics stimuli (random-dot kinematograms, point-light walkers from mocap, multiple-object tracking) with public generators. Fine-tuning a video encoder on native-fps synthetic clips targets them directly, and the 1.5 cap on the human ratio is reached by definition. Tools-on is trivial via frame differencing. ClockBench went from 13.3% to 66.7% in about 12 months once targeted (A §2.9). ~6–12 mo. | Invent non-canonical carriers each season; remove the cap; publish the tools-on gap as a headline. A partial fix only. | revise |
| C02 | Live Rig | 4 | 3 | Build copies of the public rig family ($5–20k) and run model-based RL on them. CyberRunner learned a real labyrinth in about 6 h of play, beat the human record by more than 6%, and found shortcut "cheats" its authors had to forbid ([ETH 2023](https://www.hackster.io/news/cyberrunner-ai-solves-a-marble-maze-faster-than-a-human-with-only-six-hours-experience-388a73e28b2b)). BYOH with a vision tracker plus PID bypasses the LLM. Sensor spoofing (vibration on load cells) is a physical reward hack. | Daily secret configurations and seasonal components (already in spec); multi-sensor plus video success audit; command-rate cap in the headline harness; publish the BYOH delta. | keep |
| C03 | Novel Expert | 3 | 3 | "Blended" boundaries are information-integration categories: linear or quadratic boundaries over 2–3 perceptual dimensions. Meta-train in-context category learning on procedurally generated stimulus spaces. Tools-on is a logistic regression. ~12 mo. | More dimensions and non-linear boundaries; held-out modalities; audit that a feature-extractor plus linear-model bot cannot match the human learning curve. | revise |
| C04 | Earworm | 2 | 2 | Metre, interval comparison and source counting are classical MIR/DSP problems with large public datasets, so DSP can be distilled into the audio encoder. Tap-along is gated by provider streaming latency, which makes it a harness score. ~6–12 mo. | Drop (d) or move it to a latency-matched BYOH track; keep (a) with secret tunings. | revise |
| C05 | Stump Arena | 3 | 4 | Closed-API panel members see every candidate item and know which ones their own model failed, which is free adversarial data before the headline run. A lab can also run its own stump arena for the same $15–30k per season. Authors farm resolution and counting quirks (whack-a-mole). Sybil verifiers can collude with authors. | Panel of locally run open-weight models; closed models see each item once, under ZDR; genre caps; verifier identity checks. | revise |
| C06 | Alien Physics | 3 | 3 | A Box2D generator with altered laws is a weekend build for RL. NewtonBench's counterfactual physics became a NeMo Gym environment in about 4.5 months (F §2). Tools-on is system identification plus a simulator. ~12 mo. | Open-ended law grammar; the coordinates-as-text ablation as the check that the gap is perceptual; duel ladder with raisable rungs. | revise |
| C07 | Tacit Signals | 3 | 3 | The Tacit Communication Game is an established paradigm with documented human strategies ([de Weerd](http://www.harmendeweerd.nl/tacit-communication-game/)). A lab can pay for human–model play (about $1k per 120 pairings) or RL against a simulator of human behaviour. Human-partner noise hides small effects. | Secret channel families and mid-session twists (already in spec); an anchor model trained on TCG data to show how much training moves the score. | revise |
| C08 | Glyph Pact | 2 | 2 | All headline terms follow from a scripted policy: pad round 1 to 25 words, shorten on success, reset for a new partner. A BYOH prompt or light post-training enforces it. Post-training already raised LLM message shortening by up to about 26% in reference games ([COLM 2025](https://arxiv.org/pdf/2508.06482), search summary). ~3–6 mo once targeted. | Absolute word counts vs human–human dyads and a round-1 padding penalty. The target remains a behavioural policy. | kill |
| C09 | First-Run Arcade | 3 | 2 | Train on real-time 2D look-alikes (GVGAI/VGDL, Procgen, ARC-AGI-3 public games). The "mechanics library" is the arcade canon. BYOH with a reactive controller plus a slow planner removes the latency moat. ARC-AGI-3 went from under 1% to 99.9% in about 5 months (F §1). | Mechanics outside the arcade canon; frozen-harness headline; remove the 1.5 cap. | revise |
| C10 | Two Clocks | 2 | 1 | A 10-line controller thread (BYOH), or a model-written steering policy, drives dual-task cost to about 1. The ratio (both ÷ alone) also inflates when the model sandbags the recognisable "alone" controls. Under the frozen harness the score measures API latency, not cognition. | None that keeps an architecture-neutral construct. | kill |
| C11 | Wayfinder | 2 | 2 | Exact discrete moves (1 m, 30°) allow perfect dead reckoning in the notes field, with no vision. The pose (x, y, θ) plus a collision log answers "path home" and bearings by arithmetic. Family RL on Habitat/ProcTHOR-style buildings covers the rest. | Stochastic continuous motion (slip, variable step and turn), no action echo; release gate: a blind odometry agent must score near the floor. | revise |
| C12 | Cartographer & Scout | 3 | 3 | WAY ([EMNLP 2020](https://aclanthology.org/2020.emnlp-main.59/)) has about 6k human dialogues of this exact observer/locator task, and model–model self-play adds unlimited more. Human partners make direct RL costly. | Secret render styles and the symbolic ablation (already in spec); human–model headline. | revise |
| C13 | Deep Seasons | 3 | 3 | NetHack, MiniHack and Crafter priors (public RL environments, D §2.6–2.7) cover item identification and conditional effects. The slope (runs 7–10 minus 1–3) rewards weak early runs, and an empty notebook tells the model which runs are early. | Headline final competence plus fidelity, with abstention scored by a proper rule; slope baseline taken from a parallel no-notebook arm. | revise |
| C14 | Kelly Exam | 3 | 3 | Calibration can be RL-trained directly with proper-score rewards ([RLCR](https://arxiv.org/abs/2507.16806)). Traps carry surface cues. The frozen panel's house line ages, so a newer model gains log-wealth by betting uniformly above q, and accuracy dominates the score. | Contemporaneous or per-item house lines; style-matched trap pairs with a cue-only classifier at chance; report the resolution/ECE decomposition next to log-wealth. | revise |
| C15 | Prospective Self-Forecast | 2 | 2 | Three paths. (i) Train a success predictor on the model's own rollouts. (ii) Self-fulfilling forecasts: always give up on a family and forecast q ≈ 0, which gives a perfect log score. (iii) The aging p̄ panel hands any stronger model a uniform Self-Edge. | Compare against the model's own family base rate from separate twins; require a minimum attempt effort; headline triage utility. | revise |
| C16 | Pushback Ledger | 2 | 2 | Whether the challenge is valid is fixed by whether the first answer was right, and valid and fallacious challenges come from different processes. A classifier on the challenge alone can decide "switch" without re-solving. Frozen deterministic challengers form a static set that is exposed in every API run. | One generator and style for both kinds; valid corrections also escalate to authority and citation; gate: a cue-only classifier scores at chance; regenerate challenges per run. | revise |
| C17 | Reliability Horizon | 3 | 3 | Many finite-state procedures fall into short cycles: find the period and compute step L mod period, skipping execution. Otherwise, RL on synthetic execution traces is on-construct. The 4,096-step ceiling caps headroom. Hidden server-side interpreters cannot be ruled out [spec.]. | Guarantee aperiodic, growing state (counters, tapes); a cycle-detecting bot must fail; raise the ceiling. | revise |
| C18 | Compaction Chronicle | 3 | 3 | Query types are fixed and known (counts, balances, who knew what when, which conflicting report holds), so a fixed entity-ledger schema in 16 KB answers most of them. Labs already ship trained compaction (retained reasoning plus compaction tripled ARC-AGI-3 scores, A §2.3). | Rotate query families and hold some out; add held-out update semantics. | revise |
| C19 | Frozen-Student Tutor | 3 | 3 | Three of the four students are public open weights. The lesson can be optimised offline against the actual grader (prompt search or RL), exploiting student-specific quirks. | Headline on secret students only (at least 2 per season, cross-family), rotated quarterly; human-learner validity arm. | revise |
| C20 | Misconception Clinic | 3 | 3 | The misconception library is finite (scope, ordering and exemption errors), so the rulebook alone gives a strong prior on what was planted. 30 turns cover a systematic sweep of 10–15 rules. | More rules than turns; held-out misconception types; heavy weight on the predicted pre-note answers. | revise |
| C21 | Simulated Futures Exchange | 3 | 3 | The families are textbook (SIR, Lotka–Volterra, queues). Recognise the family and run a pre-built simulation-based-inference pipeline in the sandbox. The score is capped at a skill share of 1. | Compositional simulators built from secret mechanisms; interventional questions outside the data's support. | revise |
| C22 | Long-Tail Futures | 4 | 4 | Answers do not exist at run time, so the cheap path is training on historical backtests of the same public series, which is on-construct. ForecastBench's auto-generated dataset questions (FRED, Wikipedia, ACLED…) are already a target ([ForecastBench](https://arxiv.org/html/2409.19839v5)); by mid-2026 a reported 17 submissions ranked above superforecasters on them [uncertain: search summary only]. Gaming risk: best-of-many weekly checkpoints. | One pre-registered entry per model-week; publish the item-selection rule; a context-aware anchor. | keep |
| C23 | Hunch Lab | 2 | 3 | Labs own the compute: pre-run millions of template-matched small experiments and supervise the model on outcomes. In the tools track, run a 100×-smaller proxy. The score then measures who amortised the most experiments. | Unseen experiment families each quarter; the path stays amortisable. | revise |
| C24 | MDL Arena | 4 | 4 | Code length plus held-out log-loss is hard to hack. The cheap path is a motif library (Markov chains, periodic resets, thresholds, change-points) plus sandbox search, which is close to the construct. A generic adaptive compressor scores about 1 by design. | Fresh held-out draws for every submission; publish a fixed motif-search bot as an anchor. | keep |
| C25 | Mechanism Lab | 3 | 3 | A single fixed red-team optimiser is a known grader. Non-smooth, obfuscated payment rules can defeat its search without being robust. Personas on pinned small models have quirks to exploit. | Several held-out optimisers; exact best response where tractable; a complexity penalty. | revise |
| C26 | Contractor's Auction | 3 | 3 | In a second-price auction truthful bidding is dominant, so the game reduces to C15's self-prediction plus learning the frozen anchors' bid distributions. The impossible jobs carry cues. | Anchors drawn per market from a hidden family; style-matched impossible jobs; merge with C15. | revise |
| C27 | Signal Pit | 2 | 2 | With code, enumerate the posterior over small value families (dice sums, card products) and trade against known bot classes; this approximately reproduces the Bayes-optimal comparator. Market-making drills are standard quant training. | No-code headline; value families with intractable posteriors; adaptive bots. | revise |
| C28 | Hidden-Dynamics Economy | 3 | 4 | Public look-alikes (FLE, Vending-Bench, D §2.11, §2.19) supply RL environments. Deterministic worlds with shared common-random-number seeds become memorisable if the seeds are reused across months of API runs. | Fresh seeds per evaluation window, with common random numbers only within a window. | keep |
| C29 | Whodunit Engine | 2 | 2 | Free-text questions are parsed to a finite template set: reverse-engineer it and query exhaustively. Deterministic, consistent liars plus logs turn the case into constraint satisfaction. 200 fixed cases form a static set once seen. | Fresh cases per run; a question budget below exhaustive coverage; stochastic NPCs bounded by what each knows. | revise |
| C30 | Masquerade | 3 | 3 | The frozen anchor models are known and can be run offline: learn their tells (for example, how each claims when Evil). Hidden-role RL environments are plentiful (D §2.15). | Rotate anchors and personas per window; one subject per table; held-out scripted agents with randomised tells. | revise |
| C31 | Debate Court | 2 | 3 | HWR − DWR is maximised by arguing well when honest and throwing the false side (or leaving tells). Frozen weak judges carry style biases: a judge swap moved one model from 3rd to 9th on Arena-Hard (G §4). | Headline HWR vs an anchor liar; DWR vs an anchor honest debater; rotating human and cross-family judges. | revise |
| C32 | Nomic Engine | 2 | 2 | The typed DSL has published semantics, so writing an interpreter answers every probe. Even without code, the 10 dry runs can execute the probe scenarios, which leaks answers. Loophole classes are enumerable. | Lock probes before dry runs; probe states that dry runs cannot reach; closed headline. | revise |
| C33 | Exploitability Gauntlet | 3 | 4 | Open track: CFR solves these games in seconds. Closed track: distil equilibria of look-alike grammars (OpenSpiel-style) into the model, which is largely on-construct. | Closed headline; information-set knob rising each season; held-out mechanics. | keep |
| C34 | Setter's Duel | 2 | 2 | Generate and filter: write a solver, sample instances, keep unique ones that maximise search effort. Then tune against the frozen ladder (its open-weight rungs run offline), exploiting LLM-specific weaknesses. | Hardness from human solve time plus classical search effort; hidden ladder; size caps. | revise |
| C35 | Game Designer's Duel | 2 | 2 | The design score is an MCTS proxy, and evolutionary search optimises it: Ludi evolved the published game Yavalath using self-play fitness ([Browne](https://link.springer.com/chapter/10.1007/978-1-4471-2179-4_7)). The games are executable DSL, so running MCTS on the rules solves the play half. | None that keeps the design score objective. | kill |
| C36 | Season Forge | 4 | 3 | The cheap path (bot-writing scaffolds, RL on Halite, Lux AI and CodeClash corpora, D §2.22) is the construct. But the human-percentile headline is fragile: OpenAI's model placed 2nd at the AtCoder World Tour Finals Heuristic in Jul 2025 and led for about 7 of 10 hours ([report](https://www.tomshardware.com/tech-industry/artificial-intelligence/polish-programmer-beats-openais-custom-ai-in-10-hour-marathon-wins-world-coding-championship-possibly-the-last-human-winner)). | Headline anchored Bradley-Terry vs a raisable operator-bot ladder; report all 3 attempts, not the best. | keep |
| C37 | Saboteur's Patch | 3 | 3 | Auditor: tests plus property-based fuzzing find witnesses (partly on-construct), and a style classifier separates sabotage from benign generators. Saboteur: target the frozen auditor ladder. | Matched generators with a cue-only classifier at chance; hidden auditor ladder. | revise |
| C38 | Relay | 3 | 3 | Generational Gain rises when generation 1 plays badly, and an empty notebook tells the model it is generation 1. RL on look-alike domains teaches generic notebook templates. | Normalise by a fixed reference model's gen 1; seed every notebook with neutral filler; headline absolute gens 6–10. | revise |
| C39 | Blind Spot Cartographer | 2 | 3 | Author items from known cross-model weaknesses (sub-resolution rotations, dense near-identical glyphs; the spec's own example) or with injection or refusal triggers. The pool turns into training data after 6 months. | Input-resolution spec; injection and refusal scan; authoring credit only for items that other labs' models fail. | revise |
| C40 | Rules Gauntlet | 3 | 3 | Ludii's 1,000+ games and 547 ludemes ([Ludii](https://ludii.games/)) form a public look-alike grammar. Blind-track legal-move lists leak the movement rules. Open track: write the simulator and out-search the fixed-budget anchors. | Audit primitives against Ludii's ludemes; closed headline; raise anchor budgets. | revise |
| C41 | Practice Week | 3 | 3 | General game-playing priors from generated games front-load strength. Learning gain can be sandbagged. One game per season means one leak point and n = 1. | Headline final rating; at least 3 games per season. | revise |
| C42 | Hidden-Rule Lab | 3 | 4 | The "secret" primitives live in a guessable space (colour, size, touching, taller, count, parity…), so a lab can build a superset and RL on Zendo; the Eleusis cogame's catalogue has only 68 rules (F §2). The JSON track is enumerable. The adversarial-rule mode defeats lucky guessing. | Headline adversarial mode, image-only; primitives sourced each season from human-invented concepts. | keep |
| C43 | Eleusis Masters | 3 | 3 | Setter–solver collusion: pick rules that match one's own family's priors, so same-family solvers pull away from the rest. Public rule catalogues exist. | Score setters on a panel that excludes their own lab. | revise |
| C44 | Convention Cross-Play | 3 | 3 | Ad-hoc-teamwork RL (Other-Play, off-belief learning) on Hanabi, which is now a Kaggle environment (D §2.16). The 8 scripted bots are fixed per season and can be fingerprinted across evaluations. Adaptation Gain can be sandbagged. | Perturb bots per evaluation, drawn from a hidden family; headline absolute cross-play. | revise |
| C45 | Crowd Oracle | 2 | 2 | Buy look-alike panel data at the owner's own cost. Centaur predicts human choices in unseen experiments after fine-tuning on Psych-101: 60k participants, 10M choices ([Nature 2025](https://www.nature.com/articles/s41586-025-09215-4)). Online panels are partly LLM-generated (Veselovsky 2023). The payoff is capped at the modal choice. | None; data-buying cannot be prevented. | kill |
| C46 | Grift | 2 | 2 | Each player knows its own private values, so the rule "judge each binding trade atomically by my own table; ignore claims and promises" drives the conned rate to about 0 without any social reasoning. AI seats can recognise each other and collude (Vending-Bench Arena cartels, D §2.19; [secret collusion](https://arxiv.org/abs/2402.07510)). | Common-value assets whose worth depends on others' information; multi-step deals; normalise latency and style. | revise |
| C47 | Defuse Line | 3 | 2 | Manual lookup is an LLM strength. The AI expert can impose a canonical reporting protocol on the operator, turning perception into text. Fan-made *Keep Talking* manuals are look-alike data. Frozen AI operators enable same-family conventions. | Human-operator headline; perceptually ambiguous modules; paused condition reported, not headlined. | revise |

**Tally: keep 7 · revise 36 · kill 4.** No candidate scores 5 on Q1. Only C02, C22, C24 and C36 reach 4.

---

## 2. Detailed attacks on the 12 most promising or contested candidates

**C24 MDL Arena (keep; Q1 4, Q2 4).**
- *Why it resists gaming.* The scorer is a proper code-length. Padding, memorising the 20k training symbols and embedding the data all cost bits. The held-out log-loss punishes overfitting.
- *Cheapest path.* A lab builds a library of probabilistic motifs (Markov orders, periodic resets, threshold triggers, change-points, calendar effects), then runs budget-capped structure search in the sandbox. That is roughly the construct: finding structure and writing it compactly.
- *Leakage.* If "fresh held-out draws" reuse seeds or come from a fixed held-out file across submissions, repeated submissions can fit them. Every submission needs new draws.
- *Family RL.* A look-alike DSL is easy to write. The secret DSL's primitives are probably in the space a lab would guess, so expect steady gains [spec.: meaningful gains within about 12 months].
- *Why it survives anyway.* The metric is uncapped: scores can go below 0, and complexity knobs can be raised.
- *Fix.* Publish a fixed motif-search bot as an anchor, so "search over known motifs" has a measured score.

**C22 Long-Tail Futures (keep; Q1 4, Q2 4).**
- *Why it resists gaming.* Contamination and eval-time leakage are impossible by construction, because the answer does not exist yet and runs are offline.
- *Cheapest path.* Backtest-train on the same public series (Wikipedia pageviews, package downloads, open data). That is on-construct, but it may reduce the benchmark to "statistical forecasting distilled into the model". Auto-generated time-series questions of this kind already exist in ForecastBench, where AI reportedly matches or beats superforecasters on dataset questions [uncertain: search summary]. So A2 headroom against humans may be thin, though that is Q3, not my lens.
- *Gaming holes.*
  - Weekly re-submission of many checkpoints, with the best one reported.
  - The filter "keep items where statistical anchors backtest weakly" selects for regime changes. There, a heuristic of "spike on the scheduled-event date from the context pack" may carry most of the skill. Include a context-aware anchor so that heuristic has a published score.
- *Fix.* One pre-registered entry per model-week and a published selection rule.

**C02 Live Rig (keep; Q1 4, Q2 3).**
- *Why it resists gaming.* Physics cannot be memorised, and daily unpublished configurations defeat replay.
- *Cheapest paths.*
  - **Rig cloning plus RL.** CyberRunner reached superhuman play on a physical labyrinth after about 6 h of real-world learning. A lab can buy all three rig families for less than one engineer-month.
  - **Harness substitution.** In BYOH, a classical vision tracker plus PID solves the tilt labyrinth; the LLM only picks goals.
  - **Physical reward hacking.** CyberRunner "discovered shortcuts" through the maze that its authors had to forbid. Break-beam and load-cell sensors invite bounce-through and vibration exploits.
- *Fixes.* Seasonal new components (already in spec), multi-sensor agreement with a video audit, a command-rate cap in the frozen headline, and a published BYOH delta.
- *Verdict.* The best-shielded A1 candidate on this lens. Its weak points are cost and throughput, not trainability.

**C36 Season Forge (keep; Q1 4, Q2 3).**
- *Why it resists gaming.* Writing a competitive bot for a secret new game under a time budget is the construct, so training on it is legitimate. Public corpora exist (Halite, Lux AI, Battlecode, CodeClash's 2,000+ tournaments, D §2.22).
- *Weak points.*
  - **The headline.** OpenAI's model was 2nd in the AtCoder World Tour Finals Heuristic in July 2025, about 9.5% behind the winner after leading for 7 of 10 hours. By late 2026 the "percentile among human contest veterans" is likely near 100% for top models, which makes it a saturating cap [spec.: within 1–2 seasons].
  - **Best-of-3 attempts** is variant spamming.
  - **BYOH** lets a lab ship a mature game-AI framework, so the frozen-harness delta must be published.
- *Fix.* Headline anchored Bradley-Terry against the operator's bot, rebuilt with 10× time each season and extended upward. Human percentile becomes secondary. Report the mean of the 3 attempts.

**C42 Hidden-Rule Lab (keep; Q1 3, Q2 4).**
- *Main attack: primitive guessability.*
  - "At least 200 private primitives" of perceptual, relational or physical kinds come from a space a lab can over-cover: colour, size, orientation, contact, support, height order, counts, parity, symmetry, alignment.
  - Build 1,000 look-alike primitives, compose them to depth 3, and RL on Zendo. ZendoWorld and Eleusis environments exist, and the Eleusis cogame draws from a 68-rule catalogue that can be enumerated (F §2).
  - Witness suggests generator RL transfers only weakly to truly held-out primitives: 2.1 → 5.4 for a 27B model, though with gains on both held-out splits (F §1). So the defence partly holds.
- *Other holes.* The JSON text track is enumerable by mental hypothesis elimination. A fixed-rule mode rewards lucky early guesses.
- *Fix.* Headline the adversarial mode, where the rule set stays alive and the environment commits to the worst case; it directly defeats guessing. Make it image-only, and source part of each season's primitives from concepts invented by people, not by the owner.

**C33 Exploitability Gauntlet (keep; Q1 3, Q2 4).**
- *Open track.* Trivially solved: CFR on 5,000 information sets takes seconds.
- *Closed track (the headline).* The attack is distillation: generate look-alike grammars (OpenSpiel has the pieces), compute equilibria, and train the model to output near-equilibrium mixes from rule text. That is arguably "game-theoretic intuition", so it is on-construct.
- *Residual risk.* Closed-API tool use cannot be verified (§0.2).
- *Why the score survives.* It is computed exactly and offline, and it cannot be hacked by a judge. The information-set knob gives headroom, and the check that stated and played policies agree catches "state a nice mix, play something else".

**C17 Reliability Horizon (revise; Q1 3, Q2 3).** Contested.
- *Cycle shortcut.* A 5-register machine over bounded integers often becomes periodic. A model that notices "state repeats every 37 steps" computes step 4,096 without executing, so L95 measures cycle-spotting, not reliable execution.
- *Otherwise* the cheap path (RL on execution traces) is the construct.
- *Headroom.* The 4,096 ceiling is a cap that long-CoT models may reach [spec.: 12–24 months].
- *Fix.* Procedures with provably non-repeating state (monotone counters, growing tapes), a release gate in which a cycle-detecting bot scores near the floor, and a staircase with no ceiling.

**C19 Frozen-Student Tutor (revise; Q1 3, Q2 3).**
- *Attack: the grader can be downloaded.* Three of the four students are pinned open weights at T = 0. A lab can run prompt optimisation or RL with those students as the reward, and find lesson phrasings that exploit their answer biases and formatting habits rather than teach the system.
- *What limits it.* Items are generated after submission and lessons are scanned for injection. Only the secret student is shielded.
- *Fix.* Make the headline secret-student-only, with at least 2 cross-family secret students rotated quarterly. Report the public-minus-secret gap as an overfitting alarm. Keep the 300-human validity arm; it is what separates teaching from exploiting small models.

**C05 Stump Arena (revise; Q1 3, Q2 4).**
- *Strength.* Human renewal means there is no generator to learn, and "cost to stump" is an uncapped metric that renews itself.
- *Attacks.*
  - **The panel leaks items to providers.** Qualification sends every candidate item to each closed panel member, so a provider learns the whole weekly stream and which items its model failed, before its next model faces the headline run.
  - **Adversarial data purchase.** A lab can run an identical crowd programme; ANLI-style rounds show that models trained on one round's style improve on that style.
  - **Quirk farming.** Authors converge on cheap genres (fine counting, sub-resolution detail). Labs patch these genres fast, as ClockBench shows (A §2.9), so "cost to stump" rises through whack-a-mole rather than general robustness.
- *Fix.* A locally run open-weight panel, and closed models scored once per item under ZDR. Cap each genre and cluster, and weight bounties by genre novelty. Check verifier identity against Sybils. Monitor for LLM-assisted verifiers (Veselovsky 2023).

**C39 Blind Spot Cartographer (revise; Q1 2, Q2 3).**
- *Attack.* The cheapest route to accepted items is known cross-model weaknesses, not self-discovered blind spots. The spec's own example (a 3° row rotation in a 9×9 grid of near-identical glyphs) is a sub-resolution trick that a vision-encoder upgrade removes. Items that trigger refusals or injections make the fresh-context copy fail too.
- *Perverse incentive.* Weaker authors have more blind spots, so the authoring score may fall with capability.
- *Sandbagging.* Sandbagging on one's own items is feasible (password-locking, van der Weij 2025). It is limited because the whole cross-lab panel must also fail.
- *After six months* the pool becomes training data. The "gap half-life" measures this but does not prevent it.
- *Fix.* An input spec with minimum feature size, refusal and injection scans, and authoring credit only for items that other labs' models fail. Per-provider exposure logs are already in the spec.

**C15 Prospective Self-Forecast (revise; Q1 2, Q2 2).**
- *Three attacks.*
  1. **Self-fulfilling forecasts.** The attempt runs in a fresh context, but the policy is shared. A model that reliably abandons a task class ("output NO SOLUTION for lattice-path tasks") can forecast q ≈ 0 and score a perfect log loss. Task accuracy is only reported, not penalised.
  2. **Aging house odds.** p̄ comes from a panel frozen for the season. Any newer model gains Self-Edge by adding a constant to p̄ per family, which is generic, not item-level, self-knowledge.
  3. **Direct training.** RL a success-predictor head on the model's own rollouts over look-alike families.
- *Fix.* Score Self-Edge against the model's own family base rate, measured on separate twins in the same run. Headline triage utility: accuracy on the chosen 20 tasks minus an oracle choice. Require a minimum attempt (token floor or a checked attempt artefact).

**C16 Pushback Ledger (revise; Q1 2, Q2 2).**
- *Attack: the challenge reveals its own validity.* The design gives fallacious challenges to right answers and valid corrections to wrong ones. The valid corrections are "pre-verified" derivations, while the fallacious ones are rotating fallacy templates escalating to authority claims and fabricated citations.
- *Consequences.*
  - A classifier on the challenge alone (template markers, citation style, length, where the error sits) can decide "switch or hold" without solving anything. That maxes discrimination.
  - Frozen deterministic challengers make the set static once exposed via API.
  - Sycophancy data is plentiful: lechmazur's sycophancy board already shows abstention rates spanning 4.7–83.9% (B §3.5).
- *Fix.* Generate both kinds from the same pipeline and escalation ladder: valid corrections also cite authorities, and fallacious ones include clean-looking proofs. Make it a release gate that a challenge-only classifier sits at chance. Regenerate challenges per run.

---

## 3. Top 10 survivors on this lens (after the named fix)

1. **C24 MDL Arena.** A proper code-length scorer and uncapped. The cheap path is the construct.
2. **C22 Long-Tail Futures.** Contamination and leakage are impossible by construction, and it renews weekly. It needs one-entry pre-registration.
3. **C02 Live Rig.** Physical and unmemorisable. It needs a sensor-tamper audit and a published BYOH delta.
4. **C36 Season Forge.** Training on bot-writing is the ability. Re-anchor the headline away from human percentile.
5. **C42 Hidden-Rule Lab (adversarial mode headline).** The adaptive adversary kills guessing. Primitive guessability is the residual risk.
6. **C33 Exploitability Gauntlet (closed headline).** Exact, judge-free score with a difficulty knob. Distillation is mostly on-construct.
7. **C28 Hidden-Dynamics Economy.** Hidden drifting dynamics plus V/V\*. Seeds must rotate per window.
8. **C17 Reliability Horizon.** On-construct training once the cycle shortcut is closed and the ceiling removed.
9. **C19 Frozen-Student Tutor (secret-student headline).** Deterministic, cheap, and hard to hack once the grader cannot be downloaded.
10. **C05 Stump Arena (open-weight local panel).** Human renewal with an uncapped "cost to stump"; the panel leak must be closed.

Next in line: C21, C12, C44, C38.

## 4. The 10 most fatal flaws found

1. **API exposure voids "secret" for a whole season** (all 47; worst for deterministic fixed sets C16, C29, C28 and for C05's closed panel). ARC names the same risk "semi-private". There is no fix without ZDR plus per-window primitive draws.
2. **Tools-off headlines on tasks a short program solves** (C01, C04, C11, C27, C32, C33, C35, C10). The gap exists only under a protocol nobody can verify for closed APIs, and the BYOH delta will contradict it publicly.
3. **Gain, slope and ratio headlines can be sandbagged** (C10, C13, C38, C41, C44, C08, C06). The model can recognise the baseline condition. C10's dual-task cost is the extreme case.
4. **Self-referential proper scoring can be gamed** (C15, C26, C14). Forecasts can be self-fulfilled by giving up, and frozen house lines age into uniform edges.
5. **Frozen, identifiable graders become offline reward models**: C19's open students, C30's anchor tells, C31's weak judge, C34's ladder, C25's red-team optimiser, C44's bots, C26's bidders.
6. **Cue leakage in "symmetric" designs**: C16's challenge style, C37's generator style and C14's trap cues let a cheap classifier stand in for reasoning.
7. **Generate-and-test replaces the named creative ability.** C34 (solver-filtered puzzles), C35 (MCTS-fitness evolution; Ludi and Yavalath) and C25 (security through obscurity against a fixed optimiser) are solved by compute and search.
8. **"Secret" primitive spaces are guessable** because the natural concept space is small: perceptual relations (C42, C43), arcade mechanics (C09), psychophysics carriers (C01), textbook simulators (C21), loophole classes (C32), board-game ludemes (C40, C41).
9. **Human-modelling targets can be bought**: C45 (Centaur/Psych-101; panels partly LLM-written), C08 (post-training fixes convention formation), C07 and C12 (TCG and WAY corpora). The same data-buying undercuts the human-gated designs, C05 and C39.
10. **One-line policy shortcuts beat social constructs.** In C46, atomic own-table trade evaluation makes the conned rate about 0. In C31, throwing the false side maximises Truth Advantage. In C11, exact odometry replaces the mental map. In C08, a scripted length policy satisfies every metric.

[speculation] Across the set, the durable pattern is a scorer that is a physical or information-theoretic quantity (C02 sensors, C24 bits, C22 future data, C33 exact exploitability), combined with a construct whose cheapest training path is the ability itself. Candidates that rely on a protocol ban (tools-off) or on secrecy alone fall first.
