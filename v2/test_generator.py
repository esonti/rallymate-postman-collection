#!/usr/bin/env python3
"""
Test script to validate the Postman collection generator.
Performs basic checks without generating full collections.
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all required modules are available."""
    print("🧪 Testing imports...")
    try:
        import json
        import re
        from datetime import datetime, timedelta
        print("   ✅ All standard library imports successful")
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_proto_files():
    """Test that proto files exist and are readable."""
    print("\n🧪 Testing proto files...")
    script_dir = Path(__file__).parent
    proto_dir = script_dir.parent.parent / "rallymate-api" / "protos"
    
    services = ['auth', 'users', 'facilities', 'locks', 'cameras', 'videos', 'bridge', 'system_support']
    
    found = []
    missing = []
    
    for service in services:
        proto_file = proto_dir / f"{service}.proto"
        if proto_file.exists():
            found.append(service)
            print(f"   ✅ {service}.proto found")
        else:
            missing.append(service)
            print(f"   ❌ {service}.proto missing")
    
    if missing:
        print(f"\n   ⚠️  Missing proto files: {', '.join(missing)}")
        print(f"   Expected location: {proto_dir}")
        return False
    
    print(f"\n   ✅ All {len(found)} proto files found")
    return True

def test_output_directory():
    """Test that output directory can be created."""
    print("\n🧪 Testing output directory...")
    script_dir = Path(__file__).parent
    output_dir = script_dir / "generated"
    
    try:
        output_dir.mkdir(exist_ok=True)
        print(f"   ✅ Output directory: {output_dir}")
        
        # Test write permissions
        test_file = output_dir / ".test"
        test_file.write_text("test")
        test_file.unlink()
        print("   ✅ Write permissions OK")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_parser():
    """Test basic proto parsing functionality."""
    print("\n🧪 Testing proto parser...")
    try:
        from generate_postman_collections import ProtoParser
        
        script_dir = Path(__file__).parent
        proto_file = script_dir.parent.parent / "rallymate-api" / "protos" / "auth.proto"
        
        if not proto_file.exists():
            print(f"   ⚠️  Skipping (auth.proto not found)")
            return True
        
        parser = ProtoParser(proto_file)
        service_data = parser.parse_service()
        
        if service_data and service_data['rpcs']:
            print(f"   ✅ Successfully parsed {len(service_data['rpcs'])} RPCs")
            print(f"   ✅ Service name: {service_data['name']}")
            return True
        else:
            print("   ❌ Failed to parse service data")
            return False
            
    except Exception as e:
        print(f"   ❌ Parser error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_generator():
    """Test data generation functionality."""
    print("\n🧪 Testing data generator...")
    try:
        from generate_postman_collections import TestDataGenerator
        
        gen = TestDataGenerator()
        
        # Test various field types
        tests = [
            ('phone_number', 'string', '+1234567890'),
            ('email', 'string', 'test.user@example.com'),
            ('device_id', 'string', 'device-001'),
            ('page', 'int32', 1),
            ('is_active', 'bool', True),
        ]
        
        all_passed = True
        for field_name, field_type, expected_type in tests:
            value = gen.generate_value(field_name, field_type)
            if value is not None:
                print(f"   ✅ {field_name}: {value}")
            else:
                print(f"   ⚠️  {field_name}: None")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Data generator error: {e}")
        return False

def test_collection_generator():
    """Test collection generation functionality."""
    print("\n🧪 Testing collection generator...")
    try:
        from generate_postman_collections import PostmanCollectionGenerator, ProtoParser
        
        script_dir = Path(__file__).parent
        proto_file = script_dir.parent.parent / "rallymate-api" / "protos" / "auth.proto"
        
        if not proto_file.exists():
            print(f"   ⚠️  Skipping (auth.proto not found)")
            return True
        
        parser = ProtoParser(proto_file)
        service_data = parser.parse_service()
        
        if not service_data:
            print("   ❌ No service data to test")
            return False
        
        generator = PostmanCollectionGenerator(service_data, parser)
        collection = generator.generate_collection()
        
        # Validate collection structure
        required_keys = ['info', 'auth', 'variable', 'item']
        for key in required_keys:
            if key not in collection:
                print(f"   ❌ Missing required key: {key}")
                return False
        
        print(f"   ✅ Collection structure valid")
        print(f"   ✅ Generated {len(collection['item'])} requests")
        return True
        
    except Exception as e:
        print(f"   ❌ Collection generator error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("🚀 Postman Collection Generator - Validation Tests")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Proto Files", test_proto_files),
        ("Output Directory", test_output_directory),
        ("Proto Parser", test_parser),
        ("Data Generator", test_data_generator),
        ("Collection Generator", test_collection_generator),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("="*60)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Generator is ready to use.")
        print("\nRun: ./generate-all.sh")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
