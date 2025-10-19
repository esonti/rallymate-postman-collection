# 📦 RallyMate Postman Collections - Generated

**Auto-generated Postman collections with realistic test data for all RallyMate services**

---

## 🎯 What's Included

This package contains **8 comprehensive Postman collections** for testing RallyMate Services:

1. **auth_service.postman_collection.json** - Authentication (OTP/OTC, Sessions, Logout)
2. **users_service.postman_collection.json** - User Management & Memberships
3. **facilities_service.postman_collection.json** - Facility Management
4. **locks_service.postman_collection.json** - Smart Lock Operations
5. **cameras_service.postman_collection.json** - Camera Management & Control
6. **videos_service.postman_collection.json** - Video Management & Associations
7. **bridge_service.postman_collection.json** - Bridge Devices, Edge Connections & Tunnels
8. **system_support_service.postman_collection.json** - Admin Role Management

Plus **3 environment files**:
- `rallymate-local.postman_environment.json` - Local development (localhost:8080)
- `rallymate-development.postman_environment.json` - Dev server
- `rallymate-production.postman_environment.json` - Production API

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ Import into Postman

**Import Collections:**
1. Open Postman
2. Click **"Import"** (top left)
3. Drag all `*_service.postman_collection.json` files
4. Click **"Import"**

**Import Environment:**
1. Click **"Import"** again
2. Select `rallymate-local.postman_environment.json`
3. Click **"Import"**
4. **Select the environment** from the dropdown (top right corner)

### 2️⃣ Test Authentication Flow

**User Authentication (Mobile App):**
```
1. Open "RallyMate AuthService" collection
2. Run "Send OTP" request
   - Uses phone_number from environment
   - Check console for OTP code (or SMS in production)
3. Run "Verify OTP" request
   - Paste OTP code into request body
   - ✅ Session token automatically saved!
```

**Device Authentication (Bridge/IoT):**
```
1. Run "Send OTC" request
   - Uses device_id from environment
2. Get OTC from device logs/admin panel
3. Run "Verify OTC" request
   - ✅ Device session token saved + CA/MQTT endpoints extracted!
```

### 3️⃣ Start Testing!

All requests now automatically use the extracted `{{session_token}}` via Bearer authentication.

**Try these workflows:**
- Create Facility → Create User → Add Membership
- Register Bridge → Register Lock → Lock Control
- Register Camera → Start Recording → Upload Video

---

## ✨ Key Features

### 🎯 Realistic Test Data

Every request includes **meaningful example data**:

```json
{
  "phone_number": "+1234567890",
  "name": "Downtown Tennis Club",
  "device_id": "lock-court-01",
  "address": "123 Main St, City, State 12345",
  "timezone": "America/New_York"
}
```

No more empty placeholders or `"string"` values!

### 🔄 Automatic Variable Extraction

Test scripts automatically extract and save:
- ✅ `session_token` - Auth token for subsequent requests
- ✅ `user_id` - Created user IDs
- ✅ `facility_id` - Facility IDs
- ✅ `device_id` - Device identifiers
- ✅ `membership_id` - Membership IDs
- ✅ `video_id` - Uploaded video IDs
- ✅ `tunnel_id` - Created tunnel IDs

**Check the Console** after each request to see extracted values!

### 🧪 Comprehensive Tests

Each request includes:
- Status code validation (200 OK)
- Response time checks (< 2s)
- Response parsing and logging
- Smart variable extraction based on response type

### 🔗 Request Chaining

Variables flow automatically between requests:

```
Create Facility
  ↓ (extracts facility_id)
Create User  
  ↓ (extracts user_id)
Create Membership
  ↓ (uses facility_id + user_id)
✅ Done!
```

---

## 📚 Collection Details

### 1. Authentication Service (auth_service)

**OTP Flow (Users):**
- Send OTP - `POST /api/auth/otp/send`
- Verify OTP - `POST /api/auth/otp/verify` → Extracts session_token

