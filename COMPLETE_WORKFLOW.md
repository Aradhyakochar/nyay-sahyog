# 📋 Nyay Sahyog - Complete Workflow & System Architecture

## 🎯 Project Overview

**Nyay Sahyog** is a full-stack legal services e-marketplace connecting clients with verified legal service providers (advocates, mediators, arbitrators, notaries, document writers).

---

## 🏗️ System Architecture

### **Three-Tier Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                          │
│  React + TypeScript Frontend (Port 3000)                 │
│  - User Interface                                        │
│  - State Management (Context API)                       │
│  - Routing (React Router)                               │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/REST API
                   │ (JWT Authentication)
┌──────────────────▼──────────────────────────────────────┐
│                  SERVER LAYER                            │
│  Flask Backend API (Port 5000)                          │
│  - Business Logic                                       │
│  - Authentication & Authorization                       │
│  - API Endpoints                                        │
│  - Data Validation                                      │
└──────────────────┬──────────────────────────────────────┘
                   │ SQLAlchemy ORM
┌──────────────────▼──────────────────────────────────────┐
│                  DATA LAYER                              │
│  SQLite (Dev) / PostgreSQL (Production)                 │
│  - User Data                                            │
│  - Provider Profiles                                    │
│  - Bookings                                             │
│  - Messages & Reviews                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Complete User Workflows

### **1. Client Registration & Login Flow**

```
┌─────────────┐
│   Client    │
│  Visits     │
│  /register  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Fill Registration Form  │
│ - Username, Email       │
│ - Password, Full Name   │
│ - Role: client          │
│ - Location (optional)   │
└──────┬──────────────────┘
       │ POST /api/auth/register
       ▼
┌─────────────────────────┐
│  Backend Creates User   │
│  - Hash password        │
│  - Create user record   │
│  - Generate JWT token   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Auto-Login & Redirect  │
│  - Save token           │
│  - Set auth header      │
│  - Navigate to home     │
└─────────────────────────┘

┌─────────────┐
│   Client    │
│  Visits     │
│  /login     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Enter Credentials       │
│ - Username              │
│ - Password              │
└──────┬──────────────────┘
       │ POST /api/auth/login
       ▼
┌─────────────────────────┐
│  Backend Validates      │
│  - Check credentials    │
│  - Generate 6-digit OTP│
│  - Store OTP in DB     │
│  - Return OTP in resp   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Show OTP Alert         │
│  (Email disabled)       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Enter OTP              │
└──────┬──────────────────┘
       │ POST /api/auth/verify-otp
       ▼
┌─────────────────────────┐
│  Backend Verifies OTP    │
│  - Check OTP validity   │
│  - Mark OTP as used     │
│  - Generate JWT token   │
│  - Return token + user  │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Login Success          │
│  - Save token           │
│  - Fetch user profile   │
│  - Navigate to home     │
└─────────────────────────┘
```

### **2. Provider Discovery Flow**

```
┌─────────────┐
│   Client    │
│  Clicks     │
│  "Discover" │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  GET /api/providers      │
│  - Apply filters         │
│  - Search, sort, paginate│
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Backend Queries DB      │
│  - Filter providers     │
│  - Eager load user data │
│  - Paginate results     │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Display Providers      │
│  - List or Map view     │
│  - Provider cards       │
│  - Filters sidebar      │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Click "View Profile"   │
└──────┬──────────────────┘
       │ GET /api/providers/:id
       ▼
┌─────────────────────────┐
│  Show Provider Details  │
│  - Full profile         │
│  - Reviews & ratings    │
│  - "Book" button        │
└─────────────────────────┘
```

### **3. Booking Creation Flow**

```
┌─────────────┐
│   Client    │
│  (Logged in)│
│  Views      │
│  Provider   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  Click "Book            │
│  Consultation"          │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Show Booking Form      │
│  - Date & Time          │
│  - Duration             │
│  - Description          │
│  - Location/Link        │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Submit Form            │
│  - Validate data        │
│  - Convert date to ISO  │
└──────┬──────────────────┘
       │ POST /api/bookings
       │ (JWT token in header)
       ▼
┌─────────────────────────┐
│  Backend Validates      │
│  - Check user role      │
│  - Verify provider      │
│  - Parse booking date   │
│  - Create booking record│
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Booking Created        │
│  - Status: pending      │
│  - Return booking data  │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Success & Redirect     │
│  - Show success message │
│  - Navigate to /bookings│
└─────────────────────────┘
```

### **4. Admin Dashboard Flow**

