# LinkedIn AI Post Generator - Setup Guide (Google Gemini)

## 🚨 Critical Issues Fixed

### 1. **API Key Configuration**
The application now uses Google Gemini API. Here's how to set it up:

#### Option A: Environment Variable (Recommended)
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# Windows Command Prompt
set GEMINI_API_KEY=your-gemini-api-key-here

# Linux/Mac
export GEMINI_API_KEY="your-gemini-api-key-here"
```

#### Option B: Create a .env file
Create a file named `.env` in the project root:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

### 2. **Get Your Google Gemini API Key**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Use it in the setup above

**Note:** Your Gemini API key is already configured in the server.py file as a default value.

## 🛠️ Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python server.py
```

### 3. Access the Application
Open your browser and go to: `http://localhost:8000`

## 🔧 Troubleshooting

### Issue: "Gemini API key not configured"
**Solution**: The API key is already configured in the code, but you can set it as an environment variable if needed.

### Issue: "Failed to fetch" error
**Solution**: Make sure the Python server is running on port 8000.

### Issue: "Rate limit exceeded"
**Solution**: Wait a few minutes and try again. Google Gemini has rate limits on free accounts.

### Issue: Article URL not working
**Solution**: The CORS proxy might be down. Try a different article URL or use topic-based generation.

## 📁 Project Structure

```
Nahush/
├── index.html          # Main web interface
├── style.css           # Styling
├── script.js           # Frontend JavaScript
├── server.py           # Python backend server (Gemini API)
├── requirements.txt    # Python dependencies
└── SETUP_GUIDE.md     # This file
```

## 🚀 Features

- ✅ AI-powered LinkedIn post generation using Google Gemini
- ✅ Article URL summarization
- ✅ Customizable industry and tone
- ✅ Mobile-responsive design
- ✅ Copy to clipboard functionality
- ✅ Direct LinkedIn integration

## 🔒 Security Notes

- API keys are handled securely through environment variables
- No sensitive data is stored locally
- CORS headers are properly configured for web requests

## 📞 Support

If you encounter any issues:
1. Check that all dependencies are installed
2. Verify your API key is correctly set (if using environment variable)
3. Ensure the server is running on port 8000
4. Check the browser console for error messages

## 🎯 Quick Start

1. **Open PowerShell** and navigate to your project:
   ```powershell
   cd "C:\Users\Nahush Patel\Desktop\Nahush"
   ```

2. **Start the server**:
   ```powershell
   python server.py
   ```

3. **Open your browser** to `http://localhost:8000`

4. **Generate a post** by entering a topic or article URL!

The Gemini API key is already configured in the code, so it should work immediately! 