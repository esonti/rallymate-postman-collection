# 🚀 rallymate Services - Postman Collections v2

**Comprehensive, auto-generated Postman collections with realistic test data for all rallymate Services**

> **NEW:** Complete generator that creates collections from proto files with intelligent test data!

---

## 🎯 Quick Start (3 Steps)

### 1️⃣ Generate Collections
```bash
cd rallymate-postman-collection/v2
chmod +x generate-all.sh
./generate-all.sh
```

### 2️⃣ Import to Postman
1. Open Postman
2. Click **Import** → Select all `.json` files from `generated/` folder
3. Select **"rallymate - Local"** environment

### 3️⃣ Start Testing
1. Open **"rallymate AuthService"**
2. Run **"Send OTP"** → **"Verify OTP"**
3. ✅ Session token auto-saved - test other endpoints!

---

## 📦 What You Get

### ✨ 8 Complete Collections (72+ Endpoints)
- **auth_service** - Authentication (OTP/OTC, Sessions, Logout)
- **users_service** - User Management & Memberships
- **facilities_service** - Facility CRUD Operations
- **locks_service** - Smart Lock Control & Activities
- **cameras_service** - Camera Control & Activities
- **videos_service** - Video Management & Associations
- **bridge_service** - Bridge Devices, Edges, Tunnels
- **system_support_service** - Admin Role Management

### 🌍 3 Pre-configured Environments
- Local Development (localhost:8080)
- Development Server
- Production API

### 🎯 Key Features
- ✅ **Realistic test data** (no placeholders!)
- ✅ **Automatic variable extraction** (tokens, IDs, etc.)
- ✅ **Smart test scripts** with validation
- ✅ **Request chaining** support
- ✅ **Context-aware data** generation
- ✅ **Enum value** support from proto files

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | 3-step setup guide |
| **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** | Complete overview of what was built |
| **[GENERATOR_COMPLETE.md](GENERATOR_COMPLETE.md)** | Technical documentation |
| **[generated/README.md](generated/README.md)** | Full user guide with all endpoints |
| **[EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md)** | Sample generated collections |

---

## 🎬 Example: What Gets Generated

### Realistic Test Data
```json
{
  "phone_number": "+1234567890",
  "name": "Downtown Tennis Club",
  "device_id": "lock-court-01",
  "action": "LOCK_ACTION_UNLOCK",
  "start_date": "2025-10-15T10:00:00Z"
}
```

### Smart Test Scripts
```javascript
// Auto-extracts session tokens
if (response.session && response.session.session_token) {
    pm.collectionVariables.set('session_token', response.session.session_token);
    console.log('🔑 Session token saved');
}
```

---

## 🔧 Testing the Generator

Before generating collections, test the generator:
```bash
python3 test_generator.py
```

This validates:
- ✅ Python dependencies
- ✅ Proto files exist
- ✅ Parser functionality
- ✅ Data generation
- ✅ Collection structure

---

## 🎯 Test Workflows

### User Authentication Flow
```
1. Send OTP → 2. Verify OTP (extracts token) → 3. Get Profile
```

### Device Setup Flow
```
1. Send OTC → 2. Verify OTC → 3. Register Bridge → 4. Register Lock
```

### Access Control Flow
```
1. Auth → 2. Get Locks → 3. Unlock → 4. Check Activities
```

---

## 💡 Why This Generator is Better

| Feature | Old Script | New Generator |
|---------|-----------|---------------|
| Test Data | Generic placeholders | Realistic, context-aware |
| Enums | Not supported | Uses actual proto values |
| Variables | Manual setup | Auto-extraction |
| Tests | Basic | Comprehensive validation |
| Documentation | Minimal | Complete guides |

---

## 📋 File Structure

```
v2/
├── generate_postman_collections.py  ⭐ Main generator (850+ lines)
├── generate-all.sh                  Quick generation script
├── test_generator.py                Validation tests
├── QUICKSTART.md                    3-step guide
├── IMPLEMENTATION_SUMMARY.md        Complete overview
├── GENERATOR_COMPLETE.md            Technical docs
├── EXAMPLE_OUTPUT.md                Sample outputs
└── generated/                       Output directory
    ├── README.md                    User guide (500+ lines)
    ├── *.postman_collection.json    8 collections
    └── *.postman_environment.json   3 environments
```

---

## 🐛 Troubleshooting

### Generator Issues

**Proto files not found?**
```bash
# Check path
ls ../../rallymate-api/protos/*.proto

# Run from correct directory
cd rallymate-postman-collection/v2
```

