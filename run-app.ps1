#!/usr/bin/env pwsh
# SMRITHI Full-Stack Application Launcher (PowerShell)
# This script installs all dependencies and runs both frontend and backend

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SMRITHI - Full-Stack Application Launcher" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
$nodeVersion = node --version 2>$null
if ($null -eq $nodeVersion) {
    Write-Host "ERROR: Node.js is not installed!" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is installed
$pythonVersion = python --version 2>$null
if ($null -eq $pythonVersion) {
    Write-Host "ERROR: Python is not installed!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Node.js version: $nodeVersion" -ForegroundColor Green
Write-Host "✓ Python version: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Install root dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing root dependencies..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

# Install backend dependencies
if (-not (Test-Path "backend\venv")) {
    Write-Host "Setting up Python virtual environment and dependencies..." -ForegroundColor Yellow
    cd backend
    python -m venv venv
    & ".\venv\Scripts\Activate.ps1"
    pip install -r requirements.txt
    cd ..
    Write-Host ""
}

# Install frontend dependencies
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    cd frontend
    npm install
    cd ..
    Write-Host ""
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Starting SMRITHI Full-Stack Application" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend will run on:  http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend will run on: http://localhost:5173" -ForegroundColor Green
Write-Host "Swagger Docs:         http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Start the application
npm run dev
