# ✅ Netlify Deployment Checklist

Use this checklist to ensure your deployment goes smoothly.

---

## 📋 Pre-Deployment

### Code Ready

- [ ] All code committed to Git
- [ ] `.gitignore` properly configured
- [ ] No sensitive data in repository (API keys, passwords, etc.)
- [ ] `netlify.toml` in project root
- [ ] `frontend/public/_redirects` exists

### Configuration Files

- [ ] `netlify.toml` - Main configuration
- [ ] `frontend/.env.production` - Production environment variables
- [ ] `frontend/.env.development` - Development environment variables
- [ ] `.env.example` - Environment template for others
- [ ] `netlify/functions/package.json` - Function dependencies

### Functions

- [ ] `netlify/functions/analyze-frame.js` exists
- [ ] `netlify/functions/health.js` exists
- [ ] Functions export `exports.handler`
- [ ] CORS headers configured in functions

### Frontend

- [ ] API calls use relative paths (`/api/*`)
- [ ] No hardcoded `localhost` URLs in production code
- [ ] React Router configured for SPA
- [ ] `public/_redirects` includes SPA fallback

---

## 🧪 Test Locally

### Build Test

```bash
cd /home/nick_1804/CompouterVision/Module8/ShockScore
./test-netlify-build.sh
```

- [ ] Script completes without errors
- [ ] Frontend builds successfully
- [ ] `frontend/build/` directory created
- [ ] Build size is reasonable (< 5MB)

### Local Server Test

**Terminal 1:**
```bash
cd backend
npm start
```

**Terminal 2:**
```bash
cd frontend
npm start
```

- [ ] Backend starts on port 5000
- [ ] Frontend starts on port 3000
- [ ] Health endpoint responds: `http://localhost:5000/api/health`
- [ ] Webcam feature works locally
- [ ] No console errors in browser (F12)

### API Endpoint Test

```bash
cd backend
node test-endpoint.js
```

- [ ] Test script returns 200 status
- [ ] Mock data includes `shockScore`
- [ ] Response includes `_mode: 'mock'`

---

## 📤 GitHub Setup

### Repository

- [ ] Repository created on GitHub
- [ ] Remote added: `git remote add origin <url>`
- [ ] Main branch exists
- [ ] All files pushed to GitHub

### Commands

```bash
cd /home/nick_1804/CompouterVision/Module8/ShockScore

# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Configure for Netlify deployment"

# Push to GitHub
git push -u origin main
```

- [ ] Push successful
- [ ] Files visible on GitHub
- [ ] No errors in git push

---

## 🚀 Netlify Setup

### Account

