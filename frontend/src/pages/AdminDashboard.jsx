import React, { useState, useEffect } from 'react'
import api from '../services/api'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './AdminDashboard.css'

function AdminDashboard() {
  const [analytics, setAnalytics] = useState(null)
  const [users, setUsers] = useState([])
  const [providers, setProviders] = useState([])
  const [bookings, setBookings] = useState([])
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchData()
  }, [activeTab])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError('')
      console.log(`📊 Fetching admin data for tab: ${activeTab}`)
      
      if (activeTab === 'overview') {
        console.log('📡 Requesting /admin/analytics...')
        const response = await api.get('/admin/analytics')
        console.log('✅ Analytics response:', response.data)
        setAnalytics(response.data)
      } else if (activeTab === 'users') {
        console.log('📡 Requesting /admin/users...')
        const response = await api.get('/admin/users')
        console.log('✅ Users response:', response.data)
        setUsers(response.data.users || [])
      } else if (activeTab === 'providers') {
        console.log('📡 Requesting /admin/providers...')
        const response = await api.get('/admin/providers')
        console.log('✅ Providers response:', response.data)
        setProviders(response.data.providers || [])
      } else if (activeTab === 'bookings') {
        console.log('📡 Requesting /admin/bookings...')
        const response = await api.get('/admin/bookings')
        console.log('✅ Bookings response:', response.data)
        setBookings(response.data.bookings || [])
      }
    } catch (err) {
      console.error('❌ Admin dashboard error:', err)
      console.error('Error details:', {
        message: err.message,
        status: err.response?.status,
        data: err.response?.data,
        config: err.config
      })
      
      let errorMsg = 'Failed to load data'
      if (err.response?.status === 401) {
        errorMsg = 'Authentication required. Please log in again.'
      } else if (err.response?.status === 403) {
        errorMsg = 'Access denied. Admin role required.'
      } else if (err.response?.status === 404) {
        errorMsg = 'API endpoint not found. Check backend is running.'
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

  const handleVerify = async (userId, verify) => {
    try {
      await api.put(`/admin/users/${userId}/verify`, { verify })
      fetchData()
      alert(`User ${verify ? 'verified' : 'unverified'} successfully`)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update verification')
    }
  }

  const handleActivate = async (userId, activate) => {
    try {
      await api.put(`/admin/users/${userId}/activate`, { activate })
      fetchData()
      alert(`User ${activate ? 'activated' : 'deactivated'} successfully`)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update activation')
    }
  }

  if (loading && activeTab === 'overview' && !analytics) {
    return (
      <div className="container">
        <div className="loading">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div className="container">
      <h1>Admin Dashboard</h1>
      {error && (
        <div className="error" style={{ padding: '15px', marginBottom: '20px', backgroundColor: '#fee', border: '1px solid #fcc', borderRadius: '4px' }}>
          <strong>Error:</strong> {error}
          <br />
          <small>Check browser console (F12) for details</small>
        </div>
      )}
      {loading && <div className="loading">Loading {activeTab}...</div>}

      <div className="admin-tabs">
        <button
          className={activeTab === 'overview' ? 'active' : ''}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={activeTab === 'users' ? 'active' : ''}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
        <button
          className={activeTab === 'providers' ? 'active' : ''}
          onClick={() => setActiveTab('providers')}
        >
          Providers
        </button>
        <button
          className={activeTab === 'bookings' ? 'active' : ''}
          onClick={() => setActiveTab('bookings')}
        >
          Bookings
        </button>
      </div>

      {activeTab === 'overview' && (
        <>
          {!analytics && !loading && (
            <div className="error">No analytics data available. Check backend console for errors.</div>
          )}
          {analytics && (
        <div className="dashboard-overview">
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Users</h3>
              <p className="stat-value">{analytics.users.total}</p>
              <p className="stat-detail">Clients: {analytics.users.clients} | Providers: {analytics.users.providers}</p>
            </div>
            <div className="stat-card">
              <h3>Verified Providers</h3>
              <p className="stat-value">{analytics.users.verified_providers}</p>
            </div>
            <div className="stat-card">
              <h3>Total Bookings</h3>
              <p className="stat-value">{analytics.bookings.total}</p>
              <p className="stat-detail">Pending: {analytics.bookings.pending} | Completed: {analytics.bookings.completed}</p>
            </div>
            <div className="stat-card">
              <h3>Total Revenue</h3>
              <p className="stat-value">₹{analytics.revenue.total.toLocaleString()}</p>
              <p className="stat-detail">Last 30 days: ₹{analytics.revenue.in_period.toLocaleString()}</p>
            </div>
            <div className="stat-card">
              <h3>Average Rating</h3>
              <p className="stat-value">⭐ {analytics.ratings.average}</p>
            </div>
          </div>

          <div className="charts-section">
            <div className="chart-card">
              <h3>Booking Trends</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={analytics.booking_trends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="count" stroke="#667eea" name="Bookings" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-card">
              <h3>Popular Specializations</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics.popular_specializations}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="specialization" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#764ba2" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="top-providers">
            <h3>Top Providers by Bookings</h3>
            <div className="providers-list">
              {analytics.top_providers.map((provider, index) => (
                <div key={provider.provider_id} className="top-provider-card">
                  <span className="rank">#{index + 1}</span>
                  <div className="provider-info">
                    <strong>{provider.name}</strong>
                    <p>{provider.booking_count} bookings | ⭐ {provider.rating}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
          )}
        </>
      )}

      {activeTab === 'users' && (
        <div className="admin-table">
          {users.length === 0 && !loading && (
            <div style={{ padding: '20px', textAlign: 'center' }}>No users found.</div>
          )}
          {users.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Full Name</th>
                <th>Role</th>
                <th>Verified</th>
                <th>Active</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>{user.full_name}</td>
                  <td>{user.role}</td>
                  <td>{user.is_verified ? 'Yes' : 'No'}</td>
                  <td>{user.is_active ? 'Yes' : 'No'}</td>
                  <td>
                    <button
                      onClick={() => handleVerify(user.id, !user.is_verified)}
                      className="btn btn-sm btn-success"
                    >
                      {user.is_verified ? 'Unverify' : 'Verify'}
                    </button>
                    <button
                      onClick={() => handleActivate(user.id, !user.is_active)}
                      className="btn btn-sm btn-danger"
                    >
                      {user.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          )}
        </div>
      )}

      {activeTab === 'providers' && (
        <div className="admin-table">
          {providers.length === 0 && !loading && (
            <div style={{ padding: '20px', textAlign: 'center' }}>No providers found.</div>
          )}
          {providers.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Specialization</th>
                <th>Rating</th>
                <th>Fee</th>
                <th>Verified</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {providers.map(provider => (
                <tr key={provider.id}>
                  <td>{provider.id}</td>
                  <td>{provider.user?.full_name}</td>
                  <td>{provider.specialization}</td>
                  <td>⭐ {provider.rating.toFixed(1)}</td>
                  <td>₹{provider.consultation_fee}</td>
                  <td>{provider.is_verified ? 'Yes' : 'No'}</td>
                  <td>
                    <button
                      onClick={() => handleVerify(provider.user_id, !provider.is_verified)}
                      className="btn btn-sm btn-success"
                    >
                      {provider.is_verified ? 'Unverify' : 'Verify'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          )}
        </div>
      )}

      {activeTab === 'bookings' && (
        <div className="admin-table">
          {bookings.length === 0 && !loading && (
            <div style={{ padding: '20px', textAlign: 'center' }}>No bookings found.</div>
          )}
          {bookings.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Client</th>
                <th>Provider</th>
                <th>Date</th>
                <th>Fee</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {bookings.map(booking => (
                <tr key={booking.id}>
                  <td>{booking.id}</td>
                  <td>{booking.client?.full_name}</td>
                  <td>{booking.provider?.full_name}</td>
                  <td>{new Date(booking.booking_date).toLocaleString()}</td>
                  <td>₹{booking.fee}</td>
                  <td><span className={`badge badge-${booking.status}`}>{booking.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
          )}
        </div>
      )}
    </div>
  )
}

export default AdminDashboard

