import sys, pandas as pd, numpy as np
R=sys.argv[1]
y = pd.read_csv(f"{R}/yellow_date_hour.csv", parse_dates=["dt"])
y["dow"]=y.dt.dt.dayofweek
y["mph"]=y.mi/y.hrs
def prof(day, refs):
    a = y[y.dt==day].set_index("h")
    b = y[y.dt.isin(pd.to_datetime(refs))].groupby("h")[["n","mi","hrs","fare"]].mean()
    b["mph"]=b.mi/b.hrs
    out = pd.DataFrame({"n_day":a.n, "n_ref":b.n.round(0), "ratio":(a.n/b.n).round(2), "mph_day":a.mph.round(1), "mph_ref":b.mph.round(1), "fare_ph_eng_day":(a.fare/a.hrs).round(1), "fare_ph_eng_ref":(b.fare/b.hrs).round(1)})
    print(f"== {day} vs {refs}"); print(out.to_string())
    tot = a.n.sum()/b.n.sum(); print("daily ratio", round(tot,3))
prof("2023-09-29", ["2023-09-15","2023-09-22","2023-10-06","2023-10-13"])
prof("2024-01-16", ["2024-01-09","2024-01-23","2024-01-30"])
prof("2023-04-30", ["2023-04-16","2023-05-07","2023-05-14"])
prof("2023-06-07", ["2023-05-31","2023-06-14","2023-06-21"])
prof("2023-07-27", ["2023-07-13","2023-07-20","2023-08-03"])
