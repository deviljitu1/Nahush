# Deployment Guide

## 🚀 GitHub Pages Deployment

### Step 1: Prepare Your Repository

1. **Create a new repository** on GitHub
   - Name: `linkedin-ai-post-generator`
   - Make it public
   - Don't initialize with README (we'll upload files)

### Step 2: Upload Files

Upload these files to your repository:

**Required Files:**
- `index-github.html` → Rename to `index.html`
- `script-github.js` → Rename to `script.js`
- `style.css`
- `README.md`
- `LICENSE`

**Optional Files (for local development):**
- `server.py`
- `requirements.txt`
- `run_linkedin_automation.bat`

### Step 3: Enable GitHub Pages

1. **Go to repository Settings**
2. **Scroll to "Pages" section**
3. **Under "Source" select:**
   - Source: "Deploy from a branch"
   - Branch: "main"
   - Folder: "/ (root)"
4. **Click "Save"**

### Step 4: Wait for Deployment

- GitHub will build your site
- Check the "Actions" tab for build status
- Your site will be available at: `https://username.github.io/linkedin-ai-post-generator`

### Step 5: Test Your Site

1. **Visit your GitHub Pages URL**
2. **Test the interface** (should show setup instructions)
3. **Verify all features work** correctly

## 🔧 Custom Domain (Optional)

### Step 1: Add CNAME File

Create a file named `CNAME` in your repository root:
```
yourdomain.com
```

### Step 2: Configure DNS

Add these DNS records to your domain provider:
```
Type: CNAME
Name: @
Value: username.github.io
```

### Step 3: Update GitHub Pages

1. **Go to repository Settings → Pages**
2. **Add your custom domain**
3. **Check "Enforce HTTPS"**
4. **Save changes**

## 📱 Mobile Testing

Test your site on:
- ✅ Desktop browsers
- ✅ Mobile browsers
- ✅ Different screen sizes
- ✅ Touch interactions

## 🔍 Troubleshooting

### Common Issues

**Site not loading:**
- Check repository is public
- Verify GitHub Pages is enabled
- Wait 5-10 minutes for deployment

**Styling issues:**
- Ensure `style.css` is uploaded
- Check file paths are correct
- Clear browser cache

**JavaScript errors:**
- Verify `script.js` is uploaded
- Check browser console for errors
- Ensure all dependencies are loaded

### Getting Help

1. **Check GitHub Actions** for build errors
2. **Review browser console** for JavaScript errors
3. **Verify file structure** matches requirements
4. **Contact support** if issues persist

## 🎯 Next Steps

After successful deployment:

1. **Update README.md** with your actual GitHub URL
2. **Share your site** with others
3. **Consider adding analytics** (Google Analytics)
4. **Monitor usage** and gather feedback

## 📊 Analytics Setup (Optional)

### Google Analytics

1. **Create Google Analytics account**
2. **Add tracking code** to `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### GitHub Insights

- **Go to repository Insights**
- **View traffic** and visitor statistics
- **Monitor popular pages**

---

**Your LinkedIn AI Post Generator is now live! 🎉** 