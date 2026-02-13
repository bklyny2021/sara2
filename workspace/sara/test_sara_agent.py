#!/usr/bin/env python3
"""
Test script for Sara AI agent
Tests if Sara responds correctly to identity queries
"""

import subprocess
import json
import sys

def test_sara_agent():
    """Test Sara agent by asking who she is"""
    
    test_query = "Who are you? Please respond with just your name."
    
    print(f"🧪 Testing Sara AI Agent...")
    print(f"📝 Query: {test_query}")
    print("=" * 50)
    
    try:
        # Use ollama to query the Sara model
        result = subprocess.run([
            'ollama', 'run', 'sara-ai-partner', test_query
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            response = result.stdout.strip()
            print(f"✅ Sara's Response:")
            print(f"\"{response}\"")
            print("=" * 50)
            
            # Check if response contains "Sara"
            if "sara" in response.lower():
                print("🎉 SUCCESS: Sara responded with her name!")
                return True
            else:
                print("⚠️  WARNING: Sara didn't mention her name in the response")
                print("🤔 This might indicate the model needs adjustment")
                return False
        else:
            print(f"❌ Error running Sara model: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ ERROR: Query timed out (30 seconds)")
        return False
    except Exception as e:
        print(f"💥 ERROR: {str(e)}")
        return False

def main():
    print("🤖 Sara AI Agent Test Script")
    print("=" * 50)
    print("This tests if Sara responds correctly to identity queries")
    print("even when running through the super agent cluster.")
    print()
    
    success = test_sara_agent()
    
    if success:
        print("\n🌟 TEST PASSED: Sara is responding correctly!")
        print("🚀 Ready for super agent cluster integration")
    else:
        print("\n💔 TEST FAILED: Sara needs model adjustment")
        print("🔧 Consider updating the .modelfile configuration")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()