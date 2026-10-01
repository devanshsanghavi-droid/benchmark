"""Brackwater engine (SEALED SOURCE). The public copy is shipped only as compiled bytecode.

Hidden dynamics (not in the public rules beyond a qualitative description):
  * tide period P ~ U{20..40}, phase ~ U{0..P-1}, drawn per match from the match seed;
  * triangle wave h(t) = 1 - |2f - 1|, f = ((t + phase) mod P) / P;
  * level = #thresholds exceeded among (0.55, 0.72, 0.88)  -> elev-0 fens flooded 45% of
    the time, elev-1 28%, elev-2 12%; level changes by at most 1 per turn for P >= 20.
"""
import json
import random

VERSION = "1.0"

TURNS = 200
START_CREWS = 3
START_GRAIN = 20
HUB_INCOME = 2
CREW_CAP = 24
VISION_CREW = 2
VISION_HUB = 3
VISION_STAKE = 1
ORDERS = ("N", "E", "S", "W", "H", "K")
YIELDS = {".": 1, "2": 2, "1": 3, "0": 5}

_TIDE_TH = (0.55, 0.72, 0.88)
_PERIOD_RANGE = (20, 40)


class IllegalAction(Exception):
    pass


def recruit_cost(n_crews):
    return int(12 * 1.2 ** n_crews)


def _tide_levels(period, phase, n):
    out = []
    for t in range(n):
        f = ((t + phase) % period) / period
        h = 1.0 - abs(2.0 * f - 1.0)
        lvl = 0
        for th in _TIDE_TH:
            if h > th:
                lvl += 1
        out.append(lvl)
    return out


def load_map(path):
    with open(path) as fh:
        return parse_map(json.load(fh))


def parse_map(d):
    rows = d["rows"]
    H = len(rows)
    W = len(rows[0])
    terrain = "".join(rows)
    if len(terrain) != W * H:
        raise ValueError("ragged map")
    for ch in terrain:
        if ch not in "#.012AB":
            raise ValueError("bad terrain char %r" % ch)
    hubs = [terrain.index("A"), terrain.index("B")]
    return {"name": d.get("name", "map"), "width": W, "height": H, "rows": list(rows),
            "terrain": terrain, "hubs": hubs}


class _Geo:
    """Per-map precomputation."""

    def __init__(self, m):
        W, H = m["width"], m["height"]
        self.W, self.H, self.N = W, H, W * H
        t = m["terrain"]
        self.terrain = t
        self.hubs = list(m["hubs"])
        elev = []
        for ch in t:
            if ch == "#":
                elev.append(-1)
            elif ch in "012":
                elev.append(int(ch))
            else:
                elev.append(3)
        self.elev = elev
        self.yld = [YIELDS.get(ch, 0) for ch in t]
        self.by_elev = [[c for c in range(self.N) if elev[c] == e] for e in range(3)]
        # moves: dict order->target or None (off-board or rock). Enemy hub handled per player.
        self.nbr = []
        for c in range(self.N):
            x, y = c % W, c // W
            d = {}
            for o, (dx, dy) in (("N", (0, -1)), ("E", (1, 0)), ("S", (0, 1)), ("W", (-1, 0))):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and t[ny * W + nx] != "#":
                    d[o] = ny * W + nx
                else:
                    d[o] = None
            self.nbr.append(d)
        self.vis_crew = [self._box(c, VISION_CREW) for c in range(self.N)]
        self.vis_hub = [self._box(h, VISION_HUB) for h in self.hubs]
        self.vis_stake = [self._box(c, VISION_STAKE) for c in range(self.N)]

    def _box(self, c, r):
        W, H = self.W, self.H
        x, y = c % W, c // W
        return tuple(ny * W + nx for ny in range(max(0, y - r), min(H, y + r + 1))
                     for nx in range(max(0, x - r), min(W, x + r + 1)))


