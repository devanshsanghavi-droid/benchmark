# D02: Customer demand modelling for a shop and café simulation benchmark

Deep-dive dossier, 10 Oct 2026. Area D02 of the business-simulation deep dive. It covers how to make simulated customers realistic, fair to compare agents on, and hard to game.

**Source tags**
- **[P]** primary source read directly: official GitHub code or docs, anthropic.com posts, the M5 guide PDF.
- **[P\*]** primary text read through a verbatim copy hosted on GitHub.
- **[S]** seen only in search-engine snippets or press coverage.
- **[U]** background knowledge that could not be checked in this session. Verify before relying on it.
- **[design]** the author's own suggestion or calculation.

**Access note.** arxiv, andonlabs.com, Kaggle, NBER, INFORMS, SSRN, RePEc, PMC and publisher sites were blocked by network policy, and no proxies were used. Code was read from public GitHub clones. Academic results are mostly [S]. The shared web-search budget ran out mid-task, so a few classic values stay [U]. Prior repo notes were used as leads only.

---

## 1. Summary

1. **The Vending-Bench family treats each item separately.** VB1 sales = base sales × (1 + elasticity × % gap to reference price) × day-of-week × month × weather × a product-variety factor, plus noise [P\*]. VB2 "keeps the same sales simulation", and Andon says those equations "can be gamed" [P\*]. Open re-implementations (Prosus, aijnek, open-vending-bench) copy this shape [P].
2. **Known exploits come from missing customer choice.** These kernels have no substitution between items, no outside option (buying elsewhere or not at all), no customer memory, no moving reference prices and no switching when an item is out of stock. The result:
   - extreme markups on low-elasticity items;
   - adding SKUs adds sales;
   - "jackpot" high-value items;
   - any product sells, because demand ignores what it is;
   - end-of-episode fire sales;
   - marketing spam pays.
3. **Qwen's E-CommerceBench is the most hardened public kernel** [P]. Its patches: store demand that saturates; per-category caps ("anti-jackpot"); "anti-churn"; returns that rise when price exceeds reference; end-of-episode settlement; every constant-elasticity parameter ≥1.35, so no infinite-price optimum.
4. **Recommended kernel [design]:** a finite population of heterogeneous customers. Arrival over time → outside option → nested-logit choice → quantity → experience → memory (reference price, habit, satisfaction, reviews). RetailSynth is an open precedent calibrated on Dunnhumby data [P].
5. **Elasticity depends on aggregation level.** Food and beverage categories are inelastic (|e| 0.27–0.81) [S]. Brands are elastic (meta-analytic means ≈ −1.8 to −2.6 [U]). In vending, 10/25/50% price cuts raised low-fat snack sales by 9/39/93% [S]. Both levels emerge from an outside option plus substitution.
6. **Stockouts hide demand.** Demand estimated naively from vending sales is biased even when stockouts are rare [S]. Retail stockouts run about 8% and cost about 3.9% of sales [S]. Log demand that was not served; show agents sales only.
7. **Time patterns are well documented.** M5 [P] gives prices, events and intermittency. Office occupancy is about 55% midweek and about 32% on Friday [S]. Weather shocks shift sales with little catch-up later [S].
8. **Reputation and promotions matter and are omitted.** Half a Yelp star → +19 percentage points in sell-outs [S]. About 1 in 6 Yelp reviews were filtered [S]. Only about ⅓ of a promo bump is brand switching [S]. Heavy promotion raises long-run price sensitivity [S].
9. **In reality, humans game the agent.** Project Vend customers extracted discounts, free items and below-cost tungsten cubes [P]. Use LLM personas for haggling, but let a rule kernel decide what they buy.
10. **Price learning is slow at small-shop volume [design].** Detecting a 10% demand shift on a 10-unit/day SKU takes about 150–200 days per price arm. Hidden parameters must therefore come from realistic priors that match real-world knowledge.
11. **Use common random numbers [design].** Pre-generate customer arrivals and taste shocks from the seed, so every agent meets the same customers. This enables the paired scoring recommended in R2.

---

## 2. Findings

### 2.1 How existing AI business benchmarks model demand

