from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import json
import random
import os
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyCR2qkH4DXw4jBXbT94YnAOgwaSD6r-rBI')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

class AIGenerator:
    def __init__(self, openrouter_api_key, gemini_api_key):
        self.openrouter_api_key = openrouter_api_key
        self.gemini_api_key = gemini_api_key
        self.headers = {
            'Authorization': f'Bearer {self.openrouter_api_key}',
            'Content-Type': 'application/json'
        }

    def generate_linkedin_post(self, topic=None, industry=None, tone="professional", word_count=200):
        """Generate a LinkedIn post using AI, fallback to Gemini if OpenRouter fails"""
        if not topic:
            topics = [
                "latest project completion",
                "industry insights and tips", 
                "professional achievement",
                "client success story",
                "technology trends",
                "business growth strategies",
                "team collaboration",
                "innovation in the field"
            ]
            topic = random.choice(topics)
        
        if not industry:
            industry = "technology and digital marketing"

        prompt = f"""Create a unique, engaging LinkedIn post about: {topic}\n\nContext:\n- Industry: {industry}\n- Tone: {tone}\n- Topic: {topic}\n- Word Count: EXACTLY {word_count} words\n\nRequirements:\n- Make the content SPECIFIC to \"{topic}\" - don't be generic\n- Length: EXACTLY {word_count} words - count carefully\n- Include relevant emojis for visual appeal\n- Make it professional yet conversational\n- End with an engaging question related to {topic}\n- Include 5-7 relevant hashtags specific to {topic}\n- Add value and insights about {topic}\n- Make it shareable and thought-provoking\n- Include a call-to-action\n- Focus on SEO-optimized content with meaningful insights\n- Create high-quality, unique content every time\n\nStructure:\n1. Hook/Opening about {topic}\n2. Key insights or value about {topic}\n3. Personal perspective or industry context\n4. Engaging question for audience\n5. Relevant hashtags\n\nGenerate a unique, high-quality LinkedIn post:"""

        try:
            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=self.headers,
                json={
                    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                    "messages": [
                        {"role": "system", "content": f"You are a professional LinkedIn content creator specializing in {industry}. Create unique, specific, and engaging posts that provide real value to the audience. Each post should be different and tailored to the exact topic provided. Focus on SEO-optimized content with meaningful insights. CRITICAL: Generate EXACTLY {word_count} words."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 800,
                    "temperature": 0.9
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                raise Exception(f"AI API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"OpenRouter failed, falling back to Gemini: {e}")
            return self.generate_with_gemini(prompt, word_count)

    def generate_post_from_article(self, url, industry=None, tone="professional", word_count=200):
        """Generate a LinkedIn post from article content, fallback to Gemini if OpenRouter fails"""
        try:
            article_content = self.extract_article_content(url)
            if not article_content:
                raise Exception("Could not extract content from the article URL")
            
            domain = self.extract_domain(url)
            source_name = self.get_source_name(domain)
            
            prompt = f"""Create a unique, engaging LinkedIn post summarizing this article:\n\nArticle Content:\n{article_content}\n\nSource: {source_name}\n\nRequirements:\n- Industry: {industry or 'general'}\n- Tone: {tone}\n- Word Count: EXACTLY {word_count} words\n- Focus on the MOST IMPORTANT news and insights from the article\n- Include specific facts, numbers, and key details from the article\n- Make it SEO-optimized with meaningful content\n- Include relevant emojis\n- End with an engaging question\n- Add 5-7 relevant hashtags\n- Include a call-to-action\n- Create high-quality, unique content that provides real value\n- Make it shareable and thought-provoking\n\nStructure:\n1. Hook with the most important news/finding\n2. Key insights and specific details from the article\n3. Industry implications or broader context\n4. Engaging question for audience\n5. Relevant hashtags\n\nGenerate a unique, high-quality LinkedIn post summary:"""

            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=self.headers,
                json={
                    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                    "messages": [
                        {"role": "system", "content": f"You are a professional LinkedIn content creator specializing in {industry or 'general'}. Create unique, specific, and engaging posts that provide real value to the audience. Focus on SEO-optimized content with meaningful insights. CRITICAL: Generate EXACTLY {word_count} words."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 800,
                    "temperature": 0.9
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                raise Exception(f"AI API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"OpenRouter failed, falling back to Gemini: {e}")
            return self.generate_with_gemini(prompt, word_count)

    def extract_article_content(self, url):
        """Extract content from article URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try to find main content areas
            content_selectors = [
                'article',
                '[class*="content"]',
                '[class*="article"]',
                '[class*="post"]',
                '[class*="story"]',
                'main',
                '.entry-content',
                '.post-content',
                '.article-content',
                '.story-content'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        text = element.get_text(separator=' ', strip=True)
                        if len(text) > 200:  # Only use substantial content
                            content += text + " "
            
            # If no specific content areas found, get all text
            if not content.strip():
                content = soup.get_text(separator=' ', strip=True)
            
            # Clean up the content
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)]', '', content)
            
            # Limit content length for API
            if len(content) > 3000:
                content = content[:3000] + "..."
            
            return content.strip()
            
        except Exception as e:
            print(f"❌ Error extracting article content: {e}")
            return None

    def extract_domain(self, url):
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return "unknown"

    def get_source_name(self, domain):
        """Get readable source name from domain"""
        domain_mapping = {
            'techcrunch.com': 'TechCrunch',
            'wired.com': 'Wired',
            'theverge.com': 'The Verge',
            'arstechnica.com': 'Ars Technica',
            'cnn.com': 'CNN',
            'bbc.com': 'BBC',
            'reuters.com': 'Reuters',
            'bloomberg.com': 'Bloomberg',
            'forbes.com': 'Forbes',
            'hbr.org': 'Harvard Business Review',
            'medium.com': 'Medium',
            'substack.com': 'Substack',
            'github.com': 'GitHub',
            'stackoverflow.com': 'Stack Overflow',
            'dev.to': 'DEV Community'
        }
        
        for key, value in domain_mapping.items():
            if key in domain.lower():
                return value
        
        # Extract from domain if not in mapping
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain.split('.')[0].title()

    def generate_with_gemini(self, prompt, word_count):
        """Generate content using Gemini AI"""
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": min(word_count * 2, 1024),
                    "temperature": 0.9
                }
            }
            response = requests.post(
                f"{GEMINI_API_URL}?key={self.gemini_api_key}",
                headers=headers,
                json=data,
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()
                # Gemini's response structure
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                print(f"Gemini API Error: {response.status_code} - {response.text}")
                return "[AI Error: Unable to generate content from both OpenRouter and Gemini]"
        except Exception as e:
            print(f"Gemini fallback failed: {e}")
            return "[AI Error: Unable to generate content from both OpenRouter and Gemini]"

# Initialize AI Generator
ai_generator = AIGenerator(OPENROUTER_API_KEY, GEMINI_API_KEY)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    """Serve the CSS file"""
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def script():
    """Serve the JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/generate', methods=['POST'])
def generate_post():
    """Generate LinkedIn post endpoint"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        industry = data.get('industry', 'technology')
        tone = data.get('tone', 'professional')
        word_count = int(data.get('word_count', 200))
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        if word_count < 50 or word_count > 1000:
            return jsonify({'error': 'Word count must be between 50 and 1000'}), 400
        
        # Check if topic is a URL
        if topic.startswith(('http://', 'https://')):
            post = ai_generator.generate_post_from_article(topic, industry, tone, word_count)
        else:
            post = ai_generator.generate_linkedin_post(topic, industry, tone, word_count)
        
        return jsonify({'post': post})
        
    except Exception as e:
        print(f"Error generating post: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'message': 'LinkedIn AI Post Generator is running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 