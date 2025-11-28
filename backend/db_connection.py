"""Database connection module using raw SQL (JDBC-style)"""
import os
import sqlite3
from contextlib import contextmanager
from urllib.parse import urlparse
import threading

# Optional PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    psycopg2 = None
    RealDictCursor = None

class DatabaseConnection:
    """Database connection manager using raw SQL"""
    
    _local = threading.local()
    
    def __init__(self, database_url=None):
        """Initialize database connection"""
        self.database_url = database_url or os.environ.get('DATABASE_URL') or 'sqlite:///nyay_sahyog.db'
        self._parse_database_url()
    
    def _parse_database_url(self):
        """Parse database URL to determine connection type"""
        if self.database_url.startswith('postgresql://') or self.database_url.startswith('postgres://'):
            parsed = urlparse(self.database_url)
            self.db_type = 'postgresql'
            self.db_config = {
                'host': parsed.hostname,
                'port': parsed.port or 5432,
                'database': parsed.path[1:] if parsed.path else 'nyay_sahyog',
                'user': parsed.username,
                'password': parsed.password
            }
        else:
            # SQLite
            self.db_type = 'sqlite'
            # Extract path from sqlite:///path
            if self.database_url.startswith('sqlite:///'):
                self.db_path = self.database_url.replace('sqlite:///', '')
            else:
                self.db_path = self.database_url
    
    @contextmanager
    def get_connection(self):
        """Get database connection (context manager)"""
        if self.db_type == 'postgresql':
            if not PSYCOPG2_AVAILABLE:
                raise ImportError("psycopg2 is required for PostgreSQL but is not installed. Install it with: pip install psycopg2-binary")
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = False
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
        else:
            # SQLite
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
    
    @contextmanager
    def get_cursor(self, dict_cursor=False):
        """Get database cursor (context manager)"""
        with self.get_connection() as conn:
            if self.db_type == 'postgresql':
                if dict_cursor:
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                else:
                    cursor = conn.cursor()
            else:
                cursor = conn.cursor()
            
            try:
                yield cursor
            finally:
                cursor.close()
    
    def execute(self, query, params=None, fetch_one=False, fetch_all=False, dict_cursor=False):
        """Execute SQL query"""
        with self.get_cursor(dict_cursor=dict_cursor) as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                result = cursor.fetchone()
                if dict_cursor and result:
                    return dict(result)
                return result
            elif fetch_all:
                results = cursor.fetchall()
                if dict_cursor and results:
                    return [dict(row) for row in results]
                return results
            else:
                return cursor.rowcount
    
    def execute_many(self, query, params_list):
        """Execute query multiple times with different parameters"""
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        create_tables_sql = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'client',
            full_name VARCHAR(200) NOT NULL,
            phone VARCHAR(20),
            address TEXT,
            city VARCHAR(100),
            state VARCHAR(100),
            pincode VARCHAR(10),
            is_verified BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        
        -- Providers table
        CREATE TABLE IF NOT EXISTS providers (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            specialization VARCHAR(200),
            experience_years INTEGER DEFAULT 0,
            bar_council_number VARCHAR(100),
            qualification TEXT,
            bio TEXT,
            consultation_fee REAL DEFAULT 0.0,
            hourly_rate REAL DEFAULT 0.0,
            rating REAL DEFAULT 0.0,
            total_reviews INTEGER DEFAULT 0,
            is_verified BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Bookings table
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES users(id),
            provider_id INTEGER NOT NULL REFERENCES users(id),
            provider_profile_id INTEGER NOT NULL REFERENCES providers(id),
            service_type VARCHAR(100),
            booking_date TIMESTAMP NOT NULL,
            duration_minutes INTEGER DEFAULT 60,
            fee REAL NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            description TEXT,
            meeting_link VARCHAR(500),
            location VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # SQLite uses different syntax
        if self.db_type == 'sqlite':
            create_tables_sql = create_tables_sql.replace('SERIAL', 'INTEGER')
            create_tables_sql = create_tables_sql.replace('REAL', 'REAL')
            create_tables_sql = create_tables_sql.replace('BOOLEAN', 'INTEGER')
            create_tables_sql = create_tables_sql.replace('TIMESTAMP', 'TIMESTAMP')
            create_tables_sql = create_tables_sql.replace('CURRENT_TIMESTAMP', "datetime('now')")
            create_tables_sql = create_tables_sql.replace('VARCHAR', 'VARCHAR')
            create_tables_sql = create_tables_sql.replace('TEXT', 'TEXT')
            # SQLite doesn't support SERIAL, use INTEGER PRIMARY KEY AUTOINCREMENT
            create_tables_sql = create_tables_sql.replace('id SERIAL PRIMARY KEY', 'id INTEGER PRIMARY KEY AUTOINCREMENT')
            # SQLite boolean: 0/1 instead of TRUE/FALSE
            create_tables_sql = create_tables_sql.replace('DEFAULT FALSE', 'DEFAULT 0')
            create_tables_sql = create_tables_sql.replace('DEFAULT TRUE', 'DEFAULT 1')
            create_tables_sql = create_tables_sql.replace('FALSE', '0')
            create_tables_sql = create_tables_sql.replace('TRUE', '1')
        
        # Split by semicolon and execute each statement
        statements = [s.strip() for s in create_tables_sql.split(';') if s.strip()]
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for statement in statements:
                if statement:
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        # Table might already exist, ignore
                        if 'already exists' not in str(e).lower() and 'duplicate' not in str(e).lower():
                            print(f"Warning: {e}")
            conn.commit()
            cursor.close()

# Global database instance
db = DatabaseConnection()

