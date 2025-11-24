"""Main Flask application for Nyay Sahyog"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config
from models import db
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

if os.environ.get('FLASK_ENV') == 'testing':
    test_env_path = os.path.join(BASE_DIR, '.env.test')
    if os.path.exists(test_env_path):
        load_dotenv(test_env_path, override=True)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # JWT error handlers for better error messages
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"❌ Invalid token error: {str(error)}")
        return jsonify({'error': f'Invalid token: {str(error)}', 'details': 'Token may be malformed or signature is invalid'}), 422
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is missing'}), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Fresh token required'}), 401
    
    # EMAIL DISABLED - Mail initialized but not used (can be re-enabled later)
    mail = Mail(app)  # Keep for future use
    CORS(app)  # Enable CORS for React frontend
    
    # Initialize mail in auth module (commented out but kept for future)
    from auth import init_mail
    init_mail(mail)  # Keep initialized but not used
    
    # Register blueprints
    from auth import auth_bp
    from providers import providers_bp
    from bookings import bookings_bp
    from admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(providers_bp, url_prefix='/api/providers')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            
            # Create admin user if it doesn't exist (non-blocking)
            from models import User
            try:
                admin = User.query.filter_by(username='admin').first()
                if not admin:
                    admin = User(
                        username='admin',
                        email='admin@nyaysahyog.com',
                        role='admin',
                        full_name='System Administrator',
                        is_verified=True,
                        is_active=True
                    )
                    admin.set_password('admin123')
                    db.session.add(admin)
                    db.session.commit()
                    print("✅ Admin user created: username='admin', password='admin123'")
            except Exception as e:
                print(f"⚠️  Error creating admin user: {e}")
                db.session.rollback()
            
            # Clean up expired OTPs on startup (non-blocking, limit to avoid lag)
            try:
                from models import OTP
                expired_otps = OTP.query.filter(OTP.expires_at < datetime.utcnow()).limit(100).all()
                if expired_otps:
                    for otp in expired_otps:
                        db.session.delete(otp)
                    db.session.commit()
                    print(f"✅ Cleaned up {len(expired_otps)} expired OTPs")
            except Exception as e:
                print(f"⚠️  Error cleaning OTPs: {e}")
                db.session.rollback()
        except Exception as e:
            print(f"⚠️  Database initialization error: {e}")
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Nyay Sahyog API is running'}, 200
    
    @app.route('/api/config')
    def get_config():
        """Get public configuration"""
        return {
            'google_maps_api_key': app.config.get('GOOGLE_MAPS_API_KEY', '')
        }, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

