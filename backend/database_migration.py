"""Database migration script for PostgreSQL"""
from app import create_app
from models import db
import os

def migrate_to_postgresql():
    """Migrate from SQLite to PostgreSQL"""
    app = create_app()
    
    with app.app_context():
        # Get PostgreSQL connection string from environment
        postgres_url = os.environ.get('DATABASE_URL')
        
        if not postgres_url:
            print("DATABASE_URL not set. Using SQLite.")
            print("To use PostgreSQL, set DATABASE_URL environment variable:")
            print("  DATABASE_URL=postgresql://user:password@localhost:5432/nyay_sahyog")
            return
        
        # Update database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
        
        # Create all tables
        db.create_all()
        
        print("Database migration completed!")
        print(f"Using database: {postgres_url.split('@')[1] if '@' in postgres_url else postgres_url}")

if __name__ == '__main__':
    migrate_to_postgresql()

