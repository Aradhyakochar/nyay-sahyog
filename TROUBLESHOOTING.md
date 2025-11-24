# Troubleshooting Guide

## 🔍 Common Issues & Fixes

### Issue 1: Discover Button Not Showing Lawyers/Providers

**Symptoms:**
- Clicking "Discover" shows "No providers found"
- Empty providers list
- Error message about failed to load providers

**Causes & Fixes:**

1. **No Data in Database**
   ```powershell
   # Seed sample data
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
   venv\Scripts\activate
   python seed_data.py
   ```
   This creates:
   - 5 clients
   - 10 advocates
   - 3 mediators
   - Sample bookings and reviews

2. **Backend Not Running**
   ```powershell
   # Start backend
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
   venv\Scripts\activate
   python app.py
   ```
   Should see: `Running on http://0.0.0.0:5000`

3. **API Connection Issue**
   - Check browser console (F12) for errors
   - Verify backend is on `http://localhost:5000`
   - Check `frontend\.env` has: `VITE_API_URL=http://localhost:5000/api`

4. **CORS Error**
   - Backend should have CORS enabled (already configured)
   - Check backend console for CORS errors

---

### Issue 2: Login Not Working

**Symptoms:**
- Login form doesn't submit
- OTP not showing
- "Authentication failed" error
- Stuck on login screen

**Causes & Fixes:**

1. **Backend Not Running**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
   venv\Scripts\activate
   python app.py
   ```

2. **OTP Not Showing**
   - **Email is disabled** - OTP is shown in:
     - Browser alert popup
     - Backend console (when running `python app.py`)
     - API response (check Network tab in browser)
   
   **How to get OTP:**
   - After clicking "Continue" on login, check:
     - Alert popup (should show OTP)
     - Backend terminal (shows: `📧 OTP for user@email.com: 123456`)
     - Browser console (F12 → Console tab)

3. **Wrong Credentials**
   - Default users from seed data:
     - Clients: `client1`, `client2`, etc. (password: `password123`)
     - Advocates: `advocate1`, `advocate2`, etc. (password: `password123`)
     - Admin: `admin` (password: `admin123`)

4. **API Error**
   - Check browser console (F12) for errors
   - Check Network tab for failed requests
   - Verify backend is responding: `http://localhost:5000/api/health`

---

## 🚀 Quick Diagnostic Steps

### Step 1: Check Backend
```powershell
# Test backend health
curl http://localhost:5000/api/health
# Should return: {"status": "ok", ...}
```

Or open in browser: `http://localhost:5000/api/health`

### Step 2: Check Frontend Connection
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try to login or load providers
4. Check if requests are going to `http://localhost:5000/api/...`
5. Check response status (should be 200)

### Step 3: Check Database
```powershell
cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
venv\Scripts\activate
python
```

```python
from app import create_app
from models import db, User, Provider

app = create_app()
with app.app_context():
    print(f"Users: {User.query.count()}")
    print(f"Providers: {Provider.query.count()}")
```

If counts are 0, run: `python seed_data.py`

---

## 🔧 Common Fixes

### Fix 1: Restart Everything
```powershell
# Stop all (Ctrl+C in terminals)
# Then restart:

# Terminal 1 - Backend
cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
venv\Scripts\activate
python app.py

# Terminal 2 - Frontend
cd C:\Users\KIIT\OneDrive\Desktop\projectR\frontend
npm run dev
```

### Fix 2: Clear Browser Cache
- Press `Ctrl+Shift+Delete`
- Clear cache and cookies
- Reload page (`Ctrl+F5`)

### Fix 3: Check Environment Variables
```powershell
# Backend .env should have:
notepad C:\Users\KIIT\OneDrive\Desktop\projectR\backend\.env

# Frontend .env should have:
notepad C:\Users\KIIT\OneDrive\Desktop\projectR\frontend\.env
```

### Fix 4: Reinstall Dependencies
```powershell
# Backend
cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd C:\Users\KIIT\OneDrive\Desktop\projectR\frontend
npm install
```

---

## 📋 Verification Checklist

Before reporting issues, verify:

- [ ] Backend is running (`python app.py`)
- [ ] Frontend is running (`npm run dev`)
- [ ] Backend health check works: `http://localhost:5000/api/health`
- [ ] Database has data (run `seed_data.py`)
- [ ] Browser console shows no errors
- [ ] Network tab shows successful API calls
- [ ] `.env` files are configured

---

## 🐛 Debug Mode

### Enable Detailed Logging

**Backend:**
Already enabled - check console output

**Frontend:**
1. Open browser DevTools (F12)
2. Console tab shows all logs
3. Network tab shows all API calls
4. Check for red errors

### Test API Directly

```powershell
# Test providers endpoint
curl http://localhost:5000/api/providers

# Test login endpoint
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"client1\",\"password\":\"password123\"}"
```

---

## 📞 Still Not Working?

1. **Check Error Messages:**
   - Backend console output
   - Browser console (F12)
   - Network tab responses

2. **Verify Setup:**
   - All dependencies installed
   - `.env` files created
   - Database exists

3. **Common Mistakes:**
   - Forgot to activate virtualenv
   - Backend not running
   - Wrong port numbers
   - Missing seed data

---

**Most issues are solved by:**
1. ✅ Running `seed_data.py` (creates test data)
2. ✅ Restarting backend and frontend
3. ✅ Checking browser console for errors

