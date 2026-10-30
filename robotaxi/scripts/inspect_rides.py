"""Manual inspection of generated rides (the first 'test': look, don't auto-judge).

Samples query locations and times, runs a generator, and writes:
  * a printed table of example rides per query and summary counts,
  * a 24-hour profile (rides per hour) for each location on a weekday and a Saturday,
  * rides.csv, and map.html (open in a browser: pickups green, drop-offs red, lines between).

    python scripts/inspect_rides.py --out out/inspect --seed 1
    python scripts/inspect_rides.py --lat 40.7484 --lon -73.9857 --when 2026-11-06T18:00 --minutes 60
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from robotaxi.rides.global_generator import GlobalRideGenerator  # noqa: E402
from robotaxi.rides.interface import RideQuery  # noqa: E402
from robotaxi.rides.registry import available, create  # noqa: E402

# Hand-picked spots plus random ones, so both familiar and arbitrary places get looked at.
LANDMARKS = {
    "Times Square": (40.7580, -73.9855),
    "Grand Central": (40.7527, -73.9772),
    "Financial District": (40.7075, -74.0113),
    "SoHo": (40.7233, -74.0030),
    "Upper West Side": (40.7870, -73.9754),
    "Harlem 125th St": (40.8090, -73.9482),
    "Washington Heights": (40.8417, -73.9394),
}
TIMES = ["08:30", "12:30", "18:00", "23:00", "03:00"]


def ride_rows(rides):
    for r in rides:
        yield {"ride_id": r.ride_id, "time": r.request_time.isoformat(timespec="seconds"),
               "origin": r.origin.name, "origin_cat": r.origin.category, "origin_zone": r.meta.get("origin_zone_name"),
               "o_lat": r.origin.lat, "o_lon": r.origin.lon,
               "dest": r.destination.name, "dest_cat": r.destination.category, "dest_zone": r.meta.get("dest_zone_name"),
               "d_lat": r.destination.lat, "d_lon": r.destination.lon, "straight_line_m": r.meta.get("straight_line_m"),
               "day_type": r.meta.get("day_type")}


def write_map(path: Path, groups: list[tuple[str, RideQuery, list]]) -> None:
    colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666"]
    layers = []
    for i, (label, q, rides) in enumerate(groups):
        layers.append({"label": f"{label} ({len(rides)} rides)", "color": colors[i % len(colors)],
                       "center": [q.lat, q.lon], "radius": q.radius_m,
                       "rides": [[r.origin.lat, r.origin.lon, r.destination.lat, r.destination.lon,
                                  html.escape(f"{r.request_time:%a %H:%M} | {r.origin.name} ({r.origin.category}) -> "
                                              f"{r.destination.name} ({r.destination.category}), {r.meta.get('straight_line_m')} m")]
                                 for r in rides]})
    path.write_text(f"""<!doctype html><html><head><meta charset="utf-8"><title>Generated rides</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>html,body,#m{{height:100%;margin:0}}</style></head><body><div id="m"></div><script>
