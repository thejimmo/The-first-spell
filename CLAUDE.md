# The First Spell — Codebase & Session Guide

## Project overview
Promotion site for the book **"The First Spell — A Practical Magic System for the
Modern World"** by Jimi Knightley ([Amazon](https://www.amazon.com/dp/B0H4NDPFPC)).

A single-page static site: plain HTML + CSS + vanilla JS. **No framework, no build
step.** Live at **https://jimiknightley.com/**.

- Local root: `C:\Users\Jimi\Program\The-first-spell`
- GitHub: `https://github.com/thejimmo/The-first-spell` (public)
- Branch: `main` (the only branch; it is what GitHub Pages serves)

---

## Deployment

**Method:** GitHub Pages, served straight from `main` at the repo root. There is no
FTP and no CI build — pushing to `main` *is* the deploy. Pages rebuilds in ~30–60s.

Run from the project root:

```bash
python deploy.py                    # stage all → commit → push → wait for the Pages build
python deploy.py -m "Fix hero copy" # same, with a specific commit message
python deploy.py --no-wait          # push and return immediately
python deploy.py --status           # report Pages status + site HTTP code, deploy nothing
```

`deploy.py` refuses to run from any branch other than `main`, since Pages would not
pick it up. It reads GitHub API state through the `gh` CLI's stored auth — no tokens
or secrets live in the repo.

**Convention:** deploy after every completed task (no need to ask). There is
deliberately **no** PostToolUse auto-deploy hook here, unlike rabbla.se — a commit
per individual file edit would shred the git history. One task, one commit.

Custom domain is pinned by the `CNAME` file (`jimiknightley.com`). HTTPS certificate
is issued by GitHub and auto-renews. **Do not delete `CNAME`** — the site falls back
to `thejimmo.github.io/The-first-spell/` and the domain breaks.

`_config.yml` keeps tooling and docs (`deploy.py`, `README.md`, `CLAUDE.md`) out of
the published site. Add anything else that shouldn't be publicly fetchable there.

---

## File structure

```
/                       ← web root, served as-is by GitHub Pages
  index.html            ← the entire site (hero, #contract, #about, #listen sections)
  CNAME                 ← custom domain: jimiknightley.com. Do not remove.
  _config.yml           ← Pages/Jekyll config; excludes tooling from the built site
  deploy.py             ← commit + push + watch the Pages build
  README.md             ← public-facing repo readme
  CLAUDE.md             ← this file

css/
  style.css             ← all styles; design tokens in :root at the top

js/
  main.js               ← scroll-reveal (IntersectionObserver) + custom podcast player

assets/
  cover.jpg             ← real book cover used by the hero
  cover.png             ← og:image (social preview)
  cover.svg             ← hand-built fallback if cover.jpg is ever missing
  favicon.svg
  ai_radio.mp3          ← podcast episode played in the #listen section (~4.5 MB)
```

---

## Key patterns

- **Progressive enhancement.** `js/main.js` adds a `.js` class to `<html>`; the
  reveal-on-scroll styling hangs off that class, so with JS disabled all content is
  simply visible. The podcast player enhances a native `<audio>` element — keep it
  working without the custom controls.
- **Cover fallback.** The hero loads `assets/cover.jpg` and falls back to
  `assets/cover.svg` on error. Swapping the cover needs no code change.
- **Relative asset paths only.** This keeps the `thejimmo.github.io/The-first-spell/`
  project-page subpath working as a fallback URL.
- **Design tokens.** Colors and fonts are CSS custom properties in `:root`
  (`--bg`, `--gold`, `--serif`, …). Change them there, not inline.
  Palette: deep midnight blue + gold; Cormorant Garamond (serif) / Inter (sans).
- **Absolute URLs in meta.** `og:image` and `og:url` point at `https://jimiknightley.com/…`
  — update them if the domain ever changes.

---

## Preview locally

```bash
pip install rangehttpserver && python -m RangeHTTPServer 8000
# → http://localhost:8000
```

Use `RangeHTTPServer` rather than `python -m http.server`: the plain server ignores
Range requests, so seeking in the podcast audio breaks.

---

## Notes & gotchas

- Cache-bust changed CSS/JS by bumping the `?v=` query string on the tags in
  `index.html` — Pages sets long cache lifetimes and iOS Safari is stubborn about it.
- `ai_radio.mp3` is ~4.5 MB. Git handles it fine, but avoid committing new large
  binaries casually; there is no LFS configured.
- The repo has one branch by design. Work directly on `main` for small edits; for
  anything risky, branch, then merge to `main` before deploying.
- `python deploy.py --status` is the fastest way to tell whether what you see live
  matches what you pushed.
