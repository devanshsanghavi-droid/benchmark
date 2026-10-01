"""Unrun Lab pilot -- sealed configuration: simulators, experiment menus, questions. SEALED."""

QUANTILES = [0.05, 0.25, 0.50, 0.75, 0.95]
QKEYS = ["q05", "q25", "q50", "q75", "q95"]
N_TRUTH = 10000

# null ("no change") value per intervention type, used by the naive extrapolator and
# published in the intervention menus. mode: multiplier / additive / set
IV_TYPES = {
    "nutrient_load":   dict(mode="multiplier", null=1.0),
    "fish_removal":    dict(mode="additive", null=0.0),
    "grazer_stocking": dict(mode="additive", null=0.0),
    "demand":          dict(mode="multiplier", null=1.0),
    "staff_day":       dict(mode="additive", null=0.0),
    "outage":          dict(mode="additive", null=0.0, size_field="duration"),
    "seed":            dict(mode="additive", null=0.0),
    "friction":        dict(mode="multiplier", null=1.0),
    "broadcast":       dict(mode="additive", null=0.0),
    "reserve":         dict(mode="set", null=20.0),
    "entrants":        dict(mode="additive", null=0.0),
    "budget":          dict(mode="multiplier", null=1.0),
    "feed_conc":       dict(mode="multiplier", null=1.0),
    "dilution":        dict(mode="set", null=0.10),
    "setpoint":        dict(mode="set", null=34.0),
}

SIMS = {
    "S1": dict(module="sim_s1", folder="S1_pond", n_hist=25, time="day", grouped=False),
    "S2": dict(module="sim_s2", folder="S2_calldesk", n_hist=30, time="hour", grouped=False),
    "S3": dict(module="sim_s3", folder="S3_adoption", n_hist=28, time="day", grouped=True),
    "S4": dict(module="sim_s4", folder="S4_auction", n_hist=40, time="round", grouped=False),
    "S5": dict(module="sim_s5", folder="S5_fermenter", n_hist=25, time="hour", grouped=False),
}

# Fixed pilot experiment menus (stand-in for solver-chosen experiments): 20 sample paths each.
EXPERIMENTS = {
    "S1": [
        dict(id="S1-E1", paths=4, iv=[dict(type="nutrient_load", start=100, size=1.5)]),
        dict(id="S1-E2", paths=3, iv=[dict(type="nutrient_load", start=100, size=0.5)]),
        dict(id="S1-E3", paths=4, iv=[dict(type="fish_removal", start=150, size=0.4)]),
        dict(id="S1-E4", paths=3, iv=[dict(type="grazer_stocking", start=200, size=300)]),
        dict(id="S1-E5", paths=3, iv=[dict(type="nutrient_load", start=50, size=1.25)]),
        dict(id="S1-E6", paths=3, iv=[dict(type="nutrient_load", start=100, size=1.5), dict(type="fish_removal", start=150, size=0.4)]),
    ],
    "S2": [
        dict(id="S2-E1", paths=4, iv=[dict(type="demand", start=48, size=1.15)]),
        dict(id="S2-E2", paths=3, iv=[dict(type="demand", start=48, size=0.85)]),
        dict(id="S2-E3", paths=4, iv=[dict(type="staff_day", start=24, size=-1)]),
        dict(id="S2-E4", paths=3, iv=[dict(type="staff_day", start=24, size=1)]),
        dict(id="S2-E5", paths=3, iv=[dict(type="outage", start=82, duration=1)]),
        dict(id="S2-E6", paths=3, iv=[dict(type="outage", start=206, duration=2)]),
    ],
    "S3": [
        dict(id="S3-E1", paths=4, iv=[dict(type="seed", start=20, size=15, community="B")]),
        dict(id="S3-E2", paths=3, iv=[dict(type="seed", start=20, size=15, community="all")]),
        dict(id="S3-E3", paths=3, iv=[dict(type="seed", start=20, size=15, community="A")]),
        dict(id="S3-E4", paths=4, iv=[dict(type="broadcast", start=60, size=0.01, duration=5)]),
        dict(id="S3-E5", paths=3, iv=[dict(type="friction", start=0, size=0.7)]),
        dict(id="S3-E6", paths=3, iv=[dict(type="friction", start=0, size=1.3)]),
    ],
    "S4": [
        dict(id="S4-E1", paths=3, iv=[dict(type="reserve", start=100, size=40)]),
        dict(id="S4-E2", paths=4, iv=[dict(type="reserve", start=100, size=55)]),
        dict(id="S4-E3", paths=4, iv=[dict(type="entrants", start=80, size=5)]),
        dict(id="S4-E4", paths=3, iv=[dict(type="budget", start=50, size=1.5)]),
        dict(id="S4-E5", paths=3, iv=[dict(type="budget", start=50, size=0.8)]),
        dict(id="S4-E6", paths=3, iv=[dict(type="entrants", start=150, size=10)]),
    ],
    "S5": [
        dict(id="S5-E1", paths=4, iv=[dict(type="feed_conc", start=100, size=1.3)]),
        dict(id="S5-E2", paths=3, iv=[dict(type="feed_conc", start=100, size=0.7)]),
        dict(id="S5-E3", paths=3, iv=[dict(type="dilution", start=150, size=0.12)]),
        dict(id="S5-E4", paths=3, iv=[dict(type="dilution", start=150, size=0.14)]),
        dict(id="S5-E5", paths=2, iv=[dict(type="dilution", start=150, size=0.08)]),
        dict(id="S5-E6", paths=3, iv=[dict(type="setpoint", start=100, size=37)]),
        dict(id="S5-E7", paths=2, iv=[dict(type="setpoint", start=100, size=31)]),
    ],
}

