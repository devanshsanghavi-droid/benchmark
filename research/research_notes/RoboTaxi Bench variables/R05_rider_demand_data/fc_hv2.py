import sys, duckdb, pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 100)
d = sys.argv[1]
con = duckdb.connect(); con.execute("PRAGMA threads=4")
q = lambda s: print(con.execute(s).fetchdf().to_string())

con.execute(f"""create table t as select PULocationID pul, DOLocationID dol, pickup_datetime pu, dropoff_datetime dof from '{d}/fhvhv_2023-01.parquet' where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01'""")
print("== DO/PU ratio per zone-hour (weekday, pooled over month), zones with >=50 PU per hour-slot-day avg")
q("""with p as (select pul z, hour(pu) h, count(*) n from t where dayofweek(pu) between 1 and 5 group by 1,2),
 o as (select dol z, hour(dof) h, count(*) n from t where dayofweek(dof) between 1 and 5 group by 1,2)
 select quantile_cont(o.n*1.0/p.n,[0.05,0.25,0.5,0.75,0.95]) q from p join o using(z,h) where p.n>=50*22""")
print("== nightlife zones hourly profile Sat+Sun early hours (79 East Village, 148 Lower East Side, 249 West Village)")
q("""select hour(pu) h, round(count(*)/count(distinct cast(pu as date)),0) per_day from t where pul in (79,148,249) and dayofweek(pu) in (6,0) group by 1 order by 1""")
print("== airport-bound share by hour, weekdays (22 Mon-Fri days in Jan 2023, incl. 2 holidays)")
q("""select hour(pu) h, round(avg(case when dol in (1,132,138) then 1.0 else 0 end)*100,1) apt_do_pct, round(sum(case when dol in (1,132,138) then 1 else 0 end)/22.0) apt_do_per_day from t where dayofweek(pu) between 1 and 5 group by 1 order by 1""")
