import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  define: {
    'process.env.NODE_ENV': JSON.stringify('development'), // 替换 process.env.NODE_ENV 为 'development'
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // 设置路径别名
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 后端地址
        changeOrigin: true, // 允许跨域
        rewrite: (path) => path.replace(/^\/api/, ''), // 可选：重写路径
      },
    },
  },
});