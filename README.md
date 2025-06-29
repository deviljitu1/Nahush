# LinkedIn AI Post Generator

🚀 **Create engaging LinkedIn posts with AI-powered content generation**

A modern web application that generates professional LinkedIn posts using AI. Features include topic-based content generation, article summarization, and a beautiful responsive interface.

## 🚀 Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy/schema-new?schema=https://raw.githubusercontent.com/YOUR_USERNAME/linkedin-ai-post-generator/main/render.yaml)

**Click the button above to deploy instantly to Render (100% free!)**

## ✨ Features

- 🤖 **AI-Powered Content**: Uses OpenRouter AI to generate engaging posts
- 📰 **Article Summarizer**: Paste any article URL for instant LinkedIn summaries
- 🎨 **Customizable**: Choose industry, tone, and topic
- 📱 **Mobile Ready**: Responsive design works on all devices
- ⚡ **Fast & Secure**: Backend API handling with environment variable security
- 🎯 **LinkedIn Optimized**: Content tailored for maximum engagement

## 🚀 Quick Start

### Option 1: Free Cloud Deployment (Recommended)

1. **Click the "Deploy to Render" button above**
2. **Sign up with GitHub** (free)
3. **Set your OpenRouter API key** in environment variables
4. **Your app is live in 5 minutes!**

### Option 2: Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/linkedin-ai-post-generator.git
   cd linkedin-ai-post-generator
   ```

2. **Get your API key**
   - Visit [OpenRouter.ai](https://openrouter.ai)
   - Sign up for a free account
   - Copy your API key

3. **Set up environment**
   ```bash
   # Windows
   set OPEN_ROUTER=your-api-key-here
   
   # macOS/Linux
   export OPEN_ROUTER=your-api-key-here
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the server**
   ```bash
   python server.py
   ```

6. **Open in browser**
   - Visit: `http://localhost:8000`
   - Start generating posts!

## 📁 Project Structure

```
linkedin-ai-post-generator/
├── server.py              # Python backend server
├── index.html             # Main application (local)
├── index-github.html      # GitHub Pages version
├── script.js              # Frontend JavaScript (local)
├── script-github.js       # Frontend JavaScript (GitHub)
├── style.css              # Stylesheet
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment config
├── railway.json           # Railway deployment config
├── vercel.json            # Vercel deployment config
├── run_linkedin_automation.bat  # Windows startup script
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

- `OPEN_ROUTER`: Your OpenRouter API key (required)

### API Configuration

The application automatically detects if it's running locally or on cloud platforms:

- **Local**: Uses backend server on port 8000
- **Render/Railway/Vercel**: Uses environment variables for configuration

## 🎯 Usage

### Generating Posts

1. **Enter a topic** or **paste an article URL**
2. **Select your industry** (Technology, Marketing, Business, etc.)
3. **Choose your tone** (Professional, Casual, Enthusiastic, Educational)
4. **Click "Generate Post"**
5. **Copy to clipboard** and paste on LinkedIn

### Article Summarization

- Paste any article URL in the topic field
- The AI will automatically:
  - Extract the article content
  - Summarize key points
  - Create a LinkedIn-optimized post

## 🛠️ Development

### Running Locally

```bash
# Start the development server
python server.py

# The server runs on http://localhost:8000
```

### File Descriptions

- `server.py`: Python HTTP server with API endpoints
- `index.html`: Main application interface
- `script.js`: Frontend logic and API calls
- `style.css`: Responsive styling and animations

### API Endpoints

- `POST /api/generate-post`: Generate LinkedIn post from topic
- `POST /api/generate-post`: Generate LinkedIn post from article URL
- `GET /`: Serve the main application

## 🌐 Deployment Options

### 🆓 Free Options ($0/month)

| Platform | Always Online | Setup Time | Best For |
|----------|---------------|------------|----------|
| **Render** | Sleeps after 15min | 5 min | **Personal projects** |
| Vercel | ✅ Always online | 10 min | High traffic |
| Netlify | ✅ Always online | 8 min | Simple APIs |

### Render (Recommended Free Option)

1. **Click "Deploy to Render" button above**
2. **Or follow manual steps:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Connect your repository
   - Set environment variables
   - Deploy!

### GitHub Pages (Demo Only)

1. **Upload files** to your GitHub repository
2. **Enable GitHub Pages** in repository settings
3. **Set source** to main branch
4. **Your site** will be available at `https://username.github.io/repository-name`

## 🔒 Security

- API keys are stored as environment variables
- No sensitive data in frontend code
- CORS protection on API endpoints
- Input validation and sanitization

## 📱 Browser Support

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenRouter AI](https://openrouter.ai) for AI capabilities
- [Font Awesome](https://fontawesome.com) for icons
- [Google Fonts](https://fonts.google.com) for typography

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/linkedin-ai-post-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/linkedin-ai-post-generator/discussions)
- **Email**: your-email@example.com

## 🔄 Updates

### Version 1.0.0
- Initial release
- AI content generation
- Article summarization
- Responsive design
- Free cloud deployment options

---

**Made with ❤️ for the LinkedIn community** 