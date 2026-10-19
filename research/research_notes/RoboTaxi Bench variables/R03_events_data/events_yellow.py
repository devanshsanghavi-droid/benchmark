import sys, duckdb, pandas as pd, numpy as np
agg = sys.argv[1]
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 200)
con = duckdb.connect()
pu = con.execute(f"select * from '{agg}/pu_date_hour_zone.parquet'").fetchdf(); pu['dt']=pd.to_datetime(pu.dt)
do = con.execute(f"select * from '{agg}/do_date_hour_zone.parquet'").fetchdf(); do['dt']=pd.to_datetime(do.dt)
D = lambda s: pd.Timestamp(s)
def daily(df, zcol, zones, h0=0, h1=24, col='n'):
    m = (df.h>=h0)&(df.h<h1)
    if zones is not None: m &= df[zcol].isin(zones)
    return df[m].groupby('dt')[col].sum()
def cmp(label, s, ev_days, base_days):
    ev = s.reindex(ev_days, fill_value=0); b = s.reindex(base_days, fill_value=0)
    print(f"{label}: event {[round(x,1) for x in ev.values]} | baseline mean {b.mean():.1f} (n={len(b)}) | ratio {ev.mean()/max(b.mean(),1e-9):.2f}")
def speed(df, zones, h0, h1, days):
    m = (df.h>=h0)&(df.h<h1)&df.dt.isin(days)
    if zones is not None: m &= df.pul.isin(zones)
    x = df[m]; return 60*x.mi_ok.sum()/x.dur_ok.sum()
def same_dow(d, start, end, excl=()):
    d=D(d); return [x for x in pd.date_range(start,end) if x.dayofweek==d.dayofweek and x!=d and x not in [D(e) for e in excl]]

print("=== US Open 2023 (Aug 28-Sep 10) zone 93 [Flushing Meadows] ===")
uso = list(pd.date_range('2023-08-28','2023-09-10'))
base = [x for x in pd.date_range('2023-07-31','2023-09-24') if x not in uso]
cmp("DO zone 93 all day", daily(do,'dol',[93]), uso, base)
cmp("PU zone 93 all day", daily(pu,'pul',[93]), uso, base)
cmp("PU zone 93 21-24h", daily(pu,'pul',[93],21,24), uso, base)
cmp("PU zone 93 0-2h", daily(pu,'pul',[93],0,2), [x+pd.Timedelta(days=1) for x in uso], [x+pd.Timedelta(days=1) for x in base])

print("\n=== Governors Ball 2023 (Jun 9-11, Flushing Meadows) zone 93 ===")
gb = list(pd.date_range('2023-06-09','2023-06-11'))
base = [x for x in pd.date_range('2023-05-12','2023-07-02') if x.dayofweek>=4 and x not in gb]
cmp("DO zone 93 12-20h", daily(do,'dol',[93],12,20), gb, base)
cmp("PU zone 93 21-24h", daily(pu,'pul',[93],21,24), gb, base)

print("\n=== Electric Zoo 2023 (Fri Sep 1 cancelled; Sat Sep 2, Sun Sep 3) zone 194 Randalls Island ===")
s1 = daily(do,'dol',[194],12,22); s2 = daily(pu,'pul',[194],18,24)
for d in ['2023-08-25','2023-08-26','2023-08-27','2023-09-01','2023-09-02','2023-09-03','2023-09-08','2023-09-09','2023-09-10']:
    print(d, "DO 12-22h", s1.get(D(d),0), "PU 18-24h", s2.get(D(d),0))

print("\n=== NYC Marathon Sun 2023-11-05 ===")
mar = D('2023-11-05'); base = [D('2023-10-29'), D('2023-11-12'), D('2023-11-19')]
cmp("Citywide yellow trips 7-17h", daily(pu,'pul',None,7,17), [mar], base)
cmp("Citywide yellow trips all day", daily(pu,'pul',None), [mar], base)
ues = [140,141,236,237,262,263,74,75]
cmp("PU UES/East Harlem 9-16h (1st Ave route)", daily(pu,'pul',ues,9,16), [mar], base)
cmp("PU Central Park zone 43 9-18h", daily(pu,'pul',[43],9,18), [mar], base)
cmp("PU Midtown 9-17h", daily(pu,'pul',[161,162,163,164,230,233,229],9,17), [mar], base)
for h0,h1 in [(9,12),(12,15),(15,18)]:
    print(f"Manhattan-yellow-zone trip speed {h0}-{h1}h: marathon {speed(pu, None, h0,h1,[mar]):.2f} mph vs base {speed(pu,None,h0,h1,base):.2f} mph; UES-origin {speed(pu,ues,h0,h1,[mar]):.2f} vs {speed(pu,ues,h0,h1,base):.2f}")
