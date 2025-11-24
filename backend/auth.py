"""Authentication routes and JWT handling"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_mail import Mail
from models import db, User, Provider, OTP
from datetime import datetime, timedelta
# EMAIL DISABLED - Imports kept for future use (can be re-enabled later)
from email_service import send_otp_email, send_welcome_email, generate_otp
auth_bp = Blueprint('auth', __name__)

# EMAIL DISABLED - Mail instance initialized but not used (can be re-enabled later)
# Mail instance will be initialized in app.py
mail = None

def init_mail(mail_instance):
    """Initialize mail instance (kept for future use)"""
    global mail
    mail = mail_instance

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
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            role=data['role'],
            full_name=data['full_name'],
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            pincode=data.get('pincode'),
            is_verified=False,
            is_active=True
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Get user.id
        
        # Create provider profile if role is a provider type
        provider_roles = ['advocate', 'mediator', 'arbitrator', 'notary', 'document_writer']
        if data['role'] in provider_roles:
            provider = Provider(
                user_id=user.id,
                specialization=data.get('specialization'),
                experience_years=data.get('experience_years', 0),
                bar_council_number=data.get('bar_council_number'),
                qualification=data.get('qualification'),
                bio=data.get('bio'),
                consultation_fee=data.get('consultation_fee', 0.0),
                hourly_rate=data.get('hourly_rate', 0.0),
                is_verified=False,
                is_active=True
            )
            db.session.add(provider)
        
        db.session.commit()
        
        # EMAIL DISABLED - Commented out for development (can be re-enabled later)
        # Send welcome email
        # try:
        #     if mail:
        #         send_welcome_email(mail, user.email, user.full_name)
        # except Exception as e:
        #     print(f"Error sending welcome email: {str(e)}")
        
        # Create access token (identity must be string)
        access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        
        print(f"✅ User registered successfully: {user.username} (ID: {user.id})")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint - Step 1: Generate and send OTP"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Generate OTP
        otp_code = generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=current_app.config.get('OTP_EXPIRY_MINUTES', 10))
        
        # Invalidate previous OTPs for this user
        OTP.query.filter_by(user_id=user.id, is_used=False).update({'is_used': True})
        
        # Create new OTP
        otp = OTP(
            user_id=user.id,
            otp_code=otp_code,
            expires_at=expires_at
        )
        db.session.add(otp)
        db.session.commit()
        
        # EMAIL DISABLED - OTP shown in console/response (can be re-enabled later)
        # Send OTP email
        # mail_password = current_app.config.get('MAIL_PASSWORD', '')
        # is_dev_mode = current_app.config.get('FLASK_ENV') == 'development'
        # email_configured = mail and mail_password and mail_password not in ['', 'dummy', 'dummy-password', 'app-password']
        # 
        # if email_configured:
        #     try:
        #         send_otp_email(mail, user.email, otp_code)
        #         print(f"✅ OTP email sent to {user.email}")
        #     except Exception as e:
        #         print(f"❌ Error sending OTP email: {str(e)}")
        #         email_configured = False
        # 
        # if is_dev_mode or not email_configured:
        #     print(f"📧 Email not configured - OTP for {user.email}: {otp_code}")
        #     return jsonify({
        #         'message': 'OTP generated (dev mode: check console or response)',
        #         'otp': otp_code,
        #         'user_id': user.id,
        #         'email_sent': email_configured
        #     }), 200
        # 
        # return jsonify({
        #     'message': 'OTP sent to your email. Please verify to complete login.',
        #     'user_id': user.id
        # }), 200
        
        # Always return OTP in response (email disabled)
        print(f"📧 OTP for {user.email}: {otp_code}")
        return jsonify({
            'message': 'OTP generated - check console or response',
            'otp': otp_code,
            'user_id': user.id,
            'email_sent': False
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP and complete login - Step 2"""
    try:
        data = request.get_json()
        
        if not data.get('user_id') or not data.get('otp'):
            return jsonify({'error': 'User ID and OTP are required'}), 400
        
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Find valid OTP
        otp = OTP.query.filter_by(
            user_id=user.id,
            otp_code=data['otp'],
            is_used=False
        ).order_by(OTP.created_at.desc()).first()
        
        if not otp or not otp.is_valid():
            return jsonify({'error': 'Invalid or expired OTP'}), 401
        
        # Mark OTP as used
        otp.is_used = True
        db.session.commit()
        
        # Create access token (identity must be string)
        access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/oauth/google', methods=['POST'])
def google_oauth():
    """Google OAuth login endpoint"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Google token is required'}), 400
        
        # Verify Google token
        try:
            GOOGLE_CLIENT_ID = current_app.config.get('GOOGLE_CLIENT_ID')
            if not GOOGLE_CLIENT_ID:
                return jsonify({'error': 'Google OAuth not configured'}), 500
            
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            google_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            picture = idinfo.get('picture', '')
            
        except ValueError:
            return jsonify({'error': 'Invalid Google token'}), 401
        
        # Find or create user
        user = User.query.filter_by(google_id=google_id).first()
        
        if not user:
            # Check if user exists with this email
            user = User.query.filter_by(email=email).first()
            
            if user:
                # Link Google account to existing user
                user.google_id = google_id
            else:
                # Create new user
                username = email.split('@')[0]
                # Ensure username is unique
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(
                    username=username,
                    email=email,
                    full_name=name,
                    role='client',
                    google_id=google_id,
                    is_verified=True,  # Google verified
                    is_active=True
                )
                # Set a random password (user won't use it)
                user.set_password(str(google_id))
                db.session.add(user)
                
                # EMAIL DISABLED - Commented out for development (can be re-enabled later)
                # Send welcome email
                # try:
                #     if mail:
                #         send_welcome_email(mail, user.email, user.full_name)
                # except Exception as e:
                #     print(f"Error sending welcome email: {str(e)}")
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        db.session.commit()
        
        # Create access token (identity must be string)
        access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
        
    except Exception as e:
        db.session.rollback()
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
        
        user = User.query.get_or_404(user_id)
        
        response_data = user.to_dict()
        
        # Include provider profile if exists
        if user.provider_profile:
            response_data['provider_profile'] = user.provider_profile.to_dict()
        
        print(f"✅ Profile response for user {user_id} ({user.username})")
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
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Update allowed fields
        updatable_fields = ['full_name', 'phone', 'address', 'city', 'state', 'pincode', 'email']
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        response_data = user.to_dict()
        if user.provider_profile:
            response_data['provider_profile'] = user.provider_profile.to_dict()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': response_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
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
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({'error': 'Old password and new password are required'}), 400
        
        if not user.check_password(data['old_password']):
            return jsonify({'error': 'Invalid old password'}), 401
        
        user.set_password(data['new_password'])
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

