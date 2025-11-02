import streamlit as st
import pandas as pd
from database import DatabaseManager
from llm_client import LLMClient
import sqlparse
from typing import Dict, Any

# Page config
st.set_page_config(
    page_title="LLM SQL CRUD Assistant",
    page_icon="🗃️",
    layout="wide"
)

# Initialize session state
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager()
if 'llm_client' not in st.session_state:
    st.session_state.llm_client = LLMClient()
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

def format_sql(sql: str) -> str:
    """Format SQL query for better readability"""
    try:
        return sqlparse.format(sql, reindent=True, keyword_case='upper')
    except:
        return sql

def execute_natural_language_query(user_input: str):
    """Process natural language query and execute SQL"""
    with st.spinner("🤖 Converting to SQL..."):
        # Get current schema for context
        schema_info = get_schema_context()
        
        # Generate SQL
        llm_result = st.session_state.llm_client.generate_sql(user_input, schema_info)
        
        if not llm_result["success"]:
            st.error(f"❌ Failed to generate SQL: {llm_result['error']}")
            return
        
        sql_query = llm_result["sql"]
        
        # Display generated SQL
        st.code(format_sql(sql_query), language="sql")
        
        # Execute SQL
        with st.spinner("⚡ Executing query..."):
            result = st.session_state.db_manager.execute_query(sql_query)
            
            if result["success"]:
                st.success(f"✅ Query executed successfully! Rows affected: {result.get('rows_affected', 0)}")
                
                # Display results if it's a SELECT query
                if "data" in result and not result["data"].empty:
                    st.subheader("📊 Query Results")
                    st.dataframe(result["data"], use_container_width=True)
                
                # Add to history
                st.session_state.query_history.append({
                    "natural_language": user_input,
                    "sql": sql_query,
                    "success": True,
                    "rows_affected": result.get('rows_affected', 0)
                })
            else:
                st.error(f"❌ Query failed: {result['error']}")
                st.session_state.query_history.append({
                    "natural_language": user_input,
                    "sql": sql_query,
                    "success": False,
                    "error": result['error']
                })

def get_schema_context() -> str:
    """Get database schema information for LLM context"""
    try:
        tables_result = st.session_state.db_manager.get_all_tables()
        if not tables_result["success"] or tables_result["data"].empty:
            return "No tables found in database."
        
        schema_info = "Database Schema:\n"
        for _, row in tables_result["data"].iterrows():
            table_name = row["table_name"]
            schema_result = st.session_state.db_manager.get_table_schema(table_name)
            if schema_result["success"] and not schema_result["data"].empty:
                schema_info += f"\nTable: {table_name}\n"
                for _, col_row in schema_result["data"].iterrows():
                    schema_info += f"  - {col_row['column_name']}: {col_row['data_type']}\n"
        
        return schema_info
    except:
        return "Schema information unavailable."

# Main UI
st.title("🗃️ LLM SQL CRUD Assistant")
st.markdown("Convert natural language to SQL queries and execute them on PostgreSQL")

# Sidebar
with st.sidebar:
    st.header("🔧 Database Connection")
    
    # Test connection
    if st.button("Test Connection"):
        if st.session_state.db_manager.test_connection():
            st.success("✅ Connected to database")
        else:
            st.error("❌ Failed to connect to database")
    
    st.header("📋 Database Schema")
    
    # Show tables
    tables_result = st.session_state.db_manager.get_all_tables()
    if tables_result["success"] and not tables_result["data"].empty:
        for _, row in tables_result["data"].iterrows():
            table_name = row["table_name"]
            with st.expander(f"📊 {table_name}"):
                schema_result = st.session_state.db_manager.get_table_schema(table_name)
                if schema_result["success"]:
                    st.dataframe(schema_result["data"], use_container_width=True)
    else:
        st.info("No tables found")

# Main content
tab1, tab2, tab3 = st.tabs(["💬 Natural Language Query", "⚡ Direct SQL", "📈 Query History"])

with tab1:
    st.header("💬 Ask in Natural Language")
    st.markdown("Examples: *'Show all users'*, *'Delete the first row from products'*, *'Create a table called orders with id and customer_name'*")
    
    user_input = st.text_area(
        "Enter your request:",
        placeholder="e.g., Show me all records from users table",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🚀 Execute", type="primary"):
            if user_input.strip():
                execute_natural_language_query(user_input)
            else:
                st.warning("Please enter a query")

with tab2:
    st.header("⚡ Direct SQL Execution")
    
    sql_input = st.text_area(
        "Enter SQL query:",
        placeholder="SELECT * FROM your_table;",
        height=150
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Execute SQL", type="primary"):
            if sql_input.strip():
                with st.spinner("Executing..."):
                    result = st.session_state.db_manager.execute_query(sql_input)
                    
                    if result["success"]:
                        st.success(f"✅ Query executed! Rows affected: {result.get('rows_affected', 0)}")
                        if "data" in result and not result["data"].empty:
                            st.dataframe(result["data"], use_container_width=True)
                    else:
                        st.error(f"❌ Error: {result['error']}")
            else:
                st.warning("Please enter a SQL query")

with tab3:
    st.header("📈 Query History")
    
    if st.session_state.query_history:
        for i, query in enumerate(reversed(st.session_state.query_history)):
            with st.expander(f"Query {len(st.session_state.query_history) - i}: {query['natural_language'][:50]}..."):
                st.write("**Natural Language:**", query['natural_language'])
                st.code(format_sql(query['sql']), language="sql")
                if query['success']:
                    st.success(f"✅ Success - Rows affected: {query['rows_affected']}")
                else:
                    st.error(f"❌ Error: {query.get('error', 'Unknown error')}")
    else:
        st.info("No queries executed yet")

# Footer
st.markdown("---")
st.markdown("🤖 Powered by OpenRouter LLM | 🗃️ PostgreSQL Database | ⚡ Streamlit Interface")