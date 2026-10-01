"""S4 -- Repeated sealed-bid auction with adaptive bidders (market family). SEALED.

Hidden mechanisms:
  * one lot per round, first-price sealed bid with a reserve price
  * bidder private base values (lognormal) x a hidden two-state market regime (REGIME SWITCH,
    Markov) x idiosyncratic noise
  * ADAPTIVE SHADING: bidders shade more after wins, less after losses they could have won
  * WEEKLY BUDGETS (7 rounds) that reset -> strong bidders drop out late in the week
  * DISCOURAGEMENT FEEDBACK: bidders who have not won for a long time leave (hazard) and
    come back after a random absence (DELAY) with reset shading
Observed per round: reserve, sold, price (blank if unsold), revenue, n_bids, active_bidders.
"""
import numpy as np

T = 250
COLUMNS = ["reserve", "sold", "price", "revenue", "n_bids", "active_bidders"]
M = 64  # bidder slots

P = dict(
    n0=26, mu_log=np.log(50.0), mu_sd=0.35, noise=0.08,
    bull=1.12, bear=0.88, switch=0.015,
    sig_lo=0.65, sig_hi=0.80, d_win=0.015, d_lose=0.025, sig_min=0.45, sig_max=0.97,
    budget=1.6, week=7,
    L=30, exit_h=0.04, ret_mean=50.0,
    reserve0=20.0, burn=150,
)


def run(R, seed, interventions=(), params=None):
    p = dict(P)
    if params:
        p.update(params)
    rng = np.random.default_rng(seed)
    mu = np.exp(rng.normal(p["mu_log"], p["mu_sd"], (R, M)))
    member = np.zeros((R, M), bool)     # belongs to market population
    member[:, :p["n0"]] = True
    present = member.copy()
    away = np.zeros((R, M), np.int64)   # rounds remaining away
    sig = rng.uniform(p["sig_lo"], p["sig_hi"], (R, M))
    since = rng.integers(0, 20, (R, M))
    regime = rng.random(R) < 0.5        # True = bull
    bmult = 1.0
    spent = np.zeros((R, M))
    reserve = np.full(R, p["reserve0"])
    obs = {c: np.zeros((R, T)) for c in COLUMNS}
    rows = np.arange(R)
    for t in range(-p["burn"], T):
        for iv in interventions:
            if iv["start"] != t:
                continue
            if iv["type"] == "reserve":
                reserve[:] = iv["size"]
            elif iv["type"] == "entrants":
                k = int(iv["size"])
                for r in range(R):
                    free = np.where(~member[r])[0][:k]
                    member[r, free] = True
                    present[r, free] = True
                    away[r, free] = 0
                    mu[r, free] = np.exp(rng.normal(p["mu_log"], p["mu_sd"], len(free)))
                    sig[r, free] = rng.uniform(p["sig_lo"], p["sig_hi"], len(free))
                    since[r, free] = 0
            elif iv["type"] == "budget":
                bmult = iv["size"]
            else:
                raise ValueError(iv)
        if (t % p["week"]) == 0:
            spent[:] = 0.0
        # regime switch
        sw = rng.random(R) < p["switch"]
        regime = np.where(sw, ~regime, regime)
        mfac = np.where(regime, p["bull"], p["bear"])
        v = mu * mfac[:, None] * np.exp(rng.normal(0, p["noise"], (R, M)))
        left = p["budget"] * bmult * mu - spent
        bid = np.maximum(sig * v, reserve[:, None])
        bid = np.minimum(bid, left)
        can = present & (v >= reserve[:, None]) & (bid >= reserve[:, None])
        bidm = np.where(can, bid, -1.0)
        win = bidm.argmax(1)
        best = bidm[rows, win]
        sold = best >= 0
        price = np.where(sold, best, np.nan)
        # learning
        won = np.zeros((R, M), bool)
        won[rows[sold], win[sold]] = True
        spent[won] += np.repeat(best[sold], 1)
        sig = np.where(won, sig - p["d_win"], sig)
        couldwin = can & ~won & (v > np.where(sold, best, 0)[:, None])[...]
        sig = np.where(couldwin, sig + p["d_lose"], sig)
        sig = np.clip(sig, p["sig_min"], p["sig_max"])
        since = np.where(won, 0, since + present)
        # exits and returns
        ex = present & (since > p["L"]) & (rng.random((R, M)) < p["exit_h"])
        present[ex] = False
        away[ex] = rng.geometric(1.0 / p["ret_mean"], ex.sum())
        away[~present & member] -= 1
        back = member & ~present & (away <= 0)
        present[back] = True
        sig[back] = rng.uniform(p["sig_lo"], p["sig_hi"], back.sum())
        since[back] = 0
        if t >= 0:
            obs["reserve"][:, t] = reserve
            obs["sold"][:, t] = sold
            obs["price"][:, t] = price
            obs["revenue"][:, t] = np.where(sold, best, 0.0)
            obs["n_bids"][:, t] = can.sum(1)
            obs["active_bidders"][:, t] = present.sum(1)
    return obs
