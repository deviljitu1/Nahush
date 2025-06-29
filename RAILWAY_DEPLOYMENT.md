# 🚂 Railway Deployment Guide

## Deploy Your LinkedIn AI Post Generator to Railway (Free!)

Railway offers a generous free tier that's perfect for your AI post generator. Here's how to deploy it:

---

## 🚀 Quick Deploy (5 minutes)

### Step 1: Prepare Your Files
Make sure you have these files in your project:
- ✅ `server.py` (updated for Railway)
- ✅ `index.html` (or `index-github.html`)
- ✅ `script.js` (or `script-github.js`)
- ✅ `style.css`
- ✅ `requirements.txt`
- ✅ `railway.json`
- ✅ `Procfile`
- ✅ `runtime.txt`

### Step 2: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"

### Step 3: Deploy from GitHub
1. **Connect GitHub Repository**
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect it's a Python app

2. **Set Environment Variables**
   - Go to your project dashboard
   - Click "Variables" tab
   - Add: `OPEN_ROUTER` = `your-api-key-here`
   - Replace with your real OpenRouter API key

3. **Deploy**
   - Railway will automatically build and deploy
   - Wait 2-3 minutes for deployment

### Step 4: Get Your URL
- Railway will give you a URL like: `https://your-app-name.railway.app`
- Your app is now live! 🎉

---

## 🔧 Manual Setup (Alternative)

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway
```bash
railway login
```

### Step 3: Initialize Project
```bash
railway init
```

### Step 4: Set Environment Variables
```bash
railway variables set OPEN_ROUTER=your-api-key-here
```

### Step 5: Deploy
```bash
railway up
```

---

## 📊 Railway Free Tier Limits

- **$5/month credit** (usually enough for small apps)
- **Automatic HTTPS**
- **Custom domains** (optional)
- **Auto-deploy from GitHub**
- **No sleep/wake delays**

---

## 🔍 Troubleshooting

### "Build Failed"
- Check that `requirements.txt` exists
- Ensure Python version in `runtime.txt` is supported
- Check Railway logs for specific errors

### "API Key Not Found"
- Go to Railway dashboard → Variables
- Add `OPEN_ROUTER` variable with your key
- Redeploy the app

### "Port Issues"
- Railway automatically sets the `PORT` environment variable
- The updated `server.py` handles this automatically

---

## 🌐 Custom Domain (Optional)

1. **Add Custom Domain**
   - Go to Railway dashboard → Settings → Domains
   - Add your domain (e.g., `ai-post-generator.yourdomain.com`)

2. **Configure DNS**
   - Add CNAME record pointing to your Railway app
   - Railway will provide the target URL

---

## 📱 Update Your Frontend

After deployment, update your frontend to use the Railway URL:

```javascript
// In script.js, change the API URL
const API_URL = 'https://your-app-name.railway.app/api/generate-post';
```

---

## 🎯 Benefits of Railway

- ✅ **Always Online** - No sleep/wake delays
- ✅ **Auto-Deploy** - Updates when you push to GitHub
- ✅ **HTTPS Included** - Secure by default
- ✅ **Easy Scaling** - Upgrade when needed
- ✅ **Good Free Tier** - $5/month credit
- ✅ **Simple Setup** - 5-minute deployment

---

## 🔄 Continuous Deployment

Once set up, Railway will automatically:
- Deploy when you push to GitHub
- Restart on crashes
- Scale based on traffic
- Monitor your app health

---

## 💰 Cost Estimation

**Free Tier Usage:**
- Small app like yours: ~$1-2/month
- $5 credit should last 2-5 months
- Easy to upgrade if needed

---

**Your LinkedIn AI Post Generator will be live at:**
`https://your-app-name.railway.app`

**Share this URL with anyone who wants to use your AI post generator!** 🚀 