m = pu[(pu.dt.isin([mar]+base))]
hh = m.groupby(['dt','h']).n.sum().unstack(0)
hh['base']=hh[base].mean(axis=1); print((hh[[mar,'base']]).round(0).T.to_string())
fh = m.groupby(['dt','h']).agg(f=('fare','sum'),n=('n','sum'),d=('dur_ok','sum'))
fh['fare_per_trip']=fh.f/fh.n; fh['fare_per_hr_engaged']=fh.f/(fh.d/60)
x=fh.reset_index(); print("Fare per engaged hour 9-17h: marathon %.1f vs base %.1f; mean fare/trip %.2f vs %.2f" % (
   x[(x.dt==mar)&(x.h.between(9,16))].f.sum()/(x[(x.dt==mar)&(x.h.between(9,16))].d.sum()/60), x[(x.dt.isin(base))&(x.h.between(9,16))].f.sum()/(x[(x.dt.isin(base))&(x.h.between(9,16))].d.sum()/60),
   x[(x.dt==mar)&(x.h.between(9,16))].f.sum()/x[(x.dt==mar)&(x.h.between(9,16))].n.sum(), x[(x.dt.isin(base))&(x.h.between(9,16))].f.sum()/x[(x.dt.isin(base))&(x.h.between(9,16))].n.sum()))

print("\n=== UNGA high-level week 2023 (Mon Sep 18 - Fri Sep 22) ===")
ung = list(pd.date_range('2023-09-18','2023-09-22')); base = list(pd.date_range('2023-09-11','2023-09-15')) + list(pd.date_range('2023-10-02','2023-10-06'))
mte = [162,229,233,170,137,161]
cmp("PU Midtown East/Turtle Bay/Murray Hill 7-20h", daily(pu,'pul',mte,7,20), ung, base)
cmp("DO same zones 7-20h", daily(do,'dol',mte,7,20), ung, base)
cmp("PU UN/Turtle Bay S (233) 7-20h", daily(pu,'pul',[233],7,20), ung, base)
cmp("Citywide yellow 7-20h", daily(pu,'pul',None,7,20), ung, base)
for h0,h1 in [(8,11),(11,16),(16,20)]:
    print(f"Speed of trips from Midtown East zones {h0}-{h1}h: UNGA {speed(pu,mte,h0,h1,ung):.2f} mph vs base {speed(pu,mte,h0,h1,base):.2f}; all zones {speed(pu,None,h0,h1,ung):.2f} vs {speed(pu,None,h0,h1,base):.2f}")
for d in ung: print(d.date(), "mte speed 8-20h %.2f" % speed(pu,mte,8,20,[d]))

print("\n=== NYE 2023 (Sun Dec 31) ===")
nye = D('2023-12-31'); base = [D('2023-12-03'),D('2023-12-10'),D('2023-12-17')]
s = pu[pu.pul==230].groupby(['dt','h']).n.sum()
print("Times Sq (230) pickups by hour Dec31 vs mean of 3 Dec Sundays:")
print(pd.DataFrame({'nye':[s.get((nye,h),0) for h in range(12,24)],'base':[np.mean([s.get((b,h),0) for b in base]) for h in range(12,24)]}, index=range(12,24)).round(0).T.to_string())
s2 = pu.groupby(['dt','h']).n.sum()
nyd = D('2024-01-01'); bm = [D('2024-01-07'),D('2024-01-14')]
print("Citywide yellow pickups Jan 1 2024 0-5h vs Sundays Jan 7/14:", [s2.get((nyd,h),0) for h in range(6)], [round(np.mean([s2.get((b,h),0) for b in bm])) for h in range(6)])
f = pu[(pu.dt==nyd)&(pu.h<4)]; fb = pu[(pu.dt.isin(bm))&(pu.h<4)]
print("Jan1 0-4h mean fare %.2f vs %.2f; mean trip miles %.2f vs %.2f" % (f.fare.sum()/f.n.sum(), fb.fare.sum()/fb.n.sum(), f.mi.sum()/f.n.sum(), fb.mi.sum()/fb.n.sum()))

print("\n=== Javits zone 246: NY Comic Con Oct 12-15 2023; NY Auto Show Apr 7-16 2023 ===")
nycc = list(pd.date_range('2023-10-12','2023-10-15')); base = [x-pd.Timedelta(days=7) for x in nycc]+[x+pd.Timedelta(days=7) for x in nycc]
cmp("PU 246 all day", daily(pu,'pul',[246]), nycc, base); cmp("DO 246 7-13h", daily(do,'dol',[246],7,13), nycc, base); cmp("PU 246 16-21h", daily(pu,'pul',[246],16,21), nycc, base)
auto = list(pd.date_range('2023-04-07','2023-04-16')); base = list(pd.date_range('2023-03-17','2023-03-26'))+list(pd.date_range('2023-04-21','2023-04-30'))
cmp("PU 246 all day (auto show)", daily(pu,'pul',[246]), auto, base)

print("\n=== Taylor Swift MetLife (Fri-Sun May 26-28 2023): yellow DO outside NYC (265) 13-19h ===")
ts = list(pd.date_range('2023-05-26','2023-05-28')); base=[x for x in pd.date_range('2023-05-05','2023-06-25') if x.dayofweek>=4 and x not in ts]
cmp("DO 265 13-19h", daily(do,'dol',[265],13,19), ts, base)
cmp("DO 265 all day", daily(do,'dol',[265]), ts, base)

