import sys, duckdb
d = sys.argv[1]
con = duckdb.connect()
con.execute("PRAGMA threads=4")
f = f"{d}/fhvhv_2023-01.parquet"
print(con.execute(f"select hvfhs_license_num, count(*), count(on_scene_datetime), min(pickup_datetime), max(pickup_datetime) from '{f}' group by 1").fetchall())
con.execute(f"""
create table t as select
  hvfhs_license_num lic, request_datetime rq, on_scene_datetime os, pickup_datetime pu, dropoff_datetime dropt,
  PULocationID pul, DOLocationID dol, trip_miles mi, trip_time tt, base_passenger_fare fare, tolls, bcf, sales_tax, congestion_surcharge cs, airport_fee af, tips, driver_pay pay, shared_request_flag srf
from '{f}' where pickup_datetime >= '2023-01-01' and pickup_datetime < '2023-02-01'
""")
con.execute("""create table t2 as select *, hour(pu) h, dayofweek(pu) dow, cast(pu as date) dt,
 case when cast(pu as date) in ('2023-01-01','2023-01-02','2023-01-16') then 'holiday'
      when dayofweek(pu)=0 then 'Sun' when dayofweek(pu)=6 then 'Sat' else 'Wkday' end daytype from t""")
print("rows", con.execute("select count(*) from t2").fetchone())
# day counts
dc = dict(con.execute("select daytype, count(distinct dt) from t2 group by 1").fetchall()); print(dc)
q = """
select daytype, h, count(*)*1.0/count(distinct dt) trips_per_day,
 round(median(epoch(pu - rq))/60.0,2) med_req_to_pu_min,
 round(median(epoch(os - rq))/60.0,2) med_req_to_onscene_min,
 round(sum(mi)/sum(tt)*3600,1) mph,
 round(avg(mi),2) avg_mi, round(avg(tt)/60,1) avg_min,
 round(avg(pay),2) pay_trip, round(sum(pay)/sum(tt)*3600,1) pay_per_engaged_hr,
 round(sum(fare)/sum(mi),2) fare_per_mi, round(sum(fare)/sum(tt)*60,2) fare_per_min,
 round(avg(case when tips>0 then 1 else 0 end)*100,1) tip_incid_pct, round(avg(tips),2) avg_tip,
 round(avg(case when pul in (1,132,138) then 1 else 0 end)*100,1) apt_pu_pct,
 round(avg(case when dol in (1,132,138) then 1 else 0 end)*100,1) apt_do_pct
from t2 where daytype in ('Wkday','Sat','Sun') group by 1,2 order by 1,2"""
res = con.execute(q).fetchdf()
import pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200); pd.set_option('display.max_columns', 30)
print(res.to_string())
res.to_csv(f"{sys.argv[2]}/hvfhv_2023-01_hourly.csv", index=False)
print(con.execute("select dayname(dt) dn, count(*)*1.0/count(distinct dt) per_day, round(sum(pay)/sum(tt)*3600,1) pay_eng_hr, round(avg(pay),2) pay_trip from t2 where daytype<>'holiday' group by 1 order by 2 desc").fetchdf().to_string())
print(con.execute("select dt, dayname(dt), count(*) n, round(sum(pay)/sum(tt)*3600,1) pay_eng_hr from t2 group by 1,2 order by 1").fetchdf().to_string())
