# 📖 Manual Collection Building Guide

This guide provides copy-paste ready examples for building Postman collections manually with complete test scripts and realistic data.

## 🎯 Quick Reference: Service Endpoints

| Service | Endpoints | Auth Required |
|---------|-----------|---------------|
| Auth | 11 | No (for SendOTP/SendOTC) |
| Users | 11 | Yes |
| Facilities | 6 | Yes |
| Bridge | 11 | Yes |
| Locks | 6 | Yes |
| Cameras | 6 | Yes |
| Videos | 10 | Yes |
| System Support | 5 | Yes (Admin) |

## 🔐 Authentication Service (11 Endpoints)

### 1. Send OTP

```json
{
  "name": "Send OTP",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"phone_number\": \"{{phone_number}}\",\n  \"device_info\": \"iPhone 14 Pro, iOS 16.5, App v2.1.0\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/auth/otp/send",
      "host": ["{{base_url}}"],
      "path": ["api", "auth", "otp", "send"]
    },
    "description": "Send OTP code to user's phone number for authentication"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('OTP sent successfully', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.success).to.be.true;",
          "    pm.expect(response.message).to.exist;",
          "    pm.expect(response.expires_at).to.exist;",
          "    ",
          "    console.log('✅ OTP sent');",
          "    console.log('📅 Expires at:', response.expires_at);",
          "});",
          "",
          "pm.test('Response time under 2s', function() {",
          "    pm.expect(pm.response.responseTime).to.be.below(2000);",
          "});"
        ]
      }
    }
  ]
}
```

### 2. Verify OTP

```json
{
  "name": "Verify OTP",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"phone_number\": \"{{phone_number}}\",\n  \"otp_code\": \"123456\",\n  \"device_info\": \"iPhone 14 Pro, iOS 16.5, App v2.1.0\",\n  \"ip_address\": \"192.168.1.100\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/auth/otp/verify",
      "host": ["{{base_url}}"],
      "path": ["api", "auth", "otp", "verify"]
    },
    "description": "Verify OTP code and create authenticated session"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('OTP verified and session created', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.success).to.be.true;",
          "    pm.expect(response.session).to.exist;",
          "    pm.expect(response.session.session_token).to.exist;",
          "    pm.expect(response.session.refresh_token).to.exist;",
          "    pm.expect(response.session.user_id).to.be.a('number');",
          "    pm.expect(response.session.expires_at).to.exist;",
          "    ",
          "    // Save session data",
          "    pm.collectionVariables.set('session_token', response.session.session_token);",
          "    pm.collectionVariables.set('refresh_token', response.session.refresh_token);",
          "    pm.collectionVariables.set('user_id', response.session.user_id);",
          "    pm.collectionVariables.set('session_expires_at', response.session.expires_at);",
          "    ",
          "    console.log('✅ Session token saved');",
          "    console.log('👤 User ID:', response.session.user_id);",
          "    console.log('📅 Session expires:', response.session.expires_at);",
          "});",
          "",
          "pm.test('Session status is active', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.session.status).to.equal('SESSION_STATUS_ACTIVE');",
          "});"
        ]
      }
    }
  ]
}
```

### 3. Validate Session

```json
{
  "name": "Validate Session",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"session_token\": \"{{session_token}}\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/auth/session/validate",
      "host": ["{{base_url}}"],
      "path": ["api", "auth", "session", "validate"]
    },
    "description": "Validate current session token and get session details"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Session is valid', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.is_valid).to.be.true;",
          "    pm.expect(response.session).to.exist;",
          "    pm.expect(response.session.status).to.equal('SESSION_STATUS_ACTIVE');",
          "    ",
          "    console.log('✅ Session is valid');",
          "    console.log('👤 User ID:', response.session.user_id);",
          "    console.log('⏰ Expires:', response.session.expires_at);",
          "});"
        ]
      }
    }
  ]
}
```

### 4. Refresh Session

