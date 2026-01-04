# Microsoft OAuth Configuration Verification

## ✅ Your Current Configuration

Based on your Microsoft Entra admin center setup:

### Web Redirect URIs:
- ✅ `http://localhost:8000/api/auth/microsoft/callback` - **CORRECT!**
- ⚠️ `http://localhost` - Not needed (can be removed)

### Status: **CORRECT** ✅

The redirect URI `http://localhost:8000/api/auth/microsoft/callback` matches exactly what the code expects!

---

## What You Need to Do

### 1. Keep the Correct URI
- ✅ **Keep**: `http://localhost:8000/api/auth/microsoft/callback`
- ❌ **Remove**: `http://localhost` (not needed, can cause confusion)

### 2. About the Warning
The warning says: *"This app has implicit grant settings enabled. If you are using any of these URIs in a SPA with MSAL.js 2.0, you should migrate URIs."*

**For our use case**: This warning is **OK to ignore** because:
- We're using a web application (not a SPA)
- We're using the authorization code flow (not implicit grant)
- The code uses `PublicClientApplication` which handles this correctly

### 3. Additional Settings to Check

Make sure these are configured:

1. **Platform Type**: Should be "Web"
2. **Supported Account Types**: Should allow your organization (or all)
3. **ID Tokens**: Should be enabled (for authentication)

---

## Complete Configuration Checklist

### In Microsoft Entra Admin Center:

- [x] **Redirect URI Added**: `http://localhost:8000/api/auth/microsoft/callback` ✅
- [ ] **Platform Type**: Web application
- [ ] **ID Tokens**: Enabled (check in "Implicit grant and hybrid flows")
- [ ] **Supported Account Types**: Configured correctly

### In Your .env File:

Add this (if not already present):

```env
# Microsoft OAuth (uses existing MS_CLIENT_ID and MS_TENANT_ID)
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/auth/microsoft/callback
```

**Note**: Your `MS_CLIENT_ID` and `MS_TENANT_ID` are already configured, which is perfect!

---

## Testing

1. **Click "Save"** in the Microsoft Entra admin center

2. **Add to .env** (if not already there):
   ```env
   MICROSOFT_REDIRECT_URI=http://localhost:8000/api/auth/microsoft/callback
   ```

3. **Restart your application**:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

4. **Test**:
   - Visit: `http://localhost:8000/login`
   - Click "Sign in with Microsoft"
   - Should redirect to Microsoft login
   - After login, redirects back to app

---

## Summary

✅ **Your configuration is CORRECT!**

The redirect URI `http://localhost:8000/api/auth/microsoft/callback` is exactly what's needed.

**Optional cleanup**: You can remove `http://localhost` if you want, but it won't cause issues if left there.

**Next step**: Click "Save" in the Microsoft Entra admin center, and you're ready to test!

