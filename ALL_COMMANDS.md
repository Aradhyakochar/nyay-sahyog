# 🚀 All Commands - Quick Reference

**Project:** `C:\Users\KIIT\OneDrive\Desktop\projectR`  
**Backend:** `C:\Users\KIIT\OneDrive\Desktop\projectR\backend`  
**Frontend:** `C:\Users\KIIT\OneDrive\Desktop\projectR\frontend`

---

## ⚡ Quick Start (Recommended)

**One-click restart:**
```powershell
.\RESTART_ALL.bat
```

**Test backend connection:**
```powershell
.\TEST_BACKEND.bat
```

**If backend URL not found, see:** `FIX_BACKEND_URL.md`

**Or manually:**

---

## 1. First-Time Setup

1. **Create & activate backend virtualenv**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
   python -m venv venv
   venv\Scripts\activate
   ```
2. **Install backend dependencies**
   ```powershell
   pip install --upgrade pip
   pip install -r C:\Users\KIIT\OneDrive\Desktop\projectR\backend\requirements.txt
   ```
3. **Install frontend dependencies**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\frontend
   npm install
   ```

---

## 2. Daily Manual Workflow

1. **Start backend API**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
   venv\Scripts\activate
   python C:\Users\KIIT\OneDrive\Desktop\projectR\backend\app.py
   ```
2. **Start frontend (new terminal)**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\frontend
   npm run dev
   ```
3. **IMPORTANT: Seed sample data (creates test users & providers)**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
   venv\Scripts\activate
   python C:\Users\KIIT\OneDrive\Desktop\projectR\backend\seed_data.py
   ```
   **Creates:** 5 clients, 10 advocates, 3 mediators (all password: `password123`)

---

## 3. Docker Workflow

1. **Build & start everything**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR
   docker-compose up --build
   ```
2. **Run in background / view logs / stop**
   ```powershell
   # background
   docker-compose up -d
   # live logs
   docker-compose logs -f
   # stop & remove
   docker-compose down
   ```
3. **Common extras**
   ```powershell
   docker-compose exec backend python seed_data.py
   docker-compose build backend
   docker-compose build frontend
   docker-compose down -v   # remove volumes
   ```

---

## 4. Docker Image & Container Utilities

```powershell
# Build images directly
docker build -t nyay-sahyog-backend:latest -f C:\Users\KIIT\OneDrive\Desktop\projectR\backend\Dockerfile C:\Users\KIIT\OneDrive\Desktop\projectR\backend
docker build -t nyay-sahyog-frontend:latest -f C:\Users\KIIT\OneDrive\Desktop\projectR\frontend\Dockerfile C:\Users\KIIT\OneDrive\Desktop\projectR\frontend

# Run containers manually
docker run -d --name nyay-sahyog-backend -p 5000:5000 -v C:\Users\KIIT\OneDrive\Desktop\projectR\backend:/app nyay-sahyog-backend:latest
docker run -d --name nyay-sahyog-frontend -p 3000:3000 -v C:\Users\KIIT\OneDrive\Desktop\projectR\frontend:/app nyay-sahyog-frontend:latest

# Inspect / manage
docker ps
docker logs -f nyay-sahyog-backend
docker exec -it nyay-sahyog-backend python seed_data.py
docker stop nyay-sahyog-backend
docker rm nyay-sahyog-backend
```

---

## 5. Ngrok (optional share)

```powershell
# one-time setup
ngrok config add-authtoken 35t9H1vLSjfLi1HIILqJBdq1Fce_UNFNGw5fmYcFNWsntFqF

# tunnel the frontend dev server
ngrok http 3000

# diagnostics
ngrok config check
```

---

## 6. Cleanup Shortcuts

```powershell
docker rm -f $(docker ps -aq)          # remove all containers
docker rmi -f $(docker images -q)      # remove all images
docker system prune -a                 # reclaim space
docker volume prune                    # drop unused volumes
cd C:\Users\KIIT\OneDrive\Desktop\projectR
docker-compose down -v && docker system prune -a --volumes
```

---

## 7. Restart Everything

**Automatic (Recommended):**
```powershell
.\RESTART_ALL.bat
```

**Manual:**
1. Stop all: Close all terminal windows
2. Start backend: `cd backend && venv\Scripts\activate && python app.py`
3. Start frontend: `cd frontend && npm run dev`
4. Seed data: `cd backend && venv\Scripts\activate && python seed_data.py`

---

## 8. Environment & Data Setup

### Create Environment Files
```powershell
# Backend (development)
copy C:\Users\KIIT\OneDrive\Desktop\projectR\backend\env.example C:\Users\KIIT\OneDrive\Desktop\projectR\backend\.env

# Frontend
copy C:\Users\KIIT\OneDrive\Desktop\projectR\frontend\env.example C:\Users\KIIT\OneDrive\Desktop\projectR\frontend\.env
```

### What to Configure

**Backend `.env` - Required:**
- `SECRET_KEY` - Generate: `python -c "import secrets; print(secrets.token_hex(32))"`
- `JWT_SECRET_KEY` - Generate: `python -c "import secrets; print(secrets.token_hex(32))"`
- `DATABASE_URL` - Default: `sqlite:///nyay_sahyog.db` (works as-is)
- `GOOGLE_MAPS_API_KEY` - You have: `AIzaSyC0qqyeeC3FpuK4jcDdVTcV7aqAIEDpH9o`

**Backend `.env` - Optional (for full features):**
- `MAIL_USERNAME` & `MAIL_PASSWORD` - Gmail App Password (for 2FA emails)
- `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET` - Google OAuth (for "Sign in with Google")

**Frontend `.env` - Required:**
- `VITE_API_URL` - Default: `http://localhost:5000/api` (works as-is)
- `VITE_GOOGLE_MAPS_API_KEY` - Same as backend key

**📖 Full details:** See `ENV_SETUP_GUIDE.md` for complete instructions.

### Where Data is Stored
- **Manual/dev:** SQLite `C:\Users\KIIT\OneDrive\Desktop\projectR\backend\nyay_sahyog.db`
- **Testing:** SQLite `backend\nyay_sahyog_test.db` (when `FLASK_ENV=testing`)
- **Docker:** PostgreSQL volume `postgres-data` in `docker-compose.yml`

### Seed Dummy Data
```powershell
cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
venv\Scripts\activate
python seed_data.py
```
Creates: 5 clients, 10 advocates, 3 mediators, 20 bookings, reviews, messages  
**All passwords:** `password123` | **Admin:** `admin` / `admin123`

### Seed People Data (50 additional users)
```powershell
cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
venv\Scripts\activate
python seed_people.py
```
Creates: 50 additional client users from provided data  
**Password:** `password123` for all

---

## 8. Quick References

- **Configs**  
  `docker-compose.yml`, `backend\Dockerfile`, `frontend\Dockerfile`, `frontend\Dockerfile.prod`

- **Core app files**  
  `backend\app.py`, `backend\seed_data.py`, `backend\requirements.txt`, `frontend\package.json`

- **URLs**  
  Frontend dev `http://localhost:3000`  
  Backend health `http://localhost:5000/api/health`  
  Ngrok inspector `http://localhost:4040`

Ready to run! 🚀

