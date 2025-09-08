# Postman Collection Updates - RallyMate API

## Summary of Changes Made

### 1. Environment Variables Added
Updated `local.json` environment file with new variables:
- `test_edge_device_id` - For testing bridge edge connections
- `test_lock_device_id` - For lock device registration
- `test_camera_device_id` - For camera device registration  
- `test_bridge_device_id` - For bridge device registration
- `created_lock_activity_id` - Auto-populated lock activity ID
- `created_camera_activity_id` - Auto-populated camera activity ID
- `created_bridge_activity_id` - Auto-populated bridge activity ID

### 2. Fixed Request Body Structures

#### Lock Registration (`POST /api/locks/register`)
**Before:**
```json
{
    "device_id": "lock-{{$randomUUID}}",
    "facility_id": {{created_facility_id}},
    "location": "Main Entrance",
    "device_name": "Main Door Lock",
    "device_type": "smart_lock",
    "bridge_device_id": "{{bridge_device_id}}"
}
```

**After (matches protobuf RegisterLockRequest):**
```json
{
    "device_id": "{{test_lock_device_id}}",
    "facility_id": {{created_facility_id}},
    "name": "Main Door Lock"
}
```

#### Lock Control (`POST /api/locks/{device_id}/control`)
**Before:**
```json
{
    "action": "unlock",
    "duration_seconds": 30
}
```

**After (matches protobuf LockControlRequest):**
```json
{
    "facility_id": {{created_facility_id}},
    "device_id": "{{lock_device_id}}",
    "user_id": {{user_id}},
    "action": "UNLOCK",
    "reason": "User requested access"
}
```

#### Camera Registration (`POST /api/cameras/register`)
**Before:**
```json
{
    "device_id": "camera-{{$randomUUID}}",
    "facility_id": {{created_facility_id}},
    "location": "Main Entrance",
    "device_name": "Main Entrance Camera",
    "device_type": "security_camera",
    "bridge_device_id": "{{bridge_device_id}}",
    "stream_url": "rtsp://192.168.1.101:554/stream"
}
```

**After (matches protobuf RegisterCameraRequest):**
```json
{
    "device_id": "{{test_camera_device_id}}",
    "facility_id": {{created_facility_id}},
    "name": "Main Entrance Camera"
}
```

#### Camera Control (`POST /api/cameras/{device_id}/control`)
**Before:**
```json
{
    "action": "start_recording",
    "duration_seconds": 60
}
```

**After (matches protobuf CameraControlRequest):**
```json
{
    "facility_id": {{created_facility_id}},
    "device_id": "{{camera_device_id}}",
    "user_id": {{user_id}},
    "action": "START_RECORD",
    "reason": "User initiated recording"
}
```

#### Bridge Registration (`POST /api/bridges`)
**Before:**
```json
{
    "bridge_device_id": "bridge-{{$randomUUID}}",
    "facility_id": {{created_facility_id}},
    "device_name": "Main Bridge Device",
    "location": "Server Room",
    "ip_address": "192.168.1.100",
    "port": 8080
}
```

**After (matches protobuf RegisterBridgeRequest):**
```json
{
    "device_id": "{{test_bridge_device_id}}",
    "facility_id": {{created_facility_id}},
    "name": "Main Bridge Device"
}
```

#### Lock Update (`PUT /api/locks/{device_id}`)
**Before:**
```json
{
    "device_name": "Updated Main Door Lock",
    "location": "Updated Main Entrance"
}
```

**After (matches protobuf UpdateLockRequest):**
```json
{
    "facility_id": {{created_facility_id}},
    "device_id": "{{lock_device_id}}",
    "name": "Updated Main Door Lock",
    "firmware_version": "1.2.3",
    "edge_connectivity": "CONNECTED",
    "state": "LOCKED"
}
```

### 3. Fixed Enum Values

#### Membership Roles
**Before:** `"role": "player"`
**After:** `"role": "MEMBERSHIP_ROLE_PLAYER"`

Available values:
- `MEMBERSHIP_ROLE_UNSPECIFIED`
- `MEMBERSHIP_ROLE_PLAYER`
- `MEMBERSHIP_ROLE_MANAGER`

#### Lock Actions
**Before:** `"action": "unlock"`
**After:** `"action": "UNLOCK"`

Available values:
- `LOCK_ACTION_UNSPECIFIED`
- `LOCK`
- `UNLOCK`
- `STATUS_CHECK`

#### Camera Actions
**Before:** `"action": "start_recording"`
**After:** `"action": "START_RECORD"`

Available values:
- `CAMERA_ACTION_UNSPECIFIED`
- `START_LIVE_STREAM`
- `STOP_LIVE_STREAM`
- `START_RECORD`
- `STOP_RECORD`
- `STATUS_CHECK`

### 4. Fixed Query Parameters

#### Get Locks (`GET /api/locks`)
**Before:** 
- `status=locked`
- `location=main_entrance`

