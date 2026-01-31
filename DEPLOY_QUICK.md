# ⚡ DEPLOY IN 5 MINUTES (TLDR)

## Step 1: Install Git
Download from https://git-scm.com/download/win

## Step 2: Push to GitHub

```powershell
cd "C:\Users\Tolaros\Desktop\Stock forecats"

# One-time setup
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Initialize and push
git init
git add .
git commit -m "Stock forecasting app"
git remote add origin https://github.com/YOUR_USERNAME/stock-forecats.git
git branch -M main
git push -u origin main
```

**Need GitHub?** Sign up here: https://github.com/signup

## Step 3: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **Sign up** → **Sign in with GitHub**
3. Click **New app**
4. Select: Repository: `stock-forecats`, Branch: `main`, File: `app.py`
5. Click **Deploy**

## Done! ✅

Your app is live at: `https://stock-forecats-YOUR_USERNAME.streamlit.app`

---

## Updating Your App

Every time you want to update:

```powershell
git add .
git commit -m "Your change description"
git push
```

Streamlit Cloud redeploys automatically! 🔄

---

**Questions?** Read `DEPLOY_NOW.md` for detailed instructions.

**All set!** Your app is now on the web permanently! 🚀
