import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import LocationAutocomplete from '../components/LocationAutocomplete'
import './Auth.css'

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'client',
    phone: '',
    address: '',
    city: '',
    state: '',
    pincode: '',
    specialization: '',
    experience_years: '',
    consultation_fee: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const providerRoles = ['advocate', 'mediator', 'arbitrator', 'notary', 'document_writer']
  const isProvider = providerRoles.includes(formData.role)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const registrationData = { ...formData }
      
      // Clean up empty strings and convert to proper types
      Object.keys(registrationData).forEach(key => {
        if (registrationData[key] === '') {
          delete registrationData[key]
        }
      })
      
      if (registrationData.experience_years) {
        registrationData.experience_years = parseInt(registrationData.experience_years)
      }
      if (registrationData.consultation_fee) {
        registrationData.consultation_fee = parseFloat(registrationData.consultation_fee)
      }

      console.log('📝 Registering user with data:', registrationData)
      const result = await register(registrationData)
      
      if (result.success) {
        console.log('✅ Registration successful')
        navigate('/')
      } else {
        console.error('❌ Registration failed:', result.error)
        setError(result.error || 'Registration failed. Please try again.')
      }
    } catch (err) {
      console.error('❌ Registration error:', err)
      setError('An unexpected error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Register for Nyay Sahyog</h2>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username *</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Email *</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Password *</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Full Name *</label>
            <input
              type="text"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Role *</label>
            <select name="role" value={formData.role} onChange={handleChange} required>
              <option value="client">Client</option>
              <option value="advocate">Advocate</option>
              <option value="mediator">Mediator</option>
              <option value="arbitrator">Arbitrator</option>
              <option value="notary">Notary</option>
              <option value="document_writer">Document Writer</option>
            </select>
          </div>
          <div className="form-group">
            <label>Phone</label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>Location (Auto-complete)</label>
            <LocationAutocomplete
              value={formData.address}
              onChange={(locationData) => {
                setFormData({
                  ...formData,
                  address: locationData.address || '',
                  city: locationData.city || '',
                  state: locationData.state || '',
                  pincode: locationData.pincode || ''
                })
              }}
              placeholder="Start typing your address..."
            />
          </div>
          <div className="form-group">
            <label>City</label>
            <input
              type="text"
              name="city"
              value={formData.city}
              onChange={handleChange}
              readOnly
              style={{ backgroundColor: '#f5f5f5' }}
            />
          </div>
          <div className="form-group">
            <label>State</label>
            <input
              type="text"
              name="state"
              value={formData.state}
              onChange={handleChange}
              readOnly
              style={{ backgroundColor: '#f5f5f5' }}
            />
          </div>
          <div className="form-group">
            <label>Pincode</label>
            <input
              type="text"
              name="pincode"
              value={formData.pincode}
              onChange={handleChange}
              readOnly
              style={{ backgroundColor: '#f5f5f5' }}
            />
          </div>
          {isProvider && (
            <>
              <h3>Provider Information</h3>
              <div className="form-group">
                <label>Specialization</label>
                <input
                  type="text"
                  name="specialization"
                  value={formData.specialization}
                  onChange={handleChange}
                  placeholder="e.g., Criminal Law, Family Law"
                />
              </div>
              <div className="form-group">
                <label>Experience (Years)</label>
                <input
                  type="number"
                  name="experience_years"
                  value={formData.experience_years}
                  onChange={handleChange}
                  min="0"
                />
              </div>
              <div className="form-group">
                <label>Consultation Fee (₹)</label>
                <input
                  type="number"
                  name="consultation_fee"
                  value={formData.consultation_fee}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                />
              </div>
            </>
          )}
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>
        <p className="auth-link">
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </div>
    </div>
  )
}

export default Register

