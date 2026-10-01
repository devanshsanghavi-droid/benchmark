"""S2 -- Support call desk (queueing / service family). SEALED.

Hidden mechanisms:
  * fresh demand: hour-of-day profile, weekend dip, day-level gamma noise, rare heavy-tailed
    incident surges (Pareto) that decay over hours
  * abandonment hazard rising with waiting time (age-bucketed patience)
  * RETRIAL FEEDBACK: abandoned callers call again 1-4 h later with prob. p_retry
  * RUSH MODE (threshold + delayed feedback): when the waiting line exceeds Q_rush, agents
    shorten calls, but a fraction of rushed calls come back as repeat calls 12-36 h later
  * BACKUP POOL (threshold + delay, not reported): when the line exceeds Q_backup, 3 extra
    agents join after 30 min, stay >= 2 h, and leave once the line is short (07:00-22:00 only)
Observed hourly: offered, answered, abandoned, queue_end, avg_wait_min, scheduled_agents.
Time: 14 days x 24 h = 336 hourly rows per episode (day 0 = Monday); 5-minute substeps.
"""
import numpy as np

DAYS = 14
T = DAYS * 24
SUB = 12  # 5-minute substeps per hour
K = 8     # waiting-age buckets (5 min each; last bucket absorbs >= 35 min)
COLUMNS = ["offered", "answered", "abandoned", "queue_end", "avg_wait_min", "scheduled_agents"]

PROFILE = np.array([4, 3, 3, 3, 3, 4, 6, 15, 35, 55, 62, 60, 50, 55, 58, 52, 45, 35, 25, 18, 12, 9, 6, 5], float)

P = dict(
    weekend=0.55, day_k=25.0,
    inc_p=0.04, inc_scale=35.0, inc_alpha=1.8, inc_cap=400.0, inc_decay=0.7,
    staff_wd=7, staff_we=4, staff_night=2,
    svc_norm=6.5, svc_rush=4.5, Q_rush=12, p_repeat=0.30,
    haz=[0.03, 0.06, 0.10, 0.18, 0.18, 0.18, 0.18, 0.18],
    p_retry=0.5, retry_kernel=[0.45, 0.30, 0.15, 0.10],
    Q_backup=30, backup_n=3, backup_delay=6, backup_min=24, backup_off=5,
)


def scheduled(hour_abs, p, staff_delta_from):
    d = hour_abs // 24
    h = hour_abs % 24
    dow = d % 7
    if 8 <= h < 20:
        base = p["staff_we"] if dow >= 5 else p["staff_wd"]
        return base
    return p["staff_night"]


