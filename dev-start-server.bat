@echo off
REM start_server.bat
REM Start FastAPI Server

cd /d "%~dp0\fullstack\backend"

echo Starting FastAPI server...

poetry run uvicorn app.main:app --reload --host 0.0.0.0