# Outcome spec: column, and either step (single time index) or agg over [from, to] inclusive.
# For S3, 'group' selects a community (0=A, 1=B, 2=C); absent = summed over communities.
QUESTIONS = [
    dict(id="S1-Q1", sim="S1", iv=[dict(type="nutrient_load", start=100, size=2.2)],
         out=dict(col="grazers", step=350),
         text="From day 100 onward the nutrient inflow is multiplied by 2.2 (nutrient_load, size 2.2, start 100). Forecast the recorded value of `grazers` on day 350."),
    dict(id="S1-Q2", sim="S1", iv=[dict(type="fish_removal", start=150, size=0.9)],
         out=dict(col="grazers", agg="mean", **{"from": 250, "to": 299}),
         text="On day 150, 90% of the fish are removed (fish_removal, size 0.9, start 150). Forecast the mean of the recorded `grazers` values over days 250-299 (inclusive)."),
    dict(id="S1-Q3", sim="S1", iv=[dict(type="grazer_stocking", start=200, size=1500)],
         out=dict(col="algae", agg="mean", **{"from": 210, "to": 249}),
         text="On day 200, 1500 adult grazers are added (grazer_stocking, size 1500, start 200). Forecast the mean of the recorded `algae` values over days 210-249 (inclusive)."),
    dict(id="S2-Q1", sim="S2", iv=[dict(type="demand", start=48, size=1.6)],
         out=dict(col="abandoned", agg="sum", **{"from": 216, "to": 335}),
         text="From the start of day 2 (hour 48) onward, new-customer demand is multiplied by 1.6 (demand, size 1.6, start hour 48). Forecast the total of `abandoned` over hours 216-335 (days 9-13, inclusive)."),
    dict(id="S2-Q2", sim="S2", iv=[dict(type="staff_day", start=24, size=3)],
         out=dict(col="offered", agg="sum", **{"from": 168, "to": 335}),
         text="From hour 24 (start of day 1) onward, 3 extra agents are added to every day shift (staff_day, size 3, start hour 24). Forecast the total of `offered` over hours 168-335 (days 7-13, inclusive)."),
    dict(id="S2-Q3", sim="S2", iv=[dict(type="outage", start=177, duration=4)],
         out=dict(col="abandoned", agg="sum", **{"from": 177, "to": 200}),
         text="A 4-hour outage starts at hour 177 (day 7, 09:00) and lasts through hour 180 (outage, start hour 177, duration 4). Forecast the total of `abandoned` over hours 177-200 (inclusive)."),
    dict(id="S3-Q1", sim="S3", iv=[dict(type="seed", start=20, size=45, community="all")],
         out=dict(col="active", step=50),
         text="On day 20, 45 non-practising residents chosen at random from the whole town are recruited (seed, size 45, community all, start 20). Forecast total `active` (sum over A, B and C) on day 50."),
    dict(id="S3-Q2", sim="S3", iv=[dict(type="broadcast", start=60, size=0.03, duration=5)],
         out=dict(col="active", step=75),
         text="A broadcast campaign with size 0.03 runs on days 60-64 (broadcast, size 0.03, start 60, duration 5). Forecast total `active` (sum over A, B and C) on day 75."),
    dict(id="S3-Q3", sim="S3", iv=[dict(type="seed", start=20, size=40, community="B")],
         out=dict(col="active", group=2, step=50),
         text="On day 20, 40 non-practising residents of neighbourhood B are recruited (seed, size 40, community B, start 20). Forecast `active` in neighbourhood C on day 50."),
    dict(id="S4-Q1", sim="S4", iv=[dict(type="reserve", start=100, size=75)],
         out=dict(col="revenue", agg="sum", **{"from": 150, "to": 249}),
         text="From round 100 onward the reserve price is 75 (reserve, size 75, start 100). Forecast total `revenue` over rounds 150-249 (inclusive)."),
    dict(id="S4-Q2", sim="S4", iv=[dict(type="entrants", start=80, size=20)],
         out=dict(col="active_bidders", step=200),
         text="At round 80, 20 new bidders join the market (entrants, size 20, start 80). Forecast `active_bidders` in round 200."),
    dict(id="S4-Q3", sim="S4", iv=[dict(type="budget", start=50, size=0.5)],
         out=dict(col="revenue", agg="sum", **{"from": 150, "to": 249}),
         text="From round 50 onward every bidder's spending allowance is multiplied by 0.5 (budget, size 0.5, start 50). Forecast total `revenue` over rounds 150-249 (inclusive)."),
    dict(id="S5-Q1", sim="S5", iv=[dict(type="feed_conc", start=100, size=1.8)],
         out=dict(col="product", step=300),
         text="From hour 100 onward the feed substrate concentration is multiplied by 1.8 (feed_conc, size 1.8, start 100). Forecast the recorded `product` at hour 300."),
    dict(id="S5-Q2", sim="S5", iv=[dict(type="dilution", start=150, size=0.24)],
         out=dict(col="biomass", agg="mean", **{"from": 300, "to": 399}),
         text="From hour 150 onward the dilution rate is set to 0.24 per hour (dilution, size 0.24, start 150). Forecast the mean of the recorded `biomass` over hours 300-399 (inclusive)."),
    dict(id="S5-Q3", sim="S5", iv=[dict(type="dilution", start=150, size=0.17)],
         out=dict(col="temperature", step=300),
         text="From hour 150 onward the dilution rate is set to 0.17 per hour (dilution, size 0.17, start 150). Forecast the recorded `temperature` at hour 300."),
]
