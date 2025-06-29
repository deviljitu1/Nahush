# 🆓 Render Deployment Guide (100% Free!)

## Deploy Your LinkedIn AI Post Generator to Render for $0/month

Render offers a completely free tier that's perfect for your AI post generator. Here's how to deploy it:

---

## 🚀 Quick Deploy (5 minutes)

### Step 1: Prepare Your Files
Make sure you have these files in your project:
- ✅ `server.py` (updated for cloud deployment)
- ✅ `index.html` (or `index-github.html`)
- ✅ `script.js` (or `script-github.js`)
- ✅ `style.css`
- ✅ `requirements.txt`
- ✅ `render.yaml` (optional, for easier setup)

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (free)
3. Click "New +" → "Web Service"

### Step 3: Connect GitHub Repository
1. **Connect Repository**
   - Click "Connect a repository"
   - Select your GitHub repository
   - Render will auto-detect it's a Python app

2. **Configure Service**
   - **Name:** `linkedin-ai-post-generator`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
   - **Plan:** `Free`

3. **Set Environment Variables**
   - Click "Environment" tab
   - Add: `OPEN_ROUTER` = `your-api-key-here`
   - Replace with your real OpenRouter API key

4. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment

### Step 4: Get Your Free URL
- Render will give you: `https://your-app-name.onrender.com`
- Your app is now live for FREE! 🎉

---

## 📊 Render Free Tier Limits

- **750 hours/month** (31 days = 744 hours, so you get 6 extra hours!)
- **Sleeps after 15 minutes** of inactivity
- **Auto-wakes** when someone visits
- **HTTPS included**
- **Custom domains** (optional)
- **Auto-deploy from GitHub**

---

## ⏰ Sleep/Wake Behavior

**How it works:**
- ✅ **Always free** - No charges ever
- ⏰ **Sleeps after 15 minutes** of no traffic
- 🔄 **Auto-wakes** when someone visits (takes 30-60 seconds)
- 📊 **750 hours/month** is more than enough

**For your use case:**
- Most users won't notice the 30-second wake delay
- 750 hours = 31 days, so you never run out
- Perfect for personal projects and demos

---

## 🔍 Troubleshooting

### "Build Failed"
- Check that `requirements.txt` exists
- Ensure all dependencies are listed
- Check Render logs for specific errors

### "API Key Not Found"
- Go to Render dashboard → Environment
- Add `OPEN_ROUTER` variable with your key
- Redeploy the service

### "Service Sleeping"
- This is normal for free tier
- First request takes 30-60 seconds to wake up
- Subsequent requests are instant

---

## 🌐 Custom Domain (Optional)

1. **Add Custom Domain**
   - Go to Render dashboard → Settings → Domains
   - Add your domain (e.g., `ai-post-generator.yourdomain.com`)

2. **Configure DNS**
   - Add CNAME record pointing to your Render app
   - Render will provide the target URL

---

## 📱 Update Your Frontend

After deployment, update your frontend to use the Render URL:

```javascript
// In script.js, change the API URL
const API_URL = 'https://your-app-name.onrender.com/api/generate-post';
```

---

## 🎯 Benefits of Render Free Tier

- ✅ **100% Free** - No charges ever
- ✅ **Always Available** - 750 hours/month
- ✅ **Auto-Deploy** - Updates when you push to GitHub
- ✅ **HTTPS Included** - Secure by default
- ✅ **Easy Setup** - 5-minute deployment
- ✅ **Good Performance** - Fast when awake

---

## 🔄 Continuous Deployment

Once set up, Render will automatically:
- Deploy when you push to GitHub
- Restart on crashes
- Monitor your app health
- Wake up when needed

---

## 💰 Cost: $0/month

**Free Tier Usage:**
- Your app: ~$0/month
- 750 hours = 31 days of continuous running
- Sleep/wake is free
- No hidden charges

---

## 🆚 Comparison: Render vs Railway

| Feature | Render (Free) | Railway (Free) |
|---------|---------------|----------------|
| **Cost** | $0/month | $5/month after first month |
| **Always Online** | Sleeps after 15 min | Always online |
| **Wake Time** | 30-60 seconds | Instant |
| **Hours/Month** | 750 hours | Unlimited |
| **Best For** | **Personal projects** | Business apps |

---

**Your LinkedIn AI Post Generator will be live at:**
`https://your-app-name.onrender.com`

**Completely free forever!** 🆓🚀

---

## 🎯 Recommendation

**Use Render** because:
- ✅ **100% free forever**
- ✅ Perfect for personal projects
- ✅ 750 hours/month is plenty
- ✅ Sleep/wake is acceptable for demos
- ✅ Easy 5-minute setup
- ✅ No credit card required

**Share your free URL with anyone who wants to use your AI post generator!** 🎉 