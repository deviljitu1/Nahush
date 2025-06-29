# LinkedIn Automation Tool with AI Content Generation

A Python-based automation tool for posting AI-generated text content to LinkedIn automatically using OpenRouter.ai.

## ⚠️ Important Notes

**LinkedIn API Limitations:**
- LinkedIn's official API has restrictions on posting content
- This tool uses an unofficial LinkedIn API wrapper
- Use at your own risk and in compliance with LinkedIn's Terms of Service
- Avoid posting too frequently to prevent account restrictions

**AI Content Generation:**
- Uses OpenRouter.ai for text generation
- Requires OpenRouter API key
- Generated content should be reviewed before posting
- Respect content guidelines and copyright laws

## 🚀 Features

- ✅ **AI Text Generation** - Generate engaging LinkedIn posts using AI
- ✅ **Manual Posting** - Post your own content with images
- ✅ **Batch AI Posting** - Generate and post multiple AI posts
- ✅ **Customizable Content** - Control topic, industry, and tone
- ✅ **GUI Interface** - User-friendly graphical interface
- ✅ **Command-line Interface** - Script-based automation
- ✅ **Rate Limiting Protection** - Built-in delays to avoid restrictions

## 📋 Prerequisites

- Python 3.7 or higher
- LinkedIn account
- Valid LinkedIn credentials
- OpenRouter API key (for AI content generation)

