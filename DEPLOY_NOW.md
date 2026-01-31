# 🚀 DEPLOY YOUR APP TO THE WEB IN 5 MINUTES

## Step 1: Push Your Code to GitHub (2 minutes)

### 1.1 Create a GitHub Account
- Go to https://github.com/signup
- Sign up with your email
- Verify your email

### 1.2 Create a New Repository
- Go to https://github.com/new
- **Repository name**: `stock-forecats` (or any name you like)
- **Description**: Stock Analyzer with AI Scoring & Forecasting
- Select **Public** (required for free Streamlit Cloud)
- Click **Create repository**

### 1.3 Push Your Code
In your terminal (PowerShell), run these commands:

```powershell
cd "C:\Users\Tolaros\Desktop\Stock forecats"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Stock analyzer with scoring and forecasting"

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/stock-forecats.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: You'll need to:
1. Install Git: https://git-scm.com/download/win
2. Create a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Check `repo` checkbox
   - Copy the token
3. When prompted for password, paste the token instead

---

## Step 2: Deploy on Streamlit Cloud (3 minutes)

### 2.1 Sign Up for Streamlit Cloud
- Go to https://streamlit.io/cloud
- Click **Sign up**
- Click **Sign in with GitHub**
- Authorize Streamlit to access your GitHub

### 2.2 Deploy Your App
- Click **New app**
- Select:
  - **Repository**: `stock-forecats`
  - **Branch**: `main`
  - **Main file path**: `app.py`
- Click **Deploy**

### 2.3 Wait for Deployment
- Your app will deploy in ~2 minutes
- You'll see a URL like: `https://stock-forecats-USERNAME.streamlit.app`
- **That's your permanent URL!** ✅

---

## Step 3: Share Your App! (Ongoing)

Your app is now **live on the internet!** 🎉

- Share URL: `https://stock-forecats-USERNAME.streamlit.app`
- Everyone can access it
- It updates automatically when you push changes to GitHub

---

## What Gets Deployed?

Your Streamlit Cloud app includes:
✅ `app.py` - Main application
✅ `utils/` - All utility modules
✅ `requirements.txt` - All dependencies
✅ Charts, indicators, scoring, forecasts
✅ Beautiful UI with recommendations

---

## Cost Breakdown

| Feature | Cost |
|---------|------|
| Streamlit Cloud Hosting | **FREE** ✅ |
| Custom Domain | Optional: $12/year |
| Total Year 1 | **$0-12** |

---

## Automatic Updates

Every time you:
1. Make changes to your code
2. Push to GitHub (`git push`)
3. Streamlit Cloud automatically redeploys! 🔄

No manual deployment needed!

---

## API Keys in Production

⚠️ **Important**: Your app uses NewsAPI for news sentiment. 

**Option 1: Keep Free Tier** (Recommended)
- Free NewsAPI key allows 100 requests/day
- Works great for shared deployment
- No action needed

**Option 2: Add Your API Key Securely**
- In Streamlit Cloud, go to **App Settings** → **Secrets**
- Add your NewsAPI key there
- App will use the secure secret

---

## Troubleshooting

### App won't deploy?
- Make sure `requirements.txt` has all packages
- Check that `app.py` is in the root directory
- Repository must be **Public**

### Missing packages?
```bash
# In your project root, update requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### App runs slow?
- Normal for first load (cold start)
- Caching helps after that
- Consider upgrading to paid tier if needed

---

## Next Steps

### Quick Win (Do This Now)
1. ✅ Install Git
2. ✅ Create GitHub account
3. ✅ Push code to GitHub
4. ✅ Deploy on Streamlit Cloud
5. ✅ Share your URL!

### After Deployment
- Get user feedback
- Track usage metrics
- Plan Phase 2 features
- Consider mobile app if demand exists

---

## Example Deployment Commands

```powershell
# Complete deployment workflow
cd "C:\Users\Tolaros\Desktop\Stock forecats"

# 1. Install Git (if needed)
# Download from https://git-scm.com/download/win

# 2. Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Initialize repository
git init
git add .
git commit -m "Initial commit"

# 4. Add GitHub remote (replace USERNAME)
git remote add origin https://github.com/USERNAME/stock-forecats.git
git branch -M main
git push -u origin main

# 5. That's it! Go to Streamlit Cloud and deploy
```

---

## Your Deployment URL

Once deployed, your app will be live at:

```
https://stock-forecats-USERNAME.streamlit.app
```

Example: `https://stock-forecats-tolaros.streamlit.app`

Replace `USERNAME` with your GitHub username!

---

## Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud Help**: https://docs.streamlit.io/streamlit-cloud/get-started
- **GitHub Docs**: https://docs.github.com

---

**You're ready to go live!** 🚀

Questions? Open `00_START_HERE.md` for more options!