**OTC Flow (Devices):**
- Send OTC - `POST /api/auth/otc/send`
- Verify OTC - `POST /api/auth/otc/verify` → Extracts session_token + endpoints

**Session Management:**
- Refresh Session - `POST /api/auth/session/refresh`
- Validate Session - `POST /api/auth/session/validate`
- Revoke Session - `POST /api/auth/session/revoke`
- Get User Sessions - `GET /api/auth/sessions/user/{user_id}`
- Get Device Sessions - `GET /api/auth/sessions/device/{device_id}`

**Logout:**
- Logout - `POST /api/auth/logout`
- Logout From All Devices - `POST /api/auth/logout/all`
- Admin Logout User - `POST /api/auth/admin/logout`

### 2. Users Service (users_service)

**Profile Management:**
- Get User Profile - `GET /api/users/profile`
- Get Users - `GET /api/users`
- Create User - `POST /api/users` → Extracts user_id
- Update User - `PUT /api/users/{id}`
- Delete User - `DELETE /api/users/{id}`

**User Discovery:**
- Discover Users - `GET /api/users/discover`

**Membership Management:**
- Create Membership By Phone - `POST /api/users/memberships/phone`
- Create Membership By User Id - `POST /api/users/memberships/user`
- Update Membership - `PUT /api/users/memberships/{membership_id}`
- Delete Membership - `DELETE /api/users/memberships/{membership_id}`
- Get User Memberships - `GET /api/users/{user_id}/memberships`
- Get Facility Memberships - `GET /api/facilities/{facility_id}/memberships`

### 3. Facilities Service (facilities_service)

- Get Facilities - `GET /api/facilities`
- Get Facility - `GET /api/facilities/{id}`
- Create Facility - `POST /api/facilities` → Extracts facility_id
- Update Facility - `PUT /api/facilities/{id}`
- Delete Facility - `DELETE /api/facilities/{id}`
- Get User Facilities - `GET /api/facilities/user/{user_id}`

### 4. Locks Service (locks_service)

**Lock Management:**
- Register Lock - `POST /api/locks/register` → Extracts lock_device_id
- Unregister Lock - `DELETE /api/locks/{device_id}/unregister`
- Update Lock - `PUT /api/locks/{device_id}`
- Get Locks - `GET /api/locks`

**Lock Control:**
- Lock Control - `POST /api/locks/{device_id}/control`
  - Actions: LOCK, UNLOCK, TOGGLE

**Audit Trail:**
- Get Lock Activities - `GET /api/locks/activities`

### 5. Cameras Service (cameras_service)

**Camera Management:**
- Register Camera - `POST /api/cameras/register` → Extracts camera_device_id
- Unregister Camera - `DELETE /api/cameras/{device_id}/unregister`
- Update Camera - `PUT /api/cameras/{device_id}`
- Get Cameras - `GET /api/cameras`

**Camera Control:**
- Camera Control - `POST /api/cameras/{device_id}/control`
  - Actions: START_RECORDING, STOP_RECORDING, SNAPSHOT

**Audit Trail:**
- Get Camera Activities - `GET /api/cameras/activities`

### 6. Videos Service (videos_service)

**Video Management:**
- Get Videos - `GET /api/videos`
- Get Video - `GET /api/videos/{id}`
- Get User Videos - `GET /api/videos/user/{user_id}`
- Upload Video - `POST /api/videos/upload` → Extracts video_id
- Update Video - `PUT /api/videos/{id}`
- Delete Video - `DELETE /api/videos/{id}`

**Video Associations:**
- Associate Video To User - `POST /api/videos/{video_id}/users/{user_id}`
- Remove Video User Association - `DELETE /api/videos/{video_id}/users/{user_id}`
- Get Video Associations - `GET /api/videos/{video_id}/associations`
- Bulk Associate Videos - `POST /api/videos/associate/bulk`
- Get User Video Associations - `GET /api/users/{user_id}/video-associations`

### 7. Bridge Service (bridge_service)

