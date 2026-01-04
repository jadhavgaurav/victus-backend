# Microsoft OAuth Fix - Client Secret Required

## ❌ Current Error
```
AADSTS7000218: The request body must contain the following parameter: 'client_assertion' or 'client_secret'
```

## 🔍 Root Cause
Microsoft OAuth is failing because:
- **MS_CLIENT_SECRET is missing** from your `.env` file
- Web applications require a client secret for security
- The code is falling back to `PublicClientApplication` which doesn't work for web apps

## ✅ Solution: Add Client Secret

### Step 1: Get Client Secret from Azure Portal

1. **Go to Azure Portal**: https://portal.azure.com
2. **Navigate to**: Azure Active Directory → App registrations
3. **Select your app**: "VICTUS AI ASSISTANT"
4. **Go to**: "Certificates & secrets" (in the left menu)
5. **Create a new secret**:
   - Click "New client secret"
   - Add a description (e.g., "Web App Secret")
   - Choose expiration (recommend 24 months)
   - Click "Add"
6. **Copy the secret value immediately** (you won't see it again!)
   - ⚠️ **IMPORTANT**: Copy the VALUE, not the Secret ID

### Step 2: Update Your .env File

Add the client secret to your `.env` file:

```env
MS_CLIENT_ID=your_client_id_here
MS_CLIENT_SECRET=the_secret_value_you_copied
MS_TENANT_ID=your_tenant_id_here
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/auth/microsoft/callback
```

### Step 3: Verify Azure Portal Settings

In Azure Portal → Authentication:

1. **Platform Configuration**:
   - Make sure you have a **"Web"** platform (not just Mobile/Desktop)
   - Redirect URI: `http://localhost:8000/api/auth/microsoft/callback`

2. **Advanced Settings**:
   - "Allow public client flows" can be **Yes** or **No** (doesn't matter for web apps with secret)
   - We're using `ConfidentialClientApplication` which works regardless

### Step 4: Restart Your Server

```bash
poetry run uvicorn src.main:app --reload
```

## 🔧 How It Works Now

The code automatically:
1. Checks if `MS_CLIENT_SECRET` exists
2. Uses `ConfidentialClientApplication` (with secret) - ✅ For web apps
3. Falls back to `PublicClientApplication` (no secret) - ❌ Won't work for web apps

## ✅ After Adding Secret

Once you add `MS_CLIENT_SECRET` to `.env`:
- Microsoft OAuth will use `ConfidentialClientApplication`
- The error `AADSTS7000218` will be resolved
- Microsoft login will work correctly

## 📝 Quick Checklist

- [ ] Client secret created in Azure Portal
- [ ] Secret VALUE copied (not Secret ID)
- [ ] `MS_CLIENT_SECRET` added to `.env` file
- [ ] Server restarted
- [ ] Test Microsoft OAuth login

---

**Note**: If you lose the secret value, you'll need to create a new one in Azure Portal.

