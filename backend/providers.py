"""Provider and service listing routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, User, Provider, Review
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import joinedload
from datetime import datetime

providers_bp = Blueprint('providers', __name__)

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
        
        # Base query - join User and Provider
        query = db.session.query(Provider).join(User).filter(
            User.is_active == True,
            Provider.is_active == True
        )
        
        # Apply filters
        if verified_only:
            query = query.filter(Provider.is_verified == True)
        
        if role:
            query = query.filter(User.role == role)
        
        if specialization:
            query = query.filter(Provider.specialization.ilike(f'%{specialization}%'))
        
        if min_fee is not None:
            query = query.filter(Provider.consultation_fee >= min_fee)
        
        if max_fee is not None:
            query = query.filter(Provider.consultation_fee <= max_fee)
        
        if min_rating is not None:
            query = query.filter(Provider.rating >= min_rating)
        
        if city:
            query = query.filter(User.city.ilike(f'%{city}%'))
        
        if state:
            query = query.filter(User.state.ilike(f'%{state}%'))
        
        # Search across multiple fields
        if search:
            search_filter = or_(
                User.full_name.ilike(f'%{search}%'),
                User.username.ilike(f'%{search}%'),
                Provider.specialization.ilike(f'%{search}%'),
                Provider.bio.ilike(f'%{search}%'),
                User.city.ilike(f'%{search}%'),
                User.state.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        # Sorting
        if sort_by == 'rating':
            order_by = Provider.rating.desc() if sort_order == 'desc' else Provider.rating.asc()
        elif sort_by == 'fee':
            order_by = Provider.consultation_fee.asc() if sort_order == 'asc' else Provider.consultation_fee.desc()
        elif sort_by == 'experience':
            order_by = Provider.experience_years.desc() if sort_order == 'desc' else Provider.experience_years.asc()
        else:
            order_by = Provider.rating.desc()
        
        query = query.order_by(order_by)
        
        # Pagination - optimize query with eager loading
        pagination = query.options(
            joinedload(Provider.user)
        ).paginate(page=page, per_page=per_page, error_out=False)
        providers = pagination.items
        
        # Convert to dict efficiently
        providers_data = []
        for p in providers:
            try:
                providers_data.append(p.to_dict())
            except Exception as e:
                print(f"Error converting provider {p.id} to dict: {e}")
                continue
        
        return jsonify({
            'providers': providers_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@providers_bp.route('/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    """Get a specific provider by ID"""
    try:
        provider = Provider.query.options(joinedload(Provider.user)).get(provider_id)
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404
        
        if not provider.is_active or not provider.user.is_active:
            return jsonify({'error': 'Provider not found'}), 404
        
        # Get reviews
        reviews = Review.query.filter_by(provider_id=provider_id).order_by(Review.created_at.desc()).limit(10).all()
        
        provider_data = provider.to_dict()
        provider_data['reviews'] = [r.to_dict() for r in reviews]
        
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
        provider = Provider.query.filter_by(user_id=user_id).first_or_404()
        
        return jsonify(provider.to_dict()), 200
        
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
        provider = Provider.query.filter_by(user_id=user_id).first_or_404()
        data = request.get_json()
        
        # Update allowed fields
        updatable_fields = [
            'specialization', 'experience_years', 'bar_council_number',
            'qualification', 'bio', 'consultation_fee', 'hourly_rate'
        ]
        for field in updatable_fields:
            if field in data:
                setattr(provider, field, data[field])
        
        provider.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'provider': provider.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@providers_bp.route('/specializations', methods=['GET'])
def get_specializations():
    """Get list of all specializations"""
    try:
        specializations = db.session.query(Provider.specialization).distinct().filter(
            Provider.specialization.isnot(None),
            Provider.specialization != ''
        ).all()
        
        return jsonify({
            'specializations': [s[0] for s in specializations if s[0]]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@providers_bp.route('/stats', methods=['GET'])
def get_provider_stats():
    """Get provider statistics"""
    try:
        total_providers = Provider.query.filter_by(is_active=True).count()
        verified_providers = Provider.query.filter_by(is_active=True, is_verified=True).count()
        avg_rating = db.session.query(func.avg(Provider.rating)).filter(
            Provider.is_active == True,
            Provider.rating > 0
        ).scalar() or 0.0
        
        return jsonify({
            'total_providers': total_providers,
            'verified_providers': verified_providers,
            'average_rating': round(avg_rating, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

