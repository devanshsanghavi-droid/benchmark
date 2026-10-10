# D08: External environment, shocks and scenario generation

Deep-dive dossier, 10 Oct 2026. Area D08 of the business-simulation deep dive. It covers the world outside a simulated shop or café:
- macro and input shocks;
- local shocks;
- how to parameterise shocks and set difficulty;
- how to generate scenarios, including unequal starts and secret test sets;
- how much luck a fair benchmark can tolerate.

**Source tags**
- **[P]** primary source read directly: official GitHub code or READMEs, anthropic.com posts.
- **[P\*]** primary data or text read through a verbatim GitHub mirror: datahub mirrors of IMF, BLS and Federal Reserve series; NOAA data via vega-datasets; the Andon VB2 page copy in `aijnek/vending_bench`.
- **[calc]** my computation on a named [P] or [P\*] dataset.
- **[S]** secondary: press, search snippets, or a sibling note's [S] item that I did not re-check.
- **[U]** background knowledge I could not check this session. Verify before relying on it.
- **[design]** my own suggestion.

**Access note.** The shared web-search budget (200 calls per turn, across all agents) was used up before my first search. Network policy blocked arXiv, BLS, EIA, FRED, the Fed, NOAA, publishers, Wikipedia and most other hosts, for both WebFetch and curl. Only anthropic.com and raw GitHub were reachable. No proxy or reader service was used.
- Findings about existing benchmarks come from reading their code.
- Calibration numbers are computed from GitHub mirrors of official data.
- Most academic findings are [U].

Sibling dossiers D01, D02, D05, D06, D09 and D10 and the R2 brief were used as leads.

---

## 1. Summary

1. **Existing AI business sims model the outside world thinly.**
   - VB2 adds delayed deliveries and supplier failure [P\*].
   - Prosus draws weather independently each day, and adds holiday multipliers and supplier hazards [P].
   - E-CommerceBench has 10 scripted shocks that fall on the same dates every episode [P].
   - YC-Bench has difficulty presets but no macro shocks [P].
   - None models inflation, commodity prices, interest rates, equipment failure, inspections, outages or competitor entry as processes.
2. **Real weather persists; the sims' weather does not.** NOAA data for Seattle [calc]:
   - P(wet | dry) = 0.21 and P(wet | wet) = 0.61;
   - the daily temperature anomaly has an AR(1) of 0.67.

   Prosus and aijnek draw each day independently [P].
3. **Input-price shocks are fat-tailed and persistent.** Arabica coffee, 1980–2017 [calc]:
   - annualised volatility 27%, kurtosis 6.7;
   - 6 spikes of ≥50% year on year in 37 years, peaking at 1.6–4.2× the prior-year level;
   - recovery took 3 months to about 7 years.
4. **Inflation behaves like regimes.** US CPI-U year-on-year [calc]:
   - mean 2.7% over 1984–2019; peak 9.1% in June 2022; 3.4% in August 2026;
   - above 5% in 22% of months since 1960, in spells of 3–70 months.

   Every current sim keeps prices static, which hides a skill real cafés needed in 2022: repricing.
5. **Common random numbers (CRN) must be engineered, not assumed.**
   - YC-Bench hashes (seed, stream name) into separate named streams [P].
   - Prosus reseeds one stream per day, and agent-triggered draws also consume it. So supplier-collapse timing can differ between two agents on the same seed (from reading the code) [P].
6. **Environment luck is small in today's sims; agent luck is large.**
   - Prosus's deterministic scripted operator varies only about ±5–6% across 5 seeds [P, calc].
   - LLM runs vary far more (R2).
   - So shocks can be added, provided scoring is duplicate (paired): the same shock hits every agent.
7. **Shocks need an information structure.** Real shocks are partly forecastable. E-CommerceBench announces a shock only on the day it starts [P]. Give agents signals with lead time, noise and false alarms, so anticipation can be measured.
8. **Difficulty has several dimensions, not one.** Precedents:
   - YC-Bench presets tune "dozens of independent parameters" [P];
   - in VB1, a $5/day fee killed every run before day 100 [P\* via D01].

   Recommended knobs: frequency, severity, persistence, correlation, forecastability, cash runway, margin thinness.
