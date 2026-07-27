import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages base URL /Formulas/
export default defineConfig({
  base: process.env.VITE_BASE || '/Formulas/',
  plugins: [react()],
})
