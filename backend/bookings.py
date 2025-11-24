"""Booking and messaging routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, User, Provider, Booking, Message, Review
from datetime import datetime
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload

bookings_bp = Blueprint('bookings', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@bookings_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    """Create a new booking"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        user = User.query.get_or_404(user_id)
        
        print(f"📅 Booking request from user {user_id} ({user.username}, role: {user.role})")
        
        # Only clients can create bookings
        if user.role != 'client':
            return jsonify({'error': 'Only clients can create bookings'}), 403
        
        data = request.get_json()
        print(f"📦 Booking data received: {data}")
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['provider_id', 'booking_date', 'fee', 'service_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        provider = User.query.get(data['provider_id'])
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404
        
        provider_profile = Provider.query.filter_by(user_id=provider.id).first()
        if not provider_profile:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        if not provider.is_active or not provider_profile.is_active:
            return jsonify({'error': 'Provider is not available'}), 400
        
        # Parse booking date - handle multiple formats
        booking_date_str = data['booking_date']
        try:
            # Try ISO format first
            if 'T' in booking_date_str:
                # Remove 'Z' and replace with '+00:00' if needed
                if booking_date_str.endswith('Z'):
                    booking_date_str = booking_date_str[:-1] + '+00:00'
                elif '+' not in booking_date_str and '-' not in booking_date_str[-6:]:
                    # No timezone, assume UTC
                    booking_date_str = booking_date_str + '+00:00'
                booking_date = datetime.fromisoformat(booking_date_str)
            else:
                # Try parsing as regular datetime string
                booking_date = datetime.fromisoformat(booking_date_str)
        except Exception as e:
            print(f"❌ Date parsing error: {e}, input: {booking_date_str}")
            return jsonify({'error': f'Invalid booking_date format: {str(e)}. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)'}), 400
        
        # Create booking
        booking = Booking(
            client_id=user_id,
            provider_id=provider.id,
            provider_profile_id=provider_profile.id,
            service_type=data['service_type'],
            booking_date=booking_date,
            duration_minutes=data.get('duration_minutes', 60),
            fee=data['fee'],
            status='pending',
            description=data.get('description'),
            meeting_link=data.get('meeting_link'),
            location=data.get('location')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        print(f"✅ Booking created successfully: ID {booking.id} for client {user_id} with provider {provider.id}")
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Booking creation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get bookings for current user"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        user = User.query.get_or_404(user_id)
        claims = get_jwt()
        role = claims.get('role')
        
        # Query based on role with eager loading for performance
        if role == 'client':
            bookings = Booking.query.options(
                joinedload(Booking.client),
                joinedload(Booking.provider),
                joinedload(Booking.provider_profile)
            ).filter_by(client_id=user_id).order_by(Booking.booking_date.desc()).all()
        elif role in ['advocate', 'mediator', 'arbitrator', 'notary', 'document_writer']:
            bookings = Booking.query.options(
                joinedload(Booking.client),
                joinedload(Booking.provider),
                joinedload(Booking.provider_profile)
            ).filter_by(provider_id=user_id).order_by(Booking.booking_date.desc()).all()
        elif role == 'admin':
            # Admin can see all bookings
            bookings = Booking.query.options(
                joinedload(Booking.client),
                joinedload(Booking.provider),
                joinedload(Booking.provider_profile)
            ).order_by(Booking.booking_date.desc()).all()
        else:
            return jsonify({'error': 'Invalid role'}), 403
        
        # Convert to dict efficiently
        bookings_data = []
        for b in bookings:
            try:
                bookings_data.append(b.to_dict())
            except Exception as e:
                print(f"Error converting booking {b.id} to dict: {e}")
                continue
        
        return jsonify({
            'bookings': bookings_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get a specific booking"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        user = User.query.get_or_404(user_id)
        claims = get_jwt()
        role = claims.get('role')
        
        booking = Booking.query.get_or_404(booking_id)
        
        # Check access
        if role != 'admin' and booking.client_id != user_id and booking.provider_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify(booking.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    """Update booking status"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        user = User.query.get_or_404(user_id)
        claims = get_jwt()
        role = claims.get('role')
        
        booking = Booking.query.get_or_404(booking_id)
        
        # Check access - provider or admin can update status
        if role != 'admin' and booking.provider_id != user_id:
            return jsonify({'error': 'Only provider or admin can update booking'}), 403
        
        data = request.get_json()
        
        # Update status
        if 'status' in data:
            valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
            if data['status'] not in valid_statuses:
                return jsonify({'error': 'Invalid status'}), 400
            booking.status = data['status']
        
        # Update other fields
        if 'meeting_link' in data:
            booking.meeting_link = data['meeting_link']
        if 'location' in data:
            booking.location = data['location']
        if 'booking_date' in data:
            try:
                booking.booking_date = datetime.fromisoformat(data['booking_date'].replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Invalid booking_date format'}), 400
        
        booking.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Booking updated successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/<int:booking_id>/review', methods=['POST'])
@jwt_required()
def create_review(booking_id):
    """Create a review for a completed booking"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        booking = Booking.query.get_or_404(booking_id)
        
        # Only client can review
        if booking.client_id != user_id:
            return jsonify({'error': 'Only the client can review this booking'}), 403
        
        # Booking must be completed
        if booking.status != 'completed':
            return jsonify({'error': 'Can only review completed bookings'}), 400
        
        # Check if review already exists
        existing_review = Review.query.filter_by(booking_id=booking_id).first()
        if existing_review:
            return jsonify({'error': 'Review already exists for this booking'}), 400
        
        data = request.get_json()
        
        if not data.get('rating') or not (1 <= data['rating'] <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Create review
        review = Review(
            booking_id=booking_id,
            provider_id=booking.provider_profile_id,
            client_id=user_id,
            rating=data['rating'],
            comment=data.get('comment')
        )
        
        db.session.add(review)
        
        # Update provider rating
        provider = Provider.query.get(booking.provider_profile_id)
        reviews = Review.query.filter_by(provider_id=provider.id).all()
        total_rating = sum(r.rating for r in reviews) + review.rating
        provider.total_reviews = len(reviews) + 1
        provider.rating = total_rating / provider.total_reviews
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    """Get messages for current user"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        booking_id = request.args.get('booking_id', type=int)
        
        query = Message.query.filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id)
        )
        
        if booking_id:
            query = query.filter_by(booking_id=booking_id)
        
        messages = query.order_by(Message.created_at.asc()).all()
        
        return jsonify({
            'messages': [m.to_dict() for m in messages]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    """Send a message"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        data = request.get_json()
        
        required_fields = ['receiver_id', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Verify receiver exists
        receiver = User.query.get_or_404(data['receiver_id'])
        
        # If booking_id provided, verify user has access to that booking
        if data.get('booking_id'):
            booking = Booking.query.get_or_404(data['booking_id'])
            if booking.client_id != user_id and booking.provider_id != user_id:
                return jsonify({'error': 'Access denied to this booking'}), 403
            if booking.client_id != data['receiver_id'] and booking.provider_id != data['receiver_id']:
                return jsonify({'error': 'Receiver must be part of this booking'}), 400
        
        # Create message
        message = Message(
            booking_id=data.get('booking_id'),
            sender_id=user_id,
            receiver_id=data['receiver_id'],
            subject=data.get('subject'),
            content=data['content']
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'message': 'Message sent successfully',
            'message_data': message.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_message_read(message_id):
    """Mark a message as read"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        message = Message.query.get_or_404(message_id)
        
        if message.receiver_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        message.is_read = True
        db.session.commit()
        
        return jsonify({
            'message': 'Message marked as read',
            'message_data': message.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

