import { defineConfig } from 'vite'
import solid from 'vite-plugin-solid'
import path from 'node:path'

export default defineConfig({
  plugins: [solid()],
  resolve: {
    alias: {
      "~bootstrap": path.resolve(__dirname, 'node_modules/bootstrap')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Django lives here internally
        changeOrigin: true,
      },
    },
  },
})
