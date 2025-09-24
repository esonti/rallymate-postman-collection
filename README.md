# RallyMate API Testing Collections

Comprehensive Postman collections for testing all RallyMate platform services, including REST APIs, gRPC services, and integration scenarios.

## Overview

This collection provides complete API testing capabilities for:
- **Core Platform APIs**: Main RallyMate services (HTTP/gRPC)
- **Certificate Authority**: CA service testing and validation
- **Bridge Services**: Device bridge API testing
- **Integration Scenarios**: End-to-end workflow testing
- **Development Workflows**: Local development and testing

## Collection Structure

### Environment Files
- **`local-updated-v2.json`** - Complete local development environment
- **`edge-api-local.json`** - Local bridge testing environment
- **`edge-api-pi-zero.json`** - Pi Zero bridge testing environment
- **`ca-testing.json`** - Certificate Authority testing environment

### API Collections

#### Core Platform APIs
- **`RallyMate_HTTP_REST_API_v2.postman_collection.json`**
  - Complete REST API testing for main services
  - User authentication and management
  - Facility management operations
  - Device control and monitoring
  - Video and media management

- **`RallyMate_gRPC_API_v2.postman_collection.json`**
  - gRPC service testing with Postman
  - High-performance API testing
  - Protocol buffer message validation
  - Service discovery and health checks

#### Service-Specific Collections
- **`CA_Testing.postman_collection.json`** 🆕
  - Certificate Authority API testing
  - Certificate issuance workflows
  - Session token validation
  - Certificate lifecycle management

- **`Bridge_Testing.postman_collection.json`** 🆕
  - Bridge service API testing
  - Device provisioning workflows
  - Tunnel management operations
  - Health monitoring endpoints

- **`RallyMate_Edge_API.postman_collection.json`**
  - Edge device API testing
  - Local network device control
  - mDNS discovery testing
  - IoT device integration

## Quick Setup

### Core API Testing (RallyMate Platform)

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

### Edge API Testing (Bridge Devices)

1. **Import Edge API Collection**
   - Import `collections/rest/RallyMate_Edge_API.postman_collection.json`

2. **Import Environment**
   - For local bridge: Import `environments/edge-api-local.json`
   - For Pi Zero bridge: Import `environments/edge-api-pi-zero.json`

3. **Configure Bridge Connection**
   - Update `bridge_host` with your bridge's IP or hostname
   - Ensure bridge is running and accessible

