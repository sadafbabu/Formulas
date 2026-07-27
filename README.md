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

## Live site (GitHub Pages)

**URL:** https://sadafbabu.github.io/Formulas/

If the link 404s, enable Pages once:

1. Open https://github.com/sadafbabu/Formulas/settings/pages
2. **Deploy from a branch**
3. Branch: `gh-pages` · folder: `/ (root)`
4. Save

(Or choose **GitHub Actions** as source — workflow is already in `.github/workflows/deploy.yml`.)
