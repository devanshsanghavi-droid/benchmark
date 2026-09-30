import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intervals import IntervalSet  # noqa: E402


class IntervalTests(unittest.TestCase):
    def test_add_merge(self):
        s = IntervalSet()
        s.add(0, 5)
        s.add(10, 15)
        s.add(3, 12)
        self.assertEqual(s.intervals(), [(0, 15)])

    def test_add_adjacent(self):
        s = IntervalSet()
        s.add(0, 5)
        s.add(5, 8)
        s.add(20, 25)
        self.assertEqual(s.intervals(), [(0, 8), (20, 25)])
        self.assertEqual(s.measure(), 13)

    def test_empty_and_invalid(self):
        s = IntervalSet()
        s.add(4, 4)
        self.assertEqual(s.intervals(), [])
        with self.assertRaises(ValueError):
            s.add(5, 2)
        with self.assertRaises(ValueError):
            s.remove(5, 2)

    def test_remove_middle(self):
        s = IntervalSet()
        s.add(0, 10)
        s.remove(3, 7)
        self.assertEqual(s.intervals(), [(0, 3), (7, 10)])

    def test_remove_edges(self):
        s = IntervalSet()
        s.add(0, 10)
        s.add(20, 30)
        s.remove(-5, 2)
        s.remove(8, 22)
        self.assertEqual(s.intervals(), [(2, 8), (22, 30)])
        s.remove(-100, 100)
        self.assertEqual(s.intervals(), [])

    def test_contains(self):
        s = IntervalSet()
        s.add(0, 3)
        s.add(6, 9)
        self.assertTrue(s.contains(0))
        self.assertFalse(s.contains(3))
        self.assertTrue(s.contains(8))
        self.assertFalse(s.contains(-1))
        self.assertFalse(s.contains(100))

    def test_gaps(self):
        s = IntervalSet()
        s.add(2, 4)
        s.add(6, 8)
        self.assertEqual(s.gaps(0, 10), [(0, 2), (4, 6), (8, 10)])
        self.assertEqual(s.gaps(3, 7), [(4, 6)])
        self.assertEqual(s.gaps(2, 4), [])

    def test_overlaps(self):
        s = IntervalSet()
        s.add(10, 20)
        self.assertTrue(s.overlaps(15, 30))
        self.assertFalse(s.overlaps(20, 30))
        self.assertFalse(s.overlaps(0, 10))
        self.assertFalse(s.overlaps(12, 12))


if __name__ == "__main__":
    unittest.main()
