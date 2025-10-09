# MCP Integration Guide for RedCalibur

## 🔌 Model Context Protocol (MCP) Overview

MCP is a standardized protocol for integrating AI tools and agents. It provides a universal interface for connecting LLMs to external tools, data sources, and services.

**Key Benefits:**
- Standardized tool invocation
- Cross-platform compatibility
- Built-in error handling and retry logic
- Streaming support for real-time results
- Secure parameter passing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RedCalibur Application                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  MCP Client Layer                     │  │
│  │  - Connection Management                              │  │
│  │  - Protocol Handling (STDIO/SSE)                      │  │
│  │  - Tool Discovery                                      │  │
│  │  - Request/Response Marshaling                        │  │
│  └────────────┬─────────────────────────────────────────┘  │
│               │                                              │
└───────────────┼──────────────────────────────────────────────┘
                │ MCP Protocol (JSON-RPC 2.0)
                │
┌───────────────┼──────────────────────────────────────────────┐
│               │         MCP Server Ecosystem                 │
│  ┌────────────▼────────┐  ┌───────────────┐  ┌────────────┐│
│  │   nmap-mcp          │  │ metasploit-mcp│  │ nuclei-mcp ││
│  │   - Port Scanning   │  │ - Exploitation│  │ - Vuln Scan││
│  └─────────────────────┘  └───────────────┘  └────────────┘│
│  ┌─────────────────────┐  ┌───────────────┐  ┌────────────┐│
│  │   sqlmap-mcp        │  │ hydra-mcp     │  │ ffuf-mcp   ││
│  │   - SQL Injection   │  │ - Brute Force │  │ - Fuzzing  ││
│  └─────────────────────┘  └───────────────┘  └────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 MCP Client Implementation

### 1. Core MCP Client

```python
# redcalibur/mcp/client.py

import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

class MCPTransport(Enum):
    STDIO = "stdio"  # Standard input/output
    SSE = "sse"      # Server-Sent Events (HTTP)

@dataclass
class MCPTool:
    """Represents an MCP tool definition"""
    name: str
    description: str
    inputSchema: Dict[str, Any]

@dataclass
class MCPServer:
    """Represents an MCP server configuration"""
    name: str
    command: str
    args: List[str]
    transport: MCPTransport
    tools: List[MCPTool]

class MCPClient:
    """
    Client for communicating with MCP servers.
    Supports both STDIO and SSE transports.
    """
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.connections: Dict[str, Any] = {}
        self.logger = logging.getLogger("mcp.client")
        
    async def register_server(
        self,
        name: str,
        command: str,
        args: List[str] = None,
        transport: MCPTransport = MCPTransport.STDIO
    ) -> MCPServer:
        """
        Register a new MCP server.
        
        Args:
            name: Unique identifier for the server
            command: Command to start the server (e.g., "npx")
            args: Arguments to pass (e.g., ["-y", "nmap-mcp"])
            transport: STDIO or SSE
            
        Returns:
            MCPServer instance
        """
        
        server = MCPServer(
            name=name,
            command=command,
            args=args or [],
            transport=transport,
            tools=[]
        )
        
        # Connect to server
        await self._connect_server(server)
        
        # Discover available tools
        tools = await self._discover_tools(server)
        server.tools = tools
        
        self.servers[name] = server
        self.logger.info(f"Registered MCP server: {name} ({len(tools)} tools)")
        
        return server
    
    async def _connect_server(self, server: MCPServer):
        """Establish connection to MCP server"""
        
        if server.transport == MCPTransport.STDIO:
            # Start subprocess
            process = await asyncio.create_subprocess_exec(
                server.command,
                *server.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.connections[server.name] = {
                'process': process,
                'transport': 'stdio'
            }
            
        elif server.transport == MCPTransport.SSE:
            # HTTP/SSE connection
            import aiohttp
            
            session = aiohttp.ClientSession()
            self.connections[server.name] = {
                'session': session,
                'transport': 'sse'
            }
    
    async def _discover_tools(self, server: MCPServer) -> List[MCPTool]:
        """
        Discover available tools from MCP server.
        Uses MCP protocol's tools/list method.
        """
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        response = await self._send_request(server.name, request)
        
        tools = []
        for tool_data in response.get('result', {}).get('tools', []):
            tools.append(MCPTool(
                name=tool_data['name'],
                description=tool_data['description'],
                inputSchema=tool_data['inputSchema']
            ))
        
        return tools
    
    async def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a tool on an MCP server.
        
        Args:
            server_name: Name of the registered server
            tool_name: Name of the tool to call
            arguments: Tool-specific parameters
            
        Returns:
            Tool execution result
        """
        
        if server_name not in self.servers:
            raise ValueError(f"Server {server_name} not registered")
        
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        self.logger.info(f"Calling {server_name}.{tool_name} with args: {arguments}")
        
        response = await self._send_request(server_name, request)
        
        if 'error' in response:
            raise Exception(f"MCP Error: {response['error']}")
        
        return response.get('result', {})
    
    async def _send_request(
        self,
        server_name: str,
        request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send JSON-RPC request to server"""
        
        connection = self.connections[server_name]
        
        if connection['transport'] == 'stdio':
            process = connection['process']
            
            # Send request
            request_json = json.dumps(request) + '\n'
            process.stdin.write(request_json.encode())
            await process.stdin.drain()
            
            # Read response
            response_line = await process.stdout.readline()
            response = json.loads(response_line.decode())
            
            return response
            
        elif connection['transport'] == 'sse':
            # HTTP/SSE request
            session = connection['session']
            # Implementation for SSE transport
            pass
    
    async def list_tools(self, server_name: Optional[str] = None) -> List[MCPTool]:
        """
        List available tools.
        
        Args:
            server_name: Specific server or None for all servers
            
        Returns:
            List of available tools
        """
        
        if server_name:
            return self.servers[server_name].tools
        else:
            all_tools = []
            for server in self.servers.values():
                all_tools.extend(server.tools)
            return all_tools
    
    async def close(self):
        """Close all server connections"""
        
        for server_name, connection in self.connections.items():
            if connection['transport'] == 'stdio':
                process = connection['process']
                process.terminate()
                await process.wait()
            elif connection['transport'] == 'sse':
                session = connection['session']
                await session.close()
        
        self.connections.clear()
```

