"""Authentication routes and JWT handling"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from db_access import (
    create_user, get_user_by_username, get_user_by_email, get_user_by_id,
    update_user, check_password, create_provider, get_provider_by_user_id
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        print(f"📝 Registration request received: {data.get('username', 'unknown')} ({data.get('email', 'unknown')})")
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'full_name', 'role']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate role
        valid_roles = ['client', 'advocate', 'mediator', 'arbitrator', 'notary', 'document_writer']
        if data['role'] not in valid_roles:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Check if user already exists
        if get_user_by_username(data['username']):
            return jsonify({'error': 'Username already exists'}), 400
        
        if get_user_by_email(data['email']):
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password': data['password'],
            'role': data['role'],
            'full_name': data['full_name'],
            'phone': data.get('phone'),
            'address': data.get('address'),
            'city': data.get('city'),
            'state': data.get('state'),
            'pincode': data.get('pincode'),
            'is_verified': False,
            'is_active': True
        }
        user_id = create_user(user_data)
        user = get_user_by_id(user_id)
        
        # Create provider profile if role is a provider type
        provider_roles = ['advocate', 'mediator', 'arbitrator', 'notary', 'document_writer']
        if data['role'] in provider_roles:
            provider_data = {
                'user_id': user_id,
                'specialization': data.get('specialization'),
                'experience_years': data.get('experience_years', 0),
                'bar_council_number': data.get('bar_council_number'),
                'qualification': data.get('qualification'),
                'bio': data.get('bio'),
                'consultation_fee': data.get('consultation_fee', 0.0),
                'hourly_rate': data.get('hourly_rate', 0.0),
                'is_verified': False,
                'is_active': True
            }
            create_provider(provider_data)
        
        # Create access token (identity must be string)
        access_token = create_access_token(identity=str(user_id), additional_claims={'role': user['role']})
        
        print(f"✅ User registered successfully: {user['username']} (ID: {user_id})")
        
        # Format user dict for response
        user_dict = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'full_name': user['full_name'],
            'phone': user.get('phone'),
            'address': user.get('address'),
            'city': user.get('city'),
            'state': user.get('state'),
            'pincode': user.get('pincode'),
            'is_verified': user.get('is_verified', False),
            'is_active': user.get('is_active', True),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
        }
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user_dict,
            'access_token': access_token
        }), 201
        
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint - Simple username/password login"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = get_user_by_username(data['username'])
        
        if not user or not check_password(user, data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Create access token (identity must be string)
        access_token = create_access_token(identity=str(user['id']), additional_claims={'role': user['role']})
        
        # Format user dict for response
        user_dict = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'full_name': user['full_name'],
            'phone': user.get('phone'),
            'address': user.get('address'),
            'city': user.get('city'),
            'state': user.get('state'),
            'pincode': user.get('pincode'),
            'is_verified': user.get('is_verified', False),
            'is_active': user.get('is_active', True),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
        }
        
        return jsonify({
            'message': 'Login successful',
            'user': user_dict,
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        # Get JWT claims for debugging
        claims = get_jwt()
        user_id_str = get_jwt_identity()
        # Convert string identity back to integer for database query
        user_id = int(user_id_str) if user_id_str else None
        
        print(f"📋 Profile request - User ID: {user_id} (from token: {user_id_str}), Claims: {claims}")
        
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        response_data = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'full_name': user['full_name'],
            'phone': user.get('phone'),
            'address': user.get('address'),
            'city': user.get('city'),
            'state': user.get('state'),
            'pincode': user.get('pincode'),
            'is_verified': user.get('is_verified', False),
            'is_active': user.get('is_active', True),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
        }
        
        # Include provider profile if exists
        provider = get_provider_by_user_id(user_id)
        if provider:
            provider_dict = {
                'id': provider['id'],
                'user_id': provider['user_id'],
                'specialization': provider.get('specialization'),
                'experience_years': provider.get('experience_years', 0),
                'bar_council_number': provider.get('bar_council_number'),
                'qualification': provider.get('qualification'),
                'bio': provider.get('bio'),
                'consultation_fee': float(provider.get('consultation_fee', 0.0)),
                'hourly_rate': float(provider.get('hourly_rate', 0.0)),
                'rating': float(provider.get('rating', 0.0)),
                'total_reviews': provider.get('total_reviews', 0),
                'is_verified': provider.get('is_verified', False),
                'is_active': provider.get('is_active', True),
                'created_at': provider.get('created_at').isoformat() if provider.get('created_at') else None
            }
            response_data['provider_profile'] = provider_dict
        
        print(f"✅ Profile response for user {user_id} ({user['username']})")
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"❌ Profile error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        update_data = {}
        updatable_fields = ['full_name', 'phone', 'address', 'city', 'state', 'pincode', 'email']
        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]
        
        if update_data:
            update_user(user_id, update_data)
            user = get_user_by_id(user_id)
        
        response_data = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'full_name': user['full_name'],
            'phone': user.get('phone'),
            'address': user.get('address'),
            'city': user.get('city'),
            'state': user.get('state'),
            'pincode': user.get('pincode'),
            'is_verified': user.get('is_verified', False),
            'is_active': user.get('is_active', True),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
        }
        
        provider = get_provider_by_user_id(user_id)
        if provider:
            provider_dict = {
                'id': provider['id'],
                'user_id': provider['user_id'],
                'specialization': provider.get('specialization'),
                'experience_years': provider.get('experience_years', 0),
                'bar_council_number': provider.get('bar_council_number'),
                'qualification': provider.get('qualification'),
                'bio': provider.get('bio'),
                'consultation_fee': float(provider.get('consultation_fee', 0.0)),
                'hourly_rate': float(provider.get('hourly_rate', 0.0)),
                'rating': float(provider.get('rating', 0.0)),
                'total_reviews': provider.get('total_reviews', 0),
                'is_verified': provider.get('is_verified', False),
                'is_active': provider.get('is_active', True),
                'created_at': provider.get('created_at').isoformat() if provider.get('created_at') else None
            }
            response_data['provider_profile'] = provider_dict
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': response_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({'error': 'Old password and new password are required'}), 400
        
        if not check_password(user, data['old_password']):
            return jsonify({'error': 'Invalid old password'}), 401
        
        update_user(user_id, {'password': data['new_password']})
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

