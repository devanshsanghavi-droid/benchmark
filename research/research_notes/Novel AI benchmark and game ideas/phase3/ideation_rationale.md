# Phase 3 ideation rationale (companion to `candidates_spec.md`)

As of 30 Sep 2026. This file collects everything that was deliberately left out of the neutral spec file:
- source idea IDs and merges;
- the ideators' expected results and expected separation;
- evidence links, self-scores, known risks, prior art and cited factual claims;
- panel recommendations and a coverage-and-gaps note.

It is written for the Phase 4 organisers, not for the blind red-team pass.

**Sources consolidated.** All paths are in `phase3/`:
- `ideas_H_human_gt_ai.md` (H1–H13, A1 lens);
- `ideas_D_ai_gt_human_discriminative.md` (D1–D14, A2 lens);
- `ideas_G_games.md` (G1–G13, games lens);
- `ideas_W_wildcard.md` (W1–W12 plus §3 twists).

Principles P1–P20, the §5 opportunity map, the §6 Must items (M1–M11) and the §7 rubric are in `../phase2/design_principles.md`. Dossier references ("A §2.3", "E Q1", …) point to `../phase1/`.

**Labels carried over from the sources.** They are preserved verbatim in this file.

| Label | Meaning |
|---|---|
| [speculation] / [spec] | The ideator's untested prediction. Every expected result and every cost estimate is speculation unless it cites evidence |
| [uncertain] / [uncertain: …] | Doubt carried over from the dossier fact-checks |
| [web], [web, S], [prior-art search] | The ideator's own quick web check, 30 Sep 2026, from search excerpts only. Not verified; treat as uncertain |
| [bg] / [background] | The ideator's background knowledge, not verified |
| [I] / [interpretation] | The ideator's interpretation |
| [S] (inside dossier citations) | The dossier marked the figure as coming from a search summary |

**Self-scores.** These are each ideator's own scores on the Phase 2 §7 rubric, 1–5 each:

| Code | Question |
|---|---|
| Q1 | Could it be trained on or gamed? |
| Q2 | Will it saturate quickly? |
| Q3 | Does it separate models, or humans from AI? |
| Q4 | Can a human baseline be measured fairly? |
| Q5 | Is scoring objective and cheap? |
| Q6 | Would people care? |

The decision rule [interpretation, Phase 2]: no score of 1; at least 4 on Q1, Q3 and Q5; and a mean of at least 3.5. All self-scores are [speculation] and are for the red team to overturn.

---

## 1. Source → candidate map

| Candidate | Name | Source idea(s) | Merge? |
|---|---|---|---|
| C01 | Kinetic | H1 | — |
| C02 | Live Rig | H4 | — |
| C03 | Novel Expert | H7 | — |
| C04 | Earworm | H11 | — |
| C05 | Stump Arena | H3 (+ W §3 twists) | — |
| C06 | Alien Physics | **H10 + G13** | merged |
| C07 | Tacit Signals | H2 (+ W §3 twist) | — |
| C08 | Glyph Pact | G3 (+ W §3 twist) | — |
| C09 | First-Run Arcade | H5 | — |
| C10 | Two Clocks | H13 | — |
| C11 | Wayfinder | H9 | — |
| C12 | Cartographer & Scout | G6 | — |
| C13 | Deep Seasons | G7 | — |
| C14 | Kelly Exam | D1 | — |
| C15 | Prospective Self-Forecast | W3 | — |
| C16 | Pushback Ledger | D12 | — |
| C17 | Reliability Horizon | D13 | — |
| C18 | Compaction Chronicle | D4 | — |
| C19 | Frozen-Student Tutor | D3 | — |
| C20 | Misconception Clinic | W1 | — |
| C21 | Simulated Futures Exchange | D10 | — |
| C22 | Long-Tail Futures | W5 | — |
| C23 | Hunch Lab | W6 | — |
| C24 | MDL Arena | W7 | — |
| C25 | Mechanism Lab | W10 | — |
| C26 | Contractor's Auction | D2 | — |
| C27 | Signal Pit | D7 | — |
| C28 | Hidden-Dynamics Economy | **D8 + G5** | merged |
| C29 | Whodunit Engine | D5 | — |
| C30 | Masquerade | G4 | — |
| C31 | Debate Court | W12 | — |
| C32 | Nomic Engine | G9 | — |
| C33 | Exploitability Gauntlet | G10 | — |
| C34 | Setter's Duel | D6 (+ W §3 twist) | — |
| C35 | Game Designer's Duel | W8 | — |
| C36 | Season Forge | G8 | — |
| C37 | Saboteur's Patch | D9 (+ W §3 twists) | — |
| C38 | Relay | W9 | — |
| C39 | Blind Spot Cartographer | W2 | — |
| C40 | Rules Gauntlet | **G1 + D14** | merged |
| C41 | Practice Week | H6 | — |
| C42 | Hidden-Rule Lab | **H8 + W4** | merged |
| C43 | Eleusis Masters | G11 (+ W §3 twists) | — |
| C44 | Convention Cross-Play | **D11 + G2** (+ W §3 twist on D11) | merged |
| C45 | Crowd Oracle | G12 | — |
| C46 | Grift | H12 | — |
| C47 | Defuse Line | W11 | — |

52 source ideas were consolidated into 47 candidates through 5 merges. No idea was dropped.

---

## 2. Merge log

### Merges performed

1. **C06 = H10 Alien Physics + G13 Strange Billiards.**
   - Same ability: infer an unfamiliar physical law from video, then plan actions with it.
   - Same generator type: a secret pool of altered-physics primitives, rotated each season with a held-out split.
   - Same tool split: tools-off headline, and an open track that allows CV and fitting.
   - Kept from H10: the observe-then-act protocol (6 clips, 5 placement puzzles with 3 attempts each, 10 forced-choice predictions), the normal-physics control, and the 200-adult baseline. This became "puzzle mode".
   - Kept from G13: the interactive, adversarial duel against a true-physics bot ladder, the resting-point prediction probe with a prediction-error curve, the coordinates-as-text ablation, and the 100-casual-gamer baseline with quantised input. This became "duel mode".
   - Format is labelled "hybrid" because H10 was a benchmark and G13 a game.
2. **C28 = D8 Twin-Seed Colony + G5 Unknown Factory.**
   - Both fill the same slot: a single-agent, fully deterministic, long-horizon economic simulator with no LLM counterparties, hidden dynamics, irreversible bankruptcy, and scoring normalised to an oracle planner.
   - Both are A2 and cite the same prior art (Vending-Bench, FLE).
   - Kept from D8: the colony/business variant, hidden *drifting* dynamics, the typed tool API, common random numbers with antithetic seed pairs, regret against an MPC oracle, and a 150-day human version plus full-length experts.
   - Kept from G5: the factory variant, a secret recipe graph found through a costly lab-bench action, generated logistics primitives, code-as-action, a V/V\* oracle with MILP layout, the end-of-run hands-off holdout, and human engineers on the same API.
   - The two are presented as variants (a) and (b) of one environment family.
3. **C40 = G1 Blind Rules Gauntlet + D14 Rulebook Gauntlet.**
   - Both use a secret generator of novel two-player board games, an anchored MCTS/ISMCTS ladder rated by Bradley-Terry, and a play-vs-compile (Closed/Open) split.
   - D14 is essentially G1's "rules revealed" track with a long rulebook that contains rare edge-case rules.
   - Kept from G1: the blind track (legal-move list only, goal withheld), the learning curve over games 1–8, the blind-minus-revealed gap, about 60 families per season with 20% held-out primitives, and the 250-person first-exposure baseline.
   - Kept from D14: the rulebook track with a 20–30-page rulebook, the illegal-move rate, and the 80 hobby board-gamers who read the rulebook and then play.
4. **C42 = H8 Koan Lab + W4 Devil's Laboratory.**
   - The task format is the same: Zendo-style scene-building experiments, then labelling held-out probe scenes. So is the ability: experiment efficiency plus rule fidelity.
   - W4's own card says its mechanism "could be layered onto H8 or G11". W §3 proposes replacing H8's fixed hidden rule with W4's adaptive adversary.
   - Kept from H8: the 3D block world with physical-stability primitives, image-only state, divergence probes (intended vs shortcut rule), and AUC scoring relative to an ideal Bayesian reasoner and the human median.
   - Kept from W4: the adaptive adversary with worst-case held-out scoring, the text/JSON track, the rule-length cap, and the release gate (the median human must reach 90% worst-case accuracy within 30 experiments).
   - Archetype is set to "both" because W4 targets A2 on its text track, while H8 and W4's visual track target A1.
5. **C44 = D11 Stranger Coordination + G2 Convention Crucible.**
   - Same game family: generated, Hanabi-like, cooperative, hidden-information signalling games with no chat.
   - Same ability: zero-shot coordination, i.e. inferring an unfamiliar partner's conventions from its actions.
   - Same scoring core: cross-play with hidden-convention anchor partners, plus human cells.
   - Kept from G2: the grammar details, 8 scripted convention bots, 6-game matches, Cross-Play Score, Adaptation Gain and Human-Team Ratio.
   - Kept from D11: the frozen-model anchor partners, the self-play-minus-cross-play gap, and 200 humans playing 10 games each with random blind partners.

### Pairs considered but kept separate

These are genuinely distinct in the scored subject or the construct. They are flagged for possible bundling later.

- **C05 Stump Arena (H3) vs C39 Blind Spot Cartographer (W2).**
  - Both use identical gating: at least 3 of 5 naive paid humans within 3 minutes, and a frozen panel that fails at pass@3.
  - The scored subject differs. H3 scores models as *solvers* of human-authored items and uses human cost-to-stump as the headline. W2 scores models as *authors* who must fail their own items.
  - W2 already includes an "H3-style" human-author arm, so the two could share infrastructure.
- **C19 Frozen-Student Tutor (D3) vs C20 Misconception Clinic (W1).** Both score teaching by the outcome on frozen small models. W1 adds a secret planted misconception found by interactive probing, a do-no-harm term and a fine-tuning-data track. The W panel explicitly re-cut W1 to be distinct from D3.
- **C14 Kelly Exam (D1) vs C15 Prospective Self-Forecast (W3).** Both score log-wealth against a house line set by a frozen panel. D1 is a *retrospective* bet on an answer already given. W3 is a *prospective* forecast made before a blind attempt on a twin item, and includes triage.
- **C07 Tacit Signals (H2) vs C08 Glyph Pact (G3) vs C44 Convention Cross-Play.**
  - H2 jointly invents conventions with a live human over a *non-linguistic* channel.
  - G3 builds a *linguistic* lexicon for unnamed figures.
  - C44 infers the *pre-existing* hidden conventions of bots and strangers.
- **C09 First-Run Arcade (H5) vs C10 Two Clocks (H13).** The H panel suggested "an arcade with a dual-task mode" as a possible merge. The constructs differ: discovering a new game in real time, versus doing two tasks at once.
- **C41 Practice Week (H6) vs C40 Rules Gauntlet.** Both are novel games against MCTS ladders. H6's construct is multi-day learning with the rules given, and its headline is learning gain.
- **C06 (H10) vs C42 (H8).** The H panel suggested merging H8 and H10 into one "Lab" with physical primitives. It was not done, because H10's observe-then-act physics protocol is closer to G13 (merged into C06), while H8 is closer to W4.
- **C11 Wayfinder (H9) vs C12 Cartographer & Scout (G6).** Solo map-building versus a map-to-view dyad over language.
- **C29, C30, C31 and C46** (Whodunit, Masquerade, Debate Court, Grift) are all deception-related, but their formats differ: scripted-witness investigation, hidden-role deduction, oversight debate, and mixed human–AI trading.
- **C21, C22 and C23** (simulated, real-world and not-yet-run forecasting) have different sources of ground truth.

### Content moved out of the spec file

- **Per-track archetype expectations.** For example, "blind track A1 at launch; revealed track A2". These appear below.
- **Optional variants proposed in W §3** for other panels' ideas. They were omitted from the specs for length and neutrality, and are listed per candidate below.
- **Illustrative example numbers that read as outcomes or claims.** For example, D3's "11% / 34% / 58%" and G8's "best 2026 agents' logs show…". These are listed under the relevant candidate.
- **Minor protocol details dropped for the 180-word limit.** These are listed per candidate under "Spec omissions".

---

## 3. Panel-level context

### 3.1 Provenance of the "Common protocol" in the spec file