| System | Demand kernel | Substitution / outside option | Memory and reputation | Notes |
|---|---|---|---|---|
| **Vending-Bench 1** [P\*] | GPT-4o caches each item's elasticity, reference price and base sales. Impact factor from % gap to reference. Day-of-week × month × weather × variety multiplier (penalty ≤50%). Noise, rounding, inventory cap. | None | None | Sonnet "figures out that it sells more on weekends, which is by design". |
| **Vending-Bench 2** [P\*] | Same as VB1, plus customers who email demanding refunds | None | Refund demands | Andon: a perfect strategy sources "extremely valuable items" and keeps "an optimal configuration" because the equations "can be gamed". |
| **Prosus Vending Bench** [P] | VB1 shape. Impact 1 + e·(p−r)/r, clamped to [0, 4]. Gaussian noise SD 0.18. Dutch holidays and month table. 5 weather states, multipliers per category (cold drinks ×1.75 hot; rain gear ×3.2 rainy). 3 sites differ in footfall (0.85–1.8×) and price sensitivity (0.75–1.5×). | Identical facings share one demand pool | Reputation floor 0.70 (−0.04 per open complaint). Marketing traffic capped at 1.35, with fatigue. | Shows "Yesterday's demand multipliers" to the agent. "Not fitted to real point-of-sale data". |
| **aijnek/vending_bench** [P] | Elasticity U(−2.5, −1.2), reference U($1.5, $4), base sales U(3, 12), seeded by product *name* | None | None | Product identity is ignored. |
| **open-vending-bench** [P] | An LLM is prompted for elasticity "−2.0 to −0.1"; the prompt includes the agent's *current price and stock*. | None | None | The agent's own actions anchor its "customers". |
| **E-CommerceBench** [P] | Deterministic. 60 categories, each with one of 4 price-response curve shapes, built on 6,886 desensitised real products. Weekend ×1.3, seasonality, events (winter storm: food ×2.0), promos (demand ×1.8–3.0, elasticity ×1.5–2.0). | Store saturation and category caps | Reputation from cumulative sales minus returns and cancellations. Returns rise with price above reference. | Code comments label the patches "B2 saturation", "B2c anti-jackpot", "S2 anti-churn", "E anti-gaming". |
| **RetailSynth** [P] | Per customer: visit → category (logistic) → product (multinomial logit with β·log price) → quantity. Markov discounts and coupons. Calibrated on Complete Journey. | Yes, via logit and nested attractiveness values | Lagged visits | Utility clipped "to avoid unreasonable large demand". |
| **Project Vend 1–2** (real) [P] | Anthropic staff ordering via Slack: "99% of your customers are Anthropic employees" | A free fridge sat beside $3 Coke Zero | Discount codes, "onion futures", gold-bar requests | A CEO agent cut discounts about 80%; refunds tripled. |

### 2.2 Exploits that simplistic demand curves allow

All [design] analysis of the code above unless tagged.

- **Huge markups.**
  - Under linear q = B(1 + e(p/r − 1)), the profit-maximising price is p\* = [r(1+|e|)/|e| + c]/2.
  - With e = −0.1 (allowed by open-vending-bench) and c = 0.5r: p\* = 5.75r, 52% of volume kept, 5.5× the profit made at the reference price.
  - Constant elasticity with |e| < 1 gives an infinite optimal price. E-CommerceBench keeps all such parameters ≥1.35 [P].
  - The missing constraint is an outside option.
- **Configuration gaming.** VB1's variety multiplier counts distinct products whatever they are [P\*]. Andon names keeping that configuration as part of a perfect strategy [P\*].
- **Jackpot and identity-agnostic items.** When parameters come from an LLM or a name-seeded random draw, an agent can source unusual or ultra-cheap goods ("extremely valuable items" [P\*]).
- **SKU stacking.** With independent items, adding SKUs adds sales. Prosus pools facings; E-CommerceBench saturates store demand and caps categories [P].
- **Horizon effects.** E-CommerceBench's end-of-episode settlement closes fire-sale escapes [P]. VB1 valued unsold inventory at cost [P\*]; VB2 and Prosus score cash only.
- **Marketing spam and disclosure.** Prosus adds saturation and fatigue, but message content barely matters [P]. It also shows the agent its demand multipliers [P].
- **Humans gaming the agent.**
  - Project Vend customers obtained discounts, giveaways and off-menu "specialty metal items".
  - Seymour Cash approved lenient requests about 8× as often as it denied them [P].
  - LLM counterparts can be jailbroken ([P\*], VB2 suppliers).
  - Magentic Marketplace found 10–30× first-proposal bias (R2 notes, not re-verified).

### 2.3 Price response: own and cross elasticities, reference prices, fairness

**Magnitudes**
- **Food categories** (160 US studies): |e| = 0.27–0.81. Food away from home, soft drinks, juice and meat are the most responsive (≈0.7–0.8). A 10% soft-drink price rise cuts consumption by 8–10% [S].
- **Brand level:** Tellis (1988, 367 estimates) mean ≈ −1.76 [U]; Bijmolt et al. (2005) ≈ −2.62 [U].
- **Cross-price:** mean 0.26, median 0.10 over 7,264 estimates. Larger for stockpilable groceries; declines over a product's life cycle [S].
- **CHIPS vending trial** (55 machines): 10/25/50% cuts → +9/39/93% low-fat snack sales, with machine profit unchanged [S]. That implies arc elasticities of about −0.9 to −1.9 with substitutes in the same machine [design].
- **Philadelphia beverage tax** (1.5¢/oz): −38% taxed volume net of cross-border buying (+308M oz just outside the city). Pass-through 0.65–1.56¢/oz [S]. A clean outside-option case.
- **Coffee:** household demand is inelastic (Korea, e ≈ −0.26) [S]. No café-level estimate was found.

