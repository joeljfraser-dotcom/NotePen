"""Illustrations for the MyPowerfulNotes site, drawn as inline SVG in the app's own style.

They are illustrations of the app's screens (not screenshots): the layout, icons and colours follow the apps,
and the handwriting is drawn by ink.py so it reads as writing without being real words.
"""
import json
import math
import os

import ink

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, "icons.json")))

TEXT = "#1E242B"
TEXT2 = "#5C6670"
ACCENT = "#0E6E66"
SOFT = "#E3F1EF"
BAR = "#FAFAFA"
BORDER = "#E1E1E1"
DESK = "#ECECE8"
RULE = "#D6E1EC"
INK = "#1E242B"
BLUE_INK = "#1F4FBF"
RED = "#C62828"
GREEN = "#2E7D32"
HL = "#FFD400"
DIM = "#4F7C93"
FONT = "font-family=\"Inter, 'Segoe UI', system-ui, sans-serif\""


def icon(name, x, y, size=20, color=TEXT, sw=1.6):
    return (f'<g transform="translate({x} {y}) scale({size / 24:.4f})"><path d="{ICONS[name]}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></g>')


def text(x, y, s, size=12, color=TEXT, weight=400, anchor="start", extra=""):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" {FONT} font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


def hand(d, color=INK, w=1.4, extra=""):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" {extra}/>')


def tick_box(x, y, s=11, ticked=False, seed=1):
    """A hand-drawn tick box (slightly wobbly square), as the app finds them."""
    j = [(0.4, -0.3), (-0.5, 0.4), (0.3, 0.5), (-0.3, -0.4)]
    p = [(x + j[0][0], y + j[0][1]), (x + s + j[1][0], y + j[1][1]), (x + s + j[2][0], y + s + j[2][1]),
         (x + j[3][0], y + s + j[3][1])]
    d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in p) + f" L{p[0][0] + 1:.1f} {p[0][1] + 0.6:.1f}"
    out = hand(d, INK, 1.3)
    if ticked:
        out += hand(f"M{x + 2} {y + s * 0.55} L{x + s * 0.42} {y + s - 1.5} L{x + s + 3} {y - 4}", INK, 1.6)
    return out


def flag(x, y, done=False):
    c = "#9AA3AD" if done else "#E8710A"
    return (f'<path d="M{x} {y + 12} V{y} h8 l-2 3 l2 3 h-8" fill="{c}" stroke="{c}" stroke-width="1.2" '
            f'stroke-linejoin="round"/>')


def ruled(x1, x2, y0, y1, gap, color=RULE):
    return "".join(f'<line x1="{x1}" x2="{x2}" y1="{y:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="0.8"/>'
                   for y in frange(y0, y1, gap))


def dots(x1, x2, y1, y2, gap, color="#C9D3DE", r=0.7):
    out = []
    for y in frange(y1, y2, gap):
        for x in frange(x1, x2, gap):
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>')
    return f'<g fill="{color}">' + "".join(out) + "</g>"


def grid(x1, x2, y1, y2, gap, color="#E3EAF1"):
    out = [f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y1}" y2="{y2}"/>' for x in frange(x1, x2 + 0.01, gap)]
    out += [f'<line x1="{x1}" x2="{x2}" y1="{y:.1f}" y2="{y:.1f}"/>' for y in frange(y1, y2 + 0.01, gap)]
    return f'<g stroke="{color}" stroke-width="0.7">' + "".join(out) + "</g>"


def frange(a, b, step):
    v = a
    while v <= b + 1e-9:
        yield v
        v += step


def page_shadow(x, y, w, h, r=2):
    return (f'<rect x="{x}" y="{y + 2}" width="{w}" height="{h}" rx="{r}" fill="#000" opacity="0.06"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" stroke="#D5DBE2" stroke-width="0.8"/>')


def pdf_text(x, y, w, lines, gap=9, seed=1, color="#C3CAD2", h=3.4):
    import random
    rnd = random.Random(seed)
    out = []
    for i in range(lines):
        ww = w * (0.55 if i == lines - 1 else rnd.uniform(0.86, 1.0))
        out.append(f'<rect x="{x}" y="{y + i * gap:.1f}" width="{ww:.1f}" height="{h}" rx="1.2" fill="{color}"/>')
    return "".join(out)


