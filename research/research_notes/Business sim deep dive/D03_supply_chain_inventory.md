# D03: Suppliers, inventory and production

Deep-dive dossier for the business-simulation benchmark (shop/vending track and café track). Research date: 10 Oct 2026.

**Tags.**
- [P] = primary source read directly this session (GitHub source, README and config files; anthropic.com).
- [P\*] = primary text read this session through a verbatim GitHub copy of a blocked page.
- [S] = press or search snippet only, mostly inherited from sibling dossiers D01, D05, D06 and D09.
- [K] = standard OR or industry literature cited from background knowledge. The host was blocked and the source was **not re-read this session**; verify before relying.
- [design] = our suggestion. [inference] = our reading.

**Access.** Only raw.githubusercontent.com, anthropic.com, claude.com and pypi.org were reachable. arxiv, andonlabs, fda.gov, wrap, INFORMS, MIT and Semantic Scholar failed DNS. The shared WebSearch budget was already used up, and no proxy or reader services were used.

---

## 1. Summary

- **The supply side now belongs in a deterministic kernel.** Andon admits Vending-Bench 2's supplier LLMs "can be jailbroken to give away stuff for free" ([P\*][vb2]). E-Commerce Bench and Prosus Vending Bench fix every price and accept/reject decision in seeded code; an LLM only writes the prose ([P][ecb], [P][prosus]).
- **Prosus publishes a complete supplier model in one TOML file** ([P][prosuscfg]). It covers:
  - markups of 1.32–3.40× true cost, with floors at 0.56–0.92 of list;
  - concession of 0.30–0.75 of the remaining gap per round, reaching the floor after 5 rounds;
  - minimum orders of €50–150 and 2–12-day lead times;
  - a 5–35% delay chance (+2–9 days), 28% bait-and-switch (ships 45–75% of the line), 10% ghosting, and a 0.0035/day chance of the supplier collapsing.
  - It is the best template found.
- **Fraud is the most discriminating supply variable.** In E-Commerce Bench, 26% of suppliers (152 of 576) run one of five scams. The richest model routed 18.5% of procurement to fraudsters, against 0.12% for the most cautious ([P][ecb]).
- **LLMs anchor on early supplier prices.** On repeat orders, 18 of 21 configurations paid significantly *more* than a random reshuffle of their own past quotes ([P][ecbsite]).
- **Delivery timing breaks agents, and receiving is untested.** Vending-Bench 1's dominant failure is assuming an order arrived on its due morning (D01 [P\*]). Vending-Bench 2 still auto-registers deliveries in storage ([P\*][vb2]).
- **Perishables are where the real café failed.** Andon Café reportedly bought 1,331 pastries and sold 326, ordered 120 eggs with no stove, then "overcorrected" into no perishables after a model swap (D01 [S]). No public sim models lot ages, FEFO (first-expiry-first-out) or which menu items the equipment can make. Prosus has one 3-day sandwich ([P][prosuscfg]).
- **Strong, auditable reference policies exist** and should anchor scoring:
  - newsvendor, EOQ (economic order quantity) and Clark–Scarf base-stock in stockpyl [P];
  - static and *hindsight* (s,S) policies in MABIM [P];
  - exact perishable optima in MDPax [P];
  - a scripted reorder-point operator in Prosus [P].
- **The Beer Game is a ready-made behavioural yardstick.** Humans under-weight orders already in transit (the supply line) and create bullwhip even when demand is constant (Sterman 1989; Croson et al. 2014, [K]). An executable "Sterman-formula" orderer is in DeepBeerInventory-RL [P].
- **Physical work needs a price.**
  - Project Vend paid Andon staff hourly to restock ([P][vend1]); phase 2 still relied on humans for "delivering the items and stacking the shelves" ([P][vend2]).
  - Prosus charges simulated minutes in an 8-hour day: restocking a machine takes 45 minutes ([P][prosusguide]).
- **Reference code has bugs.** OR-Gym's `Newsvendor-v0` reward multiplies purchase cost by excess inventory × order quantity, which looks wrong ([P][orgymnv]; [inference]). Unit- and money-conservation tests are mandatory.
- **Café production is untouched by AI benchmarks.** Recipes, yields, batch prep, equipment capacity and breakdowns, waste streams and menu engineering must come from OR and food-service literature [K].

---

## 2. Findings

### 2.1 What existing sims model on the supply side