```
┌─────────────┐
│   Admin     │
│  Logs in    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  See "Admin" Link       │
│  in Navbar              │
└──────┬──────────────────┘
       │ Click
       ▼
┌─────────────────────────┐
│  GET /api/admin/*       │
│  (JWT with admin role)  │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Backend Checks Role    │
│  - Verify admin role    │
│  - Return data          │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Display Dashboard      │
│  - Analytics tab        │
│  - Users management     │
│  - Providers management │
│  - Bookings overview    │
└─────────────────────────┘
```

---

## 📁 File Structure & Responsibilities

### **Backend Files (Flask)**

| File | Purpose | Key Functions |
|------|---------|---------------|
| `app.py` | Main application entry | Creates Flask app, registers blueprints, initializes DB |
| `config.py` | Configuration | Environment variables, JWT settings, API keys |
| `models.py` | Database models | User, Provider, Booking, Review, Message, OTP models |
| `auth.py` | Authentication | Login, Register, OTP, Profile, Password change |
| `providers.py` | Provider management | List, search, filter, get provider details |
| `bookings.py` | Booking management | Create, update, list bookings, messages, reviews |
| `admin.py` | Admin dashboard | Analytics, user/provider management |
| `seed_data.py` | Sample data | Creates test users, providers, bookings |
| `seed_people.py` | People data | Seeds 50 specific client users |

### **Frontend Files (React)**

| File | Purpose | Key Features |
|------|---------|--------------|
| `App.tsx` | Main app component | Routes, layout, private routes |
| `main.tsx` | Entry point | React DOM render |
| `AuthContext.tsx` | Auth state | Login, register, fetch user, logout |
| `api.ts` | API client | Axios instance, interceptors, token handling |
| `Home.jsx` | Landing page | Hero, features, stats, services, testimonials |
| `Login.tsx` | Login page | 2FA with OTP, form handling |
| `Register.jsx` | Registration | User registration form |
| `Providers.jsx` | Provider listing | Search, filters, list/map view |
| `ProviderDetail.jsx` | Provider details | Profile, reviews, booking form |
| `Bookings.jsx` | Bookings page | List bookings, messages, status updates |
| `Profile.jsx` | User profile | View/edit profile |
| `AdminDashboard.jsx` | Admin panel | Analytics, user/provider management |

---

## 🔐 Authentication Flow (Detailed)

### **JWT Token Lifecycle:**

```
1. User Login
   └─> POST /api/auth/login
       └─> Validate credentials
       └─> Generate OTP
       └─> Return OTP + user_id

2. OTP Verification
   └─> POST /api/auth/verify-otp
       └─> Validate OTP
       └─> Create JWT token
           └─> identity: str(user.id)  ← STRING (not int!)
           └─> claims: {role: user.role}
       └─> Return token + user data

3. Token Storage
   └─> Frontend saves token in localStorage
   └─> Sets Authorization header: "Bearer <token>"

4. Protected Requests
   └─> All API calls include token in header
   └─> Backend validates token
       └─> Extract user_id (string)
       └─> Convert to int for DB query
       └─> Check user exists & active
       └─> Process request

5. Token Expiry
   └─> Token expires after 24 hours
   └─> Frontend redirects to login on 401
```

---

## 🗄️ Database Schema

### **Tables:**

1. **users**
   - id, username, email, password_hash
   - role (client/advocate/mediator/arbitrator/notary/document_writer/admin)
   - full_name, phone, address, city, state, pincode
   - is_verified, is_active
   - created_at, updated_at

2. **providers**
   - id, user_id (FK)
   - specialization, experience_years
   - bar_council_number, qualification, bio
   - consultation_fee, hourly_rate
   - rating, total_reviews
   - is_verified, is_active

3. **bookings**
   - id, client_id (FK), provider_id (FK), provider_profile_id (FK)
   - service_type, booking_date, duration_minutes
   - fee, status (pending/confirmed/completed/cancelled)
   - description, meeting_link, location
   - created_at, updated_at

4. **reviews**
   - id, booking_id (FK), provider_id (FK), client_id (FK)
   - rating, comment
   - created_at

5. **messages**
   - id, booking_id (FK), sender_id (FK), receiver_id (FK)
   - subject, content, is_read
   - created_at

6. **otps**
   - id, user_id (FK), otp_code
   - expires_at, is_used
   - created_at

---

## 🔄 API Endpoints

### **Authentication (`/api/auth`)**
- `POST /register` - User registration
- `POST /login` - Step 1: Get OTP
- `POST /verify-otp` - Step 2: Verify OTP & get token
- `GET /profile` - Get current user profile (JWT required)
- `PUT /profile` - Update profile (JWT required)
- `POST /change-password` - Change password (JWT required)
- `POST /oauth/google` - Google OAuth (commented out)

### **Providers (`/api/providers`)**
- `GET /` - List providers (search, filter, paginate)
- `GET /:id` - Get provider details
- `GET /specializations` - Get all specializations
- `GET /my-profile` - Get own provider profile (provider only)
- `PUT /my-profile` - Update own profile (provider only)

