# 🔍 Debug Login Issues

## ✅ Backend is Working!

I tested the backend directly and it's responding correctly:
- **Status**: 200 OK
- **Response**: `{"otp": "468338", "user_id": 53, "email_sent": false}`

---

## 🐛 If Login Still Not Working in Browser

### Step 1: Check Browser Console (F12)

1. Open http://localhost:3000/login
2. Press **F12** → **Console** tab
3. Try to login
4. Look for these messages:
   ```
   🔐 Attempting login with: { username: 'client1' }
   📡 API Base URL: /api
   ✅ Login response: { user_id: ..., otp: '...' }
   ```

### Step 2: Check Network Tab

1. Press **F12** → **Network** tab
2. Try to login
3. Look for request to `/api/auth/login`
4. Check:
   - **Status**: Should be 200
   - **Request URL**: Should be `http://localhost:3000/api/auth/login`
   - **Response**: Should have `user_id` and `otp`

### Step 3: Check Backend Console

Look at the backend terminal for:
```
📧 OTP for client1@example.com: 123456
```

---

## 🔧 Common Issues

### Issue 1: "Network Error" or "ECONNREFUSED"
**Fix**: Backend not running
```powershell
cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
venv\Scripts\activate
python app.py
```

### Issue 2: "404 Not Found"
**Fix**: Frontend proxy not working
- Restart frontend
- Check `frontend/.env` - should have `VITE_API_URL=` (empty)

### Issue 3: "Invalid username or password"
**Fix**: Wrong credentials
- Try: `client1` / `password123`
- Or: `admin` / `admin123`

### Issue 4: OTP Not Appearing
**Fix**: Check browser console
- Should see alert popup with OTP
- If not, check Network tab for response

### Issue 5: "CORS Error"
**Fix**: Backend CORS not enabled
- Check backend console for CORS errors
- Make sure `CORS(app)` is in `app.py`

---

## 🧪 Test Login Directly

```powershell
$body = @{username='client1';password='password123'} | ConvertTo-Json
Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/login' -Method POST -Body $body -ContentType 'application/json'
```

Should return: `{"otp": "...", "user_id": ...}`

---

## ✅ Expected Flow

1. **Enter credentials** → Click "Continue"
2. **Backend responds** with OTP
3. **Alert popup appears** with OTP code
4. **Enter OTP** in the form
5. **Click "Verify OTP"**
6. **Redirected to home** page (logged in)

---

## 🚨 If Still Not Working

**Share these details:**
1. Browser console errors (F12 → Console)
2. Network tab request/response (F12 → Network)
3. Backend console output
4. Exact error message you see

This will help me identify the exact issue!