print("\n=== St Patrick's Day parade Fri Mar 17 2023 (5th Ave 44th-79th, ~11:00-16:30) ===")
sp = D('2023-03-17'); base = [D('2023-03-03'),D('2023-03-10'),D('2023-03-24'),D('2023-03-31')]
cmp("Citywide 11-17h", daily(pu,'pul',None,11,17), [sp], base)
cmp("PU Midtown Center/East/North + UES S (161,162,163,237,140,141) 11-17h", daily(pu,'pul',[161,162,163,237,140,141],11,17), [sp], base)
for h0,h1 in [(9,11),(11,14),(14,17),(17,20)]:
    print(f"speed {h0}-{h1}: parade {speed(pu,None,h0,h1,[sp]):.2f} vs {speed(pu,None,h0,h1,base):.2f}; from 161/162/163 {speed(pu,[161,162,163],h0,h1,[sp]):.2f} vs {speed(pu,[161,162,163],h0,h1,base):.2f}")
cmp("Citywide 17-24h", daily(pu,'pul',None,17,24), [sp], base)
cmp("PU Greenwich/E Village/LES/Midtown bars? (79,148,113,114,249) 17-24h", daily(pu,'pul',[79,148,113,114,249],17,24), [sp], base)

print("\n=== NYC Pride March Sun Jun 25 2023 ===")
pr = D('2023-06-25'); base=[D('2023-06-11'),D('2023-06-18'),D('2023-07-09')]
vil=[249,158,113,114,125,68,90,234]
cmp("PU Village/Chelsea 12-18h", daily(pu,'pul',vil,12,18), [pr], base); cmp("PU Village/Chelsea 18-24h", daily(pu,'pul',vil,18,24), [pr], base)
cmp("Citywide 10-18h", daily(pu,'pul',None,10,18), [pr], base)
for h0,h1 in [(11,14),(14,18)]: print(f"speed {h0}-{h1}: pride {speed(pu,None,h0,h1,[pr]):.2f} vs {speed(pu,None,h0,h1,base):.2f}; village origin {speed(pu,vil,h0,h1,[pr]):.2f} vs {speed(pu,vil,h0,h1,base):.2f}")

print("\n=== Village Halloween Parade Tue Oct 31 2023 (6th Ave, ~19:00-22:30) ===")
hw = D('2023-10-31'); base=[D('2023-10-17'),D('2023-10-24'),D('2023-11-07'),D('2023-11-14')]
cmp("PU Village/Chelsea 21-24h", daily(pu,'pul',vil,21,24), [hw], base); cmp("Citywide 18-24h", daily(pu,'pul',None,18,24), [hw], base)
print(f"speed 18-22 village origin: {speed(pu,vil,18,22,[hw]):.2f} vs {speed(pu,vil,18,22,base):.2f}")

print("\n=== Sep 29 2023 flash flood (Fri; subway suspensions, state of emergency) ===")
fl = D('2023-09-29'); base=[D('2023-09-08'),D('2023-09-15'),D('2023-09-22'),D('2023-10-06'),D('2023-10-13')]
s = pu[pu.dt.isin([fl]+base)].groupby(['dt','h']).agg(n=('n','sum'),f=('fare','sum'),mi=('mi_ok','sum'),d=('dur_ok','sum')).reset_index()
t = s.pivot(index='h', columns='dt', values='n'); t['base']=t[base].mean(axis=1); print("trips/h:", t[[fl,'base']].round(0).T.to_string())
s['mph']=60*s.mi/s.d; t2=s.pivot(index='h',columns='dt',values='mph'); t2['base']=t2[base].mean(axis=1); print("mph:", t2[[fl,'base']].round(1).T.to_string())
s['fpt']=s.f/s.n; t3=s.pivot(index='h',columns='dt',values='fpt'); t3['base']=t3[base].mean(axis=1); print("fare/trip:", t3[[fl,'base']].round(1).T.to_string())
cmp("Citywide all day", daily(pu,'pul',None), [fl], base)
cmp("Outer borough PU (Boro zones in Brooklyn/Queens) all day", daily(pu,'pul',list(range(1,264)),0,24), [fl], base)

print("\n=== Jan 8 2024 (Mon) bridge/tunnel protest check ===")
pt = D('2024-01-08'); base=[D('2024-01-22'),D('2024-01-29'), D('2023-12-11'), D('2023-12-18')]
s = pu[pu.dt.isin([pt]+base)].groupby(['dt','h']).agg(n=('n','sum'),mi=('mi_ok','sum'),d=('dur_ok','sum')).reset_index(); s['mph']=60*s.mi/s.d
t=s.pivot(index='h',columns='dt',values='mph'); t['base']=t[base].mean(axis=1); print("mph:", t[[pt,'base']].round(1).T.to_string())
t=s.pivot(index='h',columns='dt',values='n'); t['base']=t[base].mean(axis=1); print("n:", t[[pt,'base']].round(0).T.to_string())
