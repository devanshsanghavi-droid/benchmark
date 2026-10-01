"""Brackwater map generator (SEALED). Point-symmetric 16x16 maps: cell i <-> N-1-i."""
import math
import random

W = H = 16


def _mirror(c, N):
    return N - 1 - c


def generate(seed, W=W, H=H, name=None):
    rng = random.Random("brackwater-map-%d" % seed)
    N = W * H
    for _attempt in range(200):
        # --- fen basins (symmetric set) ---
        basins = []
        k = rng.randint(2, 4)
        for _ in range(k):
            cx, cy = rng.uniform(0, W - 1), rng.uniform(0, H - 1)
            r = rng.uniform(2.0, 3.8)
            basins.append((cx, cy, r))
            basins.append((W - 1 - cx, H - 1 - cy, r))
        if rng.random() < 0.7:  # contested central marsh
            basins.append(((W - 1) / 2 + rng.uniform(-1, 1), (H - 1) / 2 + rng.uniform(-1, 1), rng.uniform(2.2, 3.6)))
            cx, cy, r = basins[-1]
            basins.append((W - 1 - cx, H - 1 - cy, r))
        noise = [0.0] * N
        for c in range(N // 2):
            v = rng.uniform(-0.18, 0.18)
            noise[c] = v
            noise[_mirror(c, N)] = v
        elev = [3] * N
        for c in range(N):
            x, y = c % W, c // W
            best = 3
            for (bx, by, r) in basins:
                d = math.hypot(x - bx, y - by)
                depth = 1.0 - d / r + noise[c]
                if depth > 0.62:
                    e = 0
                elif depth > 0.34:
                    e = 1
                elif depth > 0.0:
                    e = 2
                else:
                    e = 3
                best = min(best, e)
            elev[c] = best
        # --- hubs ---
        hx, hy = rng.randint(1, 3), rng.randint(1, 3)
        ha = hy * W + hx
        hb = _mirror(ha, N)
        for h in (ha, hb):
            x0, y0 = h % W, h // W
            for yy in range(max(0, y0 - 2), min(H, y0 + 3)):
                for xx in range(max(0, x0 - 2), min(W, x0 + 3)):
                    elev[yy * W + xx] = 3
        # --- rocks ---
        rock = [False] * N
        n_rock = rng.randint(8, 16)  # per half
        placed = 0
        tries = 0
        while placed < n_rock and tries < 1000:
            tries += 1
            c = rng.randrange(N)
            m = _mirror(c, N)
            if c == m:
                continue
            x, y = c % W, c // W
            if max(abs(x - ha % W), abs(y - ha // W)) <= 2 or max(abs(x - hb % W), abs(y - hb // W)) <= 2:
                continue
            if rock[c]:
                continue
            rock[c] = rock[m] = True
            placed += 1
            # occasionally grow a short ridge
            if rng.random() < 0.5:
                dx, dy = rng.choice([(1, 0), (0, 1), (1, 1), (1, -1)])
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H:
                    c2 = ny * W + nx
                    m2 = _mirror(c2, N)
                    if c2 != m2 and max(abs(nx - ha % W), abs(ny - ha // W)) > 2 and max(abs(nx - hb % W), abs(ny - hb // W)) > 2:
                        rock[c2] = rock[m2] = True
        # --- connectivity: keep component of hub A ---
        seen = {ha}
        stack = [ha]
        while stack:
            c = stack.pop()
            x, y = c % W, c // W
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < W and 0 <= ny < H:
                    n = ny * W + nx
                    if not rock[n] and n not in seen:
                        seen.add(n)
                        stack.append(n)
        if hb not in seen:
            continue
        for c in range(N):
            if c not in seen:
                rock[c] = True
        # --- quality checks ---
        open_cells = [c for c in range(N) if not rock[c]]
        fen = [c for c in open_cells if elev[c] < 3]
        e0 = [c for c in fen if elev[c] == 0]
        frac = len(fen) / len(open_cells)
        if not (0.28 <= frac <= 0.55):
            continue
        if len(e0) < 8:
            continue
        if len(open_cells) < 200:
            continue
        # build rows
        rows = []
        for y in range(H):
            row = []
            for x in range(W):
                c = y * W + x
                if c == ha:
                    row.append("A")
                elif c == hb:
                    row.append("B")
                elif rock[c]:
                    row.append("#")
                elif elev[c] == 3:
                    row.append(".")
                else:
                    row.append(str(elev[c]))
            rows.append("".join(row))
        return {"name": name or ("gen-%d" % seed), "rows": rows}
    raise RuntimeError("map generation failed for seed %d" % seed)


if __name__ == "__main__":
    import sys
    for s in map(int, sys.argv[1:] or ["1", "2", "3"]):
        m = generate(s)
        print(m["name"])
        print("\n".join(m["rows"]))
        print()
