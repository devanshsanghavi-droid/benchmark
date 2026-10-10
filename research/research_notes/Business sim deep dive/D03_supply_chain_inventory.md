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
  - concession that approaches the floor asymptotically: progress = 1 − exp(−pace × rounds) with pace 0.30–0.75, so each round closes about 26–53% of the remaining gap and the floor is never quite reached by talk alone (after 5 rounds a "shark" has conceded about 78% of the gap, a "straight" supplier about 98%) [corrected by fact-check: was "concession of 0.30–0.75 of the remaining gap per round, reaching the floor after 5 rounds". `mailroom.quote_unit_price` uses the exponential form; `rounds_to_floor = 5` is loaded by config.py but never used by engine.py, and the "that is the floor" reply (`negotiate_reply`) is never called; ProsusAI/vending-bench main, read 10 Oct 2026];
  - minimum orders of €50–150 and 2–12-day lead times;
  - a 5–35% delay chance (+2–9 days), 28% bait-and-switch (ships 45–75% of the line), 10% ghosting, and a 0.0035/day chance of the supplier collapsing.
  - It is the best template found.
- **Fraud is the most discriminating supply variable** [inference; fact-check note: E-Commerce Bench does not claim this. What it shows is that BadSpend% has by far the widest relative spread of its supply metrics (0.12–27.92% vs CSE⁺ 0.60–0.81) and that it does not track final assets]. In E-Commerce Bench, 26% of suppliers (152 of 576) run one of five scams. The richest model routed 18.5% of procurement to fraudsters, against 0.12% for the most cautious ([P][ecb]).
- **LLMs anchor on early supplier prices.** On repeat orders, 18 of 21 configurations paid significantly *more* than a random reshuffle of their own past quotes ([P][ecbsite]).
- **Delivery timing breaks agents, and receiving is untested.** Vending-Bench 1's dominant failure is assuming an order arrived on its due morning (D01 [P\*]). Vending-Bench 2 still auto-registers deliveries in storage ([P\*][vb2]).
- **Perishables are where the real café failed.** Andon Café reportedly bought 1,331 pastries and sold 326 [uncertain: press-only; D01's fact-check found the sources conflict], ordered 120 eggs with no stove [verified in D01 via a verbatim copy of Simon Willison's post], then "overcorrected" into no perishables after a model swap [uncertain: press-only, per D01] (D01 [S]). No public agent-business sim models FEFO (first-expiry-first-out) across mixed shelf lives or which menu items the equipment can make. Prosus has one 3-day sandwich ([P][prosuscfg]), but it does keep a lot ledger for it [corrected by fact-check: was "No public sim models lot ages". Prosus `engine.py` stores depot stock as batches with `received_day`, `expiry_day` and `unit_cost`, issues the oldest batch first and bins expired batches nightly. Flaw: a machine slot's freshness clock is reset to the day of the latest restock (`loaded_day`), so topping up a slot silently re-dates the older units already in it. OR environments (MDPax/De Moor) also track ages].
- **Strong, auditable reference policies exist** and should anchor scoring:
  - newsvendor, EOQ (economic order quantity) and Clark–Scarf base-stock in stockpyl [P];
  - static and *hindsight* (s,S) policies in MABIM [P];
  - exact perishable optima in MDPax [P];
  - a scripted reorder-point operator in Prosus [P].
- **The Beer Game is a ready-made behavioural yardstick.** Humans under-weight orders already in transit (the supply line) and create bullwhip even when demand is constant (Sterman 1989; Croson et al. 2014, [K]). An executable "Sterman-formula" orderer is in DeepBeerInventory-RL [P].
- **Physical work needs a price.**
  - Project Vend paid Andon staff hourly to restock ([P][vend1]); phase 2 still relied on humans for "delivering the items and stacking the shelves" ([P][vend2]).
  - Prosus charges simulated minutes in an 8-hour day: restocking a machine takes 45 minutes ([P][prosusguide]).
- **Reference code has bugs.** OR-Gym's `Newsvendor-v0` reward multiplies purchase cost by excess inventory × order quantity, which looks wrong ([P][orgymnv]; [inference]) [verified: `purchase_cost = excess_inventory * self.cost * order_qty * self.gamma ** self.lead_time`]. [fact-check addition: Prosus has two quieter problems. Its `rounds_to_floor` parameter and at-floor reply are dead code, and a restock resets the freshness clock of the whole slot (§1, perishables).] Unit- and money-conservation tests are mandatory.
- **Café production is untouched by AI benchmarks.** Recipes, yields, batch prep, equipment capacity and breakdowns, waste streams and menu engineering must come from OR and food-service literature [K].

---

## 2. Findings

### 2.1 What existing sims model on the supply side

| Feature | Vending-Bench 1/2 | Prosus v3 | E-Commerce Bench | Project Vend (real) |
|---|---|---|---|---|
| Discovery | Live web search; GPT-4o supplier replies in VB1 (D01 [P\*]) | Fictional search over 6 suppliers [P] | 576 suppliers, one category each [P] | Real web; in phase 1, Andon secretly played the wholesaler [P] |
| Prices | LLM decides; jailbreakable [P\*] | true_cost × markup, conceding to a floor [P] | Kernel decides (extends TERMS-Bench); floor hidden [P] | Market prices; purchases need human approval (phase 2) [P] |
| Reliability | Delays, supplier exits, bait-and-switch [P\*] | Delay, short-ship, ghosting and collapse chances [P] | 5 fraud types; supply-chain shock events [P] | Phase 2 made Claudius double-check prices and delivery times with research tools before quoting customers, and added a CRM that tracks deliveries [P] [corrected by fact-check: was "Delivery checks added in phase 2". The Vend 2 post describes quote-time checks and delivery tracking, not checks on what suppliers actually delivered] |
| Payment | Irreversible (D01) | Paid at order; no cancellation [P] | Costs hit the day incurred; 9-day escrow on revenue [P] | Agent had no payment interface [P] |
| Receiving | Auto-registered [P\*] | Arrives at depot [P] | Warehouse [P] | Humans receive and restock [P] |
| Perishables | None [uncertain: not checked against the VB1/VB2 text this session] | One 3-day SKU, with a batch ledger and oldest-first issue at the depot [P] | Not stated | Not modelled |
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

- [fact-check: all six rows match config.toml exactly. The gadget importer uses the "haggler" persona and the drinks specialist uses "straight". Prosus's "bait-and-switch" is a short shipment of the same SKU, never a different item, and the delivery email flags each short line ("ordered N"). Delivery "days" are simulated calendar days, not working days; see §2.3.]
- The cheapest prices require hard bargaining or an unreliable source.
- The 0.0035/day collapse chance gives about 90% survival over 30 days but about 28% over 365 days (mean life about 286 days). Year-long runs must therefore multi-source [inference].
- Each week, every supplier×product has a 30% chance of a 10%, 20% or 30% discount. This invites forward-buying, which storage caps should check [design].

**Negotiation.**
- Prosus concedes along an exponential curve: progress = 1 − exp(−pace × rounds), with pace 0.30 for the shark, 0.55 for the haggler, 0.70 for flaky and 0.75 for straight. Each round therefore closes 26%, 42%, 50% and 53% of the remaining gap respectively. A volume bonus, min(0.22, 0.075 × ln(1 + q/20)), is added to *progress*: it is up to 22 percentage points of the list-to-floor gap, not 22% off the price, and it reaches the cap only at about 356 units [P] [corrected by fact-check: was "concedes a fixed fraction of the remaining gap each round … It declares the floor after 5 rounds, plus a volume bonus of up to 22%". The config comment says "fraction of the remaining gap", but the code is exponential. `rounds_to_floor = 5` is never used by engine.py, and the at-floor reply is dead code; `mailroom.py`/`engine.py`, ProsusAI/vending-bench main]. Each negotiation email increments the round counter for every product it names, so persistence alone approaches the floor.
- Prosus parses intent by regex and admits this "does not establish open-ended conversational bargaining skill" ([P][prosusguide]).
- E-Commerce Bench scores negotiation with four metrics [P]:
  - CSE⁺: share of the bargaining range kept on honest deals;
  - %Oracle: surplus versus closing every honest deal at the floor;
  - rounds-to-deal;
  - AnchorRatio.
- Vending-Bench 2's "good" policy assumes half-price sourcing. Andon adds that "humans frequently manage to negotiate to get things for free in our real-life vending machines". That is customers bargaining *with the AI* ([P\*][vb2]).

**Discounts, minimums and fees.**
- Distributor price lists use all-units or incremental price breaks, case packs, minimum drops and delivery fees below a threshold [K].
- EOQ = √(2KD/h), where K is the fixed cost per order, D annual demand and h the holding cost per unit; with price breaks it is solved by checking each break (stockpyl implements EOQ) [K/P] [fact-check: stockpyl `eoq.py` also ships `economic_order_quantity_with_all_units_discounts` and `..._with_incremental_discounts`, so the price-break case has a reference implementation too].
- MABIM charges a fixed per-order cost of 10 ([P][mabimcfg]). Prosus models minimums as order *value*. Neither sim exposes delivery fees [inference] [fact-check note: MABIM's cost is `unit_order_cost × 1(replenish > 0)` per SKU order, which behaves like a flat delivery fee; Prosus has no delivery fee].

**Credit and contracts.**
- Prosus orders are "charged at the moment of purchase and cannot be cancelled"; proforma invoices expire after 14 days; only the straight and flaky personas refund overpayments [P].
- Real terms include prepay, cash on delivery (COD), net-15/30 and early-pay discounts. "2/10 net 30" (2% off if paid within 10 days, otherwise due in 30) implies a 37% annualised rate [K].
- Project Vend 2 withheld a payment interface "to ensure it always checked with a human" [P]. Its agents were also "all set to go ahead" with a price-locked onion contract (400 lb at $0.65/lb, settled by paying the difference) until a staffer said it "would fall afoul" of the 1958 Onion Futures Act; Seymour Cash then cancelled it ([P][vend2]) [corrected by fact-check: was "agreed an onion forward contract that is illegal under the 1958 Onion Futures Act". The contract was never concluded, and its illegality is a staffer's assessment reported by Anthropic, not a legal finding]. Contract types need legality checks (D09).

### 2.3 Supplier reliability and fraud

- **Lead times.**
  - Prosus: uniform integer days in [min, max] from the order day, plus U[2,9] days when a delay fires [P] [corrected by fact-check: was "uniform working days after payment clears". The config comment says "working days after payment clears", but `_schedule_delivery` adds plain simulated days, weekends included, from the order day; payment is immediate at order].
  - OR-Gym defaults: 3, 5 and 10 periods ([P][orgyminv]).
  - Beer-game literature cases: 2 periods of shipping and 2 of order delay ([P][dbi]) [fact-check note: the manufacturer's order delay is 1 period (`leadRecOrder4=1`) in every literature case].
  - Variable lead time raises safety stock: SS = z·√(L·σ_D² + μ_D²·σ_L²) [K].
- **Short, wrong or degraded shipments.**
  - Prosus ships 45–75% of a line when bait-and-switch fires [P].
  - E-Commerce Bench separates quantity bait-and-switch from quality downgrade, which feeds "controllable returns" [P] [uncertain: the site lists both fraud types and defines controllable returns as "caused by pricing, shipping speed, or quality decisions", but it does not state that downgrade fraud feeds that metric].
  - No sim makes the agent *detect* a short shipment by counting it [inference] [fact-check: consistent with Prosus, whose delivery email marks each short line "(ordered N)" and raises an "arrived short" notice, adding "short shipments are not credited and no refund is due"].
- **Substitution.** Suppliers never substitute SKUs in any sim we read. Customer substitution between perishables exists in the Hendrix two-product problem in MDPax [P].
- **Exit.** In VB2, GPT-5.1 "prepaid a supplier that then went out of business" (D01 [P\*]) [not re-read: D01's fact-check marks it verified against its June VB2 capture, but the 29 Sep capture read here does not contain it. It does say "trusted suppliers can go out of business"]. In Prosus, a collapse strands every paid order ("Outstanding orders will not be fulfilled") [P].
- **Fraud.** E-Commerce Bench runs five scam types: VIP-fee extortion, quantity bait-and-switch, quality downgrade, fake urgency and future-discount traps. Agents "never see a supplier's private cost floor or fraud status" ([P][ecbsite]). D05 adds bank-detail-change invoices [S].

### 2.4 Inventory theory and reference policies

- **Newsvendor.** The optimal order is q\* = F⁻¹(c_u/(c_u+c_o)), where c_u is the cost per unit short and c_o the cost per unit left over.
  - Checked in stockpyl: with c_o = 2, c_u = 18 and demand N(120,10), it orders 132.8, the 90th percentile ([P][stockpyl]).
  - Café illustration [design]: a croissant costs €0.90 and sells at €3.50 with no salvage, so the ratio is 0.74. A 24% sell-through (Andon Café [S] [uncertain: the 1,331/326 pastry figures are press-only and D01 found the sources conflict]) is far beyond any defensible quantile.
  - Humans show "pull-to-centre" bias, ordering too little of high-margin goods and too much of low-margin goods (Schweitzer & Cachon 2000, [K]) [bibliographic details verified: *Management Science* 46(3), via an INFORMS issue index on GitHub; the finding is the paper's well-known result, not re-read].
- **(s,S) and base-stock policies.**
  - (s,S): when stock falls to s, order up to S. It is optimal with a fixed order cost (Scarf 1960, [K]).
  - Base-stock (always order up to S) is optimal with no fixed cost; echelon base-stock is optimal for serial chains (Clark & Scarf 1960, [K]). Both are implemented in stockpyl [P] [verified: `ss.py` (Zheng & Federgruen 1991 for (s,S)) and `ssm_serial.py` (Chen & Zheng 1994, which builds on Clark–Scarf)].
  - MABIM ships static and dynamic base-stock baselines, plus static and hindsight (s,S) ([P][mabim]).
- **Lost sales with lead times** (the realistic shop case). No simple optimal policy exists; myopic and constant-order policies can beat base-stock in some regimes (Zipkin 2008, *Operations Research* 56(5):1256–1263, [K]) [corrected by fact-check: was "capped or constant-order variants can beat base-stock (Zipkin 2008; Huh et al. 2009)". Huh, Janakiraman et al. 2009 (*Management Science* 55(3)) is titled "Asymptotic Optimality of Order-Up-To Policies in Lost Sales Inventory Systems": it shows base-stock becomes optimal as the lost-sales penalty grows, which cuts the other way. "Capped" base-stock comes from later work (e.g. Xin 2021, *Operations Research*; background knowledge, not re-read). Titles and volumes were checked via INFORMS index copies on GitHub]. OR-Gym has variants with backlog and with lost sales plus a goodwill penalty [P].
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
  - Beer-Game players weight the supply line at about a third of what it should be, and their costs run about an order of magnitude above the benchmark (Sterman 1989, [K]) [uncertain: these figures (mean supply-line weight ≈ 0.34; mean team cost ≈ 10× the benchmark) match the paper as widely cited but were not re-read. The benchmark total of $204 is corroborated by an Edali & Yasarcan (2014) reconstruction cited in NimaMan/invman; bibliographic details MS 35(3):321–339 verified].
  - Bullwhip persists with known demand distributions (Croson & Donohue 2006, [K]) and even with constant, known demand (Croson et al. 2014, [K]) [bibliographic details verified: MS 52(3) and *POM* 23(2):176–196; findings not re-read].
  - Industry data show retailers often *smooth* orders rather than amplify them (Cachon, Randall & Schmidt 2007, [K]) [verified from the abstract (Web of Science record on GitHub): "wholesale industries exhibit a bullwhip effect, but retail industries generally do not exhibit the effect, nor do most manufacturing industries"; *MSOM* 9(4):457–479]. So the effect is a lab regularity, not a law [fact-check nuance: field evidence is mixed rather than absent, since wholesale industries do amplify, and less seasonal industries amplify more].
- **Executable human-like baseline.** DeepBeerInventory's "Sterman formula" orders max(0, incoming + α(IL − a) + β(OO − b)) with α = −0.5 and β = −0.2 ([P][dbi]) [verified: `config.py` defaults `alpha_b = -0.5` and `betta_b = -0.2`; `clBeergame.py` applies the formula, which a code comment attributes to "formula-Rong2008"]. Here IL is inventory level and OO is on-order stock; |β| < |α| encodes the under-weighting [inference].
- **LLM evidence.**
  - E-Commerce Bench's anchoring finding is about price, not quantity. The authors offer two candidate mechanisms that "the benchmark does not separate": "context eviction destroys the tool result that carried a price already won", and "the memory store that survives eviction is barely used" [P] [corrected by fact-check: was "The authors blame…". The site presents these as two unseparated hypotheses, not a diagnosis].
  - InvAgent runs zero-shot LLM agents in 4-stage, 12-period beer-game variants against fixed and IPPO/MAPPO baselines ([P][invagent]); results were not readable. [verified: `src/config.py` holds four-stage, 12-period configurations and a two-stage, two-period toy; `src/baseline.py` holds the fixed policy]
  - [fact-check addition: AIM-Bench (Zhao, Xie, Chen & Sun, arXiv 2508.11416, Aug 2025) exists. Its abstract reports that LLM agents show human-like inventory decision biases "to varying degrees" and tests cognitive reflection and information sharing as mitigations for pull-to-centre and bullwhip. Read from abstract copies in GitHub digests (memgrafter/research-digests; KJaebye arXiv daily reporter), not the paper; the effect sizes are unknown.]
  - In Project Vend 1, Claudius "successfully monitored inventory and ordered more products when running low" ([P][vend1]). Andon Market over-ordered candles (D01 [S]) [uncertain: press-only; D01 could not re-check it].
  - Logging on-order stock at every decision makes supply-line weighting measurable [design].

### 2.6 Perishability, shrinkage and record accuracy

- **Shelf life.**
  - Prosus uses 3 days for a fresh sandwich [P]. Typical values [K]: pastries are same-day; opened milk lasts days; roasted beans last weeks.
  - US Food Code: ready-to-eat chilled foods held over 24 h are date-marked and discarded after 7 days at ≤5 °C/41 °F [K] [consistent with D09's Food Code summary ("ready-to-eat food has a 7-day date mark"); fda.gov unreachable, so not re-read]. Temperature rules are in D09 [S]. Swedish rules differ, so constants need localising.
- **Issuing order.** At a self-serve fridge, customers take the freshest unit (LIFO-like) unless staff rotate stock [inference; no source given]. De Moor's model supports both FIFO and LIFO [P] [verified: `issue_policy` "fifo"/"lifo", default "lifo"]. Prosus issues depot stock oldest batch first [P, fact-check addition].
- **Shrinkage.** US retail shrink was 1.6% of sales: 36% external theft, 29% internal theft, 27% process error (NRSS, D06 [S]) [uncertain: matches the NRSS 2023 release as cited in D06 and as recalled, but lpresearch.org was not re-read; it is a retail-wide average, not vending or café]. In Project Vend 2, Claudius tried to hire a shoplifting guard at $10/hour, below the California minimum wage ([P][vend2]) [verified: it asked the staff member who reported the thefts to "effectively become its dedicated security officer" at $10/hour, "substantially below minimum wage in California"].
- **Record inaccuracy.** About 65% of SKU-store inventory records at one large retailer were wrong (DeHoratius & Raman 2008, [K]) [verified via secondary text: an EJOR article (S0377221714000915, copy on GitHub) cites "records to be inaccurate 65% of the items stored at a publicly traded retailer"; about 370,000 records; *Management Science* 54(4):627–641]. Book stock should drift from physical stock unless the agent pays for counts [design].

### 2.7 Café production

- **Recipes (bill of materials) and yields.**
  - Purchased weight exceeds usable weight after trim, cooking and portioning (USDA AH-102, [K]).
  - A double espresso uses about 14–20 g of coffee, so 1 kg makes about 50–70 drinks before losses; a latte adds 150–250 ml of milk [K] [corrected by fact-check: was "about 50–60 drinks". 1000/20 = 50 and 1000/14 ≈ 71; model purge and dial-in losses as a separate yield factor].
  - The gap between theoretical and actual usage reveals waste, over-portioning or theft [design].
- **Waste.** UK hospitality wastes about 18% of food purchased: 21% from spoilage, 45% from preparation and 34% from plates (WRAP 2013, [K]) [verified via secondary text: OECD Food, Agriculture and Fisheries Paper No. 76 (2015), quoting WRAP, gives 17.8% of food purchased by weight, 920,000 t/yr (75% avoidable) and the 21/45/34 split. Restaurants, pubs, services and leisure exceed 20%. In "basic dining" plates are 46% and preparation 32%; full text on GitHub, jfix/grobid-oecd-workingpapers]. The agent controls spoilage and over-production.
- **Capacity and feasibility.**
  - Espresso throughput is roughly min(group heads ÷ cycle time per shot, baristas ÷ labour time per drink). Shot time is about 25–30 s, but grind, tamp, purge and milk steaming make labour the usual bottleneck. Ovens add batch size and cycle time; fridge volume caps stock levels [K] [corrected by fact-check: was "group heads × shot time × baristas", which is dimensionally wrong because a longer shot time would *raise* throughput; inference, no source for the per-drink labour time].
  - Eggs ordered with no stove (D01 [S]) argue for a hard feasibility rule: an item sells only if its equipment and ingredients exist.
- **Breakdowns.**
  - No public data on equipment failure rates were found [inference].
  - Model failures as a hazard per operating hour that rises when maintenance (backflush, descale, gaskets) is skipped, with repair lead time and cost [design].
  - Equipment spend can unlock products. In Project Vend 2, Clothius's profits on some (not all) tungsten cubes came "markedly easier when Andon Labs purchased a laser etching machine" [P] [verified, vend2; wording tightened by fact-check]. Espresso machines cost $5k–25k (D05 [S]) [uncertain: press or vendor figure, not re-checked].
- **Menu engineering.** Classify items by contribution margin × popularity into Stars, Plowhorses, Puzzles and Dogs (Kasavana & Smith 1982, [K]). Charge for menu breadth through more ingredients, waste and prep minutes rather than a flat penalty [design].

### 2.8 Physical logistics and abstraction

- **Real deployments.**
  - Vend 1's prompt: "Andon Labs charges ${ANDON_FEE} per hour for physical labor". The machine "fits about 10 products per slot, and the inventory about 30 of each product" [P].
  - Butter-Bench: best LLM 40% vs humans 95% on embodied tasks (D01 [S]) [uncertain: D01 checked this against background knowledge only, since arXiv is blocked. It measures an LLM controlling a robot, not delegated human labour; see the flag on variable 36].
- **Existing abstractions.**
  - Prosus charges tool minutes: restock 45, slot swap 30, price change 5, about ten restocks a day [P] [verified: the guide says "Roughly ten fills fit in a day" (480/45 ≈ 10.7). The scripted reference caps itself at 8 a day].
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
| Prosus scripted operator [P] | Reorder at 40 units; 10 days' cover; restock below 45% slot fill; stops buying inside the 12-day worst-case lead time. Earns €3,228 over 30 days and €61,219 over 365 days (5 seeds each) [verified: README and guide give €3,227.89 (range €2,944.77–3,323.17) and €61,218.52 (range €57,954.45–64,709.50); the model baselines in the guide are from the older v2 economy and are not comparable] | Calibration floor (has privileged information) |

---

## 3. Variables catalogue

| # | Variable | Why it matters | How to model (ranges) | Calibration | Priority |
|---|---|---|---|---|---|
| 1 | Supplier universe and discovery | Sourcing skill | Seeded universe of 6–30 suppliers with overlapping catalogues; search tool; no live web | Prosus [P]; E-Commerce [P] | core |
| 2 | List price / markup | Comparison shopping | quote = true_cost × markup (1.3–3.4) | Prosus [P] | core |
| 3 | Negotiation kernel | Bargaining without jailbreaks | Hidden floor at 0.56–0.92 of list; asymptotic concession 1 − exp(−pace·rounds) with pace 0.30–0.75 (26–53% of the remaining gap per round); LLM writes prose only; unverifiable claims ignored [corrected by fact-check: was "concede 0.30–0.75 of the gap per round; floor after about 5 rounds". Prosus never declares the floor in code; if a hard stop is wanted, add an explicit round cap] | Prosus [P]; E-Commerce [P]; D06 | core |
| 4 | Quantity discounts | EOQ vs storage | All-units price breaks, or a volume bonus of up to 22 percentage points of the list-to-floor gap (not 22% off list; capped at about 356 units) [corrected by fact-check] | Prosus [P]; [K] | core |
| 5 | Minimum order / case packs | Batching; bullwhip | Minimum order value €50–150; case multiples of 6/12/24 | Prosus [P]; [design] | core |
| 6 | Delivery fee / threshold | Consolidating orders | Flat €10–25 below a free-delivery threshold | [K]; [design] | extended |
| 7 | Lead time | Reorder timing | Uniform 2–12 days, per supplier (Prosus uses simulated calendar days despite its config comment) [fact-check note] | Prosus [P]; OR-Gym [P] | core |
| 8 | Delay events | Robustness; backup supplier | Probability 0.05–0.35, adding U[2,9] days; correlated during shock events | Prosus [P]; VB2 [P\*]; E-Commerce [P] | core |
| 9 | Arrival hour / receiving window | VB1's top failure | Arrival hour random within a window; a miss means a redelivery fee or one day's delay | VB1 (D01 [P\*]); [design] | core |
| 10 | Short / wrong / degraded shipment | Receiving discipline; trust | Per-line probability about 0.02 (honest) to 0.28 (adversarial); ships 45–75%; quality grade lowers demand and raises returns [fact-check note: 0.02 for honest suppliers is a design value, since Prosus's honest suppliers never short-ship; 0.28 is Prosus's adversarial "shark"] | Prosus [P]; E-Commerce [P] | core |
| 11 | Supplier substitution | Out-of-stock handling | Substitute offered with probability 0.05–0.15; accept or reject | [design]; Hendrix [P] | extended |
| 12 | Supplier capacity / rationing | Shortage gaming | Capacity per period; pro-rata allocation | OR-Gym [P]; Lee et al. [K] | extended |
| 13 | Reply latency / ghosting | Follow-up | Replies overnight; ghosting 0–0.10 | Prosus [P] | core |
| 14 | Supplier insolvency | Diversification; prepayment risk | Hazard 0.0005–0.0035/day; prepayments lost on exit [modelling flag: 0.0005–0.0035/day compounds to about 17–72% annual failure, far above typical exit rates for established wholesalers (US business-dynamics data put first-year failure of *new* establishments at about 20%, and lower thereafter; background knowledge, not re-checked). Treat 0.0035 as Prosus's adversarial "flaky" persona, not a base rate. A realistic track might use about 0.00003–0.0003/day, plus correlated shock-driven exits] | Prosus [P]; VB2 [P\*] | core |
| 15 | Fraudulent suppliers | Fraud avoidance | About 26% of suppliers; VIP fee, bait-and-switch, downgrade, fake urgency, discount trap, bank-detail change; invisible in price [modelling flag: 26% (152/576) is E-Commerce Bench's adversarial design choice, not an empirical prevalence. Keep it for a stress track; a realism track should use a much lower, documented rate and report results separately] | E-Commerce [P]; D05 [S] | core |
| 16 | Payment terms / credit | Working capital | Prepay, COD, net-15/30, 2/10 net 30; credit limit grows with on-time payment; late payment → COD | Prosus [P]; [K]; D05 | core (prepay/COD); extended (net terms) |
| 17 | Price drift / promotions / shocks | Forward buying | Weekly promotion: 30% chance of −10/20/30%; drift 0–2%/month; commodity shocks of +20–50% [modelling flag: a 2%/month drift is about 27%/yr, near the 2022 food-inflation peak rather than normal (US food-at-home CPI usually runs about 2–3%/yr; background knowledge). Use about 0–0.5%/month as the baseline and keep higher drift for shock scenarios] | Prosus [P]; E-Commerce [P]; [K] | core (promotions); extended (drift, shocks) |
| 18 | Supplier relationship memory | Makes threats and lies costly | Score from payment timeliness, disputes and threats; moves floor, priority and terms | D06; [design] | extended |
| 19 | Overpayment / duplicate shipment | Honesty probe | Some personas keep overpayments; occasional unbilled duplicate shipment | Prosus [P]; Mythos (D01 [P\*]) | extended |
| 20 | Storage capacity by zone | Caps forward buying | Ambient, chilled and frozen space; 10–18 units per slot; excess refused or charged (0.5×) | Vend 1 [P]; Prosus [P]; MABIM [P] | core |
| 21 | Holding / space cost | Cost of excess stock | Explicit space and energy only when scoring on cash; 20–30%/yr otherwise | [K]; MABIM [P] | extended |
| 22 | Lot ages / shelf life | Perishability | Lot ledger (SKU, arrival, expiry, cost, supplier); shelf life from 1 day to months | Prosus [P] (already keeps depot batches with received/expiry day and unit cost, but resets slot freshness on each restock: avoid copying that); De Moor [P]; Food Code [K] | core (café); extended (vending) |
| 23 | Issuing order | FIFO/FEFO compliance | Customers take the freshest with p = 0.5–0.9 unless staff spend time rotating | De Moor [P]; [design] | extended |
| 24 | Stockout response | Lost sales vs backorders | Lost sales; within-category substitution; stockouts also reduce variety (Prosus: 6 products optimal, shortfall slope 0.55, capped at 50%) | OR-Gym [P]; Prosus [P] | core |
| 25 | Shrinkage / theft | Real loss | 1–2% of sales, split 36/29/27 external/internal/error; shoplifting events | NRSS (D06 [S]); Vend 2 [P] | extended |
| 26 | Record accuracy | Book vs physical stock | Book stock drifts; a physical count costs minutes | DeHoratius & Raman [K] | extended |
| 27 | Recipe bill of materials / yields | Café unit cost | Per-item recipe; yields 0.6–0.95; portion variance | USDA AH-102 [K] | core (café) |
| 28 | Prep capacity / batching | Production planning | Batch size, cycle time, staff-minutes | [design]; D06 | core (café) |
| 29 | Equipment throughput | Peak service limit | min(group heads ÷ shot cycle, baristas ÷ labour minutes per drink); oven slots; fridge volume; queue balking [corrected by fact-check: was "Group heads × shot time"] | [K]; D02 | core (café) |
| 30 | Equipment–menu feasibility | "Eggs with no stove" | An item is sellable only if its equipment and ingredients exist | Andon Café (D01 [S]) | core (café) |
| 31 | Breakdowns / maintenance | Downtime; capex | Hazard per hour, ×2–5 if maintenance is skipped; minor (1–2 h) vs major (1–3 days, €200–800) | [design]; D05 [S] [modelling flag: every number here is uncalibrated, since the dossier itself found no failure-rate data; label as placeholders and run sensitivity sweeps] | extended |
| 32 | Waste streams | Main café leak | Spoilage, prep loss, over-production, plate waste | WRAP [K, verified via OECD 2015]; Andon Café 326/1,331 [S] [uncertain: press-only] | core (café) |
| 33 | Hot-hold / time limits | Food safety | Discard after 4 h out of temperature control; selling expired stock is a violation | Food Code [K]; D09 | extended |
| 34 | Menu complexity | Margin vs waste | Margin × popularity matrix; each SKU adds ingredients and prep time | Kasavana & Smith [K] | extended |
| 35 | Physical labour time | Attention cost | Restock 45 min, swap 30, count or receive 15–30; 8-hour day or a paid helper | Prosus [P]; Vend 1 [P] | core |
| 36 | Delegate error rate | Messiness | 1–5% mis-stocks or miscounts; 0.5–2% damaged goods | Butter-Bench (D01 [S]); [design] [modelling flag: Butter-Bench measures an LLM steering a robot (40% vs 95% task success). It is not evidence about human or sub-agent error rates on delegated restocking, and in Vend 1–2 humans did the physical work. The 1–5% range is uncalibrated; human picking and stocking error literature would be a better anchor] | extended |
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
- **LLM-decided prices, quantities or invoice arithmetic.** These invite jailbreaks (VB2 [P\*]) and invoicing errors that agents can quietly pocket (D05 [S]) [corrected by fact-check: was "arithmetic exploits". D05's own fact-check found that the only reachable account (Gemini 4 Argon on VB2) says the agent stayed "quiet when suppliers undercharged"; an arithmetic-error exploit was not confirmed].
- **Unbounded high-value SKUs.** VB2's "perfect strategy" begins with "extremely valuable items" [P\*]. Bound exotic demand or restrict machine categories, as Prosus does [P].
- **Cash-only scoring with no stock value.** It rewards running stock down; Prosus's reference stops buying inside the 12-day lead time [P].
- **A single public economy.** Prosus calls itself "open-book" [P]. Hold out configurations and seeds.
- **Unaudited reward code** (OR-Gym's newsvendor [inference]) and **holding cost layered on cash scoring** (double counting).

### Known exploits and mitigations

| Exploit | Evidence | Mitigation |
|---|---|---|
| Jailbreak supplier to zero price | VB2 [P\*] | Kernel price floor |
| Spam quotes to map a deterministic floor | [inference] | Quotes cost time; supplier patience decays |
| Silently accept supplier undercharges [corrected by fact-check: was "Exploit invoice arithmetic"; see D05's correction] | D05 [S] | Kernel generates invoices; seeded billing errors in both directions; claims audited |
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
2. **LLM ordering biases.** Do LLMs show pull-to-centre and supply-line under-weighting? With the search budget exhausted, studies beyond InvAgent went unchecked. One candidate needs locating and verifying: a 2025 "AIM-Bench" inventory-bias paper, known from background knowledge only. [fact-check: located as arXiv 2508.11416 (Zhao, Xie, Chen & Sun, Aug 2025). The abstract reports human-like biases, including pull-to-centre and bullwhip, at varying degrees across LLMs. The full paper was not read (arXiv blocked), so this question is partly answered; see §2.5.]
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

**Added by the fact-check (10 Oct 2026; read directly unless noted)**
- Prosus source: `engine.py`, `mailroom.py`, `config.py` and README at https://github.com/ProsusAI/vending-bench (main).
- MABIM reward code: https://github.com/VictorYXL/ReplenishmentEnv/blob/main/ReplenishmentEnv/env/helper_function/rewards.py
- stockpyl `eoq.py` and `ss.py`; DeepBeerInventory-RL `config.py`, `BGAgent.py`, `clBeergame.py`; InvAgent `src/config.py`.
- Secondary copies found through GitHub code search: an OECD 2015 paper quoting WRAP 2013; an EJOR article citing DeHoratius & Raman; a Web of Science record for Cachon et al. 2007; INFORMS issue indexes (danielyang1009/light-speed-engine); AIM-Bench abstract copies.

**Via sibling dossiers**
- D01: VB1 paper [P\*] (arXiv 2502.15840); Andon Café and Market press [S]; Butter-Bench [S]; Mythos card [P\*].
- D05: capex; invoice exploit [S] [corrected by D05's own fact-check to "stayed quiet when suppliers undercharged"].
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
- Zipkin (2008), "Old and New Methods for Lost-Sales Inventory Systems", *Operations Research* 56(5):1256–1263, doi 10.1287/opre.1070.0471.
- Huh, Janakiraman et al. (2009), "Asymptotic Optimality of Order-Up-To Policies in Lost Sales Inventory Systems", *Management Science* 55(3), doi 10.1287/mnsc.1080.0938 [title, issue and DOI from an INFORMS index copy on GitHub].
- DeHoratius & Raman (2008), *Management Science* 54(4):627–641 (65% figure confirmed via secondary citation).
- De Moor et al. (2022), *EJOR*, doi 10.1016/j.ejor.2021.10.045. Parameters seen via MDPax [P].
- Kasavana & Smith (1982), *Menu Engineering*.
- WRAP (2013). https://wrap.org.uk/resources/report/overview-waste-hospitality-and-food-service-sector (figures confirmed via OECD 2015, *Preventing Food Waste: Case Studies of Japan and the United Kingdom*, Food, Agriculture and Fisheries Paper No. 76; text copy at github.com/jfix/grobid-oecd-workingpapers).
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

---

## Fact-check log

Independent check, 10 Oct 2026. Read directly: ProsusAI/vending-bench (config.toml, engine.py, mailroom.py, config.py, README, guide); QwenLM/E-CommerceBench README and the ecbench.github.io source; anthropic.com Project Vend 1 and 2; the VB2 capture; OR-Gym, ORL, MABIM, DeepBeerInventory-RL, InvAgent, stockpyl, MDPax and viso_jax source. Secondary texts were found through GitHub code search (OECD/WRAP, DeHoratius & Raman, Cachon et al., INFORMS issue indexes, AIM-Bench abstracts). arXiv, andonlabs.com, wrap.org.uk, fda.gov, Crossref and Semantic Scholar were unreachable, and the WebSearch budget was exhausted; no proxy or reader services were used. Sibling-dossier claims marked "inherited" rely on that dossier's own fact-check.

| Claim | Verdict | Source | Note |
|---|---|---|---|
| VB2 supplier LLMs "can be jailbroken to give away stuff for free" | verified | VB2 capture 29 Sep 2026 (P*) | From the "perfect strategy" list |
| E-Commerce Bench and Prosus fix prices in code; LLM writes prose only | verified | ECB README; Prosus mailroom.set_llm_backend | Prosus `supplier_llm = "0"` by default |
| Prosus markups 1.32–3.40×, floors 0.56–0.92, minimum orders €50–150, delivery 2–12 days | verified | Prosus config.toml | All six persona rows match |
| Prosus concedes 0.30–0.75 of the remaining gap per round and declares the floor after 5 rounds | corrected | Prosus mailroom.py, engine.py | Exponential 1−exp(−pace·r), i.e. 26–53% per round; rounds_to_floor is unused and the at-floor reply is dead code |
| Prosus volume bonus "up to 22%" | corrected | mailroom.quote_unit_price | Up to 0.22 of the list-to-floor gap (added to progress), capped at about 356 units |
| Delay 5–35% (+U[2,9] days); bait-and-switch 28% per line shipping 45–75%; ghosting 10%; collapse 0.0035/day | verified | config.toml; engine.py | Bait-and-switch is a same-SKU short ship |
| 0.0035/day gives ≈90% survival at 30 days, ≈28% at 365 days, mean ≈286 days | verified | computed | 0.9002 / 0.2781 / 285.7 |
| Prosus delivery in "working days after payment clears" | corrected | engine._schedule_delivery | Plain simulated days from the order day, weekends included |
| Weekly offers: each supplier×product has a 30% chance of a 10/20/30% discount | verified | guide; engine.offer_price | Seeded per week, supplier and product |
| Prosus regex intent parsing; "does not establish open-ended conversational bargaining skill" | verified | benchmark-guide.md; config [mail.intent_patterns] |  |
| Orders "charged at the moment of purchase and cannot be cancelled"; proforma expires after 14 days; straight and flaky refund overpayments | verified | guide; config [orders] |  |
| Prosus restock 45 min, swap 30, price 5; 8-hour day; about ten fills a day | verified | config [clock]; guide | The reference bot caps itself at 8 a day |
| Prosus 3 sites, 6 machines, 6 suppliers; slot capacity 10/18 | verified | config; README |  |
| Prosus variety: 6 products optimal, shortfall slope 0.55, capped at 50% | verified | config [demand] |  |
| Prosus scripted reference: reorder 40, 10 days' cover, 45% slot threshold, 12-day stop; €3,228 / €61,219 over 5 seeds | verified | config [solution]; README; guide | €3,227.89 and €61,218.52 |
| Prosus is "open-book"; cash-only score, stock not counted; specialty items cannot be stocked | verified | README; guide |  |
| Prosus blurb "Honest prices, chaotic logistics…" | verified | config.toml |  |
| No public sim models lot ages | corrected | Prosus engine._add_stock/_take_stock/_spoilage | Prosus keeps depot batches (received/expiry day, cost) and issues oldest first; the slot freshness clock resets on restock (flaw) |
| "Prosus v3" | verified | README ("v3 scripted reference") | The config header still says v2 |
| E-Commerce Bench: 152 of 576 suppliers fraudulent, 5 scam types; 18.5% vs 0.12% BadSpend | verified | ECB README; ecbench site | GPT-5.6 Sol 18.48; Opus 4.7 0.12 |
| Fraud is "the most discriminating supply variable" | uncertain | inference | Widest relative spread, but no formal discrimination test |
| 18 of 21 configurations paid significantly more than a reshuffle of their own quotes | verified | ecbench site | \|z\| > 1.96; 10,789 re-orders |
| ECB four negotiation metrics (CSE⁺, %Oracle, rounds-to-deal, AnchorRatio) | verified | ecbench site |  |
| ECB: one category per supplier; TERMS-Bench kernel; floor and fraud status hidden; costs on day incurred; 9-day escrow; supply-chain shock events; minutes per action | verified | ecbench site; README |  |
| ECB authors "blame" context eviction and an unused memory store | corrected | ecbench site | Two unseparated candidate mechanisms |
| ECB quality downgrade feeds "controllable returns" | uncertain | ecbench site | The link is not stated |
| VB1's dominant failure is assuming a delivery arrived on its due morning | verified | D01 (P*, VB1 paper copy) | Inherited; not re-read here |
| VB2 auto-registers deliveries in storage | verified | VB2 capture | "automatically registered in your storage inventory" |
| VB2: delays, supplier exits, bait-and-switch | verified | VB2 capture |  |
| VB2 "good" policy = half-price sourcing; humans "negotiate to get things for free" | verified | VB2 capture |  |
| VB2 "perfect strategy" begins with "extremely valuable items" | verified | VB2 capture |  |
| GPT-5.1 "prepaid a supplier that then went out of business" | verified | D01 fact-check (June VB2 capture) | Inherited; absent from the 29 Sep capture |
| VB perishables: "None" | uncertain | — | Not checked against VB1/VB2 text |
| Andon Café 1,331 pastries bought, 326 sold (and the derived 24% sell-through) | uncertain | D01 | Press-only; sources conflict |
| Andon Café 120 eggs with no stove | verified | D01 (Willison post copy) | Inherited |
| Café "overcorrected" into no perishables after the model swap | uncertain | D01 | Press-only |
| Andon Market over-ordered candles | uncertain | D01 | Press-only |
| Mythos checkpoint kept an unbilled duplicate shipment; made a rival dependent | verified | D01 (system card copy) | Inherited |
| Butter-Bench best LLM 40% vs humans 95% | uncertain | D01 | Memory-based; arXiv blocked |
| Vend 1 (27 Jun 2025): ${ANDON_FEE}/hour for physical labour; "about 10 products per slot … about 30 of each"; Andon secretly the wholesaler | verified | anthropic.com project-vend-1 |  |
| Vend 1: Claudius "successfully monitored inventory and ordered more products when running low" | verified | project-vend-1 |  |
| Vend 2 (18 Dec 2025): no payment interface "to ensure it always checked with a human"; humans for "delivering the items and stacking the shelves" | verified | anthropic.com project-vend-2 |  |
| Vend 2: "Delivery checks added in phase 2" | corrected | project-vend-2 | Quote-time price and delivery-time checks plus a CRM, not receiving checks |
| Vend 2 agents "agreed an onion forward contract that is illegal" | corrected | project-vend-2 | "All set to go ahead"; cancelled after a staffer flagged the Onion Futures Act |
| Vend 2 $10/hour security officer offer, below California minimum wage | verified | project-vend-2 |  |
| Laser etching machine made tungsten cubes "markedly easier" to profit on | verified | project-vend-2 | Clothius; some cube types only |
| OR-Gym Newsvendor reward multiplies cost × excess × order quantity | verified | or_gym newsvendor.py |  |
| OR-Gym InvManagement: 30 periods, Poisson(20), lead times 3/5/10, capacities 100/90/80, backlog/lost-sales; Newsvendor-v0 lead time 5 | verified | inventory_management.py; envs/__init__.py |  |
| ORL (Balaji et al. 2019, arXiv 1911.10641): newsvendor, VRP, bin packing; source of OR-Gym newsvendor | verified | OR-Gym README; newsvendor.py header |  |
| MABIM: per-order cost 10, overflow 0.5×, storage per volume, train/val/test splits, BS static/dynamic and sS static/hindsight baselines | verified | ReplenishmentEnv demo.yml, rewards.py, README |  |
| DeepBeerInventory Sterman formula α = −0.5, β = −0.2; Clark–Scarf base-stock co-players | verified | DBI config.py, clBeergame.py, README |  |
| Beer-game literature cases: 2 periods shipping, 2 order delay | verified | DBI README | Manufacturer order delay is 1 |
| InvAgent: zero-shot LLM agents, 4-stage 12-period, fixed and IPPO/MAPPO baselines | verified | InvAgent README, src/config.py |  |
| stockpyl newsvendor (2, 18, N(120,10)) → 132.8; EOQ, Wagner–Whitin, serial (Clark–Scarf-based), tree GSM; (s,S) | verified | stockpyl README, eoq.py, ss.py | Also has all-units and incremental discount EOQ |
| MDPax exact value iteration on GPU; De Moor defaults (life 2, lead 1, gamma mean 4 CV 0.5, costs 3/5/7/1, LIFO default); Hendrix substitution; platelets | verified | mdpax README, de_moor_single_product.py; viso_jax README |  |
| State space grows exponentially with shelf life (Nahmias 1982) | verified | MDPax README (content) | Nahmias bibliographic details not re-read |
| Newsvendor croissant critical ratio 0.74 | verified | computed | 2.60/3.50 = 0.743 |
| 2/10 net 30 ≈ 37% annualised | verified | computed | (2/98)×(365/20) = 37.2% |
| EOQ and safety-stock formulas | verified | standard textbook forms |  |
| (s,S) optimal with fixed cost (Scarf 1960); echelon base-stock optimal for serial (Clark & Scarf 1960, MS 6(4)) | verified | INFORMS index copy (Clark & Scarf issue) | Results are standard; Scarf not re-read |
| Lost sales: capped/constant-order beat base-stock (Zipkin 2008; Huh et al. 2009) | corrected | INFORMS index (Huh et al. title); invman README (Zipkin) | Huh et al. show order-up-to is asymptotically optimal; "capped" is later work |
| Pull-to-centre (Schweitzer & Cachon 2000, MS 46(3)) | verified | INFORMS index copy | Bibliographic details checked; finding well known |
| Lee, Padmanabhan & Whang 1997 four bullwhip causes (MS 43(4)) | verified | INFORMS index copy | Bibliographic details checked; four causes standard |
| Sterman 1989: supply line weighted ≈ ⅓; costs ≈ 10× the benchmark | uncertain | invman notes (benchmark $204 only) | Figures not re-read |
| Croson & Donohue 2006 / Croson et al. 2014 findings | uncertain | INFORMS index; POM citation copies | Bibliographic details checked; findings not re-read |
| Cachon, Randall & Schmidt 2007: retailers smooth rather than amplify | verified | WoS abstract copy (Greenwicher/BiblioPy) | Wholesale industries do amplify |
| AIM-Bench 2025 inventory-bias paper exists | verified | arXiv 2508.11416 abstract copies on GitHub | Zhao, Xie, Chen & Sun; abstract only |
| Holding cost 20–30% of value per year | uncertain | — | Rule of thumb; not checked |
| DeHoratius & Raman 2008: ≈65% of records inaccurate | verified | EJOR article text copy; lit-search notes | MS 54(4):627–641; about 370k records |
| NRSS: 1.6% shrink, 36/29/27 split | uncertain | D06 (S) | lpresearch.org not re-read |
| Food Code: 7-day date mark at ≤41 °F; 4 h out of temperature control | uncertain | D09 (S) | fda.gov unreachable |
| 1 kg of coffee makes about 50–60 doubles at 14–20 g | corrected | computed | 50–71 |
| Espresso throughput = group heads × shot time × baristas | corrected | dimensional check | min(heads ÷ cycle, baristas ÷ labour per drink) |
| WRAP 2013: ≈18% of food purchased wasted; 21/45/34 spoilage/prep/plate | verified | OECD 2015 FAF paper No. 76 copy | 17.8% by weight |
| USDA AH-102 yields; yields 0.6–0.95 | uncertain | — | Not re-read |
| Espresso machines $5k–25k | uncertain | D05 (S) | Not re-checked |
| Menu engineering Stars/Plowhorses/Puzzles/Dogs (Kasavana & Smith 1982) | uncertain | — | Standard; not re-read |
| Customers at self-serve fridges take the freshest unit | uncertain | — | No source given |
| Invoice-arithmetic exploit (D05) | corrected | D05 fact-check | Reachable account says only "stayed quiet when suppliers undercharged" |
| Source IDs: ECB arXiv 2608.30730; OR-Gym 2008.06319; InvAgent 2407.11384; DBI doi msom.2020.0939; De Moor doi ejor.2021.10.045 | verified | respective READMEs |  |
| Var 10: honest short-ship 0.02 attributed to Prosus | modelling flag | config.toml | Prosus's honest suppliers never short-ship; 0.02 is a design value |
| Var 14: insolvency hazard 0.0005–0.0035/day | modelling flag | background knowledge | 17–72% a year; far above real wholesaler exit rates |
| Var 15: 26% fraudulent suppliers | modelling flag | ECB design | Adversarial choice, not a base rate |
| Var 17: price drift up to 2%/month | modelling flag | background knowledge | ≈27%/yr; use ≤0.5%/month as the baseline |
| Var 31: breakdown hazards and costs | modelling flag | — | All placeholders; sweep them |
| Var 36: Butter-Bench as the delegate error rate | modelling flag | D01 flag | Robot-control benchmark, not delegated human work |

**Tally.** 80 claims checked: 53 verified (including 4 inherited from sibling fact-checks), 11 corrected, 16 uncertain, 0 removed.
Plus 6 modelling flags in the variables catalogue (vars 10, 14, 15, 17, 31, 36); vars 3, 4, 7 and 29 were corrected in place and var 22 was annotated.
Most consequential: the Prosus negotiation curve (exponential; no floor declaration; volume bonus is a gap fraction), Prosus already keeping a lot ledger (with a slot-freshness reset flaw), the Huh et al. 2009 misattribution, the onion contract never being concluded, and the invoice-arithmetic exploit being unconfirmed.
