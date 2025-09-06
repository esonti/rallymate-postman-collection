# RallyMate Postman Collections v2

This directory contains comprehensive Postman collections and environments for testing RallyMate services locally. All collections have been updated to reflect the current state of the codebase with proper session management and authorization.

## What's Included

### Environment Files
- **`local-updated-v2.json`** - Complete environment configuration for local testing

### Collection Files
- **HTTP REST API** - `collections/rest/RallyMate_HTTP_REST_API_v2.postman_collection.json`
- **gRPC API** - `collections/grpc/RallyMate_gRPC_API_v2.postman_collection.json`

## Quick Setup

1. **Import Environment**
   - Open Postman
   - Click "Import" → Select `environments/local-updated-v2.json`
   - Set this as your active environment

2. **Import Collections**
   - Import both collection files from the respective folders
   - Both collections are pre-configured to use the environment variables

3. **Start Local Services**
   ```bash
   cd rallymate-services
   make run
   ```

## Authentication Flow

### Cookie-Based Authentication (Recommended)
The new implementation supports session persistence via cookies:

1. **Send OTP** - Use your phone number
2. **Verify OTP** - Provide the OTP code
3. **Automatic Session** - Session and refresh tokens are now set as HttpOnly cookies
4. **Session Persistence** - Continue testing without re-authenticating

### Token-Based Authentication (Legacy)
If you prefer manual token management:

1. Use the "Verify OTP" endpoint
2. Copy the `session_token` from the response
3. Update the `{{session_token}}` environment variable

## Environment Variables

### Required Setup
- `test_phone_number` - Your phone number for OTP testing
- `test_otp_code` - Use "123456" for local testing

### Auto-Populated Variables
These are automatically set during authentication:
- `session_token` - Current session token
- `refresh_token` - Token for session refresh
- `user_id` - Current user ID
- `created_facility_id` - ID of test facility (set during creation)
- `created_user_id` - ID of test user (set during creation)
- `created_membership_id` - ID of test membership (set during creation)
- `bridge_device_id` - ID of test bridge device (set during creation)
- `camera_device_id` - ID of test camera device (set during creation)
- `lock_device_id` - ID of test lock device (set during creation)
- `video_id` - ID of test video (set during creation)

## Testing Workflow

### 1. Authentication Test
```
01 - Authentication → Send OTP
01 - Authentication → Verify OTP
01 - Authentication → Get Current Session
```

### 2. Profile Access (Always Available)
```
02 - Users → Get User Profile
02 - Users → Update User Profile
```

### 3. System Data Access (Requires Valid Membership)
```
03 - Facilities → Get All Facilities
04 - Bridge Management → Get All Bridges
```

### 4. Admin Operations (Requires Admin Role)
```
02 - Users → Create User
03 - Facilities → Create Facility
```

## Authorization Logic

### Membership Expiry Enforcement
- **Expired Members**: Can only access profile endpoints
- **Valid Members**: Can access all facility data for their memberships
- **Admins**: Can access all data and perform admin operations

### Session Management
- **Session Tokens**: 24-hour expiry
- **Refresh Tokens**: 30-day expiry
- **Cookies**: HttpOnly, Secure, SameSite=Strict
- **Auto-Refresh**: Use refresh token to get new session token

## Collection Structure

### HTTP REST Collection
- **Authentication** - OTP flow, session management, logout
- **Users** - Profile, user management, membership management
- **Facilities** - Facility CRUD operations
- **Bridge Management** - Bridge registration and management
- **Cameras** - Camera registration, control, and activity monitoring
- **Locks** - Lock registration, control (lock/unlock), and activity monitoring
- **Videos** - Video creation, association, and management
- **System Health** - Health check endpoints

### gRPC Collection
- **Authentication Service** - OTP and session management
- **Users Service** - User and membership operations
- **Facilities Service** - Facility operations
- **Bridge Service** - Bridge operations
- **Cameras Service** - Camera operations
- **Videos Service** - Video operations
- **Locks Service** - Lock operations
- **System Support Service** - Health and system info

## Testing Membership Expiry

### Create Expired Membership
```json
{
    "phone_number": "+1987654321",
    "facility_id": {{created_facility_id}},
    "role": "player",
    "expiry_date": "2020-12-31T23:59:59Z"  // Past date
}
```

### Test Access Restriction
1. Create user with expired membership
2. Login as that user
3. Try accessing facilities - should get 403 Forbidden
4. Access profile - should work normally

## Common Test Scenarios

### 1. New User Registration Flow
```
1. Send OTP
2. Verify OTP (creates user if doesn't exist)
3. Get Profile (shows empty memberships)
4. Admin creates membership for user
5. User can now access facility data
```

### 2. Session Persistence Test
```
1. Login and verify session works
2. Close Postman/browser
3. Reopen and try any authenticated endpoint
4. Should work without re-authentication (cookies)
```

### 3. Admin Workflow Test
```
1. Login as system admin
2. Create facility
3. Create user
4. Create membership for user
5. Verify user can access facility data
```

## Environment Configuration

### Server URLs
- **HTTP**: `http://localhost:8080`
- **gRPC**: `http://localhost:9090`
- **Health**: `http://localhost:8080`