| Feature | Vending-Bench 1/2 | Prosus v3 | E-Commerce Bench | Project Vend (real) |
|---|---|---|---|---|
| Discovery | Live web search; GPT-4o supplier replies in VB1 (D01 [P\*]) | Fictional search over 6 suppliers [P] | 576 suppliers, one category each [P] | Real web; in phase 1, Andon secretly played the wholesaler [P] |
| Prices | LLM decides; jailbreakable [P\*] | true_cost × markup, conceding to a floor [P] | Kernel decides (extends TERMS-Bench); floor hidden [P] | Market prices; purchases need human approval (phase 2) [P] |
| Reliability | Delays, supplier exits, bait-and-switch [P\*] | Delay, short-ship, ghosting and collapse chances [P] | 5 fraud types; supply-chain shock events [P] | Delivery checks added in phase 2 [P] |
| Payment | Irreversible (D01) | Paid at order; no cancellation [P] | Costs hit the day incurred; 9-day escrow on revenue [P] | Agent had no payment interface [P] |
| Receiving | Auto-registered [P\*] | Arrives at depot [P] | Warehouse [P] | Humans receive and restock [P] |
| Perishables | None | One 3-day SKU [P] | Not stated | Not modelled |
| Labour | Sub-agent (VB1) | Minutes per action [P] | Minutes per action [P] | Hourly fee [P] |

### 2.2 Suppliers: catalogues, prices, negotiation and terms

**Personas and catalogue** ([P][prosuscfg]). Each quote is derived from an honest `true_cost`. Each supplier has a markup, a floor, a minimum order value, delivery days and hazards:

| Persona | Markup | Floor | Minimum order | Delivery | Hazards |
|---|---|---|---|---|---|
| Incumbent, "straight" | 1.55× | 0.92 | €75 | 2–4 days | 5% delay |
| Cash-and-carry, "haggler" | 1.95× | 0.56 | €120 | 3–6 days | 12% delay |
| "Shark" | 3.40× | 0.70 | €50 | 4–9 days | 30% delay, 28% bait-and-switch, 10% ghosting |
| "Flaky" family firm | 1.32× | 0.88 | €60 | 3–12 days | 35% delay, collapse 0.0035/day |
| Drinks specialist | 1.38× | 0.84 | €90 | 2–5 days | 8% delay |
| Gadget importer | 1.85× | 0.62 | €150 | 5–12 days | 20% delay |

- The cheapest prices require hard bargaining or an unreliable source.
- The 0.0035/day collapse chance gives about 90% survival over 30 days but about 28% over 365 days (mean life about 286 days). Year-long runs must therefore multi-source [inference].
- Each week, every supplier×product has a 30% chance of a 10%, 20% or 30% discount. This invites forward-buying, which storage caps should check [design].

**Negotiation.**
- Prosus concedes a fixed fraction of the remaining gap each round: shark 0.30, haggler 0.55, flaky 0.70, straight 0.75. It declares the floor after 5 rounds, plus a volume bonus of up to 22% [P].
- Prosus parses intent by regex and admits this "does not establish open-ended conversational bargaining skill" ([P][prosusguide]).
- E-Commerce Bench scores negotiation with four metrics [P]:
  - CSE⁺: share of the bargaining range kept on honest deals;
  - %Oracle: surplus versus closing every honest deal at the floor;
  - rounds-to-deal;
  - AnchorRatio.
- Vending-Bench 2's "good" policy assumes half-price sourcing. Andon adds that "humans frequently manage to negotiate to get things for free in our real-life vending machines". That is customers bargaining *with the AI* ([P\*][vb2]).

**Discounts, minimums and fees.**
- Distributor price lists use all-units or incremental price breaks, case packs, minimum drops and delivery fees below a threshold [K].
- EOQ = √(2KD/h), where K is the fixed cost per order, D annual demand and h the holding cost per unit; with price breaks it is solved by checking each break (stockpyl implements EOQ) [K/P].
- MABIM charges a fixed per-order cost of 10 ([P][mabimcfg]). Prosus models minimums as order *value*. Neither sim exposes delivery fees [inference].

**Credit and contracts.**
- Prosus orders are "charged at the moment of purchase and cannot be cancelled"; proforma invoices expire after 14 days; only the straight and flaky personas refund overpayments [P].
- Real terms include prepay, cash on delivery (COD), net-15/30 and early-pay discounts. "2/10 net 30" (2% off if paid within 10 days, otherwise due in 30) implies a 37% annualised rate [K].
- Project Vend 2 withheld a payment interface "to ensure it always checked with a human" [P]. Its agents also agreed an onion forward contract that is illegal under the 1958 Onion Futures Act ([P][vend2]). Contract types need legality checks (D09).

### 2.3 Supplier reliability and fraud

- **Lead times.**
  - Prosus: uniform working days after payment clears, plus U[2,9] days when a delay fires [P].
  - OR-Gym defaults: 3, 5 and 10 periods ([P][orgyminv]).
  - Beer-game literature cases: 2 periods of shipping and 2 of order delay ([P][dbi]).
  - Variable lead time raises safety stock: SS = z·√(L·σ_D² + μ_D²·σ_L²) [K].
- **Short, wrong or degraded shipments.**
  - Prosus ships 45–75% of a line when bait-and-switch fires [P].
  - E-Commerce Bench separates quantity bait-and-switch from quality downgrade, which feeds "controllable returns" [P].
  - No sim makes the agent *detect* a short shipment by counting it [inference].
