# 📖 Example Generated Collection

This is an example of what gets generated. The actual collections will be created when you run the generator.

## Sample: Auth Service Collection (Partial)

```json
{
  "info": {
    "name": "rallymate AuthService",
    "description": "Auto-generated collection for AuthService service with realistic test data",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "version": "2.0.0"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{session_token}}",
        "type": "string"
      }
    ]
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8080",
      "type": "string"
    }
  ],
  "item": [
    {
      "name": "Send OTP",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/auth/otp/send",
          "host": ["{{base_url}}"],
          "path": ["api", "auth", "otp", "send"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"phone_number\": \"+1234567890\",\n  \"device_info\": \"Test Device - Postman Collection\"\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        },
        "description": "**RPC:** SendOTP\n\n**Request:** SendOTPRequest\n\n**Response:** SendOTPResponse\n\n**Endpoint:** POST /api/auth/otp/send"
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "// Validate response status",
              "pm.test('Status is 200 OK', function() {",
              "    pm.response.to.have.status(200);",
              "});",
              "",
              "// Validate response time",
              "pm.test('Response time under 2s', function() {",
              "    pm.expect(pm.response.responseTime).to.be.below(2000);",
              "});",
              "",
              "// Parse and extract response data",
              "if (pm.response.code === 200) {",
              "    try {",
              "        const response = pm.response.json();",
              "        console.log('✅ Response:', JSON.stringify(response, null, 2));",
              "    } catch (e) {",
              "        console.log('⚠️ Could not parse response:', e);",
              "    }",
              "}"
            ],
            "type": "text/javascript"
          }
        }
      ]
    },
    {
      "name": "Verify OTP",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/auth/otp/verify",
          "host": ["{{base_url}}"],
          "path": ["api", "auth", "otp", "verify"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"phone_number\": \"+1234567890\",\n  \"otp_code\": \"123456\",\n  \"device_info\": \"Test Device - Postman Collection\",\n  \"ip_address\": \"192.168.1.100\"\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        },
        "description": "**RPC:** VerifyOTP\n\n**Request:** VerifyOTPRequest\n\n**Response:** VerifyOTPResponse\n\n**Endpoint:** POST /api/auth/otp/verify"
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "// Validate response status",
              "pm.test('Status is 200 OK', function() {",
              "    pm.response.to.have.status(200);",
              "});",
              "",
              "// Validate response time",
              "pm.test('Response time under 2s', function() {",
              "    pm.expect(pm.response.responseTime).to.be.below(2000);",
              "});",
              "",
              "// Parse and extract response data",
              "if (pm.response.code === 200) {",
              "    try {",
              "        const response = pm.response.json();",
              "        console.log('✅ Response:', JSON.stringify(response, null, 2));",
              "",
              "        // Extract session tokens",
              "        if (response.session && response.session.session_token) {",
              "            pm.collectionVariables.set('session_token', response.session.session_token);",
              "            console.log('🔑 Session token saved');",
              "        }",
              "        if (response.session && response.session.refresh_token) {",
              "            pm.collectionVariables.set('refresh_token', response.session.refresh_token);",
              "        }",
              "        if (response.session && response.session.user_id) {",
              "            pm.collectionVariables.set('user_id', response.session.user_id);",
              "            console.log('👤 User ID:', response.session.user_id);",
              "        }",
              "",
              "    } catch (e) {",
              "        console.log('⚠️ Could not parse response:', e);",
              "    }",
              "}"
            ],
            "type": "text/javascript"
          }
        }
      ]
    }
  ]
}
```

## Sample: Lock Control Request

```json
{
  "name": "Lock Control",
  "request": {
    "method": "POST",
    "header": [
      {
        "key": "Content-Type",
        "value": "application/json",
        "type": "text"
      }
    ],
    "url": {
      "raw": "{{base_url}}/api/locks/{{device_id}}/control",
      "host": ["{{base_url}}"],
      "path": ["api", "locks", "{{device_id}}", "control"]
    },
    "body": {
      "mode": "raw",
      "raw": "{\n  \"facility_id\": \"{{facility_id}}\",\n  \"device_id\": \"lock-court-01\",\n  \"user_id\": \"{{user_id}}\",\n  \"action\": \"LOCK_ACTION_UNLOCK\",\n  \"reason\": \"Testing via Postman collection\"\n}",
      "options": {
        "raw": {
          "language": "json"
        }
      }
    },
    "description": "**RPC:** LockControl\n\n**Request:** LockControlRequest\n\n**Response:** LockControlResponse\n\n**Endpoint:** POST /api/locks/{device_id}/control"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status is 200 OK', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Response time under 2s', function() {",
          "    pm.expect(pm.response.responseTime).to.be.below(2000);",
          "});",
          "",
          "if (pm.response.code === 200) {",
          "    try {",
          "        const response = pm.response.json();",
          "        console.log('✅ Response:', JSON.stringify(response, null, 2));",
          "    } catch (e) {",
          "        console.log('⚠️ Could not parse response:', e);",
          "    }",
          "}"
        ],
        "type": "text/javascript"
      }
    }
  ]
}
```

## Sample: Environment File

```json
{
  "id": "rallymate-local",
  "name": "rallymate - Local",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8080",
      "type": "default",
      "enabled": true
    },
    {
      "key": "phone_number",
      "value": "+1234567890",
      "type": "default",
      "enabled": true
    },
    {
      "key": "facility_id",
      "value": "1",
      "type": "default",
      "enabled": true
    },
    {
      "key": "session_token",
      "value": "",
      "type": "secret",
      "enabled": true
    },
    {
      "key": "refresh_token",
      "value": "",
      "type": "secret",
      "enabled": true
    },
    {
      "key": "user_id",
      "value": "",
      "type": "default",
      "enabled": true
    },
    {
      "key": "device_id",
      "value": "bridge-001",
      "type": "default",
      "enabled": true
    }
  ],
  "_postman_variable_scope": "environment",
  "_postman_exported_at": "2025-10-15T10:00:00.000Z",
  "_postman_exported_using": "Postman Collection Generator"
}
```

## Key Features Demonstrated

### ✅ Realistic Data
- Phone numbers: `+1234567890`
- Device IDs: `lock-court-01`
- Enums: `LOCK_ACTION_UNLOCK`
- Timestamps: RFC3339 format

### ✅ Variable Usage
- Path parameters: `{{device_id}}`
- Auth: `{{session_token}}`
- IDs: `{{facility_id}}`, `{{user_id}}`

### ✅ Smart Tests
- Status validation
- Response time checks
- Variable extraction
- Console logging

### ✅ Proper Structure
- Postman v2.1 format
- Valid JSON
- Complete metadata
- Bearer authentication

---

## To Generate Actual Collections

```bash
cd rallymate-postman-collection/v2
./generate-all.sh
```

This will create:
- 8 complete service collections
- 3 environment files
- All with realistic data
- Ready to import into Postman

---

**Note:** This is just a preview. Run the generator to get the full collections with all 72+ endpoints!
