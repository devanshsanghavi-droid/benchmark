import json, sys
d = json.load(open(sys.argv[1]))
def inring(x, y, ring):
    n = len(ring); inside = False; j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]; xj, yj = ring[j][0], ring[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-15) + xi):
            inside = not inside
        j = i
    return inside
def inpoly(x, y, coords):
    if not inring(x, y, coords[0]): return False
    return not any(inring(x, y, h) for h in coords[1:])
def locate(lat, lon):
    hits = []
    for f in d['features']:
        g = f['geometry']; p = f['properties']
        polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        if any(inpoly(lon, lat, pc) for pc in polys): hits.append((p['LocationID'], p['zone'], p['borough']))
    return hits
venues = {
 'Barclays Center': (40.68265, -73.97469), 'Madison Square Garden': (40.75051, -73.99345),
 'Penn Station': (40.75058, -73.99358), 'Yankee Stadium': (40.82919, -73.92650),
 'Citi Field': (40.75707, -73.84582), 'Arthur Ashe Stadium': (40.74968, -73.84722),
 'Javits Center': (40.75767, -74.00213), 'Times Square (Broadway/45th)': (40.75800, -73.98557),
 'Randalls Island festival grounds': (40.7915, -73.9230), 'UN Headquarters': (40.74893, -73.96807),
 'Vivian Beaumont (Lincoln Center)': (40.77406, -73.98422), 'Radio City / Rockefeller': (40.75997, -73.97997),
 'Port Authority Bus Terminal': (40.75690, -73.99045), 'Forest Hills Stadium': (40.71957, -73.84837),
 'UBS Arena (Elmont)': (40.7117, -73.7255), 'Gershwin Theatre (W 51st)': (40.76246, -73.98538),
 'Studio 54 (W 54th)': (40.76443, -73.98352),
}
for k, (la, lo) in venues.items(): print(f"{k}: {locate(la, lo)}")
