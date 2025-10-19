# 🏗️ Building Comprehensive Postman Collections

This guide explains how to create comprehensive Postman collections for RallyMate Services with all the features you requested.

## 📋 Requirements

Your collections should include:
1. ✅ All HTTP REST endpoints from proto annotations
2. ✅ All gRPC endpoints  
3. ✅ Meaningful example test data for request bodies
4. ✅ Test scripts to extract and store response data
5. ✅ Variable management for request chaining

## 🛠️ Tools & Approach

### Option 1: Manual Creation in Postman (Recommended)
Create collections directly in Postman UI with full features.

**Advantages:**
- Rich UI for editing
- Built-in test script editor
- Variable management
- Easy request organization
- Export when done

**Steps:**
1. Open Postman
2. Create New Collection
3. Add requests following the structure below
4. Add test scripts to each request
5. Export as JSON

### Option 2: Programmatic Generation
Generate collections from proto files programmatically.

**Tools Available:**
- `grpc-gateway` - Generates OpenAPI/Swagger from protos
- `postman-collection-sdk` - Build collections programmatically
- Custom scripts - Parse protos and generate JSON

### Option 3: Hybrid Approach (This Repository)
- Core structure generated/documented
- Manual refinement for test scripts
- Version controlled JSON files

## 📝 Collection Structure Template

```json
{
  "info": {
    "name": "Service Name",
    "description": "Service description",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [{"key": "token", "value": "{{session_token}}"}]
  },
  "variable": [
    {"key": "base_url", "value": "http://localhost:8080"},
    {"key": "session_token", "value": ""}
  ],
  "item": [
    {
      "name": "Folder Name",
      "item": [/* requests */]
    }
  ]
}
```

## 🧪 Request Template with Test Scripts

```json
{
  "name": "Request Name",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"field\": \"value\"\n}"
    },
    "url": {
      "raw": "{{base_url}}/api/endpoint",
      "host": ["{{base_url}}"],
      "path": ["api", "endpoint"]
    }
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "// Test script here",
          "pm.test('Status is 200', function() {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "// Extract data",
          "const response = pm.response.json();",
          "pm.collectionVariables.set('extracted_id', response.id);"
        ]
      }
    }
  ]
}
```

## 🎯 Implementation Guide

### Step 1: Create Base Collection Structure

Create file: `RallyMate_Services_HTTP_REST_API_v2.postman_collection.json`

Add:
- Collection info
- Global authentication
- Collection variables
- Event scripts (pre-request, test)

### Step 2: Add Service Folders

For each service (Auth, Users, Facilities, etc.):
```json
{
  "name": "1. Authentication Service",
  "description": "User and device authentication",
  "item": [/* requests */]
}
```

### Step 3: Add Requests per Endpoint

For each endpoint from proto files:

**From proto:**
```protobuf
rpc SendOTP(SendOTPRequest) returns (SendOTPResponse) {
  option (google.api.http) = {
    post: "/api/auth/otp/send"
    body: "*"
  };
}
```

**Create request:**
```json
{
  "name": "Send OTP",
  "request": {
    "method": "POST",
    "url": "{{base_url}}/api/auth/otp/send",
    "body": {
      "mode": "raw",
      "raw": "{\n  \"phone_number\": \"{{phone_number}}\",\n  \"device_info\": \"Test Device\"\n}"
    }
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('OTP sent successfully', function() {",
          "    const response = pm.response.json();",
          "    pm.expect(response.success).to.be.true;",
          "    console.log('OTP expires at:', response.expires_at);",
          "});"
        ]
      }
    }
  ]
}
```

### Step 4: Add Realistic Test Data

