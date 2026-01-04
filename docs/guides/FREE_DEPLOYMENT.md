# Free Deployment with Custom Domain - VICTUS

## 🎯 Best Free Options with Custom Domain

### 1. **Render** (Recommended - Best Free Option) ⭐

**Why Render:**
- ✅ **100% Free tier** with custom domain support
- ✅ Free SSL certificate
- ✅ Persistent storage
- ✅ Auto-deploy from GitHub
- ✅ 750 hours/month free (enough for 24/7)
- ✅ Custom domain included in free tier

**Steps:**
1. Push code to GitHub
2. Go to [Render.com](https://render.com) → Sign up (free)
3. New → Web Service
4. Connect GitHub repository
5. Configure:
   - **Name**: `victus` (or your choice)
   - **Environment**: Docker
   - **Build Command**: (auto-detected)
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (from `.env.example`)
7. Click "Create Web Service"
8. Wait for deployment (~5-10 minutes)

**Custom Domain Setup:**
1. Go to your service → Settings → Custom Domains
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `victus.yourdomain.com`)
4. Follow DNS instructions:
   - Add CNAME record: `victus` → `victus.onrender.com`
   - Or A record: `@` → Render's IP (shown in dashboard)
5. Render automatically provisions SSL certificate (free)
6. Done! Your app is live at your custom domain

**Free Tier Limits:**
- ✅ 750 hours/month (enough for 24/7)
- ✅ 512MB RAM (sufficient for VICTUS)
- ✅ Custom domain included
- ⚠️ Spins down after 15 min inactivity (wakes on request)

