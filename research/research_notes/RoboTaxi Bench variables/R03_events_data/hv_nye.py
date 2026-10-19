import sys, duckdb, pandas as pd
f=sys.argv[1]; con=duckdb.connect(); con.execute("PRAGMA threads=4")
q=f"""with t as (select cast(pickup_datetime as date)='2023-01-01' jan1, hour(pickup_datetime) h, pickup_datetime pu, request_datetime rq, trip_miles mi, base_passenger_fare fare, driver_pay pay, trip_time tt
  from '{f}' where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' and dayofweek(pickup_datetime)=0 and hour(pickup_datetime)<4 and trip_miles between 0.5 and 30)
  select jan1, h, count(*)/(case when jan1 then 1.0 else 4.0 end) n, sum(fare)/sum(mi) fpm, median(epoch(pu-rq)/60) wait, sum(pay)/sum(tt/3600.0) payhr from t group by 1,2 order by 2,1"""
print(con.execute(q).fetchdf().round(2).to_string())