**Good Examples:**
```json
// Users
{
  "phone_number": "+1234567890",
  "name": "John Doe",
  "email": "john.doe@example.com"
}

// Facilities  
{
  "name": "Downtown Tennis Club",
  "address": "123 Main St, Cityville, ST 12345",
  "description": "Premier tennis facility",
  "timezone": "America/New_York"
}

// Device Control
{
  "facility_id": 1,
  "device_id": "lock-court-01",
  "user_id": 456,
  "action": "LOCK_ACTION_UNLOCK",
  "reason": "Member access during booking"
}
```

### Step 5: Add Test Scripts for Data Extraction

**Template for extraction:**
```javascript
pm.test("Extract response data", function() {
    const response = pm.response.json();
    
    // Extract and save ID
    if (response.id) {
        pm.collectionVariables.set('created_id', response.id);
        console.log('✅ Saved ID:', response.id);
    }
    
    // Extract and save token
    if (response.session && response.session.session_token) {
        pm.collectionVariables.set('session_token', response.session.session_token);
        console.log('✅ Saved session token');
    }
    
    // Extract nested data
    if (response.user && response.user.id) {
        pm.collectionVariables.set('user_id', response.user.id);
    }
});
```

### Step 6: Add Response Validation

**Template for validation:**
```javascript
// Status code validation
pm.test("Status is 200 OK", function() {
    pm.response.to.have.status(200);
});

// Response time validation
pm.test("Response time under 1s", function() {
    pm.expect(pm.response.responseTime).to.be.below(1000);
});

// Required fields validation
pm.test("Response has required fields", function() {
    const response = pm.response.json();
    pm.expect(response).to.have.property('success');
    pm.expect(response).to.have.property('message');
});

// Data type validation
pm.test("ID is a number", function() {
    const response = pm.response.json();
    pm.expect(response.id).to.be.a('number');
});

// Enum validation
pm.test("Status is valid enum", function() {
    const response = pm.response.json();
    pm.expect(response.status).to.be.oneOf([
        'SESSION_STATUS_ACTIVE',
        'SESSION_STATUS_EXPIRED',
        'SESSION_STATUS_REVOKED'
    ]);
});
```

## 📚 Complete Example: Auth Service

Here's a complete example for the Auth service folder:

```json
{
  "name": "1. Authentication Service",
  "description": "User and device authentication with OTP/OTC",
  "item": [
    {
      "name": "OTP Flow",
      "item": [
        {
          "name": "Send OTP",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status is 200', () => pm.response.to.have.status(200));",
                  "pm.test('OTP sent', function() {",
                  "    const res = pm.response.json();",
                  "    pm.expect(res.success).to.be.true;",
                  "    pm.expect(res).to.have.property('expires_at');",
                  "    console.log('✅ OTP sent, expires:', res.expires_at);",
                  "});"
                ]
              }
            }
          ],
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"phone_number\": \"{{phone_number}}\",\n  \"device_info\": \"iPhone 14 Pro, iOS 16.5\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/auth/otp/send",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "otp", "send"]
            },
            "description": "Send OTP code to user's phone number"
          }
        },
        {
          "name": "Verify OTP",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status is 200', () => pm.response.to.have.status(200));",
                  "pm.test('OTP verified and session created', function() {",
                  "    const res = pm.response.json();",
                  "    pm.expect(res.success).to.be.true;",
                  "    pm.expect(res.session).to.exist;",
                  "    pm.expect(res.session.session_token).to.exist;",
                  "    pm.expect(res.session.refresh_token).to.exist;",
                  "    ",
                  "    // Save tokens",
                  "    pm.collectionVariables.set('session_token', res.session.session_token);",
                  "    pm.collectionVariables.set('refresh_token', res.session.refresh_token);",
                  "    pm.collectionVariables.set('user_id', res.session.user_id);",
                  "    ",
                  "    console.log('✅ Session token saved');",
                  "    console.log('✅ User ID:', res.session.user_id);",
                  "});"
                ]
              }
            }
          ],
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"phone_number\": \"{{phone_number}}\",\n  \"otp_code\": \"123456\",\n  \"device_info\": \"iPhone 14 Pro, iOS 16.5\",\n  \"ip_address\": \"192.168.1.100\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/auth/otp/verify",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "otp", "verify"]
            },
            "description": "Verify OTP code and create session"
          }
        }
      ]
    }
  ]
}
```