- **Substitution.** Suppliers never substitute SKUs in any sim we read. Customer substitution between perishables exists in the Hendrix two-product problem in MDPax [P].
- **Exit.** In VB2, GPT-5.1 "prepaid a supplier that then went out of business" (D01 [P\*]).
- **Fraud.** E-Commerce Bench runs five scam types: VIP-fee extortion, quantity bait-and-switch, quality downgrade, fake urgency and future-discount traps. Agents "never see a supplier's private cost floor or fraud status" ([P][ecbsite]). D05 adds bank-detail-change invoices [S].

### 2.4 Inventory theory and reference policies

- **Newsvendor.** The optimal order is q\* = F⁻¹(c_u/(c_u+c_o)), where c_u is the cost per unit short and c_o the cost per unit left over.
  - Checked in stockpyl: with c_o = 2, c_u = 18 and demand N(120,10), it orders 132.8, the 90th percentile ([P][stockpyl]).
  - Café illustration [design]: a croissant costs €0.90 and sells at €3.50 with no salvage, so the ratio is 0.74. A 24% sell-through (Andon Café [S]) is far beyond any defensible quantile.
  - Humans show "pull-to-centre" bias, ordering too little of high-margin goods and too much of low-margin goods (Schweitzer & Cachon 2000, [K]).
- **(s,S) and base-stock policies.**
  - (s,S): when stock falls to s, order up to S. It is optimal with a fixed order cost (Scarf 1960, [K]).
  - Base-stock (always order up to S) is optimal with no fixed cost; echelon base-stock is optimal for serial chains (Clark & Scarf 1960, [K]). Both are implemented in stockpyl [P].
  - MABIM ships static and dynamic base-stock baselines, plus static and hindsight (s,S) ([P][mabim]).
- **Lost sales with lead times** (the realistic shop case). No simple optimal policy exists; capped or constant-order variants can beat base-stock (Zipkin 2008; Huh et al. 2009, [K]). OR-Gym has variants with backlog and with lost sales plus a goodwill penalty [P].
- **Perishables.**
  - The state must track stock ages, so it grows exponentially with shelf life (Nahmias 1982, [K]). MDPax solves such problems exactly on GPU ([P][mdpax]).
  - MDPax's default De Moor configuration ([P][demoor]):
    - shelf life 2, lead time 1;
    - gamma demand with mean 4 and coefficient of variation 0.5;
    - unit costs: order 3, shortage 5, waste 7, holding 1;
    - stock issued FIFO or LIFO (default LIFO).
- **Holding cost.** The rule of thumb is 20–30% of value per year [K]. MABIM charges holding, storage per unit of volume, and 0.5× overflow above capacity [P]. If the score is cash, capital cost is already counted, so add only space and energy costs [design].

### 2.5 Behavioural evidence: bullwhip and anchoring

- **Causes of bullwhip** (Lee, Padmanabhan & Whang 1997, [K]): demand-signal processing, order batching, price swings and rationing games. Prosus's weekly promotions and order minimums deliberately create the batching and price-swing causes [inference].
- **Human evidence.**
  - Beer-Game players weight the supply line at about a third of what it should be, and their costs run about an order of magnitude above the benchmark (Sterman 1989, [K]).
  - Bullwhip persists with known demand distributions (Croson & Donohue 2006, [K]) and even with constant, known demand (Croson et al. 2014, [K]).
  - Industry data show retailers often *smooth* orders rather than amplify them (Cachon, Randall & Schmidt 2007, [K]). So the effect is a lab regularity, not a law.
- **Executable human-like baseline.** DeepBeerInventory's "Sterman formula" orders max(0, incoming + α(IL − a) + β(OO − b)) with α = −0.5 and β = −0.2 ([P][dbi]). Here IL is inventory level and OO is on-order stock; |β| < |α| encodes the under-weighting.
- **LLM evidence.**
  - E-Commerce Bench's anchoring finding is about price, not quantity. The authors blame "context eviction destroys the tool result that carried a price already won", and a memory store that "is barely used" [P].
  - InvAgent runs zero-shot LLM agents in 4-stage, 12-period beer-game variants against fixed and IPPO/MAPPO baselines ([P][invagent]); results were not readable.
  - In Project Vend 1, Claudius "successfully monitored inventory and ordered more products when running low" ([P][vend1]). Andon Market over-ordered candles (D01 [S]).
  - Logging on-order stock at every decision makes supply-line weighting measurable [design].

### 2.6 Perishability, shrinkage and record accuracy

- **Shelf life.**
  - Prosus uses 3 days for a fresh sandwich [P]. Typical values [K]: pastries are same-day; opened milk lasts days; roasted beans last weeks.
  - US Food Code: ready-to-eat chilled foods held over 24 h are date-marked and discarded after 7 days at ≤5 °C/41 °F [K]. Temperature rules are in D09 [S]. Swedish rules differ, so constants need localising.
