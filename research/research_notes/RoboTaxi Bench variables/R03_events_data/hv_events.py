import sys, duckdb, pandas as pd, numpy as np
f=sys.argv[1]; con=duckdb.connect(); con.execute("PRAGMA threads=4")
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
con.execute(f"""create table hv as select request_datetime rq, on_scene_datetime os, pickup_datetime pu, PULocationID pul, DOLocationID dol, trip_miles mi, trip_time tt, base_passenger_fare fare, driver_pay pay, tips, hvfhs_license_num lic
 from '{f}' where pickup_datetime>='2023-01-01' and pickup_datetime<'2023-02-01' and PULocationID in (186,230,25,65,97,189,52,33,181,61,246,132,138,161,162,163,164,100,68)""")
# which Brooklyn zone has spiky late pickups
q="""select pul, cast(pu as date) d, count(*) n from hv where hour(pu) between 21 and 23 group by 1,2"""
t=con.execute(q).fetchdf(); g=t.groupby('pul').n.agg(['mean','std','max']); g['cv']=g['std']/g['mean']; print(g.round(2).to_string())
def nightly(z, h0=21.5, h1=23.5):
    q=f"""select cast(pu as date) d, count(*) n, median(epoch(pu-rq)/60) wait, avg(fare/nullif(mi,0)) fpm_raw,
      sum(fare)/sum(mi) fpm, sum(fare)/sum(tt/60.0) fpmin, sum(pay)/sum(tt/3600.0) pay_hr, sum(pay)/sum(mi) paypm, avg(mi) mi, avg(tips) tip
      from hv where pul={z} and (hour(pu)+minute(pu)/60.0) between {h0} and {h1} and mi between 0.5 and 30 and dayofweek(pu) between 0 and 6 and cast(pu as date) not in ('2023-01-01') group by 1 order by 1"""
    return con.execute(q).fetchdf()
for z in [186, 189, 25, 230, 246]:
    x=nightly(z); x['dow']=pd.to_datetime(x.d).dt.dayofweek
    top=x.n.quantile(.8); bot=x.n.quantile(.4)
    a=x[x.n>=top]; b=x[x.n<=bot]
    print(f"\nzone {z} 21:30-23:30: nights={len(x)}; top20% n mean {a.n.mean():.0f} vs bottom40% {b.n.mean():.0f}; wait {a.wait.mean():.1f} vs {b.wait.mean():.1f} min; fare/mi {a.fpm.mean():.2f} vs {b.fpm.mean():.2f}; fare/min {a.fpmin.mean():.2f} vs {b.fpmin.mean():.2f}; pay/engaged hr {a.pay_hr.mean():.1f} vs {b.pay_hr.mean():.1f}; pay/mi {a.paypm.mean():.2f} vs {b.paypm.mean():.2f}; miles {a.mi.mean():.2f} vs {b.mi.mean():.2f}")
    print("corr(n, fare/mi)=%.2f corr(n, wait)=%.2f corr(n,pay_hr)=%.2f" % (x.n.corr(x.fpm), x.n.corr(x.wait), x.n.corr(x.pay_hr)))
    if z==186: print(x.sort_values('n',ascending=False).head(8).round(2).to_string())
# within-night 15-min dynamics at 186 on top nights: count, fare/mi, wait
x=nightly(186); top=set(x[x.n>=x.n.quantile(.8)].d.astype(str)); bot=set(x[x.n<=x.n.quantile(.4)].d.astype(str))
q="""select cast(pu as date)::varchar d, hour(pu)*100+(minute(pu)//15)*15 t, count(*) n, sum(fare)/sum(mi) fpm, median(epoch(pu-rq)/60) wait, median(epoch(pu-os)/60) board from hv where pul=186 and hour(pu)>=20 and mi between 0.5 and 30 group by 1,2"""
w=con.execute(q).fetchdf()
for lab,S in [('top',top),('bottom',bot)]:
    y=w[w.d.isin(S)].groupby('t').agg(n=('n','mean'),fpm=('fpm','mean'),wait=('wait','mean'),board=('board','mean'))
    print(lab); print(y.round(2).T.to_string())
# NYE night: Times Sq 230 and Midtown 0-3h Jan 1 vs other Sundays (HVFHV)
q="""select case when cast(pu as date)='2023-01-01' then 'jan1' else 'othersun' end k, hour(pu) h, count(*)/case when cast(pu as date)='2023-01-01' then 1.0 else 4.0 end n, sum(fare)/sum(mi) fpm, median(epoch(pu-rq)/60) wait, sum(pay)/sum(tt/3600.0) payhr
  from hv where dayofweek(pu)=0 and hour(pu)<4 and mi between 0.5 and 30 group by 1,2 order by 2,1"""
print(con.execute(q).fetchdf().round(2).to_string())
