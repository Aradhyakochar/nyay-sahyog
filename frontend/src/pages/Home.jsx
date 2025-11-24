import React from 'react'
import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  return (
    <div className="home">
      <div className="hero">
        <div className="container">
          <h1>Welcome to Nyay Sahyog</h1>
          <p className="hero-subtitle">Your Trusted Legal Services Marketplace</p>
          <p className="hero-description">
            Connect with verified legal experts—advocates, mediators, arbitrators, notaries, 
            and document writers. Get expert legal assistance with complete transparency and ease.
          </p>
          <div className="hero-buttons">
            <Link to="/providers" className="btn btn-primary">
              🔍 Find Legal Services
            </Link>
            <Link to="/register" className="btn btn-secondary">
              ⚖️ Join as Provider
            </Link>
          </div>
        </div>
      </div>

      <div className="stats-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">500+</div>
              <div className="stat-label">Verified Providers</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">10,000+</div>
              <div className="stat-label">Successful Consultations</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">4.8★</div>
              <div className="stat-label">Average Rating</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">50+</div>
              <div className="stat-label">Cities Covered</div>
            </div>
          </div>
        </div>
      </div>

      <div className="features">
        <h2>Why Choose Nyay Sahyog?</h2>
        <p>Everything you need for your legal requirements in one trusted platform</p>
        <div className="features-grid">
          <div className="feature-card">
            <span className="feature-card-icon">✅</span>
            <h3>Verified Providers</h3>
            <p>All legal service providers are thoroughly verified by our admin team to ensure quality, reliability, and trustworthiness.</p>
          </div>
          <div className="feature-card">
            <span className="feature-card-icon">📅</span>
            <h3>Easy Booking</h3>
            <p>Book consultations with legal experts in just a few clicks. Manage all your appointments seamlessly in one place.</p>
          </div>
          <div className="feature-card">
            <span className="feature-card-icon">💰</span>
            <h3>Transparent Pricing</h3>
            <p>View consultation fees and hourly rates upfront. No hidden charges, no surprises—complete transparency.</p>
          </div>
          <div className="feature-card">
            <span className="feature-card-icon">💬</span>
            <h3>Secure Messaging</h3>
            <p>Communicate directly with your legal service provider through our secure, encrypted messaging system.</p>
          </div>
          <div className="feature-card">
            <span className="feature-card-icon">⭐</span>
            <h3>Reviews & Ratings</h3>
            <p>Read authentic reviews from other clients to make informed decisions about your legal service provider.</p>
          </div>
          <div className="feature-card">
            <span className="feature-card-icon">🎯</span>
            <h3>Multiple Services</h3>
            <p>Find advocates, mediators, arbitrators, notaries, and document writers—all in one comprehensive platform.</p>
          </div>
        </div>
      </div>

      <div className="services-section">
        <div className="container">
          <h2>Our Legal Services</h2>
          <p className="section-subtitle">Comprehensive legal solutions for all your needs</p>
          <div className="services-grid">
            <div className="service-card">
              <div className="service-icon">⚖️</div>
              <h3>Legal Consultation</h3>
              <p>Get expert advice from experienced advocates on various legal matters including civil, criminal, corporate, and family law.</p>
            </div>
            <div className="service-card">
              <div className="service-icon">📝</div>
              <h3>Document Writing</h3>
              <p>Professional document drafting services for contracts, agreements, legal notices, and other important documents.</p>
            </div>
            <div className="service-card">
              <div className="service-icon">🤝</div>
              <h3>Mediation & Arbitration</h3>
              <p>Resolve disputes amicably through certified mediators and arbitrators without going to court.</p>
            </div>
            <div className="service-card">
              <div className="service-icon">📜</div>
              <h3>Notary Services</h3>
              <p>Get your documents notarized quickly and efficiently by verified notaries in your area.</p>
            </div>
          </div>
        </div>
      </div>

      <div className="testimonials-section">
        <div className="container">
          <h2>What Our Clients Say</h2>
          <div className="testimonials-grid">
            <div className="testimonial-card">
              <div className="testimonial-rating">⭐⭐⭐⭐⭐</div>
              <p className="testimonial-text">"Nyay Sahyog made finding the right advocate so easy. The platform is user-friendly and all providers are verified. Highly recommended!"</p>
              <div className="testimonial-author">
                <strong>Rajesh Kumar</strong>
                <span>Business Owner</span>
              </div>
            </div>
            <div className="testimonial-card">
              <div className="testimonial-rating">⭐⭐⭐⭐⭐</div>
              <p className="testimonial-text">"I needed urgent legal consultation and found an excellent advocate within minutes. The booking process was seamless."</p>
              <div className="testimonial-author">
                <strong>Priya Sharma</strong>
                <span>Individual Client</span>
              </div>
            </div>
            <div className="testimonial-card">
              <div className="testimonial-rating">⭐⭐⭐⭐⭐</div>
              <p className="testimonial-text">"As a provider, this platform has helped me reach more clients and manage my consultations efficiently. Great platform!"</p>
              <div className="testimonial-author">
                <strong>Adv. Amit Patel</strong>
                <span>Legal Practitioner</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="cta-section">
        <div className="container">
          <h2>Ready to Get Started?</h2>
          <p>Join thousands of satisfied clients and providers on Nyay Sahyog</p>
          <div className="cta-buttons">
            <Link to="/providers" className="btn btn-primary btn-large">
              🔍 Find Legal Services
            </Link>
            <Link to="/register" className="btn btn-secondary btn-large">
              ⚖️ Become a Provider
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home