**Permission denied?**
```bash
chmod +x generate-all.sh
chmod +x test_generator.py
```

**Python errors?**
```bash
# Check Python version (need 3.6+)
python3 --version

# Test generator
python3 test_generator.py
```

### Postman Issues

**401 Unauthorized?**
→ Run auth flow first (Send OTP → Verify OTP)

**Variables not extracted?**
→ Check Console tab for errors

**Can't import collections?**
→ Ensure files are valid JSON (check generator output)

---

## 🎓 Advanced Usage

### Custom Data Generation

Edit `generate_postman_collections.py`:
```python
class TestDataGenerator:
    @staticmethod
    def generate_value(field_name: str, field_type: str, context: str = "") -> Any:
        # Add your custom logic here
        if 'phone' in field_name.lower():
            return "+YOUR_PHONE_NUMBER"
```

### Custom Test Scripts

Collections are regenerable, so you can:
1. Generate base collections
2. Import to Postman
3. Customize test scripts
4. Export for team sharing

### CI/CD Integration

Use Newman for automation:
```bash
newman run generated/auth_service.postman_collection.json \
  -e generated/rallymate-local.postman_environment.json
```

---

## 🚀 Next Steps

### For Testing:
1. ✅ Generate collections
2. ✅ Import to Postman
3. ✅ Run auth flow
4. ✅ Test your APIs

### For Development:
1. Update proto files
2. Regenerate collections
3. Collections auto-update

### For Team:
1. Share generated collections
2. Build automated test suites
3. Integrate with CI/CD

---

## 📞 Support

- 📖 Read [QUICKSTART.md](QUICKSTART.md) for immediate help
- 📖 See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for details
- 📖 Check [generated/README.md](generated/README.md) for API docs
- 🧪 Run `python3 test_generator.py` to validate setup

---

## ✨ What Makes This Special

**Before (old script):**
```json
{
  "phone_number": "string",
  "device_info": "string"
}
```

**After (new generator):**
```json
{
  "phone_number": "+1234567890",
  "device_info": "Test Device - Postman Collection",
  "action": "LOCK_ACTION_UNLOCK"
}
```

Plus auto-extraction, smart tests, and complete documentation!

---

**Ready to start?** Run `./generate-all.sh` 🚀

---

## 📦 Original Collections (Legacy)

The sections below describe the original manually-created collections.
**New users should use the generator above instead.**

---

## 📦 What's Included (Legacy)

### Collections

1. **`rallymate_Services_HTTP_REST_API_v2.postman_collection.json`**
   - Complete HTTP REST API coverage via gRPC-Gateway
   - All services: Auth, Users, Facilities, Bridge, Locks, Cameras, Videos, System Support
   - Realistic test data for all endpoints
   - Automated response validation and variable extraction

2. **`rallymate_Services_gRPC_API_v2.postman_collection.json`**
   - Direct gRPC endpoint testing
   - Protobuf message examples
   - Binary payload handling

3. **`rallymate_Bridge_Edge_API_v2.postman_collection.json`**
   - Bridge device API endpoints
   - Health, Provisioning, and Device management
   - Edge-specific testing scenarios

### Environments

1. **`rallymate-local.postman_environment.json`** - Local development (localhost:8080)
2. **`rallymate-development.postman_environment.json`** - Dev server
3. **`rallymate-production.postman_environment.json`** - Production (template)

---

## 🎯 Key Features

### ✨ Realistic Test Data
Every endpoint includes:
- **Meaningful example data** based on actual use cases
- **Multiple scenarios** (success, failure, edge cases)
- **Sample user data** (phone numbers, names, emails)
- **Device identifiers** (bridges, locks, cameras)
- **Timestamp examples** in RFC3339 format

### 🔧 Automated Test Scripts
Each request includes scripts to:
- **Extract data** from responses (IDs, tokens, timestamps)
- **Store in variables** for use in subsequent requests
- **Validate responses** (status codes, required fields)
- **Chain requests** automatically
- **Handle authentication** token management

### 🔗 Request Chaining
Collections support automatic workflows:
```
Send OTP → Verify OTP → Get Profile → Create Membership → Update User
```

Variables are automatically extracted and used:
- `session_token` - Auth token for requests
- `user_id` - Created user ID
- `facility_id` - Facility identifier
- `device_id` - Device identifier
- `membership_id` - Membership ID
- And many more...

---

## 🚀 Quick Start

### 1. Import Collections

**In Postman:**
1. Click **Import**
2. Select all `.postman_collection.json` files
3. Click **Import**

