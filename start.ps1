# SourceMatch - Quick Start Script
# This script starts both backend and frontend in separate processes

Write-Host @"
================================================
    SourceMatch - Quick Start
================================================
    
This script will start:
  1. Backend API (FastAPI) on port 8000
  2. Frontend (React) on port 3000

Prerequisites:
  - Python venv activated
  - npm installed
  - Port 8000 and 3000 available

================================================
"@

# Check if we're in the right directory
if (-not (Test-Path "backend\main.py")) {
    Write-Host "ERROR: Must run from sourcematch_project root directory" -ForegroundColor Red
    exit 1
}

# Check if venv is activated
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERROR: venv not found. Please create it first:" -ForegroundColor Red
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList @"
    `$env:Path = "$($(Get-Location))\venv\Scripts;`$env:Path"
    cd "$(Get-Location)"
    python run_backend.py
"@ -NoNewWindow

Write-Host "Waiting 5 seconds for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "Starting Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList @"
    cd "$(Get-Location)\frontend"
    npm start
"@ -NoNewWindow

Write-Host @"

================================================
Services starting:
  Backend:  http://localhost:8000
  Frontend: http://localhost:3000
  API Docs: http://localhost:8000/docs
================================================

Waiting for services to start...
Open http://localhost:3000 in your browser.

Press any key to continue...
"@ -ForegroundColor Green

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
