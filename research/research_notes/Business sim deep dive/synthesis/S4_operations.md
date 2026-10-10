## Supply, inventory and service operations

The simulator must run suppliers, deliveries, stock, recipes, queues and staff as a seeded, deterministic kernel, with LLMs only writing what counterparts say, because Vending-Bench 2's LLM suppliers "can be jailbroken to give away stuff for free" (D03 §1 [P\*]). Physical friction must be real: orders arrive late or short and must be counted in, stock sits in dated lots that spoil, café items can be made only if the equipment and ingredients exist, and customers who see a long queue leave without the agent ever seeing the lost sale. In the café and store, staff are a mechanism, not a cost line: Andon says both sites "lost a lot of money (rent is high and they pay salaries to the humans they hired)" (D04 §2.1 [P\*]), and their public failures were management failures. Most sub-problems have a known operations-research (OR) reference policy, so scores can be value added over a reference ladder rather than raw profit (D03 §4; D04 §4 [design]).

**Changes to the earlier chat answer.**
- **Staffing gets its own item.** It was folded into cash flow (item 8).
- **Queues hide lost sales too (item 3).** Customers who balk or renege never show up in the data.
- **Supply-side manipulation (item 7) is closed by design.** Persuasion changes wording, never price.
- **Andon Café's 24% pastry sell-through is not a calibration target (item 5).** The counts are press-only and D12's fact-check removed them (D12 §2.5).

**Tags and terms.** Tags follow the dossiers; [K] marks literature cited from background knowledge and not re-read (treat as [U]).
- *Lead time:* order-to-delivery days.
- *MOQ:* minimum order.
- *Newsvendor:* a one-shot order of expiring goods.
- *Critical ratio:* c_u/(c_u + c_o), the cost of a unit short over the cost of a unit short plus a unit left over.
- *(s,S):* at stock s, order up to S.
- *FEFO:* first-expiry-first-out.
- *Bullwhip:* orders swinging more than demand.
- *NHPP:* Poisson arrivals with a time-varying rate.
- *Balk / renege:* leave at sight of the queue / after waiting.

### 1. Suppliers

**The kernel.** Each supplier has a hidden persona: a markup over an honest `true_cost`, a price floor, a minimum order, a lead-time range, and delay, short-ship ("bait-and-switch"), ghosting and insolvency probabilities. Prosus's six-persona TOML file is the template (D03 §2.2 [P]).

**Negotiation.** The share of the list-to-floor gap conceded after n rounds is 1 − exp(−pace × n), so each round closes 26–53% of what remains and talk alone never reaches the floor. A volume bonus adds up to 22 points to that share, not 22% off the price (D03 §2.2 [P], corrected by fact-check).

**Prosus details not to copy.**
- Its "floor after 5 rounds" is dead code. Add an explicit round cap if a hard stop is wanted, and make quotes cost time [design].
- Its blurbs nearly name each type. Randomise them so types must be learned (D03 §4 [design]).
- Its delays are independent. Use one latent logistics-stress factor that scales all delay and short-ship rates (D08 §2.2 [design]).

**Realism and stress values differ.**
- Prosus's "flaky" insolvency hazard (0.0035/day, ≈72% a year) is far above real wholesaler exits. D03's fact-check suggests 0.00003–0.0003/day plus shock-driven exits (background knowledge; D03 §3 var 14).
- E-Commerce Bench's 26% fraudulent suppliers is an adversarial choice, not a prevalence (var 15).
- Drift of 2%/month is ≈27%/yr, so use 0–0.5% as the baseline (var 17 flag).
- Report a realism track and a stress track separately [design].

**Why suppliers separate models.**
- On E-Commerce Bench, spend routed to fraudsters ranged from 0.12% to 18.5% across models (D03 §1 [P]). Calling fraud "the most discriminating" variable is D03's inference.
- On repeat orders, 18 of 21 configurations paid significantly more than a reshuffle of their own past quotes: they anchored (D03 §2.5 [P]).

### 2. Receiving and physical labour

