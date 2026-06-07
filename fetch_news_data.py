import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
NUM_ARTICLES = int(os.getenv('NUM_ARTICLES', 1000))

def fetch_from_newsapi(num_articles=1000):
    """
    Fetch news articles from NewsAPI.org
    Requires free API key from https://newsapi.org/
    """
    if not NEWSAPI_KEY:
        raise ValueError("NEWSAPI_KEY not found in .env file")
    
    articles = []
    base_url = "https://newsapi.org/v2/everything"
    
    # Fetch trusted sources (typically real news)
    trusted_sources = ['bbc-news', 'cnn', 'reuters', 'the-new-york-times', 'the-guardian-uk']
    problematic_sources = ['breitbart-news', 'info-wars', 'the-daily-stormer']
    
    print("Fetching real news from trusted sources...")
    for source in trusted_sources:
        params = {
            'sources': source,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 100,
            'apiKey': NEWSAPI_KEY
        }
        try:
            response = requests.get(base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for article in data.get('articles', []):
                    articles.append({
                        'text': article.get('title', '') + ' ' + article.get('description', ''),
                        'label': 'REAL',
                        'source': source,
                        'url': article.get('url', '')
                    })
                    if len(articles) >= num_articles // 2:
                        break
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
            continue
    
    print(f"Fetched {len(articles)} real news articles")
    
    # NOTE: For a production system, you should:
    # 1. Use fact-checking APIs (ClaimBuster, Google Fact Check API)
    # 2. Label articles based on fact-checking results
    # 3. Or use existing fake news datasets
    
    print("Note: For FAKE news, you need to:")
    print("- Use fact-checking APIs (Google Fact Check, ClaimBuster)")
    print("- Or use existing labeled datasets (FEVER, FakeNewsNet)")
    
    df = pd.DataFrame(articles)
    return df

def fetch_alternative_method():
    """
    Alternative: Use existing labeled dataset from Kaggle or similar
    For production, consider: https://github.com/several27/FakeNewsCorpus
    """
    print("\nAlternative approach:")
    print("1. Download labeled dataset from Kaggle (Fake News Detection)")
    print("2. Or use: https://raw.githubusercontent.com/several27/FakeNewsCorpus/master/news_sample.csv")
    return None

if __name__ == "__main__":
    if NEWSAPI_KEY:
        print("Fetching news data from APIs...")
        df = fetch_from_newsapi(NUM_ARTICLES)
        
        # Save to CSV for training
        df.to_csv('news_from_api.csv', index=False)
        print(f"\nSaved {len(df)} articles to news_from_api.csv")
        print("\nDataset structure:")
        print(df.head())
    else:
        print("ERROR: NEWSAPI_KEY not set in .env file")
        print("\nSetup instructions:")
        print("1. Visit https://newsapi.org/ and sign up for free API")
        print("2. Copy your API key")
        print("3. Create .env file and add: NEWSAPI_KEY=your_key_here")
        fetch_alternative_method()