## 🛠️ Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get OpenRouter API Key:**
   - Sign up at [OpenRouter](https://openrouter.ai)
   - Get your API key from the dashboard
   - Set environment variable: `export OPENROUTER_API_KEY='your-api-key'`

4. **Configure your credentials:**
   - Edit `linkedin_config.json`
   - Replace `your-email@example.com` with your LinkedIn email
   - Replace `your-password` with your LinkedIn password
   - Replace `your-openrouter-api-key` with your OpenRouter API key

## 📖 Usage

### Method 1: GUI Interface (Recommended)

Run the graphical interface for easy AI content generation and posting:

```bash
python linkedin_gui.py
```

**Steps:**
1. Enter your LinkedIn email, password, and OpenRouter API key
2. Click "Login"
3. Use the "🤖 AI Content Generation" tab for AI-powered posts
4. Use the "📝 Manual Post" tab for your own content
5. Configure AI settings (topic, industry, tone)
6. Click "🤖 Generate & Post AI Content"

### Method 2: Command Line Interface

Run the automation script:

```bash
python linkedin_automation.py
```

### Method 3: AI Content Generation Examples

Test AI content generation without posting:

```bash
python ai_example_usage.py
```

### Method 4: Configuration File

Edit `linkedin_config.json` with AI post configurations:

```json
{
    "email": "your-email@example.com",
    "password": "your-password",
    "openrouter_api_key": "your-openrouter-ai-api-key",
    "ai_posts": [
        {
            "topic": "web development project completion",
            "industry": "technology",
            "tone": "professional"
        }
    ],
    "manual_posts": [
        {
            "text": "Your manual post text here",
            "image": "path/to/image.jpg",
            "schedule": null
        }
    ]
}
```

## 🤖 AI Content Generation Features

### Text Generation Options

- **Topic**: What to write about (e.g., "project completion", "industry insights")
- **Industry**: Context (technology, marketing, business, finance, healthcare, education)
- **Tone**: Writing style (professional, casual, enthusiastic, educational)
- **Hashtags**: Automatically included relevant hashtags

### Example AI Prompts

```python
# Professional project post
{
    "topic": "web development project completion",
    "industry": "technology",
    "tone": "professional"
}

# Enthusiastic success story
{
    "topic": "client success story",
    "industry": "business",
    "tone": "enthusiastic"
}

# Educational tip
{
    "topic": "productivity tips for remote work",
    "industry": "technology",
    "tone": "educational"
}
```

## 📁 File Structure

```
linkedin-automation/
├── linkedin_automation.py    # Main automation script with AI
├── linkedin_gui.py          # GUI interface with AI features
├── ai_content_generator.py  # AI content generation module
├── ai_example_usage.py      # AI usage examples
├── linkedin_config.json     # Configuration file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── run_linkedin_automation.bat  # Windows batch script
└── images/                 # Folder for generated images
    ├── ai_generated_*.png
    └── manual_images/
```

## 🔧 Configuration Options

### AI Post Configuration

Each AI post can have:

- **topic**: The main subject to write about (required)
- **industry**: Industry context (technology, marketing, business, etc.)
- **tone**: Writing tone (professional, casual, enthusiastic, educational)

### Manual Post Configuration

Each manual post can have:

- **text**: The post content (required)
- **image**: Path to image file (optional)
- **schedule**: Scheduled time (currently not implemented)

### Image Requirements

- **AI Generated**: Automatically optimized for LinkedIn
- **Manual Images**: JPG, JPEG, PNG, GIF, BMP
- **Recommended size**: 1200x627 pixels
- **Maximum file size**: 5MB

## 🛡️ Security Best Practices

1. **Never commit credentials to version control**
2. **Use environment variables for API keys**
3. **Keep your LinkedIn and OpenRouter credentials secure**
4. **Don't share your configuration file**
5. **Review AI-generated content before posting**

## ⚡ Tips for Best Results

### AI Content Generation

1. **Be Specific**: Use detailed topics and image prompts
2. **Choose Right Tone**: Match your brand voice
3. **Industry Context**: Select relevant industry for better content
4. **Review Content**: Always review AI-generated content before posting

### General Posting

1. **Post Timing**: Post during business hours for better engagement
2. **Content Quality**: AI helps, but human review is essential
3. **Hashtags**: AI includes relevant hashtags automatically
4. **Consistency**: Post regularly but not too frequently
5. **Engagement**: Respond to comments on your posts

## 🚨 Rate Limiting

The tool includes built-in delays to avoid rate limiting:
- 30-second delay between posts
- Maximum 20 posts per hour recommended
- Respect LinkedIn's and OpenRouter's terms of service

## 🔍 Troubleshooting

### Common Issues

1. **AI Generation Failed**
   - Check OpenRouter API key
   - Verify API key has sufficient credits
   - Check internet connection
   - Review API rate limits

2. **Login Failed**
   - Check LinkedIn email and password
   - Ensure 2FA is disabled or use app password
   - Try logging in manually to LinkedIn first

3. **Post Failed**
   - Check your internet connection
   - Verify LinkedIn account is active
   - Wait a few minutes and try again

### Error Messages

- `"AI generator not initialized"`: Missing OpenRouter API key
- `"Error generating text"`: AI text generation failed
- `"Error posting text"`: LinkedIn API communication problem

## 📝 Example AI-Generated Posts

### Professional Achievement
```
🚀 Just completed a major web development project that transformed our client's digital presence!

The project involved building a modern, responsive website with advanced features including real-time analytics, user authentication, and seamless payment integration. The results exceeded expectations with a 40% increase in user engagement.

What's your experience with large-scale web development projects? I'd love to hear about your biggest challenges and successes!

#WebDevelopment #ProjectSuccess #DigitalTransformation #Technology #Innovation
```

### Industry Insight
```
💡 The future of digital marketing is becoming increasingly AI-driven, and the results are fascinating.

Recent studies show that AI-powered marketing campaigns achieve 3x better ROI compared to traditional methods. The key is combining human creativity with machine learning precision.

Are you incorporating AI into your marketing strategies? What tools or approaches have you found most effective?

#DigitalMarketing #AI #MarketingTechnology #Innovation #Growth
```

### Educational Tip
```
🎯 Pro tip for remote work productivity: Create a dedicated workspace that signals "work mode" to your brain.

I've found that having a consistent setup with good lighting, ergonomic furniture, and minimal distractions dramatically improves focus and output quality. Even small changes like using a separate work laptop or specific background music can make a huge difference.

What's your best remote work productivity hack?

#RemoteWork #Productivity #WorkFromHome #ProfessionalDevelopment #Tips
```

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new AI features
- Improving documentation
- Submitting pull requests

## 📄 License

This project is for educational purposes. Use responsibly and in compliance with LinkedIn's and OpenRouter's Terms of Service.

## ⚖️ Disclaimer

This tool is not affiliated with LinkedIn or OpenRouter. Use at your own risk and ensure compliance with all relevant Terms of Service and API usage policies.

---

**Happy AI-Powered Posting! 🚀🤖** 