4. **Test Basic Connectivity**
   ```
## Quick Setup

### Prerequisites
- Postman installed and running
- RallyMate services running locally (via `docker-compose up`)
- Network access to target environment

### Core Platform Testing

1. **Import Environment**:
   ```
   File → Import → environments/local-updated-v2.json
   ```

2. **Import Core Collections**:
   ```
   File → Import → RallyMate_HTTP_REST_API_v2.postman_collection.json
   File → Import → RallyMate_gRPC_API_v2.postman_collection.json
   ```

3. **Set Active Environment**:
   - Click environment dropdown
   - Select "RallyMate Local v2"

4. **Verify Services**:
   ```
   GET {{base_url}}/health
   GET {{bridge_url}}/api/health
   GET {{ca_url}}/health
   ```

### Certificate Authority Testing

1. **Import CA Environment & Collection**:
   ```
   File → Import → ca-testing.json
   File → Import → CA_Testing.postman_collection.json
   ```

2. **Test Certificate Workflows**:
   - Session validation
   - Certificate issuance
   - Certificate verification

### Bridge Service Testing

1. **Import Bridge Collection**:
   ```
   File → Import → Bridge_Testing.postman_collection.json
   ```

2. **Configure Environment Variables**:
   ```json
   {
     "bridge_url": "http://localhost:8090",
     "ca_url": "http://localhost:8082",
     "tunnel_url": "http://localhost:5022"
   }
   ```

## Environment Configuration

### Local Development Environment (local-updated-v2.json)

```json
{
  "base_url": "http://localhost:8080",
  "bridge_url": "http://localhost:8090", 
  "ca_url": "http://localhost:8082",
  "tunnel_url": "http://localhost:5022",
  "eventstream_url": "ws://localhost:8000",
  "database_url": "postgresql://rallymate:password@localhost:5432/rallymate"
}
```

### Bridge Testing Environments

**Local Bridge (edge-api-local.json)**:
```json
{
  "bridge_host": "localhost",
  "bridge_port": "8090",
  "bridge_url": "http://localhost:8090"
}
```

**Pi Zero Bridge (edge-api-pi-zero.json)**:
```json
{
  "bridge_host": "192.168.1.100",
  "bridge_port": "8090", 
  "bridge_url": "http://192.168.1.100:8090"
}
```

## Authentication Workflows

### Session-Based Authentication

1. **Login Request**:
   ```
   POST {{base_url}}/api/auth/login
   {
     "email": "user@example.com",
     "password": "password"
   }
   ```

2. **Cookie Persistence**:
   - Sessions automatically saved in cookies
   - No manual token management needed
   - Automatic renewal on subsequent requests

### Token-Based Authentication (Alternative)

1. **Login and Extract Token**:
   ```javascript
   // Post-request script
   const response = pm.response.json();
   pm.environment.set("auth_token", response.token);
   ```

2. **Use Token in Headers**:
   ```
   Authorization: Bearer {{auth_token}}
   ```

## Testing Workflows

### Core Service Testing

1. **Health Checks**:
   - Main services: `GET /health`
   - Bridge service: `GET /api/health`
   - CA service: `GET /health`

2. **User Management**:
   - Registration workflow
   - Login/logout flow
   - Profile management
   - Password reset

3. **Facility Management**:
   - Create/update facilities
   - Membership operations
   - Device registration
   - Access control

### Certificate Authority Testing

1. **Session Validation**:
   ```
   POST {{ca_url}}/api/validate-session
   {
     "session_token": "{{session_token}}"
   }
   ```

2. **Certificate Issuance**:
   ```
   POST {{ca_url}}/api/certificates/client
   {
     "session_token": "{{bridge_token}}",
     "client_id": "bridge-001",
     "validity_duration": "8h"
   }
   ```

3. **Certificate Verification**:
   ```
   GET {{ca_url}}/api/certificates/{{cert_id}}/status
   ```

### Bridge Service Testing

1. **Device Registration**:
   ```
   POST {{bridge_url}}/api/v1/devices/register
   {
     "device_id": "device-001",
     "device_type": "sensor"
   }
   ```

2. **Certificate Provisioning**:
   ```
   POST {{bridge_url}}/api/v1/devices/{{device_id}}/certificate
   ```

3. **Tunnel Management**:
   ```
   POST {{bridge_url}}/api/v1/tunnels
   {
     "device_id": "device-001",
     "tunnel_type": "ssh"
   }
   ```

### Integration Testing

1. **End-to-End Device Provisioning**:
   - Device registration
   - Authentication
   - Certificate provisioning  
   - Tunnel creation

2. **Cross-Service Communication**:
   - Bridge ↔ CA communication
   - Bridge ↔ Tunnel service
   - Services ↔ Database

## Advanced Testing Scenarios

### Load Testing

Use Postman's Collection Runner or Newman:

```bash
# Install Newman
npm install -g newman

# Run collection with multiple iterations
newman run RallyMate_HTTP_REST_API_v2.postman_collection.json \
  -e local-updated-v2.json \
  -n 100 \
  --delay-request 100

# Generate HTML report
newman run RallyMate_HTTP_REST_API_v2.postman_collection.json \
  -e local-updated-v2.json \
  -r htmlextra
```

### Automated Testing

Create test scripts in collection requests:

```javascript
// Test response status
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test response time
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Test response data
pm.test("Response contains expected data", function () {
    const response = pm.response.json();
    pm.expect(response).to.have.property('status', 'success');
});

