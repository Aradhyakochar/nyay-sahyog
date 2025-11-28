@echo off
echo ========================================
echo Docker Error Fix Script
echo ========================================
echo.

echo [1/6] Stopping all Docker containers...
docker stop $(docker ps -aq) 2>nul
echo.

echo [2/6] Removing all containers...
docker rm $(docker ps -aq) 2>nul
echo.

echo [3/6] Removing old images with 'nyay-sahyog' in name...
docker images | findstr "nyay-sahyog" | for /f "tokens=3" %%a in ('more') do docker rmi %%a 2>nul
echo.

echo [4/6] Pruning Docker system...
docker system prune -f
echo.

echo [5/6] Checking Docker Desktop status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Desktop is not running or not accessible!
    echo Please:
    echo   1. Open Docker Desktop
    echo   2. Wait for it to fully start (whale icon should be steady)
    echo   3. Run this script again
    pause
    exit /b 1
)
echo Docker Desktop is running.
echo.

echo [6/6] Building and starting services...
docker compose down
docker compose up --build -d
echo.

echo ========================================
echo Fix complete!
echo ========================================
echo.
echo If errors persist, try:
echo   1. Restart Docker Desktop completely
echo   2. Run: docker system prune -a --volumes
echo   3. Check Docker Desktop Settings ^> Resources ^> Advanced
echo.
pause

