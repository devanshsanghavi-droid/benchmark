import sys, duckdb, pandas as pd
pd.set_option('display.width', 250)
d = sys.argv[1]
con = duckdb.connect(); con.execute("PRAGMA threads=4")
q = lambda s: print(con.execute(s).fetchdf().to_string())
con.execute(f"create table z as select * from read_csv_auto('{d}/taxi_zone_lookup.csv')")
print("== Jan 2023 airport pickups per day: yellow vs HVFHV")
q(f"""select 'yellow' src, PULocationID z, count(*)/31.0 per_day from '{d}/yellow_2023-01.parquet' where PULocationID in (1,132,138) and tpep_pickup_datetime>='2023-01-01' and tpep_pickup_datetime<'2023-02-01' group by 1,2
 union all select 'hvfhv', PULocationID, count(*)/31.0 from '{d}/fhvhv_2023-01.parquet' where PULocationID in (1,132,138) and pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' group by 1,2 order by 2,1""")
print("== destination borough of JFK (132) and LGA (138) pickups, yellow + hvfhv Jan 2023")
q(f"""with a as (select PULocationID p, DOLocationID dl from '{d}/yellow_2023-01.parquet' where PULocationID in (132,138)
 union all select PULocationID, DOLocationID from '{d}/fhvhv_2023-01.parquet' where PULocationID in (132,138))
 select p, z.Borough, round(count(*)*100.0/sum(count(*)) over (partition by p),1) pct from a left join z on a.dl=z.LocationID group by 1,2 order by 1,3 desc""")
print("== yellow JFK pickups by ratecode Jan 2023")
q(f"""select RatecodeID, round(count(*)*100.0/sum(count(*)) over (),1) pct from '{d}/yellow_2023-01.parquet' where PULocationID=132 group by 1 order by 2 desc limit 5""")
