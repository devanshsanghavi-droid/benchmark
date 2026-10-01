"""Brackwater bot (solver: opus).

Strategy: greedy value-per-turn task assignment (land first, fens timed to a learned tide
model), conservative flood-safety via a viability DP, local combat rules, value-based recruiting.
"""

# Tide profiles (zero-run, level-1 run, level-2 run, level-3 run) by period, as observed.
PROFILES = {20: (11, 2, 1, 3), 21: (11, 2, 2, 2), 22: (13, 1, 2, 3), 23: (13, 2, 2, 2),
            24: (13, 2, 2, 3), 25: (13, 3, 2, 2), 26: (15, 2, 2, 3), 27: (15, 2, 2, 4),
            28: (15, 3, 2, 3), 29: (15, 3, 2, 4), 30: (17, 2, 3, 3), 31: (17, 3, 2, 4),
            32: (17, 3, 3, 3), 33: (19, 2, 3, 4), 34: (19, 3, 2, 5), 35: (19, 3, 3, 4),
            36: (19, 3, 3, 5), 37: (21, 3, 3, 4), 38: (21, 3, 3, 5), 39: (21, 4, 3, 4),
            40: (23, 3, 3, 5)}

PARAMS = dict(hold_enemy=40, enemy_mult=2.0, time_c=1.0, threat_mult=0.6, occupied_mult=0.0,
              fen_mult=1.0, frontier=0.0, rec_rate=1.5, rec_off=10, soft_pen=2.0)

DIRS = (("N", 0, -1), ("E", 1, 0), ("S", 0, 1), ("W", -1, 0))


def _cyc(z, a, b, c):
    return [0] * z + [1] * a + [2] * b + [3] * c + [2] * b + [1] * a


class Tide:
    """Set of (cycle, shift) hypotheses: level(T) = cyc[(T + shift) % len(cyc)]."""

    def __init__(self):
        self.obs = {}
        self.mode = 0  # 0 primary, 1 generic, 2 unknown
        self.hyps = []
        for P, pr in PROFILES.items():
            cy = _cyc(*pr)
            for s in range(P):
                self.hyps.append((cy, s, P))
        self.version = 0

    def observe(self, T, lo, hi):
        if lo > hi:
            return
        o = self.obs.get(T)
        if o is not None:
            lo, hi = max(lo, o[0]), min(hi, o[1])
            if lo > hi:
                return
            if (lo, hi) == o:
                return
        if lo <= 0 and hi >= 3:
            return
        self.obs[T] = (lo, hi)
        if self.mode == 2:
            return
        nh = [h for h in self.hyps if lo <= h[0][(T + h[1]) % h[2]] <= hi]
        if len(nh) != len(self.hyps):
            self.version += 1
        if nh:
            self.hyps = nh
            return
        self._fallback()

    def _fallback(self):
        self.version += 1
        if self.mode == 0:
            self.mode = 1
            hs = []
            obs = list(self.obs.items())
            for P in range(20, 41):
                for a in range(1, 5):
                    for b in range(1, 4):
                        for c in range(1, 7):
                            z = P - 2 * a - 2 * b - c
                            if z < 3:
                                continue
                            cy = _cyc(z, a, b, c)
                            for s in range(P):
                                ok = True
                                for T, (lo, hi) in obs:
                                    v = cy[(T + s) % P]
                                    if v < lo or v > hi:
                                        ok = False
                                        break
                                if ok:
                                    hs.append((cy, s, P))
            if hs:
                self.hyps = hs
                return
        self.mode = 2
        self.hyps = []


