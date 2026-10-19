import sys, duckdb
S = sys.argv[1]; out = sys.argv[2]
con = duckdb.connect(); con.execute("PRAGMA threads=4")
f = f"{S}/data/fhvhv_2023-01.parquet"
q = f"""
copy (
select cast(request_datetime as date) dt, hour(request_datetime) h, hvfhs_license_num lic,
 count(*) n,
 median(epoch(on_scene_datetime - request_datetime))/60.0 med_wait_os,
 avg(epoch(on_scene_datetime - request_datetime))/60.0 avg_wait_os,
 median(epoch(pickup_datetime - request_datetime))/60.0 med_wait_pu,
 median(epoch(pickup_datetime - on_scene_datetime))/60.0 med_dwell,
 sum(base_passenger_fare) fare, sum(trip_miles) mi, sum(trip_time)/3600.0 hrs,
 sum(driver_pay) pay, sum(tips) tips, sum(case when tips>0 then 1 else 0 end) n_tip,
 sum(case when PULocationID in (1,132,138) then 1 else 0 end) n_apt_pu,
 sum(case when trip_miles < 1.0 then 1 else 0 end) n_short
from '{f}'
where request_datetime >= '2023-01-01' and request_datetime < '2023-02-01'
 and trip_miles > 0 and trip_time between 60 and 3*3600 and base_passenger_fare > 0
group by 1,2,3 order by 1,2,3) to '{out}' (header, delimiter ',')
"""
con.execute(q)
print(con.execute(f"select lic, count(*), sum(n) from read_csv_auto('{out}') group by 1").fetchall())
