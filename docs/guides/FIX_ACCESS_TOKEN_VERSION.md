# Fix: Access Token Version Required

## Error Message
"Unable to change signinAudience to AzureADandPersonalMicrosoftAccount. Application must accept Access Token Version 2."

## Problem
To enable personal accounts, the app **must** have `AccessTokenAcceptedVersion` set to `2`.

---

## Solution: Add AccessTokenAcceptedVersion

### Step 1: In the Manifest Editor
You're already in the manifest - perfect!

### Step 2: Find the Right Location
Look for the `"api"` section or add it near the top level of the JSON.

### Step 3: Add AccessTokenAcceptedVersion
Add this property to your manifest:

```json
"accessTokenAcceptedVersion": 2
```

### Step 4: Complete Manifest Structure
Your manifest should have both:

```json
{
  "signInAudience": "AzureADandPersonalMicrosoftAccount",
  "accessTokenAcceptedVersion": 2,
  ...
}
```

### Step 5: Save
1. Click **Save** at the top
2. The error should be resolved
3. Wait 2-3 minutes

---

## Where to Add It

### Option 1: Top Level (Recommended)
Add it near `signInAudience`:

```json
{
  "signInAudience": "AzureADandPersonalMicrosoftAccount",
  "accessTokenAcceptedVersion": 2,
  "identifierUris": [],
  ...
}
```

### Option 2: In the "api" Section
If there's an `"api"` section, you can add it there, but top level is preferred.

---

## Complete Example

```json
{
  "id": "dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed",
  "appId": "dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed",
  "signInAudience": "AzureADandPersonalMicrosoftAccount",
  "accessTokenAcceptedVersion": 2,
  "identifierUris": [],
  ...
}
```

---

## Steps Summary

1. **In Manifest editor**, find a good spot (near `signInAudience` or top level)
2. **Add this line:**
   ```json
   "accessTokenAcceptedVersion": 2,
   ```
3. **Make sure** `signInAudience` is still set to `"AzureADandPersonalMicrosoftAccount"`
4. **Click Save**
5. **Wait 2-3 minutes**
6. **Test login with personal account**

---

## Important Notes

- `accessTokenAcceptedVersion` must be `2` (number, not string)
- `signInAudience` must be `"AzureADandPersonalMicrosoftAccount"` (string)
- Both properties are required together
- Save both changes at the same time

---

## After Fixing

✅ Personal accounts (@outlook.com, @hotmail.com) can login  
✅ Gmail accounts (linked to Microsoft) can login  
✅ Work/School accounts (@fynix.digital) can login  
✅ Any Microsoft account can login

