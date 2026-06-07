# 🚀 Quick Start with External APIs

Get the Real vs Fake News Detector working with **OpenAI, HuggingFace, Cohere, or Google APIs** in 5 minutes.

---

## ⚡ The Quick Path (Choose Your AI Service)

### Option 1: OpenAI (Recommended - Best Quality)
```bash
# 1. Get API key from https://platform.openai.com/api-keys
#    (Copy key starting with sk-proj-)

# 2. Run setup wizard
python setup_api_keys.py
# → Choose option 1 (OpenAI)
# → Paste your key when prompted

# 3. Install updated dependencies
pip install -r requirements.txt

# 4. Fetch and classify news with OpenAI
python fetch_news_multi.py

# 5. Train the model  
python train_model.py

# 6. Start the web app
python app.py
# → Visit http://localhost:5000
```

**That's it!** Your AI model is now trained and ready to detect fake news.

---

### Option 2: HuggingFace (Free Alternative)
```bash
# 1. Get token from https://huggingface.co/settings/tokens
#    (Copy token starting with hf_)

# 2. Run setup
python setup_api_keys.py
# → Choose option 2 (HuggingFace)
# → Paste your token when prompted

# 3. Rest is the same...
pip install -r requirements.txt
python fetch_news_multi.py
python train_model.py
python app.py
```

---

### Option 3: Cohere (Good Balance)
```bash
# 1. Get key from https://dashboard.cohere.ai/api-keys

# 2. Run setup
python setup_api_keys.py
# → Choose option 3 (Cohere)
# → Paste your key when prompted

# 3. Run pipeline
pip install -r requirements.txt
python fetch_news_multi.py
python train_model.py
python app.py
```

---

### Option 4: Google (Free)
```bash
# 1. Get key from https://makersuite.google.com/app/apikey

# 2. Run setup  
python setup_api_keys.py
# → Choose option 4 (Google)
# → Paste your key when prompted

# 3. Run pipeline
pip install -r requirements.txt
python fetch_news_multi.py
python train_model.py
python app.py
```

---

### Option 5: Setup All Services at Once
```bash
# Prepare all API keys (optional - get from links above)

# Run setup wizard
python setup_api_keys.py
# → Choose option 5 (All services)
# → Provide your API keys as prompted

# Install dependencies
pip install -r requirements.txt

# Now you can use any service by editing .env
# Set: AI_SERVICE=openai   (or cohere, huggingface, google)

# Run pipeline
python fetch_news_multi.py  # Uses service from .env
python train_model.py
python app.py
```

---

## 🔍 What Each Step Does

### Step 1: `setup_api_keys.py`
✅ Interactive wizard to add your API keys  
✅ Saves to `.env` file (Git-ignored for security)  
✅ Supports multiple AI services  
✅ Can add multiple keys for fallback support  

**File created:** `.env`

---

### Step 2: `pip install -r requirements.txt`
✅ Installs OpenAI, Cohere, Google libraries  
✅ Installs HuggingFace support  
✅ No conflicts with existing packages  

---

### Step 3: `python fetch_news_multi.py`
✅ Fetches sample news articles  
✅ Fetches real news from NewsAPI (if configured)  
✅ Uses YOUR chosen AI service to classify as REAL/FAKE  
✅ Creates: `news_from_{service}.csv`  

**Output:**
```
Processing article 1/10: Scientists Discover New Species...
  → Classification: REAL

Processing article 2/10: Secret Government Controls Weather...
  → Classification: FAKE

✓ Classified 10 articles using openai
✓ Saved to: news_from_openai.csv
```

---

### Step 4: `python train_model.py`
✅ Reads classified news data  
✅ Trains a Machine Learning model  
✅ Saves trained model to `./model/` directory  

**Creates:**
- `model/model.joblib` - Trained classifier
- `model/vectorizer.joblib` - Text transformer

---

### Step 5: `python app.py`
✅ Starts Flask web server  
✅ Loads your trained model  
✅ Ready for predictions  

**Access:**
- Web UI: http://localhost:5000
- API: http://localhost:5000/analyze

---

## 🧪 Test Your Setup

### Quick Test (30 seconds)
```bash
# Test that classifier loads correctly
python -c "from fetch_news_multi import get_classifier; print('✓ Classifier loaded successfully')"

# Test classification
python -c "
from fetch_news_multi import get_classifier
classifier = get_classifier()
result = classifier.classify('Breaking news from BBC: Scientists discover cure', 'News Title')
print(f'✓ Classification works: {result}')
"
```

### Full Test (3 minutes)
```bash
# Run data fetching
python fetch_news_multi.py

# Train model
python train_model.py

# Start app and test manually
python app.py

# In another terminal:
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Breaking news reported by Reuters about market trends"}'

# Expected response:
# {"prediction": "REAL"}
```

---

## 📊 What You'll Get

After completing the steps:

1. ✅ **API integration** - Real data from multiple possible sources
2. ✅ **AI classification** - Articles labeled REAL/FAKE by AI
3. ✅ **Trained model** - Machine learning model ready for predictions
4. ✅ **Web interface** - Browser-based news analyzer
5. ✅ **REST API** - Backend API for developers

---

## 🔄 Most Common Workflow

```bash
# First time setup
python setup_api_keys.py
pip install -r requirements.txt
python fetch_news_multi.py
python train_model.py
python app.py

# After app is running:
# Edit a news article in your browser
# Click "Analyze"
# Model predicts REAL or FAKE instantly!
```

---

## ⚙️ Advanced: Using Different AI Services

Switch between AI services without re-fetching data:

```bash
# Classification with OpenAI
echo "AI_SERVICE=openai" >> .env
python fetch_news_multi.py  # Creates news_from_openai.csv

# Classification with HuggingFace  
echo "AI_SERVICE=huggingface" >> .env
python fetch_news_multi.py  # Creates news_from_huggingface.csv

# Compare results
python train_model.py
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install -r requirements.txt
```

### ".env: No such file or directory"
```bash
python setup_api_keys.py  # This creates it
```

### "OPENAI_API_KEY not found in .env"
```bash
# Verify key is actually in .env
cat .env

# Run setup again
python setup_api_keys.py
```

### "Invalid API key" error
- Double-check key was copied correctly (no spaces)
- Verify key isn't expired on your API dashboard
- Try generating a new key

---

## 💡 Pro Tips

1. **Save money:** Start with HuggingFace (free) for testing
2. **Better accuracy:** Use OpenAI's `gpt-4` for production
3. **Mixed approach:** Setup all 4 services, compare results
4. **Real data:** Configure NewsAPI to add real news to training set
5. **Monitoring:** Check API usage on your service dashboard

---

## 📚 Next Steps

- 📖 Read [API_CONFIGURATION_GUIDE.md](API_CONFIGURATION_GUIDE.md) for detailed API info
- 🏗️ Read [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) for architecture
- 🐛 Read [VERIFICATION_CHECKLIST.md](VERIFICATION_CHECKLIST.md) for debugging

---

## ✅ Verification

Did everything work? Check:

```bash
# 1. ✓ .env file exists
ls .env

# 2. ✓ Model files created
ls model/model.joblib model/vectorizer.joblib

# 3. ✓ CSV with classified news
ls news_from_*.csv

# 4. ✓ App starts without errors
python app.py
# Should see: "Running on http://127.0.0.1:5000"

# 5. ✓ Can make predictions
# Open browser to http://localhost:5000
# Paste some news text and click "Analyze"
```

---

**All set! You now have a working AI-powered fake news detector! 🎉**
