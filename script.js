// API Configuration - API calls will be made through the backend
const API_URL = '/generate';

// DOM Elements
const postForm = document.getElementById('postForm');
const resultCard = document.getElementById('resultCard');
const generatedPost = document.getElementById('generatedPost');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

// Event Listeners
postForm.addEventListener('submit', handleFormSubmit);

// URL detection regex - improved to handle more URL formats
const URL_REGEX = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?(\?[^\s]*)?$/;

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const topic = document.getElementById('topic').value.trim();
    const industry = document.getElementById('industry').value;
    const tone = document.getElementById('tone').value;
    const wordCount = parseInt(document.getElementById('wordCount').value) || 200;
    
    if (!topic) {
        showError('Please enter a topic or paste an article URL');
        return;
    }

    if (wordCount < 50 || wordCount > 1000) {
        showError('Word count must be between 50 and 1000');
        return;
    }
    
    // Show loading with quality-focused message
    showLoading();
    hideError();
    hideResult();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic: topic,
                industry: industry,
                tone: tone,
                word_count: wordCount
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to generate post');
        }

        const data = await response.json();
        
        if (data.post) {
            displayResult(data.post);
        } else {
            throw new Error('No post content received');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to generate high-quality content: ${error.message}. Please try again.`);
    } finally {
        hideLoading();
    }
}

// Check if input is a valid URL
function isValidURL(string) {
    return URL_REGEX.test(string);
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
    const copyBtn = document.querySelector('.copy-btn');
    const originalText = copyBtn.innerHTML;
    
    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
    copyBtn.style.backgroundColor = '#28a745';
    
    setTimeout(() => {
        copyBtn.innerHTML = originalText;
        copyBtn.style.backgroundColor = '';
    }, 2000);
}

// Open LinkedIn with pre-filled post
function openLinkedIn() {
    const postText = generatedPost.textContent;
    const linkedinUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}&title=${encodeURIComponent('Check out this AI-generated LinkedIn post!')}&summary=${encodeURIComponent(postText)}`;
    window.open(linkedinUrl, '_blank');
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '15px 20px';
    notification.style.borderRadius = '8px';
    notification.style.color = 'white';
    notification.style.fontWeight = '500';
    notification.style.zIndex = '1000';
    notification.style.transform = 'translateX(100%)';
    notification.style.transition = 'transform 0.3s ease';
    
    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            break;
        case 'warning':
            notification.style.backgroundColor = '#ffc107';
            notification.style.color = '#212529';
            break;
        default:
            notification.style.backgroundColor = '#007bff';
    }
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Generate new post
function generateNew() {
    hideResult();
    document.getElementById('topic').focus();
}

// Utility functions for showing/hiding elements
function showLoading() {
    const spinner = document.getElementById('loadingSpinner');
    const loadingText = spinner.querySelector('p');
    loadingText.textContent = 'Generating high-quality AI content... This may take a moment for the best results.';
    spinner.style.display = 'flex';
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

// Add interactive features
document.addEventListener('DOMContentLoaded', function() {
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
    
    // Add URL detection indicator
    const topicInput = document.getElementById('topic');
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
    
    // Add character count for topic input
    addCharacterCount();
});

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