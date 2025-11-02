# Model Context Protocol (MCP) Integration Guide

## 🔌 What is Model Context Protocol?

Model Context Protocol (MCP) is an open standard that enables AI assistants to securely connect to external data sources and tools. It provides a standardized way for AI models to:

- **Discover Tools**: Find available functions and their capabilities
- **Execute Operations**: Safely run tools with proper parameters
- **Access Real-time Data**: Get live information from databases, APIs, etc.
- **Maintain Security**: Control access and permissions

## 🏗️ MCP Architecture in Our Project

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cursor/VSCode │    │   MCP Server    │    │   PostgreSQL    │
│   (AI Client)   │◄──►│  (Our Tools)    │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    JSON-RPC over              Tool                 SQL Queries
    stdin/stdout            Execution              & Results
```

## 🛠️ Available MCP Tools

### 1. Database Schema Tool
**Tool Name**: `get_database_schema`

**Purpose**: Retrieves complete database structure including all tables and their columns.

**Usage Example**:
```
User: "What tables are in my database?"
AI: I'll check your database schema for you.
[Calls get_database_schema()]
AI: Your database contains these tables:
- users (id, name, email, age, created_at)
- products (id, name, price, category, in_stock, created_at)
```

**Response Format**:
```json
{
  "success": true,
  "schema": {
    "users": [
      {
        "column_name": "id",
        "data_type": "integer",
        "is_nullable": "NO",
        "column_default": "nextval('users_id_seq'::regclass)"
      },
      {
        "column_name": "name",
        "data_type": "character varying",
        "is_nullable": "NO",
        "column_default": null
      }
    ]
  }
}
```

### 2. Natural Language to SQL Tool
**Tool Name**: `generate_sql_from_natural_language`

**Purpose**: Converts human language queries into valid PostgreSQL SQL statements.

**Parameters**:
- `query` (required): Natural language description
- `schema_context` (optional): Additional context about the database

**Usage Example**:
```
User: "Find all users who are older than 25"
AI: I'll convert that to SQL for you.
[Calls generate_sql_from_natural_language(query="Find all users who are older than 25")]
AI: Here's the SQL query: SELECT * FROM users WHERE age > 25;
```

**Response Format**:
```json
{
  "success": true,
  "sql": "SELECT * FROM users WHERE age > 25;",
  "explanation": "Generated SQL for: Find all users who are older than 25"
}
```

### 3. SQL Execution Tool
**Tool Name**: `execute_sql_query`

**Purpose**: Safely executes SQL queries on the PostgreSQL database.

**Parameters**:
- `sql` (required): Valid SQL query to execute

**Usage Example**:
```
User: "Run that query and show me the results"
AI: I'll execute the query for you.
[Calls execute_sql_query(sql="SELECT * FROM users WHERE age > 25;")]
AI: Found 2 users older than 25:
- John Doe (age 30)
- Bob Johnson (age 35)
```

**Response Format**:
```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "age": 35}
  ],
  "rows_affected": 2
}
```

### 4. Table Information Tool
**Tool Name**: `get_table_info`

**Purpose**: Gets detailed information about a specific table.

**Parameters**:
- `table_name` (required): Name of the table to inspect

**Usage Example**:
```
User: "Tell me about the users table structure"
AI: Let me get the details of the users table.
[Calls get_table_info(table_name="users")]
AI: The users table has these columns:
- id: Primary key (integer, auto-increment)
- name: User's full name (varchar, required)
- email: Email address (varchar, unique, required)
- age: User's age (integer, optional)
- created_at: Registration timestamp (timestamp, default: now)
```

### 5. Connection Test Tool
**Tool Name**: `test_database_connection`

**Purpose**: Verifies that the database connection is working properly.

**Usage Example**:
```
User: "Is the database connection working?"
AI: Let me check the database connection.
[Calls test_database_connection()]
AI: ✅ Database connection is working properly!
```

## 🔧 Setting Up MCP Integration

### For Cursor IDE

1. **Open Cursor Settings**
   - Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (Mac)
   - Or go to File → Preferences → Settings

2. **Find MCP Settings**
   - Search for "MCP" or "Model Context Protocol"
   - Look for "MCP Servers" configuration

3. **Add Our Server**
   ```json
   {
     "name": "SQL CRUD Assistant",
     "command": "python",
     "args": ["simple_mcp_server.py"],
     "cwd": "c:\\llm_sql_crud_2",
     "env": {
       "PYTHONPATH": "c:\\llm_sql_crud_2"
     }
   }
   ```

4. **Restart Cursor**
   - Close and reopen Cursor to load the MCP server
   - The server will start automatically when needed

### For VSCode

1. **Install MCP Extension**
   - Search for "Model Context Protocol" in extensions
   - Install the official MCP extension

2. **Configure Settings**
   - Open settings.json (Ctrl+Shift+P → "Open Settings JSON")
   - Add MCP server configuration:
   ```json
   {
     "mcp.servers": {
       "sql-crud": {
         "command": "python",
         "args": ["simple_mcp_server.py"],
         "cwd": "c:\\llm_sql_crud_2"
       }
     }
   }
   ```

3. **Restart VSCode**

### Manual Server Start (For Testing)

```bash
# Start the MCP server manually
cd c:\llm_sql_crud_2
python simple_mcp_server.py