### 2. Import Environment

1. Click **Import**
2. Select `rallymate-local.postman_environment.json`
3. Click **Import**
4. Select the environment from the dropdown (top right)

### 3. Configure Environment

Set these variables in your environment:

| Variable | Description | Example |
|----------|-------------|---------|
| `base_url` | API base URL | `http://localhost:8080` |
| `grpc_url` | gRPC endpoint | `localhost:50051` |
| `phone_number` | Test phone number | `+1234567890` |
| `device_id` | Test device ID | `bridge-001` |
| `facility_id` | Test facility ID | `1` |

### 4. Run Authentication Flow

**For User Authentication:**
1. Run `Auth → SendOTP`
2. Check console/SMS for OTP code
3. Run `Auth → VerifyOTP`
4. Session token automatically saved to `{{session_token}}`

**For Device Authentication:**
1. Run `Auth → SendOTC`
2. Get OTC from platform
3. Run `Auth → VerifyOTC`
4. Device session token saved

### 5. Use Authenticated Endpoints

All subsequent requests automatically use `{{session_token}}` via Bearer authentication.

---

## 📚 Collection Structure

### 1. Authentication Service

#### OTP Flow (Users)
- **POST** `/api/auth/otp/send` - Send OTP to phone
- **POST** `/api/auth/otp/verify` - Verify OTP code

#### OTC Flow (Devices)
- **POST** `/api/auth/otc/send` - Send OTC for device
- **POST** `/api/auth/otc/verify` - Verify OTC code

#### Session Management
- **POST** `/api/auth/session/refresh` - Refresh session token
- **POST** `/api/auth/session/validate` - Validate current session
- **POST** `/api/auth/session/revoke` - Revoke session
- **GET** `/api/auth/sessions/user/{user_id}` - Get user sessions
- **GET** `/api/auth/sessions/device/{device_id}` - Get device sessions

#### Logout
- **POST** `/api/auth/logout` - Logout current session
- **POST** `/api/auth/logout/all` - Logout all devices
- **POST** `/api/auth/admin/logout` - Admin logout user

### 2. Users Service

#### Profile Management
- **GET** `/api/users/profile` - Get current user profile
- **GET** `/api/users` - List users (with filters)
- **POST** `/api/users` - Create user
- **PUT** `/api/users/{id}` - Update user
- **DELETE** `/api/users/{id}` - Delete user

#### User Discovery
- **GET** `/api/users/discover` - Discover users (search)

#### Membership Management
- **POST** `/api/users/memberships/phone` - Create membership by phone
- **POST** `/api/users/memberships/user` - Create membership by user ID
- **PUT** `/api/users/memberships/{membership_id}` - Update membership
- **DELETE** `/api/users/memberships/{membership_id}` - Delete membership
- **GET** `/api/users/{user_id}/memberships` - Get user memberships
- **GET** `/api/facilities/{facility_id}/memberships` - Get facility members

### 3. Facilities Service

#### Facility CRUD
- **GET** `/api/facilities` - List facilities
- **GET** `/api/facilities/{id}` - Get facility
- **POST** `/api/facilities` - Create facility
- **PUT** `/api/facilities/{id}` - Update facility
- **DELETE** `/api/facilities/{id}` - Delete facility
- **GET** `/api/facilities/user/{user_id}` - Get user's facilities

### 4. Bridge Service

#### Bridge Management
- **POST** `/api/bridges/register` - Register bridge
- **DELETE** `/api/bridges/{device_id}/unregister` - Unregister bridge
- **PUT** `/api/bridges/{device_id}` - Update bridge
- **GET** `/api/bridges` - List bridges (with filters)

#### Edge Connections
- **POST** `/api/bridges/{bridge_device_id}/connections` - Register edge connection
- **DELETE** `/api/bridges/connections/{connection_id}` - Delete edge connection
- **PUT** `/api/bridges/{bridge_device_id}/connections/{edge_device_id}` - Update connection
- **GET** `/api/bridges/{bridge_device_id}/connections` - List connections

#### Tunnel Management
- **POST** `/api/tunnels` - Create tunnel
- **POST** `/api/tunnels/reserve` - Reserve tunnel port
- **POST** `/api/tunnels/{tunnel_id}/establish` - Establish tunnel
- **POST** `/api/tunnels/{tunnel_id}/close` - Close tunnel
- **GET** `/api/tunnels` - List tunnels
- **GET** `/api/tunnels/ports/available` - Get available ports
- **PUT** `/api/tunnels/{tunnel_id}/stats` - Update tunnel stats

