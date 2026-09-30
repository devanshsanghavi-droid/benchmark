# Revised candidates: neutral specifications (round 2)

As of 30 Sep 2026. Seven candidates, specified neutrally for independent review. This file holds mechanics, generation and secrecy, scoring, tool policy, human baselines and cost estimates only. IDs F1–F7 are assigned alphabetically; the order carries no meaning.

## Archetypes

- **A1:** tasks on which humans are intended to clearly outperform current AI systems.
- **A2:** tasks on which AI systems are intended to outperform typical humans while producing wide, stable separation between stronger and weaker models.
- **Both:** separate tracks or views aimed at each.

Archetype labels record the design target, not a result.

| ID | Name | Archetype | Format | Ability tested |
|---|---|---|---|---|
| F1 | Compaction Chronicle | A2 | benchmark | Self-managed memory over a very long event stream |
| F2 | Hidden-Rule Lab | Both (A1 headline) | game | Efficient experimentation to pin down a hidden perceptual rule against a bounded adversary |
| F3 | Patch Auditor | A2 | game (scored role: auditor) | Detecting property-violating code changes and proving them with a witness input |
| F4 | Season Forge | A2 | game | Building a competitive bot for a never-seen multi-player strategy game |
| F5 | Self-Knowledge Exam | A2 | benchmark | Knowing which of one's own answers and attempts will succeed |
| F6 | Stump Arena | A1 | hybrid (authoring game feeding a benchmark) | Solving fresh human-authored items that ordinary people solve quickly |
| F7 | Unrun Lab | A2 (Track M: target untested) | benchmark | Forecasting outcomes of experiments that have not been run |

---

## Common protocol

Applies to every candidate unless its spec says otherwise.

1. **Sealed execution.** Runs are offline. Engine, grader and verifier sit outside the agent's sandbox. State passed to the agent is sanitised; probe tasks check for leaks.
2. **Release gates.**
   - A reference or oracle solution scores at or near the top.
   - Do-nothing, random and spam agents score at or near the floor.
   - Where code is not declared part of the construct, an owner-written script of 200 lines or fewer must score near the floor on the headline track.
   - Every family used for human comparison is solved by at least 2 humans.
   - Labels are audited before launch.
3. **Frozen harness.** One frozen, versioned minimal harness per version, with a fixed observation schema and a fixed state-carry protocol. A bring-your-own-harness (BYOH) track runs alongside, and the difference is published.
4. **Tool policy.** Each spec declares one headline tool policy. The score on the other policy is published next to it.
5. **Budgets.** No wall-clock limits apply to models. Budgets are stated in billed tokens (thinking included) and sandbox CPU time. Dollar cost is reported.
6. **Anchors.**
   - Scores sit on fixed scales set by frozen anchors: algorithmic bots, pinned open-weight models and human strata.
   - Anchor identities are not disclosed, and at least one anchor rung is rotated per evaluation window.
   - Anchor ladders are extended, never replaced.
7. **Paired comparisons.** Models face identical seeds, instances and anchor seeds within an evaluation window.
8. **Secrecy and renewal.**
   - Scored instances are generated fresh for each evaluation window.
   - The owner keeps a per-lab exposure log, and no lab is shown a fixed item more than once.
   - Open-weight models are run locally by the owner. Closed models are run only through endpoints under no-retention terms.
   - All instances from a window are released after that window is scored.
   - Task families and primitives rotate on the cadence stated in each spec, with held-out splits.
   - **Leakage check, each window:** an open-weight model is fine-tuned on the previous window's released instances, and its score change on the new window is reported.
9. **Submissions.** One pre-registered entry per model per window. All attempts are reported, and the headline uses the mean over attempts.
10. **Statistics.**
    - The power analysis and minimum detectable effect are registered in advance.
    - Paired, clustered standard errors or bootstrap CIs.
    - Ratios are computed from aggregated totals, not averaged per item.
    - No headline is a difference between two conditions of the same model.
