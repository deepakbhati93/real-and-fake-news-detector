# 🏗️ Architecture Overview - Multi-AI Integration

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ENTRY POINTS                         │
├────────┬──────────────┬──────────────┬──────────────────────┤
│ FastAPI│ Web Browser │ Command Line │ Python Scripts       │
└────────┴──────────────┴──────────────┴──────────────────────┘
         │                              │
         └──────────────┬───────────────┘
                        │
         ┌──────────────▼───────────────┐
         │   app.py (Flask Backend)    │
         │  Loads model + vectorizer   │
         │  Serves predictions         │
         └──────────────┬───────────────┘
                        │
         ┌──────────────▼───────────────────────────┐
         │    model/ directory                      │
         │  • model.joblib (Trained classifier)    │
         │  • vectorizer.joblib (Text transformer) │
         └──────────────▲───────────────────────────┘
                        │
         ┌──────────────┴────────────────────────────┐
         │  Training Phase (train_model_enhanced.py) │
         │  • Loads CSV from any AI service         │
         │  • TF-IDF vectorization                  │
         │  • Logistic Regression training         │
         └──────────────▲────────────────────────────┘
                        │
    ┌───────────────────┴──────────────────────┐
    │  Data Phase (fetch_news_multi.py)        │
    │  INPUT: Select AI Service via .env       │
    │  PROCESS: Fetch news + Classify          │
    │  OUTPUT: CSV with REAL/FAKE labels       │
    └───────────────────▲──────────────────────┘
                        │
    ┌───────────────────┴──────────────────────────────────────┐
    │              AI SERVICE SELECTION                         │
    ├──────────────┬────────────────┬─────────┬──────────────┤
    │   OpenAI     │  HuggingFace   │ Cohere  │ Google/Gemini│
    │ (Premium)    │   (Free)       │(Balanced) │ (Free)    │
    ├──────────────┼────────────────┼─────────┼──────────────┤
    │ SK-PROJ-...  │  HF_TOKEN...   │ COHERE..│ GOOGLE_API.. │
    │ gpt-3.5-turbo│ distilbert...  │ classify│ gemini-pro   │
    │ Fast & Good  │ Slow but Free  │ Balanced│ Fast & Free  │
    └──────────────┴────────────────┴─────────┴──────────────┘
                        │
    ┌───────────────────┴──────────────────────┐
    │    Configuration: .env file              │
    │  • AI_SERVICE = openai                   │
    │  • OPENAI_API_KEY = sk-proj-xxxxx       │
    │  • AI_MODEL = gpt-3.5-turbo             │
    └──────────────────────────────────────────┘
                        │
    ┌───────────────────┴──────────────────────┐
    │    Setup Phase (setup_api_keys.py)       │
    │  Interactive wizard to:                  │
    │  1. Choose AI service (1-5)             │
    │  2. Input API key(s)                    │
    │  3. Save to .env file                   │
    └──────────────────────────────────────────┘
