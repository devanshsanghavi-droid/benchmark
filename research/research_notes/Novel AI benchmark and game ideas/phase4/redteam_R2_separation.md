# Phase 4 red team R2: saturation and separation (Q2, Q3)

As of 30 Sep 2026. Reviewer: independent red team R2 (Claude Opus 5.5). **Lens:** Q2 "Will it saturate quickly?" and Q3 "Does it separate strong from weak models, or humans from AI, by a clear margin?" (rubric anchors in `../phase2/design_principles.md` §7). **Independence:** I read only `../phase3/candidates_spec.md`, `../phase2/design_principles.md` and the Phase 1 dossiers. I did not open the ideation rationale or any `ideas_*.md` file.

**Conventions.**
- Dossier citations look like "A §2.3".
- Web evidence is marked [search extract] when I saw only a search-result summary; arxiv.org and several other hosts were not opened.
- [speculation] marks my own untested judgement.
- Probe results come from informal single-model probes (the reviewer model, Claude Opus 5.5) and are weak evidence. The scripts and logs are in `probes/`.

**Scores.**
- Q2: 5 = headroom that renews; 1 = saturated in under 6 months or already above 80%.
- Q3: 5 = a gap many times the CI, or disjoint frontier CIs; 1 = leaders inside each other's CIs.
- A kill means a flaw on this lens that I could not see a fix for, not a verdict on the idea overall.

**Headline.** 12 keep, 32 revise, 3 kill. For the A2 candidates, "AI beats typical humans" is almost never the binding constraint. The reviewer model solved every text-only probe task at or above what a plausible human would manage [speculation for the human side]. The binding constraints are ceiling effects and whether the score is just a noisy proxy for the general factor. For the A1 candidates, most of the evidence for a human advantage predates the Sep 2026 frontier, and much of the remaining gap is plumbing (frame rate, latency, harness), not cognition. ARC-AGI-3 shows that plumbing gaps can collapse within months: 62.7% vs 98.6% for the same model on two harnesses, and <1% to 99.9% in about 5 months (A §2.3).

---

## 1. Scores for all 47 candidates

