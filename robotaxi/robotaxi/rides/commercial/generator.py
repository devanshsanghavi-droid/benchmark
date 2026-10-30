"""Commercial-to-commercial rides in Manhattan, grounded in real data (v1).

Generation rule (DECISIONS.md D4-D11):
  1. How many rides start in each taxi zone, each hour: the real average number of
     Manhattan-internal yellow-taxi trips from that zone on that day type and hour
     (TLC, Apr + Oct 2019), times ``c2c_share`` and ``demand_scale``, times the share of
     the zone's commercial places that lie inside the query circle.
  2. Ride counts are Poisson; request times are uniform within each hour.
  3. Destination zone: drawn from the real trip records' destination mix for that
     origin zone, day type and hour.
  4. Exact pickup and drop-off points: real commercial places (Overture Maps), chosen
     inside the origin zone's part of the circle and inside the destination zone.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path

import numpy as np

from ..calendar import day_type
from ..interface import Place, Ride, RideGenerator, RideQuery
from ..seeding import rng_for
from .config import CommercialConfig

RIDE_TYPE = "commercial_to_commercial"
EARTH_R = 6_371_000.0


@dataclass
class _Data:
    lat: np.ndarray
    lon: np.ndarray
    zone: np.ndarray
    place_id: list[str]
    name: list[str]
    category: list[str]
    address: list[str]
    zone_places: dict[int, np.ndarray]                       # zone -> place indices
    od: dict[tuple[str, int, int], tuple[np.ndarray, np.ndarray]]  # (day_type, hour, pu) -> (do zones, trips/day)
    zone_names: dict[int, str]


@lru_cache(maxsize=4)
def _load(data_dir: Path) -> _Data:
    lat, lon, zone, pid, name, cat, addr = [], [], [], [], [], [], []
    with gzip.open(data_dir / "places_commercial.csv.gz", "rt", newline="") as f:
        for r in csv.DictReader(f):
            lat.append(float(r["lat"])); lon.append(float(r["lon"])); zone.append(int(r["zone_id"]))
            pid.append(r["place_id"]); name.append(r["name"]); cat.append(r["basic_category"] or r["top_category"])
            addr.append(r["address"])
    zone_arr = np.array(zone)
    zone_places = {int(z): np.flatnonzero(zone_arr == z) for z in np.unique(zone_arr)}
    rows: dict[tuple[str, int, int], tuple[list[int], list[float]]] = {}
    with gzip.open(data_dir / "od_rates_yellow2019.csv.gz", "rt", newline="") as f:
        for r in csv.DictReader(f):
            k = (r["day_type"], int(r["hour"]), int(r["pu_zone"]))
            dz, w = rows.setdefault(k, ([], []))
            dz.append(int(r["do_zone"])); w.append(float(r["trips_per_day"]))
    od = {k: (np.array(dz), np.array(w)) for k, (dz, w) in rows.items()}
    zone_names = {ft["properties"]["zone_id"]: ft["properties"]["name"]
                  for ft in json.load(open(data_dir / "zones_manhattan.geojson"))["features"]}
    return _Data(np.array(lat), np.array(lon), zone_arr, pid, name, cat, addr, zone_places, od, zone_names)


def _haversine_m(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp, dl = p2 - p1, np.radians(lon2) - np.radians(lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * EARTH_R * np.arcsin(np.sqrt(a))


def _hour_segments(start: datetime, end: datetime):
    """Split [start, end) at hour boundaries: yields (segment start, segment end)."""
    t = start
    while t < end:
        nxt = min(end, t.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
        yield t, nxt
        t = nxt


class CommercialToCommercialGenerator(RideGenerator):
    name = "commercial_to_commercial/tlc_overture_v1"
    ride_types = (RIDE_TYPE,)

    def __init__(self, config: CommercialConfig | None = None):
        self.cfg = config or CommercialConfig()
        self.data = _load(self.cfg.data_dir)
        w = self.cfg.category_weight
        self._w = np.array([w.get(c, 1.0) for c in self.data.category]) if w else np.ones(len(self.data.category))

    def describe(self) -> dict:
        d = super().describe()
        d.update({"config": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(self.cfg).items()},
                  "places": len(self.data.place_id), "zones": len(self.data.zone_places)})
        return d

    # ------------------------------------------------------------------------------------
    def _pick(self, rng: np.random.Generator, idx: np.ndarray) -> int:
        w = self._w[idx]
        return int(idx[rng.choice(len(idx), p=w / w.sum())])

    def _place(self, i: int) -> Place:
        d = self.data
        return Place(lat=float(d.lat[i]), lon=float(d.lon[i]), zone_id=int(d.zone[i]), name=d.name[i],
                     category=d.category[i], place_id=d.place_id[i], address=d.address[i] or None)

    def generate(self, query: RideQuery, seed: int) -> list[Ride]:
        d, cfg = self.data, self.cfg
        rng = rng_for(seed, self.name, query.key())
        dist = _haversine_m(query.lat, query.lon, d.lat, d.lon)
        inside = np.flatnonzero(dist <= query.radius_m)
        if inside.size == 0:
            return []
        in_zone = {int(z): inside[d.zone[inside] == z] for z in np.unique(d.zone[inside])}
        share = {z: self._w[idx].sum() / self._w[d.zone_places[z]].sum() for z, idx in in_zone.items()}

        drafts = []
        for a, b in _hour_segments(query.start, query.end):
            dt, h, secs = day_type(a.date(), cfg.holiday_profile), a.hour, (b - a).total_seconds()
            for z in sorted(in_zone):
                row = d.od.get((dt, h, z))
                if row is None:
                    continue
                dz, trips = row
                expected = trips.sum() * cfg.c2c_share * cfg.demand_scale * share[z] * secs / 3600.0
                for _ in range(rng.poisson(expected)):
                    t = a + timedelta(seconds=float(rng.uniform(0, secs)))
                    o = self._pick(rng, in_zone[z])
                    dest_zone = int(dz[rng.choice(len(dz), p=trips / trips.sum())])
                    for attempt in range(cfg.max_resample):
                        dst = self._pick(rng, d.zone_places[dest_zone])
                        km = float(_haversine_m(d.lat[o], d.lon[o], d.lat[dst], d.lon[dst]))
                        if km >= cfg.min_trip_m:
                            break
                    drafts.append((t, o, dst, dest_zone, dt, km, attempt))

        drafts.sort(key=lambda x: (x[0], x[1], x[2]))
        qid = hashlib.sha256(query.key().encode()).hexdigest()[:8]
        rides = []
        for n, (t, o, dst, dest_zone, dt, km, attempt) in enumerate(drafts):
            rides.append(Ride(
                ride_id=f"c2c-{seed}-{qid}-{n:05d}", request_time=t, origin=self._place(o),
                destination=self._place(dst), ride_type=RIDE_TYPE, generator=self.name,
                meta={"day_type": dt, "straight_line_m": round(km), "origin_zone_name": d.zone_names.get(int(d.zone[o])),
                      "dest_zone_name": d.zone_names.get(dest_zone), "too_short_after_resampling": km < cfg.min_trip_m}))
        return rides
