import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const apiBase = process.env.VITE_API_BASE || 'http://backend:8000'

console.log(`[vite] VITE_API_BASE: ${apiBase}`)

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'log-proxy',
      configureServer() {
        console.log(`[vite] proxy /api -> ${apiBase}`)
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: true,
    port: 3000,
    proxy: {
      '/api': {
        target: apiBase,
        changeOrigin: true
      }
    }
  }
})
