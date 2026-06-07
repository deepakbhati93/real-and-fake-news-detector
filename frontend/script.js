// Get base URL from current location
const BASE_URL = window.location.origin.includes('localhost') 
    ? 'http://127.0.0.1:5000'
    : window.location.origin;

async function analyzeNews() {
    const textInput = document.getElementById('newsText').value.trim();
    const urlInput = document.getElementById('newsUrl').value.trim();
    const activeTab = document.querySelector('.tab-content.active').id;
    
    // For now, we only support text analysis with this backend
    if (activeTab === 'url-tab') {
        alert('URL analysis is not yet implemented in the backend.');
        return;
    }

    const content = textInput;
    
    // Validate input
    if (!content) {
        alert('Please enter some news text to analyze!');
        return;
    }

    if (content.length < 10) {
        alert('Please enter at least 10 characters for analysis.');
        return;
    }

    // Show loading spinner
    const loadingElement = document.querySelector('.loading');
    const resultElement = document.getElementById('result');
    
    if (loadingElement) {
        loadingElement.style.display = 'flex';
    }
    if (resultElement) {
        resultElement.style.display = 'none';
    }
    
    try {
        // Make an API call to backend with timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

        const response = await fetch(`${BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: content }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            if (response.status === 503) {
                throw new Error('Model not ready. Please train the model first: python train_model_enhanced.py');
            } else if (response.status === 400) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Invalid input');
            } else {
                throw new Error(`Server error: ${response.status}`);
            }
        }

        const data = await response.json();
        
        // Validate response has required fields
        if (!data.prediction) {
            throw new Error('Invalid response from server');
        }

        // Pass prediction and confidence to showResult
        showResult(data.prediction, data.confidence || 50); 

    } catch (error) {
        console.error('Error analyzing news:', error);
        
        let errorMessage = 'An error occurred while analyzing the news.';
        
        if (error.name === 'AbortError') {
            errorMessage = 'Request timeout. Please try again.';
        } else if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Cannot connect to server. Is the Flask app running?';
        } else {
            errorMessage = error.message;
        }
        
        alert(errorMessage);
        
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
    }
}

function showResult(prediction, confidence) {
    const loadingElement = document.querySelector('.loading');
    const resultDiv = document.getElementById('result');
    
    // Hide loading
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
    
    if (!resultDiv) return;
    
    // Use the actual prediction and confidence from the backend
    const isReal = prediction === 'REAL';
    
    // Clamp confidence between 0 and 100
    const confidenceValue = Math.max(0, Math.min(100, Math.round(confidence)));
    
    const resultIcon = resultDiv.querySelector('.result-icon');
    const resultText = resultDiv.querySelector('.result-text');
    const confidenceScore = resultDiv.querySelector('.confidence-score');
    
    if (isReal) {
        resultDiv.className = 'result-section result-real';
        if (resultIcon) resultIcon.textContent = '✅';
        if (resultText) resultText.textContent = 'Likely REAL News';
        if (confidenceScore) confidenceScore.textContent = `Confidence: ${confidenceValue}%`;
    } else {
        resultDiv.className = 'result-section result-fake';
        if (resultIcon) resultIcon.textContent = '⚠️';
        if (resultText) resultText.textContent = 'Possibly FAKE News';
        if (confidenceScore) confidenceScore.textContent = `Confidence: ${confidenceValue}%`;
    }
    
    resultDiv.style.display = 'block';
    
    // Smooth scroll to results
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Tab switching functionality
function switchTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    const selectedTab = document.getElementById(`${tabName}-tab`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Enter key to analyze (when in textarea)
document.addEventListener('DOMContentLoaded', function() {
    const newsTextArea = document.getElementById('newsText');
    if (newsTextArea) {
        newsTextArea.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                analyzeNews();
            }
        });
    }
});