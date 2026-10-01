"""S5 -- Continuous fermenter (reaction-kinetics / process-control family). SEALED.

Hidden mechanisms:
  * feedstock arrives in lots of random length; lot strength lognormal with occasional weak lots
  * growth: substrate-INHIBITED kinetics x product inhibition (THRESHOLD-like) x temperature optimum
  * reaction heat proportional to growth; PI cooling controller acting on a LAGGED sensor
    with SATURATING cooling capacity
  * thermal kill (REGIME SWITCH): above ~41 C the death rate jumps -> biomass crash;
    residual substrate build-up then inhibits regrowth (FEEDBACK)
Observed hourly: biomass, substrate, product, temperature, cooling_duty.
"""
import numpy as np

T = 400
DT = 0.1
SUB = int(round(1 / DT))
COLUMNS = ["biomass", "substrate", "product", "temperature", "cooling_duty"]

P = dict(
    D0=0.10, Sin0=20.0, lot_h=1 / 60.0, lot_sd=0.08, weak_p=0.10, weak_f=0.6,
    mumax=0.45, Ks=0.3, Ki=15.0, Pc=45.0, Pn=1.5, Topt=34.0, Tw=6.0,
    Y=0.45, ms=0.02, alpha=2.0, betap=0.03,
    kd0=0.005, kd_hot=0.25, T_kill=41.0,
    hgen=4.0, hm=0.05, ka=0.25, umax=5.0, kloss=0.05, Tamb=22.0,
    Kp=1.5, Kint=0.3, tau_s=1.0, Tset0=34.0, burn=150,
)


def run(R, seed, interventions=(), params=None):
    p = dict(P)
    if params:
        p.update(params)
    rng = np.random.default_rng(seed)
    X = rng.uniform(6.0, 9.0, R)
    S = rng.uniform(0.5, 2.0, R)
    Pp = rng.uniform(15.0, 20.0, R)
    Tm = np.full(R, p["Tset0"])
    Ts = Tm.copy()
    I = np.full(R, 2.0)
    lot = np.ones(R)
    D = np.full(R, p["D0"])
    Sin_mult = np.ones(R)
    Tset = np.full(R, p["Tset0"])
    obs = {c: np.zeros((R, T)) for c in COLUMNS}
    for hr in range(-p["burn"], T):
        for iv in interventions:
            if iv["start"] != hr:
                continue
            if iv["type"] == "feed_conc":
                Sin_mult[:] = iv["size"]
            elif iv["type"] == "dilution":
                D[:] = iv["size"]
            elif iv["type"] == "setpoint":
                Tset[:] = iv["size"]
            else:
                raise ValueError(iv)
        newlot = rng.random(R) < p["lot_h"]
        f = np.exp(rng.normal(0, p["lot_sd"], R)) * np.where(rng.random(R) < p["weak_p"], p["weak_f"], 1.0)
        lot = np.where(newlot, f, lot)
        Sin = p["Sin0"] * lot * Sin_mult
        usum = np.zeros(R)
        for s in range(SUB):
            fP = np.clip(1 - (np.maximum(Pp, 0) / p["Pc"]) ** p["Pn"], 0, 1)
            fT = np.exp(-((Tm - p["Topt"]) / p["Tw"]) ** 2)
            mu = p["mumax"] * S / (p["Ks"] + S + S ** 2 / p["Ki"]) * fP * fT
            kd = p["kd0"] + p["kd_hot"] / (1 + np.exp(-(Tm - p["T_kill"]) / 0.5))
            err = Ts - Tset
            u = np.clip(p["Kp"] * err + I, 0, p["umax"])
            # anti-windup: integrate only when not saturated in the pushing direction
            sat = ((u >= p["umax"]) & (err > 0)) | ((u <= 0) & (err < 0))
            I = np.where(sat, I, I + DT * p["Kint"] * err)
            dX = (mu - kd - D) * X
            dS = D * (Sin - S) - mu * X / p["Y"] - p["ms"] * X
            dP = (p["alpha"] * mu + p["betap"]) * X - D * Pp
            dT = p["hgen"] * mu * X + p["hm"] * X * np.exp(p["ka"] * (Tm - p["Topt"])) - u - p["kloss"] * (Tm - p["Tamb"])
            X = np.maximum(X + DT * dX, 1e-4)
            S = np.maximum(S + DT * dS, 0.0)
            Pp = np.maximum(Pp + DT * dP, 0.0)
            Tm = Tm + DT * dT
            Ts = Ts + DT * (Tm - Ts) / p["tau_s"]
            usum += u
        X = X * np.exp(rng.normal(0, 0.01, R))  # small process noise
        if hr >= 0:
            obs["biomass"][:, hr] = X * np.exp(rng.normal(0, 0.04, R))
            obs["substrate"][:, hr] = np.maximum(S + rng.normal(0, 0.15, R), 0.0)
            obs["product"][:, hr] = Pp * np.exp(rng.normal(0, 0.03, R))
            obs["temperature"][:, hr] = Tm + rng.normal(0, 0.15, R)
            obs["cooling_duty"][:, hr] = usum / SUB / p["umax"]
    return obs
