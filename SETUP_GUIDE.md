# Real vs Fake News Detector - API Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup API Keys

#### Option A: Using NewsAPI (Recommended for beginners)
1. Visit https://newsapi.org/
2. Sign up for free (tier: 100 requests/day)
3. Copy your API key
4. Run the setup script:
   ```bash
   # Copy the example env file
   copy .env.example .env
   ```
5. Edit `.env` file and add your key:
   ```
   NEWSAPI_KEY=your_actual_api_key_here
   ```

#### Option B: Using NewsData.io
1. Visit https://newsdata.io/
2. Sign up for free
3. Copy your API key
4. Edit `.env` file:
   ```
   NEWSDATA_KEY=your_actual_api_key_here
   ```

### 3. Fetch News Data from API
```bash
python fetch_news_data.py
```
This will create `news_from_api.csv` with fetched articles.

### 4. Train the Model
```bash
python train_model_api.py
```
This will:
- Load data from `news_from_api.csv` (or fall back to `news.csv`)
- Train the classifier
- Save model to `./model/model.joblib`

### 5. Run the Application
```bash
python app.py
```
Visit http://localhost:5000 in your browser.

---

## Important Notes

⚠️ **For Production Fake News Detection:**
- NewsAPI alone won't label articles as fake/real
- You need to use:
  1. **Fact-checking APIs**: Google Fact Check API, ClaimBuster
  2. **Pre-labeled datasets**: FakeNewsCorpus, FEVER dataset
  3. **Hybrid approach**: Combine API data with manual labeling

### Recommended Setup for Better Results:
1. Download labeled dataset from Kaggle (Fake News Detection)
2. Use API for real-time news classification with pre-trained model
3. Use fact-checking APIs for verification

---

## API Alternatives

| API | Free Tier | Best For |
|-----|-----------|----------|
| NewsAPI | 100 requests/day | Real news sources |
| NewsData.io | 200 requests/day | News aggregation |
| Google Fact Check | Free | Fact verification |
| Mediabias Check | Free | Source credibility |

---

## File Structure
```
real_fake_news/
├── .env                 (Your API keys - NEVER commit this!)
├── .env.example         (Template for .env)
├── app.py               (Flask backend)
├── fetch_news_data.py   (Fetch news from APIs)
├── train_model_api.py   (Train model with API data)
├── train_model.py       (Original - for reference)
├── news.csv            (Original CSV - for reference)
├── requirements.txt     (Python dependencies)
├── frontend/           (Web interface)
│   ├── index.html
│   ├── script.js
│   └── style.css
└── model/              (Trained models)
    ├── model.joblib
    └── vectorizer.joblib
```

---

## Troubleshooting

**Error: "NEWSAPI_KEY not found in .env file"**
- Make sure you created `.env` (not `.env.example`)
- Add your API key to `.env`

**Error: "No module named 'dotenv'"**
- Run: `pip install python-dotenv`

---

## Next Steps

1. Get an API key and update `.env`
2. Run `python fetch_news_data.py` to fetch data
3. Run `python train_model_api.py` to train
4. Run `python app.py` to start the server
