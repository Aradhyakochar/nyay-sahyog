import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

// Use proxy for local development (Vite proxy forwards /api to backend)
// In production or when explicitly set, use full URL
// Default to /api to use Vite proxy (recommended for local dev)
const envUrl = import.meta.env.VITE_API_URL
// If VITE_API_URL is empty or not set, use proxy (/api)
// If it's a full URL (starts with http), use it directly
// IMPORTANT: For local dev, use '/api' to leverage Vite proxy
const API_BASE_URL = envUrl && envUrl.trim() && envUrl.startsWith('http') 
  ? envUrl 
  : '/api'  // This will be proxied to http://localhost:5000 by Vite

// Debug logging (remove in production)
if (import.meta.env.DEV) {
  console.log('🔧 API Configuration:', {
    baseURL: API_BASE_URL,
    envVar: envUrl || '(not set)',
    proxy: API_BASE_URL === '/api' ? '✅ Using Vite proxy' : '❌ Using direct URL'
  })
}

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if available
const token = localStorage.getItem('token')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