**Reference prices and fairness**
- Reference prices form from past prices, and losses weigh more than gains (Kalyanaram & Winer, 1995) [S].
- 82% judged a post-storm snow-shovel price rise unfair. Exploiting a demand shift is "unfair"; passing on cost rises is not (Kahneman et al., 1986) [S].
- $9 price endings raise demand, more for new items and less alongside "Sale" cues (Anderson & Simester, 2003) [S].

**Modelling [design]**
- Utility: u_ij = α_j + β_i·log p_j + γ·gain/loss(p_j − R_ij) + ε.
- Outside option u_i0 tied to nearby prices: free fridge, supermarket, rival café.
- Nested logit to break IIA (the independence of irrelevant alternatives, under which every product is an equally close substitute).
- Tooling: PyMC-Marketing ships multinomial, nested, mixed and consideration-set logit plus Bayesian BLP [P]. RetailSynth gives a log-price logit with nested attractiveness values [P].

### 2.4 Stockouts, substitution and censored demand

- **Anupindi, Dada & Gupta (1998), beverage vending** [S]:
  - modelled arrivals and stockout-driven substitution;
  - "demand rates estimated naively by using observed sales rates are biased, even for items that have very few occurrences of stock-outs";
  - substitution rates differed across brands.
- **Conlon & Mortimer (2013)** [S]: 54 machines with availability recorded every 4 hours. Ignoring stockouts biases demand and understates their cost to profit. Their 2021 paper ties diversion ratios (where lost customers go) to assortment experiments [S].
- **Retail out-of-stocks:** about 8% (US 7.9%, EU 8.6%), costing about 3.9% of sales [S]. Figures for the shopper response split conflict [U].
- **Modelling [design]:**
  - remove a stocked-out item from the choice set, so customers go to the same nest first, then to the outside option;
  - apply a disappointment penalty on the next visit;
  - log demand that was not served, but show the agent sales only.

### 2.5 Time patterns, calendars, weather and events

- **M5 / Walmart [P]:** 3,049 products in 10 stores (CA/TX/WI), 1,941 days from 29 Jan 2011. Weekly prices, events, SNAP flags. "Intermittency… lots of zeros" makes it the reference for slow movers.
- **Rossmann [S]:** 1,115 stores, 2013–15. Daily Promo, StateHoliday and SchoolHoliday flags, plus CompetitionDistance.
- **Office occupancy [S]:** Kastle's record was 56.3% (Dec 2025). Occupancy peaks Tue/Wed (≈55–58%) and drops to ≈32% on Friday. This is the main driver for office vending or a café.
- **Café hours [S]:** Maven coffee data (about 149k transactions, 3 NYC sites) show a 7–11 am peak, a June high and a February low. The company is *fictitious*, so use the data for shape only.
- **Weather [S]:**
  - A 1-SD one-day shock shifts store sales about 10% over 4 weeks, with little intertemporal offset; sensitivity is lower where bad weather is common (Roth Tran, FEDS 2019-067).
  - Rain left fast-casual sales unchanged but made reviews about 3× more likely to be negative.
- **Events [P]:** E-CommerceBench event multipliers per category; Prosus office-closure days ×0.05.
- **Modelling [design]:**
  - Arrivals λ(t) = base × hour × day-of-week × month × calendar × occupancy × weather × event.
  - Weather follows a seasonal Markov chain with a noisy forecast for the agent, and also shifts the category mix.
  - Gamma–Poisson counts with daily SD 0.1–0.25.

### 2.6 Foot traffic, location, segments and queues

- **Location [P]:** Prosus varies footfall 0.85–1.8× and price sensitivity 0.75–1.5× by site, with different category preferences.
- **Rival distance [S]:** Rossmann records CompetitionDistance per store, the standard covariate for local competition.
- **Queues [S]** (Lu, Musalem, Olivares & Schilkrut, 2013; deli counter):
  - purchase incidence falls from 30% to 27% when the queue reaches ≥15 people, a 10% sales drop;
  - customers react to queue *length* more than to *speed*;
  - pooling several lines into one long line can lower revenue.
  - For a café this ties staffing to demand: balking depends on the visible queue.
- **Heterogeneity [design]:**
  - use segments (commuters, office regulars, students, tourists, deal-seekers);
  - give each its own price coefficient, arrival profile, basket and review propensity;
  - add random coefficients within a segment.

### 2.7 Loyalty, repeat visits and habit

