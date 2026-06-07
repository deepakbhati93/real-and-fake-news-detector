# ✅ PROJECT VERIFICATION CHECKLIST

## Pre-Run Verification

Run this checklist BEFORE running the commands to ensure everything is set up.

### Files Check
```powershell
# Navigate to project
cd "C:\Users\DELL\Desktop\Learning Platform\real_fake_news"

# List required files
ls -Name

# You should see these files:
# - .env                    ← API key is here ✅
# - .env.example
# - .gitignore
# - requirements.txt
# - fetch_news_openai.py
# - train_model.py
# - app.py
# - frontend/
# - model/
# - QUICK_START.md
# - STEP_BY_STEP_GUIDE.md
# - FILES_REFERENCE.md
```

### Verify .env File
```powershell
# Check if .env exists
Test-Path .env

# Should return: True
```

### Verify API Key in .env
```powershell
# Check if API key is set
type .env

# You should see the line:
# OPENAI_API_KEY=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
```

### Check Python Installation
```powershell
# Verify Python is installed
python --version

# Should show: Python 3.8+ (version doesn't matter much)
```

---

## Installation Verification

After running `pip install -r requirements.txt`, verify packages:

```powershell
# Check installed packages
pip list

# You should see:
# Flask                    2.3.3
# flask-cors              4.0.0
# pandas                  2.0.3
# scikit-learn            1.3.1
# joblib                  1.3.2
# requests                2.31.0
# python-dotenv          1.0.0
# openai                  1.3.0
```

---

## Execution Verification

### ✅ After Step 1: `python fetch_news_openai.py`

You should see:
```
============================================================
News Classification with OpenAI GPT
============================================================

Fetching and classifying news articles using OpenAI...

Processing article 1/10: Scientists Discover...
  → Classification: REAL

Processing article 2/10: Global Stock Markets...
  → Classification: REAL

[... more articles ...]

============================================================
✓ Classified 10 articles using OpenAI
✓ Saved to: news_from_openai.csv
============================================================

Label distribution:
REAL    6
FAKE    4
Name: label, dtype: int64
```

**Files Created:**
```powershell
ls news_from_openai.csv   # Should exist

# Verify CSV has data
Import-Csv news_from_openai.csv | Select-Object -First 3
# Should show: title, text, label, source columns
```

---

### ✅ After Step 2: `python train_model.py`

You should see:
```
✓ Using OpenAI-classified data: news_from_openai.csv

[... training progress ...]

============================================================
MODEL ACCURACY: 95-100%
============================================================

Classification Report:
              precision    recall  f1-score   support

        FAKE       0.XX      0.XX      0.XX        X
        REAL       0.XX      0.XX      0.XX        X

[... more metrics ...]

✓ Model saved to: ./model/model.joblib
✓ Vectorizer saved to: ./model/vectorizer.joblib

============================================================
Training complete! Ready to run the Flask app.
============================================================
```

**Files Created:**
```powershell
ls model/               # Check directory exists
ls model/*.joblib       # Should show 2 .joblib files
```

---

### ✅ After Step 3: `python app.py`

You should see:
```
✓ Model and vectorizer loaded successfully.
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**The server is now running!** Keep this terminal open.

---

## Web Interface Verification

### ✅ Access the Website

1. Open browser
2. Go to: `http://localhost:5000`
3. You should see the **TruthLens** website with:
   - Navigation header
   - Hero section
   - News detector interface
   - Features section

### ✅ Test Text Analysis

1. Click "📝 Text Analysis" tab
2. Paste this text:
   ```
   Scientists at a major university published peer-reviewed research
   showing new findings about renewable energy. The study was funded 
   by the National Science Foundation.
   ```
3. Click "🔍 Analyze Truth Score"
4. Wait 2-3 seconds
5. **You should see:** ✅ Likely REAL News

---

## API Testing Verification

### ✅ Test Flask API

In another PowerShell window (keep app.py running):

