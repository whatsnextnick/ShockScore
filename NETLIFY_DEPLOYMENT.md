# 🚀 Netlify Deployment Guide

## Overview

Your Shock Score application is now configured for deployment on Netlify with:

- ✅ **Frontend**: React app served as static files
- ✅ **Backend**: Serverless Netlify Functions
- ✅ **Webcam Feature**: Real-time emotion analysis (mock data)
- ✅ **API Routing**: Automatic redirects from `/api/*` to functions

---

## 📋 Prerequisites

1. **GitHub Account** - To connect repository to Netlify
2. **Netlify Account** - Free tier is sufficient (sign up at https://netlify.com)
3. **Git Repository** - Your code pushed to GitHub

---

## 🎯 Quick Deploy (3 Steps)

### Step 1: Push to GitHub

```bash
cd /home/nick_1804/CompouterVision/Module8/ShockScore

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Configure for Netlify deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/shock-score.git

# Push to GitHub
git push -u origin main
```

### Step 2: Connect to Netlify

1. Go to https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **"GitHub"** and authorize
4. Select your **shock-score** repository
5. Netlify will auto-detect settings from `netlify.toml`

### Step 3: Deploy

Click **"Deploy site"** - Netlify will:
1. Install dependencies
2. Build React frontend
3. Deploy functions
4. Provide a live URL (e.g., `https://shock-score-xxxxx.netlify.app`)

---

## ⚙️ Configuration Files

### `netlify.toml`
Main configuration file at project root:

```toml
[build]
  command = "cd frontend && npm install && npm run build"
  publish = "frontend/build"
  functions = "netlify/functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

**What it does:**
- Builds React app from `frontend/` directory
- Publishes `frontend/build/` as static site
- Redirects `/api/*` requests to serverless functions

### `frontend/public/_redirects`
Backup redirect configuration:

```
/api/analyze/frame /.netlify/functions/analyze-frame 200
/api/health /.netlify/functions/health 200
/* /index.html 200
```

### Environment Files

**`.env.production`** (Frontend - production build)
```
GENERATE_SOURCEMAP=false
REACT_APP_API_URL=
```

**`.env.development`** (Frontend - local development)
```
REACT_APP_API_URL=http://localhost:5000
GENERATE_SOURCEMAP=true
```

---

## 🔧 Netlify Functions

Serverless backend functions located in `netlify/functions/`:

### 1. `analyze-frame.js`
- **Endpoint**: `POST /api/analyze/frame`
- **Purpose**: Analyze webcam frames for emotions
- **Returns**: Mock emotion data + shock score
- **Usage**: Called by WebcamShockScoreSimple component

### 2. `health.js`
- **Endpoint**: `GET /api/health`
- **Purpose**: Health check / API status
- **Returns**: Service status and version

---

## 🌐 How It Works

### Architecture on Netlify

```
User Browser
    ↓
Netlify CDN (serves React app)
    ↓
User clicks "Start Camera"
    ↓
React captures frame
    ↓
POST /api/analyze/frame
    ↓
Netlify redirect → /.netlify/functions/analyze-frame
    ↓
Serverless function executes (Node.js)
    ↓
Returns mock emotion data
    ↓
React displays shock score
```

### URL Structure

**Production:**
- Website: `https://your-app.netlify.app`
- API: `https://your-app.netlify.app/api/analyze/frame`

**Local Development:**
- Website: `http://localhost:3000`
- API: `http://localhost:5000/api/analyze/frame`

---

## 🧪 Testing Locally Before Deploy

### Test the Build Process

```bash
# Navigate to frontend
cd frontend

# Create production build
npm run build

# The build/ directory is what Netlify will serve
ls -la build/
```

### Test with Netlify CLI (Optional)

```bash
# Install Netlify CLI globally
npm install -g netlify-cli

# Login to Netlify
netlify login

# Test locally with Netlify Dev
cd /home/nick_1804/CompouterVision/Module8/ShockScore
netlify dev
```

This will:
- Run frontend on port 8888
- Serve functions at `/.netlify/functions/`
- Simulate production environment

---

## 🔐 Environment Variables on Netlify

### Setting Production Variables

1. Go to your site on Netlify dashboard
2. **Site settings** → **Environment variables**
3. Add any required variables:

```
NODE_VERSION = 18
PYTHON_VERSION = 3.11
```

**Note**: No secrets are required for the current mock data version.

---

## 📦 What Gets Deployed

### Included:
✅ `frontend/build/` - React production build
✅ `netlify/functions/` - Serverless API functions
✅ `netlify.toml` - Configuration
✅ `frontend/public/_redirects` - Routing rules

### Excluded (via .gitignore):
❌ `node_modules/` - Dependencies (reinstalled on build)
❌ `venv/` - Python virtual env (not needed for mock version)
❌ `backend/` - Express server (replaced by functions)
❌ `.env` - Local environment variables
❌ Video files, logs, caches

---

## 🚦 Deployment Checklist

Before deploying, verify:

- [ ] Code pushed to GitHub
- [ ] `netlify.toml` in project root
- [ ] `frontend/public/_redirects` exists
- [ ] `.env.production` configured
- [ ] `.gitignore` excludes build artifacts
- [ ] Frontend builds successfully (`npm run build`)
- [ ] No hardcoded localhost URLs in code

---

## 🐛 Troubleshooting

### Build Fails on Netlify

**Check the build log** for errors:

1. Go to **Deploys** tab
2. Click failed deploy
3. View **Deploy log**

**Common issues:**

**"Module not found"**
```bash
# Make sure dependencies are in package.json
cd frontend
npm install
```

**"Command failed: npm run build"**
```bash
# Test build locally first
cd frontend
npm run build
```

### API Functions Return 404

**Check function names match redirects:**

- File: `netlify/functions/analyze-frame.js`
- Redirect: `/api/analyze/frame` → `/.netlify/functions/analyze-frame`
- **Must match!**

**Verify in Netlify dashboard:**
1. **Functions** tab should show deployed functions
2. Test function directly: `https://your-app.netlify.app/.netlify/functions/analyze-frame`

### Webcam Feature Not Working

**Check browser console (F12):**

**CORS errors:**
- Functions should return `Access-Control-Allow-Origin: *` header
- Check `netlify/functions/analyze-frame.js` headers

**404 errors:**
- Verify redirects are working
- Check Network tab in DevTools
- Look for `/api/analyze/frame` request

### Site Loads But Shows Blank Page

**React Router issue:**
- Verify `_redirects` has `/* /index.html 200` as last rule
- Check `netlify.toml` has SPA redirect

---

## 🎬 Testing Your Deployed Site

Once deployed:

1. **Visit your Netlify URL** (e.g., `https://shock-score-xxxxx.netlify.app`)

2. **Test Health Endpoint**
   ```bash
   curl https://your-app.netlify.app/api/health
   ```
   Should return:
   ```json
   {
     "status": "operational",
     "service": "Shock Score API",
     "platform": "netlify"
   }
   ```

3. **Test Webcam Feature**
   - Click "🎥 Start Camera"
   - Allow camera permissions
   - Debug panel should show:
     ```
     Response: 200
     ✓ Got data: Shock=XX.X
     ```
   - Shock score should update every 1.5 seconds

---

## 🔄 Continuous Deployment

Netlify will **auto-deploy** when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update webcam feature"
git push

# Netlify automatically:
# 1. Detects push
# 2. Runs build
# 3. Deploys new version
# 4. Live in ~2 minutes
```

**View deployments:**
- Netlify dashboard → **Deploys** tab
- See build logs, preview deploys, rollback if needed

---

## 🌟 Custom Domain (Optional)

### Add Your Own Domain

1. **Buy a domain** (Namecheap, Google Domains, etc.)

2. **In Netlify:**
   - **Domain settings** → **Add custom domain**
   - Enter your domain (e.g., `shockscore.com`)

3. **Configure DNS:**
   - Add Netlify's nameservers to your domain provider
   - Or add A record: `104.198.14.52`

4. **Enable HTTPS:**
   - Netlify provides free SSL certificates
   - Auto-enabled for custom domains

---

## 📊 Monitoring

### Netlify Analytics

1. **Analytics** tab on dashboard shows:
   - Page views
   - Unique visitors
   - Top pages
   - Bandwidth usage

### Function Logs

1. **Functions** tab → Click function name
2. View invocations, errors, execution time

### Deploy Previews

- Every pull request gets a preview URL
- Test changes before merging to main

---

## 💰 Pricing

### Netlify Free Tier Includes:
- ✅ 100GB bandwidth/month
- ✅ 300 build minutes/month
- ✅ 125k function invocations/month
- ✅ Continuous deployment
- ✅ Free SSL certificates

**More than enough for development and demos!**

---

## 🚀 Next Steps

### After Basic Deployment:

1. **Custom Domain** - Add your own domain name
2. **Analytics** - Enable Netlify Analytics
3. **Form Handling** - Use Netlify Forms for feedback
4. **A/B Testing** - Split testing for features

### To Add Real Python FER Engine:

The current deployment uses **mock data**. To add real emotion detection:

1. **Option A: External API**
   - Deploy Python FER engine on AWS Lambda/Google Cloud Functions
   - Call from Netlify functions

2. **Option B: Third-party Service**
   - Use Microsoft Azure Face API
   - Use Google Cloud Vision API
   - Integrate with Netlify functions

3. **Option C: Backend Server**
   - Deploy Node.js + Python backend on Heroku/Railway
   - Keep frontend on Netlify
   - Update API URL in environment variables

---

## 📝 Summary

### What You Have Now:

✅ **Production-ready React app** on Netlify CDN
✅ **Serverless API functions** for webcam analysis
✅ **Automatic deployments** from GitHub
✅ **HTTPS enabled** by default
✅ **Global CDN** for fast loading
✅ **Zero server management** required

### File Structure:

```
ShockScore/
├── netlify.toml              # Main config
├── .gitignore                # Git exclusions
├── .env.example              # Environment template
│
├── frontend/
│   ├── public/
│   │   └── _redirects        # Routing rules
│   ├── src/                  # React source
│   ├── .env.production       # Prod env vars
│   ├── .env.development      # Dev env vars
│   └── package.json          # Dependencies
│
└── netlify/
    └── functions/
        ├── analyze-frame.js  # Webcam analysis API
        ├── health.js         # Health check API
        └── package.json      # Function dependencies
```

---

## 🎉 You're Ready to Deploy!

Push to GitHub and connect to Netlify - your app will be live in minutes!

**Questions?** Check the troubleshooting section or Netlify docs: https://docs.netlify.com