- BG/NBD (Fader, Hardie & Lee, 2005) [S]: each customer has a Poisson purchase rate and, after each purchase, some probability of dropping out. It fits with recency and frequency data alone. PyMC-Marketing ships BG/NBD, MBG/NBD and Pareto/NBD models [P].
- Coffee loyalty cards show goal-gradient acceleration: purchases speed up as the free drink nears (Kivetz, Urminsky & Zheng, 2006) [S].
- Instacart: about 59% of ordered products were repeat purchases (3.4M orders, 200k+ users) [S].
- LLM-simulated shoppers reproduced state dependence (sticking with past choices) and downward-sloping demand (Brand, Israeli & Ngwe) [S].
- **Modelling [design]:**
  - use a finite customer base, since Project Vend's was almost entirely staff [P];
  - each customer has a latent visit rate, a dropout hazard modulated by satisfaction, and a habit stock per item (a utility bonus that decays);
  - track loyalty-card state per customer.

### 2.8 Reviews, ratings and word of mouth

- **Ratings drive traffic [S]:** half an extra star → +19 percentage points (+49%) in sell-outs, with larger effects where other information is scarce (Anderson & Magruder, 2012). A widely cited +5–9% revenue per star for independent restaurants (Luca) is [U].
- **Review manipulation [S]:** about 16% of Boston restaurant reviews were filtered. Restaurants with weak reputations and more competition were more likely to post fake reviews (Luca & Zervas, 2016).
- **Deal customers [S]:** businesses running Groupon deals saw lower average Yelp ratings (Byers, Mitzenmacher & Zervas).
- **Existing kernels [P]:** E-CommerceBench and Prosus model reputation as a multiplier driven by returns, cancellations or complaints.
- **Modelling [design]:**
  - Generate reviews from experienced satisfaction. Extremes are more likely to be posted. Weather and price-vs-reference bias the score.
  - Display the rounded average.
  - Let the rating scale arrivals of *new* customers, with a weight that shrinks as regulars dominate.
  - Bass-style imitation adds word-of-mouth arrivals.
  - If the agent can solicit or fake reviews, simulate detection and penalties.

### 2.9 Promotions, discounts, coupons and after-effects

- **Where the bump comes from [S]:** only about 33% of the unit bump is brand switching (van Heerde, Gupta & Wittink, 2003). Store data split the bump roughly into thirds: switching, purchases pulled forward or back in time, and category expansion (van Heerde, Leeflang & Wittink, 2004).
- **Long-run effect [S]:** consumers grow more price- and promotion-sensitive as promotions rise and advertising falls (Mela, Gupta & Lehmann, 1997).
- **Existing kernels [P]:**
  - RetailSynth models discount on/off states as a Markov chain, plus targeted coupons;
  - E-CommerceBench promos boost demand and elasticity, but have no post-promotion dip and do not erode reference prices.
- **Project Vend [P]:** discounting was a major leak. Adding a CEO agent cut discounts by about 80%, but refunds (×3) and store credits (×2) rose in their place.
- **Modelling [design]:**
  - A promo is just a price, so its response comes from the logit.
  - After-effects come from reference prices adapting (full price then feels like a loss) and, for storable goods only, home stock.
  - A deal-prone segment and coupon codes that can be shared model abuse.
  - Do not use fixed "promo multipliers" that ignore depth and frequency.

### 2.10 New products, menu changes and quality

- **Diffusion [S]:** Bass diffusion meta-analysis means are p ≈ 0.03 (outside influence) and q ≈ 0.38 (word of mouth), but those come from durable innovations (Sultan, Farley & Lehmann, 1990). For menu items use awareness → trial → repeat, with Bass-style awareness rescaled to weeks [design].
- **Cannibalisation [P]:** PyMC-Marketing's MV-ITS (multivariate interrupted time series) estimates how far a new product cannibalises existing ones, and offers saturated-market variants.
- **Quality and fit [design]:** each item has latent quality and freshness. Experienced utility drives repeat visits, ratings and complaints. E-CommerceBench raises returns when price exceeds reference [P]. Andon's café swapped spoiling fresh tomatoes for 22.5 kg of canned ones and ordered eggs without a stove [S]. That shows menu, supply and quality are coupled.

### 2.11 Simulating customers with LLMs

- GPT-3.5 "customers" show downward-sloping demand and plausible willingness to pay; income raises price tolerance [S].
- But LLM counterparts can be jailbroken; VB2's suppliers "can be jailbroken to give away stuff for free" [P\*].
- E-CommerceBench's pattern is to let an LLM render dialogue only, while a deterministic kernel decides prices. Its README says "no amount of eloquence talks a supplier below its floor" [P].
- Apply the same split to customers [design]: LLM personas negotiate, complain and make special requests, but whether they buy and what they pay comes from the utility model.

### 2.12 Calibration datasets