class Match:
    """One 2-player match.  Documented API: game_info(p), observe(p), validate(p, action),
    step([a0, a1]), done, turn, grain, result()."""

    def __init__(self, map_data, seed):
        self._g = _Geo(map_data)
        self.map_name = map_data.get("name", "map")
        rng = random.Random(("brackwater-tide", int(seed)).__repr__())
        self.__p = rng.randint(*_PERIOD_RANGE)
        self.__ph = rng.randrange(self.__p)
        self.__lv = _tide_levels(self.__p, self.__ph, TURNS + 1)
        g = self._g
        self.turn = 0
        self.done = False
        self._level = self.__lv[0]
        self._flooded = bytearray(g.N)
        for e in range(self._level):
            for c in g.by_elev[e]:
                self._flooded[c] = 1
        self._flooded_set = {c for c in range(g.N) if self._flooded[c]}
        self.grain = [START_GRAIN, START_GRAIN]
        self._crews = [{}, {}]
        self._next_id = [0, 0]
        for p in (0, 1):
            for _ in range(START_CREWS):
                self._crews[p][self._next_id[p]] = g.hubs[p]
                self._next_id[p] += 1
        self._owner = [-1] * g.N
        self._stakes = [set(), set()]
        self._yield_sum = [0, 0]
        self._last_income = [0, 0]
        self._lost_crews = [{}, {}]
        self._lost_stakes = [[], []]
        self._new_crew = [None, None]
        self._stats = {"drowned": [0, 0], "combat_losses": [0, 0], "recruited": [0, 0],
                       "stakes_taken": [0, 0], "washed": [0, 0]}

    # ------------------------------------------------------------------ info
    def game_info(self, p):
        g = self._g
        return {
            "player": p, "width": g.W, "height": g.H, "turns": TURNS,
            "terrain": g.terrain, "hubs": list(g.hubs),
            "yields": dict(YIELDS), "hub_income": HUB_INCOME, "crew_cap": CREW_CAP,
            "start_crews": START_CREWS, "start_grain": START_GRAIN,
            "vision": {"crew": VISION_CREW, "hub": VISION_HUB, "stake": VISION_STAKE},
            "version": VERSION,
        }

    def observe(self, p):
        g = self._g
        q = 1 - p
        vis = set(g.vis_hub[p])
        vc = g.vis_crew
        for c in set(self._crews[p].values()):
            vis.update(vc[c])
        vs = g.vis_stake
        for c in self._stakes[p]:
            vis.update(vs[c])
        ec = {}
        for c in self._crews[q].values():
            if c in vis:
                ec[c] = ec.get(c, 0) + 1
        return {
            "turn": self.turn,
            "grain": self.grain[p],
            "income": self._last_income[p],
            "recruit_cost": recruit_cost(len(self._crews[p])),
            "crews": dict(self._crews[p]),
            "stakes": sorted(self._stakes[p]),
            "visible": sorted(vis),
            "flooded": sorted(vis & self._flooded_set),
            "enemy_crews": ec,
            "enemy_stakes": sorted(vis & self._stakes[q]),
            "lost_crews": dict(self._lost_crews[p]),
            "lost_stakes": sorted(self._lost_stakes[p]),
            "new_crew": self._new_crew[p],
        }

    # ------------------------------------------------------------ validation
    def validate(self, p, action):
        """Return a normalised action {'recruit': bool, 'orders': {id: order}} or raise IllegalAction."""
        if not isinstance(action, dict):
            raise IllegalAction("action must be a dict, got %s" % type(action).__name__)
        rec = action.get("recruit", False)
        if rec is None:
            rec = False
        if isinstance(rec, bool):
            pass
        elif isinstance(rec, int) and rec in (0, 1):
            rec = bool(rec)
        else:
            raise IllegalAction("'recruit' must be a bool (or 0/1), got %r" % (rec,))
        crews = self._crews[p]
        if rec:
            n = len(crews)
            if n >= CREW_CAP:
                raise IllegalAction("recruit at crew cap (%d)" % CREW_CAP)
            cost = recruit_cost(n)
            if self.grain[p] < cost:
                raise IllegalAction("recruit unaffordable: grain %d < cost %d" % (self.grain[p], cost))
        orders = action.get("orders", {})
        if orders is None:
            orders = {}
        if not isinstance(orders, dict):
            raise IllegalAction("'orders' must be a dict")
        g = self._g
        enemy_hub = g.hubs[1 - p]
        out = {}
        for k, o in orders.items():
            if isinstance(k, bool):
                raise IllegalAction("bad crew id %r" % (k,))
            if isinstance(k, str):
                try:
                    cid = int(k)
                except ValueError:
                    raise IllegalAction("bad crew id %r" % (k,))
            elif isinstance(k, int):
                cid = k
            else:
                raise IllegalAction("bad crew id %r" % (k,))
            if cid not in crews:
                raise IllegalAction("unknown crew id %r" % (k,))
            if cid in out:
                raise IllegalAction("duplicate crew id %r" % (k,))
            if not isinstance(o, str) or o not in ORDERS:
                raise IllegalAction("bad order %r for crew %d" % (o, cid))
            if o in "NESW":
                tgt = g.nbr[crews[cid]][o]
                if tgt is None:
                    raise IllegalAction("crew %d: move %s leaves the board or enters rock" % (cid, o))
                if tgt == enemy_hub:
                    raise IllegalAction("crew %d: move %s enters the enemy hub" % (cid, o))
            out[cid] = o
        return {"recruit": rec, "orders": out}

    # ------------------------------------------------------------------ step
    def _remove_stake(self, c, record=True):
        o = self._owner[c]
        if o >= 0:
            self._owner[c] = -1
            self._stakes[o].discard(c)
            self._yield_sum[o] -= self._g.yld[c]
            if record:
                self._lost_stakes[o].append(c)
        return o

    def step(self, actions):
        """actions: list of two *validated* actions (output of validate)."""
        if self.done:
            raise RuntimeError("match is over")
        g = self._g
        crews = self._crews
        lost_c = [{}, {}]
        self._lost_stakes = [[], []]
        new_crew = [None, None]
        # 1. recruit
        for p in (0, 1):
            if actions[p]["recruit"]:
                self.grain[p] -= recruit_cost(len(crews[p]))
                cid = self._next_id[p]
                self._next_id[p] += 1
                crews[p][cid] = g.hubs[p]
                new_crew[p] = cid
                self._stats["recruited"][p] += 1
        # 2. movement
        stakers = ([], [])
        nbr = g.nbr
        for p in (0, 1):
            cp = crews[p]
            for cid, o in actions[p]["orders"].items():
                if o == "K":
                    stakers[p].append(cid)
                elif o != "H":
                    cp[cid] = nbr[cp[cid]][o]
        # 3. combat
        occ0 = {}
        for cid, c in crews[0].items():
            occ0.setdefault(c, []).append(cid)
        occ1 = {}
        for cid, c in crews[1].items():
            occ1.setdefault(c, []).append(cid)
        owner = self._owner
        for c in occ0.keys() & occ1.keys():
            a = sorted(occ0[c])
            b = sorted(occ1[c])
            la = len(b) - (1 if owner[c] == 0 else 0)
            lb = len(a) - (1 if owner[c] == 1 else 0)
            la = max(0, min(len(a), la))
            lb = max(0, min(len(b), lb))
            for cid in a[len(a) - la:]:
                del crews[0][cid]
                lost_c[0][cid] = "combat"
            for cid in b[len(b) - lb:]:
                del crews[1][cid]
                lost_c[1][cid] = "combat"
            self._stats["combat_losses"][0] += la
            self._stats["combat_losses"][1] += lb
        # 4. staking
        yld = g.yld
        for p in (0, 1):
            cp = crews[p]
            hub = g.hubs[p]
            for cid in stakers[p]:
                c = cp.get(cid)
                if c is None or c == hub or owner[c] == p:
                    continue
                if owner[c] >= 0:
                    self._remove_stake(c)
                    self._stats["stakes_taken"][p] += 1
                owner[c] = p
                self._stakes[p].add(c)
                self._yield_sum[p] += yld[c]
        # 5. tide
        self.turn += 1
        nl = self.__lv[self.turn]
        if nl > self._level:
            for e in range(self._level, nl):
                for c in g.by_elev[e]:
                    self._flooded[c] = 1
                    self._flooded_set.add(c)
                    o = self._remove_stake(c)
                    if o >= 0:
                        self._stats["washed"][o] += 1
        elif nl < self._level:
            for e in range(nl, self._level):
                for c in g.by_elev[e]:
                    self._flooded[c] = 0
                    self._flooded_set.discard(c)
        self._level = nl
        fl = self._flooded
        for p in (0, 1):
            cp = crews[p]
            dead = [cid for cid, c in cp.items() if fl[c]]
            for cid in dead:
                del cp[cid]
                lost_c[p][cid] = "drowned"
            self._stats["drowned"][p] += len(dead)
        # 6. income
        for p in (0, 1):
            inc = HUB_INCOME + self._yield_sum[p]
            self.grain[p] += inc
            self._last_income[p] = inc
        self._lost_crews = lost_c
        self._new_crew = new_crew
        if self.turn >= TURNS:
            self.done = True

    def render(self):
        """Full-information ASCII view (debugging only; bots never see this).
        Two characters per cell: terrain ('#', '.', '0'-'2', '~' flooded fen, '@' hub) then
        occupant ('A'/'B' crews present, 'a'/'b' stake owner, ' ' empty)."""
        g = self._g
        occ = {}
        for p in (0, 1):
            for c in self._crews[p].values():
                occ.setdefault(c, [0, 0])[p] += 1
        lines = ["turn %d  grain A=%d B=%d  crews A=%d B=%d  stakes A=%d B=%d" % (
            self.turn, self.grain[0], self.grain[1], len(self._crews[0]), len(self._crews[1]),
            len(self._stakes[0]), len(self._stakes[1]))]
        for y in range(g.H):
            row = []
            for x in range(g.W):
                c = y * g.W + x
                ch = g.terrain[c]
                t = "@" if ch in "AB" else ("~" if self._flooded[c] else ch)
                if c in occ:
                    a, b = occ[c]
                    o = ("A" if a else "B")
                elif self._owner[c] >= 0:
                    o = "ab"[self._owner[c]]
                else:
                    o = " "
                row.append(t + o)
            lines.append("".join(row))
        return "\n".join(lines)

    def result(self):
        g0, g1 = self.grain
        w = 0 if g0 > g1 else (1 if g1 > g0 else None)
        return {"grain": [g0, g1], "winner": w, "turns": self.turn, "stats": self._stats}
