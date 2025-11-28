"""Main Flask application for Nyay Sahyog"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from db_connection import db
from db_access import create_user, get_user_by_username
from dotenv import load_dotenv
import os

# Load environment files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    jwt = JWTManager(app)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 422
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is missing'}), 401
    
    CORS(app)  # Enable CORS for React frontend
    
    # Register blueprints
    from auth import auth_bp
    from providers import providers_bp
    from bookings import bookings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(providers_bp, url_prefix='/api/providers')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    
    # Create database tables and initialize
    with app.app_context():
        try:
            db.create_tables()
            
            # Create admin user if it doesn't exist
            try:
                admin = get_user_by_username('admin')
                if not admin:
                    create_user({
                        'username': 'admin',
                        'email': 'admin@nyaysahyog.com',
                        'password': 'admin123',
                        'role': 'admin',
                        'full_name': 'System Administrator',
                        'is_verified': True,
                        'is_active': True
                    })
                    print("✅ Admin user created: username='admin', password='admin123'")
            except Exception as e:
                print(f"⚠️  Error creating admin user: {e}")
        except Exception as e:
            print(f"⚠️  Database initialization error: {e}")
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Nyay Sahyog API is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

