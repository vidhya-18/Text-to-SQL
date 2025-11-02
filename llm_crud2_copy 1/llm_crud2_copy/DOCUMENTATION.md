# LLM SQL CRUD Assistant - Complete Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [File Structure & Details](#file-structure--details)
4. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
5. [Installation & Setup](#installation--setup)
6. [Usage Guide](#usage-guide)
7. [API Reference](#api-reference)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Development](#development)

## 🎯 Project Overview

The LLM SQL CRUD Assistant is a comprehensive application that bridges natural language and SQL database operations. It leverages Large Language Models (LLMs) through the OpenRouter API to convert human language queries into executable SQL statements, providing both a web interface and IDE integration.

### Key Features

- **Natural Language Processing**: Converts plain English to SQL using state-of-the-art LLMs
- **Full CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Dynamic Schema Management**: Real-time table and column creation
- **Multi-Interface Support**: Web UI (Streamlit) and IDE integration (MCP)
- **Real-time Schema Awareness**: LLM receives current database structure for context
- **Query History & Tracking**: Complete audit trail of all operations
- **Security**: SQL injection prevention and parameterized queries

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │    │   LLM Client    │    │   Database      │
│ (Natural Lang.) │───▶│  (OpenRouter)   │───▶│  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Streamlit UI    │    │ SQL Generation  │    │ Query Execution │
│ MCP Server      │    │ & Validation    │    │ & Results       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

1. **Input**: User provides natural language query
2. **Context**: System retrieves current database schema
3. **Generation**: LLM converts natural language + schema to SQL
4. **Validation**: SQL is cleaned and validated
5. **Execution**: Query is executed on PostgreSQL database
6. **Response**: Results are formatted and returned to user

## 📁 File Structure & Details

### Core Application Files

#### `config.py`
**Purpose**: Centralized configuration management
```python
# Manages environment variables and database connections
class Config:
    - OPENROUTER_API_KEY: API key for LLM access
    - OPENROUTER_MODEL: Selected LLM model
    - DB_* variables: PostgreSQL connection parameters
    - database_url property: Formatted connection string
```

#### `database.py`
**Purpose**: PostgreSQL database interface and operations
```python
class DatabaseManager:
    - connect(): Establishes database connection
    - execute_query(): Executes SQL with error handling
    - get_table_schema(): Retrieves table structure
    - get_all_tables(): Lists all database tables
    - test_connection(): Validates database connectivity
```

**Key Features**:
- Automatic connection management
- Parameterized queries for security
- DataFrame integration for results
- Comprehensive error handling

#### `llm_client.py`
**Purpose**: OpenRouter API integration and SQL generation
```python
class LLMClient:
    - generate_sql(): Converts natural language to SQL
    - explain_query(): Provides SQL explanations
    - Response cleaning and validation
    - Fallback logic for failed generations
```

**Advanced Features**:
- HTML tag removal for problematic models
- Multi-line response handling
- Context-aware SQL generation
- Fallback patterns for common queries

#### `streamlit_app.py`
**Purpose**: Web-based user interface
```python
Features:
    - Natural language query interface
    - Direct SQL execution panel
    - Real-time schema visualization
    - Query history tracking
    - Interactive results display
```

**UI Components**:
- **Tab 1**: Natural Language Query - Main interaction interface
- **Tab 2**: Direct SQL - For advanced users
- **Tab 3**: Query History - Audit trail and debugging
- **Sidebar**: Database schema browser and connection status

### MCP Integration Files

#### `mcp_server.py` (FastMCP Implementation)
**Purpose**: Original FastMCP server implementation
```python
Tools Provided:
    - get_database_schema(): Complete schema retrieval
    - generate_sql_from_natural_language(): NL to SQL conversion
    - execute_sql_query(): Safe SQL execution
    - get_table_info(): Detailed table information
    - test_database_connection(): Connection validation
```

#### `simple_mcp_server.py` (Standalone Implementation)
**Purpose**: Asyncio-conflict-free MCP server
```python
class SimpleMCPServer:
    - handle_request(): Process MCP protocol requests
    - JSON-based communication over stdin/stdout
    - Synchronous operation to avoid event loop conflicts
    - Same tool set as FastMCP version
```

### Setup & Utility Files

#### `setup_database.py`
**Purpose**: Database initialization and sample data creation
```python
Functions:
    - create_database(): Creates PostgreSQL database if not exists
    - create_sample_tables(): Sets up users and products tables
    - Sample data insertion for testing
```

#### `test_system.py`
**Purpose**: Comprehensive system testing and validation
```python
Test Categories:
    - Configuration validation
    - Database connectivity
    - LLM client functionality
    - Full integration testing
    - Detailed error reporting
```

#### `run_mcp_server.py`
**Purpose**: MCP server launcher with error handling
```python
Features:
    - Asyncio conflict detection
    - Multiple startup methods
    - Comprehensive error reporting
    - User-friendly status messages
```

### Configuration Files

#### `.env` / `.env.example`
**Purpose**: Environment variable management
```bash
OPENROUTER_API_KEY=your_api_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=llm_crud_db
DB_USER=postgres
DB_PASSWORD=your_password
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```

#### `requirements.txt`
**Purpose**: Python dependency specification
```
streamlit>=1.29.0      # Web interface framework
psycopg2-binary>=2.9.9 # PostgreSQL adapter
openai>=1.3.8          # OpenRouter API client
python-dotenv>=1.0.0   # Environment variable loading
sqlparse>=0.4.4        # SQL parsing and formatting
pandas>=2.1.4          # Data manipulation
fastmcp>=0.2.0         # Model Context Protocol
pydantic>=2.5.3        # Data validation
```

## 🔌 Model Context Protocol (MCP)

### What is MCP?

Model Context Protocol is a standardized way for AI assistants to interact with external tools and data sources. It enables:

- **Tool Discovery**: AI can discover available functions
- **Structured Communication**: Standardized request/response format
- **Real-time Integration**: Live data access during conversations
- **Security**: Controlled access to external resources

### MCP in This Project

Our implementation provides these MCP tools:

#### 1. `get_database_schema()`
```json
{
  "name": "get_database_schema",
  "description": "Retrieve complete database schema including all tables and columns",
  "returns": {
    "success": true,
    "schema": {
      "table_name": [
        {
          "column_name": "id",
          "data_type": "integer",
          "is_nullable": "NO"
        }
      ]
    }
  }
}
```

#### 2. `generate_sql_from_natural_language(query, schema_context?)`
```json
{
  "name": "generate_sql_from_natural_language",
  "description": "Convert natural language to SQL with schema awareness",
  "parameters": {
    "query": "show all users older than 25",
    "schema_context": "optional additional context"
  },
  "returns": {
    "success": true,
    "sql": "SELECT * FROM users WHERE age > 25;",
    "explanation": "Generated SQL for: show all users older than 25"
  }
}
```

#### 3. `execute_sql_query(sql)`
```json
{
  "name": "execute_sql_query",
  "description": "Execute SQL query safely on the database",
  "parameters": {
    "sql": "SELECT * FROM users LIMIT 5;"
  },
  "returns": {
    "success": true,
    "data": [
      {"id": 1, "name": "John", "email": "john@example.com"}
    ],
    "rows_affected": 5
  }
}
```

### MCP Integration with IDEs

#### Cursor Configuration
1. Open Cursor Settings (Ctrl+,)
2. Search for "MCP" or "Model Context Protocol"
3. Add new server:
   ```json
   {
     "name": "SQL CRUD Assistant",
     "command": "python",
     "args": ["c:\\llm_sql_crud_2\\simple_mcp_server.py"],
     "cwd": "c:\\llm_sql_crud_2"
   }
   ```

#### VSCode Configuration
Add to your VSCode settings.json:
```json
{
  "mcp.servers": {
    "sql-crud": {
      "command": "python",
      "args": ["c:\\llm_sql_crud_2\\simple_mcp_server.py"],
      "cwd": "c:\\llm_sql_crud_2"
    }
  }
}
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- OpenRouter API account

### Step-by-Step Installation

1. **Clone/Create Project Directory**
   ```bash
   mkdir c:\llm_sql_crud_2
   cd c:\llm_sql_crud_2
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   copy .env.example .env
   # Edit .env with your credentials
   ```

5. **Setup Database**
   ```bash
   python setup_database.py
   ```

6. **Test Installation**
   ```bash
   python test_system.py
   ```

### Environment Configuration

#### OpenRouter Setup
1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Create account and get API key
3. Add key to `.env` file
4. Choose model (recommended: `openai/gpt-3.5-turbo`)

#### PostgreSQL Setup
1. Install PostgreSQL
2. Create database user
3. Update `.env` with credentials
4. Run `setup_database.py`

## 📖 Usage Guide

### Web Interface Usage

#### Starting the Application
```bash
streamlit run streamlit_app.py
```

#### Natural Language Queries
- **Data Retrieval**: "Show all users", "Find products under $50"
- **Data Modification**: "Delete user with id 5", "Update price of laptop to 999"
- **Schema Operations**: "Create table orders with id and total", "Add phone column to users"

#### Advanced Features
- **Query History**: Review all executed queries
- **Schema Browser**: Explore database structure
- **Direct SQL**: Execute raw SQL for complex operations

### MCP Integration Usage

#### In Cursor/VSCode
1. Start MCP server: `python run_mcp_server.py`
2. Ask AI: "Show me the database schema"
3. Request: "Create a query to find all active users"
4. Execute: "Run this SQL query for me"

#### Available Commands
- Schema exploration
- SQL generation from natural language
- Query execution and results
- Database structure analysis

## 🔧 API Reference

### DatabaseManager Class

#### Methods

**`connect() -> bool`**
- Establishes PostgreSQL connection
- Returns: Success status
- Handles: Connection errors, credential validation

**`execute_query(query: str, params: tuple = None) -> Dict[str, Any]`**
- Executes SQL query with optional parameters
- Returns: `{"success": bool, "data": DataFrame, "rows_affected": int, "error": str}`
- Security: Uses parameterized queries

**`get_table_schema(table_name: str) -> Dict[str, Any]`**
- Retrieves table column information
- Returns: Column details including types and constraints
- Usage: Schema awareness for LLM context

**`get_all_tables() -> Dict[str, Any]`**
- Lists all tables in public schema
- Returns: Table names as DataFrame
- Usage: Database exploration

### LLMClient Class

#### Methods

**`generate_sql(user_query: str, schema_info: str = "") -> Dict[str, Any]`**
- Converts natural language to SQL
- Parameters:
  - `user_query`: Natural language input
  - `schema_info`: Database schema context
- Returns: `{"success": bool, "sql": str, "explanation": str, "error": str}`

**`explain_query(sql_query: str) -> str`**
- Provides human-readable SQL explanation
- Parameters: SQL query string
- Returns: Plain English explanation

### Response Formats

#### Success Response
```json
{
  "success": true,
  "data": [...],
  "rows_affected": 5,
  "sql": "SELECT * FROM users;",
  "explanation": "Retrieved all user records"
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Table 'nonexistent' doesn't exist",
  "sql": "SELECT * FROM nonexistent;"
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENROUTER_API_KEY` | OpenRouter API key | - | Yes |
| `OPENROUTER_MODEL` | LLM model to use | `openai/gpt-3.5-turbo` | No |
| `DB_HOST` | PostgreSQL host | `localhost` | No |
| `DB_PORT` | PostgreSQL port | `5432` | No |
| `DB_NAME` | Database name | `llm_crud_db` | No |
| `DB_USER` | Database user | `postgres` | No |
| `DB_PASSWORD` | Database password | - | Yes |

### Model Selection

#### Recommended Models
- **Production**: `openai/gpt-4-turbo-preview` (Best accuracy)
- **Development**: `openai/gpt-3.5-turbo` (Good balance)
- **Free Tier**: `mistralai/mistral-7b-instruct:free` (Limited accuracy)

#### Model Comparison
| Model | Cost | Accuracy | Speed | SQL Quality |
|-------|------|----------|-------|-------------|
| GPT-4 Turbo | High | Excellent | Medium | Excellent |
| GPT-3.5 Turbo | Medium | Very Good | Fast | Very Good |
| Mistral 7B | Free | Good | Fast | Good |

### Database Configuration

#### Connection Pool Settings
```python
# In database.py, you can modify:
connection_params = {
    'host': config.DB_HOST,
    'port': config.DB_PORT,
    'database': config.DB_NAME,
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'connect_timeout': 10,
    'application_name': 'llm_sql_crud'
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Errors
**Symptoms**: "Failed to connect to database"
**Solutions**:
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database exists
- Test with: `python -c "from database import DatabaseManager; print(DatabaseManager().test_connection())"`

#### 2. LLM API Errors
**Symptoms**: "LLM Error: API key invalid"
**Solutions**:
- Verify OpenRouter API key
- Check internet connectivity
- Monitor API usage limits
- Test with: `python -c "from llm_client import LLMClient; print(LLMClient().generate_sql('test'))"`

#### 3. MCP Server Issues
**Symptoms**: "Already running asyncio in this thread"
**Solutions**:
- Use `simple_mcp_server.py` instead of `mcp_server.py`
- Restart terminal/IDE
- Check Python environment

#### 4. Empty SQL Generation
**Symptoms**: "Can't execute an empty query"
**Solutions**:
- Switch to more reliable model (GPT-3.5-turbo)
- Check query complexity
- Verify schema context is provided

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

#### Database Optimization
- Use connection pooling for high-volume usage
- Add database indexes for frequently queried columns
- Monitor query execution times

#### LLM Optimization
- Cache frequent queries
- Use shorter, more specific prompts
- Implement query result caching

## 👨‍💻 Development

### Project Structure
```
c:\llm_sql_crud_2\
├── 📄 Core Application
│   ├── config.py           # Configuration management
│   ├── database.py         # PostgreSQL interface
│   ├── llm_client.py       # OpenRouter integration
│   └── streamlit_app.py    # Web interface
├── 🔌 MCP Integration
│   ├── mcp_server.py       # FastMCP implementation
│   ├── simple_mcp_server.py # Standalone MCP server
│   └── run_mcp_server.py   # Server launcher
├── 🛠️ Setup & Testing
│   ├── setup_database.py   # Database initialization
│   ├── test_system.py      # System tests
│   └── __main__.py         # Package entry point
├── 📋 Configuration
│   ├── requirements.txt    # Dependencies
│   ├── .env.example        # Environment template
│   └── .gitignore         # Git ignore rules
└── 📚 Documentation
    ├── README.md          # Quick start guide
    └── DOCUMENTATION.md   # This file
```

### Adding New Features

#### 1. New SQL Operations
```python
# In llm_client.py, update system prompt:
system_prompt += """
- "backup table users" → CREATE TABLE users_backup AS SELECT * FROM users;
"""
```

#### 2. New MCP Tools
```python
# In simple_mcp_server.py:
@tool
def new_tool_name(self, arguments):
    # Implementation
    return {"success": True, "result": "..."}
```

#### 3. UI Enhancements
```python
# In streamlit_app.py:
with st.expander("New Feature"):
    # New UI components
```

### Testing

#### Unit Tests
```bash
python -m pytest tests/  # If you create tests/
```

#### Integration Tests
```bash
python test_system.py
```

#### Manual Testing
```bash
# Test each component
python -c "from database import DatabaseManager; print(DatabaseManager().test_connection())"
python -c "from llm_client import LLMClient; print(LLMClient().generate_sql('show tables'))"
```

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Update documentation
5. Submit pull request

### Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings for all functions
- Keep functions focused and small
- Handle errors gracefully

---

## 📞 Support

For issues and questions:
1. Check this documentation
2. Review troubleshooting section
3. Test individual components
4. Check environment configuration
5. Verify database connectivity

**Happy Querying! 🎉**