# Fix: Microsoft OAuth Multi-Tenant Configuration

## Problem
Error: "Application with identifier 'dd0f2824-3ec3-4b80-90a3-a9fcd34be3ed' was not found in the directory 'Fynix Digital'"

This happens when trying to login with a company email from a different tenant than where the app is registered.

## Solution: Enable Multi-Tenant in Azure Portal

### Step 1: Go to Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure Active Directory** → **App registrations**
3. Find your app: **VICTUS AI ASSISTANT**

### Step 2: Configure Multi-Tenant
1. Click on your app
2. Go to **Authentication** (left sidebar)
3. Under **Supported account types**, select:
   - ✅ **Accounts in any organizational directory and personal Microsoft accounts (e.g. Skype, Xbox)**
   - This enables multi-tenant access

### Step 3: Update Redirect URIs
Make sure these redirect URIs are added:
- `http://localhost:8000/api/auth/microsoft/callback`
- (Add production URL when deploying)

### Step 4: Verify .env Configuration
Your `.env` should have:
```env
MS_TENANT_ID=common
```
This is correct for multi-tenant! ✅

### Step 5: Restart Server
```bash
poetry run uvicorn src.main:app --reload
```

## After Configuration

Users from **any Microsoft tenant** can login:
- ✅ Personal Microsoft accounts (@outlook.com, @hotmail.com)
- ✅ Work/School accounts from any organization (like @fynix.digital)
- ✅ Your original tenant

## Alternative: Single Tenant (If You Only Want Your Company)

If you ONLY want users from "Fynix Digital" tenant:

1. In Azure Portal → Authentication:
   - Select: **Accounts in this organizational directory only**
   
2. Update `.env`:
   ```env
   MS_TENANT_ID=your-fynix-digital-tenant-id
   ```
   (Get tenant ID from Azure Portal → Azure Active Directory → Overview)

3. Restart server

## Current Configuration
- ✅ `MS_TENANT_ID=common` (correct for multi-tenant)
- ❌ App registration needs to be set to multi-tenant in Azure Portal

