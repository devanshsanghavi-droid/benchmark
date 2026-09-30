from common import Exps, Invalid, exact, is_name, nargs, need


def validate(ops):
    try:
        for op in ops:
            m, a = op[0], op[1:]
            if m == "add":
                nargs(op, 1, 2)
                need(is_name(a[0], 10), "node")
                if len(a) == 2:
                    need(isinstance(a[1], list) and len(a[1]) <= 10
                         and all(is_name(x, 10) for x in a[1]), "deps")
            elif m in ("remove", "deps_of", "affected"):
                nargs(op, 1)
                need(is_name(a[0], 10), "node")
            else:
                nargs(op, 0)
        return None
    except Invalid as e:
        return str(e)


def greedy(g):
    done, out = set(), []
    while True:
        ready = [n for n in g if n not in done and g[n] <= done]
        if not ready:
            break
        n = min(ready)
        out.append(n)
        done.add(n)
    return out if len(out) == len(g) else None


def expected(ops):
    g = {}
    out = Exps()
    for op in ops:
        m, a = op[0], op[1:]
        if m == "add":
            node, deps = a[0], (a[1] if len(a) > 1 else [])
            if node in deps:
                out.append(("exc", {"GraphError"}))
                continue
            g.setdefault(node, set()).update(deps)
            for d in deps:
                g.setdefault(d, set())
            out.append(("ok", None, exact))
        elif m == "remove":
            n = a[0]
            if n not in g or any(n in ds for k, ds in g.items() if k != n):
                out.append(("exc", {"GraphError"}))
            else:
                del g[n]
                out.append(("ok", None, exact))
        elif m == "nodes":
            out.append(("ok", sorted(g), exact))
        elif m == "deps_of":
            out.append(("ok", sorted(g[a[0]]), exact) if a[0] in g else ("exc", {"GraphError"}))
        else:
            if m == "affected" and a[0] not in g:
                out.append(("exc", {"GraphError"}))
                continue
            order = greedy(g)
            if order is None:
                out.append(("exc", {"CycleError"}))
            elif m == "order":
                out.append(("ok", order, exact))
            elif m == "layers":
                depth = {}
                for n in order:
                    depth[n] = 1 + max((depth[d] for d in g[n]), default=-1)
                layers = [sorted(n for n in g if depth[n] == i)
                          for i in range(max(depth.values(), default=-1) + 1)]
                out.append(("ok", layers, exact))
            elif m == "affected":
                hit, frontier = {a[0]}, [a[0]]
                while frontier:
                    x = frontier.pop()
                    for n, ds in g.items():
                        if x in ds and n not in hit:
                            hit.add(n)
                            frontier.append(n)
                out.append(("ok", [n for n in order if n in hit], exact))
    return out


def fuzz(rng):
    names = list("abcdef")
    ops = []
    for _ in range(rng.randint(2, 10)):
        k = rng.random()
        if k < 0.6:
            n = rng.choice(names)
            ops.append(["add", n, rng.sample(names, rng.randint(0, 2))])
        elif k < 0.7:
            ops.append(["remove", rng.choice(names)])
        elif k < 0.8:
            ops.append(["affected", rng.choice(names)])
        else:
            ops.append([rng.choice(["order", "layers", "nodes"])])
    ops += [["order"], ["layers"]]
    return ops
