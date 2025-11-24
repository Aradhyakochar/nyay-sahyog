import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './Auth.css'

declare global {
  interface Window {
    google: any
  }
}

function Login() {
  const [formData, setFormData] = useState({ username: '', password: '' })
  const [otpData, setOtpData] = useState({ user_id: 0, otp: '' })
  const [step, setStep] = useState<'login' | 'otp'>('login')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { fetchUser } = useAuth()
  const navigate = useNavigate()

  // GOOGLE LOGIN DISABLED - Commented out (not working, can be re-enabled later)
  // useEffect(() => {
  //   // Initialize Google Sign-In
  //   if (window.google) {
  //     window.google.accounts.id.initialize({
  //       client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID || '',
  //       callback: handleGoogleSignIn,
  //     })
  //     
  //     window.google.accounts.id.renderButton(
  //       document.getElementById('google-signin-button'),
  //       { theme: 'outline', size: 'large', width: '100%' }
  //     )
  //   }
  // }, [])

  // const handleGoogleSignIn = async (response: any) => {
  //   try {
  //     setLoading(true)
  //     setError('')
  //     
  //     const result = await api.post('/auth/oauth/google', { token: response.credential })
  //     
  //     if (result.data.access_token) {
  //       localStorage.setItem('token', result.data.access_token)
  //       api.defaults.headers.common['Authorization'] = `Bearer ${result.data.access_token}`
  //       await fetchUser()
  //       navigate('/')
  //     }
  //   } catch (err: any) {
  //     setError(err.response?.data?.error || 'Google sign-in failed')
  //   } finally {
  //     setLoading(false)
  //   }
  // }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (step === 'login') {
      setFormData({ ...formData, [e.target.name]: e.target.value })
    } else {
      setOtpData({ ...otpData, [e.target.name]: e.target.value })
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (step === 'login') {
        // Step 1: Request OTP
        console.log('🔐 Attempting login with:', { username: formData.username })
        console.log('📡 API Base URL:', api.defaults.baseURL)
        console.log('📡 Full URL will be:', `${api.defaults.baseURL}/auth/login`)
        
        const response = await api.post('/auth/login', formData)
        console.log('✅ Login response:', response.data)
        
        if (response.data.user_id) {
          setOtpData({ ...otpData, user_id: response.data.user_id })
          setStep('otp')
          
          // Show OTP (email disabled, always in response)
          if (response.data.otp) {
            alert(`Your OTP is: ${response.data.otp}\n\n(Email disabled - OTP shown here for development)`)
          } else {
            console.log('Login response:', response.data)
            setError('OTP not received. Please check backend console.')
          }
        } else {
          setError('Invalid response from server. Expected user_id.')
        }
      } else {
        // Step 2: Verify OTP
        console.log('Verifying OTP for user_id:', otpData.user_id)
        const response = await api.post('/auth/verify-otp', otpData)
        console.log('OTP verification response:', response.data)
        
        if (response.data.access_token) {
          const token = response.data.access_token
          console.log('🔑 Token received:', token.substring(0, 30) + '...')
          localStorage.setItem('token', token)
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`
          console.log('🔑 Authorization header set:', api.defaults.headers.common['Authorization']?.substring(0, 30) + '...')
          await fetchUser()
          navigate('/')
        } else {
          setError('No access token received from server')
        }
      }
    } catch (err: any) {
      console.error('❌ Login error:', err)
      console.error('Error details:', {
        message: err.message,
        code: err.code,
        response: err.response?.data,
        status: err.response?.status,
        config: err.config
      })
      
      let errorMsg = 'Authentication failed'
      
      if (err.code === 'ECONNREFUSED' || err.message?.includes('Network Error') || err.message?.includes('Failed to fetch')) {
        errorMsg = 'Cannot connect to backend server. Please ensure:\n1. Backend is running on http://localhost:5000\n2. Check browser console (F12) for details'
      } else if (err.response?.status === 401) {
        errorMsg = 'Invalid username or password. Try: client1 / password123 or admin / admin123'
      } else if (err.response?.status === 404) {
        errorMsg = 'API endpoint not found. Check if backend is running and proxy is configured correctly.'
      } else if (err.response?.data?.error) {
        errorMsg = err.response.data.error
      } else if (err.message) {
        errorMsg = err.message
      }
      
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Login to Nyay Sahyog</h2>
        {error && <div className="error">{error}</div>}
        
        {step === 'login' ? (
          <>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Username</label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Sending OTP...' : 'Continue'}
              </button>
            </form>
            
            {/* GOOGLE LOGIN DISABLED - Commented out (not working, can be re-enabled later) */}
            {/* <div className="auth-divider">
              <span>OR</span>
            </div>
            
            <div id="google-signin-button" style={{ marginBottom: '20px' }}></div> */}
          </>
        ) : (
          <form onSubmit={handleSubmit}>
            <p style={{ marginBottom: '20px', color: '#666' }}>
              We've sent a 6-digit OTP to your email. Please enter it below.
            </p>
            <div className="form-group">
              <label>Enter OTP</label>
              <input
                type="text"
                name="otp"
                value={otpData.otp}
                onChange={handleChange}
                placeholder="000000"
                maxLength={6}
                required
                style={{ textAlign: 'center', letterSpacing: '10px', fontSize: '24px' }}
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
            <button
              type="button"
              onClick={() => setStep('login')}
              className="btn btn-secondary"
              style={{ marginTop: '10px', width: '100%' }}
            >
              Back to Login
            </button>
          </form>
        )}
        
        <p className="auth-link">
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  )
}

export default Login

