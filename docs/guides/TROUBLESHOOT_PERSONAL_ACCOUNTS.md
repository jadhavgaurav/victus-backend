# Troubleshooting: Personal Accounts Still Not Working

## Current Status
✅ Manifest has correct settings:
- `"signInAudience": "AzureADandPersonalMicrosoftAccount"`
- `"accessTokenAcceptedVersion": 2`

But personal accounts still not working.

---

## Troubleshooting Steps

### Step 1: Verify Manifest Saved
1. **Refresh the page** in Azure Portal
2. Go back to **Manifest**
3. **Check if both properties are still there:**
   - `"signInAudience": "AzureADandPersonalMicrosoftAccount"`
   - `"accessTokenAcceptedVersion": 2`
4. If they're missing, add them again and save

### Step 2: Wait Longer
- Manifest changes can take **5-10 minutes** to fully propagate
- Sometimes takes up to **15 minutes**
- Be patient and wait

### Step 3: Clear Browser Cache
1. **Clear browser cache and cookies**
2. Or use **incognito/private window**
3. Try login again

### Step 4: Check Authentication Page
1. Go to **Authentication** (left sidebar)
2. Check if "Supported account types" now shows 3 options
3. If yes, select the third option
4. Click **Save**

### Step 5: Verify Gmail is Linked to Microsoft
1. Go to [Microsoft Account](https://account.microsoft.com)
2. Try signing in with your Gmail
3. If it works, it's linked ✅
4. If not, you need to link it first

### Step 6: Try Different Personal Account
Test with a known personal Microsoft account:
- `@outlook.com`
- `@hotmail.com`
- `@live.com`

If these work but Gmail doesn't, the Gmail might not be properly linked.

---

## Alternative: Check Token Configuration

### Step 1: Go to Token Configuration
1. In Azure Portal, go to **Token configuration** (left sidebar)
2. Check **Access token version**
3. Should be set to **"2"** or **"v2.0"**

### Step 2: Update if Needed
1. If it's not set to version 2, change it
2. Click **Save**
3. Wait 2-3 minutes

---

## Verify All Settings

### Checklist:
- [ ] Manifest: `signInAudience` = `"AzureADandPersonalMicrosoftAccount"`
- [ ] Manifest: `accessTokenAcceptedVersion` = `2`
- [ ] Token Configuration: Access token version = `2`
- [ ] Authentication: Supported account types = (check if 3 options now appear)
- [ ] Waited 5-10 minutes after changes
- [ ] Cleared browser cache
- [ ] Gmail is linked to Microsoft account

---

## Still Not Working?

### Option 1: Use Outlook Account Instead
Create a free Outlook account:
1. Go to [Outlook.com](https://outlook.com)
2. Create account with your Gmail
3. Use that to login

### Option 2: Check App Registration Type
1. Go to **Overview** (left sidebar)
2. Check if app type allows personal accounts
3. Might need to recreate app with different settings

### Option 3: Contact Support
If nothing works, there might be a tenant-level restriction preventing personal accounts.

---

## Quick Test

1. **Wait 10 minutes** after saving manifest
2. **Clear browser cache**
3. **Try login with:**
   - `@outlook.com` account (if you have one)
   - Or create a test Outlook account
4. If Outlook works but Gmail doesn't → Gmail linking issue
5. If nothing works → Wait longer or check tenant settings

