# 📁 Nyay Sahyog - Project Structure & Flowchart

## 📊 Quick Stats
- **Total Core Files:** ~50
- **Backend:** 13 files
- **Frontend:** 35+ files
- **Documentation:** 6 files
- **Scripts:** 2 files

## 🗂️ File Organization Flowchart

```
projectR/
│
├── 📄 ALL_COMMANDS.md          # All commands with file paths
├── 📄 TROUBLESHOOTING.md       # Common issues & fixes
├── 📄 PROJECT_STRUCTURE.md      # This file - project overview
│
├── 🐳 docker-compose.yml       # Docker setup (dev)
├── 🐳 docker-compose.prod.yml  # Docker setup (production)
│
├── 🔷 backend/                 # Flask Backend API
│   ├── 📄 app.py              # Main Flask app (entry point)
│   ├── 📄 config.py           # Configuration settings
│   ├── 📄 models.py            # Database models (User, Provider, Booking, etc.)
│   ├── 📄 auth.py              # Authentication routes (login, register, OTP, OAuth)
│   ├── 📄 providers.py         # Provider listing & search
│   ├── 📄 bookings.py          # Booking management
│   ├── 📄 admin.py             # Admin dashboard routes
│   ├── 📄 email_service.py     # Email functions (commented out)
│   ├── 📄 seed_data.py         # Sample data generator (providers, bookings)
│   ├── 📄 seed_people.py       # Additional people/users data (50 users)
│   ├── 📄 database_migration.py # PostgreSQL migration
│   ├── 📄 requirements.txt     # Python dependencies
│   ├── 📄 Dockerfile           # Backend Docker image
│   ├── 📄 env.example          # Environment template
│   ├── 📄 env.test.example     # Test environment template
│   └── 📄 .env                 # Your actual config (not in git)
│
└── ⚛️ frontend/                # React Frontend
    ├── 📄 package.json         # Node dependencies
    ├── 📄 vite.config.ts       # Vite configuration
    ├── 📄 index.html           # HTML entry point
    ├── 📄 Dockerfile           # Frontend Docker (dev)
    ├── 📄 Dockerfile.prod      # Frontend Docker (production)
    ├── 📄 nginx.conf           # Nginx config (production)
    ├── 📄 env.example          # Environment template
    ├── 📄 .env                 # Your actual config (not in git)
    │
    └── 📂 src/
        ├── 📄 main.tsx         # React entry point
        ├── 📄 App.tsx          # Main app component (routes)
        ├── 📄 App.css          # Global app styles
        ├── 📄 index.css        # Base styles
        │
        ├── 📂 components/      # Reusable components
        │   ├── Navbar.jsx      # Navigation bar
        │   ├── Navbar.css
        │   ├── Footer.tsx      # Footer with location
        │   ├── Footer.css
        │   ├── LocationAutocomplete.jsx
        │   ├── LocationAutocomplete.css
        │   ├── ProviderMap.jsx
        │   └── ProviderMap.css
        │
        ├── 📂 pages/           # Page components
        │   ├── Home.jsx        # Landing page
        │   ├── Home.css
        │   ├── Login.tsx       # Login page (2FA)
        │   ├── Register.jsx   # Registration
        │   ├── Providers.jsx   # Provider listing (Discover)
        │   ├── Providers.css
        │   ├── ProviderDetail.jsx
        │   ├── ProviderDetail.css
        │   ├── Bookings.jsx    # User bookings
        │   ├── Bookings.css
        │   ├── Profile.jsx     # User profile
        │   ├── Profile.css
        │   ├── AdminDashboard.jsx
        │   ├── AdminDashboard.css
        │   └── Auth.css        # Shared auth styles
        │
        ├── 📂 context/         # React Context (state)
        │   └── AuthContext.tsx # Authentication state
        │
        ├── 📂 services/        # API services
        │   └── api.ts          # Axios API client
        │
        └── 📂 types/           # TypeScript types
            └── index.ts        # Type definitions
```

## 🔄 Data Flow

```
User Action
    ↓
Frontend (React)
    ↓
API Service (api.ts)
    ↓
Backend API (Flask)
    ↓
Database (SQLite/PostgreSQL)
    ↓
Response
    ↓
Frontend Update
```

## 🎯 Key Files by Function

### **Authentication**
- `backend/auth.py` - Login, Register, OTP, OAuth
- `frontend/src/pages/Login.tsx` - Login UI
- `frontend/src/context/AuthContext.tsx` - Auth state

### **Provider Discovery**
- `backend/providers.py` - Provider API
- `frontend/src/pages/Providers.jsx` - Discover page
- `frontend/src/pages/ProviderDetail.jsx` - Provider profile

### **Bookings**
- `backend/bookings.py` - Booking API
- `frontend/src/pages/Bookings.jsx` - Booking management

### **Admin**
- `backend/admin.py` - Admin API
- `frontend/src/pages/AdminDashboard.jsx` - Admin UI

### **Configuration**
- `backend/config.py` - Backend config
- `backend/.env` - Backend secrets
- `frontend/.env` - Frontend config

## 📊 Database Models

```
User
  ├── Provider (if role = advocate/mediator/etc)
  ├── Booking (as client)
  ├── Booking (as provider)
  ├── Message (sent)
  ├── Message (received)
  └── OTP (for 2FA)

Provider
  ├── User (owner)
  ├── Booking
  └── Review

Booking
  ├── User (client)
  ├── User (provider)
  ├── Provider
  ├── Message
  └── Review

Review
  ├── Booking
  ├── Provider
  └── User (client)
```

## 🚀 Quick Start Files

1. **Start Backend:** `backend/app.py`
2. **Start Frontend:** `frontend/` → `npm run dev`
3. **Seed Data:** `backend/seed_data.py`
4. **Docker:** `docker-compose.yml`

## 📝 Environment Files

- `backend/env.example` → Copy to `backend/.env`
- `frontend/env.example` → Copy to `frontend/.env`

---

**Total Files:** ~50 core files (excluding node_modules, venv, etc.)