```json
{
  "name": "Refresh Session",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"refresh_token\": \"{{refresh_token}}\",\n  \"device_info\": \"iPhone 14 Pro, iOS 16.5\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/auth/session/refresh",
      "host": ["{{base_url}}"],
      "path": ["api", "auth", "session", "refresh"]
    },
    "description": "Refresh session using refresh token to get new session token"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Session refreshed successfully', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.success).to.be.true;",
          "    pm.expect(response.session).to.exist;",
          "    pm.expect(response.session.session_token).to.exist;",
          "    ",
          "    // Update session token",
          "    const oldToken = pm.collectionVariables.get('session_token');",
          "    pm.collectionVariables.set('session_token', response.session.session_token);",
          "    pm.collectionVariables.set('session_expires_at', response.session.expires_at);",
          "    ",
          "    console.log('✅ Session refreshed');",
          "    console.log('🔄 Old token:', oldToken.substring(0, 20) + '...');",
          "    console.log('🆕 New token:', response.session.session_token.substring(0, 20) + '...');",
          "    console.log('📅 New expiry:', response.session.expires_at);",
          "});"
        ]
      }
    }
  ]
}
```

### 5. Logout

```json
{
  "name": "Logout",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"session_token\": \"{{session_token}}\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/auth/logout",
      "host": ["{{base_url}}"],
      "path": ["api", "auth", "logout"]
    },
    "description": "Logout from current session and invalidate session token"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Logged out successfully', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.success).to.be.true;",
          "    pm.expect(response.message).to.exist;",
          "    ",
          "    console.log('✅ Logged out successfully');",
          "    console.log('📝 Message:', response.message);",
          "    ",
          "    // Optionally clear session token",
          "    // pm.collectionVariables.set('session_token', '');",
          "});"
        ]
      }
    }
  ]
}
```

## 👤 Users Service (11 Endpoints)

### Get User Profile

```json
{
  "name": "Get User Profile",
  "request": {
    "method": "GET",
    "header": [
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "url": {
      "raw": "{{base_url}}/api/users/{{user_id}}",
      "host": ["{{base_url}}"],
      "path": ["api", "users", "{{user_id}}"]
    },
    "description": "Get user profile information"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('User profile retrieved', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.user).to.exist;",
          "    pm.expect(response.user.id).to.equal(parseInt(pm.collectionVariables.get('user_id')));",
          "    pm.expect(response.user.phone_number).to.exist;",
          "    pm.expect(response.user.name).to.exist;",
          "    ",
          "    console.log('✅ User profile retrieved');",
          "    console.log('👤 Name:', response.user.name);",
          "    console.log('📞 Phone:', response.user.phone_number);",
          "    console.log('📧 Email:', response.user.email || 'Not set');",
          "});"
        ]
      }
    }
  ]
}
```

### Create User

```json
{
  "name": "Create User",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"phone_number\": \"+1234567890\",\n  \"name\": \"John Doe\",\n  \"email\": \"john.doe@example.com\",\n  \"profile_photo_url\": \"https://example.com/photos/johndoe.jpg\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/users",
      "host": ["{{base_url}}"],
      "path": ["api", "users"]
    },
    "description": "Create a new user"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('User created successfully', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.user).to.exist;",
          "    pm.expect(response.user.id).to.be.a('number');",
          "    pm.expect(response.user.phone_number).to.exist;",
          "    ",
          "    // Save created user ID for later use",
          "    pm.collectionVariables.set('created_user_id', response.user.id);",
          "    ",
          "    console.log('✅ User created');",
          "    console.log('🆔 ID:', response.user.id);",
          "    console.log('👤 Name:', response.user.name);",
          "});"
        ]
      }
    }
  ]
}
```

## 🏢 Facilities Service (6 Endpoints)

### List Facilities

