import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// Determine API target based on environment
const getApiTarget = () => {
  // In Docker, use service name; locally, use localhost
  if (process.env.DOCKER_ENV === 'true') {
    return 'http://backend:5000'
  }
  return process.env.VITE_API_URL || 'http://localhost:5000'
}

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: [
      'localhost',
      '.ngrok.io',
      '.ngrok-free.app',
      '.ngrok-free.dev',
      '.ngrok.app'
    ],
    watch: {
      usePolling: true
    },
    proxy: {
      '/api': {
        target: getApiTarget(),
        changeOrigin: true,
        secure: false
      }
    }
  }
})