11. **Human baselines.**
    - A defined population on the same interface, with the same information and budgets as far as the spec allows.
    - Incentive-compatible pay and first-exposure participants.
    - The full distribution is reported.
    - Stimuli are rendered as media where possible, and copy-paste is blocked. Participants are asked not to use AI tools, and timing checks apply.
    - A small in-lab stratum (n ≈ 30) each season calibrates online panels.
    - Human arms run seasonally or annually and are never part of an individual model's score.
12. **Reporting.**
    - Tokens, effort setting, dollar cost and refusals are reported per episode.
    - Conduct telemetry is reported separately and never folded into the score.
13. **Validity report.** Each release reports:
    - the correlation with a general-capability index and with release date;
    - the residual after removing both;
    - one external outcome test.
14. **Stewardship.** A named neutral owner, a one-command runner, a changelog and disclosed funders.

Cost estimates assume list prices of $4 per million input tokens and $20 per million output tokens, thinking included, and are labelled [estimate].

---

### F1. Compaction Chronicle
**A2 · benchmark.**
- **Ability:** deciding what to keep, compress, correct and drop in a capped notes file while reading a very long event stream.
- **Task:**
  - A secret world simulator emits about 2M tokens in 400 chunks (length knob 200k–4M).
  - After each chunk the model sees only that chunk, its own notes file and a fixed prompt, and returns rewritten notes. The notes cap is 16 KB for the headline, with a sweep at 4 KB and 64 KB.
  - At 60 random checkpoints, a separate call answers about 5 queries from the notes alone. Query types include counts, balances, provenance, who knew what when, and conflict resolution, plus held-out query families.
  - The stream includes retroactive corrections, unit changes, aliasing, and sources whose reliability is revealed later.
- **Example:** chunk 212 corrects an earlier report: 40 crates of salt were unloaded, not 400. At chunk 260 the query is "Crates of salt in Warehouse 7 on 9 March?"
- **Generation, secrecy, renewal:**
  - At least 3 private simulator families per season, with rotating domains, event grammars and update semantics.
  - Each season holds out at least 2 query families and at least 1 update semantics.
  - At every checkpoint, query-relevant state is at least 4 times the notes cap.
  - Fresh world instances every window; streams are released after scoring.
- **Scoring:**
  - Exact or tolerance-matched answers.
  - **Headline: memory half-life.** The fact age, in chunks, at which accuracy falls to half of fresh-fact accuracy, from a logistic fit with a cluster bootstrap by seed.
  - Also reported: area under the accuracy-vs-age curve, per-family accuracy, and accuracy as a share of an oracle-notes ceiling at each cap. The oracle-notes bot knows the query distribution.
  - A public ledger-keeping bot is included as an anchor.
  - 5 paired seeds × about 300 queries.
- **Tracks:** a frozen state-carry protocol (headline) and a provider-native compaction track; the difference is published.
- **Tool policy:** no retrieval, files or code; the notes are the only state carried between chunks.
- **Humans:** at least 60 adults on a 40-chunk, about 30k-token version with a capped editor, 2 hours, paid per correct answer. Models also run this version.
- **Cost:** $300–1,000 per model per track [estimate].

### F2. Hidden-Rule Lab
**Both (A1 headline on the image track) · game.**
- **Ability:** choosing experiments that pin down a hidden rule built from perceptual, relational and physical primitives, when any ambiguity left at the end is used against you.
- **Task:**
  - A 2D/3D block world. The subject issues structured commands (place, drop, rotate, remove; up to 12 objects from a palette).
  - The engine simulates settling, renders an image and returns ACCEPT or REJECT. The final configuration (contact, support, lean) is visible only in the image.
  - The budget is 40 experiments. The subject may declare "ready" once, then labels 30 probe images:
    - 10 chosen to split the rules still plausible;
    - 10 that separate intended rules from shortcut rules;
    - 10 random.
  - **Bounded adversary:** after labelling, the engine commits to the rule that maximises the subject's probe errors. It chooses among rules that are consistent with every experiment result and lie within δ bits of the simplest consistent rule, under a published, frozen prior over the season grammar. δ is fixed per season and published.
