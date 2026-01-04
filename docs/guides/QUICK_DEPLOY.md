# 🚀 Quick Deploy Guide - Share Your App for Free!

## ⚡ 5-Minute Setup on Render (Free + Custom Domain)

### Step 1: Push to GitHub (if not already)
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Render

1. **Go to**: https://render.com → Sign up (free)

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect GitHub → Select your repo

3. **Configure**:
   ```
   Name: victus
   Environment: Docker
   Start Command: uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables** (click "Advanced"):
   ```
   OPENAI_API_KEY=your_key_here
   SECRET_KEY=<generate: python -c "import secrets; print(secrets.token_urlsafe(32))">
   DATABASE_URL=sqlite:///./chat_history.db
   ENVIRONMENT=production
   ```

5. **Click "Create Web Service"**
   - Wait ~5-10 minutes
   - Your app: `https://victus.onrender.com` ✅

### Step 3: Add Custom Domain (Optional)

1. **Get Domain**: Namecheap/Cloudflare (~$10/year)

2. **In Render**: Settings → Custom Domains → Add
   - Enter: `victus.yourdomain.com`

3. **DNS Setup** (at your registrar):
   ```
   Type: CNAME
   Name: victus
   Value: victus.onrender.com
   ```

4. **Wait 5-10 minutes** → SSL auto-provisioned ✅

### Step 4: Keep It Awake (Free)

**UptimeRobot** (free):
1. Sign up: https://uptimerobot.com
2. Add monitor:
   - URL: `https://victus.onrender.com/api/health`
   - Interval: 5 minutes
3. Done! App stays awake 24/7

---

## 🎉 Done! Share Your App

**Your URL**: `https://victus.onrender.com` or `https://victus.yourdomain.com`

**Share with friends!** They can:
- Sign up
- Chat with VICTUS
- Use all features

---

## 📝 Full Guide

See `FREE_DEPLOYMENT.md` for detailed instructions.

---

## ✅ What You Get (Free Forever)

- ✅ Custom domain support
- ✅ Free SSL certificate
- ✅ 750 hours/month (24/7)
- ✅ Persistent storage
- ✅ Auto-deploy from Git
- ✅ $0/month cost

**Perfect for sharing your app!** 🚀

