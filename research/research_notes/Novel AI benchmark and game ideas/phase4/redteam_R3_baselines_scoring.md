# Red team R3: human baselines (Q4) and scoring and cost (Q5)

As of 30 Sep 2026. This is an independent adversarial review of the 47 candidates in `../phase3/candidates_spec.md`. I did not read the ideation rationale or the `ideas_*.md` files. The lens is rubric §7 Q4 ("Can human baselines be measured fairly?") and Q5 ("Is scoring objective and cheap?") from `../phase2/design_principles.md`.

**Scales.** Scores use the §7 anchors.
- **Q4.** 1 = no baseline. 3 = tiny or mismatched. 5 = a large paid first-attempt panel on the same interface, with ≥2 solvers per item, the full distribution and a power analysis. ARC-AGI-2 (407 people) and ARC-AGI-3 (458) score about 4.
- **Q5.** 1 = a single-lab judge, or a cost like ARC-AGI-3's $17–50k per configuration. 3 = deterministic but noisy or costly. 5 = an exact verifier out of the agent's reach, with gates, bounded cost and a one-command run.
- **Verdicts** apply to this lens only. *Keep* means sound with minor fixes. *Revise* means a design change is needed before Q4 or Q5 reaches 3 or more. *Kill* means no fix preserves the construct.

**Cost basis [speculation].** Per-model costs use Anthropic list prices cached on 25 Sep 2026:
- Claude Opus 5.5: $4 in / $20 out per MTok (cache reads $0.20). Fast mode is $8 / $40 for up to 2.5× output speed.
- Claude Fable 5.1: $10 / $50.
- Claude Sonnet 5.5: $2 / $10.

Image tokens are estimated at w·h/750 (about 87 tokens for a 256 px frame and 350 for 512 px) [from vendor docs, not re-checked]. ⚠ marks runs likely to cost more than $1k per model. Many ideator estimates leave out thinking tokens. On text benchmarks with thousands of items, output and thinking tokens at $20–50/M dominate the bill.

**Human-cost basis.**
- Prolific's minimum is $8/h and its recommendation is $12/h or more ([Prolific](https://researcher-help.prolific.com/en/articles/445266-how-much-should-i-pay-participants)). A platform fee comes on top [fee size from secondary pricing pages, not verified].
- ARC-AGI-2 paid $115–150 per 90-minute session plus $5 per task, across 407 people (G §5). ARC-AGI-3 paid about $130 per session plus $5 per solve, across 458 people (A §2.3). At those rates a first-run panel of about 400 costs roughly $55–70k [speculation].

