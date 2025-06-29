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

Article content: {article_content[:1500]}...

Context:
- Industry: {industry or 'general'}
- Tone: {tone}
- Source: Article from {url}

Requirements:
- Create a UNIQUE summary specific to this article's actual content
- Focus on the main points and key insights from the article
- Length: 3-5 sentences (150-250 words)
- Include relevant emojis for visual appeal
- Make it professional yet engaging
- End with an engaging question related to the article's topic
- Include 5-7 relevant hashtags specific to the article's subject matter
- Add your perspective or insights about the article's implications
- Make it shareable and thought-provoking
- Include a call-to-action
- If the article has a clear title, reference it naturally
- Don't be generic - make it specific to what the article actually says

Structure:
1. Hook about the article's key insight or main point
2. Your take on the article's most important findings/points
3. Why this matters to your audience and industry
4. Engaging question for discussion
5. Relevant hashtags

Generate a unique LinkedIn post based on the actual article content:"""

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
        """Enhanced article content extraction using BeautifulSoup"""
        try:
            # Set up headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try to find the main content using common selectors
            content_selectors = [
                'article',
                '[class*="content"]',
                '[class*="article"]',
                '[class*="post"]',
                '[class*="entry"]',
                '.post-content',
                '.article-content',
                '.entry-content',
                '.content-body',
                '.story-body',
                '.article-body',
                'main',
                '.main-content',
                '#content',
                '.content',
                '.text-content'
            ]
            
            content = ""
            title = ""
            
            # Extract title
            title_selectors = ['h1', '.title', '.headline', '[class*="title"]', 'title']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text().strip()
                    if title and len(title) > 10:
                        break
            
            # Try to find main content
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(separator=' ', strip=True)
                    if len(text) > 200:  # Only consider substantial content
                        content = text
                        break
                if content:
                    break
            
            # If no specific content found, try to get body text
            if not content:
                body = soup.find('body')
                if body:
                    # Remove navigation, ads, and other non-content elements
                    for elem in body.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style']):
                        elem.decompose()
                    content = body.get_text(separator=' ', strip=True)
            
            # Clean up the content
            if content:
                # Remove extra whitespace
                content = re.sub(r'\s+', ' ', content)
                # Remove common unwanted text
                content = re.sub(r'(cookie|privacy|terms|subscribe|newsletter|advertisement|ads)', '', content, flags=re.IGNORECASE)
                # Limit length
                content = content[:3000]
                
                # Combine title and content
                if title:
                    full_content = f"Title: {title}\n\nContent: {content}"
                else:
                    full_content = content
                
                return full_content
            else:
                return f"Article content could not be extracted from {url}. Please check the URL and try again."
                
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return f"Unable to extract content from {url}. Error: {str(e)}"

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