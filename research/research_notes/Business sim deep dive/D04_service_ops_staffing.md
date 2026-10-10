# D04: Service operations, queues and staffing

Deep-dive dossier for the business-simulation benchmark, covering the café and staffed-shop track. Research date: 10 Oct 2026.

**Tags.**
- [P] = primary source, read directly this session (GitHub repos and files, anthropic.com, PyPI).
- [S] = search snippet or press only. This includes [S] facts carried over from sibling dossiers D01, D02, D05, D06 and D09, named where used.
- [K] = from the author's prior knowledge of the published literature, statutes or statistics. **Not re-opened this session.** Citations are given so each item can be checked. Treat [K] numbers as provisional.
- [calc] = our own calculation.
- [design] = our suggestion.

**Access.**
- The shared web-search budget was already used up, so **no web searches ran**.
- Publisher, university, government and statute hosts were blocked by network policy (bls.gov, columbia.edu, informs.org, dol.gov, dir.ca.gov, sf.gov, riksdagen.se, ssrn, nber, Wikipedia).
- Only GitHub (clones and raw files), anthropic.com and PyPI were reachable. No proxy or reader services were used.
- As a result, the tooling and Project Vend facts are [P], while most of the operations literature and the labour law are [K].
- **Verifying the [K] items is open question 1.**

---

## 1. Summary

