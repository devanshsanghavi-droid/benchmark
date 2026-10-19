import sys, duckdb
D=sys.argv[1]
c=duckdb.connect(); c.execute("PRAGMA threads=4")
q=lambda s: print(c.execute(s).fetchdf().to_string())
c.execute(f"""create table y as select tpep_pickup_datetime pu, tpep_dropoff_datetime dr, PULocationID pul, DOLocationID dol, trip_distance mi,
 epoch(tpep_dropoff_datetime - tpep_pickup_datetime) dur from read_parquet('{D}/yellow_2023-*.parquet')
 where tpep_pickup_datetime>='2023-01-01' and tpep_pickup_datetime<'2024-01-01'""")
print("rows", c.execute("select count(*) from y").fetchone())
print("== cleaning-rule shares (pct of 2023 yellow trips)")
q("""select round(avg(case when dur<60 then 1 else 0 end)*100,2) lt60s, round(avg(case when dur<10 then 1 else 0 end)*100,2) lt10s,
 round(avg(case when dur>3*3600 then 1 else 0 end)*100,3) gt3h, round(avg(case when dur>24*3600 then 1 else 0 end)*100,4) gt24h,
 round(avg(case when mi<=0 then 1 else 0 end)*100,2) zero_dist,
 round(avg(case when dur>0 and mi/(dur/3600.0)>60 then 1 else 0 end)*100,2) gt60mph,
 round(avg(case when dur>0 and mi>0 and mi/(dur/3600.0)<1 then 1 else 0 end)*100,2) lt1mph from y""")
c.execute("""create table yc as select *, hour(pu) h, dayofweek(pu) dow, cast(pu as date) dt from y
 where dur between 60 and 3*3600 and mi>0 and mi/(dur/3600.0) between 1 and 60""")
hol="('2023-01-02','2023-01-16','2023-02-20','2023-05-29','2023-06-19','2023-07-04','2023-09-04','2023-10-09','2023-11-10','2023-11-23','2023-11-24','2023-12-25','2023-12-26')"
mid="(161,162,163,164,230,100,186)"
print("== Midtown core -> JFK(132), weekdays 2023: minutes by pickup hour")
q(f"""select h, count(*) n, round(quantile_cont(dur,0.1)/60,1) p10, round(median(dur)/60,1) med, round(quantile_cont(dur,0.9)/60,1) p90,
 round(quantile_cont(dur,0.9)/median(dur),2) p90_over_med from yc where pul in {mid} and dol=132 and dow between 1 and 5 and dt not in {hol} group by 1 order by 1""")
print("== Midtown core -> LGA(138), weekdays 2023")
q(f"""select h, count(*) n, round(quantile_cont(dur,0.1)/60,1) p10, round(median(dur)/60,1) med, round(quantile_cont(dur,0.9)/60,1) p90 from yc where pul in {mid} and dol=138 and dow between 1 and 5 and dt not in {hol} group by 1 order by 1""")
print("== Midtown core -> EWR(1), weekdays 2023 (selected)")
q(f"""select case when h between 6 and 9 then 'am' when h between 10 and 14 then 'mid' when h between 15 and 19 then 'pm' else 'night' end b, count(*) n, round(median(dur)/60,1) med, round(quantile_cont(dur,0.9)/60,1) p90 from yc where pul in {mid} and dol=1 and dow between 1 and 5 and dt not in {hol} group by 1 order by 1""")
print("== trip-level noise: per OD x weekday-hour cell with >=50 trips (weekdays, non-holiday): sd(log dur), CV, P90/median")
c.execute(f"""create table cells as select pul, dol, h, count(*) n, stddev_samp(ln(dur)) sdlog, stddev_samp(dur)/avg(dur) cv,
 quantile_cont(dur,0.9)/median(dur) r90, median(mi) medmi from yc where dow between 1 and 5 and dt not in {hol} and pul<>dol and pul<264 and dol<264 group by 1,2,3 having count(*)>=50""")
q("""select count(*) cells, sum(n) trips, quantile_cont(sdlog,[0.1,0.25,0.5,0.75,0.9]) sdlog_q, quantile_cont(cv,[0.1,0.5,0.9]) cv_q, quantile_cont(r90,[0.1,0.5,0.9]) r90_q from cells""")
q("""select case when medmi<1.5 then 'a <1.5mi' when medmi<3 then 'b 1.5-3' when medmi<6 then 'c 3-6' else 'd 6+' end band, count(*) cells, round(median(sdlog),3) med_sdlog, round(median(cv),3) med_cv, round(median(r90),3) med_r90 from cells group by 1 order by 1""")
print("== day-level factor: Manhattan-below-60th intra trips, weekday non-holiday, daily speed / annual same-hour speed (hours 8-19)")
s60="(4,12,13,45,48,50,68,79,87,88,90,100,107,113,114,125,137,144,148,158,161,162,163,164,170,186,209,211,224,229,230,231,232,233,234,246,249,261)"
c.execute(f"""create table dd as select dt, h, sum(mi)/sum(dur)*3600 mph, count(*) n from yc where pul in {s60} and dol in {s60} and dow between 1 and 5 and dt not in {hol} and h between 8 and 19 group by 1,2""")
c.execute("create table hh as select h, median(mph) mmph from dd group by 1")
c.execute("create table dayf as select dt, avg(dd.mph/hh.mmph) f from dd join hh using(h) group by 1")
q("select count(*) days, quantile_cont(f,[0.01,0.05,0.25,0.5,0.75,0.95,0.99]) q, min(f), max(f) from dayf")
q("select dt, round(f,3) f from dayf order by f limit 8")
q("select dt, round(f,3) f from dayf order by f desc limit 5")
print("== yellow weekday mph by hour, Manhattan below 60th intra (2023)")
q(f"select h, round(sum(mi)/sum(dur)*3600,2) mph, count(*) n from yc where pul in {s60} and dol in {s60} and dow between 1 and 5 and dt not in {hol} group by 1 order by 1")
print("== by month, s60 intra weekday 8-19 mph")
q(f"select month(pu) m, round(sum(mi)/sum(dur)*3600,2) mph from yc where pul in {s60} and dol in {s60} and dow between 1 and 5 and dt not in {hol} and h between 8 and 19 group by 1 order by 1")
