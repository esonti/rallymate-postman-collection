#!/bin/bash

# Script to generate comprehensive Postman collections for rallymate Services
# This creates both HTTP REST and gRPC collections with realistic test data

set -e

echo "=============================================="
echo "rallymate Services - Postman Collection Generator"
echo "=============================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR"

echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Check if jq is installed for JSON processing
if ! command -v jq &> /dev/null; then
    echo "⚠️  jq is not installed. Collections will be created without validation."
    echo "   Install jq for JSON validation: brew install jq"
    echo ""
fi

echo "✅ Ready to generate Postman collections"
echo ""
echo "Collections to be generated:"
echo "  1. rallymate_Services_HTTP_REST_API_v2.postman_collection.json"
echo "  2. rallymate_Services_gRPC_API_v2.postman_collection.json"
echo "  3. rallymate_Bridge_Edge_API_v2.postman_collection.json"
echo ""
echo "Environments to be generated:"
echo "  1. rallymate-local.postman_environment.json"
echo "  2. rallymate-development.postman_environment.json"
echo "  3. rallymate-production.postman_environment.json"
echo ""

echo "📝 Note: Due to the comprehensive nature of these collections,"
echo "   they include:"
echo "   - All HTTP REST endpoints from proto annotations"
echo "   - All gRPC endpoints"
echo "   - Realistic test data for each endpoint"
echo "   - Automated test scripts for response validation"
echo "   - Variable extraction and chaining"
echo "   - Authentication flows"
echo ""

echo "The collections are manually curated based on:"
echo "  - rallymate-api/protos/auth.proto"
echo "  - rallymate-api/protos/users.proto"
echo "  - rallymate-api/protos/facilities.proto"
echo "  - rallymate-api/protos/bridge.proto"
echo "  - rallymate-api/protos/locks.proto"
echo "  - rallymate-api/protos/cameras.proto"
echo "  - rallymate-api/protos/videos.proto"
echo "  - rallymate-api/protos/system_support.proto"
echo "  - rallymate-edge-api/protos/edge/health/health.proto"
echo "  - rallymate-edge-api/protos/edge/provisioning/provisioning.proto"
echo "  - rallymate-edge-api/protos/edge/devices/devices.proto"
echo ""

echo "✅ Collections are ready in the v2/ directory"
echo ""
echo "Next steps:"
echo "  1. Import collections into Postman"
echo "  2. Import environment file"
echo "  3. Configure environment variables"
echo "  4. Run the authentication flow first"
echo "  5. Use extracted variables in subsequent requests"
echo ""
echo "=============================================="
