# PowerShell Complete Training Script

Write-Host ""
Write-Host "============================================================"
Write-Host "  REAL vs FAKE NEWS DETECTOR - COMPLETE SETUP"
Write-Host "============================================================"
Write-Host ""

# Step 1: Install dependencies
Write-Host "[Step 1/3] Installing dependencies..."
Write-Host ""
pip install openai python-dotenv flask flask-cors scikit-learn pandas joblib numpy
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Step 1 Complete!`n"

# Step 2: Fetch and classify news
Write-Host "[Step 2/3] Fetching and classifying news data..."
Write-Host ""
python fetch_news_openai.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to fetch news" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Step 2 Complete!`n"

# Step 3: Train model
Write-Host "[Step 3/3] Training the model..."
Write-Host ""
python train_model_enhanced.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to train model" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Step 3 Complete!`n"

Write-Host "============================================================"
Write-Host "  TRAINING COMPLETE!"
Write-Host "============================================================"
Write-Host ""
Write-Host "Next: Run the app with:"
Write-Host "  python app.py"
Write-Host ""
Write-Host "Then open your browser:"
Write-Host "  http://127.0.0.1:5000"
Write-Host ""