**After:**
- `state=LOCKED`
- `edge_connectivity=CONNECTED`

### 5. Updated Descriptions
All endpoint descriptions now include available enum values for reference.

### 6. HTTP API Protobuf Compliance Update

#### Fixed VerifyOTP Response Structure
**Before (non-compliant with protobuf):**
```go
type VerifyOTPResponse struct {
    Success bool                 `json:"success"`
    Message string               `json:"message"`
    Token   string               `json:"token,omitempty"`        // NOT IN PROTO!
    User    *models.User         `json:"user,omitempty"`         // NOT IN PROTO!
    Session *UserSessionResponse `json:"session,omitempty"`      // Wrong type
}
```

**After (compliant with protobuf):**
```go
type VerifyOTPResponse struct {
    Success bool                 `json:"success"`
    Message string               `json:"message"`
    Session *models.UserSession  `json:"session,omitempty"`      // Matches proto UserSession
}
```

#### Fixed VerifyOTC Response Structure
**Before (non-compliant with protobuf):**
```go
type VerifyOTCResponse struct {
    Success bool                   `json:"success"`
    Message string                 `json:"message"`
    Session *DeviceSessionResponse `json:"session,omitempty"`   // Wrong type
}
```

**After (compliant with protobuf):**
```go
type VerifyOTCResponse struct {
    Success bool                   `json:"success"`
    Message string                 `json:"message"`
    Session *models.DeviceSession  `json:"session,omitempty"`   // Matches proto DeviceSession
}
```

#### Benefits of Compliance
- **Consistency**: HTTP and gRPC APIs now return identical response structures
- **Type Safety**: Using actual model types instead of custom response types
- **Maintainability**: Single source of truth for response structure (protobuf)
- **API Documentation**: Protobuf definitions accurately represent both gRPC and HTTP responses

Both VerifyOTP and VerifyOTC now return exactly what's defined in `auth.proto`:
```json
{
    "success": true,
    "message": "OTP/OTC verified successfully",
    "session": {
        "id": 123,
        "user_id": 456,           // Only in VerifyOTP
        "device_id": "device-xyz", // Only in VerifyOTC
        "session_token": "jwt_token_here",
        "refresh_token": "refresh_token_here",
        "status": "SESSION_STATUS_ACTIVE",
        "expires_at": "2025-09-08T23:07:29Z",
        "last_accessed_at": "2025-09-07T23:07:29Z",
        "created_at": "2025-09-07T23:07:29Z",
        "updated_at": "2025-09-07T23:07:29Z",
        "device_info": "Postman Test Client",
        "ip_address": "127.0.0.1"
    }
}
```

### 7. Updated Authentication Response Handling

#### VerifyOTP Response Format Update
**Before (inconsistent):**
- Test script expected `jsonData.token` for session token
- Test script expected `jsonData.user.id` for user ID

**After (consistent with VerifyOTC):**
- Test script now uses `jsonData.session.session_token` for session token
- Test script now uses `jsonData.session.user_id` for user ID
- Response format is now consistent between VerifyOTP and VerifyOTC

Both VerifyOTP and VerifyOTC now return:
```json
{
    "success": true,
    "message": "OTP/OTC verified successfully",
    "session": {
        "id": 123,
        "session_token": "jwt_token_here",
        "refresh_token": "refresh_token_here",
        "user_id": 456,     // Only in VerifyOTP
        "device_id": "xyz", // Only in VerifyOTC
        "status": "SESSION_STATUS_ACTIVE",
        "expires_at": "2025-09-08T23:07:29Z",
        "device_info": "Postman Test Client",
        "ip_address": "127.0.0.1"
    }
}
```

### 7. Fixed Test Scripts
Updated bridge registration test script to extract `device_id` instead of `bridge_device_id` from response.

### 7. Health Check Verification
Confirmed that health check endpoint (`GET /health`) is correctly configured and matches the implementation.

## Verification Status

✅ **Authentication endpoints** - HTTP API now strictly compliant with protobuf definitions
✅ **Response consistency** - VerifyOTP and VerifyOTC have identical structure and format
✅ **User management** - Profile, users, memberships with correct role enums
✅ **Facility management** - CRUD operations correct
✅ **Lock management** - Registration, control, activities with correct enums
✅ **Camera management** - Registration, control, activities with correct enums  
✅ **Bridge management** - Registration, edge connections with correct structure
✅ **Video management** - Upload, associate, delete operations
✅ **Storage endpoints** - File serving endpoints
✅ **gRPC Gateway** - Access to protobuf services via HTTP

## Notes

1. All request bodies now match the exact protobuf message structures
2. Enum values use the full protobuf enum names for consistency
3. Environment variables use consistent naming patterns
4. Descriptions include reference to available enum values
5. Query parameters use correct field names from protobuf definitions

The Postman collection is now fully aligned with the actual API implementation and ready for testing.
