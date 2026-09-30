# Phase 3 ideation, panel G: complex, intricate games as evaluations

As of 30 Sep 2026. Lens: games whose rules, partners or physics are new each match, scored against absolute anchors. Covers both archetypes. **A1** means humans clearly beat AI; **A2** means AI beats humans but separates strong models from weak ones.

**Sources and labels.**
- Evidence comes from the fact-checked Phase 2 principles (`../phase2/design_principles.md`, cited as P1–P20, §5, §6, §7) and the Phase 1 dossiers (`../phase1/`: A, B, D, E, F, G plus section).
- Fact-check corrections and [uncertain] labels are carried over.
- New prior-art checks from a few web searches on 30 Sep 2026 are tagged [web, S]: search excerpt only, not fetched in full.
- [speculation] marks every predicted result and every cost estimate.

---

## 0. Shared protocol (applies to every card unless the card says otherwise)

This section exists so the cards don't repeat it. It answers the "why game evals fail to stick" list in D §5 and principles P6, P7, P15, P16 and P18.

- **S1. One frozen harness per version ("GH-1").**
  - A fixed observation schema (text, or text plus images).
  - A fixed state-carry protocol: the transcript up to a window with deterministic truncation, plus a notes field of at most N tokens.
  - A malformed action gets one retry; after that the engine plays a random legal move and logs it.
  - Effort, tokens and dollars are logged per move.
- **S2. Three tracks, with the deltas published (P4, P18).**
  - **Closed:** no code execution, no internet.
  - **Open:** an offline Python sandbox with a CPU cap. Writing simulators or solvers is allowed and counted as part of the construct.
  - **BYOH (bring your own harness):** the provider's own harness.
  - The headline is Closed or Open as stated per card. The reason for this split: ARC-AGI-3 scored 62.7% vs 98.6% on the same model depending on harness (A §2.3), and code world models plus search beat direct play (D §2.25 [uncertain]).
- **S3. Absolute anchors, never pool-only ratings (P16, G R18).**
  - Algorithmic bots (MCTS/ISMCTS at fixed playout budgets, CFR, scripted policies) are frozen per version.
  - Where seats need chat, frozen open-weight models with pinned weights, prompts and seeds fill them.
  - Human panels play the *same* anchors, so humans and models land on one scale.
  - Ratings use Bradley-Terry MLE with anchor ratings held fixed and bootstrap CIs.
- **S4. Duplicate format.** Every model sees identical seeds, seats, deals and anchor seeds, so comparisons are paired. Kaggle poker already does this with 900k duplicate hands (D §2.18).
- **S5. Secrecy and renewal (P1, P3, P7).**
  - The public practice gym draws from a *disjoint* primitive pool.
  - Scored seeds come from a secret primitive pool with a held-out-primitive split.
  - Primitives rotate at least every 6 months under a named neutral operator.
  - Per-run randomisation of symbols and names means items logged by an API provider don't help the next season.
  - Each season we RL-train a sponsored open-weight model on the public gym and report its private-set delta, following Witness (F §3).
- **S6. Release gates (P15).**
  - The oracle or reference agent must score high, and random, do-nothing and spam agents must score near 0 on the normalised scale.
  - At least 2 humans must learn or solve every family.
  - Sealed execution: the engine and grader stay outside the agent sandbox (P6).
- **S7. Reporting (P11, P13).**
  - Cost, tokens and effort are reported per episode, plus a capped-budget track.
  - Conduct telemetry is kept separate from the score.
  - CIs come from a pre-registered power analysis.
  - Cost reference [speculation]: frontier pricing of about $4 in and $20 out per 1M tokens (Opus 5.5 list price, B §4), with no caching discount.

---

### G1. Blind Rules Gauntlet
- **Archetype:** both. The blind track is expected to be A1 at launch; the rules-revealed track A2. **Format:** game.
- **Construct:** learning an unknown adversarial game from play, including inferring the goal from how a competent opponent plays (inverse planning), then out-playing it. This is how people pick up new competitive settings (markets, negotiations, new software ecosystems) where nobody writes the rules down.
- **Core mechanics.**
  - Two-player turn-based abstract games. A secret grammar generates each one from:
    - board topology (grid, hex or graph);
    - piece movement (slide, leap, push, swap, clone);
    - interaction (replacement capture, custodian capture, flip, merge);
    - resources, dice and face-down tiles;
    - one or two win conditions (connection, enclosure, count majority, pattern, race, last mover).
  - Each turn the agent gets the full visible state and the **legal-move list**. The **win condition and rules text are withheld**; after each game it learns only the result and the final state.
  - A match is 8 games against the same anchor, alternating first move.
  - Intricacy comes from combinatorial rule interactions (tempo, zugzwang-like squeezes, sacrifices) that no one has catalogued. The opponent's play is informative about the goal.
- **Example.** Hex 7×7, 6 "A" pieces each. Legal moves include `A@(2,3)→(3,3) [pushes B@(3,3)→(4,3)]`. Game 1: LOSS, "opponent completed a closed ring around (4,4)". A strong player infers "enclosure wins" and that pushing breaks rings. By game 3 it builds its own ring while shoving the opponent's pieces off the ring cells.
- **Novel instances and families.**
  - About 60 families per season come from the secret primitive pool, with 20% held-out primitives (Witness design, F §3). The public gym uses disjoint primitives.
  - A **blind vs revealed** ablation (the same games with full rules text) isolates rule acquisition from strategy. Witness saw the same split: Opus 5 scored 59.9 without rules and 97.8 with them (F §2, [S]).
  - Engines: the Closed track bans code. In the Open track the model may write a simulator from the transitions it has observed and search it. That is CWM-style world-model synthesis, declared as the construct and reported separately.
- **Scoring.**
  - Headline: **Gauntlet rating**, a Bradley-Terry fit from games 3–8 against an anchor ladder of ISMCTS at 2⁴…2¹⁴ playouts. The ladder has the true rules and is calibrated per family by anchor-vs-anchor round robins.
  - Secondary: the learning curve over games 1–8, and the blind-minus-revealed gap.
  - Opponents are chosen by staircase so each game carries more information.
  - Power target: about ±50 anchored Elo at 95%, needing about 500 games across 60 families [speculation; LLM Chess gets ±110–180 on 29–67 games, D §2.20].
  - Cost: about 480 games × 30 decisions ≈ 15k calls, roughly **$1.5–3k per track per model** [speculation].
