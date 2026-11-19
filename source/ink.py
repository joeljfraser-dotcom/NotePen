"""Pseudo-handwriting for the site's illustrations: cursive-looking lines that read as writing, not as words."""
import math, random

LETTERS = "eeeeeaaaooiinnmrsuuuwcclllbdhkttfgpy"
TALL = set("lbdhkt" + "f")
LOW = set("gpyq")

def line(x, y, width, size=10, seed=1, slant=0.38, first_cap=True):
    """A path 'd' for one written line starting at (x, y) baseline, about `width` long. size = x-height."""
    rnd = random.Random(seed)
    pts_all = []
    cx = x
    end = x + width
    word_no = 0
    while cx < end - size * 2:
        n = rnd.randint(2, 7)
        if cx + n * size * 0.62 > end:
            n = max(2, int((end - cx) / (size * 0.62)))
        pts = []
        drift = rnd.uniform(-0.6, 0.6)
        for i in range(n):
            ch = rnd.choice(LETTERS)
            if first_cap and word_no == 0 and i == 0:
                ch = "l"
            w = size * rnd.uniform(0.46, 0.6)
            h = size * rnd.uniform(0.85, 1.05)
            loop = 0.0
            if ch in TALL:
                h = size * rnd.uniform(1.9, 2.3); loop = w * 0.32
            elif ch in "eaoc":
                loop = w * 0.42
            elif ch in "mn":
                loop = 0.0
            else:
                loop = w * 0.2
            down = 0
            if ch in LOW:
                down = size * rnd.uniform(0.9, 1.2)
            steps = 10
            for s in range(steps + (1 if i == n - 1 else 0)):
                t = s / steps
                if ch in "uiw":
                    # cup: up the stroke, down and round at the bottom
                    yy = y + drift - h * abs(math.sin(math.pi * t)) ** 0.5 * (1 if t < 0.5 else 1) * (1 - t) - h * (t) * (1 - abs(math.sin(math.pi * t)))
                else:
                    yy = y + drift - h * (1 - math.cos(2 * math.pi * t)) / 2
                xx = cx + w * t + loop * math.sin(2 * math.pi * t)
                if down and t > 0.55:
                    # a descender: dip below the line on the way out
                    k = (t - 0.55) / 0.45
                    yy += down * math.sin(math.pi * k)
                xx += (y - yy) * slant
                pts.append((xx, yy))
            cx += w
        pts_all.append(pts)
        cx += size * rnd.uniform(0.7, 1.1)
        word_no += 1
    d = []
    for pts in pts_all:
        d.append("M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts))
    return " ".join(d)

def block(x, y, width, lines, gap, size=10, seed=1, last_frac=0.6):
    out = []
    for i in range(lines):
        w = width * (last_frac if i == lines - 1 else random.Random(seed * 31 + i).uniform(0.82, 1.0))
        out.append(line(x, y + i * gap, w, size, seed * 7 + i))
    return " ".join(out)
