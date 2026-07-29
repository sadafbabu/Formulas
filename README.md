# Formulas

Dark, compact A5 formula book for HSC / admission.

## Live site (Cloudflare)

**https://allformulas.pages.dev/**

## Catalog

- 620 formulas across Physics, Chemistry, and Higher Math
- 52 HSC/admission chapters
- Bengali memorization guidance on every formula
- Symbols, units, derivations, assumptions, related links, and worked questions
- KaTeX + mhchem reaction/structural notation
- HSC, engineering, medical, varsity, general, and importance filters
- Mobile-friendly: swipe pages, large touch targets, safe-area support

Canonical live site: **Cloudflare Pages** (`allformulas.pages.dev`).

- `?` → worked question and solution
- `Σ` → symbols, units, and values
- `ⓘ` → derivation and assumptions
- memory icon → recall technique
- Desktop = two-page spread; tablet/mobile = single page
- Use page edges or `←` / `→` to navigate

## Develop

```bash
npm install
npm run validate:content
npm run lint
npm run dev
npm run build
npx wrangler pages deploy dist --project-name allformulas
```

## Content

```
content/subjects/<subject>/chapters/<chapter>/
  meta.json
  formulas/<id>.json
```

Formula files are loaded with `import.meta.glob`; adding a JSON file automatically
adds it to the catalog and updates its chapter count. `npm run validate:content`
checks schemas, IDs, tags, relations, ordering, and every KaTeX/mhchem expression.
