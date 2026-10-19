import datetime as dt
from zoneinfo import ZoneInfo
from astral import LocationInfo
from astral.sun import sun, azimuth, elevation
tz = ZoneInfo("America/New_York")
loc = LocationInfo("NYC","USA","America/New_York",40.7831,-73.9712)
rows=[]
d = dt.date(2026,1,1)
while d.year==2026:
    s = sun(loc.observer, date=d, tzinfo=tz)
    rows.append((d, s["dawn"], s["sunrise"], s["sunset"], s["dusk"], (s["sunset"]-s["sunrise"]).total_seconds()/3600, azimuth(loc.observer, s["sunset"]), azimuth(loc.observer, s["sunrise"])))
    d += dt.timedelta(days=1)
mn = min(rows, key=lambda r:r[5]); mx = max(rows, key=lambda r:r[5])
print("shortest day", mn[0], round(mn[5],2), "h; sunrise", mn[2].strftime("%H:%M"), "sunset", mn[3].strftime("%H:%M"))
print("longest day", mx[0], round(mx[5],2), "h; sunrise", mx[2].strftime("%H:%M"), "sunset", mx[3].strftime("%H:%M"))
es = min(rows, key=lambda r:r[3].hour*60+r[3].minute); ls = max(rows, key=lambda r:r[3].hour*60+r[3].minute)
er = min(rows, key=lambda r:r[2].hour*60+r[2].minute); lr = max(rows, key=lambda r:r[2].hour*60+r[2].minute)
print("earliest sunset", es[0], es[3].strftime("%H:%M"), "latest sunset", ls[0], ls[3].strftime("%H:%M"))
print("earliest sunrise", er[0], er[2].strftime("%H:%M"), "latest sunrise", lr[0], lr[2].strftime("%H:%M"))
print("civil twilight length (dusk-sunset) min/max min:", round(min((r[4]-r[3]).total_seconds()/60 for r in rows),1), round(max((r[4]-r[3]).total_seconds()/60 for r in rows),1))
# Manhattan grid ~ 29 deg east of true north -> crosstown streets point to azimuth ~299 (sunset) and ~119 (sunrise)
ss = sorted(rows, key=lambda r: abs(r[6]-299.0))[:4]
sr = sorted(rows, key=lambda r: abs(r[7]-119.0))[:4]
print("sunset az ~299 (Manhattanhenge-ish):", [(r[0].isoformat(), round(r[6],1)) for r in ss])
print("sunrise az ~119:", [(r[0].isoformat(), round(r[7],1)) for r in sr])
# DST transitions 2026
print("months avg sunset hour (local):", {m: round(sum(r[3].hour+r[3].minute/60 for r in rows if r[0].month==m)/sum(1 for r in rows if r[0].month==m),2) for m in range(1,13)})
