# Video Upload API - Testing Guide

## Overview
The RallyMate Video Upload API has been completely redesigned to support file uploads directly to Google Cloud Storage with automatic metadata extraction, progress tracking, and robust error handling.

## API Changes

### Old API (Deprecated)
- **Endpoint**: `POST /api/videos`
- **Content-Type**: `application/json`
- **Body**: JSON with file URLs, metadata, etc.

### New API (Current)
- **Endpoint**: `POST /api/videos`
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with actual video file + metadata

## Required Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `video` | file | ✅ | The actual video file to upload |
| `facility_id` | text | ✅ | ID of the facility where video was recorded |
| `camera_device_id` | text | ✅ | ID of the camera device that recorded the video |
| `start_time` | text | ✅ | Recording start time in RFC3339 format |
| `recording_type` | text | ❌ | Type of recording (manual, scheduled, motion_detected, etc.) |

## Automatic Features

### 1. Metadata Extraction
- **File Size**: Automatically extracted from uploaded file
- **Duration**: Extracted from video file metadata
- **Format**: Detected from file header
- **Validation**: File type and format validation

### 2. Cloud Storage Upload
- **Progress Tracking**: For files > 50MB
- **Retry Logic**: Automatic retry with exponential backoff
- **Error Recovery**: Robust error handling and recovery mechanisms
- **File Organization**: Structured storage with timestamps and camera IDs

### 3. Response Format
```json
{
  "video": {
    "id": 123,
    "facility_id": 1,
    "camera_device_id": "cam_001",
    "filename": "video.mp4",
    "file_size_bytes": 1048576,
    "duration_seconds": 300,
    "file_url": "https://storage.googleapis.com/bucket/videos/...",
    "recording_type": "manual",
    "start_time": "2025-01-05T10:00:00Z",
    "created_at": "2025-01-05T10:05:00Z"
  },
  "upload_url": "https://storage.googleapis.com/bucket/videos/..."
}
```

## Testing with Postman

### Prerequisites
1. **Authentication**: Login first using the authentication endpoints
2. **Facility**: Create or use existing facility (sets `created_facility_id`)
3. **Camera**: Register a camera device (sets `camera_device_id`)
4. **Video File**: Have a video file ready for upload (MP4, AVI, MOV recommended)

### Test Steps

#### 1. Import Collection
- Import: `RallyMate_HTTP_REST_API_v2.postman_collection.json`
- Environment: `local-updated-v2.json`

#### 2. Authentication Flow
1. **Send OTP**: Use your test phone number
2. **Verify OTP**: Use the OTP code to login
   - This automatically sets `session_token`

#### 3. Setup Test Data
1. **Create Facility**: Run "Create Facility" request
   - This sets `created_facility_id`
2. **Register Camera**: Run "Register Camera" request
   - This sets `camera_device_id`

#### 4. Upload Video
1. Go to **"07 - Videos" → "Upload Video"**
2. In the request body:
   - **video**: Click "Select Files" and choose your video file
   - **facility_id**: Should be `{{created_facility_id}}` (auto-filled)
   - **camera_device_id**: Should be `{{camera_device_id}}` (auto-filled)
   - **recording_type**: Set to "manual" or desired type
   - **start_time**: Uses `{{$isoTimestamp}}` for current time
3. **Send the request**

#### 5. Verify Response
- Status should be `201 Created`
- Response should include:
  - `video` object with all metadata
  - `upload_url` pointing to Google Cloud Storage
- Environment variables automatically set:
  - `video_id`: For subsequent operations
  - `uploaded_video_url`: Cloud storage URL

### Expected Test Results

#### Success Response (201)
```json
{
  "video": {
    "id": 1,
    "facility_id": 1,
    "camera_device_id": "test-camera-001",
    "filename": "my_video.mp4",
    "file_size_bytes": 2097152,
    "duration_seconds": 120,
    "file_url": "https://storage.googleapis.com/rallymate-videos/videos/camera-1/20250105-143022-my_video.mp4",
    "recording_type": "manual",
    "start_time": "2025-01-05T14:30:00Z",
    "created_at": "2025-01-05T14:30:22Z"
  },
  "upload_url": "https://storage.googleapis.com/rallymate-videos/videos/camera-1/20250105-143022-my_video.mp4"
}
```

#### Error Responses

##### Missing File (400)
```json
{
  "error": "Video file is required",
  "details": "http: no such file"
}
```

##### Invalid Facility (400)
```json
{
  "error": "Validation failed",
  "details": "Invalid facility ID"
}
```

##### File Too Large (400)
```json
{
  "error": "Failed to parse multipart form",
  "details": "multipart: message too large"
}
```

## Advanced Testing

### Large File Upload
- Test with files > 50MB to verify progress tracking
- Monitor console logs for progress updates

### Error Scenarios
1. **Network Issues**: Test retry logic by temporarily disconnecting
2. **Invalid Files**: Try non-video files to test validation
3. **Missing Auth**: Test without session token
4. **Invalid Metadata**: Test with malformed timestamps

### Load Testing
- Multiple concurrent uploads
- Various file sizes
- Different video formats

## Environment Variables

Ensure these are set in your Postman environment:

| Variable | Example | Description |
|----------|---------|-------------|
| `api_base_url` | `http://localhost:8080/api` | API base URL |
| `session_token` | `eyJhbGc...` | Authentication token (auto-set) |
| `created_facility_id` | `1` | Test facility ID (auto-set) |
| `camera_device_id` | `test-camera-001` | Test camera ID (auto-set) |
| `video_id` | `1` | Uploaded video ID (auto-set) |
| `uploaded_video_url` | `https://storage...` | Cloud storage URL (auto-set) |

## Troubleshooting

### Common Issues

1. **"Video file is required"**
   - Ensure you've selected a file in the form data
   - Check the field name is exactly "video"

2. **"Invalid form data"**
   - Verify all required fields are present
   - Check timestamp format (should be RFC3339)

3. **"Permission denied"**
   - Ensure you're authenticated (session_token set)
   - Check user has access to the facility

4. **"Failed to upload video"**
   - Check cloud storage configuration
   - Verify network connectivity
   - Monitor server logs for detailed errors

### Server Logs
Monitor the rallymate-services container logs:
```bash
docker logs -f <container-id>
```

### Debug Tips
1. Enable Postman console to see detailed request/response data
2. Check environment variables are properly set
3. Verify file size limits (current limit: 100MB)
4. Test with small files first, then scale up

## Features Implemented

✅ **Multipart file upload**  
✅ **Automatic metadata extraction**  
✅ **Cloud storage integration**  
✅ **Progress tracking (>50MB files)**  
✅ **Retry logic with exponential backoff**  
✅ **File validation and error handling**  
✅ **Database record creation**  
✅ **Comprehensive error responses**  
✅ **Postman collection updated**  

## Next Steps

🔄 **Real-time progress updates via WebSocket**  
🔄 **Thumbnail generation during upload**  
🔄 **Resumable uploads for large files**  
🔄 **Video transcoding and format conversion**  
🔄 **Advanced metadata extraction (codec, resolution, etc.)**
