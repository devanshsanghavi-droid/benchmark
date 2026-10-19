"""RoboTaxi Bench variable list: collect workflow outputs, write compact list, then render final boxed markdown + CSV.

Usage:
  python3 robotaxi_render.py collect <task_output_json> [<task_output_json> ...]
  python3 robotaxi_render.py render <finish_task_output_json>
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = "/home/user/benchmark"
DIR = f"{ROOT}/research/research_notes/RoboTaxi Bench variables"
FULL = f"{DIR}/all_variables.json"
COMPACT = f"{DIR}/ALL_VARIABLES_COMPACT.md"
OUT_MD = f"{ROOT}/research/reports/RoboTaxi Bench variables.md"
OUT_CSV = f"{ROOT}/research/reports/RoboTaxi Bench variables.csv"
OUT_SHORT = f"{ROOT}/research/reports/RoboTaxi Bench variables - short list.md"
CHAT = "/tmp/claude-0/-home-user-benchmark/5fc33e21-6d61-5fb2-89f8-1da370892943/scratchpad/robotaxi_chat.md"

ROLE = {"world": "World input", "rule": "Rule/price", "agent": "Agent decision", "state": "Changes during run", "setting": "Benchmark setting"}
VIS = {"visible": "agent sees", "public_or_forecast": "public/forecast", "hidden": "hidden"}
IMP = {"high": "High", "medium": "Med", "low": "Low"}


def load_result(p):
    r = json.load(open(p))
    return r.get("result", r)


def collect(paths):
    domains, variables = [], []
    for p in paths:
        for item in load_result(p).get("research", []):
            v = item["verify"] or {}
            vars_ = v.get("variables") or item["research"]["variables"]
            domains.append({"key": item["key"], "file": item["research"]["file"], "summary": item["research"]["summary"],
                            "n_research": len(item["research"]["variables"]), "n_verified": len(vars_),
                            "verify": {k: v.get(k) for k in ["checked", "verified", "corrected", "uncertain", "removed"]},
                            "key_corrections": v.get("key_corrections", []),
                            "interactions": item["research"]["interactions"], "data_sources": item["research"]["data_sources"],
                            "open_questions": item["research"]["open_questions"]})
            for x in vars_:
                x = dict(x)
                x["domain"] = item["key"]
                variables.append(x)
    domains.sort(key=lambda d: d["key"])
    ids = Counter(v["id"] for v in variables)
    dup = [i for i, n in ids.items() if n > 1]
    for v in variables:  # make ids unique if a domain reused one
        if v["id"] in dup:
            v["id"] = f'{v["domain"]}:{v["id"]}'
    os.makedirs(DIR, exist_ok=True)
    json.dump({"domains": domains, "variables": variables}, open(FULL, "w"), indent=1)
    L = ["# All variables so far (compact)", "", f"{len(variables)} variables from {len(domains)} domains. Columns: id | domain | sub-box | name | impact | role | component.", ""]
    for d in domains:
        L.append(f"## {d['key']}")
        for v in [v for v in variables if v["domain"] == d["key"]]:
            L.append(f"- {v['id']} | {v['sub_box']} | {v['name']} | {v['impact']} | {v['role']} | {v['component']}")
        L.append("")
    open(COMPACT, "w").write("\n".join(L))
    print(len(variables), "variables;", [(d["key"], d["n_research"], d["n_verified"], d["verify"]) for d in domains])


def esc(s):
    return str(s or "").replace("\n", " ").strip()


def render(finish_path):
    data = json.load(open(FULL))
    fin = load_result(finish_path)
    merge = fin["merge"]
    allv = {v["id"]: v for v in data["variables"]}
    for v in fin["gap_vars"]:
        v = dict(v)
        v["domain"] = "gap"
        allv[v["id"]] = v
    norm = lambda s: " ".join(str(s or "").lower().split())
    groups = {(norm(g["domain"]), norm(g["sub_box"])): g for g in merge.get("group_assignments", [])}
    assign = {}
    for i, v in allv.items():
        g = groups.get((norm(v.get("domain")), norm(v.get("sub_box"))))
        if g is None and v.get("domain") == "gap":
            g = groups.get(("gap", norm(v.get("sub_box"))))
        if g:
            assign[i] = {"box": g["box"], "sub_box": g["new_sub_box"]}
    for o in merge.get("overrides", []):
        if o["id"] in allv:
            assign[o["id"]] = {"box": o["box"], "sub_box": o["sub_box"]}
    unassigned = [i for i in allv if i not in assign]
    dups = {d["id"]: d["duplicate_of"] for d in merge.get("duplicates", [])
            if d["id"] in allv and d.get("duplicate_of") in allv and d["duplicate_of"] != d["id"]}
    # never drop both ends of a duplicate chain
    for i in list(dups):
        if dups.get(dups[i]) == i:
            del dups[i]
    kept = [i for i in allv if i not in dups]
    top = {t["id"]: (n + 1, t["reason"]) for n, t in enumerate(merge["top30"])}
    core = set(merge["core_mvp"])
    box_order = [b["box"] for b in merge["boxes"]]
    sub_order = {b["box"]: b["sub_boxes"] for b in merge["boxes"]}
    intro = {b["box"]: b["intro"] for b in merge["boxes"]}
    grouped = defaultdict(lambda: defaultdict(list))
    for i in kept:
        a = assign.get(i)
        box = a["box"] if a else "Unsorted"
        sub = a["sub_box"] if a else allv[i].get("sub_box", "Other")
        grouped[box][sub].append(allv[i])
    for b in grouped:
        if b not in box_order:
            box_order.append(b)
    impact_rank = {"high": 0, "medium": 1, "low": 2}

    def line(v):
        tags = [IMP.get(v["impact"], v["impact"]), ROLE.get(v["role"], v["role"]), VIS.get(v["visibility"], v["visibility"])]
        if v["id"] in core:
            tags.append("core MVP")
        if v.get("applies_to") and v["applies_to"].lower() not in ("all",):
            tags.append(esc(v["applies_to"]))
        s = f"**{esc(v['name'])}**: {esc(v['description'])}"
        if v.get("values_or_range"):
            s += f" *Values:* {esc(v['values_or_range'])}."
        s += f" `{' · '.join(tags)}`"
        return s

    def details(v):
        return f"Evidence: {esc(v['impact_evidence'])} · Data: {esc(v['data_source'])} · Model: {esc(v['how_to_model'])} · [{v['id']}]"

    n_kept = len(kept)
    cnt_imp = Counter(allv[i]["impact"] for i in kept)
    cnt_role = Counter(allv[i]["role"] for i in kept)
    L = ["# RoboTaxi Bench: independent variables, in boxes", "",
         f"*Variable list for the simulator and harness, 19 Oct 2026. {n_kept} distinct variables in {len(box_order)} boxes "
         f"({cnt_imp['high']} high, {cnt_imp['medium']} medium and {cnt_imp['low']} low impact). Built by 12 domain researchers, each checked by a separate fact-checker, "
         f"then three gap critics (a veteran NYC driver, a simulation engineer, a robotaxi fleet operator), a gap-fill round with its own fact-check, and an editor who sorted everything into boxes. "
         f"Full dossiers with sources and fact-check logs: `research/research_notes/RoboTaxi Bench variables/`. Spreadsheet version: `research/reports/RoboTaxi Bench variables.csv`.*", "",
         "**How to read each item.** Bold name, one-line description and example values, then tags in this order:",
         "- **Impact** on profit per hour: High, Med or Low.",
         "- **Role:**",
         "  - *World input*: set by the scenario or replayed from data, such as weather or demand.",
         "  - *Rule/price*: fixed by the designer, such as fares, tolls and laws.",
         "  - *Agent decision*: what the model chooses.",
         "  - *Changes during run*: state such as battery level, fatigue or position.",
         "  - *Benchmark setting*: experiment knobs.",
         "- **Visibility:** whether the agent sees it, can get it from public information or forecasts, or whether it is hidden.",
         "- *core MVP* marks the first-version set.",
         "",
         "Under each item, the smaller line gives the evidence for the impact rating, the public data source and how to model it. Source tags: [P] primary source read directly, [P\\*] primary source via a copy, [S] snippet or secondary only, [U] unverified, [design] our judgement.", "",
         f"Roles: {cnt_role['world']} world inputs, {cnt_role['rule']} rules and prices, {cnt_role['agent']} agent decisions, {cnt_role['state']} run-time states, {cnt_role['setting']} benchmark settings.", ""]
    L += ["## The 30 biggest levers on earnings", "", "| # | Variable | Box | Why it matters |", "|---|---|---|---|"]
    for i, (n, reason) in sorted(top.items(), key=lambda x: x[1][0]):
        if i in allv:
            a = assign.get(i, {})
            L.append(f"| {n} | {esc(allv[i]['name'])} | {esc(a.get('box', ''))} | {esc(reason)} |")
    L += ["", "## Your items and where they live", ""]
    for u in merge["user_items"]:
        names = [esc(allv[i]["name"]) for i in u["ids"] if i in allv]
        L.append(f"- **{esc(u['item'])}**: {'; '.join(names) if names else 'not found'}")
    L += ["", "## The boxes", ""]
    for bi, b in enumerate(box_order, 1):
        if b not in grouped:
            continue
        nb = sum(len(x) for x in grouped[b].values())
        L.append(f"### {bi}. {b} ({nb})")
        if intro.get(b):
            L.append(f"*{esc(intro[b])}*")
        L.append("")
        subs = [s for s in sub_order.get(b, []) if s in grouped[b]] + [s for s in grouped[b] if s not in sub_order.get(b, [])]
        for s in subs:
            L.append(f"* **{s}**")
            for v in sorted(grouped[b][s], key=lambda v: (impact_rank.get(v["impact"], 3), v["name"])):
                L.append(f"   * {line(v)}")
                L.append(f"      * <sub>{details(v)}</sub>")
        L.append("")
    srcs, seen = [], set()
    for d in data["domains"]:
        for s in d["data_sources"]:
            k = s["name"].lower()
            if k not in seen:
                seen.add(k)
                srcs.append(s)
    L += ["## Public data sources named by the researchers", "", "| Source | What it gives | Access | URL |", "|---|---|---|---|"]
    for s in srcs:
        L.append(f"| {esc(s['name'])} | {esc(s['what'])} | {esc(s['access'])} | {esc(s['url'])} |")
    L += ["", "## Still missing or open", ""] + [f"- {esc(x)}" for x in merge["still_missing"]]
    L += ["", "## Fact-check summary", "", "| Domain | Research items | After check | Claims checked | Corrected | Uncertain | Removed |", "|---|---|---|---|---|---|---|"]
    for d in data["domains"]:
        vv = d["verify"]
        L.append(f"| {d['key']} | {d['n_research']} | {d['n_verified']} | {vv['checked']} | {vv['corrected']} | {vv['uncertain']} | {vv['removed']} |")
    for f in fin["fills"]:
        vc = f["verify_counts"]
        L.append(f"| gap fill | - | - | {vc['checked']} | {vc['corrected']} | - | {vc['removed']} |")
    L += ["", f"Merged as duplicates: {len(dups)}. Not assigned by the editor (kept under 'Unsorted'): {len(unassigned)}.", ""]
    open(OUT_MD, "w").write("\n".join(L))
    # short list (paste-ready, user's nested-bullet style) and a compact chat version
    S = ["# RoboTaxi Bench: independent variables (short list)", "",
         f"*{n_kept} variables in {len(box_order)} boxes, 19 Oct 2026. (H/M/L) = impact on profit per hour; ★ = core first-version set. "
         "Full details, evidence and data sources: `research/reports/RoboTaxi Bench variables.md` and the `.csv` next to it.*", "",
         "* Independent variables list for robotaxi-bench simulation (in boxes)"]
    C = []
    for bi, b in enumerate(box_order, 1):
        if b not in grouped:
            continue
        nb = sum(len(x) for x in grouped[b].values())
        S.append(f"   * **{b}** ({nb})")
        C.append(f"**{bi}. {b}** ({nb})")
        subs = [s for s in sub_order.get(b, []) if s in grouped[b]] + [s for s in grouped[b] if s not in sub_order.get(b, [])]
        for s in subs:
            vs = sorted(grouped[b][s], key=lambda v: (impact_rank.get(v["impact"], 3), v["name"]))
            S.append(f"      * {s}")
            items = []
            for v in vs:
                tag = IMP.get(v["impact"], "?")[0] + (" ★" if v["id"] in core else "")
                S.append(f"         * {esc(v['name'])} ({tag})")
                items.append(f"{esc(v['name'])} ({tag})")
            C.append(f"- *{s}*: " + "; ".join(items))
        C.append("")
    open(OUT_SHORT, "w").write("\n".join(S) + "\n")
    open(CHAT, "w").write("\n".join(C) + "\n")
    cols = ["id", "box", "sub_box", "name", "description", "values_or_range", "impact", "impact_evidence", "role", "visibility", "applies_to",
            "data_source", "how_to_model", "component", "priority", "core_mvp", "top30_rank", "domain"]
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for b in box_order:
            for s, vs in grouped.get(b, {}).items():
                for v in vs:
                    w.writerow([v["id"], b, s, v["name"], v["description"], v.get("values_or_range", ""), v["impact"], v["impact_evidence"], v["role"],
                                v["visibility"], v.get("applies_to", ""), v["data_source"], v["how_to_model"], v["component"], v["priority"],
                                "yes" if v["id"] in core else "", top.get(v["id"], ("",))[0], v.get("domain", "")])
    print(f"kept {n_kept}, dups {len(dups)}, unassigned {len(unassigned)}, boxes {len(box_order)}; {OUT_MD}")


if __name__ == "__main__":
    {"collect": lambda: collect(sys.argv[2:]), "render": lambda: render(sys.argv[2])}[sys.argv[1]]()
