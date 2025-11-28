"""Provider and service listing routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from db_access import (
    get_provider_by_id, get_provider_by_user_id, update_provider,
    get_providers_search, get_specializations, get_provider_stats,
    get_user_by_id
)
from datetime import datetime

providers_bp = Blueprint('providers', __name__)

def provider_required(f):
    """Decorator to require provider role"""
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        provider_roles = ['advocate', 'mediator', 'arbitrator', 'notary', 'document_writer']
        if claims.get('role') not in provider_roles:
            return jsonify({'error': 'Provider access required'}), 403
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@providers_bp.route('', methods=['GET'])
def get_providers():
    """Get all providers with search, filter, and pagination"""
    try:
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '').strip()
        role = request.args.get('role', '').strip()
        specialization = request.args.get('specialization', '').strip()
        verified_only = request.args.get('verified_only', 'false').lower() == 'true'
        min_fee = request.args.get('min_fee', type=float)
        max_fee = request.args.get('max_fee', type=float)
        min_rating = request.args.get('min_rating', type=float)
        city = request.args.get('city', '').strip()
        state = request.args.get('state', '').strip()
        sort_by = request.args.get('sort_by', 'rating')  # rating, fee, experience
        sort_order = request.args.get('sort_order', 'desc')  # asc, desc
        
        result = get_providers_search(
            search=search,
            role=role,
            specialization=specialization,
            verified_only=verified_only,
            min_fee=min_fee,
            max_fee=max_fee,
            min_rating=min_rating,
            city=city,
            state=state,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            per_page=per_page
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@providers_bp.route('/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    """Get a specific provider by ID"""
    try:
        provider = get_provider_by_id(provider_id)
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404
        
        user = get_user_by_id(provider['user_id'])
        if not user or not user.get('is_active', True) or not provider.get('is_active', True):
            return jsonify({'error': 'Provider not found'}), 404
        
        provider_data = {
            'id': provider['id'],
            'user_id': provider['user_id'],
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone': user.get('phone'),
                'address': user.get('address'),
                'city': user.get('city'),
                'state': user.get('state'),
                'pincode': user.get('pincode')
            },
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
        
        return jsonify(provider_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@providers_bp.route('/my-profile', methods=['GET'])
@provider_required
def get_my_provider_profile():
    """Get current provider's profile"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        provider = get_provider_by_user_id(user_id)
        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        user = get_user_by_id(user_id)
        provider_dict = {
            'id': provider['id'],
            'user_id': provider['user_id'],
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone': user.get('phone'),
                'address': user.get('address'),
                'city': user.get('city'),
                'state': user.get('state'),
                'pincode': user.get('pincode')
            } if user else None,
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
        
        return jsonify(provider_dict), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@providers_bp.route('/my-profile', methods=['PUT'])
@provider_required
def update_my_provider_profile():
    """Update current provider's profile"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str) if user_id_str else None
        if not user_id:
            return jsonify({'error': 'Invalid user ID in token'}), 401
        provider = get_provider_by_user_id(user_id)
        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        update_data = {}
        updatable_fields = [
            'specialization', 'experience_years', 'bar_council_number',
            'qualification', 'bio', 'consultation_fee', 'hourly_rate'
        ]
        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]
        
        if update_data:
            update_provider(provider['id'], update_data)
            provider = get_provider_by_user_id(user_id)
        
        user = get_user_by_id(user_id)
        provider_dict = {
            'id': provider['id'],
            'user_id': provider['user_id'],
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone': user.get('phone'),
                'address': user.get('address'),
                'city': user.get('city'),
                'state': user.get('state'),
                'pincode': user.get('pincode')
            } if user else None,
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
        
        return jsonify({
            'message': 'Profile updated successfully',
            'provider': provider_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@providers_bp.route('/specializations', methods=['GET'])
def get_specializations_list():
    """Get list of all specializations"""
    try:
        specializations = get_specializations()
        
        return jsonify({
            'specializations': specializations
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@providers_bp.route('/stats', methods=['GET'])
def get_provider_stats_endpoint():
    """Get provider statistics"""
    try:
        stats = get_provider_stats()
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

