# 📋 Nyay Sahyog - Detailed Workflow Documentation

## 🎯 System Overview

**Nyay Sahyog** is a full-stack legal services marketplace connecting clients with verified legal professionals.

### **Tech Stack:**
- **Frontend:** React 18 + TypeScript + Vite + Tailwind CSS
- **Backend:** Flask + SQLAlchemy + JWT + Flask-CORS
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Authentication:** JWT + 2FA (OTP)
- **Deployment:** Docker + Docker Compose

---

## 🔄 Complete User Journey Workflows

### **WORKFLOW 1: Client Registration & First Booking**

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Client Visits Home Page                            │
│ URL: http://localhost:3000/                                 │
│                                                             │
│ Components:                                                 │
│ - Home.jsx renders                                          │
│ - Shows hero, features, stats, services, testimonials       │
│ - "Register" button visible                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Client Clicks "Register"                           │
│ URL: http://localhost:3000/register                         │
│                                                             │
│ Components:                                                 │
│ - Register.jsx renders                                      │
│ - Form fields: username, email, password, full_name, role   │
│ - LocationAutocomplete component for address               │
│ - Role selector (default: client)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Submit Registration Form                           │
│                                                             │
│ Frontend:                                                   │
│ - Register.jsx: handleSubmit()                             │
│ - Validates form data                                       │
│ - Cleans empty strings                                      │
│ - Calls AuthContext.register()                             │
│                                                             │
│ API Call:                                                   │
│ POST /api/auth/register                                     │
│ Body: {username, email, password, full_name, role, ...}    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Backend Processes Registration                     │
│                                                             │
│ Backend: auth.py - register()                              │
│ 1. Validates required fields                                │
│ 2. Checks username/email uniqueness                         │
│ 3. Creates User model                                       │
│ 4. Hashes password with bcrypt                              │
│ 5. Saves to database                                        │
│ 6. Creates JWT token (identity: str(user.id))             │
│ 7. Returns token + user data                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Auto-Login After Registration                      │
│                                                             │
│ Frontend: AuthContext.tsx                                   │
│ - Saves token to localStorage                              │
│ - Sets Authorization header                                │
│ - Sets user state                                          │
│ - Navigates to home page                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: Client Browses Providers                           │
│ URL: http://localhost:3000/providers                        │
│                                                             │
│ Components:                                                 │
│ - Providers.jsx renders                                    │
│ - Fetches providers on mount                               │
│                                                             │
│ API Call:                                                   │
│ GET /api/providers?page=1&per_page=10                      │
│                                                             │
│ Backend: providers.py - get_providers()                    │
│ - Queries Provider model with filters                      │
│ - Eager loads User data (joinedload)                        │
│ - Paginates results                                        │
│ - Returns providers array + pagination info               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 7: Client Views Provider Details                      │
│ URL: http://localhost:3000/providers/:id                    │
│                                                             │
│ Components:                                                 │
│ - ProviderDetail.jsx renders                               │
│ - Fetches provider details on mount                         │
│                                                             │
│ API Call:                                                   │
│ GET /api/providers/:id                                      │
│                                                             │
│ Backend: providers.py - get_provider()                      │
│ - Gets provider by ID                                       │
│ - Eager loads User and Reviews                             │
│ - Returns full provider data                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 8: Client Clicks "Book Consultation"                  │
│                                                             │
│ Components:                                                 │
│ - ProviderDetail.jsx: setShowBookingForm(true)             │
│ - Shows booking form                                        │
│ - Fields: date, duration, description, location, link       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 9: Client Submits Booking Form                        │
│                                                             │
│ Frontend: ProviderDetail.jsx - handleBookingSubmit()       │
│ 1. Validates user is client                                │
│ 2. Converts date to ISO 8601 format                        │
│ 3. Creates booking payload                                  │
│ 4. Calls API                                                │
│                                                             │
│ API Call:                                                   │
│ POST /api/bookings                                          │
│ Headers: Authorization: Bearer <token>                      │
│ Body: {provider_id, booking_date, fee, service_type, ...} │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 10: Backend Creates Booking                          │
│                                                             │
│ Backend: bookings.py - create_booking()                     │
│ 1. Validates JWT token (extracts user_id as string)        │
│ 2. Converts user_id to int                                 │
│ 3. Checks user role is 'client'                            │
│ 4. Validates required fields                               │
│ 5. Gets provider User and Provider records                 │
│ 6. Parses booking_date (handles multiple formats)          │
│ 7. Creates Booking model                                   │
│ 8. Saves to database                                        │
│ 9. Returns booking data                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 11: Booking Success                                   │
│                                                             │
│ Frontend: ProviderDetail.jsx                                │
│ - Shows success alert                                       │
│ - Resets form                                               │
│ - Navigates to /bookings                                   │
│                                                             │
│ Components:                                                 │
│ - Bookings.jsx renders                                      │
│ - Fetches user's bookings                                  │
│                                                             │
│ API Call:                                                   │
│ GET /api/bookings                                           │
│ Headers: Authorization: Bearer <token>                      │
│                                                             │
│ Backend: bookings.py - get_bookings()                       │
│ - Gets user_id from token                                   │
│ - Queries bookings for client                              │
│ - Eager loads client and provider data                      │
│ - Returns bookings array                                   │
└─────────────────────────────────────────────────────────────┘
```

---

### **WORKFLOW 2: Provider Login & Booking Management**

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Provider Logs In                                   │
│ URL: http://localhost:3000/login                             │
│                                                             │
│ Process: Same as client login (2FA with OTP)               │
│ Username: advocate1, advocate2, etc.                       │
│ Password: password123                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Provider Views Bookings                            │
│ URL: http://localhost:3000/bookings                         │
│                                                             │
│ Components:                                                 │
│ - Bookings.jsx renders                                      │
│ - Fetches bookings (filtered by provider_id)                │
│                                                             │
│ API Call:                                                   │
│ GET /api/bookings                                           │
│                                                             │
│ Backend: bookings.py - get_bookings()                       │
│ - Detects user role is 'advocate' (or other provider)      │
│ - Filters bookings by provider_id                          │
│ - Returns provider's bookings                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Provider Updates Booking Status                    │
│                                                             │
│ Components:                                                 │
│ - Bookings.jsx: handleStatusUpdate()                       │
│ - Shows status dropdown (pending → confirmed → completed)   │
│                                                             │
│ API Call:                                                   │
│ PUT /api/bookings/:id                                       │
│ Body: {status: 'confirmed'}                                │
│                                                             │
│ Backend: bookings.py - update_booking()                    │
│ - Validates user is provider or admin                      │
│ - Updates booking status                                   │
│ - Saves to database                                         │
│ - Returns updated booking                                  │
└─────────────────────────────────────────────────────────────┘
```

