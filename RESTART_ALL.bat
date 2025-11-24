@echo off
echo ========================================
echo   Nyay Sahyog - Complete Restart
echo ========================================
echo.

echo [1/5] Stopping all processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul
echo ✓ Processes stopped
echo.

echo [2/5] Cleaning Docker (if running)...
docker-compose down 2>nul
echo ✓ Docker cleaned
echo.

echo [3/5] Starting Backend...
start "Backend Server" cmd /k "cd /d C:\Users\KIIT\OneDrive\Desktop\projectR\backend && venv\Scripts\activate && python app.py"
timeout /t 3 /nobreak >nul
echo ✓ Backend starting...
echo.

echo [4/5] Starting Frontend...
start "Frontend Server" cmd /k "cd /d C:\Users\KIIT\OneDrive\Desktop\projectR\frontend && npm run dev"
timeout /t 3 /nobreak >nul
echo ✓ Frontend starting...
echo.

echo [5/5] Database Status...
echo    To seed data, run in new terminal:
echo    cd backend && venv\Scripts\activate && python seed_data.py
echo.

echo ========================================
echo   ✓ Restart Complete!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul

