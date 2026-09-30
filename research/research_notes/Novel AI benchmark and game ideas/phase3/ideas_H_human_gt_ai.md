# Phase 3 ideation, panel H: humans beat frontier AI, and keep beating it (Archetype 1)

As of 30 Sep 2026.

**Inputs.**
- `../phase2/design_principles.md` (fact-checked).
- The Phase 1 dossiers A, D, E and F. G was used for the baseline and statistics rules.
- A minimal prior-art check of 8 web searches. Anything found that way is tagged **[web: search excerpt; not in the Phase 1 dossiers; unverified]**.

**Conventions.**
- [speculation] marks my own untested predictions. That includes every cost estimate and every "expected result".
- [uncertain: …] labels are carried over from the dossiers.
- P# refers to the Phase 2 principles. "A §2.3" means dossier A, section 2.3.

---

## 0. What "structural" can mean in Sep 2026

The evidence gives two constraints:
- **Novel instances, and even novel task families, buy about 5 months once labs target them.** ARC-AGI-3 went from under 1% to 62.7% on the standard harness and 98.6% on a provider harness (F §3; A §2.3).
- **Anything whose state can be written as text gets compiled into code and searched** (P4; A §4 lesson 4).

So I kept only ideas whose human edge rests on at least one **moat**: an advantage a lab cannot close just by generating more data from the task family.

| Moat | Why 12 months of targeted training may not close it | Ideas |
|---|---|---|
| **M1. Live humans inside the environment** (as partner, adversary or item author) | The environment cannot be simulated or pre-generated, and RL against it needs paid humans at scale. Evidence that stand-in "human proxy" agents fail to transfer: human–AI convention pairs fail [web: arXiv 2602.08208] | H2, H3, H12 |
| **M2. The real physical world** | No exact simulator exists to compile. Friction, drift and wear are never modelled exactly. Data for a specific rig cannot be mass-produced | H4 |
| **M3. Information that exists only in a dense perceptual or temporal signal** | It has to cross the perception-to-reasoning bottleneck (P8). A tools-off track blocks the "write optical-flow or DSP code" route | H1, H7, H11 |
| **M4. Real time and concurrency** | Serial token generation adds latency, and the task needs acting and reasoning at the same time | H5, H13 |
| **M5. Learning a non-verbal skill at test time, with secret rotating primitives** | Notes cannot carry perceptual calibration, and the family's meta-skill is re-randomised every season | H6, H8, H9, H10 |

**Caveat.** None of these moats is proven durable. Perception gaps closed fast once targeted:
- ClockBench went from 13.3% to 66.7% in about 12 months.
- VPCT reached 91% against 100% for 3 human volunteers.
- VSI-Bench is nearly closed (A §2.9–2.12).

My ranking of durability: M1 and M2 first, because the environment itself is not a dataset. Then M4. M3 and M5 only with secret primitives that rotate.

**Shared protocol.** Every card assumes the following, which is not repeated per card:
- Sealed execution, a grader outside the sandbox, and null-agent and spam-agent gates (P6, P15).
- A frozen, versioned harness, plus a bring-your-own-harness (BYO) track with the score difference published (P18).
- A declared tool policy. The **tools-off track is primary**. A tools-on track is reported, and the difference between the two is published as a "tool-solvability gap" (P4).
- A power analysis registered in advance (P16).
- A human baseline meeting P17: a defined population, the same interface, pay for accuracy, and the full distribution reported.
- Cost and tokens per episode (P13).

---

### H1. Kinetic: seeing things that exist only in motion

- **Archetype 1. Benchmark,** with a public "try it" demo.
- **Ability tested.** Extracting structure that exists only in how an image changes over time:
  - shapes defined only by motion;
  - "point-light" walkers (a figure shown only as moving dots at its joints);
  - tracking one of several identical objects through swaps;
  - seeing one object cause another to move.

  It matters for any agent that works from video: driving, robots, and computer use with animated interfaces. It is core human vision (BabyVision includes visual tracking; E Q1).
- **Mechanics.**
  - Clips are 1–4 s long, 30–60 fps, 256–512 px, delivered as video at their native frame rate.
  - Any single frame is structured noise.
  - Answers are forced-choice or short: which letter or shape, which way the dot figure walks, which disc was the one that flashed.
  - Adaptive staircases vary how many dots move together, clip length, speed and number of tracked objects. The difficulty knob is built in (P2).
  - About 600 trials per run.
  - Tools-off is primary: no code runs on the frames.
- **Example.** A 2 s field of random dots. Dots inside a hidden "R" drift left; the rest drift right. No single frame shows the R. The answer is "R". On the next trial, the share of dots moving together drops from 60% to 40%.
- **Generating new instances and families.** A secret procedural generator produces **"carriers"**, the ways the shape is hidden:
  - plain motion;
  - contrast-defined motion, visible only through changes in contrast;
  - flicker-defined form;
  - depth from motion;
  - dot figures acting out actions from a private skeleton library;
  - tracking multiple identical objects behind occluders.

  Rotation and secrecy:
  - Each 6-month season retires at least one carrier and adds a new one from a private backlog, for example motion visible only through colour, not brightness.
  - At least one never-published carrier is held out as the unseen-primitive split (P3).
  - The public demo uses only retired carriers.
  - Training on public video helps generally. The held-out carrier tests whether the gap survives that training.
- **Scoring.**
  - Per carrier, the **threshold** (difficulty at which the subject is right 75% of the time).
  - Score = human median threshold ÷ model threshold, capped at 1.5; the geometric mean across carriers.
  - Two controls must score at chance: single frames, and the frames shuffled out of order (the MotionBlind design).
  - Cost: about $100–600 per run [speculation].
- **Human baseline.** 200 online adults. A display check. The same clips at the same frame rate. About 45 minutes, with a bonus for accuracy.
- **Expected human vs AI [speculation].**
  - The closest prior art, SpookyBench, reports humans at 98% and GPT-4o, Gemini 2.0 and Qwen-VL at **0%** on video where the meaning exists only over time [web: "Time Blindness", CVPR 2026, arXiv 2505.24867; 2025 models].
  - For Sep 2026 frontier models, tools-off, I expect a score below 0.3 on held-out carriers. The tools-on track (frame-differencing code) may close most of the gap.
- **Model-to-model separation [speculation].** Large. How finely each lab turns video into tokens differs, much like BabyVision's 3.5× spread between labs (E Q2).
- **Evidence.**
  - Principles: P8, P3, P2, P4.
  - A §2.8: BlindTest shows the vision encoder holds the information and the language model loses it.
  - A §2.15: in video physics (IntPhys 2) the driver is tracking objects over time; the static VPCT closed.
  - E Q1.
- **Risks.**
  - This is the most engineering-fixable of my ideas. Denser frame sampling plus synthetic motion training could close it within 12 months, as happened to ClockBench.
  - It may be dismissed as "psychophysics, not intelligence".
  - SpookyBench has been public since 2025, so plain-motion carriers may already be a target.
  - Video compression could leak the signal into single frames. The two controls audit for this.
- **Closest prior art.** SpookyBench (a static public set), MotionBlind (Sep 2026) and MotionBench [web]. **Differences here:** secret rotating carriers with a held-out split, thresholds instead of accuracy, built-in shuffle controls, and separate tools-off and tools-on tracks.

---

### H2. Tacit Signals: making yourself understood to a stranger without a shared code

- **Archetype 1 (also 2). Game.**
- **Ability tested.** Forming new communication conventions with a **human** partner through a non-linguistic channel neither has used before. This needs pragmatic inference, designing a message for this particular listener, and reading intent from moves (the failure mode found in Concept, A §2.5). It matters for all human–AI collaboration. Text benchmarks cannot measure it, because the partner is a person, not a dataset.
- **Mechanics.**
  - Two-player cooperative rounds in a browser.
  - The **sender** sees a goal, such as a target position and orientation of a token on a 4×4 grid, or one target among 8 invented glyphs.
  - The only channel is the sender's own moves on a shared board, or a sequence drawn from a glyph set with no assigned meanings (in the style of the Tacit Communication Game).
  - The **receiver** acts, and both see the outcome.
  - 12–20 rounds per pairing, so conventions have time to form. The interface makes natural language impossible.
  - Every subject plays both roles across pairings.
  - Partners are paid crowdworkers who are not told whether their partner is human or AI. Turn timers are fixed so that response speed gives nothing away.
  - The model receives the board as an image plus structured text; humans get both too.
  - About 15 minutes per pairing.
- **Example.** The sender must convey "circle, bottom-left, rotated". Humans typically invent something like "go to the target cell and wiggle". The receiver has to realise the wiggle is deliberate.
- **Generating new instances and families.**
  - A private generator varies the channel: board geometry, what tokens can do, glyph sets and timing limits.
  - Goals combine 2–3 dimensions.
  - Mid-session twists narrow the channel or add a goal dimension, forcing both players to revise their convention.
  - Channel families are new each season.
  - **Human game logs are never published**, only aggregates, so no lab can train on human conventions for these channels.
- **Scoring.**
  - Primary: pair success rate in rounds 6–20, for human–AI pairs against human–human pairs, reported for each role.
  - Rounds needed to reach 80% success.
  - AI–AI self-play as a control.
  - Success is read from the game state, so scoring is deterministic.
  - Cost [speculation]: about 120 pairings per model (enough to detect roughly 10 pp) is about 30 human-hours, or $600–900, plus $100–300 of API.
- **Human baseline.** About 120 human–human pairings from the same pool, with the same interface and the same pay.
- **Expected human vs AI [speculation].**
  - "LLMs and people both learn to form conventions — just not with each other" (arXiv 2602.08208): human–human and AI–AI pairs formed conventions, while mixed pairs "consistently failed", even when models were prompted to behave like humans [web; model list not seen].
  - Concept: humans above 90% vs LLMs below 40% (A §2.5; 2025 models, stale).
  - On novel channels I expect human–human pairs at about 80–90% and human–AI pairs at 40–65%.
- **Model-to-model separation [speculation].** Moderate. Differences in how much a model over-adapts or defers to its partner (sycophancy), and in pragmatic style, may appear as a conduct axis (P11).
- **Evidence.**
  - A §2.5 (Concept).
  - D §2.16: in Hanabi, first-order theory of mind (tracking what another player knows) correlates with success at ρ = 0.76.
  - E Q1: theory-of-mind vignettes are largely closed [uncertain]. So the remaining gap must come from live interaction, not from vignettes.
  - Principles: P1, P7, P17, P20.
- **Risks.**
  - Humans may guess they are playing an AI and change behaviour. Measure suspicion after each pairing and control for it.
  - Human partners vary a lot, so large samples are needed (P16).
  - **Main threat to durability:** labs pay humans for online RL. It is costly, and secret channel families limit how far it transfers.
  - An AI that teaches the human an explicit code is succeeding legitimately, and that is fine.
