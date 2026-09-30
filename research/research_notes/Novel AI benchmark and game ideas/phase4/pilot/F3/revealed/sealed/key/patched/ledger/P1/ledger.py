"""A small in-memory ledger of integer-cent accounts."""

HOUSE = "__house__"


class LedgerError(ValueError):
    pass


class InsufficientFunds(LedgerError):
    pass


class UnknownAccount(LedgerError):
    pass


def _check_name(name):
    if not isinstance(name, str) or not name or name == HOUSE:
        raise LedgerError("invalid account name")


def _check_amount(cents, allow_zero=False):
    if not isinstance(cents, int) or isinstance(cents, bool):
        raise LedgerError("amount must be an int")
    if cents < 0 or (cents == 0 and not allow_zero):
        raise LedgerError("amount out of range")


class Ledger:
    def __init__(self):
        self._bal = {HOUSE: 0}
        self._log = []

    def _get(self, name):
        if name not in self._bal or name == HOUSE:
            raise UnknownAccount(name)
        return self._bal[name]

    def open(self, name, cents=0):
        _check_name(name)
        _check_amount(cents, allow_zero=True)
        if name in self._bal:
            raise LedgerError("account exists")
        self._bal[name] = cents
        self._log.append(("open", name, cents))

    def deposit(self, name, cents):
        _check_amount(cents)
        self._get(name)
        self._bal[name] += cents
        self._log.append(("deposit", name, cents))

    def transfer(self, src, dst, cents):
        _check_amount(cents)
        bal = self._get(src)
        self._get(dst)
        if cents > bal:
            raise InsufficientFunds(src)
        if src == dst:
            raise LedgerError("self transfer")
        self._bal[src] -= cents
        self._bal[dst] += cents
        self._log.append(("transfer", src, dst, cents))

    def fee_shares(self, names, fee):
        """Return {name: cents} for splitting `fee` across `names`."""
        payers = sorted(names)
        n = len(payers)
        base, rem = fee // n, fee % n
        shares = {}
        for i, name in enumerate(payers):
            shares[name] = base + (1 if i < rem else 0)
        return shares

    def split_fee(self, names, fee):
        _check_amount(fee, allow_zero=True)
        if not isinstance(names, list) or not names:
            raise LedgerError("need at least one payer")
        if len(set(names)) != len(names):
            raise LedgerError("duplicate payer")
        for name in names:
            self._get(name)
        shares = self.fee_shares(names, fee)
        for name, share in shares.items():
            if self._bal[name] < share:
                raise InsufficientFunds(name)
        for name, share in shares.items():
            self._bal[name] -= share
            self._bal[HOUSE] += share
        self._log.append(("fee", tuple(sorted(names)), fee))
        return shares

    def balance(self, name):
        if name == HOUSE:
            return self._bal[HOUSE]
        return self._get(name)

    def total(self):
        return sum(self._bal.values())

    def history(self):
        return [list(entry) for entry in self._log]
