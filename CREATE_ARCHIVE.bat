@echo off
echo ========================================
echo   Nyay Sahyog - Create Archive
echo ========================================
echo.

echo [1/3] Creating temporary directory...
if exist "temp_archive" rmdir /s /q "temp_archive"
mkdir temp_archive
mkdir temp_archive\backend
mkdir temp_archive\frontend

echo [2/3] Copying files...
echo   - Backend files...
copy backend\*.py temp_archive\backend\ >nul 2>&1
copy backend\*.txt temp_archive\backend\ >nul 2>&1
copy backend\*.yml temp_archive\backend\ >nul 2>&1
copy backend\*.example temp_archive\backend\ >nul 2>&1
copy backend\Dockerfile temp_archive\backend\ >nul 2>&1

echo   - Frontend source...
xcopy frontend\src temp_archive\frontend\src\ /E /I /Q >nul 2>&1
copy frontend\*.json temp_archive\frontend\ >nul 2>&1
copy frontend\*.ts temp_archive\frontend\ >nul 2>&1
copy frontend\*.js temp_archive\frontend\ >nul 2>&1
copy frontend\*.html temp_archive\frontend\ >nul 2>&1
copy frontend\*.conf temp_archive\frontend\ >nul 2>&1
copy frontend\Dockerfile* temp_archive\frontend\ >nul 2>&1

echo   - Documentation and config...
copy *.md temp_archive\ >nul 2>&1
copy *.bat temp_archive\ >nul 2>&1
copy *.yml temp_archive\ >nul 2>&1

echo [3/3] Creating ZIP archive...
powershell -Command "Compress-Archive -Path temp_archive\* -DestinationPath nyay_sahyog_project.zip -Force"

echo.
echo  Archive created: nyay_sahyog_project.zip
echo.

echo Cleaning up...
rmdir /s /q "temp_archive"

echo.
echo ========================================
echo    Compression Complete!
echo ========================================
echo.
echo Archive: nyay_sahyog_project.zip
echo Location: %CD%
echo.
pause
