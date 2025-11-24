import React from 'react'
import { Link } from 'react-router-dom'
import './Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>⚖️ Nyay Sahyog</h3>
            <p>Your trusted legal services marketplace. Connect with verified legal experts and get expert assistance with complete transparency.</p>
            <div className="social-links">
              <a href="#" aria-label="Facebook">📘</a>
              <a href="#" aria-label="Twitter">🐦</a>
              <a href="#" aria-label="LinkedIn">💼</a>
              <a href="#" aria-label="Instagram">📷</a>
            </div>
          </div>

          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/providers">Find Providers</Link></li>
              <li><Link to="/register">Become a Provider</Link></li>
              <li><Link to="/login">Login</Link></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Services</h4>
            <ul>
              <li>Legal Consultation</li>
              <li>Document Writing</li>
              <li>Mediation & Arbitration</li>
              <li>Notary Services</li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>📍 Location & Contact</h4>
            <div className="location-info">
              <p>
                <strong>📍 Address:</strong><br />
                Nyay Sahyog Legal Services<br />
                KIIT University Campus<br />
                Patia, Bhubaneswar<br />
                Odisha 751024, India
              </p>
              <p>
                <strong>📧 Email:</strong><br />
                <a href="mailto:nyaysahyoglegalservices@gmail.com">
                  nyaysahyoglegalservices@gmail.com
                </a>
              </p>
              <p>
                <strong>📞 Phone:</strong><br />
                +91-XXX-XXX-XXXX
              </p>
              <p>
                <strong>🕒 Hours:</strong><br />
                Mon - Sat: 9:00 AM - 6:00 PM<br />
                Sunday: Closed
              </p>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} Nyay Sahyog. All rights reserved.</p>
          <div className="footer-links">
            <Link to="/">Privacy Policy</Link>
            <span>|</span>
            <Link to="/">Terms of Service</Link>
            <span>|</span>
            <Link to="/">About Us</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer

