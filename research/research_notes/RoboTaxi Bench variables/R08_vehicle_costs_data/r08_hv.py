import sys, duckdb
d = sys.argv[1]
con = duckdb.connect()
con.execute("PRAGMA threads=4")
f = f"{d}/fhvhv_2023-01.parquet"
con.execute(f"""create table t as select hvfhs_license_num lic, PULocationID pul, DOLocationID dol, trip_miles mi, trip_time tt,
 base_passenger_fare fare, tolls, bcf, sales_tax, congestion_surcharge cs, airport_fee af, tips, driver_pay pay,
 shared_request_flag srf, shared_match_flag smf, wav_request_flag wrf, wav_match_flag wmf, access_a_ride_flag aar,
 pickup_datetime pu
 from '{f}' where pickup_datetime >= '2023-01-01' and pickup_datetime < '2023-02-01' and trip_miles>0 and trip_time>0""")
q = lambda s: print(con.execute(s).fetchdf().to_string())
print("== by licence")
q("""select lic, count(*) n, round(avg(mi),2) avg_mi, round(median(mi),2) med_mi, round(avg(tt)/60,1) avg_min,
 round(avg(pay),2) avg_pay, round(sum(pay)/sum(mi),2) pay_per_mi, round(sum(pay)/sum(tt)*3600,1) pay_per_eng_hr,
 round(avg(case when tolls>0 then 1 else 0 end)*100,2) toll_pct, round(avg(case when tolls>0 then tolls end),2) toll_mean_if,
 round(sum(tolls)/sum(fare)*100,2) tolls_pct_of_fare,
 round(avg(case when wrf='Y' then 1 else 0 end)*100,3) wav_req_pct, round(avg(case when wmf='Y' then 1 else 0 end)*100,3) wav_match_pct,
 round(avg(case when srf='Y' then 1 else 0 end)*100,3) shared_req_pct, round(avg(case when smf='Y' then 1 else 0 end)*100,3) shared_match_pct,
 round(avg(case when aar='Y' then 1 else 0 end)*100,3) aar_pct
 from t group by 1 order by 2 desc""")
print("== most common toll values")
q("select round(tolls,2) toll, count(*) n from t where tolls>0 group by 1 order by 2 desc limit 15")
print("== drop-offs outside NYC (265) and EWR (1), pickups there")
q("""select sum(case when dol=265 then 1 else 0 end)*100.0/count(*) do_outside_pct, sum(case when dol=1 then 1 else 0 end)*100.0/count(*) do_ewr_pct,
 sum(case when pul=265 then 1 else 0 end)*100.0/count(*) pu_outside_pct, sum(case when pul=1 then 1 else 0 end)*100.0/count(*) pu_ewr_pct,
 avg(case when dol in (1,265) then mi end) avg_mi_out, avg(case when dol in (1,265) then pay end) avg_pay_out from t""")
print("== airport drop/pickup JFK 132, LGA 138")
q("""select sum(case when dol in (132,138) then 1 else 0 end)*100.0/count(*) do_apt_pct, sum(case when pul in (132,138) then 1 else 0 end)*100.0/count(*) pu_apt_pct,
 avg(case when pul in (132,138) or dol in (132,138) then mi end) apt_mi, avg(case when (pul in (132,138) or dol in (132,138)) and tolls>0 then 1.0 else 0 end) from t""")
print("== trip miles distribution")
q("select quantile_cont(mi, [0.1,0.25,0.5,0.75,0.9,0.99]) q from t")
print("== illustrative per-trip energy cost: gas 30 mpg @3.40/gal, hybrid 45 mpg, EV 0.30 kWh/mi @0.35/kWh; deadhead factor 1.5 miles per paid mile")
q("""select round(avg(mi)*1.5*3.40/30,2) gas_cost_trip, round(avg(mi)*1.5*3.40/45,2) hyb_cost_trip, round(avg(mi)*1.5*0.30*0.35,2) ev_cost_trip, round(avg(pay),2) pay_trip,
 round(avg(mi)*1.5*3.40/30/avg(pay)*100,1) gas_pct_pay, round(avg(mi)*1.5*0.30*0.35/avg(pay)*100,1) ev_pct_pay from t""")
