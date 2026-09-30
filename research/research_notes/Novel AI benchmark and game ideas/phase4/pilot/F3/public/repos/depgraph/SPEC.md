# Spec: `depgraph`

`depgraph.DepGraph` stores build targets and their dependencies. "`x` depends on `d`" means `d` must be built before `x`. Exceptions are named by class; any subclass also satisfies a rule. Messages are unspecified. "Sorted" means ascending Python string order.

**Domain.** Node names are non-empty strings of at most 10 characters. `deps` is a list of at most 10 node names. Behaviour on other argument types is unspecified.

| Rule | Statement |
|---|---|
| D1 | `add(node, deps=())` records that `node` depends on every name in `deps` (adding to any earlier dependencies of `node`). Every name in `deps` that is not yet a node becomes a node with no dependencies. Raises `GraphError` and changes nothing if `node` appears in `deps`. Cycles through two or more nodes may be created; they are reported by D4. |
| D2 | `remove(node)` deletes `node` and its own dependency edges. Raises `GraphError` and changes nothing if `node` is unknown or if another node depends on it. |
| D3 | `nodes()` returns all nodes, sorted. `deps_of(node)` returns the direct dependencies of `node`, sorted; raises `GraphError` for an unknown node. |
| D4 | If the dependency relation has a cycle, `order()`, `layers()` and `affected(node)` (for a known `node`) raise `CycleError`. |
| D5 | Otherwise `order()` returns every node exactly once, built greedily: at each step the next node is the smallest (sorted order) node, among those not yet listed, whose dependencies have all been listed. |
| D6 | `layers()` returns a list of lists. The depth of a node with no dependencies is 0; otherwise it is 1 plus the largest depth among its dependencies. Entry `i` holds the nodes of depth `i`, sorted. There are no empty entries. |
| D7 | `affected(node)` returns `node` together with every node that depends on it directly or transitively, listed in the relative order they have in `order()`. Raises `GraphError` for an unknown node. |
| D8 | Only `add` and `remove` change the graph. |

## Witness format

A witness is a JSON object `{"ops": [...]}` with at most 60 operations. A fresh `DepGraph()` is created, then each operation `[method, arg1, ...]` is called in order, with `method` one of `add`, `remove`, `nodes`, `deps_of`, `order`, `layers`, `affected`. Exceptions are recorded and execution continues. Example: `{"ops": [["add", "app", ["lib"]], ["order"]]}`.