Vending-Bench 1's dominant failure was an agent "believing an order arrived prematurely" (D05 §2.1, verified verbatim; D01 §2.4 [P\*]), yet VB2 still auto-registers deliveries (D03 §1 [P\*]).
- **Dock state.** Deliveries land at a random hour; the agent counts, then accepts or disputes within a window [design] (D03 §2.8).
- **Who did the work.** Humans: Vend 1's prompt says Andon "charges ${ANDON_FEE} per hour for physical labor"; in Vend 2 humans were still "delivering the items and stacking the shelves" (D03 §2.8 [P]). Price it as minutes in an 8-hour day (Prosus) or a paid helper.
- **Delegate error.** The error rate is a placeholder. Butter-Bench measures LLM robot control and is not evidence for it (D03 §3 var 36 flag).

### 3. Inventory and perishables

**Lot ledger.** Keep it beside the money ledger and assert every step that purchases = sales + waste + shrink + on hand (D03 §4 [design]). Prosus issues depot batches oldest-first but re-dates older units on restock; do not copy that flaw (D03 §1 [P]).

**Issuing order.** At self-serve fridges customers take the freshest unit unless staff spend minutes rotating stock. This is a design prior with no source (D03 §2.6).

**Food safety.** The Food Code's 7-day date mark and 4-hour discard rule are US-only; Stockholm needs EU/Swedish values (D09 §2.3).

**Record drift.** About 65% of SKU-store records were wrong at one large retailer (DeHoratius & Raman; D03 §2.6, verified via a secondary copy), so book stock should drift unless the agent pays for counts.

**Shrink.** NRSS's 1.6% shrink [S] fits the shop. Café losses are mostly spoilage (D06 §3; D12 §2.4 flags).

**Biases to probe, not hard-code** (D03 §2.4–2.5).
- *Pull-to-centre:* under-ordering high-margin goods and over-ordering low-margin ones (Schweitzer & Cachon 2000 [K]).
- *Supply-line under-weighting:* stock on order gets about a third of its due weight (Sterman 1989) [uncertain: not re-read].
- *Bullwhip is not universal:* retail industries generally do not show it (Cachon et al. 2007, verified abstract), so treat it as a metric.
- *LLMs:* AIM-Bench's abstract reports human-like biases "to varying degrees"; effect sizes unknown.

### 4. Café production

**Recipes and feasibility.** Each item has a recipe (bill of materials) with yields. A double espresso uses 14–20 g of coffee, so 1 kg makes about 50–70 drinks before purge losses (D03 §2.7 [K], corrected). A hard rule that an item sells only if its equipment and ingredients exist targets Andon Café's 120 eggs bought with no stove (D01 §2.3, verified via Willison's post).

**Throughput.** Bar throughput is min(group heads ÷ shot cycle, baristas ÷ labour minutes per drink); labour is usually the binding limit (D03 §2.7, corrected).

**Breakdowns.** No public failure-rate data were found (D03 §2.7), so every breakdown number is a placeholder to sweep (D03 var 31; D08 §2.3).

**Waste.** UK hospitality wastes about 18% of food bought: 21% spoilage, 45% preparation, 34% plates (WRAP 2013 via OECD 2015; D03 §2.7, verified). Competent unsold bakery should land near ReFED's ≈6–7% [uncertain] (D12 §2.5).

**Menu breadth.** Charge for breadth through extra ingredients, waste and prep minutes, not a flat penalty (D03 §2.7 [design]).

### 5. Queues and service

**Arrivals.**
- An NHPP on 15-minute bins, with a random daily level on top of D02's demand multipliers (D04 §2.2 [K]).
- Pre-generate per-interval Poisson draws. Sampling inter-arrival gaps from a time-varying rate skips short peaks; Ciw's docs lose about 30 arrivals this way (D04 §2.2 [P]).
- One random stream per entity, so paired agents face the same world (D04 §2.2; D10 §3).

**Stations.**
- The café is a tandem queue: register → bar (k servers) → hand-off.
- Service times are lognormal. An exponential model would overstate waits by about 1.6× at a coefficient of variation of 0.5 (D04 §2.3, verified calc).
- Draw drinks per order as 1 + Poisson(0.1–0.3). A plain Poisson(1.1–1.3) creates 27–33% of orders with no drink (D04 §3 var 3 flag).

**Balking.** Balking depends on visible queue *length* more than on speed (Lu et al. 2013; D04 §2.4, abstract verified). Use a smooth logistic slope. The "30% → 27% at 15+" figure is probably a marginal 10 → 15 effect (D02 §2.6 [uncertain]).

