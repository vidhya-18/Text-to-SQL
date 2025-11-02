#!/usr/bin/env python3
"""
Simple MCP Server for SQL CRUD Assistant
Standalone implementation without FastMCP to avoid asyncio conflicts
"""

import json
import sys
from database import DatabaseManager
from llm_client import LLMClient

class SimpleMCPServer:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.llm_client = LLMClient()
    
    def handle_request(self, request):
        """Handle MCP request"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "tools/list":
                return {
                    "tools": [
                        {
                            "name": "get_database_schema",
                            "description": "Get all tables and their schemas from the database"
                        },
                        {
                            "name": "generate_sql_from_natural_language", 
                            "description": "Convert natural language to SQL query",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string"},
                                    "schema_context": {"type": "string"}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "execute_sql_query",
                            "description": "Execute SQL query on the database",
                            "inputSchema": {
                                "type": "object", 
                                "properties": {
                                    "sql": {"type": "string"}
                                },
                                "required": ["sql"]
                            }
                        }
                    ]
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "get_database_schema":
                    return self.get_database_schema()
                elif tool_name == "generate_sql_from_natural_language":
                    return self.generate_sql(arguments)
                elif tool_name == "execute_sql_query":
                    return self.execute_sql(arguments)
                else:
                    return {"error": f"Unknown tool: {tool_name}"}
            
            else:
                return {"error": f"Unknown method: {method}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def get_database_schema(self):
        """Get database schema"""
        try:
            tables_result = self.db_manager.get_all_tables()
            if not tables_result["success"]:
                return {"error": "Failed to get tables"}
            
            schema_info = {}
            if not tables_result["data"].empty:
                for _, row in tables_result["data"].iterrows():
                    table_name = row["table_name"]
                    schema_result = self.db_manager.get_table_schema(table_name)
                    if schema_result["success"]:
                        schema_info[table_name] = schema_result["data"].to_dict('records')
            
            return {"success": True, "schema": schema_info}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_sql(self, arguments):
        """Generate SQL from natural language"""
        try:
            query = arguments.get("query", "")
            schema_context = arguments.get("schema_context", "")
            
            # Get current schema for context
            schema_result = self.get_database_schema()
            if schema_result.get("success"):
                full_context = f"{schema_result['schema']}\n{schema_context}"
            else:
                full_context = schema_context
            
            result = self.llm_client.generate_sql(query, full_context)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_sql(self, arguments):
        """Execute SQL query"""
        try:
            sql = arguments.get("sql", "")
            result = self.db_manager.execute_query(sql)
            
            # Convert DataFrame to dict for JSON serialization
            if result.get("success") and "data" in result:
                result["data"] = result["data"].to_dict('records')
            
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run(self):
        """Run the MCP server"""
        print("🚀 Simple MCP Server started", file=sys.stderr)
        print("📡 Listening on stdin/stdout", file=sys.stderr)
        
        try:
            for line in sys.stdin:
                if line.strip():
                    try:
                        request = json.loads(line.strip())
                        response = self.handle_request(request)
                        print(json.dumps(response))
                        sys.stdout.flush()
                    except json.JSONDecodeError:
                        error_response = {"error": "Invalid JSON"}
                        print(json.dumps(error_response))
                        sys.stdout.flush()
        except KeyboardInterrupt:
            print("👋 Server stopped", file=sys.stderr)

if __name__ == "__main__":
    server = SimpleMCPServer()
    server.run()