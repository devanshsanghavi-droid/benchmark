# Build a duplicate shop league where every model must learn the same secret shop from rich and poor starts

*Recommendation note, 11 Oct 2026. Evidence base: the 10 Oct design report, 12 fact-checked dossiers (D01–D12), the 402-variable catalogue, a sweep of about 85 benchmarks and studies, nine candidate directions, and a three-way novelty check of every candidate facet. No shop simulation has been run yet; every number comes from sources or arithmetic.*

## Answer first

Build a **duplicate shop league** on the kiosk (vending route) the design report already plans. Every model runs the same seeded worlds ("boards"), each from a rich and a poor starting position ("seats"). Each world hides its own cause and effect: what a price rise, a better slot, an earlier restock or a new sign really does, and one to three of six levers do nothing at all. The agent must find out by running affordable tests on noisy sales that hide sold-out demand, and it is scored on what it **earned** (value added over the par for its seat) and what it **learned** (its stated beliefs checked against the simulator's exact truth).

Core facets, in the way Vending-Bench is "long-running agents + realistic scenarios":

1. **Secret worlds you must learn:** hidden lever effects, including real zeros.
2. **Beliefs scored against exact truth:** lost profit split into "believed the wrong thing" and "knew but did not act".
3. **Sales are not demand:** sold-out and confounded data the agent must see through.
4. **Same world, unequal seats:** identical worlds from rich and poor starts, scored against par for the seat.
5. **Code decides every number:** not novel, but necessary.

The pitch [design]: *Vending-Bench asks whether an agent can keep a shop running. This asks whether it can work out how its shop actually works, from whatever position it starts in.*

## Independent and dependent variables

There are two views. **In the benchmark's experiment,** the AI model is the subject; the main independent variable (what we change on purpose) is "who runs the shop", and dependent variables are what we measure. **From the agent's own view,** its levers (prices, orders, hours) are its independent variables and its sales and cash its dependent variables: it is experimenting on its own shop. The recommended direction scores whether it recovers that map. A *world tape* is every outside random event drawn in advance from a seed, so all models meet the same world.

| Role | What it means | Who sets it | Can the agent see it? | Examples |
|---|---|---|---|---|
| Treatment (independent) | What we change to compare | Designer, per run | No | Which model runs the shop. Ablations only: context size, effort tier |
| Scenario factors (independent, like bridge boards) | Dials defining the test worlds | Designer, per scenario | Only through consequences (cash, lease, equipment) | Seat: cash runway 1–12 months, traffic ×0.5–2, debt. Route, rent, trap on/off. **Ours: hidden lever effects, including zeros** |
| Controlled | Held identical so differences belong to the model | Maintainer, frozen config | Rules yes; seed no | ≈45 tools costing 5 or 25 sim-minutes (field tasks cost their task time); 30k-token context; effort tier; horizon in sim-days; voice model; scoring rules |
| Agent decisions (levers) | Choices made through tools; outputs of the model, not inputs | The agent (or a script or human on the same seed) | Settings yes; true effect no | Prices, orders, delivery checks, slots, hours, refunds, the tests it runs |
| Outside randomness | Events nobody controls in the run | Seeded draws from calibrated priors | Some forecast, some after, some never | Weather, passers-by, supplier honesty, breakdowns, attackers |
| Hidden state (mediators) | The world's memory, carrying past decisions forward | Fixed update rules | Partly: cash yes; remembered prices, true stock no | Customers' remembered prices, regulars, stock by dated lot, equipment wear |
| Outcomes (dependent) | What we measure and score | Defined in advance; computed after | Sales and cash yes; score, lost demand, conduct flags no | Value added over par, ruin, waste, stockouts, conduct, cost. **Ours: belief skill, superstition rate** |

**Example causal chains** ([design] mechanisms from the design report):

- **Cold spell.** Temperature [outside] → hot/cold demand mix [hidden slope] → order mix [lever] → stock by lot [hidden state] → waste or stockouts [outcome].
- **Permanent discount.** Price [lever] → today's sales [hidden elasticity] → customers' remembered price falls [hidden state] → fewer buy at full price next month → 12-week profit [outcome].
- **Walking vs shopping route.** Route [scenario] → 7–9 am peak [outside] → best seller gone by 10:00 [hidden state] → lost customers the agent never sees [outcome, verifier only] → regulars drift away.
- **Cash cliff.** Rent and fixed fees [seat] + few regulars [hidden state] → bills due together [calendar] → agent cuts costs or borrows [levers] → survival or ruin [outcome].
- **Superstition (ours).** Sign lever with true effect zero [designed hidden factor] → agent changes the sign in a warm week [lever plus confound] → weather lifts sales → agent believes "the sign works" [belief, probed] → buys more signs [lever] → superstition counted, money lost [outcomes].

**What to vary and what to hold fixed:**

- **Vary:** the model; the world seed; the seat; hidden effect sizes (including zeros); a trap card against a no-trap twin. Harness settings change only in a separate ablation.
- **Hold fixed:** tools and minute costs, context, effort tier, horizon, counterpart rules and voice model, token prices, scoring rules and references, simulator version.
- **Record, never treat as a cause:** the agent's levers. "Models that priced higher earned more" is not causal, because skill drives both; to test a lever, force it in a scripted twin.
- **Label roles per experiment:** starting cash is a scenario factor when swept, a control when fixed, and hidden state once the run starts.

## What exists already

| Benchmark (owner, year) | Core facets in one line |
|---|---|
| Vending-Bench 1 and 2 (Andon, 2025) | One machine; long horizon; LLM suppliers that can be jailbroken; end cash only (VB2; VB1 also counted stock at cost); compute charged in-world (VB2) |
| Vending-Bench Arena (Andon) | 3–5 agents share a site; cartels reported in prose, not scored |
| Project Vend, Andon Market and Café | Real shops and customers (hired staff at the store and café); no score; n = 1 per site (Vend 2 ran several sites) |
| ProsusAI vending-bench (2026) | Seeded six-machine route; tools cost sim-minutes; scripted reference; cash headline |
| E-Commerce Bench (Qwen, 2026) | Code sets prices, LLMs only voice; 26% scam suppliers; seven metrics |
| YC-Bench (Collinear, 2026) | Deterministic startup year; hidden employee skills; adversarial clients |
| CEO-Bench (Princeton, 2026) | 500 days of compounding effects; rule-based reference and upper bound |
| RetailBench, MerchantBench (2026) | 180–365-day retail with hidden or late-arriving outcomes; oracle or 3-person human baseline |
| CoffeeBench (Sakana, 2026) | Coffee supply chain; fixed LLM reference firms; "idle drift" |
| STOCKTAKE (QpiAI, 2026) | Hidden regime changes; detection lag; same-information oracle; knowing-doing gap |
| InventoryBench (2026) | Inventory instances; human–AI teams; LLMs "falsely identify demand shifts" in noise |
| Supply_Chain_Bench | Beer game; score = reference cost ÷ agent cost, paired by seed and week |
| CausalGame (ICML 2026) | Agents design experiments with hidden confounders; games, not business |

**Facet coverage** (✓ has it, ~ partly, · no, ? unknown):

| Facet | VB2 | Arena | Prosus | E-Com | YC | CEO | Retail | STOCK-TAKE | Causal-Game | Ours |
|---|---|---|---|---|---|---|---|---|---|---|
| Long horizon (months) | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ? | ~ |
| Code sets every number | · | · | ✓ | ✓ | ✓ | ~ | ? | ✓ | ? | ✓ |
| Adversarial counterparts | ✓ | ✓ | ~ | ✓ | ✓ | · | ? | · | · | ~ |
| Several agents in one market | · | ✓ | · | · | · | · | · | · | · | · |
| Hidden state to infer | ~ | ~ | ~ | ~ | ✓ | · | ✓ | ✓ | ✓ | ✓ |
| Agent's beliefs scored against truth | · | · | · | · | · | · | · | ~ | ~ | ✓ |
| Null levers; false discoveries scored | · | · | ~ | · | · | · | · | · | ? | ✓ |
| Unseen (sold-out) demand scored | · | · | · | · | · | · | ~ | · | · | ✓ |
| Same-world pairing in the headline | · | · | ~ | ~ | ~ | ~ | · | ~ | ? | ✓ |
| Rotated unequal starts, scored vs par | · | · | · | · | · | · | · | · | · | ✓ |
| Validated against real results | · | · | · | · | · | · | · | · | · | · (v2) |

The gap sits in the bottom half: many benchmarks hide state, but almost none score what the agent *believes* about it, plant do-nothing levers or rotate unequal starts. Prosus's ~ is real: its marketing text has exactly zero effect, but nothing scores whether the agent notices (D02 fact-check row 14) [P code]. Supply_Chain_Bench already pairs by seed [P], so pairing alone is not new.

## The recommended direction

**Facet 1: Secret worlds you must learn.**
- *Meaning:* each world draws its own effect for six levers: two prices, slot position, restock time, hot/cold mix and a sign. One to three are exactly zero. Some effects are learnable in 60 sim-days, some only with a well-designed test, some not at all; for those, "can't tell yet" is right.
- *Why it matters:* no owner is handed a demand curve, and the real coffee machine changed prices about 3 times a year [D]. A 10% effect on a 10-unit/day item needs about 155–220 days per arm to detect (D02) [design calc], so honest uncertainty is part of the skill.
- *Novelty:* **new to business-agent benchmarks; borrowed from experiment-design benchmarks and p-hacking studies.**
- *Closest prior art:* CausalGame (best of 29–30 agents, depending on paper version, 68.0% survival against 78–85% optima; whether its games include do-nothing factors is unchecked) [S]; BoxingGym [S]; phack, which plants true-zero effects to catch false discoveries [S]; InventoryBench saw false shift detection but did not score it [S].

**Facet 2: Beliefs scored against exact truth.**
- *Meaning:* at hidden checkpoints the scorer copies the agent's context into a throwaway side call and asks for low/middle/high (10/50/90%) answers, such as "weekly sales of item 3 at €2.40 if it never sold out". The simulator knows the exact expected value. A *proper scoring rule* (the best strategy is to report what you really believe; here a CRPS-style quantile score) gives skill from 0 (no better than the public prior) to 1 (exact). A scripted experimenter with the agent's information splits lost profit into *learning regret* (believed the wrong thing) and *acting regret* (knew, did not act).
- *Why it matters:* money alone cannot tell a lucky guess from a correct inference: the "cheap path" the earlier report found kills benchmarks. Only a simulator knows the true effect, so real deployments cannot measure this.
- *Novelty:* **new to business-agent benchmarks; borrowed from belief-elicitation and knowing-doing research.** Claim only: causal and lost-demand questions, in side calls, priced in dollars, in a running shop.
- *Closest prior art:* a NeurIPS 2026 paper splitting estimation from execution error in a pricing game [S]; Schmied et al. on the knowing-doing gap [S]; STOCKTAKE, read from text [S]; mid-game belief scoring (arXiv 2608.24691, 2606.17383) [S].

**Facet 3: Sales are not demand.**
- *Meaning:* sold-out items hide lost customers, and weather and weekdays move sales while the agent changes things. With six machines at three sites, the agent can split a test across machines on the same day, cancelling shared daily noise, or compare before with after, which does not.
- *Why it matters:* naive vending demand estimates are biased even when stockouts are rare (Anupindi et al. 1998; Conlon & Mortimer 2013) [S]. For a 20% effect at 30 units/day, same-day splits need roughly half the days (about 13–16 vs 26–31 per arm) [our calc].
- *Novelty:* **scoring it is new to agent benchmarks; borrowed from operations research (censored demand) and experimental design.** The setting is not new: censored sales already appear in LLM inventory benchmarks (InvEvolve; InventoryBench's lost-sales instances) [S]. Scoring the agent's lost-demand estimates and test design was not found [S, one search per method].
- *Closest prior art:* RetailBench and STOCKTAKE (hidden state) [S]; InvEvolve (sales = min(demand, stock)) [S]; Prosus, which shows the agent its demand multipliers, removing confounds [P].

**Facet 4: Same world, unequal seats.**
- *Meaning:* each world is dealt as two seats, for example an established route (six machines, regulars, six months of cash) and a struggling takeover (two machines, high site commission, supplier debt, six weeks of cash). Every model plays every seat of every world. *Par* is what fixed scripted policies achieve from that seat.
- *Why it matters:* real businesses never get a fresh $500 start; Andon blames its store and café losses on "rent is high and they pay salaries" [P\*]. Position also changes learning: a two-machine seat cannot split tests, and a poor seat cannot afford many. Pairing saves runs: at 30% run-to-run variation, a 10% gap needs 141 unpaired runs per model but 28 at pairing correlation 0.8 (D11) [calc].
- *Novelty:* **new to LLM business benchmarks; borrowed from duplicate bridge, poker and business-school games.** Claim only "first business benchmark rotating the same agent through rich and poor starts, scored against par for the seat".
- *Closest prior art:* Buyout Game's mirrored rich/poor packs (a social game) [P]; Markstrat [P\*]; Bazaar's asymmetric rivals, SovSim's dominant player [S]; the team's "Duplicate CEO League" note.

**Facet 5: Code decides every number.** Code sets prices, floors and acceptances; language models only write words. **Not novel but necessary:** E-Commerce Bench, YC-Bench and Prosus do this, and VB2's suppliers show the alternative can be jailbroken [P\*].

**How it resists cheap scores.** Answering probes with the prior or wide ranges scores 0. Never testing is the floor policy; testing constantly costs margin and erodes remembered prices. Saying "no effect" to everything is caught, because misses are scored next to superstitions. Probes run at hidden times, include decoy levers, and voices never see hidden values (CI checks leaks). Private seasons shift priors 10–30% and add held-out mechanism families [design].

**How it uses the design report.** It *reuses* the seeded kernel, keyed world tape, forkable state store (trap twins now also compute probe truth), settled-equity value added, floor and oracle references, hidden lost sales, remembered prices, the Prosus fork, the hosted gateway and private seasons; the storefront-appeal prior ("mostly near zero") becomes the null-lever generator. It *changes* five things: (1) "never pin an uncalibrated parameter" becomes "draw it and score whether the agent learns it", turning the calibration weakness into the test; (2) belief probes and a Learned co-headline; (3) a same-information Bayesian experimenter beside the privileged oracle; (4) scoring per (world, seat) with par per seat and a variance gate; (5) the six-machine route moves forward from v2. Café, store, staff, arena and most of the 43 traps wait.

**Pilot plan** [design; costs at Opus 5.5 prices].

*Build first:* (1) fork Prosus v3 and key every random draw to its event; (2) the lever generator, with zeros and private mechanism families; (3) probes, three sets of eight per run, truth computed on CPU by forking; (4) references: a floor (never tests), a fair experimenter (same information, tests efficiently), an oracle (knows the truth); (5) two seats per world. About 20–30 engineer-weeks, or about 7–10 weeks for three people [design, rough].

*Step A, CPU only:* references on 8 worlds × 2 seats × 20 seeds. Gates: floor < experimenter < oracle on both scores; a good policy in the poor seat beats a bad one in the rich seat; the variance split (world, seat, policy, policy × seat) is published; the experimenter learns the learnable levers and says "can't tell" on the rest.

*Step B, LLMs:* 3 models × 8 worlds × 2 seats × 2 replicates = 96 runs of 60 sim-days. At about 12 calls per sim-day, $35–130 per run, ≈$3.3k–12.5k in total plus ≈$0.1–0.4k for probes [design calc]. Six machines may need more calls; measure first.

*It works if* (pre-registered): Learned separates at least two model tiers with non-overlapping cluster-bootstrap intervals; superstition rates differ between models; Learned and Earned correlate positively but well below 1 (else Learned adds nothing); the model, not the seat, explains a meaningful share of variance (else drop rotation, keep facets 1–3); no scripted cheap path beats the fair experimenter.

## Runner-up directions

**Real Twin (check the simulator against a real AI-run kiosk).** This fills the most important open gap: no business benchmark has shown its ranking predicts real results, and Andon says simulation "cannot accurately predict real-life performance" [P\*]. It would rebuild documented incidents, fork a real kiosk's state into the simulator weekly and pre-register forecasts. It lost because it is slow (one site, ten weeks), needs ethics review and real money, cannot test the rent and salaries that cost Andon most, and the method has precedents outside business (OpenAI's pre-registered deployment simulation; Nubank) [S]. It is the right **v2 validation layer**.

**Hold the Counter (moves for evidence, not pressure).** Every refund claim, discount plea and "owner's memo" becomes a trial with a known right answer, and twin runs vary evidence and pressure separately. It targets Project Vend's real losses (cajoled discounts, an imposter CEO, refunds tripling as discounts fell) [P]. It lost because the measurement is well covered outside business (BASIL, SycoBench-600, SycEval) [S], kiosk stakes are a few dollars per trial, and natural text with known evidence strength is hard to write. It stays as the People module and a season-2 track.

**Setups and teams (Manager Draft, Front Office League).** These carry the user's "setups not models" and "AI plus-minus" ideas: executor × advisor × effort grids, the token bill as the manager's wage, and per-role ratings across lineups. They lost because HAL already crosses models × scaffolds × benchmarks with cost and tests reasoning effort [S], Shapley ratings for mixed-model teams exist [S], and firm runs cost an estimated 2–3× solo runs [design estimate]. They enter **season 2** on the same worlds. Luck subtraction (AIVAT) and per-decision forking (CFR-X) become measurement tools, not identities [S].

## What not to claim as novel

- **Code sets numbers, LLMs voice them:** E-Commerce Bench, YC-Bench, Prosus.
- **Long horizon, realistic vending or retail:** Vending-Bench 1–2, MerchantBench, RetailBench.
- **Seeded worlds, paired comparison:** YC-Bench, CEO-Bench, Supply_Chain_Bench, Kaggle duplicate poker, Project Deal's parallel markets.
- **Reference or oracle normalisation:** CEO-Bench, Supply_Chain_Bench, STOCKTAKE, RetailBench.
- **Hidden state:** RetailBench, STOCKTAKE, EnterpriseArena, YC-Bench.
- **Knowing-doing gap; belief elicitation with proper scoring:** Schmied et al., STOCKTAKE, the NeurIPS 2026 pricing paper, arXiv 2606.17383 and 2608.24691.
- **Planting true-zero effects:** phack; causal-discovery environments.
- **Unequal positions in general:** Bazaar, SovSim, CoffeeBench, Buyout Game, Markstrat.
- **Conduct scoring, framing gaps, planted traps:** Business Arena, MerchantBench, ODCV-Bench; the "Safety Validity Gap" paper; STOCKTAKE's detection lag and Bazaar's ranking of adaptation after an unannounced shift.
- **Compute charged in-world:** Vending-Bench 2.
- **Names to avoid:** "CEO bench" (three exist), "PACT" (two), "Bazaar" (three), "LemonadeBench" (two).

## Risks and open questions

1. **Learnability versus realism.** At real kiosk volumes most 10% effects cannot be learned in a run; bigger effects buy measurability at the cost of realism. Publish and stress-test the effect-size priors.
2. **Prior art is close and mostly read through snippets.** Read CausalGame, the NeurIPS 2026 pricing paper, phack, RetailBench, arXiv 2608.14825 and AgentSC-Bench in full before claiming "first" [S].
3. **Stated beliefs and the simulator's truth are limits.** A model might act well without stating good numbers; claims concern learning this world, not real elasticities.
4. **Seats may not bind at kiosk scale,** where fixed costs are small. The CPU gate decides; the direction survives without rotation.
5. **Pairing may help less than hoped** if long runs drift apart [speculative until measured].
6. **Public generators become training environments within months,** so the mechanism grammar must stay private and rotate.
7. **Real-world validity stays unproven** until Real Twin runs.
8. **Open:** combine Learned and Earned into one headline? Disclose functional forms? How many null levers per world?

## Sources

*Local:* `research/reports/Business simulation benchmark design.md`; D01–D12 and `MASTER_VARIABLES_CATALOGUE.md` in `research/research_notes/Business sim deep dive/`; `TALKING_POINTS.md`, `R2_business_sim_orchestration.md` in `research/research_notes/Meeting 2026-10 ideas/`; `research/reports/Novel AI benchmark and game ideas.md`.

*Read directly or via verbatim copy:*
1. [P] Anthropic, Project Vend 1 and 2: https://www.anthropic.com/research/project-vend-1 ; https://www.anthropic.com/research/project-vend-2
2. [P\*] Vending-Bench 2 captures; Andon "Why we built Pion": https://github.com/aijnek/vending_bench ; https://github.com/kzinmr/ai-topics
3. [P] ProsusAI vending-bench: https://github.com/ProsusAI/vending-bench
4. [P] E-Commerce Bench: https://github.com/QwenLM/E-CommerceBench ; YC-Bench: https://github.com/collinear-ai/yc-bench
5. [P] Supply_Chain_Bench: https://github.com/ConstantinVictorBeatErtel/Supply_Chain_Bench ; Buyout Game: https://github.com/lechmazur/buyout_game
6. [P] Project Deal: https://www.anthropic.com/features/project-deal ; CoffeeBench: https://github.com/SakanaAI/CoffeeBench ; MerchantBench: https://github.com/KhanCold/merchantbench
7. [P\*] Markstrat handbook, quoted in R2. [D] Coffee vending log, analysed in D12

*Search snippets only (arXiv and most paper hosts were blocked):*
8. [S] CausalGame: https://arxiv.org/abs/2607.04293 ; BoxingGym: https://arxiv.org/abs/2501.01540 ; phack: https://pypi.org/project/phack/
9. [S] Reasoning-to-execution gap: https://neurips.cc/virtual/2026/172999 ; Schmied et al.: https://arxiv.org/abs/2504.16078 ; belief scoring: https://arxiv.org/abs/2608.24691 , https://arxiv.org/abs/2606.17383
10. [S] STOCKTAKE: https://arxiv.org/abs/2607.13618 ; RetailBench: https://arxiv.org/abs/2606.15862 ; MerchantBench: https://arxiv.org/abs/2607.28956 ; EnterpriseArena: https://arxiv.org/abs/2603.23638
11. [S] InventoryBench: https://arxiv.org/abs/2602.12631 ; InvEvolve: https://arxiv.org/abs/2605.00369 ; Bazaar: https://arxiv.org/abs/2608.00102 ; SovSim: https://arxiv.org/abs/2605.29062
12. [S] Anupindi et al. 1998: https://web-static.stern.nyu.edu/om/faculty/anupindi/estimate.html ; Conlon & Mortimer 2013: https://nber.org/system/files/working_papers/w14315/w14315.pdf
13. [S] HAL: https://arxiv.org/abs/2510.11977 ; Collaboration Tax: https://arxiv.org/abs/2608.22152 ; AIVAT: https://arxiv.org/abs/1612.06915 ; CFR-X: https://neurips.cc/virtual/2026/173087
14. [S] OpenAI deployment simulation: https://www.alphaxiv.org/abs/2607.07184 ; Nubank: https://arxiv.org/abs/2609.30137 ; SycoBench-600: https://aclanthology.org/2026.findings-acl.1759/ ; Safety Validity Gap: https://arxiv.org/abs/2606.23583 ; MIT/Andon misaligned emails: https://arxiv.org/abs/2608.14825

## Fact-check log

*11 Oct 2026.* An independent checker read the note in full. It checked **104 claims** against the 10 Oct design report, dossiers D01–D12 (corrected values), the variables catalogue README, R1/R2/TALKING_POINTS, the phase-1 games notes, the three-way novelty checks and the prior-art matrix. It also ran 9 web searches (search snippets only [S]; no proxy or mirror services). It made **16 corrections**, all as minimal in-place edits. Confirmed without change: about 45 tools and the 30k window; seat ranges (runway 1–12 months, D08; traffic ×0.5–2); 43 numbered trap families; the storefront prior "mostly near zero"; "never pin an uncalibrated rank-flipper"; multi-site kiosk in v2; 155–220 days per arm (D02 §1 item 10); about 3 price changes a year (D12); 141 vs 28 runs (D11 power table); per-run cost $35–130 (Opus 5.5 at $0.048–0.18 per call × 720 calls); 96 runs and the totals; probe cost; 402 variables (README; the catalogue header says approximately 407); Prosus null marketing text (D02 row 14) and visible multipliers (row 15); Anupindi's "even for items that have very few occurrences of stock-outs"; the Andon "rent is high" quote (D01, [P\*]); Project Vend facts (cajoled codes, imposter CEO, refunds tripled); Kaggle poker's 900k duplicate hands (local notes, [S]).

Key corrections:
1. **Facet 3 novelty was overstated.** Censored sales already appear in LLM inventory benchmarks (InvEvolve; InventoryBench lost-sales instances). The note now claims only the *scoring* (lost-demand estimates, test design) as new.
2. **Facet 3 arithmetic:** "12–16 vs 25–31" days became "13–16 vs 26–31". Recomputed with Poisson at 30/day plus a day SD of 0.18, at 80% power, for ln(1.2) or 0.2 effects. This matches the novelty check's 13 vs 26.
3. **Facet coverage table:** CausalGame's "null levers" cell went from · to ? (unchecked; causal-discovery environments contain null edges). STOCKTAKE's "pairing in headline" cell went from · to ~ (its skill score is normalised by a fair oracle on the same observations; confirmed by search [S]).
4. **HAL** crosses models × scaffolds × benchmarks with cost and reports reasoning-effort effects. It does not cross "model × scaffold × effort" as stated (ICLR 2026 abstract [S]).
5. **"Firm runs cost 2–3× solo runs"** has no local source; it is now tagged [design estimate].
6. **Vending-Bench row:** both are 2025 releases. End-cash-only scoring and the in-world compute charge are VB2 only; VB1 counted stock at cost (D01).
7. **Project Vend row:** Vend 2 ran several sites, so "one site each" became "n = 1 per site". The Hold the Counter losses are Project Vend's (Anthropic with Andon), not Andon's own.
8. **CausalGame agent count** varies by version: 30 on arXiv, 29 in PMLR, 16 in the ICLR submission [S]. It now reads "29–30".
9. **Bazaar** ranks adaptation after an unannounced shift; it does not measure detection lag (prior-art matrix).
10. **Smaller fixes:** field tasks cost their own task time (design report §Time). The Andon rent quote refers to store and café losses. 20–30 engineer-weeks for three people is 7–10 weeks, not 2–3 months. MerchantBench and RetailBench are retail, not vending. The proper-scoring citations now include arXiv 2606.17383 and 2608.24691.

Still unverified [S]: InventoryBench's "falsely identify demand shifts" quote (not found in snippets of the paper's abstract); Bazaar's name and Visa affiliation (the arXiv 2608.00102 snippet shows the title "Can LLM Agents Price Competitively?" only); phack's 33–97% false-positive range (author's PyPI claim). Searches used: CausalGame (proceedings.mlr.press/v306/chen26l.html; icml.cc/virtual/2026/poster/63530); STOCKTAKE (arxiv.org/pdf/2607.13618 snippet); HAL (proceedings.iclr.cc ICLR 2026 abstract); InventoryBench (arxiv.org/html/2602.12631v1 snippet); phack (pypi.org/project/phack/); the NeurIPS reasoning-to-execution paper (neurips.cc/virtual/2026/172999); Safety Validity Gap (huggingface.co/papers/2606.23583); Bazaar (arxiv.org/pdf/2608.00102 snippet); Kaggle Game Arena poker (search snippets).
