# JWT Security Setup Guide

## Overview
The JWT implementation has been completely overhauled with proper security measures. Here's what was fixed:

### ✅ Security Improvements Made:

1. **Strong Secret Key Management**
   - Removed hardcoded weak secret key
   - Added environment variable configuration
   - Implemented proper secret key validation

2. **Secure Password Hashing**
   - Replaced SHA256 with bcrypt (industry standard)
   - Added proper salt generation
   - Implemented secure password verification

3. **Proper JWT Implementation**
   - Added PyJWT library to requirements
   - Implemented access and refresh token system
   - Added proper token expiration handling
   - Enhanced error handling and validation

4. **Fixed Authentication Flow**
   - Removed circular dependency in login route
   - Consolidated authentication logic
   - Added token refresh mechanism
   - Improved route protection

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the backend directory with:

```env
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-make-it-long-and-random
JWT_ACCESS_TOKEN_EXPIRE_HOURS=2
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# Database Configuration
DATABASE_URL=mysql://username:password@localhost:3306/study_buddy

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

**⚠️ IMPORTANT:** Generate a strong secret key for production:
```python
import secrets
print(secrets.token_urlsafe(64))
```

### 3. API Endpoints

#### Authentication
- `POST /api/auth/login` - Login (returns access + refresh tokens)
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout (client discards tokens)

#### User Management
- `POST /api/users/register` - Register new user
- `GET /api/users/profile` - Get user profile (requires auth)

#### Documents
- `POST /api/documents/upload` - Upload document (requires auth)
- `GET /api/documents/my-documents` - Get user's documents (requires auth)

#### Quiz
- `GET /api/quiz/test` - Test authentication (requires auth)
- `POST /api/quiz/generate` - Generate quiz (requires auth)

### 4. Token Usage

#### Login Request
```json
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Login Response
```json
{
  "message": "Login successful!",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "user@example.com"
  }
}
```

#### Authenticated Requests
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:5050/api/users/profile
```

#### Token Refresh
```json
POST /api/auth/refresh
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 5. Security Features

- **Access Tokens**: Short-lived (2 hours) for API requests
- **Refresh Tokens**: Long-lived (30 days) for getting new access tokens
- **Password Security**: bcrypt hashing with salt
- **Token Validation**: Proper signature verification and expiration checks
- **Error Handling**: Secure error messages without information leakage

### 6. Migration Notes

If you have existing users with SHA256 hashed passwords, you'll need to:
1. Implement a password reset mechanism
2. Or create a migration script to re-hash passwords on next login

### 7. Production Checklist

- [ ] Set strong JWT_SECRET_KEY in environment
- [ ] Set FLASK_DEBUG=False
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Add CORS restrictions
- [ ] Set up proper logging
- [ ] Configure secure session management

## Testing

Test the authentication flow:

1. Register a new user
2. Login to get tokens
3. Use access token for protected routes
4. Test token refresh
5. Test token expiration

The JWT implementation is now production-ready with industry-standard security practices!