class Bot:
    def __init__(self, player, game_info):
        self.P = dict(PARAMS)
        self.p = player
        W = self.W = game_info["width"]
        H = self.H = game_info["height"]
        N = self.N = W * H
        terr = self.terr = game_info["terrain"]
        self.turns = game_info.get("turns", 200)
        hubs = game_info["hubs"]
        self.hub = hubs[player]
        self.ehub = hubs[1 - player]
        self.cap = game_info.get("crew_cap", 24)
        yl = game_info.get("yields", {".": 1, "2": 2, "1": 3, "0": 5})
        elev = []
        yld = []
        for ch in terr:
            if ch == "#":
                elev.append(-1)
            elif ch in "012":
                elev.append(int(ch))
            else:
                elev.append(3)
            yld.append(yl.get(ch, 0) if ch in yl else 0)
        self.elev = elev
        self.yld = yld
        self.stakeable = [terr[c] != "#" and c not in hubs for c in range(N)]
        # legal moves for me
        mv = []
        nb = []
        for c in range(N):
            x, y = c % W, c // W
            lst = []
            if terr[c] != "#":
                for o, dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        n = ny * W + nx
                        if terr[n] != "#" and n != self.ehub:
                            lst.append((o, n))
            mv.append(lst)
            nb.append([n for _, n in lst])
        self.mv = mv
        self.nb = nb
        # all-pairs distances (my movement rules)
        D = [None] * N
        for s in range(N):
            if terr[s] == "#":
                continue
            d = [99] * N
            d[s] = 0
            q = [s]
            for c in q:
                dc = d[c] + 1
                for n in nb[c]:
                    if d[n] > dc:
                        d[n] = dc
                        q.append(n)
            D[s] = d
        self.D = D
        self.dhub = D[self.hub]
        self.dehub = D[self.ehub] if D[self.ehub] is not None else [99] * N
        self.cells = [c for c in range(N) if self.stakeable[c]]
        self.fens = [c for c in range(N) if 0 <= elev[c] <= 2]
        self.chev = {}
        self.tide = Tide()
        self.estakes = {}  # cell -> turn last seen
        self.last_orders = {}
        self.last_pos = {}
        self._pred_ver = -1
        self.Lmax = {}
        self.Ev = None

    # ------------------------------------------------------------------ tide
    def _observe_tide(self, obs):
        t = obs["turn"]
        elev = self.elev
        lo, hi = 0, 3
        fl = obs["flooded"]
        for c in fl:
            e = elev[c]
            if 0 <= e <= 2 and e + 1 > lo:
                lo = e + 1
        fls = set(fl)
        for c in obs["visible"]:
            e = elev[c]
            if 0 <= e < hi and c not in fls:
                hi = e
        # drowned crews: level now > elevation of where they moved
        for cid, why in obs.get("lost_crews", {}).items():
            if why == "drowned":
                c = self.last_pos.get(cid)
                o = self.last_orders.get(cid)
                if c is None:
                    continue
                n = c
                if o in ("N", "E", "S", "W"):
                    for oo, nn in self.mv[c]:
                        if oo == o:
                            n = nn
                if 0 <= elev[n] <= 2 and elev[n] + 1 > lo:
                    lo = elev[n] + 1
        if lo <= hi:
            self.tide.observe(t, lo, hi)

    def _predict(self, t):
        """Lmax[T] (conservative) and expected fen values Ev[e][k] for arrival at t+k."""
        tide = self.tide
        HZ = 48
        hyps = tide.hyps
        if tide.mode == 2 or not hyps:
            self.Lmax = {T: 3 for T in range(t, t + HZ + 2)}
            self.Lmin = {T: 0 for T in range(t, t + HZ + 2)}
            self.Ev = [[0.0] * HZ for _ in range(3)]
            self.Ed = [[0.0] * HZ for _ in range(3)]
            self.known = False
            return
        Lmax = {}
        Lmin = {}
        for T in range(t, t + HZ + 2):
            mx, mn = 0, 3
            for cy, s, P in hyps:
                v = cy[(T + s) % P]
                if v > mx:
                    mx = v
                if v < mn:
                    mn = v
                if mx == 3 and mn == 0:
                    break
            Lmax[T] = mx
            Lmin[T] = mn
        self.Lmax = Lmax
        self.Lmin = Lmin
        self.known = len(hyps) <= 2
        # expected values with subsample
        n = len(hyps)
        if n > 40:
            step = n / 40.0
            sub = [hyps[int(i * step)] for i in range(40)]
        else:
            sub = hyps
        ns = len(sub)
        END = self.turns
        Ev = [[0.0] * HZ for _ in range(3)]
        Ed = [[0.0] * HZ for _ in range(3)]
        span = HZ + 45
        for cy, s, P in sub:
            lev = [cy[(T + s) % P] for T in range(t, t + span)]
            for e in range(3):
                # run[i]: consecutive dry starting at index i
                run = [0] * (span + 1)
                for i in range(span - 1, -1, -1):
                    run[i] = run[i + 1] + 1 if lev[i] <= e else 0
                nxt = span
                nd = [span] * (span + 1)
                for i in range(span - 1, -1, -1):
                    if lev[i] <= e:
                        nxt = i
                    nd[i] = nxt
                Eve = Ev[e]
                Ede = Ed[e]
                for k in range(HZ):
                    ta = nd[k]
                    if ta >= span - 1:
                        continue
                    r = run[ta + 1]
                    cap = END - (t + ta)
                    if r > cap:
                        r = cap
                    if r > 0:
                        Eve[k] += r
                    Ede[k] += ta - k
        for e in range(3):
            for k in range(HZ):
                Ev[e][k] /= ns
                Ed[e][k] /= ns
        self.Ev = Ev
        self.Ed = Ed

    def _viability(self, t):
        """viable[c] for end of this turn (time t+1), under conservative Lmax."""
        HV = 16
        elev = self.elev
        Lmax = self.Lmax
        fens = self.fens
        nb = self.nb
        nxt = None
        for T in range(t + HV, t, -1):
            L = Lmax.get(T, 3)
            cur = {}
            for c in fens:
                if elev[c] < L:
                    cur[c] = False
                elif nxt is None:
                    cur[c] = False
                else:
                    ok = nxt[c]
                    if not ok:
                        for n in nb[c]:
                            if elev[n] >= 3 or nxt.get(n, False):
                                ok = True
                                break
                    cur[c] = ok
            nxt = cur
        return nxt

    # ------------------------------------------------------------------ main
    def act(self, obs):
        try:
            return self._act(obs)
        except Exception:
            return {"orders": {}, "recruit": False}

    def _act(self, obs):
        P = self.P
        t = obs["turn"]
        crews = obs["crews"]
        elev = self.elev
        yld = self.yld
        D = self.D
        END = self.turns
        self._observe_tide(obs)
        self._predict(t)
        viable = self._viability(t)

        def safe(c):
            if elev[c] >= 3:
                return True
            return viable.get(c, False)

        mine = set(obs["stakes"])
        vis = obs["visible"]
        es_now = set(obs["enemy_stakes"])
        for c in vis:
            if c in es_now:
                self.estakes[c] = t
            elif c in self.estakes:
                del self.estakes[c]
        for c in obs.get("lost_stakes", []):
            if elev[c] >= 3 and c not in vis:
                self.estakes[c] = t
        Lmin = self.Lmin
        lm = Lmin.get(t, 0)
        for c in list(self.estakes):
            if elev[c] <= 2 and lm > elev[c]:
                del self.estakes[c]
        estakes = self.estakes
        ecrew = obs["enemy_crews"]
        threat = {}
        for ec, k in ecrew.items():
            threat[ec] = threat.get(ec, 0) + k
            for n in self._enb(ec):
                threat[n] = threat.get(n, 0) + k

        Ev, Ed = self.Ev, self.Ed
        HZ = len(Ev[0])
        hold_e = P["hold_enemy"]
        emult = P["enemy_mult"]
        tc = P["time_c"]
        thr_m = P["threat_mult"]
        occ_m = P["occupied_mult"]
        fen_m = P["fen_mult"]
        front = P["frontier"]
        dhub, dehub = self.dhub, self.dehub
        tg = []
        for c in self.cells:
            if c in mine:
                continue
            e = elev[c]
            en = c in estakes
            m = 1.0
            k = ecrew.get(c, 0)
            if k:
                m = occ_m
            elif threat.get(c, 0):
                m = 0.0 if en else thr_m
            if front and e >= 3 and not en:
                # frontier land: bonus when contested (closer to enemy than to us)
                if dehub[c] <= dhub[c] + 2:
                    m *= front
            tg.append((c, e, en, m, yld[c] * fen_m))
        assigned = {}
        taken = set()
        intr = [(c, k) for c, k in ecrew.items() if c in mine]
        cand = []
        crew_list = sorted(crews.items())
        rem0 = END - t
        for cid, cc in crew_list:
            Dc = D[cc]
            best = []
            for (g, e, en, m, y) in tg:
                d = Dc[g]
                if d >= 99:
                    continue
                if e >= 3:
                    r = rem0 - d
                    if r <= 0:
                        continue
                    if en:
                        v = r + min(r, hold_e) * (emult - 1.0)
                    else:
                        v = r
                    tt = d + 1
                else:
                    if d >= HZ:
                        continue
                    v = Ev[e][d] * y
                    if en:
                        v *= emult
                    tt = d + 1 + Ed[e][d]
                    if v <= 0:
                        continue
                best.append((v * m / (tt + tc), g))
            for g, k in intr:
                d = Dc[g]
                if d <= 1 and k == 1:
                    best.append((1000.0, g))
            best.sort(reverse=True)
            for sc, g in best[:6]:
                cand.append((sc, cid, g))
        cand.sort(reverse=True)
        for sc, cid, g in cand:
            if cid in assigned or g in taken:
                continue
            assigned[cid] = g
            taken.add(g)
        # unassigned crews: recompute against remaining targets
        for cid, cc in crew_list:
            if cid in assigned:
                continue
            Dc = D[cc]
            bs, bg = 0.0, None
            for (g, e, en, m, y) in tg:
                if g in taken:
                    continue
                d = Dc[g]
                if d >= 99:
                    continue
                if e >= 3:
                    r = rem0 - d
                    if r <= 0:
                        continue
                    v = r + (min(r, hold_e) * (emult - 1.0) if en else 0.0)
                    tt = d + 1
                else:
                    if d >= HZ:
                        continue
                    v = Ev[e][d] * y * (emult if en else 1.0)
                    tt = d + 1 + Ed[e][d]
                sc = v * m / (tt + tc)
                if sc > bs:
                    bs, bg = sc, g
            if bg is not None:
                assigned[cid] = bg
                taken.add(bg)

        orders = {}
        soft = P["soft_pen"]
        for cid, cc in crew_list:
            g = assigned.get(cid, cc)
            Dg = D[g]
            dc = Dg[cc]
            best_o, best_k = None, None
            stay_o = "K" if (cc == g and g not in mine and self.stakeable[g]) else "H"
            for oo, n in [(stay_o, cc)] + self.mv[cc]:
                if not safe(n):
                    continue
                k = ecrew.get(n, 0)
                th = threat.get(n, 0)
                hard = 0
                pen = 0.0
                if k:
                    if not (n in mine and k == 1 and n == g):
                        hard = 1
                elif th:
                    if n in mine:
                        if th >= 2:
                            pen = soft
                    elif n in estakes:
                        hard = 1
                    else:
                        pen = soft
                key = (hard, Dg[n] - dc + pen, -elev[n] if elev[n] < 3 else -3)
                if best_k is None or key < best_k:
                    best_k, best_o = key, oo
            if best_o is None:
                # no tide-safe option: climb
                be, best_o = elev[cc], "H"
                for oo, n in self.mv[cc]:
                    if elev[n] > be:
                        be, best_o = elev[n], oo
            if best_o == "K" and ecrew.get(cc, 0):
                best_o = "H"
            orders[cid] = best_o
        self.last_orders = orders
        self.last_pos = dict(crews)

        n = len(crews)
        cost = obs["recruit_cost"]
        rec = False
        if n < self.cap and obs["grain"] >= cost:
            if cost <= P["rec_rate"] * (END - t - P["rec_off"]):
                rec = True
        return {"orders": orders, "recruit": rec}

    def _enb(self, c):
        r = self.chev.get(c)
        if r is None:
            W = self.W
            x, y = c % W, c // W
            r = []
            for o, dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < self.H:
                    n = ny * W + nx
                    if self.terr[n] != "#" and n != self.hub:
                        r.append(n)
            self.chev[c] = r
        return r