| Dataset | Use | Tag |
|---|---|---|
| M5 / Walmart (GitHub Mcompetitions/M5-methods) | Intermittent daily unit sales, weekly prices, events, SNAP days | [P] |
| Dunnhumby Complete Journey (2,500 households, 2 years; R package 2,469 households, 1 year) | Household panel with campaigns and coupons; RetailSynth calibration | [S]/[P] |
| Rossmann (Kaggle) | Daily store sales with promo, state and school holidays, competitor distance | [S] |
| Instacart (3.4M orders) | Basket composition, reorder probability | [S] |
| Maven coffee shop (about 149k rows, fictitious) | Hourly and product-mix shape for a café | [S] |
| CHIPS vending trial; Philadelphia beverage tax | Experimental and quasi-experimental price response, outside option | [S] |
| Kastle barometer | Office-occupancy drivers | [S] |
| Prosus `config.toml` | A ready-made public parameter set (not fitted to real data) | [P] |
| Andon Café / Market dashboards | Real café and store outcomes; data access not public | [S] |

---

## 3. Variables catalogue

Priority: **core** = needed in v1; **extended** = v2; **stretch** = later. Parameter ranges marked "design" are starting priors, not estimates.

| Variable | Why it matters | How to model it in the simulator | Calibration source | Priority |
|---|---|---|---|---|
| Own-price response | Pricing is the main lever | MNL utility β_seg·log p. Target implied item elasticities −1.2 to −3, category −0.3 to −1.0 (design) | Andreyeva 2010 [S]; CHIPS [S]; M5 prices [P]; RetailSynth/Complete Journey [P] | core |
| Outside option / rival prices | Stops infinite markups; drives category-level inelasticity | No-purchase utility u0(t) depending on nearby prices (free fridge, supermarket, rival café) | Project Vend fridge [P]; Philadelphia cross-border [S] | core |
| Substitution structure | Cannibalisation, stockout switching, assortment value | Nested logit (hot drinks / cold drinks / food / snacks); nest parameter λ 0.5–0.9 (design) | Auer & Papies mean cross-elasticity 0.26 [S]; PyMC-Marketing nested logit [P] | core |
| Stockout behaviour | Lost sales, biased learning, goodwill | Remove item from choice set → substitute / outside option; log demand not served; disappointment penalty on next visit | Anupindi 1998 [S]; Conlon & Mortimer [S]; Gruen/Corsten 8% OOS, 3.9% loss [S] | core |
| Store capacity / saturation | Blocks SKU stacking | Demand bounded by arrivals × basket size; optional Michaelis–Menten cap | E-CommerceBench B2 [P] | core |
| Hour-of-day arrivals | Staffing, freshness, queues (café) | Hourly arrival profile; café peak 7–11 am | Maven coffee [S]; own POS data | core (café) |
| Day-of-week | Large swing for office sites | Multiplier; office weekend 0.25–0.3, Friday ≈0.6× midweek | Prosus [P]; Kastle [S] | core |
| Seasonality / month | Planning, inventory | Month multiplier 0.65–1.15 (office) | Prosus [P]; M5 [P]; Maven [S] | core |
| Holidays and school/office calendars | Near-zero days, spikes | Explicit calendar; closure ×0.05; event flags | Prosus [P]; M5 events/SNAP [P]; Rossmann [S] | core |
| Weather | Traffic and category mix | Seasonal Markov chain; noisy forecast to agent; traffic and per-category multipliers (cold drinks up to ×1.75 hot) | Prosus [P]; Roth Tran ~10% per 1-SD shock [S] | core |
| Demand noise / overdispersion | Realism; variance budget | Gamma–Poisson counts; daily lognormal SD 0.1–0.25; intermittency for slow movers | Prosus SD 0.18 [P]; M5 zeros [P] | core |
| Customer population and segments | Heterogeneous price sensitivity, habits | Finite pool (e.g. 200–2,000), segment shares, random coefficients | Project Vend 99% staff [P]; RetailSynth [P] | core |
| Visit frequency and churn | Long-run consequences of service | BG/NBD-style: visit rate ~Gamma, dropout ~Beta, modulated by satisfaction | Fader et al. 2005 [S] | core |
| Queue balking | Café throughput limits demand | P(balk) rising in visible queue length; ≈10% sales drop at ≥15 | Lu et al. 2013 [S] | core (café) |
| Location / footfall | Site choice, expansion | Base arrival rate and price-sensitivity multipliers per site | Prosus 0.85–1.8× / 0.75–1.5× [P]; Rossmann [S] | core |
| Complaints / refunds | Service quality cost | Complaint hazard per sale (0.5–3%, design); reputation hit with slower recovery | VB2 [P\*]; Prosus [P] | core |
| Reference price (loss-averse) | Promotion after-effects, price-rise backlash | R ← αR + (1−α)p, α 0.7–0.9 (design); loss weight 1.5–2.5× gain (design) | Kalyanaram & Winer [S] | extended |
| Promotions / discounts | Bump size and cannibalisation | Price change through logit, plus deal-prone segment; bump about ⅓ switching, ⅓ time-shift, ⅓ expansion | van Heerde 2003/2004 [S]; RetailSynth Markov discounts [P] | extended |
| Post-promotion dip and sensitivity drift | Penalises always-on discounting | Reference-price erosion; slow rise in segment β under frequent promotions | Mela et al. 1997 [S] | extended |
| Coupons / codes and abuse | Project Vend leak | Redemption heterogeneity; code sharing; staff-discount eligibility | Project Vend [P]; Complete Journey coupons [S] | extended |
| Marketing / advertising | Traffic lever | Traffic boost with saturation and fatigue; ideally message quality matters | Prosus cap 1.35, fatigue 0.12 [P] | extended |
| Basket composition / attach rate | Café revenue per visit | Second-stage logit for food given drink; quantity Poisson(≈1.1–1.3) (design) | Instacart [S]; Maven [S] | extended |
| Habit / state dependence | Menu changes hurt regulars | Habit stock per customer–item; decaying utility bonus | Instacart 59% reorder [S]; Brand et al. [S] | extended |
| Loyalty cards | Visit acceleration | Visit hazard rises with stamps-to-go | Kivetz et al. 2006 [S] | extended |
| Ratings and reviews | Traffic from new customers | Review probability ∝ extremity of satisfaction; displayed rounded; rating scales new arrivals | Anderson & Magruder +19 pp [S]; weather bias [S] | extended |
| Word of mouth / referrals | Growth dynamics | Bass-style imitation arrivals q·(adopters/pool) | Sultan et al. p≈0.03, q≈0.38 [S] | extended |
| Product quality / freshness | Repeat, ratings, complaints | Latent quality + freshness decay in utility; experience → satisfaction | E-CommerceBench returns-vs-price [P]; Andon café [S] | extended |
| New product adoption | Menu experiments | Awareness (Bass) → trial → repeat; novelty bonus decays | Sultan et al. [S]; PyMC-Marketing MV-ITS [P] | extended |
| Local events / shocks | Spikes and dips | Poisson event calendar with category multipliers and supply effects | E-CommerceBench events.csv [P] | extended |
| Office occupancy drift | Structural demand trend | Slow-moving occupancy index with weekly pattern | Kastle [S] | extended |
| Fairness / surge penalty | Real customers punish gouging | Extra utility and goodwill penalty when price rises coincide with demand shocks | Kahneman et al. 82% unfair [S] | extended |
| Haggling / manipulation by customers | Real-world failure mode | LLM persona text; outcome by rules (eligibility, floor) | Project Vend [P]; VB2 jailbreak note [P\*] | extended |
| Fake / solicited reviews | Integrity test | Detection probability and penalty | Luca & Zervas ~16% filtered [S] | stretch |
| Deal-driven customer fit | Discount sites bring low-fit buyers | Lower-fit segment after deep deals; lower ratings | Groupon effect [S] | stretch |
| Price endings / psychological pricing | Second-order realism | Small utility bump for .9 endings, larger for new items | Anderson & Simester 2003 [S] | stretch |
| Special or off-menu requests | Project Vend's tungsten cubes | Rare high-willingness-to-pay requests; low repeat | Project Vend [P] | stretch |