- **Issuing order.** At a self-serve fridge, customers take the freshest unit (LIFO-like) unless staff rotate stock. De Moor's model supports both FIFO and LIFO [P].
- **Shrinkage.** US retail shrink was 1.6% of sales: 36% external theft, 29% internal theft, 27% process error (NRSS, D06 [S]). In Project Vend 2, Claudius tried to hire a shoplifting guard at $10/hour, below the California minimum wage ([P][vend2]).
- **Record inaccuracy.** About 65% of SKU-store inventory records at one large retailer were wrong (DeHoratius & Raman 2008, [K]). Book stock should drift from physical stock unless the agent pays for counts [design].

### 2.7 Café production

- **Recipes (bill of materials) and yields.**
  - Purchased weight exceeds usable weight after trim, cooking and portioning (USDA AH-102, [K]).
  - A double espresso uses about 14–20 g of coffee, so 1 kg makes about 50–60 drinks; a latte adds 150–250 ml of milk [K].
  - The gap between theoretical and actual usage reveals waste, over-portioning or theft [design].
- **Waste.** UK hospitality wastes about 18% of food purchased: 21% from spoilage, 45% from preparation and 34% from plates (WRAP 2013, [K]). The agent controls spoilage and over-production.
- **Capacity and feasibility.**
  - Espresso throughput is set by group heads × shot time (about 25–30 s) × baristas; ovens add batch size and cycle time; fridge volume caps stock levels [K].
  - Eggs ordered with no stove (D01 [S]) argue for a hard feasibility rule: an item sells only if its equipment and ingredients exist.
- **Breakdowns.**
  - No public data on equipment failure rates were found [inference].
  - Model failures as a hazard per operating hour that rises when maintenance (backflush, descale, gaskets) is skipped, with repair lead time and cost [design].
  - Equipment spend can unlock products. Project Vend's tungsten cubes became profitable "markedly easier when Andon Labs purchased a laser etching machine" [P]. Espresso machines cost $5k–25k (D05 [S]).
- **Menu engineering.** Classify items by contribution margin × popularity into Stars, Plowhorses, Puzzles and Dogs (Kasavana & Smith 1982, [K]). Charge for menu breadth through more ingredients, waste and prep minutes rather than a flat penalty [design].

### 2.8 Physical logistics and abstraction

- **Real deployments.**
  - Vend 1's prompt: "Andon Labs charges ${ANDON_FEE} per hour for physical labor". The machine "fits about 10 products per slot, and the inventory about 30 of each product" [P].
  - Butter-Bench: best LLM 40% vs humans 95% on embodied tasks (D01 [S]).
- **Existing abstractions.**
  - Prosus charges tool minutes: restock 45, slot swap 30, price change 5, about ten restocks a day [P].
  - VB1 used a physical-world sub-agent (D01 [P\*]).
  - Vend 1 used a paid human.
- **Missing everywhere** [design]:
  - delivery windows with redelivery fees;
  - receiving checks (count, temperature, invoice match) that cost minutes and catch short shipments;
  - an error rate for delegated work;
  - storage zones by temperature;
  - travel time between sites (Prosus has 3 sites but a flat 45-minute restock).

### 2.9 OR environments and baselines

| Environment | Offers | Use |
|---|---|---|
| [OR-Gym][orgym] [P] | `InvManagement` multi-echelon chain, with backlog or lost sales (30 periods, Poisson(20) demand, lead times 3/5/10, capacities 100/90/80); `NetworkManagement`; `Newsvendor-v0` (lead time 5) | Templates; audit the rewards first |
| [ORL][orl] [P] | Newsvendor with lead times, vehicle routing, bin packing (Balaji et al. 2019) | Source of OR-Gym's newsvendor |
| [MABIM][mabim] [P] | Many SKUs; shared capacity with overflow cost; vendor lead time; per-order cost; train/validation/test date splits; base-stock and (s,S) baselines including hindsight | Capacity coupling; upper bound |
| [DeepBeerInventory][dbi] [P] | Beer game with Clark–Scarf base-stock, Sterman-formula and random co-players | Bullwhip probe; human-like baseline |
| [InvAgent][invagent] [P] | LLM multi-agent beer game | Prior art |
| [stockpyl][stockpyl] [P] | EOQ, newsvendor, Wagner–Whitin, serial and tree multi-echelon optimisation, simulation | Reference-policy library |
| [MDPax][mdpax] / [viso_jax][viso] [P] | Exact value iteration for perishable problems (De Moor; Hendrix with substitution; platelets with weekday demand and uncertain shelf life at arrival) | Café sub-problem optima |
| Prosus scripted operator [P] | Reorder at 40 units; 10 days' cover; restock below 45% slot fill; stops buying inside the 12-day worst-case lead time. Earns €3,228 over 30 days and €61,219 over 365 days (5 seeds each) | Calibration floor (has privileged information) |