def run(R, seed, interventions=(), params=None):
    p = dict(P)
    if params:
        p.update(params)
    rng = np.random.default_rng(seed)
    BURN_D = 2
    TT = (BURN_D + DAYS) * 24
    fut = np.zeros((R, TT + 48))  # extra (non-fresh) arrival intensity per hour
    Q = np.zeros((R, K), np.int64)
    busy = np.zeros(R, np.int64)
    haz = np.array(p["haz"])
    p_norm = 1 - np.exp(-5.0 / p["svc_norm"])
    p_rush = 1 - np.exp(-5.0 / p["svc_rush"])
    bk_state = np.zeros(R, np.int64)   # 0 off, 1 pending, 2 active
    bk_timer = np.zeros(R, np.int64)
    rk = np.array(p["retry_kernel"])
    rep_kernel = np.ones(25) / 25.0     # hours 12..36
    obs = {c: np.zeros((R, T)) for c in COLUMNS}
    # interventions
    dem_mult = 1.0
    dem_from = None
    staff_delta, staff_from = 0, None
    outages = []
    for iv in interventions:
        if iv["type"] == "demand":
            dem_mult, dem_from = iv["size"], iv["start"]
        elif iv["type"] == "staff_day":
            staff_delta, staff_from = int(iv["size"]), iv["start"]
        elif iv["type"] == "outage":
            outages.append((iv["start"], iv["start"] + iv["duration"]))
        else:
            raise ValueError(iv)
    dayfac = None
    waits = np.arange(K) * 5.0 + 2.5
    for H in range(-BURN_D * 24, T):
        hi = H + BURN_D * 24  # index into fut
        d, h = H // 24, H % 24
        if h == 0:
            dayfac = rng.gamma(p["day_k"], 1.0 / p["day_k"], R)
            # incidents
            inc = rng.random(R) < p["inc_p"]
            if inc.any():
                size = np.minimum(p["inc_scale"] * rng.random(R) ** (-1 / p["inc_alpha"]), p["inc_cap"])
                h0 = rng.integers(8, 17, R)
                for j in range(10):
                    idx = hi + h0 + j
                    add = np.where(inc, size * p["inc_decay"] ** j, 0.0)
                    fut[np.arange(R), idx] += add
        dow = (d % 7)
        lam = PROFILE[h] * (p["weekend"] if dow >= 5 else 1.0) * dayfac
        if dem_from is not None and H >= dem_from:
            lam = lam * dem_mult
        lam_tot = (lam + fut[:, hi]) / SUB
        sched = scheduled(H, p, None) if H >= 0 else scheduled(H + 7 * 24, p, None)
        if staff_from is not None and H >= staff_from and 8 <= h < 20:
            sched = max(sched + staff_delta, 0)
        out = any(a <= H < b for a, b in outages)
        off = np.zeros(R); ans = np.zeros(R); ab_h = np.zeros(R); wsum = np.zeros(R)
        rep_acc = np.zeros(R)
        for s in range(SUB):
            qtot = Q.sum(1)
            rush = qtot > p["Q_rush"]
            comp = rng.binomial(busy, np.where(rush, p_rush, p_norm))
            busy -= comp
            rep_acc += np.where(rush, comp, 0)
            # abandonment
            ab = rng.binomial(Q, haz)
            Q -= ab
            ab_s = ab.sum(1)
            ab_h += ab_s
            # backup pool logic
            day_ok = 7 <= h < 22
            trig = (qtot > p["Q_backup"]) & (bk_state == 0) & day_ok
            bk_state[trig] = 1
            bk_timer[trig] = p["backup_delay"]
            pend = bk_state == 1
            bk_timer[pend] -= 1
            act_now = pend & (bk_timer <= 0)
            bk_state[act_now] = 2
            bk_timer[act_now] = p["backup_min"]
            act = bk_state == 2
            bk_timer[act] -= 1
            leave = act & (((bk_timer <= 0) & (qtot < p["backup_off"])) | (not day_ok))
            bk_state[leave] = 0
            avail = sched + np.where(bk_state == 2, p["backup_n"], 0)
            if out:
                avail = np.zeros(R, np.int64)
            free = np.maximum(avail - busy, 0)
            qtot = Q.sum(1)
            start = np.minimum(free, qtot)
            rev = Q[:, ::-1]
            cum = np.cumsum(rev, 1)
            take = np.clip(start[:, None] - (cum - rev), 0, rev)
            Q -= take[:, ::-1]
            wsum += (take[:, ::-1] * waits).sum(1)
            busy += start
            ans += start
            # ageing
            Q[:, K - 1] += Q[:, K - 2]
            Q[:, 1:K - 1] = Q[:, 0:K - 2]
            Q[:, 0] = 0
            # arrivals
            n = rng.poisson(lam_tot)
            Q[:, 0] += n
            off += n
        # schedule retrials and repeat calls (as future extra intensity)
        for j, w in enumerate(rk):
            fut[:, hi + 1 + j] += ab_h * p["p_retry"] * w
        fut[:, hi + 12:hi + 37] += (rep_acc * p["p_repeat"])[:, None] * rep_kernel[None, :]
        if H >= 0:
            obs["offered"][:, H] = off
            obs["answered"][:, H] = ans
            obs["abandoned"][:, H] = ab_h
            obs["queue_end"][:, H] = Q.sum(1)
            obs["avg_wait_min"][:, H] = np.where(ans > 0, wsum / np.maximum(ans, 1), 0.0)
            obs["scheduled_agents"][:, H] = sched
    return obs
