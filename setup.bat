@echo off
title Real vs Fake News Detector - Setup

echo.
echo ====================================
echo  Real vs Fake News Detector Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Installing dependencies...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Setting up .env file...
echo.

if not exist .env (
    echo Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo Created .env file!
) else (
    echo .env file already exists
)

echo.
echo ====================================
echo      NEXT STEPS
echo ====================================
echo.
echo 1. Edit .env file and add your API key:
echo    - Get key from: https://newsapi.org/
echo    - Edit .env and replace: NEWSAPI_KEY=your_key_here
echo.
echo 2. Fetch news data:
echo    python fetch_news_data.py
echo.
echo 3. Train the model:
echo    python train_model_api.py
echo.
echo 4. Run the application:
echo    python app.py
echo.
echo Then open: http://localhost:5000
echo.
echo For more info, see: SETUP_GUIDE.md
echo.
pause