const L_=L, m=L.map('m').setView([40.765,-73.975],13);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'&copy; OpenStreetMap'}}).addTo(m);
const groups={json.dumps(layers)}, overlays={{}};
for (const g of groups) {{
  const lg=L.layerGroup();
  L.circle(g.center,{{radius:g.radius,color:g.color,fill:false,dashArray:'4'}}).addTo(lg);
  for (const [a,b,c,d,t] of g.rides) {{
    L.polyline([[a,b],[c,d]],{{color:g.color,weight:1,opacity:.5}}).bindTooltip(t).addTo(lg);
    L.circleMarker([a,b],{{radius:3,color:'green'}}).bindTooltip(t).addTo(lg);
    L.circleMarker([c,d],{{radius:3,color:'red'}}).bindTooltip(t).addTo(lg);
  }}
  lg.addTo(m); overlays[g.label]=lg;
}}
L.control.layers(null,overlays,{{collapsed:false}}).addTo(m);
</script></body></html>""")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--generator", default="commercial_to_commercial/tlc_overture_v1", choices=available())
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="out/inspect")
    ap.add_argument("--date", default="2026-11-04", help="weekday date used for the sampled times (YYYY-MM-DD)")
    ap.add_argument("--random-points", type=int, default=3)
    ap.add_argument("--radius", type=float, default=600)
    ap.add_argument("--minutes", type=int, default=30)
    ap.add_argument("--lat", type=float); ap.add_argument("--lon", type=float); ap.add_argument("--when")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    gen = GlobalRideGenerator([create(a.generator)])
    print(json.dumps(gen.describe(), indent=1, default=str))

    if a.lat is not None:
        queries = [(f"custom @ {a.when}", RideQuery(a.lat, a.lon, datetime.fromisoformat(a.when),
                                                    timedelta(minutes=a.minutes), a.radius))]
    else:
        child = gen.generators[0]
        rng = np.random.default_rng(a.seed)
        spots = dict(LANDMARKS)
        for i in range(a.random_points):  # random real commercial places as query centres
            j = int(rng.integers(len(child.data.lat)))
            spots[f"random #{i + 1} ({child.data.zone_names[int(child.data.zone[j])]})"] = (float(child.data.lat[j]), float(child.data.lon[j]))
        day = datetime.fromisoformat(a.date)
        queries = []
        for label, (lat, lon) in spots.items():
            t = TIMES[int(rng.integers(len(TIMES)))]
            when = datetime.fromisoformat(f"{day:%Y-%m-%d}T{t}")
            queries.append((f"{label} @ {when:%a %H:%M}", RideQuery(lat, lon, when, timedelta(minutes=a.minutes), a.radius)))

    groups, all_rows = [], []
    for label, q in queries:
        rides = gen.generate(q, a.seed)
        groups.append((label, q, rides))
        rows = list(ride_rows(rides)); all_rows += [{"query": label, **r} for r in rows]
        print(f"\n=== {label}: {len(rides)} rides within {q.radius_m:.0f} m in {q.duration} ===")
        for r in rows[:10]:
            print(f"  {r['time'][11:19]}  {r['origin'][:30]:30} ({r['origin_cat'][:22]:22}) -> "
                  f"{r['dest'][:30]:30} ({r['dest_cat'][:22]:22}) {r['dest_zone'][:22]:22} {r['straight_line_m']:>6} m")
        if rides:
            m = np.array([r["straight_line_m"] for r in rows])
            print(f"  straight-line distance m: median {np.median(m):.0f}, p10 {np.percentile(m, 10):.0f}, p90 {np.percentile(m, 90):.0f}")
            print("  top origin categories:", Counter(r["origin_cat"] for r in rows).most_common(5))
            print("  top destination zones:", Counter(r["dest_zone"] for r in rows).most_common(5))

    # Timing pattern: rides per hour over a full weekday and Saturday for the first two spots.
    print("\n=== Rides per hour (radius %.0f m), weekday vs Saturday ===" % a.radius)
    wd = datetime.fromisoformat(a.date).replace(hour=0, minute=0)
    sat = wd + timedelta(days=(5 - wd.weekday()) % 7)
    for label, q in queries[:2]:
        for day0 in (wd, sat):
            counts = Counter(r.request_time.hour for r in gen.generate(
                RideQuery(q.lat, q.lon, day0, timedelta(hours=24), q.radius_m), a.seed))
            print(f"  {label.split(' @')[0][:20]:20} {day0:%a}: " + " ".join(f"{counts.get(h, 0):3d}" for h in range(24)))
    print("  hours:                    " + " ".join(f"{h:3d}" for h in range(24)))

    if all_rows:
        with open(out / "rides.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(all_rows[0])); w.writeheader(); w.writerows(all_rows)
    write_map(out / "map.html", groups)
    print(f"\nwrote {out / 'rides.csv'} and {out / 'map.html'}")


if __name__ == "__main__":
    main()
