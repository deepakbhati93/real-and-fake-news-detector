# 📁 Project Files Reference

## What Each File Does

### Configuration Files

| File | Purpose |
|------|---------|
| `.env` | **ALREADY CREATED** - Contains your OpenAI API key - KEEP SECRET! |
| `.env.example` | Template for .env file (safe to share) |
| `.gitignore` | Prevents .env from being committed to git |
| `requirements.txt` | List of Python packages to install |

### Python Scripts

| File | Purpose | When to Run |
|------|---------|------------|
| `fetch_news_openai.py` | Fetches sample news & classifies using OpenAI | **1st** - Creates `news_from_openai.csv` |
| `train_model.py` | Trains ML model on classified data | **2nd** - Creates model files |
| `train_model_api.py` | Alternative training script (not needed) | Optional |
| `app.py` | Flask web server backend | **3rd** - Runs the server |
| `fetch_news_data.py` | Alternative news fetcher (not needed) | Optional |

### Frontend Files

| File | Purpose |
|------|---------|
| `frontend/index.html` | Main web page |
| `frontend/script.js` | JavaScript for web interface |
| `frontend/style.css` | Styling for web page |

### Generated Files (Created During Running)

| File | Created By | Purpose |
|------|-----------|---------|
| `news_from_openai.csv` | `fetch_news_openai.py` | Dataset of classified articles |
| `model/model.joblib` | `train_model.py` | Trained machine learning model |
| `model/vectorizer.joblib` | `train_model.py` | Feature transformer for text |

### Documentation Files

| File | Purpose |
|------|---------|
| `QUICK_START.md` | **👈 START HERE** - 5-minute setup |
| `STEP_BY_STEP_GUIDE.md` | Detailed instructions with expected outputs |
| `SETUP_GUIDE.md` | Original setup guide (reference) |

---

## The Complete Workflow

```
.env (has API key)
   ↓
pip install -r requirements.txt
   ↓
python fetch_news_openai.py  ←→  OpenAI API
   ↓
news_from_openai.csv
   ↓
python train_model.py
   ↓
model/model.joblib + vectorizer.joblib
   ↓
python app.py
   ↓
Flask runs on http://localhost:5000
   ↓
frontend/ serves web interface
   ↓
User pastes news → JavaScript → Backend API
   ↓
Backend uses model.joblib to predict REAL/FAKE
   ↓
Result shown to user
```

---

## File Dependencies

```
fetch_news_openai.py
  ├── needs: .env (OPENAI_API_KEY)
  ├── needs: openai package
  ├── needs: pandas package
  ├── needs: requests package
  └── creates: news_from_openai.csv

train_model.py
  ├── needs: news_from_openai.csv (from fetch_news_openai.py)
  ├── needs: pandas, scikit-learn, joblib
  └── creates: model/model.joblib + model/vectorizer.joblib

app.py
  ├── needs: model/model.joblib (from train_model.py)
  ├── needs: model/vectorizer.joblib (from train_model.py)
  ├── needs: Flask, flask-cors
  └── serves: frontend/
  
frontend/
  ├── index.html (main page)
  ├── script.js (calls backend API)
  ├── style.css (styling)
  └── makes requests to: app.py /analyze endpoint
```

---

## Quick Reference Commands

```powershell
# Installation
pip install -r requirements.txt

# Data & Training
python fetch_news_openai.py     # Uses OpenAI API
python train_model.py            # Creates model

# Running
python app.py                     # Starts server

# Testing (in another PowerShell)
$body = @{ text = "your text here" } | ConvertTo-Json
$response = Invoke-WebRequest -Uri "http://localhost:5000/analyze" -Method POST -Body $body -ContentType "application/json"
$response.Content
```

---

## Environment Variables (.env)

```
OPENAI_API_KEY=sk-proj-...          # Your OpenAI API key ← ALREADY SET ✅
NEWSAPI_KEY=                         # For future use
MODEL_NAME=gpt-3.5-turbo           # OpenAI model to use
USE_OPENAI=true                    # Enable OpenAI
NUM_ARTICLES=1000                  # Number to fetch
```

---

## Python Packages Used

| Package | Purpose |
|---------|---------|
| Flask | Web framework for backend |
| flask-cors | Allow frontend-backend communication |
| pandas | Data handling (CSV, DataFrames) |
| scikit-learn | Machine learning (TF-IDF, classifier) |
| joblib | Save/load trained models |
| requests | Make HTTP requests to APIs |
| python-dotenv | Load .env files |
| openai | OpenAI API client |

---

## Directory Structure After Setup

```
real_fake_news/
├── .env                           ← Your API key (NEVER COMMIT!)
├── .env.example                   ← Template (safe to commit)
├── .gitignore                     ← Prevents committing secrets
├── requirements.txt               ← Install with: pip install -r requirements.txt
├── fetch_news_openai.py           ← Run 1st: python fetch_news_openai.py
├── train_model.py                 ← Run 2nd: python train_model.py
├── app.py                         ← Run 3rd: python app.py
├── fetch_news_data.py             ← Alternative (optional)
├── train_model_api.py             ← Alternative (optional)
│
├── news_from_openai.csv           ← Created by fetch_news_openai.py
├── news.csv                       ← Original (reference)
│
├── model/                         ← Created by train_model.py
│   ├── model.joblib               ← Trained ML model
│   └── vectorizer.joblib          ← Text transformer
│
├── frontend/
│   ├── index.html                 ← Web page
│   ├── script.js                  ← JavaScript
│   └── style.css                  ← Styling
│
├── QUICK_START.md                 ← 👈 You are here - START!
├── STEP_BY_STEP_GUIDE.md          ← Detailed instructions
└── SETUP_GUIDE.md                 ← Reference guide
```

---

## Extending Later

### Add NewsAPI
1. Get key from https://newsapi.org/
2. Add to .env: `NEWSAPI_KEY=your_key`
3. Update `fetch_news_openai.py` to fetch from NewsAPI
4. Re-run training

### Add More Training Data
1. Prepare CSV with columns: `text`, `label`
2. Update `train_model.py` to use your CSV
3. Run: `python train_model.py`

### Add More Features
1. Edit `frontend/index.html` for UI
2. Edit `frontend/script.js` for frontend logic
3. Add endpoints to `app.py` as needed

---

## Security Notes

⚠️ **IMPORTANT:**
- `.env` contains your API key - NEVER commit to git ✅ (.gitignore protects this)
- `.env.example` is safe to share - it's just a template
- Don't share your actual `.env` file
- Regenerate API keys if accidentally exposed
- Keep `requirements.txt` (safe - no secrets)

✅ **You're good to go!** Your .env is already set up with your API key.

---

## Getting Help

If something doesn't work:

1. **Check QUICK_START.md** for the 5-minute setup
2. **Check STEP_BY_STEP_GUIDE.md** for detailed instructions
3. **Check the Troubleshooting section** in either guide
4. **Verify .env exists:** `type .env`
5. **Check requirements installed:** `pip list | findstr flask`
6. **Test API:** See testing section above

---

## Success Indicators

After running all 3 commands, you should have:

✅ Output from `fetch_news_openai.py` showing classified articles
✅ File `news_from_openai.csv` with 10 articles
✅ Output from `train_model.py` showing model accuracy
✅ folder `model/` with 2 .joblib files
✅ Flask server running on `http://localhost:5000`
✅ Web interface loads in browser
✅ Can input text and get predictions

---

**Ready to start? Open QUICK_START.md and follow the 3 commands!**
