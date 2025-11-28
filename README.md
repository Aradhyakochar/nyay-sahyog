# ⚖️ Nyay Sahyog - Legal Services Platform

A simple full-stack web application connecting clients with legal service providers.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm

### Setup

1. **Backend Setup:**
   ```powershell
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Frontend Setup:**
   ```powershell
   cd frontend
   npm install
   ```

3. **Start Application:**
   ```powershell
   # Option 1: Use the startup script
   .\START.bat
   
   # Option 2: Manual start
   # Terminal 1 - Backend:
   cd backend
   venv\Scripts\activate
   python app.py
   
   # Terminal 2 - Frontend:
   cd frontend
   npm run dev
   ```

## 📋 Default Credentials

- **Admin:** username=`admin`, password=`admin123`
- **Test Users:** Create via registration

## 🌐 URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Health Check: http://localhost:5000/api/health

## 🛠️ Tech Stack

- **Frontend:** React + TypeScript + Vite + Tailwind CSS
- **Backend:** Flask + JWT
- **Database:** SQLite

## 📁 Project Structure

```
projectR/
├── backend/          # Flask API
│   ├── app.py       # Main application
│   ├── auth.py      # Authentication routes
│   ├── providers.py # Provider routes
│   └── bookings.py  # Booking routes
├── frontend/         # React application
└── START.bat        # Startup script
```

## ✨ Features

- User registration and login
- Provider listing and search
- Booking management
- User profiles

---

**Ready to use!** 🎉
