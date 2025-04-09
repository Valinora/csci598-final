import { defineConfig } from 'vite'
import solid from 'vite-plugin-solid'
import { resolve } from 'node:path'

export default defineConfig({
  plugins: [solid()],
  resolve: {
    alias: {
      "~bootstrap": resolve(__dirname, 'node_modules/bootstrap')
    }
  },
  build: {
        rollupOptions: {
            input: {
                index: resolve(__dirname, 'index.html'),
                about: resolve(__dirname, 'about.html')
            },
            output: {
                entryFileNames: `assets/[name].js`,
                assetFileNames: `assets/[name].[ext]`
            }
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
