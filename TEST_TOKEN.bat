@echo off
echo ========================================
echo   Testing JWT Token
echo ========================================
echo.

echo [1/2] Getting token from login...
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}" > login_response.json
echo.
echo Login response saved to login_response.json
echo.

echo [2/2] Extracting token and testing profile endpoint...
powershell -Command "$response = Get-Content login_response.json | ConvertFrom-Json; $token = $response.access_token; if ($token) { Write-Host 'Token extracted: ' $token.Substring(0, 30) '...'; $headers = @{'Authorization'='Bearer ' + $token}; try { $profile = Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/profile' -Headers $headers -UseBasicParsing; Write-Host 'Profile Status:' $profile.StatusCode; Write-Host 'Profile Data:' $profile.Content } catch { Write-Host 'Profile Error:' $_.Exception.Message; if ($_.Exception.Response) { $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream()); $responseBody = $reader.ReadToEnd(); Write-Host 'Error Response:' $responseBody } } } else { Write-Host 'No token in response' }"
echo.

echo ========================================
echo   Test Complete
echo ========================================
echo.
pause

