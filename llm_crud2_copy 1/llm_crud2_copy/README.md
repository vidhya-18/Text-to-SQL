# 🗃️ LLM SQL CRUD Assistant

> **Transform natural language into powerful SQL operations with AI assistance**

A comprehensive application that bridges the gap between human language and database operations. Using state-of-the-art Large Language Models through OpenRouter API, this system converts natural language queries into executable SQL statements, providing both an intuitive web interface and seamless IDE integration.

## ✨ Key Features

🤖 **AI-Powered SQL Generation** - Convert plain English to SQL using advanced LLMs  
📊 **Complete CRUD Operations** - Full Create, Read, Update, Delete functionality  
🔄 **Dynamic Schema Management** - Real-time table and column creation  
🌐 **Multi-Interface Support** - Web UI (Streamlit) + IDE integration (MCP)  
🧠 **Context-Aware Processing** - LLM receives current database structure  
📈 **Query Analytics** - Complete history tracking and performance monitoring  
🛡️ **Enterprise Security** - SQL injection prevention and parameterized queries  
⚡ **Real-Time Operations** - Instant query execution and results display

## 🎯 What Makes This Special

- **Zero SQL Knowledge Required**: Ask in plain English, get perfect SQL
- **Schema Intelligence**: AI understands your database structure automatically
- **IDE Integration**: Works directly in Cursor/VSCode through MCP protocol
- **Production Ready**: Built with security, performance, and reliability in mind

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- OpenRouter API key

## 🛠️ Installation

1. **Clone/Create the project directory**:
   ```bash
   cd c:\llm_sql_crud_2
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your credentials:
     ```
     OPENROUTER_API_KEY=your_openrouter_api_key_here
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=llm_crud_db
     DB_USER=postgres
     DB_PASSWORD=your_password_here
     OPENROUTER_MODEL=openai/gpt-4-turbo-preview
     ```

4. **Setup PostgreSQL database**:
   ```bash
   python setup_database.py
   ```

## 🚀 Usage

### Streamlit Web Interface

```bash
streamlit run streamlit_app.py
```

Access the application at `http://localhost:8501`

### MCP Server (for Cursor/VSCode)

```bash
python run_mcp_server.py
```

## 💬 Example Natural Language Queries

- **Data Retrieval**:
  - "Show all users"
  - "Get products with price greater than 100"
  - "Find users older than 25"

- **Data Modification**:
  - "Delete the first row from users"
  - "Update the price of laptop to 899.99"
  - "Insert a new user named Alice with email alice@example.com"

- **Schema Operations**:
  - "Create a table called orders with id, customer_name, and total"
  - "Add a column called phone to users table"
  - "Drop the products table"

## 🏗️ Project Structure

```
c:\llm_sql_crud_2\
├── streamlit_app.py      # Main Streamlit application
├── database.py           # PostgreSQL database manager
├── llm_client.py         # OpenRouter LLM client
├── mcp_server.py         # FastMCP server implementation
├── config.py             # Configuration management
├── setup_database.py     # Database initialization
├── run_mcp_server.py     # MCP server runner
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `OPENROUTER_MODEL`: LLM model to use (default: openai/gpt-4-turbo-preview)
- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: llm_crud_db)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password

### MCP Integration with Cursor/VSCode

1. Start the MCP server:
   ```bash
   python run_mcp_server.py
   ```

2. Configure your IDE to use the MCP server (refer to your IDE's MCP documentation)

## 🛡️ Security Features

- SQL injection prevention through parameterized queries
- Input validation and sanitization
- Error handling without exposing sensitive information
- Environment variable management for credentials

## 🔍 Available MCP Tools

- `get_database_schema()`: Retrieve complete database schema
- `generate_sql_from_natural_language()`: Convert natural language to SQL
- `execute_sql_query()`: Execute SQL queries safely
- `get_table_info()`: Get detailed table information
- `test_database_connection()`: Test database connectivity

## 📊 Supported SQL Operations

- **DDL**: CREATE TABLE, ALTER TABLE, DROP TABLE
- **DML**: INSERT, UPDATE, DELETE
- **DQL**: SELECT with various clauses (WHERE, ORDER BY, GROUP BY, etc.)
- **PostgreSQL-specific**: SERIAL, TIMESTAMP, BOOLEAN types

## 🐛 Troubleshooting

1. **Database Connection Issues**:
   - Verify PostgreSQL is running
   - Check connection credentials in `.env`
   - Ensure database exists

2. **LLM API Issues**:
   - Verify OpenRouter API key
   - Check internet connectivity
   - Monitor API usage limits

3. **MCP Server Issues**:
   - Ensure all dependencies are installed
   - Check Python path configuration
   - Verify IDE MCP configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📚 Documentation

- **[Complete Documentation](DOCUMENTATION.md)** - Comprehensive guide covering all aspects
- **[MCP Integration Guide](MCP_INTEGRATION_GUIDE.md)** - Detailed MCP setup and usage
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Quick Start](#-usage)** - Get started in minutes

## 🤝 Contributing

We welcome contributions! Please see our [Development Guide](DOCUMENTATION.md#development) for details on:
- Setting up development environment
- Code style guidelines
- Testing procedures
- Submitting pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support & Community

- 📖 **Documentation**: Check our comprehensive guides above
- 🐛 **Issues**: Report bugs and request features
- 💬 **Discussions**: Join community discussions
- 📧 **Contact**: Reach out for enterprise support

## 🌟 Acknowledgments

- **OpenRouter** for providing access to state-of-the-art LLMs
- **PostgreSQL** for robust database foundation
- **Streamlit** for beautiful web interface framework
- **FastMCP** for Model Context Protocol implementation

---

**Ready to transform your database interactions? Let's get started! 🚀**