def dim_line(x1, y1, x2, y2, label, off=14, size=10, color=DIM):
    """A CAD length label: a line parallel to the edge with ticks and its length, as the drawing tool shows."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = uy, -ux  # left of the direction of travel
    ax, ay = x1 + nx * off, y1 + ny * off
    bx, by = x2 + nx * off, y2 + ny * off
    t = 3
    out = [f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="0.9"/>']
    for px, py in ((ax, ay), (bx, by)):
        out.append(f'<line x1="{px - (ux + nx) * t:.1f}" y1="{py - (uy + ny) * t:.1f}" x2="{px + (ux + nx) * t:.1f}" '
                   f'y2="{py + (uy + ny) * t:.1f}" stroke="{color}" stroke-width="1.1"/>')
    mx, my = (ax + bx) / 2 + nx * (size * 0.55), (ay + by) / 2 + ny * (size * 0.55)
    ang = math.degrees(math.atan2(dy, dx))
    if ang > 90 or ang < -90:
        ang += 180
    out.append(f'<text x="{mx:.1f}" y="{my:.1f}" {FONT} font-size="{size}" fill="{color}" text-anchor="middle" '
               f'dominant-baseline="middle" transform="rotate({ang:.1f} {mx:.1f} {my:.1f})">{label}</text>')
    return "".join(out)


def right_angle(x, y, ax, ay, bx, by, s=6, color=DIM):
    """A square corner mark at (x, y) between unit directions a and b."""
    p1 = (x + ax * s, y + ay * s)
    p2 = (x + ax * s + bx * s, y + ay * s + by * s)
    p3 = (x + bx * s, y + by * s)
    return (f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} L{p3[0]:.1f} {p3[1]:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="0.9"/>')


def angle_arc(x, y, a1, a2, r, label, size=9, color=DIM):
    """An angle arc from direction a1 to a2 (degrees, screen y down) with its value beyond it."""
    p = (x + r * math.cos(math.radians(a1)), y + r * math.sin(math.radians(a1)))
    q = (x + r * math.cos(math.radians(a2)), y + r * math.sin(math.radians(a2)))
    sweep = 1 if (a2 - a1) % 360 < 180 else 0
    mid = math.radians(a1 + ((a2 - a1) % 360) / 2)
    lx, ly = x + (r + 13) * math.cos(mid), y + (r + 13) * math.sin(mid)
    return (f'<path d="M{p[0]:.1f} {p[1]:.1f} A{r} {r} 0 0 {sweep} {q[0]:.1f} {q[1]:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="0.9"/>' + text(f"{lx:.1f}", f"{ly + 3:.1f}", label, size, color, anchor="middle"))


def room(ox, oy, k, labels=True, size=10):
    """The chamfered room used in the drawing illustrations: 4200 x 3600 mm with a 1200 mm chamfer."""
    pts_mm = [(0, 0), (4200, 0), (4200, 2400), (3000, 3600), (0, 3600)]
    pts = [(ox + x * k, oy + y * k) for x, y in pts_mm]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    out = [f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>']
    if labels:
        names = ["A = 4200", "2400", "1697", "3000", "B = 3600"]
        for i in range(5):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 5]
            # The outline runs clockwise on screen, so "left of travel" is outside.
            out.append(dim_line(x1, y1, x2, y2, names[i], off=12, size=size))
        (x0, y0), (x1, y1), (x2, y2), (x3, y3), (x4, y4) = pts
        out.append(right_angle(x0, y0, 1, 0, 0, 1))
        out.append(right_angle(x1, y1, -1, 0, 0, 1))
        out.append(right_angle(x4, y4, 1, 0, 0, -1))
        out.append(angle_arc(x2, y2, 90 + 45, 270, 14, "135°", size - 1))
        out.append(angle_arc(x3, y3, 180, 315, 14, "135°", size - 1))
    return "".join(out)


# ---------------------------------------------------------------------------------------------------------------
# Frames
# ---------------------------------------------------------------------------------------------------------------

def window(w, h, title, body):
    """A Windows 11 window."""
    return f'''<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="9" fill="#fff" stroke="#C9CFD6"/>
<clipPath id="clip-{title_id(title)}"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="8"/></clipPath>
<g clip-path="url(#clip-{title_id(title)})">
<rect x="0" y="0" width="{w}" height="34" fill="#F3F3F3"/>
{logo_small(12, 9, 16)}
{text(36, 21.5, title, 12, TEXT)}
<g stroke="{TEXT}" stroke-width="1" fill="none">
<line x1="{w - 126}" x2="{w - 116}" y1="17" y2="17"/>
<rect x="{w - 80}" y="12" width="10" height="10" rx="1.5"/>
<path d="M{w - 34} 12 l10 10 M{w - 24} 12 l-10 10"/>
</g>
{body}
</g>'''


_ids = {}


def title_id(t):
    return _ids.setdefault(t, f"w{len(_ids) + 1}")


def tablet(w, h, body, uid):
    b = 20
    return f'''<rect x="0" y="0" width="{w}" height="{h}" rx="34" fill="#202327"/>
<rect x="3" y="3" width="{w - 6}" height="{h - 6}" rx="31" fill="none" stroke="#3A3F45" stroke-width="1"/>
<circle cx="{w / 2}" cy="{b / 2 + 1}" r="2.6" fill="#3A3F45"/>
<clipPath id="clip-{uid}"><rect x="{b}" y="{b}" width="{w - 2 * b}" height="{h - 2 * b}" rx="14"/></clipPath>
<g clip-path="url(#clip-{uid})"><g transform="translate({b} {b})">{body}</g></g>'''


def phone(w, h, body, uid):
    b = 12
    return f'''<rect x="0" y="0" width="{w}" height="{h}" rx="40" fill="#202327"/>
<clipPath id="clip-{uid}"><rect x="{b}" y="{b}" width="{w - 2 * b}" height="{h - 2 * b}" rx="30"/></clipPath>
<g clip-path="url(#clip-{uid})"><g transform="translate({b} {b})">{body}</g></g>
<circle cx="{w / 2}" cy="{b + 13}" r="5" fill="#202327"/>'''


_logo_count = [0]


def logo_small(x, y, s):
    """The brand mark (brand.py's small version), placed at x, y, s units across."""
    import brand
    _logo_count[0] += 1
    k = s / 512
    return (f'<g transform="translate({x} {y}) scale({k:.5f})">'
            + brand.mark_body(small=True, ids=f"ls{_logo_count[0]}") + "</g>")


def tool(name, x, y, on=False, size=20):
    out = ""
    if on:
        out += f'<rect x="{x - 7}" y="{y - 7}" width="{size + 14}" height="{size + 14}" rx="5" fill="{SOFT}"/>'
        out += f'<rect x="{x + size / 2 - 7}" y="{y + size + 5}" width="14" height="2.6" rx="1.3" fill="{ACCENT}"/>'
    return out + icon(name, x, y, size, ACCENT if on else TEXT)


def swatches(x, y, chosen=0):
    cols = ["#111111", "#1F4FBF", "#C62828", "#2E7D32", "#FFD400"]
    out = []
    for i, c in enumerate(cols):
        cx = x + i * 22
        if i == chosen:
            out.append(f'<circle cx="{cx}" cy="{y}" r="10" fill="none" stroke="{ACCENT}" stroke-width="2"/>')
        out.append(f'<circle cx="{cx}" cy="{y}" r="7" fill="{c}"/>')
    return "".join(out)


def chip(x, y, label, on=False, icon_name=None, h=26):
    w = 16 + len(label) * 6.9 + (20 if icon_name else 0)
    fill = SOFT if on else "#fff"
    stroke = ACCENT if on else "#D1D6DC"
    out = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{fill}" stroke="{stroke}"/>'
    tx = x + 10
    if icon_name:
        out += icon(icon_name, x + 8, y + h / 2 - 8, 16, ACCENT if on else TEXT)
        tx += 18
    out += text(tx, y + h / 2 + 4, label, 11.5, ACCENT if on else TEXT, 500)
    return out, w


def chips(x, y, items):
    out = []
    for item in items:
        label = item[0]
        on = item[1] if len(item) > 1 else False
        ic = item[2] if len(item) > 2 else None
        s, w = chip(x, y, label, on, ic)
        out.append(s)
        x += w + 8
    return "".join(out)


# ---------------------------------------------------------------------------------------------------------------
# The hero page
# ---------------------------------------------------------------------------------------------------------------

def hero_page():
    W, H = 420, 594
    body = [page_shadow(0, 0, W, H, 3)]
    body.append(ruled(28, W - 28, 108, H - 40, 24))
    body.append(f'<line x1="58" x2="58" y1="20" y2="{H - 20}" stroke="#E8B4B4" stroke-width="0.9"/>')
    body.append(text(W - 30, 34, "Wed 19 Nov", 10, "#8A939C", anchor="end"))
    body.append(hand(ink.line(70, 76, 190, 13, seed=11), INK, 2.0))
    body.append(hand(ink.block(70, 132, 300, 3, 24, size=8.5, seed=4, last_frac=0.7), INK, 1.4))
    # highlighter across part of the second line
    body.append(f'<rect x="150" y="146" width="150" height="15" rx="2" fill="{HL}" opacity="0.42"/>')
    for i, (t, w) in enumerate([(True, 210), (False, 170), (False, 240)]):
        y = 222 + i * 24
        body.append(tick_box(70, y - 10, 11, t))
        body.append(hand(ink.line(92, y, w, 8, seed=20 + i, first_cap=False), INK, 1.4))
    body.append(flag(332, 266))
    # a quick sketch with a length
    body.append(f'<path d="M84 330 L232 328 L234 410 L86 412 Z" fill="none" stroke="{BLUE_INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    body.append(f'<path d="M84 318 L232 316 M84 314 v8 M232 312 v8" stroke="{BLUE_INK}" stroke-width="1.2" fill="none"/>')
    body.append(hand(ink.line(140, 310, 40, 7, seed=3, first_cap=False), BLUE_INK, 1.2))
    body.append(hand(ink.block(258, 348, 110, 2, 24, size=7.5, seed=9), BLUE_INK, 1.3))
    # the line being written (drawn word by word on page load)
    for i, word in enumerate(ink.line(70, 468, 280, 8.5, seed=31).split(" M")):
        d = word if word.startswith("M") else "M" + word
        body.append(hand(d, INK, 1.4, f'class="writing w{i}" pathLength="1"'))
    return f'<svg viewBox="-6 -6 {W + 12} {H + 14}" role="img" aria-label="A page of handwritten notes on ruled A4 paper, with a tick-box list, a highlighted line and a sketch">{"".join(body)}</svg>'


# ---------------------------------------------------------------------------------------------------------------
# The anatomy page: one page with everything the app can put on it
# ---------------------------------------------------------------------------------------------------------------

def anatomy_page():
    W, H = 420, 594
    b = [page_shadow(0, 0, W, H, 3), dots(20, W - 20, 20, H - 20, 14)]
    # A: handwriting and pen pressure
    b.append(hand(ink.line(36, 58, 170, 12, seed=41), INK, 2.0))
    b.append(hand(ink.block(36, 86, 320, 2, 22, size=8, seed=42, last_frac=0.8), INK, 1.4))
    b.append(hand(ink.line(36, 130, 230, 8, seed=44), BLUE_INK, 1.4))
    # B: a PDF page to write on
    b.append(f'<rect x="36" y="152" width="348" height="104" rx="2" fill="#fff" stroke="#C9D1DA"/>')
    b.append(f'<rect x="50" y="164" width="120" height="6" rx="2" fill="#8D97A2"/>')
    b.append(pdf_text(50, 180, 320, 7, 10, seed=5))
    b.append(f'<rect x="48" y="196" width="250" height="9" fill="{HL}" opacity="0.45"/>')
    b.append(f'<rect x="48" y="206" width="180" height="9" fill="{HL}" opacity="0.45"/>')
    b.append(hand("M300 226 C320 214 368 218 366 232 C364 246 316 248 300 238 C292 232 298 224 312 222", RED, 1.5))
    # C: typed text and a table
    b.append(text(36, 284, "Kitchen benchtops", 12, TEXT, 600))
    tx, ty, cw, rh = 36, 294, [120, 90, 90], 17
    b.append(f'<rect x="{tx}" y="{ty}" width="{sum(cw)}" height="{rh}" fill="#E8EDF2"/>')
    rows = [["Option", "Size", "Price"], ["Stone", "3.2 m", "$2,400"], ["Laminate", "3.2 m", "$900"]]
    for r, row in enumerate(rows):
        x = tx
        for c, cell in enumerate(row):
            b.append(text(x + 5, ty + r * rh + 12, cell, 9.5, TEXT, 600 if r == 0 else 400))
            x += cw[c]
    gl = []
    for r in range(4):
        gl.append(f'<line x1="{tx}" x2="{tx + sum(cw)}" y1="{ty + r * rh}" y2="{ty + r * rh}"/>')
    x = tx
    for c in range(4):
        gl.append(f'<line x1="{x}" x2="{x}" y1="{ty}" y2="{ty + 3 * rh}"/>')
        if c < 3:
            x += cw[c]
    b.append(f'<g stroke="#5D6A77" stroke-width="0.6">{"".join(gl)}</g>')
    # D: tick boxes and a flag
    b.append(tick_box(36, 362, 11, True))
    b.append(hand(ink.line(58, 372, 150, 8, seed=51, first_cap=False), INK, 1.4))
    b.append(tick_box(36, 386, 11, False))
    b.append(hand(ink.line(58, 396, 120, 8, seed=52, first_cap=False), INK, 1.4))
    b.append(f'<rect x="228" y="360" width="140" height="40" rx="2" fill="none" stroke="#E8710A" stroke-width="0.8" stroke-dasharray="3 2"/>')
    b.append(flag(226, 352))
    b.append(hand(ink.line(240, 384, 110, 8, seed=53), INK, 1.4))
    # E: a scale drawing
    b.append(f'<rect x="36" y="420" width="348" height="102" fill="#fff" stroke="#9AA6B2" stroke-width="0.8"/>')
    b.append(grid(36, 384, 420, 522, 10.2, "#EEF2F6"))
    b.append(room(84, 442, 0.0165, True, 7))
    b.append(text(250, 470, "Area 14.40 m²", 8, DIM))
    b.append(text(250, 482, "Perimeter 14897", 8, DIM))
    b.append(text(250, 500, "A + B = 7800", 8, DIM))
    # F: a link and a sticky note
    b.append(f'<rect x="36" y="540" width="170" height="20" rx="4" fill="#EAF2FC"/>')
    b.append(text(44, 554, "supplier.com.au/benchtops", 9.5, "#1565C0", extra='text-decoration="underline"'))
    b.append(f'<g transform="rotate(-3 300 552)"><rect x="262" y="532" width="86" height="44" fill="#FFF3A6" stroke="#E9D766"/>'
             f'{hand(ink.block(268, 548, 70, 2, 13, size=5.5, seed=61), INK, 1.1)}</g>')
    return (f'<svg viewBox="-6 -6 {W + 12} {H + 14}" role="img" aria-label="One page holding handwriting, a marked-up PDF, '
            f'a typed heading and table, tick boxes and a flag, a scale drawing with lengths and angles, a web link and a sticky note">'
            + "".join(b) + "</svg>")


# ---------------------------------------------------------------------------------------------------------------
# Paper designs strip
# ---------------------------------------------------------------------------------------------------------------

def paper(kind):
    W, H = 84, 119
    b = [f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="2" fill="#fff" stroke="#CDD5DE"/>']
    if kind == "Ruled":
        b.append(ruled(6, W - 6, 18, H - 6, 6.5))
        b.append(f'<line x1="14" x2="14" y1="4" y2="{H - 4}" stroke="#E8B4B4" stroke-width="0.7"/>')
    elif kind == "Grid":
        b.append(grid(4, W - 4, 4, H - 4, 5, "#DCE5EE"))
    elif kind == "Dots":
        b.append(dots(6, W - 6, 6, H - 6, 6, "#B9C5D2", 0.6))
    elif kind == "Cornell":
        b.append(ruled(26, W - 6, 22, H - 30, 6.5))
        b.append(f'<g stroke="#9DB3C8" stroke-width="0.8"><line x1="4" x2="{W - 4}" y1="14" y2="14"/>'
                 f'<line x1="24" x2="24" y1="14" y2="{H - 26}"/><line x1="4" x2="{W - 4}" y1="{H - 26}" y2="{H - 26}"/></g>')
    elif kind == "Day planner":
        for i in range(10):
            y = 16 + i * 10
            b.append(f'<line x1="18" x2="{W - 5}" y1="{y}" y2="{y}" stroke="#D2DCE6" stroke-width="0.7"/>')
            b.append(text(5, y + 3, f"{7 + i:02d}", 4.5, "#8A97A4"))
    elif kind == "Music":
        for s in range(5):
            for l in range(5):
                y = 14 + s * 21 + l * 3
                b.append(f'<line x1="7" x2="{W - 7}" y1="{y:.1f}" y2="{y:.1f}" stroke="#A9B6C3" stroke-width="0.3"/>')
    elif kind == "Isometric":
        out = []
        for i in range(-20, 30):
            x = i * 6
            out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
            out.append(f'<line x1="{x}" y1="0" x2="{x + H * 1.732}" y2="{H}"/>')
            out.append(f'<line x1="{x}" y1="0" x2="{x - H * 1.732}" y2="{H}"/>')
        b.append(f'<clipPath id="iso"><rect x="3" y="3" width="{W - 6}" height="{H - 6}"/></clipPath>'
                 f'<g clip-path="url(#iso)" stroke="#DCE5EE" stroke-width="0.5">{"".join(out)}</g>')
    elif kind == "Three views":
        b.append(grid(4, W - 4, 4, H - 4, 5, "#EEF2F6"))
        b.append(f'<g stroke="#9DB3C8" stroke-width="0.8" fill="none"><line x1="{W / 2}" x2="{W / 2}" y1="6" y2="{H - 6}"/>'
                 f'<line x1="6" x2="{W - 6}" y1="{H / 2}" y2="{H / 2}"/></g>')
        for lx, ly, t in ((7, 12, "Plan"), (7, H / 2 + 8, "Front"), (W / 2 + 3, H / 2 + 8, "Side")):
            b.append(text(lx, ly, t, 5, "#7F95AB", 600))
    elif kind == "Your own":
        b.append(f'<rect x="4" y="4" width="{W - 8}" height="16" fill="#EAF2FC"/>')
        b.append(ruled(8, W - 8, 30, H - 8, 9, "#BFD3E8"))
    return f'<svg viewBox="-2 -2 {W + 4} {H + 4}" aria-hidden="true">{"".join(b)}</svg>'


# ---------------------------------------------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------------------------------------------

def windows_notebook():
    W, H = 1000, 620
    b = []
    # toolbar: places, tools, colours, widths, then undo and the rest (build 52)
    b.append(f'<rect x="0" y="34" width="{W}" height="52" fill="{BAR}"/><line x1="0" x2="{W}" y1="86" y2="86" stroke="{BORDER}"/>')
    x = 18
    for name in ["SEARCH", "PAGES", "NOTEBOOKS", "MAP"]:
        b.append(icon(name, x, 50, 20))
        x += 36
    b.append(f'<line x1="{x - 4}" x2="{x - 4}" y1="48" y2="72" stroke="{BORDER}"/>')
    x += 12
    for i, name in enumerate(["PEN", "FINELINER", "HIGHLIGHTER", "COLOUR", "ERASER", "SELECT", "DRAWING", "NOTE", "TEXT",
                              "LINK", "FLAG", "TALK", "RULER"]):
        b.append(tool(name, x, 50, on=(i == 0)))
        x += 37
    b.append(f'<line x1="{x - 6}" x2="{x - 6}" y1="48" y2="72" stroke="{BORDER}"/>')
    b.append(swatches(x + 12, 60, 0))
    x += 12 + 5 * 22 + 2
    for i, r in enumerate([1.5, 2.5, 4]):
        b.append(f'<circle cx="{x + i * 18}" cy="60" r="{r}" fill="{TEXT}"/>')
    b.append(f'<circle cx="{x + 18}" cy="60" r="8.5" fill="none" stroke="{ACCENT}" stroke-width="1.6"/>')
    for i, name in enumerate(["UNDO", "ACTIONS", "MORE"]):
        b.append(icon(name, W - 116 + i * 36, 50, 20))
    # pages panel
    b.append(f'<rect x="0" y="87" width="176" height="{H - 87}" fill="{BAR}"/><line x1="176" x2="176" y1="87" y2="{H}" stroke="{BORDER}"/>')
    b.append(text(16, 112, "Pages", 13, TEXT, 600))
    b.append(icon("PAGE_ADD", 142, 99, 18))
    for i in range(4):
        y = 126 + i * 108
        on = i == 1
        b.append(f'<rect x="44" y="{y}" width="72" height="98" rx="2" fill="#fff" stroke="{ACCENT if on else "#D5DBE2"}" stroke-width="{2 if on else 1}"/>')
        b.append(hand(ink.block(52, y + 18, 54, 4 if i != 2 else 2, 9, size=3.2, seed=70 + i), INK, 0.7))
        if i == 2:
            b.append(f'<rect x="52" y="{y + 40}" width="56" height="34" fill="none" stroke="{BLUE_INK}" stroke-width="0.8"/>')
        b.append(text(30, y + 12, str(i + 1), 10, TEXT2, anchor="end"))
    # desk and page
    b.append(f'<rect x="177" y="87" width="{W - 177}" height="{H - 87}" fill="{DESK}"/>')
    px, py, pw, ph = 412, 104, 362, 512
    b.append(page_shadow(px, py, pw, ph, 2))
    b.append(ruled(px + 18, px + pw - 18, py + 92, py + ph - 20, 21))
    b.append(f'<line x1="{px + 48}" x2="{px + 48}" y1="{py + 10}" y2="{py + ph - 10}" stroke="#E8B4B4" stroke-width="0.8"/>')
    b.append(text(px + pw - 20, py + 26, "Wed 19 Nov", 9, "#8A939C", anchor="end"))
    b.append(text(px + 20, py + 26, "Site notes", 9, "#8A939C"))
    b.append(hand(ink.line(px + 58, py + 70, 170, 11, seed=81), INK, 1.8))
    b.append(hand(ink.block(px + 58, py + 113, 270, 4, 21, size=7.2, seed=82, last_frac=0.55), INK, 1.25))
    b.append(f'<rect x="{px + 120}" y="{py + 122}" width="130" height="13" rx="2" fill="{HL}" opacity="0.42"/>')
    for i, t in enumerate([True, True, False]):
        y = py + 218 + i * 21
        b.append(tick_box(px + 58, y - 9, 10, t))
        b.append(hand(ink.line(px + 78, y, 150 + i * 30, 7.2, seed=84 + i, first_cap=False), INK, 1.25))
    b.append(hand(ink.block(px + 58, py + 302, 260, 3, 21, size=7.2, seed=88), BLUE_INK, 1.25))
    b.append(f'<path d="M{px + 70} {py + 380} L{px + 200} {py + 378} L{px + 202} {py + 452} L{px + 72} {py + 454} Z" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    b.append(hand(ink.line(px + 220, py + 420, 90, 7, seed=89), INK, 1.2))
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="MyPowerfulNotes on Windows: the pen toolbar, the pages panel and a page of handwritten site notes">{window(W, H, "MyPowerfulNotes", "".join(b))}</svg>'


def tablet_pdf():
    W, H = 1000, 660
    sw, sh = W - 40, H - 40
    b = [f'<rect x="0" y="0" width="{sw}" height="{sh}" fill="{DESK}"/>']
    b.append(f'<rect x="0" y="0" width="{sw}" height="54" fill="{BAR}"/><line x1="0" x2="{sw}" y1="54" y2="54" stroke="{BORDER}"/>')
    b.append(icon("LEFT", 14, 16, 22))
    b.append(text(48, 25, "Contracts", 10.5, TEXT2))
    b.append(text(48, 41, "Supply agreement", 13, TEXT, 600))
    x = 300
    for i, name in enumerate(["PEN", "HIGHLIGHTER", "ERASER", "SELECT", "TEXT", "FLAG"]):
        b.append(tool(name, x, 17, on=(i == 1)))
        x += 42
    b.append(swatches(x + 14, 27, 4))
    b.append(f'<rect x="{sw - 150}" y="14" width="74" height="26" rx="13" fill="#fff" stroke="#D1D6DC"/>')
    b.append(text(sw - 113, 31, "3 / 12", 11.5, TEXT, 500, anchor="middle"))
    b.append(icon("MORE", sw - 54, 16, 22))
    # the PDF page
    px, py, pw, ph = 292, 70, 376, 532
    b.append(page_shadow(px, py, pw, ph, 1))
    b.append(f'<rect x="{px + 30}" y="{py + 34}" width="170" height="9" rx="2" fill="#5F6B78"/>')
    b.append(f'<rect x="{px + 30}" y="{py + 52}" width="110" height="5" rx="2" fill="#9AA4AF"/>')
    y = py + 80
    for para in range(5):
        b.append(text(px + 30, y + 4, f"{para + 4}.", 8, "#5F6B78", 600))
        b.append(pdf_text(px + 46, y, pw - 76, 5 if para != 2 else 6, 10, seed=90 + para))
        y += (5 if para != 2 else 6) * 10 + 18
    # highlights and ink
    b.append(f'<rect x="{px + 44}" y="{py + 156}" width="300" height="9" fill="{HL}" opacity="0.5"/>')
    b.append(f'<rect x="{px + 44}" y="{py + 166}" width="220" height="9" fill="{HL}" opacity="0.5"/>')
    b.append(hand(f"M{px + 24} {py + 226} C{px + 10} {py + 214} {px + 16} {py + 196} {px + 34} {py + 196} C{px + 52} {py + 196} {px + 54} {py + 214} {px + 42} {py + 224} C{px + 34} {py + 230} {px + 22} {py + 228} {px + 20} {py + 220}", RED, 1.6))
    b.append(hand(f"M{px + 52} {py + 258} L{px + 300} {py + 257}", RED, 1.4))
    b.append(hand(f"M{px + pw + 10} {py + 160} C{px + pw + 30} {py + 150} {px + pw + 40} {py + 140} {px + pw + 56} {py + 126}", BLUE_INK, 1.4))
    b.append(hand(ink.block(px + pw + 30, py + 112, 220, 3, 20, size=7.5, seed=95), BLUE_INK, 1.4))
    b.append(hand(ink.block(px + pw + 30, py + 300, 200, 2, 20, size=7.5, seed=97), RED, 1.4))
    b.append(hand(f"M{px + pw + 20} {py + 306} L{px + pw - 30} {py + 330}", RED, 1.3))
    b.append(f'<rect x="20" y="{py + 180}" width="248" height="138" rx="3" fill="#fff" stroke="#C9D1DA"/>')
    b.append(hand(ink.block(30, py + 232, 220, 4, 22, size=7.5, seed=99), INK, 1.4))
    b.append(text(30, py + 202, "Questions for Monday", 12, TEXT, 600))
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="MyPowerfulNotes on an Android tablet: a PDF contract with highlighted '
            f'clauses, circled numbers and handwritten notes in the margin">{tablet(W, H, "".join(b), "tab1")}</svg>')


def cad_screen():
    W, H = 1000, 620
    b = []
    b.append(f'<rect x="0" y="34" width="{W}" height="52" fill="{BAR}"/><line x1="0" x2="{W}" y1="86" y2="86" stroke="{BORDER}"/>')
    b.append(chips(16, 47, [("Line", True, "DRAWING"), ("Rectangle", False), ("Arc", False), ("Offset", False),
                            ("Measure", False, "MEASURE"), ("Area", False, "AREA"), ("Sum", False, "SUM"),
                            ("Links", False), ("Move…", False, "MOVE"), ("Angles", True)]))
    b.append(text(W - 20, 64, "Scale 1:50", 11.5, TEXT2, anchor="end"))
    b.append(f'<rect x="0" y="87" width="{W}" height="{H - 87}" fill="{DESK}"/>')
    b.append(f'<rect x="60" y="104" width="880" height="560" fill="#fff" stroke="#D5DBE2"/>')
    b.append(f'<rect x="110" y="140" width="780" height="440" fill="#fff" stroke="#9AA6B2"/>')
    b.append(grid(110, 890, 140, 580, 20, "#EEF2F6"))
    k = 0.085
    ox, oy = 200, 196
    b.append(room(ox, oy, k, True, 12))
    # selected line and its handles
    x1, y1, x2, y2 = ox, oy, ox + 4200 * k, oy
    b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ACCENT}" stroke-width="3" opacity="0.35"/>')
    for hx in (x1, x2):
        b.append(f'<circle cx="{hx}" cy="{y1}" r="5" fill="#fff" stroke="{ACCENT}" stroke-width="2"/>')
    b.append(text(ox + 4200 * k * 0.38, oy + 3600 * k * 0.45, "Area 14.40 m²", 13, DIM, anchor="middle"))
    b.append(text(ox + 4200 * k * 0.38, oy + 3600 * k * 0.45 + 18, "Perimeter 14897", 12, DIM, anchor="middle"))
    b.append(text(640, 230, "A + B = 7800", 13, DIM))
    # the length box, as when a length is tapped
    bx, by = 640, 300
    b.append(f'<rect x="{bx}" y="{by}" width="220" height="132" rx="8" fill="#fff" stroke="#D1D6DC"/>')
    b.append(f'<rect x="{bx}" y="{by + 2}" width="220" height="132" rx="8" fill="#000" opacity="0.04"/>')
    b.append(text(bx + 16, by + 26, "Length of A", 12, TEXT, 600))
    b.append(f'<rect x="{bx + 16}" y="{by + 38}" width="188" height="30" rx="4" fill="#fff" stroke="{ACCENT}" stroke-width="1.5"/>')
    b.append(text(bx + 26, by + 58, "B + 600", 13, TEXT))
    b.append(text(bx + 194, by + 58, "= 4200", 12, TEXT2, anchor="end"))
    b.append(f'<circle cx="{bx + 24}" cy="{by + 88}" r="6" fill="none" stroke="{ACCENT}" stroke-width="1.6"/><circle cx="{bx + 24}" cy="{by + 88}" r="3" fill="{ACCENT}"/>')
    b.append(text(bx + 36, by + 92, "Keep the start", 11.5, TEXT))
    b.append(f'<rect x="{bx + 18}" y="{by + 104}" width="12" height="12" rx="2.5" fill="{ACCENT}"/><path d="M{bx + 20.5} {by + 110} l3 3 l5 -6" stroke="#fff" stroke-width="1.6" fill="none"/>')
    b.append(text(bx + 36, by + 114, "Linked lines follow", 11.5, TEXT))
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="The drawing tool: a room drawn to scale with lengths, named sides A and B, '
            f'right-angle marks, 135 degree angles, the area and perimeter, and a length being set with a sum">'
            f'{window(W, H, "MyPowerfulNotes - drawing", "".join(b))}</svg>')


def map_screen():
    W, H = 1000, 620
    b = [f'<rect x="0" y="34" width="{W}" height="{H - 34}" fill="#F7F8FA"/>', dots(20, W - 20, 54, H - 10, 22, "#D9DFE6", 1)]
    b.append(f'<rect x="0" y="34" width="{W}" height="48" fill="{BAR}"/><line x1="0" x2="{W}" y1="82" y2="82" stroke="{BORDER}"/>')
    b.append(chips(16, 45, [("Thought", False, "PLUS"), ("Link", False, "LINK"), ("Area", False), ("Tags", True, "TAG")]))
    b.append(icon("SEARCH", W - 50, 48, 20))
    # area
    b.append(f'<rect x="560" y="300" width="390" height="270" rx="10" fill="#EEF4FB" stroke="#B9CDE3" stroke-dasharray="6 4"/>')
    b.append(text(576, 324, "Kitchen job", 13, "#3D5A78", 600))

    def node(x, y, label, kind="page", w=None):
        w = w or (len(label) * 7.2 + 34)
        if kind == "root":
            return f'<rect x="{x - w / 2}" y="{y - 18}" width="{w}" height="36" rx="18" fill="{ACCENT}"/>' + text(x, y + 5, label, 13.5, "#fff", 600, "middle")
        if kind == "notebook":
            return (f'<rect x="{x - w / 2}" y="{y - 17}" width="{w}" height="34" rx="8" fill="#fff" stroke="{ACCENT}" stroke-width="1.5"/>'
                    + icon("NOTEBOOKS", x - w / 2 + 9, y - 9, 18, ACCENT) + text(x - w / 2 + 32, y + 4.5, label, 12.5, TEXT, 600))
        if kind == "thought":
            return (f'<rect x="{x - w / 2}" y="{y - 17}" width="{w}" height="34" rx="6" fill="#FFF3A6" stroke="#E9D766"/>'
                    + text(x, y + 4.5, label, 12, TEXT, 400, "middle"))
        if kind == "link":
            return (f'<rect x="{x - w / 2}" y="{y - 17}" width="{w}" height="34" rx="6" fill="#fff" stroke="#9BBCE0"/>'
                    + icon("WEB", x - w / 2 + 9, y - 8, 16, "#1565C0") + text(x - w / 2 + 30, y + 4.5, label, 12, "#1565C0", 500))
        if kind == "tag":
            return (f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="13" fill="#EAF6EC" stroke="#9CCBA3"/>'
                    + text(x, y + 4.5, label, 11.5, GREEN, 500, "middle"))
        return (f'<rect x="{x - w / 2}" y="{y - 16}" width="{w}" height="32" rx="6" fill="#fff" stroke="#CBD3DC"/>'
                + icon("PAGES", x - w / 2 + 8, y - 8, 16, TEXT2) + text(x - w / 2 + 30, y + 4.5, label, 12, TEXT))

    def link(x1, y1, x2, y2, c="#9AA9B8", dash=""):
        mx = (x1 + x2) / 2
        return f'<path d="M{x1} {y1} C{mx} {y1} {mx} {y2} {x2} {y2}" fill="none" stroke="{c}" stroke-width="1.5" {dash}/>'

    L = [link(150, 330, 300, 190), link(150, 330, 300, 330), link(150, 330, 300, 470),
         link(300, 190, 520, 140), link(300, 190, 520, 230),
         link(300, 330, 640, 380), link(300, 330, 640, 450), link(640, 380, 860, 380, ACCENT),
         link(640, 450, 860, 520, ACCENT), link(520, 230, 800, 250, "#9CCBA3", 'stroke-dasharray="4 4"'),
         link(640, 450, 800, 250, "#9CCBA3", 'stroke-dasharray="4 4"'), link(300, 470, 520, 530)]
    b.extend(L)
    b.append(node(150, 330, "My notes", "root"))
    b.append(node(300, 190, "Site notes", "notebook"))
    b.append(node(300, 330, "Projects", "notebook"))
    b.append(node(300, 470, "Ideas", "notebook"))
    b.append(node(520, 140, "Site visit 19 Nov"))
    b.append(node(520, 230, "Slab and drainage"))
    b.append(node(640, 380, "Benchtop options"))
    b.append(node(640, 450, "Kitchen layout"))
    b.append(node(860, 380, "Supplier catalogue", "link"))
    b.append(node(860, 520, "Ask about lead times", "thought"))
    b.append(node(800, 250, "#quotes", "tag"))
    b.append(node(520, 530, "Workshop shelving"))
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="The notes map: notebooks, pages, a web link, a thought and a tag, '
            f'joined by lines, with an area grouping the kitchen job">{window(W, H, "MyPowerfulNotes - notes map", "".join(b))}</svg>')


