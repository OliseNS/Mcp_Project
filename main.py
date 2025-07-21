#!/usr/bin/env python3
"""
MCP Server - Main Entry Point
A minimal MCP Server with Vector DB and LLM Integration
"""

import sys
import os
from mcp_server.config import Config
from mcp_server.api import run_server

def main():
    """Main entry point for the MCP Server"""
    print("🤖 Starting MCP Server...")
    
    try:
        # Validate configuration
        Config.validate()
        print("✅ Configuration validated successfully")
        
        # Start the server
        print(f"🚀 Starting server on {Config.HOST}:{Config.PORT}")
        print(f"📊 Vector DB path: {Config.CHROMA_DB_PATH}")
        print(f"🧠 Using model: {Config.MODEL_NAME}")
        print("=" * 50)
        
        success = run_server()
        
        if not success:
            print("❌ Failed to start server")
            sys.exit(1)
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n📝 Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 