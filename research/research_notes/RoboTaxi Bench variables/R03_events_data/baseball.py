import sys, csv, duckdb, pandas as pd, numpy as np
gl, agg = sys.argv[1], sys.argv[2]
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
rows=[]
for r in csv.reader(open(gl)):
    rows.append(dict(date=r[0], dow=r[2], vis=r[3], home=r[6], outs=int(r[11]) if r[11] else None, dn=r[12], park=r[16], att=int(r[17]) if r[17] else 0, mins=int(r[18]) if r[18] else None))
g = pd.DataFrame(rows); g['dt']=pd.to_datetime(g.date)
ny = g[g.park.isin(['NYC21','NYC20'])].copy()
print("Home games by park:", ny.groupby('park').size().to_dict())
for p in ['NYC21','NYC20']:
    s = ny[ny.park==p]
    print(p, "attendance mean %.0f sd %.0f min %d max %d; duration mean %.1f sd %.1f p10 %.0f p90 %.0f min %d max %d; extra-inning share %.3f; night share %.2f" % (
      s.att.mean(), s.att.std(), s.att.min(), s.att.max(), s.mins.mean(), s.mins.std(), s.mins.quantile(.1), s.mins.quantile(.9), s.mins.min(), s.mins.max(), (s.outs>54).mean(), (s.dn=='N').mean()))
allg = g[g.mins.notna()]
print("All MLB 2023 game duration mean %.1f sd %.1f; 9-inning games (51-54 outs) mean %.1f sd %.1f" % (allg.mins.mean(), allg.mins.std(), allg[allg.outs<=54].mins.mean(), allg[allg.outs<=54].mins.std()))
con = duckdb.connect()
pu = con.execute(f"select * from '{agg}/pu_date_hour_zone.parquet'").fetchdf(); pu['dt']=pd.to_datetime(pu.dt)
do = con.execute(f"select * from '{agg}/do_date_hour_zone.parquet'").fetchdf(); do['dt']=pd.to_datetime(do.dt)
pu = pu[pu.dt.dt.year==2023]; do = do[do.dt.dt.year==2023]
def window(df, zcol, zones, h0, h1):
    s = df[(df[zcol].isin(zones)) & (df.h>=h0) & (df.h<h1)].groupby('dt').n.sum()
    return s.reindex(pd.date_range('2023-01-01','2023-12-31'), fill_value=0)
for park, zones_list in [('NYC21',[[247],[69],[119],[159],[42],[41]]), ('NYC20',[[93],[253],[56,57],[173],[92]])]:
    s = ny[ny.park==park]; season = (pd.Timestamp('2023-03-30'), pd.Timestamp('2023-10-01'))
    night = set(s[s.dn=='N'].dt); day = set(s[s.dn=='D'].dt); games=set(s.dt)
    days = pd.date_range(*season)
    nong = [d for d in days if d not in games]
    print(f"\n== {park}: {len(night)} night, {len(day)} day home games; {len(nong)} non-game days in season")
    for zones in zones_list:
        a = window(do,'dol',zones,16,20); b = window(pu,'pul',zones,21,24); c = window(pu,'pul',zones,0,24)
        print(f"zones {zones}: DO 16-20h night-game mean {a[list(night)].mean():.1f} vs non-game {a[nong].mean():.1f} | PU 21-24h night-game {b[list(night)].mean():.1f} vs non-game {b[nong].mean():.1f} | PU all-day game {c[list(games)].mean():.1f} vs non {c[nong].mean():.1f}")
