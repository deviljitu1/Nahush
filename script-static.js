// Static version for GitHub Pages
// Users need to add their own API key to make it work

// DOM Elements
const postForm = document.getElementById('postForm');
const resultCard = document.getElementById('resultCard');
const generatedPost = document.getElementById('generatedPost');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const apiNotice = document.getElementById('apiNotice');

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
    
    // Show API setup notice instead of generating
    showApiSetupNotice();
}

// Show API setup notice
function showApiSetupNotice() {
    hideResult();
    hideError();
    hideLoading();
    apiNotice.style.display = 'block';
    
    // Scroll to notice
    apiNotice.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Show API setup instructions
function showApiInstructions() {
    const instructions = `
🔑 API Key Setup Instructions:

1. Visit OpenRouter.ai:
   • Go to https://openrouter.ai
   • Sign up for a free account
   • Get your API key from the dashboard

2. Add your API key to script-static.js:
   • Open script-static.js in a text editor
   • Find line with "YOUR_API_KEY_HERE"
   • Replace with your actual API key

3. Alternative: Use Local Version:
   • Download the full project
   • Run with Python server for secure handling

Example:
const OPENROUTER_API_KEY = 'sk-or-v1-your-actual-api-key-here';
    `;
    
    alert(instructions);
}

// Download local version
function downloadLocalVersion() {
    const message = `
📥 To download the local version:

1. Clone the repository:
   git clone https://github.com/yourusername/linkedin-ai-post-generator.git

2. Set environment variable:
   set OPEN_ROUTER=your-api-key-here

3. Install dependencies:
   pip install -r requirements.txt

4. Run the server:
   python server.py

This version handles API keys securely!
    `;
    
    alert(message);
}

// Display generated result (demo)
function displayResult(post) {
    generatedPost.textContent = post;
    resultCard.style.display = 'block';
    apiNotice.style.display = 'none';
    
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
    apiNotice.style.display = 'none';
}

function hideLoading() {
    loadingSpinner.style.display = 'none';
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    apiNotice.style.display = 'none';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function hideResult() {
    resultCard.style.display = 'none';
}

// Add some interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Show API notice on page load
    apiNotice.style.display = 'block';
    
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
        // Ctrl/Cmd + Enter to show API notice
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            showApiSetupNotice();
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

// Check if input is a valid URL
function isValidURL(string) {
    return URL_REGEX.test(string);
}

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