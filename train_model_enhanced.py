"""
Enhanced Model Training Script
Works with multiple data sources (OpenAI, HuggingFace, Cohere, etc.)
"""

import os
import glob
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path

def find_latest_news_csv():
    """Find the latest news CSV file from any AI service"""
    pattern = "news_from_*.csv"
    files = glob.glob(pattern)
    
    if not files:
        # Try to find the old news.csv
        if os.path.exists("news.csv"):
            return "news.csv"
        raise FileNotFoundError(
            f"No CSV files found matching pattern '{pattern}'\n"
            "Please run: python fetch_news_multi.py"
        )
    
    # Get most recently modified file
    latest = max(files, key=os.path.getmtime)
    return latest


def train_model():
    """Train a fake news detection model"""
    print("\n" + "="*60)
    print("🤖 Training Fake News Detection Model")
    print("="*60 + "\n")
    
    # Find data file
    csv_file = find_latest_news_csv()
    print(f"📊 Loading data from: {csv_file}\n")
    
    # Load data
    df = pd.read_csv(csv_file)
    
    print(f"✓ Loaded {len(df)} articles")
    print(f"✓ Label distribution:\n{df['label'].value_counts()}\n")
    
    # Validate data
    if len(df) == 0:
        print("❌ No data found in CSV!")
        exit(1)
    
    if 'label' not in df.columns or 'text' not in df.columns:
        print("❌ CSV must have 'label' and 'text' columns!")
        print(f"   Available columns: {list(df.columns)}")
        exit(1)
    
    # Prepare data
    X = df['text']
    y = df['label']
    
    print("Processing text with TF-IDF Vectorizer...\n")
    
    # Create vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2),
        max_df=0.95,
        min_df=1  # Changed from 2 to 1 for small datasets
    )
    
    # Vectorize text
    X_vectorized = vectorizer.fit_transform(X)
    
    print(f"✓ Vectorized text into {X_vectorized.shape[1]} features")
    print(f"✓ Matrix shape: {X_vectorized.shape}\n")
    
    # Split data
    print("Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized,
        y,
        test_size=0.2,
        random_state=42
    )
    
    print(f"✓ Train set: {X_train.shape[0]} articles")
    print(f"✓ Test set: {X_test.shape[0]} articles\n")
    
    # Train model
    print("Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"✓ Training accuracy: {train_score:.4f} ({train_score*100:.2f}%)")
    print(f"✓ Testing accuracy: {test_score:.4f} ({test_score*100:.2f}%)\n")
    
    # Save model
    model_dir = Path('./model')
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / 'model.joblib'
    vectorizer_path = model_dir / 'vectorizer.joblib'
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print("="*60)
    print("✅ Model Training Complete!")
    print("="*60)
    print(f"\n📁 Saved files:")
    print(f"   • {model_path} - Trained classifier")
    print(f"   • {vectorizer_path} - Text vectorizer")
    print(f"\n📊 Performance:")
    print(f"   • Training accuracy: {train_score*100:.2f}%")
    print(f"   • Testing accuracy: {test_score*100:.2f}%")
    print(f"\n🚀 Next step: python app.py")
    print()


if __name__ == "__main__":
    try:
        train_model()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