---

### **WORKFLOW 3: Admin Dashboard Access**

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Admin Logs In                                      │
│ Username: admin                                             │
│ Password: admin123                                          │
│                                                             │
│ Process: Same 2FA flow as other users                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Admin Sees "Admin" Link in Navbar                  │
│                                                             │
│ Components:                                                 │
│ - Navbar.jsx: Shows Admin link if user.role === 'admin'   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Admin Clicks "Admin" Link                          │
│ URL: http://localhost:3000/admin                             │
│                                                             │
│ Components:                                                 │
│ - App.tsx: PrivateRoute checks requiredRole='admin'        │
│ - AdminDashboard.jsx renders                               │
│ - Fetches analytics on mount                               │
│                                                             │
│ API Call:                                                   │
│ GET /api/admin/analytics                                    │
│ Headers: Authorization: Bearer <token>                      │
│                                                             │
│ Backend: admin.py - get_analytics()                         │
│ - admin_required decorator checks role                      │
│ - Queries database for stats                                │
│ - Calculates revenue, ratings, trends                       │
│ - Returns analytics data                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Admin Views Different Tabs                        │
│                                                             │
│ Components:                                                 │
│ - AdminDashboard.jsx: Tab buttons (Overview, Users, etc.)  │
│ - Fetches data based on activeTab                           │
│                                                             │
│ API Calls:                                                   │
│ - GET /api/admin/users (Users tab)                          │
│ - GET /api/admin/providers (Providers tab)                  │
│ - GET /api/admin/bookings (Bookings tab)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Admin Verifies User/Provider                       │
│                                                             │
│ Components:                                                 │
│ - AdminDashboard.jsx: handleVerify()                        │
│                                                             │
│ API Call:                                                   │
│ PUT /api/admin/users/:id/verify                             │
│ Body: {verify: true}                                        │
│                                                             │
│ Backend: admin.py - verify_user()                           │
│ - Updates user.is_verified                                 │
│ - Updates provider.is_verified (if exists)                  │
│ - Saves to database                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Flow (Detailed)

