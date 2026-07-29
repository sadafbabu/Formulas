# Formulas

Dark, compact A5 formula book for HSC / admission.

## Live site

**GitHub Pages:** https://sadafbabu.github.io/Formulas/

**Cloudflare preview** (temporary Workers deploy):

```bash
npm run build
npx wrangler deploy --temporary
```

> First visit on Cloudflare may show a short security check — continue in the browser.

## Current chapter

**তড়িত প্রবাহের চৌম্বক ক্রিয়া** — formulas with top-bar tag filters (HSC / Eng / Medical / …).

- **Σ** → symbols · units · values
- **ⓘ** → how it derives
- Click left/right edges, swipe (mobile), or `←` `→` keys to flip
- Desktop = two-page spread · tablet/mobile = single page

## Develop

```bash
npm install
npm run dev
npm run build
```

### Deploy

- **GitHub Pages** — push to `main` runs `.github/workflows/deploy.yml` (builds with `VITE_BASE=/Formulas/` and publishes the `gh-pages` branch).
- **Cloudflare Workers** — `npx wrangler deploy` (or `--temporary` for a preview URL).

```bash
# Local Pages-style build (correct asset base)
VITE_BASE=/Formulas/ npm run build
```

## Content

```
content/subjects/<subject>/chapters/<chapter>/
  meta.json
  formulas/<id>.json
```
