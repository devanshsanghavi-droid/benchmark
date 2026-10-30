"""Mechanical tests of the ride-generator contract. Realism is judged by eye (scripts/inspect_rides.py)."""
from __future__ import annotations

import math
from datetime import date, datetime, timedelta

import pytest

from robotaxi.rides.calendar import day_type, us_federal_holidays
from robotaxi.rides.commercial.config import CommercialConfig
from robotaxi.rides.commercial.generator import CommercialToCommercialGenerator
from robotaxi.rides.global_generator import GlobalRideGenerator
from robotaxi.rides.interface import Place, Ride, RideGenerator, RideQuery
from robotaxi.rides.registry import available, create

NAME = "commercial_to_commercial/tlc_overture_v1"
GRAND_CENTRAL = (40.7527, -73.9772)


@pytest.fixture(scope="module")
def gen():
    return create(NAME)


def q(hour=12, minutes=30, day=date(2026, 11, 4), radius=500, where=GRAND_CENTRAL):
    return RideQuery(where[0], where[1], datetime(day.year, day.month, day.day, hour), timedelta(minutes=minutes), radius)


def dump(rides):
    return [r.to_dict() for r in rides]


def test_registered():
    assert NAME in available()


def test_same_seed_same_rides(gen):
    assert dump(gen.generate(q(), 42)) == dump(gen.generate(q(), 42))


def test_fresh_instance_same_rides(gen):
    assert dump(gen.generate(q(), 42)) == dump(CommercialToCommercialGenerator().generate(q(), 42))


def test_different_seed_differs(gen):
    assert dump(gen.generate(q(), 1)) != dump(gen.generate(q(), 2))


def test_rides_respect_query(gen):
    query = q(hour=17, minutes=45)
    rides = gen.generate(query, 3)
    assert rides, "expected some rides near Grand Central at 5 pm on a weekday"
    times = [r.request_time for r in rides]
    assert times == sorted(times)
    for r in rides:
        assert query.start <= r.request_time < query.end
        dlat = math.radians(r.origin.lat - query.lat)
        dlon = math.radians(r.origin.lon - query.lon) * math.cos(math.radians(query.lat))
        assert 6_371_000 * math.hypot(dlat, dlon) <= query.radius_m + 1
        assert r.ride_type == "commercial_to_commercial"
        assert r.origin.place_id and r.destination.place_id and r.origin.place_id != r.destination.place_id
    assert len({r.ride_id for r in rides}) == len(rides)


def test_far_from_manhattan_is_empty(gen):
    assert gen.generate(q(where=(40.6413, -73.7781)), 1) == []  # JFK: outside this generator's scope


def test_weekday_morning_busier_than_sunday_morning(gen):
    wd = sum(len(gen.generate(q(hour=8, minutes=60, day=date(2026, 11, 4)), s)) for s in range(3))
    sun = sum(len(gen.generate(q(hour=8, minutes=60, day=date(2026, 11, 8)), s)) for s in range(3))
    assert wd > 1.5 * sun


def test_c2c_share_scales_volume():
    lo = CommercialToCommercialGenerator(CommercialConfig(c2c_share=0.1)).generate(q(minutes=60), 5)
    hi = CommercialToCommercialGenerator(CommercialConfig(c2c_share=0.4)).generate(q(minutes=60), 5)
    assert 2.5 < len(hi) / max(len(lo), 1) < 6


class _Dummy(RideGenerator):
    name = "dummy/v1"
    ride_types = ("dummy",)

    def generate(self, query, seed):
        return [Ride(f"d-{seed}", query.start, Place(query.lat, query.lon), Place(query.lat, query.lon), "dummy", self.name)]


def test_global_generator_isolates_children(gen):
    alone = [r for r in GlobalRideGenerator([gen]).generate(q(), 9)]
    mixed = [r for r in GlobalRideGenerator([_Dummy(), gen]).generate(q(), 9) if r.generator == NAME]
    assert dump(alone) == dump(mixed)


def test_calendar():
    assert date(2026, 11, 26) in us_federal_holidays(2026)       # Thanksgiving
    assert day_type(date(2026, 11, 26)) == "sunday"              # holiday -> Sunday profile
    assert day_type(date(2026, 11, 7)) == "saturday"
    assert day_type(date(2026, 11, 4)) == "weekday"
