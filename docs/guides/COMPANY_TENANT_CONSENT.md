# Grant Admin Consent for Company Tenant (Fynix Digital)

## Problem
- Admin consent was granted for "MSFT" tenant ✅
- But your company account is in "Fynix Digital" tenant
- Need to grant consent for **Fynix Digital** tenant

---

## Solution: Grant Consent for Fynix Digital Tenant

### Option 1: Direct URL (Easiest)

1. **Get your Fynix Digital Tenant ID:**
   - Go to Azure Portal
   - Switch to Fynix Digital tenant (if you have access)
   - Azure AD → Overview → Copy "Tenant ID"

2. **Use this URL** (replace `FYNIX_TENANT_ID` with actual tenant ID):
   ```
   https://login.microsoftonline.com/FYNIX_TENANT_ID/adminconsent?client_id=dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed
   ```

3. **Or use common** (works for any tenant):
   ```
   https://login.microsoftonline.com/common/adminconsent?client_id=dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed
   ```

4. **Make sure you're logged in with a Fynix Digital admin account**

5. Click **Accept**

---

### Option 2: Via Azure Portal (Fynix Digital Tenant)

1. **Switch to Fynix Digital Tenant:**
   - In Azure Portal, click your profile (top right)
   - Click "Switch directory"
   - Select "Fynix Digital" tenant

2. **Navigate to App Registrations:**
   - Azure Active Directory → App registrations
   - Search for: **VICTUS AI ASSISTANT**
   - If it doesn't exist, you need to add it first (see below)

3. **Grant Admin Consent:**
   - Click on the app
   - Go to: **API permissions**
   - Click: **"Grant admin consent for Fynix Digital"**
   - Click **Yes**

---

### Option 3: If App Doesn't Exist in Fynix Digital Tenant

If "VICTUS AI ASSISTANT" doesn't appear in Fynix Digital tenant:

#### Option A: Add Multi-Tenant App (Recommended)

1. In **MSFT tenant** (where app exists):
   - Go to App registrations → VICTUS AI ASSISTANT
   - Go to **Authentication**
   - Under "Supported account types", select:
     - ✅ **"Accounts in any organizational directory and personal Microsoft accounts"**
   - Save

2. Then use the direct URL method (Option 1) to grant consent in Fynix Digital

#### Option B: Create App in Fynix Digital Tenant

1. Switch to Fynix Digital tenant in Azure Portal
2. Create new app registration: **VICTUS AI ASSISTANT**
3. Use same Client ID (if possible) or configure separately
4. Add same API permissions
5. Grant admin consent

---

## Quick Steps Summary

1. **Make sure app is multi-tenant:**
   - MSFT tenant → App registrations → VICTUS AI ASSISTANT
   - Authentication → "Accounts in any organizational directory"

2. **Grant consent for Fynix Digital:**
   - Login to Azure Portal with **Fynix Digital admin account**
   - Use direct URL: `https://login.microsoftonline.com/common/adminconsent?client_id=dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed`
   - Or: Switch to Fynix Digital tenant → App registrations → Grant consent

3. **Test:**
   - Logout from app
   - Login with `gaurav@fynix.digital`
   - Should work now! ✅

---

## Important Notes

- **Different Tenants = Separate Consent:**
  - MSFT tenant consent ≠ Fynix Digital tenant consent
  - Each tenant needs its own admin consent

- **Multi-Tenant App:**
  - App must be configured as multi-tenant
  - Then each tenant can grant its own consent

- **Admin Rights:**
  - You need to be a **Global Administrator** in Fynix Digital tenant
  - Or have permission to grant admin consent

---

## Troubleshooting

**"Can't find app in Fynix Digital tenant":**
- App might not be visible if it's not multi-tenant
- Use direct URL method instead
- Or contact Fynix Digital admin to grant consent

**"Don't have admin rights in Fynix Digital":**
- Contact your Fynix Digital IT admin
- Ask them to grant admin consent using the direct URL
- Provide them with: Client ID: `dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed`

**"Still getting admin approval":**
- Wait 5-10 minutes for changes to propagate
- Clear browser cache
- Try incognito/private window

