#!/usr/bin/env python3
"""
Test script to verify quality improvements in AI content generation
"""

import requests
import json
import time

def test_ai_quality():
    """Test the AI content generation quality"""
    
    print("🧪 Testing AI Content Quality Improvements...")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "topic": "artificial intelligence in healthcare",
            "industry": "healthcare",
            "tone": "professional",
            "word_count": 300
        },
        {
            "topic": "https://techcrunch.com/2024/01/15/ai-startup-funding/",
            "industry": "technology",
            "tone": "enthusiastic", 
            "word_count": 250
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Topic: {test_case['topic']}")
        print(f"Industry: {test_case['industry']}")
        print(f"Tone: {test_case['tone']}")
        print(f"Word Count: {test_case['word_count']}")
        print("-" * 30)
        
        try:
            start_time = time.time()
            
            response = requests.post(
                'http://localhost:5000/generate',
                headers={'Content-Type': 'application/json'},
                json=test_case,
                timeout=120  # 2 minutes timeout for quality content
            )
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                post = data.get('post', '')
                
                print(f"✅ Success! Generated in {generation_time:.2f} seconds")
                print(f"📊 Word Count: {len(post.split())}")
                print(f"📄 Content Preview:")
                print(post[:200] + "..." if len(post) > 200 else post)
                
                # Quality checks
                quality_score = 0
                checks = []
                
                # Check for emojis
                if any(emoji in post for emoji in ['🚀', '💡', '📈', '🎯', '🔥', '✨', '📊', '🔍']):
                    quality_score += 1
                    checks.append("✅ Contains relevant emojis")
                else:
                    checks.append("❌ Missing emojis")
                
                # Check for hashtags
                if '#' in post:
                    quality_score += 1
                    checks.append("✅ Contains hashtags")
                else:
                    checks.append("❌ Missing hashtags")
                
                # Check for engaging question
                if any(q in post.lower() for q in ['what', 'how', 'why', 'when', 'where', '?']):
                    quality_score += 1
                    checks.append("✅ Contains engaging question")
                else:
                    checks.append("❌ Missing engaging question")
                
                # Check word count accuracy
                actual_words = len(post.split())
                target_words = test_case['word_count']
                if abs(actual_words - target_words) <= 20:  # Allow 20 word tolerance
                    quality_score += 1
                    checks.append(f"✅ Word count accurate ({actual_words}/{target_words})")
                else:
                    checks.append(f"❌ Word count off ({actual_words}/{target_words})")
                
                # Check for specific content (not generic)
                specific_indicators = ['specific', 'particular', 'according', 'reported', 'found', 'shows', 'reveals']
                if any(indicator in post.lower() for indicator in specific_indicators):
                    quality_score += 1
                    checks.append("✅ Contains specific content")
                else:
                    checks.append("❌ Content seems generic")
                
                print(f"\n📊 Quality Score: {quality_score}/5")
                for check in checks:
                    print(f"  {check}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout - AI is taking longer for quality content")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n" + "=" * 50)
        time.sleep(2)  # Brief pause between tests

if __name__ == "__main__":
    test_ai_quality() 