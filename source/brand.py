#!/usr/bin/env python3
"""Makes every file in brand/ from one description of the mark (graphite and teal, Nov 2026).

The mark: an A4 page with three lines of handwriting and a teal stylus, on a rounded graphite tile.
Run from the repo root:  python3 source/brand.py   (needs rsvg-convert, ImageMagick and the Inter fonts).
Then run source/build.py, which copies the mark into the site.
"""
import os
import shutil
import subprocess
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, "brand")
FONTS = "/usr/share/fonts/opentype/inter/"

# ---- Colours ----
TILE_LIGHT = "#3A424C"    # graphite tile, top left
TILE_DEEP = "#1A1F25"     # graphite tile, bottom right
GRAPHITE = "#26323F"      # handwriting on the page
TEAL = "#0E6E66"          # the accent: the stylus, the middle line, links, "Powerful"
TEAL_BAND = "#E9F5F3"
TEXT = "#1E242B"
PAPER = "#FFFDF8"
FOLD = "#E4E1D8"
TIP_GREY = "#C9D3D2"
POINT_INK = "#26323F"

PAGE = "M150 108 H310 L364 162 V386 Q364 404 346 404 H168 Q150 404 150 386 V126 Q150 108 168 108 Z"
CORNER = "M310 108 V146 Q310 162 326 162 H364 Z"
# Three lines of handwriting: graphite, teal, graphite. The last ends where the stylus touches the page.
LINES = [
    ("M180 206 C192 186 200 220 212 204 S230 188 242 206 S262 220 274 202 S298 192 330 204", GRAPHITE),
    ("M180 262 C196 242 206 276 220 258 S244 244 258 262 S288 270 318 256", TEAL),
    ("M180 318 C194 300 206 332 220 314 S246 300 262 318 S286 326 300 318", GRAPHITE),
]
# Small sizes: smoother, heavier lines that stay readable at 16 to 48 px.
LINES_SMALL = [
    ("M182 206 C210 192 240 220 270 204 S316 196 330 204", GRAPHITE),
    ("M182 262 C210 248 240 276 270 260 S306 254 318 256", TEAL),
    ("M182 318 C206 304 232 332 258 316 S290 314 300 318", GRAPHITE),
]
# The stylus, drawn pointing down at (0, 0) and placed where the last line ends, leaning right.
STYLUS_AT = "translate(300 318) rotate(35)"
BARREL = "M-11 -176 Q-11 -188 0 -188 Q11 -188 11 -176 V-38 H-11 Z"
BAND = "M-11 -64 H11 V-52 H-11 Z"
CONE = "M-11 -38 H11 L2.5 -2 Q0 1 -2.5 -2 Z"


def stylus(small=False):
    if small:
        return (f'<g transform="{STYLUS_AT}"><path d="{BARREL}" fill="{TEAL}" stroke="{PAPER}" stroke-width="6" '
                f'stroke-linejoin="round"/><path d="{CONE}" fill="{TIP_GREY}"/></g>')
    return (f'<g transform="{STYLUS_AT}">'
            f'<path d="{BARREL}" fill="{TEAL}" stroke="{PAPER}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="{BAND}" fill="{TEAL_BAND}"/>'
            f'<path d="{CONE}" fill="{TIP_GREY}"/>'
            f'<circle cx="0" cy="-3" r="2.6" fill="{POINT_INK}"/></g>')


def mark_body(small=False, tile=True, square=False, ids="m"):
    """The mark's SVG content in a 512-unit box. ids keeps gradient ids unique when marks share a file."""
    rx = "0" if square else "116"
    defs = (f'<defs><linearGradient id="{ids}tile" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{TILE_LIGHT}"/><stop offset="1" stop-color="{TILE_DEEP}"/></linearGradient></defs>')
    back = f'<rect width="512" height="512" rx="{rx}" fill="url(#{ids}tile)"/>' if tile else ""
    width = 20 if small else 13
    lines = "".join(f'<path d="{d}" stroke="{c}"/>' for d, c in (LINES_SMALL if small else LINES))
    return (defs + back +
            '<g transform="translate(256 262) scale(1.1) translate(-257 -256)">'
            f'<path d="{PAGE}" fill="{PAPER}"/><path d="{CORNER}" fill="{FOLD}"/>'
            f'<g fill="none" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{lines}</g>'
            f'{stylus(small)}</g>')


def mark_svg(small=False, square=False):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">\n'
            '<!-- MyPowerfulNotes: an A4 page with handwriting and a teal stylus, on a graphite tile. -->\n'
            + mark_body(small, square=square) + "\n</svg>\n")


def text_paths(parts, size, x, baseline, font_file="Inter-SemiBold.otf"):
    """Outlined text: parts is a list of (text, colour). Returns (svg, end x)."""
    font = TTFont(FONTS + font_file)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    kern = {}
    out = []
    for text, colour in parts:
        d = []
        for ch in text:
            name = cmap[ord(ch)]
            pen = SVGPathPen(glyphs)
            glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
            d.append(pen.getCommands())
            x += glyphs[name].width * scale
        out.append(f'<path fill="{colour}" d="{" ".join(d)}"/>')
    return "".join(out), x


