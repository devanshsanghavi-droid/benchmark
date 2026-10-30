"""Build the derived data files for the commercial-to-commercial ride generator (v1).

Run once; the outputs are small and committed to the repo, so the generator itself
never touches the network.

    python data_prep/build_commercial_v1.py --raw-dir /some/cache/dir

Sources (see DECISIONS.md D3-D5 for why these):
  * NYC TLC yellow taxi trip records, Apr + Oct 2019 (pickup/drop-off zone and time).
  * NYC TLC taxi zone polygons and lookup table.
  * Overture Maps "places" (real business locations), release pinned below.

Official hosts (nyc.gov, the TLC CloudFront bucket, NYC Open Data) were blocked from the
machine that first ran this, so the TLC files come from the DataTalksClub GitHub copy of
the official files. Swap in the OFFICIAL_* URLs once those hosts are reachable.

Needs: duckdb, pyarrow, shapely (prep only; the generator needs none of them).
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "robotaxi" / "data" / "derived" / "commercial_v1"

TLC_MONTHS = ["2019-04", "2019-10"]
TLC_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{month}.csv.gz"
OFFICIAL_TLC_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month}.parquet"
ZONE_LOOKUP_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
OFFICIAL_ZONE_LOOKUP_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
# GeoJSON conversion of the official TLC taxi_zones shapefile (WGS84).
ZONE_GEOJSON_URL = ("https://raw.githubusercontent.com/AdukNyang/urban_mobility_data_explorer_Team_1/"
                    "main/frontend/data/taxi_zones.geojson")
OFFICIAL_ZONE_SHAPEFILE_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip"

OVERTURE_RELEASE = "2026-10-21.0"
OVERTURE_PLACES = f"overturemaps-us-west-2/release/{OVERTURE_RELEASE}/theme=places/type=place/"
# Bounding box around Manhattan (west, south, east, north). Places are then clipped to zones.
BBOX = (-74.0300, 40.6950, -73.9050, 40.8820)

# Zones with no public road access: Governor's / Ellis / Liberty Islands.
EXCLUDED_ZONES = {103, 104, 105}

# Which Overture places count as "commercial" (top level of Overture's taxonomy).
COMMERCIAL_TOP_CATEGORIES = {
    "food_and_drink", "shopping", "services_and_business", "lifestyle_services",
    "arts_and_entertainment", "lodging",
}
# Fine categories dropped even inside those groups: not trip destinations, or mostly
# registered at private homes (home_service = plumbers, cleaners, etc.).
EXCLUDED_BASIC_CATEGORIES = {"atm", "parking", "home_service", "storage_facility", "ev_charging_station",
                             "gas_station", "shipping_or_delivery_service"}
MIN_CONFIDENCE = 0.5


def download(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"downloading {url}")
    with urllib.request.urlopen(url, timeout=600) as r, open(dest, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    return dest


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------------------------------------------------------
# Zones
# ----------------------------------------------------------------------------------------
def build_zones(raw: Path) -> dict[int, dict]:
    lookup = download(ZONE_LOOKUP_URL, raw / "taxi_zone_lookup.csv")
    geo = download(ZONE_GEOJSON_URL, raw / "taxi_zones.geojson")
    names = {}
    with open(lookup) as f:
        for row in csv.DictReader(f):
            if row["Borough"] == "Manhattan":
                names[int(row["LocationID"])] = (row["Zone"], row["service_zone"])
    feats = [ft for ft in json.load(open(geo))["features"]
             if ft["properties"]["LocationID"] in names and ft["properties"]["LocationID"] not in EXCLUDED_ZONES]
    zones = {}
    for ft in feats:
        zid = ft["properties"]["LocationID"]
        zones.setdefault(zid, {"zone_id": zid, "name": names[zid][0], "service_zone": names[zid][1], "geoms": []})
        zones[zid]["geoms"].append(ft["geometry"])
    out = {"type": "FeatureCollection", "features": []}
    for zid in sorted(zones):
        z = zones[zid]
        geom = z["geoms"][0] if len(z["geoms"]) == 1 else {
            "type": "MultiPolygon",
            "coordinates": [c for g in z["geoms"] for c in ([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"])]}
        out["features"].append({"type": "Feature", "geometry": geom,
                                "properties": {"zone_id": zid, "name": z["name"], "service_zone": z["service_zone"]}})
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "zones_manhattan.geojson", "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"zones: {len(out['features'])}")
    return {ft["properties"]["zone_id"]: ft for ft in out["features"]}


# ----------------------------------------------------------------------------------------
# Places (Overture)
# ----------------------------------------------------------------------------------------
def extract_overture(raw: Path) -> Path:
    """Read only the Parquet row groups whose bbox overlaps Manhattan (no full download)."""
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.fs as pafs
    import pyarrow.parquet as pq

    dest = raw / f"overture_places_{OVERTURE_RELEASE}_manhattan_bbox.parquet"
    if dest.exists():
        return dest
    kw = {}
    if os.environ.get("HTTPS_PROXY"):
        px = urlparse(os.environ["HTTPS_PROXY"])
        kw["proxy_options"] = {"scheme": px.scheme, "host": px.hostname, "port": px.port}
    fs = pafs.S3FileSystem(anonymous=True, region="us-west-2", connect_timeout=30, request_timeout=300, **kw)
    files = sorted(f.path for f in fs.get_file_info(pafs.FileSelector(OVERTURE_PLACES)) if f.path.endswith(".parquet"))
    cols = ["id", "names", "basic_category", "taxonomy", "confidence", "operating_status", "bbox", "addresses"]
    xmin, ymin, xmax, ymax = BBOX
    parts = []
    for path in files:
        pf = pq.ParquetFile(path, filesystem=fs)
        md = pf.metadata
        colnames = [md.schema.column(i).path for i in range(md.num_columns)]
        ix = {k: colnames.index(f"bbox.{k}") for k in ("xmin", "xmax", "ymin", "ymax")}
        for rg in range(md.num_row_groups):
            st = {k: md.row_group(rg).column(i).statistics for k, i in ix.items()}
            if not (st["xmin"].min <= xmax and st["xmax"].max >= xmin and st["ymin"].min <= ymax and st["ymax"].max >= ymin):
                continue
            t = pf.read_row_group(rg, columns=cols)
            x = pc.struct_field(t.column("bbox"), "xmin")
            y = pc.struct_field(t.column("bbox"), "ymin")
            m = pc.and_(pc.and_(pc.greater_equal(x, xmin), pc.less_equal(x, xmax)),
                        pc.and_(pc.greater_equal(y, ymin), pc.less_equal(y, ymax)))
            t = t.filter(m)
            if t.num_rows:
                parts.append(t)
    pq.write_table(pa.concat_tables(parts), dest)
    return dest


def build_places(raw: Path, zones: dict[int, dict]) -> None:
    import duckdb
    from shapely import STRtree
    from shapely.geometry import Point, shape

    src = extract_overture(raw)
    con = duckdb.connect()
    rows = con.execute(f"""
        select id, names.primary as name, basic_category, taxonomy.hierarchy[1] as top_category,
               (bbox.ymin + bbox.ymax) / 2 as lat, (bbox.xmin + bbox.xmax) / 2 as lon, confidence,
               addresses[1].freeform as address
        from '{src}'
        where coalesce(operating_status, 'open') = 'open'
          and confidence >= {MIN_CONFIDENCE}
          and taxonomy.hierarchy[1] in ({",".join("'" + c + "'" for c in sorted(COMMERCIAL_TOP_CATEGORIES))})
          and coalesce(basic_category, '') not in ({",".join("'" + c + "'" for c in sorted(EXCLUDED_BASIC_CATEGORIES))})
          and names.primary is not null
        order by id
    """).fetchall()
    ids = sorted(zones)
    polys = [shape(zones[z]["geometry"]) for z in ids]
    tree = STRtree(polys)
    kept, per_zone = [], {}
    for pid, name, basic, top, lat, lon, conf, addr in rows:
        pt = Point(lon, lat)
        hit = [i for i in tree.query(pt) if polys[i].covers(pt)]
        if not hit:
            continue
        zid = ids[hit[0]]
        per_zone[zid] = per_zone.get(zid, 0) + 1
        kept.append((pid, name, basic or "", top, round(lat, 6), round(lon, 6), zid, round(conf, 3), addr or ""))
    with gzip.open(OUT_DIR / "places_commercial.csv.gz", "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(["place_id", "name", "basic_category", "top_category", "lat", "lon", "zone_id", "confidence", "address"])
        w.writerows(kept)
    print(f"places: {len(rows)} commercial in bbox, {len(kept)} inside Manhattan zones; "
          f"zones with places: {len(per_zone)}/{len(zones)}")


# ----------------------------------------------------------------------------------------
# Origin-destination rates (TLC yellow)
# ----------------------------------------------------------------------------------------
def build_od_rates(raw: Path, zones: dict[int, dict]) -> dict:
    import duckdb

    files = [download(TLC_URL.format(month=m), raw / f"yellow_tripdata_{m}.csv.gz") for m in TLC_MONTHS]
    zl = ",".join(str(z) for z in sorted(zones))
    con = duckdb.connect()
    sel = []
    for m, p in zip(TLC_MONTHS, files):
        y, mo = map(int, m.split("-"))
        nxt = f"{y + (mo == 12)}-{(mo % 12) + 1:02d}-01"
        sel.append(f"""
          select cast(tpep_pickup_datetime as timestamp) pu, cast(tpep_dropoff_datetime as timestamp) dof,
                 cast(PULocationID as int) pul, cast(DOLocationID as int) dol
          from read_csv('{p}', header=true, all_varchar=true)
          where tpep_pickup_datetime >= '{m}-01' and tpep_pickup_datetime < '{nxt}'""")
    con.execute("create table t as " + " union all ".join(sel))
    con.execute(f"""create table v as select pu, pul, dol, cast(pu as date) d, hour(pu) h,
                      case when dayofweek(pu) = 0 then 'sunday' when dayofweek(pu) = 6 then 'saturday' else 'weekday' end dt
                    from t where pul in ({zl}) and dol in ({zl})
                      and dof > pu and dof < pu + interval 3 hour""")
    # Drop federal holidays inside the sample so 'weekday' means an ordinary working day.
    from robotaxi.rides.calendar import us_federal_holidays
    hol = sorted({d for m in TLC_MONTHS for d in us_federal_holidays(int(m[:4])) if d.strftime("%Y-%m") == m})
    if hol:
        con.execute("delete from v where d in (" + ",".join(f"DATE '{d.isoformat()}'" for d in hol) + ")")
    days = dict(con.execute("select dt, count(distinct d) from v group by 1").fetchall())
    rows = con.execute("""select dt, h, pul, dol, count(*) n from v group by 1, 2, 3, 4 order by 1, 2, 3, 4""").fetchall()
    total = con.execute("select count(*) from v").fetchone()[0]
    with gzip.open(OUT_DIR / "od_rates_yellow2019.csv.gz", "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day_type", "hour", "pu_zone", "do_zone", "trips_per_day"])
        for dt, h, pul, dol, n in rows:
            w.writerow([dt, h, pul, dol, round(n / days[dt], 5)])
    print(f"od: {total} Manhattan-internal trips, {len(rows)} nonzero cells, days per type {days}, holidays dropped {hol}")
    return {"days_per_type": days, "holidays_dropped": [d.isoformat() for d in hol], "trips": total}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", required=True, help="cache for raw downloads (not committed)")
    a = ap.parse_args()
    raw = Path(a.raw_dir)
    raw.mkdir(parents=True, exist_ok=True)
    zones = build_zones(raw)
    od = build_od_rates(raw, zones)
    build_places(raw, zones)
    manifest = {
        "built_by": "data_prep/build_commercial_v1.py",
        "tlc": {"months": TLC_MONTHS, "url_used": TLC_URL, "official_url": OFFICIAL_TLC_URL, **od},
        "zones": {"geojson_url_used": ZONE_GEOJSON_URL, "lookup_url_used": ZONE_LOOKUP_URL,
                  "official": [OFFICIAL_ZONE_SHAPEFILE_URL, OFFICIAL_ZONE_LOOKUP_URL], "excluded": sorted(EXCLUDED_ZONES)},
        "overture": {"release": OVERTURE_RELEASE, "path": "s3://" + OVERTURE_PLACES, "bbox": BBOX,
                     "commercial_top_categories": sorted(COMMERCIAL_TOP_CATEGORIES),
                     "excluded_basic_categories": sorted(EXCLUDED_BASIC_CATEGORIES), "min_confidence": MIN_CONFIDENCE,
                     "licence": "Overture places: CDLA Permissive 2.0 (some sources ODbL); see docs.overturemaps.org"},
        "outputs_sha256": {p.name: sha256(p) for p in sorted(OUT_DIR.iterdir()) if p.name != "MANIFEST.json"},
    }
    with open(OUT_DIR / "MANIFEST.json", "w") as f:
        json.dump(manifest, f, indent=1)
    print("wrote", OUT_DIR)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(HERE.parent))
    main()
