import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression  # Changed from PassiveAggressiveClassifier for consistency
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
from dotenv import load_dotenv
import glob

# Load environment variables
load_dotenv()

def find_latest_csv():
    """Find the latest CSV file from any source"""
    # Look for news_from_*.csv files first
    pattern = "news_from_*.csv"
    files = glob.glob(pattern)
    
    if files:
        latest = max(files, key=os.path.getmtime)
        return latest
    
    # Fallback to original files
    if os.path.exists('news_from_openai.csv'):
        return 'news_from_openai.csv'
    elif os.path.exists('news_from_api.csv'):
        return 'news_from_api.csv'
    else:
        return 'news.csv'

CSV_FILE = find_latest_csv()
print(f"✓ Using data: {CSV_FILE}")

print(f"📊 Loading dataset from {CSV_FILE}...\n")

try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"❌ ERROR: {CSV_FILE} not found!")
    print("\nBefore training, run:")
    print("  python fetch_news_openai.py")
    print("  or")
    print("  python fetch_news_multi.py")
    exit(1)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}\n")

# Check for required columns
if 'text' not in df.columns or 'label' not in df.columns:
    print("❌ ERROR: CSV must have 'text' and 'label' columns")
    print(f"Found columns: {df.columns.tolist()}")
    exit(1)

# Handle missing values
initial_count = len(df)
df = df.dropna(subset=['text', 'label'])
removed_count = initial_count - len(df)

if removed_count > 0:
    print(f"⚠️ Removed {removed_count} rows with missing values")

print(f"✓ Using {len(df)} rows\n")

# Get the labels and text
labels = df['label']
text = df['text']

print("📊 Label distribution:")
print(labels.value_counts())
print()

# Check if we have both labels
if len(labels.unique()) < 2:
    print("⚠️ WARNING: Only one label found! Model needs both REAL and FAKE samples.")
    print(f"Labels in data: {labels.unique()}")

# Split the dataset into training and testing sets
print("Splitting data (80% train, 20% test)...")
try:
    x_train, x_test, y_train, y_test = train_test_split(
        text, labels, test_size=0.2, random_state=42, stratify=labels
    )
except ValueError as e:
    print(f"❌ Error splitting data: {e}")
    print("Make sure you have at least 2 samples in your dataset")
    exit(1)

print(f"✓ Training set: {len(x_train)} samples")
print(f"✓ Test set: {len(x_test)} samples\n")

# Initialize a TfidfVectorizer
print("🔤 Initializing TF-IDF Vectorizer...")
tfidf_vectorizer = TfidfVectorizer(
    stop_words='english',
    max_df=0.7,
    min_df=1,
    ngram_range=(1, 2),
    max_features=5000
)

# Fit and transform the training set, transform the test set
print("Fitting TF-IDF on training data...")
tfidf_train = tfidf_vectorizer.fit_transform(x_train)
tfidf_test = tfidf_vectorizer.transform(x_test)

print(f"✓ TF-IDF matrix shape (train): {tfidf_train.shape}")
print(f"✓ TF-IDF matrix shape (test): {tfidf_test.shape}\n")

# Initialize and train LogisticRegression (consistent with enhanced trainer)
print("🤖 Training Logistic Regression Model...")
model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    n_jobs=-1,
    solver='lbfgs'  # Better for smaller datasets
)

try:
    model.fit(tfidf_train, y_train)
    print("✓ Model training complete\n")
except Exception as e:
    print(f"❌ Error training model: {e}")
    exit(1)

# Evaluate the model
print("📈 Evaluating model...")
y_pred = model.predict(tfidf_test)
score = accuracy_score(y_test, y_pred)

print("="*60)
print(f"✅ MODEL ACCURACY: {round(score*100, 2)}%")
print("="*60)
print()

# Detailed classification report
print("📋 Classification Report:")
print("-"*60)
print(classification_report(y_test, y_pred, zero_division=0))

# Confusion matrix
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)
print()

# Save models
model_dir = './model'
os.makedirs(model_dir, exist_ok=True)

print("💾 Saving model files...")
try:
    joblib.dump(model, f'{model_dir}/model.joblib')
    joblib.dump(tfidf_vectorizer, f'{model_dir}/vectorizer.joblib')
    print(f"✓ Model saved to: {model_dir}/model.joblib")
    print(f"✓ Vectorizer saved to: {model_dir}/vectorizer.joblib\n")
except Exception as e:
    print(f"❌ Error saving models: {e}")
    exit(1)

print("="*60)
print("🎉 TRAINING COMPLETE!")
print("="*60)
print("\n✅ Next steps:")
print("  1. python app.py")
print("  2. Open http://127.0.0.1:5000 in your browser")
print()


# Confusion matrix
print("Confusion Matrix:")
print("-"*60)
cm = confusion_matrix(y_test, y_pred, labels=['FAKE', 'REAL'])
print(cm)
print()

# 6. Save the trained model and the vectorizer
print("Saving model and vectorizer...")

# Create model directory if it doesn't exist
os.makedirs('./model', exist_ok=True)

joblib.dump(pac, './model/model.joblib')
joblib.dump(tfidf_vectorizer, './model/vectorizer.joblib')

print("✓ Model saved to: ./model/model.joblib")
print("✓ Vectorizer saved to: ./model/vectorizer.joblib")
print()
print("="*60)
print("Training complete! Ready to run the Flask app.")
print("="*60)