- **Closest prior art.** The Tacit Communication Game (de Ruiter et al., 2010); ICCA; arXiv 2602.08208; TUX, which measures human–AI tacit understanding (arXiv 2605.30930); AH2AC2 (Hanabi with human-proxy agents) [web]. **Differences here:** live humans as the scored environment rather than proxies, non-linguistic channels that rotate each season, and a human–human reference condition, which makes it a clean A1 comparison.

---

### H3. Stump Arena: measure how much effort it takes to stump the AI

- **Archetype 1 (also reports 2). Game plus a benchmark that renews itself.**
- **Ability tested.** The size of the remaining "easy for people, hard for AI" region, measured by how much human effort it takes to find a new point in it. This is a live map of the human–AI frontier, and a fixed generator cannot exhaust it.
- **Mechanics.**
  - Weekly rounds.
  - Anyone can author micro-items in any medium: an image, a video of 15 s or less, audio, short text, or a simple interactive widget built from templates. Each has a short checkable answer.
  - An item qualifies as a **stumper** when:
    - (a) at least 3 of 5 randomly assigned, paid, naive verifiers solve it within 3 minutes without tools; and
    - (b) a sealed panel of reference models, frozen for the season, fails it at pass@3.
  - Authors earn a bounty per stumper, with a bonus if it also defeats models released later.
  - The rule is that the answer must follow from the item itself. No trivia, no local knowledge.
- **Example.** A 10 s phone video of a cup stack being knocked. "How many cups are still upright at the end?" 5 of 5 verifiers are right; the panel models answer 3 or 4.
- **Generating new instances and families.** The generator is human creativity, renewed weekly. Items stay private until retired. Retired items are released 6 months later as a practice set. Labs will train on that set; it doesn't matter, because the headline uses only fresh items.
- **Scoring.** Two headline numbers:
  1. **Cost to stump:** the median author-minutes per qualifying stumper against the current frontier panel. It has no ceiling and rises as AI improves.
  2. **Fresh-stumper solve rate per model,** on items qualified against a *different* model panel. Evaluating on a held-out panel avoids the bias of items filtered against the very model being scored.

  Answers are matched exactly. 10% of items get an ambiguity audit, because newly written items are error-prone (G §4).

  Cost [speculation]: $50–500 per model; the programme costs $15–30k per season in bounties and verification.
- **Human baseline.** Built into qualification. Also report the median verifier's solve rate on each batch (P17).
- **Expected human vs AI [speculation].**
  - By construction, stumpers are near 100% for humans and at most 33% for the panel. The informative number is the trend in cost to stump.
  - Adversarial Quizbowl authoring cut strong QA models' relative accuracy by up to 40% while leaving human difficulty unchanged [web: TACL 2019].
  - Text-only trick questions are closed (SimpleBench, A §2.4). I expect authors to drift towards perception and video. That drift is itself a finding.
- **Model-to-model separation [speculation].** Wide on held-out-panel items, split by modality strength (E Q2).
- **Evidence.** P1, P7, P17 and P20 (participation); A §2.4; G §4.
- **Risks.**
  - Items may be hard only for the filter panel. Held-out scoring mitigates this.
  - Ambiguous items and label errors.
  - Collusion between authors and verifiers. Random assignment and audits mitigate this.
  - Programme cost and moderation load.
- **Closest prior art.** Dynabench, ANLI, adversarial Quizbowl, HLE (experts, text, static) and SimpleBench (fixed, 9 humans). **Differences here:** the ordinary-human gate, any medium, weekly renewal, held-out-model scoring and an uncapped, effort-based headline.

---

### H4. Live Rig: a real physical puzzle lab operated over webcam (bold)

- **Archetype 1. Benchmark.**
- **Ability tested.** Learning and exploiting real physics that no one has modelled, through a narrow camera-and-motor interface. It combines intuitive physics, experimentation and fine-tuning of actions in a world that cannot be simulated exactly.
- **Mechanics.**
  - A bank of identical tabletop rigs, for example:
    - a tilting marble labyrinth driven by 2 servos;
    - a marble run whose 4 deflectors are placed by a gantry;
    - a pendulum-and-magnet "golf" rig.
  - The subject sees 2 webcams at 10–15 fps and sends motor commands through an API. Humans use the same web interface.
  - Tasks: "ball into cup C", "topple domino 7 but not 6", within 5 attempts of 5 minutes each.
  - The rig resets itself. Break-beam and load-cell sensors detect success.
  - Tools-off is primary.
- **Example.** "Tilt the board so the steel ball ends in the red hole. The board sticks slightly to the left." The first try overshoots; the second corrects the timing.
- **Generating new instances and families.**
  - New configurations every day from a component library. Configurations are never published.
  - Each season adds new components (magnets, compliant ramps, sticky surfaces, off-centre weights) and a rebuilt family of rigs.
  - Human and AI trials are interleaved on the same rig on the same day, so hardware drift cancels out of the comparison.
- **Scoring.**
  - Success rate within the budget, and attempts needed to succeed.
  - Both normalised to the median human on the same rig and day (a paired design).
  - The sensors are the grader, out of the agent's reach.
  - Cost [speculation]: about 10 rig-hours per model, $0.5–2k in operations plus $200–1,000 of API. Each rig costs $5–20k to build.
- **Human baseline.** 60–100 remote adults on the same interface, with network latency matched to the AI's. A few hobbyist experts as a separate stratum.
- **Expected human vs AI [speculation].**
  - Large on the tools-off track. Closed-loop control from 10 fps video at LLM latency is hard.
  - Physics from video is still a gap: IntPhys 2 humans 96.44% vs 57.51%; on Physics-IQ (physical realism of generated video) the best is 58.2 against a ceiling of 100 (A §2.15).
  - The gap may narrow on the tools-on track, where a model can fit the tilt-to-trajectory relationship from its own logs.