def wordmark(white=False):
    dark = "#FFFFFF" if white else TEXT
    accent = "#FFFFFF" if white else TEAL
    words, end = text_paths([("My", dark), ("Powerful", accent), ("Notes", dark)], 250, 600, 345)
    width = int(end + 24)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 512" width="{width}" height="512">\n'
            f'<g transform="translate(16 16) scale(0.9375)">{mark_body(ids="w")}</g>\n{words}\n</svg>\n')


def run(args):
    subprocess.run(args, check=True)


def render(svg_text, path, w, h=None):
    tmp = "/tmp/mpn-brand.svg"
    open(tmp, "w").write(svg_text)
    args = ["rsvg-convert", "-w", str(w)] + (["-h", str(h)] if h else []) + [tmp, "-o", path]
    run(args)


def feature_graphic(path):
    sys.path.insert(0, os.path.join(ROOT, "source"))
    import art  # the site's own illustrations
    page = art.hero_page().replace('<svg viewBox="-6 -6 432 608"', '<svg x="600" y="40" width="370" height="535" viewBox="-6 -6 432 608"')
    page = page.replace('class="writing', 'class="done')
    logo = (f'<svg x="68" y="52" width="58" height="58" viewBox="0 0 512 512">{mark_body(ids="f")}</svg>')
    name, _ = text_paths([("My", TEXT), ("Powerful", TEAL), ("Notes", TEXT)], 26, 138, 90)
    head, _ = text_paths([("Handwritten notes on", TEXT)], 48, 68, 208, "InterDisplay-SemiBold.otf")
    head2, _ = text_paths([("proper pages, on your", TEXT)], 48, 68, 266, "InterDisplay-SemiBold.otf")
    head3, _ = text_paths([("PC and your tablet.", TEXT)], 48, 68, 324, "InterDisplay-SemiBold.otf")
    sub, _ = text_paths([("Windows and Android. Encrypted on your devices.", "#4A535C")], 21, 68, 384, "Inter-Regular.otf")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="500" viewBox="0 0 1024 500">
<defs><pattern id="d" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.1" fill="#D6D8D4"/></pattern></defs>
<rect width="1024" height="500" fill="#F3F3F0"/><rect width="1024" height="500" fill="url(#d)"/>
{logo}{name}{head}{head2}{head3}{sub}
<g transform="rotate(-2.5 785 300)">{page}</g>
</svg>'''
    render(svg, path, 1024, 500)


def windows_assets(folder):
    os.makedirs(folder, exist_ok=True)
    big = mark_svg()
    small = mark_svg(small=True)
    tmp = "/tmp/mpn-win"
    os.makedirs(tmp, exist_ok=True)

    def place(name, w, h, size, svg):
        render(svg, f"{tmp}/m.png", size)
        run(["convert", "-size", f"{w}x{h}", "xc:none", f"{tmp}/m.png", "-gravity", "center", "-composite",
             os.path.join(folder, name)])

    place("Square150x150Logo.scale-200.png", 300, 300, 184, big)
    place("Wide310x150Logo.scale-200.png", 620, 300, 184, big)
    place("SplashScreen.scale-200.png", 1240, 600, 260, big)
    place("Square44x44Logo.scale-200.png", 88, 88, 88, small)
    place("Square44x44Logo.targetsize-24_altform-unplated.png", 24, 24, 24, small)
    place("StoreLogo.png", 50, 50, 50, small)
    place("LockScreenLogo.scale-200.png", 48, 48, 44, small)
    place("Square44x44Logo.targetsize-48_altform-lightunplated.png", 48, 48, 48, small)
    # The .exe icon: the small mark up to 48 px, the full mark above.
    sizes = []
    for size in (16, 24, 32, 48, 64, 128, 256):
        render(small if size <= 48 else big, f"{tmp}/i{size}.png", size)
        sizes.append(f"{tmp}/i{size}.png")
    run(["convert", *sizes, os.path.join(folder, "AppIcon.ico")])


def main():
    files = {
        "mark.svg": mark_svg(),
        "mark-small.svg": mark_svg(small=True),
        "wordmark.svg": wordmark(),
        "wordmark-white.svg": wordmark(white=True),
    }
    for name, text in files.items():
        open(os.path.join(BRAND, name), "w").write(text)
    render(files["mark.svg"], os.path.join(BRAND, "logo-512.png"), 512)
    render(files["mark.svg"], os.path.join(BRAND, "logo-1024.png"), 1024)
    render(mark_svg(square=True), os.path.join(BRAND, "play-icon-512.png"), 512)
    render(files["wordmark.svg"], os.path.join(BRAND, "wordmark.png"), 590)
    feature_graphic(os.path.join(BRAND, "play-feature-graphic-1024x500.png"))
    windows_assets(os.path.join(BRAND, "windows-assets"))
    print("brand files made")


if __name__ == "__main__":
    main()
