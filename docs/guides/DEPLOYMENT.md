# VICTUS Deployment Guide

## 🚫 Vercel Deployment - NOT Recommended

**Vercel is NOT suitable for this application** because:

1. **Stateful Application**: Loads ML models (Whisper, Piper TTS) into memory
2. **Persistent Storage**: Needs file system for uploads, FAISS index, audio files
3. **Long-running Processes**: Agent execution exceeds serverless time limits
4. **Memory Requirements**: ML models need significant RAM
5. **Database**: SQLite requires persistent volume

## ✅ Recommended Deployment Platforms

### 1. Railway (Easiest - Recommended)

**Why Railway:**
- ✅ One-click deployment
- ✅ Persistent volumes
- ✅ Automatic HTTPS
- ✅ Environment variables UI
- ✅ Free tier available

**Steps:**
1. Push code to GitHub
2. Go to [Railway](https://railway.app)
3. New Project → Deploy from GitHub
4. Select repository
5. Add environment variables from `.env.example`
6. Deploy!

**Configuration:**
- Uses `railway.json` (already created)
- Port: Railway sets `$PORT` automatically
- Database: SQLite works, or add PostgreSQL service

---

### 2. Render

**Why Render:**
- ✅ Docker support
- ✅ Persistent disks
- ✅ Auto-deploy from Git
- ✅ Free tier available

**Steps:**
1. Push code to GitHub
2. Go to [Render](https://render.com)
3. New Web Service → Connect GitHub
4. Select repository
5. Use `render.yaml` (already created) or configure:
   - Build Command: (auto-detected from Dockerfile)
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy!

**Configuration:**
- Uses `render.yaml` (already created)
- Health Check: `/api/health`
- Auto-deploy: Enabled

---

### 3. Fly.io

**Why Fly.io:**
- ✅ Global edge deployment
- ✅ Persistent volumes
- ✅ Great Docker support
- ✅ Free tier available

**Steps:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Initialize: `fly launch` (in project root)
4. Configure `fly.toml`:
   ```toml
   [build]
     dockerfile = "Dockerfile"
   
   [env]
     PORT = "8000"
   
   [[services]]
     internal_port = 8000
     protocol = "tcp"
   ```
5. Deploy: `fly deploy`

---

### 4. DigitalOcean App Platform

**Why DigitalOcean:**
- ✅ Managed platform
- ✅ Auto-scaling
- ✅ Database options
- ✅ Professional support

**Steps:**
1. Push code to GitHub
2. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
3. Create App → GitHub
4. Select repository
5. Configure:
   - Build Command: (auto from Dockerfile)
   - Run Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy!

---

## 📋 Pre-Deployment Checklist

### 1. Environment Variables
- [ ] Copy `.env.example` to `.env`
- [ ] Set `OPENAI_API_KEY`
- [ ] Generate secure `SECRET_KEY`: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure `CORS_ORIGINS` (remove `*` in production)
- [ ] Set OAuth redirect URIs to production URLs

### 2. Security
- [ ] Change default `SECRET_KEY`
- [ ] Set proper `CORS_ORIGINS` (not `*`)
- [ ] Enable rate limiting
- [ ] Review authentication settings
- [ ] Check file upload limits

### 3. Database
- [ ] For production, consider PostgreSQL instead of SQLite
- [ ] Run migrations: `alembic upgrade head`
- [ ] Backup database before deployment

### 4. Files
- [ ] Ensure `.dockerignore` is configured
- [ ] Remove unnecessary files from repository
- [ ] Check file permissions

### 5. Testing
- [ ] Run tests: `pytest`
- [ ] Test health endpoint: `/api/health`
- [ ] Test authentication flow
- [ ] Test file uploads

---

## 🔧 Production Configuration

### Environment Variables (Production)

```env
ENVIRONMENT=production
DEBUG=false

# Security
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://user:pass@host:5432/victus

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/victus.log

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

### Docker Production Build

```bash
# Build
docker build -t victus:latest .

# Run
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e SECRET_KEY=your_secret \
  -v $(pwd)/data:/app/data \
  --name victus \
  victus:latest
```

---

## 📊 Monitoring & Health Checks

### Health Endpoint
- URL: `/api/health`
- Returns: System status, model availability
- Use for: Load balancer health checks

### Metrics Endpoint
- URL: `/metrics` (Prometheus format)
- Returns: HTTP metrics, performance data
- Use for: Monitoring dashboards

### Logs
- Location: `logs/victus.log` (if configured)
- Format: Structured JSON logs
- Level: INFO in production

---

## 🚀 Quick Deploy Commands

### Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Render
```bash
# Deploy via Git push (auto-deploy enabled)
git push origin main
```

### Fly.io
```bash
fly deploy
```

---

## 🔍 Troubleshooting

### Application won't start
- Check environment variables
- Check logs: `docker logs victus` or platform logs
- Verify database connection
- Check port configuration

### Models not loading
- Check model files exist in `models/` directory
- Verify disk space
- Check memory limits

### Database errors
- Run migrations: `alembic upgrade head`
- Check database permissions
- Verify `DATABASE_URL` format

### CORS errors
- Update `CORS_ORIGINS` with exact domain
- Include protocol (https://)
- Remove trailing slashes

---

## 📝 Post-Deployment

1. **Test endpoints:**
   - Health: `https://yourdomain.com/api/health`
   - Docs: `https://yourdomain.com/docs`

2. **Update OAuth redirect URIs:**
   - Google: Update in Google Cloud Console
   - Microsoft: Update in Azure Portal

3. **Set up monitoring:**
   - Configure alerts
   - Set up log aggregation
   - Monitor metrics endpoint

4. **Backup strategy:**
   - Database backups
   - File uploads backup
   - Configuration backup

---

## 🎯 Recommended Setup

**For Production:**
1. **Platform**: Railway or Render (easiest)
2. **Database**: PostgreSQL (add as service)
3. **Storage**: Persistent volume for uploads
4. **Monitoring**: Platform metrics + Prometheus
5. **Backups**: Automated database backups

**For Development:**
- Local with Docker
- SQLite database
- All features enabled

---

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Fly.io Docs](https://fly.io/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

