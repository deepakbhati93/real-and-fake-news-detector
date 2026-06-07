# 🚀 COMPLETE SETUP & TRAINING GUIDE

## ⚠️ Issue: Invalid API Key

Your current API key in `.env` appears to be expired or invalid.

## ✅ Solution: Update Your API Key

### **Method 1: Quick Update (Recommended)**

1. **Get a NEW API Key:**
   - Open: https://platform.openai.com/api-keys
   - Sign in (or create free account)
   - Click "Create new secret key"
   - Copy the key

2. **Update .env file:**
   - Open: `.env` file in your project
   - Find: `OPENAI_API_KEY=sk-proj-...`
   - Replace with your NEW key:
     ```
     OPENAI_API_KEY=sk-proj-YOUR_NEW_KEY_HERE
     ```
   - Save the file

3. **IMPORTANT:** PowerShell users use semicolon (`;`) not ampersand (`&&`)

---

## 🎯 Run Complete Training

### **Step 1: For PowerShell Users**
```powershell
cd 'C:\Users\DELL\Desktop\Learning Platform\real_fake_news'
.\train_complete.ps1
```

### **Step 2: For CMD Users**
```cmd
cd "C:\Users\DELL\Desktop\Learning Platform\real_fake_news"
train_complete.bat
```

### **Step 3: Or Run Manually One by One**
```
python fetch_news_openai.py
python train_model_enhanced.py
```

---

## 📋 What Each Step Does

**Step 1: Fetch Data**
- Collects 10 news articles
- Classifies with OpenAI GPT
- Creates: `news_from_openai.csv`

**Step 2: Train Model** 
- Vectorizes text (5000 TF-IDF features)
- Trains Logistic Regression
- Creates: `./model/model.joblib` and `./model/vectorizer.joblib`
- Shows: Training & Testing Accuracy

---

## 🎓 After Training

```bash
python app.py
```

Then open: `http://127.0.0.1:5000`

---

## ✅ Troubleshooting

**Error: "Incorrect API key"**
- Get new key from: https://platform.openai.com/api-keys
- Update `.env` file
- Try again

**Error: "ModuleNotFoundError"**
- Run: `pip install openai python-dotenv flask flask-cors scikit-learn pandas joblib`

**PowerShell syntax error:**
- Use: `semicolon (;)` not `&&`
- Example: `python script1.py ; python script2.py`

---

## 🆘 Need Help?

1. Update `.env` with valid API key
2. Run: `python fetch_news_openai.py`
3. Check output for errors
4. Share error messages for help

---

**Next: Update your API key in `.env` and run `.\train_complete.ps1` or `train_complete.bat`**
