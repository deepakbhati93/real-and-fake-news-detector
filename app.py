from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

# Get absolute path to frontend folder
frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')

# Create a Flask web server with proper paths for templates and static files
app = Flask(__name__, 
    template_folder=frontend_path,
    static_folder=frontend_path,
    static_url_path='/static')

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Global variables for model and vectorizer
model = None
vectorizer = None
model_loaded = False

def load_model_and_vectorizer():
    """Load the trained model and vectorizer from files"""
    global model, vectorizer, model_loaded
    
    print("Loading model and vectorizer...")
    try:
        model = joblib.load('./model/model.joblib')
        vectorizer = joblib.load('./model/vectorizer.joblib')
        print("✓ Model and vectorizer loaded successfully.")
        model_loaded = True
        return True
    except FileNotFoundError as e:
        print(f"ERROR: Model files not found!")
        print(f"Please train the model first:")
        print(f"  1. python fetch_news_openai.py")
        print(f"  2. python train_model_enhanced.py")
        return False
    except Exception as e:
        print(f"ERROR loading model: {e}")
        return False

# Load models on startup
if not load_model_and_vectorizer():
    print("WARNING: App starting without model. Model functionality disabled.")

# Serve frontend files
@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"ERROR rendering template: {e}")
        return jsonify({'error': f'Frontend not found: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    try:
        return jsonify({
            'status': 'healthy',
            'model_loaded': model_loaded,
            'api_key_set': bool(os.getenv('OPENAI_API_KEY')),
            'message': 'News Detector API is running'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_news():
    """Analyze news text and return REAL/FAKE prediction with confidence"""
    try:
        # Validate request has JSON data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        news_text = data.get('text', '').strip()

        if not news_text:
            return jsonify({'error': 'No text provided. Please enter news content.'}), 400
        
        if len(news_text) < 10:
            return jsonify({'error': 'Text too short. Please provide at least 10 characters.'}), 400

        # Check if model is loaded
        if not model_loaded or vectorizer is None or model is None:
            return jsonify({'error': 'Model not ready. Please train the model first.'}), 503

        # Transform the input text using the loaded vectorizer
        try:
            text_vectorized = vectorizer.transform([news_text])
        except Exception as e:
            return jsonify({'error': f'Error vectorizing text: {str(e)}'}), 400

        # Predict using the loaded model
        try:
            prediction = model.predict(text_vectorized)
            # Get probability scores for confidence
            probabilities = model.predict_proba(text_vectorized)
            
            result = prediction[0]
            
            # Calculate confidence (probability of predicted class)
            if result == 'REAL':
                confidence = float(probabilities[0][1]) * 100 if len(probabilities[0]) > 1 else 50
            else:
                confidence = float(probabilities[0][0]) * 100 if len(probabilities[0]) > 0 else 50
            
            confidence = max(0, min(100, round(confidence, 2)))
            
        except Exception as e:
            return jsonify({'error': f'Error making prediction: {str(e)}'}), 500

        # Return the result with confidence score
        return jsonify({
            'prediction': result,
            'confidence': confidence,
            'message': f'{result} news (Confidence: {confidence}%)'
        }), 200
    
    except Exception as e:
        print(f"ERROR in /analyze endpoint: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Return API status and configuration"""
    return jsonify({
        'app_name': 'Real vs Fake News Detector',
        'version': '2.0',
        'model_status': 'LOADED' if model_loaded else 'NOT_LOADED',
        'endpoints': ['/analyze', '/health', '/api/status'],
        'usage': {
            'method': 'POST',
            'endpoint': '/analyze',
            'body': {'text': 'news article text'},
            'response': {'prediction': 'REAL|FAKE', 'confidence': 'percentage'}
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': ['/analyze', '/health', '/api/status']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500

# Run the app
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Real vs Fake News Detector API")
    print("="*60)
    print(f"✓ Model Loaded: {model_loaded}")
    print(f"✓ OpenAI API Key Set: {bool(os.getenv('OPENAI_API_KEY'))}")
    print(f"✓ Server running on: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    # Use port 5000 for the backend server
    app.run(port=5000, debug=True)
