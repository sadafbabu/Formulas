# Formulas

A5 formula book (black theme) — screen spreads + future A4-landscape print.

## What’s in this sample

One **average template spread** for Physics / Newtonian Mechanics:

- A5 pages paired as a landscape spread on desktop
- Single-page stack on mobile
- Tags (`HSC`, `Eng Admission`, `Medical`, …) beside each formula
- **বিস্তারিত →** opens a derivation page (`/formula/:id`)
- Search + tag filter

## Develop

```bash
npm install
npm run dev
```

```bash
npm run build
npm run preview
```

## Content layout

New formulas = data only (no UI changes):

```
content/
  tags.json
  subjects/<subject>/
    meta.json
    formulas/<id>.json
```

Each formula JSON: `title`, `titleBn`, `latex`, `summary`, `tags`, `derivation`.

## Stack

Vite · React · TypeScript · KaTeX · React Router