#### Activities
- **GET** `/api/bridges/activities` - Get bridge activities

### 5. Locks Service

#### Lock Management
- **POST** `/api/locks/register` - Register lock
- **DELETE** `/api/locks/{device_id}/unregister` - Unregister lock
- **PUT** `/api/locks/{device_id}` - Update lock
- **GET** `/api/locks` - List locks (with filters)

#### Lock Control
- **POST** `/api/locks/{device_id}/control` - Control lock (lock/unlock)

#### Activities
- **GET** `/api/locks/activities` - Get lock activities

### 6. Cameras Service

#### Camera Management
- **POST** `/api/cameras/register` - Register camera
- **DELETE** `/api/cameras/{device_id}/unregister` - Unregister camera
- **PUT** `/api/cameras/{device_id}` - Update camera
- **GET** `/api/cameras` - List cameras (with filters)

#### Camera Control
- **POST** `/api/cameras/{device_id}/control` - Control camera (start/stop recording)

#### Activities
- **GET** `/api/cameras/activities` - Get camera activities

### 7. Videos Service

#### Video Management
- **GET** `/api/videos` - List videos
- **GET** `/api/videos/{id}` - Get video
- **GET** `/api/videos/user/{user_id}` - Get user's videos
- **POST** `/api/videos/upload` - Upload video
- **PUT** `/api/videos/{id}` - Update video
- **DELETE** `/api/videos/{id}` - Delete video

#### Video Associations
- **POST** `/api/videos/{video_id}/users/{user_id}` - Associate video to user
- **DELETE** `/api/videos/{video_id}/users/{user_id}` - Remove association
- **GET** `/api/videos/{video_id}/associations` - Get video associations
- **POST** `/api/videos/associate/bulk` - Bulk associate videos
- **GET** `/api/users/{user_id}/video-associations` - Get user's video associations

### 8. System Support Service

#### Admin Management
- **GET** `/api/system-support/user/{user_id}` - Get user's admin role
- **POST** `/api/system-support` - Create admin role
- **PUT** `/api/system-support/{support_id}` - Update admin role
- **DELETE** `/api/system-support/{support_id}` - Delete admin role
- **GET** `/api/system-support/admins` - List all admins

---

## 🧪 Example Request: Send OTP

```http
POST {{base_url}}/api/auth/otp/send
Content-Type: application/json

{
  "phone_number": "+1234567890",
  "device_info": "iPhone 14 Pro, iOS 16.5"
}
```

**Test Script:**
```javascript
pm.test("Status is 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("Response has success field", function() {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('success');
    pm.expect(jsonData.success).to.be.true;
});

pm.test("Response has expires_at", function() {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('expires_at');
    console.log('OTP expires at:', jsonData.expires_at);
});
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "expires_at": "2025-10-15T10:15:00Z"
}
```

---

## 🧪 Example Request: Verify OTP

```http
POST {{base_url}}/api/auth/otp/verify
Content-Type: application/json

{
  "phone_number": "+1234567890",
  "otp_code": "123456",
  "device_info": "iPhone 14 Pro, iOS 16.5",
  "ip_address": "192.168.1.100"
}
```

**Test Script:**
```javascript
pm.test("Status is 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("Response has session", function() {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('session');
    pm.expect(jsonData.session).to.have.property('session_token');
    pm.expect(jsonData.session).to.have.property('refresh_token');
    
    // Extract and save tokens
    pm.collectionVariables.set('session_token', jsonData.session.session_token);
    pm.collectionVariables.set('refresh_token', jsonData.session.refresh_token);
    pm.collectionVariables.set('user_id', jsonData.session.user_id);
    
    console.log('✅ Session token saved:', jsonData.session.session_token.substring(0, 20) + '...');
    console.log('✅ User ID:', jsonData.session.user_id);
});
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "session": {
    "id": 123,
    "user_id": 456,
    "session_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "refresh_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "status": "SESSION_STATUS_ACTIVE",
    "expires_at": "2025-10-16T10:00:00Z",
    "created_at": "2025-10-15T10:00:00Z"
  }
}
```

---

## 🔐 Authentication Flow

### User Authentication (OTP)
```
1. Send OTP
   POST /api/auth/otp/send
   Body: { "phone_number": "+1234567890" }
   
2. Verify OTP
   POST /api/auth/otp/verify
   Body: { "phone_number": "+1234567890", "otp_code": "123456" }
   
3. Extract Token
   session_token → Saved automatically
   
4. Use Token
   All requests: Authorization: Bearer {{session_token}}
```

