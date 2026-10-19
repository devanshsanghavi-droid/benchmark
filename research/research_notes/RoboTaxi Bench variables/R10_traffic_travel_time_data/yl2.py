import sys, duckdb
D=sys.argv[1]
c=duckdb.connect(); c.execute("PRAGMA threads=4")
q=lambda s: print(c.execute(s).fetchdf().to_string())
c.execute(f"""create table y as select tpep_pickup_datetime pu, tpep_dropoff_datetime dr, PULocationID pul, DOLocationID dol, trip_distance mi,
 epoch(tpep_dropoff_datetime - tpep_pickup_datetime) dur from read_parquet('{D}/yellow_2023-*.parquet')
 where tpep_pickup_datetime>='2023-01-01' and tpep_pickup_datetime<'2024-01-01'""")
print("rows", c.execute("select count(*) from y").fetchone())
c.execute("""create table yc as select *, hour(pu) h, dayofweek(pu) dow, cast(pu as date) dt from y
 where dur between 60 and 3*3600 and mi>0 and mi/(dur/3600.0) between 1 and 60""")
hol="('2023-01-02','2023-01-16','2023-02-20','2023-05-29','2023-06-19','2023-07-04','2023-09-04','2023-10-09','2023-11-10','2023-11-23','2023-11-24','2023-12-25','2023-12-26')"
print("== day-level factor: Manhattan-below-60th intra trips, weekday non-holiday, daily speed / annual same-hour speed (hours 8-19)")
s60="(4,12,13,45,48,50,68,79,87,88,90,100,107,113,114,125,137,144,148,158,161,162,163,164,170,186,209,211,224,229,230,231,232,233,234,246,249,261)"
c.execute(f"""create table dd as select dt, h, sum(mi)/sum(dur)*3600 mph, count(*) n from yc where pul in {s60} and dol in {s60} and dow between 1 and 5 and dt not in {hol} and h between 8 and 19 group by 1,2""")
c.execute("create table hh as select h, median(mph) mmph from dd group by 1")
c.execute("create table dayf as select dt, avg(dd.mph/hh.mmph) f from dd join hh using(h) group by 1")
q("select count(*) ndays, quantile_cont(f,[0.01,0.05,0.25,0.5,0.75,0.95,0.99]) q, min(f), max(f) from dayf")
q("select dt, round(f,3) f from dayf order by f limit 8")
q("select dt, round(f,3) f from dayf order by f desc limit 5")
print("== yellow weekday mph by hour, Manhattan below 60th intra (2023)")
q(f"select h, round(sum(mi)/sum(dur)*3600,2) mph, count(*) n from yc where pul in {s60} and dol in {s60} and dow between 1 and 5 and dt not in {hol} group by 1 order by 1")
print("== by month, s60 intra weekday 8-19 mph")
q(f"select month(pu) m, round(sum(mi)/sum(dur)*3600,2) mph from yc where pul in {s60} and dol in {s60} and dow between 1 and 5 and dt not in {hol} and h between 8 and 19 group by 1 order by 1")
