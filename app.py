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

    def generate_linkedin_post(self, topic=None, industry=None, tone="professional", word_count=200):
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
- Word Count: {word_count} words

Requirements:
- Make the content SPECIFIC to "{topic}" - don't be generic
- Length: Approximately {word_count} words
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
                    "max_tokens": word_count,
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

    def generate_post_from_article(self, url, industry=None, tone="professional", word_count=200):
        """Generate LinkedIn post from article URL"""
        try:
            # Extract domain name for cleaner references
            try:
                from urllib.parse import urlparse
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.replace('www.', '')
                source_name = domain.split('.')[0].title()  # Get first part of domain
            except:
                domain = "the article"
                source_name = "the source"
            
            # Extract content from URL using a simple approach
            # In production, you might want to use a more robust article extraction service
            article_content = self._extract_article_content(url)
            
            prompt = f"""Create a LinkedIn post that SUMMARIZES this specific news article from {source_name}.

Article content: {article_content[:2000]}...

Context:
- Industry: {industry or 'general'}
- Tone: {tone}
- Source: {source_name}
- Word Count: EXACTLY {word_count} words (not more, not less)

Requirements:
- Create an ACTUAL SUMMARY of the article's main news points and key facts
- Focus on the specific news content, facts, and important details from the article
- Length: EXACTLY {word_count} words - count carefully
- Include relevant emojis for visual appeal
- Make it professional yet engaging
- End with an engaging question related to the article's specific topic
- Include 5-7 relevant hashtags specific to the article's subject matter
- Reference specific details, numbers, or quotes from the article when possible
- Make it clear this is a summary of the article's content
- Don't be generic - focus on what the article actually says
- Extract and highlight ONLY the most important news points from the article
- Use the exact word count specified: {word_count} words

Structure:
1. Hook about the article's main news finding or key point
2. Summary of the article's most important details and facts
3. Why this matters to your audience
4. Engaging question about the article's topic
5. Relevant hashtags

Example format for news articles:
"📰 [Article Title] from {source_name} reveals [key news finding]. The article reports [specific details from article]. This matters because [why it's important]. What's your take on [specific aspect from article]?

#[relevant hashtags]"

Generate a LinkedIn post that actually summarizes this news article in EXACTLY {word_count} words:"""

            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=self.headers,
                json={
                    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                    "messages": [
                        {"role": "system", "content": f"You are a professional LinkedIn content creator specializing in {industry or 'general'} content. Your job is to create ACTUAL SUMMARIES of news articles that include specific details, facts, and insights from the article content. Focus on what the article actually says, not generic commentary. Always include specific information from the article in your summaries. CRITICAL: You must generate EXACTLY the number of words specified by the user - count carefully and do not exceed or fall short of the target word count."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": word_count,
                    "temperature": 0.8
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return self._get_fallback_post(f"article from {source_name}", industry, tone)
                
        except Exception as e:
            print(f"❌ Error generating from article: {e}")
            return self._get_fallback_post(f"article from {source_name}", industry, tone)

    def _extract_article_content(self, url):
        """Enhanced article content extraction using BeautifulSoup"""
        try:
            # Try to import BeautifulSoup, fallback to simple extraction if it fails
            try:
                from bs4 import BeautifulSoup
                use_beautifulsoup = True
            except ImportError:
                use_beautifulsoup = False
                print("BeautifulSoup not available, using simple text extraction")
            
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
            
            if use_beautifulsoup:
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                    script.decompose()
                
                # Extract title first
                title = ""
                title_selectors = ['h1', '.title', '.headline', '[class*="title"]', 'title']
                for selector in title_selectors:
                    title_elem = soup.select_one(selector)
                    if title_elem:
                        title = title_elem.get_text().strip()
                        if title and len(title) > 10:
                            break
                
                # Try to find main content using news-specific selectors
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
                    '.news-content',
                    '.story-content',
                    'main',
                    '.main-content',
                    '#content',
                    '.content',
                    '.text-content'
                ]
                
                content = ""
                
                # Try to find main content
                for selector in content_selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text(separator=' ', strip=True)
                        if len(text) > 300:  # Only consider substantial content
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
            else:
                # Fallback to simple text extraction
                content = re.sub(r'<[^>]+>', '', response.text)
                title = ""
            
            # Clean up the content
            if content:
                # Remove extra whitespace
                content = re.sub(r'\s+', ' ', content)
                # Remove common unwanted text
                content = re.sub(r'(cookie|privacy|terms|subscribe|newsletter|advertisement|ads|sign in|sign up|login|register)', '', content, flags=re.IGNORECASE)
                
                # Extract important news sentences (those with key words or numbers)
                sentences = content.split('.')
                important_sentences = []
                
                # Keywords that indicate important news content
                news_keywords = [
                    # Action words
                    'announced', 'launched', 'released', 'introduced', 'developed', 'created',
                    'reported', 'found', 'discovered', 'revealed', 'showed', 'indicated',
                    'arrested', 'charged', 'accused', 'investigated', 'probed', 'questioned',
                    'filed', 'submitted', 'complained', 'alleged', 'claimed', 'stated',
                    
                    # Numbers and data
                    'million', 'billion', 'percent', '%', 'dollars', '$', 'users', 'customers',
                    'people', 'students', 'victims', 'suspects', 'accused', 'witnesses',
                    
                    # News-specific terms
                    'police', 'investigation', 'case', 'incident', 'crime', 'victim',
                    'survivor', 'accused', 'suspect', 'arrest', 'charge', 'trial',
                    'court', 'judge', 'lawyer', 'advocate', 'prosecution', 'defense',
                    'evidence', 'witness', 'testimony', 'statement', 'complaint',
                    
                    # Location and time
                    'kolkata', 'delhi', 'mumbai', 'bangalore', 'chennai', 'hyderabad',
                    'india', 'state', 'city', 'district', 'area', 'location',
                    'yesterday', 'today', 'morning', 'evening', 'night', 'week',
                    'month', 'year', 'date', 'time', 'period',
                    
                    # Educational/Institutional terms
                    'college', 'university', 'school', 'institution', 'authority',
                    'administration', 'faculty', 'staff', 'student', 'teacher',
                    'principal', 'director', 'head', 'official', 'committee',
                    
                    # General important terms
                    'technology', 'innovation', 'startup', 'company', 'business', 'market',
                    'research', 'study', 'survey', 'analysis', 'data', 'results', 'findings'
                ]
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 25:  # Only consider substantial sentences
                        # Check if sentence contains important keywords or numbers
                        has_keywords = any(keyword.lower() in sentence.lower() for keyword in news_keywords)
                        has_numbers = bool(re.search(r'\d+', sentence))
                        has_quotes = '"' in sentence or "'" in sentence  # Quotes often contain important info
                        
                        if has_keywords or has_numbers or has_quotes:
                            important_sentences.append(sentence)
                
                # If we found important sentences, use them; otherwise use the original content
                if important_sentences:
                    content = '. '.join(important_sentences[:15])  # Limit to 15 most important sentences
                else:
                    # Fallback: use first few sentences that seem substantial
                    content = '. '.join([s.strip() for s in sentences[:10] if len(s.strip()) > 30])
                
                # Limit length
                content = content[:4000]  # Increased limit for better content
                
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
        
        # Extract domain name if topic contains a URL
        if topic_clean.startswith('http'):
            try:
                from urllib.parse import urlparse
                parsed_url = urlparse(topic_clean)
                domain = parsed_url.netloc.replace('www.', '')
                topic_clean = f"article from {domain}"
            except:
                topic_clean = "this article"
        
        fallback_posts = [
            f"📰 Interesting article from {topic_clean}! The piece covers important developments in {industry_clean} that could impact how we approach our work. What specific insights from this article resonate with your experience?\n\n#{industry_clean.replace(' ', '')} #{topic_clean.replace(' ', '').replace('articlefrom', '')} #ProfessionalGrowth #Innovation #DigitalMarketing",
            
            f"🔍 Just read a compelling piece from {topic_clean} about {industry_clean} trends. The article highlights key points that professionals in our field should consider. Which aspects of this coverage stand out to you?\n\n#{industry_clean.replace(' ', '')} #{topic_clean.replace(' ', '').replace('articlefrom', '')} #ProfessionalGrowth #Innovation #DigitalMarketing",
            
            f"📊 {topic_clean} published an insightful article on {industry_clean} developments. The coverage provides valuable perspectives that could influence our industry approach. What's your reaction to the main points discussed?\n\n#{industry_clean.replace(' ', '')} #{topic_clean.replace(' ', '').replace('articlefrom', '')} #ProfessionalGrowth #Innovation #DigitalMarketing",
            
            f"💡 Worthwhile read from {topic_clean} on {industry_clean} topics. The article presents important information that professionals should be aware of. How do you see these insights applying to your work?\n\n#{industry_clean.replace(' ', '')} #{topic_clean.replace(' ', '').replace('articlefrom', '')} #ProfessionalGrowth #Innovation #DigitalMarketing"
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
        word_count = int(data.get('wordCount', 200))  # Default to 200 words
        
        # Validate word count
        if word_count < 50 or word_count > 1000:
            return jsonify({'error': 'Word count must be between 50 and 1000'}), 400
        
        if post_type == 'article':
            url = data.get('url')
            if not url:
                return jsonify({'error': 'URL is required for article type'}), 400
            
            post = ai_generator.generate_post_from_article(url, industry, tone, word_count)
        else:
            topic = data.get('topic')
            if not topic:
                return jsonify({'error': 'Topic is required for topic type'}), 400
            
            post = ai_generator.generate_linkedin_post(topic, industry, tone, word_count)
        
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