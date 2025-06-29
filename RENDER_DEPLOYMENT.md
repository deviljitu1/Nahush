# Deploy LinkedIn AI Post Generator to Render

This guide will help you deploy the LinkedIn AI Post Generator to Render, making it accessible to anyone on the internet.

## Prerequisites

1. A GitHub account
2. A Render account (free tier available)
3. Your OpenRouter API key

## Step 1: Prepare Your Repository

Make sure your repository contains these files:
- `app.py` - Flask web application
- `index.html` - Main web interface
- `style.css` - Styling
- `script.js` - Frontend JavaScript
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration

## Step 2: Push to GitHub

1. Create a new repository on GitHub
2. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Step 3: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click "Apply" to deploy

### Option B: Manual Deployment

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `linkedin-ai-post-generator`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Health Check Path**: `/health`

5. Add Environment Variables:
   - **Key**: `OPENROUTER_API_KEY`
   - **Value**: Your OpenRouter API key

6. Click "Create Web Service"

## Step 4: Configure Environment Variables

In your Render dashboard, go to your service and add these environment variables:

- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `PYTHON_VERSION`: `3.9.16`

## Step 5: Access Your App

Once deployed, Render will provide you with a URL like:
`https://your-app-name.onrender.com`

You can now share this URL with anyone, and they can use the LinkedIn AI Post Generator from any device!

## Features Available After Deployment

✅ **Public Access**: Anyone can use your app from any device
✅ **Mobile Friendly**: Responsive design works on phones and tablets
✅ **Article Summarization**: Paste article URLs to generate LinkedIn posts
✅ **AI-Powered**: Uses OpenRouter AI for content generation
✅ **Professional Design**: Modern, clean interface
✅ **Copy to Clipboard**: Easy sharing functionality
✅ **Direct LinkedIn Access**: Quick access to LinkedIn

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check that all files are in the repository
2. **API Errors**: Verify your OpenRouter API key is correct
3. **App Not Loading**: Check the health check endpoint at `/health`

### Logs and Debugging:

1. In Render dashboard, go to your service
2. Click on "Logs" tab
3. Check for any error messages

## Cost

- **Free Tier**: 750 hours/month (enough for personal use)
- **Paid Plans**: Start at $7/month for more resources

## Security Notes

- Your API key is stored securely in Render's environment variables
- The app doesn't store any user data
- All processing happens in memory

## Support

If you encounter issues:
1. Check the Render logs
2. Verify your API key is working
3. Test the health endpoint: `https://your-app.onrender.com/health`

## Next Steps

After deployment, you can:
1. Share the URL with colleagues and friends
2. Customize the design by editing `style.css`
3. Add more features to `app.py`
4. Monitor usage in Render dashboard

---

**Your app is now live and accessible to everyone on the internet! 🚀** 