import { defineConfig } from 'vite'
import solid from 'vite-plugin-solid'
import path from 'node:path'

export default defineConfig({
  plugins: [solid()],
  resolve: {
    alias: {
      "~bootstrap": path.resolve(__dirname, 'node_modules/bootstrap')
    }
  }
})
