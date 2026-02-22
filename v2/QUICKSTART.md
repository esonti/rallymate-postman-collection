# 🚀 Quick Start - rallymate Postman Collections

## 3-Step Setup

### 1️⃣ Generate Collections
```bash
cd rallymate-postman-collection/v2
chmod +x generate-all.sh
./generate-all.sh
```

### 2️⃣ Import to Postman
1. Open Postman
2. Click **Import** (top left)
3. Drag all `.json` files from `generated/` folder
4. Click **Import**
5. Select **"rallymate - Local"** environment (top right)

### 3️⃣ Test Authentication
1. Open **"rallymate AuthService"** collection
2. Run **"Send OTP"** request
3. Check console for OTP code
4. Run **"Verify OTP"** request
5. ✅ Session token automatically saved!

---

## 📦 What You Get

✅ **8 Service Collections** (72+ endpoints)
- Auth (OTP/OTC, Sessions, Logout)
- Users (CRUD, Memberships, Discovery)
- Facilities (CRUD, Associations)
- Locks (Registration, Control, Activities)
- Cameras (Registration, Control, Activities)
- Videos (CRUD, Associations, Bulk)
- Bridge (Devices, Edges, Tunnels, Ports)
- System Support (Admin Roles)

✅ **3 Environments**
- Local (localhost:8080)
- Development
- Production

✅ **Realistic Test Data**
- Phone numbers: `+1234567890`
- Device IDs: `bridge-001`, `lock-court-01`
- Addresses: `123 Main St, City, State 12345`
- Timestamps: RFC3339 format
- Enums: Actual proto values

✅ **Smart Test Scripts**
- Auto-extract session tokens
- Save user/facility/device IDs
- Validate responses
- Console logging with emojis

---

## 🎯 Quick Test Workflows

### User Authentication
```
1. Send OTP
2. Verify OTP (saves session_token)
3. Get User Profile
```

### Device Setup
```
1. Send OTC (device)
2. Verify OTC (saves device session)
3. Register Bridge
4. Register Lock/Camera
```

### Access Control
```
1. Auth with OTP
2. Get Locks
3. Lock Control (unlock)
4. Get Activities
```

---

## 🔧 Key Variables

Auto-extracted by test scripts:
- `session_token` - Auth token
- `user_id` - User ID
- `facility_id` - Facility ID
- `device_id` - Device ID
- `membership_id` - Membership ID

Pre-configured in environment:
- `base_url` - http://localhost:8080
- `phone_number` - +1234567890

---

## 💡 Pro Tips

1. **Check Console** - See extracted variables after each request
2. **Use Collection Runner** - Run multiple requests in sequence
3. **Customize Data** - Edit request bodies for your testing
4. **Save Responses** - Create examples for success/error cases
5. **Watch Variables** - Keep Variables tab open while testing

---

## 🐛 Troubleshooting

**401 Unauthorized?**
→ Run auth flow (Send OTP → Verify OTP)

**Variables not extracted?**
→ Check Console tab for errors

**Device not found?**
→ Register device first

---

## 📚 Full Documentation

See `generated/README.md` for:
- Complete endpoint list
- Detailed workflows
- Advanced features
- Best practices
- Troubleshooting guide

---

**Ready?** Run `./generate-all.sh` and start testing! 🚀
