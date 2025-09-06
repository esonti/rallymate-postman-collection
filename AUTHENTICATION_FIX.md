# Authentication Fix for 401 Errors

## Issue Identified

The 401 authentication errors were caused by incorrect authentication settings in the Postman collection. Specifically:

### Root Cause
1. **API Info endpoint** (`/api/info`) was set to `"type": "noauth"` but requires authentication
2. **Refresh Session endpoint** (`/api/auth/session/refresh`) was using Bearer token auth but should be `noauth`

### Server Authentication Rules
According to the server code (`internal/auth/http_middleware.go`), these are the ONLY public endpoints that don't require authentication:

- ✅ `GET /health` - Health check
- ✅ `POST /api/auth/otp/send` - Send OTP
- ✅ `POST /api/auth/otp/verify` - Verify OTP  
- ✅ `POST /api/auth/session/refresh` - Refresh session tokens

**All other endpoints require Bearer token authentication.**

## Fixes Applied

### 1. Fixed API Info Endpoint
**File**: `collections/rest/RallyMate-Complete-HTTP-APIs.json`

**Before:**
```json
"request": {
    "auth": {
        "type": "noauth"
    },
    "method": "GET",
    ...
}
```

**After:**
```json
"request": {
    "method": "GET",
    // Inherits Bearer token from collection-level auth
    ...
}
```

### 2. Fixed Refresh Session Endpoint
**File**: `collections/rest/RallyMate-Complete-HTTP-APIs.json`

**Before:**
```json
"request": {
    "method": "POST",
    "header": [
        {
            "key": "Authorization",
            "value": "Bearer {{refresh_token}}"
        }
    ],
    ...
}
```

**After:**
```json
"request": {
    "auth": {
        "type": "noauth"
    },
    "method": "POST",
    "header": [
        {
            "key": "Content-Type",
            "value": "application/json"
        }
    ],
    ...
}
```

## Testing the Fix

### 1. Authentication Flow
Follow this sequence in Postman:

1. **Send OTP** (`POST /api/auth/otp/send`)
   - Uses test phone number from environment
   - Should return 200 with OTP expiry info

2. **Verify OTP** (`POST /api/auth/otp/verify`)
   - Use OTP code "123456" (development default)
   - Should return 200 with tokens
   - **Tokens auto-saved to environment variables**

3. **Test Authenticated Endpoint** (`GET /api/info`)
   - Should now return 200 with API information
   - Uses Bearer token automatically

### 2. Verify Token Extraction
After running "Verify OTP", check that these environment variables are populated:
- `session_token` - JWT session token
- `refresh_token` - JWT refresh token  
- `user_id` - Current user ID

### 3. Test Other Endpoints
All other endpoints should now work with automatic Bearer token authentication:
- `GET /api/users`
- `GET /api/facilities`
- Device management endpoints
- etc.

## Troubleshooting

### If Still Getting 401 Errors:

1. **Check Environment Variables**
   - Ensure you're using the "Local Development" environment
   - Verify `session_token` is populated after OTP verification

2. **Re-authenticate**
   - Run "Send OTP" → "Verify OTP" sequence again
   - Check that test scripts executed successfully

3. **Check Phone Number**
   - Update `test_phone_number` in environment if needed
   - Use a phone number that exists in your test database

4. **Server Issues**
   - Ensure RallyMate services are running on localhost:8080
   - Check server logs for detailed error messages

### Common Issues:

**Empty Tokens**: If `session_token` remains empty after OTP verification:
- Check that test scripts executed (Console tab in Postman)
- Verify JSON response structure matches expected format
- Try manually setting a token for testing

**Invalid Token**: If getting "Invalid or expired token":
- Session may have expired (re-authenticate)
- Check server time vs local time
- Verify JWT secret configuration

**Wrong Environment**: Ensure you've selected "Local Development" environment in Postman dropdown

## Updated Collection Features

✅ **Fixed Authentication**: All endpoints now use correct auth settings  
✅ **Automatic Token Management**: Tokens extracted and used automatically  
✅ **Comprehensive Testing**: Test scripts validate responses and extract data  
✅ **Environment Integration**: All variables properly configured  

## Next Steps

1. Import the updated collection into Postman
2. Select "Local Development" environment  
3. Run the authentication flow (Send OTP → Verify OTP)
4. Test any endpoint to verify 401 errors are resolved

---

**Updated**: September 2, 2025  
**Status**: Ready for Testing ✅
