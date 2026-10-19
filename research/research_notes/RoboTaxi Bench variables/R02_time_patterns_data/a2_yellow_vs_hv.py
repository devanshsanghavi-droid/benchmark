import sys, duckdb, pandas as pd
d = sys.argv[1]
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300); pd.set_option('display.max_columns', 30)
con = duckdb.connect(); con.execute("PRAGMA threads=4")
con.execute(f"""create view hv as select pickup_datetime pu, PULocationID pul, DOLocationID dol, trip_miles mi, trip_time tt, driver_pay pay
 from '{d}/fhvhv_2023-01.parquet' where pickup_datetime >= '2023-01-01' and pickup_datetime < '2023-02-01'""")
con.execute(f"""create view ye as select tpep_pickup_datetime pu, tpep_dropoff_datetime dof, PULocationID pul, DOLocationID dol, trip_distance mi,
 epoch(tpep_dropoff_datetime - tpep_pickup_datetime) tt, fare_amount fare, extra, tip_amount tip, payment_type pt, total_amount tot, RatecodeID rc, airport_fee af, congestion_surcharge cs
 from '{d}/yellow_2023-01.parquet' where tpep_pickup_datetime >= '2023-01-01' and tpep_pickup_datetime < '2023-02-01'""")
wk = "dayofweek(pu) between 1 and 5 and cast(pu as date) not in ('2023-01-02','2023-01-16')"
print("yellow rows", con.execute("select count(*) from ye").fetchone())
# 15-min weekday bins 13:00-20:00, yellow vs hv
q = f"""
with y as (select (hour(pu)*60+minute(pu))//15 b, count(*)/20.0 n from ye where {wk} group by 1),
     h as (select (hour(pu)*60+minute(pu))//15 b, count(*)/20.0 n from hv where {wk} group by 1)
select lpad(cast(y.b*15//60 as varchar),2,'0')||':'||lpad(cast(y.b*15%60 as varchar),2,'0') t, round(y.n) yellow, round(h.n) hvfhv, round(y.n/h.n,4) ratio
from y join h using(b) where y.b between 48 and 84 order by y.b"""
print(con.execute(q).fetchdf().to_string())
# Yellow hourly profile by daytype
q = f"""select case when {wk} then 'Wkday' when dayofweek(pu)=6 then 'Sat' when dayofweek(pu)=0 and cast(pu as date)<>'2023-01-01' then 'Sun' else 'other' end dtp, hour(pu) h,
 count(*)*1.0/count(distinct cast(pu as date)) per_day,
 round(sum(mi)/sum(tt)*3600,1) mph,
 round(avg(extra),2) avg_extra,
 round(100*sum(case when pt=1 then tip else 0 end)/nullif(sum(case when pt=1 then fare else 0 end),0),1) tip_pct_card,
 round(100*avg(case when pt=1 then 1 else 0 end),1) card_share,
 round(avg(fare),2) avg_fare
 from ye where tt between 60 and 10800 and mi between 0.1 and 100 group by 1,2 order by 1,2"""
yh = con.execute(q).fetchdf(); print(yh.to_string()); yh.to_csv(f"{sys.argv[2]}/yellow_2023-01_hourly.csv", index=False)
# Extra component distribution by hour on weekdays vs weekend to check surcharge structure
q = f"""select case when {wk} then 'Wkday' else 'Wkend/hol' end dt, hour(pu) h, mode(extra) mode_extra, count(*) n from ye where fare>0 group by 1,2 order by 1,2"""
print(con.execute(q).fetchdf().pivot(index='h', columns='dt', values='mode_extra').to_string())
print(con.execute("select airport_fee, count(*) from (select af airport_fee from ye) group by 1 order by 2 desc limit 5").fetchall())
print(con.execute("select rc, count(*) from ye group by 1 order by 2 desc limit 8").fetchall())