**Key external evidence (web, this review).**
- **Crowdworkers use LLMs.** 33–46% of MTurk workers used LLMs on a summarisation task ([Veselovsky et al. 2023](https://arxiv.org/abs/2306.07899)). The follow-up found about 30% prevalence. Asking workers not to, and blocking copy-paste, cut use from 27.6% to 15.9%, not to zero ([arXiv 2310.15683](https://arxiv.org/abs/2310.15683)).
- **Frontier latency.** Time to first token is about 0.7–1.4 s for non-reasoning modes and 28–67 s P50 for reasoning modes ([secondary survey](https://www.digitalapplied.com/blog/ai-model-latency-benchmarks-2026-ttft-throughput), L–M). A DOOM-control study reports that reasoning models exceed a real-time budget ([arXiv 2604.07385](https://arxiv.org/pdf/2604.07385), [S]).
- **Human–AI Hanabi.** With learned vs rule-based agents there was no significant score difference, but human preferences differed strongly ([Siu et al., NeurIPS 2021](https://arxiv.org/abs/2107.07630)).
- **The Convention Gap.** Humans rely on implicit conventions that AI pairs don't use: +26.2 pp in human pairs, −0.7 pp in AI pairs, +16.4 pp in human–AI pairs ([arXiv 2609.11489](https://arxiv.org/abs/2609.11489), Sep 2026).
- **Reference games.** Multimodal LLMs do not compress their descriptions over rounds without heavy prompting ([ICCA, arXiv 2408.01417](https://arxiv.org/abs/2408.01417)). Agents stay "verbose from round one" ([arXiv 2606.08081](https://arxiv.org/abs/2606.08081)).
- **Cicero.** It played 82 anonymous people on webDiplomacy.net under IRB approval, paying over $70 per 3-hour game, and "passed as human" ([arXiv 2406.04643](https://arxiv.org/pdf/2406.04643)).
- **ForecastBench.** The public baseline was 500 people plus 39 superforecasters ([arXiv 2409.19839](https://arxiv.org/abs/2409.19839)).
- **Debate.** Human judges reached 88% with debate vs 60% naive on QuALITY ([arXiv 2402.06782](https://arxiv.org/abs/2402.06782)).

**Dossier evidence used.**
- Median human baseline is 8 people, 2% ran a power analysis, 14% reported ethics review (G §5, Wei et al.).
- METR's pay scheme pushed baseliners to quit early (G §5).
- Resolving 3 pp takes about 969 items; clustered SEs run up to 3.05× naive ones (G §3).
- Swapping the judge moved one model from 3rd to 9th (G §4).
- 205 of 243 Arena models were silently deprecated (P2 §3 row 10).
- Vending-Bench 2 runs use 60–100M output tokens; one API provider gave 2× another's score (B §3.2, P2 P12).
- VideoGameBench scores 0.48% in real time vs 1.6% paused (A §2.17).

---

## 1. All 47 candidates

| ID | Name | Q4 | Q5 | Est. cost / model run [spec.] | Main attack | Fix | Verdict |
|---|---|---|---|---|---|---|---|
| C01 | Kinetic | 4 | 4 | $60–300 | Browser rendering drops frames at 60 fps, and monitors run at 60–144 Hz, so online motion thresholds drift. Vendors also ingest video differently (native sampled video vs image lists under per-request caps), so "native frame rate" has no model equivalent, and subsampling aliases the motion carriers. | One frames-as-images protocol for all (30 fps, ≤64 frames); log human dropped frames; a lab stratum (n≈30) to calibrate the online panel | keep |
| C02 | Live Rig | 2 | 1 | $1–3k ⚠ + $5–20k capex per rig | The denominator is the median human "on the same rig and day", so every model-day needs a fresh human panel, and a median of about 10 people is noisy. Rig wear, humidity and failed resets make runs irreproducible, and no third party can rerun them. | At most a showcase, with a simulated twin as headline | **kill** |
| C03 | Novel Expert | 3 | 4 | $150–1,200 (depends on caching) | 200 adults over about 10 spaces is about 20 per space, too few for trials-to-80% distributions. Uncached 400-trial transcripts cost about 28M tokens per space. The 50-word stated rule needs a judge. | ≥60 humans per space; windowed transcript; score the rule by a frozen reader's transfer accuracy, as a secondary score only | revise |
| C04 | Earworm | 3 | 3 | $20–150 (audio-capable models only) | Family (d), real-time tapping, needs a streaming-audio API most frontier models lack, so the frozen harness can't be vendor-neutral. Online keypress latency varies by device. (a)–(c) exclude every text-and-image-only model. | Drop (d), or run it offline with loopback-calibrated humans (REPP-style [from memory]); publish model coverage | revise |
| C05 | Stump Arena | 3 | 3 | $50–500; programme $15–30k per season | A 3-of-5 gate passes a coin-flip item 50% of the time and a 40%-solvable item 32%. Authors optimising for panel failure select ambiguity. About 30% of crowd verifiers may use LLMs. "Author-minutes" can't be measured, because prep happens offline. | ≥4/5 plus an independent re-gate; AI-use deterrents; drop cost-to-stump | revise |
| C06 | Alien Physics | 4 | 4 | $100–500 puzzles; ~$1k duels ⚠ | Per-law human n is thin: 200 adults across a seasonal grammar, so "relative to humans" per law is noisy. | IRT normalisation per law family; ≥40 humans per family | keep |
| C07 | Tacit Signals | 3 | 2 | ~$1k incl. humans ⚠ | The human partner is part of the instrument. Each model needs about 120 fresh pairings, partner skill dominates variance, and cohorts drift between model evaluations. "Fixed timers" penalise seconds-long reasoning latency. Blind partners require deception consent and debrief. | Merge into C44: scripted-convention bots as headline; a seasonal human–model arm with a concurrent human–human control | revise |
| C08 | Glyph Pact | 3 | 3 | ~$3k incl. 150 dyads ⚠ | The ratio of round-6 to round-1 words rewards padding round 1 up to the 25-word cap. Live dyads recur for every model. The matcher role doesn't need live humans. | Absolute round-6 words at ≥90% accuracy; matcher role on replayed human-director logs; director dyads seasonal | revise |
| C09 | First-Run Arcade | 4 | 2 | Real-time $0.1–1k; paused (120k decisions) $2–6k ⚠ | At 10 Hz, a 0.7–67 s time to first token means the score measures serving speed, region and load, and a lab can buy points with fast mode. "Latency-matched" humans is undefined. | A token clock (§2); wall-clock play as a side track | revise |
| C10 | Two Clocks | 4 | 1 | $500–3k ⚠ | A single model can't steer at 10 Hz, so solo corridor performance sits near the floor and the dual-task ratio divides by about 0. BYOH (a fast controller plus a slow reasoner) drives dual-task cost to about 0, so the score measures harness architecture. | None that keeps the construct | **kill** |
| C11 | Wayfinder | 4 | 4 | $300–1.5k | Online humans can sketch maps on paper, which can't be policed, while a model's reasoning text is already a map. "Tools-off parity" is therefore a fiction. Spatial ability varies widely with gaming history. | The same notes box for humans; a no-paper lab stratum (n≈40); stratify by gaming | keep |
| C12 | Cartographer & Scout | 3 | 3 | ~$1.5k incl. humans ⚠ | 100 human–model dyads per model, clustered by dyad, give a minimum detectable effect of about 15 pp between models [spec.]. Humans recur for every model, and runs are irreproducible. | Frozen-partner and symbolic-grid headline; human dyads seasonal with a human–human control | revise |
| C13 | Deep Seasons | 2 | 3 | $1–6k ⚠ | Humans can't be memory-capped: the 3,000-token notebook sits on top of full episodic memory. 4-hour sessions confound the learning slope with fatigue. | Compare humans with the full-log track; 2×2 h sessions; power the slope | revise |
| C14 | Kelly Exam | 3 | 5 | $150–800 (thinking tokens) | Pay proportional to final wealth makes the payoff linear in p, so a risk-neutral human bets 0.02 or 0.98. Kelly play is not elicited, which breaks the log-wealth headline. | Pay linear in log-wealth growth, with a floor; 1–2 tables per person | keep |
| C15 | Prospective Self-Forecast | 2 | 4 | $300–1,200 | Humans can't attempt a twin "in a fresh context" because they remember it. Agentic 10–40-call tasks make a human arm METR-scale in cost. The closed-model p̄ panel will be deprecated. | Human arm on non-agentic families with a single attempt; open-weight p̄ panel | keep |
| C16 | Pushback Ledger | 3 | 4 | $200–900 (ideator $15–80) | The branch depends on the model's own first answer, so P(switch \| valid) is estimated on each model's few, hardest wrong answers: strong models get tiny, biased cells. Fabricated citations deceive human participants. | Injected-first-answer arm with balanced cells; report cell n; debrief humans | keep |
| C17 | Reliability Horizon | 3 | 4 | $0.9–3k ⚠ | Tokens scale with L. Humans can't hand-run more than about 64–128 steps reliably in 90 minutes. "Fixed output caps" can't be enforced when thinking is always on and hidden. | Headline L ≤ 1,024; report billed thinking; IRT-adaptive staircase | keep |
| C18 | Compaction Chronicle | 2 | 5 | $300–1,000 | The human arm is infeasible. 200k tokens in 3 h is about 830 words per minute, against roughly 240 typical [from memory], so humans do a different task (skimming). | ~30k-token human version, or drop it (A2); oracle-note bot anchor | keep |
| C19 | Frozen-Student Tutor | 3 | 5 | $50–250 | Lessons can be tuned to small-model quirks, such as answer-format tricks, rather than content. T = 0 determinism needs a pinned inference stack. | Secret rotating student; the 300-human learner arm as external check; pin the engine | keep |
| C20 | Misconception Clinic | 3 | 4 | $30–300 + owner fine-tuning | Misconceptions planted in fine-tuned 1–8B learners can be unstable, and the fine-tuning pipeline must be rebuilt every quarter. Only 30 + 30 humans. | Pre-use stability check on each learner; publish gate results | keep |
| C21 | Simulated Futures Exchange | 3 | 5 | $100–500 | 60 humans across 20 simulators is about 3 per simulator. The no-code public stratum is a different task. | Pool the human reference by family; not a headline | keep |
| C22 | Long-Tail Futures | 3 | 4 | $20–200/week; $0.3–2.6k per season ⚠ | A late entrant can never be scored on past weeks, so comparisons need concurrent entry. API series get backfilled. Humans can cover only about 1% of items. | Difficulty-adjusted cross-week scoring (ForecastBench-style); frozen resolution-snapshot rules | keep |
| C23 | Hunch Lab | 3 | 4 | $50–300 + $5–20k owner compute per season | Truth taken from 3–5 seeds is itself noisy, so CRPS penalises correct forecasts. 40 ML researchers are costly. | ≥10 seeds on headline items; score against a fitted seed distribution | keep |
| C24 | MDL Arena | 2 | 3 | $100–1,000 | A free-form program that "defines a probability model" can emit unnormalised likelihoods. Normalisation can't be checked in general, so bits can be faked. 30 humans at 3 h per dataset is tiny. | Generative-only PPL whose interpreter scores declared random choices; canonical bit count from the AST | revise |
| C25 | Mechanism Lab | 2 | 4 | $100–500 incl. persona-agent compute | A fixed red-team optimiser invites mechanisms tuned to its blind spots. The oracle's quality sets the denominator. 40 experts is thin. | Private rotating red-team ensemble; report the oracle gap | keep |
| C26 | Contractor's Auction | 2 | 4 | $100–600 | The human–model comparison hinges on an arbitrary hours-to-credits rate ($75/h). Profit with ruin is heavy-tailed, so 3 replicate markets are underpowered. | Drop the human-delivery comparison; ≥10 markets; report the median and the ruin rate | keep |
| C27 | Signal Pit | 3 | 5 | $150–600 | P&L pay with a zero floor makes human incentives convex, so humans over-trade. The P&L ÷ Bayes-optimal ratio explodes where the optimum is near 0. | Bounded linear or tournament pay; aggregate before dividing | keep |
| C28 | Hidden-Dynamics Economy | 2 | 3 | (a) $0.75–2k ⚠; (b) $1.5–3k ⚠ | Human versions are truncated (150 days) or tiny (10 full-length runs). Long-horizon variance is large (Vending-Bench bands up to ±$2.1k; a 2× provider effect). | Shorter headline with more common-random-number seeds; humans as reference only | revise |
| C29 | Whodunit Engine | 4 | 5 | $150–600 | The natural-language → template parser is a hidden grader: humans and models fail it at different rates, and models learn parser-friendly phrasing. | Structured question builder for both; natural language as a separate track | keep |
| C30 | Masquerade | 3 | 3 | $1.5–2k ⚠ | A lone human at a 7-seat table otherwise filled with AI is not human play: pace, style and anchor reactions differ. At chat latency, 4 games take 2–4 h. Seat variance is large. | Human reference on the detection sub-score via replayed transcripts; cut the chat budget | revise |
| C31 | Debate Court | 3 | 3 | $50–300 model + ~$1k human judges ⚠ | Human judges cost about $5 per debate for each model, and they learn a model's tells across debates. A frozen weak judge is a static target that persuasion will overfit (a judge swap moved one model from 3rd to 9th, G §4). | Rotating private cross-family judge panel as headline; human judges seasonal, one debate per judge per model | revise |
| C32 | Nomic Engine | 3 | 4 | $0.5–1k | Humans get a GUI while models read the DSL, so probe accuracy compares different representations. Two hours to learn a 40-rule DSL invites fatigue. | The same text DSL for both, with the GUI as a viewer only; probes as a fixed item set | keep |
| C33 | Exploitability Gauntlet | 2 | 4 | $0.5–1k | Slider elicitation of up to about 600 probabilities measures elicitation, not play. With "sampled" information sets, exact exploitability is undefined without a completion rule. | Completion rule from played frequencies; compare humans on EV vs the exploit bots | keep |
| C34 | Setter's Duel | 3 | 4 | $200–600 incl. ladder solves | A frozen ladder of API models will be deprecated, which breaks hardness points. 3 stochastic attempts make hardness noisy. | Open-weight pinned ladder; seeded attempts | keep |
| C35 | Game Designer's Duel | 2 | 3 | $200–2k ⚠ + MCTS CPU | Depth measured by MCTS doubling rewards search-heavy or degenerate long games. The novelty gate needs a judge. Human designers need days per game, and n is 30. | Validate depth by human play on a subset; novelty as DSL distance only | revise |
| C36 | Season Forge | 3 | 3 | $1–3k per season ⚠; human prizes $20–50k | The headline is a percentile among that season's humans, which is pool-relative and shifts every season. Remote proctoring can't stop AI use. | Anchored Bradley-Terry headline; in-person or locked-VM humans | revise |
| C37 | Saboteur's Patch | 3 | 4 | $100–500 | Six minutes per diff in a 5–20k-line repo is not time-matched to the model. "Benign" refactors may accidentally break properties, which is label noise. | Matched time budgets; fuzz benign diffs before labelling | keep |
| C38 | Relay | 4 | 2 | $1.5–9k ⚠ (lite $0.3–1.8k) | Chains are sequential and autocorrelated, so effective n is the number of chains. Mixed chains need humans for every model. The gain ratio is unstable when oracle − gen 1 is small. | Lite track as headline with ≥30 chains; human chains seasonal | revise |
| C39 | Blind Spot Cartographer | 3 | 3 | $20–200 model + ~$4 per gated item | The same gate and crowd-AI attacks as C05. Gating at $12/h (5 × 3 min plus fee) is about $4 per item, not $1.5. ZDR on panel endpoints can't be verified. | Merge with C05; ≥4/5 plus re-gate | revise |
| C40 | Rules Gauntlet | 3 | 3 | Blind $1.5–3k ⚠; rulebook $100–600 | 250 humans over about 60 families is about 4 per family. A GUI board for humans vs a text move list for models breaks parity. | Fewer, IRT-chosen families per run; the same rendered board plus move list for both | revise |
| C41 | Practice Week | 2 | 3 | $0.5–3k ⚠ | Humans practise at home for 7 days, with unlimited memory, friends, engines and chatbots. One game per season makes the learning gain n = 1. | Proctored sessions; ≥3 games per season | revise |
| C42 | Hidden-Rule Lab | 4 | 5 | $50–1,000 | The scene-building interface differs (a drag-and-drop GUI vs JSON), so the experiment count partly measures interface fluency. | One structured command set, with a form builder that maps 1:1 | keep |
| C43 | Eleusis Masters | 3 | 3 | <$500 + a human panel per setter | Setter discrimination uses a model-and-human panel, so every model's rules need fresh human solvers. Public accepts and rejects let solvers free-ride on table-mates. | Duplicate tables with fixed anchor solvers; human panel seasonal | revise |
| C44 | Convention Cross-Play | 3 | 4 | $30–1.5k + ~$2k humans ⚠ | The Human-Team Ratio is noisy (Siu et al.) and recurs for every model. Blind-partner deception needs consent. | Held-out bot cross-play as headline; human ratio seasonal | keep |
| C45 | Crowd Oracle | 4 | 5 | <$100; panel $15–20k per season, shared | A panel paid for "picking" produces a different distribution than one paid for "coordinating". Prolific panellists are non-naive, and about 30% may use LLMs. A modal ceiling fitted on the same sample is biased. | Pay the panel for matching; split-half scoring; AI-use deterrents | keep |
| C46 | Grift | 2 | 1 | $1–3k API ⚠ + $15–20k humans per season | Every score depends on that week's human grifters and marks, so nothing reproduces. Real people become targets of AI manipulation, with money at stake and AI identities hidden, and the logs make a manipulation training set. | None on this lens | **kill** |
| C47 | Defuse Line | 3 | 2 | $0.5–1.5k incl. operators ⚠ | "Devices per hour" is wall-clock time, so reasoning latency over a 10–30-page manual sets the score. Operator variance dominates, and every model needs new operators. | Token clock; frozen AI operators as headline; human operators seasonal | revise |

**Tally:** kill 3 (C02, C10, C46) · revise 20 · keep 24. Kill here means only that the candidate fails on this lens.

---

## 2. Detailed attacks on 12 promising or contested candidates

### C09 First-Run Arcade (contested; strongest A1 game on paper)

- **Q4 panel.** 300 first-run adults at ≥60 per game is ARC-AGI-3 scale. It costs about $10–15k per season at $12/h plus bonus and fee [spec.]. That part is fine.
- **The interface is the fatal problem.** 10 Hz means 100 ms per decision. Time to first token is about 0.7–1.4 s without reasoning and 28–67 s P50 with it [Sec]. The model therefore acts on 1 frame in 10 to 1 frame in 600. The score becomes a function of decode speed, region, provider load and time of day.
  - The same model has already scored 2× differently through two API providers (Vending-Bench, P2 P12).
  - A lab can buy points outright: Opus 5.5 fast mode gives up to 2.5× the output speed for 2× the price.
  - "Latency-matched" humans would need 1–30 s of added lag, which destroys the human game.
  - VideoGameBench already shows real-time vs paused scores diverge: 0.48% vs 1.6% (A §2.17).
- **Q5.** The engine grades exactly, but reproducibility fails. The paused track is expensive: 120k decisions × about 5k context tokens is about 600M input tokens, roughly $2.4k uncached at Opus 5.5 list and $6k at Fable 5.1 [spec.].
- **Fix: a token clock.** The engine advances game time by a fixed Δ ms per billed output token (thinking included), plus a fixed overhead per call. It holds still otherwise.
  - The clock is deterministic and vendor-neutral, and it still penalises long deliberation.
  - Fast mode stops mattering.
  - Calibrate Δ so a terse policy can act at about human rate.
  - Humans play in real time.
  - Make the 10-game budget track the headline.

### C42 Hidden-Rule Lab (top survivor)

- **Q4.** This is the best-specified baseline in the set.
  - ≥300 first-run adults, plus a solvability gate (the median human reaches 90% within 30 experiments).
  - It matches AutumnBench (517 people) and ARC-AGI-3 (458), and far exceeds ZendoWorld's 19 (F §2).
  - Sessions of 10–15 minutes let each person do 3–4 rules with little fatigue.
  - Visual, interactive items resist crowdworker LLM use better than text does.
- **Attack 1: interface.** If humans drag blocks in a 3D GUI while models emit JSON, the experiment count partly measures interface fluency. The image-only track also asks the model to perceive its own scene; that is legitimate A1 content, but the ablation must be published.
- **Attack 2: the "ideal Bayesian" reference.** Depth-3 compositions of ≥200 primitives give roughly 10⁶–10⁷ rules [spec.]. That is tractable offline, but the prior over rules defines "ideal" and must be published and frozen, or the efficiency ratio is arbitrary.
- **Attack 3: rule fidelity.** A stated rule would need a judge. Score fidelity only through probes that separate intended from shortcut rules, which the spec already includes.
- **Q5 = 5.** Probe accuracy and experiment counts are exact. The adversarial mode is deterministic given the adversary. Cost is low.

### C45 Crowd Oracle (top survivor)

- **Q4 fairness.** Leave-one-out scoring against the panel is fair by construction, because the human population is the construct.
- **Load and cost.**
  - 300 responses per item from about 1,000 adults means about 180 items per person, with fatigue and within-session level-k learning.
  - 180k responses per season at about 20 s each is about 1,000 hours, roughly $16k at $12/h plus fee [spec.]. The $10–15k estimate is slightly low, and representative country strata cost more.
- **Attack 1: incentives.** Schelling items must pay panellists for matching other panellists. People asked to "pick" and people asked to "coordinate" choose differently (Mehta, Starmer & Sugden 1994 [from memory, not re-checked]). With a flat fee, models are scored against preferences, not focal points.
- **Attack 2: a contaminated population.** About 30% of crowdworkers used LLMs on text tasks, and deterrents only halved it (27.6% → 15.9%; arXiv 2310.15683). Every panellist who asks a chatbot pulls the "human distribution" toward the model's own, which rewards the model for being itself.
- **Attack 3: estimation.** The payoff and the modal ceiling are fitted on the same 300 responses, which biases them upward. Use split-half scoring.
- **Q5 = 5.** Scoring is exact against the frozen empirical distribution, a model run costs under $100, and the harness is trivial.

### C05 Stump Arena, with C39 Blind Spot Cartographer

- **The human gate is noisy.** Under a binomial model, "≥3 of 5 solve" passes items as follows:

  | True solve rate p | P(pass) |
  |---|---|
  | 0.4 | 32% |
  | 0.5 | 50% |
  | 0.6 | 68% |
  | 0.8 | 94% |

  With a uniform prior over p, accepted items average about 71% solvable (posterior mean over k = 3–5). Adversarial authors shift the pool toward hard or ambiguous items, so "ordinary people solve it quickly" is overstated.
- **Crowd AI use.** Crowd verifiers using AI make the gate partly an AI test, especially for text items.
- **Unmeasurable cost metric.** "Author-minutes" can't capture offline preparation.
- **Panel-dependent scoring.** Scoring is exact match, but items adversarially filtered against a panel penalise models whose errors correlate with panel members [interpretation]. Ranks then depend on who sits on the panel.
- **The frozen panel won't stay frozen.** Closed endpoints get deprecated (205 of 243 Arena models; P2 §3). Use open-weight models, or archive responses.
- **Cost.** At $12/h, 5 × 3 minutes plus fee is about $4 per item [spec.], so C39's $1.5 is 2–3× low.
- **Fix.**
  - A ≥4/5 gate plus an independent 5-person re-gate. A 50% item then passes both with probability 0.19², about 3.5%.
  - Publish each item's human solve rate with a CI.
  - Render items as images and block copy-paste.
  - Merge C05 and C39 into one pipeline with a human-author arm and a model-author arm.

### C13 Deep Seasons

- **The memory asymmetry can't be fixed.** A human's "3,000-token notebook" sits on top of full episodic memory of 10 runs. The A1 learning-slope gap therefore conflates the harness's state-carry protocol with learning. Harness effects are huge on interactive tasks: ARC-AGI-3 scored 62.7% vs 98.6% under two harnesses (P2 P18).
- **Fatigue.** About 4 hours for 10 runs puts runs 7–10 at peak fatigue, which biases the human slope down.
- **Power.** 120 humans across 8 campaigns and 2 strata is about 15 per cell. A slope is a difference of noisy means, and roguelike run variance is high: NetHack on BALROG was underpowered at 4–5 episodes (P2 §3).
- **Cost.** 32k turns × 15–30k context tokens is 0.5–1B input tokens: about $2–4k uncached, or about $0.3–0.6k with caching. Output adds $0.6–1.9k. Total $1–6k ⚠.
- **Fix.**
  - Compare humans with the model's full-log track; keep the notebook track as a model-only ablation.
  - Run humans in 2 × 2 h sessions on consecutive days.
  - Use 4 campaigns × 2 seeds, with a pre-registered power analysis for the slope.

### C14 Kelly Exam

- **The incentive flaw.** Given belief b, the expected multiplier is b·p/q + (1−b)(1−p)/(1−q), which is linear in p.
  - Under pay proportional to final wealth, a risk-neutral human should bet 0.98 when b > q and 0.02 otherwise. Only log utility gives p = b.
  - Compounding over 100 items also makes payouts extremely skewed, and a pay floor then rewards gambling. This is the same failure METR hit (G §5).
- **Fix.** Pay linear in mean log-wealth growth (the proper log score), with a floor, or use binarised lottery pay.
- **Load.** 2,000 items is impossible for one person, so each human does 1–2 tables. 250 people give about 300 tables, which is enough as a population reference.
- **Q5.** Short answers are exact after normalisation. The "NOT DETERMINABLE" trap labels need a pre-launch audit, because novel expert sets carry label errors (FrontierMath 42%; HLE 18–29% [uncertain]).
- **Cost.** 6,000 calls with thinking is roughly $150–800 [spec.], 3–5× the ideator figure.
- **Anchors.** House lines q depend on the anchor panel, so pin open-weight anchors.

### C17 Reliability Horizon

- **Cost is badly underestimated.** Tracing one register-machine step takes roughly 20–50 tokens: L = 512 needs 10–25k tokens and L = 2,048 needs 40–100k. 3,000 items clustered near a frontier threshold of L ≈ 500–1,000 means 45–150M output tokens. That is $0.9–3k at Opus 5.5 and $2.3–7.5k at Fable 5.1 [spec.], against an ideator estimate of $20–100.
- **Caps confound the headline.** Opus 5.5's thinking can't be disabled, so any cap must be on billed output. At long L the cap binds, so L95 partly measures the cap.
- **The human range is short.** At 10–20 s per step, a human manages about 300–500 steps in 90 minutes in total. Human L95 therefore exists only at L ≤ about 64–128 [spec.]. Say so; it is acceptable for an A2 benchmark.
- **Fix.** Headline L ≤ 1,024; treat the cap as a published knob with a curve; use an IRT-adaptive staircase over fewer lengths.

### C29 Whodunit Engine (top survivor)

- **Strengths.** NPCs are scripted and deterministic, the simulator is private, and scoring is exact (log score on the culprit, categorical method, time and motive). There is no LLM judge in the loop.
- **Attack: the parser is a hidden grader.**
  - Natural-language questions go through a parser to templates. Humans write natural, ambiguous questions, while models quickly learn the phrasing the parser accepts. Unless parse failures are refunded, parity breaks.
  - If the parser is an LLM, it is a judge with style bias (G §4).
  - Motive must be categorical for exact match to work.
- **Q4.** 150 public participants plus 30 enthusiasts, 3 cases × 45 minutes, and log-score pay. The pay is proper and the load feasible.
- **Cost.** 200 cases × 60 questions with growing context is $150–600, depending on caching.
- **Fix.** A structured question builder (who, where, when, what was seen) as the headline for both humans and models. Natural language becomes an ablation, and parse failures are refunded and logged.

### C38 Relay

- **Rare genuine parity.** A fresh human is exactly a memoryless successor. Paying people for both their own score and their successor's aligns incentives.
- **Logistics.** Ten-generation chains are sequential, so each chain takes days, and drop-outs break chains unless there is a replacement rule.
- **Statistics.** Outcomes are autocorrelated because one bad note poisons every descendant. Effective n is the number of chains: about 96 for 960 people, split across domains and mixed conditions, which leaves about 10–20 per cell.
- **Unstable ratio.** Generational Gain divides by oracle − gen 1, which is small in easy domains.
- **Cost.** $1.5–9k per model ⚠, and mixed human→model chains need humans for every model.
- **Fix.** Make the lite track the headline with ≥30 chains per model; run pure-human chains once per season as a reference; aggregate before taking the ratio.

### C44 Convention Cross-Play (keep; headline the bots)

- **Q5 is strong.** The Cross-Play Score against 8 held-out scripted bots with undisclosed conventions is exact, cheap, reproducible and duplicate-dealt.
- **But bot cross-play may not transfer to humans.** The Convention Gap paper shows humans rely on implicit conventions AI pairs lack: +26.2 pp in human pairs, −0.7 pp in AI pairs, +16.4 pp in human–AI pairs (Sep 2026).
- **The human component is noisy.** Siu et al. found no significant score difference between learned and rule-based Hanabi partners, while subjective ratings split sharply. The Human-Team Ratio therefore needs large n, and 200 people × 10 games per model recurs for every model.
- **Ethics.** Blind-partner identity is deception and needs IRB consent and a debrief. Cicero is the precedent: IRB-approved, with anonymous opponents and more than $70 per 3-hour game.
- **Fix.**
  - Fit or validate the bot panel against human–human logs.
  - Keep the human ratio seasonal, with a concurrent human–human control.

### C08 Glyph Pact

- **The A1 gap is plausible.** ICCA and Wang et al. (Jun 2026) find that models do not compress their descriptions spontaneously.
- **The metric is gameable.**
  - The ratio of round-6 to round-1 words rewards padding round 1 up to the 25-word cap. A model going 25 → 3 words scores 0.12, a human going 15 → 3 scores 0.20.
  - ICCA shows heavy-handed prompting can elicit compression, so the frozen harness prompt partly sets the score.
- **Humans are part of the instrument.** 150 live human–model dyads per model is about $2k+ and recurs for every model. Humans may also compress less with a partner they believe is a machine.
- **Fix.**
  - Score absolute round-6 words and rounds-to-convergence at ≥90% accuracy.
  - Run the matcher role on replayed human-director transcripts (the ICCA method) for cheap, reproducible scoring.
  - Run the director role against asynchronous human matchers, with live dyads seasonal.

### C01 Kinetic

- **Q4 is feasible.** Online psychophysics costs about 200 × $12–15 plus fee, around $3–4k per season [spec.], and staircase thresholds are standard.
- **Attack 1: human timing.** Browser 60 fps playback drops frames on unknown hardware. Refresh rates of 60, 120 or 144 Hz change effective durations, and coherence thresholds are sensitive to both.
- **Attack 2: model ingestion.** A 4 s clip at 60 fps is 240 frames, about 84k tokens at 512 px. Per-request image caps then force subsampling, and native-video APIs sample at low fps [from memory]. Different vendors see different stimuli, so the harness sets the score.
- **Fix.**
  - One image-sequence protocol for all: 30 fps, ≤64 frames, 256–384 px.
  - A native-video track kept separate.
  - A 2-frame control, alongside the single-frame control, to catch vendors that subsample.
  - Log human frame timing and exclude sessions with more than 5% dropped frames; add a lab stratum of about 30.

---

## 3. Top 10 survivors on this lens

Ranked by Q4 + Q5, then by how cheap the fix is.

| Rank | ID | Name | Q4 / Q5 | Why it survives |
|---|---|---|---|---|
| 1 | C42 | Hidden-Rule Lab | 4 / 5 | A ≥300-person first-run panel with a solvability gate; exact probes; deterministic adversarial mode; cheap |
| 2 | C45 | Crowd Oracle | 4 / 5 | The human population is the construct; exact scoring; under $100 per model. Needs panel incentives fixed |
| 3 | C29 | Whodunit Engine | 4 / 5 | Deterministic NPCs, no judge, feasible human cases; needs the structured-question fix |
| 4 | C01 | Kinetic | 4 / 4 | Standard psychophysics with a large panel and exact forced choice; needs a fixed frame protocol |
| 5 | C06 | Alien Physics | 4 / 4 | Turn-based, quantised input shared with humans; simulator-graded; a coordinates-as-text ablation |
| 6 | C11 | Wayfinder | 4 / 4 | Discrete moves, exact path metrics, 200 adults; needs the notes-box parity fix |
| 7 | C19 | Frozen-Student Tutor | 3 / 5 | 14,400 deterministic gradings; a 300-human learner validity arm |
| 8 | C14 | Kelly Exam | 3 / 5 | Exact and cheap, with a proper-score headline; needs human pay by log-wealth |
| 9 | C21 | Simulated Futures Exchange | 3 / 5 | Truth from 10k rollouts; proper scoring; an AutoML anchor |
| 10 | C27 | Signal Pit | 3 / 5 | Common-random-number pairing against a Bayes-optimal seat; exact P&L; a feasible 1-hour human session |

Near misses: C44 (headline the bots), C16, C34, C37 and C20.

---

## 4. The 10 most fatal flaws across the set

1. **Wall-clock real time measures serving infrastructure, not cognition.**
   - Affected: C09, C10, C47, C04(d), and the timers in C07.
   - With time to first token at 0.7–67 s against a 100 ms tick, scores track decode speed, region and load. They can be bought: fast mode gives 2.5× the speed at 2× the price.
   - Fix: a token clock. It is decisive for C10, where BYOH trivially dissolves the construct.

2. **Live humans inside the measuring instrument, recurring for every model.**
   - Affected: C07, C08, C12, C30, C31, C38, C43, C44, C46, C47.
   - Partner, judge and operator variance dominate. Cohorts drift between model evaluations. Nothing reproduces, and nothing runs as a one-command third-party evaluation.
   - Blind-partner and manipulation designs add IRB burden, and only 14% of published baselines report ethics review (G §5).
   - Fix: frozen partners as the headline; seasonal human arms with a concurrent human–human control.

3. **Crowd AI use contaminates "human" gates and panels.**
   - 33–46% of MTurk workers used LLMs; deterrents cut use from 27.6% to 15.9%, not to zero.
   - This hits C05, C39 and C45 hardest: the "human-easy" gate and the "human distribution" partly become model outputs.

4. **Noisy, adversarially fed human gates.**
   - A 3-of-5 gate passes 50% items half the time.
   - Author selection concentrates ambiguity (C05, C39).

5. **Pay that isn't incentive-compatible.**
   - C14's wealth-linear pay elicits corner bets, not Kelly bets.
   - C27's zero floor makes incentives convex.
   - C45's flat-paid panels answer "picking", not "coordinating".
   - These are METR-style incentive artefacts (G §5).

6. **Asymmetries that can't be equalised.**
   - Humans can't be memory-capped (C13, C41).
   - Humans can't attempt "in a fresh context" (C15).
   - Online humans can use paper and chatbots (C11, C36, C41).
   - Interfaces differ: GUI vs DSL or text (C32, C40, C42).

7. **Infeasible or truncated human workloads, which produce a different task.**
   - C18 needs about 830 words per minute.
   - C28 truncates to 150 days, with 10 full-length experts.
   - C37 allows 6 minutes per diff in a 5–20k-line repo.
   - C33 elicits about 600 sliders.
   - C13 runs 4-hour sessions.

8. **Costs underestimated because thinking tokens are ignored, and many runs cost more than $1k.**
   - C17 is about 10–100× the ideator estimate; C16 and C14 are 3–10×.
   - ⚠ runs: C02, C06 duels, C07–C10, C12, C13, C17, C22 (season), C28, C30, C31, C35, C36, C38, C40, C41, C44, C46, C47.
   - Output caps can't be enforced uniformly when thinking is always on.

9. **"Frozen" closed-model anchors, panels, ladders and judges will be deprecated.**
   - 205 of 243 Arena models were silently deprecated.
   - Affected: C05, C14 house lines, C15 p̄, C26 anchors, C30 anchors, C31 judge, C34 ladder, C39 panel.
   - Only pinned open-weight models, or archived response sets, keep scales fixed.

10. **Subjective or gameable parts hidden inside "objective" scores.**
    - Unnormalised likelihood programs (C24).
    - The NL→template parser (C29).
    - Padding round 1 (C08).
    - MCTS depth plus a judged novelty gate (C35).
    - Selection-biased switch cells (C16).
    - Ratios whose denominators approach zero (C10, C27, C38).
    - Stated-rule scoring that needs a judge (C03, C42).