### **Bookings (`/api/bookings`)**
- `POST /` - Create booking (client only, JWT required)
- `GET /` - Get user's bookings (JWT required)
- `GET /:id` - Get booking details (JWT required)
- `PUT /:id` - Update booking status (JWT required)
- `POST /:id/reviews` - Create review (JWT required)
- `GET /:id/messages` - Get messages (JWT required)
- `POST /messages` - Send message (JWT required)
- `PUT /messages/:id/read` - Mark message as read (JWT required)

### **Admin (`/api/admin`)**
- `GET /analytics` - Platform analytics (admin only)
- `GET /users` - List all users (admin only)
- `PUT /users/:id/verify` - Verify user (admin only)
- `PUT /users/:id/activate` - Activate/deactivate user (admin only)
- `GET /providers` - List all providers (admin only)
- `GET /bookings` - List all bookings (admin only)

---

## 🚀 Deployment Workflow

### **Development:**
```
1. Start Backend
   └─> python app.py
       └─> Runs on http://localhost:5000
       └─> SQLite database
       └─> Debug mode ON

2. Start Frontend
   └─> npm run dev
       └─> Runs on http://localhost:3000
       └─> Vite dev server
       └─> Proxy /api → backend

3. Seed Data (first time)
   └─> python seed_data.py
       └─> Creates sample users, providers, bookings
```

### **Production (Docker):**
```
1. Build Images
   └─> docker-compose -f docker-compose.prod.yml build

2. Start Services
   └─> docker-compose -f docker-compose.prod.yml up
       └─> Backend + Frontend + PostgreSQL
       └─> Nginx reverse proxy
```

---

## 🔍 Code Quality Checks

### **Backend:**
- ✅ All JWT tokens use string identity
- ✅ All endpoints convert string ID to int
- ✅ Error handling with try-catch
- ✅ Database transactions with rollback
- ✅ Input validation on all endpoints
- ✅ Role-based access control

### **Frontend:**
- ✅ TypeScript for type safety
- ✅ Error handling in all API calls
- ✅ Loading states
- ✅ Private routes with role checks
- ✅ Token management in interceptors
- ✅ Responsive design

---

## 📦 Compression Guide

### **What to Include in Archive:**

**✅ Include:**
- All `.py` files (backend)
- All `.tsx`, `.ts`, `.jsx`, `.js` files (frontend)
- All `.css` files
- `package.json`, `requirements.txt`
- `vite.config.ts`, `tsconfig.json`
- `Dockerfile` files
- `docker-compose.yml` files
- `.env.example` files
- Documentation files (`.md`)
- Batch scripts (`.bat`)

**❌ Exclude:**
- `node_modules/` (can be reinstalled)
- `venv/` (can be recreated)
- `__pycache__/` (auto-generated)
- `dist/` (build output)
- `instance/*.db` (database file - can be regenerated)
- `.env` (contains secrets - use `.env.example`)

### **Compression Command:**
```powershell
# Create archive excluding unnecessary files
Compress-Archive -Path `
  backend\*.py,backend\*.txt,backend\*.yml,backend\*.example,backend\Dockerfile,`
  frontend\src,frontend\*.json,frontend\*.ts,frontend\*.js,frontend\*.html,frontend\*.conf,frontend\Dockerfile*,`
  *.md,*.bat,*.yml `
  -DestinationPath nyay_sahyog_project.zip `
  -Exclude node_modules,venv,__pycache__,dist,*.db
```

---

## ✅ Final Checklist

### **Functionality:**
- ✅ User registration
- ✅ User login with 2FA (OTP)
- ✅ Provider discovery with filters
- ✅ Provider detail view
- ✅ Booking creation
- ✅ Booking management
- ✅ Messaging system
- ✅ Reviews & ratings
- ✅ Admin dashboard
- ✅ Profile management

### **Security:**
- ✅ Password hashing (bcrypt)
- ✅ JWT authentication
- ✅ Role-based access control
- ✅ Input validation
- ✅ SQL injection prevention (ORM)

### **Performance:**
- ✅ Eager loading (joinedload)
- ✅ Database indexing
- ✅ Pagination
- ✅ Non-blocking startup

### **Code Quality:**
- ✅ Error handling
- ✅ Logging
- ✅ Type safety (TypeScript)
- ✅ Clean code structure

---

## 🎯 System Status: **FULLY FUNCTIONAL** ✅

All features tested and working:
- ✅ Authentication (Login/Register/2FA)
- ✅ Provider Discovery
- ✅ Booking System
- ✅ Admin Dashboard
- ✅ Messaging
- ✅ Reviews

**Ready for deployment!** 🚀


