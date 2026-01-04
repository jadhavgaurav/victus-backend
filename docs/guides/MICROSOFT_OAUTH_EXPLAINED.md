# Microsoft OAuth Login - Configuration Guide

## Two Different Microsoft Authentications

### 1. **Microsoft OAuth Login** (Web Redirect - Already Working ✅)
- **Purpose**: User login/signup via Microsoft account
- **Flow**: Web redirect (automatic, no manual link needed)
- **Location**: `src/auth/oauth.py`
- **Status**: ✅ Already configured correctly with web redirect

### 2. **Microsoft 365 Tools Authentication** (Device Code - For Email/Calendar)
- **Purpose**: Access to M365 tools (send email, create calendar events)
- **Flow**: Device code (requires manual link - this is what you're seeing)
- **Location**: `src/m365_auth.py`
- **Status**: This is separate from login and only needed when using M365 tools

---

## Which Microsoft Accounts Can Login?

The `MS_TENANT_ID` in your `.env` determines which accounts can login:

### Option 1: **Any Microsoft Account** (Recommended for Public Apps)
```env
MS_TENANT_ID=common
```
- ✅ Personal Microsoft accounts (@outlook.com, @hotmail.com, @live.com)
- ✅ Work/School accounts from any organization
- ✅ Most flexible option

### Option 2: **Work/School Accounts Only**
```env
MS_TENANT_ID=organizations
```
- ✅ Work/School accounts from any organization
- ❌ Personal Microsoft accounts

### Option 3: **Specific Organization Only**
```env
MS_TENANT_ID=573ff913-268d-4753-2455-703d328a45b2
```
- ✅ Only accounts from your specific Entra ID tenant
- ❌ Other Microsoft accounts

---

## Current Configuration

Based on your `.env`:
- `MS_TENANT_ID=573ff913-268d-4753-2455-703d328a45b2` (Specific tenant)

**This means**: Only accounts from your Entra ID project can login.

**To allow any Microsoft account**, change to:
```env
MS_TENANT_ID=common
```

---

## Fixing the Device Code Issue

The device code flow you're seeing is **only for M365 tools** (email/calendar), not for login.

### For Login (Already Fixed ✅)
Microsoft OAuth login already uses web redirect - no manual link needed!

### For M365 Tools (Optional - Only if you use email/calendar features)
The device code flow is a limitation of M365 tools when not using OAuth. This is separate from login.

---

## Summary

1. **Login**: Already uses web redirect ✅ - No manual link needed
2. **Account Access**: Currently limited to your Entra ID tenant
3. **To allow any Microsoft account**: Change `MS_TENANT_ID=common` in `.env`

