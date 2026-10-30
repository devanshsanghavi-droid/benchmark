# RoboTaxi Bench: ride generator (first method)

First component of the simulator: the **GlobalRideGenerator**, with one real-data-grounded ride type, **commercial-to-commercial rides in Manhattan**.

Out of scope here:
- routing and ride-time estimates;
- pricing;
- other ride types.

## How it works (v1)

Ask: *"what rides start near (lat, lon) in this time window on this date?"*
1. **How many.** Real 2019 NYC yellow-taxi trips give the average number of Manhattan-internal trips from each taxi zone, by day type (weekday, Saturday, Sunday/holiday) and hour. A fixed share (`c2c_share`, a placeholder, see DECISIONS D6) counts as commercial-to-commercial. That share is then scaled by how much of the zone's commercial activity falls inside your circle.
2. **When.** Ride counts are Poisson, and request times are uniform within each hour.
3. **Where to.** The destination zone is drawn from where real trips from that zone, day type and hour went.
4. **Exact points.** The pickup and drop-off are real businesses (Overture Maps): restaurants, shops, offices, hotels, venues.

## Use

```python
from datetime import datetime, timedelta
from robotaxi.rides.interface import RideQuery
from robotaxi.rides.registry import create
from robotaxi.rides.global_generator import GlobalRideGenerator

gen = GlobalRideGenerator([create("commercial_to_commercial/tlc_overture_v1")])
rides = gen.generate(RideQuery(40.7527, -73.9772, datetime(2026, 11, 4, 8, 30),
                               timedelta(minutes=30), radius_m=500), seed=1)
```

The same query and seed always produce the same rides.

## Check it by eye (the first test)

```bash
pip install -e .
python scripts/inspect_rides.py --out out/inspect          # landmarks + random spots, fixed weekday
python scripts/inspect_rides.py --lat 40.7484 --lon -73.9857 --when 2026-11-06T18:00 --minutes 60
```

The script prints:
- sample rides;
- the distance spread;
- the top categories and destination zones;
- a 24-hour rides-per-hour profile.

It also writes `rides.csv` and `map.html`. Open the map in a browser: pickups are green, drop-offs red, and hovering shows the details.

Mechanical tests (`pytest`) check:
- reproducibility;
- that rides respect the query;
- isolation between generators.

They do not judge realism.

## Layout

| Path | What |
|---|---|
| `robotaxi/rides/interface.py` | The contract: `RideQuery`, `Ride`, `Place`, `RideGenerator` |
| `robotaxi/rides/registry.py` | Named implementations, so several can be compared |
| `robotaxi/rides/global_generator.py` | Owns one generator per ride type and merges their output |
| `robotaxi/rides/commercial/` | The v1 commercial-to-commercial generator; `config.py` holds every constant |
| `robotaxi/data/derived/commercial_v1/` | Small derived data files (committed) and `MANIFEST.json` with sources and hashes |
| `data_prep/build_commercial_v1.py` | Rebuilds the derived data from the public sources |
| `DECISIONS.md` | Decision log |

## Adding another implementation

Subclass `RideGenerator`, give it a new versioned `name`, and register it in `registry.py`. Then run `inspect_rides.py --generator <name>` to compare.