## 🔄 Proto to Request Mapping

### From Proto File
```protobuf
message SendOTPRequest {
  string phone_number = 1;
  string device_info = 2;
}

message SendOTPResponse {
  bool success = 1;
  string message = 2;
  string expires_at = 3;
}

rpc SendOTP(SendOTPRequest) returns (SendOTPResponse) {
  option (google.api.http) = {
    post: "/api/auth/otp/send"
    body: "*"
  };
}
```

### To Postman Request
```json
{
  "name": "Send OTP",
  "request": {
    "method": "POST",
    "url": "{{base_url}}/api/auth/otp/send",
    "body": {
      "mode": "raw",
      "raw": "{\n  \"phone_number\": \"string\",\n  \"device_info\": \"string\"\n}"
    }
  }
}
```

### With Test Script
```json
{
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "const response = pm.response.json();",
        "pm.expect(response).to.have.property('success');",
        "pm.expect(response).to.have.property('message');",
        "pm.expect(response).to.have.property('expires_at');"
      ]
    }
  }]
}
```

## 🎨 Test Script Patterns

### Pattern 1: Extract Single Value
```javascript
const response = pm.response.json();
pm.collectionVariables.set('user_id', response.user.id);
```

### Pattern 2: Extract Multiple Values
```javascript
const response = pm.response.json();
pm.collectionVariables.set('facility_id', response.facility.id);
pm.collectionVariables.set('facility_name', response.facility.name);
pm.collectionVariables.set('facility_timezone', response.facility.timezone);
```

### Pattern 3: Extract from Array
```javascript
const response = pm.response.json();
if (response.users && response.users.length > 0) {
    pm.collectionVariables.set('first_user_id', response.users[0].id);
}
```

### Pattern 4: Conditional Extraction
```javascript
const response = pm.response.json();
if (response.success && response.session) {
    pm.collectionVariables.set('session_token', response.session.session_token);
} else {
    console.log('⚠️ No session in response');
}
```

### Pattern 5: Extract and Transform
```javascript
const response = pm.response.json();
// Extract timestamp and convert
const expiresAt = new Date(response.expires_at);
pm.collectionVariables.set('expires_timestamp', expiresAt.getTime());
```

## 🚀 Next Steps

1. **Start with core endpoints** (Auth, Users)
2. **Build incrementally** - Add service by service
3. **Test as you go** - Verify each request works
4. **Document examples** - Add descriptions to requests
5. **Export regularly** - Save your progress
6. **Version control** - Commit JSON files to git

## 📦 Recommended Structure

```
v2/
├── README.md (this file)
├── BUILDING_COLLECTIONS.md (current file)
├── RallyMate_Services_HTTP_REST_API_v2.postman_collection.json
├── RallyMate_Services_gRPC_API_v2.postman_collection.json
├── RallyMate_Bridge_Edge_API_v2.postman_collection.json
├── environments/
│   ├── rallymate-local.postman_environment.json
│   ├── rallymate-development.postman_environment.json
│   └── rallymate-production.postman_environment.json
└── examples/
    ├── request-templates/
    ├── test-script-templates/
    └── sample-data/
```

## 💡 Pro Tips

1. **Use folders** - Organize by service/feature
2. **Add descriptions** - Document each request
3. **Consistent naming** - Follow pattern: "Verb Resource"
4. **Pre-request scripts** - Set up auth automatically
5. **Collection variables** - Share data between requests
6. **Environment variables** - Switch contexts easily
7. **Test suites** - Group related requests
8. **Export/Import** - Back up your work regularly

---

**Ready to build?** Start with the Authentication service and work your way through each service systematically!
