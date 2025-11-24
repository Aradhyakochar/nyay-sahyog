import React, { useState, useEffect } from 'react'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import './Bookings.css'

function Bookings() {
  const { user } = useAuth()
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedBooking, setSelectedBooking] = useState(null)
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')

  useEffect(() => {
    fetchBookings()
  }, [])

  const fetchBookings = async () => {
    try {
      const response = await api.get('/bookings')
      setBookings(response.data.bookings)
      setError('')
    } catch (err) {
      setError('Failed to load bookings')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const fetchMessages = async (bookingId) => {
    try {
      const response = await api.get('/bookings/messages', {
        params: { booking_id: bookingId }
      })
      setMessages(response.data.messages)
    } catch (err) {
      console.error(err)
    }
  }

  const handleStatusUpdate = async (bookingId, newStatus) => {
    try {
      await api.put(`/bookings/${bookingId}`, { status: newStatus })
      fetchBookings()
      alert('Booking status updated successfully')
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update booking')
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!newMessage.trim() || !selectedBooking) return

    try {
      const receiverId = user.role === 'client' 
        ? selectedBooking.provider_id 
        : selectedBooking.client_id

      await api.post('/bookings/messages', {
        booking_id: selectedBooking.id,
        receiver_id: receiverId,
        content: newMessage
      })
      setNewMessage('')
      fetchMessages(selectedBooking.id)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send message')
    }
  }

  const handleBookingClick = (booking) => {
    setSelectedBooking(booking)
    fetchMessages(booking.id)
  }

  const getStatusBadgeClass = (status) => {
    return `badge badge-${status}`
  }

  if (loading) {
    return <div className="loading">Loading bookings...</div>
  }

  const isProvider = user && ['advocate', 'mediator', 'arbitrator', 'notary', 'document_writer'].includes(user.role)

  return (
    <div className="container">
      <h1>My Bookings</h1>
      {error && <div className="error">{error}</div>}

      <div className="bookings-layout">
        <div className="bookings-list">
          {bookings.length === 0 ? (
            <div className="no-bookings">No bookings found</div>
          ) : (
            bookings.map(booking => (
              <div
                key={booking.id}
                className={`booking-card ${selectedBooking?.id === booking.id ? 'active' : ''}`}
                onClick={() => handleBookingClick(booking)}
              >
                <div className="booking-header">
                  <h3>
                    {isProvider ? booking.client?.full_name : booking.provider?.full_name}
                  </h3>
                  <span className={getStatusBadgeClass(booking.status)}>
                    {booking.status}
                  </span>
                </div>
                <div className="booking-info">
                  <p><strong>Service:</strong> {booking.service_type}</p>
                  <p><strong>Date:</strong> {new Date(booking.booking_date).toLocaleString()}</p>
                  <p><strong>Fee:</strong> ₹{booking.fee}</p>
                  {booking.location && <p><strong>Location:</strong> {booking.location}</p>}
                </div>
                {booking.description && (
                  <p className="booking-description">{booking.description}</p>
                )}
              </div>
            ))
          )}
        </div>

        {selectedBooking && (
          <div className="booking-detail">
            <div className="booking-detail-header">
              <h2>Booking Details</h2>
              {isProvider && selectedBooking.status === 'pending' && (
                <div className="status-actions">
                  <button
                    onClick={() => handleStatusUpdate(selectedBooking.id, 'confirmed')}
                    className="btn btn-success"
                  >
                    Confirm
                  </button>
                  <button
                    onClick={() => handleStatusUpdate(selectedBooking.id, 'cancelled')}
                    className="btn btn-danger"
                  >
                    Cancel
                  </button>
                </div>
              )}
              {isProvider && selectedBooking.status === 'confirmed' && (
                <button
                  onClick={() => handleStatusUpdate(selectedBooking.id, 'completed')}
                  className="btn btn-success"
                >
                  Mark as Completed
                </button>
              )}
            </div>

            <div className="detail-info">
              <p><strong>Client:</strong> {selectedBooking.client?.full_name}</p>
              <p><strong>Provider:</strong> {selectedBooking.provider?.full_name}</p>
              <p><strong>Service Type:</strong> {selectedBooking.service_type}</p>
              <p><strong>Date & Time:</strong> {new Date(selectedBooking.booking_date).toLocaleString()}</p>
              <p><strong>Duration:</strong> {selectedBooking.duration_minutes} minutes</p>
              <p><strong>Fee:</strong> ₹{selectedBooking.fee}</p>
              <p><strong>Status:</strong> <span className={getStatusBadgeClass(selectedBooking.status)}>{selectedBooking.status}</span></p>
              {selectedBooking.location && <p><strong>Location:</strong> {selectedBooking.location}</p>}
              {selectedBooking.meeting_link && (
                <p><strong>Meeting Link:</strong> <a href={selectedBooking.meeting_link} target="_blank" rel="noopener noreferrer">{selectedBooking.meeting_link}</a></p>
              )}
              {selectedBooking.description && (
                <div>
                  <strong>Description:</strong>
                  <p>{selectedBooking.description}</p>
                </div>
              )}
            </div>

            <div className="messages-section">
              <h3>Messages</h3>
              <div className="messages-list">
                {messages.map(message => (
                  <div
                    key={message.id}
                    className={`message ${message.sender_id === user?.id ? 'sent' : 'received'}`}
                  >
                    <div className="message-header">
                      <strong>{message.sender?.full_name}</strong>
                      <small>{new Date(message.created_at).toLocaleString()}</small>
                    </div>
                    <p>{message.content}</p>
                  </div>
                ))}
              </div>
              <form onSubmit={handleSendMessage} className="message-form">
                <textarea
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Type your message..."
                  rows="3"
                />
                <button type="submit" className="btn btn-primary">
                  Send Message
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Bookings

