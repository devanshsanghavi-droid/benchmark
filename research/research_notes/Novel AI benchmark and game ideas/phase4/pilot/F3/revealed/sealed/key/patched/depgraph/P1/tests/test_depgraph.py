import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from depgraph import CycleError, DepGraph, GraphError  # noqa: E402


class DepGraphTests(unittest.TestCase):
    def test_chain(self):
        g = DepGraph()
        g.add("c", ["b"])
        g.add("b", ["a"])
        self.assertEqual(g.order(), ["a", "b", "c"])
        self.assertEqual(g.layers(), [["a"], ["b"], ["c"]])

    def test_independent_sorted(self):
        g = DepGraph()
        for n in ("zeta", "alpha", "mid"):
            g.add(n)
        self.assertEqual(g.order(), ["alpha", "mid", "zeta"])

    def test_diamond(self):
        g = DepGraph()
        g.add("top", ["left", "right"])
        g.add("left", ["base"])
        g.add("right", ["base"])
        self.assertEqual(g.order(), ["base", "left", "right", "top"])
        self.assertEqual(g.layers(), [["base"], ["left", "right"], ["top"]])
        self.assertEqual(g.affected("left"), ["left", "top"])
        self.assertEqual(g.affected("base"), ["base", "left", "right", "top"])

    def test_cycle(self):
        g = DepGraph()
        g.add("a", ["b"])
        g.add("b", ["a"])
        with self.assertRaises(CycleError):
            g.order()
        with self.assertRaises(CycleError):
            g.layers()

    def test_self_dependency(self):
        g = DepGraph()
        with self.assertRaises(GraphError):
            g.add("a", ["a"])
        self.assertEqual(g.nodes(), [])

    def test_remove(self):
        g = DepGraph()
        g.add("app", ["lib"])
        with self.assertRaises(GraphError):
            g.remove("lib")
        g.remove("app")
        self.assertEqual(g.nodes(), ["lib"])
        with self.assertRaises(GraphError):
            g.remove("app")

    def test_deps_of(self):
        g = DepGraph()
        g.add("x", ["b", "a"])
        g.add("x", ["c"])
        self.assertEqual(g.deps_of("x"), ["a", "b", "c"])
        self.assertEqual(g.deps_of("a"), [])
        with self.assertRaises(GraphError):
            g.deps_of("nope")


if __name__ == "__main__":
    unittest.main()
