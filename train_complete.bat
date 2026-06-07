@echo off
REM Complete Training Script for Windows

echo.
echo ============================================================
echo.  REAL vs FAKE NEWS DETECTOR - COMPLETE SETUP
echo ============================================================
echo.

echo [Step 1] Installing dependencies...
pip install openai python-dotenv flask flask-cors scikit-learn pandas joblib numpy
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo [Step 1] Complete!

echo.
echo [Step 2] Fetching and classifying news data...
python fetch_news_openai.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to fetch news
    exit /b 1
)
echo [Step 2] Complete!

echo.
echo [Step 3] Training the model...
python train_model_enhanced.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to train model
    exit /b 1
)
echo [Step 3] Complete!

echo.
echo ============================================================
echo. TRAINING COMPLETE!
echo ============================================================
echo.
echo Next: Run the app with:
echo   python app.py
echo.
echo Then open your browser:
echo   http://127.0.0.1:5000
echo.
