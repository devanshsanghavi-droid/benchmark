"""The ride-generator contract.

Everything another component may rely on lives in this file: the query a generator
answers, the ride records it returns, and the abstract base class. Other components
(ride-time estimator, pricing, orchestrator) import only these types, never a concrete
generator, so generators can be swapped or compared without touching anything else.
"""
from __future__ import annotations

import abc
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Any


@dataclass(frozen=True)
class Place:
    """A real-world point where a ride starts or ends."""

    lat: float
    lon: float
    zone_id: int | None = None          # NYC TLC taxi zone, when known
    name: str | None = None             # e.g. business name
    category: str | None = None         # e.g. "restaurant", "corporate_or_business_office"
    place_id: str | None = None         # id in the source dataset (e.g. Overture)
    address: str | None = None


@dataclass(frozen=True)
class RideQuery:
    """'Generate the rides that start near this location in this time window.'

    Times are naive local New York time. ``start`` carries the date, which matters
    because demand differs by weekday, holiday and (later) date-specific events.
    """

    lat: float
    lon: float
    start: datetime
    duration: timedelta = timedelta(hours=1)
    radius_m: float = 1000.0

    @property
    def end(self) -> datetime:
        return self.start + self.duration

    def key(self) -> str:
        """Stable text form, used to derive per-query random streams."""
        return (f"{self.lat:.6f},{self.lon:.6f},{self.start.isoformat()},"
                f"{int(self.duration.total_seconds())},{self.radius_m:.1f}")


@dataclass(frozen=True)
class Ride:
    """One ride request. No route, duration or price: those belong to other components."""

    ride_id: str
    request_time: datetime
    origin: Place
    destination: Place
    ride_type: str                       # e.g. "commercial_to_commercial"
    generator: str                       # name of the implementation that produced it
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["request_time"] = self.request_time.isoformat()
        return d


class RideGenerator(abc.ABC):
    """Base class for every ride-generator implementation.

    Contract:
      * ``generate`` returns rides whose origin is within ``query.radius_m`` of the query
        point and whose request time is in ``[query.start, query.end)``, sorted by time.
      * Same generator configuration + same query + same seed -> identical output.
      * Implementations must not read global random state or the wall clock.
    """

    #: unique, versioned implementation name, e.g. "commercial_to_commercial/tlc_overture_v1"
    name: str = "abstract"
    #: ride types this implementation can produce
    ride_types: tuple[str, ...] = ()

    @abc.abstractmethod
    def generate(self, query: RideQuery, seed: int) -> list[Ride]:
        raise NotImplementedError

    def describe(self) -> dict[str, Any]:
        """Human-readable summary of the implementation's assumptions (for logs)."""
        return {"name": self.name, "ride_types": list(self.ride_types)}