**Bridge Management:**
- Register Bridge - `POST /api/bridges/register` → Extracts bridge_device_id
- Unregister Bridge - `DELETE /api/bridges/{device_id}/unregister`
- Update Bridge - `PUT /api/bridges/{device_id}`
- Get Bridges - `GET /api/bridges`

**Edge Connections:**
- Register Edge Connection - `POST /api/bridges/{bridge_device_id}/connections`
- Delete Edge Connection - `DELETE /api/bridges/connections/{connection_id}`
- Update Edge Connection - `PUT /api/bridges/{bridge_device_id}/connections/{edge_device_id}`
- Get Edge Connections - `GET /api/bridges/{bridge_device_id}/connections`

**Tunnel Management:**
- Create Tunnel - `POST /api/tunnels` → Extracts tunnel_id
- Reserve Tunnel - `POST /api/tunnels/reserve`
- Establish Tunnel - `POST /api/tunnels/{tunnel_id}/establish`
- Close Tunnel - `POST /api/tunnels/{tunnel_id}/close`
- Get Tunnels - `GET /api/tunnels`
- Get Available Ports - `GET /api/tunnels/ports/available`
- Update Tunnel Stats - `PUT /api/tunnels/{tunnel_id}/stats`

**Audit Trail:**
- Get Bridge Activities - `GET /api/bridges/activities`

### 8. System Support Service (system_support_service)

- Get System Support - `GET /api/system-support/user/{user_id}`
- Create System Support - `POST /api/system-support` → Extracts support_id
- Update System Support - `PUT /api/system-support/{support_id}`
- Delete System Support - `DELETE /api/system-support/{support_id}`
- List Admins - `GET /api/system-support/admins`

---

## 🔧 Environment Variables

### Pre-configured Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `base_url` | `http://localhost:8080` | API base URL |
| `phone_number` | `+1234567890` | Test phone number |
| `facility_id` | `1` | Default facility ID |
| `device_id` | `bridge-001` | Default device ID |

### Auto-extracted Variables

These are automatically set by test scripts:

| Variable | Extracted From | Used In |
|----------|---------------|---------|
| `session_token` | Verify OTP/OTC | All authenticated requests |
| `refresh_token` | Verify OTP/OTC | Refresh Session |
| `user_id` | User creation/profile | User-related requests |
| `facility_id` | Facility creation | Device registration, memberships |
| `membership_id` | Membership creation | Membership updates |
| `lock_device_id` | Lock registration | Lock control |
| `camera_device_id` | Camera registration | Camera control |
| `bridge_device_id` | Bridge registration | Edge connections |
| `video_id` | Video upload | Video associations |
| `tunnel_id` | Tunnel creation | Tunnel operations |
| `connection_id` | Edge connection | Connection updates |

---

## 🎬 Example Workflows

### Workflow 1: User Onboarding

```
1. Send OTP
2. Verify OTP (extracts session_token, user_id)
3. Get User Profile
4. Create Facility (extracts facility_id)
5. Create Membership By Phone (uses facility_id)
6. Get Facility Memberships (verify)
```

### Workflow 2: Device Setup

```
1. Send OTC (for bridge device)
2. Verify OTC (extracts device session_token)
3. Register Bridge (extracts bridge_device_id)
4. Register Lock
5. Register Camera
6. Register Edge Connections (link devices to bridge)
7. Get Bridges (verify all connections)
```

### Workflow 3: Access Control

```
1. Authenticate User (OTP flow)
2. Get User Facilities
3. Get Locks (for facility)
4. Lock Control - Unlock (action: LOCK_ACTION_UNLOCK)
5. Get Lock Activities (verify action logged)
6. Lock Control - Lock (action: LOCK_ACTION_LOCK)
```

### Workflow 4: Video Management

```
1. Authenticate User
2. Register Camera
3. Camera Control - Start Recording
4. Upload Video (extracts video_id)
5. Associate Video To User
6. Get User Videos (verify association)
```