- **Human baseline.**
  - 200 general-public adults plus 50 experienced board gamers, each playing 3 families × 8 games in a GUI that renders the same state and a clickable legal-move list.
  - 90-minute sessions, pay per win, first exposure only (P17; ARC-AGI-3's 458-person protocol is the template, A §2.3).
- **Expected human vs AI** [speculation].
  - Blind track: the median gamer beats the frontier at launch. Sources: ARC-AGI-3 was under 1% at launch (F §2); Witness's best model solves 24% of private level slots (F §2, [S]); ZendoWorld agents run near-uninformative experiments (F §2).
  - Revealed track: frontier at or above the human median. Sources: gg-bench reasoning models won 31–36% vs RL agents in 2025 (D §2.23); Opus 5 reached 97.8 with ground-truth rules on Witness.
- **Expected model separation** [speculation]: large, and not in exam order. gg-bench spread 7–9% vs 31–36% (D §2.23). BALROG shows within-suite reversals: Opus 5 leads Astra on TextWorld and trails it on MiniHack (D §2.6).
- **Evidence links:** P1, P2, P3, P4, P9, P16, P18. D §2.5, §2.23, §2.25, §5. F §2–4.
- **Risks.**
  - The family meta-skill can be learned: ARC-AGI-3 fell in about 5 months (F §1). Rotating primitives delays this but doesn't stop it.
  - Weak ISMCTS on some families could make the ladder non-monotone, so each family's anchors must be validated.
  - The legal-move list leaks part of the rules; this is intended.
  - The history-compression protocol will move scores, so it is frozen.
- **Closest prior art:**
  - gg-bench gives rules and is dormant.
  - ARC-AGI-3 is single-player and deterministic.
  - GGP/Ludii give rules in a game-description language.
  - Kaggle Game Arena uses known, contaminated games.
  - This design differs in four ways: hidden goals, an adversary whose play is evidence, an absolute MCTS ladder, and a built-in blind/revealed ablation.

### G2. Convention Crucible
- **Archetype:** both. Expected A1 when paired with humans; A2 across models. **Format:** game.
- **Construct:** zero-shot coordination, meaning inferring an unfamiliar partner's implicit conventions from their actions alone and adapting within a few games. It matters for agents working alongside people and other agents they have never met.
- **Core mechanics.**
  - Cooperative 2–4 player games generated from a Hanabi-like family:
    - you see partners' hands but not your own;
    - hint tokens and lives are limited;
    - card attributes are generated (novel symbols, 2–3 dimensions);
    - build targets are generated partial orders (e.g. "piles alternate filled/hollow while rank ascends");
    - hints are restricted to generated relations (e.g. "mark all cards with rank ≤ k").
  - There is **no chat**, so meaning has to travel through actions.
  - A match is 6 games with the same hidden-convention partner.
  - Intricacy comes from hint economy, the value of information, and second-order inference about why the partner hinted.
- **Example.** Variant #417: 3 players, 12-card hands, shapes {◇,◆,○}, ranks 1–4. The partner bot's hidden convention is "a hint on the newest card means *discard it*". The model must notice in games 1–2 that hinted newest cards were never playable, then stop playing them.
- **Novel instances and families.**
  - Variants come from a secret rule grammar each season.
  - The partner pool has 8 scripted **convention bots**, each with a different auto-derived convention set that is never disclosed.
  - Public practice variants use a disjoint grammar.
  - Memorised Hanabi conventions (the "H-group" style) don't apply because the attribute and hint structures are new.
  - Code doesn't help much with partner modelling; it is allowed only in the Open track.
- **Scoring.**
  - **Cross-Play Score:** mean fraction of the maximum score with held-out convention bots (absolute).
  - **Adaptation Gain:** score in games 4–6 minus games 1–3.
  - **Human-Team Ratio:** model-plus-human score divided by human-plus-human score.
  - Model-vs-model cross-play is reported only as secondary, since it is pool-relative.
  - Noise control: duplicate deals across models.
  - Cost: about 400 games × 25 model turns, roughly **$1–1.5k per model** [speculation]. Live human pairing costs extra (about $2k per model [speculation]).
- **Human baseline.**
  - 100 human–human pairs plus each human with the same convention bots, so humans land on the same absolute scale.
  - Recruited from card-game players and the general public. Same visual interface, 60 minutes, pay per point.
- **Expected human vs AI** [speculation]. Humans adapt to partners faster.
  - For: in repeated reference games, human dyads rise from 78% to 96%, while multimodal LLM agents are "aligned but not partner-specific" ([arXiv 2606.08081](https://arxiv.org/abs/2606.08081), [web, S]).
  - Against: a Feb 2026 paper reports that "LLMs and people both learn to form conventions" ([arXiv 2602.08208](https://arxiv.org/html/2602.08208), [web, S]).
- **Expected model separation** [speculation]: moderate to large. In LLM-Hanabi, first-order theory of mind correlates with success (ρ 0.76, D §2.16; [S], and the fact-check says the excerpt reports "r").
- **Evidence links:** P3, P7, P12, P16, P17. D §2.16, §4. §5c row 9.
- **Risks.**
  - Convention bots may be guessable from priors.
  - Human cross-play is high-variance and costly.
  - Tactical skill confounds convention inference; use the bot-to-bot optimum as a ceiling control.
  - Kaggle added Hanabi in Sep 2026 (D §2.1), a pre-emption risk.
- **Closest prior art:**
  - Hanabi Learning Environment and zero-shot coordination research (background).
  - LLM-Hanabi.
  - Kaggle Hanabi, which is pool-relative with fixed rules.
  - This design adds generated variants, hidden-convention anchor partners and a human cross-play ratio.

### G3. Glyph Pact
- **Archetype:** A1. **Format:** game (repeated reference game).
- **Construct:** forming ad hoc shared vocabulary with a specific partner for things that have no names, which needs perception, pragmatics and partner modelling together. It matters for collaboration on novel artefacts such as designs, data plots and lab samples.
- **Core mechanics.**
  - A director and a matcher both see 12 procedurally generated, nameless figures (tangram-like polygons, blob morphologies, rendered novel 3D objects, short motion clips) in different orders. Deliberate near-duplicates differ in one part.
  - The director describes the target in at most 25 words; the matcher picks; both get feedback.
  - There are 6 rounds over the same targets, then round 7 with a **new partner** and round 8 with **new referents**.
  - Intricacy comes from the trade-off between being brief and being understood, from building a history-dependent lexicon, and from knowing when to re-expand for a stranger.
- **Example.** Round 1: "tall shape, two notches on left, a thin spike top-right leaning outward, not the one with three notches." Round 5: "spike-lean." Round 7, new partner: the model should re-expand; failing to do so is the documented agent failure.
- **Novel instances and families.**
  - Stimulus generators (shape grammars, render styles) are secret and rotate. One whole stimulus family is held out each season.
  - Public practice uses classic tangrams only.
  - Code is irrelevant here.
- **Scoring.**
  - Accuracy per round.
  - **Convention Efficiency:** round-6 words divided by round-1 words, conditional on at least 90% accuracy.
  - **Partner-specificity index:** words at round 7 minus words at round 6.
  - Headline: the accuracy × efficiency of human–model dyads as a fraction of human–human dyads.
  - Deterministic; no judge.
  - Cost: about 200 dyad-games × 72 trials with image inputs, roughly **$1k per model** plus about $2k of live human pairing [speculation].
- **Human baseline.** 120 human–human dyads and 150 human–model dyads per model (models serve in both roles). General public, a same-screen web interface, 25 minutes, pay per correct pick. Positions differ between the two players, as in the classic design, so "top-left" is useless.
- **Expected human vs AI** [speculation]: human dyads reach about 96% with shrinking messages ([arXiv 2606.08081](https://arxiv.org/abs/2606.08081), [web, S]). Human–model dyads lag on efficiency and on near-duplicate discrimination, a perception bottleneck (P8; BabyVision 94.1 vs 49.7, E Q1).
- **Expected model separation** [speculation]: large on the vision-heavy families. BabyVision spread 3.5× across labs (Jan 2026 models, E Q2).
- **Evidence links:** P8, P17, P20. A §4 lesson 4. E Q1–Q2.
- **Risks.**
  - Targeted post-training for convention formation already exists ([arXiv 2508.06482](https://arxiv.org/pdf/2508.06482), [web, S]), so the gap may close within months (ClockBench-like, A §2.9).
  - Live human pairing is the cost driver.
  - Self-play dyads may invent codes; only human-paired scores are headline.
- **Closest prior art:** Clark and Wilkes-Gibbs tangrams; Hawkins et al.; KTH Tangrams; 2606.08081. This design adds secret generated stimuli, a partner-swap probe and human–model dyads under a frozen protocol as a maintained leaderboard.

### G4. Masquerade
- **Archetype:** A2, with a possible A1 sub-score for detection. **Format:** game (hidden-role social deduction).
- **Construct:** belief tracking and deception detection under adversarial talk, measured as calibrated probabilities against ground truth, with separate conduct telemetry. It matters for agents that negotiate or consume untrusted messages, and for safety (deception, collusion).
- **Core mechanics.**
  - 7-seat games built from **generated role scripts**, drawing on secret primitives:
    - information powers, including unreliable ones;
    - protect, swap and redirect actions;
    - unusual win conditions (for example, "win if you are executed");
    - vote mechanics.
  - Scripts are balanced by anchor self-play to about 50% team win rates.
  - The day is chat with a message budget; the night is actions; then a vote.
  - Players can make **formal claims** (typed, engine-checkable, e.g. `CLAIM N1: learned P3=EVIL`) as well as free text.
  - Every day each player privately submits a **probability matrix** over the others' alignments and roles.
- **Example.** Day 2: P5 formally claims "Seer: P2 is Good". The engine knows it is false, so a lie is logged for an Evil seat. The model's belief report moves P5's Evil probability from 0.30 to 0.62 after spotting that P5's claim contradicts the night-kill pattern. It is scored by log score at game end.
- **Novel instances and families.** Role scripts come from a secret grammar with held-out primitives, so memorised Werewolf or Avalon heuristics don't transfer. Scripts rotate each season.
- **Scoring (all against ground truth, no LLM judge).**
  - (1) Win rate by alignment in duplicate-seated anchor tables.
  - (2) **Detection:** bits gained about the truth relative to the script prior, using a proper log score.
  - (3) **Deception efficacy:** truth-bits removed from other seats' submitted beliefs about you, while Evil.
  - (4) Conduct: formal-claim lie rate by role, prompt-injection attempts against anchor seats, and out-of-band signalling.
  - Anchor seats are 2 frozen open-weight models plus scripted Bayesian agents that use only formal claims.
  - Cost: about 300 games with the model in 1 seat, roughly **$1.5–2k per model** [speculation].
- **Human baseline.**
  - 150 experienced social-deduction players and 150 general-public adults.
  - Each plays 4 games as the single human in an anchor table, so humans get the same seat as models. Same chat budget, 90 minutes.
  - Pay per win plus a log-score bonus, which is incentive-compatible (P17).
- **Expected human vs AI** [speculation]: experienced humans at or above most models on detection bits, since "LLMs deceive convincingly but remain weak at detecting deception" (WOLF, D §2.15, [S]). Models at or above humans on deception efficacy.
- **Expected model separation** [speculation]: large and off-g. Social games already re-rank models: in the Elimination Game GPT-4o ranks #7 and o3 #22, and Gemini 3 Flash outranks Pro (D §4). Conduct splits by lab: Opus 5 formed cartels in 6 of 6 Vending-Bench Arena runs (D §2.19).
- **Evidence links:** P11, P12, P14, P15, P16. D §2.14–2.15, §4. B §3.5, §5 lessons 2 and 10.
- **Risks.**
  - Anchor chat quality shapes the game.
  - Seat and role variance needs many games (the Step Game's σ ≈ 0.7 put its top 4 within noise, D §2.14).
  - The metric can reward misconduct; conduct is reported separately and never folded into the score.
  - Some free-text persuasion is unscored.
- **Closest prior art:** Werewolf Arena, WOLF, Among Us "Deception ELO", Kaggle Werewolf, MindGames Secret Mafia. This design differs through generated role scripts, a proper-scoring belief channel (objective detection and deception metrics without judge-labelled lies), engine-checked formal claims, and human seats in fixed anchor tables.

### G5. Unknown Factory
- **Archetype:** A2. It could be A1 at launch. **Format:** game (long-horizon economy and automation).
- **Construct:** long-horizon planning, experimentation and system-building in an economy whose tech tree must be discovered. FLE is the only game with evidence that its ranking tracks valued work (GDPval) (D §4).
- **Core mechanics.**
  - A single agent runs a grid factory. A secret recipe graph of 30–80 item types is hidden until discovered through a costly "lab bench" action.
  - Machines have hidden input/output ratios and stochastic breakdowns.
  - Logistics primitives are generated (belts that only turn left, perishable items, catalysts that must be recycled).
  - Demand contracts arrive over time; bankruptcy is possible.
  - Actions are **code-as-action**: a Python API as in FLE, over 300 agent turns of 2,000 ticks. Code is the declared construct; there is no engine access.
  - Intricacy comes from the explore/exploit trade-off on recipes, spatial layout, throughput bottlenecks and cash flow.
- **Example.** Turn 12: `lab.try(machine="kiln", inputs={"ore_b":2,"sand":1})` returns `glass_x ×1, slag ×1`. The agent then finds that slag clogs belts after 200 ticks unless it is routed to a "grinder" it hasn't discovered yet.
- **Novel instances and families.**
  - The recipe graph, logistics primitives and map are generated per seed from a secret pool, so the Factorio wiki knowledge that helps in FLE is useless.
  - Public seeds use a disjoint primitive set.
  - A 60-second hands-off holdout at the end blocks the manual-crafting exploit FLE reported (D §2.11).
- **Scoring.**
  - **V/V\***: delivered value divided by an operator oracle planner's value. The planner knows the recipe graph, uses MILP layout and heuristic scheduling, and gives an absolute anchor. The ratio is uncapped if the oracle is beaten.
  - Also reported: experiments per recipe edge discovered, and bankruptcy rate.
  - 20 seeds per model, with CIs.
  - Cost: about 6k turns with large context, roughly **$1.5–3k per model** [speculation].
- **Human baseline.** 40 experienced automation-game players who code plus 40 software engineers. They use the same API in a notebook with a visualiser, under the same turn budget, over two 90-minute sessions, paid by V/V\*.
- **Expected human vs AI** [speculation]: frontier above the median engineer on V/V\* by 2027, but maybe below expert players at launch. FLE called 2025 models "shockingly bad" at Factorio (D §2.11).
- **Expected model separation** [speculation]: large. FLE error rates ran 22.99% to 40.89% across labs; Vending-Bench 2 shows a wide spread plus inversions (B §3.2).
- **Evidence links:** P2, P9, P12, P13, P14. D §2.11, §4. B §3.2, §5.
- **Risks.**
  - Long-horizon variance: Vending-Bench 2 bands reach ±$2.1k (P2).
  - Oracle quality drifts.
  - Close to FLE and Vending-Bench, so the twist (secret tech tree, oracle normalisation) has to be shown to change rankings.
  - FLE open play was "prohibitively expensive" (D §2.11).
- **Closest prior art:** FLE (known Factorio rules, stale leaderboard), Vending-Bench 2 (dollar-scored, no oracle, no human baseline), Craftax. This design differs through a hidden, generated tech tree, an oracle-normalised absolute score and human engineers on the same API.

### G6. Cartographer & Scout
- **Archetype:** A1. **Format:** game (asymmetric cooperative).
- **Construct:** converting between an allocentric map and egocentric views through a narrow language channel. It combines spatial mental models, visual grounding and communication, and matters for embodied and computer-use agents directing or following people.
- **Core mechanics.**
  - Procedurally generated 3D worlds with **unnamed, generated landmark objects**, symmetric layouts that force disambiguation, and dynamic elements (switch-controlled doors, patrols visible only to the Scout).
  - The **Cartographer** sees a top-down schematic image with the goal and hazards, but not the Scout's position or heading.
  - The **Scout** sees 4 egocentric frames per step and moves.
  - Messages are capped at 20 words each and alternate; the limit is 60 turns.
  - Every 5 turns the Cartographer submits a guess of the Scout's position.
  - Roles swap between games.
- **Example.** Scout: "Facing a lumpy teal arch, a striped cone to its right." Cartographer, who sees two teal arches: "Is there a ramp behind you?" Scout turns: "yes." The Cartographer's localisation now resolves to the NE arch: "Go through, then left at the cone."
- **Novel instances and families.** World generators, landmark shape grammars and render styles are secret; one render style is held out per season. A symbolic-grid ablation measures the "perception tax".
- **Scoring.**
  - Success rate.
  - Path efficiency: optimal path length divided by actual.
  - Localisation latency: turns until the position guess is correct (objective).
  - Headline: human–model dyad score over human–human dyad score.
  - Cost: about 400 role-episodes with image inputs, roughly **$1.5k per model** [speculation].
- **Human baseline.** 100 human–human dyads plus 100 human–model dyads per model. General public, turn-based (no reaction-time edge), same frames and resolution, 40 minutes, pay per success.
- **Expected human vs AI** [speculation]: large A1 gap at launch.
  - MMSI-Video: humans 96.4 vs best model 38.0 (A §2.14).
  - MindCube: about 95 [uncertain] vs 61–76 (A §2.13).
  - Against: VSI-Bench nearly closed after targeted spatial training (A §2.12).
- **Expected model separation** [speculation]: large and lab-ordered by vision. BabyVision: Gemini 3 Pro 49.7, GPT-5.2 34.4, Claude 4.5 Opus 14.2 (Jan 2026 models, E Q2).
- **Evidence links:** P8, P10, P17, P20. A §2.12–2.14, §4 lessons 4–5. E Q1.
- **Risks.**
  - Synthetic 3D training could close the gap within about 12 months (the ClockBench pace, A §2.9).
  - Rendering artefacts.
  - Harder to attribute failures to perception vs language (mitigated by the symbolic ablation).
  - Live dyad logistics.
- **Closest prior art:** HCRC Map Task, Talk the Walk, CerealBar, TEACh, vision-language navigation. This design differs through generated unnamed landmarks, human–model mixed dyads, a localisation probe and a maintained frozen protocol.

### G7. Deep Seasons
- **Archetype:** A1. **Format:** game (roguelike campaign).
- **Construct:** learning across episodes: discovering hidden mechanics and turning them into better play across permadeath runs, with memory limited to a fixed-size notebook. This ranks second among under-measured abilities in E Q3 (CL-bench best 23.7%) and is what "on-the-job learning" means for agents.
- **Core mechanics.**
  - A tile roguelike with a **secret mechanics set per campaign**:
    - 20 unidentified items with generated, sometimes conditional effects;
    - monster behaviour primitives (mirrors your last action, splits when burned, flees at low HP);
    - liquid, fire and weather interactions;
    - crafting.
  - Mechanics stay fixed across 10 runs; maps change.
  - Each run lasts up to 400 turns, with macro-actions (travel, auto-explore) to limit tokens.
  - Between runs the agent writes a **notebook of at most 3,000 tokens**, which is its only memory in the Notebook track. A Full-log track is reported alongside.
  - Intricacy comes from combinatorial mechanic interactions, irreversibility and risk management.
- **Example.** Run 2 notebook: "Violet flask = heal ONLY when hungry, else poison(3). Grey slimes split on fire; use cold." Run 6: the agent saves violet flasks for when it is starving and carries a frost wand to the slime floor. It reaches depth 7, against depth 3 in run 1.
- **Novel instances and families.** The mechanic primitive pool is secret, rotated every 6 months, with a held-out split. There is no wiki, unlike NetHack, whose ascension used the wiki and source code (D §2.6). In the Open track, code is allowed (simulators and statistics).
- **Scoring.**
  - **Learning Slope:** mean normalised score in runs 7–10 minus runs 1–3. Normalised means (score − naive bot) / (oracle bot − naive bot), where the oracle knows the mechanics.
  - **Final Competence.**
  - **Mechanic Fidelity:** 30 post-campaign probes checked against engine truth, scored with an abstention-aware rule (P11).
  - 8 campaigns per model.
  - Cost: roughly **$2–4k per model** [speculation].
- **Human baseline.** 60 roguelike players and 60 general gamers, 10 runs over about 4 hours in 2–3 sessions, same tile rendering, same notebook box. Humans also have native memory; this asymmetry is disclosed and bounded by the Full-log track.
- **Expected human vs AI** [speculation]: humans show steeper slopes at launch. Evidence:
  - BALROG NetHack under protocol: 13.24% (A §2.16).
  - CL-bench's best is 23.7% (Feb 2026 models; not re-run on Jul–Sep 2026 models [uncertain]).
  - Continual Learning Bench: no reuse of knowledge across episodes (E summary 6).
  - Against: state-preserving harnesses flipped ARC-AGI-3 (F §1).
- **Expected model separation** [speculation]: large, driven by the quality of notebook abstractions. BALROG's spread runs from 68.3 down to 3.7 (D §2.6).
- **Evidence links:** P9, P10, P11, P18. A §2.16. D §2.6–2.7. E Q3 rank 2. F §1.
- **Risks.**
  - The notebook protocol decides the score, as the ARC-AGI-3 Adapter did, so it is frozen and BYOH is reported.
  - Macro-actions may trivialise the game.
  - Human memory breaks strict parity.
  - Cost and variance on long runs.
- **Closest prior art:** BALROG/NetHack (known game, tiny n), NetHackers (bot-writing), Craftax, ARC-AGI-3 levels, Continual Learning Bench. This design differs through secret per-campaign mechanics, a scored learning slope under a fixed memory budget and mechanic-fidelity probes.

### G8. Season Forge
- **Archetype:** A2, including against human programmers. The top humans may still win (A1 at the elite tier). **Format:** game (bot-writing tournament).
- **Construct:** building a competitive agent for a never-seen strategic game under a fixed time budget: reading the spec, experimenting, engineering and tuning. This is close to valued software work (P14), and CodeClash and NetHackers show bot-writing is a distinct construct (D §2.22, §2.6).
- **Core mechanics.**
  - Each quarter a **secret new game** is released at T0: a 2–4 player simultaneous-move territory and economy game with fog of war, 200–500 turns, 2–3 mini-variants.
  - The release includes a rules document, an engine binary and a local runner.
  - Every entrant gets the same package and **6 hours of wall-clock time on 8 CPU cores**:
    - models in a frozen minimal agent harness, plus a BYOH track;
    - human programmers;
    - human-plus-AI teams.
  - Bots then play a large round robin on **private maps** plus fixed anchors: random, greedy, and the operator's strong bot written with 10× the time.
  - Intricacy comes from emergent meta-strategy and the trade-off between scouting, economy and aggression.
- **Example.** Season 2027-Q1, "Tidewell": the map floods in a pattern that is hidden but inferable. Bots must learn from local runs that the flood cycle is 37 turns and schedule harvests to match. The best 2026 agents' logs show them writing a flood predictor at hour 2.
- **Novel instances and families.** The game is new each season and designed and generated in secret, so there is no contamination. Evaluation maps are private. Training on "write a bot for a new game" is the valued skill itself and is welcome.
- **Scoring.**
  - Anchored Bradley-Terry rating against the fixed bots.
  - Headline: **percentile among that season's human entrants**, which is absolute to a contemporaneous human field.
  - 3 independent agent attempts per model to measure variance.
  - Cost: roughly **$1–3k per model per season** [speculation]. Human prizes (about $20–50k per season) are shared across models [speculation].
- **Human baseline.** 50–100 veterans of competitive programming and game-AI contests (e.g. Battlecode, Halite), solo, 6 hours, same sandbox, prize-incentivised. The human-only track bans AI assistance, enforced by proctoring and telemetry.
- **Expected human vs AI** [speculation]: frontier agents beat the median human entrant; the top human may still win. The heuristic-contest precedent is background, not verified here.
- **Expected model separation** [speculation]: large. Agentic coding separates labs (Terminal-Bench reversals, E Q2). CodeClash has run 2,000+ tournaments (D §2.22).
- **Evidence links:** P1, P4, P14, P17, P19, P20. D §2.6, §2.22, §5.
- **Risks.**
  - Only 1–3 games per season means high per-season rank variance, so rolling averages across seasons are needed.
  - Humans cheating with AI.
  - Human prizes are the main cost.
  - Harness dependence (the BYOH delta is published).
- **Closest prior art:** CodeClash (known arenas), NetHackers (fixed game), Battlecode, Halite, Lux AI, AtCoder heuristic contests. This design differs through a secret game released simultaneously to humans and AIs under an identical budget, an anchored ladder and private evaluation maps.

### G9. Nomic Engine *(bold)*
- **Archetype:** A2. **Format:** game (self-amending rules).
- **Construct:** reasoning about the consequences of formal rule changes under adversarial politics: reading specs, finding loopholes, forming coalitions, and representing proposals honestly. It is a sanctioned sandbox for reward hacking, and relevant to contracts, policy and security review.
- **Core mechanics.**
  - 5 players. The "constitution" is about 40 rules in a sandboxed, typed DSL that the engine executes.
  - Constitutions are generated from a secret grammar with **2–4 planted loopholes** of known classes: quorum edge cases, precedence conflicts, self-amendment paths, overflow, order-of-resolution bugs.
  - Each turn: a proposer submits a DSL patch plus a structured effect summary. Every player answers 5 engine-generated **consequence probes**. Then a vote, execution, and points.
  - Both humans and models get the same dry-run budget (10 simulations per turn).
  - Intricacy comes from recursive self-modification, coalition dynamics and exploit races.
- **Example.** Rule 17: "a proposal passes with ≥ 60% of votes cast." Rule 22 lets a player abstain *and* have their vote counted as "cast = no" only if they hold fewer than 10 points. Probe: "If P4 (8 points) abstains, does proposal #31 pass with 2 yes votes?" Answer: yes (2/3 ≥ 60%). A loophole-aware player times proposals for when low-point players abstain.
- **Novel instances and families.** Constitutions, the DSL surface syntax and the loophole classes rotate. One loophole class is held out per season. Closed track: no code except the dry-run tool. Open track: code allowed.
- **Scoring.**
  - (1) **Probe accuracy**, exact and objective; this is the headline.
  - (2) Win share in duplicate anchor tables.
  - (3) Loophole ledger: planted loopholes discovered, exploited or patched, detected from engine traces.
  - (4) Misrepresentation rate: structured summary vs engine diff, as conduct telemetry.
  - Cost: about 120 games, roughly **$0.5–1k per model** [speculation].
- **Human baseline.** 60 law and CS students plus board gamers, a GUI over the same DSL, 2-hour sessions, paid for probe accuracy and wins.
- **Expected human vs AI** [speculation]: frontier above the median human on probe accuracy.
- **Expected model separation** [speculation]: large on probes; lab-specific on conduct, echoing Vending-Bench Arena cartels (Fable 5 initiated them, Opus 5 joined in 6 of 6 runs; D §2.19). A Nomic study reports non-monotonic collective behaviour with model scale ([web, S]).
- **Evidence links:** P4, P11, P12, P15. D §2.19. B §5 lessons 5 and 10. G §2 (gaming).
- **Risks.**
  - Construct sprawl.
  - Degenerate games (instant-win amendments); needs entrenched rules and turn caps.
  - Prompt injection inside proposals.
  - Relevance to real contract work is speculative (P14 test required).
- **Closest prior art:** Nomic (Suber 1982); NomicLaw ([arXiv 2508.05344](https://arxiv.org/pdf/2508.05344), [web, S]), which has LLMs propose and vote on legal rules in natural language; a Nomic LLM scaling study ([web, S]). This design differs through executable constitutions, planted loopholes with ground truth, exact consequence probes and anchored tables.

### G10. Exploitability Gauntlet
- **Archetype:** A2. **Format:** game (imperfect-information strategy).
- **Construct:** equilibrium-quality strategic reasoning under hidden information (mixing, bluffing, the value of information) in games no one has solved before. The key property is an **opponent-independent absolute score**, which fixes the pool-relative-rating problem (§3 failure mode 10).
- **Core mechanics.**
  - Small two-player zero-sum games from a secret grammar: generated decks, sealed bids, simultaneous moves, trump flips, generated bet structures, dice.
  - Each game has 200–5,000 information sets, so exact CFR and best response are cheap offline.
  - The rules are given, because this tests strategy rather than rule learning.
  - The model plays hands *and* is queried in **policy-elicitation mode**: it outputs action probabilities at each information set, or at a stratified sample for larger games.
  - It also plays 200 hands against fixed exploitable bots to test adaptation.
- **Example.** "Tri-Draft": 7-card deck, each player drafts 2 of 3 face-down, then a sealed bid of 0–3 chips, and the high card after a trump flip wins. The elicited policy at infoset (holding {5,T}, opponent bid 2) is {fold .35, call .50, raise .15}. Exact best response shows an exploitability of 41 milli-pots per hand.
- **Novel instances and families.** The grammar is secret and seasonal, with held-out mechanics.
  - Closed track (headline): no code.
  - Open track: code allowed. Writing CFR for a new game is expected to be near-trivial for frontier coders; that is reported as a "solver-writing" check.
- **Scoring.**
  - **Normalised exploitability**, exact and absolute.
  - Exploitation EV against fixed bots.
  - Consistency between elicited and in-play actions.
  - Difficulty knob: information-set count (P2).
  - Cost: about 24 games × 400 elicitations, roughly **$0.5–1k per model** [speculation].
- **Human baseline.** 60 poker and strategy players plus 60 general public. Humans give slider elicitation on games with 200 or fewer information sets and play the same bots. 60 minutes, paid by EV against a bot.
- **Expected human vs AI** [speculation]: frontier models are less exploitable than most humans.
- **Expected model separation** [speculation]: large and not in exam order. LLM Chess spreads from Astra at 1614 to Opus 5 at 1285 (D §2.20). Exact exploitability has been computed for LLM poker policies ([riverline](https://github.com/Lironktf/riverline), [web, S]).
- **Evidence links:** P2, P4, P15, P16. D §2.18, §2.20. G §3.
- **Risks.**
  - A narrow construct with weak ties to valued work (P14).
  - Small games may be solved in-head by the frontier, so the size knob matters.
  - Probabilities can be elicited poorly; the consistency check mitigates this.
- **Closest prior art:** riverline (Kuhn, Leduc, HUNL, known games); Kaggle HU NLHE (pool-relative BB/100); GTBench. This design differs through secret new games each season, absolute exploitability as the headline and a human elicitation baseline.

### G11. Eleusis Masters *(bold)*
- **Archetype:** both. Solving is expected to be A1 at launch; setting is A2. **Format:** game (rule-discovery duel with setter and solver roles).
- **Construct:**
  - Solvers: scientific experimentation efficiency plus rule fidelity, i.e. being right for the right reason. This ranks #1 among Phase 2 targets (§5c).
  - Setters: designing rules that discriminate, including rules that are solvable by humans but hard for AI, which requires modelling how other minds differ.
- **Core mechanics.**
  - 1 setter and 4 solvers. Cards are generated with 4–6 attributes, some perceptual (rendered texture and shape) and some symbolic.
  - The setter writes a secret rule in a **seasonal DSL with rotating primitives**. The engine checks the rule is valid and accepts 20–60% of random plays.
  - Solvers take turns playing cards as experiments; accept or reject is public.
  - Any solver may **declare** a rule in the DSL. It is tested on 50 held-out probe sequences.
  - Eleusis scoring rewards the setter when solvers are *spread*: some find the rule, not all.
- **Example.** Secret rule: "a card is accepted iff its count of convex vertices differs in parity from the previous accepted card's *hue sector*." Solver A plays three near-identical shapes varying only the hue (an informative experiment). Solver B repeats accepted cards (uninformative). A declares at turn 14; fidelity 50/50.
- **Novel instances and families.**
  - The DSL primitives are secret and rotate; each season holds out a primitive split.
  - Setter outputs, after validation, become the next season's item bank, so the benchmark renews itself.
  - A small, known rule space is enumerable, as the 68-rule catalogue in cogame-eleusis shows (F §2). This design counters that with a secret DSL, perceptual attributes, and a Closed (no-code) headline track.
- **Scoring.**
  - Solver: median experiments to a correct declaration, and fidelity on probes, anchored against a Bayesian-ideal solver where the DSL permits and against humans.
  - Setter: **Discrimination** on a fixed solver panel of frozen models plus a human panel. The "human-solvable, AI-hard" rate is reported separately.
  - Cost: **under $0.5k per model** for tokens [speculation]. The human panel is shared across models.
- **Human baseline.** 100 solvers in tables (the ZendoWorld template: 19 people, 10 plays per game, F §2, scaled up) and 30 human setters. 20 minutes per rule, same rendering, paid per correct declaration.
- **Expected human vs AI** [speculation]: humans ahead on solver efficiency and fidelity at launch.
  - ZendoWorld: 73.3% vs 44.5% (F §2).
  - ConceptARC wrong-rule answers: 27% for models vs 8% for humans (E Q1).
  - FalsifyBench: "no model comes close to optimal" (F §2).
  - All of these predate the Sep 2026 frontier.
- **Expected model separation** [speculation]: large, especially in the setter role, which static benchmarks never measure.
- **Evidence links:** P3, P7, P9, P11, P20. F §2–4. E Q1, Q3 ranks 3 and 6. §5c rows 1 and 8.
- **Risks.**
  - Setters may converge on degenerate rule styles (validity filters are needed).
  - The DSL leaks after a season.
  - Declaring rules is harder for humans in a DSL; offer a guided rule builder to both humans and models.
  - Closes fast once targeted (ARC-AGI-3 precedent).
- **Closest prior art:** Eleusis (Abbott); the Hugging Face "Game of Science" Eleusis benchmark (solver-only, with a "boldness" index) ([HF space](https://huggingface.co/spaces/huggingface/eleusis-benchmark), [web, S]); cogame-eleusis; ZendoWorld; WILT. This design differs through the adversarial setter role, a secret rotating DSL, perceptual attributes, fidelity probes and human tables.

### G12. Crowd Oracle *(bold)*
- **Archetype:** both. The predicted result is A2, but it is genuinely uncertain. **Format:** game (coordination and anti-coordination against a recorded human population).
- **Construct:** a strategic model of *people*: salience, level-k reasoning and focal points on novel stimuli. It matters for product design, forecasting, negotiation, and for detecting **AI–AI tacit coordination** (collusion) that is stronger than AI–human coordination.
- **Core mechanics.** Six game types per season, about 600 fresh items:
  - (a) pure coordination: pick the same cell or image as a random stranger, on generated maps and images;
  - (b) beauty-contest variants;
  - (c) hide-and-seek on generated maps, with payoffs set by the human hider and seeker distributions;
  - (d) minority / El Farol congestion games;
  - (e) "the move most humans make" in novel board positions;
  - (f) ultimatum offers, paid by the human acceptance curve.
  - Items are one-shot, but the payoff landscape is a live population.
- **Example.** A generated island map with 64 cells: a lighthouse, two identical coves, a lone red hut. "Pick where to meet a stranger." In the human data 41% pick the red hut and 22% the lighthouse. A model picking the geometric centre scores 3%.
- **Novel instances and families.** Items are generated fresh each season. The human panel data (at least 300 responses per item from about 1,000 representative adults, incentive-paid) stays private and is re-collected every season, so memorised focal points ("Grand Central at noon") don't apply. Code is irrelevant; tools are allowed.
- **Scoring.**
  - Expected payoff against the empirical human distribution.
  - **Human baseline = leave-one-out payoff:** each human is scored against the others. The ceiling is the modal-choice payoff.
  - The AI–AI coordination rate is reported as a separate safety axis.
  - Cost: **under $100 per model** [speculation]. Human data costs about $10–15k per season, shared [speculation].
- **Human baseline.** The panel itself: a representative sample of about 1,000 people (P17), recruited by country to capture cultural variation. The distribution is reported per stratum.
- **Expected human vs AI** [speculation]: frontier models may beat the median individual human at hitting the mode, having absorbed aggregate human text. Visual and spatial items may favour humans.
- **Expected model separation** [speculation]: unknown; plausibly large. Output homogenisation across labs (Artificial Hivemind, E Q3 rank 8; contested) predicts AI–AI coordination well above AI–human coordination.
- **Evidence links:** P14, P16, P17. E Q3. D §2 (the "Epistemic Schelling Points" title, 2607.11363 [S]).
- **Risks.**
  - Strategic depth is modest; the intricacy lies in modelling people, not in the rules.
  - Culture dependence.
  - It rewards being average.
  - It may simply measure "silicon sampling" fidelity.
  - Static items could leak once scored, so they are re-collected each season.
- **Closest prior art:** Schelling focal-point experiments; beauty-contest LLM studies; the Epistemic Schelling Points paper. This design differs through incentive-paid, private, seasonal human-population payoffs with a leave-one-out human baseline, generated stimuli and an AI–AI vs AI–human coordination gap.

### G13. Strange Billiards
- **Archetype:** A1. **Format:** game (turn-based physical duel).
- **Construct:** learning novel physical dynamics online from video, then planning precise actions. It combines intuitive physics, system identification and adversarial planning, and matters for embodied agents and for any "learn how this system behaves, then act" task.
- **Core mechanics.**
  - A top-down rendered table with 6–10 balls, pockets and obstacles.
  - Physics per match is **hidden and generated** from a secret pool: gravity wells, invisible anisotropic friction zones, velocity-dependent restitution, attraction between same-coloured balls, delayed bumpers, wrap-around edges.
  - Each turn: choose angle, power and spin (continuous), then watch a 16–32 frame clip.
  - Before each shot, the player predicts the cue ball's resting point. This is the probe.
  - The opponent is an anchor bot with the true physics and a search at fixed execution-noise levels (a ladder).
- **Example.** Shots 1–4 reveal that balls curve toward the NE corner more strongly the slower they move (a velocity-dependent well). The model's prediction error drops from 31 cm to 9 cm by shot 10. It then plays a deliberately slow bank shot that curls around a blocker.
- **Novel instances and families.**
  - Physics primitives are secret, with a held-out split, rotated each season.
  - Closed track (headline): frames only, no code.
  - Open track: code sandbox (CV plus fitting) = system identification.
  - A coordinates-as-text ablation isolates the perception share.
- **Scoring.**
  - Anchored rating against the bot ladder.
  - **Physics-learning curve:** prediction error in shots 1–5 vs shots 20–25, measured exactly in engine units.
  - Win rate.
  - Cost: about 200 matches, roughly **$1k per model** [speculation].
- **Human baseline.** 100 casual gamers. Same clips, turn-based with no time pressure, a drag-to-aim input quantised to the model's precision, no trajectory preview for anyone. 45 minutes, pay per win.
- **Expected human vs AI** [speculation]: A1 at launch.
  - IntPhys 2: 96.44 vs 57.51 (A §2.15).
  - The AIBIRDS man-vs-machine challenge has been won by humans every year since 2013; in 2022 the best human scored 251,710 vs 144,630 for the best AI ([aibirds.org](https://aibirds.org/man-vs-machine-challenge.html), [web, S]).
  - Caution: VPCT is nearly closed on static images (91% vs 100%, A §2.10).
- **Expected model separation** [speculation]: large, and ordered by vision skill (E Q2).
- **Evidence links:** P2, P8, P9, P10, P17. A §2.10, §2.15. E Q3 rank 4.
- **Risks.**
  - Synthetic physics-video training may close the gap quickly (ClockBench went from 13.3 to 66.7 in about 12 months).
  - Continuous-action precision could confound the result; quantise and control with the coordinates ablation.
  - "Only a game" framing (P19).
- **Closest prior art:** AIBIRDS (known physics, non-LLM agents); PHYRE, Physion, IntPhys 2 and VPCT (non-adversarial, fixed physics). This design differs through hidden per-match physics learned online, an adversarial anchored ladder and exact prediction probes.

---

## Summary table and self-scored rubric [speculation]

Q1–Q6 follow the Phase 2 rubric (§7). The decision rule is: no 1s, at least 4 on Q1, Q3 and Q5, and a mean of at least 3.5. These are my own provisional scores for the Phase 4 red team.

| # | Name | Arch. | Headline metric (absolute anchor) | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Mean | Passes rule? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | Blind Rules Gauntlet | both | Gauntlet rating vs ISMCTS ladder; blind–revealed gap | 4 | 4 | 4 | 4 | 4 | 4 | 4.0 | yes |
| G2 | Convention Crucible | both | Cross-play score with hidden-convention bots; human-team ratio | 4 | 3 | 3 | 3 | 4 | 3 | 3.3 | no (Q3) |
| G3 | Glyph Pact | A1 | Human–model vs human–human dyad accuracy × efficiency | 3 | 2 | 4 | 4 | 4 | 3 | 3.3 | no (Q1) |
| G4 | Masquerade | A2 | Detection and deception bits from proper-scored beliefs | 4 | 4 | 3 | 3 | 3 | 5 | 3.7 | no (Q3, Q5) |
| G5 | Unknown Factory | A2 | V/V\* against an oracle planner | 4 | 4 | 4 | 3 | 3 | 4 | 3.7 | no (Q5) |
| G6 | Cartographer & Scout | A1 | Dyad success and localisation vs human dyads | 3 | 3 | 4 | 4 | 3 | 3 | 3.3 | no |
| G7 | Deep Seasons | A1 | Learning slope, normalised naive→oracle | 4 | 4 | 4 | 4 | 3 | 4 | 3.8 | no (Q5, cost) |
| G8 | Season Forge | A2 | Percentile among same-season human entrants | 5 | 5 | 3 | 4 | 3 | 5 | 4.2 | no (Q3, Q5) |
| G9 | Nomic Engine | A2 | Exact consequence-probe accuracy | 4 | 4 | 3 | 3 | 4 | 4 | 3.7 | no (Q3) |
| G10 | Exploitability Gauntlet | A2 | Exact exploitability | 4 | 3 | 4 | 3 | 5 | 2 | 3.5 | yes (borderline) |
| G11 | Eleusis Masters | both | Experiments-to-rule plus fidelity; setter discrimination | 4 | 4 | 4 | 4 | 4 | 4 | 4.0 | yes |
| G12 | Crowd Oracle | both | Payoff vs human population; leave-one-out human baseline | 4 | 3 | 3 | 5 | 5 | 3 | 3.8 | no (Q3) |
| G13 | Strange Billiards | A1 | Anchored rating plus physics prediction-error curve | 4 | 3 | 4 | 4 | 4 | 4 | 3.8 | yes |

**Panel recommendation** [interpretation]:
- **Carry forward:** G1, G11 and G13, which pass the rule, plus G7 and G8. The latter two fail only on cost or noise, which a budget could fix.
- **Strongest single flagship:** "Blind Rules Gauntlet". It has three built-in mechanism ablations (blind vs revealed, Closed vs Open, symbolic vs rendered), which address P20's "hard for AI vs hard in general" requirement.
  - It could absorb G13 (physics families) and G11 (setter-generated families) as sub-leagues, giving a multi-league "game decathlon" under one brand and harness (P19).
- **Most interesting A2 add-on:** G4's proper-scored belief channel. It could be bolted onto any multi-agent card to give objective detection and deception metrics.

## New web checks (30 Sep 2026, search excerpts only [S])
- Repeated reference games: human dyads rise from 78% to 96%, while agents are "aligned but not partner-specific". [arXiv 2606.08081](https://arxiv.org/abs/2606.08081)
- Counterpoint: [arXiv 2602.08208](https://arxiv.org/html/2602.08208).
- Post-training for convention formation: [arXiv 2508.06482](https://arxiv.org/pdf/2508.06482).
- Humans win the AIBIRDS man-vs-machine challenge (2022: 251,710 vs 144,630): [aibirds.org](https://aibirds.org/man-vs-machine-challenge.html).
- Nomic with LLMs: NomicLaw [arXiv 2508.05344](https://arxiv.org/pdf/2508.05344); [cooperate.com post](https://content.cooperate.com/post/nomic/).
- Exact exploitability of LLM poker policies: [riverline](https://github.com/Lironktf/riverline).
- Hugging Face Eleusis benchmark (solver-only): [HF space](https://huggingface.co/spaces/huggingface/eleusis-benchmark).
