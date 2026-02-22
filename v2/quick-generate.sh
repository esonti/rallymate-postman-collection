#!/bin/bash
# Quick start script for generating Postman collections

set -e

echo "🚀 rallymate Postman Collection Generator"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

# Define paths
PROTO_DIR="../../rallymate-api/protos"
OUTPUT_DIR="generated"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📁 Proto directory: $PROTO_DIR"
echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# List of services to generate
SERVICES=("auth" "users" "facilities" "bridge" "locks" "cameras" "videos" "system_support")

echo "🔧 Generating collections for services:"
for service in "${SERVICES[@]}"; do
    echo "  - $service"
done
echo ""

# Generate collection for each service
for service in "${SERVICES[@]}"; do
    echo "⚙️  Processing $service..."
    
    proto_file="$PROTO_DIR/${service}.proto"
    
    if [ ! -f "$proto_file" ]; then
        echo "  ⚠️  Proto file not found: $proto_file (skipping)"
        continue
    fi
    
    output_file="$OUTPUT_DIR/rallymate_${service^}_Service.postman_collection.json"
    
    python3 generate_collection.py \
        --proto-dir "$PROTO_DIR" \
        --service "$service" \
        --output "$output_file" \
        --base-url "{{base_url}}"
    
    echo "  ✅ Generated: $output_file"
    echo ""
done

echo ""
echo "✨ Collection generation complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Review generated collections in: $OUTPUT_DIR/"
echo "  2. Import collections into Postman"
echo "  3. Create environment variables (base_url, session_token, etc.)"
echo "  4. Customize test data in request bodies"
echo "  5. Enhance test scripts for your specific needs"
echo ""
echo "💡 Tip: The generated collections are starting points."
echo "   You'll want to:"
echo "   - Add realistic test data"
echo "   - Enhance test scripts with variable extraction"
echo "   - Add request descriptions"
echo "   - Organize into folders by feature"
echo ""
