# R01: Geography, land use and the road network

RoboTaxi Bench simulation variables, domain R01 of 12. Research dossier, October 2026. Default city: New York City.

## 1. Summary

NYC geography is very uneven: in October 2019, 16 of the city's 263 taxi zones produced half of all yellow-cab pickups and 89% came from the 55-zone Manhattan core, while app (HVFHV) pickups needed 60 zones for half and were 59.5% outer-borough (June 2021), so the same map rewards different positioning for a taxi, an app driver and a robotaxi. The biggest geographic profit drivers are where demand concentrates and where drop-offs strand the driver: Brooklyn and the Bronx receive about four yellow drop-offs per pickup, and the share of core trips heading to outer boroughs rises from 1.4% at 8am to 17.7% at 4am. Airports are a high-stakes special case: they were 7.9% of yellow trips but 22.2% of driver revenue, yet holding-lot waits have been reported at 2-3 hours and Newark is drop-off-only for NYC cars. Rules tied to places matter as much as roads: the green-taxi hail exclusion zone, the Congestion Relief Zone (Manhattan at or below 60th St; $0.75 per taxi trip, $1.50 per HVFHV trip), the 96th St surcharge line, inbound-only Hudson tolls ($16.79 peak), airport fees and out-of-town pay rates. The user's idea of comparing road density with foot-traffic density becomes a 'pickup-ability' index (stoppable curb vs pedestrians), built from NYC DOT pedestrian counts, the Pedestrian Mobility Plan street classes and MTA hourly subway ridership. Robotaxi geography in NYC is hypothetical (Waymo's test permits for Manhattan south of 112th St and Downtown Brooklyn, with no passengers, expired on 31 March 2026), so the geofence should be a benchmark setting. The dossier lists 70 variables in 10 sub-boxes (19 high, 32 medium, 19 low impact; 39 core), from zone structure to restroom access. Many headline numbers are my own computations on TLC trip records, while official fee and rule pages were readable only through search snippets.

## 2. Method and limits

- **Own data analysis [P]:** I downloaded GitHub copies of TLC trip records (DataTalksClub/nyc-tlc-data releases), because the TLC CloudFront host is blocked. The files were yellow October 2019 (7.08M clean trips), green October 2019 (473,824 trips), HVFHV June 2021 (14.96M trips; this copy has only the old schema without fares or pay) and the taxi zone lookup. From these I computed zone shares, flows, airport revenue share, tip rates and out-of-city shares. October 2019 is pre-pandemic and pre-congestion-pricing. June 2021 is mid-recovery, so its HVFHV shares are indicative only.
- **Blocked hosts:** nyc.gov, mta.info, data.ny.gov, data.cityofnewyork.us, panynj.gov, nber.org and arxiv.org were not reachable from this session, so I read official pages only through search snippets, tagged [S]. I used no proxy, reader or mirror services.
- **Search budget:** The shared web-search budget ran out partway through. Items I could not check (driver residence distribution, current MTA car toll, Newark taxi surcharge, speed-camera hours, out-of-state pickup licensing, the HVFHV rendezvous fields) are tagged [U] and listed in the open questions.
- **Tags:** [P] = primary, read directly or computed by me from primary data; [S] = search snippet or secondary; [U] = unverified background knowledge; [design] = our suggestion.

## 3. Key numbers from the TLC trip records (own computation) [P]

| Metric | Yellow, Oct 2019 | HVFHV, Jun 2021 | Green, Oct 2019 |
|---|---|---|---|
| Pickups in the Yellow Zone (55 Manhattan-core zones) | 89.0% | 32.2% | 3.1% |
| Pickups in outer-borough Boro Zones | 2.2% | 59.5% | 64.6% |
| Pickups in upper Manhattan Boro Zones | 2.4% | 6.0% | 32.3% |
| Zones needed for 50% / 80% / 95% of pickups | 16 / 32 / 48 | 60 / 125 / 188 | n/a |
| Pickups-to-drop-offs ratio: Brooklyn / Bronx / Staten Island | 0.27 / 0.24 / 0.14 | 1.02 / 1.05 / 1.03 | n/a |
| Airport-touching trips (JFK, LGA, EWR) | 7.9% of trips, 22.2% of driver revenue | 5.4% of trips | 1.8% of drop-offs |
| JFK pickups vs drop-offs | 236,737 vs 62,125 | 188,867 vs 224,571 | n/a |
| EWR pickups vs drop-offs | 57 vs 15,829 | 228 vs 63,278 | n/a |
| Trips ending outside NYC | rate code 4 (Nassau/Westchester) 0.08%, negotiated 0.17%, Newark 0.24% | 3.67% (zone 265) + 0.42% EWR | n/a |
| Mean in-trip speed, Yellow Zone vs airport pickups | ~10.2 vs ~20.9 mph | n/a | n/a |
| Driver revenue per in-trip hour, Yellow Zone / outer / airports | $64 / $75 / $75 | n/a | n/a |
| Card-trip tip as share of fare, Yellow Zone vs outer-borough pickups | 25.9% vs 19.3% | n/a | n/a |
| Card share of trips, Yellow Zone vs outer boroughs | 74.2% vs 51.7% | n/a (all app) | n/a |
| Core pickups ending in outer boroughs, 8am vs 4am | 1.4% vs 17.7% | n/a | n/a |
| Trips paying a toll; mean toll | 5.9%; $6.63 | n/a | n/a |

Driver revenue = fare + extras + tip (tips only recorded for card trips). In-trip revenue per hour is similar everywhere, so the profit gap between areas comes from empty time between trips, which these records cannot show without driver IDs. The simulator has to model that gap through the imbalance, queue and deadhead variables below.

## 4. Box view (the placeholder list, extended)

* Geography, land use and road network (R01)
   * Zones and service areas
      * R01-001 Taxi zone partition [high impact]
      * R01-002 Service-zone class [high impact]
      * R01-003 Pickup concentration (spatial skew) [high impact]
      * R01-004 Zone pickup/drop-off imbalance [high impact]
      * R01-005 Taxi vs app geographic footprint [high impact]
      * R01-006 Green taxi hail exclusionary zone [high impact]
      * R01-007 Licensing jurisdiction boundary [medium impact]
      * R01-008 Robotaxi operating geofence (ODD) [high impact]
      * R01-009 Spatial resolution [medium impact]
      * R01-010 Zone adjacency and travel-time skim [high impact]
      * R01-011 Repositioning target (where to wait or cruise) [high impact]
   * Road network structure
      * R01-012 Road hierarchy class [medium impact]
      * R01-013 One-way streets and circuity [medium impact]
      * R01-014 Turn restrictions [low impact]
      * R01-015 Speed limits [low impact]
      * R01-016 Enforcement camera locations [low impact]
      * R01-017 Road access by vehicle class [low impact]
      * R01-018 Elevation and grade [low impact]
   * Chokepoints, tolls and charging zones
      * R01-019 River crossings as chokepoints [high impact]
      * R01-020 MTA bridge and tunnel tolls [medium impact]
      * R01-021 Port Authority Hudson crossing tolls [medium impact]
      * R01-022 Congestion Relief Zone (CRZ) [medium impact]
      * R01-023 State congestion surcharge zone (96th St line) [low impact]
      * R01-024 Fee-avoiding route choice [low impact]
   * Curb access and restricted streets
      * R01-025 Curb regulation at the stop point [medium impact]
      * R01-026 Rider-driver rendezvous time [medium impact]
      * R01-027 Bus lanes [low impact]
      * R01-028 Busways and transit-priority streets [low impact]
      * R01-029 Car-free park drives and plazas [low impact]
      * R01-030 Taxi stands and hotel queues [medium impact]
      * R01-031 Taxi/FHV relief stands [low impact]
      * R01-032 Legal waiting spots (staging) [medium impact]
      * R01-033 Robotaxi pickup-point placement [low impact]
   * Foot traffic vs road density (the user's 'roads vs foot traffic' idea)
      * R01-034 Pedestrian volume by location [high impact]
      * R01-035 Pedestrian demand class of each street [medium impact]
      * R01-036 Subway entries and exits by hour [medium impact]
      * R01-037 Road-to-pedestrian ratio ('pickup-ability') [medium impact]
      * R01-038 Transit accessibility [medium impact]
      * R01-039 Population and job density [high impact]
      * R01-040 Hail visibility by street type [medium impact]
      * R01-041 Cruising route for street hails [medium impact]
   * Land use and trip generators
      * R01-042 Land-use mix per zone [high impact]
      * R01-043 Office and business districts [medium impact]
      * R01-044 Nightlife density [medium impact]
      * R01-045 Tourist and hotel density [medium impact]
      * R01-046 Hospitals, universities and institutions [low impact]
      * R01-047 Venues, stadiums and convention centres [medium impact]
      * R01-048 Retail and shopping corridors [low impact]
   * Transit hubs and airports
      * R01-049 Intercity rail and bus hubs [high impact]
      * R01-050 Airport trip share and value [high impact]
      * R01-051 Airport pickup/drop-off asymmetry [medium impact]
      * R01-052 Airport holding-lot queue [high impact]
      * R01-053 Airport queue decision [high impact]
      * R01-054 Airport fare and fee triggers [medium impact]
      * R01-055 Airport terminal layout and pickup rules [low impact]
      * R01-056 Newark Airport (EWR) special status [medium impact]
   * Out-of-city trips and the empty return
      * R01-057 Out-of-city trip share [medium impact]
      * R01-058 Out-of-city fare and pay rules [medium impact]
      * R01-059 Empty-return distance and legality [high impact]
      * R01-060 Night outward drift [high impact]
   * Driver home, depots and amenities
      * R01-061 Driver home location [medium impact]
      * R01-062 Distance and time to home [medium impact]
      * R01-063 Garages, depots and shift-change points [medium impact]
      * R01-064 Fuel station locations [low impact]
      * R01-065 EV charger locations, power and access [medium impact]
      * R01-066 Restrooms, food and break spots [low impact]
   * Neighbourhood economics and safety
      * R01-067 Neighbourhood income [medium impact]
      * R01-068 Payment mix by zone [low impact]
      * R01-069 Perceived safety and crime [low impact]
      * R01-070 Geographic refusal rules [medium impact]

## 5. Variables by sub-box

### 5.1 Zones and service areas

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-001** Taxi zone partition | The city is split into the TLC's 263 taxi zones (plus 2 unknown codes), the spatial unit of every public trip record. | 263 zones: Manhattan 69, Queens 69, Brooklyn 61, Bronx 43, Staten Island 20, EWR 1; IDs 264/265 = unknown / outside NYC | high | [P] Counted 265 rows in taxi_zone_lookup.csv (GitHub copy of the TLC file); all trip data is keyed to these IDs | world | Yes | NYC Taxi Zones, NYC Open Data 755u-8jsi (https://data.cityofnewyork.us/d/755u-8jsi); TLC lookup + shapefile (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | Load zone polygons; map every car and request position to a zone ID; demand, fares and stats keyed by zone |
| **R01-002** Service-zone class | Each zone belongs to a TLC service class that decides who may street-hail there and which fare rules apply. | Yellow Zone 55 (Manhattan core) / Boro Zone 205 (14 upper Manhattan + 191 outer borough) / Airports 2 (JFK 132, LGA 138) / EWR 1 | high | [P] Lookup counts; 89.0% of yellow pickups were in the 55 Yellow Zone zones (Oct 2019, own computation) | rule | Yes | Same as R01-001 (service_zone column) | Zone attribute checked by hail-eligibility and fare rules |
| **R01-003** Pickup concentration (spatial skew) | How unevenly trip origins are spread across zones; the more concentrated, the more location choice matters. | Yellow Oct 2019: 16 zones = 50% of pickups, 32 = 80%, 48 = 95%; HVFHV Jun 2021: 60 / 125 / 188 zones | high | [P] Own computation on TLC yellow (Oct 2019, 7.08M trips) and HVFHV (Jun 2021, 14.96M trips) records | world | Public / forecast | TLC trip records (yellow, green, FHV, HVFHV) | Demand generator samples origins from a zone x hour intensity fitted to trip records; historic heatmap can be given to the agent as public info |
| **R01-004** Zone pickup/drop-off imbalance | Ratio of pickups to drop-offs per zone; zones well below 1 are 'sinks' where a driver lands with few nearby requests. | Yellow Oct 2019 PU/DO: Manhattan 1.02, Queens 1.30, Brooklyn 0.27, Bronx 0.24, Staten Island 0.14; zone extremes JFK 3.81, Washington Heights North 0.09. HVFHV Jun 2021: every borough 1.02-1.06 | high | [P] Own computation, TLC yellow Oct 2019 and HVFHV Jun 2021 | world | Public / forecast | TLC trip records | Emerges from the OD matrix; expose historic PU/DO ratio per zone x hour as a public layer |
| **R01-005** Taxi vs app geographic footprint | Street-hail demand sits in the Manhattan core while app demand is spread over the outer boroughs, so the same map rewards different positioning by driver type. | Share of pickups in Yellow Zone: yellow 89.0% vs HVFHV 32.2%; outer boroughs: 2.2% vs 59.5%. Manhattan HV trips fell 6.1% Jan 2025 to Jan 2026 while other boroughs grew | high | [P] Own computation (yellow Oct 2019 vs HVFHV Jun 2021); [S] TLC license pause report Feb 2026 | world | Public / forecast | TLC trip records; TLC license pause reports (https://www.nyc.gov/assets/tlc/downloads/pdf/license-pause-report-2026-02.pdf) | Separate demand layers per channel (street hail, e-hail) with their own zone weights |
| **R01-006** Green taxi hail exclusionary zone | Green (boro) taxis may not take street hails in Manhattan south of E 96th St and W 110th St, or at JFK and LGA; they may drop off anywhere. | Excluded: 55 Yellow Zone zones + 2 airports. Green Oct 2019 pickups: 64.6% outer boroughs, 32.3% upper Manhattan, 3.1% Yellow Zone; 18.5% of drop-offs in Yellow Zone | high | [S] TLC 'Hail Zone' decal rule (2014) and green cab pages; [P] own computation, green Oct 2019 (473,824 trips) | rule | Yes | TLC green cab rules (https://www.nyc.gov/site/tlc/businesses/green-cab.page); TLC green trip records | Street-hail generation disabled for green cars inside excluded polygons; e-hail still allowed |
| **R01-007** Licensing jurisdiction boundary | The area where the vehicle's licence allows pickups (NYC for TLC vehicles); trips may end outside it, but pickups outside are effectively unavailable. | Inside five boroughs: pickups allowed. Outside: drop-off only. EWR: yellow 57 pickups vs 15,829 drop-offs (Oct 2019); HVFHV 228 vs 63,278 (Jun 2021). Uber JFK pickups only for TLC-licensed drivers | medium | [P] Own counts from TLC records; [S] Uber JFK driver-information page | rule | Yes | TLC trip records; Uber airport driver pages; county taxi rules [U] | Pickup-eligibility mask by polygon and licence type |
| **R01-008** Robotaxi operating geofence (ODD) | The polygon and road types where an autonomous vehicle is allowed and able to drive and serve riders. | Example: Waymo NYC test permit (Aug 2025 to 31 Mar 2026) covered Manhattan south of 112th St + Downtown Brooklyn, 8 cars, safety driver, no paying riders. Scenario options: core-only / core + airports / citywide | high | [S] West Side Spirit and Jalopnik (Apr 2026): permits expired 31 Mar 2026; passenger service would need a TLC licence; state law requires a driver behind the wheel | setting | Yes | NYC DOT AV permit news; no machine-readable geofence found | Geofence polygon + road-class whitelist; requests outside are unservable or lost to competitors |
| **R01-009** Spatial resolution | The unit at which positions and demand are represented: taxi zone, hex grid or road segment. | Taxi zone (~3 km2 mean, 263 units) / H3 hex res 8 (~0.7 km2) / OSM drivable road graph (tens of thousands of nodes) | medium | [design] Finer resolution lets positioning skill show but costs compute and data; zone level matches public trip data | setting | Yes | TLC zones; OpenStreetMap (https://www.openstreetmap.org); NYC DCP LION | Start at zone level with a random point inside the zone; upgrade to a road graph for routing, curbs and hails |
| **R01-010** Zone adjacency and travel-time skim | A zone-to-zone neighbour list and travel-time matrix used for repositioning and fleet rebalancing. | 263 x 263 matrix of travel times by hour (minutes); neighbour lists | high | [design] Needed by both single-car repositioning and fleet rebalancing; R10 supplies the times | world | Yes | Derived from OSM graph + TLC trip durations; NYC DOT traffic speeds (cross-link R10) | Precompute skims per hour band; agent tools query ETA between zones |
| **R01-011** Repositioning target (where to wait or cruise) | The agent's choice of which zone or street to drive to, or wait in, when empty; the core geographic skill the benchmark measures. | Any reachable zone or road node; options: stay, cruise a loop, drive to zone z, go to a hub or airport, go home | high | [S] Haggag, McManus and Paci (2017, AEJ Applied): neighbourhood-specific experience raises taxi driver productivity and changes search; Buchholz (2022): search frictions leave some areas unserved while others have excess cabs | agent | Yes | Logged from agent actions; benchmark compares with TLC-derived demand | Action space: reposition(zone or node), wait(here), cruise(route); travel time from R10 |

### 5.2 Road network structure

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-012** Road hierarchy class | Each road segment's class (expressway or parkway, arterial avenue, collector, local) sets its speed, capacity and how good it is for finding hails. | OSM highway = motorway / trunk / primary / secondary / tertiary / residential. Mean in-trip speed: ~10.2 mph for Yellow Zone pickups vs ~20.9 mph for airport pickups (yellow Oct 2019) | medium | [P] Own computation (distance / duration) from TLC yellow Oct 2019 | world | Yes | OpenStreetMap; NYC DCP LION street centerline (lanes, width, direction) | Graph edges carry class: free-flow speed and capacity; congestion handled in R10 |
| **R01-013** One-way streets and circuity | Manhattan's mostly one-way grid and the rivers make driving distance longer than straight-line distance, and a pickup on the wrong side costs a loop. | Avenues and most cross streets one-way; major two-way crosstown streets (14th, 23rd, 34th, 42nd, 57th, 72nd, 79th, 86th, 96th, 110th, 125th); circuity ~1.2-1.4; turn-around loop ~2-4 blocks | medium | [U] Background knowledge of the NYC grid; LION has a traffic-direction field | world | Yes | NYC DCP LION (TrafDir); OSM oneway tag | Directed graph; car heading matters for pickup ETA |
| **R01-014** Turn restrictions | Banned turns (many Midtown left turns, some by time of day) lengthen routes and ETAs. | Restricted turns per intersection; time windows such as 7am-7pm | low | [U] Background knowledge | rule | Yes | OSM turn-restriction relations; NYC DOT signage | Turn-restriction table in the router |
| **R01-015** Speed limits | Legal maximum per segment; caps free-flow speed (robotaxis obey exactly, humans may exceed). | Citywide default 25 mph; Sammy's Law lets the city set 20 mph streets and 10-15 mph school zones (all school zones 15 mph by 2029 planned); highways 40-50 mph | low | [S] Streetsblog (Oct 2026), West Side Spirit: Sammy's Law rollout; CBS conflicting on base limit | rule | Yes | NYC DOT speed-limit data on NYC Open Data [U]; OSM maxspeed | Edge attribute; robotaxi speed = min(limit, traffic speed) |
| **R01-016** Enforcement camera locations | Where speed, red-light and bus-lane cameras are, which creates fine risk for human drivers. | Speed camera fine $50 (+$25 late); bus-lane fine $50 first offence rising to $250; cameras cover all bus lanes | low | [S] NYC DOT bus-lane rules; news coverage of speed cameras | rule | Public / forecast | NYC Open Data parking and camera violations [U] | Per-edge violation probability x fine, applied when the agent's driving style breaks rules |
| **R01-017** Road access by vehicle class | Some roads are closed to some vehicles: parkways ban commercial vehicles (taxis and FHVs count as passenger cars) and robotaxis may be kept off freeways. | Parkway allowed yes/no; robotaxi freeway allowed yes/no (scenario) | low | [U] Background knowledge; medium for robotaxi if freeways are excluded | rule | Yes | OSM access tags; NYSDOT parkway rules [U] | Edge mask per vehicle class |
| **R01-018** Elevation and grade | Hills slightly raise energy use; NYC is mostly flat with steep spots (Washington Heights, Staten Island, parts of the Bronx). | Grade 0-10%+; elevation 0 to ~125 m | low | [U] Background knowledge | world | Yes | USGS 3DEP; NYC 1-ft DEM on NYC Open Data [U] | Edge grade feeds an energy multiplier in R08 |

### 5.3 Chokepoints, tolls and charging zones

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-019** River crossings as chokepoints | Bridges and tunnels are the only links between boroughs and to New Jersey, so they concentrate delay, incidents and tolls. | East River: Brooklyn, Manhattan, Williamsburg, Queensboro bridges (free), Queens-Midtown and Hugh Carey tunnels and RFK (tolled); Hudson: GWB, Lincoln, Holland; Harlem River bridges (free); Verrazzano, Throgs Neck, Whitestone, Cross Bay, Marine Pkwy | high | [P] 5.9% of yellow trips paid a toll, mean $6.63 (Oct 2019, own computation); [U] network facts | world | Yes | OpenStreetMap; NYC DOT bridge traffic volumes [U] | Crossing edges with their own capacity, incident probability (R03) and travel-time variance (R10) |
| **R01-020** MTA bridge and tunnel tolls | Toll charged at MTA crossings, by crossing, payment type and direction. | Car E-ZPass ~$6.94 at major crossings (2023), raised ~6% on 4 Jan 2026 (exact car rate unverified); Cross Bay and Marine Pkwy about half (bus E-ZPass $3.39 vs $6.42); East River and Harlem River bridges free | medium | [S] MTA franchise-bus toll page (rates effective 4 Jan 2026); news on ~6% E-ZPass rise | rule | Yes | MTA tolls (https://www.mta.info/fares-tolls/tolls) | Toll table by crossing x direction x payment; passed to the rider when loaded, paid by the driver when empty |
| **R01-021** Port Authority Hudson crossing tolls | GWB, Lincoln and Holland charge only when entering New York, so a driver returning empty from NJ pays; one-direction tolling (also Verrazzano, into Staten Island only [U]) makes return legs cost more than outbound legs. | Car E-ZPass $16.79 peak / ~$14.79 off-peak, toll-by-plate ~$23.05-23.30 (from 4 Jan 2026); peak = weekdays 6-10am and 4-8pm, weekends 11am-9pm | medium | [S] ROI-NJ (Jan 2026); PANYNJ Truckers Guide (Apr 2026) | rule | Yes | PANYNJ (https://www.panynj.gov/bridges-tunnels) | Inbound-only toll on NJ-to-NY crossing edges, charged to the driver when empty |
| **R01-022** Congestion Relief Zone (CRZ) | Manhattan at or south of 60th St (excluding FDR Drive, West Side Highway / Route 9A and Hugh Carey Tunnel links) where each taxi/FHV trip to, from, within or through the zone pays a per-trip charge. | $0.75 per yellow, green or other FHV trip; $1.50 per HVFHV trip; since 5 Jan 2025; private cars $9 peak (2025-27), $12 (2028-30), $15 (2031), $2.25 overnight; unenrolled fleets pay a daily toll | medium | [S] MTA taxi/FHV toll page; ABC7 on toll phases; 2025 political/legal challenges not resolved in my sources | rule | Yes | MTA CBD taxi zones dataset (https://catalog.data.gov/dataset/mta-central-business-district-taxi-zones); cbd_congestion_fee field in 2025+ trip records [U] | Polygon; flag trips whose route touches it (excluding exempt edges); rider-paid but shifts demand (R05) and speeds (R10) |
| **R01-023** State congestion surcharge zone (96th St line) | A second, larger zone: trips that begin, end or pass through Manhattan south of 96th St pay a state surcharge. | $2.50 yellow, $2.75 green and FHV, $0.75 shared ride | low | [S] TLC taxi-fare page | rule | Yes | TLC fare page (https://www.nyc.gov/site/tlc/passengers/taxi-fare.page) | Second polygon; per-trip surcharge in the fare engine |
| **R01-024** Fee-avoiding route choice | Because the FDR and West Side Highway are outside the CRZ and some bridges are free, a route can avoid a charge at the cost of time. | k alternative routes per OD with toll and time trade-off | low | [S] CRZ exclusion list; [design] | agent | Yes | OSM graph + toll tables | Offer k-shortest paths with costs; agent or router chooses |

### 5.4 Curb access and restricted streets

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-025** Curb regulation at the stop point | The sign type at the curb decides whether a quick pickup or drop-off is legal. | No Parking (stop OK) / No Standing (quick passenger pickup OK, no waiting) / No Stopping (not allowed) / bus stop (OK if no bus is blocked) / taxi stand (taxis only) / FHV stand ($115 if standing beyond a quick pickup) | medium | [S] NYC DOT parking sign legend; NYC DOF violation codes | rule | Yes | NYC DOT Parking Regulation Locations and Signs (NYC Open Data) [U] | Curb-segment attribute; illegal stop = fine probability or forced re-loop |
| **R01-026** Rider-driver rendezvous time | Minutes between the car arriving and the rider getting in, driven by building entrances, curb space, double parking and crowds. | 0.5-5 min typical [U]; measurable as pickup_datetime minus on_scene_datetime in HVFHV records | medium | [U] Field availability from the HVFHV data dictionary not verified here (search budget used up) | world | No (hidden) | TLC HVFHV trip records (request_datetime, on_scene_datetime, pickup_datetime) | Per-zone x hour lognormal dwell fitted from HVFHV records, added to each pickup |
| **R01-027** Bus lanes | Lanes reserved for buses that cars may enter only to turn right, reach a driveway within 200 ft, or quickly pick up or drop off at the curb. | Curbside pickup allowed; stopping in the centre of the lane not allowed; fines $50 rising to $250; cameras on all bus lanes | low | [S] NYC DOT bus-lane rules; TLC bus/bike lane brochure | rule | Yes | NYC DOT bus lanes (NYC Open Data) [U] | Lane attribute with hours; fine risk when misused |
| **R01-028** Busways and transit-priority streets | Streets where through car traffic is banned for set hours, but taxis and FHVs may enter for local pickups and must turn off at the next street. | 14th St busway (3rd to 8th Ave, ~6am-10pm); others such as Main St Flushing, Jamaica Ave, Archer Ave, 181st St [U]; 34th St bus priority (2025) | low | [S] Village Sun / amNY on 14th St busway rules; NYC DOT 34th St documents | rule | Yes | NYC DOT busways page (https://www.nyc.gov/html/brt/html/busways/busways.shtml) | Edges with through-traffic ban + forced turn after a stop |
| **R01-029** Car-free park drives and plazas | Roads closed to cars inside demand areas, so pickups move to the edges and routes detour. | Central Park loop drives car-free since 27 Jun 2018 (transverses open); Prospect Park loop car-free; Times Square / Broadway plazas; Open Streets time windows | low | [S] ABC7, Central Park Conservancy (2018) | rule | Yes | OSM; NYC DOT Open Streets data [U] | Remove edges (permanently or by time); snap pickups to the nearest legal curb |
| **R01-030** Taxi stands and hotel queues | Designated stands (hotels, transit hubs) where only taxis may wait in line for passengers. | Stand present yes/no; queue length 0-30 cabs [U] | medium | [S] NYC DOT sign legend: only taxis may wait at a taxi stand | world | Yes | NYC DCP taxi-stand study (https://www.nyc.gov/assets/planning/download/pdf/plans/transportation/td_taxistands.pdf) | FIFO queue node fed by hotel or hub demand |
| **R01-031** Taxi/FHV relief stands | Curb spaces where taxi and FHV drivers may park for up to one hour to take a break. | 113 stands: Manhattan 70, Queens 28, Bronx 12, Brooklyn 3, Staten Island 0 | low | [S] Manhattan CB1 letter (2026) citing NYC DOT; NYC DOT relief-stand page | world | Yes | NYC Open Data 'Taxi and For-Hire Vehicle (FHV) Relief Stands' (https://catalog.data.gov/dataset/taxi-and-for-hire-vehicle-fhv-relief-stands) | POI layer; a break elsewhere costs parking search time or ticket risk |
| **R01-032** Legal waiting spots (staging) | Whether the car can legally sit still near a hotspot while waiting for the next request instead of cruising. | Share of curb where standing is legal per zone; parking $0-15+/h [U]; NYC anti-idling limit 3 min (1 min next to schools) [U] | medium | [S] Schaller (2017): app cars average 11 min empty between trips vs 8 min for taxis; over 1/3 of cars empty in the Manhattan CBD | world | Yes | NYC DOT parking regulations; licensed garages on NYC Open Data [U] | Per-zone wait cost (fuel, ticket risk, parking fee) vs cruise cost; agent chooses wait, cruise or reposition |
| **R01-033** Robotaxi pickup-point placement | A robotaxi stops only at a legal, safe point, which may be up to a block away, adding rider walk time and cancellations. | Walk 0-200 m [design]; density of valid pickup points per km of curb | low | [design] / [U] Operator practice not verified | rule | Yes | None found (operator-internal); OSM curbs | Snap each request to the nearest legal curb node; walk time adds to rendezvous; cancel chance rises with walk |

### 5.5 Foot traffic vs road density

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-034** Pedestrian volume by location | How many people walk past a point; drives street-hail chances and is a proxy for latent ride demand. | DOT counts at 114 locations (100 on-street, mainly retail corridors; 13 bridges; Hudson River Greenway), counted each May and September | high | [S] NYC Open Data dataset description; Buchholz (2022, REStud): taxis are drawn to search in the most concentrated pedestrian areas | world | Public / forecast | NYC DOT Bi-Annual Pedestrian Counts (https://data.cityofnewyork.us/d/2de2-6x2h) | Street-hail arrival rate per edge proportional to pedestrian intensity x hour profile, calibrated to yellow pickups |
| **R01-035** Pedestrian demand class of each street | NYC DOT's Pedestrian Mobility Plan puts every street in one of five pedestrian-demand classes. | Baseline (~60% of roads), Community Connector (~25%), Neighborhood Corridor, Regional Corridor, Global Corridor (mostly Manhattan) | medium | [S] NYC DOT Pedestrian Mobility Plan and data.gov dataset (modified Mar 2026); MIT critique that some outer-borough streets are under-classified | world | Yes | Pedestrian Mobility Plan Pedestrian Demand (https://catalog.data.gov/dataset/pedestrian-mobility-plan-pedestrian-demand) | Categorical edge attribute feeding hail rate and curb friction |
| **R01-036** Subway entries and exits by hour | Hourly subway ridership per station shows where crowds appear and when transit thins out, shaping first/last-mile and substitute demand. | Hourly counts by station complex: 2017-19 (t69i-h2me), 2020-24 (wujg-7c2s), 2025+ (5wq4-mkjj); OD estimates (jsu2-fbtj) | medium | [S] data.ny.gov catalog entries | world | Public / forecast | MTA Subway Hourly Ridership (https://data.ny.gov/d/5wq4-mkjj) | Demand covariate; subway outages (R03) move demand to cars near affected stations |
| **R01-037** Road-to-pedestrian ratio ('pickup-ability') | The user's idea: compare how many pedestrians gather on a block with how much drivable road and stoppable curb it has; busy but curb-starved streets mean many riders but slow, congested pickups. | Index = legal-stop curb metres / pedestrians per hour (or lanes / pedestrian class); bands low / medium / high; low examples Times Sq, SoHo | medium | [design]; Buchholz (2022): competition pushes taxis to spread search beyond the densest pedestrian areas [S] | world | Yes | DOT pedestrian counts + Pedestrian Mobility Plan + LION width/lanes + DOT parking signs | Per-edge index raises hail rate (+) and pickup dwell / lowers through-speed (-) |
| **R01-038** Transit accessibility | Distance from a zone to the nearest subway station; areas far from rail rely more on cars for hire. | 0-3+ km to nearest station; transit-desert flag | medium | [P] Top HVFHV pickup zones include East New York, Crown Heights North, Bushwick South (Jun 2021); [U] transit-substitution mechanism | world | Yes | MTA GTFS static (https://new.mta.info/developers); NYC subway entrances (NYC Open Data) | Demand covariate; raises late-night demand when subway headways lengthen |
| **R01-039** Population and job density | Residents and workers per zone are the base of trip generation. | Residents/km2 and jobs/km2 per zone | high | [U] Standard trip-generation practice; Correa, Chow and Ozbay model demand from the spatial distribution of activities [S] | world | Yes | US Census ACS 5-year (https://data.census.gov); LEHD LODES (https://lehd.ces.census.gov/data/) | Demand-generator covariates when extrapolating beyond replayed data |
| **R01-040** Hail visibility by street type | Street hails happen mostly on avenues and busy corridors that cabs pass often; side streets yield few hails. | Hail multiplier: avenue 1.0, cross street 0.2-0.5 [design guess] | medium | [design] / [U]; yellow records before mid-2016 have exact coordinates and could calibrate this [U] | world | No (hidden) | Pre-2016 TLC yellow records with lat/lon | Generate hails per edge; a cruising agent only sees hails on edges it drives |
| **R01-041** Cruising route for street hails | For a taxi, which streets to drive while empty, trading distance (fuel, time) against passing more pedestrians. | Route through high-hail edges vs waiting at a stand; cruise speed in traffic | medium | [design]; Schaller (2017): yellow taxis average 8 min empty between trips in the Manhattan CBD [S] | agent | Yes | Pre-2016 TLC yellow coordinates for calibration [U] | Agent picks the next edge or a loop; hails generated only on traversed edges |

### 5.6 Land use and trip generators

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-042** Land-use mix per zone | Share of residential, office, retail, nightlife, industrial and park land; sets the daily shape of demand. | MapPLUTO land-use classes (11) by lot area per zone | high | [P] Share of core yellow pickups ending in outer boroughs: 1.4% at 8am vs 17.7% at 4am (Oct 2019), showing home-bound night flows | world | Yes | NYC DCP MapPLUTO (https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page) | Zone feature vector; demand time profile depends on land-use mix |
| **R01-043** Office and business districts | Midtown, Financial District, Hudson Yards, Downtown Brooklyn and Long Island City pull weekday daytime trips. | Jobs per zone; weekday vs weekend ratio | medium | [P] Midtown Center 4.2% and Midtown East 3.7% of all yellow pickups (Oct 2019) | world | Yes | LEHD LODES; MapPLUTO office area | Work-hour peaks per zone (remote-work days in R02) |
| **R01-044** Nightlife density | Bars, clubs and late restaurants create late-night demand and longer, outbound trips. | On-premises liquor licences per zone; key areas LES, East Village, Meatpacking, Williamsburg, Bushwick | medium | [P] East Village is the #2 HVFHV pickup zone (Jun 2021); Meatpacking among the highest-tip drop-off zones (27%) | world | Yes | NYS Liquor Authority licences (data.ny.gov) [U]; DOHMH restaurant inspections [U] | Late-night demand multiplier; destinations drawn toward residential zones |
| **R01-045** Tourist and hotel density | Hotels and attractions create airport trips, taxi-stand queues and riders less likely to use transit. | Hotel rooms per zone; attraction POIs | medium | [P] Times Sq/Theatre District = 3.5% of yellow pickups (Oct 2019) | world | Yes | OSM tourism tags; NYC hotel lists on NYC Open Data [U] | Hotel POIs as taxi-stand queues and airport-bound demand |
| **R01-046** Hospitals, universities and institutions | Large hospitals produce steady trips around shift changes and discharges (plus paratransit rides); campuses shift demand with the academic calendar. | Beds per site; shift changes ~7am / 7pm [U]; enrolment per campus, term on/off | low | [U] Background knowledge; HVFHV records carry an access_a_ride flag [U] | world | Yes | NYS DOH health facility data (health.data.ny.gov) [U]; NCES IPEDS (campuses) | POI with a daily time profile and seasonal multiplier (R02) |
| **R01-047** Venues, stadiums and convention centres | Fixed big venues whose location, capacity and exits shape event surges (the events themselves are in R03). | Capacity 2k-50k (MSG, Barclays, Yankee Stadium, Citi Field, USTA, UBS Arena, Javits, Lincoln Center); exit curb capacity | medium | [U] Background knowledge; MSG sits on Penn Station (zone 186, top-5 yellow pickup zone) [P] | world | Yes | OSM; venue websites | Venue nodes with capacity; R03 schedules events on them |
| **R01-048** Retail and shopping corridors | Shopping streets create daytime and weekend short trips. | Retail floor area per zone | low | [U] Background knowledge; most DOT pedestrian count sites are retail corridors [S] | world | Yes | MapPLUTO retail area; DOT pedestrian counts | Daytime / weekend demand covariate |

### 5.7 Transit hubs and airports

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-049** Intercity rail and bus hubs | Penn Station/Moynihan, Grand Central, Port Authority Bus Terminal, Atlantic Terminal and Jamaica produce rider pulses timed to public train and bus arrivals. | Penn Station/Madison Sq West = 3.6% of yellow pickups, PU/DO 1.40 (Oct 2019); arrival schedules public in GTFS | high | [P] Own computation, TLC yellow Oct 2019 | world | Public / forecast | GTFS feeds (MTA, NJ Transit, Amtrak); TLC records | Hub nodes with arrival-driven pulses + taxi-stand queues |
| **R01-050** Airport trip share and value | Airport trips are few but long and lucrative. | Yellow Oct 2019: 7.9% of trips, 22.2% of driver revenue (fare + extras + tips); JFK pickup mean $51.19 over 15.3 mi, LGA $37.81 over 9.1 mi. HVFHV Jun 2021: 5.4% of trips touch an airport | high | [P] Own computation, TLC yellow Oct 2019 and HVFHV Jun 2021 | world | Public / forecast | TLC trip records | Airport zones with their own demand profile tied to flight schedules (R03/R12) |
| **R01-051** Airport pickup/drop-off asymmetry | For yellow cabs airport pickups far exceed drop-offs, while app trips are roughly balanced. | Yellow PU/DO: JFK 3.81, LGA 2.06 (Oct 2019); HVFHV: JFK 0.84, LGA 0.88 (Jun 2021) | medium | [P] Own computation | world | Public / forecast | TLC trip records | Emerges from the OD matrix; decides whether an airport drop-off can be followed by an airport pickup |
| **R01-052** Airport holding-lot queue | After an airport drop-off, a driver can join a lot queue for an outbound fare or deadhead back; queue length sets the expected wait. | Yellow JFK central taxi hold: historically ~2-3 h average, up to 5 h. FHV: virtual FIFO queue (JFK Cell Phone Lot / Limo Lot; LGA lot), free parking up to 3 h, place lost if offline or after repeated declines | high | [S] NBC New York (bribery case); Uber JFK driver page; Yazici, Kamga and Singhal (2016, TR-A): proximity is the strongest predictor of the airport-pickup decision | state | Yes | No public queue data; infer from TLC airport drop-off and pickup times [design] | Per-airport FIFO queue fed by flight arrivals; agent joins or leaves; app shows queue position |
| **R01-053** Airport queue decision | After an airport drop-off, the agent decides whether to join the airport queue, leave it, or deadhead back to the city. | Join / skip / leave after t minutes; information: queue position (app) or lot count (taxi) | high | [S] Yazici, Kamga and Singhal (2016): NYC taxi drivers' airport-pickup decisions depend mainly on proximity, then time, weather and shift variables | agent | Yes | TLC airport trips for calibration | Action at airport zones; payoff = expected airport fare minus queue time vs city alternative |
| **R01-054** Airport fare and fee triggers | Fare rules switched on by airport geography (amounts owned by R07). | Taxi: JFK to/from Manhattan flat $70 (+$5 weekdays 4-8pm); LGA +$5; $1.75 access fee on JFK/LGA pickups. HVFHV: $2.50 airport fee at JFK/LGA/EWR (since Apr 2023). Newark taxi surcharge $17.50 to $20 (2022 proposal; current value unverified) | medium | [S] TLC taxi-fare page; VisaVerge / Fox5 on the FHV fee | rule | Yes | TLC fare page; airport_fee fields in trip records | Airport polygons trigger fare-engine branches |
| **R01-055** Airport terminal layout and pickup rules | Where at the airport pickups are allowed (terminal curbs, FHV zones, remote lots), adding minutes and confusion. | JFK: FHV pickups barred at Terminals 5 and 7 'until further notice', with Howard Beach FHV Hold Lot 3; arrivals-level pickups only; JFK rebuilding (New Terminal One) changes roads [U] | low | [S] Uber JFK driver page (French version); Inshur driver guide (2021) | rule | Yes | PANYNJ ground transport pages; Uber airport driver pages | Airport sub-graph with pickup nodes per terminal and extra walk/drive time |
| **R01-056** Newark Airport (EWR) special status | EWR is in New Jersey: NYC drivers drop off there but almost never pick up, so each EWR drop-off implies an empty, tolled return. | Yellow: 15,829 drop-offs vs 57 pickups (Oct 2019), rate code 3 = 0.24% of trips; HVFHV: 63,278 vs 228 (Jun 2021); return toll $14.79-16.79 E-ZPass | medium | [P] Own counts; [S] PANYNJ 2026 tolls | rule | Yes | TLC records; PANYNJ | EWR zone = drop-off only for NYC-licensed cars; forced deadhead with inbound toll |

### 5.8 Out-of-city trips and the empty return

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-057** Out-of-city trip share | Share of trips ending outside NYC (NJ, Westchester, Nassau, Long Island, Connecticut). | HVFHV Jun 2021: 3.67% end outside NYC (zone 265) + 0.42% at EWR. Yellow Oct 2019: rate code 4 (Nassau/Westchester) 0.08%, negotiated (code 5) 0.17%, Newark (code 3) 0.24% | medium | [P] Own computation | world | No (hidden) | TLC trip records | OD matrix includes external destination nodes by county |
| **R01-058** Out-of-city fare and pay rules | How trips leaving the city are priced and paid, which decides whether the empty return is compensated (amounts owned by R07). | Yellow: meter to the city line, then double meter beyond for Westchester/Nassau [U]; other places negotiated flat fare; rider pays tolls both ways for Westchester/Nassau [S]. HVFHV minimum pay from 1 Mar 2026: in-city $1.283/mi + $0.681/min (non-WAV); out-of-town $1.757/mi (non-WAV), $2.193/mi (WAV), $0.725/min | medium | [S] TLC driver-pay-rates page; TLC fare page; TLC: out-of-town formula pays for time returning without a passenger | rule | Yes | TLC driver pay rates (https://www.nyc.gov/site/tlc/about/driver-pay-rates.page) | Fare-engine branch when the destination is outside the NYC polygon |
| **R01-059** Empty-return distance and legality | After an out-of-city drop-off the driver normally returns to NYC empty, because pickups outside the city need a local licence. | Return 10-60+ km; street hails outside NYC not allowed; app pickups outside NYC depend on NJ / county licensing [U] | high | [P] Near-zero pickups at EWR and zone 265 in TLC records; [U] county licensing details | rule | Yes | TLC records; county taxi/limousine rules [U] | Compute deadhead route back to the city line or home; charge time, energy and inbound toll |
| **R01-060** Night outward drift | At night more trips leave the core for residential outer boroughs, leaving drivers far from demand. | Share of core yellow pickups ending in outer boroughs: 1.4% at 8am, 9.5% at 10pm, 13.1% at midnight, 17.7% at 4am (Oct 2019) | high | [P] Own computation, TLC yellow Oct 2019 | world | Public / forecast | TLC trip records | Emerges from hour-specific OD matrices; makes 'go home after last trip' and repositioning decisions matter |

### 5.9 Driver home, depots and amenities

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-061** Driver home location | Where the driver lives, which sets the start and end commute and the 'take me home' preference. | Zone ID sampled from a driver-residence distribution (mostly Queens, Brooklyn, Bronx; some NJ / Long Island) [U] | medium | [U] Residence distribution not verified (search budget used up) | setting | Yes | None verified; TLC licensee data if published [U] | Home node per driver; unpaid commute at shift start and end |
| **R01-062** Distance and time to home | Live network distance from the car to home; near shift end it decides whether to accept a trip or use a destination filter. | 0-40 km; destination-filter uses per day (Uber historically 2/day) [U] | medium | [U] Background knowledge of platform destination filters | state | Yes | Derived from road graph | Recompute each step; 'take me home' mode biases matching toward trips ending near home |
| **R01-063** Garages, depots and shift-change points | Yellow cab garages and robotaxi depots are where shifts start or end and cars are cleaned or charged, adding deadhead. | Garage zone; two-shift taxis change around 4-5pm [U]; robotaxi depot locations set by scenario | medium | [U] Background knowledge; [design] for robotaxi depots | setting | Yes | None found | Depot nodes; mandatory returns for shift change, charging or cleaning |
| **R01-064** Fuel station locations | Where gas stations are and the detour to reach them; Manhattan has few. | Stations per borough; detour 0-15 min | low | [U] Background knowledge | world | Yes | OSM amenity=fuel | POI layer; refuel action routes to the nearest station |
| **R01-065** EV charger locations, power and access | Location, speed and availability of chargers (public, curbside, fleet-only hubs), which set detour and downtime for EVs. | DC fast 50-350 kW; Level 2 7-19 kW; NYC DOT curbside chargers; fleet hubs | medium | [S] TLC license reviews weigh EV charging availability; [U] charger mix | world | Yes | AFDC station locator (https://afdc.energy.gov/stations) | Charger POIs with ports, power and queues; charge action (R08) |
| **R01-066** Restrooms, food and break spots | Where a driver can take a legal break with a toilet and food, which affects break length and dead time. | Public restroom POIs; 113 relief stands; break detour 0-20 min | low | [S] WNYC 'Relief in short supply for the city's taxi drivers'; [U] | world | Yes | NYC Parks public restrooms (NYC Open Data) [U]; OSM amenity=toilets | Break action needs a nearby POI; cost = detour + dwell |

### 5.10 Neighbourhood economics and safety

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-067** Neighbourhood income | Median household income of pickup and drop-off areas, which tracks card use, trip length and tipping. | ACS median income per tract mapped to zone; card-trip tip/fare 25.9% for Yellow Zone pickups vs 19.3% outer boroughs; lowest drop-off zones 18.8-19.2% (Stuyvesant Heights, Central Harlem North, Crown Heights North) vs ~27% (UES, UWS, West Village) | medium | [P] Own computation, yellow Oct 2019 card trips (tips are recorded only for card payments) | world | Yes | US Census ACS; TLC tips (yellow card trips; HVFHV tips column) | Zone covariate for tip probability and size (behaviour owned by R05) |
| **R01-068** Payment mix by zone | Share of cash vs card trips by area; affects recorded tips and cash handling for taxis (app trips are cashless). | Card share, yellow Oct 2019: Yellow Zone 74.2%, upper Manhattan 58.8%, outer boroughs 51.7%, airports 64.7% | low | [P] Own computation | world | No (hidden) | TLC yellow payment_type | Per-zone payment-type probability |
| **R01-069** Perceived safety and crime | Crime and drivers' sense of risk make some drivers avoid areas at night, thinning supply there and raising surge for those who stay, with a small real incident risk. | Complaints per 1,000 residents by precinct and hour; avoidance probability 0-1 [design] | low | [U] / [design]; benchmark must not reward illegal refusal | world | Public / forecast | NYPD Complaint Data (NYC Open Data) | Lower competitor supply in high-perceived-risk zones at night; small incident probability |
| **R01-070** Geographic refusal rules | Taxis must take passengers to any destination in the city, so the agent cannot legally refuse by neighbourhood; app drivers can decline but acceptance rate counts against them. | Taxi refusal = violation and fine [U]; app accept/decline with destination shown [U] | medium | [U] TLC rules not re-verified here | rule | Yes | TLC rules (https://www.nyc.gov/site/tlc/about/tlc-rules.page) | Block destination-based refusal for taxis; track acceptance for app drivers (R06/R07) |

### 5.11 Index: who it applies to, component, priority

| ID | Variable | Applies to | Component | Priority |
|---|---|---|---|---|
| R01-001 | Taxi zone partition | all | Map & road network | core |
| R01-002 | Service-zone class | all; decisive for taxi | Map & road network | core |
| R01-003 | Pickup concentration (spatial skew) | all | Demand generator | core |
| R01-004 | Zone pickup/drop-off imbalance | all; strongest for taxi | Demand generator | core |
| R01-005 | Taxi vs app geographic footprint | taxi, human app driver, robotaxi | Demand generator | core |
| R01-006 | Green taxi hail exclusionary zone | taxi (green) | Regulation, fees & taxes | core |
| R01-007 | Licensing jurisdiction boundary | all | Regulation, fees & taxes | core |
| R01-008 | Robotaxi operating geofence (ODD) | robotaxi, fleet | Map & road network | core |
| R01-009 | Spatial resolution | all | Benchmark harness | core |
| R01-010 | Zone adjacency and travel-time skim | all; fleet | Map & road network | core |
| R01-011 | Repositioning target (where to wait or cruise) | all; fleet (per car) | Driver state | core |
| R01-012 | Road hierarchy class | all | Map & road network | core |
| R01-013 | One-way streets and circuity | all | Map & road network | core |
| R01-014 | Turn restrictions | all; robotaxi must obey exactly | Map & road network | extended |
| R01-015 | Speed limits | all; matters most for robotaxi | Map & road network | extended |
| R01-016 | Enforcement camera locations | human app driver, taxi | Regulation, fees & taxes | stretch |
| R01-017 | Road access by vehicle class | robotaxi; all | Map & road network | extended |
| R01-018 | Elevation and grade | all; EV range | Vehicle & energy | stretch |
| R01-019 | River crossings as chokepoints | all | Map & road network | core |
| R01-020 | MTA bridge and tunnel tolls | all | Regulation, fees & taxes | core |
| R01-021 | Port Authority Hudson crossing tolls | all | Regulation, fees & taxes | core |
| R01-022 | Congestion Relief Zone (CRZ) | all; robotaxi fleet pays as TLC vehicle or daily toll | Regulation, fees & taxes | core |
| R01-023 | State congestion surcharge zone (96th St line) | all | Regulation, fees & taxes | core |
| R01-024 | Fee-avoiding route choice | all; router for robotaxi | Traffic & travel time | extended |
| R01-025 | Curb regulation at the stop point | all; robotaxi must comply exactly | Map & road network | extended |
| R01-026 | Rider-driver rendezvous time | all; longer for robotaxi (rider walks to car) | Rider behaviour | core |
| R01-027 | Bus lanes | all | Regulation, fees & taxes | extended |
| R01-028 | Busways and transit-priority streets | all | Map & road network | extended |
| R01-029 | Car-free park drives and plazas | all | Map & road network | extended |
| R01-030 | Taxi stands and hotel queues | taxi | Demand generator | extended |
| R01-031 | Taxi/FHV relief stands | human app driver, taxi | Map & road network | extended |
| R01-032 | Legal waiting spots (staging) | all; robotaxi needs staging lots | Map & road network | extended |
| R01-033 | Robotaxi pickup-point placement | robotaxi | Rider behaviour | extended |
| R01-034 | Pedestrian volume by location | taxi (hails); all | Demand generator | core |
| R01-035 | Pedestrian demand class of each street | all | Map & road network | core |
| R01-036 | Subway entries and exits by hour | all | Demand generator | extended |
| R01-037 | Road-to-pedestrian ratio ('pickup-ability') | all | Map & road network | extended |
| R01-038 | Transit accessibility | human app driver, robotaxi | Demand generator | extended |
| R01-039 | Population and job density | all | Demand generator | extended |
| R01-040 | Hail visibility by street type | taxi | Demand generator | extended |
| R01-041 | Cruising route for street hails | taxi; robotaxi with street hail (none today) | Driver state | extended |
| R01-042 | Land-use mix per zone | all | Demand generator | core |
| R01-043 | Office and business districts | all | Demand generator | core |
| R01-044 | Nightlife density | all | Demand generator | extended |
| R01-045 | Tourist and hotel density | all | Demand generator | extended |
| R01-046 | Hospitals, universities and institutions | all | Demand generator | extended |
| R01-047 | Venues, stadiums and convention centres | all | Events & disruptions | core |
| R01-048 | Retail and shopping corridors | all | Demand generator | stretch |
| R01-049 | Intercity rail and bus hubs | all | Demand generator | core |
| R01-050 | Airport trip share and value | all | Demand generator | core |
| R01-051 | Airport pickup/drop-off asymmetry | taxi, human app driver | Demand generator | core |
| R01-052 | Airport holding-lot queue | all | Competitor supply & matching | core |
| R01-053 | Airport queue decision | all | Driver state | core |
| R01-054 | Airport fare and fee triggers | all | Pricing & platform rules | core |
| R01-055 | Airport terminal layout and pickup rules | all; robotaxi airport access needs Port Authority approval [U] | Map & road network | extended |
| R01-056 | Newark Airport (EWR) special status | all | Regulation, fees & taxes | core |
| R01-057 | Out-of-city trip share | all | Demand generator | core |
| R01-058 | Out-of-city fare and pay rules | human app driver, taxi; robotaxi pricing is a setting | Pricing & platform rules | core |
| R01-059 | Empty-return distance and legality | all | Traffic & travel time | core |
| R01-060 | Night outward drift | all; taxi most | Demand generator | core |
| R01-061 | Driver home location | human app driver, taxi | Driver state | core |
| R01-062 | Distance and time to home | human app driver, taxi | Driver state | core |
| R01-063 | Garages, depots and shift-change points | taxi, robotaxi, fleet | Fleet manager | extended |
| R01-064 | Fuel station locations | gas vehicles | Vehicle & energy | extended |
| R01-065 | EV charger locations, power and access | EV drivers, robotaxi, fleet | Vehicle & energy | core |
| R01-066 | Restrooms, food and break spots | human app driver, taxi | Driver state | stretch |
| R01-067 | Neighbourhood income | all | Rider behaviour | extended |
| R01-068 | Payment mix by zone | taxi | Rider behaviour | stretch |
| R01-069 | Perceived safety and crime | human app driver, taxi; robotaxi (vandalism) | Competitor supply & matching | extended |
| R01-070 | Geographic refusal rules | taxi, human app driver | Regulation, fees & taxes | core |

## 6. Key interactions with other domains

- **R01 x R02 (time):** land-use mix sets each zone's daily profile; night outward drift (1.4% of core trips go to outer boroughs at 8am vs 17.7% at 4am) and airport and hub pulses are time-specific. Zone attributes should be stored as zone x hour tables.
- **R01 x R03 (events):** venues (R01-047), hubs and bridges are where events strike. Subway outages near high-ridership stations (R01-036) and bridge or tunnel closures (R01-019) are the geographic hooks for disruptions. With versus without public event info should be tested on these fixed POIs.
- **R01 x R04 (weather):** rain raises hail demand most on high-pedestrian streets (R01-034) and slows curb pickups (R01-026). Low-lying highways (FDR, Belt Parkway) can flood [U]. Grade matters for EV range in snow [U].
- **R01 x R05 (riders):** population, jobs and transit access drive demand. Neighbourhood income moves card use and tips (25.9% vs 19.3% tip/fare). Walk distance to a robotaxi pickup point drives cancellations.
- **R01 x R06 (competition and matching):** concentration and imbalance set how crowded hot zones get. Fréchette, Lizzeri and Salz (2019) find increasing returns to scale in taxi matching and that platform competition reduces effective density [S]. Buchholz (2022) shows competition spreads taxis away from the densest pedestrian areas [S]. Airport queue length depends on competitor supply.
- **R01 x R07 (fares and rules):** polygons trigger charges (CRZ, 96th St line, airports, EWR, out-of-town pay, hail exclusion). R07 owns the amounts and R01 owns the polygons and triggers.
- **R01 x R08 (vehicle and energy):** charger and fuel locations, grades, deadhead distance, tolls on empty returns.
- **R01 x R09 (driver and decisions):** repositioning, airport queue, cruising route and go-home decisions are geographic. Haggag, McManus and Paci (2017) show productivity gains from neighbourhood-specific experience [S]. This directly supports the "learn over 10 days, test on day 11" evaluation.
- **R01 x R10 (traffic and routing):** road hierarchy, one-way grid, turn bans and chokepoints form the graph that R10 loads with congestion. CRZ effects on speeds belong in R10.
- **R01 x R11 (fleet):** the zone adjacency and travel-time skim (R01-010), depots (R01-063) and the geofence (R01-008) are the fleet rebalancing substrate.
- **R01 x R12 (benchmark settings):** spatial resolution (R01-009), whether historic heatmaps and PU/DO ratios are given as public info, and the replay period (2019 vs 2025+ with the CRZ) are harness settings.

## 7. Public data sources

| Source | What it gives R01 | URL | Access from this session |
|---|---|---|---|
| TLC trip records (yellow, green, FHV, HVFHV; monthly Parquet) | Zone-level OD, fares, tips, tolls, airport fees; HVFHV request, on-scene and pickup times, driver pay | https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page | Blocked; GitHub copies used (https://github.com/DataTalksClub/nyc-tlc-data/releases) |
| TLC taxi zone lookup and shapefile | 263 zones, borough, service zone | NYC Open Data 755u-8jsi, https://data.cityofnewyork.us/d/755u-8jsi | Lookup read via GitHub copy [P] |
| MTA CBD taxi zones | Which zones are in the Congestion Relief Zone | https://catalog.data.gov/dataset/mta-central-business-district-taxi-zones | Snippet only |
| NYC DOT Bi-Annual Pedestrian Counts | Pedestrian volume at 114 locations, May and Sept | https://data.cityofnewyork.us/d/2de2-6x2h | Snippet only |
| NYC DOT Pedestrian Mobility Plan, Pedestrian Demand | Five pedestrian-demand classes for every street | https://catalog.data.gov/dataset/pedestrian-mobility-plan-pedestrian-demand | Snippet only |
| MTA Subway Hourly Ridership (2017-19, 2020-24, 2025+) and OD estimates | Station-hour entries; OD flows | https://data.ny.gov/d/5wq4-mkjj (2025+), wujg-7c2s, t69i-h2me, jsu2-fbtj | Snippet only |
| NYC DOT Taxi and FHV relief stands | 113 legal one-hour break spots | https://catalog.data.gov/dataset/taxi-and-for-hire-vehicle-fhv-relief-stands | Snippet only |
| NYC DCP LION street centerline | Street width, lanes, one-way direction, road class | https://www.nyc.gov/site/planning/data-maps/open-data/dwn-lion.page | Not opened [U] |
| NYC DCP MapPLUTO | Land use per tax lot | https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page | Not opened [U] |
| OpenStreetMap | Drivable graph, one-way, turn restrictions, maxspeed, fuel, toilets, POIs | https://www.openstreetmap.org (extracts via https://download.geofabrik.de) | Not opened |
| US Census ACS 5-year; LEHD LODES | Population, income, jobs per tract/block | https://data.census.gov ; https://lehd.ces.census.gov/data/ | Not opened |
| AFDC station locator | EV charger locations and power | https://afdc.energy.gov/stations | Not opened |
| MTA GTFS static; NJ Transit, Amtrak GTFS | Station locations; train arrival schedules for hub pulses | https://new.mta.info/developers | Not opened |
| NYPD Complaint Data | Crime by precinct and time, for perceived-safety layer | NYC Open Data (NYPD Complaint Data Historic / Current) | Not opened |
| MTA and PANYNJ toll schedules | Crossing tolls by direction and payment | https://www.mta.info/fares-tolls/tolls ; https://www.panynj.gov/bridges-tunnels | Blocked; snippets |
| TLC fare and driver-pay pages | Airport rules, surcharges, out-of-town pay rates | https://www.nyc.gov/site/tlc/passengers/taxi-fare.page ; https://www.nyc.gov/site/tlc/about/driver-pay-rates.page | Blocked; snippets |

## 8. Open questions

1. **Replay period:** pre-pandemic 2019 (stable, no CRZ) or 2025+ (CRZ live, current mix, a `cbd_congestion_fee` field)? The answer changes zone shares and speeds.
2. **Spatial resolution:** should version 1 stay at taxi-zone level with random intra-zone points, or route on an OSM graph from the start? Curb, hail-visibility and pickup-ability variables need the graph.
3. **Robotaxi city:** NYC has no robotaxi passenger service (Waymo test permits expired 31 Mar 2026). Should the robotaxi track use a hypothetical NYC geofence, or a second city with real robotaxi service (San Francisco, Phoenix) where trip data are scarcer?
4. **Rendezvous time:** confirm that HVFHV `on_scene_datetime` is populated well enough to fit per-zone pickup dwell (R01-026). I could not read the data dictionary.
5. **Out-of-city pickups:** can NYC TLC app drivers legally accept pickups in NJ, Westchester or Nassau (for example after an EWR drop-off)? This sets how harsh the empty return is. Not verified.
6. **Current amounts not verified:** MTA car E-ZPass toll after 4 Jan 2026; Newark taxi surcharge; speed-camera operating hours; yellow "double meter" rule beyond the city line.
7. **Driver home distribution:** is there a public source for TLC driver residence by ZIP or borough? Without one, "take me home" scenarios rest on a design guess.
8. **Street-level hail calibration:** yellow records before mid-2016 carry exact coordinates [U]. Should they be used to calibrate street-level hail rates (R01-040), given that demand has since shifted?
9. **Hidden vs visible:** should the agent get historic zone heatmaps and PU/DO ratios as "public information"? They are public data, but providing them changes what the benchmark measures (learning vs using a map).
10. **Generalisation:** for other cities, the TLC-zone, service-zone and NYC-polygon rules must be replaced by local equivalents. Keep the R01 schema generic (zones, polygons with rule triggers, POI layers, crossing edges).

## 9. Sources

- [P] TLC taxi zone lookup (taxi_zone_lookup.csv), GitHub copy: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv (read directly; 265 rows counted).
- [P] TLC yellow trip records Oct 2019, green Oct 2019, HVFHV Jun 2021, GitHub copies at https://github.com/DataTalksClub/nyc-tlc-data/releases (own computation; scripts in session scratchpad).
- [S] MTA, Taxis and For-Hire Vehicles (Congestion Relief Zone): https://www.mta.info/fares-tolls/tolls/congestion-relief-zone/taxi-fhv-tolls ; About the CRZ toll: https://www.mta.info/fares-tolls/tolls/congestion-relief-zone/about
- [S] TLC industry notices 24-06 and 24-10 (CBD per-trip charges): https://www.nyc.gov/assets/tlc/downloads/pdf/industry-notices/industry_notice_24_10_english.pdf
- [S] ABC7 on toll phases ($9 to 2027, $12 2028-30, $15 2031; $2.25 overnight): https://abc7ny.com/post/congestion-pricing-nyc-mta-board-votes-approve-plan-lower-toll/15555885/
- [S] TLC taxi fare page: https://www.nyc.gov/site/tlc/passengers/taxi-fare.page
- [S] TLC driver pay rates (effective 1 Mar 2026): https://www.nyc.gov/site/tlc/about/driver-pay-rates.page ; TLC driver pay for drivers: https://www.nyc.gov/site/tlc/about/driver-pay-drivers.page
- [S] FHV airport fee $2.50: https://www.visaverge.com/news/newark-kennedy-laguardia-airports-lead-most-expensive-drop-off-fees/ ; https://www.fox5ny.com/news/nyc-taxi-uber-lyft-fhv-surcharges-fees
- [S] TLC Boro Taxi hail-zone decal rule: https://www.nyc.gov/assets/tlc/downloads/pdf/newly_passed_rule_boro_taxi_decal.pdf ; green cab page: https://www.nyc.gov/site/tlc/businesses/green-cab.page
- [S] Waymo NYC permits expired 31 Mar 2026: https://www.westsidespirit.com/news/waymo-s-robot-car-testing-ends-in-nyc-after-permits-expire-GF5755668 ; https://jalopnik.com/2142643/waymo-stopped-testing-robotaxis-nyc/
- [S] TLC license pause report Feb 2026: https://www.nyc.gov/assets/tlc/downloads/pdf/license-pause-report-2026-02.pdf
- [S] NYC DOT parking sign legend: https://www.nyc.gov/html/dot/downloads/pdf/parking-regulations-sign-legend.pdf ; NYC DOF violation codes: https://www.nyc.gov/site/finance/vehicles/services-violation-codes.page
- [S] NYC DOT bus lane rules: https://www.nyc.gov/html/brt/html/about/bus-lanes.shtml ; TLC bus/bike lane brochure: https://www.nyc.gov/assets/tlc/downloads/pdf/bus_bike_aves_broch_18_taxi.pdf
- [S] 14th St busway: https://thevillagesun.com/14th-st-busway-study-finds-faster-speeds-scant-impact-but-drivers-already-flouting-rules ; NYC DOT busways: https://www.nyc.gov/html/brt/html/busways/busways.shtml
- [S] NYC DOT relief stands: https://www.nyc.gov/html/dot/html/motorist/taxirelief.shtml ; MCB1 letter (113 stands by borough): https://rules.cityofnewyork.us/wp-content/uploads/2026/07/MCB1-Opposition-to-Int-1000-2024.pdf
- [S] Central Park car-free: https://abc7ny.com/society/central-park-goes-car-free-as-traffic-ban-takes-effect/3657602/
- [S] Sammy's Law and speed limits: https://nyc.streetsblog.org/2026/10/08/17-community-board-resolutions-passed-sammys-law-dot-implementation ; https://www.westsidespirit.com/news/city-to-reduce-all-school-zone-speed-limits-to-15-mph-by-2029-EF5676565
- [S] PANYNJ 2026 tolls: https://www.roi-nj.com/2026/01/05/transportation/higher-gas-taxes-e-zpass-costs-greet-new-jersey-residents-in-new-year/ ; https://www.panynj.gov/content/dam/bridges-tunnels/truckers-guides/Truckers%20Guide_Eng_Apr%202026.pdf
- [S] MTA franchise bus tolls (rates from 4 Jan 2026): https://www.mta.info/fares-tolls/tolls/vehicle-types/franchise-buses
- [S] Uber JFK driver information (FIFO queue, lots, 3-hour limit, T5/T7): https://www.uber.com/global/en/r/airports/jfk/driver-information
- [S] JFK taxi hold waits: https://nbcnewyork.com/news/local/port-authority-jfk-taxi-scheme-fare-cut-line-bribe-arrest-court/1475097 ; Chris Whong airport analysis: https://blog.chriswhong.com/?p=838
- [S] Yazici, Kamga, Singhal (2016), Modeling taxi drivers' decisions for improving airport ground access: JFK case, TR-A 91: https://ideas.repec.org/a/eee/transa/v91y2016icp48-60.html
- [S] Fréchette, Lizzeri, Salz (2019), Frictions in a Competitive, Regulated Market: Evidence from Taxis, AER 109(8): https://www.aeaweb.org/doi/10.1257/aer.20161720
- [S] Buchholz (2022), Spatial Equilibrium, Search Frictions and Dynamic Efficiency in the Taxi Industry, REStud 89(2): https://nbuchholz.scholar.princeton.edu/research
- [S] Haggag, McManus, Paci (2017), Learning by Driving, AEJ Applied 9(1): https://openicpsr.org/openicpsr/project/113636/version/V1/view
- [S] Schaller (2017), Empty Seats, Full Streets: https://schallerconsult.com/rideservices/emptyseats.htm (figures via news coverage)
- [S] Correa, Chow, Ozbay, spatial-dynamic matching equilibrium of NYC taxi and Uber: https://engineering.nyu.edu/news/spatial-dynamic-matching-equilibrium-models-new-york-city-taxi-and-uber-markets
- [S] NYC DOT Bi-Annual Pedestrian Counts: https://data.cityofnewyork.us/Transportation/Bi-Annual-Pedestrian-Counts/2de2-6x2h/about
- [S] Pedestrian Mobility Plan: https://www.nyc.gov/html/dot/html/pedestrians/pedestrian-mobility.shtml ; MIT critique: https://www.fastcompany.com/91492342/mit-foot-traffic-model-nyc
- [S] MTA Subway Hourly Ridership catalog entries: https://catalog.data.gov/dataset/mta-subway-hourly-ridership-beginning-2025
- [S] WNYC, Relief in short supply for the city's taxi drivers: https://wnyc.org/story/103759-taxi-comfort-stations/
- [U] Background knowledge: Manhattan one-way grid and two-way crosstown streets; parkway access; Verrazzano one-way toll; anti-idling limits; destination filters; garage shift changes; double meter beyond city line; driver residence pattern; pre-2016 yellow coordinates.