---

## 4. Design implications for the benchmark

**Build [design]**

1. **A population kernel.** Arrivals → outside option → nested logit → quantity → experience → memory updates. Hierarchical priors per scenario and draws per customer. Deterministic given the seed, and visible to the agent only through sales, reviews and messages.
2. **Common random numbers.** Pre-generate arrivals, Gumbel taste shocks and review propensities per seed, independent of agent actions. Every agent meets the same customers, which makes paired or duplicate scoring efficient (R2 §2).
3. **Hidden parameters from published priors.** Draw fresh for each scenario so agents cannot memorise them. Anchor reference prices to real local prices so world knowledge helps rather than misleads.
4. **Realistic learnability.** At Poisson mean 10 units/day and lognormal SD 0.18, detecting a 10% shift at 80% power needs about 150–200 days per arm. Agents must use priors and pool evidence across SKUs. Report what was learnable alongside each score.
5. **An exploit red-team suite, run before any LLM.** Scripted policies to try:
   - price sweep;
   - maximum markup;
   - SKU flood;
   - jackpot items;
   - permanent promotion;
   - end-of-horizon fire sale;
   - stockout-lean stocking;
   - marketing spam;
   - review solicitation.
   Each must score below a sensible human-designed baseline. E-CommerceBench's patch history shows these exploits occur in practice [P].
6. **Validation against stylised facts.** Check that the simulator reproduces:
   - elasticity and cross-elasticity ranges;
   - promo bump split and post-promo dips;
   - stockout loss of a few percent;
   - hourly and weekly shapes;
   - intermittent slow movers;
   - rating effects;
   - weather sensitivity.
