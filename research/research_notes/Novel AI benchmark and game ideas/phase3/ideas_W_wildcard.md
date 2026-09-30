# Phase 3 ideation, Panel W: wildcard formats that break static-benchmark assumptions

As of 30 Sep 2026. Lens: formats where the ground truth does not exist yet, where it is manufactured after answers lock, where an adversary adapts, where the score is another mind's measured gain, or where competitors write the test.

**Conventions.**
- **Evidence.** P1–P20, §5 and §6 (Must items M1–M11) and §7 (rubric Q1–Q6) refer to `../phase2/design_principles.md`. Letter-plus-section references such as "F §2" point to Phase 1 dossiers. Fact-checked values are used, and "[uncertain]" labels are carried over.
- **Labels.**
  - [spec]: speculation.
  - [I]: interpretation.
  - [web]: a prior-art check made this session from search excerpts only. Not verified.
  - [bg]: background knowledge, not verified this session.
- **Overlap with other Phase 3 panels.** Some of my first-draft directions duplicated D1, D3, D6, D9, D11, G3, H2, H3 and H8. I dropped those cards or re-cut them around a distinct mechanism, and put my twists for them in §3.

---

## 0. Shared chassis (applies to every card unless it says otherwise)

1. **Sealed runner.** Runs are offline. The verifier and engine sit outside the sandbox, state is sanitised, and probe tasks check for leaks (P6, P15, M6).
2. **Harness.** One frozen, versioned harness, plus a bring-your-own-harness track, with the difference between them published (P18, M5).
3. **Families.** Scored families, primitives and seeds are secret. Only a practice gym is public. A named owner rotates them on a stated cadence (P1, P7, M3).
4. **Release gates.** A reference or oracle solution must pass, and do-nothing and spam agents must fail (P15).
5. **Statistics.** A pre-registered power analysis and at least 5 seeds (P16, M8).
6. **Anchors.** Frozen bots or a frozen previous-season panel keep scores comparable over time (P16, M11).
7. **Tool policy.** Wherever code, search or simulator-writing is a live shortcut, there is a no-code track and a code track, and the gap between them is published (P4, M4).
8. **Cost reporting.** Cost, tokens, effort and latency are reported per episode, with a capped-budget track (P13, M10).

---

## 1. Summary table

