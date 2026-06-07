import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import time

# Load environment variables
load_dotenv()

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not found in .env file")
    print("Please run: python setup_api_keys.py")
    exit(1)

try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"ERROR: Failed to initialize OpenAI client: {e}")
    exit(1)

# Sample news articles for demonstration
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

def classify_with_openai(text, title="", retry_count=3):
    """
    Use OpenAI GPT to classify news as REAL or FAKE
    Includes retry logic for API failures
    """
    for attempt in range(retry_count):
        try:
            combined_text = f"Title: {title}\n\nContent: {text}"
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert fact-checker and news analyst. 
                        Analyze the following news article and determine if it's REAL or FAKE news.
                        
                        REAL news has: credible sources, verifiable facts, proper attribution, scientific basis
                        FAKE news has: unverified claims, conspiracy theories, unnamed sources, emotional manipulation, no sources
                        
                        Respond with ONLY the word: REAL or FAKE
                        """
                    },
                    {
                        "role": "user",
                        "content": combined_text
                    }
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            classification = response.choices[0].message.content.strip().upper()
            
            # Ensure response is either REAL or FAKE
            if "REAL" in classification:
                return "REAL"
            elif "FAKE" in classification:
                return "FAKE"
            else:
                return "REAL"  # Default to REAL if unclear
                
        except Exception as e:
            if attempt < retry_count - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"  Error (attempt {attempt + 1}/{retry_count}): {str(e)[:50]}... Retrying in {wait_time}s")
                time.sleep(wait_time)
            else:
                print(f"  Error after {retry_count} attempts: {e}")
                return "REAL"  # Default fallback
    
    return "REAL"

def fetch_and_classify_news():
    """
    Fetch sample news articles and classify them using OpenAI
    """
    print("\n" + "="*60)
    print("📰 Fetching and Classifying News with OpenAI")
    print("="*60 + "\n")
    
    classified_articles = []
    successful = 0
    failed = 0
    
    for i, article in enumerate(SAMPLE_NEWS, 1):
        try:
            print(f"[{i}/{len(SAMPLE_NEWS)}] {article['title'][:40]}...", end=" ")
            
            # Classify using OpenAI
            label = classify_with_openai(article['text'], article['title'])
            
            classified_articles.append({
                'title': article['title'],
                'text': article['text'],
                'label': label,
                'source': article['source']
            })
            
            print(f"✓ {label}")
            successful += 1
            
        except Exception as e:
            print(f"✗ Error: {str(e)[:30]}")
            failed += 1
    
    # Create DataFrame
    df = pd.DataFrame(classified_articles)
    
    # Save to CSV
    df.to_csv('news_from_openai.csv', index=False)
    
    print(f"\n{'='*60}")
    print(f"✓ Classification Complete")
    print(f"  Successfully classified: {successful}/{len(SAMPLE_NEWS)}")
    print(f"  Failed: {failed}")
    print(f"✓ Saved to: news_from_openai.csv")
    print(f"{'='*60}\n")
    
    print("Label distribution:")
    print(df['label'].value_counts())
    print("\nNext steps:")
    print("  1. python train_model_enhanced.py")
    print("  2. python app.py")
    
    return df

if __name__ == "__main__":
    print("="*60)
    print("🚀 News Classification with OpenAI GPT")
    print("="*60)
    
    try:
        df = fetch_and_classify_news()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Check if .env file exists with OPENAI_API_KEY")
        print("2. Verify your API key is valid and active")
        print("3. Check you have sufficient API credits")
        print("4. Run: python setup_api_keys.py")
        exit(1)
