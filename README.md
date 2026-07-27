# Formulas

Dark, compact A5 formula book for HSC / admission.

## Live site (Cloudflare)

**https://formulas-book.frill-bison.workers.dev**

Temporary preview (claim within ~60 min to keep forever):  
https://dash.cloudflare.com/claim-preview?claimToken=33uHHel8jMAY10bD_XSHjaQwb9eCyL1bs1cCwfigivw

> First visit may show a short Cloudflare security check — continue in the browser.

## Current chapter

**তড়িত প্রবাহের চৌম্বক ক্রিয়া** — 14 formulas, with top-bar tag filters (HSC / Eng / Medical / …).

- **Σ** → symbols · units · values  
- **ⓘ** → how it derives  
- Click left/right edges to flip · `←` `→` keys  
- Desktop = two-page spread · tablet/mobile = single page  

## Develop

```bash
npm install
npm run dev
npm run build
npx wrangler deploy --temporary   # Cloudflare preview
```

## Content

```
content/subjects/<subject>/chapters/<chapter>/
  meta.json
  formulas/<id>.json
```
