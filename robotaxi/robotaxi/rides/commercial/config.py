"""Every assumption and constant of the commercial-to-commercial generator, in one place.

Change values here, not in the generator code. Each consequential choice has an entry
in DECISIONS.md (the D-numbers below).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "derived" / "commercial_v1"


@dataclass(frozen=True)
class CommercialConfig:
    data_dir: Path = DATA_DIR

    # D6: share of real Manhattan-internal taxi trips treated as commercial-to-commercial.
    # PLACEHOLDER. Public trip records carry no trip purpose, so this is not grounded in
    # data yet; it is the main open question for the next sync. Hour-of-day and
    # zone-to-zone variation still come from the real trip records.
    c2c_share: float = 0.30

    # D7: overall demand multiplier. 1.0 = the level of 2019 yellow-taxi trips. App
    # (Uber/Lyft) trips are not in this data, so real total demand is higher.
    demand_scale: float = 1.0

    # D8: which day-type profile a US federal holiday uses.
    holiday_profile: str = "sunday"

    # D9: minimum distance between pickup and drop-off places (metres). Trips shorter
    # than this are resampled (real taxi trips this short are rare and usually walks).
    min_trip_m: float = 300.0
    max_resample: int = 20

    # D10: relative weight of each place category when choosing the exact point inside a
    # zone. 1.0 for everything = uniform over real commercial places (dense blocks with
    # many businesses get proportionally more pickups). Unlisted categories use 1.0.
    category_weight: dict[str, float] = field(default_factory=dict)

    # D11: how origins are matched to the query circle: a zone's demand is scaled by the
    # fraction of its commercial places that fall inside the circle.
    zone_share_by: str = "places"