---

### 2. MCP Server Definitions

```python
# redcalibur/mcp/servers.py

from typing import Dict, List
from .client import MCPTransport

MCP_SERVERS = {
    "nmap": {
        "command": "npx",
        "args": ["-y", "nmap-mcp"],
        "transport": MCPTransport.STDIO,
        "description": "Network scanning and port discovery",
        "category": "reconnaissance"
    },
    "metasploit": {
        "command": "npx",
        "args": ["-y", "metasploit-mcp"],
        "transport": MCPTransport.STDIO,
        "description": "Exploitation framework",
        "category": "exploitation"
    },
    "sqlmap": {
        "command": "npx",
        "args": ["-y", "sqlmap-mcp"],
        "transport": MCPTransport.STDIO,
        "description": "SQL injection detection and exploitation",
        "category": "exploitation"
    },
    "nuclei": {
        "command": "npx",
        "args": ["-y", "nuclei-mcp"],
        "transport": MCPTransport.STDIO,
        "description": "Vulnerability scanner with templates",
        "category": "vulnerability_scanning"
    },
    "ffuf": {
        "command": "npx",
        "args": ["-y", "ffuf-mcp"],
        "transport": MCPTransport.STDIO,
        "description": "Fast web fuzzer",
        "category": "reconnaissance"
    },
    "hydra": {
        "command": "npx",
        "args": ["-y", "hydra-mcp"],
        "transport": MCPTransport.STDIO,
        "description": "Password brute force tool",
        "category": "credential_access"
    },
    "burpsuite": {
        "command": "python",
        "args": ["-m", "burpsuite_mcp"],
        "transport": MCPTransport.STDIO,
        "description": "Web application security testing",
        "category": "exploitation"
    },
    "gobuster": {
        "command": "npx",
        "args": ["-y", "gobuster-mcp"],
        "transport": MCPTransport.STDIO,
        "description": "Directory/file brute forcing",
        "category": "reconnaissance"
    }
}

async def register_all_servers(client):
    """Register all MCP servers with the client"""
    
    for name, config in MCP_SERVERS.items():
        try:
            await client.register_server(
                name=name,
                command=config["command"],
                args=config["args"],
                transport=config["transport"]
            )
            print(f"✓ Registered {name} MCP server")
        except Exception as e:
            print(f"✗ Failed to register {name}: {e}")
```

