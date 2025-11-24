"""Database models for Nyay Sahyog"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for all user types (client, advocate, mediator, admin)"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')  # client, advocate, mediator, arbitrator, notary, document_writer, admin
    full_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    google_id = db.Column(db.String(255), unique=True, nullable=True)  # For OAuth
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    provider_profile = db.relationship('Provider', backref='user', uselist=False, cascade='all, delete-orphan')
    bookings_as_client = db.relationship('Booking', foreign_keys='Booking.client_id', backref='client', lazy='dynamic')
    bookings_as_provider = db.relationship('Booking', foreign_keys='Booking.provider_id', backref='provider', lazy='dynamic')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_sensitive:
            data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        return data


class Provider(db.Model):
    """Provider profile for legal service providers"""
    __tablename__ = 'providers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    specialization = db.Column(db.String(200))  # e.g., "Criminal Law", "Family Law", "Corporate Law"
    experience_years = db.Column(db.Integer, default=0)
    bar_council_number = db.Column(db.String(100))  # For advocates
    qualification = db.Column(db.Text)  # Educational qualifications
    bio = db.Column(db.Text)
    consultation_fee = db.Column(db.Float, default=0.0)
    hourly_rate = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, default=0.0)  # Average rating
    total_reviews = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)  # Admin verification
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='provider_profile', lazy='dynamic')
    reviews = db.relationship('Review', backref='provider', lazy='dynamic')
    
    def to_dict(self):
        """Convert provider to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'specialization': self.specialization,
            'experience_years': self.experience_years,
            'bar_council_number': self.bar_council_number,
            'qualification': self.qualification,
            'bio': self.bio,
            'consultation_fee': self.consultation_fee,
            'hourly_rate': self.hourly_rate,
            'rating': self.rating,
            'total_reviews': self.total_reviews,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Booking(db.Model):
    """Booking model for consultations"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_profile_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    service_type = db.Column(db.String(100))  # consultation, document_writing, etc.
    booking_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    fee = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    description = db.Column(db.Text)
    meeting_link = db.Column(db.String(500))  # For online consultations
    location = db.Column(db.String(500))  # For in-person consultations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='booking', lazy='dynamic')
    review = db.relationship('Review', backref='booking', uselist=False)
    
    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client': self.client.to_dict() if self.client else None,
            'provider_id': self.provider_id,
            'provider': self.provider.to_dict() if self.provider else None,
            'provider_profile_id': self.provider_profile_id,
            'service_type': self.service_type,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None,
            'duration_minutes': self.duration_minutes,
            'fee': self.fee,
            'status': self.status,
            'description': self.description,
            'meeting_link': self.meeting_link,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Message(db.Model):
    """Message model for internal messaging"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'sender_id': self.sender_id,
            'sender': self.sender.to_dict() if self.sender else None,
            'receiver_id': self.receiver_id,
            'receiver': self.receiver.to_dict() if self.receiver else None,
            'subject': self.subject,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Review(db.Model):
    """Review model for provider ratings"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), unique=True, nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    client = db.relationship('User', backref='reviews_given')
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'provider_id': self.provider_id,
            'client_id': self.client_id,
            'client': self.client.to_dict() if self.client else None,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class OTP(db.Model):
    """OTP model for two-factor authentication"""
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='otps')
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_used and datetime.utcnow() < self.expires_at
    
    def to_dict(self):
        """Convert OTP to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_used': self.is_used,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