def phone_actions():
    W, H = 380, 780
    sw = W - 24
    b = [f'<rect x="0" y="0" width="{sw}" height="{H - 24}" fill="#fff"/>']
    b.append(text(24, 32, "9:41", 12, TEXT, 600))
    b.append(f'<rect x="0" y="48" width="{sw}" height="60" fill="{BAR}"/><line x1="0" x2="{sw}" y1="108" y2="108" stroke="{BORDER}"/>')
    b.append(icon("LEFT", 14, 66, 22))
    b.append(text(48, 84, "Actions", 18, TEXT, 600))
    b.append(icon("SEARCH", sw - 44, 66, 22))
    b.append(chips(16, 122, [("Open", True), ("Due soon", False), ("Flags", False, "FLAG")]))
    items = [
        ("Order 12 sheets of plasterboard", "Due Fri 21 Nov", "Site notes p4", "High", False, False),
        ("Call Sam about the window sizes", "Due Mon 24 Nov", "Site notes p2", "", False, False),
        ("Check slab levels before the pour", "Flagged", "Projects p7", "", False, True),
        ("Book the skip bin", "No date", "Site notes p4", "", False, False),
        ("Send the revised quote", "Done", "Projects p3", "", True, False),
    ]
    y = 170
    for title, due, where, pri, done, flg in items:
        b.append(f'<line x1="16" x2="{sw - 16}" y1="{y + 74}" y2="{y + 74}" stroke="#EEF0F3"/>')
        if done:
            b.append(f'<rect x="18" y="{y + 12}" width="20" height="20" rx="5" fill="{ACCENT}"/><path d="M22.5 {y + 22} l4 4 l7 -8" stroke="#fff" stroke-width="2" fill="none"/>')
        else:
            b.append(f'<rect x="18" y="{y + 12}" width="20" height="20" rx="5" fill="#fff" stroke="#8A939C" stroke-width="1.5"/>')
        b.append(text(52, y + 27, title, 14, TEXT2 if done else TEXT, 500,
                      extra='text-decoration="line-through"' if done else ""))
        col = RED if due.startswith("Due Fri") else TEXT2
        b.append(text(52, y + 47, due, 12, col))
        b.append(text(52, y + 64, where, 12, TEXT2))
        if pri:
            b.append(f'<rect x="{sw - 66}" y="{y + 34}" width="46" height="20" rx="10" fill="#FDECEC"/>' + text(sw - 43, y + 48, pri, 11, RED, 600, "middle"))
        if flg:
            b.append(flag(sw - 40, y + 36))
        # the handwriting it came from
        y += 82
    b.append(f'<rect x="{sw - 76}" y="{H - 24 - 92}" width="56" height="56" rx="16" fill="{ACCENT}"/>' + icon("PLUS", sw - 60, H - 24 - 76, 24, "#fff", 2))
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="The Actions list on a phone: tasks taken from tick boxes and flags, '
            f'with due dates, priority and the page each came from">{phone(W, H, "".join(b), "ph1")}</svg>')



