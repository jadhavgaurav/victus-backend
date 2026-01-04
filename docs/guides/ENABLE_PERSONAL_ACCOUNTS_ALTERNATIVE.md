# Enable Personal Accounts - Alternative Methods

## Problem
Only two options are visible in "Supported account types":
1. "Accounts in this organizational directory only"
2. "Accounts in any organizational directory"

The third option (with personal accounts) is not showing.

---

## Solution 1: Check Manifest (Recommended)

### Step 1: Go to Manifest
1. In Azure Portal, stay on the **VICTUS AI ASSISTANT** app
2. Click **Manifest** (left sidebar, under "Manage")

### Step 2: Edit Manifest
1. You'll see a JSON editor
2. Look for: `"signInAudience"`
3. Change it to: `"AzureADandPersonalMicrosoftAccount"`
4. Click **Save**

### Current value might be:
```json
"signInAudience": "AzureADMultipleOrgs"
```

### Change to:
```json
"signInAudience": "AzureADandPersonalMicrosoftAccount"
```

### Step 3: Save and Test
1. Click **Save** at the top
2. Wait 2-3 minutes
3. Try login with personal account

---

## Solution 2: Check App Registration Type

The third option might not appear if:
- App was created as "Single tenant" initially
- App type needs to be changed

### Try This:
1. Go to **Overview** (left sidebar)
2. Check the **Application type**
3. If it says "Single tenant", you might need to recreate as multi-tenant
4. Or use Solution 1 (Manifest method) instead

---

## Solution 3: Use "Help me decide" Link

1. On the Authentication page
2. Click the **"Help me decide..."** link
3. It might show additional options or guidance
4. Follow the wizard to enable personal accounts

---

## Solution 4: Check if Option Appears After Saving

Sometimes the UI doesn't show all options until you interact with it:

1. Try clicking on the second option (even if already selected)
2. Then look again - third option might appear
3. Or try refreshing the page

---

## Manifest Method (Most Reliable)

### Step-by-Step:

1. **Go to Manifest:**
   - Azure Portal → App registrations → VICTUS AI ASSISTANT
   - Click **Manifest** (left sidebar)

2. **Find and Edit:**
   - Press Ctrl+F (or Cmd+F on Mac)
   - Search for: `signInAudience`
   - Change the value to: `"AzureADandPersonalMicrosoftAccount"`

3. **Before:**
   ```json
   "signInAudience": "AzureADMultipleOrgs"
   ```

4. **After:**
   ```json
   "signInAudience": "AzureADandPersonalMicrosoftAccount"
   ```

5. **Save:**
   - Click **Save** at the top
   - Wait 2-3 minutes

6. **Test:**
   - Try login with personal account

---

## Valid signInAudience Values

- `"AzureADMyOrg"` - Single tenant only
- `"AzureADMultipleOrgs"` - Work/school accounts (multitenant)
- `"AzureADandPersonalMicrosoftAccount"` - **Work/school + Personal accounts** ← Use this!
- `"PersonalMicrosoftAccount"` - Personal accounts only

---

## After Changing Manifest

✅ **Personal accounts** (@outlook.com, @hotmail.com) can login  
✅ **Gmail accounts** (linked to Microsoft) can login  
✅ **Work/School accounts** (@fynix.digital) can login  
✅ **Any Microsoft account** can login

---

## Troubleshooting

**"Manifest is read-only":**
- Make sure you're in edit mode
- Click "Edit" if there's an edit button

**"Still not working after manifest change":**
- Wait 5-10 minutes (manifest changes can take longer)
- Clear browser cache
- Try incognito window
- Verify the manifest saved correctly

**"Can't find signInAudience in manifest":**
- It should be near the top of the JSON
- Use Ctrl+F to search for it
- If missing, add it manually (but this is unusual)