```

---

## Data Flow

```
START
  │
  ├─→ Run: python setup_api_keys.py
  │   └─→ Creates .env file with API keys
  │
  ├─→ Run: pip install -r requirements.txt
  │   └─→ Installs OpenAI, Cohere, Google libs
  │
  ├─→ Run: python fetch_news_multi.py
  │   │
  │   ├─→ Read .env (AI_SERVICE setting)
  │   │
  │   ├─→ Select Classifier:
  │   │   ├─ If "openai" → OpenAIClassifier
  │   │   ├─ If "huggingface" → HuggingFaceClassifier
  │   │   ├─ If "cohere" → CohereClassifier
  │   │   └─ If "google" → GoogleClassifier
  │   │
  │   ├─→ Fetch Data:
  │   │   ├─ Load sample articles (10 built-in)
  │   │   └─ Fetch NewsAPI (if configured)
  │   │
  │   ├─→ Classify Each Article:
  │   │   ├─ Send to selected AI service
  │   │   ├─ Get REAL/FAKE classification
  │   │   └─ Store result
  │   │
  │   └─→ Save CSV: news_from_{service}.csv
  │       (e.g., news_from_openai.csv)
  │
  ├─→ Run: python train_model_enhanced.py
  │   │
  │   ├─→ Find Latest CSV File
  │   │   └─→ Auto-detect: news_from_*.csv
  │   │
  │   ├─→ Load & Validate Data
  │   │   ├─ Check 'label' column (REAL/FAKE)
  │   │   └─ Check 'text' column (article content)
  │   │
  │   ├─→ Vectorize Text
  │   │   └─→ TF-IDF: convert text → numbers
  │   │
  │   ├─→ Train Model
  │   │   ├─ 80% training data
  │   │   ├─ 20% test data
  │   │   └─ Logistic Regression algorithm
  │   │
  │   ├─→ Evaluate Accuracy
  │   │   ├─ Training accuracy: X%
  │   │   └─ Testing accuracy: Y%
  │   │
  │   └─→ Save Models:
  │       ├─ model/model.joblib
  │       └─ model/vectorizer.joblib
  │
  ├─→ Run: python app.py
  │   │
  │   ├─→ Load Saved Models
  │   │   ├─ Load model.joblib
  │   │   └─ Load vectorizer.joblib  
  │   │
  │   ├─→ Start Flask Server
  │   │   └─ Listen on port 5000
  │   │
  │   └─→ Ready for Predictions!
  │
  ├─→ User Tests (Browser or API)
  │   │
  │   ├─→ Web: Open http://localhost:5000
  │   │   ├─ Paste news text
  │   │   ├─ Click "Analyze"
  │   │   └─ Get REAL/FAKE prediction
  │   │
  │   └─→ API: curl -X POST /analyze
  │       ├─ Send JSON: {"text": "..."}
  │       └─ Get: {"prediction": "REAL"}
  │
  └─→ SUCCESS! 🎉
```

---

## Configuration Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                    AI SERVICE SELECTION                     │
├────────────┬─────────────┬────────────┬──────────────────┤
│  OpenAI    │ HuggingFace │   Cohere   │    Google        │
├────────────┼─────────────┼────────────┼──────────────────┤
│ Best       │ Free        │ Balanced   │ Free             │
│ Quality    │ No CC       │            │ No CC            │
├────────────┼─────────────┼────────────┼──────────────────┤
│ Setup:     │ Setup:      │ Setup:     │ Setup:           │
│ 1. Get key │ 1. Get      │ 1. Get key │ 1. Get key       │
│ 2. Set     │    token    │ 2. Set     │ 2. Set env       │
│    env     │ 2. Set env  │    env     │ 3. Run scripts   │
│ 3. Run     │ 3. Run      │ 3. Run     │                  │
│    scripts │    scripts  │    scripts │                  │
├────────────┼─────────────┼────────────┼──────────────────┤
│ Cost:      │ Cost:       │ Cost:      │ Cost:            │
│ $0.0005/   │ Free (30K   │ Free (100  │ Free (rate      │
│ 1K tokens  │ /month)     │ /month)    │ limits)          │
│ + trial    │ + paid tier │ + paid     │                  │
├────────────┼─────────────┼────────────┼──────────────────┤
│ Speed:     │ Speed:      │ Speed:     │ Speed:           │
│ ⚡⚡⚡      │ ⚡⚡        │ ⚡⚡⚡      │ ⚡⚡              │
├────────────┼─────────────┼────────────┼──────────────────┤
│ Accuracy:  │ Accuracy:   │ Accuracy:  │ Accuracy:        │
│ 🧠🧠🧠    │ 🧠🧠       │ 🧠🧠      │ 🧠🧠             │
├────────────┼─────────────┼────────────┼──────────────────┤
│ Best For:  │ Best For:   │ Best For:  │ Best For:        │
│ Production │ Testing     │ Balance    │ Experimenting    │
│ Accuracy   │ Free use    │ Cost/      │ Free learning    │
│            │             │ Quality    │                  │
└────────────┴─────────────┴────────────┴──────────────────┘

.env Configuration:
AI_SERVICE=openai           ; Select which service
OPENAI_API_KEY=sk-proj-.... ; Your API key here
AI_MODEL=gpt-3.5-turbo      ; Which model to use
```

