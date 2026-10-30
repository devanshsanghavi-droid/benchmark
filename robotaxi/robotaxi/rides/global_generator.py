"""GlobalRideGenerator: owns one generator per ride type and merges their output.

It sees only the RideGenerator interface. Each child gets its own random stream,
derived from the run seed and the child's name, so adding or removing one ride type
never changes the rides another type produces.
"""
from __future__ import annotations

from .interface import Ride, RideGenerator, RideQuery
from .seeding import rng_for


class GlobalRideGenerator(RideGenerator):
    name = "global"

    def __init__(self, generators: list[RideGenerator]):
        names = [g.name for g in generators]
        if len(set(names)) != len(names):
            raise ValueError(f"duplicate generator names: {names}")
        self.generators = list(generators)
        self.ride_types = tuple(t for g in generators for t in g.ride_types)

    def generate(self, query: RideQuery, seed: int) -> list[Ride]:
        rides: list[Ride] = []
        for g in self.generators:
            child_seed = int(rng_for(seed, "global", g.name).integers(0, 2**31 - 1))
            rides.extend(g.generate(query, child_seed))
        return sorted(rides, key=lambda r: (r.request_time, r.ride_id))

    def describe(self) -> dict:
        return {"name": self.name, "children": [g.describe() for g in self.generators]}
