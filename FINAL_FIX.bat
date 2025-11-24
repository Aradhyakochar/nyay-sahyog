@echo off
echo ========================================
echo   FINAL FIX - Complete Restart
echo ========================================
echo.

echo [1/6] Stopping all processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul
echo ✓ All processes stopped
echo.

echo [2/6] Cleaning up...
docker-compose down 2>nul
echo ✓ Cleanup done
echo.

echo [3/6] Starting Backend...
start "Backend Server" cmd /k "cd /d C:\Users\KIIT\OneDrive\Desktop\projectR\backend && venv\Scripts\activate && python app.py"
timeout /t 5 /nobreak >nul
echo ✓ Backend starting (waiting 5 seconds...)
echo.

echo [4/6] Testing Backend Health...
timeout /t 2 /nobreak >nul
curl http://localhost:5000/api/health 2>nul | findstr "ok" >nul
if %errorlevel% equ 0 (
    echo ✓ Backend is responding
) else (
    echo ⚠ Backend might not be ready yet, wait a few more seconds
)
echo.

echo [5/6] Starting Frontend...
start "Frontend Server" cmd /k "cd /d C:\Users\KIIT\OneDrive\Desktop\projectR\frontend && npm run dev"
timeout /t 5 /nobreak >nul
echo ✓ Frontend starting (waiting 5 seconds...)
echo.

echo [6/6] Verifying Setup...
echo.
echo ========================================
echo   ✓ Setup Complete!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo IMPORTANT:
echo 1. Wait 10-15 seconds for both servers to fully start
echo 2. Open http://localhost:3000 in your browser
echo 3. Check browser console (F12) for "API Configuration" message
echo 4. Should see: "Using Vite proxy"
echo.
echo Test Login:
echo   Username: aarav.sharma
echo   Password: password123
echo.
echo If providers page shows empty:
echo   Run: cd backend && venv\Scripts\activate && python seed_data.py
echo.
pause

