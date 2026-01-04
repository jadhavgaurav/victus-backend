# Allow Personal Microsoft Accounts

## Problem
Error: "You can't sign in here with a personal account. Use your work or school account instead."

This happens when the app registration is configured to **only** allow work/school accounts.

---

## Solution: Enable Personal Accounts in Azure Portal

### Step 1: Go to Azure Portal
1. Open [Azure Portal](https://portal.azure.com)
2. Make sure you're logged in with your **admin account** (`gaurav@wqs42.onmicrosoft.com`)

### Step 2: Navigate to App Registration
1. Go to: **Azure Active Directory** → **App registrations**
2. Find and click: **VICTUS AI ASSISTANT**

### Step 3: Change Supported Account Types
1. Click **Authentication** (left sidebar)
2. Scroll down to **"Supported account types"**
3. **Change the selection to:**
   - ✅ **"Accounts in any organizational directory and personal Microsoft accounts (e.g. Skype, Xbox)"**
   - This allows BOTH work/school AND personal accounts

### Step 4: Save
1. Click **Save** at the top
2. Wait a few seconds for changes to apply

### Step 5: Test
1. Logout from the app
2. Try logging in with Microsoft OAuth again
3. Now you can use:
   - ✅ Personal accounts (@outlook.com, @hotmail.com, @gmail.com with Microsoft account)
   - ✅ Work/School accounts (@fynix.digital, etc.)

---

## Important Notes

### Personal Microsoft Accounts
- Gmail accounts (`@gmail.com`) can be used **if** they're linked to a Microsoft account
- To link Gmail to Microsoft:
  1. Go to [Microsoft Account](https://account.microsoft.com)
  2. Sign in with your Gmail
  3. If not linked, create a Microsoft account using your Gmail

### Or Use Outlook/Hotmail
- Personal Microsoft accounts are typically:
  - `@outlook.com`
  - `@hotmail.com`
  - `@live.com`
  - `@msn.com`

---

## Quick Checklist

- [ ] Go to Azure Portal → App registrations → VICTUS AI ASSISTANT
- [ ] Click **Authentication**
- [ ] Change "Supported account types" to **"Accounts in any organizational directory and personal Microsoft accounts"**
- [ ] Click **Save**
- [ ] Test login with personal account

---

## After Enabling Personal Accounts

✅ **Personal accounts** (@outlook.com, @hotmail.com) can login  
✅ **Work/School accounts** (@fynix.digital) can login  
✅ **Gmail accounts** (if linked to Microsoft) can login  
✅ **Any Microsoft account** can login

---

## Troubleshooting

**"Still showing error after changing":**
- Wait 2-3 minutes for changes to propagate
- Clear browser cache
- Try incognito/private window
- Make sure you clicked "Save" in Azure Portal

**"Gmail account still not working":**
- Gmail accounts need to be linked to Microsoft account first
- Or use an Outlook/Hotmail account instead
- Or create a new Microsoft account with your Gmail

**"Want to restrict to work/school only":**
- Keep current setting: "Accounts in this organizational directory only"
- Or: "Accounts in any organizational directory" (work/school only, no personal)

