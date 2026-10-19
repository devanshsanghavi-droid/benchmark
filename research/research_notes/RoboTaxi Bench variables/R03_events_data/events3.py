import sys, duckdb, pandas as pd, numpy as np
agg=sys.argv[1]; con=duckdb.connect()
pu=con.execute(f"select * from '{agg}/pu_date_hour_zone.parquet'").fetchdf(); pu['dt']=pd.to_datetime(pu.dt)
do=con.execute(f"select * from '{agg}/do_date_hour_zone.parquet'").fetchdf(); do['dt']=pd.to_datetime(do.dt)
def daily(df,zcol,zones,h0=0,h1=24):
    m=(df.h>=h0)&(df.h<h1)
    if zones is not None: m&=df[zcol].isin(zones)
    return df[m].groupby('dt').n.sum()
def cmp(label,s,ev,base):
    e=s.reindex(ev,fill_value=0); b=s.reindex(base,fill_value=0)
    print(f"{label}: event {list(e.values)} | base mean {b.mean():.1f} (n={len(b)}) | ratio {e.mean()/max(b.mean(),1e-9):.2f}")
def speed(zones,h0,h1,days):
    m=(pu.h>=h0)&(pu.h<h1)&pu.dt.isin(days)
    if zones is not None: m&=pu.pul.isin(zones)
    x=pu[m]; return 60*x.mi_ok.sum()/x.dur_ok.sum()
D=pd.Timestamp
print("== Rockefeller tree lighting Wed Nov 29 2023 ==")
ev=[D('2023-11-29')]; base=[D('2023-11-08'),D('2023-11-15'),D('2023-12-06'),D('2023-12-13')]
cmp("PU Midtown Center 161 17-22h",daily(pu,'pul',[161],17,22),ev,base); cmp("DO 161 16-20h",daily(do,'dol',[161],16,20),ev,base)
print("speed from 161/162/163 17-22h: %.2f vs %.2f" % (speed([161,162,163],17,22,ev), speed([161,162,163],17,22,base)))
print("== SantaCon Sat Dec 9 2023 (bar crawl) ==")
ev=[D('2023-12-09')]; base=[D('2023-11-18'),D('2023-12-02'),D('2023-12-16')]
for z,lab in [([79,148,4,107,234],'E Village/LES/Gramercy/Union Sq'),([161,162,163,164,230,100,186],'Midtown')]:
    cmp(f"PU {lab} 12-20h",daily(pu,'pul',z,12,20),ev,base); cmp(f"PU {lab} 20-24h",daily(pu,'pul',z,20,24),ev,base)
print("== Thanksgiving parade Thu Nov 23 2023: route-zone pickups 6-13h, share of the day's trips vs Christmas Day Mon Dec 25 ==")
route=[142,143,239,238,43,163,230,161,164,186,100,68,246]
for d in ['2023-11-23','2023-12-25','2023-07-04']:
    a=daily(pu,'pul',route,6,13).get(D(d),0); t=daily(pu,'pul',None).get(D(d),0); print(d, a, t, round(a/t,3), "speed route 8-12h %.2f" % speed(route,8,12,[D(d)]))
print("== July 4 2023 fireworks (East River) 21-24h pickups, east-side zones vs other evening hours share ==")
east=[137,170,224,107,233,229,162,4,79,148,232]
for d in ['2023-07-04','2023-07-11','2023-06-27']:
    print(d, "east 21-24h", daily(pu,'pul',east,21,24).get(D(d),0), "east 18-21h", daily(pu,'pul',east,18,21).get(D(d),0))
