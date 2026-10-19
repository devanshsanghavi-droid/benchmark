import sys, duckdb
d = sys.argv[1]
con = duckdb.connect()
q = lambda s: print(con.execute(s).fetchdf().to_string())
con.execute(f"create table z as select * from read_csv_auto('{d}/taxi_zone_lookup.csv')")
hv = f"'{d}/fhvhv_2023-01.parquet'"
print("== HVFHV Jan 2023: tolls on trips by destination class (pickup inside NYC)")
q(f"""select hvfhs_license_num lic,
 case when DOLocationID=265 then 'DO outside NYC (265)' when DOLocationID=1 then 'DO EWR (1)' else 'DO in NYC' end cls,
 count(*) n, round(avg(case when tolls>0 then 1.0 else 0 end)*100,1) pct_tolled, round(avg(tolls),2) mean_toll_all,
 round(median(case when tolls>0 then tolls end),2) med_toll_if, round(avg(trip_miles),1) mi
 from {hv} where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' and trip_miles>0 and PULocationID not in (1,264,265)
 group by 1,2 order by 1,2""")
print("== HVFHV Jan 2023: most common toll values on trips to EWR / outside NYC")
q(f"""select round(tolls,2) toll, count(*) n from {hv} where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' and DOLocationID in (1,265) group by 1 order by 2 desc limit 12""")
print("== HVFHV Jan 2023: trips with toll exactly 20.00 or 21.00 by drop-off class and licence")
q(f"""select hvfhs_license_num lic, round(tolls,2) toll, case when DOLocationID in (1,265) then 'out/EWR' when PULocationID in (1,265) then 'from out/EWR' else 'in NYC' end cls, count(*) n
 from {hv} where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' and round(tolls,2) in (20.00,21.00) group by 1,2,3 order by 4 desc limit 10""")
print("== HVFHV Jan 2023: Brooklyn->Staten Island vs Staten Island->Brooklyn tolls (Verrazzano one-way toll)")
q(f"""select zp.Borough pb, zd.Borough db, count(*) n, round(avg(case when tolls>0 then 1.0 else 0 end)*100,1) pct_tolled,
 round(median(case when tolls>0 then tolls end),2) med_toll_if
 from {hv} t join z zp on t.PULocationID=zp.LocationID join z zd on t.DOLocationID=zd.LocationID
 where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' and ((zp.Borough='Brooklyn' and zd.Borough='Staten Island') or (zp.Borough='Staten Island' and zd.Borough='Brooklyn')) group by 1,2""")
y = f"read_parquet('{d}/yellow_2023-*.parquet')"
print("== Yellow 2023: tolls on trips to EWR / outside NYC (ratecode 3 = Newark)")
q(f"""select case when DOLocationID=265 then 'DO outside NYC (265)' when DOLocationID=1 then 'DO EWR (1)' else 'DO in NYC' end cls, count(*) n,
 round(avg(case when tolls_amount>0 then 1.0 else 0 end)*100,1) pct_tolled, round(median(case when tolls_amount>0 then tolls_amount end),2) med_toll_if
 from {y} where tpep_pickup_datetime>='2023-01-01' and tpep_pickup_datetime<'2024-01-01' and fare_amount>0 and PULocationID not in (1,264,265) group by 1 order by 1""")
q(f"""select round(tolls_amount,2) toll, count(*) n from {y} where tpep_pickup_datetime>='2023-01-01' and tpep_pickup_datetime<'2024-01-01' and DOLocationID=1 and fare_amount>0 group by 1 order by 2 desc limit 8""")
print("== Yellow 2023: denominator for passenger_count shares")
q(f"""select count(*) n_all, count(passenger_count) n_pc_notnull from {y} where tpep_pickup_datetime>='2023-01-01' and tpep_pickup_datetime<'2024-01-01' and trip_distance>0 and fare_amount>0""")
