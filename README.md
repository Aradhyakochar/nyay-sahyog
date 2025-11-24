# ⚖️ Nyay Sahyog - Legal Services e-Marketplace

A full-stack web application connecting clients with verified legal service providers.

## 🚀 Quick Start

### Option 1: Automatic Restart (Recommended)
```powershell
.\RESTART_ALL.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
cd backend
venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

**Terminal 3 - Seed Data (First Time):**
```powershell
cd backend
venv\Scripts\activate
python seed_data.py          # Creates providers, bookings, etc.
python seed_people.py        # Creates 50 additional client users (optional)
```

## 📋 Setup Checklist

- [ ] Copy `backend/env.example` to `backend/.env` and configure
- [ ] Copy `frontend/env.example` to `frontend/.env`
- [ ] Install backend deps: `pip install -r backend/requirements.txt`
- [ ] Install frontend deps: `npm install` (in frontend folder)
- [ ] Run `python seed_data.py` to create test data

## 🎯 Default Credentials

- **Clients:** `client1` to `client5` (password: `password123`)
- **Advocates:** `advocate1` to `advocate10` (password: `password123`)
- **Admin:** `admin` (password: `admin123`)

## 📁 Project Structure

See `PROJECT_STRUCTURE.md` for complete file organization.

## 🛠️ Tech Stack

- **Frontend:** React + TypeScript + Vite + Tailwind CSS
- **Backend:** Flask + SQLAlchemy + JWT
- **Database:** SQLite (dev) / PostgreSQL (Docker)
- **Features:** 2FA, OTP, JWT Auth, Google Maps

## 📚 Documentation

- `QUICK_START.md` - Fastest way to get started
- `ALL_COMMANDS.md` - All commands with file paths
- `PROJECT_STRUCTURE.md` - File organization flowchart
- `TROUBLESHOOTING.md` - Common issues & fixes
- `CHANGES_SUMMARY.md` - Recent enhancements

## 🌐 URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Health Check: http://localhost:5000/api/health

---

**Ready to use!** 🎉

