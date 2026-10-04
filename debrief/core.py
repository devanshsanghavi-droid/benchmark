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
}

LEVEL_PROVISIONS = {
    1: ["rounding", "vol", "weekend"],
    2: ["rounding", "vol", "weekend", "remote", "gold", "gold_excl"],
    3: ["rounding", "vol", "weekend", "remote", "gold", "gold_excl", "doc_cap"],
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
    return System(
        seed=seed, level=level, name=name, provisions=list(LEVEL_PROVISIONS[level]),
        first=dict(zip(ZONES, firsts)), per=dict(zip(ZONES, pers)),
        divisor=r.choice([4000, 5000, 6000]), weekend_pct=r.choice([10, 15, 20, 25]),
        remote_prefixes=prefixes, remote_fee=r.choice(range(200, 500, 50)),
        gold_pct=r.choice([5, 10, 15]), excl_zone=r.choice(ZONES), doc_cap=r.choice(range(600, 1300, 100)),
    )


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
    if "vol" in P:
        use_vol = (c.kind == "PARCEL" and "no_vol" not in mis) or (c.kind == "DOCUMENT" and "vol_on_docs" in mis)
        if use_vol:
            l, wd, h = c.dims
            w = max(w, _round_kg(l * wd * h / sys.divisor, nearest))
    base = sys.first[c.zone] + (w - 1) * sys.per[c.zone]
    remote = 0
    if "remote" in P:
        pc = c.postcode.upper()
        hit = any(p in pc for p in sys.remote_prefixes) if "remote_any_position" in mis else any(pc.startswith(p) for p in sys.remote_prefixes)
        remote = sys.remote_fee if hit else 0
    weekend = "weekend" in P and c.day in ("Sat", "Sun")
    if weekend and "weekend_on_total" in mis:
        total = base + remote
        total += total * sys.weekend_pct // 100
    else:
        total = base + (base * sys.weekend_pct // 100 if weekend else 0) + remote
    if "gold" in P and c.account == "GOLD":
        excluded = "gold_excl" in P and c.zone == sys.excl_zone and "no_gold_excl" not in mis
        if not excluded:
            total -= total * sys.gold_pct // 100
    if "doc_cap" in P and c.kind == "DOCUMENT" and "no_cap" not in mis:
        total = min(total, sys.doc_cap)
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
               doc_cap=sys.doc_cap)
    lines = [f"{sys.name.upper()}: DOMESTIC TARIFF (edition {sys.seed % 9 + 2})", "",
             "All prices are in cents. Apply the sections in order."]
    sec = 1
    distract = r.sample(DISTRACTORS, 3)
    lines.append(f"\n§{sec} {distract[0]}"); sec += 1
    lines.append(f"\n§{sec} Weight. " + r.choice(PHRASES["rounding"]).format(**fmt)); sec += 1
    if "vol" in sys.provisions:
        lines.append(f"\n§{sec} Chargeable weight. " + r.choice(PHRASES["vol"]).format(**fmt)); sec += 1
    base = "; ".join(f"Zone {z}: {sys.first[z]} for the first kg, then {sys.per[z]} per further kg" for z in ZONES)
    lines.append(f"\n§{sec} Base price. {base}."); sec += 1
    lines.append(f"\n§{sec} {distract[1]}"); sec += 1
    surch = [r.choice(PHRASES[p]).format(**fmt) for p in ("weekend", "remote") if p in sys.provisions]
    if surch:
        lines.append(f"\n§{sec} Surcharges. " + " ".join(surch)); sec += 1
    disc = [r.choice(PHRASES[p]).format(**fmt) for p in ("gold", "gold_excl") if p in sys.provisions]
    if disc:
        lines.append(f"\n§{sec} Discounts. " + " ".join(disc)); sec += 1
    if "doc_cap" in sys.provisions:
        lines.append(f"\n§{sec} Cap. " + r.choice(PHRASES["doc_cap"]).format(**fmt)); sec += 1
    lines.append(f"\n§{sec} {distract[2]}")
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
    for _ in range(20000):
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


def make_item(seed: int, level: int, n_practice: int = 8, n_fresh: int = 12) -> Item:
    sys = make_system(seed, level)
    r = random.Random(seed * 31 + level)
    practice = sample_cases(sys, n_practice, "P", r, min_cover=1)
    fresh = sample_cases(sys, n_fresh, "F", r, min_cover=2, guards=2)
    return Item(sys, render_spec(sys), practice, fresh,
                {c.cid: price(sys, c) for c in practice}, {c.cid: price(sys, c) for c in fresh})


# ---------------------------------------------------------------------------
# Diagnosis by mutation search, and the template-coach baseline
# ---------------------------------------------------------------------------

def diagnose(item: Item, answers: dict, max_size: int = 3):
    """Smallest misconception set reproducing the most practice answers. Returns (set, n_explained,
    per-case labels) where unexplained wrong answers are labelled 'slip'."""
    sys = item.system
    live = live_misconceptions(sys)
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
    keyw = {"rounding": "Weight.", "vol": "Chargeable weight.", "weekend": "Surcharges.", "remote": "Surcharges.",
            "gold": "Discounts.", "gold_excl": "Discounts.", "doc_cap": "Cap."}
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