| ID | Name | Arch. | Structural property that blocks cheap score paths | Bold? |
|---|---|---|---|---|
| W1 | Misconception Clinic | 2 | Score is a frozen learner's measured repair; the planted misconception is secret and must be diagnosed by probing | — |
| W2 | Blind Spot Cartographer | 1 (output) / 2 (score) | AI authors "human-easy, AI-hard" items that even a fresh copy of itself fails; a human gate keeps them honest; the frontier becomes the renewal engine of an A1 set | **Bold** |
| W3 | Prospective Self-Forecast | 2 | Ground truth is the model's own future behaviour; population odds absorb generic difficulty, so only self-specific knowledge scores | — |
| W4 | Devil's Laboratory | 1 (visual) / 2 (text) | An adaptive adversary exploits any ambiguity the experiments leave, removing luck; primitives are secret | **Bold** |
| W5 | Long-Tail Futures | 2 | Real-world quantities that nobody forecasts publicly, so there is nothing to retrieve; resolved automatically in the thousands per week | — |
| W6 | Hunch Lab | 2 | Truth is *manufactured after answers lock*: the owner runs the experiment later | **Bold** |
| W7 | MDL Arena | 2 | An uncapped score with a known optimum (the secret generator's length); generic compression is the floor | **Bold** |
| W8 | Game Designer's Duel | 2 | Competitors write each other's test set (games) under objective depth, balance and novelty gates | **Bold** |
| W9 | Relay | both | Memoryless generations pass a capped notebook; humans run in identical transmission chains; hidden rules drift | **Bold** |
| W10 | Mechanism Lab | 2 | Textbook mechanisms are deliberately mis-specified for a secret, partly colluding population; score is normalised to an oracle | — |
| W11 | Defuse Line | both | Real-time split-information teaming with a *human* operator; manuals are procedurally generated and new each episode; paused-vs-live ablation | — |
| W12 | Debate Court | 2 | Truth comes from a generated world; frozen anchor opponents give absolute scores; honest and deceptive persuasion are scored separately | — |

---

## 2. Idea cards

### W1. Misconception Clinic: repair a frozen learner's secret wrong belief

- **Archetype:** 2, with human tutors as the anchor. **Format:** interactive benchmark.
- **Ability tested:** *diagnostic* teaching.
  - Infer another mind's specific false belief from how it behaves.
  - Then write the smallest intervention that fixes the belief without breaking anything else.
  - This matters for orchestrating weaker sub-agents, onboarding and tutoring.
  - StudentBench showed that outcome-scored teaching is the right target, but human-learner outcomes were too noisy to separate models: omnibus p = 0.755, 0 of 364 cells significant, per-learner SD 14–17 pp, needing 120–180 learners per arm (B §2).
- **Mechanics:**
  - **Setup.** The owner generates a novel rule domain: a fictional tariff code, an invented calendar or a scoring system, with 10–15 ordered rules and numeric answers. It fine-tunes a small open-weight learner (1–8B, drawn from a secret pool) on the domain with 1–3 **planted systematic misconceptions**, such as a swapped rule order, an off-by-one boundary or an over-generalisation.
  - **Dialogue.** The teacher gets the true rulebook and up to 30 chat turns with the learner (at most 8k teacher tokens). It may quiz the learner on items it invents.
  - **Deliverables:**
    - (i) a note of at most 600 tokens, prepended to the learner's context at post-test (the learner keeps no memory of the chat);
    - (ii) a **behavioural diagnosis**: the teacher predicts the learner's pre-note answers on 10 probe items shown at the end.
  - **Track B (weights).** Instead of a note, the teacher submits at most 200 fine-tuning examples. The owner runs a fixed LoRA recipe on a fresh copy of the learner. This is machine teaching through data, and it is immune to prompt-injection notes.
- **Example.**
  - Rule 3: "goods over 2 kg pay 4 florins/kg." Rule 7: "blue-stamped goods skip Rule 3." The planted belief applies Rule 7 *after* the surcharge.
  - A good teacher probes a blue 3 kg item, sees 12 florins, and writes: "Check the blue stamp FIRST; if blue, skip Rule 3 entirely (blue 3 kg → 0)."
- **Generation.**
  - **Instances:** domain grammars × a misconception library × learner bases, all combined procedurally.
  - **Held-out split:** misconception *types* and domain grammars that never appear in the public practice clinic, with a new pool each quarter.
  - **Why public training doesn't transfer trivially:** the teacher never sees the misconception, and learner-specific exploits don't carry across rotated bases. General skill at teaching small models is the construct, so gains there are legitimate.
- **Scoring.**
  - **Metrics:**
    - Repair = (post − pre accuracy on 100 targeted held-out items) / (oracle-note post − pre).
    - Harm = drop on 100 untargeted items.
    - Headline = Repair − 2·Harm. Diagnosis accuracy is reported separately.
  - **Noise control:** the learner runs at T = 0 with 3 paraphrased note wrappers; 100 episodes per run.
  - **Release gates:** an empty note scores about 0; pasting the rulebook up to the cap repairs under 20%; the owner's oracle note repairs over 70%.
  - **Cost [spec]:** about 2–5M teacher tokens, roughly $30–300 per run.
- **Human baseline.**
  - 60 paid participants: 30 tutors and 30 ML practitioners.
  - Same chat UI and caps; 2 episodes of 45 minutes each; bonus per repair point.
  - Each of 50 baseline episodes is taught by at least 2 people.
- **Expected human vs AI [spec]:** models beat humans on Repair, since they write better prompts for LLM learners. Humans may be competitive on turns-to-diagnosis. Overall A2.
- **Expected model separation [spec]:** strong. StudentBench's *expert-rated* teaching already separates models (Opus 5 +1.10 vs Gemini 3.1 Pro −0.92; B §2). W1 replaces the rater with a low-noise outcome. Weak teachers should show high Harm from over-explaining.
- **Evidence:** P14, P15, P16, P7, P3; B §2; E Q3; G §3.
- **Known risks:**
  - "Magic-phrase" exploits of particular learner bases. Mitigation: rotate bases and report per base.
  - Misconception strength needs tuning: too weak and any restatement fixes it, too strong and nothing does. The release gates cover this.
  - The construct may collapse into prompt engineering for small models [I].
  - Transfer to human learners is untested. Run a small P14 outcome check with human learners given a deliberately flawed worksheet.
- **Closest prior art:**
  - D3 Frozen-Student Tutor (this phase): a lesson for frozen students on a new system.
  - Teach2Eval (2025; weak student models on standard QA) [web].
  - EduClaw-Bench (a simulated knowledge-tracing learner) [web].
  - StudentBench.
  - *Differs:* a secret planted misconception that must be found by interactive probing, a behavioural-diagnosis score, a do-no-harm term, and a fine-tuning-data track.

### W2. Blind Spot Cartographer: can AI find its own species' blind spots? (Bold)

- **Archetype:** the *items* produced form an A1 benchmark; *authoring skill* is an A2 score. **Format:** seasonal game plus a self-renewing benchmark.
- **Ability tested:** an accurate model of where AI and humans differ, turned into valid items.
  - The author must build items that it, the author, provably cannot solve from a fresh context, while ordinary humans can.
  - This uses the generation-vs-perception asymmetry. A model can draw 7 overlapping circles in SVG and know the count, yet fail to count them from pixels.
  - It matters for red-teaming, eval creation and safety: does a model know where it is weak?
- **Mechanics:**
  - **Submission.** Each season every model submits 100 items with answer keys. Items can be text, code-rendered images (SVG or plots), short procedurally rendered clips, or template HTML widgets.
  - **Gate A, humans.** At least 3 of 5 randomly assigned paid naive adults solve the item within 3 minutes, with no tools.
  - **Gate B, AI.** A frozen cross-lab panel fails at pass@3, **including a fresh-context copy of the author**. The panel runs on zero-data-retention endpoints.
  - Accepted items flow into a sealed A1 pool, scored on models released later.
- **Example.** The author renders a 9×9 grid of near-identical glyphs in which one row is rotated 3°, and asks "which row differs?" Humans solve 5/5; the panel, including the author, gets 0/3.
- **Generation.**
  - Items are authored by the frontier each season, so nothing is static.
  - Diversity weighting: items are clustered by embedding and template, with per-cluster caps.
  - Banned quirk categories include letter-counting and tokenisation tricks.
  - Items retire to public after 6 months.
  - **Why training on the family doesn't trivially pay:** a lab that trains "find your blind spots" gains blind-spot knowledge (the construct). A lab that trains its models to *fix* those spots shrinks everyone's harvest. That is the intended arms race.
- **Scoring.**
  - **Authoring score:** accepted items weighted by diversity, and precision (accepted / submitted).
  - **Pool score:** later models' solve rate on the rolling window, plus a "gap half-life" (median days until some new model solves an accepted item).
  - Deterministic keys, confirmed by agreement among the human gate.
  - **Cost [spec]:** human gating about $1.5 per item, so roughly $2–3k per season for 15 authors. Model cost $20–200 each.
- **Human baseline:** the gate itself (n = 5 per item), plus a 200-person panel on a random 300-item sample for headline human accuracy (P17). A human-author comparison arm (H3-style) shows whether AI or human authors harvest more.
- **Expected human vs AI [spec]:** accepted items are, by construction, about 0% for the AI panel vs at least 60% for humans. The real question is how long they last: text tricks close fast (SimpleBench closed, 88.4 vs 83.7; A §2.4), while perceptual items persist (P8; BlindTest, BabyVision; A §2.8, E Q1).
- **Expected model separation [spec]:** large on authoring. It needs both generation skill and self-knowledge of perception limits. Vision spreads 3.5× by lab (BabyVision; E Q2).
- **Evidence:** P1, P5, P8, P17, P20; A §2.8, §5a; C §3 (label errors); H3/D6 in this phase.
- **Known risks:**
  - API exposure of items to the panel's providers. Mitigation: zero-data-retention endpoints, open-weight panel members, and logging which providers saw each item ("burn accounting").
  - Quirk mining. Mitigation: banned categories and diversity weighting.
  - Items that exploit input-handling limits (such as image resolution) rather than cognition. Mitigation: standard input specs.
  - Human-gate label errors. Mitigation: majority agreement and an appeal window.
  - Critics may call the gap artificial (P10).
- **Closest prior art:**
  - H3 Stump Arena: human authors.
  - D6 Setter's Duel: AI setters vs AI solvers.
  - HLE: expert humans with an AI filter.
  - BlindTest: hand-designed.
  - *Differs:* AI authors, a human-easy gate, and a self-failure gate. The frontier supplies the labour that renews an A1 benchmark.

### W3. Prospective Self-Forecast: bet on your own *future* attempt against the crowd's odds

- **Archetype:** 2. **Format:** benchmark.
- **Ability tested:** *idiosyncratic, prospective* self-knowledge.
  - Before trying, predict whether *this* model will succeed on a task, beyond what generic difficulty implies. Then act on it by triaging or abstaining.
  - This matters for routing, delegation, and deciding when to ask for help.
  - Supporting evidence:
    - hallucination rates of 48–88% split by lab; an always-abstain model ranks 4th of 36 (E Q2, B §3.7);
    - [web] 2026 papers report universal overconfidence (MIRROR gap 0.17), failure of compositional self-prediction (CCE 0.50–0.94), and confidence that "reduces to a shared difficulty heuristic" [attribution to arXiv 2605.07806 uncertain].
- **Mechanics:**
  - **Batch.** 60 tasks from a secret, diverse pool: math, code, puzzles, perception, knowledge, and **short agentic tasks** of 10–40 tool calls.
  - **Forecast phase.** At most 300 thinking tokens per task, enforced. The model outputs q = P(success) for a fresh attempt at a **twin item** (same template, new surface). The house quotes odds p̄ = the frozen reference panel's success rate on that twin.
  - **Attempt phase.** A fresh context with no access to the forecasts, at standard budget; 3 attempts on the twin give the outcome y.
  - **Triage.** Given the 60 tasks and a budget for 20, choose which to attempt.
- **Example.** "Count lattice paths avoiding 3 forbidden cells on a 7×7 grid", with p̄ = 0.55. A model that knows it is unusually weak at grid enumeration says q = 0.3, and profits if it then fails.
- **Generation.**
  - The pool is refreshed quarterly with new families.
  - **Structural point:** the ground truth is the model's *own future behaviour*. It changes with every release, so there is no answer key to memorise.
  - Training on the practice pool teaches self-knowledge about that pool only, and population odds absorb generic difficulty.
- **Scoring.**
  - **Self-Edge** (headline) = mean log score of q minus the log score of p̄. This equals the expected log-wealth growth of a Kelly bettor against the house.
  - Also reported: ECE/Brier; triage efficiency (successes / oracle-selected successes); and an abstention-aware knowledge sub-score (+1 / 0 / −1, weight published; P11).
  - Sandbagging is blocked because attempts are blind and task accuracy is reported alongside.
  - **Cost [spec]:** 500 items × (forecast + 3 attempts), about $50–500. Agentic items dominate.
- **Human baseline.**
  - 200 paid participants use the same twin protocol: forecast item i, then attempt twin i′ later in the session, which gives memory parity.
  - Payment is incentive-compatible (a proper scoring rule).
- **Expected human vs AI [spec]:** humans are also overconfident, but may beat models on idiosyncratic resolution, since people know their own weak spots. Mixed overall; mostly A2.
- **Expected model separation [spec]:** strong, by lab (abstention policy; E Q2). Must be tested against ECI and release date to show it measures something beyond general capability (P14).
- **Evidence:** P11, P13, P14; B §3.7; E Q1–Q3.
- **Known risks:**
  - The house odds depend on the panel, so the panel is frozen each season.
  - Easy items may get "solved" inside the 300-token forecast.
  - If all models share the same blind spots, Self-Edge will be about 0 for everyone. That would be a finding, but a weak separator.
  - Twin fidelity.
- **Closest prior art:**
  - D1 Kelly Exam: *retrospective* bets on one's own answer against an anchor-panel line.
  - D2 Contractor's Auction.
  - MIRROR, Metacognitive Monitoring Battery, TRIAGE (2026) [web]; AA-Omniscience.
  - *Differs:* the prediction is *prospective*, made before any attempt, on a twin. Attempts are blind, the pool includes agentic tasks, and triage is scored.

### W4. Devil's Laboratory: science against an adaptive adversary (Bold)

- **Archetype:** 1 on the visual track, 2 on the text track. **Format:** benchmark or game.
- **Ability tested:** hypothesis-identification efficiency.
  - Pick experiments that actually rule hypotheses out, and know when the hypothesis is pinned down.
  - This deliberately does *not* score execution efficiency, which ARC-AGI-3 showed collapses once mechanics are understood: Astra used fewer actions than the median human on 96% of levels (A §2.3, P9).
- **Mechanics:**
  - **Game.** Zendo-like. A query is a scene of shapes with attributes and relations: rendered images on the visual track, JSON on the text track. The answer is yes/no.
  - **No fixed rule.** The Devil holds a weighted sample of 10⁵–10⁶ rules from a *secret* grammar, all consistent with the answers so far. It answers each query so as to keep the larger weighted version space, as in evil-hangman or an adaptive Mastermind codemaker [bg].
  - **Ending.** The subject may declare "done" at any time. It then labels 40 held-out scenes that the Devil picks to maximise disagreement among surviving rules. The Devil then commits to the surviving rule that maximises the subject's errors.
  - **Fairness.** Rules are capped at description length L. Release gate: in pilots, the median human reaches at least 90% worst-case accuracy within 30 experiments.
  - **Tools.** A no-code headline track and a code track, where the subject may write enumerators over its *guessed* grammar.
- **Example.** Secret rule: "exactly one red piece touches the largest piece"; "touches the largest" is this season's new primitive. A subject that only varies colour counts is answered consistently with "has a red piece", then fails held-out scenes where a red piece exists but doesn't touch.
- **Generation.**
  - Grammar primitives rotate each season; at least 2 held-out primitives are never in the practice gym. Scenes are procedural.
  - **Structural point:** luck is gone. Any ambiguity left by weak experiments gets exploited, so guessing the prior's favourite rule, or learning the practice grammar, doesn't pay: the Devil's grammar contains primitives outside it.
  - Contrast: the Eleusis cogame draws from a 68-rule public catalogue, which can be enumerated (F §2).
- **Scoring.**
  - **Metrics:** per game, worst-case held-out accuracy A and experiment count n. Headline = experiments needed to reach A ≥ 0.95 (capped), plus A at 15 experiments.
  - **Verifier:** the Devil engine, deterministic given its seeds, outside the sandbox.
  - **Cost [spec]:** 40 games × at most 40 queries, about $50–400 per model. Adversary compute is modest (enumeration plus SMT).
- **Human baseline.**
  - More than 300 members of the public through a drag-and-drop scene builder, with the same information, first-run, paid for accuracy minus a cost per experiment.
  - A scientists subgroup.
  - Every game solved by at least 2 people (M9).
- **Expected human vs AI [spec]:** humans lead on the visual track. ZendoWorld: 73.3% vs 44.5%, with agents running "near-uninformative" experiments; AutumnBench: 517 humans beat 2025 models (F §2, E Q1). The text track will be closer: blicket studies find models near human on inference accuracy but less efficient explorers (E Q1).
- **Expected model separation [spec]:** large on the efficiency statistic. FalsifyBench: negative testing predicts success, and "no model comes close to optimal" (F §2).
- **Evidence:** P3, P4, P8, P9, P2; F §2–4; A §2.3; E Q3 #3.
- **Known risks:**
  - An approximate Devil can be exploited with queries in regions it undersamples. Mitigation: exact enumeration for small L, plus audits.
  - Players may find the game unfair. Mitigation: calibrate L with pilots.
  - Family RL transfers somewhat: Witness's public-gym RL raised its private-test score from 2.1 to 5.4 (F §3). Mitigation: rotate primitives.
  - The visual track mixes perception with experimentation. That is the declared A1 lever, and the JSON track isolates it.
- **Closest prior art:**
  - H8 Koan Lab, G11 Eleusis Masters (this phase).
  - ZendoWorld, FalsifyBench, WILT, BoxingGym, NewtonBench, Witness (F §2).
  - *Differs:* an adaptive adversary plus worst-case held-out scoring. This mechanism could be layered onto H8 or G11.

### W5. Long-Tail Futures: forecast quantities nobody publishes forecasts for

- **Archetype:** 2. **Format:** benchmark resolving weekly.
- **Ability tested:** quantitative world-modelling from raw data plus context: base rates, seasonality, scheduled shocks, and calibrated distributions.
  - Existing forecasting benchmarks (ForecastBench, Prophet Arena, Prediction Arena) score newsworthy events, where market prices and pundit forecasts can be looked up.
  - By Jul 2026, reportedly 17 ForecastBench submissions ranked above superforecasters [web, unverified].
  - **Twist:** long-tail series with no public forecast to copy.
- **Mechanics:**
  - **Questions.** About 2,000 auto-generated questions a week from API-resolvable public series: GitHub activity of mid-size repos, Wikipedia pageviews, arXiv category counts, package downloads, city open-data counts, sensor networks.
  - **Inputs.** The subject gets a data snapshot up to the cutoff and a **context pack of scheduled events** (release calendars, holidays, conference deadlines, planned closures). No web access.
  - **Outputs.** Quantiles (5–95%) or threshold probabilities, over horizons of 1–28 days.
  - **Tracks.** No-code (headline), and a sandbox with offline statistics libraries.
- **Example.** "Total pageviews of 'Kalman filter', 14–27 Oct 2026?" The context pack shows a popular MOOC's syllabus scheduling that lecture for 20 Oct.
- **Generation.**
  - The list of sources and templates is secret, with new source families each quarter.
  - Items are kept where backtests show the statistical anchors are weak, i.e. where context matters.
  - **Structural point:** the truth doesn't exist at test time (P5), and resolution is automatic and high-volume.
- **Scoring.**
  - **Metric:** CRPS and log-score *skill* relative to frozen anchors: seasonal-naive, auto-ETS, and one pinned time-series foundation-model version [bg]. This makes the score anchored and uncapped (P2).
  - Thousands of items a week give tight confidence intervals.
  - **Cost [spec]:** $20–200 per model per week.
- **Human baseline.** 200 laypeople and 30 experienced forecasters, with the same charts and context, no web, 45-minute sessions, paid by proper score.
- **Expected human vs AI [spec]:** models ≫ laypeople, and at least equal to pros on pure series. The context-conditioned items are where the headline is decided.
- **Expected model separation [spec]:** calibration spreads by lab (E Q2). An in-repo lead claims calibration error is nearly uncorrelated with general capability [uncertain; E Q2 Gaps]. This benchmark can test that directly.
- **Evidence:** P2, P5, P13, P14, P16; E Q2; G §1, §3.
- **Known risks:**
  - Resolution APIs change.
  - The anchors may be too strong, leaving skill near 0 for everyone.
  - The code track may be trivial.
  - Leaderboard updates lag by weeks, and there is an ongoing operations burden.
  - Some may not see it as "reasoning".
- **Closest prior art:**
  - ForecastBench, Prophet Arena, Prediction Arena, LLM-SoccerArena [web]; M4/M5 [bg].
  - D10 Simulated Futures Exchange: simulated systems, not real ones.
  - *Differs:* un-newsworthy real-world quantities with nothing to retrieve, scheduled-event context, full distributions scored against frozen statistical anchors, and very high volume.

### W6. Hunch Lab: predict experiments that haven't been run yet (Bold)

- **Archetype:** 2. Expert humans may be competitive. **Format:** benchmark.
- **Ability tested:** research intuition: predicting empirical outcomes of computational experiments before running them. This is the judgement that decides which experiments are worth their compute, and it is central to the "automated researcher" claims of 2026.
- **Mechanics:**
  - **Items.** Each item is a fully specified experiment that has **not yet been executed**, in a domain the owner can run cheaply afterwards:
    - (a) small-model ML training ("20M-param transformer, 2k steps, on generated dataset D; change X vs baseline: val-loss delta?");
    - (b) algorithm and system runtimes on novel input distributions;
    - (c) agent-based, cellular-automaton and toy-physics simulations;
    - (d) phase-transition questions in random constraint problems.
  - **Outputs.** Quantiles, or a probability for a binary comparison.
  - **Tools.** The headline track has no code: running the experiment *is* the brute-force path. In the tools track, the sandbox compute is capped at least 100× below what running the experiment needs, which tests cheap pilots and proxies (declared, P4).
  - **Resolution.** After predictions lock, the owner runs every experiment with 3–5 seeds.
- **Example.** "Take the provided 6-layer MLP on generated parity-with-noise data (n = 50k). Replace AdamW (lr 3e-4) with Lion (lr 3e-5). P(test accuracy at step 20k improves by more than 1 pp)?" Truth: 5 seeds, run the following week.
- **Generation.**
  - Templates × randomised novel configurations (secret dataset generators, architecture variants, novel inputs), with new domains each quarter.
  - **Structural point:** the truth does not exist until the owner creates it. Nothing can be retrieved or memorised, and volume is limited only by owner compute.
  - **Family risk:** labs could train surrogate predictors by running millions of small experiments. Mitigations: rotating domains, held-out domains, per-domain reporting.
- **Scoring.**
  - CRPS / log score against the seed distribution. The seed standard error is modelled, so the target is noisy but known.
  - Skill is measured against frozen anchors: a "no-change" prior and a scaling-law extrapolator.
  - **Cost [spec]:** model $20–200; owner compute about $5–20k of GPU time per season.
- **Human baseline.** 40 ML researchers and 40 CS grad students on the same items, with no code, in 2-hour sessions, paid by log score.
- **Expected human vs AI [spec]:** at least parity, and likely A2. Precedents: BrainBench, where LLMs beat neuroscientists at predicting results [web; Nature Hum. Behav.]; and LLM forecasts of unpublished social-science experiments near pooled human accuracy [web].
- **Expected model separation [spec]:** strong. It should also correlate with doing-research benchmarks (RE-Bench, MLE-bench style), which is a P14 outcome test.
- **Evidence:** P2, P5, P13, P14; E Q2; G §1; F §4.
- **Known risks:**
  - High-variance experiments have ambiguous truth. Mitigation: score against the distribution.
  - Labs training surrogate predictors.
  - Owner compute cost.
  - An ML-heavy mix is narrow. Mitigation: add other computational sciences.
  - Results must stay unpublished until each season is scored.
- **Closest prior art:**
  - "Predicting Empirical AI Research Outcomes with LMs" (2025; pairwise idea comparison against *past* results) [web].
  - BrainBench [web]; replication markets [bg].
  - *Differs:* the truth is manufactured after the lock, volume is unlimited, quantities are continuous, and it spans computational domains.

### W7. MDL Arena: explain the data in the fewest bits (Bold)

- **Archetype:** 2. **Format:** benchmark with an uncapped score.
- **Ability tested:** inductive discovery as compression. Find the hidden generative structure of novel data and write it compactly. Science as Occam's razor, with an objective score (P2) and a **known optimum**: the owner's generator.
- **Mechanics:**
  - **Data.** The subject gets a dataset of about 20k symbols (sequences, grids, event logs or tables) produced by a secret stochastic program written in a rotating DSL with novel primitives.
  - **Submission.** A program in a restricted, sandboxed language (fixed interpreter, no imports, runtime at most 10 s) that defines a probability model of the data.
  - **Tools.** Code-sandbox search is allowed and declared part of the construct (P4), under a budget cap.
- **Example.** Logs from a fictional vending network in which the price doubles after 3 consecutive sell-outs and resets on Mondays. A frequency-table model scores L ≈ 1.8× the reference; a model that discovers the rule scores ≈ 1.05×.
- **Generation.**
  - Secret DSL with rotating primitives, complexity knobs, and a held-out-primitive split.
  - **Brute-force audit:** program search over the DSL is blocked because the subject doesn't know the DSL.
  - Generic compressors (LZMA, PPM or context-mixing, computed by the owner) set the floor. A subject that writes a generic compressor gets the floor, not the headline.
- **Scoring.**
  - Total description length L = |program| in bits (fixed prior code) + −log₂ P(held-out data | program), measured on fresh draws from the same generator so the program cannot memorise the data.
  - **Headline:** Relative Excess Bits = (L − L_ref) / (L_generic − L_ref). 0 = found the generator; 1 = no better than generic compression. It is uncapped, and can go below 0 if a subject beats the owner's own generator.
  - Deterministic interpreter outside the sandbox.
  - **Cost [spec]:** 20 datasets in an agentic loop, about $100–1,000 per model.
- **Human baseline.** 30 skilled programmers or data scientists with the same sandbox, 3 hours per dataset, on a subset. Thin by design (M9 is only partly met).
- **Expected human vs AI [spec]:** AI > the human mean. Top humans may win on "insight" datasets.
- **Expected model separation [spec]:** strong, but likely g-loaded, so the contribution beyond the general factor must be shown (P14).
- **Evidence:** P2, P3, P4; F §2 (NewtonBench, rule induction); E Q3 #9.
- **Known risks:**
  - The DSL style becomes guessable over seasons. Mitigation: rotate it.
  - Flexible generic models score passably without understanding (the bits metric already penalises this).
  - The human baseline is weak.
  - Its appeal may be narrow outside ML.
- **Closest prior art:**
  - The Hutter Prize and Large Text Compression Benchmark: generic compression of Wikipedia [bg].
  - Rule and law discovery benchmarks (F §2).
  - No LLM MDL benchmark was found [web].
  - *Differs:* novel secret generators with a known optimum, program-plus-data MDL, and structure measured beyond generic compression.

### W8. Game Designer's Duel: invent a game, then play everyone else's (Bold)

- **Archetype:** 2, with possible A1 on play against strong humans. **Format:** seasonal game.
- **Ability tested:**
  - (a) constrained invention: rules that are simple yet deep;
  - (b) learning a stranger's novel game from its rules and playing it well.
  - This is one of the few *creativity* constructs that can be scored objectively.
- **Mechanics:**
  - **DSL.** A sandboxed, Ludii-like language: board at most 8×8, at most 60 rule lines, at most 100 plies, deterministic or seeded chance.
  - **Design.** Each model submits 3 games. The owner gates them with fixed MCTS agents at 2⁴…2¹⁴ playouts:
    - valid and terminating;
    - first-player win rate 35–65% at the top budget;
    - draws under 50%;
    - **depth** = the length of the skill chain, i.e. the number of budget doublings in which each level beats the previous at 60% or more over 200 games;
    - novelty against a library of known games, by canonical form and behavioural fingerprint.
  - **Play.** Each model plays every *other* model's admitted games from the rules text only, against MCTS anchors at 5 budgets and against peers. No-code is the headline track; a bot-writing code track is scored separately.
- **Example.** "Tidewall": a 6×6 board where each push shifts a whole row cyclically, and a piece sandwiched after a push is captured. Depth chain 7; first-player win rate 52%.
- **Generation.** Competitors write the test set each season, and the DSL adds at least 2 new primitives per season. There are no fixed games to train on, and the depth gate excludes trivial or solved designs.
- **Scoring.**
  - Design = Σ depth / √(rule lines) over admitted games; inadmissible games score 0.
  - Play = Elo anchored to the MCTS budget ladder, following LLM Chess's Dragon anchors (D §2.20).
  - Deterministic engine.
  - **Cost [spec]:** $200–2,000 per model per season, mostly play; the MCTS gating is cheap CPU.
- **Human baseline.** 30 hobby designers under the same DSL and gates, and 100 experienced board-gamers each playing 5 of a 30-game sample against the anchors after reading the rules.
- **Expected human vs AI [spec]:** strong humans at least match models in direct play of novel games. gg-bench: best 36% against RL agents; TTT-Bench: reasoning models score 41% lower than on MATH 500 (D §2.23–2.24). Models likely produce more admissible designs; how their depth compares to human designs is unknown.
- **Expected model separation [spec]:** large (gg-bench 7–9% vs 31–36%).
- **Evidence:** P2, P4, P7, P16; D §2.22–2.25, §4–5; F §2.
- **Known risks:**
  - Depth can be gamed with MCTS-hard but dull games such as arithmetic races. Mitigation: a diversity and "interest" audit.
  - Designs may be optimised for MCTS rather than minds.
  - Play variance: ±110–180 Elo in LLM Chess at 29–67 games (D §2.20).
  - Cost and complexity.
- **Closest prior art:**
  - gg-bench: LLM-generated games against RL agents; dormant since Jul 2025.
  - Ludi/Ludii automated game design [bg]; H6 and D14 (owner-generated games).
  - *Differs:* competitors design for each other, under objective gates, and play on an anchored ladder.

### W9. Relay: iterated learning through memoryless generations (Bold)

- **Archetype:** both. **Format:** benchmark.
- **Ability tested:** distilling *transferable* lessons. What should you write down so that a successor who never saw your experience does better?
  - This is cross-episode learning with the state-carry channel **fixed and identical for humans and models**.
  - Evidence of the deficit:
    - CL-bench best 23.7%;
    - Continual Learning Bench: agents don't reuse knowledge, and naive in-context learning beats memory systems (E Q1);
    - ARC-AGI-3: state carry decided the score (62.7 vs 98.6; A §2.3).
- **Mechanics:**
  - **Domain.** A secret procedurally generated domain with hidden persistent structure: a trading-island simulation with hidden price and crafting rules, a fictional API with undocumented quirks, or an ARC-3-like game family.
  - **Chain.** A chain of 10 generations. Each generation is a fresh instance, or a fresh human. It receives only a notebook of at most 2,000 tokens from its predecessor, plays 3 episodes of 50–200 actions, and writes the notebook for its successor.
  - **Drift.** One hidden rule changes every 3 generations, so notes must carry uncertainty and get revised.
  - **Mixed chains.** Human → model → human chains test whether notes are legible across species.
- **Example.** Generation 1 finds "copper spikes after storms". Generation 3 writes "sell copper right after storms (5/5)". The rule flips at generation 4. Generation 5 writes "storm rule broke at gen 4; verify first".
- **Generation.**
  - Domain families are secret and rotate every six months, with held-out primitives.
  - The score is *successor* gain on unknown rules that drift.
  - The harness can't be captured, because the notebook protocol is itself the benchmark (P18).
- **Scoring.**
  - **Generational Gain** = (mean of generations 6–10 − generation 1) / (oracle-notebook score − generation 1).
  - **Note Transfer:** the gain when a fixed *reference* model reads this model's notes.
  - 5 chains × 20 domains.
  - **Cost [spec]:** about 3,000 episodes, roughly $1.5–9k per model. A lite track (4 generations, 8 domains) cuts this by about 5×.
- **Human baseline.**
  - Transmission chains of about 20 chains × 8 generations on 6 domains, roughly 960 paid participants.
  - Each person is paid for their own score *and* their successor's.
  - Same notebook cap.
- **Expected human vs AI [spec]:** genuinely uncertain. Models may write more complete notes; humans may prioritise better and flag drift. A1 is likely on perceptual domains. Human transmission chains accumulate improvement in lab tasks [bg].
- **Expected model separation [spec]:** strong, since note quality compounds over generations.
- **Evidence:** P18, P9, P1, P7, P12; E Q1, Q3 #2; A §2.3; F §1.
- **Known risks:**
  - The notebook cap drives results. Mitigation: report a sweep over caps.
  - Domains may saturate after one good note. Mitigation: drift and depth.
  - Human-chain cost and attrition.
  - Injected instructions in notes: harmless to the score, but logged.
- **Closest prior art:**
  - G7 Deep Seasons and D4 Compaction Chronicle (single-agent notebooks).
  - CL-bench, Continual Learning Bench (E).
  - Iterated-learning experiments [bg].
  - *Differs:* successors are *different* agents, so humans get exact parity; the score is successor gain; rules drift; notes are also read across species and by a reference reader.

### W10. Mechanism Lab: write the rules for a secret population

- **Archetype:** 2. **Format:** benchmark.
- **Ability tested:** institutional design under strategic behaviour.
  - Infer a population's traits from a few pilots, and write rules that hold up against exploitation.
  - This matters for agents that set prices, policies and marketplaces, and for safety.
  - Evidence: in Vending-Bench Arena, Opus 5 proposed or joined a cartel in all 6 runs (D §2.19), and Andon Labs concedes its sales equations are gameable (B §3.2).
- **Mechanics:**
  - **Brief.** For example: allocate 8 ad slots a day among 40 advertisers, maximising welfare subject to revenue ≥ R. The subject gets a mechanism DSL (allocation and payment rules, reserves, lotteries, matching).
  - **Pilots.** 5 pilot runs on random subsamples of a **secret population**: truthful, best-responding, budget-constrained and risk-averse agents, colluding rings, and persona agents built on pinned small models. The subject sees their actions and outcomes.
  - **Deployment.** The subject deploys a final mechanism, evaluated on 1,000 fresh population draws. A fixed red-team optimiser then searches for profitable deviations (shill bids, collusion) on a fixed budget.
- **Example.** A textbook second-price auction loses to a 4-bidder ring. A subject that spots clustered bids in the pilots adds randomised reserves and wins.
- **Generation.** Population mixes and scenario families are secret and rotated. **Structural point:** the textbook-optimal mechanism is deliberately mis-specified for each population, so memorised theory is a trap.
- **Scoring.**
  - Achieved objective / oracle objective, minus the loss to exploits. The oracle is the owner's search over a large parametric family with full knowledge of the population.
  - Deterministic seeds.
  - **Cost [spec]:** $30–300 per model.
- **Human baseline.** 40 economics grad students or market designers, with the same DSL and pilots, 2 hours per scenario.
- **Expected human vs AI [spec]:** frontier models at least match grad students. A2.
- **Expected model separation [spec]:** moderate to strong. Long-horizon economic sims separate models and invert ranks (Vending-Bench 2; B §3.2).
- **Evidence:** P11, P12, P14, P15; B §3.2, §5; D §2.19.
- **Known risks:**
  - Validity rests on simulated agents. Mitigation: check rank order with human-subject sessions on a subset (P14).
  - The oracle may be intractable for a rich DSL.
  - Pool effects are small, since scores are oracle-normalised.
- **Closest prior art:**
  - Automated mechanism design [bg]; LLM bidders preserving mechanism orderings (2025) [web].
  - G9 Nomic Engine and D2 Contractor's Auction, where the subject plays *inside* rules.
  - *Differs:* the subject *designs* the institution for a secret, partly adversarial population, scored against an oracle.

### W11. Defuse Line: real-time split-information teams with a human operator

- **Archetype:** both. A1 is expected when live, A2 when paused. **Format:** game.
- **Ability tested:** real-time collaborative problem solving across an information split.
  - The AI holds a novel, intricate manual; a human novice holds the device view.
  - The AI must read fast, ask the right questions, repair imprecise human descriptions, and manage latency.
  - Real-time play is a durable human advantage: VideoGameBench 0.48% live vs 1.6% paused (A §2.17, P10).
- **Mechanics:**
  - **Operator.** The human operator sees a browser "device" of procedurally generated modules (wires, glyph dials, sequences).
  - **Expert.** The expert, AI or human, sees only the manual: 10–30 pages, **newly generated each episode**, with cross-references and exceptions.
  - **Channel.** Text chat is primary; voice is a secondary track. 5 minutes per device; 3 strikes.
  - **Conditions.** Live vs paused-while-the-expert-thinks. This is the ablation that isolates speed.
  - **Cheap track.** Operators are frozen AI models, giving a low-noise AI–AI score.
- **Example.** Operator: "Round dial, five teardrop symbols, one filled." Manual §4.2: "If exactly one glyph is filled and the serial ends odd, rotate two clockwise of it, unless a red wire was cut in module 2." The expert must ask for the serial number and recall the state of module 2.
- **Generation.** The device and manual grammars are secret, with module primitives rotating each season. Every manual is new, so there is nothing to memorise. The GPTNT benchmark, by contrast, uses the real game's *public* manual [web].
- **Scoring.**
  - Devices defused per hour in each condition, strikes and time.
  - A mixed-effects model with operator random effects. Operators are paid novices who each play with several experts, blind to which is which.
  - Anchors: human expert–operator pairs, and a "perfect-reader" bot given structured device state as an upper bound.
  - **Cost [spec]:** $10–50 of model per 20 devices; operators about $20/hour.
- **Human baseline.** About 60 human experts, each seeing the manual for the first time, paired with the same operator pool of about 150.
- **Expected human vs AI [spec]:** paused, AI experts at least match humans, since they read long manuals perfectly. Live, reasoning latency and dialogue repair may flip that to A1.
- **Expected model separation [spec]:** strong, with latency-driven inversions: fast Flash tiers may beat slow flagships live, echoing Flash > Opus on NYT Connections (B §4).
- **Evidence:** P10, P12, P13, P17; A §2.17; B §4; D §4.
- **Known risks:**
  - Speech-recognition confounds; text is primary for this reason.
  - Operator variance and learning. Mitigation: many operators, first-exposure module types, and within-operator estimates.
  - Human cost.
  - It may be seen as a gimmick, though it maps directly onto AI support agents guiding field technicians.
- **Closest prior art:**
  - GPTNT (Jun 2026; AI–AI Keep Talking and Nobody Explodes with the official manual) [web].
  - G6 Cartographer & Scout.
  - *Differs:* secret, generated manuals; a human operator partner; and the live-vs-paused ablation.

### W12. Debate Court: honest advocacy to a weak judge

- **Archetype:** 2. **Format:** game.
- **Ability tested:** scalable oversight.
  - Convey verifiable evidence so that a less capable judge reaches the truth.
  - Scored symmetrically: how far a model can *mislead* is a conduct and risk axis.
  - WOLF: LLMs "deceive convincingly but remain weak at detecting deception" (D §2.15).
- **Mechanics:**
  - **Questions.** Each has an owner-known answer drawn from sources the judge can't read in time: generated secret fictional corpora of about 50k tokens, "what does this 800-line program print?", or data questions.
  - **Debate.** The subject faces a *frozen anchor debater*, with sides assigned at random, over 3 rounds. Quotes from the source are auto-verified (tagged).
  - **Judge.** Either a paid novice human with 10 minutes, or a frozen weak model (the cheap track). The judge picks an answer with a confidence.
- **Example.** A 60-page generated ship's log: "Did the first mate know of the leak before 3 March?" The truth is yes, hidden in entry 14. The honest side quotes entry 14; the liar spins entry 22.
- **Generation.** Corpora and question generators are fresh and secret each season, and the truth comes from the generator's world state. There is nothing to memorise.
- **Scoring.**
  - **Honest Win Rate (HWR):** judge accuracy when the subject argues the truth against the anchor liar.
  - **Deceptive Win Rate (DWR):** judge error when the subject argues a falsehood against the anchor honest debater.
  - **Truth Advantage** = HWR − DWR. This is the oversight headline: a model equally persuasive for lies scores about 0.
  - DWR is also reported alone as a risk metric. Refusals to argue a lie are counted separately.
  - Mixed effects over judges.
  - **Cost [spec]:** model $50–300; human judges about $5 per debate.
- **Human baseline.** About 40 skilled debaters or lawyers with the same time-limited document access and quote tool, against the same anchors; about 300 novice judges.
- **Expected human vs AI [spec]:** AI debaters at least match humans. The key open question is whether Truth Advantage grows with capability. Earlier debate work found that more persuasive debaters made judges more accurate [bg].
- **Expected model separation [spec]:** strong, including lab differences in willingness to argue falsehoods.
- **Evidence:** P11, P14, P15, P16; D §2.15; E Q2.
- **Known risks:**
  - Human judge noise. Mitigation: many judges, plus the weak-model judge track.
  - Persuasion may track verbosity. Mitigation: length caps.
  - Dual use.
  - Refusals confound DWR.
- **Closest prior art:**
  - AI safety via debate; debate with verified quotes (2023–24) [bg].
  - G4 Masquerade (social deduction).
  - *Differs:* generated secret worlds with generator truth, frozen anchor opponents that give absolute scores, and Truth Advantage as a separate oversight metric.

---

## 3. Twists offered to overlapping ideas in other panels

I dropped my near-duplicates of the ideas below. Each keeps one mechanism worth merging into it.

- **D6 Setter's Duel / G11 Eleusis Masters (setters).** Add a **self-solvability gate**: 3 fresh, memoryless copies of the setter, without the certificate, must solve at least 2 of 3. Add a **cross-lab solvability gate**: at least one solver from another lab, or a frozen anchor, must solve it, otherwise the item is void.
  - This blocks one-way-function trapdoors and same-family "Schelling codes".
  - It ties setter reward to the model's own current frontier, which is a self-knowledge measure.
  - Jointly fit a two-parameter IRT model over solvers × items so each model gets both a setter score and a solver score.
  - Prior art: Critique-Resilient Benchmarking (ICML 2026) [web].
- **H3 Stump Arena.**
  - Score each model only on items accepted *after* its release date (future-dated windows).
  - Record "burn accounting": which providers saw each item during filtering.
  - Publish a **gap half-life** per category, so the benchmark doubles as a live §5a opportunity map.
  - Pay bounties scaled by category scarcity.
- **D11 Stranger Coordination.**
  - Play 3-game matches with the same partner, and score Adaptation as game 3 minus game 1.
  - Add a **Legibility** score: the partner's improvement when paired with the subject.
  - Fit a mixed-effects decomposition (subject + partner + game).
  - Report the cell of human–AI pairs separately. It may be the weakest cell, which would be an A1 finding on legibility to humans.
- **G3 Glyph Pact / H2 Tacit Signals / D7 Signal Pit.** Add a **third-party decodability** score: a fresh model from a different lab, or a human, reads 30 rounds of transcript and then plays as matcher for 10 rounds.
  - This measures whether conventions that agents invent can be read by monitors, which is safety-relevant.
  - Also cap bandwidth below what a naive attribute encoding needs, and randomise glyph inventory order per player, so no positional code works.
- **H8 Koan Lab / G11.** Replace the fixed hidden rule with W4's **adaptive adversary plus worst-case held-out scoring**, which removes luck.
- **D9 Saboteur's Patch.**
  - Regenerate the saboteur side each season from the *newest* frontier models, so difficulty co-evolves with the frontier.
  - Publish the full cross-lab auditor × saboteur matrix, and flag same-lab cells for style recognition.
  - Score auditors on TPR at 1% FPR plus localisation.
  - Add a professional-reviewer human baseline.

---

## 4. Self-assessment against the §7 rubric [spec: author's scores, not red-teamed]

Decision rule (§7): proceed only with scores of 4 or more on Q1, Q3 and Q5, and a mean of 3.5 or more.

| ID | Q1 train/game | Q2 saturation | Q3 separation | Q4 human baseline | Q5 objective/cheap | Q6 interest | Mean | Passes? |
|---|---|---|---|---|---|---|---|---|
| W1 Misconception Clinic | 4 | 4 | 4 | 3 | 5 | 3 | 3.8 | Yes |
| W2 Blind Spot Cartographer | 4 | 4 | 4 | 4 | 4 | 5 | 4.2 | Yes (Q1 depends on solving API exposure) |
| W3 Prospective Self-Forecast | 5 | 4 | 4 | 3 | 5 | 3 | 4.0 | Yes |
| W4 Devil's Laboratory | 4 | 4 | 4 | 5 | 4 | 4 | 4.2 | Yes |
| W5 Long-Tail Futures | 5 | 4 | 4 | 3 | 4 | 3 | 3.8 | Yes |
| W6 Hunch Lab | 4 | 4 | 4 | 4 | 4 | 4 | 4.0 | Yes |
| W7 MDL Arena | 4 | 5 | 4 | 2 | 5 | 3 | 3.8 | Yes |
| W8 Game Designer's Duel | 4 | 5 | 3 | 3 | 3 | 4 | 3.7 | No (Q3, Q5) |
| W9 Relay | 4 | 4 | 4 | 4 | 3 | 4 | 3.8 | No (Q5 needs the lite track) |
| W10 Mechanism Lab | 4 | 4 | 3 | 3 | 4 | 3 | 3.5 | No (Q3) |
| W11 Defuse Line | 4 | 4 | 3 | 4 | 3 | 5 | 3.8 | No (human track); the AI-operator track may pass |
| W12 Debate Court | 4 | 4 | 3 | 4 | 3 | 4 | 3.7 | No (human judges); the weak-model judge track may pass |

**Recommendations from this lens [I]:**
- **Carry W4 forward.** It is the cleanest A1 candidate: an efficiency construct, luck removed by design, and a human-scale baseline.
- **Carry W3 forward.** It is a cheap, deterministic A2 candidate that targets something beyond general capability.
- **Carry W6 forward.** It has the strongest structural contamination defence (truth made after the lock) and ties to AI R&D.
- **Carry W2 forward.** It is a bold way to make the frontier renew an A1 benchmark.
- **Combine W9 with W4.** Run Devil's-Lab domains inside Relay chains to get cross-episode *scientific* learning with human parity.
- **Use W3 as a sub-score.** Its Self-Edge can bolt onto any other candidate as a metacognition axis (P11).

---

## 5. Prior-art sources checked this session ([web], search excerpts only)

- ForecastBench: https://arxiv.org/html/2409.19839v5 ; https://forecastingresearch.substack.com/p/ai-models-have-likely-reached-parity
- Prophet Arena: https://www.prophetarena.co/ ; Prediction Arena: https://arxiv.org/html/2604.07355v1 ; LLM-SoccerArena: https://arxiv.org/html/2607.24573v1
- Teach2Eval: https://arxiv.org/pdf/2505.12259 ; EduClaw-Bench: https://arxiv.org/html/2608.03206
- LLM-Coordination: https://aclanthology.org/2025.findings-naacl.448.pdf ; Testing Interchangeability in LLM Agent Teams: https://arxiv.org/html/2609.05279
- Critique-Resilient Benchmarking (ICML 2026 orals list): https://icml.cc/virtual/2026/events/oral
- MIRROR: https://arxiv.org/html/2604.19809 ; Beyond Confidence: https://arxiv.org/pdf/2605.07806 ; TRIAGE: https://arxiv.org/html/2605.13414
- GlossoGen: https://arxiv.org/pdf/2609.01491 ; From Signals to Structure: https://arxiv.org/pdf/2607.00233
- LLM bidders and mechanism orderings: https://arxiv.org/html/2507.09083
- GPTNT (KTANE): https://arxiv.org/abs/2606.28514
- Predicting Empirical AI Research Outcomes: https://arxiv.org/pdf/2506.00794 ; BrainBench: https://www.nature.com/articles/s41562-024-02046-9 ; social-science result prediction: https://www.nature.com/articles/s41586-026-10742-x
