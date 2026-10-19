import sys, json, importlib.util
spec = importlib.util.spec_from_file_location('v', sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
out_md, out_json = sys.argv[2], sys.argv[3]
VIS = {"visible": "visible", "public_or_forecast": "public or forecast", "hidden": "hidden"}
rows = []
for i, v in enumerate(m.V, 1):
    sb, name, desc, vals, imp, ev, role, vis, app, ds, how, comp, pri = v
    rows.append(dict(id=f"R03-{i:03d}", sub_box=m.SB[sb], name=name, description=desc, values_or_range=vals, impact=imp,
                     impact_evidence=ev, role=role, visibility=vis, applies_to=app, data_source=ds, how_to_model=how,
                     component=comp, priority=pri, _sb=sb))
json.dump([{k: r[k] for k in r if k != '_sb'} for r in rows], open(out_json, 'w'), indent=1)

def esc(s): return s.replace('|', '/')
L = []
A = L.append
A("# R03 Events, disruptions and public event information: simulation variables for RoboTaxi Bench")
A("")
A("Domain R03 of 12. Owner of the full list: Devansh. Researched on 19 Oct 2026 for the \"independent variables list\" action from the RoboTaxi Bench meeting.")
A("")
A("## Summary")
A("")
A(open(sys.argv[4]).read().strip())
A("")
A("### How to read the tables")
A("")
A("- **Variable**: ID and name, then (priority; applies to; component).")
A("- **Impact**: effect on driver or fleet profit per hour (high / medium / low). For closures the effect is often negative.")
A("- **Role**: world = outside input; rule = designer-set rule; agent = model decision; state = changes during the run; setting = benchmark knob.")
A("- **Agent sees?**: visible / public or forecast (public information or a forecast it may get) / hidden (simulator only).")
A("- **Source tags**: [P] primary read directly; [P*] primary data via a verbatim copy, including my own calculations on SHA-256-verified TLC files; [S] search snippet or secondary; [U] unverified background knowledge; [design] our suggestion or guess.")
A("- Driver types: human app driver (Uber/Lyft, NYC \"HVFHV\"), taxi (yellow/green, street hail plus e-hail), robotaxi (Waymo-like). Levels: single car and fleet of N.")
A("")
A(open(sys.argv[5]).read().strip())
A("")
A("## Box view (the placeholder list, extended)")
A("")
A("* Events, disruptions and public event information (R03)")
cur = None
for r in rows:
    if r['_sb'] != cur:
        cur = r['_sb']; A(f"   * {m.SB[cur]}")
    A(f"      * {r['id']} {r['name']} [{r['impact']} impact]")
A("")
A("## Variables by sub-box")
for sb in m.SB:
    rs = [r for r in rows if r['_sb'] == sb]
    A("")
    A(f"### {sb}. {m.SB[sb]} ({len(rs)} variables)")
    A("")
    A("| Variable | What it is | Values or range | Impact | Evidence | Role | Agent sees? | Data source | How to model |")
    A("|---|---|---|---|---|---|---|---|---|")
    for r in rs:
        A(f"| **{r['id']} {esc(r['name'])}** ({r['priority']}; {esc(r['applies_to'])}; {r['component']}) | {esc(r['description'])} | {esc(r['values_or_range'])} | {r['impact']} | {esc(r['impact_evidence'])} | {r['role']} | {VIS[r['visibility']]} | {esc(r['data_source'])} | {esc(r['how_to_model'])} |")
A("")
A(open(sys.argv[6]).read().strip())
A("")
open(out_md, 'w').write("\n".join(L))
from collections import Counter
print(len(rows), Counter(r['impact'] for r in rows), Counter(r['priority'] for r in rows), Counter(r['_sb'] for r in rows))
