@echo off
echo ========================================
echo Starting Nyay Sahyog Application
echo ========================================
echo.

echo [1/2] Starting Backend...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python app.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Application started!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul

