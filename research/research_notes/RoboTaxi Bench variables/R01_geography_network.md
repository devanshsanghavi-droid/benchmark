# R01: Geography, land use and the road network

RoboTaxi Bench simulation variables, domain R01 of 12. Research dossier, October 2026. Default city: New York City.

## 1. Summary

NYC geography is very uneven: in October 2019, 16 of the city's 263 taxi zones produced half of all yellow-cab pickups and 89% came from the 55-zone Manhattan core, while app (HVFHV) pickups needed 60 zones for half and were 59.5% outer-borough (June 2021), so the same map rewards different positioning for a taxi, an app driver and a robotaxi. The biggest geographic profit drivers are where demand concentrates and where drop-offs strand the driver: Brooklyn and the Bronx receive about four yellow drop-offs per pickup, and the share of core trips heading to outer boroughs rises from 1.4% at 8am to 17.7% at 4am. Airports are a high-stakes special case: they were 7.9% of yellow trips but 22.2% of driver revenue, yet holding-lot waits have been reported at 2-3 hours [uncertain: not re-checked] and Newark is drop-off-only for NYC cars (taxi riders pay a $20 surcharge and tolls both ways). Rules tied to places matter as much as roads: the green-taxi hail exclusion zone, the Congestion Relief Zone (Manhattan at or below 60th St; $0.75 per taxi trip, $1.50 per HVFHV trip), the 96th St surcharge line, inbound-only Hudson tolls ($16.79 peak), airport fees and out-of-town pay rates. The user's idea of comparing road density with foot-traffic density becomes a 'pickup-ability' index (stoppable curb vs pedestrians), built from NYC DOT pedestrian counts, the Pedestrian Mobility Plan street classes and MTA hourly subway ridership. Robotaxi geography in NYC is hypothetical (Waymo's test permits for Manhattan south of 112th St and Downtown Brooklyn, with no passengers, expired on 31 March 2026), so the geofence should be a benchmark setting. The dossier lists 70 variables in 10 sub-boxes (16 high, 34 medium, 20 low impact; 39 core), from zone structure to restroom access. [corrected by fact-check: originally 19 high, 32 medium, 19 low; four ratings changed] Many headline numbers are my own computations on TLC trip records, while official fee and rule pages were readable only through search snippets. [corrected by fact-check: the TLC and DOT rules were since checked against a verbatim GitHub copy of the Rules of the City of New York and the NYC Administrative Code; see the fact-check log]

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

[Fact-check note: every figure in this table was reproduced from the same files with the same cleaning filter (trip 1 min-4 h, fare $0-500, distance 0-150 mi). A lighter filter that keeps zero-distance trips shifts a few values: JFK PU/DO 3.53, yellow EWR pickups 829, 49 zones for 95% of pickups; the patterns hold.]

Driver revenue = fare + extras + tip (tips only recorded for card trips). In-trip revenue per hour is similar everywhere, so the profit gap between areas comes from empty time between trips, which these records cannot show without driver IDs. The simulator has to model that gap through the imbalance, queue and deadhead variables below.

## 4. Box view (the placeholder list, extended)

* Geography, land use and road network (R01)
   * Zones and service areas
      * R01-001 Taxi zone partition [medium impact]
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
      * R01-019 River crossings as chokepoints [medium impact]
      * R01-020 MTA bridge and tunnel tolls [medium impact]
      * R01-021 Port Authority Hudson crossing tolls [medium impact]
      * R01-022 Congestion Relief Zone (CRZ) [medium impact]
      * R01-023 State congestion surcharge zone (96th St line) [low impact]
      * R01-024 Fee-avoiding route choice [low impact]
   * Curb access and restricted streets
      * R01-025 Curb regulation at the stop point [medium impact]
      * R01-026 Rider-driver rendezvous time [low impact]
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
      * R01-059 Empty-return distance and legality [medium impact]
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
| **R01-001** Taxi zone partition | The city is split into the TLC's 263 taxi zones (plus 2 unknown codes), the spatial unit of every public trip record. | 263 zones: Manhattan 69, Queens 69, Brooklyn 61, Bronx 43, Staten Island 20, EWR 1; IDs 264/265 = unknown / outside NYC [corrected by fact-check: in the current TLC lookup 264 = Unknown and 265 = 'Outside of NYC'; older copies label both Unknown (NV / NA)] | medium | [P] Counted 265 rows in taxi_zone_lookup.csv (GitHub copy of the TLC file; borough and service-zone counts reproduced); all trip data is keyed to these IDs; [S] dataset ID 755u-8jsi confirmed by many GitHub pipelines that download it [corrected by fact-check: impact high -> medium; the partition is a structural layer whose profit effect flows through R01-003, R01-004 and R01-009] | world | Yes | NYC Taxi Zones, NYC Open Data 755u-8jsi (https://data.cityofnewyork.us/d/755u-8jsi); TLC lookup + shapefile (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | Load zone polygons; map every car and request position to a zone ID; demand, fares and stats keyed by zone |
| **R01-002** Service-zone class | Each zone belongs to a TLC service class that decides who may street-hail there and which fare rules apply. | Yellow Zone 55 (Manhattan core) / Boro Zone 205 (14 upper Manhattan + 191 outer borough) / Airports 2 (JFK 132, LGA 138) / EWR 1 | high | [P] Lookup counts; 89.0% of yellow pickups were in the 55 Yellow Zone zones (Oct 2019, own computation) | rule | Yes | Same as R01-001 (service_zone column) | Zone attribute checked by hail-eligibility and fare rules |
| **R01-003** Pickup concentration (spatial skew) | How unevenly trip origins are spread across zones; the more concentrated, the more location choice matters. | Yellow Oct 2019: 16 zones = 50% of pickups, 32 = 80%, 48 = 95%; HVFHV Jun 2021: 60 / 125 / 188 zones | high | [P] Own computation on TLC yellow (Oct 2019, 7.08M trips) and HVFHV (Jun 2021, 14.96M trips) records | world | Public / forecast | TLC trip records (yellow, green, FHV, HVFHV) | Demand generator samples origins from a zone x hour intensity fitted to trip records; historic heatmap can be given to the agent as public info |
| **R01-004** Zone pickup/drop-off imbalance | Ratio of pickups to drop-offs per zone; zones well below 1 are 'sinks' where a driver lands with few nearby requests. | Yellow Oct 2019 PU/DO: Manhattan 1.02, Queens 1.30, Brooklyn 0.27, Bronx 0.24, Staten Island 0.14; zone extremes JFK 3.81, Windsor Terrace 0.08, Washington Heights North 0.09 [corrected by fact-check: Windsor Terrace, not Washington Heights North, is the lowest zone with >3,000 drop-offs; JFK is 3.53 under a lighter cleaning filter that keeps zero-distance trips]. HVFHV Jun 2021: every borough 1.02-1.06 | high | [P] Own computation, TLC yellow Oct 2019 and HVFHV Jun 2021 (reproduced by fact-check) | world | Public / forecast | TLC trip records | Emerges from the OD matrix; expose historic PU/DO ratio per zone x hour as a public layer |
| **R01-005** Taxi vs app geographic footprint | Street-hail demand sits in the Manhattan core while app demand is spread over the outer boroughs, so the same map rewards different positioning by driver type. | Share of pickups in Yellow Zone: yellow 89.0% vs HVFHV 32.2%; outer boroughs: 2.2% vs 59.5%. Manhattan HV trips fell 6.1% Jan 2025 to Jan 2026 while other boroughs grew | high | [P] Own computation (yellow Oct 2019 vs HVFHV Jun 2021); [S] TLC license pause report Feb 2026 [uncertain: the -6.1% Manhattan figure from the Feb 2026 licence pause report was not re-checked; nyc.gov blocked] | world | Public / forecast | TLC trip records; TLC license pause reports (https://www.nyc.gov/assets/tlc/downloads/pdf/license-pause-report-2026-02.pdf) | Separate demand layers per channel (street hail, e-hail) with their own zone weights |
| **R01-006** Green taxi hail exclusionary zone | Green (boro) taxis may not accept street hails or e-hails in Manhattan south of E 96th St and W 110th St or at JFK and LGA, and may not begin base-dispatched (pre-arranged) trips in that part of Manhattan; they may drop off anywhere. [corrected by fact-check: the rule also bans pre-arranged starts in Manhattan south of E 96th / W 110th, and an e-hail counts as a hail] | Excluded: 55 Yellow Zone zones + 2 airports. Green Oct 2019 pickups: 64.6% outer boroughs, 32.3% upper Manhattan, 3.1% Yellow Zone; 18.5% of drop-offs in Yellow Zone; fine $500 plus suspension for a first violation | high | [P*] 35 RCNY 51-03 (Hail Exclusionary Zone and Pre-Arranged Exclusionary Zone definitions), 82-13 and 80-20(b)(11), read from a verbatim copy current through 13 Aug 2026; [P] own computation, green Oct 2019 (473,824 trips, reproduced) | rule | Yes | 35 RCNY 51-03 and 82-13 (verbatim copy https://github.com/jehiah/nyc_code_archive); TLC green cab page (https://www.nyc.gov/site/tlc/businesses/green-cab.page); TLC green trip records | Street-hail and e-hail generation disabled for green cars inside the excluded polygons; base-dispatched trips may not start in excluded Manhattan but may start at JFK/LGA [corrected by fact-check: the original said e-hail was still allowed] |
| **R01-007** Licensing jurisdiction boundary | The area where the vehicle's licence allows pickups (NYC for TLC vehicles); trips may end outside it, but pickups outside are effectively unavailable. | Inside five boroughs: pickups allowed. Outside: drop-off only. EWR: yellow 57 pickups vs 15,829 drop-offs (Oct 2019); HVFHV 228 vs 63,278 (Jun 2021). Uber JFK pickups only for TLC-licensed drivers | medium | [P] Own counts from TLC records; [S] Uber JFK driver-information page | rule | Yes | TLC trip records; Uber airport driver pages; county taxi rules [U] | Pickup-eligibility mask by polygon and licence type |
| **R01-008** Robotaxi operating geofence (ODD) | The polygon and road types where an autonomous vehicle is allowed and able to drive and serve riders. | Example: Waymo NYC test permit (Aug 2025 to 31 Mar 2026) covered Manhattan south of 112th St + Downtown Brooklyn, 8 cars, safety driver, no paying riders. Scenario options: core-only / core + airports / citywide | high | [S] Vital City Waymo map methodology (GitHub, 6 May 2026, citing THE CITY, CNBC and the Aug 2025 Mayor's Office release): 8 cars with safety drivers in Manhattan south of 112th St and Downtown Brooklyn, state testing permits expired 31 Mar 2026, NY law effectively bars driverless commercial service; [P*] 34 RCNY 4-17: an NYC test permit needs NYS DMV approval, a test operator in the driver's seat, DOT-approved areas and hours and a $5,000 yearly fee [uncertain: 'passenger service would need a TLC licence' not re-checked] | setting | Yes | 34 RCNY 4-17; Vital City waymo-map (https://github.com/vitalcity-nyc/waymo-map); no machine-readable NYC geofence found | Geofence polygon + road-class whitelist; requests outside are unservable or lost to competitors |
| **R01-009** Spatial resolution | The unit at which positions and demand are represented: taxi zone, hex grid or road segment. | Taxi zone (~3 km2 mean, 263 units) / H3 hex res 8 (~0.7 km2) / OSM drivable road graph (tens of thousands of nodes) | medium | [design] Finer resolution lets positioning skill show but costs compute and data; zone level matches public trip data | setting | Yes | TLC zones; OpenStreetMap (https://www.openstreetmap.org); NYC DCP LION | Start at zone level with a random point inside the zone; upgrade to a road graph for routing, curbs and hails |
| **R01-010** Zone adjacency and travel-time skim | A zone-to-zone neighbour list and travel-time matrix used for repositioning and fleet rebalancing. | 263 x 263 matrix of travel times by hour (minutes); neighbour lists | high | [design] Needed by both single-car repositioning and fleet rebalancing; R10 supplies the times | world | Yes | Derived from OSM graph + TLC trip durations; NYC DOT traffic speeds (cross-link R10) | Precompute skims per hour band; agent tools query ETA between zones |
| **R01-011** Repositioning target (where to wait or cruise) | The agent's choice of which zone or street to drive to, or wait in, when empty; the core geographic skill the benchmark measures. | Any reachable zone or road node; options: stay, cruise a loop (taxi only), drive to zone z, go to a hub or airport, go home [corrected by fact-check: 34 RCNY 4-11(b) bars vehicles other than taxis from cruising to search for passengers, so app cars and robotaxis may only wait legally or drive to a chosen spot] | high | [S] Haggag, McManus and Paci (2017, AEJ Applied 9(1):70-95; citation confirmed): neighbourhood-specific experience raises taxi driver productivity and changes search; Buchholz (2022, REStud 89(2):556-591): search frictions leave some areas unserved while others have excess cabs; [P*] 34 RCNY 4-11(b) cruising ban for non-taxis | agent | Yes | Logged from agent actions; benchmark compares with TLC-derived demand | Action space: reposition(zone or node), wait(here), cruise(route); travel time from R10 |

### 5.2 Road network structure

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-012** Road hierarchy class | Each road segment's class (expressway or parkway, arterial avenue, collector, local) sets its speed, capacity and how good it is for finding hails. | OSM highway = motorway / trunk / primary / secondary / tertiary / residential. Mean in-trip speed: ~10.2 mph for Yellow Zone pickups vs ~20.9 mph for airport pickups (yellow Oct 2019) | medium | [P] Own computation (distance / duration) from TLC yellow Oct 2019 | world | Yes | OpenStreetMap; NYC DCP LION street centerline (lanes, width, direction) | Graph edges carry class: free-flow speed and capacity; congestion handled in R10 |
| **R01-013** One-way streets and circuity | Manhattan's mostly one-way grid and the rivers make driving distance longer than straight-line distance, and a pickup on the wrong side costs a loop. | Most avenues and most cross streets one-way [corrected by fact-check: some avenues are two-way, e.g. Park Ave, Central Park West, West End Ave, York Ave [U]]; major two-way crosstown streets (14th, 23rd, 34th, 42nd, 57th, 72nd, 79th, 86th, 96th, 110th, 125th); circuity ~1.2-1.4; turn-around loop ~2-4 blocks | medium | [U] Background knowledge of the NYC grid; LION has a traffic-direction field | world | Yes | NYC DCP LION (TrafDir); OSM oneway tag | Directed graph; car heading matters for pickup ETA |
| **R01-014** Turn restrictions | Banned turns (many Midtown left turns, some by time of day) lengthen routes and ETAs. | Restricted turns per intersection; time windows such as 7am-7pm | low | [U] Background knowledge | rule | Yes | OSM turn-restriction relations; NYC DOT signage | Turn-restriction table in the router |
| **R01-015** Speed limits | Legal maximum per segment; caps free-flow speed (robotaxis obey exactly, humans may exceed). | Citywide default 25 mph; Sammy's Law lets the city set 20 mph streets and 10-15 mph school zones (all school zones 15 mph by 2029 planned); highways 40-50 mph | low | [P*] NYC Admin Code 19-177(a) and 34 RCNY 4-06(a): 25 mph unless signed otherwise; 19-177(d)-(e): 20 mph slow zones and 15-20 mph near schools; [S] Streetsblog (Oct 2026), West Side Spirit: Sammy's Law rollout [corrected by fact-check: the base limit is not in doubt; it is 25 mph by law] | rule | Yes | NYC DOT speed-limit data on NYC Open Data [U]; OSM maxspeed | Edge attribute; robotaxi speed = min(limit, traffic speed) |
| **R01-016** Enforcement camera locations | Where speed, red-light and bus-lane cameras are, which creates fine risk for human drivers. | Speed camera fine $50 (+$25 late); bus-lane fine $50 first offence rising to $250; cameras cover all bus lanes | low | [S] NYC DOT bus-lane rules; news coverage of speed cameras [uncertain: fine amounts, late fee and bus-lane camera coverage not re-checked; sources blocked] | rule | Public / forecast | NYC Open Data parking and camera violations [U] | Per-edge violation probability x fine, applied when the agent's driving style breaks rules |
| **R01-017** Road access by vehicle class | Some roads are closed to some vehicles: parkways ban commercial vehicles (taxis and FHVs count as passenger cars) and robotaxis may be kept off freeways. | Parkway allowed yes/no; robotaxi freeway allowed yes/no (scenario) | low | [U] Background knowledge; medium for robotaxi if freeways are excluded | rule | Yes | OSM access tags; NYSDOT parkway rules [U] | Edge mask per vehicle class |
| **R01-018** Elevation and grade | Hills slightly raise energy use; NYC is mostly flat with steep spots (Washington Heights, Staten Island, parts of the Bronx). | Grade 0-10%+; elevation 0 to ~125 m | low | [U] Background knowledge | world | Yes | USGS 3DEP; NYC 1-ft DEM on NYC Open Data [U] | Edge grade feeds an energy multiplier in R08 |

### 5.3 Chokepoints, tolls and charging zones

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-019** River crossings as chokepoints | Manhattan and Staten Island are islands and the Bronx is cut off from Manhattan and Queens by water, so most links between boroughs and all links to New Jersey are bridges or tunnels; they concentrate delay, incidents and tolls. [corrected by fact-check: Brooklyn and Queens share a land border and the Bronx joins Westchester by land, so bridges and tunnels are not the only links] | East River: Brooklyn, Manhattan, Williamsburg, Queensboro bridges (free), Queens-Midtown and Hugh Carey tunnels and RFK (tolled); Hudson: GWB, Lincoln, Holland (PANYNJ); Harlem River bridges free except the MTA Henry Hudson Bridge (tolled); Verrazzano, Throgs Neck, Whitestone, Cross Bay, Marine Pkwy (MTA, tolled); Staten Island to NJ: Goethals, Bayonne, Outerbridge (PANYNJ, tolled) [corrected by fact-check: added the Henry Hudson Bridge and the Staten Island-NJ crossings [U]] | medium | [P] 5.9% of yellow trips paid a toll, mean $6.63 (Oct 2019, own computation, reproduced); [U] network facts [corrected by fact-check: impact high -> medium; tolls are mostly passed to riders and crossing delay is modelled in R10] | world | Yes | OpenStreetMap; NYC DOT bridge traffic volumes [U] | Crossing edges with their own capacity, incident probability (R03) and travel-time variance (R10) |
| **R01-020** MTA bridge and tunnel tolls | Toll charged at MTA crossings, by crossing, payment type and direction. | Car E-ZPass at major crossings $6.55 until Aug 2023 and $6.94 from Aug 2023 (most common toll on yellow trip records), raised ~6% on 4 Jan 2026 [uncertain: 2026 car rate not checked]; smaller crossings (Henry Hudson, Cross Bay, Marine Pkwy) about half (bus E-ZPass $3.39 vs $6.42; a $3.18 car toll is common in 2023-24 records) [U]; East River bridges and the other Harlem River bridges free [corrected by fact-check: the Henry Hudson Bridge is tolled, so not all Harlem River crossings are free] | medium | [P*] tolls_amount in yellow 2023-24 records ($6.55 in Jul 2023; $6.94 in Sep 2023 and Jan 2024); [S] MTA franchise-bus toll page (rates effective 4 Jan 2026); news on ~6% E-ZPass rise; [P*] 35 RCNY 58-26(e)-(f): taxi passengers pay the actual E-ZPass toll, with directional rules on Cross Bay, Marine Pkwy and Verrazzano | rule | Yes | MTA tolls (https://www.mta.info/fares-tolls/tolls) | Toll table by crossing x direction x payment; passed to the rider when loaded, paid by the driver when empty |
| **R01-021** Port Authority Hudson crossing tolls | GWB, Lincoln and Holland charge only when entering New York, so a car returning empty from NJ pays; one-direction tolling (also Verrazzano, into Staten Island only [U]) makes return legs cost more than outbound legs. [corrected by fact-check: for yellow and green taxi trips to Newark, Westchester and Nassau the passenger must pay tolls to and from the destination (35 RCNY 58-26(c), (f)(2)), so the taxi's return toll is reimbursed; app drivers get the higher out-of-town pay rate instead] | Car E-ZPass $16.79 peak / ~$14.79 off-peak, toll-by-plate ~$23.05-23.30 [uncertain: toll-by-plate amount not checked] (from 4 Jan 2026); peak = weekdays 6-10am and 4-8pm, weekends 11am-9pm | medium | [S] ROI-NJ (Jan 2026); PANYNJ Truckers Guide (Apr 2026); [P*] yellow records show PANYNJ car tolls $14.75 / $12.75 (2023) and $15.38 / $13.38 (Jan 2024), consistent with yearly indexing to $16.79 / $14.79 in 2026 | rule | Yes | PANYNJ (https://www.panynj.gov/bridges-tunnels) | Inbound-only toll on NJ-to-NY crossing edges; charged to the driver on empty legs except where the passenger reimburses return tolls (taxi trips to EWR, Westchester, Nassau) |
| **R01-022** Congestion Relief Zone (CRZ) | Manhattan at or south of 60th St (excluding FDR Drive, West Side Highway / Route 9A and Hugh Carey Tunnel links) where each taxi/FHV trip to, from, within or through the zone pays a per-trip charge. | $0.75 per yellow, green or other FHV trip; $1.50 per HVFHV trip; since 5 Jan 2025; private cars $9 peak (2025-27), $12 (2028-30), $15 (2031), $2.25 overnight [uncertain: later phases and the overnight rate not re-checked]; unenrolled fleets pay a daily toll | medium | [S] MTA taxi/FHV toll page; several 2026 GitHub analyses agree on $0.75 taxi / $1.50 HVFHV / $9 peak from 5 Jan 2025 and treat the charge as still in force in 2026; [S] TLC trip-record dictionaries (Mar 2025) list cbd_congestion_fee 'starting Jan. 5, 2025' (via sibling dossier R07, read there as P*) | rule | Yes | MTA CBD taxi zones dataset (https://catalog.data.gov/dataset/mta-central-business-district-taxi-zones); cbd_congestion_fee field in 2025+ TLC trip records [S] | Polygon; flag trips whose route touches it (excluding exempt edges); rider-paid but shifts demand (R05) and speeds (R10) |
| **R01-023** State congestion surcharge zone (96th St line) | A second, larger zone: trips that begin, end or pass through Manhattan south of 96th St pay a state surcharge. | $2.50 yellow, $2.75 green and FHV, $0.75 shared ride | low | [P*] 35 RCNY 51-03: 'Congestion Zone' = Manhattan south of and excluding 96th St; [P*] amounts seen in trip records: yellow $2.50, green $2.75 (Oct 2019), HVFHV $2.75 and shared $0.75 (Jan 2023); [S] TLC taxi-fare page | rule | Yes | TLC fare page (https://www.nyc.gov/site/tlc/passengers/taxi-fare.page) | Second polygon; per-trip surcharge in the fare engine |
| **R01-024** Fee-avoiding route choice | Because the FDR and West Side Highway are outside the CRZ and some bridges are free, a route can avoid a charge at the cost of time. | k alternative routes per OD with toll and time trade-off | low | [S] CRZ exclusion list; [design] | agent | Yes | OSM graph + toll tables | Offer k-shortest paths with costs; agent or router chooses |

### 5.4 Curb access and restricted streets

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-025** Curb regulation at the stop point | The sign type at the curb decides whether a quick pickup or drop-off is legal. | No Parking (stop OK) / No Standing (quick passenger pickup OK, no waiting) / No Stopping (not allowed) / bus stop (OK if no bus is blocked) / taxi stand (taxis only; other cars may only briefly load, and TLC fines an FHV driver $350 for a first pickup at a taxi stand) / 'For-Hire Vehicles Only' curb ($115 if standing beyond a quick pickup [uncertain: fine amount not checked]) [corrected by fact-check: added the taxi-stand pickup ban for FHVs] | medium | [P*] 34 RCNY 4-11(c): taxis and FHVs may briefly stop to pick up or drop off where standing or parking is banned, within 12 in of the curb, but not where stopping is banned, in a bike lane or in a crosswalk; 34 RCNY 4-08(c)(1); 35 RCNY 80-19(d)(2); [S] NYC DOT parking sign legend; NYC DOF violation codes | rule | Yes | NYC DOT Parking Regulation Locations and Signs (NYC Open Data) [U] | Curb-segment attribute; illegal stop = fine probability or forced re-loop |
| **R01-026** Rider-driver rendezvous time | Minutes between the car arriving and the rider getting in, driven by building entrances, curb space, double parking and crowds. | Uber trips, Jan 2023: pickup minus on-scene time median 0.8 min, 75th percentile 1.8, 90th 2.0, 0.5% over 5 min (values bunch just above 2 min) [corrected by fact-check: the original said '0.5-5 min typical [U]'; Lyft (HV0005) records leave on_scene_datetime empty in 99.9% of trips] | low | [P*] Fact-check computation on HVFHV Jan 2023 (18.48M trips; fields request_datetime, on_scene_datetime and pickup_datetime confirmed) [corrected by fact-check: impact medium -> low for human drivers, about 1 min per trip; could be medium for robotaxis if riders must walk to the car [design]] | world | No (hidden) | TLC HVFHV trip records (request_datetime, on_scene_datetime, pickup_datetime) | Per-zone x hour lognormal dwell fitted from HVFHV records, added to each pickup |
| **R01-027** Bus lanes | Lanes reserved for buses (and Access-A-Ride vans) that other cars may enter only to make a right turn (through an intersection only within 200 ft of entering the lane), to reach the curb, or to quickly pick up or drop off passengers. [corrected by fact-check: the 200 ft limit applies to right turns, not to driveways only; 34 RCNY 4-12(m)] | Curbside pickup allowed; stopping in the centre of the lane not allowed; fines $50 rising to $250; cameras on all bus lanes | low | [P*] 34 RCNY 4-12(m)(1); [S] NYC DOT bus-lane rules; TLC bus/bike lane brochure [uncertain: fine schedule and camera coverage not re-checked] | rule | Yes | NYC DOT bus lanes (NYC Open Data) [U] | Lane attribute with hours; fine risk when misused |
| **R01-028** Busways and transit-priority streets | Streets where through car traffic is banned for set hours, but taxis and FHVs may enter for local pickups and must turn off at the next street. | 14th St busway (3rd to 9th Ave, 6am-10pm daily; cars may enter to pick up or drop off and must turn right within a block or two, no left turns) [corrected by fact-check: the original said 3rd to 8th Ave]; others such as Main St Flushing, Jamaica Ave, Archer Ave, 181st St [U]; 34th St bus priority (2025) | low | [P*] 34 RCNY 4-12(m)(2): only buses and Access-A-Ride vans during restricted hours except where signs allow; [S] NYT (Oct 2019, GitHub copy) and Village Sun / amNY on 14th St busway rules; NYC DOT 34th St documents | rule | Yes | NYC DOT busways page (https://www.nyc.gov/html/brt/html/busways/busways.shtml) | Edges with through-traffic ban + forced turn after a stop |
| **R01-029** Car-free park drives and plazas | Roads closed to cars inside demand areas, so pickups move to the edges and routes detour. | Central Park loop drives car-free since 27 Jun 2018 (transverses open); Prospect Park loop car-free; Times Square / Broadway plazas; Open Streets time windows | low | [S] ABC7, Central Park Conservancy (2018) | rule | Yes | OSM; NYC DOT Open Streets data [U] | Remove edges (permanently or by time); snap pickups to the nearest legal curb |
| **R01-030** Taxi stands and hotel queues | Designated stands (hotels, transit hubs) where only taxis may wait in line for passengers. | Stand present yes/no; queue length 0-30 cabs [U]; the first two cabs must stay in the driver's seat; green cabs may use stands only in the Hail Zone | medium | [P*] 34 RCNY 4-08(c)(1): only taxis may stand at a taxi stand; 35 RCNY 80-19(d): queue rules and green-cab limits; [S] NYC DOT sign legend | world | Yes | NYC DCP taxi-stand study (https://www.nyc.gov/assets/planning/download/pdf/plans/transportation/td_taxistands.pdf) | FIFO queue node fed by hotel or hub demand |
| **R01-031** Taxi/FHV relief stands | Curb spaces where taxi and FHV drivers may park for up to one hour to take a break. | 113 stands: Manhattan 70, Queens 28, Bronx 12, Brooklyn 3, Staten Island 0 [uncertain: count not re-checked]; one-hour limit | low | [P*] 34 RCNY 4-08(c)(2): taxis and FHVs may park at a relief stand for no more than one hour; [S] Manhattan CB1 letter (2026) citing NYC DOT; NYC DOT relief-stand page | world | Yes | NYC Open Data 'Taxi and For-Hire Vehicle (FHV) Relief Stands' (https://catalog.data.gov/dataset/taxi-and-for-hire-vehicle-fhv-relief-stands) | POI layer; a break elsewhere costs parking search time or ticket risk |
| **R01-032** Legal waiting spots (staging) | Whether the car can legally sit still near a hotspot while waiting for the next request instead of cruising. | Share of curb where standing is legal per zone; parking $0-15+/h [U]; NYC anti-idling limit 3 min (1 min next to schools); a taxi awaiting a fare may stand only at a taxi stand (or at a hydrant with the driver in the seat); non-taxis may not cruise for passengers [corrected by fact-check: idling limits confirmed and staging rules added] | medium | [P*] NYC Admin Code 24-163(a), (f); 34 RCNY 4-11(a)-(b); [S] Schaller (2017): in the Manhattan CBD, app cars had 55K passenger hours vs 37K empty hours (60% busy), and utilisation fell from 67% (taxis, 2013) to 62% (taxis and apps, 2017) [uncertain: the '11 min vs 8 min empty between trips' figures were not found in the checked excerpts] | world | Yes | NYC DOT parking regulations; licensed garages on NYC Open Data [U] | Per-zone wait cost (fuel, ticket risk, parking fee) vs cruise cost; agent chooses wait, cruise or reposition |
| **R01-033** Robotaxi pickup-point placement | A robotaxi stops only at a legal, safe point, which may be up to a block away, adding rider walk time and cancellations. | Walk 0-200 m [design]; density of valid pickup points per km of curb | low | [design] / [U] Operator practice not verified | rule | Yes | None found (operator-internal); OSM curbs | Snap each request to the nearest legal curb node; walk time adds to rendezvous; cancel chance rises with walk |

### 5.5 Foot traffic vs road density

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-034** Pedestrian volume by location | How many people walk past a point; drives street-hail chances and is a proxy for latent ride demand. | DOT counts at 114 locations (100 on-street, mainly retail corridors; 13 bridges; Hudson River Greenway), counted each May and September | high | [S] NYC Open Data dataset description (confirmed via GitHub copies: 114 locations, 100 on-street mostly retail corridors, 13 East River and Harlem River bridge points, Hudson River Greenway); Buchholz (2022, REStud): taxis are drawn to search in the most concentrated pedestrian areas [uncertain: this paraphrase of Buchholz was not checked against the paper] | world | Public / forecast | NYC DOT Bi-Annual Pedestrian Counts (https://data.cityofnewyork.us/d/2de2-6x2h) | Street-hail arrival rate per edge proportional to pedestrian intensity x hour profile, calibrated to yellow pickups |
| **R01-035** Pedestrian demand class of each street | NYC DOT's Pedestrian Mobility Plan puts every street in one of five pedestrian-demand classes. | Baseline (~60% of roads), Community Connector (~25%) [uncertain: shares not re-checked], Neighborhood Corridor, Regional Corridor, Global Corridor (mostly Manhattan) | medium | [S] NYC DOT Pedestrian Mobility Plan and data.gov dataset (modified Mar 2026); class names confirmed in GitHub uses of the Pedestrian_Demand file; [P*] 34 RCNY 5-11 uses the plan's corridor categories; MIT critique that some outer-borough streets are under-classified | world | Yes | Pedestrian Mobility Plan Pedestrian Demand (https://catalog.data.gov/dataset/pedestrian-mobility-plan-pedestrian-demand) | Categorical edge attribute feeding hail rate and curb friction |
| **R01-036** Subway entries and exits by hour | Hourly subway ridership per station shows where crowds appear and when transit thins out, shaping first/last-mile and substitute demand. | Hourly counts by station complex: 2017-19 (t69i-h2me), 2020-24 (wujg-7c2s), 2025+ (5wq4-mkjj); OD estimates (jsu2-fbtj) [uncertain: one GitHub project reports wujg-7c2s data starting in Feb 2022; t69i-h2me and jsu2-fbtj exist in the MTA catalog but their titles were not confirmed] | medium | [S] data.ny.gov catalog entries; IDs 5wq4-mkjj (2025+) and wujg-7c2s (2020-24) confirmed by several GitHub pipelines | world | Public / forecast | MTA Subway Hourly Ridership (https://data.ny.gov/d/5wq4-mkjj) | Demand covariate; subway outages (R03) move demand to cars near affected stations |
| **R01-037** Road-to-pedestrian ratio ('pickup-ability') | The user's idea: compare how many pedestrians gather on a block with how much drivable road and stoppable curb it has; busy but curb-starved streets mean many riders but slow, congested pickups. | Index = legal-stop curb metres / pedestrians per hour (or lanes / pedestrian class); bands low / medium / high; low examples Times Sq, SoHo | medium | [design]; Buchholz (2022): competition pushes taxis to spread search beyond the densest pedestrian areas [S] [uncertain: paraphrase not checked against the paper] | world | Yes | DOT pedestrian counts + Pedestrian Mobility Plan + LION width/lanes + DOT parking signs | Per-edge index raises hail rate (+) and pickup dwell / lowers through-speed (-) |
| **R01-038** Transit accessibility | Distance from a zone to the nearest subway station; areas far from rail rely more on cars for hire. | 0-3+ km to nearest station; transit-desert flag | medium | [P] Top HVFHV pickup zones include East New York, Crown Heights North, Bushwick South (Jun 2021); [U] transit-substitution mechanism | world | Yes | MTA GTFS static (https://new.mta.info/developers); NYC subway entrances (NYC Open Data) | Demand covariate; raises late-night demand when subway headways lengthen |
| **R01-039** Population and job density | Residents and workers per zone are the base of trip generation. | Residents/km2 and jobs/km2 per zone | high | [U] Standard trip-generation practice; Correa, Chow and Ozbay model demand from the spatial distribution of activities [S] | world | Yes | US Census ACS 5-year (https://data.census.gov); LEHD LODES (https://lehd.ces.census.gov/data/) | Demand-generator covariates when extrapolating beyond replayed data |
| **R01-040** Hail visibility by street type | Street hails happen mostly on avenues and busy corridors that cabs pass often; side streets yield few hails. | Hail multiplier: avenue 1.0, cross street 0.2-0.5 [design guess] | medium | [design] / [U]; yellow records carry exact coordinates only until June 2016 (zone IDs from July 2016) [S] toddwschneider/nyc-taxi-data README | world | No (hidden) | Pre-2016 TLC yellow records with lat/lon | Generate hails per edge; a cruising agent only sees hails on edges it drives |
| **R01-041** Cruising route for street hails | For a taxi, which streets to drive while empty, trading distance (fuel, time) against passing more pedestrians. | Route through high-hail edges vs waiting at a stand; cruise speed in traffic | medium | [design]; Schaller (2017): yellow taxis average 8 min empty between trips in the Manhattan CBD [S] [uncertain: figure not found in the checked excerpts]; [P*] 34 RCNY 4-11(b): only taxis may cruise for passengers | agent | Yes | Pre-2016 TLC yellow coordinates for calibration [U] | Agent picks the next edge or a loop; hails generated only on traversed edges |

### 5.6 Land use and trip generators

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-042** Land-use mix per zone | Share of residential, office, retail, nightlife, industrial and park land; sets the daily shape of demand. | MapPLUTO land-use classes (11) by lot area per zone | high | [P] Share of core yellow pickups ending in outer boroughs: 1.4% at 8am vs 17.7% at 4am (Oct 2019), showing home-bound night flows | world | Yes | NYC DCP MapPLUTO (https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page) | Zone feature vector; demand time profile depends on land-use mix |
| **R01-043** Office and business districts | Midtown, Financial District, Hudson Yards, Downtown Brooklyn and Long Island City pull weekday daytime trips. | Jobs per zone; weekday vs weekend ratio | medium | [P] Midtown Center 4.2% and Midtown East 3.7% of all yellow pickups (Oct 2019) | world | Yes | LEHD LODES; MapPLUTO office area | Work-hour peaks per zone (remote-work days in R02) |
| **R01-044** Nightlife density | Bars, clubs and late restaurants create late-night demand and longer, outbound trips. | On-premises liquor licences per zone; key areas LES, East Village, Meatpacking, Williamsburg, Bushwick | medium | [P] East Village is the #2 HVFHV pickup zone (Jun 2021); Meatpacking among the highest-tip drop-off zones (27%) | world | Yes | NYS Liquor Authority licences (data.ny.gov) [U]; DOHMH restaurant inspections [U] | Late-night demand multiplier; destinations drawn toward residential zones |
| **R01-045** Tourist and hotel density | Hotels and attractions create airport trips, taxi-stand queues and riders less likely to use transit. | Hotel rooms per zone; attraction POIs | medium | [P] Times Sq/Theatre District = 3.5% of yellow pickups (Oct 2019) | world | Yes | OSM tourism tags; NYC hotel lists on NYC Open Data [U] | Hotel POIs as taxi-stand queues and airport-bound demand |
| **R01-046** Hospitals, universities and institutions | Large hospitals produce steady trips around shift changes and discharges (plus paratransit rides); campuses shift demand with the academic calendar. | Beds per site; shift changes ~7am / 7pm [U]; enrolment per campus, term on/off | low | [U] Background knowledge; [P*] HVFHV records carry access_a_ride_flag (confirmed in the Jan 2023 schema) | world | Yes | NYS DOH health facility data (health.data.ny.gov) [U]; NCES IPEDS (campuses) | POI with a daily time profile and seasonal multiplier (R02) |
| **R01-047** Venues, stadiums and convention centres | Fixed big venues whose location, capacity and exits shape event surges (the events themselves are in R03). | Capacity 2k-50k (MSG, Barclays, Yankee Stadium, Citi Field, USTA, UBS Arena, Javits, Lincoln Center); exit curb capacity | medium | [U] Background knowledge; MSG sits on Penn Station (zone 186, top-5 yellow pickup zone) [P] | world | Yes | OSM; venue websites | Venue nodes with capacity; R03 schedules events on them |
| **R01-048** Retail and shopping corridors | Shopping streets create daytime and weekend short trips. | Retail floor area per zone | low | [U] Background knowledge; most DOT pedestrian count sites are retail corridors [S] | world | Yes | MapPLUTO retail area; DOT pedestrian counts | Daytime / weekend demand covariate |

### 5.7 Transit hubs and airports

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-049** Intercity rail and bus hubs | Penn Station/Moynihan, Grand Central, Port Authority Bus Terminal, Atlantic Terminal and Jamaica produce rider pulses timed to public train and bus arrivals. | Penn Station/Madison Sq West = 3.6% of yellow pickups, PU/DO 1.40 (Oct 2019); arrival schedules public in GTFS | high | [P] Own computation, TLC yellow Oct 2019 | world | Public / forecast | GTFS feeds (MTA, NJ Transit, Amtrak); TLC records | Hub nodes with arrival-driven pulses + taxi-stand queues |
| **R01-050** Airport trip share and value | Airport trips are few but long and lucrative. | Yellow Oct 2019: 7.9% of trips, 22.2% of driver revenue (fare + extras + tips); JFK pickup mean $51.19 over 15.3 mi, LGA $37.81 over 9.1 mi. HVFHV Jun 2021: 5.4% of trips touch an airport | high | [P] Own computation, TLC yellow Oct 2019 and HVFHV Jun 2021 | world | Public / forecast | TLC trip records | Airport zones with their own demand profile tied to flight schedules (R03/R12) |
| **R01-051** Airport pickup/drop-off asymmetry | For yellow cabs airport pickups far exceed drop-offs, while app trips are roughly balanced. | Yellow PU/DO: JFK 3.81, LGA 2.06 (Oct 2019); HVFHV: JFK 0.84, LGA 0.88 (Jun 2021) | medium | [P] Own computation | world | Public / forecast | TLC trip records | Emerges from the OD matrix; decides whether an airport drop-off can be followed by an airport pickup |
| **R01-052** Airport holding-lot queue | After an airport drop-off, a driver can join a lot queue for an outbound fare or deadhead back; queue length sets the expected wait. | Yellow JFK central taxi hold: historically ~2-3 h average, up to 5 h [uncertain: wait times not re-checked]. FHV: virtual FIFO queue (JFK Cell Phone Lot / Limo Lot; LGA lot), free parking up to 3 h, place lost if offline or after repeated declines | high | [S] NBC New York (bribery case); Uber JFK driver page; Yazici, Kamga and Singhal (2016, TR-A 91:48-60): proximity is the strongest predictor of the airport-pickup decision; [P*] 35 RCNY 80-19(e)-(f): taxis queue through holding areas and feed lines (separate short- and long-haul lines at some stands); FHVs may not accept a dispatch while parked in JFK/LGA pickup areas | state | Yes | No public queue data; infer from TLC airport drop-off and pickup times [design] | Per-airport FIFO queue fed by flight arrivals; agent joins or leaves; app shows queue position |
| **R01-053** Airport queue decision | After an airport drop-off, the agent decides whether to join the airport queue, leave it, or deadhead back to the city. | Join / skip / leave after t minutes; information: queue position (app) or lot count (taxi) | high | [S] Yazici, Kamga and Singhal (2016): NYC taxi drivers' airport-pickup decisions depend mainly on proximity, then time, weather and shift variables [uncertain: finding not re-checked against the paper; publisher hosts blocked] | agent | Yes | TLC airport trips for calibration | Action at airport zones; payoff = expected airport fare minus queue time vs city alternative |
| **R01-054** Airport fare and fee triggers | Fare rules switched on by airport geography (amounts owned by R07). | Taxi: JFK to/from Manhattan flat $70 (+$5 weekdays 4-8pm); LGA +$5 to and from; airport access fee on JFK/LGA taxi pickups $1.25 until Mar 2023 and $1.75 from Apr 2023 (trip records), possibly $2.00 in 2026 [uncertain: 2026 amount from a code comment only]. HVFHV: $2.50 airport fee on pickups and drop-offs at JFK/LGA/EWR, already in Jan 2023 records [corrected by fact-check: the original said 'since Apr 2023'; the April 2023 change was the taxi access fee rising to $1.75]. Newark taxi trips: meter + $20 surcharge + tolls both ways [corrected by fact-check: $20 is the rule in force, not a proposal] | medium | [P*] 35 RCNY 58-26(a)(2)(iii), (b), (c)(3); [P*] airport_fee values in yellow 2023-24 and HVFHV Jan 2023 records; [S] 2026 fare config quoting the TLC rate card; VisaVerge / Fox5 on the FHV fee | rule | Yes | TLC fare page; airport_fee fields in trip records | Airport polygons trigger fare-engine branches |
| **R01-055** Airport terminal layout and pickup rules | Where at the airport pickups are allowed (terminal curbs, FHV zones, remote lots), adding minutes and confusion. | JFK: FHV pickups barred at Terminals 5 and 7 'until further notice' [uncertain: from 2021-era driver guides; may be outdated], with Howard Beach FHV Hold Lot 3; arrivals-level pickups only; JFK rebuilding (New Terminal One) changes roads [U] | low | [S] Uber JFK driver page (French version); Inshur driver guide (2021) | rule | Yes | PANYNJ ground transport pages; Uber airport driver pages | Airport sub-graph with pickup nodes per terminal and extra walk/drive time |
| **R01-056** Newark Airport (EWR) special status | EWR is in New Jersey: NYC drivers drop off there but almost never pick up, so each EWR drop-off implies an empty return. [corrected by fact-check: for taxis the passenger pays a $20 Newark surcharge and tolls both ways (35 RCNY 58-26(c)(3)), so the return toll is reimbursed; app drivers are paid the out-of-town rate] | Yellow: 15,829 drop-offs vs 57 pickups (Oct 2019; 829 pickups under a lighter filter, mostly zero-distance records), rate code 3 = 0.24% of trips; HVFHV: 63,278 vs 228 (Jun 2021); return toll $14.79-16.79 E-ZPass; a taxi may refuse an EWR trip after 8 h of operation | medium | [P] Own counts (reproduced); [P*] 35 RCNY 58-26(c)(3), 80-20(b)(8); [S] PANYNJ 2026 tolls | rule | Yes | TLC records; PANYNJ | EWR zone = drop-off only for NYC-licensed cars; forced deadhead; inbound toll paid by the driver for app cars and reimbursed by the passenger for taxis |

### 5.8 Out-of-city trips and the empty return

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-057** Out-of-city trip share | Share of trips ending outside NYC (NJ, Westchester, Nassau, Long Island, Connecticut). | HVFHV Jun 2021: 3.67% end outside NYC (zone 265) + 0.42% at EWR. Yellow Oct 2019: rate code 4 (Nassau/Westchester) 0.08%, negotiated (code 5) 0.17%, Newark (code 3) 0.24% | medium | [P] Own computation | world | No (hidden) | TLC trip records | OD matrix includes external destination nodes by county |
| **R01-058** Out-of-city fare and pay rules | How trips leaving the city are priced and paid, which decides whether the empty return is compensated (amounts owned by R07). | Yellow: meter to the city line, then double meter beyond for Westchester/Nassau, plus tolls both ways; other places negotiated flat fare. HVFHV minimum pay from 1 Mar 2026: in-city $1.283/mi + $0.681/min (non-WAV); out-of-town $1.757/mi (non-WAV), $2.193/mi (WAV), $0.725/min [uncertain: 2026 posted values not re-checked; they match the rule's base rates after yearly CPI indexing] | medium | [P*] 35 RCNY 58-26(c)(1)-(2), (f)(2): double meter and tolls both ways confirmed; 35 RCNY 59D-22(a): out-of-town base rates ($1.700/mi, WAV $2.122, $0.574/min) are double the in-city base and are not divided by the utilisation rate; [S] TLC driver-pay-rates page | rule | Yes | TLC driver pay rates (https://www.nyc.gov/site/tlc/about/driver-pay-rates.page) | Fare-engine branch when the destination is outside the NYC polygon |
| **R01-059** Empty-return distance and legality | After an out-of-city drop-off the driver normally returns to NYC empty, because pickups outside the city need a local licence. | Return 10-60+ km; street hails outside NYC not allowed; app pickups outside NYC depend on NJ / county licensing [U]; taxi passengers reimburse tolls both ways for EWR, Westchester and Nassau; taxis may refuse those trips after 8 h of operation | medium | [P] Near-zero pickups at EWR and zone 265 in TLC records; [P*] 35 RCNY 58-26(c), 80-20(b)(8); [U] county licensing details [corrected by fact-check: impact high -> medium; such trips are ~0.5% of yellow and ~4% of app trips and are partly compensated, though a single one can cost up to an hour] | rule | Yes | TLC records; county taxi/limousine rules [U] | Compute deadhead route back to the city line or home; charge time, energy and inbound toll |
| **R01-060** Night outward drift | At night more trips leave the core for residential outer boroughs, leaving drivers far from demand. | Share of core yellow pickups ending in outer boroughs: 1.4% at 8am, 9.5% at 10pm, 13.1% at midnight, 17.7% at 4am (Oct 2019) | high | [P] Own computation, TLC yellow Oct 2019 | world | Public / forecast | TLC trip records | Emerges from hour-specific OD matrices; makes 'go home after last trip' and repositioning decisions matter |

### 5.9 Driver home, depots and amenities

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-061** Driver home location | Where the driver lives, which sets the start and end commute and the 'take me home' preference. | Zone ID sampled from a driver-residence distribution (mostly Queens, Brooklyn, Bronx; some NJ / Long Island) [U] | medium | [U] Residence distribution not verified (search budget used up) | setting | Yes | None verified; TLC licensee data if published [U] | Home node per driver; unpaid commute at shift start and end |
| **R01-062** Distance and time to home | Live network distance from the car to home; near shift end it decides whether to accept a trip or use a destination filter. | 0-40 km; destination-filter uses per day (Uber historically 2/day) [U]; taxi 'returning to garage or home' rule | medium | [U] Background knowledge of platform destination filters; [P*] 35 RCNY 80-19(a)(5): an off-duty taxi driver heading home or to the garage may take a passenger only if the destination is directly on the route and the trip record says 'Returning to garage (or home)' [corrected by fact-check: added the taxi go-home rule] | state | Yes | Derived from road graph | Recompute each step; 'take me home' mode biases matching toward trips ending near home |
| **R01-063** Garages, depots and shift-change points | Yellow cab garages and robotaxi depots are where shifts start or end and cars are cleaned or charged, adding deadhead. | Garage zone; two-shift taxis change around 4-5pm [U]; robotaxi depot locations set by scenario | medium | [U] Background knowledge; [design] for robotaxi depots | setting | Yes | None found | Depot nodes; mandatory returns for shift change, charging or cleaning |
| **R01-064** Fuel station locations | Where gas stations are and the detour to reach them; Manhattan has few. | Stations per borough; detour 0-15 min | low | [U] Background knowledge | world | Yes | OSM amenity=fuel | POI layer; refuel action routes to the nearest station |
| **R01-065** EV charger locations, power and access | Location, speed and availability of chargers (public, curbside, fleet-only hubs), which set detour and downtime for EVs. | DC fast 50-350 kW; Level 2 7-19 kW; NYC DOT curbside chargers; fleet hubs | medium | [S] TLC license reviews weigh EV charging availability; [U] charger mix [uncertain: TLC licence-review claim not re-checked] | world | Yes | AFDC station locator (https://afdc.energy.gov/stations) | Charger POIs with ports, power and queues; charge action (R08) |
| **R01-066** Restrooms, food and break spots | Where a driver can take a legal break with a toilet and food, which affects break length and dead time. | Public restroom POIs; 113 relief stands [uncertain: count not re-checked, see R01-031]; break detour 0-20 min | low | [S] WNYC 'Relief in short supply for the city's taxi drivers'; [U] | world | Yes | NYC Parks public restrooms (NYC Open Data) [U]; OSM amenity=toilets | Break action needs a nearby POI; cost = detour + dwell |

### 5.10 Neighbourhood economics and safety

| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |
|---|---|---|---|---|---|---|---|---|
| **R01-067** Neighbourhood income | Median household income of pickup and drop-off areas, which tracks card use, trip length and tipping. | ACS median income per tract mapped to zone; card-trip tip/fare 25.9% for Yellow Zone pickups vs 19.3% outer boroughs; lowest drop-off zones 18.8-19.2% (Stuyvesant Heights, Central Harlem North, Crown Heights North) vs ~27% (UES, UWS, West Village) | medium | [P] Own computation, yellow Oct 2019 card trips (tips are recorded only for card payments); reproduced, and robust alternatives give the same gap (tip/fare ratio of sums 23.9% vs 17.9%; medians 26.3% vs 22.2%) | world | Yes | US Census ACS; TLC tips (yellow card trips; HVFHV tips column) | Zone covariate for tip probability and size (behaviour owned by R05) |
| **R01-068** Payment mix by zone | Share of cash vs card trips by area; affects recorded tips and cash handling for taxis (app trips are cashless). | Card share, yellow Oct 2019: Yellow Zone 74.2%, upper Manhattan 58.8%, outer boroughs 51.7%, airports 64.7% | low | [P] Own computation | world | No (hidden) | TLC yellow payment_type | Per-zone payment-type probability |
| **R01-069** Perceived safety and crime | Crime and drivers' sense of risk make some drivers avoid areas at night, thinning supply there and raising surge for those who stay, with a small real incident risk. | Complaints per 1,000 residents by precinct and hour; avoidance probability 0-1 [design] | low | [U] / [design]; benchmark must not reward illegal refusal | world | Public / forecast | NYPD Complaint Data (NYC Open Data) | Lower competitor supply in high-perceived-risk zones at night; small incident probability |
| **R01-070** Geographic refusal rules | Taxis must take passengers to any destination in the city, Westchester, Nassau or Newark Airport and may not ask the destination before the rider is seated, so the agent cannot legally refuse by neighbourhood; app drivers can decline but acceptance rate counts against them. | Taxi refusal = mandatory penalty under 35 RCNY 80-02(e) (about $500 for a first offence [S]); allowed refusals include more than 8 h of operation for EWR/Westchester/Nassau trips; app accept/decline with destination shown [U] | medium | [P*] 35 RCNY 80-20(a)(1), (a)(4), (b) [corrected by fact-check: the rule also covers Westchester, Nassau and Newark; tag upgraded from U] | rule | Yes | 35 RCNY 80-20 and 80-02 (verbatim copy https://github.com/jehiah/nyc_code_archive); TLC rules (https://www.nyc.gov/site/tlc/about/tlc-rules.page) | Block destination-based refusal for taxis; track acceptance for app drivers (R06/R07) |

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
- **R01 x R06 (competition and matching):** concentration and imbalance set how crowded hot zones get. Fréchette, Lizzeri and Salz (2019) find increasing returns to scale in taxi matching and that platform competition reduces effective density [S] [uncertain: the second finding was not checked against the paper]. Buchholz (2022) shows competition spreads taxis away from the densest pedestrian areas [S] [uncertain: paraphrase not checked against the paper]. Airport queue length depends on competitor supply.
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
4. **Rendezvous time:** confirm that HVFHV `on_scene_datetime` is populated well enough to fit per-zone pickup dwell (R01-026). I could not read the data dictionary. [corrected by fact-check: answered. In Jan 2023 records it is filled for Uber (HV0003) trips and empty for 99.9% of Lyft (HV0005) trips; median pickup minus on-scene time is 0.8 min]
5. **Out-of-city pickups:** can NYC TLC app drivers legally accept pickups in NJ, Westchester or Nassau (for example after an EWR drop-off)? This sets how harsh the empty return is. Not verified. (Fact-check: still open; note that taxi riders reimburse return tolls for EWR, Westchester and Nassau trips.)
6. **Current amounts not verified:** MTA car E-ZPass toll after 4 Jan 2026; Newark taxi surcharge; speed-camera operating hours; yellow "double meter" rule beyond the city line. [corrected by fact-check: partly answered. The $20 Newark surcharge and the double meter with tolls both ways are in 35 RCNY 58-26(c); the 2026 MTA car toll and camera hours remain open]
7. **Driver home distribution:** is there a public source for TLC driver residence by ZIP or borough? Without one, "take me home" scenarios rest on a design guess.
8. **Street-level hail calibration:** yellow records before mid-2016 carry exact coordinates [U] [corrected by fact-check: confirmed, coordinates end in June 2016 [S]]. Should they be used to calibrate street-level hail rates (R01-040), given that demand has since shifted?
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
- [U] Background knowledge: Manhattan one-way grid and two-way crosstown streets; parkway access; Verrazzano one-way toll; anti-idling limits; destination filters; garage shift changes; double meter beyond city line; driver residence pattern; pre-2016 yellow coordinates. [corrected by fact-check: anti-idling limits, the double meter and the pre-2016 coordinates are now confirmed, see below]

Sources added by the fact-check (19 Oct 2026):

- [P*] Rules of the City of New York (Title 34 traffic rules 4-01, 4-06, 4-08, 4-11, 4-12, 4-17, 5-11; Title 35 TLC rules 51-03, 58-26, 59D-22, 80-02, 80-19, 80-20, 82-13, 82-26) and NYC Administrative Code 19-162.6, 19-177, 24-163, verbatim copy current through rules effective 13 Aug 2026: https://github.com/jehiah/nyc_code_archive
- [P*] TLC HVFHV trip records Jan 2023 (fhvhv_tripdata_2023-01.parquet, 18,479,031 rows) and yellow 2023 to Jan 2024, GitHub LFS copies whose SHA-256 matches the TLC originals (provenance in R02 appendix); used for on-scene times, airport fees, congestion surcharges and toll amounts.
- [P] Re-run of the Oct 2019 yellow and green and Jun 2021 HVFHV computations from the DataTalksClub copies (fact-check scripts in the session scratchpad, folder fc_r01).
- [S] Vital City, Waymo in America methodology (6 May 2026): https://github.com/vitalcity-nyc/waymo-map/blob/HEAD/methodology.md
- [S] Todd Schneider, nyc-taxi-data README (coordinates end June 2016): https://github.com/toddwschneider/nyc-taxi-data
- [S] Schaller (2017) quotes in tomslee/ridehail docs/cities.md: https://github.com/tomslee/ridehail
- [S] NYT on the 14th St busway (Oct 2019), GitHub text copy: https://github.com/nexync/dated_data (newspan/2019-10/53.txt)
- [S] Congestion pricing amounts in 2026 analyses: https://github.com/Erdos-Projects/summer26-congestion-pricing ; https://github.com/atharvajoshi01/nyc-tlc-congestion-pricing-causal-study
- [S] 2026 taxi fare config quoting the TLC rate card (airport access fee $2.00): https://github.com/rujui7142/dsma_project/blob/HEAD/src/config.py
- [S] Dataset IDs 755u-8jsi, 2de2-6x2h, 5wq4-mkjj, wujg-7c2s, t69i-h2me, jsu2-fbtj seen in public GitHub code (for example https://github.com/HuseinGhadiali/Geospatial-Data-Analysis-for-Retail-Optimization and https://github.com/Hussain0327/nyc-transit-demand).

## Fact-check log

**Date:** 19 Oct 2026. Independent fact-check of all 70 variables and the surrounding text.

**How I checked.** The shared web-search budget was used up before this check began, and nyc.gov, mta.info, data.ny.gov, data.cityofnewyork.us, panynj.gov, uber.com, news sites and journal sites were blocked. I used no proxy, reader, cache or mirror service. So the check rests on three things: (1) re-running every own-computation figure from the same TLC files (yellow and green Oct 2019, HVFHV Jun 2021), plus HVFHV Jan 2023 and yellow 2023 Parquet copies whose checksums match the TLC originals; (2) the Rules of the City of New York and the NYC Administrative Code, read from a verbatim GitHub copy current through rules effective 13 Aug 2026 [P*]; (3) GitHub copies and code that quote official pages or dataset IDs [S]. Claims from blocked pages that I could not re-read are marked [uncertain] where they matter.

**Counts (variables, each counted once; corrected takes precedence over uncertain):**

| Checked | Verified | Corrected | Uncertain | Removed |
|---|---|---|---|---|
| 70 | 29 | 19 | 22 | 0 |

"Uncertain" includes 6 variables whose key claims were already tagged [U] and could not be checked (R01-014, 046, 048, 061, 063, 064). No variable was wrong or meaningless enough to remove, and there were no exact duplicates; R01-007, R01-056 and R01-059 overlap (pickup mask, EWR case, empty-return cost) and could be merged at synthesis.

**Key corrections:**

1. **Green taxi exclusion (R01-006):** 35 RCNY 51-03 and 82-13 also bar green cabs from starting base-dispatched trips in Manhattan south of E 96th / W 110th, and an e-hail counts as a hail. The original "e-hail still allowed" was wrong. Source upgraded from [S] to [P*].
2. **Airport fees (R01-054):** the $2.50 HVFHV airport fee already appears on Jan 2023 records, on pickups and drop-offs, so "since Apr 2023" was wrong. The April 2023 change was the yellow access fee rising from $1.25 to $1.75. A 2026 code comment says it is now $2.00 [uncertain]. The $20 Newark surcharge is in force (35 RCNY 58-26(c)(3)), not a 2022 proposal.
3. **Who pays return tolls (R01-021, R01-056, R01-059):** for taxi trips to Newark, Westchester and Nassau the passenger pays tolls to and from the destination, so the taxi's empty-return toll is reimbursed. Taxis may also refuse those trips after 8 hours of operation. App drivers are compensated through the out-of-town pay rate instead.
4. **Rendezvous time (R01-026):** HVFHV Jan 2023 shows pickup minus on-scene time with a median of 0.8 min and 90% under about 2 min (Uber). Lyft leaves the field empty. The original "0.5-5 min [U]" range was too wide, so the impact was cut from medium to low.
5. **Cruising and staging (R01-011, R01-032, R01-041):** 34 RCNY 4-11(b) bars any vehicle other than a taxi from cruising to search for passengers, and 4-11(a) lets a waiting taxi stand only at a taxi stand. So "cruise a loop" is a taxi-only action. The anti-idling limits (3 min, 1 min by schools) are confirmed in Admin Code 24-163.
6. **River crossings (R01-019, R01-020):** bridges and tunnels are not the only links between boroughs, because Brooklyn and Queens share a land border. The Henry Hudson Bridge is a tolled Harlem River crossing, and the Staten Island-NJ crossings were missing. Trip records confirm the $6.94 MTA car E-ZPass toll from Aug 2023. The PANYNJ amounts in 2023-24 records ($14.75 / $12.75, then $15.38 / $13.38) fit the 2026 figures.
7. **Zone imbalance (R01-004):** the lowest named zone with more than 3,000 drop-offs is Windsor Terrace (0.08), not Washington Heights North (0.09). JFK's 3.81 falls to 3.53 under a lighter cleaning filter.
8. **Smaller fixes:** 14th St busway runs 3rd to 9th Ave, not 3rd to 8th (R01-028). The bus-lane 200 ft rule applies to right turns (R01-027). Some Manhattan avenues are two-way (R01-013). The 25 mph base speed limit is set by law, so there is no conflict (R01-015). Taxi destination rules cover Westchester, Nassau and Newark, upgraded from [U] to [P*] (R01-070). The taxi "returning to garage or home" rule was added to the go-home variable (R01-062). Taxi IDs 264/265 have different labels in older lookup copies (R01-001).
9. **Impact ratings changed (4):** R01-001 high to medium (structural layer). R01-019 high to medium (tolls are mostly rider-paid; delay sits in R10). R01-059 high to medium (rare and partly compensated). R01-026 medium to low (about 1 min per trip). All other ratings were judged defensible.

**Confirmed without change (examples):** all yellow, green and HVFHV shares, ratios, speeds, airport revenue share, toll share, tip and card shares, and night outward drift figures (reproduced exactly). The 263-zone, 55 / 205 / 2 / 1 service-zone split. The 96th St congestion zone definition and the $2.50 / $2.75 / $0.75 surcharges seen in records. The JFK $70 flat fare with the $5 rush surcharge and the LGA $5 surcharge. The double meter for Westchester/Nassau. One-hour relief-stand parking. The taxi-only taxi stands. The HVFHV out-of-town pay structure. Dataset IDs 755u-8jsi, 2de2-6x2h, 5wq4-mkjj and wujg-7c2s. The 114-location pedestrian count design. Citations for Haggag et al. (2017), Buchholz (2022) and Fréchette et al. (2019). Waymo's NYC test (8 cars, south of 112th St plus Downtown Brooklyn, permits expired 31 Mar 2026), via a secondary GitHub source.

**Still open:** the 2026 MTA car toll; PANYNJ toll-by-plate; CRZ later phases ($12 / $15) and the overnight rate; the 113 relief-stand count; Schaller's "11 vs 8 min" figures; the JFK hold-lot wait times; the Pedestrian Mobility Plan class shares; the paraphrased findings of Buchholz, Fréchette et al. and Yazici et al.; the 2026 HVFHV pay values (consistent with the indexed rule but not seen posted); app pickups outside NYC.
