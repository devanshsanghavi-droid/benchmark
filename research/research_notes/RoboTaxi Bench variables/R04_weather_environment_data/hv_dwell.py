import sys, pandas as pd, numpy as np
R=sys.argv[1]
w = pd.read_csv(f"{R}/dl/cpw.csv", parse_dates=["DATE"]).rename(columns={"DATE":"dt"})
h = pd.read_csv(f"{R}/hv_date_hour.csv", parse_dates=["dt"])
u = h[h.lic=="HV0003"].copy(); u["dn"]=u.med_dwell*u.n; u["pn"]=u.med_wait_pu*u.n
d = u.groupby("dt").agg(n=("n","sum"),dn=("dn","sum"),pn=("pn","sum")).reset_index(); d["dwell"]=d.dn/d.n; d["req_to_pu"]=d.pn/d.n
d = d.merge(w[["dt","PRCP"]],on="dt"); d=d[~d.dt.isin(pd.to_datetime(["2023-01-01","2023-01-02","2023-01-16"]))]
d["dow"]=d.dt.dt.dayofweek; d["trend"]=(d.dt-d.dt.min()).dt.days; d["wet"]=(d.PRCP>=0.10).astype(float)
X=pd.concat([pd.Series(1.0,index=d.index), d[["wet","trend"]].astype(float), pd.get_dummies(d.dow.astype(str),drop_first=True).astype(float)],axis=1).values
for col in ["dwell","req_to_pu"]:
    yy=d[col].values; b,*_=np.linalg.lstsq(X,yy,rcond=None); e=yy-X@b; n,k=X.shape; s2=e@e/(n-k); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    print(col, "dry mean", round(d.loc[d.wet==0,col].mean(),3), "wet effect", round(b[1],3), "t", round(b[1]/se[1],1))