```powershell
# Test with REAL news
$body = @{
    text = "Scientists discovered a new renewable energy source"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/analyze" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$response.Content

# Expected: {"prediction":"REAL"}
```

---

## Troubleshooting Verification

### Issue: "ModuleNotFoundError"

```powershell
# Verify package is installed
pip show openai

# If not installed:
pip install openai==1.3.0

# Verify again
pip show openai
```

### Issue: API Key Error

```powershell
# Verify .env file PATH
pwd   # Make sure you're in the right directory

# Verify .env content
type .env

# Should show your API key
```

### Issue: Port 5000 Already in Use

```powershell
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
Stop-Process -Id <PID> -Force

# Or use different port - edit app.py last line:
# app.run(port=5001, debug=True)
```

### Issue: Model Files Not Found

```powershell
# Verify model directory exists
ls model/

# If not, run training:
python train_model.py

# If error, run data collection first:
python fetch_news_openai.py
python train_model.py
```

---

## Complete Success Checklist

After all steps, verify:

- [ ] .env file exists with OpenAI API key
- [ ] requirements.txt packages installed
- [ ] fetch_news_openai.py ran successfully
- [ ] news_from_openai.csv created with 10 rows
- [ ] train_model.py ran successfully
- [ ] model/ folder has 2 .joblib files
- [ ] app.py running without errors
- [ ] Website loads at http://localhost:5000
- [ ] Can input text and get predictions
- [ ] Flask API responds to POST requests

---

## File Size Reference

After completing setup, file sizes should be approximately:

```
requirements.txt           ~200 bytes
.env                      ~500 bytes
fetch_news_openai.py      ~4 KB
train_model.py            ~4 KB
app.py                    ~1.5 KB
news_from_openai.csv      ~30-50 KB
model/model.joblib        ~100-200 KB
model/vectorizer.joblib   ~50-100 KB
```

If files are much smaller or don't exist, something went wrong. Re-run the steps.

---

## Performance Expectations

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| pip install | 1-3 minutes | First time slower |
| fetch_news_openai.py | 1-2 minutes | API calls take time |
| train_model.py | 30-60 seconds | ML training |
| app.py startup | 5-10 seconds | Model loading |
| Single prediction | 0.1-0.5 seconds | Very fast! |

---

## Next Steps After Verification

Once everything is verified:

1. ✅ Keep app.py running
2. ✅ Use the web interface at http://localhost:5000
3. ✅ Test with different news articles
4. ✅ Note accuracy and adjust as needed
5. ✅ Add more data when ready:
   - Get API key from NewsAPI
   - Update .env: NEWSAPI_KEY=...
   - Update fetch_news_openai.py
   - Re-run training

---

## Support Resources

| Problem | Solution | File |
|---------|----------|------|
| Setup confusion | Read this first | QUICK_START.md |
| Step-by-step help | Detailed guide | STEP_BY_STEP_GUIDE.md |
| File purposes | Reference all files | FILES_REFERENCE.md |
| Verification | This checklist | VERIFICATION_CHECKLIST.md |

---

## Quick Commands Reference

```powershell
# Navigate to project
cd "C:\Users\DELL\Desktop\Learning Platform\real_fake_news"

# Step 1: Install
pip install -r requirements.txt

# Step 2: Fetch & Classify
python fetch_news_openai.py

# Step 3: Train
python train_model.py

# Step 4: Run
python app.py

# Step 5: Open browser
# http://localhost:5000

# Step 6: Test (in another PowerShell)
$body = @{ text = "test news" } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:5000/analyze" -Method POST -Body $body -ContentType "application/json"
```

---

## ✅ YOU'RE ALL SET!

Follow the checklist above to verify everything is working. If all checks pass, your project is ready to use!

**Start with:** `QUICK_START.md`
**Need details?** `STEP_BY_STEP_GUIDE.md`
**Understanding files?** `FILES_REFERENCE.md`