```json
{
  "name": "List Facilities",
  "request": {
    "method": "GET",
    "header": [
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "url": {
      "raw": "{{base_url}}/api/facilities?page=1&page_size=20",
      "host": ["{{base_url}}"],
      "path": ["api", "facilities"],
      "query": [
        {"key": "page", "value": "1"},
        {"key": "page_size", "value": "20"}
      ]
    },
    "description": "List all facilities with pagination"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Facilities list retrieved', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.facilities).to.be.an('array');",
          "    pm.expect(response.total_count).to.be.a('number');",
          "    ",
          "    if (response.facilities.length > 0) {",
          "        // Save first facility ID for later use",
          "        pm.collectionVariables.set('facility_id', response.facilities[0].id);",
          "        ",
          "        console.log('✅ Facilities retrieved');",
          "        console.log('📊 Total count:', response.total_count);",
          "        console.log('📄 Page items:', response.facilities.length);",
          "        console.log('🏢 First facility:', response.facilities[0].name);",
          "    }",
          "});"
        ]
      }
    }
  ]
}
```

### Create Facility

```json
{
  "name": "Create Facility",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"name\": \"Downtown Tennis Club\",\n  \"address\": \"123 Main Street, Cityville, ST 12345\",\n  \"description\": \"Premier tennis facility with 8 courts, pro shop, and lounge\",\n  \"timezone\": \"America/New_York\",\n  \"contact_phone\": \"+1555123456\",\n  \"contact_email\": \"info@downtowntennis.com\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/facilities",
      "host": ["{{base_url}}"],
      "path": ["api", "facilities"]
    },
    "description": "Create a new facility"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Facility created successfully', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.facility).to.exist;",
          "    pm.expect(response.facility.id).to.be.a('number');",
          "    pm.expect(response.facility.name).to.exist;",
          "    ",
          "    // Save facility ID",
          "    pm.collectionVariables.set('facility_id', response.facility.id);",
          "    ",
          "    console.log('✅ Facility created');",
          "    console.log('🆔 ID:', response.facility.id);",
          "    console.log('🏢 Name:', response.facility.name);",
          "    console.log('🌍 Timezone:', response.facility.timezone);",
          "});"
        ]
      }
    }
  ]
}
```

## 🌉 Bridge Service (11 Endpoints)

### Register Bridge

```json
{
  "name": "Register Bridge",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"facility_id\": {{facility_id}},\n  \"name\": \"Main Building Bridge\",\n  \"mac_address\": \"B8:27:EB:AA:BB:CC\",\n  \"ip_address\": \"192.168.1.50\",\n  \"firmware_version\": \"1.2.3\",\n  \"hardware_version\": \"RPI4-B\",\n  \"location\": \"Main entrance, Equipment room B\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/bridges/register",
      "host": ["{{base_url}}"],
      "path": ["api", "bridges", "register"]
    },
    "description": "Register a new bridge device"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Bridge registered successfully', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.bridge).to.exist;",
          "    pm.expect(response.bridge.id).to.be.a('number');",
          "    pm.expect(response.bridge.mac_address).to.exist;",
          "    pm.expect(response.bridge.status).to.equal('BRIDGE_STATUS_OFFLINE');",
          "    ",
          "    // Save bridge ID",
          "    pm.collectionVariables.set('bridge_id', response.bridge.id);",
          "    pm.collectionVariables.set('bridge_mac', response.bridge.mac_address);",
          "    ",
          "    console.log('✅ Bridge registered');",
          "    console.log('🆔 ID:', response.bridge.id);",
          "    console.log('📍 MAC:', response.bridge.mac_address);",
          "    console.log('🏢 Facility:', response.bridge.facility_id);",
          "});"
        ]
      }
    }
  ]
}
```

## 🔒 Locks Service (6 Endpoints)

### Control Lock

```json
{
  "name": "Control Lock (Unlock)",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"facility_id\": {{facility_id}},\n  \"device_id\": \"{{lock_id}}\",\n  \"user_id\": {{user_id}},\n  \"action\": \"LOCK_ACTION_UNLOCK\",\n  \"reason\": \"Member access during court booking #12345\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/locks/control",
      "host": ["{{base_url}}"],
      "path": ["api", "locks", "control"]
    },
    "description": "Control lock device (unlock/lock)"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Lock controlled successfully', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.success).to.be.true;",
          "    pm.expect(response.command_id).to.exist;",
          "    pm.expect(response.status).to.exist;",
          "    ",
          "    // Save command ID to check status later",
          "    pm.collectionVariables.set('lock_command_id', response.command_id);",
          "    ",
          "    console.log('✅ Lock command sent');",
          "    console.log('🆔 Command ID:', response.command_id);",
          "    console.log('📊 Status:', response.status);",
          "});"
        ]
      }
    }
  ]
}
```

