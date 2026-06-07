# 🔐 API Configuration Guide

Complete guide for setting up external AI APIs for the Real vs Fake News Detector.

---

## 📋 Quick Setup (2 minutes)

```bash
# 1. Run the interactive setup
python setup_api_keys.py

# 2. Install new dependencies
pip install -r requirements.txt

# 3. Test with your chosen AI service
python fetch_news_multi.py

# 4. Train the model
python train_model.py

# 5. Start the app
python app.py
```

---

## 🤖 AI Service Options

### 1️⃣ OpenAI (Recommended)
**Best for:** Accuracy, speed, reliability

**Setup:**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-proj-`)
4. Run: `python setup_api_keys.py`
5. Paste key when prompted

**Cost:**
- `gpt-3.5-turbo`: ~$0.0005 per 1K tokens (⚡ Fast & Cheap)
- `gpt-4`: ~$0.03 per 1K tokens (🧠 Most Accurate)
- Free trial: $5 credit

**Configure:**
```bash
# In .env file:
AI_SERVICE=openai
AI_MODEL=gpt-3.5-turbo
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

**Advantages:**
- ✅ Most accurate
- ✅ Fastest response time
- ✅ Best documentation
- ✅ Works out of the box

---

### 2️⃣ HuggingFace (Free Alternative)
**Best for:** Free usage, learning, experimenting

**Setup:**
1. Go to https://huggingface.co/settings/tokens
2. Create a new token (read-only is fine)
3. Copy the token (starts with `hf_`)
4. Run: `python setup_api_keys.py`
5. Paste when prompted

**Cost:** FREE (with rate limits)

**Configure:**
```bash
# In .env file:
AI_SERVICE=huggingface
HUGGINGFACE_API_KEY=hf_YOUR_TOKEN_HERE
```

**Advantages:**
- ✅ Completely free
- ✅ No credit card required
- ✅ 30,000 calls/month free tier
- ✅ Multiple model options

**Rate Limits:**
- Free tier: 30,000 API calls/month
- Minimum delay: ~1 second between requests

---

### 3️⃣ Cohere API (Good Balance)
**Best for:** Text classification, good accuracy at low cost

**Setup:**
1. Go to https://dashboard.cohere.ai/api-keys
2. Sign up (free account)
3. Copy API key from dashboard
4. Run: `python setup_api_keys.py`
5. Paste when prompted

**Cost:**
- Free tier: 100 API calls/month
- Paid: $0.10 per 1M tokens

**Configure:**
```bash
# In .env file:
AI_SERVICE=cohere
COHERE_API_KEY=YOUR_KEY_HERE
```

**Advantages:**
- ✅ Specialized in classification
- ✅ Good free tier
- ✅ Fair pricing for production use
- ✅ Good documentation

---

### 4️⃣ Google PaLM/Gemini (Free Alternative)
**Best for:** Free, experimental use

**Setup:**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API key"
3. Copy the key
4. Run: `python setup_api_keys.py`
5. Paste when prompted

**Cost:** FREE (limited requests)

**Configure:**
```bash
# In .env file:
AI_SERVICE=google
GOOGLE_API_KEY=YOUR_KEY_HERE
```

**Advantages:**
- ✅ Completely free
- ✅ Good for experimentation
- ✅ Powered by Google's Gemini
- ✅ No credit card required

**Limitations:**
- Limited to ~60 requests/minute
- Beta quality

---

## 📰 Data Source APIs (Optional)

### NewsAPI
**Real news from 40,000+ sources**

1. Go to https://newsapi.org/
2. Sign up (free tier available)
3. Copy API key
4. In .env: `NEWSAPI_API_KEY=YOUR_KEY_HERE`

**Benefits:**
- Real-time news data
- Multiple countries/languages
- Free tier: 500 requests/day
- Augments sample data with real articles

---

### Guardian Open Platform
**UK news articles (free)**