---

### 3. Tool Manager Integration

```python
# redcalibur/ai_core/tool_manager.py

from redcalibur.mcp.client import MCPClient
from redcalibur.mcp.servers import register_all_servers
import asyncio

class ToolManager:
    """
    Unified tool management system that integrates:
    - Native Python tools
    - MCP servers
    - External CLI tools
    """
    
    def __init__(self):
        self.mcp_client = MCPClient()
        self.native_tools = {}
        self.cli_tools = {}
        
    async def initialize(self):
        """Initialize all tool sources"""
        
        # Register MCP servers
        await register_all_servers(self.mcp_client)
        
        # Register native tools
        self._register_native_tools()
        
        # Register CLI tools
        self._register_cli_tools()
    
    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool by name.
        Automatically routes to MCP, native, or CLI tool.
        """
        
        # Check if it's an MCP tool
        for server_name, server in self.mcp_client.servers.items():
            for tool in server.tools:
                if tool.name == tool_name:
                    return await self.mcp_client.call_tool(
                        server_name,
                        tool_name,
                        parameters
                    )
        
        # Check native tools
        if tool_name in self.native_tools:
            return await self.native_tools[tool_name](**parameters)
        
        # Check CLI tools
        if tool_name in self.cli_tools:
            return await self._execute_cli_tool(tool_name, parameters)
        
        raise ValueError(f"Tool {tool_name} not found")
    
    def _register_native_tools(self):
        """Register Python-based tools"""
        
        from redcalibur.osint import whois_lookup, dns_enumeration
        from redcalibur.phishing_detection import analyze_url
        
        self.native_tools = {
            'whois': whois_lookup,
            'dns_enum': dns_enumeration,
            'phishing_check': analyze_url
        }
    
    def _register_cli_tools(self):
        """Register external CLI tools"""
        
        self.cli_tools = {
            'theHarvester': {
                'command': 'theHarvester',
                'args_template': ['-d', '{domain}', '-b', 'all']
            },
            'subfinder': {
                'command': 'subfinder',
                'args_template': ['-d', '{domain}', '-silent']
            }
        }
    
    async def _execute_cli_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute external CLI tool"""
        
        tool_config = self.cli_tools[tool_name]
        
        # Build command
        args = []
        for arg_template in tool_config['args_template']:
            arg = arg_template.format(**parameters)
            args.append(arg)
        
        # Execute
        process = await asyncio.create_subprocess_exec(
            tool_config['command'],
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return {
            'success': process.returncode == 0,
            'stdout': stdout.decode(),
            'stderr': stderr.decode()
        }
```

---

## 🔧 Usage Examples

### Example 1: Basic MCP Tool Call

```python
from redcalibur.mcp.client import MCPClient
from redcalibur.mcp.servers import register_all_servers

# Initialize client
client = MCPClient()
await register_all_servers(client)

# Call nmap tool
result = await client.call_tool(
    server_name="nmap",
    tool_name="scan",
    arguments={
        "target": "192.168.1.1",
        "scan_type": "syn",
        "ports": "1-1000"
    }
)

print(f"Open ports: {result['open_ports']}")
```

### Example 2: Through Tool Manager

```python
from redcalibur.ai_core.tool_manager import ToolManager

# Initialize tool manager
tool_manager = ToolManager()
await tool_manager.initialize()

# Execute any tool (MCP or native)
result = await tool_manager.execute_tool(
    tool_name="sqlmap",
    parameters={
        "url": "http://vulnerable.com/login.php",
        "data": "username=admin&password=test",
        "level": 3,
        "risk": 2
    }
)
```

### Example 3: Agent Integration

```python
class ExploitAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Exploit",
            description="Exploitation specialist",
            tools=["sqlmap", "metasploit", "nuclei"]  # MCP tools
        )
        
    async def act(self, thought: AgentThought) -> AgentAction:
        return AgentAction(
            tool="sqlmap",  # Will be routed to MCP
            parameters={
                "url": "http://target.com/api",
                "technique": "BEUSTQ"
            },
            reasoning="Testing for SQL injection",
            expected_outcome="SQL injection vulnerability found"
        )
```

