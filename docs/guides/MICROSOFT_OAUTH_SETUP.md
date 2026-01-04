# Microsoft OAuth Setup Guide

## Quick Setup Steps

### 1. Get Your Client Secret from Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure Active Directory** → **App registrations**
3. Find your app: **VICTUS AI ASSISTANT** (or the app with Client ID: `dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed`)
4. Go to: **Certificates & secrets**
5. Click: **New client secret**
6. Add description: "Web App Secret"
7. Choose expiration: **24 months** (recommended)
8. Click: **Add**
9. **IMPORTANT**: Copy the **VALUE** immediately (you won't see it again!)
10. Paste it into your `.env` file as `MS_CLIENT_SECRET`

### 2. Update Your .env File

Add this line to your `.env` file:

```env
MS_CLIENT_SECRET=your_secret_value_here
```

### 3. Verify Configuration

Your `.env` should have:

```env
# Microsoft OAuth
MS_CLIENT_ID=dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed
MS_CLIENT_SECRET=your_secret_value_here
MS_TENANT_ID=573ff913-268d-4753-a455-703d328a45b2
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/auth/microsoft/callback
```

### 4. Restart Server

After adding the secret, restart your server:

```bash
# Stop server (Ctrl+C)
poetry run uvicorn src.main:app --reload
```

### 5. Test

1. Go to login page
2. Click "Sign in with Microsoft"
3. Should redirect to Microsoft login (no error!)

---

## Current Configuration Status

✅ **MS_CLIENT_ID**: Set  
✅ **MS_TENANT_ID**: Set  
❌ **MS_CLIENT_SECRET**: **MISSING** ← You need to add this!  
✅ **MICROSOFT_REDIRECT_URI**: Set

---

## Troubleshooting

**"Microsoft OAuth not configured" error:**
- Make sure `MS_CLIENT_SECRET` is in `.env` file
- No quotes around the value
- Restart server after adding

**"Invalid client secret" error:**
- Secret might be expired
- Create a new secret in Azure Portal
- Update `.env` with new value

**Redirect URI mismatch:**
- Make sure redirect URI in Azure matches exactly:
  - `http://localhost:8000/api/auth/microsoft/callback`
- Go to Azure Portal → App registrations → Your app → Authentication
- Add the redirect URI if missing

---

## Security Notes

⚠️ **Never commit `.env` file to git!**
- The `.env` file should be in `.gitignore`
- Client secrets are sensitive credentials

🔒 **For Production:**
- Use environment variables instead of `.env` file
- Rotate secrets regularly
- Use shorter expiration times (90 days recommended)