**To prevent sleep (optional):**
- Use [UptimeRobot](https://uptimerobot.com) (free) to ping every 5 minutes
- Or upgrade to paid ($7/month) for always-on

---

### 2. **Fly.io** (Great Alternative)

**Why Fly.io:**
- ✅ **Free tier** with custom domain
- ✅ Always-on (no sleep)
- ✅ Global edge deployment
- ✅ 3 shared-cpu VMs free
- ✅ 3GB persistent volume free

**Steps:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `fly auth signup` (free)
3. In project directory: `fly launch`
4. Follow prompts:
   - App name: `victus` (or your choice)
   - Region: Choose closest
   - Database: No (use SQLite for free)
5. Add secrets: `fly secrets set OPENAI_API_KEY=your_key SECRET_KEY=your_secret`
6. Deploy: `fly deploy`

**Custom Domain:**
1. `fly domains add yourdomain.com`
2. Follow DNS instructions
3. SSL auto-provisioned

**Free Tier:**
- ✅ 3 shared-cpu VMs
- ✅ 3GB storage
- ✅ Always-on
- ✅ Custom domain

---

### 3. **Railway** (Easy but Limited Free Tier)

**Why Railway:**
- ✅ Very easy deployment
- ✅ $5 free credit monthly
- ⚠️ Custom domain requires paid plan ($5/month)
- ⚠️ Free tier limited to $5/month usage

**Steps:**
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub (free)
3. New Project → Deploy from GitHub
4. Select repository
5. Add environment variables
6. Deploy!

**Custom Domain:**
- Requires Hobby plan ($5/month)
- But you get $5 free credit, so effectively free for first month
- After that, $5/month for custom domain

---

### 4. **Replit** (Alternative)

**Why Replit:**
- ✅ Free tier available
- ✅ Custom domain support
- ✅ Easy setup
- ⚠️ Less suitable for production

**Steps:**
1. Go to [Replit.com](https://replit.com)
2. Import from GitHub
3. Configure run command
4. Add custom domain in settings

---

## 🚀 Quick Start: Render (Recommended)

### Step-by-Step Guide

#### 1. Prepare Your Code
```bash
# Make sure everything is committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### 2. Deploy on Render

1. **Sign up**: Go to [render.com](https://render.com) → Sign up (free)

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect GitHub account
   - Select your repository

3. **Configure Service**:
   ```
   Name: victus
   Environment: Docker
   Region: Choose closest to you
   Branch: main
   Root Directory: (leave empty)
   Build Command: (auto-detected from Dockerfile)
   Start Command: uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable"
   
   Add these (from your `.env`):
   ```
   OPENAI_API_KEY=your_key_here
   SECRET_KEY=your_secret_here
   DATABASE_URL=sqlite:///./chat_history.db
   ENVIRONMENT=production
   CORS_ORIGINS=*
   LOG_LEVEL=INFO
   ```
   
   Optional:
   ```
   TAVILY_API_KEY=your_key
   OPENWEATHER_API_KEY=your_key
   MS_CLIENT_ID=your_id
   MS_CLIENT_SECRET=your_secret
   MS_TENANT_ID=your_tenant
   GOOGLE_CLIENT_ID=your_id
   GOOGLE_CLIENT_SECRET=your_secret
   ```

5. **Create Service**:
   - Click "Create Web Service"
   - Wait for build (~5-10 minutes)
   - Your app will be at: `https://victus.onrender.com`

#### 3. Add Custom Domain

1. **Get a Domain** (if you don't have one):
   - [Namecheap](https://namecheap.com) - ~$10/year
   - [Cloudflare](https://cloudflare.com) - ~$10/year
   - [Google Domains](https://domains.google) - ~$12/year

2. **Configure DNS**:
   - Go to your domain registrar
   - Add CNAME record:
     ```
     Type: CNAME
     Name: victus (or @ for root domain)
     Value: victus.onrender.com
     TTL: 3600
     ```

3. **Add Domain in Render**:
   - Go to your service → Settings → Custom Domains
   - Click "Add"
   - Enter: `victus.yourdomain.com` (or `yourdomain.com`)
   - Render will verify DNS
   - SSL certificate auto-provisioned (free)
   - Done! 🎉

#### 4. Prevent Sleep (Optional)

Render free tier sleeps after 15 min inactivity. To keep it awake:

**Option A: UptimeRobot (Free)**
1. Sign up at [UptimeRobot.com](https://uptimerobot.com) (free)
2. Add monitor:
   - URL: `https://victus.onrender.com/api/health`
   - Interval: 5 minutes
3. This will ping your app every 5 min, keeping it awake

**Option B: Upgrade to Paid ($7/month)**
- Always-on
- No sleep
- Better performance

---

## 📋 Environment Variables for Render

Create these in Render dashboard:

### Required:
```env
OPENAI_API_KEY=sk-...
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
DATABASE_URL=sqlite:///./chat_history.db
ENVIRONMENT=production
```

### Recommended:
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

### Optional:
```env
TAVILY_API_KEY=...
OPENWEATHER_API_KEY=...
MS_CLIENT_ID=...
MS_CLIENT_SECRET=...
MS_TENANT_ID=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=https://yourdomain.com/api/auth/google/callback
MICROSOFT_REDIRECT_URI=https://yourdomain.com/api/auth/microsoft/callback
```

---

## 🔧 Render Configuration File

Update `render.yaml` for automatic setup:

```yaml
services:
  - type: web
    name: victus
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    plan: free
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        value: sqlite:///./chat_history.db
      - key: ENVIRONMENT
        value: production
    healthCheckPath: /api/health
    autoDeploy: true
```

---

## ✅ Post-Deployment Checklist

1. **Test Your App**:
   - Visit: `https://yourdomain.com`
   - Check: `https://yourdomain.com/api/health`
   - Test: `https://yourdomain.com/docs` (API docs)

2. **Update OAuth Redirect URIs**:
   - Google: Update in Google Cloud Console
   - Microsoft: Update in Azure Portal
   - Use: `https://yourdomain.com/api/auth/{provider}/callback`

3. **Set Up Monitoring** (Optional):
   - UptimeRobot for uptime monitoring
   - Render dashboard for logs

4. **Share Your App**:
   - Share: `https://yourdomain.com`
   - Users can sign up and use immediately!

---

## 🎯 Summary: Best Free Option

**Render** is the best choice because:
- ✅ 100% free tier
- ✅ Custom domain included
- ✅ Free SSL
- ✅ Persistent storage
- ✅ Easy setup
- ✅ Auto-deploy

**Setup Time**: ~15 minutes
**Cost**: $0/month (free forever)
**Custom Domain**: Included (free)

---

## 🆘 Troubleshooting

### App won't start:
- Check logs in Render dashboard
- Verify environment variables
- Check build logs

### Custom domain not working:
- Verify DNS records (wait 24-48 hours for propagation)
- Check SSL certificate status in Render
- Ensure CNAME points to `victus.onrender.com`

### App sleeping:
- Use UptimeRobot to ping every 5 minutes
- Or upgrade to paid plan

### Build fails:
- Check Dockerfile
- Verify all dependencies in `pyproject.toml`
- Check build logs for errors

---

## 📞 Need Help?

1. Check Render docs: https://render.com/docs
2. Check Render status: https://status.render.com
3. Render community: https://community.render.com

**Your app will be live and shareable in ~15 minutes!** 🚀

