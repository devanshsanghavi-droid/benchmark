import sys, duckdb, pandas as pd, numpy as np
agg = sys.argv[1]; con = duckdb.connect()
pu = con.execute(f"select * from '{agg}/pu_date_hour_zone.parquet'").fetchdf(); pu['dt']=pd.to_datetime(pu.dt)
do = con.execute(f"select * from '{agg}/do_date_hour_zone.parquet'").fetchdf(); do['dt']=pd.to_datetime(do.dt)
GAP = set(pd.date_range('2023-09-21','2023-09-24'))
def daily(df, zcol, zones, h0=0, h1=24):
    m=(df.h>=h0)&(df.h<h1)
    if zones is not None: m&=df[zcol].isin(zones)
    return df[m].groupby('dt').n.sum()
def cmp(label, s, ev, base):
    base=[b for b in base if b not in GAP]; e=s.reindex(ev,fill_value=0); b=s.reindex(base,fill_value=0)
    print(f"{label}: event mean {e.mean():.1f} {list(e.values)} | base mean {b.mean():.1f} median {b.median():.1f} (n={len(b)}) | ratio {e.mean()/max(b.mean(),1e-9):.2f}")
def speed(zones,h0,h1,days):
    m=(pu.h>=h0)&(pu.h<h1)&pu.dt.isin(days)
    if zones is not None: m&=pu.pul.isin(zones)
    x=pu[m]; return 60*x.mi_ok.sum()/x.dur_ok.sum()
print("== US Open 2023 zone 93, excl data gap ==")
uso=list(pd.date_range('2023-08-28','2023-09-10')); base=[x for x in pd.date_range('2023-07-31','2023-09-24') if x not in uso]
cmp("DO 93 all day",daily(do,'dol',[93]),uso,base); cmp("PU 93 all day",daily(pu,'pul',[93]),uso,base); cmp("PU 93 21-24h",daily(pu,'pul',[93],21,24),uso,base)
x = pu[(pu.pul==93)&pu.dt.isin(uso)]; xb = pu[(pu.pul==93)&pu.dt.isin([b for b in base if b not in GAP])]
print("US Open PU 93 mean fare %.2f mi %.2f vs base fare %.2f mi %.2f" % (x.fare.sum()/x.n.sum(), x.mi.sum()/x.n.sum(), xb.fare.sum()/xb.n.sum(), xb.mi.sum()/xb.n.sum()))
print("\n== UNGA Mon-Wed Sep 18-20 vs Mon-Wed Sep 11-13 and Oct 2-4 ==")
ung=list(pd.date_range('2023-09-18','2023-09-20')); base=list(pd.date_range('2023-09-11','2023-09-13'))+list(pd.date_range('2023-10-02','2023-10-04'))
mte=[162,229,233,170,137,161]
cmp("PU Midtown East group 7-20h",daily(pu,'pul',mte,7,20),ung,base); cmp("DO Midtown East group 7-20h",daily(do,'dol',mte,7,20),ung,base)
cmp("PU 233 UN/Turtle Bay S 7-20h",daily(pu,'pul',[233],7,20),ung,base); cmp("PU 229 7-20h",daily(pu,'pul',[229],7,20),ung,base)
cmp("Citywide 7-20h",daily(pu,'pul',None,7,20),ung,base)
for h0,h1 in [(8,11),(11,16),(16,20)]:
    print(f"speed {h0}-{h1}: MidE UNGA {speed(mte,h0,h1,ung):.2f} vs {speed(mte,h0,h1,base):.2f} ; all {speed(None,h0,h1,ung):.2f} vs {speed(None,h0,h1,base):.2f}")
x=pu[pu.dt.isin(ung)&(pu.h.between(8,19))]; xb=pu[pu.dt.isin(base)&(pu.h.between(8,19))]
print("citywide fare per engaged hour 8-20h: UNGA %.1f vs %.1f; fare/trip %.2f vs %.2f; dur/trip %.1f vs %.1f" % (x.fare.sum()/(x.dur_ok.sum()/60), xb.fare.sum()/(xb.dur_ok.sum()/60), x.fare.sum()/x.n.sum(), xb.fare.sum()/xb.n.sum(), x.dur_ok.sum()/x.n.sum(), xb.dur_ok.sum()/xb.n.sum()))
print("\n== Broadway: Times Sq 230 yellow pickups per 15 min, 2023 (excl holidays) by weekday ==")
f = con.execute(f"select dt, h, q, sum(n) n from '{agg}/focus_15min_od.parquet' where pul=230 group by all").fetchdf(); f['dt']=pd.to_datetime(f.dt)
f=f[(f.dt.dt.year==2023)&~f.dt.isin(GAP)]
ndays = pd.Series(pd.date_range('2023-01-01','2023-12-31')); ndays=ndays[~ndays.isin(GAP)]; cnt=ndays.dt.dayofweek.value_counts()
f['dow']=f.dt.dt.dayofweek; f['t']=f.h*100+f.q*15
p=f.groupby(['t','dow']).n.sum().unstack()/cnt
print(p.loc[[1600,1630,1645,1700,1715,1730,2130,2145,2200,2215,2230,2245,2300,2315]].round(0).to_string())
x=p.loc[2200:2245].sum(); print("22:00-23:00 pickups/day by dow (0=Mon):", x.round(0).to_dict())
x=p.loc[1645:1730].sum(); print("16:45-17:45 pickups/day by dow:", x.round(0).to_dict())
print("\n== Penn/MSG zone 186: distribution of yellow pickups 22:00-24:00 per night (2023) ==")
s=daily(pu,'pul',[186],22,24); s=s[(s.index.year==2023)&~s.index.isin(GAP)]
print(s.describe().round(1).to_dict()); print("p10,p50,p90:", s.quantile([.1,.5,.9]).round(0).to_dict())
f = con.execute(f"select dt, h, q, sum(n) n from '{agg}/focus_15min_od.parquet' where pul=186 and h>=21 group by all").fetchdf(); f['dt']=pd.to_datetime(f.dt)
f=f[(f.dt.dt.year==2023)&~f.dt.isin(GAP)]; f['t']=f.h*100+f.q*15
w=f.pivot_table(index='dt',columns='t',values='n',aggfunc='sum').fillna(0)
w['late']=w[[2200,2215,2230,2245,2300]].sum(axis=1); top=w.late.quantile(.8); bot=w.late.quantile(.4)
print("15-min profile top-20% nights vs bottom-40% nights:"); print(pd.DataFrame({'top':w[w.late>=top].mean(),'bottom':w[w.late<=bot].mean()}).T.round(1).to_string())