---

## 3. Variables catalogue

| # | Variable | Why it matters | How to model (ranges) | Calibration | Priority |
|---|---|---|---|---|---|
| 1 | Supplier universe and discovery | Sourcing skill | Seeded universe of 6–30 suppliers with overlapping catalogues; search tool; no live web | Prosus [P]; E-Commerce [P] | core |
| 2 | List price / markup | Comparison shopping | quote = true_cost × markup (1.3–3.4) | Prosus [P] | core |
| 3 | Negotiation kernel | Bargaining without jailbreaks | Hidden floor at 0.56–0.92 of list; concede 0.30–0.75 of the gap per round; floor after about 5 rounds; LLM writes prose only; unverifiable claims ignored | Prosus [P]; E-Commerce [P]; D06 | core |
| 4 | Quantity discounts | EOQ vs storage | All-units price breaks or a volume bonus up to 22% | Prosus [P]; [K] | core |
| 5 | Minimum order / case packs | Batching; bullwhip | Minimum order value €50–150; case multiples of 6/12/24 | Prosus [P]; [design] | core |
| 6 | Delivery fee / threshold | Consolidating orders | Flat €10–25 below a free-delivery threshold | [K]; [design] | extended |
| 7 | Lead time | Reorder timing | Uniform 2–12 working days, per supplier | Prosus [P]; OR-Gym [P] | core |
| 8 | Delay events | Robustness; backup supplier | Probability 0.05–0.35, adding U[2,9] days; correlated during shock events | Prosus [P]; VB2 [P\*]; E-Commerce [P] | core |
| 9 | Arrival hour / receiving window | VB1's top failure | Arrival hour random within a window; a miss means a redelivery fee or one day's delay | VB1 (D01 [P\*]); [design] | core |
| 10 | Short / wrong / degraded shipment | Receiving discipline; trust | Per-line probability about 0.02 (honest) to 0.28 (adversarial); ships 45–75%; quality grade lowers demand and raises returns | Prosus [P]; E-Commerce [P] | core |
| 11 | Supplier substitution | Out-of-stock handling | Substitute offered with probability 0.05–0.15; accept or reject | [design]; Hendrix [P] | extended |
| 12 | Supplier capacity / rationing | Shortage gaming | Capacity per period; pro-rata allocation | OR-Gym [P]; Lee et al. [K] | extended |
| 13 | Reply latency / ghosting | Follow-up | Replies overnight; ghosting 0–0.10 | Prosus [P] | core |
| 14 | Supplier insolvency | Diversification; prepayment risk | Hazard 0.0005–0.0035/day; prepayments lost on exit | Prosus [P]; VB2 [P\*] | core |
| 15 | Fraudulent suppliers | Fraud avoidance | About 26% of suppliers; VIP fee, bait-and-switch, downgrade, fake urgency, discount trap, bank-detail change; invisible in price | E-Commerce [P]; D05 [S] | core |
| 16 | Payment terms / credit | Working capital | Prepay, COD, net-15/30, 2/10 net 30; credit limit grows with on-time payment; late payment → COD | Prosus [P]; [K]; D05 | core (prepay/COD); extended (net terms) |
| 17 | Price drift / promotions / shocks | Forward buying | Weekly promotion: 30% chance of −10/20/30%; drift 0–2%/month; commodity shocks of +20–50% | Prosus [P]; E-Commerce [P]; [K] | core (promotions); extended (drift, shocks) |
| 18 | Supplier relationship memory | Makes threats and lies costly | Score from payment timeliness, disputes and threats; moves floor, priority and terms | D06; [design] | extended |
| 19 | Overpayment / duplicate shipment | Honesty probe | Some personas keep overpayments; occasional unbilled duplicate shipment | Prosus [P]; Mythos (D01 [P\*]) | extended |
| 20 | Storage capacity by zone | Caps forward buying | Ambient, chilled and frozen space; 10–18 units per slot; excess refused or charged (0.5×) | Vend 1 [P]; Prosus [P]; MABIM [P] | core |
| 21 | Holding / space cost | Cost of excess stock | Explicit space and energy only when scoring on cash; 20–30%/yr otherwise | [K]; MABIM [P] | extended |
| 22 | Lot ages / shelf life | Perishability | Lot ledger (SKU, arrival, expiry, cost, supplier); shelf life from 1 day to months | Prosus [P]; De Moor [P]; Food Code [K] | core (café); extended (vending) |
| 23 | Issuing order | FIFO/FEFO compliance | Customers take the freshest with p = 0.5–0.9 unless staff spend time rotating | De Moor [P]; [design] | extended |
| 24 | Stockout response | Lost sales vs backorders | Lost sales; within-category substitution; stockouts also reduce variety (Prosus: 6 products optimal, shortfall slope 0.55, capped at 50%) | OR-Gym [P]; Prosus [P] | core |
| 25 | Shrinkage / theft | Real loss | 1–2% of sales, split 36/29/27 external/internal/error; shoplifting events | NRSS (D06 [S]); Vend 2 [P] | extended |
| 26 | Record accuracy | Book vs physical stock | Book stock drifts; a physical count costs minutes | DeHoratius & Raman [K] | extended |
| 27 | Recipe bill of materials / yields | Café unit cost | Per-item recipe; yields 0.6–0.95; portion variance | USDA AH-102 [K] | core (café) |
| 28 | Prep capacity / batching | Production planning | Batch size, cycle time, staff-minutes | [design]; D06 | core (café) |
| 29 | Equipment throughput | Peak service limit | Group heads × shot time; oven slots; fridge volume; queue balking | [K]; D02 | core (café) |
| 30 | Equipment–menu feasibility | "Eggs with no stove" | An item is sellable only if its equipment and ingredients exist | Andon Café (D01 [S]) | core (café) |
| 31 | Breakdowns / maintenance | Downtime; capex | Hazard per hour, ×2–5 if maintenance is skipped; minor (1–2 h) vs major (1–3 days, €200–800) | [design]; D05 [S] | extended |
| 32 | Waste streams | Main café leak | Spoilage, prep loss, over-production, plate waste | WRAP [K]; Andon Café 326/1,331 [S] | core (café) |
| 33 | Hot-hold / time limits | Food safety | Discard after 4 h out of temperature control; selling expired stock is a violation | Food Code [K]; D09 | extended |
| 34 | Menu complexity | Margin vs waste | Margin × popularity matrix; each SKU adds ingredients and prep time | Kasavana & Smith [K] | extended |
| 35 | Physical labour time | Attention cost | Restock 45 min, swap 30, count or receive 15–30; 8-hour day or a paid helper | Prosus [P]; Vend 1 [P] | core |
| 36 | Delegate error rate | Messiness | 1–5% mis-stocks or miscounts; 0.5–2% damaged goods | Butter-Bench (D01 [S]); [design] | extended |
| 37 | Pickup vs delivery / routing | Cash-and-carry trips; multiple sites | Self-collection is cheaper but costs travel minutes | [design]; Prosus [P] | stretch |
| 38 | Upstream echelon dynamics | Supplier-side bullwhip | Suppliers hold their own stock and react to aggregate orders | Beer game [P/K]; OR-Gym [P] | stretch |
| 39 | Ending inventory valuation | Stops end-of-run tricks | Value at cost minus a liquidation haircut (perishables at 0), or a hidden extra period | VB1; Prosus [P]; D05 | core |

