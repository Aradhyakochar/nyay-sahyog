import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import api from '../services/api'
import { User } from '../types'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (username: string, password: string) => Promise<{ success: boolean; error?: string }>
  register: (userData: RegisterData) => Promise<{ success: boolean; error?: string }>
  logout: () => void
  fetchUser: () => Promise<void>
}

interface RegisterData {
  username: string
  email: string
  password: string
  full_name: string
  role: string
  phone?: string
  city?: string
  state?: string
  pincode?: string
  specialization?: string
  experience_years?: number
  consultation_fee?: number
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token')
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUser()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUser = async (): Promise<void> => {
    try {
      const token = localStorage.getItem('token')
      console.log('📡 Fetching user profile...')
      console.log('🔑 Token exists:', !!token)
      console.log('🔑 Token preview:', token ? token.substring(0, 20) + '...' : 'none')
      console.log('🔑 Authorization header:', api.defaults.headers.common['Authorization'] ? 'set' : 'not set')
      
      const response = await api.get('/auth/profile')
      console.log('✅ Profile response:', response.data)
      setUser(response.data)
    } catch (error: any) {
      console.error('❌ Error fetching profile:', error)
      console.error('Error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message,
        headers: error.config?.headers
      })
      console.error('Full error response:', error.response?.data)
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    } finally {
      setLoading(false)
    }
  }

  const login = async (username: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await api.post('/auth/login', { username, password })
      const { access_token, user } = response.data
      localStorage.setItem('token', access_token)
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      setUser(user)
      return { success: true }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      }
    }
  }

  const register = async (userData: RegisterData): Promise<{ success: boolean; error?: string }> => {
    try {
      console.log('📡 Sending registration request to:', api.defaults.baseURL + '/auth/register')
      console.log('📦 Registration data:', userData)
      
      const response = await api.post('/auth/register', userData)
      console.log('✅ Registration response:', response.data)
      
      const { access_token, user } = response.data
      
      if (!access_token) {
        console.error('❌ No access token in response')
        return { 
          success: false, 
          error: 'Registration successful but login failed. Please try logging in.' 
        }
      }
      
      localStorage.setItem('token', access_token)
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      setUser(user)
      return { success: true }
    } catch (error: any) {
      console.error('❌ Registration error:', error)
      console.error('❌ Error response:', error.response?.data)
      console.error('❌ Error status:', error.response?.status)
      
      const errorMsg = error.response?.data?.error || error.message || 'Registration failed'
      
      // More specific error messages
      if (error.code === 'ECONNREFUSED' || error.message?.includes('Network Error')) {
        return { 
          success: false, 
          error: 'Cannot connect to server. Make sure backend is running on http://localhost:5000' 
        }
      }
      
      if (error.response?.status === 400) {
        return { 
          success: false, 
          error: errorMsg || 'Invalid registration data. Please check all fields.' 
        }
      }
      
      if (error.response?.status === 500) {
        return { 
          success: false, 
          error: 'Server error. Please try again later.' 
        }
      }
      
      return { 
        success: false, 
        error: errorMsg 
      }
    }
  }

  const logout = (): void => {
    localStorage.removeItem('token')
    delete api.defaults.headers.common['Authorization']
    setUser(null)
  }

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    fetchUser
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

