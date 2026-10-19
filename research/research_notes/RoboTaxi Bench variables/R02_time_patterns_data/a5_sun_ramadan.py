import sys, duckdb, pandas as pd, datetime as dt
from astral import LocationInfo
from astral.sun import sun
d = sys.argv[1]
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 400)
nyc = LocationInfo("NYC","USA","America/New_York",40.7128,-74.0060)
import zoneinfo; tz = zoneinfo.ZoneInfo("America/New_York")
for day in ['2023-01-01','2023-03-11','2023-03-12','2023-06-21','2023-11-04','2023-11-05','2023-12-08','2023-12-21','2023-03-23','2023-04-20']:
    s = sun(nyc.observer, date=dt.date.fromisoformat(day), tzinfo=tz)
    print(day, 'dawn', s['dawn'].strftime('%H:%M'), 'sunrise', s['sunrise'].strftime('%H:%M'), 'sunset', s['sunset'].strftime('%H:%M'), 'dusk', s['dusk'].strftime('%H:%M'), 'daylight_h', round((s['sunset']-s['sunrise']).seconds/3600,2))
con = duckdb.connect(); con.execute("PRAGMA threads=4")
con.execute(f"""create table y as select tpep_pickup_datetime pu from read_parquet(['{d}/yellow_2023-02.parquet','{d}/yellow_2023-03.parquet','{d}/yellow_2023-04.parquet','{d}/yellow_2023-05.parquet','{d}/yellow_2023-10.parquet','{d}/yellow_2023-11.parquet'], union_by_name=true)
 where dayofweek(tpep_pickup_datetime) between 1 and 4""")
def win(a,b):
    return con.execute(f"""select (hour(pu)*60+minute(pu))//15 bin, count(*)*1.0/count(distinct cast(pu as date)) n from y where pu >= '{a}' and pu < '{b}' group by 1 order by 1""").fetchdf().set_index('bin').n
# DST darkness test: share of 17:00-19:00 relative to 12:00-14:00 (Mon-Thu)
for lab,a,b in [('pre spring DST Feb27-Mar10','2023-02-27','2023-03-11'),('post spring DST Mar13-Mar22','2023-03-13','2023-03-23'),('pre fall DST Oct23-Nov3','2023-10-23','2023-11-04'),('post fall DST Nov6-Nov17','2023-11-06','2023-11-18')]:
    s = win(a,b); r = s.loc[68:75].sum()/s.loc[48:55].sum(); r2 = s.loc[76:83].sum()/s.loc[48:55].sum()
    print(lab, 'trips 17-19h / 12-14h =', round(r,3), ' 19-21h / 12-14h =', round(r2,3))
# Ramadan 2023 (Mar 23 - Apr 20): Mon-Thu, 15-min profile 17:00-21:00 normalised to 16:00-17:00
res = {}
for lab,a,b in [('pre Mar1-22','2023-03-01','2023-03-23'),('Ramadan Mar23-Apr20','2023-03-23','2023-04-21'),('post Apr24-May18','2023-04-24','2023-05-19')]:
    s = win(a,b); res[lab] = (s/s.loc[64:67].mean()).loc[68:84]
r = pd.DataFrame(res); r.index = [f"{b*15//60:02d}:{b*15%60:02d}" for b in r.index]; print(r.round(3).to_string())
