"""Brackwater bot (solver label: fable).

Strategy outline
  * Tide model: a hypothesis set over (period, hump shape, phase).  The tide is a long level-0
    stretch followed by a symmetric hump 1^a 2^b 3^c 2^b 1^a.  Each hypothesis keeps a bitmask of
    live phase offsets; observations (bounds on the water level derived from visible fens) prune
    them.  Predictions are conservative upper bounds on the level for the next H turns, from which
    a "survivable" cell set is derived (a crew must always be able to escape the rising water).
  * Economy: greedy assignment of crews to stake targets by value / time, where value is
    yield x guaranteed dry turns (land: turns remaining).  Enemy stakes are flip targets.
  * Combat: free kills of lone enemy crews standing on our stakes; avoid staking next to enemies.
  * Recruiting: while the marginal crew is expected to pay back.
"""
import sys

T_TURNS = 200
H = 26          # tide prediction horizon (turns)
EXACT_MAX = 64  # use exact per-k predictions when at most this many (P, shape) pairs are live


class Tide:
    """Hypothesis filter for the periodic tide."""

    def __init__(self):
        self.pairs = []   # [P, M, masks(0..3), (a,b,c), full]
        for P in range(20, 41):
            for a in range(1, 6):
                for b in range(1, 5):
                    for c in range(1, 7):
                        z = P - (2 * a + 2 * b + c)
                        if z < 9:
                            continue
                        pat = [0] * z + [1] * a + [2] * b + [3] * c + [2] * b + [1] * a
                        masks = [0, 0, 0, 0]
                        for p, L in enumerate(pat):
                            masks[L] |= 1 << p
                        full = (1 << P) - 1
                        self.pairs.append([P, full, masks, (a, b, c), full])
        self.live = list(self.pairs)
        self.generic = False
        self.hist = []          # (lo, hi) per turn
        self.cur = (0, 3)
        self.known = False      # single hypothesis left
        self.future = None      # exact future levels when known: list index k -> level at turn t+k

    def reset(self):
        for pr in self.pairs:
            pr[1] = pr[4]
        self.live = list(self.pairs)
        self.generic = False

    def observe(self, t, lo, hi):
        self.cur = (lo, hi)
        self.hist.append((lo, hi))
        if self.generic:
            return
        if lo == 0 and hi == 3:
            return  # no information
        nl = []
        for pr in self.live:
            P, M, masks = pr[0], pr[1], pr[2]
            allowed = 0
            for L in range(lo, hi + 1):
                allowed |= masks[L]
            r = t % P
            if r:
                allowed = ((allowed >> r) | (allowed << (P - r))) & pr[4]
            M &= allowed
            if M:
                pr[1] = M
                nl.append(pr)
        if not nl:
            # model mismatch: fall back to generic conservative predictions, then try to
            # re-learn from scratch.
            self.reset()
            self.generic = True
            self._generic_since = t
            return
        self.live = nl

    def predict(self, t):
        """Return (maxlev[0..H], minlev[0..H]); index k is the level at the start of turn t+k
        (i.e. after the tide update at the end of turn t+k-1).  Index 0 is the current bounds."""
        lo, hi = self.cur
        maxlev = [hi] + [3] * H
        minlev = [lo] + [0] * H
        self.known = False
        self.future = None
        if self.generic:
            # conservative: could rise one level per turn
            for k in range(1, H + 1):
                maxlev[k] = min(3, hi + k)
            # try re-learning after a few turns
            if t - self._generic_since > 3:
                self.generic = False
                self.reset()
            return maxlev, minlev
        live = self.live
        n = len(live)
        if n <= EXACT_MAX:
            for k in range(1, H + 1):
                mx = 0
                mn = 3
                tk = t + k
                for pr in live:
                    P, M, masks = pr[0], pr[1], pr[2]
                    r = tk % P
                    rot = ((M << r) | (M >> (P - r))) & pr[4] if r else M
                    if rot & masks[3]:
                        mx = 3
                    elif rot & masks[2]:
                        if mx < 2:
                            mx = 2
                    elif rot & masks[1]:
                        if mx < 1:
                            mx = 1
                    if rot & masks[0]:
                        mn = 0
                    elif rot & masks[1]:
                        if mn > 1:
                            mn = 1
                    elif rot & masks[2]:
                        if mn > 2:
                            mn = 2
                    if mx == 3 and mn == 0:
                        break
                maxlev[k] = mx
                minlev[k] = mn
            if n == 1 and (live[0][1] & (live[0][1] - 1)) == 0:
                # a single hypothesis: the whole future is known
                pr = live[0]
                P, M, masks = pr[0], pr[1], pr[2]
                o = M.bit_length() - 1
                pat = [0] * P
                for L in range(4):
                    mm = masks[L]
                    for p in range(P):
                        if (mm >> p) & 1:
                            pat[p] = L
                self.known = True
                self.future = [pat[(t + k + o) % P] for k in range(T_TURNS - t + 2)]
            return maxlev, minlev
        # large hypothesis set: analytic conservative bound
        if hi > 0:
            for k in range(1, H + 1):
                maxlev[k] = min(3, hi + k)
            return maxlev, minlev
        # currently at level 0: earliest possible k with level >= 1, then min a, min b
        k1 = None
        for k in range(1, H + 1):
            tk = t + k
            for pr in live:
                P, M, masks = pr[0], pr[1], pr[2]
                r = tk % P
                rot = ((M << r) | (M >> (P - r))) & pr[4] if r else M
                if rot & ~masks[0]:
                    k1 = k
                    break
            if k1 is not None:
                break
        if k1 is None:
            for k in range(1, H + 1):
                maxlev[k] = 0
            return maxlev, minlev
        amin = 9
        bmin = 9
        for pr in live:
            a, b, c = pr[3]
            if a < amin:
                amin = a
            if b < bmin:
                bmin = b
        for k in range(1, H + 1):
            if k < k1:
                maxlev[k] = 0
            elif k < k1 + amin:
                maxlev[k] = 1
            elif k < k1 + amin + bmin:
                maxlev[k] = 2
            else:
                maxlev[k] = 3
        return maxlev, minlev


