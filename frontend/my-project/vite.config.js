import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  define: {
    // 如果环境不支持 structuredClone，则使用 JSON 方式来模拟
    structuredClone: globalThis.structuredClone || ((value) => JSON.parse(JSON.stringify(value))),
  },
})