# Or use the launcher
python run_mcp_server.py
```

## 💬 Using MCP Tools in Your IDE

### Basic Queries

**Schema Exploration**:
```
You: "What's in my database?"
AI: [Uses get_database_schema()] 
    "Your database has 2 tables: users and products..."
```

**Data Queries**:
```
You: "Show me all products under $50"
AI: [Uses generate_sql_from_natural_language() then execute_sql_query()]
    "Here are the products under $50: [results table]"
```

**Database Operations**:
```
You: "Create a new table for orders"
AI: [Uses generate_sql_from_natural_language() then execute_sql_query()]
    "I've created the orders table with columns: id, customer_name, total, created_at"
```

### Advanced Workflows

**Data Analysis**:
```
You: "Analyze user registration trends"
AI: [Multiple tool calls]
    1. Gets schema to understand user table
    2. Generates SQL for date-based analysis
    3. Executes query and analyzes results
    4. Provides insights and visualizations
```

**Database Maintenance**:
```
You: "Help me optimize my database"
AI: [Comprehensive analysis]
    1. Examines all table structures
    2. Identifies missing indexes
    3. Suggests performance improvements
    4. Generates optimization SQL
```

## 🔍 MCP Protocol Details

### Communication Format

MCP uses JSON-RPC 2.0 over stdin/stdout:

**Tool Discovery Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Tool Discovery Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_database_schema",
        "description": "Get all tables and their schemas",
        "inputSchema": {
          "type": "object",
          "properties": {}
        }
      }
    ]
  }
}
```

**Tool Execution Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "generate_sql_from_natural_language",
    "arguments": {
      "query": "show all users"
    }
  }
}
```

### Error Handling

**Error Response Format**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -1,
    "message": "Database connection failed",
    "data": {
      "details": "Connection timeout after 10 seconds"
    }
  }
}
```

## 🛡️ Security Considerations

### Access Control
- MCP server only accepts connections from configured IDEs
- Database credentials are stored in environment variables
- SQL queries are parameterized to prevent injection

### Data Privacy
- No data is sent to external services except OpenRouter for SQL generation
- Database results stay within your local environment
- MCP communication is local (stdin/stdout)

### Best Practices
1. **Environment Isolation**: Use virtual environments
2. **Credential Management**: Never commit `.env` files
3. **Query Validation**: Review generated SQL before execution
4. **Access Logging**: Monitor MCP tool usage

## 🐛 Troubleshooting MCP Integration

### Common Issues

**1. Server Not Starting**
```bash
# Check if server starts manually
python simple_mcp_server.py

# Check for error messages
python run_mcp_server.py
```

**2. IDE Not Finding Server**
- Verify MCP configuration in IDE settings
- Check file paths are absolute
- Restart IDE after configuration changes

**3. Tool Calls Failing**
- Check database connection: `python test_system.py`
- Verify OpenRouter API key in `.env`
- Review server logs for error messages

**4. Permission Issues**
- Ensure Python executable is in PATH
- Check file permissions on server scripts
- Verify virtual environment activation

### Debug Mode

Enable detailed logging:
```python
# Add to simple_mcp_server.py
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)
```

### Testing MCP Tools

**Manual Tool Testing**:
```bash
# Test individual tools
python -c "
from simple_mcp_server import SimpleMCPServer
server = SimpleMCPServer()
result = server.get_database_schema()
print(result)
"
```

## 📈 Performance Optimization

### Server Performance
- Use connection pooling for database
- Cache schema information
- Implement query result caching

### IDE Integration
- Configure appropriate timeout values
- Use async tool calls where possible
- Monitor memory usage

## 🔮 Future Enhancements

### Planned Features
1. **Query Caching**: Cache frequent SQL generations
2. **Schema Versioning**: Track database schema changes
3. **Query Analytics**: Performance monitoring and optimization
4. **Multi-Database Support**: Connect to multiple databases
5. **Advanced Security**: Role-based access control

### Extension Points
- Custom tool development
- Additional database backends
- Integration with other AI models
- Web-based MCP client

---

This MCP integration transforms your IDE into a powerful database management interface, allowing natural language interaction with your PostgreSQL database through AI assistance. The tools provide comprehensive database operations while maintaining security and performance.