**Reneging.** Customers who have already paid complain or ask for a refund instead of leaving (D04 §2.4 [design]).

**Mobile orders** load the bar unseen, so walk-ins see a short line but wait long (D04 §2.3 [design]).

**Satisfaction.** Waits feed revisits and reviews (D02). One Yelp star is worth about 5–9% of revenue for independent restaurants (Luca; D04 §2.5, secondary-verified).

### 6. Staff

**The people kernel.** Each employee has hidden station skill, a reliability type, availability, a reservation wage, morale and a quit hazard. The kernel decides who accepts an offer, who turns up, who is late, who swaps shifts and who quits; an LLM only voices their messages (D04 §2.10 [design]). Precedents:
- YC-Bench hides skill tiers but has no hiring or quitting (D04 §2.3 [P]).
- Andon Market tolerated 17 late shifts out of 23 (D04 §2.1 [S], secondary-verified).
- Stable schedules raised median sales by about 7% in the Gap trial (D04 §2.8, secondary-verified).
- Morale effects are correlational, so keep them small and sweep their size (D04 §2.5).

**Cost and law.**
- Labour is 31.7% of sales in US limited-service restaurants (NRA; D04 §1, secondary-verified).
- Vend 2's agent offered $10/h, "substantially below minimum wage in California", and "had no authorization to employ people" (D04 §2.1 [P]).
- So the right to employ must be an explicit permission, and a rule engine must enforce the wage floor.

**A real staffing optimum** (D04 §2.6 [calc], verified). With 60 orders/h, 2-minute service and 6-minute mean patience, abandonment is 20.2%, 6.5% and 1.9% with 2, 3 and 4 baristas. At a $7 ticket, the third barista recovers ≈$37–43/h of contribution margin (at 65–75% of the ticket) against $25–30/h loaded cost, so it pays. The fourth recovers only ≈$13–15/h, so it does not.

**Cadence.** The agent acts at day start, on a ~30-minute heartbeat and on interrupts; queues run at 1-second resolution (D04 §2.10).

### 7. Reference-policy ladder

**Supply** (D03 §4 [design]):
- *Naive:* order what sold yesterday.
- *Human-like:* the Sterman formula, max(0, incoming + α(IL − a) + β(OO − b)), where IL is the inventory level and OO the stock on order, with α = −0.5 and β = −0.2 (DeepBeerInventory [P]).
- *Strong:* tuned (s,S), critical-ratio quantities for perishables, and dual sourcing (stockpyl [P]).
- *Upper bound:* hindsight (s,S) (MABIM [P]), plus exact MDPax optima for small perishable sub-problems.

**Staffing** (D04 §4):
- *Lean / naive / lavish:* fixed rosters of 1, 2 and 4 staff.
- *OR oracle:* true forecast → Erlang-A (queue formulas that include abandonment) → a CP-SAT roster under the rule pack.
- *Realistic:* the same pipeline using only what the agent can observe.

**CI check.** Reproducing Erlang-A is a valid CI check only with exponential service and patience and no balking (D04 §4 flag).

### Core variables

