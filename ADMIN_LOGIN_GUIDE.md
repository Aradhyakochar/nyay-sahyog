# 🔐 Admin Login Guide

## 📋 Admin Credentials

**Username:** `admin`  
**Password:** `admin123`

---

## 🚀 How to Login as Admin

### Step 1: Go to Login Page
1. Open your browser
2. Navigate to: **http://localhost:3000/login**

### Step 2: Enter Admin Credentials
1. **Username:** `admin`
2. **Password:** `admin123`
3. Click **"Continue"**

### Step 3: Enter OTP
1. An **alert popup** will appear showing your OTP (6-digit code)
   - Example: `Your OTP is: 123456`
2. **Enter the OTP** in the form
3. Click **"Verify OTP"**

### Step 4: Access Admin Dashboard
1. After successful login, you'll be redirected to the home page
2. Look for **"Admin"** link in the navigation bar (top right)
3. Click **"Admin"** to go to: **http://localhost:3000/admin**

---

## ✅ What You'll See After Login

### Navigation Bar
- You'll see an **"Admin"** link in the navbar (only visible to admin users)

### Admin Dashboard Features
Once you access `/admin`, you can:
- **View Analytics** - Statistics about users, providers, bookings
- **Manage Users** - View, verify, activate/deactivate users
- **Manage Providers** - View and verify providers
- **Manage Bookings** - View all bookings in the system

---

## 🐛 Troubleshooting

### Issue: "Invalid username or password"
**Fix:** 
- Make sure you're using: `admin` / `admin123`
- Check if admin user exists in database (should be created automatically)

### Issue: OTP Not Appearing
**Fix:**
1. Check browser console (F12) for errors
2. Check backend console - should show: `📧 OTP for admin@nyaysahyog.com: 123456`
3. The OTP should appear in an alert popup

### Issue: "Admin" Link Not Showing
**Fix:**
1. Make sure you're logged in as admin
2. Check your user role - should be `admin`
3. Try refreshing the page
4. Check browser console for errors

### Issue: Can't Access `/admin` Route
**Fix:**
1. Make sure you're logged in
2. Make sure your user role is `admin` (not `client` or `advocate`)
3. Check browser console for 403 errors
4. Try logging out and logging back in

---

## 🧪 Verify Admin User Exists

If admin login doesn't work, check if admin user exists:

```powershell
cd C:\Users\KIIT\OneDrive\Desktop\projectR\backend
venv\Scripts\activate
python -c "from app import create_app; from models import User; app = create_app(); app.app_context().push(); admin = User.query.filter_by(username='admin').first(); print(f'Admin exists: {admin is not None}'); print(f'Role: {admin.role if admin else None}'); print(f'Is active: {admin.is_active if admin else None}')"
```

**Expected Output:**
```
Admin exists: True
Role: admin
Is active: True
```

If admin doesn't exist, it will be created automatically when you start the backend.

---

## 📝 Quick Test

Test admin login directly:

```powershell
$body = @{username='admin';password='admin123'} | ConvertTo-Json
Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/login' -Method POST -Body $body -ContentType 'application/json'
```

**Expected Response:**
```json
{
  "otp": "123456",
  "user_id": 1,
  "email_sent": false,
  "message": "OTP generated - check console or response"
}
```

---

## 🎯 Summary

1. **Login URL:** http://localhost:3000/login
2. **Credentials:** `admin` / `admin123`
3. **Enter OTP** from alert popup
4. **Click "Admin"** in navbar after login
5. **Access:** http://localhost:3000/admin

---

**Note:** Admin user is automatically created when backend starts if it doesn't exist.

