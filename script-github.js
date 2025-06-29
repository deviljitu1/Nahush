// GitHub-ready version - works both locally and on GitHub Pages
// Users need to add their own API key to make it work

// API Configuration
const LOCAL_API_URL = 'http://localhost:8000/api/generate-post';
const GITHUB_API_URL = 'https://your-backend-url.com/api/generate-post'; // For production

// Detect if running locally or on GitHub Pages
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = isLocal ? LOCAL_API_URL : null; // Will be null on GitHub Pages

// DOM Elements
const postForm = document.getElementById('postForm');
const resultCard = document.getElementById('resultCard');
const generatedPost = document.getElementById('generatedPost');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

// Event Listeners
postForm.addEventListener('submit', handleFormSubmit);

// URL detection regex
const URL_REGEX = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const topic = document.getElementById('topic').value.trim();
    const industry = document.getElementById('industry').value;
    const tone = document.getElementById('tone').value;
    
    // Check if we're on GitHub Pages (no local server)
    if (!isLocal) {
        showGitHubSetupNotice();
        return;
    }
    
    // Show loading spinner
    showLoading();
    hideError();
    hideResult();
    
    try {
        let post;
        
        // Check if topic is a URL
        if (isValidURL(topic)) {
            post = await generateLinkedInPostFromArticle(topic, industry, tone);
        } else {
            post = await generateLinkedInPost(topic, industry, tone);
        }
        
        displayResult(post);
    } catch (error) {
        console.error('Error details:', error);
        showError('Failed to generate post. Please make sure the Python server is running on port 8000.');
    } finally {
        hideLoading();
    }
}

// Show GitHub setup notice
function showGitHubSetupNotice() {
    const notice = `
🔑 API Key Setup Required

This tool requires an OpenRouter API key to work.

📋 Setup Instructions:
1. Get a free API key from https://openrouter.ai
2. Download the local version for full functionality
3. Or add your API key to the code

💡 Quick Start:
• Clone the repository
• Run: python server.py
• Visit: http://localhost:8000

Would you like to see detailed setup instructions?
    `;
    
    if (confirm(notice)) {
        showDetailedInstructions();
    }
}

// Show detailed setup instructions
function showDetailedInstructions() {
    const instructions = `
🔧 Detailed Setup Instructions:

📥 Option 1: Local Setup (Recommended)
1. Clone the repository:
   git clone https://github.com/yourusername/linkedin-ai-post-generator.git

2. Navigate to the folder:
   cd linkedin-ai-post-generator

3. Set your API key:
   set OPEN_ROUTER=your-api-key-here

4. Install dependencies:
   pip install -r requirements.txt

5. Start the server:
   python server.py

6. Open http://localhost:8000

📝 Option 2: Add API Key to Code
1. Get API key from https://openrouter.ai
2. Edit script.js
3. Replace YOUR_API_KEY_HERE with your key
4. Upload to GitHub Pages

🔗 Repository: https://github.com/yourusername/linkedin-ai-post-generator
    `;
    
    alert(instructions);
}

// Check if input is a valid URL
function isValidURL(string) {
    return URL_REGEX.test(string);
}

// Generate LinkedIn post using backend API
async function generateLinkedInPost(topic, industry, tone) {
    console.log('Making API call to:', API_URL);
    
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: 'topic',
            topic: topic,
            industry: industry,
            tone: tone
        })
    });
    
    console.log('Response status:', response.status);
    
    if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`Server error: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    return data.post;
}

// Generate LinkedIn post from article URL using backend API
async function generateLinkedInPostFromArticle(url, industry, tone) {
    console.log('Making article API call to:', API_URL);
    
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: 'article',
            url: url,
            industry: industry,
            tone: tone
        })
    });
    
    console.log('Article response status:', response.status);
    
    if (!response.ok) {
        const errorText = await response.text();
        console.error('Article error response:', errorText);
        throw new Error(`Server error: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Article response data:', data);
    return data.post;
}

