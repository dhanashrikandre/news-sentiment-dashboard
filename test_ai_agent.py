#!/usr/bin/env python3
"""
Simple test script to verify AI agent functionality
"""

import os
import sys
from ai_agent import DocumentProcessor


def test_basic_functionality():
    """Test basic AI agent functionality"""
    print("🧪 Testing AI Agent Basic Functionality...")
    
    agent = DocumentProcessor()
    
    # Test document with various instruction types
    test_document = """
    System Setup Instructions:
    
    1. Create project folder
    2. Download configuration files
    3. Analyze system requirements  
    4. Start the application server
    5. Send confirmation email
    
    If setup fails, alert the admin team
    """
    
    print("📄 Processing test document...")
    results = agent.process_document(test_document)
    
    # Verify results
    assert results['instructions_found'] > 0, "No instructions found!"
    assert results['execution_summary']['total'] > 0, "No executions performed!"
    assert results['execution_summary']['success_rate'] >= 0, "Invalid success rate!"
    
    print(f"✅ Found {results['instructions_found']} instructions")
    print(f"✅ Executed {results['execution_summary']['total']} commands")
    print(f"✅ Success rate: {results['execution_summary']['success_rate']:.1f}%")
    
    return True


def test_process_categorization():
    """Test that instructions are correctly categorized by process type"""
    print("\n🧪 Testing Process Categorization...")
    
    agent = DocumentProcessor()
    
    test_document = """
    Multi-process workflow:
    - Create backup files
    - Fetch data from API 
    - Analyze the dataset
    - Send report to users
    - Start monitoring service
    """
    
    results = agent.process_document(test_document)
    processes = results['instructions_by_process']
    
    print(f"✅ Identified process types: {list(processes.keys())}")
    
    # Verify we have multiple process types
    assert len(processes) > 1, "Should identify multiple process types!"
    
    return True


def test_status_reporting():
    """Test that status is properly reported for each execution"""
    print("\n🧪 Testing Status Reporting...")
    
    agent = DocumentProcessor()
    
    test_document = "Create a new database backup"
    
    results = agent.process_document(test_document)
    
    # Check execution results have proper status fields
    for result in results['execution_results']:
        assert 'status' in result, "Missing status field!"
        assert 'success' in result, "Missing success field!"
        assert 'execution_time' in result, "Missing execution time!"
        assert 'duration_ms' in result, "Missing duration!"
        
        print(f"✅ Instruction: {result['instruction'][:50]}...")
        print(f"   Status: {result['status']}, Success: {result['success']}")
    
    return True


def run_all_tests():
    """Run all tests and report results"""
    print("🚀 Starting AI Agent Tests...\n")
    
    tests = [
        test_basic_functionality,
        test_process_categorization, 
        test_status_reporting
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print("✅ PASSED\n")
        except Exception as e:
            failed += 1
            print(f"❌ FAILED: {e}\n")
    
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! AI Agent is working correctly.")
        return True
    else:
        print("💥 Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)