# Grant Admin Consent - Step by Step

## Problem
- Admin account (`gaurav@wqs42.onmicrosoft.com`) logs in successfully
- Company account (`gaurav@fynix.digital`) still shows "Need admin approval"
- **Solution**: Grant admin consent via Azure Portal

---

## Step-by-Step: Grant Admin Consent

### Method 1: Via Azure Portal (Recommended)

#### Step 1: Go to Azure Portal
1. Open [Azure Portal](https://portal.azure.com)
2. Make sure you're logged in with: **`gaurav@wqs42.onmicrosoft.com`** (admin account)

#### Step 2: Navigate to App Registrations
1. Click on **Azure Active Directory** (or search for it)
2. In the left sidebar, click **App registrations**
3. Find and click on: **VICTUS AI ASSISTANT**

#### Step 3: Go to API Permissions
1. In the left sidebar, click **API permissions**
2. You should see these permissions:
   - ✅ Microsoft Graph
     - User.Read (Delegated)
     - Mail.ReadWrite (Delegated) ⚠️ **Requires admin consent**
     - Mail.Send (Delegated) ⚠️ **Requires admin consent**
     - Calendars.ReadWrite (Delegated) ⚠️ **Requires admin consent**

#### Step 4: Grant Admin Consent
1. Look at the top of the page
2. Click the button: **"Grant admin consent for [Your Organization Name]"**
   - This button is usually at the top, next to "Add a permission"
3. Click **Yes** to confirm
4. Wait a few seconds for it to process

#### Step 5: Verify
1. After granting consent, you should see:
   - Status changes to: **"Granted for [Organization]"** ✅
   - Green checkmarks next to all permissions
2. All permissions should show: **"Granted for [Your Organization]"**

#### Step 6: Test Company Account
1. Logout from the app
2. Login again with Microsoft OAuth
3. Select: **`gaurav@fynix.digital`** (company account)
4. Should work now! ✅

---

## Method 2: Via Direct URL (Quick)

1. Make sure you're logged into Azure Portal with admin account
2. Go to this URL (replace `YOUR_TENANT_ID` with your tenant ID):
   ```
   https://login.microsoftonline.com/YOUR_TENANT_ID/adminconsent?client_id=dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed
   ```
3. Or use this simpler URL:
   ```
   https://login.microsoftonline.com/common/adminconsent?client_id=dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed
   ```
4. Click **Accept** when prompted

---

## Method 3: Enterprise Applications

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure Active Directory** → **Enterprise applications**
3. Search for: **VICTUS AI ASSISTANT**
4. If it appears, click on it
5. Go to: **Permissions**
6. Click: **Grant admin consent**

---

## What to Look For

### Before Admin Consent:
- Status: "Not granted" or "Consent required"
- Company account: Shows "Need admin approval"

### After Admin Consent:
- Status: "Granted for [Organization]" ✅
- All permissions have green checkmarks
- Company account: Works without approval

---

## Troubleshooting

**"Grant admin consent" button is grayed out:**
- You need to be a **Global Administrator** or have **Privileged Role Administrator** role
- Check your role: Azure AD → Roles and administrators → Check if you're Global Admin

**"Can't find the app in Enterprise applications":**
- That's okay! Use Method 1 (API Permissions) instead

**"Still getting admin approval after granting consent":**
- Wait 2-3 minutes for changes to propagate
- Clear browser cache and try again
- Make sure you granted consent for the **correct tenant**

**"Which tenant should I grant consent for?"**
- Grant consent in the tenant where your company account is (`fynix.digital` tenant)
- If you're not sure, grant consent in both tenants (admin tenant and company tenant)

---

## Quick Checklist

- [ ] Logged into Azure Portal with admin account
- [ ] Navigated to App registrations → VICTUS AI ASSISTANT
- [ ] Went to API permissions
- [ ] Clicked "Grant admin consent for [Organization]"
- [ ] Verified all permissions show "Granted"
- [ ] Tested login with company account

---

## After Granting Consent

✅ All users in your organization can use the app  
✅ No individual consent needed  
✅ Company account (`gaurav@fynix.digital`) will work  
✅ M365 tools (email, calendar) will work for all users

