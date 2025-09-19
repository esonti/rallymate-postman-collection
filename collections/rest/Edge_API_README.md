# RallyMate Edge API Postman Collection

This collection provides comprehensive testing capabilities for the RallyMate Bridge Edge API, covering all device discovery, management, health monitoring, and provisioning operations.

## 📁 Collection Structure

### 🏥 Health Monitoring
- **Get Basic Health** - Basic health status check
- **Get System Information** - Detailed system info (hardware, OS, resources)
- **Get Connectivity Status** - MQTT, network, and service connectivity
- **Get Performance Metrics** - Performance metrics and operational stats

### 🔍 Discovery Service  
- **Get Bridge Information** - Bridge identification and status
- **Get Service Information** - Service capabilities and details
- **Get Network Information** - Network configuration and connectivity

### 📱 Device Management
- **List All Devices** - Get all discovered devices
- **Get Specific Device** - Detailed device information
- **Discover New Devices** - Perform mDNS device discovery
- **Connect to Device** - Establish device connection
- **Disconnect from Device** - Disconnect from device
- **Send Device Command** - Send commands (lock/unlock, etc.)
- **Get Device Status** - Current device status and state

### 🔧 Provisioning
- **Get Provisioning Status** - Current provisioning state
- **Provision with One-Time Code** - Provision bridge with OTC
- **Validate Session Token** - Check token validity
- **Refresh Session Token** - Refresh authentication
- **Reset Provisioning** - Reset to unprovisioned state

### 🧪 Testing Workflows
- **Complete Health Check** - Automated health validation
- **Device Discovery Workflow** - End-to-end discovery testing

## 🌍 Environments

### edge-api-local.json
For local development and testing:
- Bridge Host: `bridge.local`
- Port: `8090`
- Use when testing with a local bridge instance

### edge-api-pi-zero.json  
For Pi Zero bridge testing:
- Bridge Host: `192.168.1.100` (update with actual IP)
- Port: `8090`
- Use when testing with deployed Pi Zero bridge

## 🚀 Quick Start

1. **Import the Collection**
   ```
   Import: RallyMate_Edge_API.postman_collection.json
   ```

2. **Import Environment**
   ```
   Import: edge-api-local.json (or edge-api-pi-zero.json)
   ```

3. **Update Environment Variables**
   - `bridge_host`: Set to your bridge's hostname or IP
   - `bridge_port`: Set to your bridge's API port (default: 8090)

4. **Run Basic Health Check**
   ```
   GET {{base_url}}/api/health
   ```

## 🔧 Configuration

### Required Variables
- `bridge_host` - Bridge hostname or IP address
- `bridge_port` - Bridge API port (default: 8090)
- `base_url` - Complete base URL (auto-generated)

### Optional Variables (Auto-populated)
- `device_id` - Device ID for testing
- `first_device_id` - First discovered device
- `session_token` - Authentication token
- `refresh_token` - Token refresh credential

### Provisioning Variables
- `facility_id` - Facility identifier
- `bridge_name` - Human-readable bridge name
- `otc_code` - One-Time Code from RallyMate platform

## 📋 Common Workflows

### 1. Basic Health Check
```
Health Monitoring → Get Basic Health
```

### 2. Complete System Status
```
1. Get Basic Health
2. Get System Information  
3. Get Connectivity Status
4. Get Performance Metrics
```

### 3. Device Discovery & Control
```
1. Discover New Devices
2. List All Devices
3. Get Specific Device
4. Connect to Device
5. Send Device Command
6. Get Device Status
```

### 4. Bridge Provisioning
```
1. Get Provisioning Status
2. Provision with One-Time Code
3. Validate Session Token
```

## 🧪 Automated Testing

The collection includes automated test scripts that:

- ✅ Validate response status codes
- ✅ Check response times (< 5 seconds)
- ✅ Verify JSON content types
- ✅ Extract and store device IDs
- ✅ Set up variables for chained requests

### Test Execution
1. Select the environment
2. Run individual requests or entire folders
3. Use Runner for automated test execution
4. Monitor test results in the console

## 🐛 Troubleshooting

### Common Issues

**Connection Refused**
- Verify bridge is running: `systemctl status rallymate-bridge`
- Check bridge host/IP: `ping bridge.local`
- Verify port accessibility: `telnet bridge.local 8090`

**404 Not Found**
- Ensure bridge API is enabled in configuration
- Check bridge version supports Edge API
- Verify URL paths match the collection

**Discovery Returns No Devices**  
- Ensure devices are on same network
- Check mDNS functionality: `avahi-browse -a`
- Verify device advertisement is working

**Provisioning Fails**
- Verify OTC is valid and not expired
- Check network connectivity to RallyMate platform
- Ensure facility_id is correct

## 📝 API Documentation

### Response Formats
All endpoints return JSON responses with standard structures:

```json
{
  "status": "success|error",
  "data": { ... },
  "message": "Human readable message",
  "timestamp": "2025-09-19T12:00:00Z"
}
```

### Error Handling
Standard HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

### Rate Limiting
- Discovery operations: 1 request per 30 seconds
- Device commands: 10 requests per minute
- Health checks: No limit

## 🔄 Updates

To update the collection:
1. Pull latest changes from repository
2. Re-import collection (overwrite existing)
3. Update environment variables as needed
4. Test critical workflows

## 📞 Support

For issues with:
- **Collection**: Check repository issues
- **Bridge API**: Review bridge logs (`journalctl -u rallymate-bridge`)
- **Device Discovery**: Verify network and mDNS configuration
- **Provisioning**: Contact RallyMate platform support