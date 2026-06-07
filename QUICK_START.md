# 🚀 QUICK START - Run Your Project Now!

## Your OpenAI API Key is Already Set ✅

Your `.env` file contains:
```
OPENAI_API_KEY=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
```

---

## 5-Minute Setup

### **Step 1: Open PowerShell**
```
Windows Key + X → Select Windows PowerShell
```

### **Step 2: Navigate to project**
```powershell
cd "C:\Users\DELL\Desktop\Learning Platform\real_fake_news"
```

### **Step 3: Install dependencies (1 minute)**
```powershell
pip install -r requirements.txt
```

Wait for it to complete. You'll see: `Successfully installed...`

---

## Run These 3 Commands (In Order)

### **Command 1: Fetch & Classify News with OpenAI** (1-2 minutes)
```powershell
python fetch_news_openai.py
```

**What happens:**
- Downloads and analyzes 10 sample news articles
- Uses your OpenAI API key to classify each article as REAL or FAKE
- Creates a file: `news_from_openai.csv`

**You'll see:**
```
Processing article 1/10: Scientists Discover New Species...
  → Classification: REAL

Processing article 2/10: Global Stock Markets Rise...
  → Classification: REAL

...

✓ Classified 10 articles using OpenAI
✓ Saved to: news_from_openai.csv
```

---

### **Command 2: Train the Model** (30 seconds)
```powershell
python train_model.py
```

**What happens:**
- Reads the classified articles
- Creates a fast, local machine learning model
- Saves it to `./model/` folder

**You'll see:**
```
✓ Using OpenAI-classified data: news_from_openai.csv
Loading dataset...
Training Passive Aggressive Classifier...

============================================================
MODEL ACCURACY: 100.0%
============================================================

✓ Model saved to: ./model/model.joblib
```

---

### **Command 3: Start Flask Server** (10 seconds)
```powershell
python app.py
```

**You'll see:**
```
✓ Model and vectorizer loaded successfully.
 * Running on http://127.0.0.1:5000
```

**⚠️ KEEP THIS WINDOW OPEN!** The server needs to keep running.

---

## Step 4: Open Your Website

Open your browser and go to:
```
http://localhost:5000
```

You should see the **TruthLens** website!

Type or paste any news text and click **"Analyze Truth Score"**

---

## Example Test

Try pasting this:
```
Scientists at MIT discovered a new renewable energy source that could solve the global energy crisis. 
The research was published in a peer-reviewed journal and funded by the National Science Foundation.
```

**Expected Result:** ✅ Likely REAL News

---

Or try this:
```
Secret government technology can control the weather using mind control satellites. 
Anonymous sources reveal this has been hidden from the public for decades.
```

**Expected Result:** ⚠️ Possibly FAKE News

---

## ⚠️ If Something Goes Wrong

### Error: "ModuleNotFoundError: No module named 'openai'"
```powershell
pip install openai
```

### Error: "Model files not found"
Make sure you ran both commands first:
```powershell
python fetch_news_openai.py
python train_model.py
```

### Error: "Port 5000 already in use"
Stop other Flask servers or use a different port. In another PowerShell:
```powershell
netstat -ano | findstr :5000
```

### Error about API key
Check your `.env` file has the OpenAI key:
```powershell
type .env
```

---

## 📊 What's Happening Behind The Scenes

1. **fetch_news_openai.py**
   - Uses OpenAI to understand if articles are real or fake
   - Saves classified data to CSV

2. **train_model.py**
   - Trains a local ML model on the classified data
   - Creates .joblib files (the trained model)

3. **app.py**
   - Runs Flask web server
   - Uses the trained model to analyze new articles SUPER FAST
   - No API calls needed for predictions!

4. **frontend/** (Web interface)
   - Beautiful website at `http://localhost:5000`
   - Send text to Flask backend
   - Get instant predictions

---

## 🎯 That's It!

You now have a **fully working Fake News Detector** that:
- ✅ Uses OpenAI to classify training data
- ✅ Trains a fast local ML model
- ✅ Provides instant predictions
- ✅ Has a beautiful web interface

---

## 🔄 To Add Another API Later

1. Get an API key from the new service
2. Add it to `.env`:
   ```
   NEWSAPI_KEY=your_key_here
   ```
3. Update `fetch_news_openai.py` to fetch from that API
4. Run: `python fetch_news_openai.py`
5. Run: `python train_model.py`
6. Done! Your model is updated

---

## 📝 File Checklist

After running all commands, you should have:

```
✅ .env                      (has your API key)
✅ requirements.txt          (packages list)
✅ fetch_news_openai.py      (fetches data)
✅ train_model.py            (trains model)
✅ app.py                    (Flask server)
✅ frontend/                 (web interface)
✅ news_from_openai.csv      (created by fetch_news_openai.py)
✅ model/                    (created by train_model.py)
   ✅ model.joblib
   ✅ vectorizer.joblib
```

---

**You're all set! Follow the 3 commands above and you're done! 🎉**