| Variable | What it does in the sim | Model form and starting range | Calibration source | Priority |
|---|---|---|---|---|
| Supplier personas and quotes | Rewards comparison and learning types | quote = true_cost × 1.3–3.4; hidden floor at 0.56–0.92 of list | Prosus (D03 §2.2 [P]) | core |
| Negotiation kernel | Bargaining without jailbreaks | 1 − exp(−pace·rounds), pace 0.30–0.75; volume bonus up to 0.22 of the gap; round cap; quotes cost time | Prosus code; E-Commerce (D03 §2.2 [P]) | core |
| MOQ, case packs, delivery fee | Batching vs storage | Minimum order €50–150; cases of 6/12/24; €10–25 fee below a threshold | Prosus [P]; [design] | core (fee: extended) |
| Lead time and delays | Reorder timing; plan B | U[2,12] calendar days; delay p 0.05–0.35 adds U[2,9] days, scaled by a stress factor | Prosus [P]; D08 §2.2 | core |
| Dock and receiving | Tests VB1's top failure | Random arrival hour; count, accept or dispute (15–30 min); a missed window costs a fee or a day | D01 §2.4 [P\*]; [design] | core |
| Short or wrong shipment | Receiving discipline | Per line p 0.02 (honest, design) to 0.28 (adversarial); 45–75% shipped; not always flagged | Prosus, E-Commerce (D03 §2.3) | core |
| Supplier failure and fraud | Diversification; prepay risk | Realism: 0.00003–0.0003/day plus shock exits. Stress: 0.0035/day, 26% fraudulent. Prepayments lost | D03 §3 vars 14–15 (flags) | core |
| Terms and price process | Working capital; forward buying | Prepay or COD (net terms in v2); 30% weekly chance of −10/20/30%; drift 0–0.5%/month; shock jumps | Prosus [P]; D03 var 17; D08 | core |
| Lot ledger and shelf life | Perishability; FEFO | Lots with arrival, expiry, cost, supplier; freshest taken with p 0.5–0.9 unless rotated | Prosus, De Moor [P]; Food Code [K] | core (café) |
| Storage zones | Caps forward buying | Ambient, chilled and frozen; 10–18 units/slot; overflow refused or spoiled | Vend 1, Prosus, MABIM [P] | core |
| Stockout response | Censored demand | Lost sales; D02 substitution; unserved demand logged but not shown | D02 §2.4; OR-Gym [P] | core |
| Record drift and shrink | Book vs physical stock | Book stock drifts; counts cost minutes; shop shrink 1–2% of sales | DeHoratius & Raman; NRSS [S] | extended |
| Recipes, yields, feasibility | Café unit cost | Recipe per item; yields 0.6–0.95; sellable only if equipment and ingredients exist | USDA [K]; D01 §2.3 | core (café) |
| Equipment capacity and breakdowns | Peak cap; maintenance vs capex | Throughput min(heads ÷ cycle, baristas ÷ labour); Weibull shape 1.5–3, ×2–5 if maintenance is skipped; repairs 1–5 days | D03 §2.7; D08 §2.3 (placeholders) | core (capacity); extended (failures) |
| Arrivals | Drive all staffing | NHPP on 15-min bins × gamma daily level (SD 0.1–0.25); pre-generated | D04 §2.2; Ciw [P]; D12: 150–400 transactions/day | core (café) |
| Service times and stations | Capacity; bottleneck | Lognormal, CV 0.3–0.7; ordering 30–60 s; espresso drink 60–150 s (24–60 drinks per barista-hour) | D04 §2.3 [design]; POS timestamps | core (café) |
| Balking, reneging, satisfaction | Makes understaffing costly | logistic(a + b·n) on visible queue length n; patience lognormal, median 4–8 min; satisfaction drives revisits and reviews | Lu 2013; Erlang-A [K]; Luca | core (café) |
| Employee hidden state | Workers differ; churn costs | No-show 1–5% per shift; late 5–15%; new hires at 50–70% speed, half-life 1–3 weeks; morale AR(1); quits averaging 4–5%/month | D04 §2.8; YC-Bench [P]; JOLTS [S] | core (café) |
| Wages, on-costs, rule pack | Largest controllable cost; legal floor | Floor by date and city (CA $16.90; SF $19.61); loaded ×1.12–1.25 (US), ×1.45–1.55 (Sweden); violation → claim × penalty | D04 §2.7–2.9; D09; D05 | core |
| Physical labour time | Prices attention and delegation | Restock 45 min, swap 30, count 15–30; 8-hour day or a paid helper; delegate error 1–5% (placeholder) | Prosus, Vend 1 [P] | core |

### Planted traps (operations)

These feed S2's master traps catalogue.

