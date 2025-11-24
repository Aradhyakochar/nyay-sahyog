import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import ProviderMap from '../components/ProviderMap'
import './Providers.css'

function Providers() {
  const [providers, setProviders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState({
    search: '',
    role: '',
    specialization: '',
    verified_only: false,
    min_fee: '',
    max_fee: '',
    min_rating: '',
    city: '',
    state: '',
    sort_by: 'rating',
    sort_order: 'desc'
  })
  const [pagination, setPagination] = useState({ page: 1, per_page: 10, total: 0, pages: 0 })
  const [specializations, setSpecializations] = useState([])
  const [viewMode, setViewMode] = useState('list') // 'list' or 'map'

  useEffect(() => {
    fetchProviders()
    fetchSpecializations()
  }, [filters, pagination.page])

  const fetchProviders = async () => {
    try {
      setLoading(true)
      setError('')
      const params = { ...filters, page: pagination.page }
      Object.keys(params).forEach(key => {
        if (params[key] === '' || params[key] === false) {
          delete params[key]
        }
      })
      console.log('🔍 Fetching providers with params:', params)
      console.log('📡 API Base URL:', api.defaults.baseURL)
      const response = await api.get('/providers', { params })
      console.log('✅ Providers response:', response.data)
      
      if (response.data && response.data.providers) {
        setProviders(response.data.providers || [])
        setPagination(response.data.pagination || { page: 1, per_page: 10, total: 0, pages: 0 })
      } else {
        setProviders([])
        setError('No providers found. Try seeding sample data.')
      }
    } catch (err) {
      console.error('Error fetching providers:', err)
      const errorMsg = err.response?.data?.error || err.message || 'Failed to load providers'
      setError(`Error: ${errorMsg}. Make sure backend is running on http://localhost:5000`)
      setProviders([])
    } finally {
      setLoading(false)
    }
  }

  const fetchSpecializations = async () => {
    try {
      const response = await api.get('/providers/specializations')
      setSpecializations(response.data.specializations)
    } catch (err) {
      console.error(err)
    }
  }

  const handleFilterChange = (e) => {
    const { name, value, type, checked } = e.target
    setFilters({
      ...filters,
      [name]: type === 'checkbox' ? checked : value
    })
    setPagination({ ...pagination, page: 1 })
  }

  const clearFilters = () => {
    setFilters({
      search: '',
      role: '',
      specialization: '',
      verified_only: false,
      min_fee: '',
      max_fee: '',
      min_rating: '',
      city: '',
      state: '',
      sort_by: 'rating',
      sort_order: 'desc'
    })
  }

  if (loading && providers.length === 0) {
    return <div className="loading">Loading providers...</div>
  }

  return (
    <div className="container">
      <h1>Find Legal Service Providers</h1>
      
      <div className="providers-layout">
        <div className="filters-sidebar">
          <h3>Filters</h3>
          <div className="form-group">
            <label>Search</label>
            <input
              type="text"
              name="search"
              value={filters.search}
              onChange={handleFilterChange}
              placeholder="Name, specialization, location..."
            />
          </div>
          <div className="form-group">
            <label>Role</label>
            <select name="role" value={filters.role} onChange={handleFilterChange}>
              <option value="">All Roles</option>
              <option value="advocate">Advocate</option>
              <option value="mediator">Mediator</option>
              <option value="arbitrator">Arbitrator</option>
              <option value="notary">Notary</option>
              <option value="document_writer">Document Writer</option>
            </select>
          </div>
          <div className="form-group">
            <label>Specialization</label>
            <select name="specialization" value={filters.specialization} onChange={handleFilterChange}>
              <option value="">All Specializations</option>
              {specializations.map(spec => (
                <option key={spec} value={spec}>{spec}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                name="verified_only"
                checked={filters.verified_only}
                onChange={handleFilterChange}
              />
              Verified Only
            </label>
          </div>
          <div className="form-group">
            <label>Min Fee (₹)</label>
            <input
              type="number"
              name="min_fee"
              value={filters.min_fee}
              onChange={handleFilterChange}
              min="0"
            />
          </div>
          <div className="form-group">
            <label>Max Fee (₹)</label>
            <input
              type="number"
              name="max_fee"
              value={filters.max_fee}
              onChange={handleFilterChange}
              min="0"
            />
          </div>
          <div className="form-group">
            <label>Min Rating</label>
            <input
              type="number"
              name="min_rating"
              value={filters.min_rating}
              onChange={handleFilterChange}
              min="0"
              max="5"
              step="0.1"
            />
          </div>
          <div className="form-group">
            <label>City</label>
            <input
              type="text"
              name="city"
              value={filters.city}
              onChange={handleFilterChange}
            />
          </div>
          <div className="form-group">
            <label>State</label>
            <input
              type="text"
              name="state"
              value={filters.state}
              onChange={handleFilterChange}
            />
          </div>
          <div className="form-group">
            <label>Sort By</label>
            <select name="sort_by" value={filters.sort_by} onChange={handleFilterChange}>
              <option value="rating">Rating</option>
              <option value="fee">Fee</option>
              <option value="experience">Experience</option>
            </select>
          </div>
          <div className="form-group">
            <label>Order</label>
            <select name="sort_order" value={filters.sort_order} onChange={handleFilterChange}>
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
          <button onClick={clearFilters} className="btn btn-secondary">
            Clear Filters
          </button>
        </div>

        <div className="providers-content">
          {error && <div className="error">{error}</div>}
          
          <div className="view-toggle">
            <button
              className={viewMode === 'list' ? 'active' : ''}
              onClick={() => setViewMode('list')}
            >
              List View
            </button>
            <button
              className={viewMode === 'map' ? 'active' : ''}
              onClick={() => setViewMode('map')}
            >
              Map View
            </button>
          </div>
          
          {loading && providers.length === 0 ? (
            <div className="loading">Loading providers...</div>
          ) : error ? (
            <div className="error">
              {error}
              <br />
              <br />
              <strong>Quick Fix:</strong>
              <ol style={{ textAlign: 'left', display: 'inline-block' }}>
                <li>Make sure backend is running: <code>python app.py</code></li>
                <li>Seed sample data: <code>python seed_data.py</code></li>
                <li>Check browser console for errors</li>
              </ol>
            </div>
          ) : providers.length === 0 ? (
            <div className="no-results">
              <h3>No providers found</h3>
              <p>Try adjusting your filters or seed sample data:</p>
              <code style={{ display: 'block', marginTop: '10px', padding: '10px', background: '#f5f5f5' }}>
                cd backend && python seed_data.py
              </code>
            </div>
          ) : viewMode === 'map' ? (
            <ProviderMap providers={providers} />
          ) : (
            <>
              <div className="providers-grid">
                {providers.map(provider => (
                  <div key={provider.id} className="provider-card">
                    <div className="provider-header">
                      <h3>{provider.user?.full_name}</h3>
                      {provider.is_verified && (
                        <span className="badge badge-verified">Verified</span>
                      )}
                    </div>
                    <p className="provider-role">{provider.user?.role}</p>
                    {provider.specialization && (
                      <p className="provider-specialization">{provider.specialization}</p>
                    )}
                    <div className="provider-info">
                      <div className="provider-rating">
                        ⭐ {provider.rating.toFixed(1)} ({provider.total_reviews} reviews)
                      </div>
                      <div className="provider-experience">
                        {provider.experience_years} years experience
                      </div>
                      <div className="provider-fee">
                        ₹{provider.consultation_fee} consultation fee
                      </div>
                      {provider.user?.city && (
                        <div className="provider-location">
                          📍 {provider.user.city}, {provider.user.state}
                        </div>
                      )}
                    </div>
                    {provider.bio && (
                      <p className="provider-bio">{provider.bio.substring(0, 150)}...</p>
                    )}
                    <Link to={`/providers/${provider.id}`} className="btn btn-primary">
                      View Profile
                    </Link>
                  </div>
                ))}
              </div>
              
              <div className="pagination">
                <button
                  onClick={() => setPagination({ ...pagination, page: pagination.page - 1 })}
                  disabled={pagination.page === 1}
                  className="btn btn-secondary"
                >
                  Previous
                </button>
                <span>
                  Page {pagination.page} of {pagination.pages} ({pagination.total} total)
                </span>
                <button
                  onClick={() => setPagination({ ...pagination, page: pagination.page + 1 })}
                  disabled={pagination.page >= pagination.pages}
                  className="btn btn-secondary"
                >
                  Next
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default Providers

