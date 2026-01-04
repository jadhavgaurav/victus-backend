# Microsoft 365 Authentication Fix - No More Device Code!

## ✅ Problem Solved

**Before**: M365 tools (email/calendar) required manual device code authentication in terminal  
**After**: Uses your Microsoft OAuth login token automatically - no manual steps needed!

---

## What Changed

### 1. **User Model** (`src/models.py`)
Added fields to store Microsoft OAuth tokens:
- `microsoft_access_token` - Access token for M365 API
- `microsoft_refresh_token` - Refresh token to get new access tokens
- `microsoft_token_expires_at` - Token expiration time

### 2. **OAuth Scopes** (`src/auth/oauth.py`)
Updated to request M365 permissions:
- `User.Read` (for login)
- `Mail.ReadWrite`, `Mail.Send` (for email)
- `Calendars.ReadWrite` (for calendar)

### 3. **Token Storage** (`src/auth/oauth.py`)
Now stores tokens in User model during OAuth callback

### 4. **M365 Auth** (`src/m365_auth.py`)
`get_access_token()` now:
1. ✅ First tries to use stored token from user's OAuth session
2. ✅ Checks if token is expired
3. ✅ Automatically refreshes expired tokens
4. ⚠️ Falls back to device flow only if no OAuth token available

---

## Database Migration Required

You need to add the new fields to your database. Choose one method:

### Option 1: SQLite (Quick - For Development)
```sql
ALTER TABLE users ADD COLUMN microsoft_access_token TEXT;
ALTER TABLE users ADD COLUMN microsoft_refresh_token TEXT;
ALTER TABLE users ADD COLUMN microsoft_token_expires_at DATETIME;
```

### Option 2: Recreate Database (If you don't mind losing data)
```bash
rm chat_history.db
poetry run python -c "from src.database import init_db; init_db()"
```

### Option 3: Use Alembic (Recommended for Production)
```bash
# Create migration
poetry run alembic revision --autogenerate -m "add_microsoft_token_fields"

# Apply migration
poetry run alembic upgrade head
```

---

## How to Use

1. **Login with Microsoft OAuth** (if not already done)
   - Click "Sign in with Microsoft" on login page
   - Grant permissions (includes Mail & Calendar)
   - You're logged in!

2. **Use M365 Tools**
   - Ask: "Send an email to..."
   - Ask: "What's my next meeting?"
   - Ask: "Schedule a meeting..."
   - **No device code needed!** ✅

---

## Benefits

✅ **No more device code flow** - Everything uses web OAuth  
✅ **Automatic token refresh** - Tokens refresh when expired  
✅ **Seamless experience** - Login once, use all features  
✅ **Secure** - Tokens stored in database (encrypt in production)

---

## Important Notes

1. **Existing Users**: Users who logged in before this fix will need to:
   - Log out and log back in with Microsoft OAuth
   - This will store their tokens for M365 tools

2. **Token Security**: In production, encrypt tokens before storing:
   ```python
   # Example: Use cryptography library
   from cryptography.fernet import Fernet
   encrypted_token = cipher.encrypt(token.encode())
   ```

3. **Token Expiration**: Tokens automatically refresh when expired (within 5 minutes of expiration)

---

## Testing

After applying the migration and restarting:

1. Log out and log back in with Microsoft OAuth
2. Try: "What's my next meeting?"
3. Should work without device code! ✅

---

## Troubleshooting

**"Authentication failed" error:**
- Make sure you logged in with Microsoft OAuth (not just email/password)
- Log out and log back in with Microsoft

**"Token expired" error:**
- The system should auto-refresh, but if it fails:
- Log out and log back in to get a fresh token

**Still seeing device code:**
- Make sure you're logged in with Microsoft OAuth
- Check that `MS_CLIENT_SECRET` is set in `.env`
- Restart the server after changes

