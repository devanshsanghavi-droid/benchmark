import sys
import numpy as np, pandas as pd
R = sys.argv[1]
w = pd.read_csv(f"{R}/dl/cpw.csv", parse_dates=["DATE"])
w = w.rename(columns={"DATE":"dt"}); w["dt"]=w["dt"].dt.date
y = pd.read_csv(f"{R}/yellow_date_hour.csv", parse_dates=["dt"]); y["dt"]=y["dt"].dt.date
d = y.groupby("dt").sum(numeric_only=True).drop(columns=["h"]).reset_index()
d = d.merge(w, on="dt", how="left")
hol = pd.to_datetime(["2023-01-01","2023-01-02","2023-01-16","2023-02-20","2023-05-29","2023-06-19","2023-07-04","2023-09-04","2023-10-09","2023-11-23","2023-11-24","2023-12-24","2023-12-25","2023-12-26","2023-12-31","2024-01-01","2024-01-15","2023-07-03"]).date
d = d[~d["dt"].isin(hol)].copy()
dts = pd.to_datetime(d["dt"])
d["dow"]=dts.dt.dayofweek; d["ym"]=dts.dt.strftime("%Y-%m")
P=d["PRCP"]; Sn=d["SNOW"]; T=d["TMAX"]
d["r_light"]=((P>=0.01)&(P<0.25)&(Sn<0.1)).astype(float)
d["r_mod"]=((P>=0.25)&(P<1.0)&(Sn<0.1)).astype(float)
d["r_heavy"]=((P>=1.0)&(Sn<0.1)).astype(float)
d["snow"]=(Sn>=0.1).astype(float)
d["t_cold"]=(T<=35).astype(float); d["t_cool"]=((T>35)&(T<=50)).astype(float)
d["t_warm"]=((T>=81)&(T<=89)).astype(float); d["t_hot"]=(T>=90).astype(float)
print("days", len(d), "light", d.r_light.sum(), "mod", d.r_mod.sum(), "heavy", d.r_heavy.sum(), "snow", d.snow.sum(), "cold", d.t_cold.sum(), "cool", d.t_cool.sum(), "warm", d.t_warm.sum(), "hot", d.t_hot.sum())
print("heavy days:", d.loc[d.r_heavy==1, ["dt","PRCP","TMAX"]].to_string(index=False))
print("snow days:", d.loc[d.snow==1, ["dt","PRCP","SNOW","TMAX"]].to_string(index=False))
d["mph"]=d["mi"]/d["hrs"]; d["avg_fare"]=d["fare"]/d["n"]; d["avg_mi"]=d["mi"]/d["n"]
d["tip_pct"]=100*d["tip_card"]/d["fare_card"]; d["tip_inc"]=100*d["n_card_tip"]/d["n_card"]
d["apt_share"]=100*d["n_apt_pu"]/d["n"]; d["short_share"]=100*d["n_short"]/d["n"]
d["card_share"]=100*d["n_card"]/d["n"]; d["avg_min"]=60*d["hrs"]/d["n"]
d["fare_per_hr_eng"]=d["fare"]/d["hrs"]
X = pd.get_dummies(d[["dow","ym"]].astype(str), drop_first=True).astype(float)
regs=["r_light","r_mod","r_heavy","snow","t_cold","t_cool","t_warm","t_hot"]
X = pd.concat([pd.Series(1.0,index=d.index,name="const"), d[regs], X], axis=1)
def ols(yv, logy):
    yy = np.log(yv) if logy else yv
    b, res, rk, sv = np.linalg.lstsq(X.values, yy.values, rcond=None)
    e = yy.values - X.values@b; n,k = X.shape
    s2 = e@e/(n-k); cov = s2*np.linalg.inv(X.values.T@X.values); se=np.sqrt(np.diag(cov))
    out={}
    for i,c in enumerate(X.columns):
        if c in regs:
            eff = (np.exp(b[i])-1)*100 if logy else b[i]
            out[c]=f"{eff:+.1f}{'%' if logy else ''} (t={b[i]/se[i]:.1f})"
    return out
rows={}
for col,logy in [("n",True),("fare",True),("hrs",True),("mph",False),("avg_mi",False),("avg_min",False),("avg_fare",False),("fare_per_hr_eng",False),("tip_pct",False),("tip_inc",False),("card_share",False),("apt_share",False),("short_share",False)]:
    rows[col]=ols(d[col],logy)
res=pd.DataFrame(rows).T
pd.set_option("display.width",250)
print(res.to_string())
print("baseline dry means:", d.loc[(d.PRCP==0)&(d.SNOW==0), ["n","mph","avg_mi","avg_min","avg_fare","fare_per_hr_eng","tip_pct","tip_inc","apt_share","short_share"]].mean().round(2).to_dict())
d.to_csv(f"{R}/yellow_daily_weather.csv", index=False)