### Device Authentication (OTC)
```
1. Send OTC
   POST /api/auth/otc/send
   Body: { "device_id": "bridge-001" }
   
2. Verify OTC
   POST /api/auth/otc/verify
   Body: { "device_id": "bridge-001", "otc_code": "ABC123" }
   
3. Extract Token
   session_token → Saved automatically
   ca_endpoint, mqtt_endpoint → Also extracted
   
4. Use Token
   All requests: Authorization: Bearer {{session_token}}
```

---

## 📊 Test Data Examples

### Users
```json
{
  "phone_number": "+1234567890",
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

### Facilities
```json
{
  "name": "Downtown Tennis Club",
  "address": "123 Main St, City, State 12345",
  "description": "Premier tennis facility with 12 courts",
  "timezone": "America/New_York"
}
```

### Locks
```json
{
  "facility_id": 1,
  "device_id": "lock-court-01",
  "name": "Court 1 Gate Lock"
}
```

### Cameras
```json
{
  "facility_id": 1,
  "device_id": "camera-court-01",
  "name": "Court 1 Camera"
}
```

### Lock Control
```json
{
  "facility_id": 1,
  "device_id": "lock-court-01",
  "user_id": 456,
  "action": "LOCK_ACTION_UNLOCK",
  "reason": "Member access during booking"
}
```

---

## 🔧 Variable Management

### Collection Variables (Auto-populated)
- `session_token` - Current session token
- `refresh_token` - Token refresh credential
- `user_id` - Current user ID
- `facility_id` - Current facility ID
- `device_id` - Current device ID
- `membership_id` - Created membership ID
- `video_id` - Uploaded video ID
- `tunnel_id` - Created tunnel ID

### Environment Variables (Configure manually)
- `base_url` - API base URL
- `grpc_url` - gRPC endpoint
- `phone_number` - Your test phone number
- `test_facility_id` - Test facility
- `test_device_id` - Test device

---

## 🧩 Request Chaining Examples

### Create User with Membership
```
1. Create Facility → Extract facility_id
2. Create User → Extract user_id
3. Create Membership (phone) → Uses extracted IDs
4. Get User Profile → Verify membership exists
```

### Register and Control Device
```
1. Register Bridge → Extract device_id
2. Register Lock → Extract lock_id
3. Register Edge Connection → Link lock to bridge
4. Lock Control → Use extracted IDs
5. Get Lock Activities → Verify control logged
```

### Video Upload and Association
```
1. Upload Video → Extract video_id
2. Get User Profile → Extract user_id
3. Associate Video to User → Use extracted IDs
4. Get User Videos → Verify association
```

---

## 🐛 Troubleshooting

### Issue: Authentication fails
**Solution:** Ensure you're using a valid phone number and OTP code. Check console logs for details.

### Issue: Session token expired
**Solution:** Run the Refresh Session request or re-authenticate with OTP.

### Issue: Variables not extracted
**Solution:** Check the test script tab of requests. Ensure response structure matches expected format.

### Issue: Request fails with 401
**Solution:** Verify `{{session_token}}` is set and valid. Re-run authentication flow.

### Issue: Device not found
**Solution:** Register the device first using the registration endpoints.

---

## 📖 Additional Resources

- **Proto Definitions**: `rallymate-api/protos/`
- **API Documentation**: See proto file comments
- **gRPC-Gateway**: HTTP endpoints mirror gRPC methods
- **Postman Docs**: https://learning.postman.com/

---

## 🎯 Best Practices

1. **Always authenticate first** - Run OTP/OTC flow before other requests
2. **Check test scripts** - Review extracted variables in console
3. **Use environments** - Switch between local/dev/prod easily
4. **Chain requests** - Build workflows by running requests in sequence
5. **Save responses** - Use Postman's save response feature for reference
6. **Monitor variables** - Check collection/environment variables tab
7. **Read test results** - Review test tab after each request

---

## 🚦 Getting Started Checklist

- [ ] Import all collections
- [ ] Import environment file
- [ ] Configure environment variables
- [ ] Run SendOTP request
- [ ] Get OTP from console/SMS
- [ ] Run VerifyOTP request
- [ ] Verify session_token is saved
- [ ] Run GetUserProfile to test authentication
- [ ] Explore other endpoints
- [ ] Build your own test workflows

---

**Version:** 2.0  
**Last Updated:** October 15, 2025  
**Compatible with:** rallymate-services v2.0+

**Happy Testing! 🚀**
