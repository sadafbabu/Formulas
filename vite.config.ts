import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Supports Cloudflare Pages (root '/') and GitHub Pages ('/Formulas/')
export default defineConfig({
  base: process.env.VITE_BASE || '/',
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/katex')) return 'katex'
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom') || id.includes('node_modules/react-router')) {
            return 'react-vendor'
          }
        },
      },
    },
  },
})
