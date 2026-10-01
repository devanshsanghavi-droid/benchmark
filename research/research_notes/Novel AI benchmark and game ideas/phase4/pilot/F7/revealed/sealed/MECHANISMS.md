# Hidden mechanisms and question rationale (sealed)

## S1 pond (population dynamics)
Nutrient inflow with a seasonal cycle and Pareto storm pulses feeds algae growth, which is nutrient-limited and self-limited. Grazers feed on algae with interference and density-dependent recruitment, and juveniles pass through a hidden 15-day maturation pipeline. Fish prey on grazers with a sigmoid (type III) response, and a small number of fish immigrate. Hidden oxygen tracks algae with a lag and a seasonal saturation level; below 2.6 (hypoxia), grazers, juveniles and fish die off. This gives an alternative turbid regime: in baseline it is rare and recovers in winter, but under strong enrichment it is persistent.
- **Q1** (nutrients x2.2 -> grazers on day 350): regime shift. Grazers mostly collapse, whereas extrapolating the x1.5 experiment predicts an increase.
- **Q2** (90% fish removal -> grazers, days 250-299): trophic release, saturating at the density-dependence cap.
- **Q3** (+1500 grazers -> algae, days 210-249): overgrazing drives algae to about 0; the +300 experiment shows almost nothing.

## S2 call desk (queueing)
- Demand follows an hour-of-day profile with a weekend dip, gamma day noise and rare Pareto incident surges.
- Callers abandon with an age-bucketed hazard, and **retrials** follow (p = 0.5, 1-4 h later).
- **Rush mode** switches on when the line exceeds 12: calls get shorter, but 30% of rushed calls return as repeat calls 12-36 h later.
- A hidden **backup pool** adds 3 agents after a 30-minute delay when the line exceeds 30 (07:00-22:00 only).

Questions:
- **Q1** (demand x1.6): abandonment rises superlinearly.
- **Q2** (+3 staff): offered calls fall even though fresh demand is unchanged, because retrials and repeats disappear.
- **Q3** (4-hour outage): a superlinear backlog, with retrials.

## S3 adoption (network contagion)
- A fixed hidden 3-community graph with heavy-tailed degrees; B and C are strongly linked, A is weakly linked.
- **Complex contagion**: adoption needs at least 2 active neighbours plus a personal fractional threshold, Beta(5, 9).
- Spontaneous adoption plus Pareto media shocks.
- Adopters stay active for at least 12 days, then lapse, then go through a refractory period before returning to susceptible.

Questions:
- **Q1** (45 seeds spread over the town): a nonlinear cascade.
- **Q2** (broadcast 0.03 for 5 days): a large synchronised wave.
- **Q3** (40 seeds in B -> C): spillover through the B-C links, with saturation.

## S4 auction (adaptive agents)
- First-price auction with a reserve. Bidder values combine lognormal bases and a hidden bull/bear Markov regime.
- **Adaptive shading**: bidders shade more after a win and less after a loss they could have won.
- **Weekly budgets** reset every 7 rounds, so prices fall within each week.
- **Discouragement**: a bidder with no win for more than 30 rounds exits with a hazard and returns after a geometric absence.
- Bidders bid max(shaded value, reserve) when their value is at least the reserve.

Questions:
- **Q1** (reserve 75): a threshold. Reserves of 40 and 55 have no effect, but 75 causes unsold rounds because of budget limits and late-week weakness.
- **Q2** (+20 entrants): exits erode the gain.
- **Q3** (budget x0.5): an asymmetric response relative to the x1.5 experiment.

## S5 fermenter (kinetics and control)
- Substrate-inhibited growth x product inhibition x a temperature optimum.
- Reaction heat plus Arrhenius-type maintenance heat (**thermal runaway feedback**).
- A PI controller acts on a lagged sensor with **saturating cooling**; a thermal kill switches on above about 41 C.
- Feed lots vary in strength, with occasional weak lots.

Questions:
- **Q1** (feed x1.8): product plateaus at about 25 because cooling saturates and temperature rises; linear extrapolation predicts about 33.
- **Q2** (D = 0.24): bimodal washout, because heat-limited growth falls below the dilution rate.
- **Q3** (D = 0.17): cooling saturates and temperature settles at about 37-38 C.
