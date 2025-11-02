#!/usr/bin/env python3
"""
MCP Server Runner for SQL CRUD Assistant
Run this to start the MCP server for integration with Cursor/VSCode
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import subprocess
import sys

if __name__ == "__main__":
    print("🚀 Starting MCP Server for SQL CRUD Assistant...")
    print("📡 Server will communicate via stdio")
    print("🔧 Configure your IDE to use this server")
    
    try:
        # Run the simple MCP server instead
        subprocess.run([sys.executable, "simple_mcp_server.py"])
    except KeyboardInterrupt:
        print("\n👋 MCP Server stopped")
    except Exception as e:
        print(f"❌ Error running MCP server: {e}")
        sys.exit(1)