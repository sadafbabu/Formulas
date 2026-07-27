import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages project site: https://<user>.github.io/Formulas/
export default defineConfig({
  base: '/Formulas/',
  plugins: [react()],
})