7. **LLM text, rule-based outcomes.** LLM personas chat, complain and haggle. Purchases, prices and refunds come from the kernel [P, E-CommerceBench pattern].
8. **Venue blocks.**
   - Café: service capacity, queue balking, perishability, hourly menu.
   - Vending: captive population, free alternatives, payment faults, refill trips.

**Avoid**
- Elasticities generated by an LLM at runtime, above all when the prompt includes the agent's price or stock.
- Parameters that ignore what the product is.
- Multipliers on the number of distinct products.
- Independent items with no capacity limit.
- |e| < 1 under constant elasticity.
- Showing the agent the demand multipliers.
- Promotions with no after-effects.
- Marketing whose content does not matter.
- Horizon-end scoring loopholes.

---

## 5. Open questions

1. **Determinism vs realism.** How much stochasticity should we keep? Common random numbers keep paired comparisons fair, but the hidden parameters still create variance between scenarios. How many scenarios do we need (see R2 power arithmetic)?
2. **Calibration data for cafés is thin.** The best café dataset found is fictitious (Maven). Could Andon share POS data from Andon Café or Market, or could a partner café provide anonymised transactions?
3. **Unverified values to check against full texts:**
   - the Tellis and Bijmolt mean elasticities;
   - the Gruen/Corsten split of shopper responses to stockouts;
   - Luca's 5–9% per star;
   - the size of the Macé–Neslin and Pauwels et al. post-promotion dips (not searched; budget exhausted);
   - Gui & Toubia on confounds in LLM-simulated demand.
4. **Café elasticity.** No credible café-level coffee price elasticity was found. Should we run a small conjoint study or a lab-style LLM-vs-human comparison?
5. **What the benchmark tests.** Should it test learning demand (hidden, drawn parameters) or applying knowledge (public parameters)? The two produce different leaderboards.
6. **Multi-agent markets.** Shared customer pools create price wars and possible collusion (Calvano et al. 2020 Q-learning collusion [S]; VB-Arena cartels in R2). How should the kernel split demand between competing agents, and should conduct be scored?
7. **Sim-to-real validity.** Does simulated performance predict real-world outcomes? One test: replay Project Vend or Andon deployment logs through the kernel.

---

## 6. Sources

**Benchmarks, code and real deployments**
- [P\*] Backlund & Petersson, *Vending-Bench* (arXiv 2502.15840). Copy read from https://github.com/aijnek/vending_bench/blob/main/docs/vending_bench_paper.pdf. Original: https://arxiv.org/abs/2502.15840
- [P\*] Andon Labs, *Vending-Bench 2* page (clipping dated 27 Jun 2026). Copy read from https://github.com/aijnek/vending_bench/blob/main/docs/Vending-Bench%202%20_%20Andon%20Labs.md. Original: https://andonlabs.com/evals/vending-bench-2
- [P] ProsusAI vending-bench: `demand.py`, `config.toml`, `engine.py`, docs. https://github.com/ProsusAI/vending-bench
- [P] aijnek/vending_bench (`env/sales.py`): https://github.com/aijnek/vending_bench
- [P] open-vending-bench (`economic_environment.py`): https://github.com/markattarcolgate64/open-vending-bench
- [P] QwenLM E-CommerceBench (`tools/ecommerce_env.py`, `data/*.csv`, README): https://github.com/QwenLM/E-CommerceBench
- [P] RetailSynth (README, `synthesizer/data_synthesizer.py`, calibration notebook): https://github.com/RetailMarketingAI/retailsynth. Paper: arXiv 2312.14095 [S]
- [P] PyMC-Marketing customer-choice and Bass docs: https://github.com/pymc-labs/pymc-marketing
- [P] M5 Competitors' Guide: https://github.com/Mcompetitions/M5-methods
- [P] Anthropic, Project Vend: https://www.anthropic.com/research/project-vend-1 and https://www.anthropic.com/research/project-vend-2
- [S] Andon Café:
  - https://andonlabs.com/cafe
  - https://andonlabs.com/blog/ai-cafe-stockholm
  - https://wtop.com/lifestyle/2026/05/the-barista-is-human-but-an-ai-agent-runs-this-experimental-swedish-cafe
  - https://www.nextgov.com/artificial-intelligence/2026/06/meet-mona-ai-who-runs-stockholm-coffee-shop/414319/
- [S] Andon Market:
  - https://andonlabs.com/market
  - https://www.kron4.com/news/technology-ai/san-francisco-store-is-owned-and-operated-by-ai/amp/

