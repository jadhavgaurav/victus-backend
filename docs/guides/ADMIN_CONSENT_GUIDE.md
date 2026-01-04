# Admin Consent Guide for Microsoft OAuth

## Current Situation

You have two accounts:
1. **Admin Account**: `gaurav@wqs42.onmicrosoft.com` ← Use this FIRST
2. **Company Account**: `gaurav@fynix.digital` ← Use this AFTER admin consent

## Problem

The app requires **admin consent** because it requests permissions like:
- `Mail.ReadWrite` (read/write emails)
- `Mail.Send` (send emails)
- `Calendars.ReadWrite` (read/write calendar)

These are **privileged permissions** that need admin approval.

## Solution: Grant Admin Consent

### Step 1: Login with Admin Account FIRST

1. On the "Pick an account" screen, select:
   - **`gaurav@wqs42.onmicrosoft.com`** (the admin account)

2. You'll be asked to grant permissions - **Click "Accept"** or "Consent"

3. This grants admin consent for the entire organization

### Step 2: After Admin Consent

Once admin consent is granted:
- ✅ All users in your organization can use the app
- ✅ You can login with `gaurav@fynix.digital` (company account)
- ✅ No more "Need admin approval" messages

### Step 3: Login with Company Account

1. Logout from the admin account
2. Login again with Microsoft OAuth
3. Select: **`gaurav@fynix.digital`** (company account)
4. Should work without admin approval!

---

## Alternative: Grant Admin Consent via Azure Portal

If you prefer to grant consent via Azure Portal:

### Method 1: API Permissions (Recommended)

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure Active Directory** → **App registrations**
3. Find: **VICTUS AI ASSISTANT**
4. Go to: **API permissions**
5. Click: **Grant admin consent for [Your Organization]**
6. Click **Yes** to confirm

### Method 2: Enterprise Applications

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure Active Directory** → **Enterprise applications**
3. Find: **VICTUS AI ASSISTANT** (if it appears)
4. Go to: **Permissions**
5. Click: **Grant admin consent**

---

## What Happens After Admin Consent?

✅ **All users** in your organization can use the app  
✅ **No individual consent** needed for each user  
✅ **Company account** (`gaurav@fynix.digital`) will work  
✅ **M365 tools** (email, calendar) will work for all users

---

## Quick Steps Summary

1. **Now**: Select `gaurav@wqs42.onmicrosoft.com` (admin account)
2. **Grant permissions**: Click "Accept" when prompted
3. **Later**: You can use `gaurav@fynix.digital` (company account)

---

## Troubleshooting

**"Still asking for admin approval":**
- Make sure you granted consent with the admin account
- Check Azure Portal → API permissions → Verify "Granted for [Organization]"

**"Can't see admin consent option":**
- You need to be a Global Administrator or have permission to grant consent
- Contact your Azure AD admin if you don't have permissions

