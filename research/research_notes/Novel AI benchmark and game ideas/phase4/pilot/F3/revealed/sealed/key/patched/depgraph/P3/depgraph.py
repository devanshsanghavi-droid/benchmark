"""Dependency graph with deterministic build ordering."""

import heapq


class GraphError(ValueError):
    pass


class CycleError(GraphError):
    pass


class DepGraph:
    def __init__(self):
        self._deps = {}

    def add(self, node, deps=()):
        if not isinstance(node, str) or not node:
            raise GraphError("bad node name")
        deps = list(deps)
        if node in deps:
            raise CycleError("self dependency")
        self._deps.setdefault(node, set()).update(deps)
        for d in deps:
            self._deps.setdefault(d, set())

    def remove(self, node):
        if node not in self._deps:
            raise GraphError("unknown node")
        if any(node in ds for n, ds in self._deps.items() if n != node):
            raise GraphError("node has dependents")
        del self._deps[node]

    def nodes(self):
        return sorted(self._deps)

    def deps_of(self, node):
        if node not in self._deps:
            raise GraphError("unknown node")
        return sorted(self._deps[node])

    def _indegrees(self):
        waiting = {n: len(ds) for n, ds in self._deps.items()}
        users = {n: [] for n in self._deps}
        for n, ds in self._deps.items():
            for d in ds:
                users[d].append(n)
        return waiting, users

    def order(self):
        waiting, users = self._indegrees()
        ready = [n for n, k in waiting.items() if k == 0]
        heapq.heapify(ready)
        out = []
        while ready:
            n = heapq.heappop(ready)
            out.append(n)
            for u in users[n]:
                waiting[u] -= 1
                if waiting[u] == 0:
                    heapq.heappush(ready, u)
        if len(out) != len(self._deps):
            stuck = sorted(n for n, k in waiting.items() if k > 0)
            raise CycleError("cycle among: " + ", ".join(stuck))
        return out

    def layers(self):
        order = self.order()
        depth = {}
        for n in order:
            depth[n] = 1 + max((depth[d] for d in self._deps[n]), default=-1)
        width = max(depth.values(), default=-1) + 1
        return [sorted(n for n in order if depth[n] == i) for i in range(width)]

    def affected(self, node):
        """Nodes that must be rebuilt when `node` changes (node included)."""
        if node not in self._deps:
            raise GraphError("unknown node")
        _, users = self._indegrees()
        seen = {node}
        stack = [node]
        while stack:
            n = stack.pop()
            for u in users[n]:
                if u not in seen:
                    seen.add(u)
                    stack.append(u)
        return [n for n in self.order() if n in seen]