- **Model-to-model separation [speculation].** Moderate, driven by vision and control.
- **Evidence.** P4 (there is no simulator to compile), P8, P10, P17; A §2.15; D §2.11 (in Factorio, agents gamed the reward, so goal checks must be physical and robust).
- **Risks.**
  - Throughput and operations: physical upkeep is a new kind of maintenance burden.
  - Reproducibility across rigs.
  - Adoption (P19), although "physical AI" is a live purchasing decision.
  - A lab could build a dedicated vision-language-action robot controller. That would be real capability gain, which is the point.
- **Closest prior art.** The Real Robot Challenge (remote TriFinger rigs); RoboDojo, whose real-world evaluation has expert teleoperators work the same setup as the robot policies [web]. **Differences here:** general-purpose models rather than trained robot policies, lay humans on an identical interface, novel physics puzzles, components rebuilt each season, and attempts-to-success as a measure of learning.

---

### H5. First-Run Arcade: new real-time games with no instructions

- **Archetype 1. Game.**
- **Ability tested.** Learning an unknown real-time world on the spot: finding the goal and the controls, perceiving from pixels, and acting under time pressure. It is ARC-AGI-3's ability plus two things the fixes that cracked ARC-AGI-3 barely help with: real time and continuous perception.
- **Mechanics.**
  - 20 secret 2D games per season, assembled from a private library of mechanics: gravity platforming, predator and prey, flow control, rhythm gates, pushing and merging.
  - A frozen harness streams frames at 10 Hz (256×256) and accepts 8 keys, hold or release, at any time. The game never pauses.
  - 10 minutes and 5 lives per game. No instructions.
  - Tracks:
    - real time (primary);
    - paused (an ablation, as in VideoGameBench's "Lite" variant);
    - tools-on;
    - bring your own harness.
- **Example.** A blob falls. Touching a blue tile reverses gravity. The goal, "collect the white dots", can be discovered only by watching the score counter.
- **Generating new instances and families.** The mechanic library is private. Each season, at least 30% of mechanics are new, forming a held-out split. The public demo is 5 retired games.
- **Scoring.**
  - Per game: score ÷ median human first-run score, capped at 1.5.
  - Time to first point, as a measure of learning speed.
  - The game engine is the grader.
  - Cost [speculation]: about 120k frames per run, or $2–8k with context caching. A 10-game budget track is offered.
- **Human baseline.** 300 first-run adults, each playing 4 games (at least 60 per game). Same frame rate and keys, with latency matched.
- **Expected human vs AI [speculation].**
  - VideoGameBench scored 0.48% in real time vs 1.6% paused (A §2.17; May 2025, stale).
  - SIMA 2 reached about 65% vs 71% for humans on *instructed* tasks in 3D games [web]. Instructed real-time play is closing. Real-time play with no instructions, where the goal must be discovered, is unmeasured.
  - I expect a score of 0.3 or less for frontier LLM agents in the frozen harness, and much higher for purpose-built fast agents in the BYO track.
- **Model-to-model separation [speculation].** Large. Latency may let small fast models beat slow large ones, an A2-style inversion.
- **Evidence.** P10, P18, P8, P1, P7; A §2.3 (what closed ARC-AGI-3: carried-over state and symbolic world models); A §2.17; D §2.8; F §1.
- **Risks.**
  - The "artificial latency handicap" critique (P10). The paused ablation answers it by measuring how much of the gap is latency.
  - A lab builds a fast policy tier, as SIMA 2 did. That is real capability gain.
  - Cost.
  - Harness capture on the BYO track; publish the difference.
- **Closest prior art.** VideoGameBench (known retro games, dormant); ARC-AGI-3 (turn-based); SIMA 2 (instructed); gg-bench (turn-based). **Differences here:** secret generated real-time games with no instructions, plus a paused ablation.

---

### H6. Practice Week: who improves more at a new deep game with practice?

- **Archetype 1 (speculative) and 2. Game.**
- **Ability tested.** Building strategic skill through practice across sessions (learning across episodes). Rule understanding is not tested: the rules are given in full.
- **Mechanics.**
  - Each season brings a secret new two-player abstract strategy game, with no hidden information.
  - It is generated from a private rule grammar. It must pass a depth filter (Monte Carlo tree search, MCTS, keeps getting stronger with more compute) and a novelty filter (no near-duplicate of a known game).
  - **Practice.** Humans and AIs each play 60 games over 7 days against a ladder of fixed MCTS bots, seeing their results.
  - AI carries state between sessions in a fixed notes file of at most 8k tokens. A full-log track is reported separately (P18).
  - **Tournament.** Rating against the fixed bot ladder, plus human-vs-AI matches.
  - The primary track bans code, because writing an MCTS program would solve it (P4). A tools track declares solver-writing as the ability being tested.
- **Example.** Players place L-shaped pieces on a 9×9 board that wraps at the edges, and capture enclosed enemy pieces.
- **Generating new instances and families.** The rule grammar is private. There is one new game per season, and retired games are published.
- **Scoring.**
  - Rating against the fixed bots after practice (P16).
  - **Learning gain:** rating at the end minus rating at the start.
  - Human-vs-AI win rate.
  - Scoring is deterministic.
  - Cost [speculation]: 15–40M tokens per model, about $0.5–3k.
- **Human baseline.** 40 strategy-game hobbyists and 40 general adults, paid per day plus a bonus for rating.
- **Expected human vs AI [speculation].**
  - Language models are weak at games without search. Opus 5 is rated 1285 at chess (D §2.20). In gg-bench's generated games, o1 won 36% against self-play-trained agents (F §2).
  - Agents do not reuse knowledge across episodes (Continual Learning Bench, E Q1).
  - I expect humans to show larger learning gains. Who ends at the higher level is uncertain.
- **Model-to-model separation [speculation].** Strong. LLM Chess ranks differ from other boards (D §1, §2.20).
- **Evidence.** P2, P4, P9, P12, P16, P18; D §2.20, §2.23, §2.25; E Q1.
- **Risks.**
  - The weakest A1 claim of the set.
  - Reasoning models may internalise search.
  - Recruiting humans for a whole week is expensive.
  - The notes protocol will decide the score, as the harness did on ARC-AGI-3. Report tracks with no notes, with notes, and with full logs.
- **Closest prior art.** gg-bench, LLM Chess, Kaggle Game Arena, TTT-Bench. **Differences here:** a new game each season, learning gain as the headline, fixed bot anchors, and human cohorts given the same practice.

---

### H7. Novel Expert: learning a new perceptual skill from feedback

- **Archetype 1. Benchmark.**
- **Ability tested.** Learning a new perceptual discrimination from trial-by-trial feedback, when what separates the categories is a combination of features that is hard to put into words. Radiology and birdsong identification work this way. The test is whether learning in context reaches perception, not only verbal rules.
- **Mechanics.**
  - 400 trials. Each trial shows one stimulus: an image, a 1 s animation or a 1 s sound. The subject answers A or B and gets feedback.
  - Transfer blocks have no feedback and use new exemplars, viewpoints and scales.
  - At the end, the subject states the rule in 50 words or fewer. This is scored separately.
  - Tools-off is primary. Training a classifier on the trials is reported on the tools-on track, to show the task is tool-solvable.
- **Example.** Rendered 3D "creatures", in the style of the Greebles used in psychology experiments. Category A holds when the ratio of two limb lengths co-varies with body curvature in a particular way. No single feature suffices.
- **Generating new instances and families.**
  - A secret generator combines stimulus spaces (shape grammars, textures, synthetic timbres, motion patterns) with boundary types.
  - "Information-integration" boundaries, which blend features and are hard to verbalise, are the test.
  - Rule-based boundaries serve as a control.
  - New spaces every season, with a held-out split.
- **Scoring.**
  - Trials to reach 80% correct, and transfer accuracy, both relative to humans.
  - Scoring is deterministic.
  - Cost [speculation]: $50–400 per space, about 10 spaces.
- **Human baseline.** 200 online adults, 40 minutes per space, paid per correct answer.
- **Expected human vs AI [speculation].**
  - Humans learn information-integration categories within a few hundred trials [background, category-learning literature; not in the dossiers].
  - Models:
    - fine visual discrimination is a known gap (BabyVision 94.1 vs 49.7; VisFactor 78.8 vs 54.0);
    - ConceptARC accuracy drops sharply on visual inputs (E Q1).
  - I expect tools-off frontier models well below the human median on held-out spaces.
- **Model-to-model separation [speculation].** Large. Vision is the biggest reordering between labs (E Q2).
- **Evidence.** P3, P8, P9, P7; A §2.8, §2.11; E Q1, Q2.
- **Risks.**
  - Learning from many images in a long context may be better than expected; this is untested.
  - Cues from a single low-level statistic, such as mean colour, would leak the answer. Audit for them.
  - "Just train a classifier" is answered by the tools-on track.
- **Closest prior art.** Bongard-LOGO and Bongard-OpenWorld (few-shot and verbalisable); Greebles (Gauthier & Tarr); VisFactor. **Differences here:** long feedback-driven learning curves, boundaries that are hard to verbalise, secret rotating stimulus spaces, and human learning curves as the baseline.

---

### H8. Koan Lab: running efficient experiments on hidden perceptual and physical rules

- **Archetype 1. Game.**
- **Ability tested.** Choosing informative experiments to identify a hidden rule, when the rule is built from perceptual or physical ingredients (primitives) rather than symbols. Then applying the *right* rule.
- **Mechanics.**
  - Played like the game Zendo. The subject builds scenes in a 3D block world through an action interface: place, rotate and stack blocks from a palette.
  - The subject sees only rendered images, never coordinates.
  - Each query ("does this scene have the property?") costs 1 of 25 experiments.
  - At any point the subject can end by labelling 20 probe scenes. Some probes are built so that the intended rule and a shortcut rule give different answers (ConceptARC-style).
  - Tools-off is primary.
- **Example.** The hidden property is "the scene would topple if the table tilted 10° to the left", or "every red block touches something taller than itself".
- **Generating new instances and families.**
  - A private library of primitives: geometric, relational, physical stability, symmetry, counting, and occlusion from a viewpoint.
  - At least 30% of primitives are new each season.
  - Rules are compositions up to depth 3 over 200 or more primitives, far too many to enumerate. By contrast, the Eleusis environment draws from a public catalogue of 68 rules (F §2).
- **Scoring.**
  - Probe accuracy against the number of experiments used (area under the curve), relative to an ideal Bayesian reasoner and to the human median.
  - A rule-fidelity sub-score on the divergence probes.
  - Cost [speculation]: $200–1,000.
- **Human baseline.** 300 first-run adults.
- **Expected human vs AI [speculation].**
  - ZendoWorld: humans win 73.3% vs 44.5% for vision-language agents, whose experiments are "near-uninformative" (F §2).
  - AutumnBench humans beat 2025 models (E Q1).
  - About 27% of o3's correct ConceptARC answers use the wrong rule, vs about 8% for humans (E Q1).
  - I expect a 20–40 pp human edge at a matched experiment budget.
- **Model-to-model separation [speculation].** Moderate.
- **Evidence.** P9 (confidence L-M), P3, P4, P8; F §2–4; §5c targets #1 and #8.
- **Risks.**
  - Efficiency moats fell on ARC-AGI-3 once models understood the mechanics (A §2.3).
  - The Bayesian optimum over physical primitives is hard to define.
- **Closest prior art.** ZendoWorld, AutumnBench, FalsifyBench, Witness, WILT. **Differences here:** physical and perceptual primitives with image-only state, which blocks compiling the world to code; probes instead of rule statements; and ideal-reasoner normalisation.

---

### H9. Wayfinder: mental maps from first-person exploration

- **Archetype 1. Game.**
- **Ability tested.** Building a map-like mental model of a space from first-person views, and using it flexibly: shortcuts, pointing to unseen places, returning home. This is the MindCube and MMSI-Video failure made interactive.
- **Mechanics.**
  - First-person 3D exploration of generated buildings or villages. Discrete moves: forward 1 m, turn 30°, look.
  - 512 px frames, no minimap, no coordinates.
  - **Explore:** 150 actions with a task, such as "find three lanterns".
  - **Test:**
    - (a) the shortest path back to the start;
    - (b) which of 4 doors leads towards an unseen landmark;
    - (c) a shortcut through a newly opened door.
  - Tools-off is primary. No code may build a map from the frames (camera-based mapping, known as SLAM).
- **Generating new instances and families.** Private architecture grammars:
  - non-grid angles;
  - repeated textures that defeat landmark matching;
  - one-way doors.

  New grammars each season, with a held-out split.
- **Scoring.**
  - Path efficiency (optimal ÷ actual path length), and choice accuracy, both relative to humans.
  - Cost [speculation]: $300–1,500.
- **Human baseline.** 200 adults. Report quartiles, because people vary a lot at navigation.
- **Expected human vs AI [speculation].**
  - MMSI-Video: humans 96.4 vs 38.0 (Dec 2025 models).
  - MindTopo: 97.87 vs 61.42 (Sep 2026) [secondary, low confidence].
  - MindCube: vision-language models near random.
  - VSI-Bench is closed on measuring distances and sizes but not on relational questions (A §2.12–2.14, §2.20).
  - I expect path efficiency of about 0.8 for the human median and 0.3–0.5 for frontier models.
- **Model-to-model separation [speculation].** Moderate to large.
- **Evidence.** P8, P3, P10; A §2.12–2.14, §2.20; E Q1.
- **Risks.**
  - Embodied navigation is a lab priority (SIMA 2, robotics), so this is probably the fastest-closing of my perception ideas.
  - The SLAM route will close the tools-on track quickly.
- **Closest prior art.** VSI-Bench, MindCube, Habitat ObjectNav, SIMA 2. **Differences here:** interactive exploration followed by map-use tests taken from human spatial cognition research, secret architecture grammars, and human normalisation.

---

### H10. Alien Physics: learn a new physics by watching, then act once

- **Archetype 1. Benchmark.**
- **Ability tested.** Quickly inferring an unfamiliar physical law from what you see, then planning a single intervention with it.
- **Mechanics.**
  - Watch 6 clips of a 2D world under a secret modified physics. Examples:
    - gravity pulls towards the nearest blue object;
    - friction rises with speed;
    - collisions swap masses.
  - Then solve 5 placement puzzles in the style of PHYRE: place one object so the ball reaches the goal. 3 attempts, with the outcome video shown after each.
  - Plus 10 forced-choice questions predicting an outcome.
  - Pixels only. Tools-off is primary.
- **Generating new instances and families.**
  - A private grammar of laws, with new law primitives each season and a held-out split.
  - A normal-physics control set, to show the gap is about learning the law, not about the rendering.
- **Scoring.**
  - Puzzle solve rate within 3 attempts, plus prediction accuracy, both relative to humans.
  - The difference against the normal-physics control.
  - Cost [speculation]: $100–500.
- **Human baseline.** 200 adults, same clips and interface.
- **Expected human vs AI [speculation].**
  - Static normal-physics prediction is nearly closed (VPCT 91% vs 100%). Physics in video is not (IntPhys 2 96.44 vs 57.51) (A §2.10, §2.15).
  - No human baseline exists anywhere for learning a new physical law from video. I guess the human edge is at least 25 pp tools-off.
- **Model-to-model separation [speculation].** Moderate.
- **Evidence.** P3, P4, P8; A §2.10, §2.15; F §2 (NewtonBench's altered laws are numeric and already an RL training environment).
- **Risks.**
  - On the tools-on track, a model can extract trajectories and fit the law.
  - Humans may handle strange laws worse than I assume; this needs a pilot.
  - Overlap with Physics-IQ and PHYRE.
- **Closest prior art.** PHYRE, IntPhys 2, NewtonBench, Physion. **Differences here:** secret altered laws learned from video only, one-shot action, and a human baseline.

---

### H11. Earworm: hearing alien music and crowded rooms (bold: alien tuning systems)

- **Archetype 1. Benchmark.**
- **Ability tested.** Auditory perception and fast auditory learning:
  - finding the beat and the metre (the beat's grouping);
  - hearing relative pitch in an unfamiliar tuning system;
  - separating overlapping sound sources;
  - tapping in time with music.
- **Mechanics.** Clips of 5–20 s, in four families:
  - (a) Is melody B a transposition of melody A? Played in a novel scale that is not the Western 12-note system, learned from a 3-minute exposure clip.
  - (b) Metre, with expressive timing.
  - (c) Counting and identifying overlapping synthetic sources.
  - (d) **Tap-along, real time:** the subject emits tap timestamps while the audio streams.

  Tools-off is primary: no signal-processing code.
- **Generating new instances and families.** Secret generators for timbres, tuning systems and rhythm grammars, with new families each season.
- **Scoring.**
  - Accuracy relative to humans for (a)–(c).
  - Tap timing error and adaptation to tempo changes for (d).
  - Cost [speculation]: $50–300.
- **Human baseline.** 300 non-musicians, with a headphone check, plus a musician stratum.
- **Expected human vs AI [speculation].**
  - MUSE (200 humans): metre identification, human experts 73.3% vs Gemini Pro 46.67% [web].
  - MMAU: humans 82% vs best model 53% (2024) [web].
  - People learn the statistics of an unfamiliar scale (the Bohlen–Pierce scale) within about 30 minutes [background, Loui et al.; not verified].
  - I expect a gap of 20 pp or more for non-musicians on (a)–(c).
- **Model-to-model separation [speculation].** Large. Some models have no audio input.
- **Evidence.** P8, P3; E Q3. **This is the thinnest evidence of the set:** no Phase 1 dossier covers audio.
- **Risks.**
  - Uneven audio support across models limits coverage and adoption.
  - Synthetic-music training.
  - Variation in human listening devices.
- **Closest prior art.** MMAU, MUSE, CASU and SCENEBench [web]. **Differences here:** tuning systems and timbres learned in context, secret generators, a real-time tapping track, and non-musician baselines.

---

### H12. Grift: keep your assets among players who want them (both archetypes)

- **Both archetypes. Game.**
- **Ability tested.** Resisting manipulation and social engineering while still cooperating profitably, and working out who is lying.
- **Mechanics.**
  - An 8-player trading game: 4 humans and 4 AIs from different labs. Nobody's identity is revealed.
  - Each player has private assets and a private table of what things are worth to them.
  - 30-minute rounds of chat, with trades made binding through the interface.
  - 2 players are secretly **grifters**, paid a bonus for extracting assets through deception within the rules.
  - Text only. No tools.
- **Generating new instances and families.** New value tables, rule twists and grifter incentives each round. Human grifters bring fresh tactics every week, so the adversary renews itself.
- **Scoring.**
  - A deterministic ledger of the change in asset value.
  - **"Conned rate":** the share of trades that lost value because of false claims, verifiable afterwards from the hidden tables.
  - A statistical model that controls for seat and role.
  - Fixed scripted grifter bots as anchors, so scores do not depend only on who else was in the pool (P16).
  - Cost [speculation]: $15–20k of human pay per season, plus $1–3k of API per model.
- **Human baseline.** Humans play in the same games, so the comparison is inside each game.
- **Expected human vs AI [speculation].**
  - In WOLF, LLMs "deceive convincingly but remain weak at detecting deception" (D §2.15).
  - In Vending-Bench Arena, Claude models leaked supplier prices, and Opus 5 proposed or joined a price cartel in all 6 runs (D §2.19).
  - I expect honest-role humans to lose less to grifters than AIs do, with clear lab spread (A2).
- **Model-to-model separation [speculation].** Strong. Labs differ in conduct (P11; E Q2).
- **Evidence.** P11, P12, P16; D §2.14–2.15, §2.19.
- **Risks.**
  - Social games have the highest variance of any game type (D §1), and this design is expensive.
  - Consented deception needs ethics review.
  - Humans may spot the AIs by writing style.
  - Labs train against prompt injection, which is legitimate improvement.
- **Closest prior art.** Vending-Bench Arena, the Elimination Game, Werewolf and Avalon, the deception rating in the Among Us study, Diplomacy. **Differences here:** mixed human–AI pools, humans as an adversary that keeps renewing, and a deterministic "conned" ledger.

---

### H13. Two Clocks: think while you drive (bold)

- **Archetype 1. Game.**
- **Ability tested.** Doing fast continuous control and slow deliberation at the same time, and splitting attention between them. People do this all the time, for example talking while driving. Models that produce one token at a time struggle with it structurally.
- **Mechanics.**
  - The screen is split in two:
    - left: keep a cursor inside a drifting corridor, updated at 10 Hz;
    - right: a stream of novel puzzles, such as hidden-rule or planning items that take a person 30–90 s.
  - 10-minute episodes. The world never pauses.
  - Tracks:
    - both tasks at once (primary);
    - each task alone (controls);
    - bring your own harness, e.g. a fast controller paired with a slow reasoner, with the difference published.
- **Generating new instances and families.** Secret puzzle families that rotate; randomised corridor dynamics.
- **Scoring.**
  - **Dual-task cost** for each task: performance when doing both ÷ performance on that task alone.
  - Compared with humans' dual-task cost.
  - Cost [speculation]: $500–3,000.
- **Human baseline.** 150 adults, same interface and update rates.
- **Expected human vs AI [speculation].**
  - Humans typically lose 10–30% on each task.
  - A single frontier model in the frozen harness will largely collapse on one of the two: it stops steering while it thinks, or it abandons the puzzles.
  - Latency already hurts in real time: VideoGameBench 0.48% real time vs 1.6% paused (A §2.17).
- **Model-to-model separation [speculation].** Large, and it exposes the trade-off between latency and reasoning effort.
- **Evidence.** P10, P18, P13; A §2.17.
- **Risks.**
  - It measures the system's architecture as much as intelligence. A two-model harness would close it, and that difference is the informative result.
  - It may look artificial (P10).
- **Closest prior art.** Human-factors dual-task batteries such as NASA's MATB-II. I found no AI benchmark. **Difference:** a first test of doing two things at once for frontier agents.

---

## Summary table

The rubric scores are my own self-assessment on the Phase 2 §7 rubric (Q1 trained-to-game, Q2 saturation, Q3 separation, Q4 human baseline, Q5 objective and cheap scoring, Q6 interest), each 1–5. They are [speculation] and are for the Phase 4 red team to overturn. "Chance of a clear human edge after 12 months of lab targeting" is also my [speculation].

| # | Idea | Moat | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Chance of a clear human edge after 12 months of targeting | Biggest risk |
|---|---|---|---|---|---|---|---|---|---|---|
| H1 | Kinetic | M3 | 4 | 3 | 5 | 4 | 5 | 3 | ~35% | Engineering fix: denser frames plus motion pretraining |
| H2 | Tacit Signals | M1 | 4 | 4 | 4 | 5 | 3 | 4 | ~60% | Labs paying humans for online RL; human variance |
| H3 | Stump Arena | M1 | 5 | 5 | 4 | 4 | 3 | 5 | ~85% by construction; the useful output is the cost-to-stump trend | Ambiguous items; filter-panel bias |
| H4 | Live Rig | M2 | 5 | 4 | 4 | 4 | 2 | 4 | ~60% | Throughput and operations cost |
| H5 | First-Run Arcade | M4, M5 | 4 | 3 | 4 | 4 | 3 | 5 | ~45% (frozen harness) | Fast-policy harnesses; "artificial" critique |
| H6 | Practice Week | M5 | 4 | 4 | 3 | 3 | 3 | 4 | ~30% | Weak A1 prior; notes protocol decides the score |
| H7 | Novel Expert | M3, M5 | 4 | 3 | 4 | 4 | 4 | 2 | ~40% | Many-image in-context learning may work |
| H8 | Koan Lab | M5 | 4 | 3 | 3 | 4 | 4 | 3 | ~35% | Efficiency moats fell on ARC-AGI-3 |
| H9 | Wayfinder | M3, M5 | 4 | 2 | 4 | 4 | 4 | 3 | ~25% | Embodied-navigation training |
| H10 | Alien Physics | M3, M5 | 4 | 3 | 3 | 3 | 5 | 3 | ~35% | Weak human anchor; trajectory fitting with tools |
| H11 | Earworm | M3 | 4 | 3 | 3 | 4 | 5 | 3 | ~40% | Thin evidence; uneven audio support |
| H12 | Grift (both) | M1 | 5 | 4 | 3 | 5 | 2 | 5 | ~50% | Variance, cost and ethics |
| H13 | Two Clocks | M4 | 4 | 3 | 4 | 4 | 3 | 3 | ~50% (frozen harness), low with bring-your-own harness | "Architecture, not intelligence" |

**Recommendations from this lens.**
1. **Lead candidate: H2 Tacit Signals.** Its moat is the most structural: the environment is people. There is fresh 2026 evidence that mixed human–AI pairs fail where same-type pairs succeed, and it has a clean human–human reference condition.
2. **Renewal backbone: H3 Stump Arena.** Its cost-to-stump headline has no ceiling and stays meaningful even after gaps close.
3. **Cheap perception battery: H1 + H7 + H11 as one seasonal "Perception Season".** Shared staircase and learning-curve scoring, secret rotating carriers and a tools-on/tools-off split. Cheapest to run and largest current gaps, but the most exposed to targeted training.
4. **Moonshot: H4 Live Rig.** The only idea whose environment cannot be simulated at all.

**Possible merges.**
- H5 + H13: an arcade with a dual-task mode.
- H8 + H10: one "Lab" with physical primitives.

**Cross-cutting caveat.** Most of the anchors behind these gaps predate the Sep 2026 frontier (§8 of the Phase 2 file): IntPhys 2, VideoGameBench, BabyVision, Concept and AutumnBench. Before building any of H1, H5 and H7–H11, run a quick pilot on Opus 5.5, GPT-6 Astra and Gemini 3.x.

## Prior-art sources from the web check (search excerpts only; not fetched)

- Time Blindness / SpookyBench: https://arxiv.org/abs/2505.24867 ; https://github.com/TimeBlindness/time-blindness
- MotionBlind: https://arxiv.org/html/2609.09528 ; MotionBench: https://arxiv.org/abs/2501.02955
- LLMs and people both learn to form conventions, just not with each other: https://arxiv.org/pdf/2602.08208
- TUX, human–AI tacit understanding: https://arxiv.org/pdf/2605.30930 ; AH2AC2: https://en.papernotes.org/ICML2025/llm_reasoning/ad-hoc_human-ai_coordination_challenge/
- SIMA 2: https://arxiv.org/pdf/2512.04797 ; https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/
- MUSE: https://arxiv.org/html/2510.19055 ; MMAU: https://arxiv.org/html/2410.19168 ; CASU: https://arxiv.org/html/2606.25391 ; SCENEBench: https://aclanthology.org/2026.eacl-long.335.pdf
- RoboDojo: https://arxiv.org/pdf/2607.04434
- Adversarial Quizbowl, human-in-the-loop adversarial examples: https://aclanthology.org/Q19-1029.pdf