| ID | Name | Q2 | Q3 | Main attack | Fix | Verdict |
|---|---|---|---|---|---|---|
| C01 | Kinetic | 2 | 4 | The gap is real today: MLLMs mistake point-light walkers for "constellations" ([ActPLD, arXiv 2509.23517](https://arxiv.org/abs/2509.23517) [search extract]), and MMSI-Video is 96.4 vs 38.0 (A §2.14). But much of it is frame-sampling plumbing. A frame-list harness, or tools-on frame differencing, removes the "single frames are noise" barrier, and targeted training closed ClockBench from 13% to 67% in about 12 months (A §2.9). | Headline the native-rate vs frame-list-harness delta. Add carriers that defeat low-level optical flow (second-order and biological-motion semantics). Flag carriers a script can solve. | revise |
| C02 | Live Rig | 3 | 3 | With 10–15 fps webcams and API latency, the tilt-maze goals test control latency. About 10 rig-hours per model yields few independent outcomes, and rig rebuilds break comparisons across seasons. | Add a turn-based "set tilt, observe" co-headline. Use a paired rig-day design with ≥30 goals per model. | revise |
| C03 | Novel Expert | 3 | 2 | Humans also learn blended ("information-integration") categories slowly; many do not reach 80% within a few hundred trials (category-learning literature, not re-verified here), so trials-to-80% risks a floor for both sides. Training a classifier in the tools-on track trivialises the task. | Calibrate each space so the median human reaches 80% by about 150 trials. Headline transfer accuracy. | revise |
| C04 | Earworm | 2 | 4 | MUSE shows large gaps: expert meter identification 73.3% vs Gemini Pro 46.7%, with chance at 50% ([arXiv 2510.19055](https://arxiv.org/abs/2510.19055) [search extract]; 2025 models). But specialist models already solve beat tracking and synthetic audio is cheap, so one targeted data run could close (a)–(c). Tap-along (d) measures streaming latency. | Take (d) out of the headline or give it a latency-controlled track. Re-test on current audio-native models before building. | revise |
| C05 | Stump Arena | 4 | 3 | Items qualify because a panel failed them at pass@3, so solve rates regress upward on re-test even with no progress (a winner's curse; §2.11). The author-minutes metric depends on the author pool. | Report the gap against a fresh re-test of the qualifying panel. Stratify authors. Headline the cost-to-stump trend with CIs. | keep |
| C06 | Alien Physics | 3 | 4 | The IntPhys 2 gap (96.4 vs 57.5) is on Jun 2025 models (A §2.15). The coordinates-as-text ablation will probably show that inferring the law is easy for LLMs, which leaves a perception gap that closes with tracker training. | Headline the pixel-minus-text delta and the prediction-error slope. Use ≥100 puzzles per model. | keep |
| C07 | Tacit Signals | 3 | 2 | With about 120 pairings, the minimum detectable effect (MDE) on dyad success is about 10–12 pp (assumed SD 0.25–0.30; `probes/p5`). An AI sender using a legible systematic code could be learned fast by humans, closing the gap. | ≥200 dyads per arm. Model rounds-to-80% with hazard models. Use the AI–AI control as an upper bound. | revise |
| C08 | Glyph Pact | 2 | 3 | The gap evidence is current: human–AI pairs fail to converge ([2602.08208](https://arxiv.org/abs/2602.08208)), and MLLMs reach "coordination without convention" through verbose descriptions ([2606.08081](https://arxiv.org/abs/2606.08081)) [search extracts]. But the efficiency term can be trained or prompted away. | Headline partner-specificity (round-7 reset). Add a "be concise" instructed arm to expose the knob. | revise |
| C09 | First-Run Arcade | 3 | 5 | The human–AI gap is huge (VideoGameBench 0.48%; A §2.17). But frontier real-time scores will sit at the floor, so models barely separate from each other and the gap is mostly latency. The paused track looks like ARC-AGI-3 and could close in months. | Make the paused track a co-headline. Pick games where the frontier's paused score is 5–40% of the human score. | keep |
| C10 | Two Clocks | 1 | 2 | The BYOH track allows a fast controller plus a slow reasoner, which gives an AI system about zero dual-task cost by construction, so it "beats" humans. In the frozen harness, single-task control is near zero, so the ratio is undefined or noise. | none (fold into C09 as a real-time track) | kill |
| C11 | Wayfinder | 3 | 4 | Map-then-reason scaffolds and text notes can build allocentric maps without code (A §2.13; the ARC-AGI-3 notes harness). VSI-Bench nearly closed after spatial fine-tuning (A §2.12). The gap is still large today (MindTopo 97.9 vs 61.4 for GPT-5.6 Sol, secondary; A §2.20). | Run a notes-cap sweep and publish the scaffold delta. Hold out architecture grammars. | keep |
| C12 | Cartographer & Scout | 3 | 3 | 100 human–model dyads per model cost money and weeks for every new model. The symbolic-grid ablation will probably put the failure in perception, which duplicates C11 with more noise. | Headline a model–model track with a frozen, human-calibrated partner. Keep human dyads for audits. | revise |
| C13 | Deep Seasons | 3 | 3 | Learning Slope is a difference score over 8 campaigns, so its MDE is about 0.14–0.21 normalised units (assumed SD 0.10–0.15). Notebook tricks move it the way the harness moved ARC-AGI-3. | ≥24 campaigns per model. Headline final competence plus Mechanic Fidelity; report the slope as secondary. | revise |
| C14 | Kelly Exam | 3 | 4 | The spread is real: AA-Omniscience hallucination rates run 48–88%, and an always-abstain model would rank 4th of 36 (B §3.7). But abstention is a post-training knob, and a frozen-panel house line leaks general capability (§2.4). | Re-anchor q each release. Report log-wealth net of accuracy. | keep |
| C15 | Prospective Self-Forecast | 3 | 2 | Self-knowledge beyond base rates is probably small and swamped by 3-attempt Bernoulli noise. The frozen panel's p̄ rewards "I beat the old panel", which is capability. Probe: the reviewer model solved 12/12 but forecast a mean of 0.84. | Adaptive twin items near each model's 50% region, ≥1,000 of them. Report resolution separately from calibration. | revise |
| C16 | Pushback Ledger | 2 | 4 | The spread is wide today: GPT-5 flips 88.4% of correct answers vs 68.4% of incorrect ones ([2606.16011](https://arxiv.org/abs/2606.16011) [search extract]). But on verifiable items a strong model re-derives the answer, so discrimination tends to 1 as capability rises, and sycophancy is an active training target. | Add items that cannot be verified within budget. Report as a policy axis with its half-life. | revise |
| C17 | Reliability Horizon | 3 | 5 | 2025 models already spanned 120–2,176 steps ([2509.09677](https://arxiv.org/abs/2509.09677) [search extract]), so the 4,096 cap will soon bind. Random procedures can be degenerate (probe P1). The code track saturates immediately. | Uncapped staircase with a fixed token budget. Non-degeneracy filters. Report L80/L95 with cluster-bootstrap CIs. | keep |
| C18 | Compaction Chronicle | 4 | 4 | If query families are predictable, models learn to keep running ledgers and the task turns into bookkeeping. The human arm uses a different 200k-token version. | Keep information content above the notes cap. Rotate query types. Match the human arm on a sub-stream. | keep |
| C19 | Frozen-Student Tutor | 3 | 3 | Small students' capacity caps the gains, so frontier teachers converge on the student ceiling. Lessons can overfit to the pinned students. StudentBench found 0 of 364 significant learning cells (B §2). | A secret rotating student. Normalise by the oracle-lesson gain. | revise |
| C20 | Misconception Clinic | 3 | 2 | Repair − 2·Harm on about 100+100 items per stochastic fine-tuned learner, over a few domains, gives wide CIs. The oracle-note gate leaves little headroom. | ≥40 learner–domain cells per model. Deterministic decoding. | revise |
| C21 | Simulated Futures Exchange | 4 | 5 | Scoring against the rollout distribution removes nearly all outcome noise. The risk is that code-capable models identify the simulator families and approach the ceiling of 1. | Rotate mechanism families. Add knobs for data volume and intervention budget. | keep |
| C22 | Long-Tail Futures | 4 | 3 | Items are always fresh, but frontier skill differences are small next to realised-outcome noise. ForecastBench had 17 submissions above superforecasters on its preliminary board by 16 Jul 2026, a contested claim ([LessWrong summary](https://www.lesswrong.com/posts/a82q6yd8zKpYk56cF/ai-forecasting-in-2026-what-11-analyses-say) [search extract]). | SEs clustered by source. Long accumulation windows. | revise |
| C23 | Hunch Lab | 4 | 2 | Ground truth from 3–5 seeds is noisy (seed SD 5–15 pp; G §3). Items are costly, so n stays small. ML researchers may match models, so the A2 direction is unproven. | ≥20 seeds for noisy families. ≥500 items per season. Pilot the human comparison. | revise |
| C24 | MDL Arena | 4 | 4 | Generic learners written in the DSL (variable-order Markov or HMM models) may capture most of the bits, compressing the differences. 20 datasets carry dataset-level variance. | ≥60 datasets. Bits above L_ref with CIs. Report sandbox compute. | keep |
| C25 | Mechanism Lab | 3 | 3 | The score depends on a stochastic red-team optimiser and on population draws. Few scenarios. Risk of proxying code and econ knowledge. | Fixed red-team seeds with common random numbers. ≥30 scenarios. | revise |
| C26 | Contractor's Auction | 3 | 3 | Profit is heavy-tailed (ruin, damages) and driven by delivery, so it is mostly a proxy for coding and general capability. 3 replicate markets. | Headline the calibration decomposition. ≥10 markets. | revise |
| C27 | Signal Pit | 3 | 4 | Common-random-number pairing against Bayes-optimal is low-noise, but the code track saturates (a Bayes calculator is short), and a ratio above 100% rewards exploiting fixed bots. | Headline no-tools. Report the exploit component separately. | keep |
| C28 | Hidden-Dynamics Economy | 4 | 3 | Runs like Vending-Bench overlap for ranks 3–7 with ±$2k bands (B §3.2). 2,000–4,000 calls make seeds costly. Human versions are shortened. | ≥10 antithetic seed pairs. V/V* with CIs. | revise |
| C29 | Whodunit Engine | 2 | 3 | Consistent scripted NPCs make each case a closed constraint puzzle, which RL can learn once the family is known (Logic-RL reached 0.99; design principles §3). | Headline question efficiency. Add unreliable witnesses. | revise |
| C30 | Masquerade | 3 | 3 | Seat, role and anchor-pool variance dominate win rates, and the human arm gets 4 games per person. | Headline per-day detection bits over duplicate tables, ≥200 games per model. | revise |
| C31 | Debate Court | 3 | 2 | Stronger debaters raise weak-judge accuracy only marginally ([Kenton et al. 2024](https://arxiv.org/abs/2407.04622) [search extract]), so Truth Advantage compresses at the judge's ceiling. Novice judges add variance. | Headline frozen model judges. Report DWR as risk. | revise |
| C32 | Nomic Engine | 2 | 3 | Probe accuracy with 10 dry runs amounts to formal execution in a closed world that can be rendered as text. | Headline the loophole ledger. Limit dry runs. | revise |
| C33 | Exploitability Gauntlet | 4 | 4 | Exact exploitability has no outcome noise. But the Open track falls to CFR immediately, and textbook heuristics get most of the way. Probe P3: the reviewer model's no-code NashConv was 0.15, vs 1.00 for uniform play and 0.003 for CFR. | Closed-track headline. Sample information sets and check stated against played policy. | keep |
| C34 | Setter's Duel | 3 | 3 | Hardness saturates once setters routinely beat the top rung, and generate-and-filter with a self-written solver becomes a matter of search budget. | Extend the ladder yearly. Normalise by setter budget. | revise |
| C35 | Game Designer's Duel | 3 | 2 | MCTS "depth" is gameable: big branching factors win every budget doubling. Design has n = 3 games per model. | Normalise depth by branching factor. ≥15 games. | revise |
| C36 | Season Forge | 2 | 4 | The headline (percentile among human entrants) is already at ceiling: OpenAI "completely demolished" 12 finalists at AtCoder WTF 2026 Heuristic ([the-decoder](https://the-decoder.com/openais-ai-beats-every-human-at-atcoder-a-top-competitive-programming-contest/) [search extract]). | Headline anchored Bradley-Terry vs a raised bot ladder. ≥5 attempts. | revise |
| C37 | Saboteur's Patch | 3 | 4 | Auditing 300 diffs is well powered, but the frozen saboteur ladder will be outgrown, and the score likely proxies coding ability. | Refresh the saboteur ladder. Report the residual against a coding index. | keep |
| C38 | Relay | 3 | 2 | One chain is one noisy trajectory, and the Generational Gain ratio has a noisy denominator. Chains are few and costly. | Headline Note Transfer. ≥20 lite chains per model. | revise |
| C39 | Blind Spot Cartographer | 2 | 3 | Selecting on panel failure manufactures the gap, and adversarially filtered pools decay fast (HLE: 3.07% for GPT-4o at launch to 67.7% for Opus 5.5 with tools; B §3.4, E Q2). | Re-test acceptance before scoring. Headline authoring precision. | revise |
| C40 | Rules Gauntlet | 2 | 3 | Blind inference from legal-move lists is a closed world that can be rendered as text (ARC-AGI-3's collapse path), and simulator plus MCTS wins the Open track (D §2.25). An 8-game match gives about ±240 Elo. | Pool ≥480 games per model. Use the rulebook track as a control for general capability. | revise |
| C41 | Practice Week | 3 | 1 | One game per season. The gain is a difference of two 60-game ratings (95% CI about ±125 Elo; `probes/p5`). | none | kill |
| C42 | Hidden-Rule Lab | 3 | 3 | Probe P2: the reviewer model solved the text track 20/20 using 13 of 25 experiments, so the A1 gap rests on the image track (ZendoWorld 73.3% vs 44.5%; F §2). | Headline adversarial mode on images. Depth-3 rules. | revise |
| C43 | Eleusis Masters | 2 | 3 | Same solver weakness as C42: small rule spaces are enumerable ("a search, not a guess"; F §2). The setter score is noisy. | Merge into C42 as its setter role. | revise |
| C44 | Convention Cross-Play | 3 | 3 | Hanabi-like deal variance is high, Adaptation Gain is a difference score, and the human ratio needs many pairs. | Duplicate deals and ≥100 matches per partner type. Headline Cross-Play Score. | revise |
| C45 | Crowd Oracle | 2 | 2 | Payoff is bounded by the modal choice, and LLMs already share human focal points (LessWrong Schelling experiment [search extract]). Frontier models will cluster at the ceiling. | Score a log score against the human histogram instead of a single pick. | revise |
| C46 | Grift | 3 | 1 | 8-seat live chats yield few outcomes per season at $15–20k, and seat and personality effects swamp model differences. | none (run as a conduct red-team exercise) | kill |
| C47 | Defuse Line | 2 | 3 | Paused play is manual lookup that can be rendered as text, where frontier models already excel. Live play mostly adds latency. | Headline the frozen-AI-operator track. | revise |

---

## 2. Detailed attacks on 12 candidates

### Probe summary (informal, single model: the reviewer model, Claude Opus 5.5)

| Probe | Candidate | Setup | Code used by solver? | Result |
|---|---|---|---|---|
| P1 | C17 | 2 random invented register machines with hidden answers; 5 queried lengths (12/30/60 and 20/40 steps) | No (code only to generate and check) | 5/5 exact. Instance 1 was degenerate: a 4-step cycle made L trivially compressible |
| P2 | C42 text/JSON track | 1 hidden rule from a 7-template × 4-attribute grammar, budget 25 experiments | No | Rule identified in 13 experiments. 20/20 on label-balanced probes |
| P3 | C33 | 1 random Kuhn-family game (5 cards, ante 1, bet 2); stated policy for both seats | No (code only for exact exploitability and CFR) | NashConv 0.15–0.16 antes per hand. Uniform play 1.00; CFR 0.003 |
| P4 | C15/C14 | 12 random exact-answer tasks (up to 5×5-digit products, 4×4 determinant, 7×7 lattice paths with forbidden cells) | No | 12/12 correct. Mean forecast 0.84 (underconfident). Brier 0.033; log score −0.178 |
| P5 | stats | Power and L95-precision simulations (assumed SDs, stated) | n/a | See C07, C13, C17, C40, C41 |

### 2.1 C17 Reliability Horizon (keep)

**Q2.** The construct is sound, but the ceiling is close.
- On simpler key–value execution, 2025 thinking models spanned 120 (Gemini 2.5 Pro) to 2,176 steps (GPT-5 "Horizon") in a single turn ([2509.09677](https://arxiv.org/abs/2509.09677) [search extract]). That is an 18× spread, and the models are two generations behind the Sep 2026 frontier.
- The 4,096-step cap is therefore likely to bind within about 12–18 months [speculation]. At about 30 tokens per step, 4,096 steps is about 120k output tokens, which is feasible for 2026 models.
- The code track saturates on day one, since a simulator is a few lines.

**Probe P1.**
- Two instances, solved exactly by mental execution: 3/3 lengths on instance 1 and 2/2 on instance 2 (40 explicit steps).
- The first randomly generated machine fell into a 4-step loop, because R3 stayed even, which locks out 3 of 7 lines. Its 60-step answer was a closed form.
- In the second, R0 and R4 were constant and one opcode never appeared.
- An unfiltered generator therefore lets "L steps" be compressed into far fewer, and L95 inflates.
- Fix: reject instances with state cycles shorter than L, constant registers or unreached lines. The patched generator (`probes/p1_reliability_gen.py --nondegenerate`) does this.

**Q3.** Strong.
- An 18× spread on a log scale is large, and humans with a scratchpad will be orders of magnitude shorter [speculation, but a safe one], so the A2 direction is secure.
- Simulation (`probes/p5`): with 50 procedures × 12 lengths × 5 samples, a procedure random effect of SD 1 logit and a slope of 1.2 logits per doubling, the cluster-bootstrap 95% CI for L50 spans ×1.33. For L95 it spans ×1.52, and L95 sits about 6× below L50.
- So a 2× difference resolves.
- Caveat: the adaptive staircase concentrates trials near L50, so L95 is extrapolated through the logistic's tail. METR's p80/p50 ratio of 4–10× varies across models (E Q1), so the slope differs by model. Place some trials near each model's L95.

**Proxy for general capability?** Partly. L tracks reasoning budget, so fix the token caps and publish L per 1k tokens.

### 2.2 C42 Hidden-Rule Lab, with C43 (revise)

**Probe P2 (text/JSON track).**
- The hidden rule was "every yellow block touches a block of size ≥ 3" (vacuously true if there is no yellow block).
- Single-block scenes eliminated 5 of the 7 templates within 8 queries. Two targeted contrasts separated "touches something taller", "touches a cylinder" and "touches size 3".
- Three confirmations followed: 13 of 25 experiments in total, then 20/20 on probes.
- The log is in `probes/p2_query_log.txt`.

**What this means.** At this grammar depth, the text track is at ceiling for at least one frontier model, which matches F §2 (Metta's Eleusis: "a search, not a guess"). The "median human reaches 90% within 30 experiments" gate means the rules are human-easy, so at depth 1–2 both sides are at ceiling and the text track cannot carry an A1 claim.

**What remains A1.**
- The image track: ZendoWorld 73.3% vs 44.5%, but with only 19 humans and VLM agents of unnamed vintage (Jul 2026; F §2).
- The efficiency gap: the blicket study found accuracy near human with less efficient exploration (E Q1).
- ARC-AGI-3 shows the efficiency bar also fell once mechanics were understood (A §2.3). Q2 is 3 for images and 1 for text.

**Q3.**
- The adversarial mode is the strongest element: experiments to reach 95% worst-case accuracy against an adversary that keeps the consistent set alive. That is bounded below by information theory and does not reward lucky early guesses.
- Per-rule variance is large, so use ≥100 rules per model, reported against the ideal Bayesian reasoner.

**C43.** C43 adds a setter role whose discrimination score depends on the solver panel. Merge it into C42.

### 2.3 C33 Exploitability Gauntlet (keep)

**Probe P3.**
- Game: 5-card Kuhn variant, ante 1, bet 2.
- Without code, I reasoned from textbook heuristics (bluff:value 1:2, minimum defence frequency 50%) and committed a policy.
- Exact NashConv was 0.15 antes per hand for the first-pass policy and 0.16 after "refinement", against 1.00 for uniform play and 0.003 for 20k-iteration CFR (`probes/p3_result.txt`).
- The refinement did not help. The missed structure was that P1 should sometimes check its best hand, and P2 should mix calls with middle cards (CFR: call 3 at 0.42 and 4 at 0.46).

**What this means.**
- (a) Textbook heuristics get about 85% of the way from random to equilibrium, so the discriminating region is the last 15%. That needs games whose structure defeats heuristics: asymmetric bets, multiple streets, card removal.
- (b) The Open track is saturated by construction, since CFR is about 60 lines, so it can only be a control.
- (c) Public poker variants and a public practice grammar invite RL on the family. Keep the grammar's mechanics secret, as the spec says.

**Q3.** This is the cleanest metric in the set.
- Exploitability is exact and does not depend on sampled outcomes, so the only noise is the model's sampling of its own policy, and differences are paired across models.
- The expected spread is wide [speculation, from the probe plus the "no model close to optimal" pattern in FalsifyBench-like discovery tasks; F §2].

**Q2: 4.** The information-set knob (200–5,000) keeps headroom, provided policy elicitation stays affordable. Sample information sets, and check stated against played policy.

**Proxy for general capability?** Likely less so than most, because calibrated mixing is a distinct skill [speculation; untested per E Q3].

### 2.4 C15 Prospective Self-Forecast (revise), with C14 Kelly Exam (keep)

**Probe P4.**
- I forecast my own success on 12 random exact-answer tasks, then solved them mentally.
- Hits were 12/12, with a mean forecast of 0.84.
- Log score was −0.178 per item; at the 0.98 clamp it would have been −0.020. In this sample, all of the loss came from **underconfidence on items at my ceiling**.

**Attack 1: base rates leak general capability.**
- C15 scores Self-Edge against p̄, the success rate of a *frozen* panel on the twin item.
- As models pass the panel, "my q is above p̄" is correct simply because the model is stronger, so Self-Edge rises with general capability, not self-knowledge.
- C14 has the same leak: q is a frozen panel's accuracy, and a stronger model beats it on knowledge alone.

**Attack 2: most twins sit far from the model's 50% region.** For them, the score rewards confidence (my probe) or abstention policy rather than resolution. With 3 attempts per twin, the per-item outcome is a coarse Bernoulli.

**Q3 for C15.**
- Evidence that models know their own success beyond item difficulty is thin (E Q2 found no primary cross-lab data).
- Self-Edge differences among frontier models are plausibly under 0.02 nats per item, and 500 items cannot resolve that [speculation].

**C14 is stronger.**
- The spread is documented and splits by lab: hallucination 48–88% (E Q2), and always-abstaining would rank 4th of 36 (B §3.7).
- 2,000 items × 3 samples with a paired bootstrap gives high power.
- Q2 risk: abstention is a policy that can change in one release (P11: "the leader changed within about 6 months").

**Fixes.**
- Re-anchor q or p̄ each release to the *current* model pool.
- Report log-wealth net of accuracy.
- For C15, generate twins adaptively near each model's 50% point and report resolution separately from calibration.

### 2.5 C16 Pushback Ledger (revise)

**Q3 today is good.**
- "Who Flips?" finds GPT-5 flipping 88.4% of correct answers vs 68.4% of incorrect ones under counterarguments, with Gemini most resistant and Claude "succumbing to even mild pushback" ([2606.16011](https://arxiv.org/abs/2606.16011); ACL 2026 HEAL workshop [search extracts]).
- lechmazur's sycophancy board shows abstention from 4.7% to 83.9% (B §3.5).
- 1,000 items × 3 samples with frozen challengers is well powered.

**Q2 attack: the construct converges on capability.**
- The items are *verifiable*; the spec's own example is a lattice-path count.
- A model that can re-derive the answer can check the challenge: it rejects the off-by-one "proof" and accepts the valid correction. So P(switch | valid) → 1 and P(switch | fallacious) → 0 as capability rises, and discrimination → 1.
- In P4 I solved a 7×7 lattice path with 3 forbidden cells without code. Every example item of this kind is within frontier reach.
- What remains is policy (deference to authority), which labs actively train against. A reordering half-life of about 6 months is likely [speculation, by analogy to abstention; P11].

**Human side.** Humans facing fabricated citations and authority claims probably switch often. A2 holds, but that is not the binding constraint.

**Fix.**
- Add items that cannot be verified within the budget: long computations under a token cap, and questions that turn on sources.
- Report discrimination stratified by whether the model could verify the item (its solo accuracy on a twin).
- Publish it as a policy axis with its date.

### 2.6 C21 Simulated Futures Exchange (keep), with C22 Long-Tail Futures (revise)

**C21 Q3: strongest in the set.** Truth is the distribution from 10,000 rollouts, so CRPS and log score are computed against the distribution, not one realised draw. Scoring noise collapses to the model's own sampling, and 1,000 forecasts paired across models resolve small differences. The AutoML anchor gives a meaningful zero-skill reference for code-capable entrants.

**C21 Q2 attack.**
- With a sandbox, 10k rows and 20 interventions, a strong model can fit mechanistic models. On simple families it could reach 0.8–0.9 of achievable skill within a year [speculation].
- Headroom depends on the knobs: hidden thresholds, delays, heavy tails, less data, and interventional questions far from the data.
- Proxy for general capability? Probably partly, through data-science skill. The calibration component may reorder models (the forecasting/calibration lead in E Q2 is unverified).

**C22.**
- Realised outcomes bring irreducible noise, and sources cluster, since pageviews and downloads move together.
- ForecastBench: superforecasters led by 0.017 Brier in Jan 2026, "about one year of LLM progress". By 16 Jul 2026, 17 submissions ranked above superforecasters on the preliminary board, though the official board and Good Judgment dispute parity ([LessWrong summary](https://www.lesswrong.com/posts/a82q6yd8zKpYk56cF/ai-forecasting-in-2026-what-11-analyses-say) [search extract]).
- Frontier-model differences are fractions of that 0.017, so separating neighbours needs many weeks of accumulation.
- It never saturates for lack of items, but the spread compresses toward the noise floor. A2 against laypeople is near-certain.

### 2.7 C24 MDL Arena (keep)

**Q2: good.** The metric is uncapped (it can go below 0), anchored to the owner's generator, and uses a secret DSL.

**Attack 1: the scale can be distorted.** L_generic is LZMA, PPM or context mixing. A model that writes a *generic* adaptive learner in the DSL (a variable-order Markov model with learned contexts, or an HMM) may beat L_generic by a wide margin without finding any structure. That would compress everyone into the 0.2–0.5 band, and differences would hinge on the last few percent [speculation].
- Fix: add an "owner-written generic learner in the DSL" anchor as the zero point, so the score measures structure found beyond generic learning.

**Attack 2: variance.** 20 datasets per run carry large dataset-level variance. Use ≥60, and report bits above L_ref with paired CIs.

**Attack 3: compute confound.** Sandbox search budgets confound results, so report compute.

**Humans.** 30 programmers on a subset is too thin for A2 claims per family, but A2 direction is probably fine.

### 2.8 C01 Kinetic, with C04 Earworm (revise)

**The gap is real today.**
- ActPLD reports "consistently low performance" on point-light displays, with MLLMs reading walkers as "constellations or rotating lines" ([2509.23517](https://arxiv.org/abs/2509.23517) [search extract; 2025 models]).
- MMSI-Video is 96.4 vs 38.0 (Gemini 3 Pro; A §2.14).
- MindTopo is 97.9 vs 61.4 (GPT-5.6 Sol, Sep 2026; secondary; A §2.20).
- Q3 is 4.

**Q2 attack: plumbing.** "Single frames are noise" at 30–60 fps makes the input channel the bottleneck.
- Hosted video endpoints commonly subsample frames. From memory, about 1 fps by default for at least one major API; I did not verify this here.
- A frozen harness that passes 60 frames as an image list, or a provider that raises its sampling rate, could remove much of the gap overnight.
- This is ARC-AGI-3's harness lesson (62.7% vs 98.6%; A §2.3) and ClockBench's targeted-training lesson (13% → 67% in 12 months; A §2.9). The original IntPhys was saturated by V-JEPA at 98.3% (A §2.15).
- In the tools-on track, frame differencing plus clustering segments a motion-defined letter in a few lines of NumPy. That makes it a fine control but proves the headline rests on a no-code rule.

**Fix.**
- Make the headline the *delta* between native-rate input and frame-list input.
- Add carriers that low-level motion energy cannot decode: second-order motion, and semantic biological-motion judgements such as intent or weight lifted.
- Publish a "script-solvable" flag per carrier.

**C04.** MUSE finds experts at 73.3% vs Gemini Pro at 46.67% on meter identification, with Qwen2.5-Omni and Audio Flamingo 3 near chance ([2510.19055](https://arxiv.org/abs/2510.19055) [search extract]).
- These are 2025 models, and beat and meter tracking is a mature problem for specialist models, so the gap should close fast once targeted.
- Tap-along (d) measures streaming latency.
- Human non-musicians judging transpositions in a novel non-12-tone scale may be near chance, a floor risk [speculation]. Pilot this before committing.

### 2.9 C09 First-Run Arcade (keep), with C10 Two Clocks (kill)

**C09 Q3 (humans vs AI): 5.** VideoGameBench's best was 0.48% in real time and 1.6% paused (A §2.17; 2025).

**C09 separation among models.** At 10 Hz without pausing, every frontier LLM in a frozen harness will probably sit near 0% of the human first-run score. The benchmark then shows a huge human gap and no ranking of models.
- G §4: "0% pass@100 is most often a signal of a broken task".
- P20: aim for a 5–40% launch window.

**C09 Q2 attack.**
- The real-time gap is mostly latency, and the BYOH track invites fast small policies or code-as-policy.
- The *paused* gap is the cognitive part, and it is moving: Sonnet 5.5 beat Pokémon Red from screenshots alone (D §2.10, 28 Sep 2026), and turn-based ARC-AGI-3 fell in about 5 months.
- Fix: make the paused track a co-headline, select games at 5–40% frontier paused performance, and add a latency-matched human arm (humans playing at the model's effective frame rate).

**C10 (kill).** Dual-task cost is a ratio of the dual-task score to the single-task score.
- In the frozen harness, a frontier LLM's single-task corridor control at 10 Hz is near zero, so the ratio is noise.
- In BYOH, a fast controller in parallel with a slow reasoner has about zero interference by construction, so AI "beats" humans on a quantity that measures architecture, not cognition.
- There is no fix inside this framing. The corridor belongs in C09 as a real-time track.

### 2.10 C08 Glyph Pact, with C07 Tacit Signals (revise)

**Evidence for the gap is recent and specific.**
- Jones et al. (2026): humans and LLMs each form conventions in same-type dyads, but "heterogenous human–AI pairs fail" ([2602.08208](https://arxiv.org/abs/2602.08208)).
- A Jun 2026 study: MLLM agents achieve "coordination without convention", verbose from round 1 and not partner-specific ([2606.08081](https://arxiv.org/abs/2606.08081)).
- Both are search extracts; the model lists were not verified. So Q3 on the efficiency metric could be 4 today.

**Q2 attack.**
- The efficiency term (round-6 words ÷ round-1 words) is a style knob.
- Per a search extract of arXiv 2508.06482, convention formation "can be elicited" when training rewards both success and message cost. One post-training cycle, or even the instruction "shorten references once your partner succeeds", could close most of it.
- Partner-specificity (the round-7 reset) is harder to fake. Make it the headline.

**Power.**
- With 150 human–model dyads per model, the MDE is about 8–10 pp on dyad accuracy (`probes/p5`, assumed SD 0.25–0.30).
- Gating efficiency on ≥90% accuracy creates informative missingness, which biases the ratio.
- Every new model needs fresh humans, which caps the cadence.

**C07.** The same power problem applies with 120 pairings. A non-verbal channel may let an AI impose a legible systematic code that humans learn in a few rounds [speculation].

### 2.11 C39 Blind Spot Cartographer (revise), with C05 Stump Arena (keep)

**Attack 1: a winner's curse built into the acceptance rule.**
- Items are accepted when a panel fails them at pass@3.
- Illustration (uniform prior on each item's true solve probability p): accepted items have mean p = 0.2. The *same* panel re-run at pass@1 would therefore solve about 20% of "stumpers" at once.
- "Later models' solve rate" and "gap half-life" thus include regression to the mean, not just progress.

**Attack 2: the human gate is loose.**
- The human-easy gate (≥3 of 5 naive verifiers) passes an item whose true human solve rate is 0.5 half the time, and one at 0.4 about 32% of the time. "Humans solve it easily" is only loosely certified.

**Attack 3: adversarially filtered pools decay.**
- HLE, filtered against frontier models, went from GPT-4o at 3.07% (B §3.4) to Opus 5.5 at 67.7% with tools (vendor-reported; E Q2) in about 20 months. Q2 for the item pool is 2.

**Fix.**
- Before admitting an item, re-test the panel with fresh samples and require 0/k at larger k.
- Report the decay curve against a matched control pool.

**C05.** C05's *cost to stump* (median author-minutes, uncapped) is the most durable readout in either design, because it trends up as models improve and never saturates. Hence keep, with author-pool stratification.

### 2.12 C36 Season Forge (revise)

**Q2 attack: the headline is at ceiling on day one.**
- "Percentile among that season's human entrants" is already saturated for frontier systems.
- OpenAI's model placed 2nd at AtCoder WTF 2025 Heuristic. At the 2026 event it "completely demolished" the 12 human finalists, and organisers awarded "humanity surrenders" prizes ([the-decoder](https://the-decoder.com/openais-ai-beats-every-human-at-atcoder-a-top-competitive-programming-contest/); [officechai](https://officechai.com/ai/openai-completely-demolishes-human-competitors-at-atcoder-2026-after-placing-2nd-last-year/) [search extracts]).
- Contest veterans who are not world finalists will be beaten by wider margins [speculation].
- The operator's "strong bot, built with 10× the time" may itself be outscored, leaving no top anchor.

**Q3 is good in principle.** Bots are programs, so thousands of games per pair are cheap, and tournament CIs can be made tight. The dominant variance is between *development attempts*, and 3 attempts per model is too few to separate neighbours.

**Fix.**
- Headline an anchored Bradley-Terry rating against a ladder that grows each season with the best bots of earlier seasons.
- Use ≥5 attempts per model.
- Keep the human percentile as secondary context.

---

## 3. Survivors and fatal flaws

### Top 10 survivors on this lens (Q2 + Q3; all need the fixes above)

1. **C21 Simulated Futures Exchange** (4/5). Scoring against the true distribution removes outcome noise, and it has a mechanism-family renewal knob.
2. **C17 Reliability Horizon** (3/5). A log-scale spread of about 18× even among 2025 models. Needs an uncapped staircase and non-degenerate instances (probe P1).
3. **C33 Exploitability Gauntlet** (4/4). An exact, noise-free metric with an information-set knob. Probe P3 shows headroom beyond textbook heuristics in the Closed track.
4. **C24 MDL Arena** (4/4). An uncapped bits metric. Needs a generic-learner anchor and ≥60 datasets.
5. **C18 Compaction Chronicle** (4/4). A notes cap below the information content bounds the score by design, with no harness escape.
6. **C09 First-Run Arcade** (3/5, A1). The largest human–AI gap here. Needs the paused co-headline and 5–40% game selection to rank models.
7. **C14 Kelly Exam** (3/4). A documented lab-reordering axis with high power. Re-anchor house lines.
8. **C11 Wayfinder** (3/4, A1). A large, current spatial gap (MindTopo, MMSI-Video) and an enforceable closed protocol.
9. **C37 Saboteur's Patch** (3/4). A well-powered auditor log score with execution-checked witnesses. Refresh the saboteur ladder.
10. **C27 Signal Pit** (3/4). CRN-paired P&L against Bayes-optimal. Headline no-tools.

Just outside: C06 Alien Physics (3/4, stale physics evidence) and C05 Stump Arena (the cost-to-stump metric).

### The 10 most fatal flaws across the set

1. **Latency and plumbing presented as cognition** (C01, C02, C04 (d), C09 real-time, C10, C47 live). A harness or API change can erase the gap, as it did on ARC-AGI-3 (62.7% → 98.6%, same model). C10's BYOH gives AI zero dual-task cost by construction.
2. **A1 evidence is stale.** IntPhys 2 (Jun 2025), MUSE (Oct 2025), ActPLD (Sep 2025), VideoGameBench (May 2025) and AutumnBench (Oct 2025) predate Opus 5.5 and GPT-6 Astra. Targeted training closed ClockBench in about 12 months and the original IntPhys entirely. Re-baseline before building.
3. **Closed worlds rendered as text are solved on sight or with RL** (C29, C32, C40, the C42/C43 text track, C47 paused, the C17 code track). Probe P2 solved the C42 text track 20/20 in 13 experiments. Logic-RL reached 0.99 and Bulls-and-Cows fell in 9.5 weeks.
4. **Selection-manufactured gaps** (C05, C39). Pass@3-failure acceptance produces regression to the mean: under a uniform prior, about 20% of stumpers are solvable by the same panel at pass@1. A 3/5 human gate passes items whose true human solve rate is 0.5 half the time.
5. **Difference scores and ratios as headlines** (C13 slope, C41 gain, C44 adaptation, C38 generational gain, C10 dual-task cost, the C08 efficiency ratio). Their reliability collapses. C41's gain has a 95% CI of about ±125 Elo on a single game per season.
6. **Human-partner dyads without the power to rank models** (C07, C08, C12, C44, C46, C47). MDEs are about 8–12 pp at 100–150 dyads, and every new model needs fresh human recruitment, which breaks cadence and comparability.
7. **Bounded metrics near their ceiling** (C36's human-percentile headline after AtCoder 2026; C45's modal-choice payoff; C16's discrimination → 1 on verifiable items; C22's skill compressing toward outcome noise).
8. **Frozen-panel reference lines leak general capability** (C14's house line q, C15's p̄, the C34 and C37 frozen ladders). As models improve, beating the old panel rewards strength, not the named trait.
9. **Constructs that are post-training policy knobs** (C14 and C15 abstention, C16 sycophancy, C08 verbosity). They reorder models today but can flip in one release. Report them as dated policy axes, not durable capabilities.
10. **Degenerate or enumerable procedural instances** (probe P1: a 4-step cycle and constant registers; the 68-rule Eleusis catalogue; small C42 grammars). Without non-degeneracy and non-enumerability filters, "hard" instances are compressible, and scores overstate the construct.

**Proxy for the general factor (P14), for the record [speculation].** These are likely to correlate highly with a general-capability index: C17, C18, C24, C26, C29, C32, C37 and the C40 rulebook track. These are more likely to reorder models informatively: C14 and C15 (policy), C27 and C33 (probabilistic and game-theoretic play), C28 (long-horizon coherence), C30, C44 and C45 (social), and C01, C04, C09 and C11 (perception, where labs differ 3.5× on BabyVision; E Q2). Each release's validity report should test this rather than assume it.
