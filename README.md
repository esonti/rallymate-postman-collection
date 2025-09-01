# RallyMate API Testing Collections

This repository contains Postman collections for testing the RallyMate API services, including both HTTP REST and gRPC interfaces.

## 📁 Collections Structure

```
collections/
├── rest/                          # HTTP REST API collections
│   ├── RallyMate-Auth-REST.json          # Authentication endpoints
│   ├── RallyMate-Users-REST.json         # User management endpoints
│   ├── RallyMate-Facilities-REST.json    # Facility management endpoints
│   ├── RallyMate-Locks-REST.json         # Smart lock endpoints
│   ├── RallyMate-Cameras-REST.json       # Camera endpoints
│   ├── RallyMate-Videos-REST.json        # Video management endpoints
│   └── RallyMate-Bridge-REST.json        # Bridge device endpoints
├── grpc/                          # gRPC API collections
│   ├── RallyMate-Auth-gRPC.json          # Authentication gRPC services
│   ├── RallyMate-Users-gRPC.json         # User management gRPC services
│   ├── RallyMate-Facilities-gRPC.json    # Facility management gRPC services
│   ├── RallyMate-Locks-gRPC.json         # Smart lock gRPC services
│   ├── RallyMate-Cameras-gRPC.json       # Camera gRPC services
│   ├── RallyMate-Videos-gRPC.json        # Video management gRPC services
│   └── RallyMate-Bridge-gRPC.json        # Bridge device gRPC services
└── environments/                  # Environment configurations
    ├── local.json                 # Local development environment
    ├── dev.json                   # Development environment
    └── prod.json                  # Production environment
```

## 🚀 Quick Start

### Prerequisites
- [Postman](https://www.postman.com/downloads/) desktop app or web version
- Running RallyMate services (local or cloud deployment)

### Import Collections

1. **Import REST Collections:**
   - Open Postman
   - Click "Import" button
   - Select all files from `collections/rest/` directory
   - Import the environment file from `environments/`

2. **Import gRPC Collections:**
   - For gRPC testing, you'll need Postman with gRPC support
   - Import files from `collections/grpc/` directory
   - Configure the gRPC server URL in the environment

### Environment Setup

Update the environment variables to match your deployment:

- **Local Development:** Use `local.json`
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
