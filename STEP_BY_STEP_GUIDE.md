# 📋 Step-by-Step Setup Guide - Real vs Fake News Detector

## Overview
This project uses **OpenAI API** to classify news articles, then trains a local ML model for fast analysis. The trained model runs on your Flask backend.

---

## ✅ STEP 1: Install Dependencies

Open PowerShell and navigate to your project folder:

```powershell
cd "C:\Users\DELL\Desktop\Learning Platform\real_fake_news"
```

Install required packages:

```powershell
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-2.3.3, flask-cors-4.0.0, pandas-2.0.3, scikit-learn-1.3.1, joblib-1.3.2, requests-2.31.0, python-dotenv-1.0.0, openai-1.3.0
```

---

## ✅ STEP 2: Verify API Key is Set

The `.env` file is already created with your OpenAI API key. Verify it exists:

```powershell
ls -Name | findstr ".env"
```

You should see `.env` in the list.

**Check the content (optional):**
```powershell
type .env
```

Should show:
```
OPENAI_API_KEY=sk-proj-eAMqotMSSG-...
```

---

## ✅ STEP 3: Fetch and Classify News Using OpenAI

Run the script that uses OpenAI to classify sample news articles:

```powershell
python fetch_news_openai.py
```

**What it does:**
- Uses OpenAI GPT-3.5 to classify 10 sample news articles
- May take 30-60 seconds (each API call ~3-5 seconds)
- Creates `news_from_openai.csv` with classified data

**Expected output:**
```
============================================================
News Classification with OpenAI GPT
============================================================

Fetching and classifying news articles using OpenAI...

Processing article 1/10: Scientists Discover New Species...
  → Classification: REAL

Processing article 2/10: Global Stock Markets Rise...
  → Classification: REAL
...
============================================================
✓ Classified 10 articles using OpenAI
✓ Saved to: news_from_openai.csv
============================================================

Label distribution:
REAL    6
FAKE    4
Name: label, dtype: int64
```

---

## ✅ STEP 4: Train the ML Model

Train the machine learning model using the classified data:

```powershell
python train_model.py
```

**What it does:**
- Reads `news_from_openai.csv`
- Converts text to TF-IDF features
- Trains Passive Aggressive Classifier
- Saves model to `./model/model.joblib`
- Saves vectorizer to `./model/vectorizer.joblib`

**Expected output:**
```
✓ Using OpenAI-classified data: news_from_openai.csv
Loading dataset from news_from_openai.csv...

Dataset shape: (10, 4)
Columns: ['title', 'text', 'label', 'source']

Label distribution:
REAL    6
FAKE    4
Name: label, dtype: int64

Splitting data (80% train, 20% test)...
✓ Training set: 8 samples
✓ Test set: 2 samples

Initializing TF-IDF Vectorizer...
Fitting TF-IDF on training data...
TF-IDF matrix shape (train): (8, 96)
TF-IDF matrix shape (test): (2, 96)

Training Passive Aggressive Classifier...
✓ Model training complete

Evaluating model...
============================================================
MODEL ACCURACY: 100.0%
============================================================

Classification Report:
...

✓ Model saved to: ./model/model.joblib
✓ Vectorizer saved to: ./model/vectorizer.joblib

============================================================
Training complete! Ready to run the Flask app.
============================================================
```

---

## ✅ STEP 5: Run the Flask App

Start the Flask backend server:

```powershell
python app.py
```

**Expected output:**
```
✓ Model and vectorizer loaded successfully.
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Note:** Keep this terminal open!

---

## ✅ STEP 6: Test the Application

Open another PowerShell window and test the API:

```powershell
$body = @{
    text = "Scientists discovered a new species of dinosaur in Antarctica"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/analyze" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$response.Content
```

**Expected output:**
```
{"prediction":"REAL"}
```

Or test with fake news:

```powershell
$body = @{
    text = "Aliens revealed secret government conspiracy to control minds with chips"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/analyze" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$response.Content
```

**Expected output:**
```
{"prediction":"FAKE"}
```

---

## ✅ STEP 7: Open Web Interface

In your browser, go to:

```
http://localhost:5000
```

You should see the TruthLens interface where you can:
- Paste news text and get predictions
- See if it's REAL or FAKE news

---

## 📂 Project Structure (After Running All Steps)

```
real_fake_news/
├── .env                          ✓ Contains your OpenAI API key
├── .env.example                  ✓ Template
├── .gitignore                    ✓ Prevents committing .env
├── requirements.txt              ✓ Dependencies
├── fetch_news_openai.py          ✓ Fetch & classify with OpenAI
├── train_model.py                ✓ Train ML model
├── app.py                        ✓ Flask backend
├── news_from_openai.csv          ✓ Generated by fetch_news_openai.py
├── news.csv                      (Old CSV - optional)
├── frontend/
│   ├── index.html                ✓ Web interface
│   ├── script.js                 ✓ JavaScript
│   └── style.css                 ✓ Styling
└── model/
    ├── model.joblib              ✓ Generated by train_model.py
    └── vectorizer.joblib         ✓ Generated by train_model.py
```

---

## 🔄 Adding Another API Later

When you want to add another API (like NewsAPI):

1. **Get API key** from the service
2. **Update `.env`:**
   ```
   NEWSAPI_KEY=your_newsapi_key_here
   ```
3. **Update `fetch_news_openai.py`** to add another data source
4. **Run the fetching script** to get new data
5. **Re-train the model:** `python train_model.py`

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'openai'"
**Solution:**
```powershell
pip install openai
```

### Error: "OPENAI_API_KEY not found in .env file"
**Solution:**
- Verify `.env` file exists
- Check it has: `OPENAI_API_KEY=sk-proj-...`

### Error: "Invalid API key provided"
**Solution:**
- Verify your API key is correct in `.env`
- Check your OpenAI account for active keys
- Ensure you have API credits available

### Flask server not starting
**Solution:**
- Make sure port 5000 is not in use
- Kill any existing Flask processes:
  ```powershell
  Get-Process python | Stop-Process
  ```

### Model files not found
**Solution:**
- Make sure you ran: `python fetch_news_openai.py`
- Make sure you ran: `python train_model.py`
- Check `./model/` directory exists and has files

---

## 📊 Expected Workflow

```
1. pip install -r requirements.txt           ← Install packages
2. python fetch_news_openai.py              ← Classify with OpenAI (creates CSV)
3. python train_model.py                    ← Train model (creates .joblib files)
4. python app.py                            ← Run Flask server
5. Open browser to http://localhost:5000    ← Use the web interface
```

---

## 🎯 Quick Commands Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Fetch & classify news | `python fetch_news_openai.py` |
| Train model | `python train_model.py` |
| Run Flask server | `python app.py` |
| Test API | See Step 6 above |

---

## ✨ Summary

✅ Your `.env` file has the OpenAI API key  
✅ `fetch_news_openai.py` will classify news using OpenAI  
✅ `train_model.py` will train a fast local ML model  
✅ `app.py` runs the Flask backend  
✅ `frontend/` has the web interface  

**You're all set! Follow the steps above to run the project.**
