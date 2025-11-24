import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import './ProviderDetail.css'

function ProviderDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [provider, setProvider] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showBookingForm, setShowBookingForm] = useState(false)
  const [bookingData, setBookingData] = useState({
    booking_date: '',
    duration_minutes: 60,
    description: '',
    location: '',
    meeting_link: ''
  })

  useEffect(() => {
    fetchProvider()
  }, [id])

  const fetchProvider = async () => {
    try {
      const response = await api.get(`/providers/${id}`)
      setProvider(response.data)
      setError('')
    } catch (err) {
      setError('Failed to load provider details')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleBookingSubmit = async (e) => {
    e.preventDefault()
    if (!user) {
      navigate('/login')
      return
    }

    if (user.role !== 'client') {
      setError('Only clients can book consultations')
      return
    }

    if (!provider || !provider.user_id) {
      setError('Provider information is missing')
      return
    }

    try {
      // Convert datetime-local to ISO 8601 format
      let bookingDateISO = bookingData.booking_date
      if (bookingDateISO && !bookingDateISO.includes('T')) {
        // If it's just a date, add time
        bookingDateISO = bookingDateISO + 'T00:00:00'
      }
      // Ensure it's in ISO format with timezone
      if (bookingDateISO && !bookingDateISO.endsWith('Z') && !bookingDateISO.includes('+')) {
        // Convert local datetime to ISO string
        const date = new Date(bookingDateISO)
        bookingDateISO = date.toISOString()
      }

      const bookingPayload = {
        provider_id: provider.user_id,
        booking_date: bookingDateISO,
        duration_minutes: bookingData.duration_minutes || 60,
        fee: provider.consultation_fee || 0,
        service_type: 'consultation',
        description: bookingData.description || '',
        location: bookingData.location || '',
        meeting_link: bookingData.meeting_link || ''
      }

      console.log('📅 Creating booking with payload:', bookingPayload)
      const response = await api.post('/bookings', bookingPayload)
      console.log('✅ Booking created:', response.data)
      
      alert('Booking request created successfully!')
      setShowBookingForm(false)
      setBookingData({
        booking_date: '',
        duration_minutes: 60,
        description: '',
        location: '',
        meeting_link: ''
      })
      navigate('/bookings')
    } catch (err) {
      console.error('❌ Booking error:', err)
      console.error('❌ Error response:', err.response?.data)
      const errorMsg = err.response?.data?.error || err.message || 'Failed to create booking'
      setError(errorMsg)
      
      // More specific error messages
      if (err.response?.status === 401) {
        setError('Please log in to create a booking')
        navigate('/login')
      } else if (err.response?.status === 403) {
        setError('Only clients can create bookings')
      } else if (err.response?.status === 400) {
        setError(errorMsg || 'Invalid booking data. Please check all fields.')
      }
    }
  }

  if (loading) {
    return <div className="loading">Loading provider details...</div>
  }

  if (!provider) {
    return <div className="error">Provider not found</div>
  }

  return (
    <div className="container">
      <div className="provider-detail">
        <div className="provider-main">
          <div className="provider-header-detail">
            <div>
              <h1>{provider.user?.full_name}</h1>
              {provider.is_verified && (
                <span className="badge badge-verified">Verified</span>
              )}
            </div>
            <p className="provider-role-detail">{provider.user?.role}</p>
          </div>

          {provider.specialization && (
            <div className="detail-section">
              <h3>Specialization</h3>
              <p>{provider.specialization}</p>
            </div>
          )}

          {provider.bio && (
            <div className="detail-section">
              <h3>About</h3>
              <p>{provider.bio}</p>
            </div>
          )}

          <div className="detail-grid">
            <div className="detail-item">
              <strong>Experience:</strong> {provider.experience_years} years
            </div>
            <div className="detail-item">
              <strong>Rating:</strong> ⭐ {provider.rating.toFixed(1)} ({provider.total_reviews} reviews)
            </div>
            <div className="detail-item">
              <strong>Consultation Fee:</strong> ₹{provider.consultation_fee}
            </div>
            {provider.hourly_rate > 0 && (
              <div className="detail-item">
                <strong>Hourly Rate:</strong> ₹{provider.hourly_rate}
              </div>
            )}
            {provider.user?.city && (
              <div className="detail-item">
                <strong>Location:</strong> {provider.user.city}, {provider.user.state}
              </div>
            )}
            {provider.bar_council_number && (
              <div className="detail-item">
                <strong>Bar Council Number:</strong> {provider.bar_council_number}
              </div>
            )}
          </div>

          {provider.qualification && (
            <div className="detail-section">
              <h3>Qualifications</h3>
              <p>{provider.qualification}</p>
            </div>
          )}

          {user && user.role === 'client' && (
            <div className="booking-section">
              {!showBookingForm ? (
                <button
                  onClick={() => setShowBookingForm(true)}
                  className="btn btn-primary"
                >
                  Book Consultation
                </button>
              ) : (
                <div className="booking-form-card">
                  <h3>Book Consultation</h3>
                  {error && <div className="error">{error}</div>}
                  <form onSubmit={handleBookingSubmit}>
                    <div className="form-group">
                      <label>Date & Time *</label>
                      <input
                        type="datetime-local"
                        name="booking_date"
                        value={bookingData.booking_date}
                        onChange={(e) => setBookingData({ ...bookingData, booking_date: e.target.value })}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Duration (minutes)</label>
                      <input
                        type="number"
                        name="duration_minutes"
                        value={bookingData.duration_minutes}
                        onChange={(e) => setBookingData({ ...bookingData, duration_minutes: parseInt(e.target.value) })}
                        min="15"
                        step="15"
                      />
                    </div>
                    <div className="form-group">
                      <label>Description</label>
                      <textarea
                        name="description"
                        value={bookingData.description}
                        onChange={(e) => setBookingData({ ...bookingData, description: e.target.value })}
                        placeholder="Brief description of your legal issue..."
                      />
                    </div>
                    <div className="form-group">
                      <label>Location (for in-person)</label>
                      <input
                        type="text"
                        name="location"
                        value={bookingData.location}
                        onChange={(e) => setBookingData({ ...bookingData, location: e.target.value })}
                        placeholder="Office address or meeting location"
                      />
                    </div>
                    <div className="form-group">
                      <label>Meeting Link (for online)</label>
                      <input
                        type="url"
                        name="meeting_link"
                        value={bookingData.meeting_link}
                        onChange={(e) => setBookingData({ ...bookingData, meeting_link: e.target.value })}
                        placeholder="Zoom, Google Meet, etc."
                      />
                    </div>
                    <div className="form-group">
                      <strong>Total Fee: ₹{provider.consultation_fee}</strong>
                    </div>
                    <div className="form-actions">
                      <button type="submit" className="btn btn-primary">
                        Confirm Booking
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowBookingForm(false)}
                        className="btn btn-secondary"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </div>
          )}

          {provider.reviews && provider.reviews.length > 0 && (
            <div className="reviews-section">
              <h3>Reviews</h3>
              {provider.reviews.map(review => (
                <div key={review.id} className="review-card">
                  <div className="review-header">
                    <strong>{review.client?.full_name}</strong>
                    <span>⭐ {review.rating}/5</span>
                  </div>
                  {review.comment && <p>{review.comment}</p>}
                  <small>{new Date(review.created_at).toLocaleDateString()}</small>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ProviderDetail

