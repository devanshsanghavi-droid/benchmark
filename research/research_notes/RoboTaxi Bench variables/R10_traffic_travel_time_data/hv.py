import sys, duckdb
D=sys.argv[1]
c=duckdb.connect(); c.execute("PRAGMA threads=4")
f=f"{D}/fhvhv_2023-01.parquet"; z=f"{D}/taxi_zone_lookup.csv"
q=lambda s: print(c.execute(s).fetchdf().to_string())
c.execute(f"""create table t as select hvfhs_license_num lic, request_datetime rq, on_scene_datetime os, pickup_datetime pu, dropoff_datetime dropt,
 PULocationID pul, DOLocationID dol, trip_miles mi, trip_time tt, wav_match_flag wmf, wav_request_flag wrf
 from '{f}' where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01'""")
c.execute(f"create table zl as select * from read_csv_auto('{z}')")
print("== on_scene coverage by licence (HV0003 Uber, HV0005 Lyft)")
q("select lic, count(*) n, round(avg(case when os is not null then 1 else 0 end)*100,2) os_pct, round(avg(case when wmf='Y' then 1 else 0 end)*100,2) wav_match_pct from t group by 1 order by 2 desc")
print("== Uber: pickup minus on_scene (dwell) minutes, quantiles; and share negative")
q("""select count(*) n, round(avg(case when epoch(pu-os)<0 then 1 else 0 end)*100,2) neg_pct,
 quantile_cont(epoch(pu-os)/60.0,[0.1,0.25,0.5,0.75,0.9,0.95]) q_min, round(avg(epoch(pu-os))/60.0,2) mean_min
 from t where lic='HV0003' and os is not null""")
print("== Uber dwell by pickup type")
q("""select case when pul in (132,138,1) then 'airport' when zl.Borough='Manhattan' then 'Manhattan' else 'outer' end typ, count(*) n,
 quantile_cont(epoch(pu-os)/60.0,[0.25,0.5,0.75,0.9]) q_min from t join zl on t.pul=zl.LocationID where lic='HV0003' and os is not null and epoch(pu-os)>=0 group by 1 order by 1""")
print("== request -> on_scene (en route, Uber) and request -> pickup (all) by pickup borough, minutes")
q("""select zl.Borough, count(*) n, round(avg(epoch(pu-rq))/60.0,2) mean_req_pu_all, round(median(epoch(pu-rq))/60.0,2) med_req_pu_all,
 round(avg(case when lic='HV0003' then epoch(os-rq) end)/60.0,2) mean_req_os_uber, round(median(case when lic='HV0003' then epoch(os-rq) end)/60.0,2) med_req_os_uber
 from t join zl on t.pul=zl.LocationID where epoch(pu-rq) between 0 and 3600 group by 1 order by 2 desc""")
q("""select round(avg(epoch(pu-rq))/60.0,2) mean_req_pu_all_city, round(avg(case when lic='HV0003' then epoch(os-rq) end)/60.0,2) mean_req_os_uber_city from t where epoch(pu-rq) between 0 and 3600""")
print("== weekday trip speed (sum mi / sum time) by hour: midtown core intra, Manhattan south of 60th intra, citywide")
mid="(161,162,163,164,230,100,186)"
s60="(4,12,13,45,48,50,68,79,87,88,90,100,107,113,114,125,137,144,148,158,161,162,163,164,170,186,209,211,224,229,230,231,232,233,234,246,249,261)"
q(f"""select hour(pu) h,
 round(sum(case when pul in {mid} and dol in {mid} then mi end)/sum(case when pul in {mid} and dol in {mid} then tt end)*3600,2) midtown_mph,
 count(case when pul in {mid} and dol in {mid} then 1 end) n_mid,
 round(sum(case when pul in {s60} and dol in {s60} then mi end)/sum(case when pul in {s60} and dol in {s60} then tt end)*3600,2) s60_mph,
 round(sum(mi)/sum(tt)*3600,2) city_mph
 from t where dayofweek(pu) between 1 and 5 and cast(pu as date) not in ('2023-01-02','2023-01-16') and tt>0 group by 1 order by 1""")
