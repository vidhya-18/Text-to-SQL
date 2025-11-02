from fastmcp import FastMCP
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from database import DatabaseManager
from llm_client import LLMClient

class QueryRequest(BaseModel):
    query: str
    schema_context: Optional[str] = ""

class SQLExecuteRequest(BaseModel):
    sql: str

mcp = FastMCP("SQL CRUD Assistant")
db_manager = DatabaseManager()
llm_client = LLMClient()

@mcp.tool()
def get_database_schema() -> Dict[str, Any]:
    """Get all tables and their schemas from the database"""
    try:
        tables_result = db_manager.get_all_tables()
        if not tables_result["success"]:
            return {"error": "Failed to get tables"}
        
        schema_info = {}
        if not tables_result["data"].empty:
            for _, row in tables_result["data"].iterrows():
                table_name = row["table_name"]
                schema_result = db_manager.get_table_schema(table_name)
                if schema_result["success"]:
                    schema_info[table_name] = schema_result["data"].to_dict('records')
        
        return {"success": True, "schema": schema_info}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def generate_sql_from_natural_language(request: QueryRequest) -> Dict[str, Any]:
    """Convert natural language to SQL query"""
    try:
        # Get current schema for context
        schema_result = get_database_schema()
        schema_context = ""
        
        if schema_result.get("success"):
            schema_context = str(schema_result["schema"])
        
        # Combine with provided context
        full_context = f"{schema_context}\n{request.schema_context}"
        
        result = llm_client.generate_sql(request.query, full_context)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def execute_sql_query(request: SQLExecuteRequest) -> Dict[str, Any]:
    """Execute SQL query on the database"""
    try:
        result = db_manager.execute_query(request.sql)
        
        # Convert DataFrame to dict for JSON serialization
        if result.get("success") and "data" in result:
            result["data"] = result["data"].to_dict('records')
        
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_table_info(table_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific table"""
    try:
        result = db_manager.get_table_schema(table_name)
        if result["success"]:
            result["data"] = result["data"].to_dict('records')
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def test_database_connection() -> Dict[str, Any]:
    """Test the database connection"""
    try:
        is_connected = db_manager.test_connection()
        return {"success": True, "connected": is_connected}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    mcp.run_sync(transport="stdio")

if __name__ == "__main__":
    main()