| Common-protocol item | H shared protocol | D shared defaults | G shared protocol | W chassis |
|---|---|---|---|---|
| 1 Sealed execution | P6, P15 | S1 (P6, P15) | S6 (P6) | 1 (P6, P15, M6) |
| 2 Release gates | null/spam gates (P15) | S1 | S6 (P15; ≥2 humans per family) | 4 (P15) |
| 3 Frozen harness + BYOH | P18 | S2 (P18) | S1, S2 | 2 (P18, M5) |
| 4 Tool tracks | tools-off primary; publish "tool-solvability gap" (P4) | per card | S2 Closed/Open/BYOH (P4, P18) | 7 (P4, M4) |
| 5 Anchors | — | S6 (P16, D §5) | S3 (P16, G R18) | 6 (P16, M11) |
| 6 Paired comparisons | — | S5 common random numbers | S4 duplicate format (Kaggle poker's 900k duplicate hands, D §2.18) | — |
| 7 Secrecy and renewal | — | S4 (P1, P3, P5, P7) | S5 (P1, P3, P7; Witness-style RL-on-gym check, F §3) | 3 (P1, P7, M3) |
| 8 Statistics | P16 | S5 (P16, G §3) | S7 | 5 (P16, M8) |
| 9 Human baselines | P17 | per card | S3, S6 | per card |
| 10 Reporting | P13 | S3 (P13), S7 (P11; B §3.5; B §5 lesson 10) | S7 (P11, P13) | 8 (P13, M10) |
| 11 Validity report | — | S8 (P14, G R19) | — | — |

Cited rationale behind the protocol items, as given by the panels:
- **Harness sensitivity.** ARC-AGI-3 scored 62.7% vs 98.6% for the same model depending on harness (A §2.3). Code world models plus search beat direct play (D §2.25 [uncertain]). Source: G S2.
- **Refusal accounting.** On NYT Connections, Opus 4.7's 39% came from refusals scored as zero. Source: D S7, citing B §3.5 and B §5 lesson 10.
- **Cost reference.** G's cost estimates assume frontier pricing of about $4 in and $20 out per 1M tokens (Opus 5.5 list price, B §4), with no caching discount [speculation]. Source: G S7.

### 3.2 H panel: moat taxonomy (A1 durability)

The H panel kept only ideas whose human edge rests on at least one "moat". A moat is an advantage a lab cannot close just by generating more data from the task family.

| Moat | Description | H ideas → candidates |
|---|---|---|
| M1 | Live humans inside the environment (partner, adversary or author) | H2 → C07, H3 → C05, H12 → C46 |
| M2 | The real physical world | H4 → C02 |
| M3 | Information that exists only in a dense perceptual or temporal signal | H1 → C01, H7 → C03, H11 → C04 (H's summary table also tags H9 → C11 and H10 → C06 as M3) |
| M4 | Real time and concurrency | H5 → C09, H13 → C10 |
| M5 | Learning a non-verbal skill at test time, with secret rotating primitives | H6 → C41, H8 → C42, H9 → C11, H10 → C06 (H's summary table also tags H5 → C09 and H7 → C03 as M5) |

- **H's context claims.**
  - Novel instances, and even novel task families, buy about 5 months once labs target them: ARC-AGI-3 went from under 1% to 62.7% on the standard harness and 98.6% on a provider harness (F §3; A §2.3).
  - Anything whose state can be written as text gets compiled into code and searched (P4; A §4 lesson 4).
  - Evidence that stand-in human-proxy agents fail to transfer: human–AI convention pairs fail [web: arXiv 2602.08208].
- **H's caveat: none of these moats is proven durable.**
  - ClockBench went from 13.3% to 66.7% in about 12 months.
  - VPCT reached 91% against 100% for 3 human volunteers.
  - VSI-Bench is nearly closed (A §2.9–2.12).
- **H's durability ranking:** M1 and M2 first, then M4. M3 and M5 only with secret primitives that rotate.
- **H's cross-cutting caveat.** Most of the anchors behind these gaps predate the Sep 2026 frontier: IntPhys 2, VideoGameBench, BabyVision, Concept and AutumnBench. Before building H1, H5 or H7–H11, run a quick pilot on Opus 5.5, GPT-6 Astra and Gemini 3.x.

### 3.3 Panel recommendations (verbatim intent, labelled by panel)

- **H panel.**
  1. Lead candidate: H2 Tacit Signals (C07). Its moat is the most structural, because the environment is people. There is fresh 2026 evidence that mixed human–AI pairs fail, and it has a clean human–human reference.
  2. Renewal backbone: H3 Stump Arena (C05). Its cost-to-stump headline has no ceiling.
  3. Cheap perception battery: H1 + H7 + H11 as one seasonal "Perception Season" (C01 + C03 + C04). These have the largest current gaps but are the most exposed to targeted training.
  4. Moonshot: H4 Live Rig (C02).
  5. Possible merges: H5 + H13, and H8 + H10.
- **D panel [speculation].**
  - Strongest: D2 Contractor's Auction (C26), which tells the "cheap beats expensive" story informatively.
  - D3 Frozen-Student Tutor (C19), described as "StudentBench fixed".
  - D6 Setter's Duel (C34) and D7 Signal Pit (C27): anchored, uncapped and deterministic.
  - Natural bundle: D1 + D2 as a "self-knowledge economy" (C14 + C26).
  - Falsification test for every card: if a pilot on about 15 models correlates above about 0.9 with ECI or the AA index after controlling for release date, the idea adds nothing (P14).
  - On their own scores, D2, D3, D6, D7 and D9 pass the decision rule.
  - Weak spots: D8 (cost, human baseline), D10 (public-family decay) and D13 (interest). D5, D11 and D14 need large game counts.
- **G panel [interpretation].**
  - Carry forward G1, G11 and G13, which pass the rule, plus G7 and G8, which fail only on cost or noise.
  - Strongest single flagship: G1 (now part of C40). It has three built-in ablations: blind vs revealed, Closed vs Open, and symbolic vs rendered. It "could absorb G13 (physics families) and G11 (setter-generated families) as sub-leagues", giving a "game decathlon".
  - Most interesting A2 add-on: G4's proper-scored belief channel (C30), which could be bolted onto any multi-agent card.
- **W panel [I].**
  - Carry forward W4 (now part of C42), W3 (C15), W6 (C23) and W2 (C39).
  - Combine W9 with W4: run Devil's-Lab domains inside Relay chains (C38 + C42).
  - Use W3's Self-Edge as a metacognition sub-score for any candidate.

---

## 4. Per-candidate rationale

Format per candidate:
- **Sources**
- **Ideator notes**: construct motivation, and archetype per track
- **Expected human vs AI** [speculation]
- **Expected model separation** [speculation]
- **Evidence**: P# and dossier sections
- **Self-scores**
- **Risks**: as the ideator stated them
- **Closest prior art**: per the ideator
- **Cited claims**: with the source the ideator gave
- **Proposed variants**: from W §3, where given
- **Spec omissions**

### C01 Kinetic (H1)
- **Sources:** H1.
- **Ideator notes:**
  - A1 benchmark with a public "try it" demo, on moat M3.
  - Motivation: any agent that works from video (driving, robots, computer use with animated interfaces). This is core human vision; BabyVision includes visual tracking (E Q1).
- **Expected human vs AI [speculation]:** for Sep 2026 frontier models, tools-off, a score below 0.3 on held-out carriers. The tools-on track (frame-differencing code) may close most of the gap.
- **Expected separation [speculation]:** large. How finely each lab turns video into tokens differs, much like BabyVision's 3.5× spread between labs (E Q2).
- **Evidence:**
  - P8, P3, P2, P4.
  - A §2.8: BlindTest shows the vision encoder holds the information and the language model loses it.
  - A §2.15: in IntPhys 2 the driver is tracking objects over time; the static VPCT closed.
  - E Q1.
- **Self-scores:** Q1 4, Q2 3, Q3 5, Q4 4, Q5 5, Q6 3. Chance of a clear human edge after 12 months of targeting: ~35%. Biggest risk: an engineering fix (denser frames plus motion pretraining).
- **Risks:**
  - The most engineering-fixable H idea; it could close within 12 months, as ClockBench did.
  - It may be dismissed as "psychophysics, not intelligence".
  - SpookyBench has been public since 2025, so plain-motion carriers may already be a target.
  - Video compression could leak the signal into single frames; the controls audit for this.
- **Prior art:** SpookyBench (static public set), MotionBlind (Sep 2026), MotionBench [web]. Stated differences:
  - secret rotating carriers with a held-out split;
  - thresholds instead of accuracy;
  - shuffle controls;
  - separate tools-off and tools-on tracks.
- **Cited claims:**
  - SpookyBench reports humans at 98% and GPT-4o, Gemini 2.0 and Qwen-VL at **0%** on video where meaning exists only over time [web: "Time Blindness", CVPR 2026, arXiv 2505.24867; 2025 models].
  - ClockBench went from 13.3% to 66.7% in about 12 months (A §2.9–2.12).
  - URLs given: arxiv.org/abs/2505.24867; github.com/TimeBlindness/time-blindness; arxiv.org/html/2609.09528 (MotionBlind); arxiv.org/abs/2501.02955 (MotionBench).
- **Spec omissions:** 200 online adults. Carriers can include "motion visible only through colour, not brightness" as a backlog example.

### C02 Live Rig (H4)
- **Sources:** H4, which the source labelled "bold".
- **Ideator notes:** A1, on moat M2. The H panel's "moonshot": the only idea whose environment cannot be simulated at all.
- **Expected human vs AI [speculation]:**
  - Large on the tools-off track, because closed-loop control from 10 fps video at LLM latency is hard.
  - It may narrow on the tools-on track, where a model can fit the tilt-to-trajectory relationship from its logs.
- **Expected separation [speculation]:** moderate, driven by vision and control.
- **Evidence:**
  - P4 (no simulator to compile), P8, P10, P17.
  - A §2.15.
  - D §2.11: in Factorio, agents gamed the reward, so goal checks must be physical and robust.
- **Self-scores:** 5/4/4/4/2/4. About 60% chance of a human edge after 12 months. Biggest risk: throughput and operations cost.
- **Risks:**
  - Physical upkeep is a new kind of maintenance burden.
  - Reproducibility across rigs.
  - Adoption (P19), although "physical AI" is a live purchasing decision.
  - A lab could build a dedicated VLA robot controller. The ideator calls this "real capability gain, which is the point".
- **Prior art:** Real Robot Challenge (remote TriFinger rigs); RoboDojo, whose real-world evaluation has expert teleoperators on the same setup as the robot policies [web, arXiv 2607.04434]. Stated differences:
  - general-purpose models rather than trained robot policies;
  - lay humans on an identical interface;
  - novel physics puzzles;
  - components rebuilt each season;
  - attempts-to-success as a learning measure.
- **Cited claims:** physics from video is still a gap: IntPhys 2 humans 96.44% vs 57.51%; on Physics-IQ the best is 58.2 against a ceiling of 100 (A §2.15).

### C03 Novel Expert (H7)
- **Sources:** H7.
- **Ideator notes:**
  - A1, on moats M3 and M5.
  - Motivation: radiology and birdsong identification work this way. The test is whether in-context learning reaches perception, not only verbal rules.
  - "Information-integration" boundaries are the test condition.
- **Expected human vs AI [speculation]:** tools-off frontier models well below the human median on held-out spaces.
- **Expected separation [speculation]:** large. Vision is the biggest reordering between labs (E Q2).
- **Evidence:** P3, P8, P9, P7; A §2.8, §2.11; E Q1, Q2.
- **Self-scores:** 4/3/4/4/4/2. About 40%. Biggest risk: many-image in-context learning may work.
- **Risks:**
  - Learning from many images in a long context may work better than expected; this is untested.
  - A single low-level statistic, such as mean colour, would leak the answer.
  - "Just train a classifier" is answered by the tools-on track.
- **Prior art:** Bongard-LOGO and Bongard-OpenWorld (few-shot, verbalisable); Greebles (Gauthier & Tarr); VisFactor. Stated differences:
  - long feedback-driven learning curves;
  - boundaries that are hard to verbalise;
  - secret rotating spaces;
  - human learning curves as the baseline.
- **Cited claims:**
  - Humans learn information-integration categories within a few hundred trials [background, category-learning literature; not in the dossiers].
  - Fine visual discrimination gaps: BabyVision 94.1 vs 49.7; VisFactor 78.8 vs 54.0.
  - ConceptARC accuracy drops sharply on visual inputs (E Q1).

### C04 Earworm (H11)
- **Sources:** H11, which the source labelled "bold: alien tuning systems".
- **Ideator notes:** A1, on moat M3.
- **Expected human vs AI [speculation]:** a gap of at least 20 pp for non-musicians on families (a)–(c).
- **Expected separation [speculation]:** large, because some models have no audio input.
- **Evidence:** P8, P3; E Q3. The ideator notes this is "the thinnest evidence of the set: no Phase 1 dossier covers audio."
- **Self-scores:** 4/3/3/4/5/3. About 40%. Biggest risks: thin evidence and uneven audio support.
- **Risks:**
  - Uneven audio support across models limits coverage and adoption.
  - Synthetic-music training.
  - Variation in human listening devices.
- **Prior art:** MMAU, MUSE, CASU, SCENEBench [web]. Stated differences:
  - tunings and timbres learned in context;
  - secret generators;
  - a real-time tapping track;
  - non-musician baselines.
- **Cited claims:**
  - MUSE (200 humans), metre identification: human experts 73.3% vs Gemini Pro 46.67% [web, arXiv 2510.19055].
  - MMAU: humans 82% vs best model 53% (2024) [web, arXiv 2410.19168].
  - People learn the statistics of the Bohlen–Pierce scale within about 30 minutes [background, Loui et al.; not verified].
  - CASU: arXiv 2606.25391. SCENEBench: EACL 2026.

### C05 Stump Arena (H3)
- **Sources:** H3. W §3 proposed twists for it.
- **Ideator notes:**
  - A1, also reporting A2. A game plus a benchmark that renews itself, on moat M1.
  - The H panel's "renewal backbone": the cost-to-stump headline has no ceiling and stays meaningful after gaps close.
- **Expected human vs AI [speculation]:**
  - By construction, stumpers are near 100% for humans and at most 33% for the panel. The informative number is the trend in cost to stump.
  - Text-only trick questions are closed (SimpleBench, A §2.4), so authors are expected to drift toward perception and video. "That drift is itself a finding."
- **Expected separation [speculation]:** wide on held-out-panel items, split by modality strength (E Q2).
- **Evidence:** P1, P7, P17, P20 (participation); A §2.4; G §4 (newly written items are error-prone).
- **Self-scores:** 5/5/4/4/3/5. About 85% by construction. Biggest risks: ambiguous items and filter-panel bias.
- **Risks:**
  - Items may be hard only for the filter panel; held-out scoring mitigates this.
  - Ambiguity and label errors.
  - Author–verifier collusion; random assignment and audits mitigate this.
  - Programme cost and moderation load.
- **Prior art:** Dynabench, ANLI, adversarial Quizbowl, HLE (experts, text, static), SimpleBench (fixed, 9 humans). Stated differences:
  - an ordinary-human gate;
  - any medium;
  - weekly renewal;
  - held-out-model scoring;
  - an uncapped, effort-based headline.
- **Cited claims:** adversarial Quizbowl authoring cut strong QA models' relative accuracy by up to 40% while leaving human difficulty unchanged [web: TACL 2019; aclanthology.org/Q19-1029].
- **Proposed variants (W §3):**
  - Score each model only on items accepted after its release date (future-dated windows).
  - "Burn accounting": record which providers saw each item during filtering.
  - Publish a gap half-life per category, so the benchmark doubles as a live §5a opportunity map.
  - Scale bounties by category scarcity.
- **Spec omissions:**
  - Authors get a bonus if an item also defeats models released later.
  - Retired practice items will be trained on; the ideator says this doesn't matter, because the headline uses fresh items only.
- **Related:** shares its gating pipeline with C39.

### C06 Alien Physics (H10 + G13)
- **Sources:** H10 Alien Physics (A1 benchmark) and G13 Strange Billiards (A1 game). See merge log §2.
- **Ideator notes:**
  - H10 is on moats M3 and M5.
  - G13's construct combines intuitive physics, system identification and adversarial planning, for embodied agents and for "learn how this system behaves, then act".
- **Expected human vs AI [speculation]:**
  - H10: no human baseline exists anywhere for learning a new physical law from video. The ideator guesses a human edge of at least 25 pp tools-off.
  - G13: A1 at launch.
- **Expected separation [speculation]:** H10 moderate. G13 large and ordered by vision skill (E Q2).
- **Evidence:**
  - H10: P3, P4, P8; A §2.10, §2.15; F §2 (NewtonBench's altered laws are numeric and already an RL training environment).
  - G13: P2, P8, P9, P10, P17; A §2.10, §2.15; E Q3 rank 4.
- **Self-scores:**
  - H10: 4/3/3/3/5/3. About 35%. Biggest risk: a weak human anchor, plus trajectory fitting with tools.
  - G13: 4/3/4/4/4/4, mean 3.8. Passes the rule.
- **Risks:**
  - On the tools-on track, a model can extract trajectories and fit the law.
  - Humans may handle strange laws worse than assumed, so a pilot is needed.
  - Overlap with Physics-IQ and PHYRE.
  - Synthetic physics-video training may close the gap quickly (ClockBench went from 13.3 to 66.7 in about 12 months).
  - Continuous-action precision could confound the result; quantise, and use the coordinates ablation as a control.
  - "Only a game" framing (P19).
- **Prior art:** PHYRE, IntPhys 2, NewtonBench, Physion; AIBIRDS (known physics, non-LLM agents); VPCT. Stated differences:
  - secret altered laws learned from video only;
  - one-shot action;
  - a human baseline;
  - hidden per-match physics learned online against an adversarial anchored ladder;
  - exact prediction probes.
- **Cited claims:**
  - Static normal-physics prediction is nearly closed: VPCT 91% vs 100% (A §2.10).
  - Physics in video is not: IntPhys 2 96.44 vs 57.51 (A §2.15).
  - The AIBIRDS man-vs-machine challenge has been won by humans every year since 2013. In 2022 the best human scored 251,710 vs 144,630 for the best AI [web, S; aibirds.org].
- **Spec omissions:**
  - G13 details:
    - 6–10 balls, pockets and obstacles;
    - the anchor bot uses "the true physics and a search at fixed execution-noise levels";
    - no trajectory preview for anyone;
    - 45 minutes, paid per win;
    - about 200 matches.
  - Primitive examples: G13 lists invisible anisotropic friction zones, velocity-dependent restitution, delayed bumpers and wrap-around edges. H10 lists "gravity pulls towards the nearest blue object" and "collisions swap masses".
  - G13's illustrative example claimed the model's prediction error drops from 31 cm to 9 cm by shot 10. This was removed from the spec as an outcome.

### C07 Tacit Signals (H2)
- **Sources:** H2. W §3 proposed a twist for it.
- **Ideator notes:**
  - A1 (also A2), on moat M1. Text benchmarks cannot measure it, because the partner is a person, not a dataset.
  - This targets the failure mode found in Concept (A §2.5).
  - The H panel's **lead candidate**.
- **Expected human vs AI [speculation]:** on novel channels, human–human pairs at about 80–90% and human–AI pairs at 40–65%.
- **Expected separation [speculation]:** moderate. Differences in over-adaptation or deference (sycophancy) and in pragmatic style may appear as a conduct axis (P11).
- **Evidence:**
  - A §2.5 (Concept).
  - D §2.16: in Hanabi, first-order theory of mind correlates with success at ρ = 0.76.
  - E Q1: theory-of-mind vignettes are largely closed [uncertain], so the remaining gap must come from live interaction.
  - P1, P7, P17, P20.
- **Self-scores:** 4/4/4/5/3/4. About 60%. Biggest risks: labs paying humans for online RL, and human variance.
- **Risks:**
  - Humans may guess they are playing an AI; measure suspicion and control for it.
  - Human partners vary widely, so large samples are needed (P16).
  - The main durability threat is labs paying humans for online RL. That is costly, and secret channel families limit transfer.
  - An AI that teaches the human an explicit code is succeeding legitimately.
- **Prior art:** Tacit Communication Game (de Ruiter et al., 2010); ICCA; arXiv 2602.08208; TUX, human–AI tacit understanding (arXiv 2605.30930); AH2AC2, Hanabi with human-proxy agents [web]. Stated differences:
  - live humans as the scored environment, rather than proxies;
  - non-linguistic channels that rotate each season;
  - a human–human reference condition, giving a clean A1 comparison.
- **Cited claims:**
  - "LLMs and people both learn to form conventions — just not with each other" (arXiv 2602.08208): human–human and AI–AI pairs formed conventions, while mixed pairs "consistently failed", even when models were prompted to behave like humans [web; model list not seen].
  - Concept: humans above 90% vs LLMs below 40% (A §2.5; 2025 models, stale).
  - **Note:** the G panel (G2, now C44) cites the same paper as evidence *against* a human edge in convention formation ("LLMs and people both learn to form conventions"). The two panels read the source differently.
- **Proposed variants (W §3, for G3/H2/D7):**
  - A **third-party decodability** score: a fresh model from a different lab, or a human, reads 30 rounds of transcript, then plays as matcher for 10 rounds. This measures whether agent-invented conventions are readable by monitors, which is safety-relevant.
  - Cap bandwidth below what a naive attribute encoding needs.
  - Randomise glyph inventory order per player, so no positional code works.

### C08 Glyph Pact (G3)
- **Sources:** G3. W §3 proposed a twist for it.
- **Ideator notes:** A1, a repeated reference game. It matters for collaboration on novel artefacts such as designs, data plots and lab samples.
- **Expected human vs AI [speculation]:**
  - Human dyads reach about 96% with shrinking messages.
  - Human–model dyads lag on efficiency and on near-duplicate discrimination, a perception bottleneck (P8; BabyVision 94.1 vs 49.7, E Q1).
- **Expected separation [speculation]:** large on vision-heavy families. BabyVision spread 3.5× across labs (Jan 2026 models, E Q2).
- **Evidence:** P8, P17, P20; A §4 lesson 4; E Q1–Q2.
- **Self-scores:** 3/2/4/4/4/3, mean 3.3. Fails the rule on Q1.
- **Risks:**
  - Targeted post-training for convention formation already exists [web, S: arXiv 2508.06482], so the gap may close within months (ClockBench-like, A §2.9).
  - Live human pairing is the cost driver.
  - Self-play dyads may invent codes; only human-paired scores are headline.
- **Prior art:** Clark & Wilkes-Gibbs tangrams; Hawkins et al.; KTH Tangrams; arXiv 2606.08081. Stated differences:
  - secret generated stimuli;
  - a partner-swap probe;
  - human–model dyads under a frozen protocol, as a maintained leaderboard.
- **Cited claims:** in repeated reference games, human dyads rise from 78% to 96%, while multimodal LLM agents are "aligned but not partner-specific" [web, S: arXiv 2606.08081].
- **Proposed variants (W §3):** third-party decodability, a bandwidth cap, and randomised inventory order per player (see C07).
- **Spec omissions:**
  - Positions differ between the two players, as in the classic design, so "top-left" is useless.
  - The source's example line "Round 7, new partner: the model should re-expand; failing to do so is the documented agent failure" was removed as a claim.

### C09 First-Run Arcade (H5)
- **Sources:** H5.
- **Ideator notes:** A1, on moats M4 and M5. "ARC-AGI-3's ability plus two things the fixes that cracked ARC-AGI-3 barely help with: real time and continuous perception."
- **Expected human vs AI [speculation]:**
  - Instructed real-time play is closing; real-time play without instructions, where the goal must be discovered, is unmeasured.
  - A score of 0.3 or less for frontier LLM agents in the frozen harness.
  - Much higher scores for purpose-built fast agents in the BYO track.
- **Expected separation [speculation]:** large. Latency may let small fast models beat slow large ones, an A2-style inversion.
- **Evidence:**
  - P10, P18, P8, P1, P7.
  - A §2.3: what closed ARC-AGI-3 was carried-over state and symbolic world models.
  - A §2.17; D §2.8; F §1.
- **Self-scores:** 4/3/4/4/3/5. About 45% with the frozen harness. Biggest risks: fast-policy harnesses, and the "artificial" critique.
- **Risks:**
  - The "artificial latency handicap" critique (P10); the paused ablation measures how much of the gap is latency.
  - A lab builds a fast policy tier, as SIMA 2 did, which is real capability gain.
  - Cost.
  - Harness capture on the BYO track; the difference is published.
- **Prior art:** VideoGameBench (known retro games, dormant); ARC-AGI-3 (turn-based); SIMA 2 (instructed); gg-bench (turn-based). Stated differences: secret generated real-time games with no instructions, and a paused ablation.
- **Cited claims:**
  - VideoGameBench: 0.48% in real time vs 1.6% paused (A §2.17; May 2025, stale).
  - SIMA 2 reached about 65% vs 71% for humans on *instructed* tasks in 3D games [web; arXiv 2512.04797].
- **Related:** the H panel suggested an H5 + H13 "arcade with a dual-task mode".

### C10 Two Clocks (H13)
- **Sources:** H13, which the source labelled "bold".
- **Ideator notes:** A1, on moat M4. People do this all the time, for example talking while driving. Models that produce one token at a time struggle with it structurally.
- **Expected human vs AI [speculation]:**
  - Humans typically lose 10–30% on each task; the ideator gave no source for this figure.
  - A single frontier model in the frozen harness will largely collapse on one of the two tasks: it either stops steering while it thinks, or abandons the puzzles.
- **Expected separation [speculation]:** large. It exposes the trade-off between latency and reasoning effort.
- **Evidence:** P10, P18, P13; A §2.17.
- **Self-scores:** 4/3/4/4/3/3. About 50% with the frozen harness; low with BYOH. Biggest risk: "architecture, not intelligence".
- **Risks:**
  - It measures system architecture as much as intelligence. A two-model harness would close it, and "that difference is the informative result".
  - It may look artificial (P10).
- **Prior art:** human-factors dual-task batteries such as NASA's MATB-II. The ideator found no AI benchmark.
- **Cited claims:** latency already hurts in real time: VideoGameBench 0.48% real time vs 1.6% paused (A §2.17).

### C11 Wayfinder (H9)
- **Sources:** H9.
- **Ideator notes:** A1, on moats M3 and M5. "The MindCube and MMSI-Video failure made interactive."
- **Expected human vs AI [speculation]:** path efficiency of about 0.8 for the human median and 0.3–0.5 for frontier models.
- **Expected separation [speculation]:** moderate to large.
- **Evidence:** P8, P3, P10; A §2.12–2.14, §2.20; E Q1.
- **Self-scores:** 4/2/4/4/4/3. About 25%. Biggest risk: embodied-navigation training.
- **Risks:**
  - Embodied navigation is a lab priority (SIMA 2, robotics), so this is probably the fastest-closing of the H perception ideas.
  - The SLAM route will close the tools-on track quickly.
- **Prior art:** VSI-Bench, MindCube, Habitat ObjectNav, SIMA 2. Stated differences:
  - interactive exploration followed by map-use tests taken from human spatial-cognition research;
  - secret grammars;
  - human normalisation.
- **Cited claims:**
  - MMSI-Video: humans 96.4 vs 38.0 (Dec 2025 models).
  - MindTopo: 97.87 vs 61.42 (Sep 2026) [secondary, low confidence].
  - MindCube: vision-language models near random.
  - VSI-Bench is closed on distances and sizes but not on relational questions (A §2.12–2.14, §2.20).

### C12 Cartographer & Scout (G6)
- **Sources:** G6.
- **Ideator notes:** A1, an asymmetric cooperative game. It matters for embodied and computer-use agents directing or following people.
- **Expected human vs AI [speculation]:** a large A1 gap at launch.
- **Expected separation [speculation]:** large, and ordered by lab vision quality.
- **Evidence:** P8, P10, P17, P20; A §2.12–2.14, §4 lessons 4–5; E Q1.
- **Self-scores:** 3/3/4/4/3/3, mean 3.3. Fails the rule.
- **Risks:**
  - Synthetic 3D training could close the gap within about 12 months (the ClockBench pace, A §2.9).
  - Rendering artefacts.
  - It is harder to attribute failures to perception vs language; the symbolic ablation mitigates this.
  - Live dyad logistics.
- **Prior art:** HCRC Map Task, Talk the Walk, CerealBar, TEACh, vision-language navigation. Stated differences:
  - generated unnamed landmarks;
  - human–model mixed dyads;
  - a localisation probe;
  - a maintained frozen protocol.
- **Cited claims:**
  - MMSI-Video: humans 96.4 vs best model 38.0 (A §2.14).
  - MindCube: about 95 [uncertain] vs 61–76 (A §2.13).
  - Counterpoint: VSI-Bench nearly closed after targeted spatial training (A §2.12).
  - BabyVision: Gemini 3 Pro 49.7, GPT-5.2 34.4, Claude 4.5 Opus 14.2 (Jan 2026 models, E Q2).
- **Spec omissions:** the human baseline is turn-based, with no reaction-time edge.

### C13 Deep Seasons (G7)
- **Sources:** G7.
- **Ideator notes:** A1, a roguelike campaign. Learning across episodes ranks second among under-measured abilities in E Q3 (CL-bench best 23.7%). This is what "on-the-job learning" means for agents.
- **Expected human vs AI [speculation]:** humans show steeper learning slopes at launch.
- **Expected separation [speculation]:** large, driven by the quality of the notebook abstractions. BALROG's spread runs from 68.3 down to 3.7 (D §2.6).
- **Evidence:** P9, P10, P11, P18; A §2.16; D §2.6–2.7; E Q3 rank 2; F §1.
- **Self-scores:** 4/4/4/4/3/4, mean 3.8. Fails on Q5 and cost. The G panel still recommends carrying it forward.
- **Risks:**
  - The notebook protocol decides the score, as the ARC-AGI-3 adapter did; it is frozen, and BYOH is reported.
  - Macro-actions may trivialise the game.
  - Human memory breaks strict parity.
  - Cost and variance on long runs.
- **Prior art:** BALROG/NetHack (known game, tiny n), NetHackers (bot-writing), Craftax, ARC-AGI-3 levels, Continual Learning Bench. Stated differences:
  - secret per-campaign mechanics;
  - a scored learning slope under a fixed memory budget;
  - mechanic-fidelity probes.
- **Cited claims:**
  - BALROG NetHack under protocol: 13.24% (A §2.16).
  - CL-bench's best is 23.7% (Feb 2026 models; not re-run on Jul–Sep 2026 models [uncertain]).
  - Continual Learning Bench shows no reuse of knowledge across episodes (E summary 6).
  - Counterpoint: state-preserving harnesses flipped ARC-AGI-3 (F §1).
  - NetHack's ascension used the wiki and source code (D §2.6).
- **Spec omissions:** the illustrative continuation "Run 6 … reaches depth 7, against depth 3 in run 1" was removed as an outcome.

### C14 Kelly Exam (D1)
- **Sources:** D1.
- **Ideator notes:**
  - A2. Hallucination is the top deployment failure, and a model's knowledge of its own frontier appears on no leaderboard (E Q4).
  - D's spread driver: "calibration × knowledge; a do-nothing agent scores exactly 0".
  - Training on the practice families teaches calibration in general, which is the intended construct, but not the private trap structure.
- **Expected human vs AI [speculation]:**
  - AI clearly ahead, mainly on accuracy for knowledge and computation items.
  - Typical humans near zero or negative growth from overconfidence.
  - The margin may be narrower on the trap subset, because models can be badly miscalibrated too.
- **Expected separation [speculation]:**
  - Wide.
  - Likely inversions: small, well-calibrated tiers beating overconfident flagships, and lab-level reordering.
  - More reasoning effort may lower scores.
  - "Informative because it shows which model you can trust unsupervised."
- **Evidence:** P11, P2, P13, P15, P14; B §3.7, §5 lesson 4; E Q2, Q3 rank 1, Q4.
- **Self-scores:** 3/4/4/4/5/3. Fails on Q1.
- **Risks:**
  - Knowledge items load on the general factor.
  - Rankings depend on q, so results under alternative q are published.
  - Verbalised probabilities are sensitive to prompt format.
  - Label errors in generated items.
  - Calibration can be trained, which is desirable but may saturate the trap families quickly.
- **Prior art:** AA-Omniscience (+1/−1/0, static items); lechmazur confabulations; KellyBench (arXiv 2604.27865, Apr 2026: sports-betting strategies scored by log-wealth) [prior-art search]. Stated differences:
  - per-item wagering against a house line anchored to frozen models;
  - a compounding bankroll;
  - secret trap families;
  - a floor of exactly 0.
- **Cited claims:**
  - Hallucination policy splits models by lab: 48–88% on AA-Omniscience (Nov 2025 models; E Q2).
  - Under the +1/−1/0 AA-Omniscience scheme, an always-abstain model ranks 4th of 36 (B §3.7).
  - Haiku 4.5 had a 26% hallucination rate vs Opus 4.5's 58% (Nov 2025; B §4).
  - Reasoning fine-tuning cuts abstention by about 24% (E Q1).
  - HLE's calibration channel: GPT-4o calibration error 92.3 (B §3.4).
- **Related:** the D panel proposes bundling with C26 as a "self-knowledge economy". C15 is the prospective counterpart.
- **Spec omissions:**
  - Humans: 90 minutes, 100 items each, each item seen by at least 10 people.
  - A tools track runs separately.
  - Noise control: 2,000 items × 3 samples, differences paired by item, and a bootstrap over item families.

### C15 Prospective Self-Forecast (W3)
- **Sources:** W3.
- **Ideator notes:**
  - A2. Idiosyncratic, prospective self-knowledge, for routing, delegation and deciding when to ask for help.
  - The structural property: the ground truth is the model's own future behaviour, and population odds absorb generic difficulty.
  - Training on the practice pool teaches self-knowledge about that pool only.
  - Sandbagging is blocked because attempts are blind and task accuracy is reported alongside.
  - Self-Edge equals the expected log-wealth growth of a Kelly bettor against the house.
- **Expected human vs AI [spec]:** humans are also overconfident, but may beat models on idiosyncratic resolution, since people know their own weak spots. Mixed overall; mostly A2.
- **Expected separation [spec]:** strong, by lab (abstention policy; E Q2). It must be tested against ECI and release date (P14).
- **Evidence:** P11, P13, P14; B §3.7; E Q1–Q3.
- **Self-scores:** 5/4/4/3/5/3, mean 4.0. Passes.
- **W recommendation:** carry forward; also usable as a metacognition sub-score on any candidate.
- **Risks:**
  - The house odds depend on the panel, so the panel is frozen per season.
  - Easy items may get "solved" inside the 300-token forecast.
  - If all models share the same blind spots, Self-Edge will be about 0 for everyone: a finding, but a weak separator.
  - Twin fidelity.
- **Prior art:** D1 (retrospective); D2; MIRROR, Metacognitive Monitoring Battery, TRIAGE (2026) [web]; AA-Omniscience. Stated differences:
  - the forecast is made before any attempt, on a twin;
  - attempts are blind;
  - agentic tasks are included;
  - triage is scored.
- **Cited claims:**
  - Hallucination rates of 48–88% split by lab; an always-abstain model ranks 4th of 36 (E Q2, B §3.7).
  - [web] 2026 papers report universal overconfidence (MIRROR gap 0.17), failure of compositional self-prediction (CCE 0.50–0.94), and confidence that "reduces to a shared difficulty heuristic" [attribution to arXiv 2605.07806 uncertain].
  - Links given: MIRROR arXiv 2604.19809; TRIAGE arXiv 2605.13414.

### C16 Pushback Ledger (D12)
- **Sources:** D12.
- **Ideator notes:** A2, on sycophancy in deployment and trust. The design is symmetric, so never budging and always caving both score poorly.
- **Expected human vs AI [speculation]:** AI ahead on final accuracy, since its first answers are better. Humans also cave to authority (background, not in the dossiers).
- **Expected separation [speculation]:** plausibly lab-dependent.
- **Evidence:** P11, P15, P14; B §3.5, §5 lesson 4; E Q2. No cross-lab sycophancy data was found, which leaves room for this benchmark.
- **Self-scores:** 3/3/4/4/5/3. Fails on Q1.
- **Risks:**
  - Frozen challengers become recognisable.
  - Items must be hard enough to produce first-answer errors.
  - The construct may converge across labs once targeted.
- **Prior art:** FlipFlop (arXiv 2311.08596), SYCON Bench, lechmazur sycophancy, "Sycophancy as material failure under pushback" (arXiv 2606.16617) [prior-art search]. Stated differences: valid and fallacious challenges in equal measure, and a discrimination metric that punishes stubbornness as much as caving.
- **Cited claims:**
  - lechmazur's sycophancy board shows "Insufficient" rates of 4.7–83.9% (B §3.5).
  - A 2026 report that Claude's sycophancy roughly doubles under pushback (18% vs 9%) [prior-art search, uncertain].

### C17 Reliability Horizon (D13)
- **Sources:** D13.
- **Ideator notes:**
  - A2. Deployment needs p80/p95 reliability.
  - The code track is expected to be near-trivial.
  - Output-token caps follow the "Illusion of Thinking" rebuttals (E Q4).
- **Expected human vs AI [speculation]:** AI's L95 far above humans', who slip.
- **Expected separation [speculation]:** wide on L95, even where L50 is similar. Expected inversion: cheap models with larger reasoning budgets beating flagships.
- **Evidence:** P2, P9, P16; E Q1, Q3 rank 5, Q4.
- **Self-scores:** 3/4/4/4/5/2. Fails on Q1; the D panel flags low interest.
- **Risks:**
  - Loads heavily on the general factor.
  - Token caps can masquerade as failures.
  - RL on "execute procedures" inflates scores generically.
  - Low interest.
- **Prior art:** METR time horizons, BABILong, Tower-of-Hanoi scaling studies, EsoLang-Bench. Stated differences: new primitives for every item, a p95 staircase, and low cost.
- **Cited claims:**
  - The 80% horizon is 4–10× shorter than the 50% horizon (E Q1, reproduced).
  - On NYT Connections, reasoning budget drove Flash to beat Pro (B §3.5).

### C18 Compaction Chronicle (D4)
- **Sources:** D4.
- **Ideator notes:** A2. It isolates the mechanism thought to drive long-horizon inversions.
- **Expected human vs AI [speculation]:** AI clearly ahead on exact recall and throughput. Humans may compress well but make slips.
- **Expected separation [speculation]:**
  - Wide and lab-dependent, because compaction styles differ.
  - Inversions: lower effort beating higher effort, and cheap models with disciplined notes beating flagships.
- **Evidence:** P12, P18, P2; B §3.2; D §4; E Q1, Q3 rank 5.
- **Self-scores:** 3/4/4/3/5/3. Fails on Q1.
- **Risks:**
  - Crowded prior art: BEAM, MemoryAgentBench, and 2026 compaction papers ("The Compaction Cliff…", arXiv 2608.22752) [prior-art search].
  - A byte cap is not how deployed memory works (hence BYOH).
  - Loads on the general factor.
- **Prior art:** most memory benchmarks test retrieval systems or raw long context. Stated differences:
  - a byte-capped notes file the model writes itself, under a frozen protocol;
  - generated worlds with retractions;
  - deterministic answers.
- **Cited claims:**
  - Opus 4.8 did better at High than Max effort on Vending-Bench, hypothesised to be due to context compaction (B §3.2).
  - ARC-AGI-3's 62.7% vs 98.6% gap came from state handling (P18).
  - In FLE, 97.7% of Claude Opus 4.1's errors were "pragmatic", i.e. wrong beliefs about the game state (D §4).
  - The 80% horizon is 4–10× shorter than the 50% horizon (E Q1).

### C19 Frozen-Student Tutor (D3)
- **Sources:** D3, which the source labelled "bold".
- **Ideator notes:**
  - A2. Teaching as distillation.
  - It fixes StudentBench's failure: human learning outcomes were too noisy to separate models, while expert judges and outcomes disagreed (B §2).
  - The D panel calls it "StudentBench fixed".
- **Expected human vs AI [speculation]:** AI teachers clearly ahead. They induce the system faster and write denser, better-targeted lessons for model readers.
- **Expected separation [speculation]:**
  - Wide. The score mixes induction, which loads on the general factor, with selection and compression, which likely load on it less.
  - Inversion: concise mid-tier models beating verbose flagships at the 500-token budget.
  - Expert-vs-outcome divergences like StudentBench's become measurable.
  - CIs about ±1–2 pp.
- **Evidence:** P3, P7, P14, P15, P16; B §2; F §1 (CL-bench: learning from context is weak).
- **Self-scores:** 4/4/4/4/5/4. Passes.
- **Risks:**
  - Teaching machines may not transfer to teaching humans (hence the validity arm).
  - Lessons that exploit specific students.
  - A ceiling if the students are too strong.
  - Lab clustering, handled by excluding same-family pairs.
- **Prior art:** "Can Language Models Teach Weaker Agents?" (arXiv 2306.09299) [prior-art search]; TutorBench, MathTutorBench, EducationQ (judge-based); StudentBench. Stated differences:
  - secret new systems;
  - a frozen multi-lab student panel with one secret student;
  - a strict budget;
  - outcome-only scoring;
  - a human-learner validity arm.
- **Cited claims:**
  - StudentBench: omnibus p = 0.755; 0 of 364 cells significant (B §2).
  - Opus 5 ranked top with experts but in the bottom third on learning (B §2).
- **Spec omissions:**
  - The illustrative example numbers (no lesson 11%; budget-matched excerpt 34%; model lesson 58%; headline +24 pp) were removed as outcomes.
  - Humans have 2 hours with the same oracle and budget.
  - The validity arm uses the top, median and bottom AI lessons plus the human lessons.

### C20 Misconception Clinic (W1)
- **Sources:** W1.
- **Ideator notes:**
  - A2, with human tutors as the anchor. Diagnostic teaching, for orchestrating weaker sub-agents, onboarding and tutoring.
  - The structural property: the score is a frozen learner's measured repair, and the planted misconception is secret and must be found by probing.
  - Public training doesn't transfer trivially: the teacher never sees the misconception, and learner-specific exploits don't carry across rotated bases.
- **Expected human vs AI [spec]:** models beat humans on Repair, since they write better prompts for LLM learners. Humans may be competitive on turns-to-diagnosis. A2 overall.
- **Expected separation [spec]:** strong. W1 replaces StudentBench's rater with a low-noise outcome. Weak teachers should show high Harm from over-explaining.
- **Evidence:** P14, P15, P16, P7, P3; B §2; E Q3; G §3.
- **Self-scores:** 4/4/4/3/5/3, mean 3.8. Passes.
- **Risks:**
  - "Magic-phrase" exploits of particular learner bases; mitigated by rotating bases and reporting per base.
  - Misconception strength needs tuning; the release gates cover this.
  - The construct may collapse into prompt engineering for small models [I].
  - Transfer to human learners is untested; run a small P14 check with human learners given a flawed worksheet.
- **Prior art:** D3 (now C19); Teach2Eval (2025; weak student models on standard QA) [web, arXiv 2505.12259]; EduClaw-Bench (simulated knowledge-tracing learner) [web, arXiv 2608.03206]; StudentBench. Stated differences:
  - a secret planted misconception found by interactive probing;
  - a behavioural-diagnosis score;
  - a do-no-harm term;
  - a fine-tuning-data track.
- **Cited claims:**
  - StudentBench human outcomes: omnibus p = 0.755, 0 of 364 cells significant, per-learner SD 14–17 pp, needing 120–180 learners per arm (B §2).
  - Expert-rated teaching already separates models: Opus 5 +1.10 vs Gemini 3.1 Pro −0.92 (B §2).
- **Spec omissions:**
  - At most 8k teacher tokens.
  - The learner runs at T = 0 with 3 paraphrased note wrappers; 100 episodes per run; about 2–5M teacher tokens.
  - Humans get a bonus per repair point, and each of 50 baseline episodes is taught by at least 2 people.
  - Diagnosis accuracy is reported separately.

### C21 Simulated Futures Exchange (D10)
- **Sources:** D10.
- **Ideator notes:** A2. Forecasting that resolves instantly and at scale, which real-world forecasting can't.
- **Expected human vs AI [speculation]:** AI clearly ahead of typical humans; unsure against skilled analysts.
- **Expected separation [speculation]:** wide, because choosing experiments separates agents. Expected inversion: simpler, robust models beating over-fitted complex ones.
- **Evidence:** P2, P9, P11, P15; F §1–2 (ZendoWorld, AutumnBench, NewtonBench); E Q3 rank 3.
- **Self-scores:** 3/4/4/3/4/3. Fails on Q1 (public-family decay).
- **Risks:**
  - A public family would fall fast.
  - Tools and harness dominate.
  - Overlaps with data-science benchmarks.
- **Prior art:** NewtonBench, ForecastBench, KellyBench, ZendoWorld, AutumnBench. Stated differences:
  - proper scoring against exact rollout distributions;
  - interventional questions;
  - an AutoML anchor.
- **Cited claims:**
  - ZendoWorld agents ran "near-uninformative" experiments (F §2 [S]).
  - NewtonBench became an RL environment in about 4.5 months (F §2).

### C22 Long-Tail Futures (W5)
- **Sources:** W5.
- **Ideator notes:**
  - A2. The twist: long-tail series with no public forecast to copy.
  - The structural property: the truth doesn't exist at test time (P5), and resolution is automatic and high-volume.
- **Expected human vs AI [spec]:** models ≫ laypeople, and at least equal to professionals on pure series. The context-conditioned items decide the headline.
- **Expected separation [spec]:** calibration spreads by lab (E Q2).
- **Evidence:** P2, P5, P13, P14, P16; E Q2; G §1, §3.
- **Self-scores:** 5/4/4/3/4/3, mean 3.8. Passes.
- **Risks:**
  - Resolution APIs change.
  - The anchors may be too strong, leaving skill near 0 for everyone.
  - The code track may be trivial.
  - Leaderboard lag and an ongoing operations burden.
  - Some may not see it as "reasoning".
- **Prior art:** ForecastBench, Prophet Arena, Prediction Arena, LLM-SoccerArena [web]; M4/M5 [bg]; D10 (simulated systems). Stated differences:
  - un-newsworthy real-world quantities;
  - scheduled-event context;
  - full distributions scored against frozen statistical anchors;
  - very high volume.
- **Cited claims:**
  - Existing forecasting benchmarks score newsworthy events, where market prices and pundit forecasts can be looked up.
  - By Jul 2026, reportedly 17 ForecastBench submissions ranked above superforecasters [web, unverified].
  - An in-repo lead claims calibration error is nearly uncorrelated with general capability [uncertain; E Q2 Gaps].
  - The pinned time-series foundation-model anchor is [bg].
  - Links given: ForecastBench arXiv 2409.19839 and forecastingresearch.substack; Prophet Arena; Prediction Arena arXiv 2604.07355; LLM-SoccerArena arXiv 2607.24573.

### C23 Hunch Lab (W6)
- **Sources:** W6, which the source labelled "bold".
- **Ideator notes:**
  - A2; expert humans may be competitive.
  - Research intuition is the judgement that decides which experiments are worth their compute, and it is central to the 2026 "automated researcher" claims.
  - The structural property: the truth does not exist until the owner creates it, and volume is limited only by owner compute.
- **Expected human vs AI [spec]:** at least parity, and likely A2.
- **Expected separation [spec]:** strong. It should also correlate with doing-research benchmarks (RE-Bench, MLE-bench style), which is a P14 outcome test.
- **Evidence:** P2, P5, P13, P14; E Q2; G §1; F §4.
- **Self-scores:** 4/4/4/4/4/4, mean 4.0. Passes.
- **W recommendation:** carry forward. It has the strongest structural contamination defence and ties to AI R&D.
- **Risks:**
  - High-variance experiments have ambiguous truth; scored against the distribution.
  - Labs could train surrogate predictors by running millions of small experiments; mitigated by rotating and held-out domains and per-domain reporting.
  - Owner compute.
  - An ML-heavy mix is narrow; add other computational sciences.
  - Results must stay unpublished until each season is scored.
- **Prior art:** "Predicting Empirical AI Research Outcomes with LMs" (2025; pairwise idea comparison against *past* results) [web, arXiv 2506.00794]; BrainBench [web]; replication markets [bg]. Stated differences:
  - truth manufactured after the lock;
  - unlimited volume;
  - continuous quantities;
  - multiple computational domains.
- **Cited claims:**
  - BrainBench: LLMs beat neuroscientists at predicting results [web; Nature Hum. Behav., s41562-024-02046-9].
  - LLM forecasts of unpublished social-science experiments were near pooled human accuracy [web; Nature s41586-026-10742-x].

### C24 MDL Arena (W7)
- **Sources:** W7, which the source labelled "bold".
- **Ideator notes:**
  - A2. "Science as Occam's razor", with an objective score and a known optimum (the owner's generator).
  - Brute-force audit: program search over the DSL is blocked because the subject doesn't know the DSL.
  - A subject that writes a generic compressor gets the floor, not the headline.
- **Expected human vs AI [spec]:** AI above the human mean. Top humans may win on "insight" datasets.
- **Expected separation [spec]:** strong, but likely g-loaded; the contribution beyond the general factor must be shown (P14).
- **Evidence:** P2, P3, P4; F §2 (NewtonBench, rule induction); E Q3 #9.
- **Self-scores:** 4/5/4/2/5/3, mean 3.8. W marks it as passing (Q4 is not part of the decision rule).
- **Risks:**
  - The DSL style becomes guessable over seasons; rotate it.
  - Flexible generic models score passably; the bits metric already penalises this.
  - The human baseline is weak (M9 only partly met).
  - Appeal may be narrow outside ML.
- **Prior art:** Hutter Prize and Large Text Compression Benchmark [bg]; rule and law discovery benchmarks (F §2). No LLM MDL benchmark was found [web]. Stated differences:
  - novel secret generators with a known optimum;
  - program-plus-data MDL;
  - structure measured beyond generic compression.
- **Spec omissions:** the illustrative example scores (a frequency-table model at L ≈ 1.8× the reference; a rule-discovering model at ≈ 1.05×) were removed.

### C25 Mechanism Lab (W10)
- **Sources:** W10.
- **Ideator notes:**
  - A2. Institutional design under strategic behaviour, for agents that set prices, policies and marketplaces, and for safety.
  - The structural property: textbook-optimal mechanisms are deliberately mis-specified, so memorised theory is a trap.
- **Expected human vs AI [spec]:** frontier models at least match graduate students. A2.
- **Expected separation [spec]:** moderate to strong. Long-horizon economic simulations separate models and invert ranks (Vending-Bench 2; B §3.2).
- **Evidence:** P11, P12, P14, P15; B §3.2, §5; D §2.19.
- **Self-scores:** 4/4/3/3/4/3, mean 3.5. Fails on Q3.
- **Risks:**
  - Validity rests on simulated agents; check rank order with human-subject sessions on a subset (P14).
  - The oracle may be intractable for a rich DSL.
  - Pool effects are small, since scores are oracle-normalised.
- **Prior art:** automated mechanism design [bg]; LLM bidders preserving mechanism orderings (2025) [web, arXiv 2507.09083]; G9 and D2, where the subject plays *inside* the rules. Stated difference: the subject *designs* the institution for a secret, partly adversarial population, scored against an oracle.
- **Cited claims:**
  - In Vending-Bench Arena, Opus 5 proposed or joined a cartel in all 6 runs (D §2.19).
  - Andon Labs concedes its sales equations are gameable (B §3.2).

### C26 Contractor's Auction (D2)
- **Sources:** D2, which the source labelled "bold".
- **Ideator notes:**
  - A2. Agent marketplaces, model routing and delegation. Profit rewards knowing your limits, not only capability.
  - D's spread driver: self-knowledge of one's own frontier, plus cost.
  - The D panel rates it strongest, for delivering "cheap beats expensive" *informatively*: a cheap model wins only if it knows its limits.
- **Expected human vs AI [speculation]:** humans lose money at AI price levels and win few jobs they can finish within the deadline. The "human broker" arm is the interesting comparison.
- **Expected separation [speculation]:**
  - Expected inversion: a calibrated cheap tier (a Flash- or Haiku-class model that bids only on what it can do) out-earning an overconfident flagship.
  - The flat-rate vs list-price split shows whether a win comes from price or judgment.
- **Evidence:** P2, P11, P12, P13, P16; B §4 (price inversions); B §5 lessons 1, 4 and 6; E Q4.
- **Self-scores:** 4/4/4/3/4/5. Passes.
- **Risks:**
  - Knowledge of auction theory confounds the construct, though second-price bidding makes truthful bids near-optimal, which limits this.
  - The model may learn the anchors' patterns within a session; randomise them.
  - Holes in the verifier.
  - A weak human baseline for the whole market (Q4 = 3).
- **Prior art:** MarketBench (arXiv 2604.23897, Apr 2026: bids derived mechanically from elicited success probabilities on 93 SWE-bench Lite tasks) [prior-art search]; Vending-Bench. Stated differences:
  - live competitive bidding against frozen anchors;
  - penalties for non-delivery;
  - secret heterogeneous families, including impossible jobs;
  - the flat-rate vs list-price split.
- **Cited claims:** MarketBench [prior-art search, uncertain]: six models' SWE-bench Lite pass rates clustered at 75.3–80.6%, but their mean stated success probabilities ranged from 61.4% to 92.9%.
- **Spec omissions:**
  - Anchor bidders are frozen models whose bids are precomputed per version, plus scripted bidders.
  - The human time charge of $75/h follows StudentBench's human reference (B §2).
  - Professionals work 3-hour sessions on a 30-job subset. Broker-arm participants see the model's practice track record.
  - Example: job D is unsatisfiable, and declining it avoids −90.

### C27 Signal Pit (D7)
- **Sources:** D7.
- **Ideator notes:** A2. Trading, negotiation, and knowing when the other side knows more. Games measure opponent modelling that exams miss (D §4). The D panel rates it anchored, uncapped and deterministic.
- **Expected human vs AI [speculation]:** typical humans lose to adverse selection; AI ahead.
- **Expected separation [speculation]:**
  - Wide: numeric posterior reasoning combined with reading the order flow.
  - Inversions where overthinking flagships trade too little, or where labs' risk posture differs.
  - 400 markets give tight paired CIs.
- **Evidence:** P12, P16, P4, P11; D §2.18–2.19, §4; B §5 lessons 2 and 10.
- **Self-scores:** 4/4/4/4/4/4. Passes.
- **Risks:**
  - Exact posteriors with code; this is declared allowed, and a no-tools track runs.
  - Learning the bots' patterns within a session; randomise them.
  - Mixed pits invite collusion (S7).
- **Prior art:** LLM double-auction collusion (arXiv 2507.01413); information aggregation with AI agents (arXiv 2604.20050); the Bazaar sealed-bid benchmark (arXiv 2608.00102); StockBench [prior-art search]; Kaggle poker. Stated differences:
  - a common-value asset with private signals;
  - fixed anchor bots with paired common-random-number scoring;
  - secret value families.
- **Cited claims:** lab-specific risk and collusion tendencies are documented in Vending-Bench Arena (D §2.19). The claim that Opus 5 formed a cartel "in all six arena runs" is [S].
- **Proposed variant:** W §3 lists D7 alongside G3 and H2 for the third-party-decodability twist. How it would apply to a trading game is not specified.

### C28 Hidden-Dynamics Economy (D8 + G5)
- **Sources:** D8 Twin-Seed Colony and G5 Unknown Factory. See merge log §2.
- **Ideator notes:**
  - D8: long-horizon adaptive control under hidden, drifting dynamics, where errors compound. Vending-Bench spreads models widely but is noisy and has jailbreakable LLM suppliers, so this is a lower-noise version.
  - G5: FLE is the only game with evidence that its ranking tracks valued work (GDPval) (D §4). G5 is A2, possibly A1 at launch.
- **Expected human vs AI [speculation]:**
  - D8: AI ahead at full length; the short version may be close.
  - G5: frontier above the median engineer on V/V\* by 2027, but maybe below expert players at launch.
- **Expected separation [speculation]:**
  - D8: wide. Pairing should shrink CIs substantially compared with Vending-Bench's unpaired runs. Effort inversions (High > Max) and within-lab regressions (Opus 5 > Opus 5.5) should persist if real.
  - G5: large.
- **Evidence:**
  - D8: P2, P12, P16, P4, P7; B §3.2, §5 lessons 1, 3 and 8; D §2.11.
  - G5: P2, P9, P12, P13, P14; D §2.11, §4; B §3.2, §5.
- **Self-scores:**
  - D8: 3/5/4/2/3/4. Fails the rule on Q1 = 3 and Q5 = 3; the D panel flags cost and human baseline (Q4 = 2).
  - G5: 4/4/4/3/3/4, mean 3.7. Fails on Q5.
- **Risks:**
  - D8:
    - closed simulators get compiled into code and optimised (P4); declare that allowed if the dynamics are inferred, not read;
    - the public practice simulator becomes an RL environment (P7);
    - exploits in the simulator's equations; publish audits;
    - cost and human baseline.
  - G5:
    - long-horizon variance (Vending-Bench 2 bands reach ±$2.1k, P2);
    - oracle quality drifts;
    - close to FLE and Vending-Bench, so the twist must be shown to change rankings;
    - FLE open play was "prohibitively expensive" (D §2.11).
- **Prior art:** Vending-Bench 2 and Arena, FLE, CEO Arena, YC-Bench, Craftax. Stated differences:
  - paired and antithetic seeds;
  - no LLM counterparties;
  - oracle normalisation;
  - rotating hidden dynamics;
  - a hidden generated tech tree;
  - human engineers on the same API.
- **Cited claims:**
  - Vending-Bench spreads models by more than 50× [uncertain], with lab upsets (Grok 4.7 > Opus 5.5), but its ± bands overlap for ranks 3–7 and its LLM suppliers can be jailbroken (B §3.2).
  - Vending-Bench 1: Claude 3.5 Sonnet mean $2,218 vs a human's $844, though the human beat every model's worst run.
  - Vending-Bench 2 uses 60–100M output tokens per run (B §3.2).
  - FLE called 2025 models "shockingly bad" at Factorio (D §2.11).
  - FLE error rates ran from 22.99% to 40.89% across labs.
  - Vending-Bench 2 shows a wide spread plus inversions (B §3.2).
  - FLE reported a manual-crafting exploit (D §2.11); G5's 60-second hands-off holdout blocks it.
- **Spec omissions:**
  - D8:
    - 10 seeds, each with an antithetic twin;
    - an MPC oracle per seed;
    - human sessions of 2 × 2 hours; 10 paid experts over several days;
    - example: seed 7, day 311 — a silent price-regime switch, a refrigeration unit with a 30% daily failure chance unless serviced, and a second dock that pays off only if started before day 400. The paired difference of $4,120 was illustrative.
  - G5:
    - 20 seeds per model;
    - the oracle uses MILP layout and heuristic scheduling;
    - human sessions of 2 × 90 minutes, paid by V/V\*;
    - Factorio wiki knowledge is useless.

### C29 Whodunit Engine (D5)
- **Sources:** D5.
- **Ideator notes:**
  - A2, possibly both. Games like this elicit deception and detection behaviours that static Q&A can't (D §4).
  - The NPCs are scripted rather than LLMs, so they can't be jailbroken, unlike Vending-Bench's LLM suppliers (B §3.2).
- **Expected human vs AI [speculation]:** AI ahead of typical humans under the question budget and fact volume. Skilled puzzlers may match it, which would make this "both".
- **Expected separation [speculation]:** moderate to wide on detection and question efficiency. Variance comes from case difficulty, so at least 200 cases are needed.
- **Evidence:** P12, P15, P9 (efficiency), P16; D §2.15, §4; B §3.2.
- **Self-scores:** 4/3/3/4/5/5. Fails on Q3.
- **Risks:** a template question language feels artificial; parser errors; case-difficulty variance.
- **Prior art:** WhodunitBench, MIRAGE, WellPlay, Watson & Holmes (arXiv 2602.19914), hobby "murder mystery engines" [prior-art search]. Stated differences:
  - simulation-grounded witnesses with deterministic, knowledge-consistent lies;
  - a question budget;
  - proper scoring;
  - rotating secret mechanics.
- **Cited claims:** WOLF finds LLMs "weak at detecting deception" (D §2.15).

### C30 Masquerade (G4)
- **Sources:** G4.
- **Ideator notes:**
  - A2, with a possible A1 sub-score for detection. It matters for agents that negotiate or consume untrusted messages, and for safety.
  - The G panel's "most interesting A2 add-on": the proper-scored belief channel can be bolted onto any multi-agent card.
- **Expected human vs AI [speculation]:** experienced humans at or above most models on detection bits; models at or above humans on deception efficacy.
- **Expected separation [speculation]:** large and off-g.
- **Evidence:** P11, P12, P14, P15, P16; D §2.14–2.15, §4; B §3.5, §5 lessons 2 and 10.
- **Self-scores:** 4/4/3/3/3/5, mean 3.7. Fails on Q3 and Q5.
- **Risks:**
  - Anchor chat quality shapes the game.
  - Seat and role variance needs many games.
  - The metric can reward misconduct; conduct is reported separately and never folded into the score.
  - Some free-text persuasion is unscored.
- **Prior art:** Werewolf Arena, WOLF, Among Us "Deception ELO", Kaggle Werewolf, MindGames Secret Mafia. Stated differences:
  - generated role scripts;
  - a proper-scoring belief channel, giving objective detection and deception metrics without judge-labelled lies;
  - engine-checked formal claims;
  - human seats in fixed anchor tables.
- **Cited claims:**
  - "LLMs deceive convincingly but remain weak at detecting deception" (WOLF, D §2.15, [S]).
  - Elimination Game: GPT-4o ranks #7 and o3 #22, and Gemini 3 Flash outranks Pro (D §4).
  - Opus 5 formed cartels in 6 of 6 Vending-Bench Arena runs (D §2.19).
  - The Step Game's σ ≈ 0.7 put its top 4 within noise (D §2.14).
- **Spec omissions:**
  - Humans get 90 minutes, pay per win plus a log-score bonus, which is incentive-compatible (P17).
  - Conduct covers formal-claim lie rate by role, prompt-injection attempts against anchor seats, and out-of-band signalling.
  - The model occupies 1 seat.

### C31 Debate Court (W12)
- **Sources:** W12.
- **Ideator notes:** A2. Scalable oversight, scored symmetrically: how far a model can mislead is a conduct and risk axis.
- **Expected human vs AI [spec]:** AI debaters at least match humans. The key open question is whether Truth Advantage grows with capability.
- **Expected separation [spec]:** strong, including lab differences in willingness to argue falsehoods.
- **Evidence:** P11, P14, P15, P16; D §2.15; E Q2.
- **Self-scores:** 4/4/3/4/3/4, mean 3.7. Fails with human judges; the weak-model judge track may pass.
- **Risks:**
  - Human judge noise; use many judges plus the weak-model track.
  - Persuasion may track verbosity; use length caps.
  - Dual use.
  - Refusals confound DWR.
- **Prior art:** AI safety via debate; debate with verified quotes (2023–24) [bg]; G4. Stated differences:
  - generated secret worlds with generator truth;
  - frozen anchor opponents, giving absolute scores;
  - Truth Advantage as a separate oversight metric.
- **Cited claims:**
  - WOLF: LLMs "deceive convincingly but remain weak at detecting deception" (D §2.15).
  - Earlier debate work found that more persuasive debaters made judges more accurate [bg].

### C32 Nomic Engine (G9)
- **Sources:** G9, which the source labelled "bold".
- **Ideator notes:** A2. A sanctioned sandbox for reward hacking, relevant to contracts, policy and security review.
- **Expected human vs AI [speculation]:** frontier above the median human on probe accuracy.
- **Expected separation [speculation]:** large on probes; lab-specific on conduct.
- **Evidence:** P4, P11, P12, P15; D §2.19; B §5 lessons 5 and 10; G §2 (gaming).
- **Self-scores:** 4/4/3/3/4/4, mean 3.7. Fails on Q3.
- **Risks:**
  - Construct sprawl.
  - Degenerate games, such as instant-win amendments; needs entrenched rules and turn caps.
  - Prompt injection inside proposals.
  - Relevance to real contract work is speculative; a P14 test is required.
- **Prior art:** Nomic (Suber 1982); NomicLaw (arXiv 2508.05344, [web, S]), where LLMs propose and vote on legal rules in natural language; a Nomic LLM scaling study ([web, S]; content.cooperate.com/post/nomic). Stated differences:
  - executable constitutions;
  - planted loopholes with ground truth;
  - exact consequence probes;
  - anchored tables.
- **Cited claims:**
  - Vending-Bench Arena: Fable 5 initiated cartels, and Opus 5 joined in 6 of 6 runs (D §2.19).
  - A Nomic study reports non-monotonic collective behaviour with model scale ([web, S]).
- **Spec omissions:**
  - The loophole ledger records whether each loophole was discovered, exploited or patched.
  - Humans are paid for probe accuracy and wins.
  - About 120 games per model.

### C33 Exploitability Gauntlet (G10)
- **Sources:** G10.
- **Ideator notes:** A2. An opponent-independent absolute score, which fixes the pool-relative-rating problem (§3 failure mode 10). Writing CFR for a new game on the Open track is expected to be near-trivial for frontier coders.
- **Expected human vs AI [speculation]:** frontier models less exploitable than most humans.
- **Expected separation [speculation]:** large, and not in exam order.
- **Evidence:** P2, P4, P15, P16; D §2.18, §2.20; G §3.
- **Self-scores:** 4/3/4/3/5/2, mean 3.5. Passes, borderline.
- **Risks:**
  - A narrow construct with weak ties to valued work (P14).
  - The frontier may solve small games in its head, so the size knob matters.
  - Probabilities may be elicited poorly; the consistency check mitigates this.
- **Prior art:** riverline (Kuhn, Leduc and HUNL; known games); Kaggle HU NLHE (pool-relative BB/100); GTBench. Stated differences:
  - secret new games each season;
  - absolute exploitability as the headline;
  - a human elicitation baseline.
- **Cited claims:**
  - LLM Chess spreads from Astra at 1614 to Opus 5 at 1285 (D §2.20).
  - Exact exploitability has been computed for LLM poker policies ([web, S]; github.com/Lironktf/riverline).

### C34 Setter's Duel (D6)
- **Sources:** D6, which the source labelled "bold". W §3 proposed twists for it.
- **Ideator notes:** A2. Useful for test design, data generation, red-teaming, and the gap between generating and verifying. The D panel rates it anchored, uncapped and deterministic.
- **Expected human vs AI [speculation]:** AI far ahead of typical humans, who rarely produce unique puzzles within the time. Expert setters may beat AI on hardness per puzzle.
- **Expected separation [speculation]:** wide. Inversions are expected between solving strength and setting strength, because a setter must model weaker solvers.
- **Evidence:** P2, P4, P16, P15; D §2.23–2.25, §5 (anchors).
- **Self-scores:** 4/5/4/3/4/4. Passes.
- **Risks:**
  - Difficulty is measured against a ladder of LLMs, which invites puzzles that exploit LLM quirks such as tokenisation traps. Human solve time and search-tree cross-checks mitigate this.
  - The ladder ages.
  - Human setters are costly.
- **Prior art:** ZebraLogic and SATBench (puzzle generation for solving benchmarks); "Can LLMs Generate and Solve Linguistic Olympiad Puzzles?" (arXiv 2509.21820) [prior-art search]; Hide-and-Seek Game (AAAI). Stated difference: the *setter* is the subject.
- **Cited claims:** in Boardwalk, Claude 3.7 Sonnet produced 55.6% error-free code for games (D §2.25).
- **Proposed variants (W §3, for D6/G11 setters):**
  - A **self-solvability gate:** 3 fresh, memoryless copies of the setter, without the certificate, must solve at least 2 of 3.
  - A **cross-lab solvability gate:** at least one solver from another lab, or a frozen anchor, must solve the item; otherwise it is void.
  - These block one-way-function trapdoors and same-family "Schelling codes", and tie the setter's reward to its own frontier.
  - A joint two-parameter IRT fit over solvers × items gives each model both a setter score and a solver score.
  - Prior art for the twist: Critique-Resilient Benchmarking (ICML 2026) [web].
- **Spec omissions:**
  - Duel mode: two setters swap sets and solve each other's; zero-sum, for display only.
  - Human strata: 100 public (1 hour, 3 puzzles) and 20 setters (4 hours, 10 puzzles), with the same tools minus code for a no-code stratum.
  - The example's human median solve time of 14 minutes.

### C35 Game Designer's Duel (W8)
- **Sources:** W8, which the source labelled "bold".
- **Ideator notes:**
  - A2, with possible A1 on play against strong humans.
  - One of the few *creativity* constructs that can be scored objectively.
  - The depth gate excludes trivial or solved designs.
- **Expected human vs AI [spec]:** strong humans at least match models in direct play of novel games. Models likely produce more admissible designs. How their depth compares with human designs is unknown.
- **Expected separation [spec]:** large (gg-bench 7–9% vs 31–36%).
- **Evidence:** P2, P4, P7, P16; D §2.22–2.25, §4–5; F §2.
- **Self-scores:** 4/5/3/3/3/4, mean 3.7. Fails on Q3 and Q5.
- **Risks:**
  - Depth can be gamed with MCTS-hard but dull games, such as arithmetic races; a diversity and "interest" audit mitigates this.
  - Designs may be optimised for MCTS rather than minds.
  - Play variance.
  - Cost and complexity.
- **Prior art:** gg-bench (LLM-generated games against RL agents; dormant since Jul 2025); Ludi/Ludii automated game design [bg]; H6 and D14. Stated differences: competitors design for each other, under objective gates, and play on an anchored ladder.
- **Cited claims:**
  - gg-bench: best 36% against RL agents.
  - TTT-Bench: reasoning models score 41% lower than on MATH 500 (D §2.23–2.24).
  - LLM Chess has ±110–180 Elo at 29–67 games (D §2.20).
- **Spec omissions:**
  - Novelty is checked by canonical form and behavioural fingerprint.
  - Depth is measured over 200 games per level pair.
  - Inadmissible games score 0.
  - Play uses 5 anchor budgets, and a bot-writing code track is scored separately.
  - Example "Tidewall": depth chain 7, first-player win rate 52%.

### C36 Season Forge (G8)
- **Sources:** G8.
- **Ideator notes:**
  - A2, including against human programmers; the top humans may still win (A1 at the elite tier).
  - Close to valued software work (P14). Bot-writing is a distinct construct (D §2.22, §2.6).
  - Training on "write a bot for a new game" is the valued skill itself and is welcome.
- **Expected human vs AI [speculation]:** frontier agents beat the median human entrant; the top human may still win. The heuristic-contest precedent is background, not verified.
- **Expected separation [speculation]:** large. Agentic coding separates labs (Terminal-Bench reversals, E Q2).
- **Evidence:** P1, P4, P14, P17, P19, P20; D §2.6, §2.22, §5.
- **Self-scores:** 5/5/3/4/3/5, mean 4.2. Fails on Q3 and Q5. The G panel still recommends carrying it forward.
- **Risks:**
  - Only 1–3 games per season means high per-season rank variance, so rolling averages are needed.
  - Humans cheating with AI.
  - Human prizes are the main cost.
  - Harness dependence.
- **Prior art:** CodeClash (known arenas), NetHackers (fixed game), Battlecode, Halite, Lux AI, AtCoder heuristic contests. Stated differences:
  - a secret game released simultaneously to humans and AIs under an identical budget;
  - an anchored ladder;
  - private evaluation maps.
- **Cited claims:** CodeClash has run more than 2,000 tournaments (D §2.22).
- **Spec omissions:**
  - The example's claim that "the best 2026 agents' logs show them writing a flood predictor at hour 2" was removed as an outcome claim.
  - Each game has 2–3 mini-variants.
  - The human-only track is enforced by proctoring and telemetry.

### C37 Saboteur's Patch (D9)
- **Sources:** D9. W §3 proposed twists for it.
- **Ideator notes:** A2. Code review, security, and monitoring untrusted AI code.
- **Expected human vs AI [speculation]:** AI ahead on throughput and recall; professionals competitive on precision.
- **Expected separation [speculation]:** wide. Good saboteurs are not necessarily good auditors, and labs differ in refusing to sabotage (S7).
- **Evidence:** P6, P12, P15, P16; D §2.22 (code as proxy); G §2 (reward hacking).
- **Self-scores:** 4/4/4/3/4/4. Passes.
- **Risks:**
  - Refusals confound the saboteur side, so the auditor side is the headline.
  - Dual use.
  - Benign diffs must look realistic.
- **Prior art:** Hide and Seek Game (AAAI; subtle errors in math reasoning); GBQA (arXiv 2604.02648) [prior-art search]; AI-control backdoor settings (background, not in the dossiers). Stated differences:
  - an anchored two-sided ladder;
  - witnesses verified by execution;
  - secret repo and property families.
- **Cited claims:** GBQA's best model found only 48.39% of planted bugs in games (Claude 4.6 Opus) [prior-art search].
- **Proposed variants (W §3):**
  - Regenerate the saboteur side each season from the *newest* frontier models, so difficulty co-evolves with the frontier.
  - Publish the full cross-lab auditor × saboteur matrix, and flag same-lab cells for style recognition.
  - Score auditors on TPR at 1% FPR, plus localisation.
  - Add a professional-reviewer human baseline.
- **Spec omissions:**
  - 60 sabotage attempts × 5 anchor auditors.
  - Typical non-programmers can't take part, so the comparison is against skilled humans.

### C38 Relay (W9)
- **Sources:** W9, which the source labelled "bold".
- **Ideator notes:**
  - Both archetypes. Cross-episode learning, with the state-carry channel fixed and identical for humans and models.
  - The harness can't be captured, because the notebook protocol is itself the benchmark (P18).
- **Expected human vs AI [spec]:**
  - "Genuinely uncertain." Models may write more complete notes; humans may prioritise better and flag drift.
  - A1 is likely on perceptual domains.
  - Human transmission chains accumulate improvement in lab tasks [bg].
- **Expected separation [spec]:** strong, since note quality compounds over generations.
- **Evidence:** P18, P9, P1, P7, P12; E Q1, Q3 #2; A §2.3; F §1.
- **Self-scores:** 4/4/4/4/3/4, mean 3.8. Fails on Q5; it needs the lite track.
- **W recommendation:** combine with W4 (C42 adversarial mode) as Devil's-Lab domains inside Relay chains.
- **Risks:**
  - The notebook cap drives results; report a sweep.
  - Domains may saturate after one good note; mitigated by drift and depth.
  - Human-chain cost and attrition.
  - Injected instructions in notes are harmless to the score but logged.
- **Prior art:** G7 and D4 (single-agent notebooks); CL-bench and Continual Learning Bench (E); iterated-learning experiments [bg]. Stated differences:
  - successors are *different* agents, which gives humans exact parity;
  - the score is successor gain;
  - rules drift;
  - notes are read across species and by a reference reader.
- **Cited claims:**
  - CL-bench best is 23.7%.
  - Continual Learning Bench: agents don't reuse knowledge, and naive in-context learning beats memory systems (E Q1).
  - On ARC-AGI-3, state carry decided the score: 62.7 vs 98.6 (A §2.3).
- **Spec omissions:**
  - 5 chains × 20 domains per model.
  - Human chains: about 20 chains × 8 generations on 6 domains.
  - Generation 1's note "copper spikes after storms".

### C39 Blind Spot Cartographer (W2)
- **Sources:** W2, which the source labelled "bold".
- **Ideator notes:**
  - The *items* form an A1 benchmark; *authoring skill* is an A2 score.
  - It uses the generation-vs-perception asymmetry: a model can draw 7 overlapping circles in SVG and know the count, yet fail to count them from pixels.
  - It matters for red-teaming, eval creation and safety: does a model know where it is weak?
  - Why training doesn't trivially pay: a lab that trains "find your blind spots" gains blind-spot knowledge (the construct), and a lab that trains its models to fix those spots shrinks everyone's harvest ("the intended arms race").
- **Expected human vs AI [spec]:** accepted items are, by construction, about 0% for the AI panel vs at least 60% for humans. The real question is how long they last: text tricks close fast, while perceptual items persist.
- **Expected separation [spec]:** large on authoring, because it needs both generation skill and self-knowledge of perception limits.
- **Evidence:** P1, P5, P8, P17, P20; A §2.8, §5a; C §3 (label errors); H3/D6 in this phase.
- **Self-scores:** 4/4/4/4/4/5, mean 4.2. Passes; Q1 depends on solving API exposure.
- **W recommendation:** carry forward as a bold way to make the frontier renew an A1 benchmark.
- **Risks:**
  - API exposure of items to the panel's providers; mitigated by zero-data-retention endpoints, open-weight panel members, and burn accounting.
  - Quirk mining; mitigated by banned categories and diversity weighting.
  - Items that exploit input-handling limits such as image resolution; mitigated by standard input specs.
  - Human-gate label errors; mitigated by majority agreement and an appeal window.
  - Critics may call the gap artificial (P10).
- **Prior art:** H3 (human authors); D6 (AI setters vs AI solvers); HLE (expert humans with an AI filter); BlindTest (hand-designed). Stated differences:
  - AI authors;
  - a human-easy gate and a self-failure gate;
  - the frontier supplies the labour that renews an A1 benchmark.
- **Cited claims:**
  - SimpleBench closed, 88.4 vs 83.7 (A §2.4).
  - BlindTest and BabyVision show perceptual gaps (A §2.8, E Q1).
  - Vision spreads 3.5× by lab (BabyVision; E Q2).
- **Related:** uses the same gates as C05 (see merge log).
- **Spec omissions:**
  - Human gating costs about $2–3k per season for 15 authors.
  - Keys are deterministic and confirmed by human-gate agreement.

### C40 Rules Gauntlet (G1 + D14)
- **Sources:** G1 Blind Rules Gauntlet and D14 Rulebook Gauntlet. See merge log §2.
- **Ideator notes:**
  - G1 construct: learning an unknown adversarial game from play, including inferring the goal from how a competent opponent plays (inverse planning). Its blind track is expected A1 at launch, and its revealed track A2.
  - D14 construct: acting on long documents under adversarial pressure; classic games are contaminated or solvable by engines (D §5). D14 is "both".
  - The G panel calls G1 its **strongest single flagship**. It has three built-in ablations (blind vs revealed, Closed vs Open, symbolic vs rendered), which address P20. It "could absorb G13 and G11 as sub-leagues" in a "game decathlon".
- **Expected human vs AI [speculation]:**
  - G1 blind track: the median gamer beats the frontier at launch.
  - G1 revealed track: frontier at or above the human median.
  - D14: A1 possible; A2 likely at the Sep 2026 frontier, where rule compilation has become easy (F §2 trend).
- **Expected separation [speculation]:** large, and not in exam order (G1).
- **Evidence:**
  - G1: P1, P2, P3, P4, P9, P16, P18; D §2.5, §2.23, §2.25, §5; F §2–4.
  - D14: P2, P4, P10, P16; D §2.20–2.25, §5.
- **Self-scores:**
  - G1: 4/4/4/4/4/4, mean 4.0. Passes.
  - D14: 4/5/3/4/4/4. Fails on Q3 (game noise).
- **Risks:**
  - G1: the family meta-skill can be learned; ARC-AGI-3 fell in about 5 months (F §1), and rotation delays this but doesn't stop it.
  - G1: weak ISMCTS on some families could make the ladder non-monotone, so each family's anchors must be validated.
  - G1: the legal-move list leaks part of the rules (intended).
  - G1: the history-compression protocol moves scores, so it is frozen.
  - D14: game noise, so plan at least 150 games per model.
  - D14: tool-solvability through the code track.
  - D14: the cost of enough games.
- **Prior art:** gg-bench (gives rules; dormant); ARC-AGI-3 (single-player, deterministic); GGP/Ludii (rules in a game-description language); Kaggle Game Arena (known, contaminated games); TTT-Bench; DeepMind code world models. Stated differences:
  - hidden goals;
  - an adversary whose play is evidence;
  - an absolute MCTS ladder;
  - a blind/revealed ablation;
  - long rulebooks with rare-rule traps;
  - separate tracks for play and compilation.
- **Cited claims:**
  - ARC-AGI-3 was under 1% at launch (F §2).
  - Witness: the best model solves 24% of private level slots (F §2, [S]).
  - Witness: Opus 5 scored 59.9 without rules and 97.8 with them (F §2, [S]).
  - ZendoWorld agents run near-uninformative experiments (F §2).
  - gg-bench: reasoning models won 31–36% vs RL agents in 2025, and LLMs won only 7–36% against RL agents on new generated games (D §2.23).
  - TTT-Bench: reasoning models score 41% lower on new tic-tac-toe variants than on MATH 500 (D §2.24).
  - BALROG within-suite reversals: Opus 5 leads Astra on TextWorld and trails it on MiniHack (D §2.6).
  - LLM Chess still has ±110–180 Elo with 29–67 games (D §2.20).
  - G1's power target: about ±50 anchored Elo at 95% needs about 500 games across 60 families [speculation].
- **Spec omissions:**
  - G1:
    - ISMCTS at 2⁴…2¹⁴ playouts, calibrated per family by anchor round robins;
    - opponents chosen by staircase;
    - rating from games 3–8;
    - a GUI with a clickable legal-move list;
    - 200 public + 50 experienced gamers, 3 families × 8 games, 90 minutes, pay per win;
    - hex 7×7 example with push moves;
    - cost of about 480 games × 30 decisions ≈ 15k calls.
  - D14:
    - MCTS at 100/1k/10k/100k rollouts, Elo anchored like LLM Chess's Dragon ladder;
    - 40 games with alternating seats;
    - humans read for up to 45 minutes and play over 3 hours;
    - example "Ferrymen": a hex river board with hidden cargo, and a flood rule that triggers on turn 13 if 3 or more barges share a lane.

### C41 Practice Week (H6)
- **Sources:** H6.
- **Ideator notes:** A1 (speculative) and A2, on moat M5. Rule understanding is not tested; the rules are given in full.
- **Expected human vs AI [speculation]:** humans show larger learning gains; who ends at the higher level is uncertain.
- **Expected separation [speculation]:** strong.
- **Evidence:** P2, P4, P9, P12, P16, P18; D §2.20, §2.23, §2.25; E Q1.
- **Self-scores:** 4/4/3/3/3/4. About 30%. Biggest risks: a weak A1 prior, and the notes protocol deciding the score.
- **Risks:**
  - The weakest A1 claim of the H set.
  - Reasoning models may internalise search.
  - Recruiting humans for a whole week is expensive.
  - The notes protocol will decide the score, as the harness did on ARC-AGI-3; report no-notes, notes and full-log tracks.
- **Prior art:** gg-bench, LLM Chess, Kaggle Game Arena, TTT-Bench. Stated differences:
  - a new game each season;
  - learning gain as the headline;
  - fixed bot anchors;
  - human cohorts given the same practice.
- **Cited claims:**
  - Opus 5 is rated 1285 at chess (D §2.20).
  - In gg-bench's generated games, o1 won 36% against self-play-trained agents (F §2).
  - Agents do not reuse knowledge across episodes (Continual Learning Bench, E Q1).
  - LLM Chess ranks differ from other boards (D §1, §2.20).

### C42 Hidden-Rule Lab (H8 + W4)
- **Sources:** H8 Koan Lab and W4 Devil's Laboratory, which the source labelled "bold". See merge log §2.
- **Ideator notes:**
  - H8 is A1, on moat M5. It has physical and perceptual primitives with image-only state, which blocks compiling the world into code.
  - W4 is A1 on the visual track and A2 on the text track. It deliberately does *not* score execution efficiency.
  - W4's structural point: luck is removed, because any ambiguity left by weak experiments gets exploited. Guessing the prior's favourite rule or learning the practice grammar doesn't pay, since the Devil's grammar contains primitives outside it.
  - W recommendation: "carry W4 forward — the cleanest A1 candidate: an efficiency construct, luck removed by design, and a human-scale baseline".
- **Expected human vs AI [speculation]:**
  - H8: a 20–40 pp human edge at a matched experiment budget.
  - W4: humans lead on the visual track. The text track will be closer: blicket studies find models near human on inference accuracy but less efficient explorers (E Q1).
- **Expected separation [speculation]:** H8 moderate; W4 large on the efficiency statistic.
- **Evidence:**
  - H8: P9 (confidence L-M), P3, P4, P8; F §2–4; §5c targets #1 and #8.
  - W4: P3, P4, P8, P9, P2; F §2–4; A §2.3; E Q3 #3.
- **Self-scores:**
  - H8: 4/3/3/4/4/3. About 35%. Biggest risk: efficiency moats fell on ARC-AGI-3.
  - W4: 4/4/4/5/4/4, mean 4.2. Passes.
- **Risks:**
  - H8: efficiency moats fell on ARC-AGI-3 once models understood the mechanics (A §2.3).
  - H8: the Bayesian optimum over physical primitives is hard to define.
  - W4: an approximate Devil can be exploited with queries in regions it undersamples; use exact enumeration for small L, plus audits.
  - W4: players may find the game unfair; calibrate L with pilots.
  - W4: family RL transfers somewhat; rotate primitives.
  - W4: the visual track mixes perception with experimentation. That is the declared A1 lever, and the JSON track isolates it.
- **Prior art:** ZendoWorld, AutumnBench, FalsifyBench, Witness, WILT, BoxingGym, NewtonBench (F §2). Stated differences:
  - physical and perceptual primitives with image-only state;
  - probes instead of rule statements;
  - ideal-reasoner normalisation (H8);
  - an adaptive adversary plus worst-case held-out scoring (W4).
- **Cited claims:**
  - ZendoWorld: humans win 73.3% vs 44.5% for vision-language agents, whose experiments are "near-uninformative" (F §2).
  - AutumnBench: 517 humans beat 2025 models (E Q1).
  - About 27% of o3's correct ConceptARC answers use the wrong rule, vs about 8% for humans (E Q1).
  - FalsifyBench: negative testing predicts success, and "no model comes close to optimal" (F §2).
  - ARC-AGI-3: Astra used fewer actions than the median human on 96% of levels (A §2.3, P9).
  - Witness public-gym RL raised the private-test score from 2.1 to 5.4 (F §3).
  - The Eleusis cogame draws from a public catalogue of 68 rules, which can be enumerated (F §2).
- **Spec omissions:**
  - H8's 3D world uses place/rotate/stack actions from a palette.
  - Rules are compositions up to depth 3 over 200 or more primitives, and at least 30% of primitives are new per season.
  - W4's adversary holds a weighted sample of 10⁵–10⁶ rules. Probes are chosen to maximise disagreement among surviving rules.
  - Humans are paid for accuracy minus a cost per experiment. There is a scientists subgroup, and every game is solved by at least 2 people (M9).
  - Costs: H8 $200–1,000; W4 $50–400 (40 games × at most 40 queries; adversary compute is modest: enumeration plus SMT).
  - Example primitive: "touches the largest" as a new-season primitive.

### C43 Eleusis Masters (G11)
- **Sources:** G11, which the source labelled "bold". W §3 proposed twists for it.
- **Ideator notes:**
  - Both archetypes: solving is expected A1 at launch, setting A2.
  - The solver construct ranks #1 among Phase 2 targets (§5c).
  - Setters must model how other minds differ.
  - Setter outputs become the next season's item bank, so the benchmark renews itself.
- **Expected human vs AI [speculation]:** humans ahead on solver efficiency and fidelity at launch. All the supporting evidence predates the Sep 2026 frontier.
- **Expected separation [speculation]:** large, especially in the setter role, "which static benchmarks never measure".
- **Evidence:** P3, P7, P9, P11, P20; F §2–4; E Q1, Q3 ranks 3 and 6; §5c rows 1 and 8.
- **Self-scores:** 4/4/4/4/4/4, mean 4.0. Passes.
- **Risks:**
  - Setters may converge on degenerate rule styles; validity filters are needed.
  - The DSL leaks after a season.
  - Declaring rules in a DSL is harder for humans, hence a guided rule builder for both.
  - It closes fast once targeted (ARC-AGI-3 precedent).
- **Prior art:** Eleusis (Abbott); the Hugging Face "Game of Science" Eleusis benchmark (solver-only, with a "boldness" index) ([web, S], huggingface.co/spaces/huggingface/eleusis-benchmark); cogame-eleusis; ZendoWorld; WILT. Stated differences:
  - the adversarial setter role;
  - a secret rotating DSL;
  - perceptual attributes;
  - fidelity probes;
  - human tables.
- **Cited claims:**
  - ZendoWorld: 73.3% vs 44.5% (F §2).
  - ConceptARC wrong-rule answers: 27% for models vs 8% for humans (E Q1).
  - FalsifyBench: "no model comes close to optimal" (F §2).
  - The ZendoWorld template used 19 people and 10 plays per game (F §2).
- **Proposed variants (W §3):**
  - Replace the fixed hidden rule with W4's adaptive adversary plus worst-case held-out scoring.
  - Setter self-solvability and cross-lab solvability gates, and joint IRT (see C34).
- **Spec omissions:**
  - Solver anchoring uses a Bayesian-ideal solver where the DSL permits.
  - The example solver behaviours: A varies only hue and declares at turn 14 with fidelity 50/50; B repeats accepted cards.
  - The human panel is shared across models.

### C44 Convention Cross-Play (D11 + G2)
- **Sources:** D11 Stranger Coordination and G2 Convention Crucible. W §3 proposed twists for D11. See merge log §2.
- **Ideator notes:**
  - Zero-shot coordination, for multi-agent systems that mix vendors and for human–AI teams.
  - D11 and G2 are both "both". G2 expects A1 when paired with humans and A2 across models.
  - Memorised Hanabi conventions (the "H-group" style) don't apply, because attribute and hint structures are new.
- **Expected human vs AI [speculation]:**
  - D11, A1 side: human–human pairs may beat model–stranger pairs on fresh signalling games.
  - D11, A2 side: the cross-play matrix spreads models. Lab clustering (same-family models coordinating better) is itself informative.
  - G2: humans adapt to partners faster.
- **Expected separation [speculation]:** moderate to large (G2). D11 rated Q3 = 3.
- **Evidence:**
  - D11: D §2.16, §2.17; P12, P16.
  - G2: P3, P7, P12, P16, P17; D §2.16, §4; §5c row 9.
- **Self-scores:**
  - D11: 4/4/3/4/3/4. Fails on Q3 and Q5; needs large game counts.
  - G2: 4/3/3/3/4/3, mean 3.3. Fails on Q3.
- **Risks:**
  - D11: high variance from seats and deals; humans are costly; convention anchors can be learned if public.
  - G2: convention bots may be guessable from priors.
  - G2: human cross-play is high-variance and costly.
  - G2: tactical skill confounds convention inference; use the bot-to-bot optimum as a ceiling control.
  - G2: Kaggle added Hanabi in Sep 2026 (D §2.1), a pre-emption risk.
- **Prior art:** LLM-Hanabi; Kaggle Hanabi (Sep 2026; pool-relative, fixed rules); Codenames in clembench; "Epistemic Schelling Points" (arXiv 2607.11363, title only; D §2); the Hanabi Learning Environment and zero-shot coordination research (background). Stated differences:
  - fresh signalling games each season;
  - anchored cross-play including humans;
  - hidden-convention anchor partners;
  - a human cross-play ratio.
- **Cited claims:**
  - LLM-Hanabi: first-order theory of mind correlates with success at ρ = 0.76 (D §2.16; [S]; the fact-check says the excerpt reports "r"). No human baseline was found for it.
  - For a human edge: in repeated reference games human dyads rise from 78% to 96%, while multimodal LLM agents are "aligned but not partner-specific" [web, S: arXiv 2606.08081].
  - Against: "LLMs and people both learn to form conventions" [web, S: arXiv 2602.08208]. H2/C07 reads the same paper as evidence that mixed human–AI pairs fail.
- **Proposed variants (W §3 on D11):**
  - 3-game matches with Adaptation = game 3 − game 1. The merged spec uses G2's 6-game matches instead.
  - A **Legibility** score: the partner's improvement when paired with the subject.
  - A mixed-effects decomposition (subject + partner + game).
  - Report the human–AI cell separately. It may be the weakest cell, which would be an A1 finding on legibility to humans.
- **Spec omissions:**
  - G2's example variant #417: 3 players, 12-card hands, shapes {◇,◆,○}, ranks 1–4.
  - D11's example "Lanterns": flash 1 of 3 unlabelled colours; Anchor-C uses red for "play your leftmost". Its illustrative 14/20 vs 17/20 self-play figure was removed as an outcome.
  - Participants were card-game players and the general public, with 60 minutes and pay per point.
  - Costs: D11 $30–150; G2 about 400 games × 25 turns ≈ $1–1.5k, plus about $2k of live pairing.
  - Build targets are generated partial orders, e.g. "piles alternate filled/hollow while rank ascends". Hints are restricted to generated relations.

### C45 Crowd Oracle (G12)
- **Sources:** G12, which the source labelled "bold".
- **Ideator notes:**
  - Both archetypes. The predicted result is A2, "but it is genuinely uncertain".
  - It matters for product design, forecasting, negotiation, and detecting **AI–AI tacit coordination** (collusion) that is stronger than AI–human coordination.
  - Memorised focal points ("Grand Central at noon") don't apply.
- **Expected human vs AI [speculation]:** frontier models may beat the median individual at hitting the mode, having absorbed aggregate human text. Visual and spatial items may favour humans.
- **Expected separation [speculation]:** unknown; plausibly large. Output homogenisation across labs (Artificial Hivemind, E Q3 rank 8; contested) predicts AI–AI coordination well above AI–human coordination.
- **Evidence:** P14, P16, P17; E Q3; D §2 (the "Epistemic Schelling Points" title, arXiv 2607.11363 [S]).
- **Self-scores:** 4/3/3/5/5/3, mean 3.8. Fails on Q3.
- **Risks:**
  - Strategic depth is modest; the intricacy is in modelling people.
  - Culture dependence.
  - It rewards being average.
  - It may simply measure "silicon sampling" fidelity.
  - Static items could leak once scored, so they are re-collected each season.
- **Prior art:** Schelling focal-point experiments; beauty-contest LLM studies; the Epistemic Schelling Points paper. Stated differences:
  - incentive-paid, private, seasonal human-population payoffs;
  - a leave-one-out human baseline;
  - generated stimuli;
  - an AI–AI vs AI–human coordination gap.
- **Spec omissions:** the example's illustrative distribution (41% pick the red hut, 22% the lighthouse, and a centre pick scoring 3%) was removed.

### C46 Grift (H12)
- **Sources:** H12.
- **Ideator notes:** both archetypes, on moat M1. Human grifters bring fresh tactics every week, so the adversary renews itself.
- **Expected human vs AI [speculation]:** honest-role humans lose less to grifters than AIs do, with a clear lab spread (A2).
- **Expected separation [speculation]:** strong, because labs differ in conduct (P11; E Q2).
- **Evidence:** P11, P12, P16; D §2.14–2.15, §2.19.
- **Self-scores:** 5/4/3/5/2/5. About 50%. Biggest risks: variance, cost and ethics.
- **Risks:**
  - Social games have the highest variance of any game type (D §1), and this design is expensive.
  - Consented deception needs ethics review.
  - Humans may spot the AIs by writing style.
  - Labs train against prompt injection, which is legitimate improvement.
- **Prior art:** Vending-Bench Arena, the Elimination Game, Werewolf and Avalon, the deception rating in the Among Us study, Diplomacy. Stated differences:
  - mixed human–AI pools;
  - humans as an adversary that keeps renewing;
  - a deterministic "conned" ledger.
- **Cited claims:**
  - WOLF: LLMs "deceive convincingly but remain weak at detecting deception" (D §2.15).
  - In Vending-Bench Arena, Claude models leaked supplier prices, and Opus 5 proposed or joined a price cartel in all 6 runs (D §2.19).
- **Note:** the source card gives no example instance.

### C47 Defuse Line (W11)
- **Sources:** W11.
- **Ideator notes:**
  - Both archetypes: A1 expected when live, A2 when paused.
  - The AI must read fast, ask the right questions, repair imprecise human descriptions, and manage latency.
  - It maps onto AI support agents guiding field technicians.
- **Expected human vs AI [spec]:** paused, AI experts at least match humans, since they read long manuals perfectly. Live, reasoning latency and dialogue repair may flip that to A1.
- **Expected separation [spec]:** strong, with latency-driven inversions. Fast Flash tiers may beat slow flagships live, echoing Flash > Opus on NYT Connections (B §4).
- **Evidence:** P10, P12, P13, P17; A §2.17; B §4; D §4.
- **Self-scores:** 4/4/3/4/3/5, mean 3.8. Fails on the human track; the AI-operator track may pass.
- **Risks:**
  - Speech-recognition confounds, so text is primary.
  - Operator variance and learning; mitigated by many operators, first-exposure module types and within-operator estimates.
  - Human cost.
  - It may be seen as a gimmick.
- **Prior art:** GPTNT (Jun 2026; AI–AI Keep Talking and Nobody Explodes with the official manual) [web, arXiv 2606.28514]; G6. Stated differences:
  - secret, generated manuals;
  - a human operator partner;
  - the live-vs-paused ablation.
- **Cited claims:** real-time play is a durable human advantage: VideoGameBench 0.48% live vs 1.6% paused (A §2.17, P10).
- **Spec omissions:**
  - The anchor bot is a "perfect-reader" given structured device state as an upper bound.
  - Operators are paid novices, each playing with several experts.
  - Each manual runs 10–30 pages. Example manual §4.2: "If exactly one glyph is filled and the serial ends odd, rotate two clockwise of it, unless a red wire was cut in module 2."

---

## 5. Coverage & gaps

### 5.1 Distribution

- **By archetype:** A1 13 (28%), A2 24 (51%), both 10 (21%).
  - The A2 set is the largest, reflecting the D and W panels.
  - All 13 A1 candidates come from the H and G panels.
  - 8 of the 10 "both" candidates are games.
- **By format:** benchmark 17, game 27, hybrid 3.
  - Only C38 is a both-archetype benchmark.
- **By primary ability** (the consolidator's rough grouping; some candidates fit two groups):

| Ability cluster | Candidates | n |
|---|---|---|
| Perception and perceptual learning (motion, fine vision, audio, spatial, physics-from-video) | C01, C03, C04, C06, C11, C12 (plus C02 physical world; C08 partly perceptual) | 6–8 |
| Real-time and concurrent action | C09, C10, C47 | 3 |
| Rule induction, experimentation, test-time and cross-episode learning | C13, C24, C38, C40, C41, C42, C43 (C21 experiment choice) | 7–8 |
| Coordination and communication with humans or unfamiliar partners | C07, C08, C12, C44, C45, C47 | 6 |
| Deception, persuasion, adversarial social reasoning | C29, C30, C31, C46 (C32 conduct) | 4–5 |
| Metacognition, calibration, epistemic policy | C14, C15, C16, C26 | 4 |
| Teaching and transferring knowledge to other minds | C19, C20, C38 | 3 |
| Forecasting and world-modelling | C21, C22, C23, C27 | 4 |
| Strategic play and mechanism design | C25, C27, C32, C33, C41 | 5 |
| Long-horizon agency, memory, reliability | C17, C18, C28, C36 | 4 |
| Constructive or generative tasks (authoring items, puzzles, games, bots) | C05 (human authors), C34, C35, C36, C39, C43 (setter) | 5–6 |
| Program understanding and security | C37 (C36) | 1–2 |

### 5.2 Obvious gaps and imbalances

These are noted only, not filled.

1. **No cheap, text-only, human-free A1 candidate.**
   - Every A1 candidate relies on perception, real time, the physical world, live humans, or a test-time learning protocol.
   - The two partial exceptions are C40's blind track and C42's text track, whose authors expect the text variants to be *closer* or A2.
   - This matches the Phase 2 finding that text-only gaps have mostly closed.
2. **Open-ended language output is essentially absent.**
   - No candidate scores writing quality, long-document synthesis, or open-ended creativity.
   - This is consistent with the deterministic, judge-free scoring requirement. Creativity appears only through objective proxies (C34, C35, C39).
3. **Some domains are not directly targeted.**
   - Formal mathematics, theorem proving, and natural-science reasoning.
   - C23 covers computational experiments, and C21/C24 cover statistical induction.
4. **Audio is thin.**
   - It has one candidate (C04), plus a secondary voice track in C47.
   - The H panel flags audio as the thinnest evidence base; no Phase 1 dossier covers it.
5. **Embodiment is limited.** Only C02 uses real hardware. There is nothing on manipulation beyond webcam-and-servo rigs, and nothing tactile.
6. **Other absent areas.**
   - GUI and computer-use agency (operating real apps, web or OS) has no dedicated candidate, although C01 and C09 cite computer use as motivation.
   - There are no multilingual or cross-lingual candidates. Cultural variation appears only in C45's country strata.
7. **Human-participant dependence is concentrated in A1 and "both".**
   - C05, C07, C08, C12, C38, C44, C45, C46 and C47 need live or large human panels on an ongoing basis. That concentrates cost, variance and logistics.
   - Cheap-per-model A1 options, once baselines exist, are mainly C01, C03, C04 and C11.
8. **Several A2 candidates have only small or specialist human baselines.** C24, C25, C28, C36 and C37 use 30–100 skilled people. For them, "AI > human" would be established against specialists or small samples rather than typical adults.
9. **Safety and conduct are mostly a secondary axis.**
   - It is secondary in C30, C32, C37, C45 and C46.
   - It is the headline only in C31 (Truth Advantage, plus DWR as a risk metric) and partly in C46 (conned rate).
10. **Cost is skewed.**
    - Many candidates, mostly games, estimate roughly $1k or more per model run: C06 duel, C08, C09, C10, C12, C13, C28, C30, C36, C38, C40, C44. C46 and C36 also carry large per-season human costs.
    - The cheapest per model (≤~$150) are C14, C16, C17, C19, C29 and C45, all [ideator estimate].
11. **Infrastructure overlaps.** These could be bundled later:
    - stumper gating (C05, C39);
    - frozen small-model learners (C19, C20);
    - betting against a frozen-panel house line (C14, C15, and C26 bids);
    - generated-game engines with MCTS ladders (C33, C35, C40, C41);
    - hidden-rule experiment engines (C42, C43, and W's suggested C38 + C42 combination);
    - altered-physics primitive grammars (C06, with C42's physical-stability primitives).
12. **Most expectations rest on dated anchors.**
    - Most A1 expectations rest on anchors that predate the Sep 2026 frontier (H panel caveat).
    - Most A2 separation expectations rest on inversions that the sources themselves note are often within noise (Phase 2 §1).
    - The D panel's falsification test applies to every A2 candidate: correlation with ECI or AA above about 0.9 after controlling for release date means no added information.
