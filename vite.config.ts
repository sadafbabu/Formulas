import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Cloudflare / local root deploy. Override with VITE_BASE=/Formulas/ for GitHub Pages.
export default defineConfig({
  base: process.env.VITE_BASE || '/',
  plugins: [react()],
})