## 📹 Cameras Service (6 Endpoints)

### Control Camera (Start Stream)

```json
{
  "name": "Control Camera (Start Stream)",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"facility_id\": {{facility_id}},\n  \"device_id\": \"{{camera_id}}\",\n  \"user_id\": {{user_id}},\n  \"action\": \"CAMERA_ACTION_START_STREAM\",\n  \"parameters\": {\n    \"quality\": \"720p\",\n    \"duration_seconds\": 3600\n  }\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/cameras/control",
      "host": ["{{base_url}}"],
      "path": ["api", "cameras", "control"]
    },
    "description": "Control camera device (start/stop stream, record, snapshot)"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Camera command sent', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.success).to.be.true;",
          "    pm.expect(response.command_id).to.exist;",
          "    ",
          "    if (response.stream_url) {",
          "        pm.collectionVariables.set('camera_stream_url', response.stream_url);",
          "        console.log('📹 Stream URL:', response.stream_url);",
          "    }",
          "    ",
          "    console.log('✅ Camera command sent');",
          "    console.log('🆔 Command ID:', response.command_id);",
          "});"
        ]
      }
    }
  ]
}
```

## 🎥 Videos Service (10 Endpoints)

### Upload Video

```json
{
  "name": "Upload Video",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{session_token}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"title\": \"Court 1 - Tennis Match\",\n  \"description\": \"Singles match, 2024-01-15\",\n  \"facility_id\": {{facility_id}},\n  \"camera_id\": \"{{camera_id}}\",\n  \"duration_seconds\": 3600,\n  \"file_size_bytes\": 524288000,\n  \"format\": \"mp4\",\n  \"resolution\": \"1920x1080\",\n  \"recorded_at\": \"2024-01-15T14:00:00Z\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/videos/upload",
      "host": ["{{base_url}}"],
      "path": ["api", "videos", "upload"]
    },
    "description": "Initiate video upload and get upload URL"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Video upload initiated', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.video).to.exist;",
          "    pm.expect(response.video.id).to.be.a('number');",
          "    pm.expect(response.upload_url).to.exist;",
          "    ",
          "    // Save video ID and upload URL",
          "    pm.collectionVariables.set('video_id', response.video.id);",
          "    pm.collectionVariables.set('video_upload_url', response.upload_url);",
          "    ",
          "    console.log('✅ Video upload initiated');",
          "    console.log('🆔 Video ID:', response.video.id);",
          "    console.log('📤 Upload URL:', response.upload_url.substring(0, 50) + '...');",
          "});"
        ]
      }
    }
  ]
}
```

---

## 🔗 Request Chaining Example

Create a complete workflow:

1. **Send OTP** → saves nothing (just triggers SMS)
2. **Verify OTP** → saves `session_token`, `refresh_token`, `user_id`
3. **Get User Profile** → uses `user_id` from step 2
4. **List Facilities** → saves `facility_id` from first result
5. **Register Bridge** → uses `facility_id` from step 4, saves `bridge_id`
6. **Register Lock** → uses `facility_id` and `bridge_id`, saves `lock_id`
7. **Control Lock** → uses `facility_id`, `lock_id`, `user_id`

The test scripts automatically extract and save variables, so requests automatically chain!

---

## 💾 Environment Setup

Create these variables in your Postman environment:

```json
{
  "name": "rallymate Local",
  "values": [
    {"key": "base_url", "value": "http://localhost:8080"},
    {"key": "grpc_url", "value": "localhost:50051"},
    {"key": "phone_number", "value": "+1234567890"},
    {"key": "test_user_name", "value": "Test User"},
    {"key": "test_user_email", "value": "test@example.com"}
  ]
}
```

---

**🎉 You now have everything needed to build comprehensive Postman collections!**

Copy these examples, customize the test data, and you'll have fully functional request chaining with automated variable extraction.