### Test Data
- **Phone**: `+1234567890` (use your actual number for SMS)
- **OTP**: `123456` (default for local development)
- **Timezone**: `America/New_York`

## Troubleshooting

### 401 Unauthorized
- Check if session token is valid
- Try refreshing session using refresh token
- Re-authenticate if needed

### 403 Forbidden
- Check if user has valid (non-expired) membership
- Verify user has required role for the operation
- System admins: ensure admin role is assigned

### 404 Not Found
- Verify resource IDs are correct
- Check if resource exists in database
- Ensure proper facility access permissions

### Cookie Issues
- Ensure you're using the same domain/port
- Check that cookies are enabled in Postman
- Use "Authorization" header as fallback

## Notes

### Development vs Production
- These collections are configured for local development
- For production, update the environment URLs
- Production will require actual SMS for OTP verification

### Database State
- Test data persists between runs
- Use DELETE endpoints to clean up test data
- Or restart services to reset database

### gRPC Testing
- gRPC endpoints use JSON over HTTP for Postman compatibility
- Content-Type should be `application/grpc+json`
- Real gRPC clients use binary protobuf format
  - `base_url`: `http://localhost:8080`
  - `grpc_url`: `localhost:50051`

- **Cloud Development:** Use `dev.json`
  - `base_url`: `http://YOUR_CLOUD_IP:8080`
  - `grpc_url`: `YOUR_CLOUD_IP:50051`

## 🔧 Authentication Flow

1. **Send OTP:** `POST /api/auth/send-otp`
2. **Verify OTP:** `POST /api/auth/verify-otp`
3. **Use the returned session token for authenticated requests**

## 📋 Testing Scenarios

Each collection includes comprehensive test scenarios:

- ✅ **Positive test cases** - Valid inputs and expected responses
- ❌ **Negative test cases** - Invalid inputs and error handling
- 🔄 **Edge cases** - Boundary conditions and special scenarios
- 🔐 **Authentication tests** - Token validation and session management

## 🏗️ Collection Features

- **Pre-request Scripts:** Automatic token management
- **Test Scripts:** Response validation and assertion
- **Variables:** Dynamic data and environment configuration
- **Documentation:** Detailed API documentation for each endpoint

## 📡 API Coverage

### Authentication Service
- Send OTP
- Verify OTP
- Refresh Session
- Validate Session
- Revoke Session
- Get User Sessions

### User Management
- Create User
- Get Users (with filtering)
- Get User Profile
- Update User Profile
- Get User by Phone
- Create User Membership (with name/email)
- Create User Membership by Phone Only
- Create User Membership by User ID
- Update User Membership
- Delete User Membership
- Get User Memberships
- Get Facility Memberships

### Facility Management
- Get Facilities
- Create Facility
- Get Facility Details
- Update Facility
- Delete Facility

### Smart Lock Management
- Get Locks
- Register Lock
- Get Lock Details
- Update Lock
- Unregister Lock
- Lock Control (unlock/lock)
- Get Lock Status
- Batch Lock Control

### Camera Management
- Get Cameras
- Register Camera
- Get Camera Details
- Update Camera
- Unregister Camera
- Camera Control
- Get Camera Status

### Video Management
- Get Videos
- Create Video
- Get Video Details
- Update Video
- Delete Video

### Bridge Device Management
- Get Bridge Devices
- Register Bridge Device
- Get Bridge Device Details
- Update Bridge Device
- Unregister Bridge Device
- Get Bridge Status
- Get Bridge Devices for Bridge

## 🔍 Testing Tips

1. **Start with Authentication:** Always test the auth flow first
2. **Use Environment Variables:** Switch between local/dev/prod easily
3. **Check Response Status:** Verify HTTP status codes and response structure
4. **Test Error Cases:** Ensure proper error handling
5. **Validate Data:** Check that returned data matches expected schema

## ✨ New Features

### Enhanced Membership Creation
The Users collection now includes three different ways to create user memberships:

1. **Standard Membership Creation** (`POST /api/users/memberships`)
   - Requires phone number, name, and optionally email
   - Creates user if they don't exist with provided details

2. **Phone-Only Membership Creation** (`POST /api/users/memberships/phone`)
   - Requires only phone number and membership details
   - Creates user automatically with empty name/email if needed
   - Ideal for quick registrations without personal details

3. **User ID Membership Creation** (gRPC `CreateMembershipByUserId`)
   - For existing users only
   - Proto-compliant method using user ID
   - Fails if user doesn't exist

#### Example Usage:
```json
// Phone-only membership creation
{
  "phone_number": "+1555987654",
  "facility_id": 1,
  "role": "player",
  "start_date": 1672531200,
  "expiry_date": 1704067200
}
```

## 📝 Contributing

To add new test cases or update existing ones:

1. Update the relevant collection file
2. Test the changes locally
3. Commit and push the changes
4. Update documentation if needed

## 🚨 Security Notes

- Never commit real credentials or sensitive data
- Use environment variables for sensitive information
- Test with mock data when possible
- Ensure proper cleanup after testing
