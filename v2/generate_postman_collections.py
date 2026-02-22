#!/usr/bin/env python3
"""
Enhanced Postman Collection Generator for rallymate Services

Generates comprehensive Postman collections from proto files with:
- Realistic test data based on field types and names
- Automated test scripts with variable extraction
- Request chaining support
- Complete authentication flows

Usage:
    python generate_postman_collections.py
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class ProtoParser:
    """Enhanced parser for proto3 files with support for complex types."""
    
    def __init__(self, proto_file: Path):
        self.proto_file = proto_file
        self.content = proto_file.read_text()
        self.package_name = self._extract_package()
        self.messages = self._parse_messages()
        self.enums = self._parse_enums()
    
    def _find_matching_brace(self, text: str, start_pos: int) -> int:
        """Find the position of the matching closing brace.
        
        Args:
            text: The text to search in
            start_pos: Position right after the opening brace
            
        Returns:
            Position of the matching closing brace, or -1 if not found
        """
        brace_count = 1
        pos = start_pos
        in_string = False
        in_comment = False
        
        while pos < len(text) and brace_count > 0:
            # Handle line comments
            if not in_string and pos < len(text) - 1 and text[pos:pos+2] == '//':
                # Skip to end of line
                while pos < len(text) and text[pos] != '\n':
                    pos += 1
                pos += 1
                continue
            
            # Handle block comments
            if not in_string and pos < len(text) - 1 and text[pos:pos+2] == '/*':
                # Skip to end of comment
                pos += 2
                while pos < len(text) - 1:
                    if text[pos:pos+2] == '*/':
                        pos += 2
                        break
                    pos += 1
                continue
            
            # Handle strings
            if text[pos] == '"' and (pos == 0 or text[pos-1] != '\\'):
                in_string = not in_string
            
            # Count braces only when not in string or comment
            if not in_string and not in_comment:
                if text[pos] == '{':
                    brace_count += 1
                elif text[pos] == '}':
                    brace_count -= 1
            
            pos += 1
        
        return pos if brace_count == 0 else -1
    
    def _extract_package(self) -> str:
        """Extract package name from proto file."""
        match = re.search(r'package\s+([\w.]+)\s*;', self.content)
        return match.group(1) if match else ""
    
    def _parse_messages(self) -> Dict[str, Dict]:
        """Parse all message definitions."""
        messages = {}
        # Match message blocks with nested support
        pattern = r'message\s+(\w+)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}'
        
        for match in re.finditer(pattern, self.content, re.DOTALL):
            msg_name = match.group(1)
            msg_body = match.group(2)
            messages[msg_name] = self._parse_message_fields(msg_body)
        
        return messages
    
    def _parse_message_fields(self, msg_body: str) -> List[Dict]:
        """Parse fields from a message body."""
        fields = []
        # Pattern for field definition: [repeated] type name = number;
        field_pattern = r'(repeated\s+)?([\w.]+)\s+(\w+)\s*=\s*\d+;'
        
        for match in re.finditer(field_pattern, msg_body):
            is_repeated = bool(match.group(1))
            field_type = match.group(2)
            field_name = match.group(3)
            
            fields.append({
                'name': field_name,
                'type': field_type,
                'repeated': is_repeated
            })
        
        return fields
    
    def _parse_enums(self) -> Dict[str, List[str]]:
        """Parse all enum definitions."""
        enums = {}
        enum_pattern = r'enum\s+(\w+)\s*\{([^}]+)\}'
        
        for match in re.finditer(enum_pattern, self.content, re.DOTALL):
            enum_name = match.group(1)
            enum_body = match.group(2)
            
            # Extract enum values
            value_pattern = r'(\w+)\s*=\s*\d+;'
            values = [m.group(1) for m in re.finditer(value_pattern, enum_body)]
            enums[enum_name] = values
        
        return enums
    
    def parse_service(self) -> Optional[Dict]:
        """Extract service name and RPCs with HTTP annotations."""
        # Find service block with proper brace matching
        service_start = re.search(r'service\s+(\w+)\s*\{', self.content)
        
        if not service_start:
            return None
        
        service_name = service_start.group(1)
        start_pos = service_start.end()
        
        # Find matching closing brace
        end_pos = self._find_matching_brace(self.content, start_pos)
        
        if end_pos == -1:
            return None
        
        service_body = self.content[start_pos:end_pos-1]
        rpcs = self._parse_rpcs(service_body)
        
        return {
            'name': service_name,
            'rpcs': rpcs,
            'package': self.package_name
        }
    
    def _parse_rpcs(self, service_body: str) -> List[Dict]:
        """Parse RPC definitions with HTTP annotations."""
        rpcs = []
        
        # Find all RPC declarations
        rpc_pattern = r'rpc\s+(\w+)\s*\((\w+)\)\s*returns\s*\((\w+)\)\s*\{'
        
        for match in re.finditer(rpc_pattern, service_body):
            rpc_name = match.group(1)
            request_type = match.group(2)
            response_type = match.group(3)
            
            # Find the matching closing brace for this RPC
            start_pos = match.end()
            end_pos = self._find_matching_brace(service_body, start_pos)
            
            if end_pos != -1:
                rpc_body = service_body[start_pos:end_pos-1]
                
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
        # Find the start of HTTP annotation
        http_start = re.search(r'option\s+\(google\.api\.http\)\s*=\s*\{', rpc_body)
        
        if not http_start:
            return None
        
        # Find matching closing brace
        start_pos = http_start.end()
        end_pos = self._find_matching_brace(rpc_body, start_pos)
        
        if end_pos == -1:
            return None
        
        http_body = rpc_body[start_pos:end_pos-1]
        
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


class TestDataGenerator:
    """Generate realistic test data based on field types and names."""
    
    @staticmethod
    def generate_value(field_name: str, field_type: str, context: str = "") -> Any:
        """Generate realistic value for a field."""
        field_lower = field_name.lower()
        
        # Phone numbers
        if 'phone' in field_lower:
            return "+1234567890"
        
        # Email addresses
        if 'email' in field_lower:
            return "test.user@example.com"
        
        # Device IDs
        if 'device_id' in field_lower or field_name == 'device_id':
            if 'bridge' in context.lower():
                return "bridge-001"
            elif 'camera' in context.lower():
                return "camera-court-01"
            elif 'lock' in context.lower():
                return "lock-court-01"
            return "device-001"
        
        # Names
        if field_name in ['name', 'user_name', 'device_name']:
            if 'facility' in context.lower():
                return "Downtown Tennis Club"
            elif 'lock' in context.lower():
                return "Court 1 Gate Lock"
            elif 'camera' in context.lower():
                return "Court 1 Camera"
            elif 'bridge' in context.lower():
                return "Main Bridge Device"
            return "Test User"
        
        # Addresses
        if 'address' in field_lower:
            return "123 Main St, City, State 12345"
        
        # Descriptions
        if 'description' in field_lower:
            return "Automated test description"
        
        # Timezones
        if 'timezone' in field_lower:
            return "America/New_York"
        
        # OTP/OTC codes
        if field_name in ['otp_code', 'otc_code']:
            return "123456"
        
        # Device info
        if 'device_info' in field_lower:
            return "Test Device - Postman Collection"
        
        # IP addresses
        if 'ip_address' in field_lower:
            return "192.168.1.100"
        
        # Timestamps (RFC3339)
        if any(x in field_lower for x in ['timestamp', 'created_at', 'updated_at', 'start_time', 'end_time']):
            return datetime.now().isoformat() + "Z"
        
        if 'expires_at' in field_lower or 'expiry' in field_lower:
            future = datetime.now() + timedelta(days=30)
            return future.isoformat() + "Z"
        
        if 'start_date' in field_lower:
            return datetime.now().isoformat() + "Z"
        
        # URLs
        if 'url' in field_lower:
            if 'stream' in field_lower:
                return "rtsp://192.168.1.100:8554/stream"
            return "https://example.com/resource"
        
        # Firmware versions
        if 'firmware' in field_lower or 'version' in field_lower:
            return "v1.2.3"
        
        # Session tokens
        if 'session_token' in field_lower:
            return "{{session_token}}"
        
        if 'refresh_token' in field_lower:
            return "{{refresh_token}}"
        
        # Reasons
        if 'reason' in field_lower:
            return "Testing via Postman collection"
        
        # File names and sizes
        if 'filename' in field_lower:
            return "test-video-recording.mp4"
        
        if 'file_size' in field_lower:
            return 1048576  # 1MB
        
        if 'duration' in field_lower:
            return 60  # 60 seconds
        
        # Recording types
        if 'recording_type' in field_lower:
            return "manual"
        
        # Ports
        if 'port' in field_lower:
            if 'edge' in field_lower:
                return 8554
            return 12886
        
        # Search queries
        if 'search' in field_lower:
            return "test"
        
        # Pagination
        if field_name == 'page':
            return 1
        
        if 'page_size' in field_lower:
            return 10
        
        # Boolean fields
        if field_type == 'bool':
            if 'active' in field_lower or 'success' in field_lower:
                return True
            if 'only' in field_lower:
                return True
            return False
        
        # ID fields - use variables when appropriate
        if field_name == 'user_id':
            return "{{user_id}}"
        
        if field_name == 'facility_id':
            return "{{facility_id}}"
        
        if field_name == 'membership_id':
            return "{{membership_id}}"
        
        if field_name == 'video_id':
            return "{{video_id}}"
        
        if field_name == 'tunnel_id':
            return "{{tunnel_id}}"
        
        if field_name == 'connection_id':
            return "{{connection_id}}"
        
        if field_name == 'support_id':
            return "{{support_id}}"
        
        # Generic ID fields
        if field_name == 'id' or field_name.endswith('_id'):
            return 1
        
        # Integers
        if field_type in ['int32', 'uint32', 'int64', 'uint64']:
            if 'count' in field_lower:
                return 5
            if 'attempts' in field_lower:
                return 3
            return 1
        
        # Strings
        if field_type == 'string':
            return f"test_{field_name}"
        
        # Enums - return the first non-unspecified value
        if field_type.isupper() or any(x in field_type for x in ['Status', 'State', 'Action', 'Role', 'Type']):
            # Return placeholder - will be replaced with actual enum value
            return f"ENUM_VALUE_{field_type}"
        
        # Default
        return ""


class PostmanCollectionGenerator:
    """Generate Postman v2.1 collection from parsed proto data."""
    
    def __init__(self, service_data: Dict, proto_parser: ProtoParser, base_url: str = "{{base_url}}"):
        self.service_data = service_data
        self.parser = proto_parser
        self.base_url = base_url
        self.data_gen = TestDataGenerator()
    
    def generate_collection(self) -> Dict:
        """Generate complete Postman collection structure."""
        service_name = self.service_data['name']
        
        collection = {
            "info": {
                "name": f"rallymate {service_name}",
                "description": f"Auto-generated collection for {service_name} service with realistic test data",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
                "_postman_id": self._generate_uuid(),
                "version": "2.0.0"
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
        
        # Generate URL with Postman variables for path params
        url_parts = []
        for part in path.split('/'):
            if part:
                if part.startswith('{') and part.endswith('}'):
                    param_name = part[1:-1]
                    url_parts.append(f"{{{{{param_name}}}}}")
                else:
                    url_parts.append(part)
        
        full_url = f"{self.base_url}/{'/'.join(url_parts)}"
        
        # Build request body example
        request_body = None
        if method in ['POST', 'PUT', 'PATCH']:
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
                    "raw": full_url,
                    "host": ["{{base_url}}"],
                    "path": url_parts
                },
                "description": f"**RPC:** {rpc['name']}\n\n**Request:** {rpc['request_type']}\n\n**Response:** {rpc['response_type']}\n\n**Endpoint:** {method} {path}"
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
        if request_body:
            request_item['request']['body'] = {
                "mode": "raw",
                "raw": json.dumps(request_body, indent=2),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            }
        
        return request_item
    
    def _generate_request_body(self, rpc: Dict, path_params: List[str]) -> Dict:
        """Generate example request body with realistic data."""
        request_type = rpc['request_type']
        
        if request_type not in self.parser.messages:
            return {}
        
        fields = self.parser.messages[request_type]
        body = {}
        
        for field in fields:
            field_name = field['name']
            field_type = field['type']
            
            # Skip path parameters - they go in URL
            if field_name in path_params:
                continue
            
            # Generate value based on field type and name
            if field['repeated']:
                # For repeated fields, create an array with one example
                value = self.data_gen.generate_value(field_name, field_type, rpc['name'])
                body[field_name] = [value] if value else []
            else:
                value = self.data_gen.generate_value(field_name, field_type, rpc['name'])
                
                # Replace enum placeholders with actual values
                if isinstance(value, str) and value.startswith('ENUM_VALUE_'):
                    enum_name = value.replace('ENUM_VALUE_', '')
                    if enum_name in self.parser.enums:
                        enum_values = self.parser.enums[enum_name]
                        # Pick first non-unspecified value
                        for enum_val in enum_values:
                            if 'UNSPECIFIED' not in enum_val:
                                value = enum_val
                                break
                
                # Only add non-empty values to body
                if value or value is False or value == 0:
                    body[field_name] = value
        
        return body
    
    def _generate_test_script(self, rpc: Dict) -> List[str]:
        """Generate test script for the request with variable extraction."""
        lines = [
            "// Validate response status",
            "pm.test('Status is 200 OK', function() {",
            "    pm.response.to.have.status(200);",
            "});",
            "",
            "// Validate response time",
            "pm.test('Response time under 2s', function() {",
            "    pm.expect(pm.response.responseTime).to.be.below(2000);",
            "});",
            ""
        ]
        
        # Add response parsing and variable extraction
        response_type = rpc['response_type']
        
        lines.extend([
            "// Parse and extract response data",
            "if (pm.response.code === 200) {",
            "    try {",
            "        const response = pm.response.json();",
            "        console.log('✅ Response:', JSON.stringify(response, null, 2));",
            ""
        ])
        
        # Extract common variables based on response type and RPC name
        rpc_lower = rpc['name'].lower()
        
        # Session token extraction (auth endpoints)
        if 'verify' in rpc_lower and 'session' in str(self.parser.messages.get(response_type, [])).lower():
            lines.extend([
                "        // Extract session tokens",
                "        if (response.session && response.session.session_token) {",
                "            pm.collectionVariables.set('session_token', response.session.session_token);",
                "            console.log('🔑 Session token saved');",
                "        }",
                "        if (response.session && response.session.refresh_token) {",
                "            pm.collectionVariables.set('refresh_token', response.session.refresh_token);",
                "        }",
                "        if (response.session && response.session.user_id) {",
                "            pm.collectionVariables.set('user_id', response.session.user_id);",
                "            console.log('👤 User ID:', response.session.user_id);",
                "        }",
                "        if (response.session && response.session.device_id) {",
                "            pm.collectionVariables.set('device_id', response.session.device_id);",
                "        }",
                ""
            ])
        
        # User creation
        if 'create' in rpc_lower and 'user' in rpc_lower:
            lines.extend([
                "        // Extract user ID",
                "        if (response.user && response.user.id) {",
                "            pm.collectionVariables.set('user_id', response.user.id);",
                "            console.log('👤 User ID:', response.user.id);",
                "        }",
                ""
            ])
        
        # Facility creation
        if 'create' in rpc_lower and 'facility' in rpc_lower:
            lines.extend([
                "        // Extract facility ID",
                "        if (response.facility && response.facility.id) {",
                "            pm.collectionVariables.set('facility_id', response.facility.id);",
                "            console.log('🏢 Facility ID:', response.facility.id);",
                "        }",
                ""
            ])
        
        # Membership creation
        if 'create' in rpc_lower and 'membership' in rpc_lower:
            lines.extend([
                "        // Extract membership ID",
                "        if (response.membership && response.membership.id) {",
                "            pm.collectionVariables.set('membership_id', response.membership.id);",
                "            console.log('🎫 Membership ID:', response.membership.id);",
                "        }",
                ""
            ])
        
        # Device registration
        if 'register' in rpc_lower:
            if 'bridge' in rpc_lower:
                lines.extend([
                    "        // Extract bridge device ID",
                    "        if (response.bridge && response.bridge.device_id) {",
                    "            pm.collectionVariables.set('bridge_device_id', response.bridge.device_id);",
                    "            console.log('🌉 Bridge ID:', response.bridge.device_id);",
                    "        }",
                    ""
                ])
            elif 'lock' in rpc_lower:
                lines.extend([
                    "        // Extract lock device ID",
                    "        if (response.lock && response.lock.device_id) {",
                    "            pm.collectionVariables.set('lock_device_id', response.lock.device_id);",
                    "            console.log('🔒 Lock ID:', response.lock.device_id);",
                    "        }",
                    ""
                ])
            elif 'camera' in rpc_lower:
                lines.extend([
                    "        // Extract camera device ID",
                    "        if (response.camera && response.camera.device_id) {",
                    "            pm.collectionVariables.set('camera_device_id', response.camera.device_id);",
                    "            console.log('📹 Camera ID:', response.camera.device_id);",
                    "        }",
                    ""
                ])
            elif 'edge' in rpc_lower or 'connection' in rpc_lower:
                lines.extend([
                    "        // Extract connection ID",
                    "        if (response.edge_connection && response.edge_connection.id) {",
                    "            pm.collectionVariables.set('connection_id', response.edge_connection.id);",
                    "            console.log('🔗 Connection ID:', response.edge_connection.id);",
                    "        }",
                    ""
                ])
        
        # Tunnel operations
        if 'tunnel' in rpc_lower:
            lines.extend([
                "        // Extract tunnel information",
                "        if (response.tunnel && response.tunnel.id) {",
                "            pm.collectionVariables.set('tunnel_id', response.tunnel.id);",
                "            console.log('🚇 Tunnel ID:', response.tunnel.id);",
                "        }",
                "        if (response.tunnel && response.tunnel.cloud_port) {",
                "            pm.collectionVariables.set('cloud_port', response.tunnel.cloud_port);",
                "        }",
                ""
            ])
        
        # Video upload
        if 'upload' in rpc_lower or ('create' in rpc_lower and 'video' in rpc_lower):
            lines.extend([
                "        // Extract video ID",
                "        if (response.video && response.video.id) {",
                "            pm.collectionVariables.set('video_id', response.video.id);",
                "            console.log('🎥 Video ID:', response.video.id);",
                "        }",
                ""
            ])
        
        # System support
        if 'system' in rpc_lower and 'support' in rpc_lower:
            lines.extend([
                "        // Extract support ID",
                "        if (response.system_support && response.system_support.id) {",
                "            pm.collectionVariables.set('support_id', response.system_support.id);",
                "            console.log('🛠️ Support ID:', response.system_support.id);",
                "        }",
                ""
            ])
        
        lines.extend([
            "    } catch (e) {",
            "        console.log('⚠️ Could not parse response:', e);",
            "    }",
            "}"
        ])
        
        return lines
    
    def _format_request_name(self, rpc_name: str) -> str:
        """Convert RPC name to human-readable request name."""
        # Convert CamelCase to Title Case with spaces
        words = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', rpc_name)
        return ' '.join(words)
    
    def _generate_uuid(self) -> str:
        """Generate a simple UUID for Postman."""
        import uuid
        return str(uuid.uuid4())


def generate_environment(name: str, base_url: str) -> Dict:
    """Generate Postman environment file."""
    return {
        "id": f"rallymate-{name.lower()}",
        "name": f"rallymate - {name}",
        "values": [
            {
                "key": "base_url",
                "value": base_url,
                "type": "default",
                "enabled": True
            },
            {
                "key": "phone_number",
                "value": "+1234567890",
                "type": "default",
                "enabled": True
            },
            {
                "key": "facility_id",
                "value": "1",
                "type": "default",
                "enabled": True
            },
            {
                "key": "session_token",
                "value": "",
                "type": "secret",
                "enabled": True
            },
            {
                "key": "refresh_token",
                "value": "",
                "type": "secret",
                "enabled": True
            },
            {
                "key": "user_id",
                "value": "",
                "type": "default",
                "enabled": True
            },
            {
                "key": "device_id",
                "value": "bridge-001",
                "type": "default",
                "enabled": True
            }
        ],
        "_postman_variable_scope": "environment",
        "_postman_exported_at": datetime.now().isoformat() + "Z",
        "_postman_exported_using": "Postman Collection Generator"
    }


def main():
    """Main execution function."""
    # Setup paths
    script_dir = Path(__file__).parent
    proto_dir = script_dir.parent.parent / "rallymate-api" / "protos"
    output_dir = script_dir / "generated"
    output_dir.mkdir(exist_ok=True)
    
    # Proto files to process
    services = [
        'auth',
        'users',
        'facilities',
        'locks',
        'cameras',
        'videos',
        'bridge',
        'system_support'
    ]
    
    print("🚀 rallymate Postman Collection Generator")
    print("=" * 60)
    print()
    
    collections_generated = []
    
    # Generate collection for each service
    for service in services:
        proto_file = proto_dir / f"{service}.proto"
        
        if not proto_file.exists():
            print(f"⚠️  Skipping {service}: Proto file not found")
            continue
        
        print(f"📄 Processing {service}.proto...")
        
        try:
            # Parse proto file
            parser = ProtoParser(proto_file)
            service_data = parser.parse_service()
            
            if not service_data:
                print(f"   ⚠️  No service found in proto file")
                continue
            
            if not service_data['rpcs']:
                print(f"   ⚠️  Service '{service_data.get('name', 'Unknown')}' has no RPCs with HTTP annotations")
                continue
            
            print(f"   ✅ Found {len(service_data['rpcs'])} RPCs with HTTP annotations")
            
            # Generate collection
            generator = PostmanCollectionGenerator(service_data, parser)
            collection = generator.generate_collection()
            
            # Write collection file
            output_file = output_dir / f"{service}_service.postman_collection.json"
            with open(output_file, 'w') as f:
                json.dump(collection, f, indent=2)
            
            print(f"   💾 Collection saved: {output_file.name}")
            collections_generated.append(service)
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print()
    print("=" * 60)
    
    # Generate environment files
    if collections_generated:
        print("\n📦 Generating environment files...")
        
        environments = [
            ("Local", "http://localhost:8080"),
            ("Development", "https://dev.rallymate.io"),
            ("Production", "https://api.rallymate.io")
        ]
        
        for env_name, base_url in environments:
            env = generate_environment(env_name, base_url)
            env_file = output_dir / f"rallymate-{env_name.lower()}.postman_environment.json"
            
            with open(env_file, 'w') as f:
                json.dump(env, f, indent=2)
            
            print(f"   💾 {env_file.name}")
    
    # Summary
    print()
    print("=" * 60)
    print(f"✅ Successfully generated {len(collections_generated)} collections:")
    for service in collections_generated:
        print(f"   • {service}_service.postman_collection.json")
    
    print()
    print("📥 Import these files into Postman to start testing!")
    print(f"📁 Output directory: {output_dir}")
    
    return 0


if __name__ == '__main__':
    exit(main())
