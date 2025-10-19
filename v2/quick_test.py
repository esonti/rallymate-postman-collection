#!/usr/bin/env python3
"""Quick test of the fixed parser."""

from pathlib import Path
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from generate_postman_collections import ProtoParser

def test_auth_proto():
    """Test parsing auth.proto."""
    proto_file = Path(__file__).parent.parent.parent / "rallymate-api" / "protos" / "auth.proto"
    
    if not proto_file.exists():
        print(f"❌ Proto file not found: {proto_file}")
        return False
    
    print(f"📄 Testing: {proto_file.name}")
    
    try:
        parser = ProtoParser(proto_file)
        service_data = parser.parse_service()
        
        if not service_data:
            print("❌ Failed to parse service")
            return False
        
        print(f"✅ Service: {service_data['name']}")
        print(f"✅ RPCs found: {len(service_data['rpcs'])}")
        
        if service_data['rpcs']:
            print("\nFirst 3 RPCs:")
            for rpc in service_data['rpcs'][:3]:
                print(f"  • {rpc['name']}: {rpc['http']['method']} {rpc['http']['path']}")
            return True
        else:
            print("❌ No RPCs with HTTP annotations")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_auth_proto()
    sys.exit(0 if success else 1)