// Display generated result
function displayResult(post) {
    generatedPost.textContent = post;
    resultCard.style.display = 'block';
    
    // Scroll to result
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Copy post to clipboard
async function copyToClipboard() {
    const postText = generatedPost.textContent;
    
    try {
        await navigator.clipboard.writeText(postText);
        showCopySuccess();
    } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = postText;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showCopySuccess();
    }
}

// Show copy success message
function showCopySuccess() {
    const successDiv = document.createElement('div');
    successDiv.className = 'copy-success';
    successDiv.innerHTML = '<i class="fas fa-check"></i> Post copied to clipboard!';
    
    const postPreview = document.querySelector('.post-preview');
    postPreview.appendChild(successDiv);
    
    // Remove success message after 3 seconds
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.parentNode.removeChild(successDiv);
        }
    }, 3000);
}

// Open LinkedIn feed page directly
function openLinkedIn() {
    // Open LinkedIn's main feed page
    window.open('https://www.linkedin.com/feed/', '_blank');
}

// Generate new post
function generateNew() {
    hideResult();
    hideError();
    document.getElementById('topic').focus();
}

// Utility functions for showing/hiding elements
function showLoading() {
    loadingSpinner.style.display = 'block';
}

function hideLoading() {
    loadingSpinner.style.display = 'none';
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function hideResult() {
    resultCard.style.display = 'none';
}

// Add some interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Show environment info
    console.log('Environment:', isLocal ? 'Local' : 'GitHub Pages');
    console.log('API URL:', API_URL);
    
    // Add focus effects to form inputs
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to generate post
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            postForm.dispatchEvent(new Event('submit'));
        }
        
        // Escape to clear form
        if (e.key === 'Escape') {
            postForm.reset();
            hideResult();
            hideError();
        }
    });
    
    // Add sample topics and URL detection
    const topicInput = document.getElementById('topic');
    const sampleTopics = [
        'web development project completion',
        'client success story',
        'industry insights and tips',
        'professional achievement',
        'team collaboration success',
        'technology innovation',
        'business growth strategies',
        'remote work productivity'
    ];
    
    const sampleUrls = [
        'https://example.com/article-about-ai',
        'https://techcrunch.com/2024/01/15/ai-trends',
        'https://hbr.org/2024/01/leadership-insights'
    ];
    
    topicInput.addEventListener('click', function() {
        if (!this.value) {
            const randomChoice = Math.random() > 0.7 ? sampleUrls : sampleTopics;
            this.placeholder = randomChoice[Math.floor(Math.random() * randomChoice.length)];
        }
    });
    
    // Add URL detection indicator
    topicInput.addEventListener('input', function() {
        const isUrl = isValidURL(this.value);
        const formGroup = this.parentElement;
        
        // Remove existing indicator
        const existingIndicator = formGroup.querySelector('.url-indicator');
        if (existingIndicator) {
            existingIndicator.remove();
        }
        
        if (isUrl && this.value.trim()) {
            const indicator = document.createElement('div');
            indicator.className = 'url-indicator';
            indicator.innerHTML = '<i class="fas fa-link"></i> Article detected - will summarize content';
            indicator.style.color = '#0077b5';
            indicator.style.fontSize = '0.8rem';
            indicator.style.marginTop = '5px';
            indicator.style.fontWeight = '500';
            formGroup.appendChild(indicator);
        }
    });
});

// Add smooth scrolling for better UX
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Add character count for topic input
function addCharacterCount() {
    const topicInput = document.getElementById('topic');
    const charCount = document.createElement('div');
    charCount.className = 'char-count';
    charCount.style.fontSize = '0.8rem';
    charCount.style.color = '#666';
    charCount.style.textAlign = 'right';
    charCount.style.marginTop = '5px';
    
    topicInput.parentElement.appendChild(charCount);
    
    topicInput.addEventListener('input', function() {
        const count = this.value.length;
        const max = 500; // Increased for URLs
        charCount.textContent = `${count}/${max}`;
        
        if (count > max) {
            charCount.style.color = '#dc3545';
        } else {
            charCount.style.color = '#666';
        }
    });
}

// Initialize character count
document.addEventListener('DOMContentLoaded', addCharacterCount); 