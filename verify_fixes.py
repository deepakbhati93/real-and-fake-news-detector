#!/usr/bin/env python3
"""
Comprehensive Bug Fix & API Integration Verification Script
Tests all components and provides detailed diagnostics
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_check(text, status):
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {text}")

def check_environment():
    """Check environment setup"""
    print_header("🔍 Environment Check")
    
    load_dotenv()
    
    # Check .env exists
    env_exists = os.path.exists('.env')
    print_check(".env file exists", env_exists)
    
    if not env_exists:
        print("  → Run: python setup_api_keys.py")
        return False
    
    # Check API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    print_check("OPENAI_API_KEY set", bool(openai_key))
    if openai_key:
        print(f"  → Key starts with: {openai_key[:20]}...")
    
    ai_service = os.getenv('AI_SERVICE', 'openai')
    print_check(f"AI_SERVICE configured: {ai_service}", True)
    
    return env_exists and bool(openai_key)

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("📦 Dependency Check")
    
    dependencies = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'pandas': 'pandas',
        'scikit_learn': 'scikit-learn',
        'joblib': 'joblib',
        'requests': 'requests',
        'dotenv': 'python-dotenv',
        'openai': 'OpenAI',
    }
    
    all_installed = True
    for import_name, display_name in dependencies.items():
        try:
            __import__(import_name)
            print_check(f"{display_name}", True)
        except ImportError:
            print_check(f"{display_name}", False)
            all_installed = False
    
    if not all_installed:
        print("\n→ Run: pip install -r requirements.txt")
    
    return all_installed

def check_project_structure():
    """Check if required files exist"""
    print_header("📁 Project Structure Check")
    
    required_files = {
        'app.py': 'Flask Backend',
        'fetch_news_openai.py': 'OpenAI Data Fetcher',
        'fetch_news_multi.py': 'Multi-API Fetcher',
        'train_model.py': 'Model Trainer (Original)',
        'train_model_enhanced.py': 'Model Trainer (Enhanced)',
        'frontend/index.html': 'Web Interface',
        'frontend/script.js': 'Frontend Logic',
        'requirements.txt': 'Dependencies',
    }
    
    all_exist = True
    for file_path, description in required_files.items():
        exists = os.path.exists(file_path)
        print_check(f"{description}: {file_path}", exists)
        all_exist = all_exist and exists
    
    return all_exist

def check_model_files():
    """Check if trained model files exist"""
    print_header("🤖 Model Files Check")
    
    model_exists = os.path.exists('./model/model.joblib')
    vectorizer_exists = os.path.exists('./model/vectorizer.joblib')
    
    print_check("model.joblib (Trained classifier)", model_exists)
    print_check("vectorizer.joblib (Text vectorizer)", vectorizer_exists)
    
    if not (model_exists and vectorizer_exists):
        print("\n→ Run: python fetch_news_multi.py")
        print("→ Run: python train_model_enhanced.py")
        return False
    
    return True

def check_data_files():
    """Check if training data CSV files exist"""
    print_header("📊 Data Files Check")
    
    data_files = [
        'news_from_openai.csv',
        'news_from_huggingface.csv',
        'news_from_cohere.csv',
        'news_from_google.csv',
        'news.csv',
    ]
    
    found_files = []
    for file_path in data_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print_check(f"{file_path} ({size} bytes)", True)
            found_files.append(file_path)
    
    if not found_files:
        print("\n→ Run: python fetch_news_multi.py")
        return False
    
    return True

def test_api_connection():
    """Test Flask API connection"""
    print_header("🌐 API Connection Test")
    
    try:
        import requests
        response = requests.get('http://127.0.0.1:5000/health', timeout=5)
        if response.status_code == 200:
            print_check("API is responding", True)
            data = response.json()
            print_check(f"Model loaded: {data.get('model_loaded')}", data.get('model_loaded', False))
            return True
        else:
            print_check("API responding", False)
            return False
    except Exception as e:
        print_check("API Connection", False)
        print(f"  → Error: {str(e)[:50]}")
        print("  → Make sure: python app.py is running")
        return False

def test_model_prediction():
    """Test a prediction through the API"""
    print_header("🎯 Model Prediction Test")
    
    try:
        import requests
        
        test_text = "Breaking news: Scientists discover new renewable energy technology after 5 years of research."
        
        response = requests.post(
            'http://127.0.0.1:5000/analyze',
            json={'text': test_text},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            prediction = data.get('prediction')
            confidence = data.get('confidence')
            
            print_check("Prediction request successful", True)
            print(f"  → Prediction: {prediction}")
            print(f"  → Confidence: {confidence}%")
            return True
        else:
            print_check("Prediction request", False)
            print(f"  → Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_check("Model Prediction Test", False)
        print(f"  → Error: {str(e)[:50]}")
        print("  → Make sure: python app.py is running")
        return False

def check_code_quality():
    """Check for common code issues"""
    print_header("⚙️ Code Quality Checks")
    
    issues = []
    
    # Check app.py for proper error handling
    with open('app.py', 'r') as f:
        content = f.read()
        if 'try:' in content and 'except' in content:
            print_check("app.py has error handling", True)
        else:
            print_check("app.py has error handling", False)
            issues.append("app.py: Missing error handling")
        
        if '@app.route' in content:
            print_check("app.py has API endpoints", True)
        else:
            print_check("app.py has API endpoints", False)
    
    # Check script.js for proper error handling
    with open('frontend/script.js', 'r') as f:
        content = f.read()
        if 'try:' in content or 'catch' in content:
            print_check("script.js has error handling", True)
        else:
            print_check("script.js has error handling", False)
            issues.append("script.js: Missing error handling")
    
    return len(issues) == 0

def generate_report():
    """Generate comprehensive report"""
    print_header("🐛 BUG FIX & API INTEGRATION VERIFICATION")
    
    results = {
        'Environment': check_environment(),
        'Dependencies': check_dependencies(),
        'Project Structure': check_project_structure(),
        'Data Files': check_data_files(),
        'Model Files': check_model_files(),
        'Code Quality': check_code_quality(),
    }
    
    print_header("📋 Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_val in results.items():
        symbol = "✓" if passed_val else "✗"
        print(f"{symbol} {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("  1. run: python app.py")
        print("  2. Open: http://127.0.0.1:5000")
        print("  3. Test analyzing a news article")
    else:
        print(f"\n⚠️ {total - passed} check(s) failed. See above for details.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    generate_report()
    
    # Optional: Run API tests if app is running
    print("\nWould you like to test the API? (requires app.py to be running)")
    try:
        import requests
        try:
            response = requests.get('http://127.0.0.1:5000/health', timeout=1)
            if response.status_code == 200:
                print("\n📡 Detected running Flask app. Running API tests...\n")
                test_api_connection()
                test_model_prediction()
        except:
            pass
    except ImportError:
        pass