class Bot:
    def __init__(self, player, game_info):
        self.player = player
        gi = game_info
        self.W = gi["width"]
        self.Hh = gi["height"]
        self.N = self.W * self.Hh
        self.terrain = gi["terrain"]
        self.hubs = list(gi["hubs"])
        self.my_hub = self.hubs[player]
        self.en_hub = self.hubs[1 - player]
        self.cap = gi["crew_cap"]
        ylds = gi["yields"]
        N = self.N
        W = self.W
        self.elev = []
        self.yld = []
        for ch in self.terrain:
            if ch == "#":
                self.elev.append(-1)
            elif ch in "012":
                self.elev.append(int(ch))
            else:
                self.elev.append(3)
            self.yld.append(ylds.get(ch, 0))
        # neighbours (legal moves for me): list of (order, cell)
        self.moves = []
        self.nb = []
        dirs = (("N", 0, -1), ("E", 1, 0), ("S", 0, 1), ("W", -1, 0))
        for c in range(N):
            x, y = c % W, c // W
            lst = []
            for o, dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < self.Hh:
                    n = ny * W + nx
                    if self.terrain[n] != "#" and n != self.en_hub:
                        lst.append((o, n))
            self.moves.append(lst)
            self.nb.append([n for _, n in lst])
        self.passable = [self.terrain[c] != "#" and c != self.en_hub for c in range(N)]
        self.stakeable = [self.passable[c] and c != self.my_hub for c in range(N)]
        self.fens = [c for c in range(N) if 0 <= self.elev[c] <= 2]
        self.d_my = self.bfs([self.my_hub], None)
        self.d_en = self.bfs_from_enemy_hub()
        self.tide = Tide()
        self.enemy_stakes = set()      # remembered enemy stakes
        self.enemy_seen_turn = {}
        self.last_enemy_crews = {}
        self.turn = 0
        self.prev_level_hi = None
        self.cum_cpu = 0.0

    # ------------------------------------------------------------------ geometry
    def bfs(self, sources, avoid):
        dist = [-1] * self.N
        frontier = []
        for s in sources:
            dist[s] = 0
            frontier.append(s)
        d = 0
        nb = self.nb
        while frontier:
            d += 1
            nxt = []
            for c in frontier:
                for n in nb[c]:
                    if dist[n] < 0 and (avoid is None or not avoid[n]):
                        dist[n] = d
                        nxt.append(n)
            frontier = nxt
        return dist

    def bfs_from_enemy_hub(self):
        # distances as the enemy walks them (they may not enter my hub)
        W = self.W
        dist = [-1] * self.N
        dist[self.en_hub] = 0
        frontier = [self.en_hub]
        d = 0
        while frontier:
            d += 1
            nxt = []
            for c in frontier:
                x, y = c % W, c // W
                for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < self.Hh:
                        n = ny * W + nx
                        if self.terrain[n] != "#" and n != self.my_hub and dist[n] < 0:
                            dist[n] = d
                            nxt.append(n)
            frontier = nxt
        return dist

    def first_step(self, src, dist, target):
        """Order moving from src one step along a shortest path (dist = bfs from src)."""
        d = dist[target]
        if d <= 0:
            return "H", src
        cur = target
        nb = self.nb
        while d > 1:
            for n in nb[cur]:
                if dist[n] == d - 1:
                    cur = n
                    break
            else:
                return "H", src
            d -= 1
        for o, n in self.moves[src]:
            if n == cur:
                return o, n
        return "H", src

    # ------------------------------------------------------------------ main
    def act(self, obs):
        try:
            return self._act(obs)
        except Exception as e:  # never crash: fall back to holding
            print("bot error:", repr(e), file=sys.stderr)
            return {"orders": {}, "recruit": False}

    def _act(self, obs):
        t = obs["turn"]
        self.turn = t
        N = self.N
        elev = self.elev
        yld = self.yld
        crews = obs["crews"]
        my_stakes = set(obs["stakes"])
        visible = obs["visible"]
        flooded = set(obs["flooded"])
        en_crews = obs["enemy_crews"]
        en_stakes_vis = obs["enemy_stakes"]

        # ---------------- tide observation
        lo, hi = 0, 3
        for c in visible:
            e = elev[c]
            if 0 <= e <= 2:
                if c in flooded:
                    if e + 1 > lo:
                        lo = e + 1
                else:
                    if e < hi:
                        hi = e
        if lo > hi:
            lo, hi = 0, 3
        self.tide.observe(t, lo, hi)
        maxlev, minlev = self.tide.predict(t)
        future = self.tide.future  # exact levels if known

        # ---------------- survivable cells S1 (end-of-turn positions with an escape plan)
        safe = self.compute_safe(maxlev)

        # ---------------- enemy memory
        vis_set = set(visible)
        for c in en_stakes_vis:
            self.enemy_stakes.add(c)
            self.enemy_seen_turn[c] = t
        evs = set(en_stakes_vis)
        for c in list(self.enemy_stakes):
            if c in vis_set and c not in evs:
                self.enemy_stakes.discard(c)
            elif c in my_stakes:
                self.enemy_stakes.discard(c)
            elif elev[c] < 3 and lo > elev[c]:
                self.enemy_stakes.discard(c)   # washed away now
        for c in my_stakes:
            self.enemy_stakes.discard(c)
        enemy_at = en_crews  # {cell: count}
        enemy_adj = [0] * N   # number of enemy crews adjacent to (not on) a cell
        for c, k in enemy_at.items():
            for n in self.nb[c]:
                enemy_adj[n] += k
        # cells enemy crews could reach this turn
        enemy_reach = [0] * N
        for c, k in enemy_at.items():
            enemy_reach[c] += k
            for n in self.nb[c]:
                enemy_reach[n] += k

        # ---------------- per-elevation dry-window tables
        # dry_until[e][k]: number of consecutive turns from k (inclusive) that elevation e is
        # guaranteed dry, i.e. count of j>=k with maxlev[j] <= e until first failure (capped at H)
        dry_until = []
        for e in range(3):
            arr = [0] * (H + 2)
            run = 0
            for k in range(H, 0, -1):
                if maxlev[k] <= e:
                    run += 1
                else:
                    run = 0
                arr[k] = run
            dry_until.append(arr)
        if future is not None:
            # exact long-range dry runs
            L = len(future)
            dry_exact = []
            for e in range(3):
                arr = [0] * (L + 1)
                run = 0
                for k in range(L - 1, 0, -1):
                    if future[k] <= e:
                        run += 1
                    else:
                        run = 0
                    arr[k] = run
                dry_exact.append(arr)
        else:
            dry_exact = None

        def stake_life(c, k):
            """Turns of income for a stake planted by a K order at turn t+k on cell c
            (income turns t+k .. ); requires the cell to be dry after the tide updates
            k+1, k+2, ...  Capped by game end."""
            rem = T_TURNS - (t + k)
            if rem <= 0:
                return 0
            e = elev[c]
            if e >= 3:
                return rem
            if dry_exact is not None:
                if k + 1 < len(dry_exact[e]):
                    return min(rem, dry_exact[e][k + 1])
                return 0
            if k + 1 <= H:
                g = dry_until[e][k + 1]
                if g >= H - k:   # dry through the horizon: extrapolate a little
                    g = g + 4
                return min(rem, g)
            return 0

        def first_dry(c, k):
            """Earliest k' >= k such that a crew may stand on c at the end of turn t+k'-1,
            i.e. maxlev[k'] <= elev.  None if not within horizon."""
            e = elev[c]
            if e >= 3:
                return k
            if future is not None:
                L = len(future)
                for kk in range(max(k, 1), min(L, H + 20)):
                    if future[kk] <= e:
                        return kk
                return None
            for kk in range(max(k, 1), H + 1):
                if maxlev[kk] <= e:
                    return kk
            return None

        # ---------------- targets
        n_crews = len(crews)
        orders = {}
        assigned_cell = {}
        used_cells = set()
        crew_list = sorted(crews.items())

        # Threat response: lone enemy crews on my stake -> attack from adjacent (free kill)
        attackers = {}
        for c, k in enemy_at.items():
            if c in my_stakes:
                # my crews adjacent
                adj = [cid for cid, cc in crew_list if cc in self.nb[c] or cc == c]
                need = k  # attackers needed to kill all: n_a >= k ; my loss = k-1
                if len(adj) >= need and (k == 1 or len(adj) >= k):
                    chosen = adj[:max(need, 1)]
                    for cid in chosen:
                        cc = crews[cid]
                        if cc == c:
                            orders[cid] = "H"
                        else:
                            for o, n in self.moves[cc]:
                                if n == c:
                                    orders[cid] = o
                        assigned_cell[cid] = c
                        attackers[cid] = c

        # distance maps per crew
        avoid = [not safe[c] for c in range(N)]
        for c in enemy_at:
            avoid[c] = True
        dmaps = {}
        for cid, cc in crew_list:
            dmaps[cid] = self.bfs([cc], avoid)

        # candidate cells
        cand = []
        for c in range(N):
            if not self.stakeable[c] or c in my_stakes:
                continue
            if c in enemy_at:
                continue
            cand.append(c)

        remaining = T_TURNS - t
        scores = []
        d_my = self.d_my
        d_en = self.d_en
        en_st = self.enemy_stakes
        for cid, cc in crew_list:
            if cid in attackers:
                continue
            dist = dmaps[cid]
            for c in cand:
                d = dist[c]
                if d < 0:
                    continue
                if d > 14:
                    continue
                k = first_dry(c, d)
                if k is None:
                    continue
                life = stake_life(c, k)
                if life <= 0:
                    continue
                v = yld[c] * life
                if c in en_st:
                    v *= 1.6
                    if enemy_adj[c] > 0 or enemy_reach[c] > 0:
                        continue
                # contested bonus: cells nearer the enemy are claimed first
                de = d_en[c]
                dm = d_my[c]
                if de >= 0:
                    diff = de - dm
                    if diff < -3 and c not in en_st:
                        v *= 0.5
                    elif -3 <= diff <= 2:
                        v *= 1.25
                # danger: enemy crews adjacent to the target
                if enemy_adj[c] > 0 and c not in my_stakes:
                    v *= 0.4
                s = v / (k + 1.0)
                scores.append((s, cid, c))
        scores.sort(reverse=True)
        for s, cid, c in scores:
            if cid in assigned_cell or c in used_cells:
                continue
            assigned_cell[cid] = c
            used_cells.add(c)

        # ---------------- orders
        for cid, cc in crew_list:
            if cid in attackers:
                continue
            tgt = assigned_cell.get(cid)
            if tgt is None:
                # idle: move toward contested frontier / enemy stakes, staying safe
                best = None
                for o, n in self.moves[cc]:
                    if not safe[n] or n in enemy_at:
                        continue
                    sc = -(abs(d_en[n] - d_my[n]) if d_en[n] >= 0 else 99)
                    if best is None or sc > best[0]:
                        best = (sc, o)
                if best is not None and not safe[cc]:
                    orders[cid] = best[1]
                elif best is not None and self.d_my[cc] < 3:
                    orders[cid] = best[1]
                else:
                    orders[cid] = "H"
                continue
            dist = dmaps[cid]
            if tgt == cc:
                # stake now if safe
                if (cc not in my_stakes and safe[cc] and
                        (enemy_adj[cc] == 0 or (cc in my_stakes))):
                    orders[cid] = "K"
                elif enemy_adj[cc] > 0 and cc not in my_stakes:
                    # threatened while staking: step away to a safe cell (or hold)
                    o = self.retreat(cc, safe, enemy_reach)
                    orders[cid] = o
                else:
                    orders[cid] = "H"
                continue
            k = first_dry(tgt, dist[tgt])
            if k is not None and k > dist[tgt]:
                # must wait for the cell to dry: approach but do not step on it
                o, n = self.first_step(cc, dist, tgt)
                if n == tgt:
                    orders[cid] = "H" if safe[cc] else self.retreat(cc, safe, enemy_reach)
                    continue
            o, n = self.first_step(cc, dist, tgt)
            if not safe[n] or n in enemy_at:
                orders[cid] = self.retreat(cc, safe, enemy_reach) if not safe[cc] else "H"
            else:
                orders[cid] = o

        # ensure every crew on an unsafe cell tries to move somewhere safe
        for cid, cc in crew_list:
            o = orders.get(cid, "H")
            dest = cc
            if o in ("N", "E", "S", "W"):
                for oo, n in self.moves[cc]:
                    if oo == o:
                        dest = n
            if not safe[dest]:
                orders[cid] = self.retreat(cc, safe, enemy_reach)

        # ---------------- recruit
        recruit = False
        cost = obs["recruit_cost"]
        if obs["grain"] >= cost and n_crews < self.cap:
            recruit = self.want_recruit(t, n_crews, cost, obs, cand)
        return {"orders": orders, "recruit": recruit}

    def retreat(self, cc, safe, enemy_reach):
        """Best order to a safe neighbouring cell (prefers higher ground, fewer enemies)."""
        best = None
        for o, n in self.moves[cc]:
            if not safe[n]:
                continue
            sc = self.elev[n] * 10 - enemy_reach[n] * 3
            if best is None or sc > best[0]:
                best = (sc, o)
        if best is not None:
            return best[1]
        if safe[cc]:
            return "H"
        # nothing safe: climb
        best = None
        for o, n in self.moves[cc]:
            sc = self.elev[n]
            if best is None or sc > best[0]:
                best = (sc, o)
        return best[1] if best is not None and best[0] > self.elev[cc] else "H"

    def compute_safe(self, maxlev):
        """Cells on which a crew may end this turn and still be able to escape the tide."""
        elev = self.elev
        N = self.N
        nb = self.nb
        # fast paths
        if max(maxlev[1:]) == 0:
            return [elev[c] >= 0 and self.passable[c] for c in range(N)]
        m = maxlev[H]
        S = [self.passable[c] and elev[c] >= m for c in range(N)]
        prev_m = m
        changed = True
        for k in range(H, 0, -1):
            m = maxlev[k]
            if m == prev_m and not changed:
                continue
            newS = list(S)
            changed = False
            for c in self.fens:
                if elev[c] < m:
                    if newS[c]:
                        newS[c] = False
                        changed = True
                    continue
                if S[c]:
                    continue
                for n in nb[c]:
                    if S[n]:
                        newS[c] = True
                        changed = True
                        break
            # land cells are always safe
            S = newS
            prev_m = m
        for c in range(N):
            if elev[c] == 3 and self.passable[c]:
                S[c] = True
        return S

    def want_recruit(self, t, n, cost, obs, cand):
        remaining = T_TURNS - t
        if remaining < 25:
            return False
        if t == 0:
            return True
        # rough marginal value: an extra crew adds ~0.5 stake / turn while there is work
        work = len(cand)
        if work < 2 * n:
            return False
        g = max(0.0, 2.2 - 0.14 * n)
        return cost <= remaining * g * 0.6