- [ ] Netlify account created (https://netlify.com)
- [ ] GitHub connected to Netlify
- [ ] Billing set up (free tier is fine)

### Site Creation

1. [ ] Click "Add new site" on Netlify dashboard
2. [ ] Select "Import an existing project"
3. [ ] Choose GitHub as provider
4. [ ] Select your repository
5. [ ] Review build settings:
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/build`
   - Functions directory: `netlify/functions`
6. [ ] Click "Deploy site"

### Build Configuration

Netlify should auto-detect from `netlify.toml`:

- [ ] Build command detected
- [ ] Publish directory set
- [ ] Functions directory set
- [ ] Node version: 18

---

## ⚙️ Environment Variables (Optional)

If needed, set in Netlify dashboard under **Site settings → Environment variables**:

```
NODE_VERSION = 18
PYTHON_VERSION = 3.11
```

- [ ] Environment variables added (if needed)

---

## 🔍 Post-Deployment Verification

### Site Live

- [ ] Deployment succeeded (green checkmark)
- [ ] Site URL provided (e.g., `https://shock-score-xxxxx.netlify.app`)
- [ ] No build errors in deploy log

### Test Deployed Site

**1. Visit site URL**
- [ ] Site loads without errors
- [ ] Dashboard displays correctly
- [ ] No 404 errors
- [ ] CSS styles applied

**2. Test Health Endpoint**
```bash
curl https://YOUR-SITE.netlify.app/api/health
```
- [ ] Returns 200 status
- [ ] JSON response includes `"platform": "netlify"`

**3. Test Webcam Feature**
- [ ] Click "Start Camera"
- [ ] Camera permission prompt appears
- [ ] Video feed displays
- [ ] Debug panel appears
- [ ] Debug panel shows "Response: 200"
- [ ] Shock score updates
- [ ] Emotion bars animate
- [ ] No errors in browser console

**4. Check Network Tab (F12)**
- [ ] `/api/analyze/frame` returns 200
- [ ] Response includes emotion data
- [ ] No CORS errors
- [ ] Requests complete in < 2 seconds

---

## 🎯 Functionality Checklist

### Dashboard
- [ ] Stats cards display
- [ ] Charts render
- [ ] Recent films table shows
- [ ] Navigation works

### Webcam Feature
- [ ] Start camera button works
- [ ] Camera activates
- [ ] Debug logging visible
- [ ] Frames captured every 1.5s
- [ ] Shock score updates
- [ ] Emotion bars update
- [ ] Dominant emotion displays
- [ ] Stop camera works

### Routing
- [ ] Click "Upload New Film" navigates
- [ ] Click "View Report" navigates
- [ ] Browser back button works
- [ ] Direct URL access works

---

## 🐛 Troubleshooting Checklist

### Build Fails

- [ ] Check build log on Netlify
- [ ] Verify all dependencies in `package.json`
- [ ] Test build locally: `cd frontend && npm run build`
- [ ] Check Node version compatibility

### Functions Return 404

- [ ] Verify `netlify/functions/` directory exists
- [ ] Check function file names match redirects
- [ ] View **Functions** tab on Netlify dashboard
- [ ] Test function directly: `/.netlify/functions/analyze-frame`

### CORS Errors

- [ ] Check function headers include `Access-Control-Allow-Origin`
- [ ] Verify OPTIONS method handled
- [ ] Check browser console for details

### Blank Page

- [ ] Check `_redirects` file includes `/* /index.html 200`
- [ ] Verify React Router setup
- [ ] Check browser console for errors
- [ ] View page source - should have React root div

---

## 📝 Custom Domain (Optional)

If adding a custom domain:

- [ ] Domain purchased
- [ ] Domain added in Netlify: **Domain settings → Add custom domain**
- [ ] DNS configured (Netlify nameservers or A record)
- [ ] SSL certificate provisioned (automatic)
- [ ] HTTPS redirect enabled
- [ ] Site accessible via custom domain

---

## 🔄 Continuous Deployment

Verify auto-deploy works:

```bash
# Make a small change
echo "# Test" >> TEST.md

# Commit and push
git add TEST.md
git commit -m "Test auto-deploy"
git push
```

- [ ] Netlify detects push
- [ ] Build triggered automatically
- [ ] Deploy succeeds
- [ ] Changes visible on site

---

## ✅ Final Verification

### All Systems Go

- [ ] ✅ Site deployed and live
- [ ] ✅ Health endpoint responds
- [ ] ✅ Webcam feature works
- [ ] ✅ No console errors
- [ ] ✅ All pages load correctly
- [ ] ✅ Mobile responsive
- [ ] ✅ Auto-deploy configured

### Share Your Success!

**Your live URL:** `https://________.netlify.app`

Share with:
- [ ] Team members
- [ ] Stakeholders
- [ ] Test users

---

## 🎉 Deployment Complete!

Congratulations! Your Shock Score platform is now live on Netlify.

### Next Steps:

1. **Monitor** - Check Netlify analytics
2. **Test** - Have users try the webcam feature
3. **Iterate** - Make improvements based on feedback
4. **Scale** - Add real Python FER engine when ready

---

## 📞 Need Help?

- **Netlify Docs**: https://docs.netlify.com
- **Deployment Guide**: [NETLIFY_DEPLOYMENT.md](NETLIFY_DEPLOYMENT.md)
- **GitHub Issues**: Create issue in your repository

---

**Deployment Date:** _______________

**Deployed By:** _______________

**Site URL:** _______________
