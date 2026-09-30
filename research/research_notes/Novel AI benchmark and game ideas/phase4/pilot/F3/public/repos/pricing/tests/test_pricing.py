import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pricing import PricingError, checkout, line_total, split_payment, tax_on  # noqa: E402


class PricingTests(unittest.TestCase):
    def test_simple(self):
        r = checkout([["pen", 150, 2], ["pad", 400, 1]])
        self.assertEqual(r["subtotal"], 700)
        self.assertEqual(r["discount"], 0)
        self.assertEqual(r["shipping"], 599)
        self.assertEqual(r["tax"], 58)
        self.assertEqual(r["total"], 700 + 58 + 599)

    def test_bulk(self):
        self.assertEqual(line_total(250, 12), 2700)
        self.assertEqual(line_total(250, 9), 2250)
        r = checkout([["cup", 250, 12]])
        self.assertEqual(r["discount"], 300)
        self.assertEqual(r["net"], 2700)

    def test_free_shipping(self):
        r = checkout([["lamp", 6000, 1]])
        self.assertEqual(r["shipping"], 0)
        r = checkout([["lamp", 4999, 1]])
        self.assertEqual(r["shipping"], 599)

    def test_coupon(self):
        r = checkout([["lamp", 6000, 1]], "SAVE5")
        self.assertEqual(r["coupon"], 500)
        self.assertEqual(r["net"], 5500)
        r = checkout([["lamp", 3000, 1]], "SAVE5")
        self.assertEqual(r["coupon"], 0)
        r = checkout([["tv", 30000, 1]], "SAVE20")
        self.assertEqual(r["coupon"], 2000)
        with self.assertRaises(PricingError):
            checkout([["lamp", 3000, 1]], "BOGUS")

    def test_tax(self):
        self.assertEqual(tax_on(0), 0)
        self.assertEqual(tax_on(1000), 83)
        self.assertEqual(tax_on(999), 82)
        self.assertEqual(tax_on(12345), 1018)

    def test_validation(self):
        for cart in ([], [["a", 1, 0]], [["a", -1, 1]], [["a", 1, 1], ["a", 2, 1]]):
            with self.assertRaises(PricingError):
                checkout(cart)

    def test_split_payment(self):
        self.assertEqual(split_payment(1000, 3), [334, 333, 333])
        self.assertEqual(split_payment(9, 3), [3, 3, 3])
        with self.assertRaises(PricingError):
            split_payment(10, 0)


if __name__ == "__main__":
    unittest.main()