---

## File Structure

```
📦 real_fake_news/
├── 📂 model/                    # Trained models (auto-created)
│   ├── model.joblib            # Classifier model
│   └── vectorizer.joblib       # Text vectorizer
│
├── 📂 frontend/                 # Web UI (unchanged)
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── 📜 app.py                    # Flask app (unchanged)
├── 📜 train_model.py            # Original trainer (still works)
├── 📜 fetch_news_openai.py      # Original fetcher (still works)
│
├── ✨ setup_api_keys.py         # 🆕 Interactive setup wizard
├── ✨ fetch_news_multi.py       # 🆕 Multi-AI data fetcher
├── ✨ train_model_enhanced.py   # 🆕 Enhanced trainer
│
├── 📋 .env                      # 🆕 API keys (Git-ignored)
├── 📋 .env.example              # Config template
├── 📋 requirements.txt          # Updated with new APIs
│
├── 📚 GET_STARTED_WITH_APIS.md  # 🆕 Quick overview
├── 📚 QUICK_START_APIS.md       # 🆕 5-minute setup
├── 📚 API_CONFIGURATION_GUIDE.md# 🆕 Detailed reference
├── 📚 API_INTEGRATION_SUMMARY.md# 🆕 What changed
├── 📚 IMPLEMENTATION_CHECKLIST.md # 🆕 Tech details
│
└── 📚 README.md, etc.           # Original docs (still valid)
```

---

## Service Comparison

```
┌─────────────────────────────────────────────────────────────┐
│          QUICK DECISION TREE                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Do you have money?                                          │
│     ┌─────────────┬──────────────┐                          │
│     │             │              │                          │
│   YES            NO          MAYBE                          │
│     │             │              │                          │
│     ▼             ▼              ▼                          │
│  OpenAI      HuggingFace or   Cohere                        │
│  (Best)      Google (Free)    (Balanced)                    │
│              (Good)           (Good)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Setup Paths

```
Path A: I Want Best Results (15 min)
├─ Get OpenAI key (2 min)
├─ Run setup_api_keys.py (1 min)
├─ pip install (1 min)
├─ fetch_news_multi.py (3 min)
├─ train_model_enhanced.py (5 min)
└─ python app.py (READY!)

Path B: I Want Free (15 min)
├─ Get HuggingFace token (2 min)
├─ Run setup_api_keys.py (1 min)
├─ pip install (1 min)
├─ fetch_news_multi.py (3 min)
├─ train_model_enhanced.py (5 min)
└─ python app.py (READY!)

Path C: I Want Both (20 min)
├─ Get OpenAI + HuggingFace keys (5 min)
├─ Run setup_api_keys.py (2 min)
├─ pip install (1 min)
├─ Try OpenAI: fetch + train (8 min)
├─ Try HuggingFace: fetch + train (8 min)
├─ Compare results
└─ Pick your favorite!

Path D: I Want All Four (30 min)
├─ Get all 4 keys (10 min)
├─ Run setup_api_keys.py (2 min)
├─ pip install (1 min)
├─ Try each service (4 min × 4 = 16 min)
└─ Benchmark and choose!
```

---

## Quick Reference

### Most Common Commands

```bash
# Setup (run once)
python setup_api_keys.py

# Fetch & classify (run when API service changes)
python fetch_news_multi.py

# Train model (run after fetch)
python train_model_enhanced.py

# Run app (main interface)
python app.py
```

### Environment Variables

```bash
# Primary: Which AI service to use
AI_SERVICE=openai              # or: huggingface, cohere, google

# API Keys (get from their dashboards)
OPENAI_API_KEY=sk-proj-...
HUGGINGFACE_API_KEY=hf_...
COHERE_API_KEY=...
GOOGLE_API_KEY=...

# Optional: Real news source
NEWSAPI_API_KEY=...
```

---

**That's the complete architecture! You now understand how everything connects! 🎯**
