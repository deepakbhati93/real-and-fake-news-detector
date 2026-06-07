"""
Multi-API News Fetcher and Classifier
Supports: OpenAI, HuggingFace, Cohere, Google PaLM
"""

import os
import json
import pandas as pd
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# ==================== API CLIENTS ====================

class OpenAIClassifier:
    """Classify news using OpenAI GPT"""
    def __init__(self):
        from openai import OpenAI
        key = os.getenv('OPENAI_API_KEY')
        if not key:
            raise ValueError("OPENAI_API_KEY not found in .env")
        self.client = OpenAI(api_key=key)
        self.model = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
    
    def classify(self, text, title=""):
        """Classify text as REAL or FAKE"""
        try:
            combined_text = f"Title: {title}\n\nContent: {text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert fact-checker. Analyze this news and respond with ONLY one word: REAL or FAKE.
                        
REAL news has: credible sources, verifiable facts, proper attribution, scientific basis
FAKE news has: unverified claims, conspiracy theories, unnamed sources, emotional manipulation"""
                    },
                    {"role": "user", "content": combined_text}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            result = response.choices[0].message.content.strip().upper()
            return "REAL" if "REAL" in result else "FAKE"
        except Exception as e:
            print(f"Error with OpenAI: {e}")
            return "REAL"


class HuggingFaceClassifier:
    """Classify news using HuggingFace models"""
    def __init__(self):
        self.token = os.getenv('HUGGINGFACE_API_KEY')
        if not self.token:
            raise ValueError("HUGGINGFACE_API_KEY not found in .env")
        self.model = os.getenv('AI_MODEL', 'distilbert-base-uncased-finetuned-sst-2-english')
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
    
    def classify(self, text, title=""):
        """Classify text using HuggingFace API"""
        try:
            combined_text = f"Title: {title} Content: {text}"
            
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                self.api_url,
                headers=headers,
                json={"inputs": combined_text[:512]}
            )
            
            if response.status_code == 200:
                result = response.json()
                # Result format: [[{"label": "POSITIVE/NEGATIVE", "score": x}]]
                if result and result[0]:
                    label = result[0][0].get("label", "POSITIVE")
                    return "REAL" if label == "POSITIVE" else "FAKE"
            
            return "REAL"
        except Exception as e:
            print(f"Error with HuggingFace: {e}")
            return "REAL"


class CohereClassifier:
    """Classify news using Cohere API"""
    def __init__(self):
        try:
            import cohere
            key = os.getenv('COHERE_API_KEY')
            if not key:
                raise ValueError("COHERE_API_KEY not found in .env")
            self.client = cohere.Client(key)
        except ImportError:
            raise ImportError("cohere package not installed. Run: pip install cohere")
    
    def classify(self, text, title=""):
        """Classify text using Cohere"""
        try:
            combined_text = f"Title: {title} Content: {text[:500]}"
            
            # Use Cohere's classify endpoint
            response = self.client.classify(
                model="embed-english-v3.0",
                inputs=[combined_text],
                examples=[
                    ("Breaking: Scientists announce breakthrough in renewable energy after years of research", "REAL"),
                    ("Secret government conspiracy keeps aliens hidden from public", "FAKE"),
                    ("Stock market rebounds following positive earnings reports", "REAL"),
                    ("Miracle cure discovered that doctors don't want you to know", "FAKE"),
                ]
            )
            
            if response and response.classifications:
                prediction = response.classifications[0].prediction
                return "REAL" if prediction == "REAL" else "FAKE"
            
            return "REAL"
        except Exception as e:
            print(f"  Error with Cohere: {str(e)[:50]}")
            return "REAL"


class GoogleClassifier:
    """Classify news using Google Gemini API"""
    def __init__(self):
        try:
            import google.generativeai as genai
            key = os.getenv('GOOGLE_API_KEY')
            if not key:
                raise ValueError("GOOGLE_API_KEY not found in .env")
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
    
    def classify(self, text, title=""):
        """Classify text using Google Gemini"""
        try:
            prompt = f"""You are a fact-checker. Analyze this news and respond with ONLY one word.

