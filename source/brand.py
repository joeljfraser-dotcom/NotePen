#!/usr/bin/env python3
"""Makes every file in brand/ from one description of the mark (deep teal, Nov 2026).

The mark: an A4 page with a handwritten M, finished by a pencil leaning right, on a rounded deep teal tile.
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
TILE_LIGHT = "#14857C"
TILE_DEEP = "#0B4F4A"
TEAL = "#0E6E66"          # the accent: the M, links, "Powerful"
TEAL_LIGHT = "#13897F"
TEXT = "#1B1B1B"
PAPER = "#FFFDF8"
FOLD = "#E4E1D8"
RULE = "#E2E4E6"
PENCIL = "#FFB02E"
ERASER = "#F06A6A"
WOOD = "#F6E3C4"
LEAD = "#22303F"

PAGE = "M150 108 H310 L364 162 V386 Q364 404 346 404 H168 Q150 404 150 386 V126 Q150 108 168 108 Z"
CORNER = "M310 108 V146 Q310 162 326 162 H364 Z"
M_STROKE = ("M186 336 C192 300 198 246 210 214 C214 204 222 206 224 216 C230 248 236 288 246 310 "
            "C250 318 256 318 260 308 C270 280 278 238 288 214 C292 204 300 206 302 216 "
            "C306 246 308 296 316 330 C320 344 332 344 340 330")
# The pencil, drawn pointing down at (0, 0) and placed where the M ends, leaning right.
PENCIL_AT = "translate(344 322) rotate(35)"
BODY = "M-8 -150 H8 Q15 -150 15 -143 V-32 H-15 V-143 Q-15 -150 -8 -150 Z"
CAP = "M-8 -150 H8 Q15 -150 15 -143 V-130 H-15 V-143 Q-15 -150 -8 -150 Z"
TIP = "M-15 -32 L15 -32 L0 6 Z"
POINT = "M-5.3 -6 L5.3 -6 L0 6 Z"


def pencil(small=False):
    if small:
        # Fewer details for 16 to 32 px: no eraser, a heavier outline.
        return (f'<g transform="{PENCIL_AT}">'
                f'<path d="{BODY}" fill="{PENCIL}" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>'
                f'<path d="{TIP}" fill="{WOOD}" stroke="{LEAD}" stroke-width="7" stroke-linejoin="round"/>'
                f'<path d="{POINT}" fill="{LEAD}"/></g>')
    return (f'<g transform="{PENCIL_AT}">'
            f'<path d="{BODY}" fill="{PENCIL}"/><path d="{CAP}" fill="{ERASER}"/>'
            f'<path d="M-15 -130 H15" stroke="#FFFFFF" stroke-width="4"/>'
            f'<path d="{BODY}" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="{TIP}" fill="{WOOD}" stroke="{LEAD}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="{POINT}" fill="{LEAD}"/></g>')


def mark_body(small=False, tile=True, square=False, ids="m"):
    """The mark's SVG content in a 512-unit box. ids keeps gradient ids unique when marks share a file."""
    rx = "0" if square else "116"
    rules = "" if small else (
        f'<g stroke="{RULE}" stroke-width="5" stroke-linecap="round">'
        + "".join(f'<line x1="176" y1="{y}" x2="338" y2="{y}"/>' for y in (214, 262, 310, 358)) + "</g>")
    defs = (f'<defs><linearGradient id="{ids}tile" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{TILE_LIGHT}"/><stop offset="1" stop-color="{TILE_DEEP}"/></linearGradient>'
            f'<linearGradient id="{ids}ink" x1="0" y1="1" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{TEAL_LIGHT}"/></linearGradient></defs>')
    back = f'<rect width="512" height="512" rx="{rx}" fill="url(#{ids}tile)"/>' if tile else ""
    return (defs + back +
            '<g transform="translate(256 262) scale(1.1) translate(-257 -256)">'
            f'<path d="{PAGE}" fill="{PAPER}"/><path d="{CORNER}" fill="{FOLD}"/>{rules}'
            f'<path d="{M_STROKE}" fill="none" stroke="url(#{ids}ink)" stroke-width="{28 if small else 20}" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
            f'{pencil(small)}</g>')


def mark_svg(small=False, square=False):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">\n'
            '<!-- MyPowerfulNotes: an A4 page with a handwritten M, finished by a pencil, on a deep teal tile. -->\n'
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
    sub, _ = text_paths([("Windows and Android. Encrypted on your devices.", "#4D5865")], 21, 68, 384, "Inter-Regular.otf")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="500" viewBox="0 0 1024 500">
<defs><pattern id="d" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.1" fill="#CFD8D6"/></pattern></defs>
<rect width="1024" height="500" fill="#F2F4F3"/><rect width="1024" height="500" fill="url(#d)"/>
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