// Set environment variables
pm.test("Extract and set session token", function () {
    const response = pm.response.json();
    pm.environment.set("session_token", response.session_token);
});
```

## Troubleshooting

### Common Issues

1. **Connection Refused**:
   ```
   Error: connect ECONNREFUSED 127.0.0.1:8080
   ```
   - Verify services are running: `docker-compose ps`
   - Check port mapping in docker-compose.yml
   - Confirm firewall settings

2. **Authentication Failures**:
   ```
   401 Unauthorized
   ```
   - Check session token validity
   - Verify user credentials
   - Confirm auth service is running

3. **SSL/TLS Errors**:
   ```
   SSL Error: unable to verify certificate
   ```
   - In Postman: Settings → Turn off "SSL certificate verification"
   - For production: Use proper certificates

4. **gRPC Testing Issues**:
   - Enable "gRPC" mode in Postman request settings
   - Import .proto files if available
   - Check service reflection is enabled

### Debug Strategies

1. **Check Service Logs**:
   ```bash
   docker-compose logs -f rallymate-services
   docker-compose logs -f rallymate-bridge
   docker-compose logs -f rallymate-ca
   ```

2. **Validate Environment Variables**:
   - Click "Environment Quick Look" (eye icon)
   - Verify all required variables are set
   - Check variable scope (global vs environment)

3. **Network Connectivity**:
   ```bash
   # Test connectivity
   curl http://localhost:8080/health
   curl http://localhost:8090/api/health
   curl http://localhost:8082/health
   ```

4. **Database Connectivity**:
   ```bash
   # Connect to database
   docker-compose exec rallymate-database psql -U rallymate -d rallymate
   ```

## Best Practices

### Collection Organization
- **Group Related Requests**: Use folders for logical grouping
- **Consistent Naming**: Use clear, descriptive request names
- **Environment Variables**: Use variables for all configurable values
- **Pre-request Scripts**: Setup common authentication/configuration
- **Test Scripts**: Add automated validation for all requests

### Environment Management
- **Separate Environments**: Different environments for dev/staging/prod
- **Sensitive Data**: Use Postman Vault for secrets
- **Version Control**: Export and version control collections
- **Documentation**: Include comprehensive request descriptions

### Testing Strategy
- **Sequential Testing**: Use Collection Runner for workflow testing
- **Parallel Testing**: Use Newman for load testing
- **Automated Validation**: Include assertions in all test requests
- **Error Handling**: Test both success and failure scenarios

## CI/CD Integration

### Newman Integration

Create automated tests in your CI/CD pipeline:

```yaml
# GitHub Actions example
name: API Tests
on: [push, pull_request]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Start services
      run: docker-compose up -d
    - name: Wait for services
      run: sleep 30
    - name: Run Postman tests
      run: |
        npx newman run rallymate-postman-collection/RallyMate_HTTP_REST_API_v2.postman_collection.json \
        -e rallymate-postman-collection/local-updated-v2.json \
        --reporters cli,junit
    - name: Cleanup
      run: docker-compose down
```

## Contributing

### Adding New Collections

1. **Create Collection**:
   - Organize requests logically
   - Use consistent naming
   - Add comprehensive documentation

2. **Update Environment**:
   - Add new variables as needed
   - Document variable purposes
   - Test across environments

3. **Test Validation**:
   - Add test scripts to all requests
   - Validate response structure
   - Check error conditions

4. **Documentation**:
   - Update README with new collection info
   - Include example requests
   - Document any special requirements

### Maintenance Guidelines

- **Regular Updates**: Keep collections current with API changes
- **Version Control**: Use semantic versioning for collections
- **Testing**: Validate collections before committing changes
- **Documentation**: Keep documentation comprehensive and current

## Support

For issues with the Postman collections:

1. **Check Service Health**: Verify all services are running and healthy
2. **Validate Environment**: Ensure all environment variables are set correctly
3. **Review Logs**: Check service logs for error details
4. **Test Connectivity**: Verify network connectivity to services
5. **Consult Documentation**: Review API documentation for endpoint details

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
