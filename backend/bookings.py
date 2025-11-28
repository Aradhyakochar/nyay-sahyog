"""Booking routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from db_access import (
    get_user_by_id, get_provider_by_user_id, get_provider_by_id,
    create_booking, get_booking_by_id, get_bookings_by_client_id,
    get_bookings_by_provider_id, get_all_bookings, update_booking
)
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    """Create a new booking"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        print(f"📅 Booking request from user {user_id} ({user['username']}, role: {user['role']})")
        
        # Only clients can create bookings
        if user['role'] != 'client':
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
        
        provider = get_user_by_id(data['provider_id'])
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404
        
        provider_profile = get_provider_by_user_id(provider['id'])
        if not provider_profile:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        if not provider.get('is_active', True) or not provider_profile.get('is_active', True):
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
        booking_data = {
            'client_id': user_id,
            'provider_id': provider['id'],
            'provider_profile_id': provider_profile['id'],
            'service_type': data['service_type'],
            'booking_date': booking_date,
            'duration_minutes': data.get('duration_minutes', 60),
            'fee': data['fee'],
            'status': 'pending',
            'description': data.get('description'),
            'meeting_link': data.get('meeting_link'),
            'location': data.get('location')
        }
        booking_id = create_booking(booking_data)
        booking = get_booking_by_id(booking_id)
        
        print(f"✅ Booking created successfully: ID {booking_id} for client {user_id} with provider {provider['id']}")
        
        # Format booking for response
        booking_dict = {
            'id': booking['id'],
            'client_id': booking['client_id'],
            'provider_id': booking['provider_id'],
            'provider_profile_id': booking['provider_profile_id'],
            'service_type': booking.get('service_type'),
            'booking_date': booking['booking_date'].isoformat() if isinstance(booking['booking_date'], datetime) else booking.get('booking_date'),
            'duration_minutes': booking.get('duration_minutes', 60),
            'fee': float(booking.get('fee', 0.0)),
            'status': booking.get('status', 'pending'),
            'description': booking.get('description'),
            'meeting_link': booking.get('meeting_link'),
            'location': booking.get('location'),
            'created_at': booking.get('created_at').isoformat() if booking.get('created_at') else None,
            'updated_at': booking.get('updated_at').isoformat() if booking.get('updated_at') else None
        }
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking_dict
        }), 201
        
    except Exception as e:
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
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        claims = get_jwt()
        role = claims.get('role')
        
        # Query based on role
        if role == 'client':
            bookings = get_bookings_by_client_id(user_id)
        elif role in ['advocate', 'mediator', 'arbitrator', 'notary', 'document_writer']:
            bookings = get_bookings_by_provider_id(user_id)
        else:
            return jsonify({'error': 'Invalid role'}), 403
        
        # Format bookings with user/provider info
        bookings_data = []
        for b in bookings:
            try:
                client = get_user_by_id(b['client_id'])
                provider = get_user_by_id(b['provider_id'])
                provider_profile = get_provider_by_id(b['provider_profile_id'])
                
                booking_dict = {
                    'id': b['id'],
                    'client_id': b['client_id'],
                    'client': {
                        'id': client['id'],
                        'username': client['username'],
                        'email': client['email'],
                        'full_name': client['full_name']
                    } if client else None,
                    'provider_id': b['provider_id'],
                    'provider': {
                        'id': provider['id'],
                        'username': provider['username'],
                        'email': provider['email'],
                        'full_name': provider['full_name']
                    } if provider else None,
                    'provider_profile_id': b['provider_profile_id'],
                    'service_type': b.get('service_type'),
                    'booking_date': b['booking_date'].isoformat() if isinstance(b['booking_date'], datetime) else b.get('booking_date'),
                    'duration_minutes': b.get('duration_minutes', 60),
                    'fee': float(b.get('fee', 0.0)),
                    'status': b.get('status', 'pending'),
                    'description': b.get('description'),
                    'meeting_link': b.get('meeting_link'),
                    'location': b.get('location'),
                    'created_at': b.get('created_at').isoformat() if b.get('created_at') else None,
                    'updated_at': b.get('updated_at').isoformat() if b.get('updated_at') else None
                }
                bookings_data.append(booking_dict)
            except Exception as e:
                print(f"Error converting booking {b.get('id')} to dict: {e}")
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
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        claims = get_jwt()
        role = claims.get('role')
        
        booking = get_booking_by_id(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check access
        if booking['client_id'] != user_id and booking['provider_id'] != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Format booking for response
        client = get_user_by_id(booking['client_id'])
        provider = get_user_by_id(booking['provider_id'])
        
        booking_dict = {
            'id': booking['id'],
            'client_id': booking['client_id'],
            'client': {
                'id': client['id'],
                'username': client['username'],
                'email': client['email'],
                'full_name': client['full_name']
            } if client else None,
            'provider_id': booking['provider_id'],
            'provider': {
                'id': provider['id'],
                'username': provider['username'],
                'email': provider['email'],
                'full_name': provider['full_name']
            } if provider else None,
            'provider_profile_id': booking['provider_profile_id'],
            'service_type': booking.get('service_type'),
            'booking_date': booking['booking_date'].isoformat() if isinstance(booking['booking_date'], datetime) else booking.get('booking_date'),
            'duration_minutes': booking.get('duration_minutes', 60),
            'fee': float(booking.get('fee', 0.0)),
            'status': booking.get('status', 'pending'),
            'description': booking.get('description'),
            'meeting_link': booking.get('meeting_link'),
            'location': booking.get('location'),
            'created_at': booking.get('created_at').isoformat() if booking.get('created_at') else None,
            'updated_at': booking.get('updated_at').isoformat() if booking.get('updated_at') else None
        }
        
        return jsonify(booking_dict), 200
        
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
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        claims = get_jwt()
        role = claims.get('role')
        
        booking = get_booking_by_id(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check access - provider can update status
        if booking['provider_id'] != user_id:
            return jsonify({'error': 'Only provider can update booking'}), 403
        
        data = request.get_json()
        update_data = {}
        
        # Update status
        if 'status' in data:
            valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
            if data['status'] not in valid_statuses:
                return jsonify({'error': 'Invalid status'}), 400
            update_data['status'] = data['status']
        
        # Update other fields
        if 'meeting_link' in data:
            update_data['meeting_link'] = data['meeting_link']
        if 'location' in data:
            update_data['location'] = data['location']
        if 'booking_date' in data:
            try:
                update_data['booking_date'] = datetime.fromisoformat(data['booking_date'].replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Invalid booking_date format'}), 400
        
        if update_data:
            update_booking(booking_id, update_data)
            booking = get_booking_by_id(booking_id)
        
        # Format booking for response
        client = get_user_by_id(booking['client_id'])
        provider = get_user_by_id(booking['provider_id'])
        
        booking_dict = {
            'id': booking['id'],
            'client_id': booking['client_id'],
            'client': {
                'id': client['id'],
                'username': client['username'],
                'email': client['email'],
                'full_name': client['full_name']
            } if client else None,
            'provider_id': booking['provider_id'],
            'provider': {
                'id': provider['id'],
                'username': provider['username'],
                'email': provider['email'],
                'full_name': provider['full_name']
            } if provider else None,
            'provider_profile_id': booking['provider_profile_id'],
            'service_type': booking.get('service_type'),
            'booking_date': booking['booking_date'].isoformat() if isinstance(booking['booking_date'], datetime) else booking.get('booking_date'),
            'duration_minutes': booking.get('duration_minutes', 60),
            'fee': float(booking.get('fee', 0.0)),
            'status': booking.get('status', 'pending'),
            'description': booking.get('description'),
            'meeting_link': booking.get('meeting_link'),
            'location': booking.get('location'),
            'created_at': booking.get('created_at').isoformat() if booking.get('created_at') else None,
            'updated_at': booking.get('updated_at').isoformat() if booking.get('updated_at') else None
        }
        
        return jsonify({
            'message': 'Booking updated successfully',
            'booking': booking_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



