# Formulas

Dark, compact A5 physics/chemistry formula book (React 19 + Vite + TypeScript SPA, KaTeX for math). Deployed to Cloudflare Workers (`wrangler.toml` + `worker.js`) and GitHub Pages (`.github/workflows/deploy.yml`).

## Cursor Cloud specific instructions

- Frontend-only SPA; there is no backend/database. Everything runs in the browser via the Vite dev server.
- Node 22 is the expected runtime (matches CI in `.github/workflows/deploy.yml`).
- Standard commands live in `package.json` scripts: `npm run dev` (Vite dev server on port 5173), `npm run lint` (oxlint), `npm run build` (`tsc -b` + `vite build`). Lint currently emits two `exhaustive-deps` warnings in `HintPopover.tsx`; these are pre-existing and non-blocking.
- `npm run dev -- --host` is useful to expose the dev server for browser testing.
- Content is data-driven: chapters/formulas live under `content/subjects/<subject>/chapters/<chapter>/` and are loaded via `src/data/catalog.ts`. Add/edit JSON there to change formulas.
- `vite.config.ts` reads `VITE_BASE` (root `/` for Cloudflare, `/Formulas/` for GitHub Pages). Leave unset for local dev.
