# Formulas

A5 formula book (dark grey, slideshow-style) for HSC / admission.

## Current chapter

**তড়িত প্রবাহের চৌম্বক ক্রিয়া** — Magnetic Effects of Current

Each formula has:
- short name + one-line note
- tags (HSC / Eng Admission / Medical / …)
- **Σ icon** → symbols, units, constant values
- **ⓘ icon** → how it comes + full derivation page

## Develop

```bash
npm install
npm run dev
```

## Add content

```
content/subjects/<subject>/chapters/<chapter>/
  meta.json
  formulas/<id>.json
```

Formula JSON fields: `title`, `titleBn`, `latex`, `summary`, `tags`, `symbols[]`, `derivation`.

## Stack

Vite · React · TypeScript · KaTeX · React Router
