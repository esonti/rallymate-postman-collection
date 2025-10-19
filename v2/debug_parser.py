#!/usr/bin/env python3
"""Debug script to test proto parsing."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from generate_postman_collections import ProtoParser

# Test with auth.proto
proto_file = Path(__file__).parent.parent.parent / "rallymate-api" / "protos" / "auth.proto"

print(f"Testing: {proto_file}")
print(f"Exists: {proto_file.exists()}")
print()

if proto_file.exists():
    parser = ProtoParser(proto_file)
    
    print(f"Package: {parser.package_name}")
    print(f"Messages found: {len(parser.messages)}")
    print(f"Enums found: {len(parser.enums)}")
    print()
    
    service_data = parser.parse_service()
    
    if service_data:
        print(f"✅ Service: {service_data['name']}")
        print(f"✅ Package: {service_data['package']}")
        print(f"✅ RPCs: {len(service_data['rpcs'])}")
        print()
        
        if service_data['rpcs']:
            print("RPCs found:")
            for rpc in service_data['rpcs'][:3]:  # Show first 3
                print(f"  - {rpc['name']}: {rpc['http']['method']} {rpc['http']['path']}")
        else:
            print("⚠️  No RPCs with HTTP annotations found")
            print()
            print("Checking service body...")
            # Try to find service manually
            content = proto_file.read_text()
            if 'service' in content:
                print("✅ 'service' keyword found in file")
                import re
                service_match = re.search(r'service\s+(\w+)', content)
                if service_match:
                    print(f"✅ Service name: {service_match.group(1)}")
                    
                # Check for RPC
                rpc_matches = re.findall(r'rpc\s+(\w+)', content)
                print(f"✅ Found {len(rpc_matches)} RPC declarations: {rpc_matches[:5]}")
                
                # Check for HTTP annotations
                http_matches = re.findall(r'google\.api\.http', content)
                print(f"✅ Found {len(http_matches)} HTTP annotations")
    else:
        print("❌ No service data parsed")
        print()
        print("Checking file content...")
        content = proto_file.read_text()
        print(f"File size: {len(content)} bytes")
        
        import re
        if 'service' in content:
            print("✅ Contains 'service' keyword")
            service_match = re.search(r'service\s+(\w+)', content)
            if service_match:
                print(f"✅ Service name: {service_match.group(1)}")
        else:
            print("❌ No 'service' keyword found")
else:
    print("❌ File not found!")