---

## 📝 Creating Custom MCP Servers

### Example: Custom Tool MCP Server

```python
# custom_tool_mcp/server.py

from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio

# Initialize MCP server
server = Server("custom-tool-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="custom_scan",
            description="Custom scanning tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target to scan"
                    },
                    "options": {
                        "type": "object",
                        "description": "Scan options"
                    }
                },
                "required": ["target"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool"""
    
    if name == "custom_scan":
        target = arguments["target"]
        options = arguments.get("options", {})
        
        # Perform scan
        result = await perform_scan(target, options)
        
        return [
            TextContent(
                type="text",
                text=f"Scan results: {result}"
            )
        ]

async def perform_scan(target: str, options: dict):
    """Custom scan implementation"""
    # Your tool logic here
    return {"status": "completed", "findings": []}

# Run server
if __name__ == "__main__":
    import mcp.server.stdio
    
    async def main():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    asyncio.run(main())
```

---

## 🛡️ Security Considerations

### 1. Input Validation

```python
def validate_mcp_arguments(tool: MCPTool, arguments: Dict[str, Any]):
    """Validate arguments against tool schema"""
    
    schema = tool.inputSchema
    
    # Check required fields
    required = schema.get('required', [])
    for field in required:
        if field not in arguments:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate types
    properties = schema.get('properties', {})
    for field, value in arguments.items():
        if field in properties:
            expected_type = properties[field].get('type')
            # Type validation logic
```

### 2. Command Injection Prevention

```python
def sanitize_command_args(args: List[str]) -> List[str]:
    """Sanitize command arguments to prevent injection"""
    
    dangerous_chars = [';', '|', '&', '$', '`', '\n']
    
    sanitized = []
    for arg in args:
        # Check for dangerous characters
        if any(char in arg for char in dangerous_chars):
            raise ValueError(f"Dangerous characters in argument: {arg}")
        
        sanitized.append(arg)
    
    return sanitized
```

### 3. Rate Limiting

```python
from asyncio import Semaphore

class RateLimitedMCPClient(MCPClient):
    """MCP client with rate limiting"""
    
    def __init__(self, max_concurrent_requests: int = 5):
        super().__init__()
        self.semaphore = Semaphore(max_concurrent_requests)
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]):
        async with self.semaphore:
            return await super().call_tool(server_name, tool_name, arguments)
```

---

## 📊 Monitoring & Logging

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

async def call_tool_with_tracing(self, server_name: str, tool_name: str, arguments: Dict[str, Any]):
    """Call tool with OpenTelemetry tracing"""
    
    with tracer.start_as_current_span("mcp.call_tool") as span:
        span.set_attribute("mcp.server", server_name)
        span.set_attribute("mcp.tool", tool_name)
        span.set_attribute("mcp.arguments", str(arguments))
        
        try:
            result = await self.call_tool(server_name, tool_name, arguments)
            span.set_status(Status(StatusCode.OK))
            return result
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
```

---

## 🎯 Integration Roadmap

### Week 1: Foundation
- ✅ Implement base MCP client
- ✅ Add STDIO transport support
- ✅ Create server registration system

### Week 2: Tool Integration
- ✅ Integrate nmap-mcp
- ✅ Integrate metasploit-mcp
- ✅ Integrate sqlmap-mcp
- ✅ Add nuclei-mcp

### Week 3: Advanced Features
- ✅ Add SSE transport support
- ✅ Implement caching layer
- ✅ Add retry logic
- ✅ Create custom MCP servers

### Week 4: Production Ready
- ✅ Add comprehensive error handling
- ✅ Implement monitoring
- ✅ Add security controls
- ✅ Write documentation

---

## 🔗 Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [HexStrike AI MCP Implementation](https://github.com/hexstrike-ai)
- [PentestAgent MCP Servers](https://github.com/pentestagent)

---

**Implementation Priority**: HIGH
**Estimated Time**: 4 weeks
**Dependencies**: asyncio, aiohttp, json-rpc
