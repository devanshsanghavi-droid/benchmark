# Decision log

Kept by Devansh Sanghavi ([@devanshsanghavi-droid](https://github.com/devanshsanghavi-droid)).

Newest at the bottom. Each entry: the decision, why, and what would change it.
Constants live in `robotaxi/rides/commercial/config.py`; this file explains them.

## D1 (30 Oct 2026). Scope: Manhattan only, one ride type

**Decision.** Build only commercial-to-commercial rides, only in Manhattan.

**Why.**
- The meeting asked for one small area and one ride type, to learn how to generate plausible rides before expanding.
- Manhattan matches our NYC research and the public TLC trip data.

## D2. Language and structure

**Decision.**
- Python 3.11 with numpy only at run time.
- Data preparation (duckdb, pyarrow, shapely) is a separate, one-off script.
- Every generator implements `RideGenerator` in `robotaxi/rides/interface.py` and is registered by a versioned name in `registry.py`.
- `GlobalRideGenerator` sees only that interface.

**Why.**
- Python is the team's data stack.
- A tiny run-time dependency set keeps the generator easy to embed in the simulator.
- The registry lets several implementations coexist and be compared. A new version gets a new name rather than editing the old one.

## D3. Data sources and access

**Decision.** Three sources:
- **NYC TLC yellow-taxi trip records:** pickup and drop-off zone and time.
- **TLC taxi zones:** polygons and lookup table.
- **Overture Maps places:** real business locations, release `2026-10-21.0`.

**Why.**
- All three are public and free.
- TLC data says *when* and *between which areas* real trips happen.
- Overture says *where exactly* real businesses are.

**Caveats.**
- The official NYC hosts (nyc.gov, the TLC CloudFront server, NYC Open Data) were blocked by this environment's network policy. The TLC files were taken from the DataTalksClub GitHub copy of the official files, and the zone polygons from a GeoJSON conversion of the official shapefile hosted on GitHub.
- Official URLs are recorded in `data_prep/build_commercial_v1.py` and `MANIFEST.json`, so we can switch to them once those hosts are allowed.

## D4. Demand data: yellow taxi, April + October 2019

**Decision.** Use yellow-taxi trips from April and October 2019, keeping only those that start and end in Manhattan.

**Why.**
- The reachable copy has only pre-2022 yellow and green files, plus one COVID-era app (HVFHV) month.
- 2019 is the last normal pre-COVID year.
- April and October avoid summer and holiday seasons.
- Yellow taxis cover Manhattan well: about 89% of yellow pickups are in the Manhattan core.

**Limits.**
- It misses Uber and Lyft trips, so absolute volume is too low (see D7).
- Northern Manhattan is under-represented, because yellow cabs rarely serve it. Washington Heights gets almost no rides.
- Pre-COVID office patterns may overstate weekday office demand compared with 2026.

**Change when.** Official TLC HVFHV (app) files for a recent year are reachable. Rebuild the OD file from them, or from yellow plus HVFHV combined.

**Other details.**
- Columbus Day (14 Oct 2019) is dropped so that "weekday" means an ordinary working day.
- Trips with zero or negative duration, or longer than 3 hours, are dropped.

## D5. What counts as a commercial place

**Decision.**
- Keep Overture places whose top category is one of:
  - food_and_drink;
  - shopping;
  - services_and_business;
  - lifestyle_services;
  - arts_and_entertainment;
  - lodging.
- Require operating status open (or blank) and confidence of at least 0.5.
- Drop these fine categories: atm, parking, home_service, storage, EV charging, gas station, shipping.

**Why.**
- These match "restaurant, movie, services" in the brainstorm.
- Healthcare, education, government and transit hubs are their own future ride types.

**Effect.** 112,516 places in 66 zones.

**Known issue.** Overture contains some mislocated or odd records found during inspection, for example "Trump Plaza Hotel and Casino" placed in Highbridge Park, and a "condominium" category. Raising the confidence floor or adding a deny-list are options.

## D6. Share of trips that are commercial-to-commercial: PLACEHOLDER 0.30

**Decision.** Rides of this type = 30% of real Manhattan-internal taxi trips, the same share for every zone and hour.

**Why.** Public trip records have no trip purpose, so we have no data for this yet. Hour-of-day and zone-to-zone variation still come from real trips.

**This is the main open question for the next sync.** Ways to ground it:
- **Endpoint land use:** a commercial share per zone pair from land use at both ends (PLUTO lot land use, or Overture buildings).
- **Travel surveys:** NYC or regional surveys that record trip purpose (e.g. NYMTC / RHTS).
- **Classify each real trip:** label the trip as commercial or not from its pickup and drop-off land use, once exact points are available. TLC zone data does not have them, so this would need another source.

## D7. Demand scale 1.0 = 2019 yellow-taxi level

**Decision.** Keep a single multiplier, `demand_scale`, starting at 1.0.

**Why.** It keeps one knob for matching total demand once app trips are included.

## D8. Holidays use the Sunday profile

**Decision.** US federal holidays use the Sunday demand profile.

**Why.** Holidays look more like weekends than workdays. The rule is simple and adjustable. Date-specific events are a separate future ride type.

## D9. Minimum trip length 300 m

**Decision.** If the drop-off place is within 300 m of the pickup, resample it, up to 20 times. A ride that is still too short is kept and flagged in `meta`.

**Why.** Same-zone trips are common in the data, but two places in the same building are not a taxi trip.

## D10. Exact points are uniform over real commercial places

**Decision.** Within a zone, pickup and drop-off points are chosen uniformly over its commercial places. The per-category weights in config are all 1.0.

**Why.**
- It is the simplest grounded choice.
- Blocks with many businesses (office towers) naturally get more rides.

**Known issue.** Opening hours are ignored, so offices appear as pickups at 3 am. Fixing it needs a time-of-day weight per category group, which in turn needs a data source or a team decision.

## D11. Matching demand to the query circle

**Decision.** A zone's hourly demand is scaled by the share of its commercial places that lie inside the query circle. Origins are drawn only from places inside the circle.

**Why.**
- It keeps totals consistent: circles that tile Manhattan add up to the zone totals.
- It needs no finer data than taxi zones.

## D12. Reproducibility

**Decision.**
- Every random draw comes from a numpy Generator seeded by (run seed, generator name, query).
- The names are hashed with SHA-256, not Python's salted `hash`.
- `GlobalRideGenerator` gives each child generator its own stream, so adding a ride type never changes another type's rides.

**Covered by tests.** The tests check:
- the same seed gives the same rides;
- a fresh instance gives the same rides;
- different seeds give different rides;
- each child generator is isolated from the others.