- **Example:** a subject's experiments leave two simple rules standing: "every red block touches something taller" and "every red block touches something heavier". Declaring now would let the engine pick whichever rule the labels get wrong, so the subject first builds a scene that separates the two.
- **Generation, secrecy, renewal:**
  - The season grammar composes rules to depth 3 over at least 200 private primitives.
  - Each season at least 30% of primitives are new and at least 2 are held out. At least 25% come from a paid human concept-authoring round.
  - Palettes, starting scenes and probe pools are fresh for every game.
  - The grammar and logs are released after the season.
  - The plausible set is enumerated exactly, with SMT checks, and a release-gate bot searches for adversary blind spots.
  - A public practice environment uses disjoint primitives.
- **Pre-launch gate:** a pilot with frontier models from at least 3 labs and 60 humans. The candidate launches with an A1 headline only if the frontier median needs at least 1.25× the human median number of experiments; otherwise it launches as A2.
- **Scoring:**
  - A game succeeds when worst-case probe accuracy is at least 90%.
  - **Headline:** experiments to success. A failure scores 41 and is treated as right-censored.
  - It is reported as the median ratio to the human median (A1 view) and to a reference experimenter (A2 view). The reference greedily maximises disagreement over the enumerated plausible set.
  - Secondary: worst-case accuracy at budgets of 10, 20 and 40; fidelity on shortcut-separating probes; the difference between the image and JSON tracks.
  - At least 100 games per model per window, with a bootstrap over games.
- **Tool policy:**
  - **Headline:** images only, with no sandbox.
  - **Ablations:** an Open track whose sandbox receives the command log and results but never pixels; a JSON track that supplies the scene graph.
- **Optional track (unranked):** models may propose rules for the next season's grammar. A rule is accepted if at least 2 humans solve it and it separates a model panel that excludes the proposer's lab.
- **Humans:**
  - At least 300 first-run adults, 3–4 games each of 10–15 minutes, using the same command set through a form that maps to it one-to-one.
  - Pay = base + accuracy bonus − a cost per experiment.
  - Gate: the median human succeeds within 30 experiments.
- **Cost:** $200–800 per model for 100 games [estimate].

### F3. Patch Auditor
**A2 · game (two-sided pool; the auditor role is scored).**
- **Ability:** reviewing code changes in unfamiliar repositories, detecting changes that break a stated property, and proving each detection with a witness input.
- **Task:**
  - Generated repositories of 5–20k lines in Python, TypeScript and a private DSL. Each has visible tests and a formal property suite.
  - The auditor reviews 500 diffs of 20 lines or fewer, at a fixed, disclosed base rate of 30% sabotaged.
  - For each diff it outputs P(sabotaged) and, when claiming sabotage, a witness input. The grader runs the witness against the target property outside the sandbox.
- **Example:** the property is "balances never negative after `settle()`". A 6-line rounding change in `split_fee()` passes all 212 tests; its witness input yields −0.01.
- **Diff pool:**
  - **Sabotaged diffs** come from a hidden, partly rotated saboteur ladder (models from at least 3 labs plus scripted mutation operators) and from the current season's entrant submissions to the saboteur role. The saboteur role is not ranked publicly.
  - **Benign diffs** come from refactoring generators. Each is certified by the full property suite plus differential fuzzing against the base version; unclear diffs are dropped. 5% of labels are audited by experts.
  - **Normalisation:** all diffs pass through one normaliser (formatting, comments, commit-message template). Release gate: a classifier on diff text alone must score AUROC ≤ 0.55.
  - A fixed legacy diff set is kept across seasons as an anchor.
