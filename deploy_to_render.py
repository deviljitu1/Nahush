#!/usr/bin/env python3
"""
Deployment Helper Script for LinkedIn AI Post Generator
This script helps validate your setup before deploying to Render
"""

import os
import sys
import requests
import json

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'index.html', 
        'style.css',
        'script.js',
        'requirements.txt',
        'render.yaml'
    ]
    
    print("🔍 Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found!")
    return True

def check_api_key():
    """Test the OpenRouter API key"""
    api_key = os.environ.get('OPENROUTER_API_KEY', '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')
    
    print(f"\n🔑 Testing OpenRouter API key...")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://openrouter.ai/"
            },
            json={
                "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "max_tokens": 10
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API key is working!")
            return True
        else:
            print(f"❌ API key test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

def check_flask_app():
    """Test if Flask app can start"""
    print(f"\n🐍 Testing Flask app...")
    
    try:
        # Import the app
        from app import app
        
        # Test the health endpoint
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Flask app is working!")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def generate_deployment_instructions():
    """Generate deployment instructions"""
    print(f"\n📋 DEPLOYMENT INSTRUCTIONS")
    print("=" * 50)
    
    print("""
1. Push your code to GitHub:
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main

2. Deploy to Render:
   - Go to https://dashboard.render.com/
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Click "Apply"

3. Your app will be available at:
   https://your-app-name.onrender.com

4. Share the URL with anyone who wants to use your AI post generator!
""")

def main():
    print("🚀 LinkedIn AI Post Generator - Deployment Checker")
    print("=" * 60)
    
    # Check files
    files_ok = check_files()
    
    # Check API key
    api_ok = check_api_key()
    
    # Check Flask app
    flask_ok = check_flask_app()
    
    print(f"\n📊 SUMMARY")
    print("=" * 30)
    print(f"Files: {'✅' if files_ok else '❌'}")
    print(f"API Key: {'✅' if api_ok else '❌'}")
    print(f"Flask App: {'✅' if flask_ok else '❌'}")
    
    if files_ok and api_ok and flask_ok:
        print(f"\n🎉 Everything is ready for deployment!")
        generate_deployment_instructions()
    else:
        print(f"\n❌ Please fix the issues above before deploying.")
        if not files_ok:
            print("- Make sure all required files are present")
        if not api_ok:
            print("- Check your OpenRouter API key")
        if not flask_ok:
            print("- Check your Flask app configuration")

if __name__ == "__main__":
    main() 