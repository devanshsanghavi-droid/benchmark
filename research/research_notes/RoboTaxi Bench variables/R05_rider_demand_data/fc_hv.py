import sys, duckdb, pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
d = sys.argv[1]
con = duckdb.connect(); con.execute("PRAGMA threads=4")
f = f"{d}/fhvhv_2023-01.parquet"
q = lambda s: print(con.execute(s).fetchdf().to_string())
con.execute(f"""create view t as select * from '{f}' where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01'""")
print("== licence counts, on_scene coverage, aar values")
q("select hvfhs_license_num lic, count(*) n, round(count(*)*100.0/sum(count(*)) over (),2) pct, round(avg(case when on_scene_datetime is not null then 1.0 else 0 end)*100,1) onscene_pct from t group by 1 order by 2 desc")
q("select hvfhs_license_num, access_a_ride_flag, count(*) from t group by 1,2 order by 1,2")
q("select hvfhs_license_num, wav_request_flag, wav_match_flag, count(*) from t group by 1,2,3 order by 1,2,3")
print("== durations, distances, waits")
q("""select count(*) n, round(avg(trip_miles),2) mean_mi, round(median(trip_miles),2) med_mi, round(avg(trip_time)/60,1) mean_min, round(median(trip_time)/60,1) med_min,
 round(avg(epoch(pickup_datetime-request_datetime))/60,2) mean_wait, round(median(epoch(pickup_datetime-request_datetime))/60,2) med_wait,
 round(avg(case when trip_miles<=5 then 1.0 else 0 end)*100,1) le5mi
 from t where trip_miles>0 and trip_time>0 and pickup_datetime>=request_datetime and epoch(pickup_datetime-request_datetime)<3600""")
q("""select hvfhs_license_num, round(avg(epoch(on_scene_datetime-request_datetime))/60,2) mean_req_onscene, round(median(epoch(pickup_datetime-on_scene_datetime))/60,2) med_onscene_to_pu,
 round(avg(epoch(pickup_datetime-on_scene_datetime))/60,2) mean_onscene_to_pu, round(quantile_cont(epoch(pickup_datetime-on_scene_datetime)/60,0.9),2) p90_onscene_to_pu,
 round(avg(case when epoch(pickup_datetime-on_scene_datetime)>120 then 1.0 else 0 end)*100,1) pct_gt2min,
 round(avg(case when epoch(pickup_datetime-on_scene_datetime)>300 then 1.0 else 0 end)*100,1) pct_gt5min
 from t where on_scene_datetime is not null and pickup_datetime>=on_scene_datetime and epoch(pickup_datetime-on_scene_datetime)<3600 group by 1""")
print("== tips")
q("""select hvfhs_license_num, round(avg(case when tips>0 then 1.0 else 0 end)*100,1) tip_incid, round(avg(case when tips>0 then tips end),2) mean_tip_if,
 round(sum(tips)/sum(base_passenger_fare)*100,2) tips_pct_fare, round(sum(tips)/sum(driver_pay)*100,2) tips_pct_driverpay,
 round(avg(case when tips>0 then tips/nullif(base_passenger_fare,0) end)*100,1) tip_rate_if from t where base_passenger_fare>0 group by 1""")
print("== airport pickups and destination of airport pickups")
q("""select round(avg(case when PULocationID in (1,132,138) then 1.0 else 0 end)*100,2) pu_apt, round(avg(case when DOLocationID in (1,132,138) then 1.0 else 0 end)*100,2) do_apt,
 round(avg(case when DOLocationID in (1,265) then 1.0 else 0 end)*100,2) do_ewr_or_outside from t""")
print("== peak zone-hour pickups")
q("""select PULocationID, date_trunc('hour', pickup_datetime) h, count(*) n from t group by 1,2 order by 3 desc limit 8""")
q("""with zh as (select PULocationID z, date_trunc('hour', pickup_datetime) h, count(*) n from t group by 1,2) select quantile_cont(n,[0.5,0.9,0.99,0.999]) q, max(n) mx from zh""")
