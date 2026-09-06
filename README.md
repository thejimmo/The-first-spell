# The First Spell — promotion site

Promotion site for **"The First Spell — A Practical Magic System for the Modern World"** by Jimi Knightley, available on [Amazon](https://www.amazon.com/dp/B0H4NDPFPC).

A single-page static site: plain HTML + CSS + a little vanilla JS. No build step.

## Structure

- `index.html` — the whole site
- `css/style.css` — styles
- `js/main.js` — scroll-reveal animations (site works fine with JS disabled)
- `assets/cover.svg` — recreated cover artwork
- `assets/favicon.svg` — favicon

## Using the real cover

The hero loads `assets/cover.jpg` and automatically falls back to the SVG
recreation (`assets/cover.svg`) if the file doesn't exist. To show the real
cover, just add the image as `assets/cover.jpg` — no code changes needed.

## Preview locally

```bash
pip install rangehttpserver && python3 -m RangeHTTPServer 8000
# then open http://localhost:8000
# (RangeHTTPServer instead of http.server so seeking in the podcast audio works)
```

## Deploy

The site is served by GitHub Pages from the `main` branch at the repo root, so
pushing to `main` is the deploy. Rebuilds take ~30-60 seconds.

```bash
python deploy.py                    # stage, commit, push, wait for the Pages build
python deploy.py -m "Fix hero copy" # with a specific commit message
python deploy.py --status           # report build status without deploying
```

Live at `https://jimiknightley.com/` (custom domain via the `CNAME` file; the
fallback URL is `https://thejimmo.github.io/The-first-spell/`). All asset paths
are relative, so the project-page subpath works without changes.
