@echo off
echo ========================================
echo   Nyay Sahyog - Fresh Start
echo ========================================
echo.

echo Stopping all processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting Backend...
cd /d C:\Users\KIIT\OneDrive\Desktop\projectR\backend
call venv\Scripts\activate
start "Backend" cmd /k "python app.py"
timeout /t 3 /nobreak >nul

echo.
echo Starting Frontend...
cd /d C:\Users\KIIT\OneDrive\Desktop\projectR\frontend
start "Frontend" cmd /k "npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   ✓ Started!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo To seed data, run:
echo   cd backend
echo   venv\Scripts\activate
echo   python seed_data.py
echo.