### **JWT Token Lifecycle:**

```
1. TOKEN CREATION
   ┌─────────────────────────────────────┐
   │ User logs in → OTP verified          │
   │                                      │
   │ Backend: auth.py                    │
   │ create_access_token(                │
   │   identity=str(user.id),  ← STRING! │
   │   additional_claims={role: ...}     │
   │ )                                    │
   │                                      │
   │ Returns: JWT token                   │
   └─────────────────────────────────────┘
   
2. TOKEN STORAGE
   ┌─────────────────────────────────────┐
   │ Frontend: AuthContext.tsx            │
   │ localStorage.setItem('token', token)│
   │ api.defaults.headers.common[        │
   │   'Authorization'                   │
   │ ] = `Bearer ${token}`               │
   └─────────────────────────────────────┘
   
3. TOKEN USAGE
   ┌─────────────────────────────────────┐
   │ Frontend makes API call             │
   │ GET /api/auth/profile               │
   │ Headers: Authorization: Bearer ...  │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ Backend: auth.py - get_profile()    │
   │ @jwt_required()                     │
   │ user_id_str = get_jwt_identity()    │
   │ user_id = int(user_id_str)  ← INT! │
   │ user = User.query.get(user_id)     │
   └─────────────────────────────────────┘
   
4. TOKEN VALIDATION
   ┌─────────────────────────────────────┐
   │ Flask-JWT-Extended:                 │
   │ - Validates signature               │
   │ - Checks expiry                     │
   │ - Extracts identity (string)        │
   │ - Returns to endpoint               │
   └─────────────────────────────────────┘
```

---

## 🗄️ Database Operations Flow

### **Booking Creation (Database Level):**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User submits booking form                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Backend validates and creates Booking object            │
│    booking = Booking(                                      │
│        client_id=user_id,                                   │
│        provider_id=provider.id,                             │
│        provider_profile_id=provider_profile.id,             │
│        booking_date=parsed_date,                            │
│        fee=fee,                                             │
│        status='pending'                                     │
│    )                                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SQLAlchemy Session                                       │
│    db.session.add(booking)                                  │
│    db.session.commit()                                      │
│                                                             │
│    SQL Generated:                                           │
│    INSERT INTO bookings (                                   │
│        client_id, provider_id, provider_profile_id,         │
│        booking_date, fee, status, ...                       │
│    ) VALUES (?, ?, ?, ?, ?, ?, ...)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Database (SQLite/PostgreSQL)                             │
│    - Validates foreign keys                                │
│    - Checks constraints                                    │
│    - Inserts record                                        │
│    - Returns new booking.id                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Backend returns booking data                            │
│    return jsonify({                                         │
│        'message': 'Booking created',                         │
│        'booking': booking.to_dict()                         │
│    }), 201                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagrams

### **Provider Search Flow:**

```
User Input (Search/Filters)
    │
    ▼
Frontend: Providers.jsx
    │
    ├─> Build query params
    │   {search, role, specialization, 
    │    min_fee, max_fee, city, ...}
    │
    ▼
API: GET /api/providers?search=...&role=...
    │
    ▼
Backend: providers.py - get_providers()
    │
    ├─> Parse query parameters
    │
    ├─> Build SQLAlchemy query
    │   query = Provider.query
    │   if role: query.filter(role=...)
    │   if search: query.filter(name.ilike(...))
    │   ...
    │
    ├─> Apply pagination
    │   pagination = query.paginate(page, per_page)
    │
    ├─> Eager load User data
    │   .options(joinedload(Provider.user))
    │
    ▼
Database Query Execution
    │
    ├─> SELECT providers.*, users.*
    │   FROM providers
    │   JOIN users ON providers.user_id = users.id
    │   WHERE ...
    │   LIMIT 10 OFFSET 0
    │
    ▼
Backend: Convert to dict
    │
    ├─> for provider in providers:
    │       provider.to_dict()
    │
    ▼
Return JSON Response
    │
    ▼
Frontend: Display Results
    │
    ├─> Render provider cards
    ├─> Show pagination controls
    └─> Update filter state
```

---

## 🔄 State Management Flow

### **Authentication State:**

```
┌─────────────────────────────────────────────────────────────┐
│ AuthContext.tsx (Global State)                              │
│                                                             │
│ State Variables:                                            │
│ - user: User | null                                         │
│ - loading: boolean                                          │
│                                                             │
│ Functions:                                                  │
│ - login(username, password)                                │
│ - register(userData)                                        │
│ - logout()                                                  │
│ - fetchUser()                                               │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐        ┌───────────────┐
│ Login.tsx     │        │ Register.jsx  │
│ Uses: login() │        │ Uses: register()│
└───────────────┘        └───────────────┘
        │                         │
        └────────────┬─────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ API Call (api.ts)                                           │
│ - Adds Authorization header                                 │
│ - Handles errors                                            │
│ - Redirects on 401                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Backend Response                                            │
│ - Returns token + user data                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ AuthContext Updates State                                   │
│ - setUser(userData)                                         │
│ - localStorage.setItem('token', token)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ All Components Re-render                                    │
│ - Navbar shows user name                                    │
│ - Private routes accessible                                 │
│ - User-specific content shown                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Workflow

### **Development Setup:**

```
1. CLONE/EXTRACT PROJECT
   └─> Extract archive
   └─> Navigate to project root

2. BACKEND SETUP
   └─> cd backend
   └─> python -m venv venv
   └─> venv\Scripts\activate
   └─> pip install -r requirements.txt
   └─> copy env.example .env
   └─> python seed_data.py

3. FRONTEND SETUP
   └─> cd frontend
   └─> npm install
   └─> copy env.example .env

4. START SERVERS
   └─> Terminal 1: python app.py (backend)
   └─> Terminal 2: npm run dev (frontend)

5. ACCESS APPLICATION
   └─> Frontend: http://localhost:3000
   └─> Backend: http://localhost:5000
```

### **Production Deployment (Docker):**

```
1. BUILD IMAGES
   └─> docker-compose -f docker-compose.prod.yml build

2. START SERVICES
   └─> docker-compose -f docker-compose.prod.yml up -d

3. VERIFY
   └─> Check logs: docker-compose logs
   └─> Test endpoints
```

---

## 📋 API Request/Response Examples

### **Login Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "client1",
  "password": "password123"
}
```

### **Login Response:**
```json
{
  "message": "OTP generated - check console or response",
  "otp": "123456",
  "user_id": 53,
  "email_sent": false
}
```

### **OTP Verification Request:**
```http
POST /api/auth/verify-otp
Content-Type: application/json

{
  "user_id": 53,
  "otp": "123456"
}
```

### **OTP Verification Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 53,
    "username": "client1",
    "email": "client1@example.com",
    "role": "client",
    "full_name": "Client User 1"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### **Create Booking Request:**
```http
POST /api/bookings
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "provider_id": 66,
  "booking_date": "2025-11-26T10:00:00",
  "duration_minutes": 60,
  "fee": 2748.0,
  "service_type": "consultation",
  "description": "Need legal consultation"
}
```

### **Create Booking Response:**
```json
{
  "message": "Booking created successfully",
  "booking": {
    "id": 21,
    "client_id": 53,
    "provider_id": 66,
    "status": "pending",
    "booking_date": "2025-11-26T10:00:00",
    "fee": 2748.0,
    "service_type": "consultation"
  }
}
```

---

## ✅ System Verification Checklist

### **Backend:**
- [x] All endpoints working
- [x] JWT authentication working
- [x] Database operations working
- [x] Error handling in place
- [x] Input validation working
- [x] Role-based access working

### **Frontend:**
- [x] All pages rendering
- [x] Routing working
- [x] Authentication flow working
- [x] API integration working
- [x] Error handling working
- [x] Loading states working

### **Integration:**
- [x] Frontend-backend communication working
- [x] Token management working
- [x] CORS configured correctly
- [x] Proxy configuration working

### **Features:**
- [x] User registration
- [x] User login (2FA)
- [x] Provider discovery
- [x] Booking creation
- [x] Booking management
- [x] Admin dashboard
- [x] Profile management

---

## 🎯 Final Status

**✅ ALL SYSTEMS OPERATIONAL**

- ✅ Code reviewed and verified
- ✅ All workflows documented
- ✅ All features tested
- ✅ Ready for compression
- ✅ Ready for deployment

**Status:** 🟢 **PRODUCTION READY**

