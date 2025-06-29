# 🚀 Quick Deploy Guide - Render (100% Free)

## Step-by-Step: Create Project & Deploy

### Step 1: Create GitHub Repository

1. **Go to [GitHub.com](https://github.com)**
2. **Click "New repository"** (green button)
3. **Repository name:** `linkedin-ai-post-generator`
4. **Make it Public** ✅
5. **Don't initialize with README** ❌
6. **Click "Create repository"**

### Step 2: Upload Your Files

**Option A: Using Git (Recommended)**
```bash
# In your project folder (C:\Users\Nahush Patel\Desktop\Nahush)
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/linkedin-ai-post-generator.git
git push -u origin main
```

**Option B: Manual Upload**
1. Go to your new GitHub repository
2. Click "uploading an existing file"
3. Drag and drop these files:
   - `server.py`
   - `index.html`
   - `script.js`
   - `style.css`
   - `requirements.txt`
   - `render.yaml`
   - `README.md`
   - `LICENSE`

### Step 3: Create Render Account

1. **Go to [render.com](https://render.com)**
2. **Click "Get Started"**
3. **Click "Continue with GitHub"**
4. **Authorize Render** to access your GitHub

### Step 4: Create Project

1. **Click "New +"** (top right corner)
2. **Click "Web Service"**
3. **Click "Connect a repository"**
4. **Select your repository:** `linkedin-ai-post-generator`
5. **Click "Connect"**

### Step 5: Configure Service

Fill in these exact settings:

- **Name:** `linkedin-ai-post-generator`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python server.py`
- **Plan:** `Free`

### Step 6: Set API Key

1. **Click "Environment" tab**
2. **Click "Add Environment Variable"**
3. **Add this:**
   - **Key:** `OPEN_ROUTER`
   - **Value:** `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`
4. **Click "Save Changes"**

### Step 7: Deploy

1. **Click "Create Web Service"**
2. **Wait 3-5 minutes** (you'll see build progress)
3. **Your app will be live!** 🎉

### Step 8: Get Your URL

- Render will show you: `https://your-app-name.onrender.com`
- **This is your free, live app!**
- Share this URL with anyone

---

## 🔍 Troubleshooting

### "Repository not found"
- Make sure you created the GitHub repository
- Make sure you uploaded the files
- Make sure the repository is public

### "Build failed"
- Check that `requirements.txt` exists
- Check that all files are uploaded
- Look at the build logs for specific errors

### "API key not found"
- Make sure you added the `OPEN_ROUTER` environment variable
- Make sure you used your real API key
- Redeploy after adding the variable

---

## ✅ Success Checklist

- [ ] GitHub repository created
- [ ] Files uploaded to GitHub
- [ ] Render account created
- [ ] Project created in Render
- [ ] Repository connected
- [ ] Environment variables set
- [ ] Service deployed
- [ ] App is live and working

---

## 🎯 Your Result

**Your LinkedIn AI Post Generator will be live at:**
`https://your-app-name.onrender.com`

**Cost:** $0/month forever
**Setup time:** 10 minutes
**Status:** Completely free and functional! 🆓🚀

---

**Need help?** Check the build logs in Render dashboard for specific error messages. 