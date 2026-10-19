import sys, duckdb
S = sys.argv[1]; out = sys.argv[2]
con = duckdb.connect(); con.execute("PRAGMA threads=4")
files = [f"{S}/data/yellow_2023-{m:02d}.parquet" for m in range(1,13)] + [f"{S}/data/yellow_2024-01.parquet"]
flist = "[" + ",".join(f"'{f}'" for f in files) + "]"
q = f"""
copy (
select cast(tpep_pickup_datetime as date) dt,
 hour(tpep_pickup_datetime) h,
 count(*) n,
 sum(fare_amount) fare, sum(trip_distance) mi,
 sum(epoch(tpep_dropoff_datetime - tpep_pickup_datetime))/3600.0 hrs,
 sum(case when payment_type=1 then 1 else 0 end) n_card,
 sum(case when payment_type=1 then fare_amount else 0 end) fare_card,
 sum(case when payment_type=1 then tip_amount else 0 end) tip_card,
 sum(case when payment_type=1 and tip_amount>0 then 1 else 0 end) n_card_tip,
 sum(case when PULocationID in (1,132,138) then 1 else 0 end) n_apt_pu,
 sum(case when DOLocationID in (1,132,138) then 1 else 0 end) n_apt_do,
 sum(case when trip_distance < 1.0 then 1 else 0 end) n_short,
 sum(case when payment_type=3 or payment_type=4 then 1 else 0 end) n_nocharge_dispute
from read_parquet({flist})
where tpep_pickup_datetime >= '2023-01-01' and tpep_pickup_datetime < '2024-02-01'
 and trip_distance > 0 and trip_distance < 100 and fare_amount > 0 and fare_amount < 500
 and epoch(tpep_dropoff_datetime - tpep_pickup_datetime) between 60 and 3*3600
group by 1,2 order by 1,2) to '{out}' (header, delimiter ',')
"""
con.execute(q)
print(con.execute(f"select count(*), sum(n) from read_csv_auto('{out}')").fetchall())
