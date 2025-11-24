@echo off
echo ========================================
echo   Testing Login Functionality
echo ========================================
echo.

echo [1/3] Testing Backend Health...
curl -s http://localhost:5000/api/health
if %errorlevel% neq 0 (
    echo ❌ Backend is NOT running!
    echo    Start it with: cd backend && venv\Scripts\activate && python app.py
    pause
    exit /b 1
)
echo.
echo ✅ Backend is running
echo.

echo [2/3] Testing Login Endpoint...
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"client1\",\"password\":\"password123\"}"
echo.
echo.

echo [3/3] Testing Frontend Connection...
curl -s http://localhost:3000 >nul
if %errorlevel% neq 0 (
    echo ❌ Frontend is NOT running!
    echo    Start it with: cd frontend && npm run dev
) else (
    echo ✅ Frontend is running
)
echo.

echo ========================================
echo   Test Complete
echo ========================================
echo.
echo If backend login works but browser login doesn't:
echo 1. Open browser console (F12)
echo 2. Check Network tab for /api/auth/login request
echo 3. Look for CORS errors or 404 errors
echo.
pause

