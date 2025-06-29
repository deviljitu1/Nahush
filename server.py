#!/usr/bin/env python3
"""
Simple HTTP server for LinkedIn AI Post Generator
Run this script to serve the web interface locally
"""

import http.server
import socketserver
import webbrowser
import os
import json
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import urllib.request
from bs4 import BeautifulSoup

# Configuration
PORT = 8000
DIRECTORY = Path(__file__).parent

# Get API key from environment variable
OPENROUTER_API_KEY = os.getenv('OPEN_ROUTER')
if not OPENROUTER_API_KEY:
    print("⚠️  Warning: OPEN_ROUTER environment variable not set!")
    print("Please set your OpenRouter API key as an environment variable:")
    print("set OPEN_ROUTER=your-api-key-here")
    OPENROUTER_API_KEY = "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"  # Fallback

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for web API calls
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/generate-post':
            self.handle_generate_post()
        else:
            self.send_error(404, "API endpoint not found")
    
    def handle_generate_post(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Generate post based on type
            if data.get('type') == 'article':
                post = self.generate_post_from_article(data['url'], data['industry'], data['tone'])
            else:
                post = self.generate_post_from_topic(data['topic'], data['industry'], data['tone'])
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'post': post}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Error generating post: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def generate_post_from_topic(self, topic, industry, tone):
        """Generate LinkedIn post from topic using OpenRouter API"""
        prompt = self.create_topic_prompt(topic, industry, tone)
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://openrouter.ai/'
            },
            json={
                'model': 'mistralai/mistral-small-3.2-24b-instruct:free',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a professional LinkedIn content creator. Create engaging, authentic posts that drive engagement and provide value to the audience.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 300,
                'temperature': 0.7
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenRouter API error: {response.text}")
        
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    
    def generate_post_from_article(self, url, industry, tone):
        """Generate LinkedIn post from article URL"""
        try:
            # Extract article content
            article_data = self.extract_article_content(url)
            
            # Create prompt for article summarization
            prompt = self.create_article_prompt(article_data, industry, tone)
            
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://openrouter.ai/'
                },
                json={
                    'model': 'mistralai/mistral-small-3.2-24b-instruct:free',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a professional LinkedIn content creator. Create engaging posts that summarize articles and drive engagement.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'max_tokens': 400,
                    'temperature': 0.7
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenRouter API error: {response.text}")
            
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            print(f"Error generating post from article: {e}")
            raise e
    
    def extract_article_content(self, url):
        """Extract content from article URL"""
        try:
            # Use a CORS proxy to fetch the article content
            proxy_url = f"https://api.allorigins.win/get?url={urllib.parse.quote(url)}"
            response = requests.get(proxy_url)
            data = response.json()
            
            if data.get('contents'):
                # Parse the HTML content
                soup = BeautifulSoup(data['contents'], 'html.parser')
                
                # Extract text content from common article selectors
                selectors = [
                    'article',
                    '[class*="content"]',
                    '[class*="article"]',
                    '[class*="post"]',
                    '.post-content',
                    '.article-content',
                    '.entry-content',
                    'main',
                    '.main-content'
                ]
                
                content = ''
                for selector in selectors:
                    element = soup.select_one(selector)
                    if element:
                        content = element.get_text().strip()
                        if len(content) > 100:
                            break
                
                # If no specific content found, get body text
                if not content or len(content) < 100:
                    content = soup.body.get_text().strip() if soup.body else ''
                
                # Clean up the content
                content = ' '.join(content.split())[:2000]
                
                return {
                    'title': soup.title.string if soup.title else 'Article',
                    'content': content,
                    'url': url
                }
            
            raise Exception('Could not extract content from URL')
            
        except Exception as e:
            print(f"Error extracting article content: {e}")
            raise Exception('Failed to extract article content. Please check the URL and try again.')
    
    def create_topic_prompt(self, topic, industry, tone):
        """Create prompt for topic-based post generation"""
        default_topic = topic or 'latest project completion'
        default_industry = industry or 'technology and digital marketing'
        
        return f"""Create a compelling LinkedIn post about {default_topic} in the {default_industry} industry.

Requirements:
- Tone: {tone}
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

Generate the post:"""
    
    def create_article_prompt(self, article_data, industry, tone):
        """Create prompt for article summarization"""
        return f"""Create a compelling LinkedIn post that summarizes this article:

Article Title: {article_data['title']}
Article URL: {article_data['url']}
Article Content: {article_data['content'][:1500]}...

Requirements:
- Tone: {tone}
- Industry Context: {industry}
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

Generate the LinkedIn post:"""

def main():
    """Start the HTTP server and open the browser"""
    
    # Change to the directory containing this script
    os.chdir(DIRECTORY)
    
    # Create server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 LinkedIn AI Post Generator Server")
        print(f"📁 Serving files from: {DIRECTORY}")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print(f"📱 Open your browser and go to: http://localhost:{PORT}")
        print(f"⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        if OPENROUTER_API_KEY:
            print("✅ OpenRouter API key configured")
        else:
            print("⚠️  OpenRouter API key not found in environment variables")
        
        # Open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("✅ Browser opened automatically!")
        except:
            print("⚠️  Could not open browser automatically. Please open it manually.")
        
        print("\n🎯 Features:")
        print("• Generate LinkedIn posts with AI")
        print("• Article URL summarization")
        print("• Choose topic, industry, and tone")
        print("• Copy posts to clipboard")
        print("• Direct link to LinkedIn")
        print("• Mobile-friendly design")
        print("• Secure API key handling")
        print("-" * 50)
        
        try:
            # Start serving
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 