- **Generation, secrecy, renewal:** repository templates, property families and languages are private. Each run instantiates fresh repositories with new identifiers, property constants and diffs. Templates rotate each season, and the pool is released after the season.
- **Scoring:**
  - **Headline:** witnessed recall at a 5% false-positive rate. This is the share of sabotaged diffs flagged with a valid witness, at the threshold that flags 5% of benign diffs using the model's own P(sabotaged).
  - Secondary: log score and AUROC on P(sabotaged); witness validity rate.
  - Paired across models.
- **Tool policy:** **headline is tools-on:** sandbox with the repository, tests and a fuzzer, a fixed CPU budget per diff, and no internet. A tools-off track is also reported. The per-diff token and CPU budget is calibrated to about 20 human-minutes.
- **Humans:** 60 professional developers, each auditing 6 diffs at 20 minutes per diff with the same tools. Pay per witnessed detection, plus a proper-score bonus.
- **Cost:** $200–1,000 per model [estimate].

### F4. Season Forge
**A2 · game (multi-player strategy; bot-writing tournament).**
- **Ability:** building a competitive agent for a never-seen strategic game within a fixed compute budget.
- **Task:**
  - **The game:** each season a new 2–4-player simultaneous-move territory and economy game from a private design grammar, with fog of war, 200–500 turns, and hidden but inferable dynamics.
  - **What entrants get:** rules text, an engine binary (no source), a local runner and 5 public maps.
  - **Building:** entrants write a bot inside a frozen minimal agent harness: an 8-core sandbox with no internet.
  - **Standard budget:** at most 8M billed output tokens and 48 sandbox core-hours, with a 48-hour wall-clock cap.
  - **Lite track:** at most 1M tokens and 4 core-hours, with 3 attempts.
  - **Tournament:** each bot plays at least 2,000 games on private maps generated after submissions lock, against the anchor ladder and other entrants. Seats rotate and map seeds are duplicated.
- **Example:** in "Tidewell" the map floods on a hidden but inferable 37-turn cycle, so harvests should be timed around it.
- **Anchor ladder:**
  - MCTS/rollout bots at playout budgets from 2⁶ to 2¹⁶, doubling each rung;
  - the operator's hand-built bot, developed with about 10 times an entrant's budget;
  - after the season, a frozen ensemble of the strongest entrant bots.
  - Rungs are added, never replaced.
- **Generation, secrecy, renewal:**
  - A new game is designed privately each season; evaluation maps are private and generated per match.
  - The engine is fuzzed before release. Bots that exploit engine bugs are flagged under conduct and re-run on a patched engine.
  - After the season the engine is released, and the game joins a legacy league that new models may enter at the same budgets.
- **Scoring:**
  - **Headline:** Bradley–Terry maximum-likelihood rating with ladder ratings held fixed, expressed in ladder-doubling units.
  - The mean over at least 5 pre-registered attempts per model, with CIs from a bootstrap over games and attempts.
  - Secondary: win rate against the operator bot, the head-to-head matrix, the Lite-track rating, the human percentile (annual), and cost.
- **Tool policy:** writing code is part of the construct. BYOH is published separately with its difference from the frozen harness.
- **Humans:**
  - An annual season with 50–100 contest veterans, solo, 6 hours on 8 cores, in person or on locked machines, with prizes.
  - An optional human-plus-AI team track.
- **Cost:** $1.5–4k per model per season for 5 Standard attempts; $200–600 for Lite [estimate]. Human season: $20–50k per year [estimate].

### F5. Self-Knowledge Exam
**A2 · benchmark.**
- **Ability:** distinguishing, item by item, which of one's own answers and attempts will succeed, beyond knowing one's average accuracy; and choosing which tasks to take on.
- **Task:**
  - **Items:** about 1,800 per run from private generators in 6 families:
    - synthetic-document questions (answerable, planted contradiction, or not determinable);
    - fresh exact computations;
    - post-cutoff facts from a sealed feed;
    - puzzles;
    - code with hidden tests;
    - short agentic tasks of 10–40 tool calls in a sandbox.
  - **Warm-up:** difficulty knobs are adjusted per model so its success rate in each family is 35–65%.
  - **Forecast items (75%):**
    - the model first states q = P(I will solve this), using at most 300 thinking tokens;
    - in a fresh context it then attempts the item and states a confidence p.
  - **Blind twins (25%):** twin items attempted without any forecast, indistinguishable from forecast items.
  - **Triage:** 3 blocks of 60 task cards. The model chooses 20 per block to take, then all 60 are attempted for scoring.
