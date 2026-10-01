"""Shared planner for the sealed Brackwater reference bots (rungs L1-L3).

Every rung is the same crew->target planner with different feature switches:
  tide      : "crude"  - only "water is up" caution from currently visible flooding
              "approx" - level bounds + trend + period from observed flood onsets (no waveform)
              "exact"  - operator knowledge of the waveform family; filters (period, phase)
  threat    : avoid ending turns where visible enemy crews could win a fight
  defend    : intercept enemy crews standing on own stakes
  enemy_tg  : treat enemy stakes as (double-value) targets
  memory    : remember enemy stakes after they leave vision
  recruit   : "always" | "payback" | "value"
"""
from bot_api import Grid, recruit_cost  # noqa: F401

_APSP_CACHE = {}


def apsp(g):
    key = (g.terrain, g.player)
    d = _APSP_CACHE.get(key)
    if d is None:
        d = [g.bfs(c) if g.passable(c) else [-1] * g.N for c in range(g.N)]
        if len(_APSP_CACHE) > 64:
            _APSP_CACHE.clear()
        _APSP_CACHE[key] = d
    return d


def level_bounds(g, obs):
    lo, hi = 0, 3
    fl = set(obs["flooded"])
    elev = g.elev
    for c in obs["visible"]:
        e = elev[c]
        if 0 <= e <= 2:
            if c in fl:
                if e + 1 > lo:
                    lo = e + 1
            elif e < hi:
                hi = e
    return lo, hi


# ------------------------------------------------------------------ tide models
_TH = (0.55, 0.72, 0.88)
_HYP = None
_HORIZON = 260


def _hypotheses():
    global _HYP
    if _HYP is None:
        hyps = []
        for P in range(20, 41):
            for ph in range(P):
                lv = bytearray(_HORIZON)
                for t in range(_HORIZON):
                    f = ((t + ph) % P) / P
                    h = 1.0 - abs(2.0 * f - 1.0)
                    lv[t] = (h > _TH[0]) + (h > _TH[1]) + (h > _TH[2])
                hyps.append(bytes(lv))
        _HYP = hyps
    return _HYP


class CrudeTide:
    """Knows only what is flooded right now."""

    def update(self, t, lo, hi):
        self.lo = lo

    def unsafe_next(self, t):
        d = self.lo
        return [e <= d - 0 and d > 0 for e in range(3)]

    def window(self, e, ts, T):
        return T - ts if e >= 3 else min(8, T - ts)


