"""S1 -- Pond community (population dynamics family). SEALED.

Hidden mechanisms:
  * nutrient inflow with seasonal cycle and heavy-tailed storm pulses (Pareto)
  * algae growth: nutrient-limited, self-limited, grazed (saturating)
  * grazers reproduce into a juvenile pipeline with a fixed MATURATION DELAY (hidden stage)
  * fish predation on grazers with a sigmoid (type-III) functional response
  * hidden dissolved oxygen tracks algae with lag; below a THRESHOLD (hypoxia)
    grazers/juveniles/fish suffer extra mortality -> alternative turbid regime
    (positive feedback: fewer grazers -> more algae -> less oxygen)
Observed daily: nutrient, algae, grazers, fish (all with measurement noise).
"""
import numpy as np

T = 400
DT = 0.25
SUB = int(round(1 / DT))
COLUMNS = ["nutrient", "algae", "grazers", "fish"]

P = dict(
    I0=0.76, seas_amp=0.35, storm_p=0.010, storm_scale=3.0, storm_alpha=1.5, storm_cap=45.0,
    dN=0.10, rA=1.0, KN=1.5, KA=110.0, yN=0.06, mA=0.15,
    cg=0.0825, hA=100.0, iG=0.02, KG=1500.0, bg=0.53, delay=15, sj=0.55, dg=0.01, imm=0.4,
    pf=0.55, H=400.0, ef=0.015, df=0.005, fimm=0.03,
    Osat=9.0, Oseas=1.2, cO=0.105, kO=0.5, Ocrit=2.6,
    hyp_g=0.30, hyp_j=0.30, hyp_f=0.07,
    sigA=0.10, sigG=0.05,
)


def run(R, seed, interventions=(), params=None):
    p = dict(P)
    if params:
        p.update(params)
    rng = np.random.default_rng(seed)
    # initial conditions (per episode)
    N = rng.uniform(2.0, 4.0, R)
    A = rng.uniform(10.0, 25.0, R)
    G = rng.uniform(350.0, 650.0, R)
    F = rng.uniform(25.0, 40.0, R)
    O = np.full(R, 7.0)
    D = p["delay"] * SUB
    juv = np.zeros((R, D))  # juvenile cohorts pipeline (per substep)
    juv += (p["bg"] * G * A / (A + p["hA"] + p["iG"] * G) * np.maximum(1 - G / p["KG"], 0) * DT)[:, None]
    ptr = 0
    nut_mult = np.ones(R)
    obs = {c: np.zeros((R, T)) for c in COLUMNS}
    ivs = sorted(interventions, key=lambda d: d["start"])
    BURN = int(p.get("burn", 365))
    for day in range(-BURN, T):
        # interventions applied at the start of the day
        for iv in ivs:
            if iv["start"] == day:
                if iv["type"] == "nutrient_load":
                    nut_mult[:] = iv["size"]
                elif iv["type"] == "fish_removal":
                    F *= (1.0 - iv["size"])
                elif iv["type"] == "grazer_stocking":
                    G += iv["size"]
                else:
                    raise ValueError(iv)
        # storms (daily)
        storm = rng.random(R) < p["storm_p"]
        pulse = np.where(storm, np.minimum(p["storm_scale"] * rng.random(R) ** (-1 / p["storm_alpha"]), p["storm_cap"]), 0.0)
        N += pulse * nut_mult
        seas = np.sin(2 * np.pi * (day - 30) / 365.0)
        inflow = p["I0"] * (1 + p["seas_amp"] * seas) * nut_mult
        Osat = p["Osat"] - p["Oseas"] * seas
        epsA = rng.normal(0, p["sigA"], R)
        epsG = rng.normal(0, p["sigG"], R)
        for s in range(SUB):
            hyp = O < p["Ocrit"]
            growth = p["rA"] * A * N / (N + p["KN"]) * np.maximum(1 - A / p["KA"], -0.5) * np.exp(epsA)
            graze_pc = p["cg"] * A / (A + p["hA"] + p["iG"] * G)
            graze = graze_pc * G
            dA = growth - p["mA"] * A - graze
            dN = inflow - p["dN"] * N - p["yN"] * np.maximum(growth, 0)
            births = p["bg"] * G * A / (A + p["hA"] + p["iG"] * G) * np.maximum(1 - G / p["KG"], 0) * np.exp(epsG)
            pred = p["pf"] * F * G ** 2 / (G ** 2 + p["H"] ** 2)
            # juvenile pipeline: oldest cohort matures now
            mature = juv[:, ptr] * p["sj"]
            juv[:, ptr] = births * DT
            ptr = (ptr + 1) % D
            if hyp.any():
                juv[hyp] *= np.exp(-p["hyp_j"] * DT)
            dG = mature / DT - p["dg"] * G - pred - hyp * p["hyp_g"] * G + p["imm"]
            dF = p["ef"] * pred - p["df"] * F - hyp * p["hyp_f"] * F + p["fimm"]
            dO = p["kO"] * (Osat - p["cO"] * A - O)
            A = np.maximum(A + DT * dA, 0.05)
            N = np.maximum(N + DT * dN, 0.0)
            G = np.maximum(G + DT * dG, 0.0)
            F = np.maximum(F + DT * dF, 0.0)
            O = O + DT * dO
        if day < 0:
            continue
        obs["nutrient"][:, day] = N * np.exp(rng.normal(0, 0.08, R))
        obs["algae"][:, day] = A * np.exp(rng.normal(0, 0.10, R))
        obs["grazers"][:, day] = np.round(G * np.exp(rng.normal(0, 0.12, R)))
        obs["fish"][:, day] = rng.poisson(F * 0.8)  # standardized survey count
    return obs
