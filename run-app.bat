@echo off
REM SMRITHI Full-Stack Application Launcher
REM This script installs all dependencies and runs both frontend and backend

echo.
echo ============================================
echo   SMRITHI - Full-Stack Application Launcher
echo ============================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Checking Node.js and Python installations...
node --version
python --version
echo.

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing root dependencies...
    call npm install
    echo.
)

if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
    echo.
)

if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    echo.
)

echo.
echo ============================================
echo   Starting SMRITHI Full-Stack Application
echo ============================================
echo.
echo Backend will run on:  http://localhost:8000
echo Frontend will run on: http://localhost:5173
echo Swagger Docs:         http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the application
echo.

REM Start the application
call npm run dev

pause