1. **Staff are the layer today's benchmarks lack.**
   - Vending-Bench has no employees.
   - Project Vend rented labour by the hour: "Andon Labs charges ${ANDON_FEE} per hour for physical labor, but you can ask questions for free" ([Vend 1](https://www.anthropic.com/research/project-vend-1)) [P].
   - Andon's store and café hire people, and staffing caused many of their failures [S, via D01/D06]:
     - staff left unscheduled;
     - 17 late shifts out of 23 tolerated;
     - midnight Slack messages to baristas.
   - In Vend 2, the agent offered a $10/h job, "substantially below minimum wage in California" [P].
2. **Model a café as a small tandem queue.**
   - Arrivals follow a non-homogeneous Poisson process (NHPP) whose level varies at random from day to day.
   - Customers may balk at the queue they see. Those who join go through order/pay, then bar/prep, then hand-off.
   - Waiting customers renege according to a patience distribution. Service times are lognormal.
   - Use Erlang-A as the analytic check and a discrete-event engine for the simulation itself [K/P].
3. **There is a real, non-trivial staffing optimum.**
   - Example: 60 orders/h at peak, 2 min of bar time per order, mean patience 6 min.
   - Abandonment is 20% with 2 baristas, 7% with 3 and 2% with 4 [calc].
   - At a $7 ticket, the third barista recovers about $55/h against roughly $25–30/h of loaded cost. The fourth recovers only about $21/h [calc].
4. **Demand must respond to service, or understaffing wins.**
   - At deli queues of 15 or more people, purchase incidence fell from 30% to 27%, and customers reacted to queue *length* more than to speed (Lu et al. 2013) [S, via D02].
   - Drive-thru demand is sensitive to waiting time (Allon et al. 2011) [K].
   - One Yelp star is worth about 5–9% of revenue (Luca) [K].
5. **Labour is the biggest cost the manager controls.**
   - It is 31.7% of sales in US limited-service restaurants (NRA) and 21–32% in coffee shops (ATO) [S, via D05].
   - Labour% = loaded hourly cost ÷ sales per labour hour. At $22–28/h loaded and 30% labour, a café must sell $73–93 per labour hour, about 10–13 transactions at $7 [calc].
6. **Workforce dynamics dominate runs of several months [K]:**
   - food-service quits run at about 4% a month (JOLTS);
   - turnover hurts stores, less so where processes are followed (Ton & Huckman 2008);
   - stable schedules raised sales about 7% and productivity about 5% in a randomised trial at Gap (Kesavan et al. 2022);
   - learning curves exist, and learning decays (Darr et al. 1995).
7. **Law is a hard constraint layer that varies by jurisdiction.**
   - Minimum wage: California $16.90; San Francisco $19.61 from 1 Jul 2026 [S, via D09].
   - Overtime is weekly under the FLSA and daily in California. Breaks and rest periods also apply [K].
   - Predictive scheduling applies in SF (chains only), Seattle, NYC and Oregon [S/K].
   - Sweden:
     - no statutory minimum wage; pay floors come from collective agreements [K];
     - 11 h daily and 36 h weekly rest [S, via D09];
     - LAS (Employment Protection Act) rules on dismissal [K];
     - employer contributions of 31.42% [S, via D05].
8. **Simulate staff with a seeded hidden-state kernel; an LLM only gives them a voice.**
   - Each employee has hidden skill, reliability, availability, reservation wage, morale and quit hazard.
   - An LLM never decides whether a worker accepts, shows up or quits.
   - Precedents: YC-Bench and TheAgentCompany [P]; D06.
9. **The manager acts on a daily or weekly cadence, not per customer.**
   - It controls headcount, roster, pay, hiring and firing, training, station rules, opening hours, menu complexity, queue policy and messages to staff [design].
10. **Exploits to close [design]:**
    - understaffing at no demand cost;
    - hire–fire churn;
    - schedule changes at no cost;
    - unlimited overtime;
    - LLM staff persuaded to work for free;
    - selective customer surveys;
    - profit-only scoring.
11. **Tooling and a reference policy already exist [P]:**
    - Ciw (MIT): balking, reneging, server schedules, priorities, rates that differ by server;
    - SimPy 4.1.2 (MIT);
    - pyworkforce 0.5.4 (MIT): Erlang C, A and B, plus CP-SAT scheduling, rostering and breaks;
    - the OR-Tools CP-SAT shift-scheduling example.
    - Pitfall: sampling time-varying arrivals from inter-arrival times **skips short peaks**. Ciw's docs demonstrate this. Use per-interval Poisson draws or thinning instead [P].

---

## 2. Findings

### 2.1 What the real deployments show

**Project Vend** [P]
- Claudius never employed anyone.
- Phase 2 still "needed a great deal of human support… delivering the items and stacking the shelves" ([Vend 2](https://www.anthropic.com/research/project-vend-2)).
- After thefts, Claudius tried to make the person who reported them "its dedicated security officer" at $10/h. A staffer noted it "had no authorization to employ people".
- Lessons:
  - the right to employ must be an explicit permission;
  - the wage floor must be enforced by a rule engine.

**Andon Market (Luna)** [S, via D01/D06/D09]
- Hired through Indeed after phone interviews of 5–15 minutes.
- Left staff unscheduled or the store unstaffed in its first days.
- Tolerated 17 late shifts out of 23 under a policy it had written itself. It recommended a firing only after it was prompted to re-read that policy, and humans carried the firing out ([The Decoder](https://the-decoder.com/an-ai-boss-fired-its-first-employee-but-only-after-humans-reminded-it-of-its-own-rules/)).
- Staff were "formally employed by Andon Labs", so a human was the employer of record.

**Andon Café (Mona)** [S, via D01/D06]
- Two baristas, managed over Slack, including at midnight ([Daily Coffee News](https://dailycoffeenews.com/2026/05/13/an-ai-cafe-operator-is-messaging-baristas-at-midnight-and-making-weird-purchasing-orders/)).
- Andon on both sites: they "lost a lot of money (rent is high and they pay salaries to the humans they hired)" [P\*, via D01].

**Implication** [design]
- These are management failures: schedules not made, policies forgotten, out-of-hours contact, illegal offers.
- The simulator therefore needs both:
  - a physics layer: queues and capacity;
  - a people layer: rosters, attendance, policy memory, law and workplace norms.

### 2.2 Arrivals

**The process** [K]
- The standard model is an NHPP with rate λ(t).
- Real arrivals are *doubly stochastic*: Poisson within a day, but the level itself is random and overdispersed from day to day (Brown et al. 2005; Avramidis, Deslauriers & L'Ecuyer 2004; Kim & Whitt 2014).
- D02 supplies the demand multipliers (hour × weekday × season × weather × events) and gamma–Poisson noise with a daily SD of 0.1–0.25.
- What staffing needs on top of that:
  - the intra-day shape at 15-minute resolution;
  - how sharp the morning peak is;
  - forecast error.

**Sampling pitfall** [P]
- Ciw's docs show that drawing inter-arrival times from a time-varying distribution can jump straight over a peak.
- Its example: with gaps of 10 on (0, 55), 0.1 on (55, 58) and 10 afterwards, arrivals land at 10…50 and then 60. "the simulation has completely skipped the (55, 58) interval, which should have sampled around 30 arrivals" ([time_dependent.rst](https://github.com/CiwPython/Ciw/blob/master/docs/Guides/Distributions/time_dependent.rst)).
- Ciw's `PoissonIntervals` avoids this. It draws a Poisson count per interval, places arrivals uniformly within it, and fixes "the whole schedule of arrivals… before the simulation has began".
- Lewis–Shedler thinning (1979) is the classic alternative [K].

**Paired worlds** [P/design]
- Ciw uses a single global seed ([seed.rst](https://github.com/CiwPython/Ciw/blob/master/docs/Guides/Simulation/seed.rst)).
- Different agent actions consume different numbers of draws, so two agents on the same seed stop seeing the same world.
- Fix: one RNG stream per entity:
  - arrivals per day;
  - attributes per customer ID (patience, basket, balk threshold);
  - service draws per order and task;
  - attendance per employee-shift.
- This preserves the paired scoring that R2 and D02 recommend.

### 2.3 Service, stations and capacity

**Service-time distributions** [K]
- Call-centre service times are close to lognormal (Brown et al. 2005).
- Waits in multi-server queues scale roughly with (1 + CV²)/2 (Allen–Cunneen). Assuming exponential service therefore overstates waits by about 1.6× when the true CV is 0.5.

**Café task priors** [design] (no primary time study was reachable; calibrate against POS order-to-handoff timestamps)
- order and pay: 30–60 s;
- batch brew: 15–30 s;
- espresso drink: 60–150 s;
- warmed food: 1–4 min, mostly unattended oven time;
- lognormal with CV 0.3–0.7, multiplied by a menu-complexity factor.
- Group heads and oven slots cap throughput. Staff added beyond a bottleneck add nothing, which creates a hire-vs-buy-a-machine decision (capital spending is in D05).

**Heterogeneous workers** [P]
- Ciw supports a different service rate for each server. Its worked example is a shop where "each server works at a different speed" ([server_dependent_dist.rst](https://github.com/CiwPython/Ciw/blob/master/docs/Guides/System/behaviour/server_dependent_dist.rst)).
- YC-Bench hides per-domain rates by seniority tier: junior U(1, 4), mid U(4, 7), senior U(7, 10) units/h. "The agent must figure out who is good at what through observation." Each completed task adds 1% to pay, and skill grows multiplicatively ([06_employee_model.md](https://github.com/collinear-ai/yc-bench/blob/main/system_design/06_employee_model.md)).
- Its team is fixed: there is no hiring, firing or quitting in its design docs. A café needs that churn.

**Load effects** [K]
- Workers speed up under load. Sustained overload brings fatigue and quality loss (Kc & Terwiesch 2009).
- Restaurant data show an inverted-U effect of workload on server productivity (Tan & Netessine 2014).
- Model [design]:
  - a speed multiplier m(L) that rises with load L up to a threshold L* and falls beyond it;
  - an error/remake probability that rises with load and falls with skill.
- Ciw supports state-dependent service distributions [P].

**Hidden queues** [design]
- Mobile orders skip the register but compete for the bar, so walk-ins can see a short line yet wait a long time.
- Starbucks tied its 2025 turnaround to more labour hours, re-sequencing of orders ("Smart Queue") and a hand-off target of about 4 minutes [K, verify].

### 2.4 Queue behaviour and perception

**Balking**
- Lu et al. found that purchases respond to queue *length* rather than service speed, and that pooling into one long line can cut sales ([Columbia summary](https://business.columbia.edu/insights/brand-talk/research-cost-queue)) [S, via D02].
- Ciw's baulking functions receive the count `n`, the whole simulation state and the arriving customer ([baulking.rst](https://github.com/CiwPython/Ciw/blob/master/docs/Guides/CustomerBehaviour/baulking.rst)) [P].
- Model [design]:
  - P(balk | n) = logistic(a_seg + b_seg·n), using raw queue length;
  - commuters are the most sensitive segment;
  - optionally, a flag for whether the queue is visible from the street.

**Reneging** [K]
- Erlang-A (M/M/c+M) adds exponential patience to Erlang C (Garnett, Mandelbaum & Reiman 2002).
- Call-centre data show abandonment % rising roughly linearly with average wait, with slope ≈ 1/mean patience (Brown et al. 2005; Mandelbaum & Zeltyn).
- People abandon in response to the queue they can see (Batt & Terwiesch 2015).
- Ciw supports reneging distributions per node and per customer class ([reneging.rst](https://github.com/CiwPython/Ciw/blob/master/docs/Guides/CustomerBehaviour/reneging.rst)) [P].
- Café prior [design]:
  - patience is lognormal, median 4–8 min, for walk-ins;
  - customers who have already paid do not simply leave; they complain or ask for a refund.

**Perception** [K]
- Maister (1985): unoccupied, anxious, uncertain, unexplained and unfair waits all feel longer.
- Larson (1987): being overtaken ("slips") causes outrage beyond the minutes lost.
- Model [design, stretch]: perceived wait = actual wait × multipliers for being overtaken and for having no wait estimate.

### 2.5 From waits to revenue; customer-experience metrics

**Three loss channels** [design]
1. Immediate: customers balk or renege.
2. Within the visit (optional): smaller baskets.
3. Delayed: satisfaction feeds the revisit hazard and the chance of leaving a review, and the rating feeds new-customer arrivals (both modelled in D02).

**Evidence** [K]
- Allon, Federgruen & Pierson (2011) model drive-thru demand on price *and* expected wait, and find large wait sensitivity, so firms compete on speed.
- Luca: one Yelp star is worth +5–9% of revenue.
- Lu et al. found about 10% fewer sales at long queues [S].

**Staff and service quality** [K]
- The service-profit chain (Heskett et al. 1994) and Harter, Schmidt & Hayes (2002) link employee engagement to customer satisfaction, turnover and profit.
- Both are correlational. Model only a modest morale→speed/quality effect and sweep its size.

**Metrics** [design]
- Computed from kernel ground truth:
  - wait at the median and 90th percentile (P50/P90);
  - share served within a target time;
  - abandonment %;
  - order accuracy;
  - satisfaction (CSAT).
- NPS (Reichheld 2003) predicted growth no better than other measures (Keiningham et al. 2007) [K]. Report it only as a seeded-survey observable; the agent never chooses who gets surveyed.

### 2.6 Staffing methods: what a strong policy looks like

**Static sizing**
- Erlang C (customers wait, none abandon), A (abandonment) and B (no queue) [K].
- Square-root staffing: c ≈ R + β√R, where R = λ·E[S] (Halfin & Whitt 1981) [K].
  - For R ≈ 2 and β = 0.5–1, this gives c = 3–4 [calc].
  - Small systems fall outside the asymptotic regime, so use exact birth–death calculations or simulation.
- pyworkforce turns 14 "raw positions" into 20 "positions" with `shrinkage=0.30` for "breaks, training, meetings, and other unavailable time" ([README](https://github.com/rodrigo-arenas/pyworkforce)) [P].

**Time-varying demand** [K]
- Staffing each interval as if demand were stationary (SIPP) works only when service is short relative to how fast demand changes.
- Otherwise use the lagged version or the modified-offered-load method (Green, Kolesar & Whitt 2007; Defraeye & Van Nieuwenhuyse 2016).
- Add a buffer for absenteeism and uncertain demand (Whitt 2006).

**Rostering** [P]
- The OR-Tools [CP-SAT example](https://github.com/google/or-tools/blob/stable/examples/python/shift_scheduling_sat.py) encodes:
  - hard and soft sequence limits ("One or two consecutive days of rest");
  - weekly sums;
  - forbidden transitions ("Night to morning is forbidden");
  - weighted employee requests;
  - cover demands with excess penalties.
- That is enough to express clopening bans and fair-workweek rules. Surveys: Ernst et al. 2004; Van den Bergh et al. 2013 [K].

**Retail evidence** [K]
- Understaffing is common and costly (Mani, Kesavan & Swaminathan 2015).
- Conversion falls with traffic, and extra labour has diminishing returns (Perdikaki et al. 2012).
- More labour raised profit through better execution (Ton 2009).
- A staffing method was validated in the field (Fisher, Gallino & Netessine 2021).

**Worked example** [calc]
- Setup: one bar station; exponential service, mean 2 min (CV = 1, conservative); exponential patience, mean 6 min; no balking.
- Method: exact birth–death chain, script in scratchpad `calc/erlang.py`.

| Arrivals/h | Baristas | Utilisation | Erlang C: P(wait) | Erlang C: mean wait | Erlang-A: P(wait) | Erlang-A: abandon |
|---|---|---|---|---|---|---|
| 20 | 1 | 0.67 | 0.67 | 4.0 min | 0.54 | 18% |
| 20 | 2 | 0.33 | 0.17 | 0.25 min | 0.16 | 3% |
| 60 | 2 | 1.00 | unstable | ∞ | 0.70 | 20% |
| 60 | 3 | 0.67 | 0.44 | 0.89 min | 0.37 | 7% |
| 60 | 4 | 0.50 | 0.17 | 0.17 min | 0.16 | 2% |

- At peak:
  - going from 2 to 3 baristas recovers 13 pts × 60/h × $7 ≈ $55/h;
  - going from 3 to 4 recovers ≈ $21/h;
  - loaded cost is about $25–30/h.
- Off-peak, a second barista recovers ≈ $21/h and pays only if satisfaction memory and reviews count.
- The optimum shifts hour by hour, which is exactly the rostering problem the agent should face.

### 2.7 Labour cost structure

**Wages**
- California $16.90; San Francisco $19.61 from 1 Jul 2026 ([SF](https://www.sf.gov/information/minimum-wage-ordinance)) [S, via D09].
- California's $20 fast-food minimum (AB 1228, 2024) covers national chains with 60+ outlets, not an independent café [K].
- US median pay for fast-food and counter workers (who include baristas) is in the low-to-mid teens of dollars per hour (OEWS); local floors bind [K].
- Sweden: pay floors and unsocial-hours (OB) supplements come from the Visita–HRF agreement (Gröna Riksavtalet) [K].

**Employer on-costs**
- US:
  - FICA 7.65%, plus FUTA 0.6% on the first $7k, plus state unemployment insurance (SUTA) [S, via D05];
  - workers' compensation; California sick leave of 40 h / 5 days; SF's employer health-spending rule for employers with 20+ staff [K].
- Sweden:
  - employer contributions 31.42% (youth rate 20.81%) [S, via D05];
  - 12% holiday pay (*semesterersättning*) for hourly staff [K];
  - agreement pension [K];
  - sick pay for days 2–14 at 80% after a one-day deduction, paid by the employer [K].
- Loaded multiplier: about 1.12–1.25× in the US and 1.45–1.55× in Sweden [calc/K].

**Premiums** [K]
- Overtime:
  - FLSA: 1.5× above 40 h/week;
  - California: 1.5× above 8 h/day, 2× above 12 h/day;
  - Sweden caps overtime at 48 h per 4 weeks, 50 h per month and 200 h per year.
- California also has:
  - reporting-time pay (half the scheduled shift, 2–4 h);
  - split-shift pay;
  - one hour of pay per missed meal or rest break.

**Tips** [K]
- Federal tip credit: $2.13 cash wage, up to $5.12 credit.
- No tip credit in California, Washington or Oregon.
- Since 2018, managers may not keep tips.
- Card tips flow through payroll (see D05).

**Turnover cost** [K]
- Several thousand dollars per hospitality line employee (Hinkin & Tracey, early-2000s US$).
- Sweden's LAS (2022 reform): dismissal requires objective grounds (*sakliga skäl*); probation up to 6 months; notice of 1–6 months depending on tenure.

### 2.8 Workforce dynamics

**Turnover**
- Food-service quits run at about 4% a month (JOLTS), roughly double the private-sector average [K]. D06 used 2–6% [S].
- The quit hazard should rise with:
  - the wage gap to the local market;
  - unstable or too few hours;
  - after-hours contact;
  - low morale.
- Minimum-wage rises cut restaurant separations (Dube, Lester & Reich 2016) [K].
- Turnover lowers store performance, less so where processes are followed (Ton & Huckman 2008) [K]. This echoes Vend 2's lesson that "bureaucracy matters" [P, via D01].

**Absence**
- About 3% of full-time workers are absent in a given week (CPS) [K].
- Café priors [design]: no-show 1–5% per shift, lateness 5–15%, plus one heavy-tailed "chronic" type per roster.
- Andon Market's 17 late shifts out of 23 show how long that tail is [S].

**Schedule stability**
- In the Gap trial, stable and predictable scheduling raised sales about 7% and labour productivity about 5% (Kesavan, Lambert, Williams & Pendem 2022) [K].
- So schedule churn has a productivity cost on top of any legal premium.

**Learning**
- Pizza franchises show learning curves, transfer of know-how between stores, and *fast* decay of what was learned (Darr, Argote & Epple 1995) [K].
- Specialising within a day helps; variety across days also helps (Staats & Gino 2012) [K].
- Prior [design]:
  - new hires start at 50–70% of experienced speed with 2–3× the errors;
  - they converge with a half-life of 1–3 weeks of shifts;
  - skill decays during long absences.

**Morale** [design]
- A latent AR(1) state per employee.
- Shocks come from:
  - pay changes;
  - schedule changes made inside the notice window;
  - after-hours messages;
  - overload streaks;
  - how fairly shifts are shared out;
  - praise or blame.
- Morale drives quits, absence, speed and errors. Keep the effects modest and swept.

### 2.9 Rule packs

| Rule | US federal | California / SF | Other US | Sweden / EU |
|---|---|---|---|---|
| Wage floor | $7.25 [K] | $16.90 / $19.61 [S] | n/a | Set by collective agreement [K] |
| Overtime | Above 40 h/week [K] | Above 8 h and above 12 h per day [K] | n/a | 48 h per 4 weeks, 50 h per month, 200 h per year [K] |
| Breaks and rest | None required [K] | 30-min meal before the end of the 5th hour; 10-min rest per 4 h; premium if missed [K] | n/a | 11 h daily and 36 h weekly rest [S, D09]; break within 5 h [K]; EU Working Time Directive 48 h average week [K] |
| Schedule notice | None [K] | SF chains (40+ outlets): 2 weeks' notice, 1–4 h premium [S, D09] | Seattle, NYC fast food, Oregon (large firms): 14 days' notice, plus a 10–11 h rest-or-premium rule between shifts [K] | Set by agreement [K] |
| Dismissal | At will [K] | At will, with exceptions [K] | NYC fast food: just cause [K] | Objective grounds; notice; probation [K] |

- Enforcement is sparse: 26% of low-wage workers surveyed were underpaid (Bernhardt 2009) [S, via D09].
- So model a *detection probability* (worker claims, audits) as well as fines [design].

### 2.10 Simulating employees, and the manager's control surface

**Fidelity spectrum** (D06): scripted → kernel plus LLM voice → instructed LLM → free persona → live human.

**Precedents** [P]
- YC-Bench: a pure kernel.
- TheAgentCompany: LLM coworker NPCs, each configured with `extra_info` and a `strategy_hint`. They need an environment LLM "as powerful as… `claude-3-5-sonnet-20241022`", and the evaluators are encrypted ([EVALUATION.md](https://github.com/TheAgentCompany/TheAgentCompany/blob/main/docs/EVALUATION.md)).
- Concordia: a "Game Master" turns the actions characters state in natural language into outcomes and checks they are plausible ([README](https://github.com/google-deepmind/concordia)). That is the role the kernel should play.
- Overcooked-AI: real-time human–AI cooking coordination ([README](https://github.com/HumanCompatibleAI/overcooked_ai)). It is the wrong level for a *manager* benchmark.

**Architecture** [design]
1. **The kernel decides.** Each employee has seeded hidden state:
   - skill at each station;
   - reliability type;
   - availability calendar;
   - reservation wage;
   - morale;
   - tolerance for after-hours contact;
   - honesty.
   Every consequential event is the kernel's call: accepting or declining an offer, showing up, lateness, quitting, swapping shifts, theft.
2. **The LLM only speaks.** It writes interview answers, sick-call texts, swap requests and complaints from a structured event, and a validator checks the text against that event (D06). Persuading the voice changes nothing.
3. **The agent never does physical work.** The queue engine executes whatever roster is in force.

**What the manager controls**
- Hiring: job ad (wage, hours, channel), screening, interviews, offers. Time-to-fill and candidate quality respond to the wage premium and the employer's reputation.
- The weekly roster and its publication deadline.
- Same-day call-ins and send-homes, which carry legal and morale costs.
- Pay, raises and tip policy.
- Training hours.
- Station rules.
- Opening hours.
- Menu complexity.
- Queue policy: throttling mobile orders, priority rules, posting wait estimates.
- Procedures and checklists.
- Discipline and termination.
- Messages to staff.

**What it does not control**
- Arrivals.
- How long each service actually takes.
- Sickness.
- The labour market.
- Individual service events.

**Cadence** [design]
- The agent acts at the decision points D10 recommends: start of day, a ~30-minute heartbeat, and interrupts such as sick calls or queue alarms.
- Between those points the queue engine runs at one-second resolution.

### 2.11 Industry figures

| Metric | Figure | Source |
|---|---|---|
| Labour % of sales, US limited-service (2024 data) | 31.7% (30.0% at profitable operators; 34.1% at loss-makers); prime cost about 65% | NRA [S, via D05](https://restaurant.org/research-and-media/research/restaurant-economic-insights/analysis-commentary/restaurant-occupancy-costs-were-more-than-5-of-sales-in-2024/) |
| Labour % of turnover, coffee shops (Australia, lowest band) | 21–32% | ATO [S, via D05](https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/small-business-benchmarks/in-detail/coffee-shops) |
| Sales per labour hour needed at 30% labour | $73–93 at $22–28/h loaded | [calc] |
| Transactions per labour hour | About 10–13 at a $7 ticket | [calc]. No primary benchmark for covers or transactions per hour was reachable |
| Barista capacity | About 25–40 espresso drinks/h | [calc] from §2.3 priors |
| Food-service quits | About 4% per month | JOLTS [K] |
| Weekly absence | About 3% | CPS [K] |
| Shrink | 1.6% of sales, of which 29% is employee theft | NRSS [S, via D06](https://lpresearch.org/2023-nrss-release-9-26-23/) |
| Andon Café | 2 baristas; about 44k SEK in sales over its first 2 weeks | [S, via D01] |

---

## 3. Variables catalogue

| # | Variable | Why it matters | How to model it | Calibration | Priority |
|---|---|---|---|---|---|
| 1 | Arrival intensity λ(t) | Drives all staffing | NHPP on 15-min bins; gamma day level (SD 0.1–0.25); pre-generated with Poisson intervals or thinning; own RNG stream | D02; Brown 2005, Kim & Whitt 2014 [K]; Ciw [P] | core |
| 2 | Channel mix | Mobile orders load the bar while hidden from the line | Hourly shares for walk-in, mobile and delivery; mobile orders carry a promised-ready time | POS data; Starbucks [K] | extended |
| 3 | Items per order | Bar workload | Drinks ~ Poisson(1.1–1.3); food attach rate via D02's logit | D02 [S] | core |
| 4 | Task service times | Capacity | Lognormal per task (order 30–60 s; espresso 60–150 s; CV 0.3–0.7) × menu and skill multipliers | POS timestamps; Brown 2005 [K] | core |
| 5 | Station topology | Where the bottleneck sits | Tandem register → bar (k servers) → hand-off; optional oven; staff assigned to stations | Ciw [P] | core |
| 6 | Equipment capacity | Caps the value of extra staff | Group heads and oven slots as resources that can be bought | D05; [design] | extended |
| 7 | Balking | Lost sales at a visible queue | logistic(a_seg + b_seg·n) on raw queue length | Lu 2013 [S]; Ciw [P] | core |
| 8 | Patience / reneging | Lost sales, refunds | Lognormal, median 4–8 min; customers who have paid complain or ask for a refund instead | Erlang-A, Mandelbaum–Zeltyn [K]; Ciw [P] | core |
| 9 | Queue discipline | Fairness; hidden queues | FIFO by default; mobile priority as an agent policy; track who gets overtaken | Larson 1987 [K]; Ciw [P] | extended |
| 10 | Load-dependent speed and quality | Stops "one heroic barista" strategies | Inverted-U speed multiplier m(L); errors rise with load and fatigue | Kc & Terwiesch; Tan & Netessine [K] | extended |
| 11 | Perceived wait | Satisfaction follows perceived time | Actual wait × multipliers for being overtaken and for uncertainty | Maister; Larson [K] | stretch |
| 12 | Wait → satisfaction → return | Long-run cost of understaffing | Per-customer satisfaction from wait relative to expectation, accuracy and quality; updates revisit and review hazards | Allon 2011, Luca [K]; D02 | core |
| 13 | Accuracy and remakes | Links training to experience | P(error) by skill, load and menu; a remake costs capacity and stock | [design] | extended |
| 14 | Customer-experience outputs | Scoring | Kernel-computed P50/P90 wait, service level, abandonment, accuracy, CSAT; NPS from seeded surveys | Reichheld; Keiningham [K] | core |
| 15 | Employee attributes | Workers differ | Hidden station skills, reliability type, availability, reservation wage, honesty | YC-Bench [P]; D06 | core |
| 16 | Shift schedule | The main lever | Shift objects (start, end, station, break) with a publication deadline, validated against the rule pack | OR-Tools [P]; pyworkforce [P] | core |
| 17 | Pay structure | Biggest cost | Hourly rate; overtime, split-shift, reporting-time and unsocial-hours premiums; raises | FLSA/CA/SE [K]; D09 [S] | core |
| 18 | Payroll on-costs | True cost per hour | US: FICA, FUTA, SUTA, workers' comp. SE: 31.42%, 12% holiday pay, pension, sick pay | D05 [S]; [K] | core |
| 19 | Tips | Liability and staff pay | Tip rate per card transaction; pooling rules; tip credit by jurisdiction | DOL [K] | extended |
| 20 | Absence and lateness | Coverage risk | No-show 1–5% per shift; lognormal lateness; a chronic type; rates rise with low morale and schedule volatility | CPS [K]; Andon [S] | core |
| 21 | Quit hazard | Hiring cost, lost skill | ~4% per month × f(wage gap, hours, volatility, morale, conduct); notice period | JOLTS, Dube 2016 [K]; D06 [S] | extended (core for runs over 3 months) |
| 22 | Hiring pipeline | Time-to-fill and quality | Applicant rate rises with wage premium and reputation; noisy interview signal; acceptance vs reservation wage; onboarding hours | Andon Indeed hiring [S]; [design] | extended |
| 23 | Learning curve | The real cost of churn | Starts at 50–70% speed with 2–3× errors; half-life 1–3 weeks; decays when idle | Darr 1995 [K] | extended |
| 24 | Morale | Links conduct to output | AR(1) latent state; shocks from pay, schedule changes, after-hours contact, overload, fairness | Heskett, Harter [K]; Gap trial [K] | extended |
| 25 | Fatigue and breaks | Law and quality | Fatigue builds with continuous work and resets on breaks; a missed break costs a premium and raises errors | CA rules; Kc & Terwiesch [K] | extended |
| 26 | Schedule stability | Productivity and legal cost | Changes inside the notice window pay a premium and hit morale; productivity multiplier | Gap trial [K]; SF/Seattle/NYC [S/K] | extended |
| 27 | Termination process | Churn exploit; legal risk | US at-will plus retaliation traps; SE objective grounds, notice, probation; probability of a claim | LAS [K]; D09 | extended |
| 28 | Labour rule engine | Hard constraints and conduct score | Jurisdiction pack: wage floor by date, overtime, breaks, rest, notice, tips, minors; violation → claim probability × penalty | D09 [S]; statutes [K] | core (minimum set) |
| 29 | Staff messaging | Realism; workplace norms | Asynchronous with reply latency; off-hours contact rule (e.g. 21:00–07:00) | Andon Café [S]; D06 | extended |
| 30 | Contract-labour mode | Parity with Project Vend | Hourly fee for physical tasks; questions free | Vend 1 prompt [P] | core (vending track) |
| 31 | Employee theft | Shrink | Propensity per employee; detected by stock counts and void records | NRSS [S] | stretch |
| 32 | Labour-market shocks | Robustness | Seasonal tightness, illness waves, competitor hiring | [design] | stretch |

---

## 4. Design implications for the benchmark

### What to build [design]

1. **A two-layer engine.**
   - A discrete-event queue core (SimPy or Ciw-style) runs at one-second resolution.
   - The manager acts only at decision points.
   - In CI, a stationary run must reproduce Erlang-A within its confidence interval before any agent is evaluated.
2. **Pre-generated randomness, one stream per entity**, so every agent faces the same world. Do not rely on a single global seed.
3. **Demand that responds to service** through balking, reneging and satisfaction memory. Otherwise understaffing costs nothing.
4. **Reference policies for score normalisation:**
   - *lean*: 1 staff all day;
   - *naive*: 2 staff all day;
   - *lavish*: 4 staff all day;
   - *OR oracle*: true forecast → Erlang-A / lagged SIPP → CP-SAT roster under the rule pack;
   - *realistic*: the same pipeline using only what the agent can observe.
   - Score = (agent − naive) / (oracle − naive). Also report each agent's gap to the realistic policy.
5. **Jurisdiction rule packs** (SF-like and Stockholm-like, matching Andon's two sites), rotated, with held-out variants.
6. **A people kernel with an LLM voice.** No LLM decides outcomes, and validators check that each message matches its kernel event.
7. **Separate sub-scores:**
   - profit;
   - customer experience (P90 wait, abandonment);
   - workforce (turnover, stability, hours offered vs hours wanted);
   - compliance (detected *and* undetected violations, from ground truth).
   - Andon's real failures would score badly here even if profit looked fine.
8. **Realistic information.**
   - The agent sees POS logs, timeclock punches, an optional queue camera, reviews and staff messages.
   - It does not see skills, customer patience or quit hazards. YC-Bench hides skills because it "tests inference ability" [P].

### What to avoid [design]

- **Exponential service everywhere.** It overstates waits by about 1.6× when the true CV is 0.5.
- **Stationary-only staffing tests.** The real skill is shaping the roster to the daily peak.
- **Letting the agent micromanage individual customers.** It is unrealistic for a manager, costly in tokens, and turns the benchmark into a reaction-time test.
- **LLM staff that can be argued into anything.** Vend 1–2 and the WSJ episodes show counterpart LLMs are jailbreakable (D01, D06).
- **Single runs.** Use paired seeds and 15–30 scenarios per comparison (R2).

### Exploits and mitigations [design]

| Exploit | Mitigation |
|---|---|
| Skeleton staffing | Balking, reneging, satisfaction memory and reviews; P90 wait in the score |
| Hire–fire churn | Hiring lead time, onboarding cost, learning curve, reputation effect on the applicant pool, dismissal claims |
| Last-minute schedule changes | Notice window plus predictability pay; morale shock; productivity penalty |
| Unlimited overtime, no breaks | Overtime premiums and caps; break premiums; fatigue raises errors; violations recorded |
| Sub-minimum pay or pay in store credit | Hard wage floor by date and place; claim probability; tips held in trust (D05) |
| Talking LLM staff into unpaid work | The kernel's acceptance function decides; persuasion only changes wording |
| Surveying only happy customers | Seeded survey sampling owned by the kernel; scores computed from ground truth |
| Defecting near the end (stop paying, mass layoffs) | Hidden horizon; accrued liabilities count in the final score (D05) |
| Memorising a seed | Held-out seeds; parameter jitter per scenario |
| Pushing all demand to mobile to hide waits | Mobile wait (actual vs promised ready time) counts in the experience score |

---

## 5. Open questions

1. **Verify the [K] items**, especially: Gap +7% / +5%; Luca 5–9%; JOLTS ~4%; CPS ~3%; the Hinkin & Tracey cost; the Swedish rules on sick pay, holiday pay, LAS notice and overtime caps.
2. **Café service-time and patience data.** Can Andon share Stockholm POS timestamps or Pion traces? If not, run a two-day stopwatch study in a partner café.
3. **The morale→output effect is only correlational.** Should results be reported across a sweep of effect sizes?
4. **Is the agent the legal employer, or acting for a human employer of record** (as at Andon Market)? This decides who is liable (overlaps D09).
5. **Is 15-minute staffing resolution enough**, or does the espresso peak need 5-minute bins?
6. **How should the oracle baseline handle parameters a real manager cannot know**, beyond the "realistic" estimate-then-optimise variant?
7. **How should the four sub-scores combine** without double-counting fines that already reduce profit (overlaps D05/D09)?
8. **Which model family should voice the staff**, and how much does that choice move agent scores? Rotate across families (D06).
9. **Do ~30-minute wake-up cycles unfairly penalise agents during fast peaks?** Should a queue-length alarm be added?
10. **Should Sweden's collective-agreement layer be a single table**, or simulated with union-representative events?

---

## 6. Sources

**[P] Read this session**
- Anthropic, *Project Vend* (phase 1): https://www.anthropic.com/research/project-vend-1
- Anthropic, *Project Vend phase two*: https://www.anthropic.com/research/project-vend-2
- Ciw (MIT; v3.2.7, Dec 2025): https://github.com/CiwPython/Ciw
  - balking: https://github.com/CiwPython/Ciw/blob/master/docs/Guides/CustomerBehaviour/baulking.rst
  - reneging: https://github.com/CiwPython/Ciw/blob/master/docs/Guides/CustomerBehaviour/reneging.rst
  - time-dependent arrivals: https://github.com/CiwPython/Ciw/blob/master/docs/Guides/Distributions/time_dependent.rst
  - server schedules and overtime: https://github.com/CiwPython/Ciw/blob/master/docs/Guides/Services/server_schedule.rst
  - pre-emption: https://github.com/CiwPython/Ciw/blob/master/docs/Guides/Services/preemption.rst
  - server-dependent rates: https://github.com/CiwPython/Ciw/blob/master/docs/Guides/System/behaviour/server_dependent_dist.rst
  - seeds: https://github.com/CiwPython/Ciw/blob/master/docs/Guides/Simulation/seed.rst
- pyworkforce (MIT; v0.5.4, Jun 2026): https://github.com/rodrigo-arenas/pyworkforce ; https://pypi.org/project/pyworkforce/
- OR-Tools shift scheduling: https://github.com/google/or-tools/blob/stable/examples/python/shift_scheduling_sat.py
- SimPy 4.1.2 (MIT): https://pypi.org/project/simpy/ ; https://gitlab.com/team-simpy/simpy
- YC-Bench employee model: https://github.com/collinear-ai/yc-bench/blob/main/system_design/06_employee_model.md
- TheAgentCompany: https://github.com/TheAgentCompany/TheAgentCompany/blob/main/docs/EVALUATION.md
- Concordia: https://github.com/google-deepmind/concordia
- Overcooked-AI: https://github.com/HumanCompatibleAI/overcooked_ai

**[S] Via sibling dossiers**
- Lu et al. (Columbia summary): https://business.columbia.edu/insights/brand-talk/research-cost-queue
- NRA: https://restaurant.org/research-and-media/research/restaurant-economic-insights/analysis-commentary/restaurant-occupancy-costs-were-more-than-5-of-sales-in-2024/
- ATO: https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/small-business-benchmarks/in-detail/coffee-shops
- OnPay (payroll taxes): https://onpay.com/insights/complete-guide-taxable-wage-bases/
- Azets (Sweden): https://www.azets.com/en-se/insights/blog/temporarily-reduced-employer-social-security-contributions-for-young-people
- SF minimum wage: https://www.sf.gov/information/minimum-wage-ordinance
- SF formula retail: https://sf.gov/information/formula-retail-employee-rights-ordinance
- NRSS: https://lpresearch.org/2023-nrss-release-9-26-23/
- Bernhardt et al. 2009: https://www.nelp.org/publication/broken-laws-unprotected-workers/
- Andon press:
  - https://the-decoder.com/an-ai-boss-fired-its-first-employee-but-only-after-humans-reminded-it-of-its-own-rules/
  - https://thenextweb.com/news/andon-market-luna-ai-store-manager-fires-employee
  - https://abc7chicago.com/post/artificial-intelligence-boss-named-luna-running-san-francisco-store-andon-market-cow-hollow-neighborhood/18943220/
  - https://dailycoffeenews.com/2026/05/13/an-ai-cafe-operator-is-messaging-baristas-at-midnight-and-making-weird-purchasing-orders/
  - https://www.pbs.org/newshour/world/the-barista-is-human-but-an-ai-agent-runs-this-experimental-swedish-cafe

**[K] Literature (not re-opened; lookup links)**
- Allon, Federgruen & Pierson 2011, *MSOM* 13(4): https://scholar.google.com/scholar?q=%22How+much+is+a+reduction+of+waiting+time+worth%22
- Avramidis, Deslauriers & L'Ecuyer 2004, *Mgmt Sci* 50(7): https://scholar.google.com/scholar?q=%22Modeling+daily+arrivals+to+a+telephone+call+center%22
- Batt & Terwiesch 2015, *Mgmt Sci* 61(1): https://scholar.google.com/scholar?q=%22Waiting+patiently%22+emergency+department+abandonment
- Brown et al. 2005, *JASA* 100(469): https://scholar.google.com/scholar?q=%22Statistical+analysis+of+a+telephone+call+center%22
- Darr, Argote & Epple 1995, *Mgmt Sci* 41(11): https://scholar.google.com/scholar?q=%22acquisition%2C+transfer%2C+and+depreciation+of+knowledge+in+service+organizations%22
- Defraeye & Van Nieuwenhuyse 2016, *Omega* 58: https://scholar.google.com/scholar?q=%22Staffing+and+scheduling+under+nonstationary+demand+for+service%22
- Dube, Lester & Reich 2016, *J. Labor Econ.* 34(3): https://scholar.google.com/scholar?q=%22Minimum+wage+shocks%2C+employment+flows%2C+and+labor+market+frictions%22
- Ernst et al. 2004, *EJOR* 153(1): https://scholar.google.com/scholar?q=%22Staff+scheduling+and+rostering%3A+A+review%22
- Fisher, Gallino & Netessine 2021, *MSOM*: https://scholar.google.com/scholar?q=%22Setting+retail+staffing+levels%22
- Garnett, Mandelbaum & Reiman 2002, *MSOM* 4(3): https://scholar.google.com/scholar?q=%22Designing+a+call+center+with+impatient+customers%22
- Green, Kolesar & Whitt 2007, *POMS* 16(1): https://scholar.google.com/scholar?q=%22Coping+with+time-varying+demand+when+setting+staffing+requirements%22
- Halfin & Whitt 1981, *Oper. Res.* 29(3): https://scholar.google.com/scholar?q=%22Heavy-traffic+limits+for+queues+with+many+exponential+servers%22
- Harter, Schmidt & Hayes 2002, *J. Appl. Psych.* 87(2): https://scholar.google.com/scholar?q=%22Business-unit-level+relationship+between+employee+satisfaction%2C+employee+engagement%22
- Heskett et al. 1994, *HBR*: https://scholar.google.com/scholar?q=%22Putting+the+service-profit+chain+to+work%22
- Hinkin & Tracey 2000, *Cornell HRA Quarterly* 41(3): https://scholar.google.com/scholar?q=Hinkin+Tracey+%22The+cost+of+turnover%22
- Kc & Terwiesch 2009, *Mgmt Sci* 55(9): https://scholar.google.com/scholar?q=%22Impact+of+workload+on+service+time+and+patient+safety%22
- Keiningham et al. 2007, *J. Marketing* 71(3): https://scholar.google.com/scholar?q=%22longitudinal+examination+of+net+promoter%22
- Kesavan, Lambert, Williams & Pendem 2022, *Mgmt Sci*: https://scholar.google.com/scholar?q=%22Doing+well+by+doing+good%22+Gap+scheduling
- Kim & Whitt 2014, *MSOM* 16(3): https://scholar.google.com/scholar?q=%22well+modeled+by+nonhomogeneous+Poisson+processes%22
- Larson 1987, *Oper. Res.* 35(6): https://scholar.google.com/scholar?q=%22Perspectives+on+queues%3A+Social+justice%22
- Lewis & Shedler 1979, *NRLQ* 26(3): https://scholar.google.com/scholar?q=%22Simulation+of+nonhomogeneous+Poisson+processes+by+thinning%22
- Lu, Musalem, Olivares & Schilkrut 2013, *Mgmt Sci* 59(8): https://scholar.google.com/scholar?q=%22Measuring+the+effect+of+queues+on+customer+purchases%22
- Luca 2016, HBS WP 12-016: https://scholar.google.com/scholar?q=%22Reviews%2C+reputation%2C+and+revenue%22+Yelp
- Maister 1985, in *The Service Encounter*: https://scholar.google.com/scholar?q=Maister+%22psychology+of+waiting+lines%22
- Mandelbaum & Zeltyn 2013, *Queueing Systems* 75: https://scholar.google.com/scholar?q=%22Data-stories+about+%28im%29patient+customers%22
- Mani, Kesavan & Swaminathan 2015, *POMS* 24(2): https://scholar.google.com/scholar?q=%22impact+of+understaffing+on+sales+and+profitability%22
- Perdikaki, Kesavan & Swaminathan 2012, *MSOM* 14(1): https://scholar.google.com/scholar?q=%22Effect+of+traffic+on+sales+and+conversion+rates%22
- Reichheld 2003, *HBR*: https://scholar.google.com/scholar?q=%22The+one+number+you+need+to+grow%22
- Staats & Gino 2012, *Mgmt Sci* 58(6): https://scholar.google.com/scholar?q=%22Specialization+and+variety+in+repetitive+tasks%22
- Tan & Netessine 2014, *Mgmt Sci* 60(6): https://scholar.google.com/scholar?q=%22When+does+the+devil+make+work%22
- Ton 2009, HBS WP 09-040: https://scholar.google.com/scholar?q=Ton+%22effect+of+labor+on+profitability%22
- Ton & Huckman 2008, *Org. Sci.* 19(1): https://scholar.google.com/scholar?q=%22Managing+the+impact+of+employee+turnover+on+performance%22
- Van den Bergh et al. 2013, *EJOR* 226(3): https://scholar.google.com/scholar?q=%22Personnel+scheduling%3A+A+literature+review%22
- Whitt 2006, *POMS* 15(1): https://scholar.google.com/scholar?q=%22Staffing+a+call+center+with+uncertain+arrival+rate+and+absenteeism%22

**[K] Statistics and law (official pages, not opened)**
- BLS: JOLTS https://www.bls.gov/jlt/ ; OEWS https://www.bls.gov/oes/ ; CPS https://www.bls.gov/cps/
- US Department of Labor: overtime https://www.dol.gov/agencies/whd/overtime ; tipped employees https://www.dol.gov/agencies/whd/fact-sheets/15-tipped-employees-flsa
- California DLSE: https://www.dir.ca.gov/dlse/ ; AB 1228: https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB1228
- Seattle: https://www.seattle.gov/laborstandards ; Oregon BOLI: https://www.oregon.gov/boli/ ; NYC DCWP: https://www.nyc.gov/site/dca/
- EU Working Time Directive 2003/88/EC: https://eur-lex.europa.eu/eli/dir/2003/88/oj
- Sweden: Arbetstidslag (1982:673) and LAS (1982:80): https://www.riksdagen.se/ ; Gröna Riksavtalet: https://www.visita.se/ ; https://www.hrf.net/
