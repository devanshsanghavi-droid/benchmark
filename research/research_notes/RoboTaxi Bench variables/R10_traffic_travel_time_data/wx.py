import sys, duckdb
D=sys.argv[1]; W=sys.argv[2]
c=duckdb.connect(); c.execute("PRAGMA threads=4")
q=lambda s: print(c.execute(s).fetchdf().to_string())
c.execute(f"""create table yc as select cast(tpep_pickup_datetime as date) dt, hour(tpep_pickup_datetime) h, dayofweek(tpep_pickup_datetime) dow,
 PULocationID pul, DOLocationID dol, trip_distance mi, epoch(tpep_dropoff_datetime - tpep_pickup_datetime) dur
 from read_parquet('{D}/yellow_2023-*.parquet') where tpep_pickup_datetime>='2023-01-01' and tpep_pickup_datetime<'2024-01-01'
 and epoch(tpep_dropoff_datetime - tpep_pickup_datetime) between 60 and 10800 and trip_distance>0
 and trip_distance/(epoch(tpep_dropoff_datetime - tpep_pickup_datetime)/3600.0) between 1 and 60""")
hol="('2023-01-02','2023-01-16','2023-02-20','2023-05-29','2023-06-19','2023-07-04','2023-07-03','2023-09-04','2023-10-09','2023-11-10','2023-11-23','2023-11-24','2023-12-25','2023-12-26')"
s60="(4,12,13,45,48,50,68,79,87,88,90,100,107,113,114,125,137,144,148,158,161,162,163,164,170,186,209,211,224,229,230,231,232,233,234,246,249,261)"
c.execute(f"""create table dd as select dt, h, sum(mi)/sum(dur)*3600 mph from yc where pul in {s60} and dol in {s60} and dow between 1 and 5 and dt not in {hol} and h between 7 and 20 group by 1,2""")
c.execute("""create table hm as select month(dt) m, h, median(mph) mmph from dd group by 1,2""")
c.execute("""create table dayf as select dt, avg(dd.mph/hm.mmph) f from dd join hm on month(dd.dt)=hm.m and dd.h=hm.h group by 1""")
c.execute(f"""create table wx as select cast(DATE as date) dt, cast(PRCP as double) p, cast(SNOW as double) s from read_csv_auto('{W}', all_varchar=true)""")
print("== weekday speed factor (vs same month-hour median, Manhattan below 60th, 7AM-8PM) by Central Park daily precipitation, 2023")
q("""select case when s>0 then 'e snow>0' when p=0 then 'a dry' when p<0.25 then 'b 0.01-0.24in' when p<1 then 'c 0.25-0.99in' else 'd >=1in' end cat,
 count(*) n, round(median(f),3) med_f, round(avg(f),3) mean_f, round(min(f),3) min_f from dayf join wx using(dt) group by 1 order by 1""")
q("select dt, p, s, round(f,3) f from dayf join wx using(dt) where p>=1 or s>0 order by dt")
