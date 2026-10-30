"""Calendar helpers shared by generators: day types and US federal holidays."""
from __future__ import annotations

from datetime import date, timedelta
from functools import lru_cache


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(year: int, month: int, weekday: int) -> date:
    d = date(year + (month == 12), month % 12 + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def _observed(d: date) -> date:
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


@lru_cache(maxsize=None)
def us_federal_holidays(year: int) -> frozenset[date]:
    """Observed US federal holidays (Juneteenth from 2021)."""
    days = {
        _observed(date(year, 1, 1)),
        _nth_weekday(year, 1, 0, 3),     # MLK Day
        _nth_weekday(year, 2, 0, 3),     # Presidents' Day
        _last_weekday(year, 5, 0),       # Memorial Day
        _observed(date(year, 7, 4)),
        _nth_weekday(year, 9, 0, 1),     # Labor Day
        _nth_weekday(year, 10, 0, 2),    # Columbus / Indigenous Peoples' Day
        _observed(date(year, 11, 11)),
        _nth_weekday(year, 11, 3, 4),    # Thanksgiving
        _observed(date(year, 12, 25)),
    }
    if year >= 2021:
        days.add(_observed(date(year, 6, 19)))
    return frozenset(days)


def day_type(d: date, holiday_profile: str = "sunday") -> str:
    """'weekday', 'saturday' or 'sunday'; federal holidays use ``holiday_profile``."""
    if d in us_federal_holidays(d.year):
        return holiday_profile
    return {5: "saturday", 6: "sunday"}.get(d.weekday(), "weekday")
