"""Data access layer using raw SQL queries (JDBC-style)"""
from db_connection import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from typing import Optional, List, Dict, Any

def row_to_dict(row, cursor_description=None):
    """Convert database row to dictionary"""
    if isinstance(row, dict):
        return row
    elif hasattr(row, 'keys'):
        return dict(row)
    elif cursor_description:
        return {desc[0]: val for desc, val in zip(cursor_description, row)}
    else:
        return dict(row)

# ============ USER OPERATIONS ============

def create_user(data: Dict[str, Any]) -> int:
    """Create a new user and return user ID"""
    query = """
    INSERT INTO users (username, email, password_hash, role, full_name, phone, address, city, state, pincode, is_verified, is_active, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    if db.db_type == 'sqlite':
        query = query.replace('%s', '?')
        query = query.replace('SERIAL', 'INTEGER')
        # SQLite uses different syntax
        query = """
        INSERT INTO users (username, email, password_hash, role, full_name, phone, address, city, state, pincode, is_verified, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    
    password_hash = generate_password_hash(data['password']) if 'password' in data else data.get('password_hash', '')
    now = datetime.utcnow()
    
    params = (
        data['username'],
        data['email'],
        password_hash,
        data.get('role', 'client'),
        data['full_name'],
        data.get('phone'),
        data.get('address'),
        data.get('city'),
        data.get('state'),
        data.get('pincode'),
        data.get('is_verified', False),
        data.get('is_active', True),
        now,
        now
    )
    
    if db.db_type == 'postgresql':
        # PostgreSQL - use RETURNING clause
        query = query.rstrip(')') + ' RETURNING id'
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            return result[0] if result else None
    else:
        # SQLite
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            user_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return user_id

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Get user by ID"""
    query = "SELECT * FROM users WHERE id = %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM users WHERE id = ?"
    
    result = db.execute(query, (user_id,), fetch_one=True, dict_cursor=True)
    if result:
        # Convert boolean fields for SQLite
        if db.db_type == 'sqlite':
            result['is_verified'] = bool(result['is_verified'])
            result['is_active'] = bool(result['is_active'])
    return result

def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user by username"""
    query = "SELECT * FROM users WHERE username = %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM users WHERE username = ?"
    
    result = db.execute(query, (username,), fetch_one=True, dict_cursor=True)
    if result and db.db_type == 'sqlite':
        result['is_verified'] = bool(result['is_verified'])
        result['is_active'] = bool(result['is_active'])
    return result

def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email"""
    query = "SELECT * FROM users WHERE email = %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM users WHERE email = ?"
    
    result = db.execute(query, (email,), fetch_one=True, dict_cursor=True)
    if result and db.db_type == 'sqlite':
        result['is_verified'] = bool(result['is_verified'])
        result['is_active'] = bool(result['is_active'])
    return result

def update_user(user_id: int, data: Dict[str, Any]) -> bool:
    """Update user"""
    fields = []
    params = []
    
    allowed_fields = ['full_name', 'phone', 'address', 'city', 'state', 'pincode', 'email', 'is_verified', 'is_active']
    for field in allowed_fields:
        if field in data:
            fields.append(f"{field} = %s" if db.db_type == 'postgresql' else f"{field} = ?")
            params.append(data[field])
    
    if 'password' in data:
        fields.append("password_hash = %s" if db.db_type == 'postgresql' else "password_hash = ?")
        params.append(generate_password_hash(data['password']))
    
    if not fields:
        return False
    
    fields.append("updated_at = %s" if db.db_type == 'postgresql' else "updated_at = ?")
    params.append(datetime.utcnow())
    params.append(user_id)
    
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
    if db.db_type == 'sqlite':
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
    
    db.execute(query, tuple(params))
    return True

def check_password(user: Dict, password: str) -> bool:
    """Check if password matches"""
    return check_password_hash(user['password_hash'], password)

# ============ PROVIDER OPERATIONS ============

def create_provider(data: Dict[str, Any]) -> int:
    """Create a provider profile"""
    query = """
    INSERT INTO providers (user_id, specialization, experience_years, bar_council_number, qualification, bio, consultation_fee, hourly_rate, is_verified, is_active, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    if db.db_type == 'sqlite':
        query = """
        INSERT INTO providers (user_id, specialization, experience_years, bar_council_number, qualification, bio, consultation_fee, hourly_rate, is_verified, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    
    now = datetime.utcnow()
    params = (
        data['user_id'],
        data.get('specialization'),
        data.get('experience_years', 0),
        data.get('bar_council_number'),
        data.get('qualification'),
        data.get('bio'),
        data.get('consultation_fee', 0.0),
        data.get('hourly_rate', 0.0),
        data.get('is_verified', False),
        data.get('is_active', True),
        now,
        now
    )
    
    if db.db_type == 'postgresql':
        # PostgreSQL - use RETURNING clause
        query = query.rstrip(')') + ' RETURNING id'
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            return result[0] if result else None
    else:
        # SQLite
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            provider_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return provider_id

def get_provider_by_id(provider_id: int) -> Optional[Dict]:
    """Get provider by ID"""
    query = "SELECT * FROM providers WHERE id = %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM providers WHERE id = ?"
    
    result = db.execute(query, (provider_id,), fetch_one=True, dict_cursor=True)
    if result and db.db_type == 'sqlite':
        result['is_verified'] = bool(result['is_verified'])
        result['is_active'] = bool(result['is_active'])
    return result

def get_provider_by_user_id(user_id: int) -> Optional[Dict]:
    """Get provider by user ID"""
    query = "SELECT * FROM providers WHERE user_id = %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM providers WHERE user_id = ?"
    
    result = db.execute(query, (user_id,), fetch_one=True, dict_cursor=True)
    if result and db.db_type == 'sqlite':
        result['is_verified'] = bool(result['is_verified'])
        result['is_active'] = bool(result['is_active'])
    return result

def update_provider(provider_id: int, data: Dict[str, Any]) -> bool:
    """Update provider"""
    fields = []
    params = []
    
    allowed_fields = ['specialization', 'experience_years', 'bar_council_number', 'qualification', 'bio', 'consultation_fee', 'hourly_rate', 'is_verified', 'is_active']
    for field in allowed_fields:
        if field in data:
            fields.append(f"{field} = %s" if db.db_type == 'postgresql' else f"{field} = ?")
            params.append(data[field])
    
    if not fields:
        return False
    
    fields.append("updated_at = %s" if db.db_type == 'postgresql' else "updated_at = ?")
    params.append(datetime.utcnow())
    params.append(provider_id)
    
    query = f"UPDATE providers SET {', '.join(fields)} WHERE id = %s"
    if db.db_type == 'sqlite':
        query = f"UPDATE providers SET {', '.join(fields)} WHERE id = ?"
    
    db.execute(query, tuple(params))
    return True

def update_provider_rating(provider_id: int, rating: float, total_reviews: int) -> bool:
    """Update provider rating"""
    query = "UPDATE providers SET rating = %s, total_reviews = %s, updated_at = %s WHERE id = %s"
    if db.db_type == 'sqlite':
        query = "UPDATE providers SET rating = ?, total_reviews = ?, updated_at = ? WHERE id = ?"
    
    db.execute(query, (rating, total_reviews, datetime.utcnow(), provider_id))
    return True

# ============ BOOKING OPERATIONS ============

def create_booking(data: Dict[str, Any]) -> int:
    """Create a booking"""
    query = """
    INSERT INTO bookings (client_id, provider_id, provider_profile_id, service_type, booking_date, duration_minutes, fee, status, description, meeting_link, location, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    if db.db_type == 'sqlite':
        query = """
        INSERT INTO bookings (client_id, provider_id, provider_profile_id, service_type, booking_date, duration_minutes, fee, status, description, meeting_link, location, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    
    now = datetime.utcnow()
    params = (
        data['client_id'],
        data['provider_id'],
        data['provider_profile_id'],
        data.get('service_type'),
        data['booking_date'],
        data.get('duration_minutes', 60),
        data['fee'],
        data.get('status', 'pending'),
        data.get('description'),
        data.get('meeting_link'),
        data.get('location'),
        now,
        now
    )
    
    if db.db_type == 'postgresql':
        # PostgreSQL - use RETURNING clause
        query = query.rstrip(')') + ' RETURNING id'
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            return result[0] if result else None
    else:
        # SQLite
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            booking_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return booking_id

def get_booking_by_id(booking_id: int) -> Optional[Dict]:
    """Get booking by ID"""
    query = "SELECT * FROM bookings WHERE id = %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM bookings WHERE id = ?"
    
    return db.execute(query, (booking_id,), fetch_one=True, dict_cursor=True)

def get_bookings_by_client_id(client_id: int) -> List[Dict]:
    """Get all bookings for a client"""
    query = "SELECT * FROM bookings WHERE client_id = %s ORDER BY booking_date DESC"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM bookings WHERE client_id = ? ORDER BY booking_date DESC"
    
    return db.execute(query, (client_id,), fetch_all=True, dict_cursor=True) or []

def get_bookings_by_provider_id(provider_id: int) -> List[Dict]:
    """Get all bookings for a provider"""
    query = "SELECT * FROM bookings WHERE provider_id = %s ORDER BY booking_date DESC"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM bookings WHERE provider_id = ? ORDER BY booking_date DESC"
    
    return db.execute(query, (provider_id,), fetch_all=True, dict_cursor=True) or []

def get_all_bookings() -> List[Dict]:
    """Get all bookings"""
    query = "SELECT * FROM bookings ORDER BY created_at DESC"
    return db.execute(query, fetch_all=True, dict_cursor=True) or []

def update_booking(booking_id: int, data: Dict[str, Any]) -> bool:
    """Update booking"""
    fields = []
    params = []
    
    allowed_fields = ['status', 'meeting_link', 'location', 'booking_date']
    for field in allowed_fields:
        if field in data:
            fields.append(f"{field} = %s" if db.db_type == 'postgresql' else f"{field} = ?")
            params.append(data[field])
    
    if not fields:
        return False
    
    fields.append("updated_at = %s" if db.db_type == 'postgresql' else "updated_at = ?")
    params.append(datetime.utcnow())
    params.append(booking_id)
    
    query = f"UPDATE bookings SET {', '.join(fields)} WHERE id = %s"
    if db.db_type == 'sqlite':
        query = f"UPDATE bookings SET {', '.join(fields)} WHERE id = ?"
    
    db.execute(query, tuple(params))
    return True

# ============ REVIEW OPERATIONS ============

def create_review(data: Dict[str, Any]) -> int:
    """Create a review"""
    query = """
    INSERT INTO reviews (booking_id, provider_id, client_id, rating, comment, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    if db.db_type == 'sqlite':
        query = """
        INSERT INTO reviews (booking_id, provider_id, client_id, rating, comment, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
    
    params = (
        data['booking_id'],
        data['provider_id'],
        data['client_id'],
        data['rating'],
        data.get('comment'),
        datetime.utcnow()
    )
    
    if db.db_type == 'postgresql':
        # PostgreSQL - use RETURNING clause
        query = query.rstrip(')') + ' RETURNING id'
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            return result[0] if result else None
    else:
        # SQLite
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            review_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return review_id

def get_review_by_booking_id(booking_id: int) -> Optional[Dict]:
    """Get review by booking ID"""
    query = "SELECT * FROM reviews WHERE booking_id = %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM reviews WHERE booking_id = ?"
    
    return db.execute(query, (booking_id,), fetch_one=True, dict_cursor=True)

def get_reviews_by_provider_id(provider_id: int, limit: int = 10) -> List[Dict]:
    """Get reviews for a provider"""
    query = "SELECT * FROM reviews WHERE provider_id = %s ORDER BY created_at DESC LIMIT %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM reviews WHERE provider_id = ? ORDER BY created_at DESC LIMIT ?"
    
    return db.execute(query, (provider_id, limit), fetch_all=True, dict_cursor=True) or []

def get_all_reviews_for_provider(provider_id: int) -> List[Dict]:
    """Get all reviews for a provider"""
    query = "SELECT * FROM reviews WHERE provider_id = %s"
    if db.db_type == 'sqlite':
        query = "SELECT * FROM reviews WHERE provider_id = ?"
    
    return db.execute(query, (provider_id,), fetch_all=True, dict_cursor=True) or []

# ============ MESSAGE OPERATIONS ============

def create_message(data: Dict[str, Any]) -> int:
    """Create a message"""
    query = """
    INSERT INTO messages (booking_id, sender_id, receiver_id, subject, content, is_read, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    if db.db_type == 'sqlite':
        query = """
        INSERT INTO messages (booking_id, sender_id, receiver_id, subject, content, is_read, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
    
    params = (
        data.get('booking_id'),
        data['sender_id'],
        data['receiver_id'],
        data.get('subject'),
        data['content'],
        data.get('is_read', False),
        datetime.utcnow()
    )
    
    if db.db_type == 'postgresql':
        # PostgreSQL - use RETURNING clause
        query = query.rstrip(')') + ' RETURNING id'
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            return result[0] if result else None
    else:
        # SQLite
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            message_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return message_id

def get_messages_by_user_id(user_id: int, booking_id: Optional[int] = None) -> List[Dict]:
    """Get messages for a user"""
    if booking_id:
        query = "SELECT * FROM messages WHERE (sender_id = %s OR receiver_id = %s) AND booking_id = %s ORDER BY created_at ASC"
        if db.db_type == 'sqlite':
            query = "SELECT * FROM messages WHERE (sender_id = ? OR receiver_id = ?) AND booking_id = ? ORDER BY created_at ASC"
        params = (user_id, user_id, booking_id)
    else:
        query = "SELECT * FROM messages WHERE sender_id = %s OR receiver_id = %s ORDER BY created_at ASC"
        if db.db_type == 'sqlite':
            query = "SELECT * FROM messages WHERE sender_id = ? OR receiver_id = ? ORDER BY created_at ASC"
        params = (user_id, user_id)
    
    results = db.execute(query, params, fetch_all=True, dict_cursor=True) or []
    if db.db_type == 'sqlite':
        for r in results:
            r['is_read'] = bool(r['is_read'])
    return results

def update_message_read(message_id: int, user_id: int) -> bool:
    """Mark message as read"""
    query = "UPDATE messages SET is_read = %s WHERE id = %s AND receiver_id = %s"
    if db.db_type == 'sqlite':
        query = "UPDATE messages SET is_read = ? WHERE id = ? AND receiver_id = ?"
    
    db.execute(query, (True, message_id, user_id))
    return True

# ============ OTP OPERATIONS ============

def create_otp(data: Dict[str, Any]) -> int:
    """Create an OTP"""
    query = """
    INSERT INTO otps (user_id, otp_code, expires_at, is_used, created_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    if db.db_type == 'sqlite':
        query = """
        INSERT INTO otps (user_id, otp_code, expires_at, is_used, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
    
    params = (
        data['user_id'],
        data['otp_code'],
        data['expires_at'],
        data.get('is_used', False),
        datetime.utcnow()
    )
    
    if db.db_type == 'postgresql':
        # PostgreSQL - use RETURNING clause
        query = query.rstrip(')') + ' RETURNING id'
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            return result[0] if result else None
    else:
        # SQLite
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            otp_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return otp_id

def get_valid_otp(user_id: int, otp_code: str) -> Optional[Dict]:
    """Get valid OTP for user"""
    query = """
    SELECT * FROM otps 
    WHERE user_id = %s AND otp_code = %s AND is_used = %s AND expires_at > %s
    ORDER BY created_at DESC
    LIMIT 1
    """
    if db.db_type == 'sqlite':
        query = """
        SELECT * FROM otps 
        WHERE user_id = ? AND otp_code = ? AND is_used = ? AND expires_at > ?
        ORDER BY created_at DESC
        LIMIT 1
        """
    
    now = datetime.utcnow()
    result = db.execute(query, (user_id, otp_code, False, now), fetch_one=True, dict_cursor=True)
    if result and db.db_type == 'sqlite':
        result['is_used'] = bool(result['is_used'])
    return result

def invalidate_user_otps(user_id: int) -> bool:
    """Invalidate all unused OTPs for a user"""
    query = "UPDATE otps SET is_used = %s WHERE user_id = %s AND is_used = %s"
    if db.db_type == 'sqlite':
        query = "UPDATE otps SET is_used = ? WHERE user_id = ? AND is_used = ?"
    
    db.execute(query, (True, user_id, False))
    return True

def mark_otp_used(otp_id: int) -> bool:
    """Mark OTP as used"""
    query = "UPDATE otps SET is_used = %s WHERE id = %s"
    if db.db_type == 'sqlite':
        query = "UPDATE otps SET is_used = ? WHERE id = ?"
    
    db.execute(query, (True, otp_id))
    return True

def delete_expired_otps(limit: int = 100) -> int:
    """Delete expired OTPs"""
    query = "DELETE FROM otps WHERE expires_at < %s LIMIT %s"
    if db.db_type == 'sqlite':
        query = "DELETE FROM otps WHERE expires_at < ? LIMIT ?"
    
    return db.execute(query, (datetime.utcnow(), limit))

# ============ QUERY HELPERS ============

def get_users_with_filters(role: Optional[str] = None, is_active: Optional[bool] = None, search: Optional[str] = None, page: int = 1, per_page: int = 20) -> Dict:
    """Get users with filters and pagination"""
    conditions = []
    params = []
    
    if role:
        conditions.append("role = %s" if db.db_type == 'postgresql' else "role = ?")
        params.append(role)
    
    if is_active is not None:
        conditions.append("is_active = %s" if db.db_type == 'postgresql' else "is_active = ?")
        params.append(1 if is_active else 0)
    
    if search:
        conditions.append("(username LIKE %s OR email LIKE %s OR full_name LIKE %s)" if db.db_type == 'postgresql' else "(username LIKE ? OR email LIKE ? OR full_name LIKE ?)")
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])
    
    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    
    # Count total
    count_query = f"SELECT COUNT(*) FROM users {where_clause}"
    total = db.execute(count_query, tuple(params), fetch_one=True)
    if isinstance(total, tuple):
        total = total[0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    query = f"SELECT * FROM users {where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
    if db.db_type == 'sqlite':
        query = f"SELECT * FROM users {where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?"
    
    params.extend([per_page, offset])
    results = db.execute(query, tuple(params), fetch_all=True, dict_cursor=True) or []
    
    if db.db_type == 'sqlite':
        for r in results:
            r['is_verified'] = bool(r['is_verified'])
            r['is_active'] = bool(r['is_active'])
    
    return {
        'items': results,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def get_providers_with_filters(verified: Optional[bool] = None, page: int = 1, per_page: int = 20) -> Dict:
    """Get providers with filters and pagination"""
    conditions = ["p.is_active = 1", "u.is_active = 1"]
    params = []
    
    if verified is not None:
        conditions.append("p.is_verified = %s" if db.db_type == 'postgresql' else "p.is_verified = ?")
        params.append(1 if verified else 0)
    
    where_clause = "WHERE " + " AND ".join(conditions)
    
    # Count total
    count_query = f"SELECT COUNT(*) FROM providers p JOIN users u ON p.user_id = u.id {where_clause}"
    total = db.execute(count_query, tuple(params), fetch_one=True)
    if isinstance(total, tuple):
        total = total[0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    query = f"""
    SELECT p.*, u.* FROM providers p 
    JOIN users u ON p.user_id = u.id 
    {where_clause} 
    ORDER BY p.created_at DESC 
    LIMIT %s OFFSET %s
    """
    if db.db_type == 'sqlite':
        query = query.replace('%s', '?')
    
    params.extend([per_page, offset])
    results = db.execute(query, tuple(params), fetch_all=True, dict_cursor=True) or []
    
    if db.db_type == 'sqlite':
        for r in results:
            r['is_verified'] = bool(r.get('is_verified', 0))
            r['is_active'] = bool(r.get('is_active', 0))
    
    return {
        'items': results,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def get_bookings_with_filters(status: Optional[str] = None, page: int = 1, per_page: int = 20) -> Dict:
    """Get bookings with filters and pagination"""
    conditions = []
    params = []
    
    if status:
        conditions.append("status = %s" if db.db_type == 'postgresql' else "status = ?")
        params.append(status)
    
    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    
    # Count total
    count_query = f"SELECT COUNT(*) FROM bookings {where_clause}"
    total = db.execute(count_query, tuple(params), fetch_one=True)
    if isinstance(total, tuple):
        total = total[0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    query = f"SELECT * FROM bookings {where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
    if db.db_type == 'sqlite':
        query = f"SELECT * FROM bookings {where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?"
    
    params.extend([per_page, offset])
    results = db.execute(query, tuple(params), fetch_all=True, dict_cursor=True) or []
    
    return {
        'items': results,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def get_providers_search(search: str = '', role: str = '', specialization: str = '', verified_only: bool = False,
                        min_fee: Optional[float] = None, max_fee: Optional[float] = None,
                        min_rating: Optional[float] = None, city: str = '', state: str = '',
                        sort_by: str = 'rating', sort_order: str = 'desc', page: int = 1, per_page: int = 10) -> Dict:
    """Get providers with search, filters, and pagination"""
    conditions = ["u.is_active = 1", "p.is_active = 1"]
    params = []
    
    if verified_only:
        conditions.append("p.is_verified = 1")
    
    if role:
        conditions.append("u.role = %s" if db.db_type == 'postgresql' else "u.role = ?")
        params.append(role)
    
    if specialization:
        conditions.append("p.specialization LIKE %s" if db.db_type == 'postgresql' else "p.specialization LIKE ?")
        params.append(f"%{specialization}%")
    
    if min_fee is not None:
        conditions.append("p.consultation_fee >= %s" if db.db_type == 'postgresql' else "p.consultation_fee >= ?")
        params.append(min_fee)
    
    if max_fee is not None:
        conditions.append("p.consultation_fee <= %s" if db.db_type == 'postgresql' else "p.consultation_fee <= ?")
        params.append(max_fee)
    
    if min_rating is not None:
        conditions.append("p.rating >= %s" if db.db_type == 'postgresql' else "p.rating >= ?")
        params.append(min_rating)
    
    if city:
        conditions.append("u.city LIKE %s" if db.db_type == 'postgresql' else "u.city LIKE ?")
        params.append(f"%{city}%")
    
    if state:
        conditions.append("u.state LIKE %s" if db.db_type == 'postgresql' else "u.state LIKE ?")
        params.append(f"%{state}%")
    
    if search:
        conditions.append("(u.full_name LIKE %s OR u.username LIKE %s OR p.specialization LIKE %s OR p.bio LIKE %s OR u.city LIKE %s OR u.state LIKE %s)" if db.db_type == 'postgresql' else "(u.full_name LIKE ? OR u.username LIKE ? OR p.specialization LIKE ? OR p.bio LIKE ? OR u.city LIKE ? OR u.state LIKE ?)")
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term, search_term, search_term, search_term])
    
    where_clause = "WHERE " + " AND ".join(conditions)
    
    # Sorting
    sort_map = {
        'rating': 'p.rating',
        'fee': 'p.consultation_fee',
        'experience': 'p.experience_years'
    }
    sort_field = sort_map.get(sort_by, 'p.rating')
    order_clause = f"ORDER BY {sort_field} {'DESC' if sort_order == 'desc' else 'ASC'}"
    
    # Count total
    count_query = f"SELECT COUNT(*) FROM providers p JOIN users u ON p.user_id = u.id {where_clause}"
    total = db.execute(count_query, tuple(params), fetch_one=True)
    if isinstance(total, tuple):
        total = total[0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    query = f"""
    SELECT p.*, u.id as user_table_id, u.username, u.email, u.full_name, u.phone, u.address, u.city, u.state, u.pincode
    FROM providers p 
    JOIN users u ON p.user_id = u.id 
    {where_clause} 
    {order_clause}
    LIMIT %s OFFSET %s
    """
    if db.db_type == 'sqlite':
        query = query.replace('%s', '?')
    
    params.extend([per_page, offset])
    results = db.execute(query, tuple(params), fetch_all=True, dict_cursor=True) or []
    
    # Format results
    formatted_results = []
    for r in results:
        provider_data = {
            'id': r['id'],
            'user_id': r['user_id'],
            'specialization': r.get('specialization'),
            'experience_years': r.get('experience_years', 0),
            'bar_council_number': r.get('bar_council_number'),
            'qualification': r.get('qualification'),
            'bio': r.get('bio'),
            'consultation_fee': float(r.get('consultation_fee', 0.0)),
            'hourly_rate': float(r.get('hourly_rate', 0.0)),
            'rating': float(r.get('rating', 0.0)),
            'total_reviews': r.get('total_reviews', 0),
            'is_verified': bool(r.get('is_verified', 0)) if db.db_type == 'sqlite' else r.get('is_verified', False),
            'is_active': bool(r.get('is_active', 0)) if db.db_type == 'sqlite' else r.get('is_active', True),
            'created_at': r.get('created_at'),
            'user': {
                'id': r.get('user_table_id'),
                'username': r.get('username'),
                'email': r.get('email'),
                'full_name': r.get('full_name'),
                'phone': r.get('phone'),
                'address': r.get('address'),
                'city': r.get('city'),
                'state': r.get('state'),
                'pincode': r.get('pincode')
            }
        }
        formatted_results.append(provider_data)
    
    return {
        'providers': formatted_results,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }
    }

def get_specializations() -> List[str]:
    """Get list of all specializations"""
    query = "SELECT DISTINCT specialization FROM providers WHERE specialization IS NOT NULL AND specialization != ''"
    results = db.execute(query, fetch_all=True, dict_cursor=True) or []
    return [r['specialization'] for r in results if r.get('specialization')]

def get_provider_stats() -> Dict:
    """Get provider statistics"""
    total_query = "SELECT COUNT(*) FROM providers WHERE is_active = 1"
    verified_query = "SELECT COUNT(*) FROM providers WHERE is_active = 1 AND is_verified = 1"
    avg_rating_query = "SELECT AVG(rating) FROM providers WHERE is_active = 1 AND rating > 0"
    
    total = db.execute(total_query, fetch_one=True)
    verified = db.execute(verified_query, fetch_one=True)
    avg_rating = db.execute(avg_rating_query, fetch_one=True)
    
    if isinstance(total, tuple):
        total = total[0]
    if isinstance(verified, tuple):
        verified = verified[0]
    if isinstance(avg_rating, tuple):
        avg_rating = avg_rating[0] or 0.0
    
    return {
        'total_providers': total,
        'verified_providers': verified,
        'average_rating': round(float(avg_rating), 2) if avg_rating else 0.0
    }


