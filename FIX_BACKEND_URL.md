# 🔧 Fix Backend URL Not Found Issue

## ✅ Quick Fix

**The backend IS running**, but the frontend might not be connecting correctly.

### Step 1: Restart Frontend (Important!)

The frontend needs to be restarted to pick up the proxy configuration:

1. **Stop the frontend** (Ctrl+C in the frontend terminal)
2. **Restart it:**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\frontend
   npm run dev
   ```

### Step 2: Check Browser Console

1. Open your browser (http://localhost:3000)
2. Press **F12** to open DevTools
3. Go to **Console** tab
4. Look for: `API Base URL: /api | VITE_API_URL: ...`
5. Try logging in and check for errors

### Step 3: Verify Backend is Running

Open a new terminal and test:
```powershell
curl http://localhost:5000/api/health
```

Should return: `{"status":"ok","message":"Nyay Sahyog API is running"}`

### Step 4: Test Login Endpoint

```powershell
.\TEST_BACKEND.bat
```

---

## 🔍 Troubleshooting

### If you see "Network Error" or "ECONNREFUSED":

1. **Backend not running?**
   ```powershell
   cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
   venv\Scripts\activate
   python app.py
   ```

2. **Frontend proxy not working?**
   - Check `frontend/vite.config.ts` - proxy should forward `/api` to `http://localhost:5000`
   - Restart frontend after any config changes

3. **CORS errors?**
   - Backend has CORS enabled, but if you see CORS errors, check backend console
   - Make sure backend is running on `0.0.0.0:5000` (not just `127.0.0.1`)

### If you see "404 Not Found":

- The route might be wrong
- Check browser Network tab to see what URL is being requested
- Should be: `http://localhost:3000/api/auth/login` (frontend proxy)
- Which forwards to: `http://localhost:5000/api/auth/login` (backend)

---

## ✅ Expected Behavior

1. **Frontend console shows:** `API Base URL: /api | VITE_API_URL: (empty or undefined)`
2. **Login request goes to:** `http://localhost:3000/api/auth/login`
3. **Vite proxy forwards to:** `http://localhost:5000/api/auth/login`
4. **Backend responds with:** OTP code

---

## 🚀 Complete Restart (If Still Not Working)

```powershell
.\RESTART_ALL.bat
```

This will:
- Stop all processes
- Clean Docker
- Restart backend
- Restart frontend

Wait 5-10 seconds after running, then try again.

