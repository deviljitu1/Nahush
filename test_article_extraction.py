#!/usr/bin/env python3
"""
Test script for article extraction functionality
"""

import requests
from bs4 import BeautifulSoup
import re

def test_article_extraction(url):
    """Test the article extraction function"""
    print(f"Testing article extraction for: {url}")
    print("=" * 60)
    
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
            
            print("✅ SUCCESS: Article content extracted!")
            print(f"Title: {title}")
            print(f"Content length: {len(content)} characters")
            print(f"First 200 characters: {content[:200]}...")
            return full_content
        else:
            print("❌ FAILED: No content found")
            return None
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

if __name__ == "__main__":
    # Test with a sample URL
    test_url = input("Enter a URL to test article extraction: ").strip()
    if test_url:
        result = test_article_extraction(test_url)
        if result:
            print("\n" + "=" * 60)
            print("EXTRACTED CONTENT:")
            print("=" * 60)
            print(result[:500] + "..." if len(result) > 500 else result)
    else:
        print("No URL provided. Exiting.") 