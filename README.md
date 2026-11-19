# mypowerfulnotes.com

The MyPowerfulNotes website, deployed by Netlify from this repository.

- `site/` is what's published (plain HTML and CSS, no JavaScript). Netlify serves it as is; `netlify.toml` sets the
  publish folder, security headers and redirects.
- `source/` builds `site/`: `python3 source/build.py`. The pages, privacy policy and terms are in `build.py`;
  the illustrations of the app's screens are drawn by `art.py` (handwriting by `ink.py`). It needs Python 3 with
  fontTools, `rsvg-convert` and ImageMagick, and the Inter fonts.
- `brand/` holds the logo, wordmark, colours and store graphics (see `brand/README.md`).

After changing anything in `source/`, rebuild and commit `site/` too.
