import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Supports Cloudflare Pages (root '/') and GitHub Pages ('/Formulas/')
export default defineConfig({
  base: process.env.VITE_BASE || '/',
  plugins: [react()],
})
