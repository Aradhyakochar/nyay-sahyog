@echo off
echo ========================================
echo   Testing All Functionalities
echo ========================================
echo.

echo [1/8] Testing Backend Health...
curl -s http://localhost:5000/api/health | findstr "ok" >nul
if %errorlevel% equ 0 (
    echo ✅ Backend is running
) else (
    echo ❌ Backend is NOT running - Start it first!
    pause
    exit /b 1
)
echo.

echo [2/8] Testing Providers Endpoint...
curl -s http://localhost:5000/api/providers | findstr "providers" >nul
if %errorlevel% equ 0 (
    echo ✅ Providers endpoint working
) else (
    echo ❌ Providers endpoint failed
)
echo.

echo [3/8] Testing Login Endpoint...
powershell -Command "$body = @{username='client1';password='password123'} | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/login' -Method POST -Body $body -ContentType 'application/json' -UseBasicParsing -ErrorAction SilentlyContinue; if ($response.StatusCode -eq 200) { Write-Host '✅ Login endpoint working' } else { Write-Host '❌ Login endpoint failed' }"
echo.

echo [4/8] Testing Registration Endpoint...
powershell -Command "$body = @{username='testuser999';email='test999@example.com';password='test123';full_name='Test User';role='client'} | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/register' -Method POST -Body $body -ContentType 'application/json' -UseBasicParsing -ErrorAction SilentlyContinue; if ($response.StatusCode -eq 201) { Write-Host '✅ Registration endpoint working' } else { Write-Host '⚠️  Registration endpoint (may fail if user exists)' }"
echo.

echo [5/8] Testing Provider Details Endpoint...
curl -s http://localhost:5000/api/providers/1 | findstr "user" >nul
if %errorlevel% equ 0 (
    echo ✅ Provider details endpoint working
) else (
    echo ❌ Provider details endpoint failed (may need seeded data)
)
echo.

echo [6/8] Testing Specializations Endpoint...
curl -s http://localhost:5000/api/providers/specializations | findstr "specializations" >nul
if %errorlevel% equ 0 (
    echo ✅ Specializations endpoint working
) else (
    echo ❌ Specializations endpoint failed
)
echo.

echo [7/8] Checking Frontend...
netstat -ano | findstr :3000 >nul
if %errorlevel% equ 0 (
    echo ✅ Frontend is running on port 3000
) else (
    echo ❌ Frontend is NOT running - Start it first!
)
echo.

echo [8/8] Summary...
echo.
echo ========================================
echo   Test Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Open http://localhost:3000 in browser
echo 2. Try logging in: client1 / password123
echo 3. Go to Discover page - should show providers
echo 4. Click on a provider - should show details
echo 5. Try booking a consultation (must be logged in as client)
echo 6. Check Bookings page - should show your bookings
echo.
pause