# ---------------------------------------------------------------------------------------------------------------
# Woodwork: the compact drawing bar, a carcass to scale with parts, dimensions, hidden lines and guides
# ---------------------------------------------------------------------------------------------------------------

GUIDE = "#6FA8DC"


def bar_button(x, y, glyph, on=False, w=30, drop=False):
    """A square icon button on the drawing bar. glyph is an icon name or raw SVG drawn in a 20-unit box."""
    out = ""
    if on:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1"/>'
    c = ACCENT if on else TEXT
    if glyph in ICONS:
        out += icon(glyph, x + (w - 18) / 2 - (3 if drop else 0), y + 6, 18, c)
    else:
        out += (f'<g transform="translate({x + (w - 18) / 2 - (3 if drop else 0)} {y + 6}) scale(0.9)" fill="none" stroke="{c}" '
                f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>')
    if drop:
        out += f'<path d="M{x + w - 9} {y + 14} l3 3 l3 -3" stroke="{TEXT2}" stroke-width="1.2" fill="none"/>'
    return out


G_POINTS = '<circle cx="5" cy="15" r="2.4"/><circle cx="15" cy="5" r="2.4"/><path d="M7 13 L13 7" stroke-dasharray="2 2"/>'
G_GROUP = '<rect x="2" y="2" width="9" height="9"/><rect x="9" y="9" width="9" height="9"/>'
G_OFFSET = '<path d="M3 6 H17 M3 14 H17"/><path d="M10 6 V14" stroke-dasharray="2 2"/>'
G_EDIT = '<path d="M4 16 L5 12 L14 3 L17 6 L8 15 Z"/>'
G_SHAPES = '<rect x="2" y="8" width="9" height="9"/><circle cx="13" cy="7" r="5"/>'
G_CORNER = '<path d="M3 17 V9 Q3 3 9 3 H17"/><path d="M3 3 H6 M3 3 V6" stroke-dasharray="1.5 1.5"/>'
G_LINKS = '<path d="M8 12 L12 8"/><path d="M9 6 L11 4 a3.5 3.5 0 0 1 5 5 L14 11"/><path d="M11 14 L9 16 a3.5 3.5 0 0 1 -5 -5 L6 9"/>'
G_FILL = '<path d="M4 9 L10 3 L16 9 L10 15 Z"/><path d="M16 12 q2 3 0 4 q-2 -1 0 -4" fill="currentColor"/>'
G_EYE = '<path d="M1 10 Q10 1 19 10 Q10 19 1 10 Z"/><circle cx="10" cy="10" r="2.6"/>'
G_LIST = '<path d="M6 5 H17 M6 10 H17 M6 15 H17"/><circle cx="2.5" cy="5" r=".8"/><circle cx="2.5" cy="10" r=".8"/><circle cx="2.5" cy="15" r=".8"/>'
G_WOOD = ('<rect x="2" y="4" width="16" height="12" rx="1"/><path d="M5 8 C8 6.5 12 9.5 15 8 M5 12 C8 10.5 12 13.5 15 12"/>')


def dim_h(x1, x2, y, label, ext_from, size=10, color=DIM):
    """A horizontal dimension at y, with extension lines up or down to ext_from and arrows."""
    d = 1 if ext_from > y else -1
    out = [f'<g stroke="{color}" stroke-width="0.8" fill="none">',
           f'<path d="M{x1} {ext_from - 3 * d} V{y - 4 * d} M{x2} {ext_from - 3 * d} V{y - 4 * d}"/>',
           f'<path d="M{x1} {y} H{x2}"/>',
           f'<path d="M{x1 + 6} {y - 2.5} L{x1} {y} L{x1 + 6} {y + 2.5} M{x2 - 6} {y - 2.5} L{x2} {y} L{x2 - 6} {y + 2.5}"/></g>']
    tw = len(label) * size * 0.58 + 6
    out.append(f'<rect x="{(x1 + x2) / 2 - tw / 2}" y="{y - size * 0.7}" width="{tw}" height="{size * 1.4}" fill="#fff"/>')
    out.append(text((x1 + x2) / 2, y + size * 0.36, label, size, color, 500, "middle"))
    return "".join(out)


def dim_v(x, y1, y2, label, ext_from, size=10, color=DIM):
    d = 1 if ext_from > x else -1
    out = [f'<g stroke="{color}" stroke-width="0.8" fill="none">',
           f'<path d="M{ext_from - 3 * d} {y1} H{x - 4 * d} M{ext_from - 3 * d} {y2} H{x - 4 * d}"/>',
           f'<path d="M{x} {y1} V{y2}"/>',
           f'<path d="M{x - 2.5} {y1 + 6} L{x} {y1} L{x + 2.5} {y1 + 6} M{x - 2.5} {y2 - 6} L{x} {y2} L{x + 2.5} {y2 - 6}"/></g>']
    cy = (y1 + y2) / 2
    tw = len(label) * size * 0.58 + 6
    out.append(f'<g transform="rotate(-90 {x} {cy})"><rect x="{x - tw / 2}" y="{cy - size * 0.7}" width="{tw}" height="{size * 1.4}" fill="#fff"/>'
               + text(x, cy + size * 0.36, label, size, color, 500, "middle") + "</g>")
    return "".join(out)


def part_tag(x, y, label, size=9):
    w = len(label) * size * 0.56 + 10
    return (f'<rect x="{x - w / 2}" y="{y - size * 0.85}" width="{w}" height="{size * 1.7}" rx="{size * 0.85}" fill="#fff" stroke="#9CCBA3"/>'
            + text(x, y + size * 0.35, label, size, GREEN, 500, "middle"))


def woodwork_screen():
    W, H = 1000, 676
    b = []
    # main toolbar, scale drawing tool on
    b.append(f'<rect x="0" y="34" width="{W}" height="46" fill="{BAR}"/>')
    x = 18
    for name in ["SEARCH", "PAGES", "NOTEBOOKS", "MAP"]:
        b.append(icon(name, x, 47, 18))
        x += 32
    b.append(f'<line x1="{x - 2}" x2="{x - 2}" y1="45" y2="67" stroke="{BORDER}"/>')
    x += 12
    for i, name in enumerate(["PEN", "FINELINER", "HIGHLIGHTER", "COLOUR", "ERASER", "SELECT", "DRAWING", "NOTE", "TEXT", "LINK", "FLAG"]):
        b.append(tool(name, x, 47, on=(name == "DRAWING"), size=18))
        x += 34
    for i, name in enumerate(["UNDO", "ACTIONS", "MORE"]):
        b.append(icon(name, W - 110 + i * 34, 47, 18))
    # the compact drawing bar, docked under the toolbar
    b.append(f'<rect x="0" y="80" width="{W}" height="80" fill="#FFFFFF"/><line x1="0" x2="{W}" y1="160" y2="160" stroke="{BORDER}"/>'
             f'<line x1="0" x2="{W}" y1="80" y2="80" stroke="{BORDER}"/>')
    y = 87
    x = 12

    def box(w, label, val=None):
        nonlocal x
        o = f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="5" fill="#fff" stroke="#D1D6DC"/>' + text(x + 8, y + 19.5, label, 11.5, TEXT, 500)
        if val:
            o += f'<path d="M{x + w - 13} {y + 13} l3 3 l3 -3" stroke="{TEXT2}" stroke-width="1.2" fill="none"/>'
        x += w + 5
        return o

    def btn(g, on=False, drop=False, w=30):
        nonlocal x
        o = bar_button(x, y, g, on, w + (8 if drop else 0), drop)
        x += w + (8 if drop else 0) + 3
        return o

    def sep():
        nonlocal x
        o = f'<line x1="{x + 2}" x2="{x + 2}" y1="{y + 4}" y2="{y + 26}" stroke="{BORDER}"/>'
        x += 8
        return o

    b.append(box(52, "1:10", True))
    b.append(box(44, "mm", True))
    b.append(sep())
    # pick mode: draw, select, points, groups
    b.append(f'<rect x="{x - 2}" y="{y - 2}" width="{4 * 33 + 1}" height="34" rx="7" fill="#F3F3F0"/>')
    b.append(btn("DRAWING", on=True))
    b.append(btn("SELECT"))
    b.append(btn(G_POINTS))
    b.append(btn(G_GROUP))
    b.append(sep())
    b.append(box(54, "560"))
    b.append(box(40, "90°"))
    b.append(btn("PLUS"))
    b.append(btn(G_OFFSET))
    b.append(btn(G_EDIT))
    b.append(btn("TRASH"))
    b.append(sep())
    # line type: a dashed sample
    b.append(bar_button(x, y, '<path d="M1 10 H5 M8 10 H12 M15 10 H19"/>', False, 38, True)); x += 41
    b.append(btn(G_SHAPES, drop=True))
    b.append(btn(G_CORNER))
    b.append(btn("MOVE", drop=True))
    b.append(btn("COPY", drop=True))
    b.append(btn(G_GROUP, drop=True))
    b.append(btn(G_LINKS))
    # the bar wraps onto a second row, as it does in the app when the window is narrower than the bar
    y += 36
    x = 12
    b.append(btn("MEASURE"))
    b.append(btn("AREA"))
    b.append(btn("SUM"))
    b.append(btn(G_FILL, drop=True))
    b.append(btn(G_EYE, drop=True))
    b.append(btn(G_LIST))
    b.append(btn(G_WOOD, on=True, drop=True))
    b.append(btn("MORE"))
    wood_x = x - 33 - 41
    # desk and drawing frame
    b.append(f'<rect x="0" y="161" width="{W}" height="{H - 161}" fill="{DESK}"/>')
    b.append(f'<rect x="40" y="176" width="920" height="490" fill="#fff" stroke="#D5DBE2"/>')
    fx, fy, fw, fh = 330, 196, 600, 450
    b.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#fff" stroke="#9AA6B2"/>')
    b.append(grid(fx, fx + fw, fy, fy + fh, 10, "#F1F4F7"))
    # the carcass at 1:10 (1 mm = 0.5 units): 600 wide, 720 high, 18 mm boards
    k = 0.5
    ox, oy = 540, 251
    cw, ch, t = 600 * k, 720 * k, 18 * k
    L = []
    L.append(f'<rect x="{ox}" y="{oy}" width="{cw}" height="{ch}"/>')
    L.append(f'<rect x="{ox + t}" y="{oy + t}" width="{cw - 2 * t}" height="{ch - 2 * t - 60 * k}"/>')  # inside, over the plinth
    L.append(f'<path d="M{ox} {oy + ch - 60 * k} H{ox + cw}"/>')  # top of the plinth
    b.append(f'<g fill="none" stroke="{INK}" stroke-width="1.5">{"".join(L)}</g>')
    # three drawers: 180, 220, 266 openings with 3 mm gaps
    ix, iw = ox + t, cw - 2 * t
    tops = [oy + t]
    hs = [180, 210, 252]
    fronts = []
    yy = oy + t
    for h in hs:
        fronts.append((ix + 1.5, yy + 1.5, iw - 3, h * k - 3))
        yy += h * k
    for i, (a, b2, c, d) in enumerate(fronts):
        b.append(f'<rect x="{a}" y="{b2}" width="{c}" height="{d}" fill="#FBFAF7" stroke="{INK}" stroke-width="1.2"/>')
        b.append(f'<path d="M{a + c / 2 - 30} {b2 + 22} H{a + c / 2 + 30}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    # hidden: drawer boxes and runners (dashed)
    for (a, b2, c, d) in fronts:
        b.append(f'<rect x="{a + 8}" y="{b2 + 10}" width="{c - 16}" height="{d - 22}" fill="none" stroke="#7D8893" stroke-width="0.9" stroke-dasharray="6 3"/>')
        b.append(f'<path d="M{a + 2} {b2 + d / 2 + 6} H{a + 8} M{a + c - 8} {b2 + d / 2 + 6} H{a + c - 2}" stroke="#7D8893" stroke-width="2"/>')
    # proportion guides: golden ratio sections, dotted
    gy = oy + ch * 0.382
    b.append(f'<g stroke="{GUIDE}" stroke-width="1" stroke-dasharray="1.5 3" fill="none">'
             f'<path d="M{ox - 18} {oy + ch * 0.382} H{ox + cw + 18}"/><path d="M{ox - 18} {oy + ch * 0.618} H{ox + cw + 18}"/>'
             f'<path d="M{ox + cw * 0.382} {oy - 14} V{oy + ch + 14}"/><path d="M{ox + cw * 0.618} {oy - 14} V{oy + ch + 14}"/></g>')
    # dimensions, offset from the lines
    b.append(dim_h(ox, ox + cw, oy - 26, "600", oy))
    b.append(dim_v(ox - 30, oy, oy + ch, "720", ox))
    yy = oy + t
    for h in hs:
        b.append(dim_v(ox + cw + 26, yy, yy + h * k, str(h), ox + cw, 9))
        yy += h * k
    # part labels
    b.append(part_tag(ox + t / 2, oy + ch * 0.5, "Side ×2"))
    b.append(part_tag(ox + cw / 2, oy + t / 2, "Top"))
    b.append(part_tag(ox + cw / 2, fronts[1][1] + fronts[1][3] - 16, "Drawer front 2"))
    b.append(part_tag(ox + cw / 2, oy + ch - 30 * k, "Plinth"))
    b.append(text(fx + 12, fy + fh - 12, "Bedside cabinet, front · 1:10 · 18 mm birch ply", 10, TEXT2))
    # the Woodwork menu, open under its button
    mx, my = wood_x, 160
    items = ["Make a part (tap inside a shape)…", "Parts in this drawing (9)…", "Plan drawers (tap the opening)…",
             "Proportion guides", "Make a cut list…", "Materials…", "Import a parts list (CSV)…", "Import a DXF drawing…"]
    b.append(f'<rect x="{mx}" y="{my + 3}" width="250" height="{len(items) * 30 + 12}" rx="8" fill="#000" opacity="0.06"/>')
    b.append(f'<rect x="{mx}" y="{my}" width="250" height="{len(items) * 30 + 12}" rx="8" fill="#fff" stroke="#D1D6DC"/>')
    for i, it in enumerate(items):
        iy = my + 6 + i * 30
        if it == "Make a cut list…":
            b.append(f'<rect x="{mx + 5}" y="{iy}" width="240" height="28" rx="4" fill="{SOFT}"/>')
        if i in (3, 5):
            b.append(f'<line x1="{mx + 10}" x2="{mx + 240}" y1="{iy - 1}" y2="{iy - 1}" stroke="#EEF0F3"/>')
        b.append(text(mx + 16, iy + 18.5, it, 11.5, TEXT))
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Woodwork on Windows: the compact drawing bar under the toolbar, '
            f'a bedside cabinet drawn at 1:10 with dimensions, dashed hidden drawer boxes, golden ratio guides and part labels, '
            f'and the Woodwork menu open">{window(W, H, "MyPowerfulNotes - workshop", "".join(b))}</svg>')


# ---------------------------------------------------------------------------------------------------------------
# A cut list page on an Android tablet: parts table and a sheet layout
# ---------------------------------------------------------------------------------------------------------------

def sheet_layout(x, y, w, parts, sheet=(2400, 1200), trim=10):
    """parts: (px, py, pw, ph, label) in mm on the sheet. Draws the sheet to fit w units across."""
    k = w / sheet[0]
    h = sheet[1] * k
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#F4EBDD" stroke="#9A8A72" stroke-width="0.8"/>',
           f'<rect x="{x + trim * k}" y="{y + trim * k}" width="{w - 2 * trim * k}" height="{h - 2 * trim * k}" fill="none" stroke="#C9B99E" stroke-width="0.5" stroke-dasharray="2 2"/>']
    for px, py, pw, ph, label in parts:
        rx, ry, rw, rh = x + px * k, y + py * k, pw * k, ph * k
        out.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="#fff" stroke="{INK}" stroke-width="0.8"/>')
        if rw > 40 and rh > 14:
            out.append(text(rx + rw / 2, ry + rh / 2 + 3, label, 7.5 if rw > 70 else 6.5, TEXT, 500, "middle"))
    return "".join(out), h


