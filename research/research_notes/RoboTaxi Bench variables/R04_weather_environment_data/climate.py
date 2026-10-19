import sys, pandas as pd, numpy as np
R=sys.argv[1]
w = pd.read_csv(f"{R}/dl/cpw.csv", parse_dates=["DATE"])
w["y"]=w.DATE.dt.year; w["m"]=w.DATE.dt.month
f = w[(w.y>=2009)&(w.y<=2025)]
ny = f.y.nunique(); print("years", ny, "rows", len(f), "missing PRCP", f.PRCP.isna().sum(), "SNOW", f.SNOW.isna().sum(), "AWND", f.AWND.isna().sum())
def per_year(mask): return round(mask.sum()/ny,1)
P,Sn,T,Tn,A=f.PRCP,f.SNOW,f.TMAX,f.TMIN,f.AWND
print("annual precip in", round(P.sum()/ny,1), "snowfall in", round(Sn.sum()/ny,1))
for t in [0.01,0.1,0.25,0.5,1.0,2.0,3.0]: print(f"days PRCP>={t}", per_year(P>=t))
for t in [0.1,1,4,6,10]: print(f"days SNOW>={t}", per_year(Sn>=t))
print("days snow depth>=1", per_year(f.SNWD>=1))
for t in [85,90,95,100]: print(f"days TMAX>={t}", per_year(T>=t))
print("days TMAX<=32", per_year(T<=32), "TMIN<=32", per_year(Tn<=32), "TMIN<=20", per_year(Tn<=20), "TMIN<=10", per_year(Tn<=10))
print("AWND mean mph", round(A.mean(),2), "days AWND>=10", per_year(A>=10), ">=15", per_year(A>=15))
m = f.groupby("m").agg(p_wet=("PRCP", lambda x:(x>=0.01).mean()), p_wet25=("PRCP", lambda x:(x>=0.25).mean()), p_1in=("PRCP", lambda x:(x>=1.0).mean()), p_snow=("SNOW", lambda x:(x>=0.1).mean()), snow_in=("SNOW", lambda x:x.sum()/ny), tmax=("TMAX","mean"), tmin=("TMIN","mean"), hot90=("TMAX", lambda x:(x>=90).sum()/ny), frz=("TMIN", lambda x:(x<=32).sum()/ny), awnd=("AWND","mean"))
print(m.round(2).to_string())
print("top precip days:\n", f.nlargest(12,"PRCP")[["DATE","PRCP","SNOW","TMAX"]].to_string(index=False))
print("top snow days:\n", f.nlargest(10,"SNOW")[["DATE","PRCP","SNOW","SNWD","TMAX"]].to_string(index=False))
f2=w.copy(); f2["season"]=np.where(f2.m>=7, f2.y, f2.y-1)
s=f2[(f2.season>=2009)&(f2.season<=2025)].groupby("season").SNOW.sum(); print("season snowfall:", s.round(1).to_dict())
print("hottest:", f.nlargest(5,"TMAX")[["DATE","TMAX"]].to_string(index=False)); print("coldest:", f.nsmallest(5,"TMIN")[["DATE","TMIN"]].to_string(index=False))
# 2015 blizzard and 2016 Jonas, 2012 Sandy, 2011 Irene, 2021 Ida/Henri, 2023-09-29, 2024-02-13, Jan 2026
for dt in ["2011-08-27","2011-08-28","2012-10-29","2012-10-30","2015-01-26","2015-01-27","2016-01-23","2016-01-24","2021-08-22","2021-09-01","2023-09-29","2024-02-13","2025-07-14","2025-07-31","2026-01-25","2026-01-26","2026-02-22","2026-02-23"]:
    r=w[w.DATE==dt]
    if len(r): print(dt, r[["PRCP","SNOW","SNWD","TMAX","TMIN","AWND"]].to_dict("records")[0])
g = pd.read_csv(f"{R}/dl/thesis_2023.csv", dtype=str)
fr = g.FRSHTT.str.zfill(6)
print("GSOD 2023 days: fog", (fr.str[0]=="1").sum(), "rain/drizzle", (fr.str[1]=="1").sum(), "snow", (fr.str[2]=="1").sum(), "hail", (fr.str[3]=="1").sum(), "thunder", (fr.str[4]=="1").sum())
vis = pd.to_numeric(g.VISIB, errors="coerce").replace(999.9, np.nan)
print("GSOD 2023 mean daily visibility mi: days <5", (vis<5).sum(), "<3", (vis<3).sum(), "<1", (vis<1).sum(), "n", vis.notna().sum())
gust = pd.to_numeric(g.GUST, errors="coerce").replace(999.9,np.nan); mx=pd.to_numeric(g.MXSPD,errors="coerce").replace(999.9,np.nan)
print("GSOD 2023 gust knots: days>=30", (gust>=30).sum(), ">=40", (gust>=40).sum(), "max", gust.max(), "n", gust.notna().sum())
