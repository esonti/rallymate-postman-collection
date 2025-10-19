#!/usr/bin/env python3
"""
Generate Postman collection JSON from proto files with HTTP annotations.

This script helps automate the creation of Postman collection items from proto files.
It parses proto files to extract:
- Service RPCs with google.api.http annotations
- Request/Response message types
- HTTP methods and paths

Usage:
    python generate_collection.py --proto-dir ../rallymate-api/protos --service auth
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ProtoParser:
    """Parse proto files to extract service definitions and HTTP annotations."""
    
    def __init__(self, proto_file: Path):
        self.proto_file = proto_file
        self.content = proto_file.read_text()
    
    def parse_service(self) -> Dict:
        """Extract service name and RPCs with HTTP annotations."""
        service_pattern = r'service\s+(\w+)\s*{([^}]+)}'
        service_match = re.search(service_pattern, self.content, re.DOTALL)
        
        if not service_match:
            return None
        
        service_name = service_match.group(1)
        service_body = service_match.group(2)
        
        rpcs = self._parse_rpcs(service_body)
        
        return {
            'name': service_name,
            'rpcs': rpcs
        }
    
    def _parse_rpcs(self, service_body: str) -> List[Dict]:
        """Parse RPC definitions with HTTP annotations."""
        rpcs = []
        
        # Pattern to match RPC with HTTP annotation
        rpc_pattern = r'rpc\s+(\w+)\s*\((\w+)\)\s*returns\s*\((\w+)\)\s*{([^}]+)}'
        
        for match in re.finditer(rpc_pattern, service_body, re.DOTALL):
            rpc_name = match.group(1)
            request_type = match.group(2)
            response_type = match.group(3)
            rpc_body = match.group(4)
            
            # Extract HTTP annotation
            http_annotation = self._parse_http_annotation(rpc_body)
            
            if http_annotation:
                rpcs.append({
                    'name': rpc_name,
                    'request_type': request_type,
                    'response_type': response_type,
                    'http': http_annotation
                })
        
        return rpcs
    
    def _parse_http_annotation(self, rpc_body: str) -> Optional[Dict]:
        """Extract HTTP method and path from google.api.http annotation."""
        # Pattern for HTTP annotation
        http_pattern = r'option\s+\(google\.api\.http\)\s*=\s*{([^}]+)}'
        http_match = re.search(http_pattern, rpc_body, re.DOTALL)
        
        if not http_match:
            return None
        
        http_body = http_match.group(1)
        
        # Extract method and path
        method = None
        path = None
        body_field = None
        
        # Check for each HTTP method
        for http_method in ['get', 'post', 'put', 'patch', 'delete']:
            method_pattern = rf'{http_method}:\s*"([^"]+)"'
            method_match = re.search(method_pattern, http_body)
            if method_match:
                method = http_method.upper()
                path = method_match.group(1)
                break
        
        # Extract body field if present
        body_pattern = r'body:\s*"([^"]+)"'
        body_match = re.search(body_pattern, http_body)
        if body_match:
            body_field = body_match.group(1)
        
        if method and path:
            return {
                'method': method,
                'path': path,
                'body': body_field
            }
        
        return None
    
    def get_message_fields(self, message_name: str) -> List[Dict]:
        """Extract fields from a message definition."""
        message_pattern = rf'message\s+{message_name}\s*{{([^}}]+)}}'
        message_match = re.search(message_pattern, self.content, re.DOTALL)
        
        if not message_match:
            return []
        
        message_body = message_match.group(1)
        fields = []
        
        # Pattern for field definition
        field_pattern = r'(\w+)\s+(\w+)\s*=\s*\d+;'
        
        for match in re.finditer(field_pattern, message_body):
            field_type = match.group(1)
            field_name = match.group(2)
            fields.append({
                'type': field_type,
                'name': field_name
            })
        
        return fields


class PostmanCollectionGenerator:
    """Generate Postman collection JSON from parsed proto data."""
    
    def __init__(self, service_data: Dict, base_url: str = "{{base_url}}"):
        self.service_data = service_data
        self.base_url = base_url
    
    def generate_collection(self) -> Dict:
        """Generate complete Postman collection structure."""
        service_name = self.service_data['name']
        
        collection = {
            "info": {
                "name": f"RallyMate {service_name} Service API",
                "description": f"Auto-generated collection for {service_name} service",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "auth": {
                "type": "bearer",
                "bearer": [
                    {
                        "key": "token",
                        "value": "{{session_token}}",
                        "type": "string"
                    }
                ]
            },
            "variable": [
                {
                    "key": "base_url",
                    "value": "http://localhost:8080",
                    "type": "string"
                }
            ],
            "item": []
        }
        
        # Generate requests for each RPC
        for rpc in self.service_data['rpcs']:
            request_item = self._generate_request(rpc)
            collection['item'].append(request_item)
        
        return collection
    
    def _generate_request(self, rpc: Dict) -> Dict:
        """Generate Postman request item from RPC definition."""
        http_info = rpc['http']
        method = http_info['method']
        path = http_info['path']
        
        # Parse path parameters
        path_params = re.findall(r'\{(\w+)\}', path)
        
        # Generate URL
        url_parts = path.split('/')
        url_path = []
        for part in url_parts:
            if part:
                # Convert {param} to {{param}}
                if part.startswith('{') and part.endswith('}'):
                    param_name = part[1:-1]
                    url_path.append(f"{{{{{param_name}}}}}")
                else:
                    url_path.append(part)
        
        # Build request body example
        request_body = self._generate_request_body(rpc, path_params)
        
        # Build test script
        test_script = self._generate_test_script(rpc)
        
        request_item = {
            "name": self._format_request_name(rpc['name']),
            "request": {
                "method": method,
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json",
                        "type": "text"
                    }
                ],
                "url": {
                    "raw": f"{self.base_url}/{'/'.join(url_path)}",
                    "host": [self.base_url],
                    "path": url_path
                },
                "description": f"Calls {rpc['name']} RPC"
            },
            "event": [
                {
                    "listen": "test",
                    "script": {
                        "exec": test_script,
                        "type": "text/javascript"
                    }
                }
            ]
        }
        
        # Add body if method supports it
        if method in ['POST', 'PUT', 'PATCH'] and request_body:
            request_item['request']['body'] = {
                "mode": "raw",
                "raw": json.dumps(request_body, indent=2)
            }
        
        return request_item
    
    def _generate_request_body(self, rpc: Dict, path_params: List[str]) -> Dict:
        """Generate example request body."""
        # This is a placeholder - you'd need to parse message definitions
        # For now, return empty object or basic structure
        request_type = rpc['request_type']
        
        # Filter out path parameters from body
        body = {}
        
        # Add example fields based on common patterns
        if 'phone' in request_type.lower():
            body['phone_number'] = "{{phone_number}}"
        
        if 'otp' in request_type.lower():
            body['otp_code'] = "123456"
        
        if 'device' in request_type.lower():
            body['device_info'] = "Test Device"
        
        if 'user' in request_type.lower():
            body['user_id'] = "{{user_id}}"
        
        if 'facility' in request_type.lower():
            body['facility_id'] = "{{facility_id}}"
        
        return body
    
    def _generate_test_script(self, rpc: Dict) -> List[str]:
        """Generate test script for the request."""
        lines = [
            "// Validate response status",
            "pm.test('Status is 200', function() {",
            "    pm.response.to.have.status(200);",
            "});",
            "",
            "// Validate response time",
            "pm.test('Response time under 1s', function() {",
            "    pm.expect(pm.response.responseTime).to.be.below(1000);",
            "});",
            "",
            "// Extract response data",
            "if (pm.response.code === 200) {",
            "    try {",
            "        const response = pm.response.json();",
            "        console.log('✅ Response:', JSON.stringify(response, null, 2));",
            "        ",
            "        // TODO: Add specific data extraction based on response type",
            f"        // Response type: {rpc['response_type']}",
            "    } catch (e) {",
            "        console.log('⚠️ Could not parse response:', e);",
            "    }",
            "}"
        ]
        
        return lines
    
    def _format_request_name(self, rpc_name: str) -> str:
        """Convert RPC name to human-readable request name."""
        # Convert CamelCase to Title Case with spaces
        words = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', rpc_name)
        return ' '.join(words)


def main():
    parser = argparse.ArgumentParser(description='Generate Postman collection from proto files')
    parser.add_argument('--proto-dir', required=True, help='Directory containing proto files')
    parser.add_argument('--service', required=True, help='Service name (e.g., auth, users)')
    parser.add_argument('--output', help='Output file path (default: stdout)')
    parser.add_argument('--base-url', default='{{base_url}}', help='Base URL for requests')
    
    args = parser.parse_args()
    
    # Find proto file
    proto_dir = Path(args.proto_dir)
    proto_file = proto_dir / f"{args.service}.proto"
    
    if not proto_file.exists():
        print(f"Error: Proto file not found: {proto_file}")
        return 1
    
    # Parse proto file
    print(f"Parsing {proto_file}...")
    parser = ProtoParser(proto_file)
    service_data = parser.parse_service()
    
    if not service_data:
        print(f"Error: No service found in {proto_file}")
        return 1
    
    print(f"Found service: {service_data['name']}")
    print(f"Found {len(service_data['rpcs'])} RPCs with HTTP annotations")
    
    # Generate collection
    generator = PostmanCollectionGenerator(service_data, args.base_url)
    collection = generator.generate_collection()
    
    # Output
    collection_json = json.dumps(collection, indent=2)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(collection_json)
        print(f"✅ Collection written to {output_path}")
    else:
        print("\n" + "="*80)
        print(collection_json)
    
    return 0


if __name__ == '__main__':
    exit(main())
