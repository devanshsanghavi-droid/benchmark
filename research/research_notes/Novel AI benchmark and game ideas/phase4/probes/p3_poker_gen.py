"""Probe for C33 Exploitability Gauntlet: a random Kuhn-family game. Prints rules only (writes params to a json)."""
import os, random, json
HERE=os.path.dirname(os.path.abspath(__file__))
rng=random.Random(int.from_bytes(os.urandom(4),'big'))
N=rng.choice([5,6,7]); b=rng.choice([1,2,3]); ante=1
json.dump({"N":N,"b":b,"ante":ante}, open(os.path.join(HERE,"p3_params.json"),"w"))
print(f"Deck: cards 1..{N}, one of each. Each of two players antes {ante} and is dealt one private card (no replacement).")
print(f"P1 acts first: CHECK or BET {b}.")
print(f" - If P1 checks, P2 may CHECK (showdown) or BET {b}; if P2 bets, P1 may FOLD (P2 wins pot) or CALL (showdown).")
print(f" - If P1 bets, P2 may FOLD (P1 wins pot) or CALL (showdown).")
print("Showdown: higher card wins the pot. Report a behavioural strategy for both seats: probabilities per card at each decision point.")
