#!/usr/bin/env python3
"""
Simple MCP Client for VSCode
Communicates with our MCP server for testing
"""

import json
import subprocess
import sys
from typing import Dict, Any

class VSCodeMCPClient:
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.server_process = None
    
    def start_server(self):
        """Start the MCP server process"""
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, self.server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd="c:\\llm_sql_crud_2"
            )
            print("✅ MCP Server started")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send request to MCP server"""
        if not self.server_process:
            return {"error": "Server not started"}
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        try:
            # Send request
            request_json = json.dumps(request) + "\n"
            self.server_process.stdin.write(request_json)
            self.server_process.stdin.flush()
            
            # Read response
            response_line = self.server_process.stdout.readline()
            if response_line:
                return json.loads(response_line.strip())
            else:
                return {"error": "No response from server"}
                
        except Exception as e:
            return {"error": f"Communication error: {e}"}
    
    def list_tools(self):
        """List available MCP tools"""
        return self.send_request("tools/list")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None):
        """Call a specific MCP tool"""
        params = {
            "name": tool_name,
            "arguments": arguments or {}
        }
        return self.send_request("tools/call", params)
    
    def get_database_schema(self):
        """Get database schema"""
        return self.call_tool("get_database_schema")
    
    def generate_sql(self, query: str, schema_context: str = ""):
        """Generate SQL from natural language"""
        return self.call_tool("generate_sql_from_natural_language", {
            "query": query,
            "schema_context": schema_context
        })
    
    def execute_sql(self, sql: str):
        """Execute SQL query"""
        return self.call_tool("execute_sql_query", {"sql": sql})
    
    def stop_server(self):
        """Stop the MCP server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            print("🛑 MCP Server stopped")

def main():
    """Interactive MCP client for testing"""
    client = VSCodeMCPClient("simple_mcp_server.py")
    
    if not client.start_server():
        return
    
    try:
        print("\n🔌 MCP Client Started - Type 'help' for commands")
        
        while True:
            command = input("\n> ").strip().lower()
            
            if command == "help":
                print("""
Available commands:
  schema     - Get database schema
  sql <query> - Generate SQL from natural language
  exec <sql>  - Execute SQL query
  tools      - List available tools
  quit       - Exit client
                """)
            
            elif command == "schema":
                result = client.get_database_schema()
                print(json.dumps(result, indent=2))
            
            elif command.startswith("sql "):
                query = command[4:]
                result = client.generate_sql(query)
                print(json.dumps(result, indent=2))
            
            elif command.startswith("exec "):
                sql = command[5:]
                result = client.execute_sql(sql)
                print(json.dumps(result, indent=2))
            
            elif command == "tools":
                result = client.list_tools()
                print(json.dumps(result, indent=2))
            
            elif command in ["quit", "exit"]:
                break
            
            else:
                print("Unknown command. Type 'help' for available commands.")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    
    finally:
        client.stop_server()

if __name__ == "__main__":
    main()