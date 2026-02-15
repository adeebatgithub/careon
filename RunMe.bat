@echo off
title Careon Runner

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Start server
echo ===============================
echo Starting Django server...
echo Open browser at http://127.0.0.1:8000/
echo ===============================
py manage.py runserver

pause
un