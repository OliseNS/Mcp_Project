#!/usr/bin/env python3
"""
Test script for Healthcare MCP Server setup verification with OpenRouter
"""

import sys
import os
import requests
import json
from typing import Dict, Any

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from mcp_server.config import Config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Config: {e}")
        return False
    
    try:
        from mcp_server.vector_db import VectorDB
        print("✅ VectorDB module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import VectorDB: {e}")
        return False
    
    try:
        from mcp_server.llm_handler import LLMHandler
        print("✅ LLMHandler module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import LLMHandler: {e}")
        return False
    
    try:
        from mcp_server.agent import HealthcareAgent
        print("✅ HealthcareAgent module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import HealthcareAgent: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        from mcp_server.config import Config
        
        # Test if API key is set (don't validate it)
        if Config.OPENROUTER_API_KEY:
            print("✅ OpenRouter API key is configured")
        else:
            print("⚠️  OpenRouter API key not found - please set OPENROUTER_API_KEY in .env file")
        
        print(f"✅ Model: {Config.MODEL_NAME}")
        print(f"✅ Temperature: {Config.TEMPERATURE}")
        print(f"✅ Max Tokens: {Config.MAX_TOKENS}")
        print(f"✅ ChromaDB Path: {Config.CHROMA_DB_PATH}")
        print(f"✅ Healthcare Collection: {Config.HEALTHCARE_COLLECTION}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_vector_db():
    """Test vector database functionality"""
    print("\n🔍 Testing vector database...")
    
    try:
        from mcp_server.vector_db import VectorDB
        
        # Initialize vector DB
        vector_db = VectorDB("test_healthcare_collection")
        print("✅ VectorDB initialized successfully")
        
        # Test adding documents
        test_docs = [
            {
                "text": "This is a test healthcare document about diabetes management.",
                "metadata": {"source": "test", "category": "diseases"},
                "id": "test_healthcare_doc_1"
            }
        ]
        
        vector_db.add_documents(test_docs)
        print("✅ Healthcare documents added successfully")
        
        # Test search
        results = vector_db.search("diabetes", n_results=1)
        if results:
            print("✅ Healthcare search functionality working")
        else:
            print("⚠️  Healthcare search returned no results")
        
        # Test category search
        results = vector_db.search("diabetes", n_results=1, category="diseases")
        if results:
            print("✅ Category-based search working")
        else:
            print("⚠️  Category-based search returned no results")
        
        # Clean up
        vector_db.clear_collection()
        print("✅ Test collection cleared")
        
        return True
    except Exception as e:
        print(f"❌ VectorDB test failed: {e}")
        return False

def test_openrouter_connection():
    """Test OpenRouter API connection"""
    print("\n🔍 Testing OpenRouter connection...")
    
    try:
        from mcp_server.config import Config
        from mcp_server.llm_handler import LLMHandler
        
        if not Config.OPENROUTER_API_KEY:
            print("⚠️  OpenRouter API key not configured - skipping connection test")
            return True
        
        llm_handler = LLMHandler()
        
        # Test simple request
        test_response = llm_handler.generate_response(
            "Hello, this is a test message.",
            include_disclaimer=False
        )
        
        if test_response and not test_response.startswith("Error"):
            print("✅ OpenRouter connection successful")
            return True
        else:
            print(f"❌ OpenRouter test failed: {test_response}")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter connection test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints if server is running"""
    print("\n🔍 Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint responding")
            print(f"   Response: {response.json()}")
        else:
            print(f"⚠️  Health endpoint returned {response.status_code}")
            return False
        
        # Test config endpoint
        response = requests.get(f"{base_url}/config", timeout=5)
        if response.status_code == 200:
            print("✅ Config endpoint responding")
            config = response.json()
            print(f"   Model: {config.get('model_name', 'N/A')}")
        else:
            print(f"⚠️  Config endpoint returned {response.status_code}")
        
        # Test healthcare knowledge stats
        response = requests.get(f"{base_url}/knowledge/stats", timeout=5)
        if response.status_code == 200:
            print("✅ Healthcare knowledge stats endpoint responding")
            stats = response.json()
            print(f"   Documents: {stats.get('total_documents', 0)}")
        else:
            print(f"⚠️  Healthcare knowledge stats endpoint returned {response.status_code}")
        
        return True
    except requests.exceptions.ConnectionError:
        print("⚠️  API server not running - start with: python main.py")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_streamlit():
    """Test if Streamlit can be imported"""
    print("\n🔍 Testing Streamlit...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Streamlit: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Healthcare MCP Server Setup Test (OpenRouter)")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Vector Database", test_vector_db),
        ("OpenRouter Connection", test_openrouter_connection),
        ("Streamlit", test_streamlit),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Healthcare MCP Server is ready to use.")
        print("\nNext steps:")
        print("1. Set your OpenRouter API key in .env file")
        print("2. Start the server: python main.py")
        print("3. Launch Streamlit: streamlit run streamlit_app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 