import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ratelimit import ClockError, Limiter  # noqa: E402


class LimiterTests(unittest.TestCase):
    def test_capacity(self):
        lim = Limiter(3, 100)
        self.assertEqual([lim.allow("a", t) for t in (1, 2, 3, 4)], [True, True, True, False])
        self.assertEqual(lim.remaining("a", 5), 0)

    def test_window_expiry(self):
        lim = Limiter(2, 10)
        self.assertTrue(lim.allow("a", 0))
        self.assertTrue(lim.allow("a", 3))
        self.assertFalse(lim.allow("a", 9))
        self.assertTrue(lim.allow("a", 11))
        self.assertFalse(lim.allow("a", 12))
        self.assertTrue(lim.allow("a", 14))

    def test_denied_not_recorded(self):
        lim = Limiter(1, 10)
        self.assertTrue(lim.allow("a", 0))
        self.assertFalse(lim.allow("a", 5))
        self.assertTrue(lim.allow("a", 12))

    def test_remaining(self):
        lim = Limiter(4, 50)
        lim.allow("a", 1)
        lim.allow("a", 2)
        self.assertEqual(lim.remaining("a", 30), 2)
        self.assertEqual(lim.remaining("a", 60), 4)
        self.assertEqual(lim.remaining("zz", 60), 4)

    def test_retry_after(self):
        lim = Limiter(2, 10)
        lim.allow("a", 100)
        self.assertEqual(lim.retry_after("a", 101), 0)
        lim.allow("a", 104)
        self.assertEqual(lim.retry_after("a", 105), 5)

    def test_keys_and_reset(self):
        lim = Limiter(2, 10)
        lim.allow("a", 1)
        lim.allow("b", 2)
        self.assertEqual(sorted(lim.keys(3)), ["a", "b"])
        lim.reset("a")
        self.assertEqual(lim.keys(4), ["b"])
        self.assertEqual(lim.keys(50), [])
        lim.reset("nope")

    def test_clock(self):
        lim = Limiter(2, 10)
        lim.allow("a", 10)
        lim.allow("a", 10)
        with self.assertRaises(ClockError):
            lim.allow("b", 9)
        with self.assertRaises(ValueError):
            lim.remaining("a", 3)

    def test_bad_constructor(self):
        with self.assertRaises(ValueError):
            Limiter(0, 10)
        with self.assertRaises(ValueError):
            Limiter(1, 0)


if __name__ == "__main__":
    unittest.main()
