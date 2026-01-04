# Quick Setup: Microsoft OAuth Client Secret

## ✅ Use the VALUE, NOT the Secret ID

### In Azure Portal:

- **Value**: `H3~8Q~~5nZ4vkC4rekH-R3WGYohjW-z...` ← **USE THIS ONE**
- **Secret ID**: `945dc725-9346-4c4f-b819-aa6e28898e7d` ← Don't use this

### Steps:

1. **Copy the Value:**

   - In Azure Portal, find your client secret
   - Click the **COPY icon** next to the **Value** column
   - The value is a long string (usually 40+ characters)

2. **Add to .env:**

   MS_CLIENT_SECRET=REDACTED_SECRET

   - Replace `...` with the complete value you copied
   - No quotes, no spaces around `=`

3. **Verify:**

   ```bash
   grep "^MS_CLIENT_SECRET=" .env
   ```

   Should show: `MS_CLIENT_SECRET=H3~8Q~~...` (your full value)

4. **Restart Server:**
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

### ⚠️ Important:

- The Value is **sensitive** - keep it secret!
- If you can't see the full value, you need to create a new secret
- The Value shown in Azure is truncated for security

### 🔍 How to Get Full Value:

If the value is truncated (`...`), you need to:

1. Create a **new client secret** in Azure Portal
2. Copy the value **immediately** (you won't see it again!)
3. Use that new value in your `.env`
