# Spec: `ledger`

`ledger.Ledger` keeps integer-cent balances for named accounts plus one built-in house account named `"__house__"`. All exceptions below are named by class; raising any subclass of the named class also satisfies the rule. Exception messages are unspecified.

**Domain.** Account names are non-empty strings of at most 20 characters. Amounts are Python `int` values with absolute value at most 10**9. Behaviour on other argument types is unspecified.

| Rule | Statement |
|---|---|
| L1 | `open(name, cents=0)`: creates an account with balance `cents`. Raises `LedgerError` if `name` is `"__house__"`, `cents < 0`, or the account already exists. |
| L2 | `deposit(name, cents)`: adds `cents` to the account. Raises `LedgerError` if `cents <= 0` and `UnknownAccount` if the account does not exist or is the house account. |
| L3 | `transfer(src, dst, cents)`: moves `cents` from `src` to `dst`. Raises `LedgerError` if `cents <= 0` or `src == dst`; `UnknownAccount` if either account does not exist (the house account cannot be named); `InsufficientFunds` if `balance(src) < cents`. When several of these conditions hold at once, any one of the listed exceptions may be raised. |
| L4 | `split_fee(names, fee)`: `names` is a non-empty list of distinct existing account names (not the house account); `fee >= 0`. Otherwise raises `LedgerError` (`UnknownAccount` for a missing account). |
| L5 | Fee shares: let `n = len(names)`, `q, r = divmod(fee, n)`. Sort `names` in ascending Python string order. The first `r` names in that order pay `q + 1` cents; the rest pay `q` cents. `split_fee` returns a dict mapping every payer to its share; dict ordering is unspecified. `fee_shares(names, fee)` returns the same dict without changing any state; it is only defined for a non-empty list of distinct names and `fee >= 0` (account existence is not checked). |
| L6 | Shares are debited from the payers and the full `fee` is credited to `"__house__"`. |
| L7 | Atomicity: if any payer's balance is less than its share, `split_fee` raises `InsufficientFunds` and no balance changes. More generally, every method that raises leaves all balances and the history unchanged. |
| L8 | Balances are never negative. |
| L9 | Conservation: `total()` equals the sum of all balances including the house account, and it changes only through `open` (by `cents`) and `deposit` (by `cents`). |
| L10 | `balance(name)` returns the balance; `balance("__house__")` is allowed. Raises `UnknownAccount` for a missing account. |
| L11 | `history()` returns one entry per successful state-changing call, oldest first: `["open", name, cents]`, `["deposit", name, cents]`, `["transfer", src, dst, cents]`, `["fee", sorted_names, fee]` (where `sorted_names` is a list). Failed calls add nothing. |

## Witness format

A witness is a JSON object `{"ops": [...]}` with at most 60 operations. A fresh `Ledger()` is created, then each operation `[method, arg1, arg2, ...]` is called in order. `method` is one of `open`, `deposit`, `transfer`, `split_fee`, `fee_shares`, `balance`, `total`, `history`. Exceptions are recorded and execution continues with the next operation. Example: `{"ops": [["open", "a", 5], ["split_fee", ["a"], 2], ["balance", "a"]]}`.
