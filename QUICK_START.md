# ⚡ Quick Start Guide

## 🚀 One-Command Start

```powershell
.\RESTART_ALL.bat
```

That's it! Opens backend and frontend in separate windows.

---

## 📋 First Time Setup

### 1. Install Dependencies

**Backend:**
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```powershell
cd frontend
npm install
```

### 2. Configure Environment

```powershell
# Backend
copy backend\env.example backend\.env
notepad backend\.env
# Generate keys: python -c "import secrets; print(secrets.token_hex(32))"

# Frontend
copy frontend\env.example frontend\.env
# Usually works as-is
```

### 3. Seed Data

```powershell
cd backend
venv\Scripts\activate
python seed_data.py
```

### 4. Start Everything

```powershell
.\RESTART_ALL.bat
```

---

## 🎯 Access

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5000/api/health
- **Login:** `client1` / `password123`

---

## 📚 More Info

- `README.md` - Overview
- `ALL_COMMANDS.md` - All commands
- `PROJECT_STRUCTURE.md` - File organization
- `TROUBLESHOOTING.md` - Fix issues

---

**Ready!** 🎉

