@echo off
echo ========================================
echo   Testing Backend Connection
echo ========================================
echo.

echo [1/3] Testing Health Endpoint...
curl http://localhost:5000/api/health
echo.
echo.

echo [2/3] Testing Login Endpoint...
powershell -Command "$body = @{username='aarav.sharma';password='password123'} | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/login' -Method POST -Body $body -ContentType 'application/json'; Write-Host 'Status:' $response.StatusCode; Write-Host 'Response:' $response.Content"
echo.

echo [3/3] Checking if Backend is Running...
netstat -ano | findstr :5000
echo.

echo ========================================
echo   Test Complete!
echo ========================================
echo.
echo If you see errors above, the backend might not be running.
echo Run: cd backend && venv\Scripts\activate && python app.py
echo.
pause