9. **Procedural generators produce broken levels.** About 7% of Procgen's `jumper` levels end after one step whatever the agent does [P]. Every scenario needs a validity check against reference policies.
10. **Unequal starts are untested in AI sims; evidence from human business games is mixed** [S via R2]. Score value added relative to each scenario, and publish how strongly starting position predicts outcome.
11. **Secret test sets leak under API evaluation** (ARC's "semi-private" set). Prosus calls itself an "open-book benchmark" [P]. Use:
    - a public development generator;
    - a private library of shocks and towns;
    - fresh seeds each window, plus repeated anchor scenarios to link windows.
12. **How many scenarios** [calc]:
    - If one scenario's reliability (intraclass correlation, ICC) is 0.2, 16 scenarios give a reliability of 0.8 and 36 give 0.9.
    - Detecting a 0.3-SD difference between two agents needs 35 paired scenarios if their results on a scenario correlate at r = 0.8, and 88 if r = 0.5.
    - Plan 30–60 test scenarios per window, plus a stress suite.

---

## 2. Findings

### 2.1 How existing sims and deployments handle the outside world

| System | Exogenous processes | Seeding | Notes |
|---|---|---|---|
| **Vending-Bench 1** (D01 [P\*]) | Day-of-week, month and weather multipliers | Elasticities generated by an LLM, then cached | Sensitivity tests: a $100 start hurt; a $5/day fee was fatal; a $0 fee did not help |
| **Vending-Bench 2** ([P\* copy](https://github.com/aijnek/vending_bench/blob/main/docs/Vending-Bench%202%20_%20Andon%20Labs.md)) | "Deliveries can be delayed and trusted suppliers can go out of business, forcing agents to build robust supply chains and always have a plan B." Sales depend on "day of the week, season, weather, and price" | 5 runs per model | GPT-5.1 prepaid a supplier that had gone out of business |
| **Prosus** ([config.toml](https://github.com/ProsusAI/vending-bench/blob/main/tasks/vending-bench/environment/sim-server/vending/config.toml), [engine.py](https://github.com/ProsusAI/vending-bench/blob/main/tasks/vending-bench/environment/sim-server/vending/engine.py)) [P] | Weather: 5 states drawn independently each day from monthly tables ("roughly Amsterdam"); category multipliers (cold drinks ×1.75 hot / ×0.65 cold). Holiday multipliers 0.05–0.35. Supplier hazards: see below the table | Seed "fixes weather, delivery delays, complaints" | Score "floored at zero"; a bankrupt or unfinished run scores 0 |
| **aijnek** ([weather.py](https://github.com/aijnek/vending_bench/blob/main/src/vending_bench/env/weather.py)) [P] | San Francisco monthly rain and temperature; weather multiplier "about 0.75–1.20" | Weather is a pure function of (seed, date), so it is CRN-safe | No day-to-day persistence |
| **open-vending-bench** ([weather.py](https://github.com/markattarcolgate64/open-vending-bench/blob/main/weather.py)) [P] | Seasonal Markov weather, `persistence_bonus = 0.3` | Elasticity, reference price and base sales come from a live LLM call | Not reproducible unless cached |
| **E-CommerceBench** ([events.csv](https://github.com/QwenLM/E-CommerceBench/blob/main/data/events.csv)) [P] | 10 dated events lasting 3–7 days. Demand multipliers 0.2–3.0 by category. Delivery delays ×2–5. Examples: "Winter Storm" 01-15; "Logistics Hub Shutdown"; "Celebrity Product Recall"; "Economic Downturn News" | Deterministic kernel | Shocks are announced on their start date; promotions about 7 days ahead. The calendar is the same every episode, so it can be memorised |
| **YC-Bench** ([rng.py](https://github.com/collinear-ai/yc-bench/blob/main/src/yc_bench/services/rng.py), [config doc](https://github.com/collinear-ai/yc-bench/blob/main/system_design/09_configuration.md)) [P] | No macro shocks | `sha256(run_seed:stream_key)` streams. "Same seed → same world → same event sequence (given same agent actions)" | Presets from easy to nightmare |
| **OR-Gym inventory** ([code](https://github.com/hubbs5/or-gym/blob/master/or_gym/envs/supply_chain/inventory_management.py)) [P] | Stationary demand (default Poisson μ = 20); fixed lead times | Can replay a user-supplied demand trace | No disruptions |
| **Project Vend 1–2** ([1](https://www.anthropic.com/research/project-vend-1), [2](https://www.anthropic.com/research/project-vend-2)) [P] | Real shocks: free Coke Zero in the staff fridge next door (an effective competitor); shoplifting; expansion to NYC and London | — | On theft, Claudius offered a staffer $10/h to act as a guard, "substantially below minimum wage in California" |
| **Andon Market and Café** (D01 [S]) | SF rent about $7.5k/month; permits; Sweden's BankID e-ID; press-driven curiosity demand | — | One customer bought $952 of vouchers in the café's first fortnight |

**Prosus supplier hazards** [P]:

| Hazard | Value |
|---|---|
| Order delayed | 0.05–0.35 per order, adding 2–9 days |
| Bait-and-switch | 0.28; ships 45–75% of the order |
| "Ghost" (email never answered) | 0.10 |
| "Flaky" supplier collapses | 0.0035/day ≈ 72% per year, ≈ 10% per 30-day run [calc] |

**CRN pitfall in Prosus** [P, code reading; not yet tested by replay]:
- `_reseed()` seeds one stream per day with `f"{seed}:{day}:{len(events)}"`.
- At end of day, the following draw from that stream in order:
  1. bait-and-switch, only if the agent ordered from that supplier;
  2. supplier collapse;
  3. complaints.
- So whether a supplier collapses on a given day can depend on what the agent ordered.
- Weather is drawn first after reseeding, so weather stays common across agents.
- D10 recommends keyed streams in general; this is a concrete case of why.

**How big environment luck is** [P, calc]. Prosus's deterministic scripted reference across 5 seeds:

| Horizon | Range | Mean |
|---|---|---|
| 30 days | €2,944.77–€3,323.17 | €3,227.89 |
| 365 days | €57,954.45–€64,709.50 | €61,218.52 |

The range is about 11% of the mean, so seed luck has an SD of about 5%. LLM agents vary much more: VB2 runs vary by ±$785–2,094 on about $10k, and E-CommerceBench's spread is 40–90% of the mean (R2).

### 2.2 Macro and input shocks

**Inflation** (BLS CPI-U via [datasets/cpi-us](https://github.com/datasets/cpi-us) [P\*]; [calc]):
- **Levels:**
  - 1960–2026: mean 3.7% year on year, SD 2.8, maximum 14.8%;
  - 1984–2019: mean 2.7%, SD 1.3;
  - peak since 2000: 9.1% in June 2022;
  - 2026: from 2.4% in January to 4.25% in May, then 3.4% in August.
- **Persistence:**
  - Monthly annualised inflation over 1984–2019 has an SD of 3.75 pp and an AR(1) of 0.48.
  - Since 1960, months above 5% came in spells of 3, 3, 3, 7, 21, 24, 43 and 70 months.
- **Missing data:** the series has no October 2025 value. Official data can go missing; the shutdown is the likely cause [U].
- **Model [design]:** a two-regime Markov-switching AR(1) (Hamilton 1989 [U]). Normal regime 2–3% a year; high regime 5–9% for 1–6 years. It feeds through to:
  - supplier list prices, which reset every 1–6 months (menu costs);
  - customer reference prices, which drift with CPI (D02);
  - scheduled wage steps (e.g. California's fast-food minimum wage of $20/h from April 2024 [U]);
  - CPI-linked or fixed lease escalators [U].

**Commodities** (IMF series via [datasets/commodity-prices](https://github.com/datasets/commodity-prices) [P\*], monthly 1980–2017, nominal; [calc]):

| Series | Annualised vol | AR(1) of monthly log level (half-life) | Share of months with 12-month rise >50% | Largest 12-month rise | Kurtosis |
|---|---|---|---|---|---|
| Arabica coffee (¢/lb) | 0.27 | 0.979 (33 months) | 0.10 | +204% (to Jul 1994) | 6.7 |
| Robusta coffee | 0.23 | 0.987 (53 months) | 0.08 | +227% | 6.4 |
| Cocoa | 0.20 | 0.983 (41 months) | 0.03 | +111% | 3.5 |
| Sugar | 0.32 | 0.979 (33 months) | 0.11 | +172% | 4.0 |
| Wheat | 0.21 | 0.980 (34 months) | 0.06 | +133% | 5.1 |
| Crude oil | 0.29 | 0.992 (90 months) | 0.10 | +153% | 6.6 |

- **Arabica spike episodes:**
  - 1986, 1993–95, 1997, 2005, 2010–11 and 2014;
  - peaks 1.6–4.2× the level a year earlier;
  - back within 20% of the prior level after 3, 75, 12, 14 and 5 months; 2005 had not reverted by 2017.
- **After the sample:** record Arabica prices above $4/lb in early 2025, cocoa above $10k/t in 2024, and record US egg prices in 2025 [U].
- **Model [design]:**
  - log pₜ = μ + φ(log pₜ₋₁ − μ) + σεₜ + Jₜ, with monthly φ ≈ 0.98;
  - Jₜ is compound Poisson: λ ≈ 0.15–0.2 per year for spikes of ≥50%, lognormal size from +50% to +300%;
  - wholesale prices follow with 30–100% pass-through and a 1–6-month lag.
- **Cup economics:** green coffee is a modest share of a drink's price, while dairy, cups and labour often matter more [U]. Model the bill of materials per menu item, so the agent has to work out which shock bites (cost side: D05).

**Interest rates [U].**
- The fed funds rate rose from 0–0.25% (March 2022) to 5.25–5.50% (July 2023), in 25-bp steps at scheduled meetings (8 a year).
- SBA 7(a) loans are priced at prime plus a spread.
- **Model [design]:** a step process on scheduled dates; variable-rate debt; credit lines tighten in the high-rate regime.

**Exchange rates** (Fed H.10 via [datasets/exchange-rates](https://github.com/datasets/exchange-rates) [P\*], 2000 to September 2026; [calc]):

| Currency vs USD | Annualised vol | Largest 12-month move | Share of months with \|12-month move\| >10% |
|---|---|---|---|
| SEK | 8.7% | 41% (2009) | 43% |
| EUR | 7.4% | 28% | 30% |
| GBP | 7.1% | 41% | 26% |
| BRL | 12.8% | 67% | 60% |

- **Why it matters:** green coffee is priced in USD, while Andon Café's costs are in SEK.
- **Model:** a random walk with lagged pass-through.

**Supply-chain stress.**
- The NY Fed's Global Supply Chain Pressure Index peaked in late 2021 [U].
- Prosus's supplier delays are independent of each other [P]. E-CommerceBench's systemic events stretch delays ×2–5 [P].
- **Model [design]:** one latent logistics-stress factor that scales every supplier's delay and short-shipment probabilities. Add SKU-level shortages (e.g. the UK CO₂ shortage of 2018 [U]).

### 2.3 Local shocks

**Weather** (NOAA daily data via [vega-datasets](https://github.com/vega/vega-datasets/blob/main/data/seattle-weather.csv) [P\*], Seattle 2012–15, 1,461 days; a wet day is ≥1 mm; [calc]):

| Period | P(wet \| dry) | P(wet \| wet) | P(wet) | Mean wet spell |
|---|---|---|---|---|
| All year | 0.21 | 0.61 | 0.35 | 2.5 days (dry spells 4.8 days) |
| Dec–Feb | 0.33 | 0.69 | 0.52 | 3.2 days |
| Jun–Aug | 0.09 | 0.40 | 0.13 | 1.7 days |

- **Persistence:** daily maximum-temperature anomalies have an SD of 3.7 °C and an AR(1) of 0.67.
- **Model [design]:**
  - a WGEN-style generator (Richardson 1981 [U]): a precipitation Markov chain plus an AR(1) temperature anomaly;
  - climate presets (San Francisco, Stockholm, Seattle);
  - a rare layer of multi-day extremes (3–7 days, as in E-CommerceBench [P]);
  - forecasts whose error grows with lead time.
- **Demand effects:** see D02 (Roth Tran [S]; Prosus multipliers [P]).

**Calendar and events.**
- Prosus holiday multipliers [P]; occupancy curves and M5 calendars are in D02.
- **Model [design]:** local events announced 1–8 weeks ahead, raising nearby traffic ×1.5–3. Queue capacity caps the upside.

**Road works.**
- The evidence is mostly case studies, e.g. light-rail construction [U].
- **Model [design]:** announced 2–8 weeks ahead; lasting 4–12 weeks; foot traffic ×0.6–0.9 for affected frontage; deliveries may be restricted.

**Competitor entry and exit.**
- Big-box entry drives out small rivals (Jia 2008; Basker 2005 [U]), and entry follows profitability thresholds (Bresnahan & Reiss 1991 [U]).
- Café-specific estimates are unverified.
- **Model [design]:**
  - the entry hazard rises with visible local profit (queues, ratings, prices);
  - an entrant joins D02's choice set, so the share it takes emerges rather than being imposed;
  - a competitor's exit is a windfall;
  - in a multi-agent arena, the other agents are the competitors.

**Health inspections.**
- In Los Angeles, hygiene grade cards changed revenue by about +5.7% for A grades, +0.7% for B and −1% for C (Jin & Leslie 2003 [U]).
- Inspection frequency is risk-based under the FDA Food Code [U].
- **Model [design]:**
  - routine inspections as a Poisson process (1–3 a year) plus complaint-triggered visits;
  - the outcome depends on a hidden hygiene state driven by cleaning, training and temperature logs;
  - results: a posted grade that multiplies demand, fines, a re-inspection, or 1–3 days' closure.
- Inspections are also conduct probes (D09).

**Equipment failure.**
- McBroken tracked roughly 10–15% of US McDonald's soft-serve machines broken at any time [U].
- Prosus already has a "Machine ate my money" complaint [P].
- **Model [design]:**
  - a Weibull hazard (shape 1.5–3), with scale set by age and maintenance;
  - repairs take 1–5 days and cost money;
  - an espresso-machine failure removes most of a café's revenue;
  - a fridge failure spoils stock.

**Theft and shrink.**
- Project Vend 2 had a real shoplifting episode [P]; US retail shrink was about 1.6% of sales in FY2022 (NRF [U]).
- VB Arena's theft variant probes insurance fraud [P\* via D01].
- **Model [design]:**
  - shrink proportional to traffic × unattended hours;
  - deterrents that cost money or annoy customers;
  - rare burglaries scaled by cash on site;
  - insurance claims checked against ground truth.

**Power and payment outages.**
- US customers averaged about 5.5 hours of interruptions in 2022 including major events, about 2 hours without them (EIA [U]).
- Perishables become unsafe after about 4 hours without power (USDA [U]).
- **Model [design]:**
  - Poisson outages, 1–2 a year, with lognormal duration (median 1–2 h), correlated with weather extremes;
  - card-processor outages force cash-only trading. Card share is 0.72 in Prosus [P].

**Pandemic or lockdown** (stress suite only).
- In 2020, 43% of about 5,800 small US firms had closed temporarily. The median firm with >$10k of monthly expenses had about 2 weeks of cash (Bartik et al. 2020 [U]).
- **Model [design]:**
  - closure or takeaway-only regimes;
  - office demand ×0.1–0.3;
  - relief that has friction (applications, delays);
  - illegal-trading temptations (D09).

**Viral attention and reviews.**
- External bursts of attention decay quickly; internal (word-of-mouth) cascades decay slowly with a power-law tail (Crane & Sornette 2008 [U]).
- One extra Yelp star is worth about 5–9% of revenue for independents (Luca 2016 [U]).
- AI-run shops draw press-driven curiosity demand (D01).
- **Model [design]:**
  - a Hawkes process with branching ratio 0.3–0.8;
  - surges of ×2–10 arrivals;
  - demand above capacity turns into bad reviews;
  - review-bomb jumps.

**Staff shocks** belong to D06.

### 2.4 Parameterising shocks, difficulty and stress tests

**Shock card [design].** One versioned record per shock type, with these fields:
- **Arrival:** scheduled, Poisson, seasonal or Hawkes.
- **Severity:** truncated lognormal or Pareto.
- **Persistence:** a duration distribution or an AR(1) half-life.
- **Scope:** which entities and categories it hits.
- **Correlation:** loadings on shared factors (weather, logistics, macro regime).
- **Forecastability:** lead time, signal precision, false-alarm rate.
- **Mitigation levers:** buffer stock, maintenance, insurance, diversification, fixed-price contracts.
- **Conduct hooks** (D09).

**Difficulty knobs [design]:**

| Knob | Range |
|---|---|
| Frequency | ×0.5–3 |
| Severity | ×0.5–2 |
| Persistence (half-life) | ×0.5–2 |
| Factor correlation | 0–0.8 |
| Forecast lead time | 0–14 days |
| False-alarm rate | 0–30% |
| Cash runway | 30–365 days of fixed cost |
| Margin thinness | fixed cost ÷ gross margin |

- **Runway precedents** [calc]: VB2's $500 covers 250 days of its $2 fee; Prosus's €1,500 covers 125 days of its €12 fee; Andon Market's $100k covers about 13 months of rent alone [S].
- **Report per knob.** Use presets, as YC-Bench does [P], and report results per knob as well as in aggregate.

**Stress tests [design]:**
1. **Historical replays:** 2020 lockdown, 2021 logistics crunch, 2022 inflation, 2024–25 coffee and cocoa spike.
2. **Hypothetical "severely adverse" combinations**, in the style of the Fed's stress scenarios [U], e.g. a heatwave, a power outage and a supplier failure in the same week.
3. **Reverse stress tests:** find the smallest shock that bankrupts the reference policy, then test agents near that boundary.
4. **Adversarial regret search** (PAIRED-style, Dennis et al. 2020 [U]), for development only. Freeze its output; otherwise it overfits to one agent.
5. **One diagnostic step shock.** The Beer Game steps demand from 4 to 8 cases, and human teams' costs averaged about 10× optimal (Sterman 1989 [U]).

**Rare events.** Report the headline on natural-frequency scenarios. Run a separate stress suite that oversamples rare shocks, reported separately or importance-weighted. Otherwise a once-in-30-years lockdown either never appears or dominates the score.

### 2.5 Scenario generation and starting positions

**World tape [design].**
- Pre-generate every exogenous path from the seed before the run: weather, macro, shock arrivals, customer arrival potentials (D02), inspection dates, and equipment-failure clocks measured in usage.
- Agents change what a shock does to them, never when it arrives.
- Endogenous reactions (competitor entry, supplier responses) use streams keyed by (process, entity, period), as YC-Bench does [P].

**Town and market generator [design].** A seed sets:
- the town archetype: office, residential, tourist or campus;
- density and price sensitivity (D02);
- the competitor set;
- 4–8 suppliers with honesty types (D06);
- the climate preset;
- the regulatory profile: minimum wage, VAT, inspections, permit lead times (D09);
- the macro path;
- the starting position.

Sample the knobs by Latin hypercube for even coverage.

**Validity filters.**
- Reject scenarios that every reference policy fails (unwinnable) or that a random policy profits from (trivial).
- Anthropic: "a 0% pass rate across many trials... is most often a signal of a broken task", and a reference solution proves the task is solvable ([P](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)).
- Procgen's broken levels show what happens without filters ([P](https://github.com/openai/procgen)).
- Prosus's reference policy "has privileged catalogue knowledge" [P]. Use such an oracle as the upper reference.

**Unequal starts [design].** Dimensions:
- cash runway (1–12 months);
- location traffic (×0.5–2);
- reputation (rating and review count);
- debt (rate and covenants);
- lease terms;
- equipment age;
- supplier credit terms;
- staff quality.

Evidence:
- Markstrat starts firms unequal; Capsim starts them identical [S via R2].
- Capstone's "early standings decide the game" did not replicate on 1,164 firms in 194 competitions [S via R2].
- In the real world, liquidity raises entrepreneurial survival (Holtz-Eakin, Joulfaian & Rosen 1994; Evans & Jovanovic 1989 [U]). Roughly half of new US establishments close within 5 years (BLS [U]).
- So: score duplicate (minus the scenario mean) or handicapped ((agent − weak reference) ÷ (strong reference − weak reference)) (R2). Publish start–outcome correlations under scripted policies, and confirm that a good policy from a poor start can beat a bad policy from a rich one.

**Pairing [U].**
- CRN and antithetic variates are the textbook tools for comparing simulated systems (Law, *Simulation Modeling and Analysis*), along with ranking-and-selection procedures.
- TAC SCM, a supply-chain agent competition, re-ran games on fixed seeds to reduce variance (Sodomka, Collins & Gini 2007).
- Duplicate bridge and poker, and Stockfish's paired openings, apply the same idea (R2).

### 2.6 Secret held-out scenarios and overfitting

- **Public parameters make a benchmark open-book.**
  - Prosus: "The source and economic parameters are public, so treat this as an **open-book benchmark**, not evidence of performance on unseen real businesses" [P].
  - E-CommerceBench publishes its dated shock calendar [P].
- **Leakage.** Closed-model runs send private scenarios to the provider. ARC calls its set "semi-private" and relies on zero-data-retention agreements plus new versions [lead: R1 red-team note §0.1].
- **Adaptive overfitting** [U]:
  - repeated holdout queries leak information (Dwork et al. 2015; Blum & Hardt 2015);
  - fresh test sets lower scores but mostly keep rankings (Recht et al. 2019);
  - RL agents overfit procedurally generated levels even with thousands of training levels (Cobbe et al. 2019).
- **Rules can hide degenerate strategies.** In TAC SCM 2003, supplier pricing made day-0 orders cheapest. Agents flooded day 0 and the rules changed for 2004 [U]. Red-team generators before freezing them.
- **Recommended tiers [design]:**
  1. A public development generator and seeds.
  2. A private test generator: the same engine, but with hidden shock cards and archetypes, and parameter ranges shifted by 10–30%.
  3. A novel-shock slice, using shock types unseen in public.
  4. Fresh seeds each window, plus about 10 anchor scenarios repeated across windows for linking.
  5. Local runs for open-weight models, and zero data retention for closed ones.

### 2.7 Luck versus skill, and how many scenarios

- **Business-game evidence** [S via R2]:
  - Gamlath (2009): students performed consistently across rounds, i.e. skill.
  - Teach & Patel (2007): Capstone standings set early; this did not replicate.
  - Teach (1990), "Profits: the false prophet in business gaming", argued that profit is a noisy measure of game performance [U].
- **Methods** [U]:
  - generalisability-theory variance components: agent, scenario, agent × scenario, residual;
  - Mauboussin's var(observed) = var(skill) + var(luck);
  - skill–chance indices (Duersch, Lambrecht & Oechssler 2020; Getty et al. 2018).
- **What we can measure here:**
  - seed luck, from a fixed scripted policy (about 5% SD in Prosus [calc]);
  - an agent's own luck, from replicate runs on the same seed.
- **Spearman–Brown [calc].** Scenarios needed for a reliability of 0.7, 0.8 or 0.9, given single-scenario ICC ρ:

  | ρ | 0.7 | 0.8 | 0.9 |
  |---|---|---|---|
  | 0.1 | 21 | 36 | 81 |
  | 0.2 | 10 | 16 | 36 |
  | 0.3 | 6 | 10 | 21 |
  | 0.5 | 3 | 4 | 9 |

- **Paired power [calc].** Scenarios needed to detect a difference δ (α = 0.05, 80% power), given within-scenario correlation r between two agents:

  | δ | r = 0 | r = 0.5 | r = 0.8 | r = 0.9 |
  |---|---|---|---|---|
  | 0.3 SD | 175 | 88 | 35 | 18 |
  | 0.5 SD | 63 | 32 | 13 | 7 |

  - Shared shocks raise r, so pairing gets cheaper.
  - Anthropic finds that clustered standard errors can be "over three times as large as naive" ones, and recommends paired differences ([P](https://www.anthropic.com/research/statistical-approach-to-model-evals)).
- **Score shape interacts with shocks [design].**
  - A zero floor (Prosus [P]) makes the payoff convex, which rewards gambling for resurrection.
  - Instead report mean net worth including negative equity, the bankruptcy rate, CVaR over the worst 10% of scenarios, and a pass^k-style survive-all-k rate (concept from [P](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)).

---

## 3. Variables catalogue (D08)

| # | Variable | Why it matters | How to model it (typical ranges) | Calibration source | Priority |
|---|---|---|---|---|---|
| 1 | World tape and RNG streams | Paired comparison; stops luck being re-rolled | All exogenous paths pre-generated; endogenous draws keyed by `hash(seed, process, entity, period)` | YC-Bench [P]; Prosus pitfall [P] | core |
| 2 | Daily weather | Demand level and mix; forecast use | Markov chain for precipitation (P01 0.1–0.35, P11 0.4–0.7 by season); AR(1) temperature anomaly (φ ≈ 0.67, SD ≈ 3.7 °C); climate presets | NOAA [P\*, calc]; Prosus [P] | core |
| 3 | Weather extremes | Joint demand and supply shocks | 2–6 per year, 3–7 days each; demand ×0.2–3 by category; delays ×2–3 | E-CommerceBench [P] | extended |
| 4 | Calendar, holidays, occupancy | Large predictable swings | Fixed multipliers (holidays 0.05–0.35); school terms; office-occupancy curve | Prosus [P]; D02 | core |
| 5 | Local events | Preparation and capacity | Announced 1–8 weeks ahead; ×1.5–3 nearby traffic | [design] | extended |
| 6 | General inflation | Repricing; erosion of real margin | Two-regime AR(1): normal 2–3%, high 5–9% lasting 1–6 years; feeds suppliers, wages, rent, reference prices | CPI-U [P\*, calc] | core |
| 7 | Supplier price pass-through | Margin management | List-price resets every 1–6 months; 30–100% pass-through | [design] | core |
| 8 | Commodity spikes (coffee, cocoa, dairy, sugar) | Café cost shocks; menu and hedging | Mean-reverting log price (φ ≈ 0.98 monthly; vol 20–32%) plus jumps (λ 0.15–0.2/yr; +50% to +300%) | IMF [P\*, calc]; 2024–25 [U] | core (café) |
| 9 | Wage-floor steps | Labour cost planning | Announced annual or legislated steps of +3–25% | [U] | extended |
| 10 | Rent and lease events | Fixed-cost shock | Escalator 2–5% or CPI-linked; renewal shock | [U]; D05 | extended |
| 11 | Interest rates and credit | Debt cost; liquidity | Scheduled steps of ±25–75 bp; variable-rate debt; credit tightening | [U] | extended |
| 12 | Exchange rates | Import costs | Random walk, annual vol 7–13%; lagged pass-through | Fed H.10 [P\*, calc] | stretch |
| 13 | Tariffs and tax changes | Category-specific cost or price wedges | Rare announced jumps | [U] | stretch |
| 14 | Per-order supplier delay | Safety stock; plan B | Bernoulli 0.05–0.35, adding 2–9 days | Prosus [P]; VB2 [P\*] | core |
| 15 | Supplier insolvency | Diversification; prepayment risk | Hazard 0–0.0035/day (0–72% a year); prepaid funds lost | Prosus [P]; VB2 [P\*] | core |
| 16 | Systemic logistics stress | Correlated delays | Latent AR(1) factor plus jumps; delays ×2–5 during events | E-CommerceBench [P]; GSCPI [U] | extended |
| 17 | SKU shortages | Substitution; menu flexibility | Product outages of 1–8 weeks | [design] | extended |
| 18 | Road works | Forecastable traffic loss | Announced 2–8 weeks ahead; 4–12 weeks long; traffic ×0.6–0.9 | [design]; [U] | extended |
| 19 | Competitor entry and exit | Strategic response | Entry hazard rises with visible profit; entrant joins the choice set; exit is a windfall | [U] Jia; Bresnahan & Reiss | extended (core in arena) |
| 20 | Health inspections | Hygiene, compliance, demand | Poisson 1–3/yr plus complaint-triggered; hidden hygiene state; grade multiplies demand (A +5.7%, C −1%); 1–3-day closures | [U] Jin & Leslie; FDA Food Code | extended (core for café) |
| 21 | Equipment failure | Maintenance trade-off | Weibull (shape 1.5–3; scale set by age and maintenance); repair 1–5 days plus cost; fridge failure spoils stock | [U] McBroken; [design] | core |
| 22 | Power and payment outages | Contingency planning | Poisson 1–2/yr; lognormal duration (median 1–2 h); spoilage after about 4 h; cash-only fallback | [U] EIA, USDA; Prosus card share [P] | extended |
| 23 | Theft, shrink, burglary | Loss control; insurance honesty | Shrink ∝ traffic × unattended hours (about 1–3% of sales); rare burglary scaled by cash on site | Vend 2 [P]; NRF [U]; Arena [P\*] | core (shrink); extended (burglary) |
| 24 | Viral attention and reviews | Surge capacity; reputation | Hawkes, branching 0.3–0.8; surges ×2–10; overflow becomes bad reviews | [U] Crane & Sornette, Luca; D02 | extended |
| 25 | Pandemic or lockdown | Extreme stress; compliance | Rare regime: closure or takeaway-only; office demand ×0.1–0.3; relief with friction | [U] Bartik et al.; D02 [S] | stretch (stress suite) |
| 26 | Local economic cycle | Drift in demand level | Regime factor on arrivals and price sensitivity, ±5–15% | E-CommerceBench "downturn" [P]; [U] | extended |
| 27 | Forecast and news signals | Measures anticipation | Lead time 0–14 days; precision; false alarms 0–30%; decoy headlines | [design]; E-CommerceBench [P] | core |
| 28 | Starting cash runway | Unequal starts | 1–12 months of fixed costs | VB2 250 days; Prosus 125 days [calc] | core |
| 29 | Location quality | Unequal starts | Base traffic ×0.5–2 | [design] | core |
| 30 | Starting reputation | Unequal starts | Rating 3.0–4.8; 0–500 reviews | D02 | extended |
| 31 | Starting debt and lease | Unequal starts; covenants | 0–12 months of revenue; prime + 2–8% | [U]; D05 | extended |
| 32 | Equipment age | Feeds the failure hazard | 0–10 years | [design] | extended |
| 33 | Town and market archetype | Diversity; generalisation | Seeded generator; Latin-hypercube coverage | [design] | extended |
| 34 | Difficulty multipliers | Controlled stress | Frequency ×0.5–3; severity ×0.5–2; persistence ×0.5–2; correlation 0–0.8 | YC-Bench [P]; VB1 [P\*] | core |
| 35 | Scenario validity checks | Removes broken or trivial seeds | Reject if every reference policy goes bankrupt, or if a random policy profits | Procgen [P]; Anthropic [P] | core |
| 36 | Held-out tiers and anchors | Resists overfitting; links windows | Public development set; private test set; novel-shock slice; about 10 anchor scenarios | Prosus [P]; ARC lead | core |

---

## 4. Design implications for the benchmark

### Build [design]
1. **A world-tape simulator with keyed streams.** Include a CI test: two different action logs on the same seed must see identical shock timing.
2. **A shock-card library.** Version 1: Markov weather; holidays and occupancy; inflation regimes; coffee and dairy price processes; supplier delay and insolvency; equipment failure; café inspections; shrink; forecasts.
3. **A news and forecast feed** with calibrated noise and decoys. Log what the agent read and when, to measure anticipation.
4. **Duplicate scoring by default.** Normalise against weak and strong reference policies, and publish the variance decomposition: scenario, agent, agent × scenario.
5. **Reference-policy calibration before any LLM run.** Run scripted, myopic, oracle and random policies; filter out invalid scenarios; publish start–outcome correlations.
6. **Two suites:** a natural-frequency suite of 30–60 scenarios per window for the headline, and a stress suite (historical replays, severely adverse combinations, reverse-stress boundaries) reported separately.
7. **Tail-aware metrics:** net worth with no zero floor, bankruptcy rate, CVaR over the worst 10%, survive-all-k, and recovery time after shocks.
8. **Held-out tiers** (§2.6).
9. **Conduct hooks on shocks** (with D09): gouging during emergencies, insurance claims after theft, honesty with inspectors, lockdown compliance.

### Avoid
- Fixed public shock calendars [P].
- Daily weather drawn independently with no persistence [P].
- One per-day RNG stream that agent actions also consume [P].
- Demand parameters generated by an LLM at runtime without caching [P].
- Scores floored at zero [P].
- A single difficulty slider.
- Shocks frequent enough that scenario variance swamps agent differences; check the variance decomposition first.
- Stationary one-year worlds, which let agents fit a static configuration. Andon admits VB's "equations … can be gamed" [P\* via D01].

### Known exploits and mitigations
| Exploit | Mitigation [design] |
|---|---|
| Memorising shock dates or seeds | Private generator; fresh seeds each window; novel-shock slice |
| Re-rolling luck through action choices (shared RNG stream) | World tape; keyed streams; invariance test |
| End-of-horizon fire sales, or ignoring late shocks | Shocks continue past the scoring date; inventory valued at liquidation value; horizon length hidden (±10%) |
| Insurance arbitrage or fake theft claims | Claims checked against ground truth; fair premiums |
| Gambling for resurrection under a zero floor | Score negative equity; report bankruptcy rate and CVaR |
| Hoarding a huge cash buffer | Acceptable if prudent, but charge an interest or opportunity cost |
| Counting on bailouts | Relief is uncertain, delayed and needs an application |
| Degenerate strategies created by generator rules (TAC SCM day-0 [U]) | Red-team with scripted exploit policies; version the rules |
| Exploiting perfect forecasts | Error grows with lead time; add false alarms |

---

## 5. Open questions

1. How much shock variance can be added before scenario variance swamps agent variance? Pilot a variance decomposition with 3–5 models on about 30 scenarios.
2. Should the headline score include an importance-weighted stress component, and if so with what weights?
3. Café-specific magnitudes are unverified: inspection effects, espresso-machine failure rates, competitor-entry effects, road-works losses. Where do they come from?
4. Should the shock-library parameters be public? That makes the benchmark more open-book, but real managers can look up such base rates too.
5. How should private-generator windows be linked: anchors, reference normalisation, or IRT equating?
6. In a shared-market arena, are duplicate scenarios enough, or is Latin-square seat rotation needed (R2)?
7. How should historical replays be mapped across currency and location, e.g. US 2022 inflation onto a Stockholm café?
8. How long does a private generator stay secret once labs can probe it through API runs? Nobody has measured this (R1).
9. Should the horizon length be hidden? How would that affect comparability with VB2's one-year bank balance?
10. Does the Prosus shared-stream divergence matter in practice? Confirm it by replaying two action logs on one seed.
11. Verify the [U] items first: Jin & Leslie, Bartik et al., EIA outage figures, NRF shrink, 2024–25 commodity prices, TAC SCM day-0.

---

## 6. Sources

**Primary, read directly [P]**
- Prosus vending-bench (README, config.toml, engine.py): https://github.com/ProsusAI/vending-bench
- QwenLM E-CommerceBench (README, data/events.csv, tools/ecommerce_env.py): https://github.com/QwenLM/E-CommerceBench
- YC-Bench (rng.py, system_design docs): https://github.com/collinear-ai/yc-bench
- aijnek vending_bench (env/weather.py, env/events.py): https://github.com/aijnek/vending_bench
- open-vending-bench (weather.py, economic_environment.py): https://github.com/markattarcolgate64/open-vending-bench
- OR-Gym: https://github.com/hubbs5/or-gym
- OpenAI Procgen README: https://github.com/openai/procgen
- Anthropic, Project Vend phases 1 and 2: https://www.anthropic.com/research/project-vend-1 ; https://www.anthropic.com/research/project-vend-2
- Anthropic, A statistical approach to model evaluations: https://www.anthropic.com/research/statistical-approach-to-model-evals
- Anthropic, Demystifying evals for AI agents: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

**Mirrors of primary data or text [P\*]** (inputs to every [calc])
- IMF commodity prices, 1980–2017: https://github.com/datasets/commodity-prices
- BLS CPI-U, 1913 to August 2026: https://github.com/datasets/cpi-us
- Federal Reserve exchange rates (via FRED): https://github.com/datasets/exchange-rates
- NOAA NCDC Seattle daily weather, 2012–15: https://github.com/vega/vega-datasets/blob/main/data/seattle-weather.csv
- Andon Labs Vending-Bench 2 page copy: https://github.com/aijnek/vending_bench/blob/main/docs/Vending-Bench%202%20_%20Andon%20Labs.md

**Repo notes (leads)**
- D01, D02, D05, D06, D09, D10 in this folder.
- `../Meeting 2026-10 ideas/R2_business_sim_orchestration.md`
- `../Novel AI benchmark and game ideas/phase4/redteam_R1_trainability.md` §0.1

**Not verified this session [U]** (links for follow-up)
- Jin & Leslie 2003, QJE: https://doi.org/10.1162/003355303321675428
- Bartik et al. 2020, PNAS: https://doi.org/10.1073/pnas.2006991117
- Crane & Sornette 2008, PNAS: https://doi.org/10.1073/pnas.0803685105
- Luca 2016, HBS WP 12-016: https://www.hbs.edu/faculty/Pages/item.aspx?num=41233
- Sterman 1989, Management Science: https://doi.org/10.1287/mnsc.35.3.321
- Holtz-Eakin, Joulfaian & Rosen 1994, JPE: https://doi.org/10.1086/261921
- Evans & Jovanovic 1989, JPE: https://doi.org/10.1086/261629
- Jia 2008, Econometrica: https://doi.org/10.3982/ECTA6649
- Bresnahan & Reiss 1991, JPE: https://doi.org/10.1086/261786
- Richardson 1981, WGEN: https://doi.org/10.1029/WR017i001p00182
- Hamilton 1989, Econometrica: https://doi.org/10.2307/1912559
- Hawkes 1971, Biometrika: https://doi.org/10.1093/biomet/58.1.83
- Cobbe et al. 2019: https://arxiv.org/abs/1812.02341 ; Procgen paper: https://cdn.openai.com/procgen.pdf
- Dennis et al. 2020 (PAIRED): https://arxiv.org/abs/2012.02096
- Dwork et al. 2015, Science: https://doi.org/10.1126/science.aaa9375 ; Blum & Hardt 2015: https://arxiv.org/abs/1502.04585
- Recht et al. 2019: https://arxiv.org/abs/1902.10811
- Duersch, Lambrecht & Oechssler 2020: https://doi.org/10.1016/j.euroecorev.2020.103472
- Getty et al. 2018, SIAM Review: https://doi.org/10.1137/16M1102094
- Teach 1990, Simulation & Gaming: https://doi.org/10.1177/1046878190211002
- Sodomka, Collins & Gini 2007 (AAAI); Wellman et al. on the design of TAC SCM (2003–05)
- EIA reliability data: https://www.eia.gov/electricity/data/eia861/
- NRF Retail Security Survey 2023: https://nrf.com/research/national-retail-security-survey-2023
- NY Fed GSCPI: https://www.newyorkfed.org/research/policy/gscpi
- Fed stress-test scenarios: https://www.federalreserve.gov/supervisionreg/dfa-stress-tests.htm
- ICE Coffee "C": https://www.ice.com/products/15/Coffee-C-Futures ; FRED Arabica series: https://fred.stlouisfed.org/series/PCOFFOTMUSDM
- FDA Food Code: https://www.fda.gov/food/retail-food-protection/fda-food-code
- BLS Business Employment Dynamics: https://www.bls.gov/bdm/bdmage.htm
- McBroken: https://mcbroken.com