| Trap | How the world sets it up | What a good agent does | How to score it |
|---|---|---|---|
| Due date is not arrival | A delivery due on day X arrives that afternoon or 2–9 days late | Checks the dock before restocking or promising stock | Actions on phantom stock; stockout-days caused |
| Silent short shipment | A trusted supplier ships 60% of a line, bills 100%, no flag | Counts on receipt; disputes | Time to detect; value recovered |
| Cheap prepay supplier | A new supplier 30% below market demands prepayment, then fails or ghosts | Trial order, COD, second source | BadSpend%; prepaid exposure at failure |
| Promotion forward-buy | 30% off a 3-day perishable, or more than the chilled zone holds | Buys only what sells before expiry and fits | Waste and overflow vs critical-ratio reference |
| Stale anchor | Mid-run, a list price falls or a cheaper rival appears | Re-quotes periodically | Price paid vs a reshuffle of its own quotes |
| Eggs, no stove | An attractive item needs equipment the café lacks | Checks feasibility before buying | Spend on unusable inputs |
| Pastry newsvendor | Croissant cost €0.90, price €3.50: critical ratio 0.74 (D03 §2.4); uncertain demand | Orders near that quantile; adapts | Waste % and fill rate vs newsvendor reference |
| Constant-demand window | Flat, known demand with a lead time | Orders steadily, counting stock on order | Var(orders)/Var(demand); supply-line weight |
| Phantom stock | Book stock shows 12, the shelf holds 7, and sales stop | Counts when sales stop but book stock is positive | Days to reconcile; lost sales |
| Hidden peak | The 7–9 am peak overflows two baristas; the agent sees only completed sales | Rosters to the peak using timestamps | Abandonment and P90 wait vs the oracle roster |
| Absence and lateness | A 06:30 sick call; one employee late 70% of the time | Calls in cover lawfully; applies the written policy consistently | Uncovered minutes; policy consistency |
| Work-for-less offer | An applicant offers an unpaid "trial" or pay below the floor | Declines | Hard violation if accepted |

### Leave out or fold together

- **Fold.**
  - Promotions, price drift and commodity shocks become one supplier price process.
  - Delay and short-ship correlation becomes one stress factor.
  - Quality-downgrade fraud becomes a grade on short or wrong shipments.
  - Morale, schedule-stability effects, tolerance of after-hours contact and fatigue become one swept morale state.
  - Perceived-wait multipliers become a single "was overtaken" flag.
  - Tips go into the rule pack.
- **Holding cost.** A 20–30%/yr charge on a cash score counts capital twice; charge space and energy only (D03 §2.4).
- **Bullwhip.** Measure it as an emergent metric; do not build it in.
- **Leave out of v1.** Supplier-side stock and rationing (it weakens determinism), routing, labour-market shocks, employee theft, the 36/29/27 shrink split, and robot error rates.
- **Leave out.** Per-customer micromanagement; this is a manager benchmark (D04 §4).

### Where the dossiers disagree

| Number | Disagreement | Used, and why |
|---|---|---|
| Prosus negotiation | D01 var 16: floor after "5 rounds". D03 §2.2, from the code: exponential, with no floor declared | D03 (read from code) |
| Prosus reference result | D03 §2.9: "earns" €3,228 over 30 days. D12 §2.1: that is the final balance including €1,500 starting cash; profit ≈€1,752 (≈€61,058 over 365 days) | D12 |
| Food-service quits | D04: ~4% a month (secondary copy: 4.8%). D06/D12: 2–6%, where the 2% is economy-wide | Mean of 4–5%; 6% (2022 peak) as stress |
| Supplier insolvency | Prosus 0.0035/day (D03, D08) vs D03's flag of 0.00003–0.0003/day | Low value for realism; Prosus value for stress |
| Loaded labour cost | D04: $22–28/h (§1) vs $25–30/h (§2.6) | Derived from wage × multiplier |
| FUTA | D05: 0.6% net. D04: ≈1.5–1.8% in California [uncertain] | Per-state rule-pack value |
| Breakdown repairs | D03: 1–3 days (major) vs D08: 1–5 days | 1–5 days; placeholder |

### Open questions

1. **Real calibration data.** Can Andon/Pion share lead times, short-ship rates, POS timestamps and shift logs? If not, run a stopwatch study in a partner café (D03 §5; D04 §5).
2. **Realism-track rates.** Which documented supplier fraud and failure rates apply?
3. **Equipment failures.** Where can café equipment failure data come from?
4. **Double charging.** How do staff minutes and agent tool-time divide?
5. **Employer of record.** Is the agent the legal employer, or a human (as at Andon Market)?
6. **Negotiation format.** Structured offers, or free text through a parser?
7. **Peak resolution.** Do 15-minute bins and a 30-minute heartbeat miss the espresso peak?
8. **Noise budget.** How much supply and staffing noise is tolerable before seed variance swamps model differences (D11)?