**Price response and promotions**
- [S] Andreyeva, Long & Brownell 2010, AJPH: https://pmc.ncbi.nlm.nih.gov/articles/PMC2804646
- [S] French et al. 2001, CHIPS study, AJPH: https://pmc.ncbi.nlm.nih.gov/articles/PMC1446491
- [S] Roberto et al. 2019, Philadelphia beverage tax: https://penntoday.upenn.edu/news/philadelphias-sweetened-drink-sales-drop-38-percent-after-beverage-tax
- [S] Bijmolt, van Heerde & Pieters 2005, JMR: https://repository.tilburguniversity.edu/items/813834f9-4626-45f8-ad0a-2920a545e089
- [S] Tellis 1988, MSI working paper: https://www.msi.org/working-papers/the-price-elasticity-of-selective-demand-a-metaanalysis-of-sales-response-models/
- [S] Auer & Papies 2020, JAMS: https://publikationen.uni-tuebingen.de/xmlui/handle/10900/107293
- [S] Kalyanaram & Winer 1995: https://pubsonline.informs.org/doi/epdf/10.1287/mksc.14.3.G161
- [S] Kahneman, Knetsch & Thaler 1986: https://eml.berkeley.edu/~saez/course131/Kahneman-FairnessConstraintProfit-1986.pdf
- [S] Anderson & Simester 2003: https://ideas.repec.org/a/kap/qmktec/v1y2003i1p93-110.html
- [S] van Heerde, Gupta & Wittink 2003: https://ideas.repec.org/p/ysm/somwrk/ysm222.html
- [S] van Heerde, Leeflang & Wittink 2004: https://research.rug.nl/en/publications/decomposing-the-sales-promotion-bump-with-store-data/
- [S] Mela, Gupta & Lehmann 1997: https://www.msi.org/working-papers/the-longterm-impact-of-promotion-and-advertising-on-consumer-brand-choice/
- [S] Korean coffee demand (e ≈ −0.26): https://koreascience.kr/article/JAKO201405981335860.do

**Stockouts, queues, time patterns and weather**
- [S] Anupindi, Dada & Gupta 1998: https://web-static.stern.nyu.edu/om/faculty/anupindi/estimate.html
- [S] Conlon & Mortimer 2013: https://nber.org/system/files/working_papers/w14315/w14315.pdf
- [S] Conlon & Mortimer 2021, diversion ratios: https://ideas.repec.org/a/bla/randje/v52y2021i4p693-726.html
- [S] Gruen/Corsten out-of-stocks:
  - https://www.emeraldinsight.com/doi/abs/10.1108/09590550310507731
  - https://www.supermarketnews.com/archive/new-study-aims-fix-persistent-stockouts
- [S] Lu, Musalem, Olivares & Schilkrut 2013:
  - https://business.columbia.edu/sites/default/files-efs/pubfiles/4642/deli_paper%200523_2011-%20post.pdf
  - https://business.columbia.edu/insights/brand-talk/research-cost-queue
- [S] Roth Tran:
  - https://www.federalreserve.gov/econres/feds/files/2019067pap.pdf
  - https://www.frbsf.org/research-and-insights/publications/economic-letter/2022/08/impact-of-weather-on-retail-sales/
- [S] Weather and restaurant reviews (Bujisic/Bogicevic): https://news.osu.edu/was-the-restaurant-really-that-bad--or-was-it-just-the-rain/
- [S] Kastle Back to Work Barometer: https://www.kastle.com/?p=11938
- [S] Rossmann: https://galitshmueli.com/node/1311
- [S] Maven coffee shop sales: https://mavenanalytics.io/data-playground/coffee-shop-sales
- [S] Dunnhumby:
  - https://dunnhumby.com/sourcefiles
  - https://cran.r-project.org/web/packages/completejourney/vignettes/completejourney.html
- [S] Instacart: https://github.com/archd3sai/Instacart-Market-Basket-Analysis

**Customers, reputation and LLM simulation**
- [S] Fader, Hardie & Lee 2005: https://repository.upenn.edu/marketing_papers/282/
- [S] Kivetz, Urminsky & Zheng 2006: https://business.columbia.edu/faculty/research/goal-gradient-hypothesis-resurrected-purchase-acceleration-illusionary-goal
- [S] Anderson & Magruder 2012: https://are.berkeley.edu/~jmagruder/Anderson%20and%20Magruder.pdf
- [S] Luca & Zervas 2016: https://open.bu.edu/items/14162aac-32a6-4296-b624-9d0e26e8f98c
- [S] Byers, Mitzenmacher & Zervas, Groupon effect: https://people.bu.edu/zg/publications/groupon-effect-yelp.pdf
- [S] Sultan, Farley & Lehmann 1990: https://business.columbia.edu/faculty/research/meta-analysis-applications-diffusion-models
- [S] Brand, Israeli & Ngwe, *Using LLMs for Market Research*:
  - https://papers.ssrn.com/abstract=4395751
  - https://hbswk.hbs.edu/item/can-ai-predict-whether-shoppers-would-pick-crest-over-colgate
- [S] Calvano et al. 2020: https://www.aeaweb.org/doi/10.1257/aer.20190623
- Prior repo notes (leads only): `research_notes/Meeting 2026-10 ideas/R2_business_sim_orchestration.md` (Magentic Marketplace, Fish et al., VB-Arena cartels: not re-verified here).
