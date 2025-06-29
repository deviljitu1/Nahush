# Setup Guide - LinkedIn AI Post Generator

## 🔑 Step 1: Get Your API Key

1. **Go to OpenRouter.ai**
   - Visit: https://openrouter.ai
   - Click "Sign Up" or "Get Started"

2. **Create Account**
   - Sign up with email or GitHub
   - Verify your email

3. **Get Your API Key**
   - Go to your dashboard
   - Copy your API key (starts with `sk-or-v1-`)
   - Keep it safe - you'll need it!

## 🚀 Step 2: Start the Server

### Option A: Automatic Setup (Recommended)
1. **Double-click** `start_server.bat`
2. **Enter your API key** when prompted
3. **Wait for server to start**
4. **Open browser** to `http://localhost:8000`

### Option B: Manual Setup
1. **Open PowerShell** in this folder
2. **Set your API key:**
   ```powershell
   $env:OPEN_ROUTER = "your-actual-api-key-here"
   ```
3. **Start the server:**
   ```powershell
   python server.py
   ```

## ✅ Step 3: Test It Works

1. **Open browser** to `http://localhost:8000`
2. **Enter a topic** like "web development project"
3. **Choose industry** and **tone**
4. **Click "Generate Post"**
5. **You should see a LinkedIn post!**

## 🔧 Troubleshooting

### "No auth credentials found" Error
- Make sure you entered your real API key
- Check that it starts with `sk-or-v1-`
- Try restarting the server

### "Port already in use" Error
- Close other applications using port 8000
- Or restart your computer

### "Python not found" Error
- Install Python 3.7 or higher
- Make sure Python is in your PATH

## 📱 Using the App

### Generate from Topic
- Enter: "client success story"
- Industry: Business
- Tone: Professional
- Click "Generate Post"

### Generate from Article
- Paste: `https://techcrunch.com/2024/01/15/ai-trends`
- Industry: Technology
- Tone: Educational
- Click "Generate Post"

## 🎯 Next Steps

- **Copy posts** to clipboard
- **Open LinkedIn** to post them
- **Share with others** who need help
- **Deploy to GitHub** for public access

---

**Need help?** Check the main README.md or create an issue on GitHub. 