import sys, csv, duckdb, pandas as pd
agg, gl = sys.argv[1], sys.argv[2]
con = duckdb.connect()
pu = con.execute(f"select * from '{agg}/pu_date_hour_zone.parquet'").fetchdf(); pu['dt'] = pd.to_datetime(pu.dt)
do = con.execute(f"select * from '{agg}/do_date_hour_zone.parquet'").fetchdf(); do['dt'] = pd.to_datetime(do.dt)
D = pd.Timestamp
fl = D('2023-09-29'); base = [D('2023-09-08'), D('2023-09-15'), D('2023-10-06'), D('2023-10-13')]
s = pu[pu.dt.isin([fl] + base)].groupby(['dt', 'h']).agg(n=('n', 'sum'), f=('fare', 'sum'), mi=('mi_ok', 'sum'), d=('dur_ok', 'sum')).reset_index()
t = s.pivot(index='h', columns='dt', values='n'); t['base'] = t[base].mean(axis=1); t['ratio'] = t[fl] / t['base']
print("trips/h (4 Fridays, Sep 22 excluded):"); print(t[[fl, 'base', 'ratio']].round(2).T.to_string())
s['mph'] = 60 * s.mi / s.d; t2 = s.pivot(index='h', columns='dt', values='mph'); t2['base'] = t2[base].mean(axis=1); print("mph:"); print(t2[[fl, 'base']].round(1).T.to_string())
s['fpt'] = s.f / s.n; t3 = s.pivot(index='h', columns='dt', values='fpt'); t3['base'] = t3[base].mean(axis=1); t3['r'] = t3[fl] / t3['base']; print("fare/trip:"); print(t3[[fl, 'base', 'r']].round(2).T.to_string())
day = pu[pu.dt.isin([fl] + base)].groupby('dt').n.sum(); print("daily:", day.to_dict(), "ratio %.3f" % (day[fl] / day[base].mean()))
# baseball with gap days excluded
gap = {D('2023-09-21'), D('2023-09-22'), D('2023-09-23'), D('2023-09-24')}
rows = [dict(date=r[0], dow=r[2], dn=r[12], park=r[16], att=int(r[17]) if r[17] else 0) for r in csv.reader(open(gl))]
g = pd.DataFrame(rows); g['dt'] = pd.to_datetime(g.date)
for p, z in [('NYC21', 247), ('NYC20', 93)]:
    allg = g[g.park == p]; games = set(allg.dt)
    print(p, "home dates in gap:", sorted(str(x.date()) for x in games & gap))
    s2 = g[(g.park == p) & (g.dn == 'N') & (g.att > 0) & ~g.dt.between('2023-08-28', '2023-09-10') & ~g.dt.isin(gap)].copy()
    a = do[(do.dol == z) & (do.h >= 16) & (do.h < 20)].groupby('dt').n.sum()
    s2['do'] = s2.dt.map(a).fillna(0)
    days = pd.date_range('2023-03-30', '2023-10-01'); nong = [d for d in days if d not in games and d not in gap]
    an = a.reindex(nong, fill_value=0)
    print(p, "n night games %d; DO per 10k %.2f; corr %.2f; night-game DO mean %.1f vs non-game %.1f (n=%d)" % (len(s2), 1e4 * s2['do'].sum() / s2.att.sum(), s2.att.corr(s2['do']), s2['do'].mean(), an.mean(), len(nong)))
