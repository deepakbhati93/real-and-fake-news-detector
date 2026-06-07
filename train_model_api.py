import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if we have API data, otherwise fall back to CSV
if os.path.exists('news_from_api.csv'):
    CSV_FILE = 'news_from_api.csv'
    print("Using API-fetched data: news_from_api.csv")
else:
    CSV_FILE = 'news.csv'
    print("Using CSV file: news.csv")
    print("To use API data instead, run: python fetch_news_data.py")

# 1. Load the dataset
print(f"\nLoading dataset from {CSV_FILE}...")
df = pd.read_csv(CSV_FILE)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nLabel distribution:")
print(df['label'].value_counts())

# Get the labels and text
labels = df['label']
text = df['text']

# 2. Split the dataset into training and testing sets
print("\nSplitting data (80% train, 20% test)...")
x_train, x_test, y_train, y_test = train_test_split(
    text, labels, test_size=0.2, random_state=7, stratify=labels
)

# 3. Initialize a TfidfVectorizer
print("Initializing TF-IDF Vectorizer...")
tfidf_vectorizer = TfidfVectorizer(
    stop_words='english',
    max_df=0.7,
    min_df=2,
    ngram_range=(1, 2)
)

# Fit and transform the training set, transform the test set
tfidf_train = tfidf_vectorizer.fit_transform(x_train)
tfidf_test = tfidf_vectorizer.transform(x_test)

print(f"TF-IDF matrix shape: {tfidf_train.shape}")

# 4. Initialize a PassiveAggressiveClassifier
print("\nTraining Passive Aggressive Classifier...")
pac = PassiveAggressiveClassifier(max_iter=50, random_state=7)
pac.fit(tfidf_train, y_train)

# 5. Predict on the test set and calculate accuracy
print("Evaluating model...")
y_pred = pac.predict(tfidf_test)
score = accuracy_score(y_test, y_pred)

print(f"\n{'='*50}")
print(f"Model Accuracy: {round(score*100, 2)}%")
print(f"{'='*50}")

# Print detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 6. Save the trained model and the vectorizer
print("\nSaving model and vectorizer...")

# Create model directory if it doesn't exist
os.makedirs('./model', exist_ok=True)

joblib.dump(pac, './model/model.joblib')
joblib.dump(tfidf_vectorizer, './model/vectorizer.joblib')

print("✓ Model saved to ./model/model.joblib")
print("✓ Vectorizer saved to ./model/vectorizer.joblib")
print("\nTraining complete!")
