# MyPowerfulNotes brand

## The mark
An A4 page with three lines of handwriting (graphite, teal, graphite) and a teal stylus finishing the last line, on a rounded graphite tile (Nov 2026). The small version (`mark-small.svg`, for 16 to 48 px) has smoother, heavier lines.
The page and pen stroke say what the app is: handwriting on proper pages. The earlier blue tile had a four-point
spark, dropped because it looked too like Gemini's.

Every file here is made by `source/brand.py` (run from the repo root, then `source/build.py` for the site).
Change the mark or colours there, not in the files.

| File | Use |
|---|---|
| `mark.svg` | The logo (rounded tile). Use at 32 px and up. |
| `mark-small.svg` | Simplified (no ruled lines, thicker M) for 16 to 32 px: favicons, small icons. |
| `wordmark.svg`, `wordmark.png` | Logo with the name, for light backgrounds. Text is outlined, so no font is needed. |
| `wordmark-white.svg` | For dark or blue backgrounds. |
| `logo-512.png`, `logo-1024.png` | The mark as PNG with transparent corners. |
| `play-icon-512.png` | Google Play hi-res icon (square, full bleed; Play rounds it). |
| `play-feature-graphic-1024x500.png` | Google Play feature graphic. |
| `windows-assets/` | Windows app tiles and icons, named as Visual Studio expects. |

The Android launcher icon (adaptive, with a themed version) is drawn from the same shapes in
`app/src/main/res/drawable/ic_launcher_*.xml` in the Android repo.

## Colours
| Name | Hex | Use |
|---|---|---|
| Teal | `#0E6E66` | The accent: buttons, links, the stylus, the middle line, the "Powerful" in the name |
| Teal hover | `#0B4F4A` | Button hover |
| Graphite tile | `#3A424C` → `#1A1F25` | The tile gradient |
| Graphite | `#1E242B` | Text, the name, the site footer and the testing banner |
| Handwriting | `#26323F` | The graphite lines on the page |
| Stylus | `#0E6E66` | Band `#E9F5F3`, tip `#C9D3D2` |
| Paper | `#FFFDF8` | The page in the mark (fold `#E4E1D8`) |
| Secondary text | `#4A535C` | |
| Desk | `#F3F3F0` | Warm grey behind paper: the hero and tinted sections |
