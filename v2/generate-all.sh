#!/bin/bash
# Generate all RallyMate Postman collections with realistic test data

set -e

echo "🚀 RallyMate Postman Collection Generator v2"
echo "=============================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

echo "📦 Running comprehensive collection generator..."
echo ""

# Run the generator
python3 generate_postman_collections.py

echo ""
echo "✨ All done!"
echo ""
echo "📋 Next steps:"
echo "  1. Open Postman"
echo "  2. Click 'Import' in the top left"
echo "  3. Select all .json files from the 'generated/' folder"
echo "  4. Click 'Import'"
echo "  5. Select the 'RallyMate - Local' environment"
echo "  6. Start testing!"
echo ""
echo "💡 Tips:"
echo "  - Start with Auth service (Send OTP → Verify OTP)"
echo "  - Session tokens are automatically extracted"
echo "  - All requests include realistic test data"
echo "  - Check the 'Tests' tab to see variable extraction"
echo "  - Review console output for extracted values"
echo ""
