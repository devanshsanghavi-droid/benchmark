import sys, duckdb
d = sys.argv[1]
con = duckdb.connect()
con.execute("PRAGMA threads=4")
con.execute(f"""create table y as select tpep_pickup_datetime pu, passenger_count pc, trip_distance mi, RatecodeID rc, PULocationID pul, DOLocationID dol,
 payment_type pt, fare_amount fare, tolls_amount tolls, total_amount tot, month(tpep_pickup_datetime) m,
 epoch(tpep_dropoff_datetime - tpep_pickup_datetime) secs
 from read_parquet('{d}/yellow_2023-*.parquet') where tpep_pickup_datetime >= '2023-01-01' and tpep_pickup_datetime < '2024-01-01' and trip_distance>0 and fare_amount>0""")
q = lambda s: print(con.execute(s).fetchdf().to_string())
print("== passenger count distribution (2023, rows with pc not null)")
q("select pc, count(*) n, round(count(*)*100.0/sum(count(*)) over (),2) pct from y where pc is not null group by 1 order by 1")
print("== tolls")
q("""select round(avg(case when tolls>0 then 1 else 0 end)*100,2) toll_pct, round(avg(case when tolls>0 then tolls end),2) mean_if,
 round(sum(tolls)/sum(fare)*100,2) tolls_pct_fare, round(avg(mi),2) avg_mi, round(median(mi),2) med_mi, count(*) n from y""")
q("select round(tolls,2) toll, count(*) n from y where tolls>0 group by 1 order by 2 desc limit 10")
print("== ratecode shares (3 Newark, 4 Nassau/Westchester, 2 JFK flat, 5 negotiated)")
q("select rc, count(*) n, round(count(*)*100.0/sum(count(*)) over (),3) pct, round(avg(mi),1) avg_mi, round(avg(tolls),2) avg_toll from y group by 1 order by 1")
print("== outside-NYC drop (265) and EWR (1)")
q("""select round(avg(case when dol=265 then 1 else 0 end)*100,3) do_out, round(avg(case when dol=1 then 1 else 0 end)*100,3) do_ewr,
 round(avg(case when pul in (1,265) then 1 else 0 end)*100,3) pu_out from y""")
print("== monthly avg distance and engaged mph")
q("select m, round(avg(mi),2) avg_mi, round(sum(mi)/sum(case when secs>0 then secs end)*3600,1) mph from y where secs between 60 and 10800 group by 1 order by 1")
