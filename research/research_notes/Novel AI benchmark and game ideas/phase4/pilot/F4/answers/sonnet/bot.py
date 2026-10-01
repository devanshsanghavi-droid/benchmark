"""Brackwater bot (solver label: sonnet).

Strategy: tide-aware stake expansion.  The tide is a deterministic function of its period, so the
bot keeps the set of (period, phase) candidates consistent with everything it has seen and
forecasts the water level from it.  Crews are assigned greedily to the stake targets with the best
(yield x dry-lifetime) / time-to-complete ratio, never entering a cell they cannot escape from
before it floods.  Enemy stakes are valued double (we gain, they lose).
"""
import time

from bot_api import Grid

PROFILES = {
    20: '11233321100000000000',
    21: '112233221100000000000',
    22: '1223332210000000000000',
    23: '11223322110000000000000',
    24: '112233322110000000000000',
    25: '1112233221110000000000000',
    26: '11223332211000000000000000',
    27: '112233332211000000000000000',
    28: '1112233322111000000000000000',
    29: '11122333322111000000000000000',
    30: '112223332221100000000000000000',
    31: '1112233332211100000000000000000',
    32: '11122233322211100000000000000000',
    33: '112223333222110000000000000000000',
    34: '1112233333221110000000000000000000',
    35: '11122233332221110000000000000000000',
    36: '111222333332221110000000000000000000',
    37: '1112223333222111000000000000000000000',
    38: '11122233333222111000000000000000000000',
    39: '111122233332221111000000000000000000000',
    40: '1112223333322211100000000000000000000000',
}

# ---------------------------------------------------------------- tunables
RISK_CREW = 0.03       # tolerated probability mass of tide candidates when judging crew safety
CAP = 30               # cap on stake lifetime used in valuation
HV = 44                # forecast horizon (turns)
HS_UNCERTAIN = 22      # survival-DP horizon when the tide is not identified
NMAX = 11              # target crew count
RECRUIT_UNTIL = 150
MAXD = 16


