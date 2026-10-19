import sys, duckdb, pandas as pd
pd.set_option('display.width', 250)
d = sys.argv[1]
con = duckdb.connect(); con.execute("PRAGMA threads=4")
q = lambda s: print(con.execute(s).fetchdf().to_string())
con.execute(f"""create table t as select PULocationID pul, pickup_datetime pu from '{d}/fhvhv_2023-01.parquet' where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01'""")
print("== overdispersion: zone x hour over Tue-Thu (13 days in Jan 2023), cells with mean >=50 trips")
q("""with c as (select pul, hour(pu) h, cast(pu as date) dt, count(*) n from t where dayofweek(pu) in (2,3,4) group by 1,2,3),
 s as (select pul, h, avg(n) m, stddev_samp(n) sd, count(*) k from c group by 1,2 having count(*)>=11 and avg(n)>=50)
 select count(*) cells, round(median(sd/m)*100,1) med_cv, round(quantile_cont(sd/m,0.25)*100,1) p25_cv, round(quantile_cont(sd/m,0.75)*100,1) p75_cv,
 round(median(1/sqrt(m))*100,1) med_poisson_cv, round(median((sd*sd)/m),2) med_var_to_mean from s""")
print("== citywide daily total CV on Tue-Thu")
q("""with c as (select cast(pu as date) dt, count(*) n from t where dayofweek(pu) in (2,3,4) group by 1) select count(*) ndays, round(stddev_samp(n)/avg(n)*100,1) cv from c""")
