// OpenRouter API Configuration
const OPENROUTER_API_KEY = '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';
const API_URL = 'https://openrouter.ai/api/v1/chat/completions';

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
        showError('Failed to generate post. Please try again.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Check if input is a valid URL
function isValidURL(string) {
    return URL_REGEX.test(string);
}

// Extract article content from URL
async function extractArticleContent(url) {
    try {
        // Use a CORS proxy to fetch the article content
        const proxyUrl = `https://api.allorigins.win/get?url=${encodeURIComponent(url)}`;
        const response = await fetch(proxyUrl);
        const data = await response.json();
        
        if (data.contents) {
            // Parse the HTML content
            const parser = new DOMParser();
            const doc = parser.parseFromString(data.contents, 'text/html');
            
            // Extract text content from common article selectors
            const selectors = [
                'article',
                '[class*="content"]',
                '[class*="article"]',
                '[class*="post"]',
                '.post-content',
                '.article-content',
                '.entry-content',
                'main',
                '.main-content'
            ];
            
            let content = '';
            for (const selector of selectors) {
                const element = doc.querySelector(selector);
                if (element) {
                    content = element.textContent.trim();
                    if (content.length > 100) break;
                }
            }
            
            // If no specific content found, get body text
            if (!content || content.length < 100) {
                content = doc.body.textContent.trim();
            }
            
            // Clean up the content
            content = content.replace(/\s+/g, ' ').substring(0, 2000);
            
            return {
                title: doc.title || 'Article',
                content: content,
                url: url
            };
        }
        
        throw new Error('Could not extract content from URL');
    } catch (error) {
        console.error('Error extracting article content:', error);
        throw new Error('Failed to extract article content. Please check the URL and try again.');
    }
}

// Generate LinkedIn post from article URL
async function generateLinkedInPostFromArticle(url, industry, tone) {
    try {
        // Extract article content
        const articleData = await extractArticleContent(url);
        
        // Create prompt for article summarization
        const prompt = createArticlePrompt(articleData, industry, tone);
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://openrouter.ai/'
            },
            body: JSON.stringify({
                model: 'mistralai/mistral-small-3.2-24b-instruct:free',
                messages: [
                    {
                        role: 'system',
                        content: 'You are a professional LinkedIn content creator. Create engaging posts that summarize articles and drive engagement.'
                    },
                    {
                        role: 'user',
                        content: prompt
                    }
                ],
                max_tokens: 400,
                temperature: 0.7
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`API Error: ${errorData.error?.message || response.statusText}`);
        }
        
        const data = await response.json();
        return data.choices[0].message.content.trim();
    } catch (error) {
        console.error('Error generating post from article:', error);
        throw error;
    }
}

// Create prompt for article summarization
function createArticlePrompt(articleData, industry, tone) {
    return `Create a compelling LinkedIn post that summarizes this article:

Article Title: ${articleData.title}
Article URL: ${articleData.url}
Article Content: ${articleData.content.substring(0, 1500)}...

Requirements:
- Tone: ${tone}
- Industry Context: ${industry}
- Length: 3-5 sentences
- Include emojis for engagement
- Summarize key points from the article
- Add your professional insights
- End with a question to encourage interaction
- Include 3-5 relevant hashtags
- Mention the source article

Format:
🚀 [Engaging opening about the article topic]

[2-3 sentences summarizing key insights from the article]

[Your professional take or industry perspective]

[Question to engage audience]

[Source: Article Title]

#Hashtag1 #Hashtag2 #Hashtag3

Generate the LinkedIn post:`;
}

// Generate LinkedIn post using OpenRouter API
async function generateLinkedInPost(topic, industry, tone) {
    const prompt = createPrompt(topic, industry, tone);
    
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://openrouter.ai/'
        },
        body: JSON.stringify({
            model: 'mistralai/mistral-small-3.2-24b-instruct:free',
            messages: [
                {
                    role: 'system',
                    content: 'You are a professional LinkedIn content creator. Create engaging, authentic posts that drive engagement and provide value to the audience.'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            max_tokens: 300,
            temperature: 0.7
        })
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`API Error: ${errorData.error?.message || response.statusText}`);
    }
    
    const data = await response.json();
    return data.choices[0].message.content.trim();
}

// Create prompt for AI generation
function createPrompt(topic, industry, tone) {
    const defaultTopic = topic || 'latest project completion';
    const defaultIndustry = industry || 'technology and digital marketing';
    
    return `Create a compelling LinkedIn post about ${defaultTopic} in the ${defaultIndustry} industry.

Requirements:
- Tone: ${tone}
- Length: 2-4 sentences
- Include emojis for engagement
- Make it professional yet engaging
- End with a question to encourage interaction
- Include 3-5 relevant hashtags

Example format:
🚀 [Engaging opening about the topic]

[2-3 sentences with insights, achievements, or tips]

[Question to engage audience]

#Hashtag1 #Hashtag2 #Hashtag3

Generate the post:`;
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

// Show notification
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#d4edda' : '#d1ecf1'};
        color: ${type === 'success' ? '#155724' : '#0c5460'};
        border: 1px solid ${type === 'success' ? '#c3e6cb' : '#bee5eb'};
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 500;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

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

// Add loading animation for better user experience
function addLoadingAnimation() {
    const generateBtn = document.querySelector('.generate-btn');
    const originalText = generateBtn.innerHTML;
    
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    generateBtn.disabled = true;
    
    return () => {
        generateBtn.innerHTML = originalText;
        generateBtn.disabled = false;
    };
}

// Enhanced error handling with retry functionality
function showErrorWithRetry(message) {
    showError(message);
    
    const retryBtn = document.createElement('button');
    retryBtn.textContent = 'Retry';
    retryBtn.className = 'action-btn copy-btn';
    retryBtn.style.marginTop = '10px';
    retryBtn.onclick = () => {
        hideError();
        postForm.dispatchEvent(new Event('submit'));
    };
    
    errorMessage.appendChild(retryBtn);
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