class Tide:
    def __init__(self, nturns):
        self.L = nturns + 130
        self.lv = []
        self.Pof = []
        self.w = []
        for P in range(20, 41):
            prof = bytes(int(ch) for ch in PROFILES[P])
            rep = prof * ((self.L + P) // P + 3)
            for ph in range(P):
                self.lv.append(rep[ph:ph + self.L])
                self.Pof.append(P)
                self.w.append(1.0 / P)
        self.alive = list(range(len(self.lv)))
        self.ver = 0
        self.broken = False
        self._cache = {}
        self._cache_ver = 0

    def update(self, t, lo, hi):
        if self.broken or (lo <= 0 and hi >= 3):
            return
        lv = self.lv
        new = [i for i in self.alive if lo <= lv[i][t] <= hi]
        if not new:
            self.broken = True
            return
        if len(new) != len(self.alive):
            self.alive = new
            self.ver += 1

    def known(self):
        return (not self.broken) and len(self.alive) == 1

    def dist(self, s):
        """(safe_level, mid_level) forecast for the level at the start of turn s."""
        if self.broken:
            return (3, 3)
        if s >= self.L:
            s = self.L - 1
        if self._cache_ver != self.ver:
            self._cache = {}
            self._cache_ver = self.ver
        r = self._cache.get(s)
        if r is None:
            alive = self.alive
            lv = self.lv
            if len(alive) == 1:
                x = lv[alive[0]][s]
                r = (x, x)
            else:
                cnt = [0.0, 0.0, 0.0, 0.0]
                w = self.w
                for i in alive:
                    cnt[lv[i][s]] += w[i]
                tot = cnt[0] + cnt[1] + cnt[2] + cnt[3]
                acc = 0.0
                safe = 3
                mid = 3
                gotmid = False
                for l in range(4):
                    acc += cnt[l]
                    if not gotmid and acc >= 0.5 * tot:
                        mid = l
                        gotmid = True
                    if acc >= (1.0 - RISK_CREW) * tot - 1e-12:
                        safe = l
                        break
                r = (safe, mid)
            self._cache[s] = r
        return r


class Bot:
    def __init__(self, player, game_info):
        self.cpu0 = time.process_time()
        self.g = g = Grid(game_info)
        self.me = player
        self.N = N = g.N
        self.elev = g.elev
        self.yld = g.yld
        self.turns = game_info["turns"]
        self.crew_cap = game_info["crew_cap"]
        self.nbr = [[n for _, n in g.moves[c]] for c in range(N)]
        self.order_to = [dict((n, o) for o, n in g.moves[c]) for c in range(N)]
        self.fens = [c for c in range(N) if 0 <= g.elev[c] <= 2]
        self.landmask = bytearray(1 if g.elev[c] == 3 else 0 for c in range(N))
        self.D = [g.bfs(c) if g.passable(c) else None for c in range(N)]
        self.targets = [c for c in range(N)
                        if g.passable(c) and g.yld[c] > 0 and c != g.my_hub]
        self.tide = Tide(self.turns)
        self.enemy_mem = {}          # cell -> turn last seen holding an enemy stake
        self.last_wash = [-1, -1, -1]  # latest turn the level surely exceeded elev e
        self.prev_target = {}
        self.vcyc_key = None
        self.vcyc = None
        self.dbg = False

    # ------------------------------------------------------------ survival DP
    def _build_V(self, levels, H):
        """levels[k] for k in 0..H = level at start of turn base+k.  Returns list of bytearrays."""
        elev = self.elev
        N = self.N
        nbr = self.nbr
        fens = self.fens
        V = [None] * (H + 1)
        last = bytearray(N)
        Lh = levels[H]
        for x in range(N):
            last[x] = 1 if elev[x] >= Lh else 0
        V[H] = last
        landmask = self.landmask
        for k in range(H - 1, -1, -1):
            nxt = V[k + 1]
            cur = bytearray(landmask)
            L = levels[k]
            for x in fens:
                if elev[x] >= L:
                    if nxt[x]:
                        cur[x] = 1
                    else:
                        for y in nbr[x]:
                            if nxt[y]:
                                cur[x] = 1
                                break
            V[k] = cur
        return V

    # ------------------------------------------------------------ main
    def act(self, obs):
        try:
            return self._act(obs)
        except Exception:
            import traceback
            traceback.print_exc()
            return self._fallback(obs)

    def _fallback(self, obs):
        orders = {}
        for cid in obs["crews"]:
            orders[int(cid)] = "H"
        return {"orders": orders, "recruit": False}

    def _act(self, obs):
        g = self.g
        t = obs["turn"]
        elev = self.elev
        N = self.N
        crews = {int(k): v for k, v in obs["crews"].items()}
        my_stakes = set(obs["stakes"])
        enemy_crews = {int(k): v for k, v in obs["enemy_crews"].items()}
        flooded = set(obs["flooded"])
        visible = obs["visible"]

        # ---- tide observation
        lo, hi = 0, 3
        for c in visible:
            e = elev[c]
            if 0 <= e <= 2:
                if c in flooded:
                    if e + 1 > lo:
                        lo = e + 1
                elif e < hi:
                    hi = e
        self.tide.update(t, lo, hi)
        tide = self.tide
        # inferred lower bound of level this turn (for stake memory)
        if tide.broken:
            lo_now = lo
        else:
            lv = tide.lv
            lo_now = min(lv[i][t] for i in tide.alive) if len(tide.alive) < 50 else lo
            lo_now = max(lo_now, lo)
        for e in range(3):
            if lo_now > e:
                self.last_wash[e] = t

        # ---- enemy stake memory
        vis_set = set(visible)
        enemy_stakes_now = set(obs["enemy_stakes"])
        mem = self.enemy_mem
        for c in list(mem.keys()):
            e = elev[c]
            if c in vis_set:
                if c not in enemy_stakes_now:
                    del mem[c]
            elif 0 <= e <= 2 and self.last_wash[e] > mem[c]:
                del mem[c]
        for c in enemy_stakes_now:
            mem[c] = t
        for c in my_stakes:
            if c in mem:
                del mem[c]

        # ---- forecasts
        Ls = []
        Lm = []
        for k in range(HV + 2):
            a, b = tide.dist(t + k)
            Ls.append(a)
            Lm.append(b)
        if tide.known():
            i0 = tide.alive[0]
            P = tide.Pof[i0]
            if self.vcyc_key != i0:
                lvl = tide.lv[i0]
                levels = [lvl[s] for s in range(3 * P + 1)]
                Vfull = self._build_V(levels, 3 * P)
                self.vcyc = [Vfull[P + j] for j in range(P)]
                self.vcyc_key = i0
            vcyc = self.vcyc

            def Vat(k, x, t=t, P=P, vcyc=vcyc):
                return vcyc[(t + k) % P][x]
        else:
            Hs = HS_UNCERTAIN
            Vl = self._build_V(Ls[:Hs + 1], Hs)

            def Vat(k, x, Vl=Vl, Hs=Hs):
                if k > Hs:
                    return 1
                return Vl[k][x]

        # ---- precompute per-elevation arrays
        okarr = {}
        lifearr = {}
        nxtok = {}
        T_left = self.turns - t
        for e in (0, 1, 2):
            ok = [1 if (Ls[k] <= e and Ls[k + 1] <= e) else 0 for k in range(HV + 1)]
            okarr[e] = ok
            # next ok index
            nx = [-1] * (HV + 2)
            nxt = -1
            for k in range(HV, -1, -1):
                if ok[k]:
                    nxt = k
                nx[k] = nxt
            nxtok[e] = nx
            # life: stake planted during turn t+k survives until first j>=k with Lm[j+1] > e
            life = [0] * (HV + 1)
            nb = HV + 5  # beyond horizon: no wash known
            for k in range(HV, -1, -1):
                if Lm[k + 1] > e:
                    nb = k
                life[k] = nb - k
            lifearr[e] = life

        # ---- threats
        reach = {}
        for q, n in enemy_crews.items():
            reach[q] = reach.get(q, 0) + n
            for y in self.nbr[q]:
                reach[y] = reach.get(y, 0) + n

        # ---- candidate scoring
        D = self.D
        yld = self.yld
        pairs = []
        for cid, p in crews.items():
            Dp = D[p]
            prev = self.prev_target.get(cid)
            for c in self.targets:
                if c in my_stakes:
                    continue
                d = Dp[c]
                if d < 0 or d > MAXD:
                    continue
                e = elev[c]
                if e == 3:
                    k = d
                    life = T_left - k
                else:
                    if d > HV:
                        continue
                    k = nxtok[e][d]
                    if k < 0 or k > HV - 1:
                        continue
                    if not Vat(k + 1, c):
                        continue
                    life = lifearr[e][k]
                    if life > T_left - k:
                        life = T_left - k
                if life <= 0:
                    continue
                if life > CAP:
                    life = CAP
                val = yld[c] * life
                if c in mem:
                    val *= 2.0
                if c in reach and c not in my_stakes:
                    val *= 0.4
                sc = val / (k + 1.0)
                if prev == c:
                    sc *= 1.25
                pairs.append((sc, cid, c, k))
        pairs.sort(reverse=True)
        assigned = {}
        used_cells = set()
        for sc, cid, c, k in pairs:
            if cid in assigned or c in used_cells:
                continue
            assigned[cid] = (c, k)
            used_cells.add(c)
            if len(assigned) == len(crews):
                break
        self.prev_target = dict((cid, v[0]) for cid, v in assigned.items())

        # ---- orders
        orders = {}
        Ls1 = Ls[1]
        for cid, p in crews.items():
            tk = assigned.get(cid)
            opts = [(p, "H")]
            for o, n in g.moves[p]:
                opts.append((n, o))
            good = []
            for n, o in opts:
                if elev[n] >= Ls1 and Vat(1, n):
                    good.append((n, o))
            if not good:
                # no survivable option by forecast: run to the best land/high cell
                best = None
                for n, o in opts:
                    s = (elev[n], -D[n][p] if D[n] else 0)
                    if best is None or s > best[0]:
                        best = (s, o)
                orders[cid] = best[1]
                continue
            if tk is None:
                # idle: hold if safe
                dec = "H"
                for n, o in good:
                    if n == p:
                        dec = "H"
                        break
                else:
                    dec = good[0][1]
                orders[cid] = dec
                continue
            c, k = tk
            if p == c and k == 0:
                if any(n == p for n, o in good):
                    orders[cid] = "K"
                else:
                    orders[cid] = good[0][1]
                continue
            Dc = D[c]
            bestv = None
            bo = "H"
            for n, o in good:
                dn = Dc[n]
                if dn < 0:
                    continue
                pen = 0.0
                if n in reach and n not in my_stakes:
                    pen += 0.9
                s = dn + pen
                if n == p:
                    s += 0.05
                if bestv is None or s < bestv:
                    bestv = s
                    bo = o
            orders[cid] = bo

        # ---- recruit
        n_crews = len(crews)
        cost = obs["recruit_cost"]
        recruit = False
        if (obs["grain"] >= cost and n_crews < self.crew_cap and n_crews < NMAX
                and t <= RECRUIT_UNTIL):
            recruit = True
        return {"orders": orders, "recruit": recruit}
