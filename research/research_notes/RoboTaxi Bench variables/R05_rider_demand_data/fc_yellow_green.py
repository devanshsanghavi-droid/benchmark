import sys, duckdb, pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
d = sys.argv[1]; dl = sys.argv[2]
con = duckdb.connect(); con.execute("PRAGMA threads=4")
q = lambda s: print(con.execute(s).fetchdf().to_string())
con.execute(f"""create view y as select * from read_parquet('{d}/yellow_2023-*.parquet') where tpep_pickup_datetime>='2023-01-01' and tpep_pickup_datetime<'2024-01-01'""")
print("== yellow 2023 payment types")
q("select payment_type, count(*) n, round(count(*)*100.0/sum(count(*)) over (),2) pct from y group by 1 order by 1")
print("== yellow 2023 tips")
q("""select round(avg(case when tip_amount>0 then 1.0 else 0 end)*100,1) any_tip_pct,
 round(avg(case when payment_type=1 and tip_amount>0 then 1.0 when payment_type=1 then 0 end)*100,1) card_tip_incid,
 round(sum(case when payment_type=1 then tip_amount end)/sum(case when payment_type=1 then fare_amount end)*100,1) card_tip_pct_fare,
 round(median(case when payment_type=1 and tip_amount>0 and fare_amount>0 then tip_amount/fare_amount end)*100,1) med_tip_rate_card_tipped,
 round(sum(case when payment_type=1 then fare_amount end)/sum(fare_amount)*100,1) card_share_of_fare
 from y where fare_amount>0""")
print("== yellow 2023 distance/duration")
q("""select count(*) n, round(avg(trip_distance),2) mean_mi, round(median(trip_distance),2) med_mi,
 round(median(epoch(tpep_dropoff_datetime-tpep_pickup_datetime))/60,1) med_min, round(avg(epoch(tpep_dropoff_datetime-tpep_pickup_datetime))/60,1) mean_min,
 round(avg(case when trip_distance<=5 then 1.0 else 0 end)*100,1) le5mi, count(*)/365.0 per_day
 from y where trip_distance>0 and trip_distance<100 and fare_amount>0 and epoch(tpep_dropoff_datetime-tpep_pickup_datetime) between 30 and 10800""")
print("== yellow 2023 airport pickups share, JFK flat fare (ratecode 2) fare values")
q("select round(avg(case when PULocationID in (1,132,138) then 1.0 else 0 end)*100,2) pu_apt, round(avg(case when DOLocationID in (1,132,138) then 1.0 else 0 end)*100,2) do_apt from y")
q("select fare_amount, count(*) n from y where RatecodeID=2 group by 1 order by 2 desc limit 4")
print("== yellow 2019-10 (csv)")
con.execute(f"create view y19 as select * from read_csv_auto('{dl}/yellow_2019-10.csv.gz', sample_size=-1)")
q("""select count(*) n, round(avg(trip_distance),2) mean_mi, round(median(trip_distance),2) med_mi,
 round(avg(case when trip_distance<=5 then 1.0 else 0 end)*100,1) le5mi,
 round(avg(case when trip_distance<=5 and fare_amount<=18 then 1.0 else 0 end)*100,1) le5mi_and_le18,
 round(avg(case when fare_amount<=18 then 1.0 else 0 end)*100,1) le18,
 round(avg(case when payment_type=1 then 1.0 else 0 end)*100,1) card, round(avg(case when payment_type=2 then 1.0 else 0 end)*100,1) cash,
 round(avg(case when tip_amount=0 then 1.0 else 0 end)*100,1) zero_tip
 from y19 where trip_distance>0 and fare_amount>0""")
print("== green 2019-10 trip_type")
con.execute(f"create view g as select * from read_csv_auto('{dl}/green_2019-10.csv.gz', sample_size=-1)")
q("select trip_type, count(*) n, round(count(*)*100.0/sum(count(*)) over (),2) pct from g group by 1 order by 1")
