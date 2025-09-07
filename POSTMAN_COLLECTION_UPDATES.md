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

### 6. Fixed Test Scripts
Updated bridge registration test script to extract `device_id` instead of `bridge_device_id` from response.

### 7. Health Check Verification
Confirmed that health check endpoint (`GET /health`) is correctly configured and matches the implementation.

## Verification Status

✅ **Authentication endpoints** - All OTP/OTC flows correct
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