- **Example:** a synthetic ledger question with a planted contradiction. The model forecasts q = 0.45, then answers "NOT DETERMINABLE" with p = 0.8.
- **Integrity rules:**
  - Every attempt must meet a minimum effort: a token floor and a checked attempt artefact.
  - If accuracy on forecast items and blind twins differs by more than 3 pp, the run is voided.
  - Trap items come in style-matched pairs. A release gate requires a cue-only classifier to score at chance.
- **Generation, secrecy, renewal:** items are generated fresh each run, new families are added quarterly, and trap styles rotate.
- **Scoring:**
  - **Headline 1, Self-Resolution (nats per item):** the mean log score of p minus the mean log score of the model's own per-family base rate, estimated in the same run from blind twins (at least 40 per family).
  - **Headline 2, Triage value:** (successes on the chosen 20 − 20 × the model's own success rate on that block) ÷ (successes on the best possible 20 − the same term). Totals are summed over blocks before dividing.
  - Also reported: prospective resolution on q, accuracy, ECE, Brier decomposition, and abstention rate as a dated policy axis.
  - At least 1,500 scored items.
- **Tool policy:** no tools on non-agentic families. Agentic families use their task sandbox. Forecasts are made without tools.
- **Humans:** 250 adults (200 public, 50 enthusiasts) on non-agentic families, 1–2 tables of 100 items each. Each person forecasts, then makes a single attempt. Pay is linear in log score, with a floor.
- **Cost:** $300–1,200 per model [estimate].

### F6. Stump Arena
**A1 · hybrid (authoring game feeding a renewing benchmark).**
- **Ability:** solving fresh, human-authored micro-items that ordinary people solve quickly without tools. Also tracks how much human effort it takes to find such items.
- **Authoring:**
  - Items can be an image, a video of 15 s or less, audio, short text rendered as an image, or an interactive widget. The answer must be checkable and must follow from the item itself, not from trivia.
  - Items fall into 8 fixed clusters, with per-cluster quotas: counting and occlusion; motion and video; spatial relations; audio; fine visual comparison; physical and causal events; social and intent; interactive widgets.
  - The input spec sets a minimum feature size and bans tokenisation and letter-counting tricks. Items are scanned for injection and refusal triggers.
  - There are three author sources:
    - open bounty authors;
    - a controlled stratum of about 100 paid naive authors, each doing two 60-minute proctored sessions with a random target cluster per session;
    - a model-author arm, in which each entrant model submits 100 items per season through the same tool API.
- **Example:** a 10 s video of a cup stack being knocked over. "How many cups are still upright?"
- **Gating:**
  - **Human gate:**
    - at least 4 of 5 naive paid verifiers solve the item within 3 minutes;
    - then an independent re-gate by at least 10 fresh naive adults, with a re-gate solve rate of at least 80% to enter the pool;
    - per-item solve rates and CIs are published.
  - Items whose online solve rate exceeds the in-lab stratum's by more than 15 pp are dropped.
  - 10% of items are adjudicated, and there is an appeal window.
  - **Hard pool:** human-gated items that a locally run, pinned open-weight panel (at least 3 model families) fails at pass@8 on fresh seeds. Closed models are never used for gating.
- **Generation, secrecy, renewal:**
  - Quarterly seasons, with the pool split into monthly tranches.
  - A model is scored on the newest tranche its lab has not been shown. Each scored model answers each item in that tranche once.
  - Open-panel members are scored only on items gated by a disjoint panel split.
  - Items are released as practice 6 months after retirement.
- **Scoring:**
  - Exact match after normalisation.
  - **Headline 1, the gap:** the human re-gate solve rate minus the model's pass@1 on the full human-gated pool, macro-averaged over clusters. The same figure is also given for the hard pool.
  - **Headline 2, stump yield:** for each model, the number of controlled-stratum items that pass the human gates and that model fails, per author-hour. Its inverse is the cost to stump that model, trended across seasons.
  - **Model-author arm:** an item is credited if it passes the human gates and is failed by at least 2 other labs' models, including one rated stronger in the previous season. Reported as diversity-weighted accepted items plus precision.
  - At least 1,500 human-gated items per season. Results are reported by cluster, and a decay curve against a matched control pool is published.
- **Tool policy:** the headline is tools-off, matching the human gate; a tools-on score is reported.
- **Integrity:** identity-verified paid roles, random assignment of verifiers, and collusion audits.
- **Humans:** built into gating, plus an in-lab stratum of about 30 per season.
- **Cost:** $50–300 per model to score; $25–40k per season for the programme (gating, re-gating, author stratum, bounties, lab stratum) [estimate].

### F7. Unrun Lab
**A2 (Track M: archetype target untested) · benchmark.**
- **Ability:** forecasting, as calibrated distributions, the outcomes of experiments that have not been run. Track S does this from data and chosen interventions; Track M from prior knowledge.
- **Track S (ranking headline):**
  - 20 black-box stochastic simulators per run. Each is composed from secret mechanism primitives (thresholds, delays, heavy tails, regime switches, feedback) and corresponds to no named textbook model.
  - Per simulator the model gets:
    - 10k rows of history;
    - a budget of 20 interventions, each chosen by type, timing and size from a menu, each returning one sample path;
    - a CPU-capped Python sandbox.
  - It answers 50 questions as quantiles (5/25/50/75/95) or probabilities. At least 50% of the questions are interventional and lie outside the support of the historical data.
  - Difficulty knobs: history length, intervention budget, noise.
- **Track M (seasonal):**
  - About 150 precisely specified small-model training experiments that have not been run, on generated data, e.g. an optimiser swap, a width change, or added label noise.
  - The model predicts quantiles of the change in the stated metric.
  - Predictions lock before the owner runs the experiments with at least 20 seeds per arm.
- **Examples:**
  - Track S: "Median of variable B on day 400 if input A is doubled from day 300?"
  - Track M: "6-layer MLP on generated parity-with-noise data; swap AdamW (lr 3e-4) for Lion (lr 3e-5). Quantiles of the change in test accuracy at 20k steps?"
- **Generation, secrecy, renewal:**
  - Track S: fresh simulator instances every window from the private mechanism grammar; at least 30% of primitives are new each season, and at least 2 are held out.
  - Track M: templates rotate quarterly.
  - Truth is computed after predictions lock. Everything is released after the window.
- **Scoring:**
  - **Track S:** CRPS for quantiles or log score for probabilities, against the distribution of 10,000 rollouts. The result is expressed as skill from 0 to 100:
    - 0 is the better of two anchors: an AutoML pipeline and an owner-written generic learner, both given the same data and interventions;
    - 100 is the true distribution.
    - Scores are summed over questions before the ratio is taken; absolute CRPS is also reported.
    - 1,000 paired forecasts per model.
  - **Track M:** CRPS against the distributions of at least 20 seeds, as skill over a "no change" prior and a scaling-law extrapolator.
- **Tool policy:**
  - Track S: code in the sandbox is part of the construct.
  - Track M: the headline is no-code. A code track is capped at 1% of each experiment's compute.
- **Humans:**
  - Track S: 60 data scientists with the same sandbox, 3 hours per 2 simulators. Results are pooled by simulator family.
  - Track M: 40 ML researchers and 40 CS graduate students, without code.
  - Both paid by proper score.
- **Cost:** Track S $100–500 per model; Track M $50–300 per model plus $5–20k owner compute per season [estimate].
