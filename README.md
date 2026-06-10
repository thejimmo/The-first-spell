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

The hero currently shows an SVG recreation of the cover. To use the real cover image instead:

1. Add the file as `assets/cover.jpg` (or `.png`)
2. In `index.html`, change the `<img src="assets/cover.svg" ...>` in the hero to point at it
3. Update the `og:image` meta tag in `<head>` to match

## Preview locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy on GitHub Pages

1. Merge this branch into `main`
2. On GitHub: **Settings → Pages → Build and deployment**
3. Source: **Deploy from a branch**, branch `main`, folder `/ (root)`
4. The site appears at `https://thejimmo.github.io/The-first-spell/`

All asset paths are relative, so the project-page subpath works without changes.