class ApproxTide:
    def __init__(self):
        self.last_level = None
        self.last_t = None
        self.trend = 0
        self.onsets = []
        self.recessions = []
        self.period = None
        self.lo, self.hi = 0, 3

    def update(self, t, lo, hi):
        self.lo, self.hi = lo, hi
        if lo != hi:
            return
        L = lo
        if self.last_level is not None and self.last_t == t - 1:
            if L > self.last_level:
                self.trend = 1
                if L == 1 and self.last_level == 0:
                    self.onsets.append(t)
            elif L < self.last_level:
                self.trend = -1
                if L == 0 and self.last_level == 1:
                    self.recessions.append(t)
        if L == 3:
            self.trend = -1
        self.last_level, self.last_t = L, t
        for seq in (self.onsets, self.recessions):
            if len(seq) >= 2 and seq[-1] - seq[-2] >= 15:
                self.period = seq[-1] - seq[-2]

    def next_onset(self, t):
        if self.period and self.onsets:
            n = self.onsets[-1]
            while n <= t:
                n += self.period
            return n
        return None

    def unsafe_next(self, t):
        uns = [False, False, False]
        lo, hi = self.lo, self.hi
        rising = self.trend >= 0
        for e in (1, 2):
            if hi <= e - 1:
                continue
            if lo >= e:
                uns[e] = rising
            elif self.last_level is not None and t - self.last_t <= 3:
                uns[e] = self.last_level >= e - 1 and rising
            else:
                uns[e] = True
        if lo >= 1:
            uns[0] = True
        else:
            no = self.next_onset(t)
            if no is not None:
                uns[0] = no - t <= 2
            elif self.recessions and self.last_level == 0:
                uns[0] = t - self.recessions[-1] >= 9
            else:
                uns[0] = True
        return uns

    def window(self, e, ts, T):
        if e >= 3:
            return T - ts
        no = self.next_onset(ts)
        if no is None:
            return min(6, T - ts)
        return max(0, min(T - ts, no - ts + e * (self.period // 12)))


class ExactTide:
    """Operator knowledge of the waveform family; filters (period, phase) hypotheses."""

    def __init__(self):
        self.alive = list(range(len(_hypotheses())))
        self._cache = {}

    def update(self, t, lo, hi):
        self.t = t
        H = _HYP
        keep = [i for i in self.alive if lo <= H[i][t] <= hi]
        if keep and len(keep) != len(self.alive):
            self.alive = keep
            self._cache = {}
        # unsafe for end of this turn: level at t+1 may exceed e
        self._uns = [self._may_exceed(t + 1, e) for e in range(3)]

    def _may_exceed(self, tt, e):
        H = _HYP
        for i in self.alive:
            if H[i][tt] > e:
                return True
        return False

    def unsafe_next(self, t):
        return self._uns

    def first_flood(self, e, tt):
        """Earliest time index >= tt at which elevation e may be flooded."""
        key = (e, tt)
        r = self._cache.get(key)
        if r is None:
            H = _HYP
            alive = self.alive
            r = tt + 60
            for x in range(tt, min(tt + 60, _HORIZON)):
                hit = False
                for i in alive:
                    if H[i][x] > e:
                        hit = True
                        break
                if hit:
                    r = x
                    break
            self._cache[key] = r
        return r

    def surely_dry_from(self, e, tt):
        """Earliest time index >= tt at which elevation e is dry under every live hypothesis."""
        key = (e, tt, 1)
        r = self._cache.get(key)
        if r is None:
            H = _HYP
            alive = self.alive
            r = tt + 60
            for x in range(tt, min(tt + 60, _HORIZON)):
                ok = True
                for i in alive:
                    if H[i][x] > e:
                        ok = False
                        break
                if ok:
                    r = x
                    break
            self._cache[key] = r
        return r

    def window(self, e, ts, T):
        """Turns of income from a stake placed during turn ts on elevation e."""
        if e >= 3:
            return T - ts
        ff = self.first_flood(e, ts + 1)
        return max(0, min(T - ts, ff - 1 - ts))


# ------------------------------------------------------------------ planner
class Planner:
    OPTS = {}
    DEFAULTS = dict(tide="approx", threat=True, defend=True, enemy_tg=True, memory=False,
                    recruit="payback", wait_drain=False, fen_bias=1.0, chase=0, enemy_mult=2.0, dexp=1.0)

    def __init__(self, player, game_info):
        self.o = dict(self.DEFAULTS, **self.OPTS)
        self.g = g = Grid(game_info)
        self.D = apsp(g)
        self.cands = [c for c in range(g.N) if g.passable(c) and c != g.my_hub]
        self.adj1 = [tuple([c] + g.neighbors(c)) for c in range(g.N)]
        self.tide = {"crude": CrudeTide, "approx": ApproxTide, "exact": ExactTide}[self.o["tide"]]()
        self.fens = [c for c in range(g.N) if 0 <= g.elev[c] <= 2]
        self.fen_nb = {c: tuple(g.neighbors(c)) for c in self.fens}
        self.mem_es = set()
        self.T = g.turns

    # --------------------------------------------------------------
    def act(self, obs):
        g = self.g
        D = self.D
        o = self.o
        t = obs["turn"]
        T = self.T
        left = T - t
        lo, hi = level_bounds(g, obs)
        tide = self.tide
        tide.update(t, lo, hi)
        uns = tide.unsafe_next(t)
        mine = set(obs["stakes"])
        fl = set(obs["flooded"])
        es_vis = set(obs["enemy_stakes"])
        if o["memory"]:
            vis = obs["visible"]
            for c in vis:
                if c in es_vis:
                    self.mem_es.add(c)
                else:
                    self.mem_es.discard(c)
            self.mem_es -= mine
            if lo > 0:
                self.mem_es = {c for c in self.mem_es if not (0 <= g.elev[c] < lo)}
            es = set(self.mem_es)
        else:
            es = es_vis
        ec = obs["enemy_crews"]
        threat = {}
        if o["threat"] or o["defend"]:
            for c, k in ec.items():
                for n in self.adj1[c]:
                    threat[n] = threat.get(n, 0) + k
        elev = g.elev
        yld = g.yld

        if o["tide"] == "exact":
            okset = self._escape_set(t)

            def unsafe(c):
                return c in fl or (0 <= elev[c] <= 2 and c not in okset)
        else:
            def unsafe(c):
                e = elev[c]
                return c in fl or (0 <= e <= 2 and uns[e])

        crews = obs["crews"]
        orders = {}
        planned = {}
        busy = set()
        # ---- defense
        if o["defend"]:
            for c, k in sorted(ec.items()):
                if c in mine and threat.get(c, 0) <= 1 + (k - 1) and not unsafe(c):
                    need = k
                    got = []
                    for cid in sorted(crews):
                        if cid in busy:
                            continue
                        if D[crews[cid]][c] == 1:
                            got.append(cid)
                            if len(got) >= need:
                                break
                    if len(got) >= need:
                        for cid in got:
                            cc = crews[cid]
                            for oo, n in g.moves[cc]:
                                if n == c:
                                    orders[cid] = oo
                                    break
                            busy.add(cid)
                        planned[c] = planned.get(c, 0) + len(got)
        # ---- chase raiders standing on / next to own stakes
        chase_tg = {}
        if o["chase"]:
            raiders = [c for c in ec if c in mine or any(n in mine for n in self.adj1[c])]
            for rc in sorted(raiders, key=lambda c: -ec[c]):
                best = None
                for cid in sorted(crews):
                    if cid in busy:
                        continue
                    d = D[crews[cid]][rc]
                    if 1 < d <= o["chase"] and (best is None or d < best[0]):
                        best = (d, cid)
                if best is not None:
                    chase_tg[best[1]] = rc
                    busy.add(best[1])
        # ---- target base list
        base = []
        for c in self.cands:
            if c in mine:
                continue
            if c in es:
                if not o["enemy_tg"]:
                    continue
                mult = o["enemy_mult"]
            else:
                mult = 1.0
            if o["threat"] and threat.get(c, 0) > 0:
                mult *= 0.3
            e = elev[c]
            if c in fl and not o["wait_drain"]:
                continue
            base.append((c, e, yld[c] * mult * (o["fen_bias"] if 0 <= e <= 2 else 1.0)))
        # rough prefilter by value at distance 0
        pre = []
        for c, e, m in base:
            w = tide.window(e if e <= 2 else 3, t, T)
            pre.append((m * max(w, 1), c, e, m))
        pre.sort(reverse=True)
        pre = pre[:70]
        free = [cid for cid in sorted(crews) if cid not in busy]
        for cid, rc in chase_tg.items():
            c = crews[cid]
            dt = D[rc]
            od = None
            for oo, n in sorted(g.moves[c], key=lambda on: (on[1] not in mine, on[0])):
                if 0 <= dt[n] < dt[c] and not unsafe(n) and self._ok(n, planned, threat, mine):
                    od = oo
                    break
            if od is None:
                od = "H" if not unsafe(c) else next((oo for oo, n in g.moves[c] if not unsafe(n)), "H")
            orders[cid] = od
            n = c if od == "H" else dict(g.moves[c])[od]
            planned[n] = planned.get(n, 0) + 1
        pairs = []
        exact = o["tide"] == "exact"
        dexp = o["dexp"]
        for cid in free:
            cc = crews[cid]
            dc = D[cc]
            for _, c, e, m in pre:
                d = dc[c]
                if d < 0 or d >= left:
                    continue
                ts = t + d
                if 0 <= e <= 2:
                    if exact:
                        ts = tide.surely_dry_from(e, ts)
                        if ts >= T:
                            continue
                    w = tide.window(e, ts, T)
                else:
                    w = T - ts
                if w <= 0:
                    continue
                v = m * w
                pairs.append((v / (ts - t + 1.5) ** dexp, cid, c))
        pairs.sort(reverse=True)
        assigned = {}
        used = set()
        for s, cid, c in pairs:
            if cid in assigned or c in used:
                continue
            assigned[cid] = c
            used.add(c)
        for cid in free:
            c = crews[cid]
            tgt = assigned.get(cid)
            od = None
            if tgt == c:
                if not unsafe(c) and (not o["threat"] or self._ok(c, planned, threat, mine)):
                    od = "K"
            elif tgt is not None:
                dt = D[tgt]
                for oo, n in g.moves[c]:
                    if dt[n] < 0 or dt[n] >= dt[c]:
                        continue
                    if unsafe(n):
                        continue
                    if o["threat"] and not self._ok(n, planned, threat, mine):
                        continue
                    od = oo
                    break
            if od is None:
                if not unsafe(c) and (not o["threat"] or self._ok(c, planned, threat, mine)):
                    od = "K" if (c not in mine and c != g.my_hub and c not in fl) else "H"
                else:
                    od = "H"
                    for oo, n in g.moves[c]:
                        if not unsafe(n) and (not o["threat"] or self._ok(n, planned, threat, mine)):
                            od = oo
                            break
            orders[cid] = od
            n = c if od in ("H", "K") else dict(g.moves[c])[od]
            planned[n] = planned.get(n, 0) + 1
        return {"orders": orders, "recruit": self._recruit(obs, left)}

    def _escape_set(self, t, K=8):
        """Fen cells a crew may end turn t on and still walk to safety later (exact tide only)."""
        tide = self.tide
        mx = [[tide._may_exceed(t + 1 + k, e) for e in range(3)] for k in range(K)]
        if not any(any(r) for r in mx):
            return set(self.fens)
        elev = self.g.elev
        R = {c for c in self.fens if not mx[K - 1][elev[c]]}
        for k in range(K - 2, -1, -1):
            row = mx[k]
            nr = set()
            for c in self.fens:
                if row[elev[c]]:
                    continue
                if c in R:
                    nr.add(c)
                    continue
                for n in self.fen_nb[c]:
                    if n in R or elev[n] == 3:
                        nr.add(c)
                        break
            R = nr
        return R

    def _ok(self, n, planned, threat, mine):
        k = threat.get(n, 0)
        if k == 0:
            return True
        return planned.get(n, 0) + 1 + (1 if n in mine else 0) > k

    def _recruit(self, obs, left):
        n = len(obs["crews"])
        cost = obs["recruit_cost"]
        if n >= self.g.crew_cap or obs["grain"] < cost:
            return False
        r = self.o["recruit"]
        if r == "always":
            return left > 30
        if r == "payback":
            return left > 25 and cost <= 2.0 * left
        # "value": marginal income per crew, discounted
        per = max(2.0, (obs["income"] - 2) / max(1, n))
        per = min(per, 6.0)
        return cost <= 0.5 * per * (left - 12)
