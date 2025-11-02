#!/usr/bin/env python3
"""
System Test Script for LLM SQL CRUD Assistant
Tests all components to ensure everything works correctly
"""

import os
import sys
from database import DatabaseManager
from llm_client import LLMClient
from config import Config

def test_config():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    try:
        config = Config()
        if not config.OPENROUTER_API_KEY:
            print("⚠️ Warning: OPENROUTER_API_KEY not set")
            return False
        if not config.DB_PASSWORD:
            print("⚠️ Warning: DB_PASSWORD not set")
            return False
        print("✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_database():
    """Test database connection and operations"""
    print("🗃️ Testing database connection...")
    try:
        db = DatabaseManager()
        if not db.test_connection():
            print("❌ Database connection failed")
            return False
        
        print("✅ Database connection successful")
        
        # Test basic query
        result = db.execute_query("SELECT 1 as test")
        if not result["success"]:
            print("❌ Basic query failed")
            return False
        
        print("✅ Database queries working")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_llm_client():
    """Test LLM client"""
    print("🤖 Testing LLM client...")
    try:
        llm = LLMClient()
        result = llm.generate_sql("show all tables", "")
        if not result["success"]:
            print(f"❌ LLM client error: {result.get('error', 'Unknown error')}")
            return False
        
        print("✅ LLM client working")
        print(f"   Generated SQL: {result['sql']}")
        return True
    except Exception as e:
        print(f"❌ LLM client error: {e}")
        return False

def test_integration():
    """Test full integration"""
    print("🔄 Testing full integration...")
    try:
        db = DatabaseManager()
        llm = LLMClient()
        
        # Get schema context
        tables_result = db.get_all_tables()
        schema_context = ""
        if tables_result["success"] and not tables_result["data"].empty:
            schema_context = "Available tables: " + ", ".join(tables_result["data"]["table_name"].tolist())
        
        # Test natural language query
        nl_query = "show all users"
        llm_result = llm.generate_sql(nl_query, schema_context)
        
        if not llm_result["success"]:
            print(f"❌ Integration test failed at LLM step: {llm_result.get('error')}")
            return False
        
        # Execute the generated SQL
        sql_result = db.execute_query(llm_result["sql"])
        
        if not sql_result["success"]:
            print(f"❌ Integration test failed at SQL execution: {sql_result.get('error')}")
            return False
        
        print("✅ Full integration test successful")
        print(f"   Natural Language: {nl_query}")
        print(f"   Generated SQL: {llm_result['sql']}")
        print(f"   Rows returned: {sql_result.get('rows_affected', 0)}")
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting System Tests for LLM SQL CRUD Assistant")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("Database", test_database),
        ("LLM Client", test_llm_client),
        ("Integration", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
        print("-" * 40)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run: streamlit run streamlit_app.py")
        print("   2. Or run: python run_mcp_server.py")
    else:
        print("⚠️ Some tests failed. Please check your configuration.")
        print("\n🔧 Common fixes:")
        print("   1. Ensure PostgreSQL is running")
        print("   2. Check your .env file")
        print("   3. Run: python setup_database.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)