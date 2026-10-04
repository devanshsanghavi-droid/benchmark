"""DEBRIEF reference implementation (v0.1): parcel-tariff family.

A DEBRIEF item is a novel, programmatically generated rule system (here: a courier tariff),
a practice set and a hidden fresh set of cases. A fixed "junior" model attempts the practice
cases; the model under test reads the spec, the junior's attempts and the key, and writes one
note of at most B words; the junior then answers the fresh cases with spec + note. The headline
is the Net Fix Rate (NFR): the share of the junior's control errors on fresh cases removed by
the note, net of correct answers it breaks.

Everything that determines a score is computed here by code: the spec text (rendered from a
human-written phrase bank), the answer key (interpreter), the misconception labels (mutation
search), and the score. No LLM writes test content.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import re
from dataclasses import asdict, dataclass, field

# ---------------------------------------------------------------------------
# Rule system
# ---------------------------------------------------------------------------

ZONES = ["A", "B", "C"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Misconception library (= trap catalogue = mutation library). Each entry names the provision
# it misapplies; a misconception is only "live" if its provision is present in the system.
MISCONCEPTIONS = {
    "round_nearest": "rounding",       # rounds weights to nearest kg instead of up
    "no_vol": "vol",                   # ignores volumetric weight for parcels
    "vol_on_docs": "vol",              # over-generalises volumetric weight to documents
    "weekend_on_total": ("weekend", "remote"),  # applies weekend % after the remote fee (needs both)
    "no_gold_excl": "gold_excl",       # applies the GOLD discount in the excluded zone
    "no_cap": "doc_cap",               # ignores the document price cap
    "remote_any_position": "remote",   # matches remote prefixes anywhere in the postcode
    # L4-L5 (v0.2): counter-default provisions that interact
    "no_doc_reclass": "doc_reclass",   # keeps treating heavy documents as documents
    "discount_flat_fees": ("gold", "flat_undiscounted"),  # discounts the flat fees as well
    "no_tier": "tier",                 # charges every kg at the ordinary rate
    "tier_all_kg": "tier",             # once over the threshold, charges ALL further kg at the heavy rate
    "no_zone_div": "zone_div",         # uses the general divisor in the amended zone
    "oversize_once": "oversize",       # charges the oversize fee once even when 2+ sides are long
    "no_minimum": "minimum",           # ignores the minimum charge
}

# Misconceptions found AFTER pilot v1 by a coach (not by the authors). Used only for diagnosis, never for case
# sampling, so items generated from a seed stay identical. Promote to MISCONCEPTIONS at the next version bump.
POSTHOC_MISCONCEPTIONS = {
    "tier_outside_base": "tier",       # treats the heavy-kg uplift as a separate add-on: % surcharge and GOLD
                                       # discount computed on the ordinary base only (found by the Opus coach)
}

LEVEL_PROVISIONS = {
    1: ["rounding", "vol", "weekend"],
    2: ["rounding", "vol", "weekend", "remote", "gold", "gold_excl"],
    3: ["rounding", "vol", "weekend", "remote", "gold", "gold_excl", "doc_cap"],
    4: ["rounding", "vol", "weekend", "remote", "gold", "gold_excl", "doc_cap", "doc_reclass", "flat_undiscounted",
        "tier"],
    5: ["rounding", "vol", "weekend", "remote", "gold", "gold_excl", "doc_cap", "doc_reclass", "flat_undiscounted",
        "tier", "zone_div", "oversize", "minimum"],
}


@dataclass
class System:
    seed: int
    level: int
    name: str
    provisions: list
    first: dict
    per: dict
    divisor: int
    weekend_pct: int
    remote_prefixes: list
    remote_fee: int
    gold_pct: int
    excl_zone: str
    doc_cap: int
    reclass_kg: int = 2
    tier_kg: int = 8
    tier_add: int = 60
    zone_div_zone: str = "C"
    zone_divisor: int = 3000
    oversize_cm: int = 60
    oversize_fee: int = 300
    minimum: int = 700


@dataclass
class Case:
    cid: str
    zone: str
    weight: float  # kg, one decimal
    dims: tuple  # cm
    kind: str  # PARCEL | DOCUMENT
    day: str
    postcode: str
    account: str  # STANDARD | GOLD

    def render(self) -> str:
        l, w, h = self.dims
        return (f"{self.cid}: Zone {self.zone}, {self.weight} kg, {l}x{w}x{h} cm, {self.kind}, "
                f"collected {self.day}, postcode {self.postcode}, {self.account} account")


def make_system(seed: int, level: int) -> System:
    r = random.Random(seed)
    firsts = sorted(r.sample(range(300, 1000, 10), 3))
    pers = sorted(r.sample(range(100, 300, 10), 3))
    letters = "ABDEFGHJKLMNPRSTUWXYZ"
    prefixes = ["".join(r.sample(letters, 2)) for _ in range(2)]
    name = r.choice(["Northvale", "Brightwater", "Kestrel", "Halden", "Marlow", "Ostrey", "Tamsin", "Wexcombe"])
    name += " " + r.choice(["Couriers", "Parcel Co.", "Freight", "Express", "Post"])
    sysobj = System(
        seed=seed, level=level, name=name, provisions=list(LEVEL_PROVISIONS[level]),
        first=dict(zip(ZONES, firsts)), per=dict(zip(ZONES, pers)),
        divisor=r.choice([4000, 5000, 6000]), weekend_pct=r.choice([10, 15, 20, 25]),
        remote_prefixes=prefixes, remote_fee=r.choice(range(200, 500, 50)),
        gold_pct=r.choice([5, 10, 15]), excl_zone=r.choice(ZONES), doc_cap=r.choice(range(600, 1300, 100)),
        # v0.2 parameters; drawn from a separate stream so L1-L3 systems are unchanged
        **_v02_params(seed),
    )
    sysobj.minimum = sysobj.first["A"] + sysobj.minimum  # binds on light, discounted Zone A consignments
    return sysobj


def _v02_params(seed: int) -> dict:
    r = random.Random(seed * 101 + 7)
    return dict(reclass_kg=r.choice([1, 2, 3]), tier_kg=r.choice([5, 6, 8, 10]), tier_add=r.choice(range(40, 160, 20)),
                zone_div_zone=r.choice(ZONES), zone_divisor=r.choice([2500, 3000, 3500]),
                oversize_cm=r.choice([40, 45, 50]), oversize_fee=r.choice(range(150, 450, 50)),
                minimum=r.choice([60, 100, 150]))  # offset above Zone A's first-kg price; set in make_system


def live_misconceptions(sys: System) -> list:
    return [m for m, prov in MISCONCEPTIONS.items() if all(p in sys.provisions for p in _provs(prov))]


def _provs(prov) -> tuple:
    return prov if isinstance(prov, tuple) else (prov,)


def _round_kg(x: float, nearest: bool) -> int:
    v = math.floor(x + 0.5) if nearest else math.ceil(x - 1e-9)
    return max(1, int(v))


def price(sys: System, c: Case, mis: frozenset = frozenset()) -> int:
    """Exact interpreter. `mis` applies misconceptions (used to simulate and diagnose errors)."""
    P = sys.provisions
    nearest = "round_nearest" in mis
    w = _round_kg(c.weight, nearest)
    kind = c.kind
    if "doc_reclass" in P and kind == "DOCUMENT" and w > sys.reclass_kg and "no_doc_reclass" not in mis:
        kind = "PARCEL"  # a heavy document is treated as a parcel for all purposes
    if "vol" in P:
        use_vol = (kind == "PARCEL" and "no_vol" not in mis) or (kind == "DOCUMENT" and "vol_on_docs" in mis)
        if use_vol:
            l, wd, h = c.dims
            div = sys.divisor
            if "zone_div" in P and c.zone == sys.zone_div_zone and "no_zone_div" not in mis:
                div = sys.zone_divisor
            w = max(w, _round_kg(l * wd * h / div, nearest))
    first, per = sys.first[c.zone], sys.per[c.zone]
    uplift = 0
    if "tier" in P and w > sys.tier_kg and "no_tier" not in mis and "tier_outside_base" in mis:
        base = first + (w - 1) * per
        uplift = (w - sys.tier_kg) * sys.tier_add
    elif "tier" in P and w > sys.tier_kg and "no_tier" not in mis:
        if "tier_all_kg" in mis:
            base = first + (w - 1) * (per + sys.tier_add)
        else:
            base = first + (sys.tier_kg - 1) * per + (w - sys.tier_kg) * (per + sys.tier_add)
    else:
        base = first + (w - 1) * per
    remote = 0
    if "remote" in P:
        pc = c.postcode.upper()
        hit = any(p in pc for p in sys.remote_prefixes) if "remote_any_position" in mis else any(pc.startswith(p) for p in sys.remote_prefixes)
        remote = sys.remote_fee if hit else 0
    oversize = 0
    if "oversize" in P and kind == "PARCEL":
        n_long = sum(d > sys.oversize_cm for d in c.dims)
        if n_long:
            oversize = sys.oversize_fee * (2 if n_long >= 2 and "oversize_once" not in mis else 1)
    flat = remote + oversize + uplift
    weekend = "weekend" in P and c.day in ("Sat", "Sun")
    if weekend and "weekend_on_total" in mis:
        pct_part = (base + flat) * sys.weekend_pct // 100
    else:
        pct_part = base * sys.weekend_pct // 100 if weekend else 0
    discountable, total = base + pct_part, base + pct_part + flat
    if "gold" in P and c.account == "GOLD":
        excluded = "gold_excl" in P and c.zone == sys.excl_zone and "no_gold_excl" not in mis
        if not excluded:
            if "flat_undiscounted" in P and "discount_flat_fees" not in mis:
                total -= discountable * sys.gold_pct // 100
            else:
                total -= total * sys.gold_pct // 100
    if "doc_cap" in P and kind == "DOCUMENT" and "no_cap" not in mis:
        total = min(total, sys.doc_cap)
    if "minimum" in P and "no_minimum" not in mis:
        total = max(total, sys.minimum)
    return int(total)


# ---------------------------------------------------------------------------
# Spec rendering (human-written phrase bank; distractor sections included)
# ---------------------------------------------------------------------------

PHRASES = {
    "rounding": ["All weights are rounded UP to the next whole kilogram (minimum 1 kg) before any comparison or charge.",
                 "Weights are always rounded upward to a whole kilogram, never to the nearest; the minimum is 1 kg."],
    "vol": ["For a PARCEL, the chargeable weight is the greater of its actual weight and its volumetric weight, where volumetric weight = length x width x height in cm / {divisor}. Each is rounded up separately before the two are compared. A DOCUMENT is always charged on its actual weight only.",
            "PARCELS are charged on whichever is larger: actual weight, or volumetric weight (L x W x H in cm divided by {divisor}), each rounded up first. DOCUMENTS are never charged on volumetric weight."],
    "weekend": ["Collections on Saturday or Sunday attract a surcharge of {weekend_pct}% of the base price only (rounded down to a whole cent).",
                "A weekend collection (Sat/Sun) adds {weekend_pct}% of the base price, rounded down; the percentage is never applied to other surcharges."],
    "remote": ["Postcodes that BEGIN with {prefixes} are remote: add a flat {remote_fee} cents after any percentage surcharge.",
               "A flat remote-area fee of {remote_fee} cents applies when the postcode starts with {prefixes}; it is added after percentage surcharges."],
    "gold": ["GOLD accounts receive {gold_pct}% off the total after all surcharges (rounded down to a whole cent)."],
    "gold_excl": ["The GOLD discount is not available on Zone {excl_zone} consignments.",
                  "Zone {excl_zone} consignments are excluded from the GOLD discount."],
    "doc_cap": ["A DOCUMENT never costs more than {doc_cap} cents in total, after all surcharges and discounts.",
                "The final price of any DOCUMENT is capped at {doc_cap} cents."],
}
PHRASES_V02 = {
    "doc_reclass": ["A DOCUMENT whose rounded actual weight exceeds {reclass_kg} kg is treated as a PARCEL for all purposes in this tariff.",
                    "Any DOCUMENT weighing more than {reclass_kg} kg (after rounding) is reclassified as a PARCEL and priced as one in every section."],
    "flat_undiscounted": ["GOLD accounts receive {gold_pct}% off the base price plus any percentage surcharge (rounded down to a whole cent); flat fees are never discounted.",
                          "For GOLD accounts, {gold_pct}% (rounded down) is deducted from the base price and percentage surcharges only. Flat fees such as the remote-area or oversize fee are charged in full."],
    "tier": ["For each chargeable kg above {tier_kg} kg, the per-kg rate is increased by {tier_add} cents. The first {tier_kg} kg are charged at the ordinary rates.",
             "Each chargeable kilogram beyond the {tier_kg}th costs {tier_add} cents more than the zone's ordinary per-kg rate; kilograms up to and including the {tier_kg}th are unaffected."],
    "zone_div": ["(a) For Zone {zone_div_zone} consignments only, the volumetric divisor is {zone_divisor} instead of the divisor stated in the chargeable-weight section."],
    "oversize": ["(b) A PARCEL with any one side longer than {oversize_cm} cm pays a flat oversize fee of {oversize_fee} cents; if two or more sides are longer than {oversize_cm} cm, the fee is doubled."],
    "minimum": ["(c) No consignment is charged less than {minimum} cents in total, after all other sections (including any cap)."],
}
SECTION_TITLES = {"rounding": "Weight.", "vol": "Chargeable weight.", "weekend": "Surcharges.", "remote": "Surcharges.",
                  "gold": "Discounts.", "gold_excl": "Discounts.", "flat_undiscounted": "Discounts.", "doc_cap": "Cap.",
                  "doc_reclass": "Reclassification.", "tier": "Heavy items.", "zone_div": "Amendments",
                  "oversize": "Amendments", "minimum": "Amendments"}

DISTRACTORS = [
    "Claims. Loss or damage must be reported within 14 days of the delivery date with photographs of the packaging.",
    "Delivery times. Zone A: next working day. Zone B: two working days. Zone C: three to five working days.",
    "Prohibited items. Lithium batteries, aerosols and perishable goods are not accepted for carriage.",
    "Definitions. 'Consignment' means one item collected from one address. 'Working day' excludes public holidays.",
    "Tracking. Every consignment receives a tracking reference by email on the day of collection.",
]


def render_spec(sys: System) -> str:
    r = random.Random(sys.seed * 7 + 1)
    fmt = dict(divisor=sys.divisor, weekend_pct=sys.weekend_pct, remote_fee=sys.remote_fee,
               prefixes=" or ".join(sys.remote_prefixes), gold_pct=sys.gold_pct, excl_zone=sys.excl_zone,
               doc_cap=sys.doc_cap, reclass_kg=sys.reclass_kg, tier_kg=sys.tier_kg, tier_add=sys.tier_add,
               zone_div_zone=sys.zone_div_zone, zone_divisor=sys.zone_divisor, oversize_cm=sys.oversize_cm,
               oversize_fee=sys.oversize_fee, minimum=sys.minimum)
    P = sys.provisions
    pick = lambda k: r.choice((PHRASES_V02 if k in PHRASES_V02 else PHRASES)[k]).format(**fmt)
    lines = [f"{sys.name.upper()}: DOMESTIC TARIFF (edition {sys.seed % 9 + 2})", "",
             "All prices are in cents. Apply the sections in order."]
    sec = 1
    distract = r.sample(DISTRACTORS, 3)
    lines.append(f"\n§{sec} {distract[0]}"); sec += 1
    lines.append(f"\n§{sec} Weight. " + pick("rounding")); sec += 1
    if "doc_reclass" in P:
        lines.append(f"\n§{sec} Reclassification. " + pick("doc_reclass")); sec += 1
    if "vol" in P:
        lines.append(f"\n§{sec} Chargeable weight. " + pick("vol")); sec += 1
    base = "; ".join(f"Zone {z}: {sys.first[z]} for the first kg, then {sys.per[z]} per further kg" for z in ZONES)
    lines.append(f"\n§{sec} Base price. {base}."); sec += 1
    if "tier" in P:
        lines.append(f"\n§{sec} Heavy items. " + pick("tier")); sec += 1
    lines.append(f"\n§{sec} {distract[1]}"); sec += 1
    surch = [pick(k) for k in ("weekend", "remote") if k in P]
    if surch:
        lines.append(f"\n§{sec} Surcharges. " + " ".join(surch)); sec += 1
    gold_key = "flat_undiscounted" if "flat_undiscounted" in P else "gold"
    disc = [pick(k) for k in (gold_key, "gold_excl") if k in P or (k == gold_key and "gold" in P)]
    if disc:
        lines.append(f"\n§{sec} Discounts. " + " ".join(disc)); sec += 1
    if "doc_cap" in P:
        lines.append(f"\n§{sec} Cap. " + pick("doc_cap")); sec += 1
    lines.append(f"\n§{sec} {distract[2]}"); sec += 1
    amend = [pick(k) for k in ("zone_div", "oversize", "minimum") if k in P]
    if amend:
        lines.append(f"\n§{sec} Amendments to this edition (these override any earlier section). " + " ".join(amend))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Case sampling with coverage constraints
# ---------------------------------------------------------------------------

def random_case(r: random.Random, sys: System, cid: str) -> Case:
    kind = "DOCUMENT" if r.random() < 0.3 else "PARCEL"
    if kind == "DOCUMENT":
        dims = (r.choice([30, 35, 40, 45]), r.choice([25, 30, 35]), r.choice([3, 5, 8, 12]))
        weight = round(r.uniform(0.1, 4.0), 1)
    else:
        dims = (r.randrange(10, 90, 5), r.randrange(10, 70, 5), r.randrange(5, 60, 5))
        weight = round(r.uniform(0.2, 12.0), 1)
    if r.random() < 0.35 and "remote" in sys.provisions:
        p = r.choice(sys.remote_prefixes)
        postcode = p + str(r.randint(1, 9))
    elif r.random() < 0.15 and "remote" in sys.provisions:
        p = r.choice(sys.remote_prefixes)
        postcode = "Q" + p + str(r.randint(1, 9))  # contains, but does not begin with, a prefix
    else:
        postcode = "".join(r.sample("ABDEFGHJLMNPRSTUW", 2)) + str(r.randint(1, 9))
    return Case(cid, r.choice(ZONES), weight, dims, kind, r.choice(DAYS), postcode,
                "GOLD" if r.random() < 0.4 else "STANDARD")


def sensitive(sys: System, c: Case, m: str) -> bool:
    return price(sys, c, frozenset([m])) != price(sys, c)


def sample_cases(sys: System, n: int, prefix: str, r: random.Random, min_cover: int, guards: int = 0) -> list:
    """Coverage-first sampling: every live misconception changes >= min_cover answers, and at least
    `guards` exception-guard cases (documents that 'vol_on_docs' would break) are included; the rest
    of the set is filled with unconstrained random cases, then shuffled and relabelled."""
    need = {m: min_cover for m in live_misconceptions(sys)}
    if "vol_on_docs" in need:
        need["vol_on_docs"] = max(need["vol_on_docs"], guards)
    need0 = dict(need)
    chosen = []
    if sys.level >= 4:  # v0.2: best-of-N greedy cover (many interacting traps need efficient covering)
        for _ in range(n):
            if all(v <= 0 for v in need.values()):
                break
            cands = [random_case(r, sys, "tmp") for _ in range(400)]
            sens = [{m for m, v in need.items() if v > 0 and sensitive(sys, c, m)} for c in cands]
            freq = {m: sum(m in s_ for s_ in sens) for m in need}
            # rarity-weighted greedy: traps that few random cases expose are covered first
            scores = [sum(1.0 / (1 + freq[m]) for m in s_) for s_ in sens]
            best = cands[max(range(len(cands)), key=scores.__getitem__)]
            chosen.append(best)
            for m in need:
                if sensitive(sys, best, m):
                    need[m] -= 1
    for _ in range(0 if sys.level >= 4 else 20000):
        if all(v <= 0 for v in need.values()):
            break
        if len(chosen) >= n:  # restart: greedy set grew too large
            chosen, need = [], dict(need0)
        c = random_case(r, sys, "tmp")
        hits = [m for m, v in need.items() if v > 0 and sensitive(sys, c, m)]
        if hits:
            chosen.append(c)
            for m in need:
                if sensitive(sys, c, m):
                    need[m] -= 1
    if any(v > 0 for v in need.values()):
        raise RuntimeError(f"coverage constraints unsatisfiable: {need}")
    while len(chosen) < n:
        chosen.append(random_case(r, sys, "tmp"))
    r.shuffle(chosen)
    for i, c in enumerate(chosen):
        c.cid = f"{prefix}{i+1}"
    return chosen


@dataclass
class Item:
    system: System
    spec: str
    practice: list
    fresh: list
    practice_key: dict = field(default_factory=dict)
    fresh_key: dict = field(default_factory=dict)

    def to_json(self) -> str:
        d = {"system": asdict(self.system), "spec": self.spec,
             "practice": [asdict(c) for c in self.practice], "fresh": [asdict(c) for c in self.fresh],
             "practice_key": self.practice_key, "fresh_key": self.fresh_key}
        return json.dumps(d, indent=1)


LEVEL_SIZES = {4: (10, 14), 5: (12, 16)}  # (practice, fresh); L1-L3 use 8 / 12


def make_item(seed: int, level: int, n_practice: int | None = None, n_fresh: int | None = None) -> Item:
    dp, df = LEVEL_SIZES.get(level, (8, 12))
    n_practice, n_fresh = n_practice or dp, n_fresh or df
    sys = make_system(seed, level)
    for attempt in range(1 if level < 4 else 25):  # v0.2: deterministic retries for heavily constrained levels
        r = random.Random(seed * 31 + level + 1000 * attempt)
        try:
            practice = sample_cases(sys, n_practice, "P", r, min_cover=1)
            fresh = sample_cases(sys, n_fresh, "F", r, min_cover=2, guards=2)
            break
        except RuntimeError:
            if level < 4 or attempt == 24:
                raise
    return Item(sys, render_spec(sys), practice, fresh,
                {c.cid: price(sys, c) for c in practice}, {c.cid: price(sys, c) for c in fresh})


# ---------------------------------------------------------------------------
# Diagnosis by mutation search, and the template-coach baseline
# ---------------------------------------------------------------------------

def diagnose(item: Item, answers: dict, max_size: int = 3, posthoc: bool = False):
    """Smallest misconception set reproducing the most practice answers. Returns (set, n_explained,
    per-case labels) where unexplained wrong answers are labelled 'slip'. posthoc=True also searches
    POSTHOC_MISCONCEPTIONS."""
    sys = item.system
    live = live_misconceptions(sys)
    if posthoc:
        live += [m for m, prov in POSTHOC_MISCONCEPTIONS.items() if all(p in sys.provisions for p in _provs(prov))]
    best = (frozenset(), -1)
    for k in range(0, max_size + 1):
        for combo in itertools.combinations(live, k):
            s = frozenset(combo)
            n = sum(price(sys, c, s) == answers.get(c.cid) for c in item.practice)
            if n > best[1]:
                best = (s, n)
    s, n = best
    labels = {}
    for c in item.practice:
        a = answers.get(c.cid)
        if a == item.practice_key[c.cid]:
            labels[c.cid] = "correct"
        elif a == price(sys, c, s):
            labels[c.cid] = "diagnosable"
        else:
            labels[c.cid] = "slip"
    return s, n, labels


def template_coach_note(item: Item, answers: dict, budget: int = 150) -> str:
    """No-LLM diagnosis baseline: restate verbatim the provisions blamed by the mutation search."""
    s, _, _ = diagnose(item, answers)
    if not s:
        return truncate_words("Re-read every section of the tariff and apply each rule exactly as written.", budget)
    provs = sorted({p for m in s for p in _provs(MISCONCEPTIONS[m])})
    paras = [p for p in item.spec.split("\n") if p.strip()]
    keyw = SECTION_TITLES
    picked = []
    for pv in provs:
        for p in paras:
            if keyw[pv] in p and p not in picked:
                picked.append(p)
    return truncate_words("Re-read these rules carefully: " + " ".join(picked), budget)


PLACEBO_NOTE = ("Work through every rule in order. Re-read each surcharge, discount and exception before "
                "answering, and recompute your arithmetic.")


def truncate_words(text: str, budget: int) -> str:
    words = text.split()
    return " ".join(words[:budget])


# ---------------------------------------------------------------------------
# Prompts and parsing
# ---------------------------------------------------------------------------

NO_TOOLS = "Do not use any tools, code execution or browsing; answer from the text alone."


def junior_prompt(item: Item, cases: list, note: str | None) -> str:
    note_block = f"\n\nNOTE FROM A REVIEWER (may help you):\n<<<\n{note}\n>>>" if note is not None else ""
    lines = "\n".join(c.render() for c in cases)
    return (f"{NO_TOOLS}\n\nYou are pricing consignments under the tariff below.\n\nTARIFF:\n{item.spec}{note_block}\n\n"
            f"CASES:\n{lines}\n\nFor each case, think briefly, then end your reply with exactly one line per case in the "
            f"form `<case id>: <price in cents as an integer>` (e.g. `{cases[0].cid}: 1234`).")


def coach_prompt(item: Item, junior_answers: dict, budget: int = 150) -> str:
    log = "\n".join(f"{c.render()} | junior answered {junior_answers.get(c.cid, 'NO ANSWER')} | correct {item.practice_key[c.cid]}"
                    for c in item.practice)
    return (f"{NO_TOOLS}\n\nA junior assistant priced practice consignments under the tariff below. You will see the "
            f"tariff, each practice case, the junior's answer and the correct answer. Write ONE note of at most {budget} words "
            f"that will help the same junior price NEW consignments correctly (you will not see them). The junior will get "
            f"the tariff plus your note. Notes are truncated at {budget} words.\n\nTARIFF:\n{item.spec}\n\nPRACTICE LOG:\n{log}\n\n"
            f"Reply with the note only, between <note> and </note>.")


ANSWER_RE = re.compile(r"^\s*\**\s*([PF]\d+)\s*\**\s*[:=]\s*\**\s*(-?[\d,]+)", re.M)


def parse_answers(text: str) -> dict:
    out = {}
    for cid, val in ANSWER_RE.findall(text or ""):
        out[cid] = int(val.replace(",", ""))  # last occurrence wins
    return out


def parse_note(text: str, budget: int) -> str:
    m = re.search(r"<note>(.*?)</note>", text or "", re.S)
    return truncate_words((m.group(1) if m else (text or "")).strip(), budget)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def nfr(control: list, post: list) -> float:
    """control, post: per-item lists of per-case correctness in [0,1]. Returns NFR in %."""
    num = sum(p - c for ci, pi in zip(control, post) for c, p in zip(ci, pi))
    den = sum(1 - c for ci in control for c in ci)
    return 100.0 * num / den if den else float("nan")


def nfr_ci(control: list, post: list, B: int = 2000, seed: int = 0):
    """Cluster bootstrap over items."""
    r = random.Random(seed)
    n = len(control)
    vals = []
    for _ in range(B):
        idx = [r.randrange(n) for _ in range(n)]
        v = nfr([control[i] for i in idx], [post[i] for i in idx])
        if not math.isnan(v):
            vals.append(v)
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]
