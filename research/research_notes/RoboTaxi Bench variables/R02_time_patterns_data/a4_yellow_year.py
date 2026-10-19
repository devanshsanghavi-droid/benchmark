import sys, duckdb, pandas as pd, numpy as np
d, out = sys.argv[1], sys.argv[2]
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 400); pd.set_option('display.max_columns', 40)
con = duckdb.connect(); con.execute("PRAGMA threads=4")
con.execute(f"""create table y as select tpep_pickup_datetime pu, tpep_dropoff_datetime dof, PULocationID pul, DOLocationID dol, trip_distance mi,
 epoch(tpep_dropoff_datetime - tpep_pickup_datetime) tt, fare_amount fare, extra, tip_amount tip, payment_type pt
 from read_parquet('{d}/yellow_2023-*.parquet', union_by_name=true) where tpep_pickup_datetime >= '2023-01-01' and tpep_pickup_datetime < '2024-01-01'""")
print("rows", con.execute("select count(*) from y").fetchone())
daily = con.execute("""select cast(pu as date) dt, count(*) n, sum(case when tt between 60 and 10800 and mi between 0.1 and 100 then mi end)/sum(case when tt between 60 and 10800 and mi between 0.1 and 100 then tt end)*3600 mph from y group by 1 order by 1""").fetchdf()
daily['dt'] = pd.to_datetime(daily.dt); daily['dow'] = daily.dt.dt.dayofweek
hol = {'2023-01-01':"New Year's Day (Sun)",'2023-01-02':'NYD observed (Mon)','2023-01-16':'MLK Day','2023-01-22':'Lunar New Year (Sun)','2023-02-20':"Presidents' Day",
 '2023-04-09':'Easter Sunday','2023-04-21':'Eid al-Fitr (Fri)','2023-05-29':'Memorial Day','2023-06-19':'Juneteenth','2023-07-03':'Mon before July 4','2023-07-04':'Independence Day (Tue)',
 '2023-09-04':'Labor Day','2023-09-25':'Yom Kippur (Mon)','2023-10-09':'Columbus/Indigenous Day','2023-11-05':'Marathon + DST end (Sun)','2023-11-07':'Election Day','2023-11-22':'Wed before Thanksgiving',
 '2023-11-23':'Thanksgiving','2023-11-24':'Black Friday','2023-11-26':'Sun after Thanksgiving','2023-12-22':'Fri before Christmas','2023-12-24':'Christmas Eve (Sun)','2023-12-25':'Christmas (Mon)','2023-12-26':'Dec 26 (Tue)','2023-12-29':'Fri Dec 29','2023-12-31':"New Year's Eve (Sun)",
 '2023-03-12':'DST start (Sun)','2023-09-16':'Rosh Hashanah d1 (Sat)','2023-09-19':'UNGA high-level week (Tue)','2023-06-25':'Pride March (Sun)','2023-11-12':'Diwali (Sun)'}
hd = set(pd.to_datetime(list(hol.keys())))
rows=[]
for k,v in hol.items():
    t = pd.Timestamp(k); same = daily[(daily.dow==t.dayofweek)&(abs((daily.dt-t).dt.days)<=28)&(~daily.dt.isin(hd))]
    r = daily[daily.dt==t].iloc[0]
    rows.append((k,v,int(r.n),int(same.n.median()), round(r.n/same.n.median(),2), round(r.mph,1), round(same.mph.median(),1)))
print(pd.DataFrame(rows, columns=['date','label','trips','baseline_median_same_dow','ratio','mph','base_mph']).to_string())
# monthly weekday hourly share + mph
q = """select month(pu) m, hour(pu) h, count(*)*1.0/count(distinct cast(pu as date)) per_day,
 sum(case when tt between 60 and 10800 and mi between 0.1 and 100 then mi end)/sum(case when tt between 60 and 10800 and mi between 0.1 and 100 then tt end)*3600 mph
 from y where dayofweek(pu) between 1 and 5 group by 1,2"""
mh = con.execute(q).fetchdf()
print("weekday trips/day by month x hour"); print(mh.pivot(index='h', columns='m', values='per_day').round(0).to_string())
print("weekday mph by month x hour"); print(mh.pivot(index='h', columns='m', values='mph').round(1).to_string())
mh.to_csv(f"{out}/yellow_2023_month_hour.csv", index=False)
# DST days hour counts vs neighbouring Sundays
q = """select cast(pu as date) dt, hour(pu) h, count(*) n from y where cast(pu as date) in ('2023-03-05','2023-03-12','2023-03-19','2023-10-29','2023-11-05','2023-11-12') and hour(pu)<5 group by 1,2 order by 1,2"""
print(con.execute(q).fetchdf().pivot(index='h', columns='dt', values='n').to_string())
print("negative or zero durations on DST end day 1-2am:", con.execute("select count(*) from y where cast(pu as date)='2023-11-05' and hour(pu)=1 and tt<=0").fetchone(), con.execute("select count(*) from y where cast(pu as date)='2023-11-05' and hour(pu)=1").fetchone())
print("durations >2h starting 1-2am on spring DST:", con.execute("select count(*), avg(tt) from y where cast(pu as date)='2023-03-12' and hour(pu)=1 and dof >= '2023-03-12 03:00'").fetchone())
# rush surcharge on weekday holidays 16-20h
print(con.execute("""select cast(pu as date) dt, mode(extra) m, count(*) from y where cast(pu as date) in ('2023-07-04','2023-09-04','2023-11-23','2023-12-25','2023-07-05','2023-09-05') and hour(pu) between 16 and 19 and fare>0 group by 1 order by 1""").fetchall())
