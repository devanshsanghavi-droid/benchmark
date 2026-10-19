import sys, duckdb
d = sys.argv[1]
con = duckdb.connect()
q = lambda s: print(con.execute(s).fetchdf().to_string())
print("== yellow: share of tolled trips at 6.55 vs 6.94 by month 2023")
q(f"""select month(tpep_pickup_datetime) m, sum(case when round(tolls_amount,2)=6.55 then 1 else 0 end) n655, sum(case when round(tolls_amount,2)=6.94 then 1 else 0 end) n694
 from read_parquet('{d}/yellow_2023-0[7-9].parquet') where tpep_pickup_datetime>='2023-07-01' and tpep_pickup_datetime<'2023-10-01' group by 1 order by 1""")
q(f"""select cast(tpep_pickup_datetime as date) dt, sum(case when round(tolls_amount,2)=6.55 then 1 else 0 end) n655, sum(case when round(tolls_amount,2)=6.94 then 1 else 0 end) n694
 from read_parquet('{d}/yellow_2023-08.parquet') where tpep_pickup_datetime>='2023-08-03' and tpep_pickup_datetime<'2023-08-09' group by 1 order by 1""")
print("== HVFHV Jan 2023: long trips (EV range relevance)")
q(f"""select count(*) n, round(avg(case when trip_miles>30 then 1.0 else 0 end)*100,3) gt30, round(avg(case when trip_miles>50 then 1.0 else 0 end)*100,3) gt50,
 round(avg(case when trip_miles>100 then 1.0 else 0 end)*100,4) gt100, round(avg(trip_miles/(trip_time/3600.0)),1) mean_mph,
 round(sum(trip_miles)/sum(trip_time)*3600,1) agg_mph
 from '{d}/fhvhv_2023-01.parquet' where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' and trip_miles>0 and trip_time>0""")
print("== HVFHV Jan 2023: Manhattan-internal trips speed (borough via zone lookup)")
con.execute(f"create table z as select * from read_csv_auto('{d}/taxi_zone_lookup.csv')")
q(f"""select zp.Borough pb, count(*) n, round(sum(trip_miles)/sum(trip_time)*3600,1) mph, round(avg(trip_miles),2) avg_mi
 from '{d}/fhvhv_2023-01.parquet' t join z zp on t.PULocationID=zp.LocationID join z zd on t.DOLocationID=zd.LocationID
 where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' and trip_miles>0 and trip_time>0 and zp.Borough=zd.Borough group by 1 order by 2 desc""")
