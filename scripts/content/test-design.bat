@echo off
REM Test the new design locally

cd /d C:\Users\dswann\Documents\GitHub\azure-noob-blog

echo.
echo ====================================
echo Azure Noob Blog - Testing v2.0 Design
echo ====================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Starting Flask development server...
echo.
echo Visit: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start Flask
python -m flask run
