# Google OAuth Configuration Guide

## Step-by-Step Setup

Based on your current Google Cloud Console session, here's the complete configuration process:

---

## Step 1: Create OAuth Client ID in Google Cloud Console

You're already on the right page! Here's what to fill in:

### In the "Create OAuth client ID" form:

1. **Application type**: 
   - ✅ Select **"Web application"** (you already have this selected)

2. **Name**: 
   - Enter a descriptive name like: `Project VICTUS Web Client`
   - Or keep the default: `Web client 1`

3. **Authorized JavaScript origins**:
   - Click **"+ Add URI"**
   - Add: `http://localhost:8000`
   - (For production, add your production domain with HTTPS)

4. **Authorized redirect URIs**:
   - Click **"+ Add URI"**
   - Add: `http://localhost:8000/api/auth/google/callback`
   - ⚠️ **IMPORTANT**: This must match exactly, including the path!

5. Click **"Create"** button

---

## Step 2: Copy Your Credentials

After clicking "Create", Google will show you:

- **Your Client ID** (looks like: `123456789-abcdefghijklmnop.apps.googleusercontent.com`)
- **Your Client Secret** (looks like: `GOCSPX-abcdefghijklmnopqrstuvwxyz`)

**⚠️ IMPORTANT**: Copy these immediately - you won't be able to see the secret again!

---

## Step 3: Configure OAuth Consent Screen (If Not Done)

Before OAuth works, you need to configure the consent screen:

1. In Google Cloud Console, go to **"OAuth consent screen"** (in the left menu)
2. Choose **"External"** (unless you have a Google Workspace)
3. Fill in required fields:
   - **App name**: `Project VICTUS`
   - **User support email**: Your email
   - **Developer contact information**: Your email
4. Click **"Save and Continue"**
5. **Scopes**: Click "Add or Remove Scopes"
   - Add: `.../auth/userinfo.email`
   - Add: `.../auth/userinfo.profile`
   - Add: `openid`
6. Click **"Save and Continue"**
7. **Test users** (for development): Add your email
8. Click **"Save and Continue"**

---

## Step 4: Add Credentials to .env File

Open your `.env` file and add:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

**Example:**
```env
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

---

## Step 5: Verify Configuration

### Check Your .env File

Make sure your `.env` has:
```env
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

### Test the Configuration

1. Start your application:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

2. Visit: `http://localhost:8000/login`

3. Click **"Sign in with Google"** button

4. You should be redirected to Google's login page

5. After logging in, you'll be redirected back to the app

---

## Common Issues & Solutions

### Issue 1: "redirect_uri_mismatch" Error

**Problem**: The redirect URI doesn't match exactly.

**Solution**:
- Check that `GOOGLE_REDIRECT_URI` in `.env` matches exactly what you entered in Google Console
- Must be: `http://localhost:8000/api/auth/google/callback` (no trailing slash)
- Check for typos or extra spaces

### Issue 2: "OAuth client not found"

**Problem**: Client ID is incorrect.

**Solution**:
- Double-check the Client ID in `.env`
- Make sure there are no extra spaces
- Verify in Google Console that the client exists

### Issue 3: "Invalid client secret"

**Problem**: Client Secret is incorrect or expired.

**Solution**:
- If you lost the secret, you need to create a new OAuth client
- Or reset the secret in Google Console (Credentials > Your Client > Reset Secret)

### Issue 4: "Access blocked: This app's request is invalid"

**Problem**: OAuth consent screen not configured or app in testing mode.

**Solution**:
- Complete the OAuth consent screen setup
- Add your email as a test user
- Wait a few minutes for changes to propagate

---

## Production Configuration

For production deployment:

1. **Update Redirect URI**:
   ```env
   GOOGLE_REDIRECT_URI=https://yourdomain.com/api/auth/google/callback
   ```

2. **Add Production URIs in Google Console**:
   - Authorized JavaScript origins: `https://yourdomain.com`
   - Authorized redirect URIs: `https://yourdomain.com/api/auth/google/callback`

3. **Publish Your App** (if ready):
   - In OAuth consent screen, click "PUBLISH APP"
   - This allows any Google user to sign in

---

## Quick Reference

### Required Google Console Settings:
- **Application type**: Web application
- **Authorized redirect URI**: `http://localhost:8000/api/auth/google/callback`
- **Scopes**: 
  - `openid`
  - `.../auth/userinfo.email`
  - `.../auth/userinfo.profile`

### Required .env Variables:
```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

---

## Testing Checklist

- [ ] OAuth client created in Google Console
- [ ] Redirect URI added: `http://localhost:8000/api/auth/google/callback`
- [ ] OAuth consent screen configured
- [ ] Test user added (your email)
- [ ] Credentials added to `.env` file
- [ ] Application restarted after .env changes
- [ ] Can click "Sign in with Google" button
- [ ] Redirected to Google login
- [ ] Successfully redirected back to app
- [ ] User created/logged in successfully

---

## Need Help?

If you encounter issues:
1. Check the browser console for errors
2. Check server logs for detailed error messages
3. Verify all URIs match exactly
4. Wait a few minutes after making changes in Google Console

---

**Once configured, users can sign in with their Google accounts!** 🎉

