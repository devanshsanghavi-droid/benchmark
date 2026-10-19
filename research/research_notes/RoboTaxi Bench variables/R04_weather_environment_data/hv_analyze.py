import sys, pandas as pd, numpy as np
R=sys.argv[1]
w = pd.read_csv(f"{R}/dl/cpw.csv", parse_dates=["DATE"]).rename(columns={"DATE":"dt"})
h = pd.read_csv(f"{R}/hv_date_hour.csv", parse_dates=["dt"])
u = h[h.lic=="HV0003"].copy()  # Uber
u["wn"] = u.med_wait_os*u.n
d = u.groupby("dt").agg(n=("n","sum"), fare=("fare","sum"), mi=("mi","sum"), hrs=("hrs","sum"), pay=("pay","sum"), tips=("tips","sum"), n_tip=("n_tip","sum"), wn=("wn","sum"), n_short=("n_short","sum")).reset_index()
d["wait"]=d.wn/d.n
d = d.merge(w[["dt","PRCP","SNOW","TMAX","TMIN","AWND"]], on="dt")
d = d[~d.dt.isin(pd.to_datetime(["2023-01-01","2023-01-02","2023-01-16"]))]
d["dow"]=d.dt.dt.dayofweek
d["fare_mi"]=d.fare/d.mi; d["pay_hr"]=d.pay/d.hrs; d["tip_inc"]=100*d.n_tip/d.n; d["tip_per_trip"]=d.tips/d.n; d["short"]=100*d.n_short/d.n
d["fare_trip"]=d.fare/d.n; d["pay_share"]=100*d.pay/d.fare
d["wet"]=(d.PRCP>=0.10).astype(float)
print(d[["dt","dow","PRCP","TMAX","n","wait","fare_mi","fare_trip","pay_hr","pay_share","tip_inc","short"]].round(2).to_string(index=False))
X = pd.concat([pd.Series(1.0,index=d.index,name="c"), d[["wet"]], pd.get_dummies(d.dow.astype(str),drop_first=True).astype(float)],axis=1).values
for col,logy in [("n",True),("wait",False),("fare_mi",False),("fare_trip",False),("pay_hr",False),("pay_share",False),("tip_inc",False),("tip_per_trip",False),("short",False)]:
    yy = np.log(d[col].values) if logy else d[col].values
    b,*_ = np.linalg.lstsq(X,yy,rcond=None); e=yy-X@b; n,k=X.shape; s2=e@e/(n-k); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    eff=(np.exp(b[1])-1)*100 if logy else b[1]
    print(col, f"wet-day effect {eff:+.2f}{'%' if logy else ''} t={b[1]/se[1]:.1f}", "dry mean", round(d.loc[d.wet==0,col].mean(),2))
