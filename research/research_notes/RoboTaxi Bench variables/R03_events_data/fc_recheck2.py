import sys, csv, duckdb, pandas as pd
agg, gl = sys.argv[1], sys.argv[2]
con = duckdb.connect(); D = pd.Timestamp
pu = con.execute(f"select * from '{agg}/pu_date_hour_zone.parquet'").fetchdf(); pu['dt'] = pd.to_datetime(pu.dt)
do = con.execute(f"select * from '{agg}/do_date_hour_zone.parquet'").fetchdf(); do['dt'] = pd.to_datetime(do.dt)
print(pu.columns.tolist())
fl = D('2023-09-29'); base = [D('2023-09-08'), D('2023-09-15'), D('2023-10-06'), D('2023-10-13')]
for lab, days in [('flood', [fl]), ('base4', base)]:
    x = pu[pu.dt.isin(days) & (pu.h >= 7) & (pu.h < 20)]
    print(lab, "7-20h fare per engaged hour %.1f" % (x.fare.sum() / (x.dur_ok.sum() / 60)), "trips/day %.0f" % (x.n.sum() / len(days)))
gap = {D('2023-09-21'), D('2023-09-22'), D('2023-09-23'), D('2023-09-24')}
rows = [dict(date=r[0], dn=r[12], park=r[16], att=int(r[17]) if r[17] else 0) for r in csv.reader(open(gl))]
g = pd.DataFrame(rows); g['dt'] = pd.to_datetime(g.date)
uso = set(pd.date_range('2023-08-28', '2023-09-10'))
for p, z in [('NYC21', 247), ('NYC20', 93)]:
    games = set(g[g.park == p].dt)
    s2 = g[(g.park == p) & (g.dn == 'N') & (g.att > 0) & ~g.dt.isin(uso) & ~g.dt.isin(gap)].copy()
    a = do[(do.dol == z) & (do.h >= 16) & (do.h < 20)].groupby('dt').n.sum()
    s2['do'] = s2.dt.map(a).fillna(0)
    nong = [d for d in pd.date_range('2023-03-30', '2023-10-01') if d not in games and d not in gap and d not in uso]
    base_m = a.reindex(nong, fill_value=0).mean()
    print(p, "night games %d, mean att %.0f, DO %.1f vs non-game (excl US Open, gap) %.1f, ratio %.2f, total per 10k %.2f, extra per 10k %.2f" % (len(s2), s2.att.mean(), s2['do'].mean(), base_m, s2['do'].mean()/base_m, 1e4*s2['do'].mean()/s2.att.mean(), 1e4*(s2['do'].mean()-base_m)/s2.att.mean()))
