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

        prompt = f"""Create a unique, engaging LinkedIn post about: {topic}

Context:
- Industry: {industry}
- Tone: {tone}
- Topic: {topic}

Requirements:
- Make the content SPECIFIC to "{topic}" - don't be generic
- Length: 3-5 sentences (150-250 words)
- Include relevant emojis for visual appeal
- Make it professional yet conversational
- End with an engaging question related to {topic}
- Include 5-7 relevant hashtags specific to {topic}
- Add value and insights about {topic}
- Make it shareable and thought-provoking
- Include a call-to-action

Structure:
1. Hook/Opening about {topic}
2. Key insights or value about {topic}
3. Personal perspective or industry context
4. Engaging question for audience
5. Relevant hashtags

Generate a unique LinkedIn post:"""

        try:
            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=self.headers,
                json={
                    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                    "messages": [
                        {"role": "system", "content": f"You are a professional LinkedIn content creator specializing in {industry}. Create unique, specific, and engaging posts that provide real value to the audience. Each post should be different and tailored to the exact topic provided."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 400,
                    "temperature": 0.8
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
            
            prompt = f"""Create a unique LinkedIn post summarizing this article: {url}

Article content: {article_content[:1000]}...

Context:
- Industry: {industry or 'general'}
- Tone: {tone}
- Source: Article from {url}

Requirements:
- Create a UNIQUE summary specific to this article's content
- Length: 3-5 sentences (150-250 words)
- Include relevant emojis for visual appeal
- Make it professional yet engaging
- End with an engaging question related to the article
- Include 5-7 relevant hashtags specific to the article topic
- Add your perspective or insights about the article
- Make it shareable and thought-provoking
- Include a call-to-action
- Mention it's based on an article but make it your own take

Structure:
1. Hook about the article's key insight
2. Your take on the article's main points
3. Why this matters to the audience
4. Engaging question for discussion
5. Relevant hashtags

Generate a unique LinkedIn post:"""

            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=self.headers,
                json={
                    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                    "messages": [
                        {"role": "system", "content": f"You are a professional LinkedIn content creator specializing in {industry or 'general'} content. Create unique, specific summaries that add value and perspective to articles. Each summary should be different and tailored to the specific article content."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.8
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
        # Create more specific fallback posts based on the actual topic
        topic_clean = topic.replace('"', '').strip()
        industry_clean = industry.replace('"', '').strip()
        
        fallback_posts = [
            f"🚀 Excited to dive deep into {topic_clean}! The {industry_clean} landscape is evolving rapidly, and understanding {topic_clean} is crucial for staying ahead. What's your biggest challenge with {topic_clean}?\n\n#{industry_clean.replace(' ', '')} #{topic_clean.replace(' ', '')} #ProfessionalGrowth #Innovation #DigitalMarketing",
            
            f"💡 Just explored the fascinating world of {topic_clean} in {industry_clean}! The insights I've gained are game-changing. How has {topic_clean} impacted your professional journey?\n\n#{industry_clean.replace(' ', '')} #{topic_clean.replace(' ', '')} #ProfessionalGrowth #Innovation #DigitalMarketing",
            
            f"🎯 {topic_clean} is revolutionizing how we approach {industry_clean}! The opportunities are endless for those willing to adapt. What's your experience with {topic_clean}?\n\n#{industry_clean.replace(' ', '')} #{topic_clean.replace(' ', '')} #ProfessionalGrowth #Innovation #DigitalMarketing",
            
            f"🔥 The future of {industry_clean} lies in mastering {topic_clean}! It's not just about keeping up—it's about leading the way. How are you leveraging {topic_clean} in your work?\n\n#{industry_clean.replace(' ', '')} #{topic_clean.replace(' ', '')} #ProfessionalGrowth #Innovation #DigitalMarketing"
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