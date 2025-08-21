@echo off
chcp 65001 >nul
echo ===========================================
echo CS Material Library - Development Environment
echo ===========================================

echo.
echo Starting backend service...
start "Backend" cmd /k "cd backend && python run_server.py"

echo.
echo Waiting for backend service to start...
timeout /t 3 /nobreak >nul

echo.
echo Starting frontend service...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ===========================================
echo Services started successfully!
echo Backend service: http://127.0.0.1:8000
echo Frontend service: http://localhost:3000
echo API documentation: http://127.0.0.1:8000/docs
echo ===========================================
echo.
echo Press any key to exit...
pause >nul