Title: {title}
Content: {text[:500]}

Respond with ONLY: REAL or FAKE"""
            
            response = self.model.generate_content(prompt, timeout=10)
            result = response.text.strip().upper()
            
            if "REAL" in result:
                return "REAL"
            elif "FAKE" in result:
                return "FAKE"
            else:
                return "REAL"
        except Exception as e:
            print(f"  Error with Google: {str(e)[:50]}")
            return "REAL"


# ==================== CLASSIFIER FACTORY ====================

def get_classifier():
    """Get classifier based on configured AI service"""
    service = os.getenv('AI_SERVICE', 'openai').lower()
    
    classifiers = {
        'openai': OpenAIClassifier,
        'huggingface': HuggingFaceClassifier,
        'cohere': CohereClassifier,
        'google': GoogleClassifier,
    }
    
    if service not in classifiers:
        print(f"Unknown service: {service}. Using OpenAI by default.")
        service = 'openai'
    
    return classifiers[service]()


# ==================== DATA SOURCES ====================

SAMPLE_NEWS = [
    # Real news examples
    {
        "title": "Scientists Discover New Species of Deep-Sea Fish",
        "text": "Researchers from the Marine Biology Institute announced today the discovery of a previously unknown species of bioluminescent fish at a depth of 2000 meters. The discovery was made during a collaborative expedition sponsored by the National Science Foundation.",
        "source": "Science Daily"
    },
    {
        "title": "Global Stock Markets Rise On Positive Economic Data",
        "text": "Major stock indices around the world rallied today following the release of better-than-expected quarterly earnings reports from leading technology companies. The S&P 500 index rose 2.3% in today's trading session.",
        "source": "Financial Times"
    },
    {
        "title": "Environmental Groups Celebrate New Conservation Policy",
        "text": "The World Wildlife Fund and other environmental organizations praised today's announcement of new protections for endangered species habitat. The policy was developed in consultation with scientific experts and indigenous communities.",
        "source": "Reuters"
    },
    {
        "title": "Tech Company Launches New Battery Technology",
        "text": "A leading technology company unveiled a new solid-state battery technology that promises to double the energy density of current lithium-ion batteries. The breakthrough was achieved after five years of research and development.",
        "source": "Tech News"
    },
    {
        "title": "University Researchers Publish Peer-Reviewed Study",
        "text": "Researchers at a major university published findings in a peer-reviewed journal showing positive results from a new medical treatment. The study involved 500 participants over a two-year period.",
        "source": "Medical Journal"
    },
    # Fake news examples
    {
        "title": "Secret Government Program Controls Weather Using Technology",
        "text": "Anonymous sources claim the government has been secretly controlling weather using advanced technology hidden from the public. The program allegedly costs billions of dollars and is controlled by an elite group.",
        "source": "Conspiracy Blog"
    },
    {
        "title": "Celebrity Announces Shocking Secret That Will Change Everything",
        "text": "In an exclusive interview, a famous celebrity revealed information that will supposedly shake the foundations of modern society. The celebrity refused to provide specific details but promised more revelations soon.",
        "source": "Celebrity Gossip"
    },
    {
        "title": "Miracle Cure Discovered That Doctors Don't Want You To Know",
        "text": "A natural health blogger claims to have found a simple cure for a common disease that major pharmaceutical companies are allegedly suppressing. No scientific evidence or studies are provided to support the claims.",
        "source": "Alternative Health"
    },
    {
        "title": "Politician Caught In Unverified Scandal",
        "text": "According to unnamed sources, a politician allegedly engaged in unethical behavior. The claims have not been verified by any credible news sources and lack supporting documentation.",
        "source": "Tabloid Website"
    },
    {
        "title": "Mysterious Object Spotted In Sky Raises UFO Questions",
        "text": "Residents report seeing unusual lights in the sky with no explanation. While officials suggest it was likely a weather balloon or satellite, a UFO enthusiast claims it proves alien visitation.",
        "source": "UFO Forums"
    }
]


def fetch_newsapi():
    """Fetch real news from NewsAPI"""
    key = os.getenv('NEWSAPI_API_KEY')
    if not key:
        print("NewsAPI key not configured. Skipping NewsAPI fetch.")
        return []
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&language=en&apiKey={key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = []
            for article in data.get('articles', [])[:5]:  # Limit to 5 for API cost
                articles.append({
                    'title': article.get('title', ''),
                    'text': article.get('description', '') or article.get('content', ''),
                    'source': article.get('source', {}).get('name', 'NewsAPI')
                })
            print(f"✓ Fetched {len(articles)} articles from NewsAPI")
            return articles
    except Exception as e:
        print(f"Error fetching from NewsAPI: {e}")
    
    return []


def fetch_all_news():
    """Fetch news from all available sources"""
    all_articles = SAMPLE_NEWS.copy()
    
    # Try to fetch from external APIs
    newsapi_articles = fetch_newsapi()
    all_articles.extend(newsapi_articles)
    
    return all_articles


def classify_news_batch(articles, classifier):
    """Classify a batch of news articles"""
    classified = []
    
    for i, article in enumerate(articles, 1):
        print(f"Processing article {i}/{len(articles)}: {article['title'][:50]}...")
        
        label = classifier.classify(
            article.get('text', ''),
            article.get('title', '')
        )
        
        classified.append({
            'title': article.get('title', ''),
            'text': article.get('text', ''),
            'label': label,
            'source': article.get('source', 'Unknown')
        })
        
        print(f"  → Classification: {label}\n")
    
    return classified


def main():
    """Main function"""
    print("\n" + "="*60)
    print("🚀 Multi-API News Fetcher & Classifier")
    print("="*60 + "\n")
    
    # Get classifier
    service = os.getenv('AI_SERVICE', 'openai')
    print(f"📌 Using AI Service: {service.upper()}\n")
    
    try:
        classifier = get_classifier()
        print(f"✓ {service.upper()} classifier initialized\n")
    except Exception as e:
        print(f"❌ Error initializing classifier: {e}")
        print("\nTroubleshooting:")
        print("  1. Run: python setup_api_keys.py")
        print(f"  2. Check .env has the correct API key for {service.upper()}")
        print("  3. Verify API key is valid and has sufficient credits")
        print(f"  4. Run: pip install -r requirements.txt")
        exit(1)
    
    # Fetch news
    print("📰 Fetching articles...")
    try:
        articles = fetch_all_news()
        if not articles:
            print("❌ No articles fetched!")
            exit(1)
        print(f"✓ Fetched {len(articles)} articles\n")
    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
        exit(1)
    
    # Classify
    print(f"🔍 Classifying with {service.upper()}...\n")
    try:
        classified = classify_news_batch(articles, classifier)
        if not classified:
            print("❌ No articles classified!")
            exit(1)
    except Exception as e:
        print(f"❌ Error classifying articles: {e}")
        exit(1)
    
    # Save to CSV
    try:
        df = pd.DataFrame(classified)
        output_file = f'news_from_{service}.csv'
        df.to_csv(output_file, index=False)
        
        print("="*60)
        print(f"✅ SUCCESS!")
        print(f"  • Classified {len(df)} articles using {service.upper()}")
        print(f"  • Saved to: {output_file}")
        print("="*60 + "\n")
        
        # Print summary
        print("📊 Summary:")
        print(df['label'].value_counts().to_string())
        print(f"\nNext steps:")
        print(f"  1. python train_model_enhanced.py")
        print(f"  2. python app.py")
        print()
        
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