1. Go to https://open-platform.theguardian.com/
2. Register for API key
3. In .env: `GUARDIAN_API_KEY=YOUR_KEY_HERE`

**Benefits:**
- Completely free
- High-quality UK news
- No rate limits for development

---

## 🔧 Configuration Files

### .env File Structure
```
# AI Service
AI_SERVICE=openai              # Which AI to use
AI_MODEL=gpt-3.5-turbo        # Which model variant
OPENAI_API_KEY=sk-proj-...    # Your API key

# Data Sources (optional)
NEWSAPI_API_KEY=...
GUARDIAN_API_KEY=...

# Settings
ARTICLES_TO_FETCH=100
```

### Load in Your Code
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Access your configuration
service = os.getenv('AI_SERVICE')
api_key = os.getenv('OPENAI_API_KEY')
model = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
```

---

## 🚀 Usage Examples

### Using in Code

**OpenAI:**
```python
from fetch_news_multi import get_classifier

classifier = get_classifier()  # Auto-loads from .env
label = classifier.classify("News text here", "Title here")
print(label)  # REAL or FAKE
```

**Run Full Pipeline:**
```bash
# Fetch & classify with your AI service
python fetch_news_multi.py

# Train model
python train_model.py

# Start Flask app
python app.py
```

---

## 💰 Cost Comparison

| Service | Free Cost | Production | Speed | Accuracy |
|---------|-----------|-----------|-------|----------|
| **OpenAI** | $5 trial | $0.0005/1K tokens | ⚡🚀 | 🧠🧠🧠 |
| **HuggingFace** | 30K/month | Paid | ⚡ | 🧠🧠 |
| **Cohere** | 100/month | $0.10/M tokens | ⚡ | 🧠🧠 |
| **Google** | Unlimited | Coming soon | ⚡ | 🧠 |

---

## 🆘 Troubleshooting

### "API key not found"
```bash
# Check your .env file exists
ls -la .env

# Verify key is set
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### "Invalid API key"
- Check key isn't expired or revoked
- Make sure it's copied correctly (no extra spaces)
- Try regenerating a new key on your API dashboard

### "Rate limit exceeded"
- Wait between requests (add delay)
- Use a paid tier with higher limits
- Use HuggingFace free tier with proper delays

### Module import errors
```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade

# For specific service:
pip install openai cohere google-generativeai
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# 1. Check .env file exists
[ -f .env ] && echo "✓ .env found"

# 2. Verify API key is set
python setup_api_keys.py  # Re-run to verify

# 3. Test classifier
python -c "from fetch_news_multi import get_classifier; c = get_classifier(); print(c.classify('Test'))"

# 4. Run full fetch
python fetch_news_multi.py

# 5. Train model
python train_model.py

# 6. Start app
python app.py  # Should run on port 5000
```

---

## 🔐 Security Best Practices

✅ **DO:**
- Keep API keys in `.env` file
- Add `.env` to `.gitignore`
- Rotate/regenerate keys periodically
- Use read-only tokens when possible
- Monitor API usage on dashboards

❌ **DON'T:**
- Commit `.env` to version control
- Share API keys in chat/email
- Hardcode keys in source code
- Use keys in client-side JavaScript
- Post keys in public forums

**Check if key leaked:**
```bash
git log --all --full-history -- ".env"
```

---

## 📚 Additional Resources

- [OpenAI Documentation](https://platform.openai.com/docs)
- [HuggingFace Inference API](https://huggingface.co/inference-api)
- [Cohere Documentation](https://docs.cohere.io/)
- [Google Gemini API](https://ai.google.dev/)
- [NewsAPI Docs](https://newsapi.org/docs)

---

## 🆘 Support

If you encounter issues:

1. Check the API service status
2. Verify your API key validity
3. Check your account balance/quota
4. Review rate limits for your tier
5. Check `.env` file permissions

**Still stuck?** Check `SOLUTION_SUMMARY.md` for architecture details.
