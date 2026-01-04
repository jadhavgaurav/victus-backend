# Authentication Setup Guide

## Overview

Project VICTUS now includes a complete authentication system with:
- Email/Password signup and login
- Google OAuth integration
- Microsoft OAuth integration
- JWT token-based authentication
- Protected API endpoints

---

## Environment Variables

Add these to your `.env` file:

```env
# JWT Configuration (REQUIRED)
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200  # 30 days

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# Microsoft OAuth (Optional - can reuse MS_CLIENT_ID)
# MS_CLIENT_ID and MS_TENANT_ID are already configured for M365
# These will also be used for OAuth login
```

---

## Setting Up OAuth Providers

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Go to **Credentials** > **Create Credentials** > **OAuth 2.0 Client ID**
5. Application type: **Web application**
6. Authorized redirect URIs: `http://localhost:8000/api/auth/google/callback`
7. Copy **Client ID** and **Client Secret** to `.env`

### Microsoft OAuth Setup

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Select your existing app (or create new)
4. Go to **Authentication**
5. Add platform: **Web**
6. Redirect URI: `http://localhost:8000/api/auth/microsoft/callback`
7. Enable **ID tokens** in Implicit grant
8. The **Client ID** and **Tenant ID** are already in your `.env`

---

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login with email/password
- `GET /api/auth/me` - Get current user info (requires auth)
- `POST /api/auth/logout` - Logout (requires auth)
- `GET /api/auth/google/login` - Initiate Google OAuth
- `GET /api/auth/google/callback` - Google OAuth callback
- `GET /api/auth/microsoft/login` - Initiate Microsoft OAuth
- `GET /api/auth/microsoft/callback` - Microsoft OAuth callback

### Protected Endpoints

All chat and upload endpoints now accept optional authentication:
- `POST /api/chat` - Requires auth token in header
- `POST /api/history` - Requires auth token in header
- `POST /api/upload` - Requires auth token in header

---

## Frontend Pages

- `/login` - Login page
- `/signup` - Signup page
- `/` - Main app (requires authentication)

---

## Usage

### Signup Flow

1. User visits `/signup`
2. Fills in email, username, password
3. On success, token is stored in localStorage
4. User is redirected to main app

### Login Flow

1. User visits `/login`
2. Enters email and password
3. On success, token is stored in localStorage
4. User is redirected to main app

### OAuth Flow

1. User clicks "Sign in with Google/Microsoft"
2. Redirected to provider's login page
3. After authentication, redirected back to `/api/auth/{provider}/callback`
4. Token is generated and user is redirected to main app with token in URL
5. Frontend stores token and reloads

---

## Database Migration

Run Alembic migration to create User table:

```bash
alembic revision --autogenerate -m "Add user authentication"
alembic upgrade head
```

---

## Security Notes

1. **Change SECRET_KEY**: Use a strong, random secret key in production
2. **HTTPS**: Always use HTTPS in production for OAuth callbacks
3. **Token Storage**: Tokens are stored in localStorage (consider httpOnly cookies for production)
4. **Password Requirements**: Minimum 8 characters (can be enhanced)

---

## Testing

Test the authentication:

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Get user info (use token from login)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Troubleshooting

### OAuth not working
- Check redirect URIs match exactly
- Verify client IDs and secrets are correct
- Check that OAuth is enabled in provider console

### Token not working
- Check token hasn't expired
- Verify SECRET_KEY matches
- Ensure Authorization header format: `Bearer TOKEN`

### User not found errors
- Run database migrations
- Check user exists in database
- Verify user.is_active is True

