"""Brackwater bot API helpers (public source).

A bot is a Python file defining

    class Bot:
        def __init__(self, player: int, game_info: dict): ...
        def act(self, obs: dict) -> dict: ...

See API.md for the observation and action formats.  Nothing in this module is required;
it only offers conveniences (grid geometry, legal orders, distances, recruit cost).
"""
from collections import deque

ORDERS = ("N", "E", "S", "W", "H", "K")
MOVES = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


def recruit_cost(n_crews):
    """Grain needed to recruit one crew when you currently have n_crews crews."""
    return int(12 * 1.2 ** n_crews)


class Grid:
    """Static geometry built from game_info.  Cells are integers c = y * width + x."""

    def __init__(self, game_info):
        self.info = game_info
        self.player = game_info["player"]
        self.W = game_info["width"]
        self.H = game_info["height"]
        self.N = self.W * self.H
        self.terrain = game_info["terrain"]
        self.hubs = list(game_info["hubs"])
        self.my_hub = self.hubs[self.player]
        self.enemy_hub = self.hubs[1 - self.player]
        self.crew_cap = game_info["crew_cap"]
        self.turns = game_info["turns"]
        ylds = game_info["yields"]
        # elevation: -1 rock, 0/1/2 fen, 3 land (incl. hubs)
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
        # legal moves for *this* player: list of (order, target) per cell (enemy hub excluded)
        self.moves = []
        for c in range(self.N):
            x, y = c % self.W, c // self.W
            lst = []
            for o, (dx, dy) in MOVES.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.W and 0 <= ny < self.H:
                    n = ny * self.W + nx
                    if self.terrain[n] != "#" and n != self.enemy_hub:
                        lst.append((o, n))
            self.moves.append(lst)

    def xy(self, c):
        return c % self.W, c // self.W

    def cell(self, x, y):
        return y * self.W + x

    def passable(self, c):
        return self.terrain[c] != "#" and c != self.enemy_hub

    def neighbors(self, c):
        """Cells reachable from c in one legal move."""
        return [n for _, n in self.moves[c]]

    def legal_orders(self, c):
        """All legal orders for a crew standing on cell c."""
        return [o for o, _ in self.moves[c]] + ["H", "K"]

    def chebyshev(self, a, b):
        return max(abs(a % self.W - b % self.W), abs(a // self.W - b // self.W))

    def bfs(self, sources, avoid=None):
        """Shortest legal-move distances from one or more source cells (list, -1 = unreachable).
        `avoid` is an optional set of cells that may not be entered."""
        if isinstance(sources, int):
            sources = [sources]
        dist = [-1] * self.N
        dq = deque()
        for s in sources:
            dist[s] = 0
            dq.append(s)
        moves = self.moves
        while dq:
            c = dq.popleft()
            d = dist[c] + 1
            for _, n in moves[c]:
                if dist[n] < 0 and (avoid is None or n not in avoid):
                    dist[n] = d
                    dq.append(n)
        return dist

    def step_toward(self, c, dist_to_target):
        """An order moving from c one step closer along a distance map (from bfs(target)); 'H' if none."""
        best, bo = dist_to_target[c], "H"
        for o, n in self.moves[c]:
            d = dist_to_target[n]
            if 0 <= d < best:
                best, bo = d, o
        return bo
