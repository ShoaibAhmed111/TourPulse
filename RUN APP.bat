@echo off
title TourPulse Server
color 0B

echo ========================================================
echo        Launching TourPulse (http://localhost:5000)
echo ========================================================
echo.

cd /d "C:\Users\shoai\OneDrive\Documents\TourPulse"

:: Set Python executable path
set "PYTHON_EXE=C:\Users\shoai\AppData\Local\Python\pythoncore-3.14-64\python.exe"

:: 1. Launch default browser directly to localhost:5000
start explorer "http://localhost:5000"

:: 2. Start Uvicorn Server
"%PYTHON_EXE%" -m uvicorn app.main:app --reload --port 5000 --host 127.0.0.1

pause