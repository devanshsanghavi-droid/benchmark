import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ledger import HOUSE, InsufficientFunds, Ledger, LedgerError, UnknownAccount  # noqa: E402


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.l = Ledger()
        self.l.open("alice", 1000)
        self.l.open("bob", 500)
        self.l.open("carol", 0)

    def test_open_and_balance(self):
        self.assertEqual(self.l.balance("alice"), 1000)
        self.assertEqual(self.l.balance(HOUSE), 0)
        with self.assertRaises(LedgerError):
            self.l.open("alice", 5)
        with self.assertRaises(LedgerError):
            self.l.open(HOUSE, 5)
        with self.assertRaises(UnknownAccount):
            self.l.balance("zed")

    def test_deposit(self):
        self.l.deposit("carol", 25)
        self.assertEqual(self.l.balance("carol"), 25)
        with self.assertRaises(LedgerError):
            self.l.deposit("carol", 0)

    def test_transfer(self):
        self.l.transfer("alice", "carol", 300)
        self.assertEqual(self.l.balance("alice"), 700)
        self.assertEqual(self.l.balance("carol"), 300)

    def test_transfer_insufficient(self):
        with self.assertRaises(InsufficientFunds):
            self.l.transfer("bob", "alice", 501)
        self.assertEqual(self.l.balance("bob"), 500)

    def test_self_transfer(self):
        with self.assertRaises(LedgerError):
            self.l.transfer("alice", "alice", 10)

    def test_split_even(self):
        shares = self.l.split_fee(["alice", "bob"], 200)
        self.assertEqual(shares, {"alice": 100, "bob": 100})
        self.assertEqual(self.l.balance("alice"), 900)
        self.assertEqual(self.l.balance(HOUSE), 200)

    def test_split_uneven_conserves(self):
        before = self.l.total()
        self.l.split_fee(["bob", "alice"], 7)
        self.assertEqual(self.l.total(), before)
        self.assertEqual(self.l.balance(HOUSE), 7)
        self.assertEqual(self.l.balance("alice") + self.l.balance("bob"), 1493)

    def test_split_fee_insufficient_single(self):
        with self.assertRaises(InsufficientFunds):
            self.l.split_fee(["carol"], 1)
        self.assertEqual(self.l.balance("carol"), 0)
        self.assertEqual(self.l.balance(HOUSE), 0)

    def test_split_fee_validation(self):
        with self.assertRaises(LedgerError):
            self.l.split_fee([], 10)
        with self.assertRaises(LedgerError):
            self.l.split_fee(["alice", "alice"], 10)
        with self.assertRaises(UnknownAccount):
            self.l.split_fee(["alice", "zed"], 10)

    def test_history(self):
        self.l.transfer("alice", "bob", 1)
        self.l.split_fee(["bob", "alice"], 4)
        h = self.l.history()
        self.assertEqual(h[-2], ["transfer", "alice", "bob", 1])
        self.assertEqual(list(h[-1][1]), ["alice", "bob"])
        self.assertEqual(len(h), 5)

    def test_total(self):
        self.assertEqual(self.l.total(), 1500)
        self.l.deposit("bob", 5)
        self.assertEqual(self.l.total(), 1505)


if __name__ == "__main__":
    unittest.main()
