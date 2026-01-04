# Fix: Enable Personal Microsoft Accounts

## Current Problem
Your app is set to: **"Accounts in any organizational directory (Multitenant)"**
- ✅ Allows: Work/School accounts (@fynix.digital, etc.)
- ❌ Blocks: Personal Microsoft accounts (@outlook.com, @gmail.com linked to Microsoft)

---

## Solution: Change to Allow Personal Accounts

### Step 1: In Azure Portal (Authentication Page)
You're already on the right page! Now:

1. **Find "Supported account types" section**
2. **Look for the third option:**
   - "Accounts in any organizational directory and personal Microsoft accounts (e.g. Skype, Xbox)"
3. **Click on this option** (the third radio button)
4. **Click "Save"** at the bottom of the page
5. **Wait 2-3 minutes** for changes to propagate

---

## What Each Option Means

### Option 1: "Accounts in this organizational directory only"
- ✅ Only your specific tenant (MSFT)
- ❌ No other tenants
- ❌ No personal accounts

### Option 2: "Accounts in any organizational directory" (Currently Selected)
- ✅ Any work/school account from any organization
- ❌ **NO personal accounts** ← This is why Gmail isn't working!

### Option 3: "Accounts in any organizational directory and personal Microsoft accounts" ← **SELECT THIS**
- ✅ Any work/school account
- ✅ Personal Microsoft accounts (@outlook.com, @hotmail.com)
- ✅ Gmail accounts linked to Microsoft
- ✅ **This is what you need!**

---

## Step-by-Step Instructions

1. **On the Authentication page** (where you are now)
2. **Scroll to "Supported account types"**
3. **Click the THIRD radio button:**
   - "Accounts in any organizational directory and personal Microsoft accounts (e.g. Skype, Xbox)"
4. **Scroll down and click "Save"**
5. **Wait 2-3 minutes**
6. **Test login with your Gmail account**

---

## After Changing

✅ **Personal accounts** (@outlook.com, @hotmail.com) can login  
✅ **Gmail accounts** (linked to Microsoft) can login  
✅ **Work/School accounts** (@fynix.digital) can login  
✅ **Any Microsoft account** can login

---

## About Gmail + Microsoft Account

If your Gmail is linked to a Microsoft account:
- You can use your Gmail email to sign in
- Microsoft will recognize it as a personal account
- After enabling the third option, it should work!

**To verify your Gmail is linked:**
1. Go to [Microsoft Account](https://account.microsoft.com)
2. Try signing in with your Gmail
3. If it works, it's linked ✅

---

## Troubleshooting

**"Still not working after changing":**
- Wait 5-10 minutes (sometimes takes longer)
- Clear browser cache completely
- Try incognito/private window
- Make sure you clicked "Save" and it saved successfully

**"Gmail still shows error":**
- Verify Gmail is linked to Microsoft account
- Try using @outlook.com account instead to test
- Check if you're using the correct Gmail address

**"Can't find the third option":**
- Make sure you're in the "Authentication" page
- Scroll down to "Supported account types"
- Look for all three radio button options

