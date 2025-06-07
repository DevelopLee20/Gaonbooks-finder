@echo off
setlocal enabledelayedexpansion

:: 포터블 Python 경로 설정
set PYTHON=python\python.exe

:: 기본 시작 포트
set PORT=8000

:: 사용 가능한 포트 찾기
:find_port
netstat -aon | findstr :%PORT% >nul
if %ERRORLEVEL%==0 (
    set /a PORT+=1
    goto find_port
)

:: uvicorn 실행
%PYTHON% -m poetry run uvicorn app.main:app --port !PORT! --host 0.0.0.0

pause
