@echo off
echo ======================================================================
echo Starting CreditTransAct Fraud Analytics Full-Stack Local Server...
echo ======================================================================
cd /d "%~dp0"
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe server.py 8080
) else (
    python server.py 8080
)
pause
