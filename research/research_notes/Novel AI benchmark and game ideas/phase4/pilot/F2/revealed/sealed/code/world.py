"""F2 Hidden-Rule Lab pilot -- block world: scene generation, mutation, rendering.

A scene is a side view of up to 4 stacks standing on the ground in 4 fixed slots.
Each stack holds 1-3 objects (bottom -> top). Physics constraint ("settled" world):
only squares can support another object, so circles/triangles only appear on top.
Object = (shape, colour, size).
"""
import random
from PIL import Image, ImageDraw, ImageFont

SHAPES = ["square", "circle", "triangle"]
COLOURS = ["red", "blue", "green", "yellow"]
SIZES = ["small", "large"]
NSLOTS = 4
MAXH = 3

RGB = {"red": (214, 45, 38), "blue": (40, 96, 214), "green": (34, 160, 64), "yellow": (246, 206, 24)}
OUTLINE = (35, 35, 35)
BG = (250, 250, 247)
GROUND = (110, 84, 60)

PW, PH = 200, 150          # panel drawing area (px, final resolution)
GROUND_Y = 138
SLOT_X = [28, 76, 124, 172]
SIDE = {"small": 22, "large": 38}
SS = 3                     # supersampling factor

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


# ---------------------------------------------------------------- scenes
def canon(scene):
    return tuple((st["slot"], tuple(tuple(o) for o in st["objs"])) for st in sorted(scene, key=lambda s: s["slot"]))


def valid_scene(scene):
    slots = [s["slot"] for s in scene]
    if len(scene) < 1 or len(set(slots)) != len(slots):
        return False
    for st in scene:
        if not (1 <= len(st["objs"]) <= MAXH) or not (0 <= st["slot"] < NSLOTS):
            return False
        for o in st["objs"][:-1]:
            if o[0] != "square":
                return False
    return True


def rand_obj(rng, top):
    shape = rng.choice(SHAPES) if top else "square"
    return [shape, rng.choice(COLOURS), rng.choice(SIZES)]


def random_scene(rng):
    n = rng.choices([1, 2, 3, 4], weights=[0.10, 0.30, 0.35, 0.25])[0]
    slots = sorted(rng.sample(range(NSLOTS), n))
    scene = []
    for s in slots:
        h = rng.choices([1, 2, 3], weights=[0.40, 0.35, 0.25])[0]
        objs = [rand_obj(rng, top=(i == h - 1)) for i in range(h)]
        scene.append({"slot": s, "objs": objs})
    return scene


def copy_scene(scene):
    return [{"slot": st["slot"], "objs": [list(o) for o in st["objs"]]} for st in scene]


def mutate(scene, rng, tries=20):
    """One small physically valid edit (a 'near miss' generator)."""
    for _ in range(tries):
        sc = copy_scene(scene)
        op = rng.choice(["recolour", "resize", "reshape", "remove", "add", "move", "swapcol", "newstack"])
        st = rng.choice(sc)
        if op == "recolour":
            o = rng.choice(st["objs"]); o[1] = rng.choice([c for c in COLOURS if c != o[1]])
        elif op == "resize":
            o = rng.choice(st["objs"]); o[2] = "large" if o[2] == "small" else "small"
        elif op == "reshape":
            o = st["objs"][-1]; o[0] = rng.choice([s for s in SHAPES if s != o[0]])
        elif op == "remove":
            if sum(len(s["objs"]) for s in sc) <= 1:
                continue
            st["objs"].pop()
            if not st["objs"]:
                sc.remove(st)
        elif op == "add":
            if len(st["objs"]) >= MAXH:
                continue
            if st["objs"][-1][0] != "square":
                if rng.random() < 0.5:
                    st["objs"][-1][0] = "square"
                else:
                    continue
            st["objs"].append(rand_obj(rng, top=True))
        elif op == "move":
            free = [s for s in range(NSLOTS) if s not in [x["slot"] for x in sc]]
            if not free:
                a, b = rng.sample(sc, 2) if len(sc) >= 2 else (None, None)
                if a is None:
                    continue
                a["slot"], b["slot"] = b["slot"], a["slot"]
            else:
                st["slot"] = rng.choice(free)
        elif op == "swapcol":
            objs = [o for s in sc for o in s["objs"]]
            if len(objs) < 2:
                continue
            a, b = rng.sample(objs, 2)
            if a[1] == b[1]:
                continue
            a[1], b[1] = b[1], a[1]
        elif op == "newstack":
            free = [s for s in range(NSLOTS) if s not in [x["slot"] for x in sc]]
            if not free:
                continue
            h = rng.choice([1, 2])
            sc.append({"slot": rng.choice(free), "objs": [rand_obj(rng, top=(i == h - 1)) for i in range(h)]})
        sc.sort(key=lambda s: s["slot"])
        if valid_scene(sc) and canon(sc) != canon(scene):
            return sc
    return None


