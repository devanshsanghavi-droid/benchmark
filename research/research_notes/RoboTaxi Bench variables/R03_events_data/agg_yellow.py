import sys, duckdb
d, out = sys.argv[1], sys.argv[2]
con = duckdb.connect(); con.execute("PRAGMA threads=4")
files = [f"{d}/yellow_2023-{m:02d}.parquet" for m in range(1,13)] + [f"{d}/yellow_2024-01.parquet"]
flist = "[" + ",".join(f"'{f}'" for f in files) + "]"
con.execute(f"""create view y as select tpep_pickup_datetime pu, tpep_dropoff_datetime dof, PULocationID pul, DOLocationID dol,
  trip_distance mi, fare_amount fare, tip_amount tip, total_amount tot, RatecodeID rc,
  epoch(tpep_dropoff_datetime - tpep_pickup_datetime)/60.0 dur
  from read_parquet({flist}, union_by_name=true)
  where tpep_pickup_datetime >= '2023-01-01' and tpep_pickup_datetime < '2024-02-01'""")
con.execute(f"""copy (select cast(pu as date) dt, hour(pu) h, pul, count(*) n, sum(fare) fare, sum(tot) tot, sum(mi) mi, sum(dur) dur,
   sum(case when dur between 1 and 180 and mi between 0.1 and 100 then mi end) mi_ok, sum(case when dur between 1 and 180 and mi between 0.1 and 100 then dur end) dur_ok
   from y group by all) to '{out}/pu_date_hour_zone.parquet' (format parquet)""")
con.execute(f"""copy (select cast(dof as date) dt, hour(dof) h, dol, count(*) n from y where dof >= '2023-01-01' and dof < '2024-02-01' group by all) to '{out}/do_date_hour_zone.parquet' (format parquet)""")
con.execute(f"""copy (select cast(pu as date) dt, hour(pu) h, (minute(pu)//15) q, pul, dol, count(*) n, sum(fare) fare, sum(tot) tot, sum(mi) mi, sum(dur) dur
   from y where pul in (230,186,246,93,253,247,43,194,265,132,138) or dol in (230,186,246,93,253,247,194,265,1,132,138) group by all) to '{out}/focus_15min_od.parquet' (format parquet)""")
print(con.execute(f"select count(*), sum(n) from '{out}/pu_date_hour_zone.parquet'").fetchall())