---

## 4. Design implications for the benchmark

### Build

1. **Deterministic supply kernel with an LLM voice.** Seed it per (supplier, SKU, cycle) [P]. A validator checks that the rendered text matches the decision (D06).
2. **Hidden supplier types with noisy signals.** Prosus's blurbs nearly name the type ("Honest prices, chaotic logistics…") [P]. Use history, reviews and occasionally false signals, so types must be *learned* [design].
3. **A lot-level unit ledger beside the money ledger (D05).** Check conservation every step: purchases = sales + waste + shrink + on hand.
4. **A receiving step.** Deliveries land in a "dock" state and are counted and accepted or disputed within a window, at a cost in minutes. This tests VB1's failure directly [design].
5. **Two production layers.**
   - Shop: buy and sell.
   - Café: buy, then prep (recipes, yields, batch and equipment capacity), then sell, with hard feasibility rules.
6. **Per-seed reference policies with privileged parameters.**
   - Naive: order what sold yesterday.
   - Sterman-formula (human-like).
   - Strong: tuned (s,S) plus critical-ratio quantities for perishables plus dual-sourcing.
   - Hindsight (s,S) as an upper bound.
   - MDPax optima for small sub-problems.
   - Normalise each agent's score as (agent − naive)/(strong − naive) [design; R2].
7. **Supply diagnostics beside profit.**
   - Stock: fill rate, stockout-days, waste %, inventory turns.
   - Bullwhip ratio Var(orders)/Var(demand), and how much weight the agent gives on-order stock.
   - Supplier dealings: CSE⁺, AnchorRatio, BadSpend%, supplier concentration, share of deliveries verified, time to detect a short shipment.
8. **Embedded probes.** Single-period newsvendor decisions at known critical ratios (tests pull-to-centre), and a constant-demand window (tests bullwhip with nothing to forecast) [design].

### Avoid

