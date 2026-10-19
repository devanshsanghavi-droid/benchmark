import sys, csv, duckdb, pandas as pd, numpy as np
gl, agg = sys.argv[1], sys.argv[2]
rows=[dict(date=r[0], dow=r[2], outs=int(r[11]) if r[11] else None, dn=r[12], park=r[16], att=int(r[17]) if r[17] else 0, mins=int(r[18]) if r[18] else None) for r in csv.reader(open(gl))]
g=pd.DataFrame(rows); g['dt']=pd.to_datetime(g.date)
for p in ['NYC21','NYC20']:
    s=g[(g.park==p)&(g.att>0)]; print(p, "n with attendance", len(s), "mean %.0f sd %.0f min %d max %d" % (s.att.mean(), s.att.std(), s.att.min(), s.att.max()))
print("share MLB games >180 min: %.3f; >200 min: %.3f" % ((g.mins>180).mean(), (g.mins>200).mean()))
con=duckdb.connect()
do=con.execute(f"select * from '{agg}/do_date_hour_zone.parquet'").fetchdf(); do['dt']=pd.to_datetime(do.dt)
pu=con.execute(f"select * from '{agg}/pu_date_hour_zone.parquet'").fetchdf(); pu['dt']=pd.to_datetime(pu.dt)
for p,z in [('NYC21',247),('NYC20',93)]:
    s=g[(g.park==p)&(g.dn=='N')&(g.att>0)&~g.dt.between('2023-08-28','2023-09-10')].copy()
    a=do[(do.dol==z)&(do.h>=16)&(do.h<20)].groupby('dt').n.sum(); b=pu[(pu.pul==z)&(pu.h>=21)].groupby('dt').n.sum()
    s['do']=s.dt.map(a).fillna(0); s['pu']=s.dt.map(b).fillna(0)
    print(p, "night games", len(s), "corr(att, DO)=%.2f corr(att,PU)=%.2f; DO per 10k attendees %.2f; weekend vs weekday DO %.1f vs %.1f" % (s.att.corr(s['do']), s.att.corr(s['pu']), 1e4*s['do'].sum()/s.att.sum(), s[s.dow.isin(['Fri','Sat'])]['do'].mean(), s[~s.dow.isin(['Fri','Sat'])]['do'].mean()))
