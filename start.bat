@echo off
REM SourceMatch - Start Backend and Frontend
REM This script starts both the backend and frontend servers

echo ========================================
echo SourceMatch - Starting Backend & Frontend
echo ========================================
echo.

REM Check if running from correct directory
if not exist "backend\main.py" (
    echo ERROR: Please run this script from the sourcematch_project root directory
    pause
    exit /b 1
)

REM Start backend in new window
echo Starting Backend (FastAPI on port 8000)...
start "SourceMatch Backend" cmd /k "cd backend && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in new window
echo Starting Frontend (React on port 3000)...
start "SourceMatch Frontend" cmd /k "cd frontend && npm start"

REM Display URLs
echo.
echo ========================================
echo Services started:
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Backend window will show startup logs
echo Frontend window will compile and open browser
echo.
pause
