# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Get Your API Key
1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Copy your API key (starts with `sk-or-v1-`)

### Step 2: Start the Server

**Option A: Using PowerShell (Recommended)**
```powershell
# Right-click on start_server.ps1 and select "Run with PowerShell"
# Or run in PowerShell:
.\start_server.ps1
```

**Option B: Using Command Prompt**
```cmd
# Double-click start_server.bat
# Or run in Command Prompt:
start_server.bat
```

**Option C: Manual Setup**
```powershell
# Set your API key
$env:OPEN_ROUTER = "your-api-key-here"

# Start the server
python server.py
```

### Step 3: Use the Application
1. Open your browser
2. Go to: `http://localhost:8000`
3. Start generating LinkedIn posts!

## 🔧 Troubleshooting

### "API Key Not Found" Error
- Make sure you set the environment variable correctly
- Use the startup scripts for automatic setup
- Check that your API key starts with `sk-or-v1-`

### "Port Already in Use" Error
- Close any other running servers
- Or use a different port by editing `server.py`

### "Python Not Found" Error
- Install Python 3.7 or higher
- Make sure Python is in your PATH

## 📱 Features

- ✅ **AI Content Generation** - Create posts from topics
- ✅ **Article Summarization** - Paste URLs for instant posts
- ✅ **Customizable** - Choose industry and tone
- ✅ **Mobile Ready** - Works on all devices
- ✅ **Secure** - API key stays on your computer

## 🎯 Example Usage

1. **Topic-based post:**
   - Enter: "web development project completion"
   - Industry: Technology
   - Tone: Professional
   - Click "Generate Post"

2. **Article summary:**
   - Paste: `https://techcrunch.com/2024/01/15/ai-trends`
   - Industry: Technology
   - Tone: Educational
   - Click "Generate Post"

## 🔗 Useful Links

- [OpenRouter AI](https://openrouter.ai) - Get your API key
- [GitHub Repository](https://github.com/yourusername/linkedin-ai-post-generator) - Source code
- [Live Demo](https://yourusername.github.io/linkedin-ai-post-generator) - GitHub Pages version

---

**Need help?** Check the main README.md for detailed instructions. 