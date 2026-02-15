@echo off
title Django Project Runner

echo ===============================
echo Django Project Setup and Run
echo ===============================

REM Check Python
py --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed or not added to PATH.
    echo Please install Python from https://www.python.org
    pause
    exit /b
)

REM Create virtual environment if not exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    py -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
py -m pip install --upgrade pip

REM Install requirements
IF EXIST requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found!
    pause
    exit /b
)

REM Run migrations
echo Running migrations...
py manage.py migrate

REM Start server
echo ===============================
echo Starting Django server...
echo Open browser at http://127.0.0.1:8000/
echo ===============================
py manage.py runserver

pause
un