- **Live web suppliers or real third parties.** Results are not reproducible and the ethics are contested (Andon Café, D01).
- **LLM-decided prices, quantities or invoice arithmetic.** These invite jailbreaks and arithmetic exploits (VB2 [P\*]; D05 [S]).
- **Unbounded high-value SKUs.** VB2's "perfect strategy" begins with "extremely valuable items" [P\*]. Bound exotic demand or restrict machine categories, as Prosus does [P].
- **Cash-only scoring with no stock value.** It rewards running stock down; Prosus's reference stops buying inside the 12-day lead time [P].
- **A single public economy.** Prosus calls itself "open-book" [P]. Hold out configurations and seeds.
- **Unaudited reward code** (OR-Gym's newsvendor [inference]) and **holding cost layered on cash scoring** (double counting).

### Known exploits and mitigations

| Exploit | Evidence | Mitigation |
|---|---|---|
| Jailbreak supplier to zero price | VB2 [P\*] | Kernel price floor |
| Spam quotes to map a deterministic floor | [inference] | Quotes cost time; supplier patience decays |
| Exploit invoice arithmetic | D05 [S] | Kernel generates invoices; claims audited |
| Keep overpayments or unbilled duplicates | Prosus [P]; Mythos (D01 [P\*]) | Allowed but logged as conduct |
| Lie about rival quotes | D06 | Kernel ignores; logged |
| Forward-buy promotions beyond capacity | Prosus [P] | Zone capacity; overflow refused or spoiled |
| Run stock down at the end | Prosus/VB2 cash score [P] | Liquidation haircut or hidden continuation |
| Sell expired food or relabel dates | Food Code [K]; D09 | Expiry is a ledger fact; inspections |
| Infer supplier type from blurb | Prosus [P] | Randomised names and blurbs; noisy signals |
| Make a rival dependent on your supply (Arena) | Mythos (D01 [P\*]) | Allowed in the Arena track; telemetry |

---

## 5. Open questions

1. **Calibration data.** Andon's real lead times, short-ship rates and supplier failures (Café, Market) are unpublished. Could Pion share anonymised logs?
2. **LLM ordering biases.** Do LLMs show pull-to-centre and supply-line under-weighting? With the search budget exhausted, studies beyond InvAgent went unchecked. One candidate needs locating and verifying: a 2025 "AIM-Bench" inventory-bias paper, known from background knowledge only.
3. **Supplier stock dynamics.** Should suppliers have their own stock that reacts to the agent's orders? That adds rationing games but weakens determinism.
4. **Equipment failure rates.** None found for café equipment. Possible sources are equipment service records or chains.
5. **Localisation.** Should the Stockholm and San Francisco packs differ in delivery days, VAT invoices and food-safety rules, or stay stylised?
6. **How to model bargaining.** Structured offers measure more cleanly; free text through a kernel is more realistic but limited by the parser (Prosus [P]).
7. **Labour accounting.** How should staff minutes (D06) divide against agent tool-time without charging twice?
8. **Contracts.** Should consignment, buy-back of unsold bakery goods, standing orders and forward contracts (onion futures [P]) be included?
9. **Noise budget.** How much supply randomness is tolerable before run variance swamps model differences? Run R2's variance decomposition.

---

## 6. Sources

**[P] read this session**
- `vend1`: Anthropic, "Project Vend" (Jun 2025). https://www.anthropic.com/research/project-vend-1
- `vend2`: Anthropic, "Project Vend: Phase two" (Dec 2025). https://www.anthropic.com/research/project-vend-2
- Prosus Vending Bench:
  - `prosus`: repository. https://github.com/ProsusAI/vending-bench
  - `prosuscfg`: config file. https://github.com/ProsusAI/vending-bench/blob/main/tasks/vending-bench/environment/sim-server/vending/config.toml
  - `prosusguide`: benchmark guide. https://github.com/ProsusAI/vending-bench/blob/main/docs/benchmark-guide.md
- E-Commerce Bench:
  - `ecb`: repository. https://github.com/QwenLM/E-CommerceBench (paper arXiv 2608.30730)
  - `ecbsite`: website source. https://github.com/ecbench/ecbench.github.io (served at https://ecbench.github.io)
- OR-Gym:
  - `orgym`: repository. https://github.com/hubbs5/or-gym (paper arXiv 2008.06319)
  - `orgyminv`: https://github.com/hubbs5/or-gym/blob/master/or_gym/envs/supply_chain/inventory_management.py
  - `orgymnv`: https://github.com/hubbs5/or-gym/blob/master/or_gym/envs/classic_or/newsvendor.py
- `orl`: AWS ORL benchmarks. https://github.com/awslabs/or-rl-benchmarks (paper arXiv 1911.10641)
- MABIM:
  - `mabim`: repository. https://github.com/VictorYXL/ReplenishmentEnv
  - `mabimcfg`: demo config. https://github.com/VictorYXL/ReplenishmentEnv/blob/main/ReplenishmentEnv/config/demo.yml
- `dbi`: DeepBeerInventory-RL. https://github.com/OptMLGroup/DeepBeerInventory-RL (paper doi 10.1287/msom.2020.0939)
- `invagent`: InvAgent. https://github.com/zefang-liu/InvAgent (paper arXiv 2407.11384)
- `stockpyl`: stockpyl. https://github.com/LarrySnyder/stockpyl
- MDPax and viso_jax:
  - `mdpax`: https://github.com/joefarrington/mdpax
  - `viso`: https://github.com/joefarrington/viso_jax
  - `demoor`: https://github.com/joefarrington/mdpax/blob/main/src/mdpax/problems/perishable_inventory/de_moor_single_product.py

**[P\*] verbatim copies read this session**
- `vb2`: Vending-Bench 2 page, capture of 29 Sep 2026. https://github.com/fstandhartinger/model-market-comparison/blob/main/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-vending-bench-2/packet-r1.md (canonical: https://andonlabs.com/evals/vending-bench-2)
- Andon Labs, "Why we built Pion" (copy). https://github.com/kzinmr/ai-topics/blob/main/wiki/raw/articles/2026-09-15_andonlabs-pion--de6c4af1.md

**Via sibling dossiers**
- D01: VB1 paper [P\*] (arXiv 2502.15840); Andon Café and Market press [S]; Butter-Bench [S]; Mythos card [P\*].
- D05: capex; invoice exploit [S].
- D06: NRSS shrink [S]; supplier lies.
- D09: Food Code temperatures [S].

**[K] background literature (not re-read; verify)**
- Sterman (1989), *Management Science* 35(3), doi 10.1287/mnsc.35.3.321.
- Lee, Padmanabhan & Whang (1997), *Management Science* 43(4), doi 10.1287/mnsc.43.4.546.
- Croson & Donohue (2006), *Management Science* 52(3).
- Croson, Donohue, Katok & Sterman (2014), *POM* 23(2).
- Cachon, Randall & Schmidt (2007), *MSOM* 9(4).
- Schweitzer & Cachon (2000), *Management Science* 46(3), doi 10.1287/mnsc.46.3.404.12070.
- Scarf (1960), "The optimality of (S,s) policies…", in *Mathematical Methods in the Social Sciences*.
- Clark & Scarf (1960), *Management Science* 6(4), doi 10.1287/mnsc.6.4.475.
- Nahmias (1982), *Operations Research* 30(4), doi 10.1287/opre.30.4.680.
- Zipkin (2008), *Operations Research* 56(5).
- Huh et al. (2009), *Management Science* 55(3).
- DeHoratius & Raman (2008), *Management Science* 54(4).
- De Moor et al. (2022), *EJOR*, doi 10.1016/j.ejor.2021.10.045. Parameters seen via MDPax [P].
- Kasavana & Smith (1982), *Menu Engineering*.
- WRAP (2013). https://wrap.org.uk/resources/report/overview-waste-hospitality-and-food-service-sector
- FDA Food Code 2022. https://www.fda.gov/food/fda-food-code/food-code-2022
- USDA ARS, Agriculture Handbook 102. https://www.ars.usda.gov/ARSUserFiles/80400525/Data/Classics/ah102.pdf

[vend1]: https://www.anthropic.com/research/project-vend-1
[vend2]: https://www.anthropic.com/research/project-vend-2
[prosus]: https://github.com/ProsusAI/vending-bench
[prosuscfg]: https://github.com/ProsusAI/vending-bench/blob/main/tasks/vending-bench/environment/sim-server/vending/config.toml
[prosusguide]: https://github.com/ProsusAI/vending-bench/blob/main/docs/benchmark-guide.md
[ecb]: https://github.com/QwenLM/E-CommerceBench
[ecbsite]: https://github.com/ecbench/ecbench.github.io
[orgym]: https://github.com/hubbs5/or-gym
[orgyminv]: https://github.com/hubbs5/or-gym/blob/master/or_gym/envs/supply_chain/inventory_management.py
[orgymnv]: https://github.com/hubbs5/or-gym/blob/master/or_gym/envs/classic_or/newsvendor.py
[orl]: https://github.com/awslabs/or-rl-benchmarks
[mabim]: https://github.com/VictorYXL/ReplenishmentEnv
[mabimcfg]: https://github.com/VictorYXL/ReplenishmentEnv/blob/main/ReplenishmentEnv/config/demo.yml
[dbi]: https://github.com/OptMLGroup/DeepBeerInventory-RL
[invagent]: https://github.com/zefang-liu/InvAgent
[stockpyl]: https://github.com/LarrySnyder/stockpyl
[mdpax]: https://github.com/joefarrington/mdpax
[viso]: https://github.com/joefarrington/viso_jax
[demoor]: https://github.com/joefarrington/mdpax/blob/main/src/mdpax/problems/perishable_inventory/de_moor_single_product.py
[vb2]: https://github.com/fstandhartinger/model-market-comparison/blob/main/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-vending-bench-2/packet-r1.md
