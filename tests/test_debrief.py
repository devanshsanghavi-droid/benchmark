import random

from debrief.core import (MISCONCEPTIONS, diagnose, live_misconceptions, make_item, nfr, parse_answers,
                          parse_note, price, sensitive, template_coach_note)


def test_items_deterministic_and_covered():
    for level in (1, 2, 3):
        a, b = make_item(7, level), make_item(7, level)
        assert a.to_json() == b.to_json()
        for m in live_misconceptions(a.system):
            assert sum(sensitive(a.system, c, m) for c in a.fresh) >= 2, m


def test_misconceptions_only_live_when_provision_present():
    item = make_item(3, 1)
    live = live_misconceptions(item.system)
    for m in MISCONCEPTIONS:
        if m not in live:
            assert all(price(item.system, c, frozenset([m])) == price(item.system, c) for c in item.fresh)


def test_mutation_search_recovers_planted_misconceptions():
    hits = 0
    for seed in range(20):
        item = make_item(100 + seed, 2)
        live = [m for m in live_misconceptions(item.system) if m != "vol_on_docs"]
        planted = frozenset(random.Random(seed).sample(live, 2))
        answers = {c.cid: price(item.system, c, planted) for c in item.practice}
        s, n, _ = diagnose(item, answers)
        assert n == len(item.practice)  # always fully explains noise-free answers
        hits += s == planted
    assert hits >= 14  # exact recovery in most cases (others are observationally equivalent on practice)


def test_template_coach_respects_budget():
    item = make_item(5, 3)
    answers = {c.cid: price(item.system, c, frozenset(["no_vol"])) for c in item.practice}
    note = template_coach_note(item, answers, budget=150)
    assert len(note.split()) <= 150 and "volumetric" in note.lower()


def test_nfr_math():
    assert nfr([[0, 0, 1]], [[1, 0, 1]]) == 50.0
    assert nfr([[0, 1]], [[0, 0]]) == -100.0
    assert nfr([[0.5, 0.5]], [[1, 0.5]]) == 50.0


def test_parsers():
    txt = "reasoning...\n**F1**: 1,450\nF2: 990\nF1: 1500"
    assert parse_answers(txt) == {"F1": 1500, "F2": 990}
    assert parse_note("x <note> a b c d </note> y", 2) == "a b"


# --- v0.2 (L4-L5) provisions: hand-computed cases ---------------------------------------------
def _sys5():
    from debrief.core import System, LEVEL_PROVISIONS
    return System(seed=0, level=5, name="T", provisions=list(LEVEL_PROVISIONS[5]),
                  first={"A": 400, "B": 600, "C": 900}, per={"A": 100, "B": 200, "C": 250}, divisor=5000,
                  weekend_pct=20, remote_prefixes=["KX"], remote_fee=300, gold_pct=10, excl_zone="C", doc_cap=1500,
                  reclass_kg=2, tier_kg=5, tier_add=50, zone_div_zone="B", zone_divisor=2500, oversize_cm=50,
                  oversize_fee=200, minimum=500)


def test_v02_tier_oversize_flat_undiscounted():
    from debrief.core import Case, price
    s = _sys5()
    # Zone A parcel 7.2 kg -> 8 kg (vol 60*55*10/5000 = 6.6 -> 7). base = 400 + 4*100 + 3*150 = 1250.
    # two sides > 50 cm -> oversize 400. Sat: +20% of base = 250. GOLD: 10% of (1250+250) = 150 off; flat 400 + KX 300 kept.
    c = Case("F1", "A", 7.2, (60, 55, 10), "PARCEL", "Sat", "KX4", "GOLD")
    assert price(s, c) == 1250 + 250 - 150 + 400 + 300
    assert price(s, c, frozenset(["oversize_once"])) == 1250 + 250 - 150 + 200 + 300
    assert price(s, c, frozenset(["no_tier"])) == 1100 + 220 - 132 + 400 + 300
    assert price(s, c, frozenset(["tier_all_kg"])) == (400 + 7 * 150) + 290 - 174 + 400 + 300
    assert price(s, c, frozenset(["discount_flat_fees"])) == (1250 + 250 + 700) - (2200 * 10 // 100)


def test_v02_reclass_zone_divisor_minimum():
    from debrief.core import Case, price
    s = _sys5()
    # Zone B DOCUMENT 2.4 kg -> 3 kg > 2 -> treated as PARCEL: vol 40*30*10/2500 = 4.8 -> 5 kg (Zone B divisor 2500).
    d = Case("F2", "B", 2.4, (40, 30, 10), "DOCUMENT", "Mon", "AB1", "STANDARD")
    assert price(s, d) == 600 + 4 * 200
    assert price(s, d, frozenset(["no_zone_div"])) == 600 + 2 * 200        # vol 2.4 -> 3 kg
    assert price(s, d, frozenset(["no_doc_reclass"])) == 600 + 2 * 200     # stays a document: actual 3 kg
    # Zone A light document, GOLD: 400 - 40 = 360 -> minimum 500 applies.
    m = Case("F3", "A", 0.3, (30, 25, 3), "DOCUMENT", "Tue", "AB1", "GOLD")
    assert price(s, m) == 500
    assert price(s, m, frozenset(["no_minimum"])) == 360