### Workflow 5: Tunnel Creation

```
1. Authenticate Device (OTC flow)
2. Register Bridge
3. Register Camera (edge device)
4. Register Edge Connection (camera → bridge)
5. Get Available Ports
6. Create Tunnel (extracts tunnel_id, cloud_port)
7. Establish Tunnel
8. [Use tunnel for streaming]
9. Close Tunnel
10. Update Tunnel Stats
```

---

## 🐛 Troubleshooting

### Issue: "401 Unauthorized"

**Cause:** No session token or expired session

**Solution:**
1. Run auth flow: Send OTP → Verify OTP
2. Check collection variables: ensure `session_token` is set
3. Check token expiration in response

### Issue: "Variables not extracted"

**Cause:** Test script couldn't parse response

**Solution:**
1. Check Console tab for errors
2. Verify response structure matches expected format
3. Manually set variables in Environment tab if needed

### Issue: "Device not found"

**Cause:** Device not registered

**Solution:**
1. Register device first (Register Bridge/Lock/Camera)
2. Verify device_id matches in request
3. Check facility_id is correct

### Issue: "Phone number format invalid"

**Cause:** Phone number doesn't match E.164 format

**Solution:**
- Use format: `+[country code][number]`
- Examples: `+1234567890`, `+442071234567`
- Update `phone_number` in environment

---

## 💡 Tips & Best Practices

### 1. Start with Authentication
Always begin testing with the auth flow to get a valid session token.

### 2. Check the Console
After each request, open the **Console** (bottom left) to see:
- Full request/response details
- Extracted variables with emoji indicators
- Any parsing errors

### 3. Use Collection Runner
For workflows, use **Collection Runner**:
1. Select collection
2. Choose requests to run
3. Click "Run"
4. Watch variables flow through requests

### 4. Organize Your Tests
Create **folders** in collections to organize by:
- Feature (Authentication, User Management, etc.)
- Workflow (Onboarding, Device Setup, etc.)
- Test scenario (Happy path, Error cases, etc.)

### 5. Customize Test Data
Edit request bodies to match your testing needs:
- Real phone numbers for SMS testing
- Actual device IDs from your hardware
- Valid facility IDs from your database

### 6. Monitor Variables
Keep the **Variables** tab open while testing:
- Collection variables (auto-extracted)
- Environment variables (configured)
- Watch values update in real-time

### 7. Save Responses
Use **Save Response** to create examples:
- Success scenarios
- Error scenarios
- Edge cases

---

## 📖 Additional Resources

- **Proto Definitions:** `rallymate-api/protos/`
- **Service Implementation:** `rallymate-services/`
- **Postman Documentation:** https://learning.postman.com/
- **gRPC-Gateway:** HTTP endpoints mirror gRPC methods

---

## 🔄 Regenerating Collections

To regenerate collections after proto file changes:

```bash
cd rallymate-postman-collection/v2
./generate-all.sh
```

This will:
1. Parse all proto files
2. Generate new collections with updated endpoints
3. Create fresh environment files
4. Preserve your custom test data (backup first!)

---

## 📋 Checklist

- [ ] Import all 8 service collections
- [ ] Import local environment
- [ ] Select environment from dropdown
- [ ] Run "Send OTP" request
- [ ] Verify session_token is extracted
- [ ] Test "Get User Profile" with token
- [ ] Create a facility
- [ ] Register a device
- [ ] Explore other endpoints
- [ ] Build custom workflows

---

## 🎯 What's Next?

1. **Customize for your environment** - Update URLs, phone numbers, device IDs
2. **Add more test scenarios** - Error cases, edge conditions, load testing
3. **Build automation** - Use Newman CLI for CI/CD integration
4. **Share with team** - Export and share collections
5. **Monitor in production** - Use Postman monitors for API health checks

---

**Generated:** October 15, 2025  
**Version:** 2.0.0  
**Generator:** generate_postman_collections.py  

**Happy Testing! 🚀**
