import sys, pandas as pd, numpy as np
R=sys.argv[1]
w = pd.read_csv(f"{R}/dl/cpw.csv", parse_dates=["DATE"]).rename(columns={"DATE":"dt"})
h = pd.read_csv(f"{R}/hv_date_hour.csv", parse_dates=["dt"])
y = pd.read_csv(f"{R}/yellow_date_hour.csv", parse_dates=["dt"])
y = y[(y.dt>="2023-01-01")&(y.dt<"2023-02-01")].groupby("dt").n.sum().rename("yellow")
u = h[h.lic=="HV0003"].groupby("dt").n.sum().rename("uber")
l = h[h.lic=="HV0005"].groupby("dt").n.sum().rename("lyft")
d = pd.concat([y,u,l],axis=1).reset_index().merge(w[["dt","PRCP"]],on="dt")
d = d[~d.dt.isin(pd.to_datetime(["2023-01-01","2023-01-02","2023-01-16"]))]
d["dow"]=d.dt.dt.dayofweek; d["trend"]=(d.dt-d.dt.min()).dt.days
d["wet"]=(d.PRCP>=0.10).astype(float)
for spec in ["dow","dow+trend"]:
    cols=[pd.Series(1.0,index=d.index,name="c"), d[["wet"]], pd.get_dummies(d.dow.astype(str),drop_first=True).astype(float)]
    if "trend" in spec: cols.append(d[["trend"]].astype(float))
    X=pd.concat(cols,axis=1).values
    for col in ["yellow","uber","lyft"]:
        yy=np.log(d[col].values); b,*_=np.linalg.lstsq(X,yy,rcond=None); e=yy-X@b; n,k=X.shape; s2=e@e/(n-k); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        print(spec, col, f"wet-day {(np.exp(b[1])-1)*100:+.1f}% t={b[1]/se[1]:.1f}")
# hv waits with trend
h2=h[h.lic=="HV0003"].copy(); h2["wn"]=h2.med_wait_os*h2.n
dd=h2.groupby("dt").agg(n=("n","sum"),wn=("wn","sum")).reset_index(); dd["wait"]=dd.wn/dd.n
dd=dd.merge(d[["dt","wet","dow","trend"]],on="dt")
X=pd.concat([pd.Series(1.0,index=dd.index), dd[["wet","trend"]].astype(float), pd.get_dummies(dd.dow.astype(str),drop_first=True).astype(float)],axis=1).values
yy=dd.wait.values; b,*_=np.linalg.lstsq(X,yy,rcond=None); e=yy-X@b; n,k=X.shape; s2=e@e/(n-k); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
print("uber wait wet-day", round(b[1],3), "t", round(b[1]/se[1],1))
# hourly wait profile on heavy-ish wet days (PRCP>=0.4) vs dry same dow
hh=h[h.lic=="HV0003"].merge(w[["dt","PRCP"]],on="dt"); hh["dow"]=hh.dt.dt.dayofweek
wetd=hh[(hh.PRCP>=0.4)]; dry=hh[(hh.PRCP==0)&(hh.dow.isin([1,2,3]))&(~hh.dt.isin(pd.to_datetime(["2023-01-01","2023-01-02","2023-01-16"])))]
print(wetd.dt.drop_duplicates().dt.date.tolist())
a=wetd[wetd.dow.isin([1,2,3])].groupby("h").agg(n=("n","mean"),wait=("med_wait_os","mean")); b2=dry.groupby("h").agg(n=("n","mean"),wait=("med_wait_os","mean"))
print(pd.DataFrame({"n_wet":a.n.round(0),"n_dry":b2.n.round(0),"ratio":(a.n/b2.n).round(2),"wait_wet":a.wait.round(2),"wait_dry":b2.wait.round(2)}).to_string())
