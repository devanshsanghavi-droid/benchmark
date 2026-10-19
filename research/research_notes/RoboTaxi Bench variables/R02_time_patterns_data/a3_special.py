import sys, duckdb, pandas as pd
d = sys.argv[1]
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300); pd.set_option('display.max_columns', 40)
con = duckdb.connect(); con.execute("PRAGMA threads=4")
con.execute(f"""create table hv as select pickup_datetime pu, request_datetime rq, PULocationID pul, DOLocationID dol, trip_miles mi, trip_time tt, driver_pay pay, base_passenger_fare fare
 from '{d}/fhvhv_2023-01.parquet' where pickup_datetime >= '2023-01-01' and pickup_datetime < '2023-02-01'""")
# 1. NYE/NYD early morning vs other Sundays
q = """select hour(pu) h,
 sum(case when cast(pu as date)='2023-01-01' then 1 else 0 end) jan1,
 round(sum(case when dayofweek(pu)=0 and cast(pu as date)<>'2023-01-01' then 1 else 0 end)/4.0) other_sun,
 round(sum(case when cast(pu as date)='2023-01-01' then pay else 0 end)/sum(case when cast(pu as date)='2023-01-01' then tt else 0 end)*3600,1) jan1_payhr,
 round(sum(case when dayofweek(pu)=0 and cast(pu as date)<>'2023-01-01' then pay else 0 end)/sum(case when dayofweek(pu)=0 and cast(pu as date)<>'2023-01-01' then tt else 0 end)*3600,1) sun_payhr,
 round(median(case when cast(pu as date)='2023-01-01' then epoch(pu-rq)/60 end),1) jan1_wait,
 round(median(case when dayofweek(pu)=0 and cast(pu as date)<>'2023-01-01' then epoch(pu-rq)/60 end),1) sun_wait
 from hv where dayofweek(pu)=0 group by 1 order by 1"""
print("NYD vs other Sundays (HVFHV)"); print(con.execute(q).fetchdf().to_string())
# 2. Theatre district zone 230 pickups by 15-min, by weekday name, 15:30-18:30 and 21:30-23:30
q = """select dayname(pu) dn, (hour(pu)*60+minute(pu))//15 b, count(*)*1.0/count(distinct cast(pu as date)) n from hv where pul=230 and cast(pu as date) not in ('2023-01-01','2023-01-02','2023-01-16') group by 1,2"""
t = con.execute(q).fetchdf()
t['t'] = t.b.apply(lambda b: f"{b*15//60:02d}:{b*15%60:02d}")
pv = t.pivot(index='t', columns='dn', values='n')[['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']].round(0)
print("Theatre district (230) pickups per 15 min"); print(pv.loc['15:30':'18:30'].to_string()); print(pv.loc['21:00':'23:45'].to_string())
# 3. nightlife zones Sat/Sun early morning 15-min
q = """select case when dayofweek(pu)=6 then 'SatAM' when dayofweek(pu)=0 and cast(pu as date)<>'2023-01-01' then 'SunAM' else 'WkdayAM' end k,
 (hour(pu)*60+minute(pu))//15 b, count(*)*1.0/count(distinct cast(pu as date)) n
 from hv where pul in (79,148,249,255,256,113,114,144,4,232) and hour(pu)<7 and cast(pu as date) not in ('2023-01-01','2023-01-02','2023-01-16') group by 1,2"""
t = con.execute(q).fetchdf(); t['t'] = t.b.apply(lambda b: f"{b*15//60:02d}:{b*15%60:02d}")
print("Nightlife zones pickups per 15 min"); print(t.pivot(index='t', columns='k', values='n').round(0).to_string())
# 4. Airport pickups by hour (counts/day) weekday vs weekend
q = """select hour(pu) h,
 round(sum(case when pul=132 and dayofweek(pu) between 1 and 5 then 1 else 0 end)/22.0) jfk_pu_wk, round(sum(case when pul=138 and dayofweek(pu) between 1 and 5 then 1 else 0 end)/22.0) lga_pu_wk,
 round(sum(case when pul=132 and dayofweek(pu) in (0,6) then 1 else 0 end)/9.0) jfk_pu_we, round(sum(case when pul=138 and dayofweek(pu) in (0,6) then 1 else 0 end)/9.0) lga_pu_we,
 round(sum(case when dol=132 and dayofweek(pu) between 1 and 5 then 1 else 0 end)/22.0) jfk_do_wk, round(sum(case when dol=138 and dayofweek(pu) between 1 and 5 then 1 else 0 end)/22.0) lga_do_wk,
 round(median(case when pul=132 then epoch(pu-rq)/60 end),1) jfk_wait, round(median(case when pul=138 then epoch(pu-rq)/60 end),1) lga_wait
 from hv group by 1 order by 1"""
print("Airport pickups/dropoffs by hour"); print(con.execute(q).fetchdf().to_string())
# 5. Lunch: Midtown/FiDi pickups by 15 min on weekdays 11:00-15:00
q = """select (hour(pu)*60+minute(pu))//15 b, count(*)/20.0 n, round(avg(mi),2) mi from hv where pul in (161,162,163,164,170,230,233,229,100,186,87,88,209,261,13) and dayofweek(pu) between 1 and 5 and cast(pu as date) not in ('2023-01-02','2023-01-16') group by 1 order by 1"""
t = con.execute(q).fetchdf(); t['t'] = t.b.apply(lambda b: f"{b*15//60:02d}:{b*15%60:02d}")
print("Midtown+FiDi weekday pickups per 15 min (selected)"); print(t[(t.b>=24)&(t.b<=84)][['t','n','mi']].to_string())
