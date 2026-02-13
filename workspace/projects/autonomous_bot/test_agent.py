#!/usr/bin/env python3
"""
Local test runner for Autonomous Agent
Simulates the GitHub Actions environment
"""

import os
import json
import sys
from pathlib import Path

# Add agent directory to path
agent_path = Path(__file__).parent / "agent"
sys.path.append(str(agent_path))

def test_agent():
    """Test the autonomous agent locally"""
    
    # Set environment variables to simulate GitHub Actions
    os.environ['JOB_ID'] = 'test-job-' + str(int(time.time()))
    os.environ['TASK'] = "Create a simple Python script that demonstrates autonomous agent capabilities"
    os.environ['USER_ID'] = 'test-user'
    os.environ['TIMESTAMP'] = datetime.datetime.now().isoformat()
    
    # Mock API keys for testing
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    os.environ['TELEGRAM_BOT_TOKEN'] = 'test-token'
    
    print("🧪 Testing Autonomous Agent Locally")
    print("=" * 50)
    
    try:
        # Run the agent
        from agent.main import AutonomousAgent
        
        agent = AutonomousAgent()
        result = agent.execute_task()
        
        print("\n✅ Agent Test Completed Successfully!")
        print(f"📊 Summary: {result['summary']}")
        print(f"📁 Files Created: {len(result['files_created'])}")
        
        # Show created files
        for file_path in result['files_created']:
            if Path(file_path).exists():
                print(f"📄 {file_path} ({Path(file_path).stat().st_size} bytes)")
        
        # Check changes.json
        changes_file = Path("agent/changes.json")
        if changes_file.exists():
            with open(changes_file, 'r') as f:
                changes = json.load(f)
            print(f"\n📋 Total Actions: {len(changes.get('changes', []))}")
        
        print("\n🎉 Local test ready for GitHub deployment!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_event_handler():
    """Test the event handler locally"""
    print("\n🧪 Testing Event Handler")
    print("=" * 30)
    
    handler_dir = Path("event_handler")
    if not handler_dir.exists():
        print("⚠️ Event handler not set up yet")
        return False
    
    # Check package.json exists
    package_json = handler_dir / "package.json"
    if not package_json.exists():
        print("⚠️ package.json not found")
        return False
    
    print("✅ Event handler files present")
    print("📦 To test event handler: cd event_handler && npm install && npm start")
    
    return True

def run_tests():
    """Run all tests"""
    print("🚀 Autonomous Bot - Local Test Suite")
    print("=" * 50)
    
    # Test agent
    agent_ok = test_agent()
    
    # Test event handler
    handler_ok = test_event_handler()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"🤖 Agent: {'✅ PASS' if agent_ok else '❌ FAIL'}")
    print(f"📡 Event Handler: {'✅ PASS' if handler_ok else '❌ FAIL'}")
    
    if agent_ok and handler_ok:
        print("\n🎉 All tests passed! Ready for deployment!")
        print("\n📋 Next Steps:")
        print("1. Set up GitHub repository")
        print("2. Configure GitHub secrets")
        print("3. Create Telegram bot")
        print("4. Deploy to GitHub Actions")
    else:
        print("\n⚠️ Some tests failed. Check output above for details.")
    
    return agent_ok and handler_ok

if __name__ == "__main__":
    import time
    import datetime
    
    success = run_tests()
    sys.exit(0 if success else 1)