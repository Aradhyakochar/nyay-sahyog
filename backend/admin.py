"""Admin routes for management and analytics"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db, User, Provider, Booking, Review, Message
from sqlalchemy import func, extract
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

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


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role = request.args.get('role', '').strip()
        search = request.args.get('search', '').strip()
        is_active = request.args.get('is_active')
        
        query = User.query
        
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == (is_active.lower() == 'true'))
        
        if search:
            query = query.filter(
                db.or_(
                    User.username.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%'),
                    User.full_name.ilike(f'%{search}%')
                )
            )
        
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [u.to_dict(include_sensitive=True) for u in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>/verify', methods=['PUT'])
@admin_required
def verify_user(user_id):
    """Verify a user/provider"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        verify = data.get('verify', True)
        user.is_verified = verify
        
        # Also verify provider profile if exists
        if user.provider_profile:
            user.provider_profile.is_verified = verify
        
        db.session.commit()
        
        return jsonify({
            'message': f'User {"verified" if verify else "unverified"} successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>/activate', methods=['PUT'])
@admin_required
def activate_user(user_id):
    """Activate or deactivate a user"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        activate = data.get('activate', True)
        user.is_active = activate
        
        if user.provider_profile:
            user.provider_profile.is_active = activate
        
        db.session.commit()
        
        return jsonify({
            'message': f'User {"activated" if activate else "deactivated"} successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/providers', methods=['GET'])
@admin_required
def get_all_providers():
    """Get all providers for admin"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        verified = request.args.get('verified')
        
        query = Provider.query.join(User)
        
        if verified is not None:
            query = query.filter(Provider.is_verified == (verified.lower() == 'true'))
        
        pagination = query.order_by(Provider.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'providers': [p.to_dict() for p in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/bookings', methods=['GET'])
@admin_required
def get_all_bookings():
    """Get all bookings for admin"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', '').strip()
        
        query = Booking.query
        
        if status:
            query = query.filter(Booking.status == status)
        
        pagination = query.order_by(Booking.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'bookings': [b.to_dict() for b in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/analytics', methods=['GET'])
@admin_required
def get_analytics():
    """Get platform analytics"""
    try:
        # Time range (default: last 30 days)
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # User statistics
        total_users = User.query.count()
        total_clients = User.query.filter_by(role='client').count()
        total_providers = User.query.filter(User.role.in_(['advocate', 'mediator', 'arbitrator', 'notary', 'document_writer'])).count()
        verified_providers = Provider.query.filter_by(is_verified=True).count()
        
        # Booking statistics
        total_bookings = Booking.query.count()
        bookings_in_period = Booking.query.filter(Booking.created_at >= start_date).count()
        pending_bookings = Booking.query.filter_by(status='pending').count()
        completed_bookings = Booking.query.filter_by(status='completed').count()
        cancelled_bookings = Booking.query.filter_by(status='cancelled').count()
        
        # Revenue (sum of completed booking fees)
        total_revenue = db.session.query(func.sum(Booking.fee)).filter(
            Booking.status == 'completed'
        ).scalar() or 0.0
        
        revenue_in_period = db.session.query(func.sum(Booking.fee)).filter(
            Booking.status == 'completed',
            Booking.created_at >= start_date
        ).scalar() or 0.0
        
        # Provider ratings
        avg_rating = db.session.query(func.avg(Provider.rating)).filter(
            Provider.rating > 0
        ).scalar() or 0.0
        
        # Popular specializations
        popular_specializations = db.session.query(
            Provider.specialization,
            func.count(Provider.id).label('count')
        ).filter(
            Provider.specialization.isnot(None),
            Provider.specialization != ''
        ).group_by(Provider.specialization).order_by(func.count(Provider.id).desc()).limit(10).all()
        
        # Booking trends (daily for the period)
        booking_trends = db.session.query(
            func.date(Booking.created_at).label('date'),
            func.count(Booking.id).label('count')
        ).filter(
            Booking.created_at >= start_date
        ).group_by(func.date(Booking.created_at)).order_by(func.date(Booking.created_at)).all()
        
        # Top providers by bookings
        top_providers = db.session.query(
            User.full_name,
            Provider.id,
            func.count(Booking.id).label('booking_count'),
            Provider.rating
        ).join(Provider, User.id == Provider.user_id).join(
            Booking, Provider.id == Booking.provider_profile_id
        ).filter(
            Booking.created_at >= start_date
        ).group_by(User.full_name, Provider.id, Provider.rating).order_by(
            func.count(Booking.id).desc()
        ).limit(10).all()
        
        return jsonify({
            'users': {
                'total': total_users,
                'clients': total_clients,
                'providers': total_providers,
                'verified_providers': verified_providers
            },
            'bookings': {
                'total': total_bookings,
                'in_period': bookings_in_period,
                'pending': pending_bookings,
                'completed': completed_bookings,
                'cancelled': cancelled_bookings
            },
            'revenue': {
                'total': float(total_revenue),
                'in_period': float(revenue_in_period)
            },
            'ratings': {
                'average': round(avg_rating, 2)
            },
            'popular_specializations': [
                {'specialization': s[0], 'count': s[1]} for s in popular_specializations
            ],
            'booking_trends': [
                {'date': str(t[0]), 'count': t[1]} for t in booking_trends
            ],
            'top_providers': [
                {
                    'name': p[0],
                    'provider_id': p[1],
                    'booking_count': p[2],
                    'rating': float(p[3]) if p[3] else 0.0
                } for p in top_providers
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/search-analytics', methods=['GET'])
@admin_required
def get_search_analytics():
    """Get search analytics (popular searches)"""
    try:
        # This would typically be stored in a separate table
        # For now, return provider stats as proxy
        popular_searches = db.session.query(
            Provider.specialization,
            func.count(Provider.id).label('count')
        ).filter(
            Provider.specialization.isnot(None)
        ).group_by(Provider.specialization).order_by(
            func.count(Provider.id).desc()
        ).limit(20).all()
        
        return jsonify({
            'popular_searches': [
                {'term': s[0], 'count': s[1]} for s in popular_searches
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

