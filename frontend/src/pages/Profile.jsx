import React, { useState, useEffect } from 'react'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import './Profile.css'

function Profile() {
  const { user, fetchUser } = useAuth()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({})
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const response = await api.get('/auth/profile')
      setProfile(response.data)
      setFormData({
        full_name: response.data.full_name || '',
        email: response.data.email || '',
        phone: response.data.phone || '',
        address: response.data.address || '',
        city: response.data.city || '',
        state: response.data.state || '',
        pincode: response.data.pincode || '',
        ...(response.data.provider_profile ? {
          specialization: response.data.provider_profile.specialization || '',
          experience_years: response.data.provider_profile.experience_years || '',
          bar_council_number: response.data.provider_profile.bar_council_number || '',
          qualification: response.data.provider_profile.qualification || '',
          bio: response.data.provider_profile.bio || '',
          consultation_fee: response.data.provider_profile.consultation_fee || '',
          hourly_rate: response.data.provider_profile.hourly_rate || ''
        } : {})
      })
      setError('')
    } catch (err) {
      setError('Failed to load profile')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    try {
      // Update user profile
      await api.put('/auth/profile', {
        full_name: formData.full_name,
        email: formData.email,
        phone: formData.phone,
        address: formData.address,
        city: formData.city,
        state: formData.state,
        pincode: formData.pincode
      })

      // Update provider profile if exists
      if (profile.provider_profile) {
        await api.put('/providers/my-profile', {
          specialization: formData.specialization,
          experience_years: parseInt(formData.experience_years) || 0,
          bar_council_number: formData.bar_council_number,
          qualification: formData.qualification,
          bio: formData.bio,
          consultation_fee: parseFloat(formData.consultation_fee) || 0,
          hourly_rate: parseFloat(formData.hourly_rate) || 0
        })
      }

      setSuccess('Profile updated successfully')
      setEditing(false)
      fetchProfile()
      fetchUser()
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update profile')
    }
  }

  if (loading) {
    return <div className="loading">Loading profile...</div>
  }

  if (!profile) {
    return <div className="error">Profile not found</div>
  }

  const isProvider = profile.provider_profile !== null

  return (
    <div className="container">
      <h1>My Profile</h1>
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="profile-card">
        <div className="profile-header">
          <h2>{profile.full_name}</h2>
          {!editing && (
            <button onClick={() => setEditing(true)} className="btn btn-primary">
              Edit Profile
            </button>
          )}
        </div>

        {editing ? (
          <form onSubmit={handleSubmit}>
            <h3>Personal Information</h3>
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
              <label>Phone</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Address</label>
              <textarea
                name="address"
                value={formData.address}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>City</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>State</label>
              <input
                type="text"
                name="state"
                value={formData.state}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Pincode</label>
              <input
                type="text"
                name="pincode"
                value={formData.pincode}
                onChange={handleChange}
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
                  <label>Bar Council Number</label>
                  <input
                    type="text"
                    name="bar_council_number"
                    value={formData.bar_council_number}
                    onChange={handleChange}
                  />
                </div>
                <div className="form-group">
                  <label>Qualification</label>
                  <textarea
                    name="qualification"
                    value={formData.qualification}
                    onChange={handleChange}
                  />
                </div>
                <div className="form-group">
                  <label>Bio</label>
                  <textarea
                    name="bio"
                    value={formData.bio}
                    onChange={handleChange}
                    rows="4"
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
                <div className="form-group">
                  <label>Hourly Rate (₹)</label>
                  <input
                    type="number"
                    name="hourly_rate"
                    value={formData.hourly_rate}
                    onChange={handleChange}
                    min="0"
                    step="0.01"
                  />
                </div>
              </>
            )}

            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setEditing(false)
                  fetchProfile()
                }}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="profile-info">
            <div className="info-section">
              <h3>Personal Information</h3>
              <div className="info-grid">
                <div className="info-item">
                  <strong>Username:</strong> {profile.username}
                </div>
                <div className="info-item">
                  <strong>Email:</strong> {profile.email}
                </div>
                <div className="info-item">
                  <strong>Role:</strong> {profile.role}
                </div>
                {profile.phone && (
                  <div className="info-item">
                    <strong>Phone:</strong> {profile.phone}
                  </div>
                )}
                {profile.city && (
                  <div className="info-item">
                    <strong>Location:</strong> {profile.city}, {profile.state}
                  </div>
                )}
                {profile.address && (
                  <div className="info-item">
                    <strong>Address:</strong> {profile.address}
                  </div>
                )}
                <div className="info-item">
                  <strong>Verified:</strong> {profile.is_verified ? 'Yes' : 'No'}
                </div>
              </div>
            </div>

            {isProvider && profile.provider_profile && (
              <div className="info-section">
                <h3>Provider Information</h3>
                <div className="info-grid">
                  {profile.provider_profile.specialization && (
                    <div className="info-item">
                      <strong>Specialization:</strong> {profile.provider_profile.specialization}
                    </div>
                  )}
                  <div className="info-item">
                    <strong>Experience:</strong> {profile.provider_profile.experience_years} years
                  </div>
                  {profile.provider_profile.bar_council_number && (
                    <div className="info-item">
                      <strong>Bar Council Number:</strong> {profile.provider_profile.bar_council_number}
                    </div>
                  )}
                  {profile.provider_profile.qualification && (
                    <div className="info-item">
                      <strong>Qualification:</strong> {profile.provider_profile.qualification}
                    </div>
                  )}
                  <div className="info-item">
                    <strong>Rating:</strong> ⭐ {profile.provider_profile.rating.toFixed(1)} ({profile.provider_profile.total_reviews} reviews)
                  </div>
                  <div className="info-item">
                    <strong>Consultation Fee:</strong> ₹{profile.provider_profile.consultation_fee}
                  </div>
                  {profile.provider_profile.hourly_rate > 0 && (
                    <div className="info-item">
                      <strong>Hourly Rate:</strong> ₹{profile.provider_profile.hourly_rate}
                    </div>
                  )}
                  {profile.provider_profile.bio && (
                    <div className="info-item full-width">
                      <strong>Bio:</strong>
                      <p>{profile.provider_profile.bio}</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Profile