def tablet_cutlist():
    W, H = 1000, 660
    sw, sh = W - 40, H - 40
    b = [f'<rect x="0" y="0" width="{sw}" height="{sh}" fill="{DESK}"/>']
    b.append(f'<rect x="0" y="0" width="{sw}" height="54" fill="{BAR}"/><line x1="0" x2="{sw}" y1="54" y2="54" stroke="{BORDER}"/>')
    b.append(icon("LEFT", 14, 16, 22))
    b.append(text(48, 25, "Workshop", 10.5, TEXT2))
    b.append(text(48, 41, "Bedside cabinet", 13, TEXT, 600))
    x = 300
    for i, name in enumerate(["PEN", "HIGHLIGHTER", "ERASER", "SELECT", "TEXT", "FLAG"]):
        b.append(tool(name, x, 17, on=(i == 0)))
        x += 42
    b.append(swatches(x + 14, 27, 1))
    b.append(f'<rect x="{sw - 150}" y="14" width="74" height="26" rx="13" fill="#fff" stroke="#D1D6DC"/>')
    b.append(text(sw - 113, 31, "4 / 4", 11.5, TEXT, 500, anchor="middle"))
    b.append(icon("MORE", sw - 54, 16, 22))
    # two pages side by side: the table, and the layout
    for n, px in enumerate((40, 490)):
        b.append(page_shadow(px, 70, 430, 530, 1))
    px, py = 40, 70
    b.append(text(px + 28, py + 40, "Cut list", 17, TEXT, 600))
    b.append(text(px + 28, py + 58, "Bedside cabinet, 25 November 2026. Sizes in mm, length first.", 8.5, TEXT2))
    b.append(text(px + 28, py + 86, "18 mm birch plywood", 12, TEXT, 600))
    b.append(text(px + 28, py + 100, "18 mm thick, sheets 2400 × 1200. The grain runs along the sheet's length.", 8, TEXT2))
    rows = [["Part", "Qty", "Length", "Width", "Edges"],
            ["Side", "2", "720", "450", "Front"], ["Top", "1", "564", "450", "Front"], ["Bottom", "1", "564", "432", ""],
            ["Plinth", "1", "564", "60", "Front"], ["Drawer front 1", "1", "561", "177", "All"],
            ["Drawer front 2", "1", "561", "207", "All"], ["Drawer front 3", "1", "561", "251", "All"],
            ["Back", "1", "684", "564", ""]]
    cw = [140, 40, 60, 60, 70]
    ty, rh = py + 114, 19
    b.append(f'<rect x="{px + 28}" y="{ty}" width="{sum(cw)}" height="{rh}" fill="#EEF0EE"/>')
    for r, row in enumerate(rows):
        cx = px + 28
        for c, cell in enumerate(row):
            anchor = "end" if c in (1, 2, 3) else "start"
            tx = cx + cw[c] - 8 if anchor == "end" else cx + 6
            b.append(text(tx, ty + r * rh + 13, cell, 9, TEXT, 600 if r == 0 else 400, anchor))
            cx += cw[c]
        b.append(f'<line x1="{px + 28}" x2="{px + 28 + sum(cw)}" y1="{ty + (r + 1) * rh}" y2="{ty + (r + 1) * rh}" stroke="#D8DCDF" stroke-width="0.6"/>')
    b.append(text(px + 28, ty + len(rows) * rh + 22, "1 sheet, 78% used (the layout follows).", 9, TEXT))
    b.append(text(px + 28, ty + len(rows) * rh + 54, "Oak, 20 mm", 12, TEXT, 600))
    b.append(text(px + 28, ty + len(rows) * rh + 68, "Rough sizes add 3 mm to the thickness, 5 mm to the width and 50 mm to the length.", 8, TEXT2))
    b.append(text(px + 28, ty + len(rows) * rh + 88, "Top edging  2 × 640 × 25 rough, from one 1800 board", 9, TEXT))
    b.append(text(px + 28, ty + len(rows) * rh + 118, "Printed and bought", 12, TEXT, 600))
    b.append(text(px + 28, ty + len(rows) * rh + 136, "Soft-close runners 450 mm  3 pairs", 9, TEXT))
    b.append(text(px + 28, ty + len(rows) * rh + 152, "Drawer pulls (printed, PETG)  3", 9, TEXT))
    # handwriting on the cut list
    b.append(hand(ink.line(px + 300, py + 86, 90, 8, seed=141), BLUE_INK, 1.3))
    b.append(hand(f"M{px + 24} {py + 198} C{px + 14} {py + 194} {px + 16} {py + 214} {px + 26} {py + 214}", RED, 1.3))
    # layout page
    qx = 490
    b.append(text(qx + 28, py + 40, "18 mm birch plywood", 13, TEXT, 600))
    b.append(text(qx + 28, py + 58, "Sheet 1 of 1, 78% used. 3.2 mm kerf, 10 mm trimmed off each edge.", 8.5, TEXT2))
    parts = [(10, 10, 720, 450, "Side"), (733, 10, 720, 450, "Side"), (1456, 10, 684, 564, "Back"),
             (10, 463, 564, 450, "Top"), (577, 463, 564, 432, "Bottom"), (1144, 577, 561, 251, "Drawer front 3"),
             (1708, 577, 561, 207, "Drawer front 2"), (1144, 831, 561, 177, "Drawer front 1"), (1708, 787, 564, 60, "Plinth")]
    lay, lh = sheet_layout(qx + 28, py + 76, 374, parts)
    b.append(lay)
    b.append(f'<rect x="{qx + 28 + 1708 * 374 / 2400:.1f}" y="{py + 76 + 850 * 374 / 2400:.1f}" width="{680 * 374 / 2400:.1f}" height="{340 * 374 / 2400:.1f}" fill="#EFE5D3" stroke="#B4A486" stroke-width="0.6" stroke-dasharray="2 2"/>')
    b.append(text(qx + 28 + 2048 * 374 / 2400, py + 76 + 1030 * 374 / 2400, "Offcut", 6.5, "#7A6A50", 500, "middle"))
    b.append(text(qx + 28, py + 76 + lh + 22, "Length runs left to right, with the grain.", 8.5, TEXT2))
    # drawer plan summary
    b.append(text(qx + 28, py + 324, "Drawers", 13, TEXT, 600))
    b.append(text(qx + 28, py + 342, "Opening 564 wide, 450 deep. Side-mount runners, 12.7 mm each side.", 8.5, TEXT2))
    rows2 = [["Drawer", "Front", "Box height", "Box width", "Runner"], ["1", "177", "120", "538", "450"],
             ["2", "207", "150", "538", "450"], ["3", "251", "190", "538", "450"]]
    cw2 = [60, 70, 80, 80, 60]
    ty2 = py + 356
    b.append(f'<rect x="{qx + 28}" y="{ty2}" width="{sum(cw2)}" height="19" fill="#EEF0EE"/>')
    for r, row in enumerate(rows2):
        cx = qx + 28
        for c, cell in enumerate(row):
            b.append(text(cx + 6, ty2 + r * 19 + 13, cell, 9, TEXT, 600 if r == 0 else 400))
            cx += cw2[c]
        b.append(f'<line x1="{qx + 28}" x2="{qx + 28 + sum(cw2)}" y1="{ty2 + (r + 1) * 19}" y2="{ty2 + (r + 1) * 19}" stroke="#D8DCDF" stroke-width="0.6"/>')
    b.append(hand(ink.block(qx + 40, py + 460, 300, 2, 22, size=7.5, seed=147), INK, 1.3))
    b.append(tick_box(qx + 28, py + 494, 10, True))
    b.append(hand(ink.line(qx + 46, py + 503, 160, 7, seed=149, first_cap=False), INK, 1.25))
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="A cut list on an Android tablet: a parts table for 18 mm birch plywood, '
            f'oak edging and bought runners, a sheet layout showing how the parts fit on one sheet, and a drawer plan, with handwritten notes">'
            f'{tablet(W, H, "".join(b), "tab2")}</svg>')


