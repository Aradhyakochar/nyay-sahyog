import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Navbar.css'

function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/')
    setMobileMenuOpen(false)
  }

  const isActive = (path) => location.pathname === path

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <div className="brand-icon">⚖️</div>
          <div className="brand-text">
            <span className="brand-name">Nyay Sahyog</span>
            <span className="brand-tagline">Legal Services</span>
          </div>
        </Link>

        <div className={`navbar-links ${mobileMenuOpen ? 'mobile-open' : ''}`}>
          <Link 
            to="/" 
            className={`nav-link ${isActive('/') ? 'active' : ''}`}
            onClick={() => setMobileMenuOpen(false)}
          >
            <span className="nav-icon">🏠</span>
            <span>Home</span>
          </Link>
          
          <Link 
            to="/providers" 
            className={`nav-link ${isActive('/providers') ? 'active' : ''}`}
            onClick={() => setMobileMenuOpen(false)}
          >
            <span className="nav-icon">🔍</span>
            <span>Discover</span>
          </Link>

          {user ? (
            <>
              <Link 
                to="/bookings" 
                className={`nav-link ${isActive('/bookings') ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className="nav-icon">📅</span>
                <span>Bookings</span>
              </Link>
              
              {user.role === 'admin' && (
                <Link 
                  to="/admin" 
                  className={`nav-link ${isActive('/admin') ? 'active' : ''}`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <span className="nav-icon">⚙️</span>
                  <span>Admin</span>
                </Link>
              )}

              <div className="navbar-user-section">
                <Link 
                  to="/profile" 
                  className={`nav-link profile-link ${isActive('/profile') ? 'active' : ''}`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <span className="nav-icon">👤</span>
                  <span>{user.full_name?.split(' ')[0] || 'Account'}</span>
                </Link>
                <button onClick={handleLogout} className="btn-logout">
                  <span>🚪</span>
                  <span>Logout</span>
                </button>
              </div>
            </>
          ) : (
            <>
              <Link 
                to="/login" 
                className="nav-link btn-nav-primary"
                onClick={() => setMobileMenuOpen(false)}
              >
                <span>Login</span>
              </Link>
              <Link 
                to="/register" 
                className="nav-link btn-nav-secondary"
                onClick={() => setMobileMenuOpen(false)}
              >
                <span>Get Started</span>
              </Link>
            </>
          )}
        </div>

        <button 
          className="mobile-menu-toggle"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle menu"
        >
          <span className={mobileMenuOpen ? 'open' : ''}></span>
          <span className={mobileMenuOpen ? 'open' : ''}></span>
          <span className={mobileMenuOpen ? 'open' : ''}></span>
        </button>
      </div>
    </nav>
  )
}

export default Navbar

