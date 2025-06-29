from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import json
import random
import os
from urllib.parse import urlparse
import re

app = Flask(__name__)

# Configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

class AIGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openrouter.ai/"
        }

    def generate_linkedin_post(self, topic=None, industry=None, tone="professional"):
        """Generate a LinkedIn post using AI"""
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

        prompt = f"""Create a compelling LinkedIn post about {topic} in the {industry} industry.

Requirements:
- Tone: {tone}
- Length: 2-4 sentences
- Include emojis for engagement
- Make it professional yet engaging
- End with a question to encourage interaction
- Include 3-5 relevant hashtags

Generate the post:"""

        try:
            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=self.headers,
                json={
                    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                    "messages": [
                        {"role": "system", "content": "You are a professional LinkedIn content creator. Create engaging, authentic posts that drive engagement and provide value to the audience."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 300,
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return self._get_fallback_post(topic, industry, tone)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._get_fallback_post(topic, industry, tone)

    def generate_post_from_article(self, url, industry=None, tone="professional"):
        """Generate LinkedIn post from article URL"""
        try:
            # Extract content from URL using a simple approach
            # In production, you might want to use a more robust article extraction service
            article_content = self._extract_article_content(url)
            
            prompt = f"""Create a compelling LinkedIn post summarizing this article: {url}

Article content: {article_content[:1000]}...

Requirements:
- Tone: {tone}
- Industry context: {industry or 'general'}
- Length: 2-4 sentences
- Include emojis for engagement
- Make it professional yet engaging
- End with a question to encourage interaction
- Include 3-5 relevant hashtags
- Mention it's a summary of an article

Generate the post:"""

            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=self.headers,
                json={
                    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                    "messages": [
                        {"role": "system", "content": "You are a professional LinkedIn content creator. Create engaging, authentic posts that drive engagement and provide value to the audience."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 400,
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return self._get_fallback_post(f"article from {url}", industry, tone)
                
        except Exception as e:
            print(f"❌ Error generating from article: {e}")
            return self._get_fallback_post(f"article from {url}", industry, tone)

    def _extract_article_content(self, url):
        """Simple article content extraction"""
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            # Simple text extraction - remove HTML tags
            content = re.sub(r'<[^>]+>', '', response.text)
            content = re.sub(r'\s+', ' ', content).strip()
            
            return content[:2000]  # Limit content length
        except:
            return "Article content could not be extracted."

    def _get_fallback_post(self, topic, industry, tone):
        """Fallback post if AI fails"""
        fallback_posts = [
            f"🚀 Excited to share insights about {topic} in the {industry} space! The journey of continuous learning and growth never stops. What's your experience with this?\n\n#{industry.replace(' ', '')} #{topic.replace(' ', '')} #ProfessionalGrowth #Innovation",
            f"💡 Just completed an amazing {topic} project! The {industry} industry is evolving rapidly, and staying ahead requires constant innovation. How do you stay updated?\n\n#{industry.replace(' ', '')} #{topic.replace(' ', '')} #ProfessionalGrowth #Innovation",
            f"🎯 Another milestone achieved in {topic}! The {industry} landscape is full of opportunities for those willing to adapt and grow. What challenges are you facing?\n\n#{industry.replace(' ', '')} #{topic.replace(' ', '')} #ProfessionalGrowth #Innovation"
        ]
        return random.choice(fallback_posts)

# Initialize AI Generator
ai_generator = AIGenerator(OPENROUTER_API_KEY)

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

@app.route('/api/generate-post', methods=['POST'])
def generate_post():
    """API endpoint to generate LinkedIn posts"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        post_type = data.get('type', 'topic')
        industry = data.get('industry', 'technology')
        tone = data.get('tone', 'professional')
        
        if post_type == 'article':
            url = data.get('url')
            if not url:
                return jsonify({'error': 'URL is required for article type'}), 400
            
            post = ai_generator.generate_post_from_article(url, industry, tone)
        else:
            topic = data.get('topic')
            if not topic:
                return jsonify({'error': 'Topic is required for topic type'}), 400
            
            post = ai_generator.generate_linkedin_post(topic, industry, tone)
        
        return jsonify({'post': post})
        
    except Exception as e:
        print(f"Error generating post: {e}")
        return jsonify({'error': 'Failed to generate post'}), 500

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'message': 'LinkedIn AI Post Generator is running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 