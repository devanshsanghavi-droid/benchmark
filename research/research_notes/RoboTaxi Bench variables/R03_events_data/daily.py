import sys, duckdb, pandas as pd
agg=sys.argv[1]; con=duckdb.connect()
d=con.execute(f"select dt, sum(n) n from '{agg}/pu_date_hour_zone.parquet' group by 1 order by 1").fetchdf(); d['dt']=pd.to_datetime(d.dt)
d['dow']=d.dt.dt.dayofweek; d['med']=d.groupby([d.dt.dt.month,'dow']).n.transform('median'); d['r']=d.n/d.med
print(d[d.r<0.75].to_string())
print(d[(d.dt>='2023-09-14')&(d.dt<='2023-10-02')].to_string())