def sync_diagram():
    """Your devices, your cloud, encrypted files only: no MyPowerfulNotes server in the middle."""
    W, H = 640, 250
    b = []

    def device(x, y, label, sub, kind):
        out = f'<rect x="{x}" y="{y}" width="150" height="104" rx="12" fill="#fff" stroke="#CBD3DC"/>'
        if kind == "pc":
            out += f'<rect x="{x + 45}" y="{y + 16}" width="60" height="40" rx="3" fill="none" stroke="{TEXT}" stroke-width="1.6"/><path d="M{x + 65} {y + 64} h20 M{x + 75} {y + 56} v8" stroke="{TEXT}" stroke-width="1.6"/>'
        else:
            out += f'<rect x="{x + 52}" y="{y + 12}" width="46" height="58" rx="5" fill="none" stroke="{TEXT}" stroke-width="1.6"/><path d="M{x + 98} {y + 18} l10 -6" stroke="{BLUE_INK}" stroke-width="2" stroke-linecap="round"/>'
        out += text(x + 75, y + 86, label, 12.5, TEXT, 600, "middle")
        out += text(x + 75, y + 124, sub, 11, TEXT2, 400, "middle")
        return out

    b.append(device(10, 40, "Your PC", "Encrypted before upload", "pc"))
    b.append(device(W - 160, 40, "Your tablet", "Opened only with your key", "tab"))
    cx = W / 2
    b.append(f'<path d="M{cx - 70} 92 a40 40 0 0 1 22 -40 a50 50 0 0 1 92 6 a34 34 0 0 1 20 66 h-118 a32 32 0 0 1 -16 -32 Z" fill="#EAF2FC" stroke="#9BBCE0" stroke-width="1.5"/>')
    b.append(icon("LOCK", cx - 12, 68, 24, ACCENT, 1.8))
    b.append(text(cx, 156, "Your OneDrive or Google Drive", 12.5, TEXT, 600, "middle"))
    b.append(text(cx, 174, "holds only encrypted files", 11, TEXT2, 400, "middle"))
    for x1, x2 in ((165, cx - 78), (cx + 84, W - 165)):
        b.append(f'<path d="M{x1} 86 H{x2}" stroke="{ACCENT}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#arr)" marker-start="url(#arr2)"/>')
    defs = (f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{ACCENT}"/></marker><marker id="arr2" viewBox="0 0 10 10" refX="1" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 Z" fill="{ACCENT}"/></marker></defs>')
    b.append(text(cx, 222, "No MyPowerfulNotes server, no account with us, nothing in between", 11.5, TEXT2, 400, "middle"))
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Your PC and tablet sync through your own OneDrive or Google Drive, '
            f'which holds only encrypted files. There is no MyPowerfulNotes server.">{defs}{"".join(b)}</svg>')
