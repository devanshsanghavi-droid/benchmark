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