# ---------------------------------------------------------------- rendering
def render_panel(scene):
    W, H = PW * SS, PH * SS
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, GROUND_Y * SS, W, H], fill=(236, 232, 224))
    d.line([0, GROUND_Y * SS, W, GROUND_Y * SS], fill=GROUND, width=3 * SS)
    lw = 2 * SS
    for st in scene:
        cx = SLOT_X[st["slot"]] * SS
        y = GROUND_Y * SS - (3 * SS) // 2
        for shape, col, size in st["objs"]:
            s = SIDE[size] * SS
            x0, x1, y0, y1 = cx - s // 2, cx + s // 2, y - s, y
            if shape == "square":
                d.rectangle([x0, y0, x1, y1], fill=RGB[col], outline=OUTLINE, width=lw)
            elif shape == "circle":
                d.ellipse([x0, y0, x1, y1], fill=RGB[col], outline=OUTLINE, width=lw)
            else:
                d.polygon([(x0, y1), (x1, y1), (cx, y0)], fill=RGB[col], outline=OUTLINE, width=lw)
            y = y0
    return im.resize((PW, PH), Image.LANCZOS)


def _font(bold, size):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


CAP = 26      # caption bar height
PAD = 14
BORDER = 2


def _panel_with_caption(scene, caption, style):
    """style: 'yes' | 'no' | 'test'"""
    w, h = PW + 2 * BORDER, PH + CAP + 2 * BORDER
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    bar = {"yes": (225, 225, 225), "no": (60, 60, 60), "test": (205, 205, 205)}[style]
    txt = {"yes": (0, 0, 0), "no": (255, 255, 255), "test": (0, 0, 0)}[style]
    d.rectangle([0, 0, w - 1, CAP + BORDER], fill=bar)
    f = _font(True, 15)
    tw = d.textlength(caption, font=f)
    d.text(((w - tw) / 2, 4), caption, fill=txt, font=f)
    im.paste(render_panel(scene), (BORDER, CAP + BORDER))
    d.rectangle([0, 0, w - 1, h - 1], outline=(0, 0, 0), width=BORDER)
    return im


def panel_boxes_examples():
    """Return list of (x, y) top-left of the drawing area for the 12 example panels
    (first 6 = FITS, last 6 = DOES NOT FIT) plus sheet size."""
    cols = 3
    cw, chh = PW + 2 * BORDER, PH + CAP + 2 * BORDER
    W = PAD + cols * (cw + PAD)
    TITLE, SEC = 44, 34
    boxes = []
    y = TITLE
    for sec in range(2):
        y += SEC
        for r in range(2):
            for c in range(cols):
                x = PAD + c * (cw + PAD)
                boxes.append((x, y + r * (chh + PAD)))
        y += 2 * (chh + PAD)
    return boxes, (W, y + 4)


def panel_boxes_tests():
    cols = 4
    cw, chh = PW + 2 * BORDER, PH + CAP + 2 * BORDER
    W = PAD + cols * (cw + PAD)
    TITLE = 64
    boxes = []
    for r in range(2):
        for c in range(cols):
            boxes.append((PAD + c * (cw + PAD), TITLE + r * (chh + PAD)))
    return boxes, (W, TITLE + 2 * (chh + PAD) + 4)


def render_examples_sheet(pid, fits, nots, path):
    boxes, (W, H) = panel_boxes_examples()
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((PAD, 10), f"Problem {pid} - EXAMPLES", fill=(0, 0, 0), font=_font(True, 22))
    ys = [boxes[0][1] - 30, boxes[6][1] - 30]
    d.text((PAD, ys[0]), "These 6 scenes FIT the hidden rule  (captions YES-1 ... YES-6)", fill=(0, 0, 0), font=_font(True, 16))
    d.text((PAD, ys[1]), "These 6 scenes DO NOT FIT the hidden rule  (captions NO-1 ... NO-6)", fill=(0, 0, 0), font=_font(True, 16))
    d.line([PAD, ys[1] - 8, W - PAD, ys[1] - 8], fill=(0, 0, 0), width=2)
    for i, sc in enumerate(fits):
        im.paste(_panel_with_caption(sc, f"YES-{i+1}  (fits)", "yes"), boxes[i])
    for i, sc in enumerate(nots):
        im.paste(_panel_with_caption(sc, f"NO-{i+1}  (does not fit)", "no"), boxes[6 + i])
    im.save(path, optimize=True)


def render_tests_sheet(pid, tests, path):
    boxes, (W, H) = panel_boxes_tests()
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((PAD, 8), f"Problem {pid} - TESTS (unlabeled)", fill=(0, 0, 0), font=_font(True, 22))
    d.text((PAD, 38), "Decide for each scene T1 ... T8 whether it fits the hidden rule of this problem.", fill=(0, 0, 0), font=_font(False, 15))
    for i, sc in enumerate(tests):
        im.paste(_panel_with_caption(sc, f"T{i+1}", "test"), boxes[i])
    im.save(path, optimize=True)


def panel_origin(box):
    """drawing-area origin inside a captioned panel placed at box"""
    return box[0] + BORDER, box[1] + CAP + BORDER


if __name__ == "__main__":
    rng = random.Random(1)
    scs = [random_scene(rng) for _ in range(20)]
    render_examples_sheet("PX", scs[:6], scs[6:12], "/tmp/claude-0/-home-user-benchmark/5fc33e21-6d61-5fb2-89f8-1da370892943/scratchpad/demo_ex.png")
    render_tests_sheet("PX", scs[12:20], "/tmp/claude-0/-home-user-benchmark/5fc33e21-6d61-5fb2-89f8-1da370892943/scratchpad/demo_te.png")
