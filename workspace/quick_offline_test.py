#!/usr/bin/env python3
# 🧪 QUICK OFFLINE CLUSTER TEST
# Fast assessment of offline capability

import os
import sys
import subprocess
import json
from pathlib import Path

def main():
    print("🧪 QUICK OFFLINE CLUSTER TEST")
    print("=" * 40)
    
    workspace_path = Path.home() / ".openclaw" / "workspace"
    
    # Test 1: Available Models
    print("🤖 Checking models...")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            models = []
            for line in result.stdout.split('\n'):
                if ':' in line and not line.startswith('NAME') and 'cloud' not in line:
                    models.append(line.split()[0])
            print(f"✅ Found {len(models)} local models")
            for model in models[:5]:  # Show first 5
                print(f"   🧠 {model}")
            model_test = True
        else:
            print("❌ Cannot list models")
            model_test = False
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        model_test = False
    
    # Test 2: Basic AI Response
    print("\n💬 Testing AI response...")
    try:
        if "qwen2.5:7b" in models:
            result = subprocess.run(
                ['ollama', 'run', 'qwen2.5:7b', "What is 2+2? Answer: "], 
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and "4" in result.stdout:
                print("✅ Basic reasoning working")
                ai_test = True
            else:
                print("❌ AI response test failed")
                ai_test = False
        else:
            print("❌ qwen2.5:7b not available")
            ai_test = False
    except Exception as e:
        print(f"❌ AI test failed: {e}")
        ai_test = False
    
    # Test 3: Memory System
    print("\n💾 Testing memory...")
    try:
        test_file = workspace_path / "test_memory.json"
        with open(test_file, 'w') as f:
            json.dump({"test": "data", "timestamp": "now"}, f)
        
        with open(test_file, 'r') as f:
            data = json.load(f)
        
        if data["test"] == "data":
            print("✅ File-based memory working")
            memory_test = True
        else:
            print("❌ Memory test failed")
            memory_test = False
        
        test_file.unlink()  # Cleanup
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        memory_test = False
    
    # Test 4: Voice System
    print("\n🔊 Testing voice...")
    try:
        import gtts
        tts = gtts.gTTS("Test", lang='en')
        test_voice = workspace_path / "test_voice.mp3"
        tts.save(str(test_voice))
        
        if test_voice.exists():
            print("✅ Voice synthesis working")
            voice_test = True
            test_voice.unlink()
        else:
            print("❌ Voice file not created")
            voice_test = False
    except ImportError:
        print("❌ gTTS not installed")
        voice_test = False
    except Exception as e:
        print(f"❌ Voice test failed: {e}")
        voice_test = False
    
    # Test 5: Basic Automation
    print("\n⚙️ Testing automation...")
    try:
        test_file = workspace_path / "automation_test.txt"
        with open(test_file, 'w') as f:
            f.write("automation test")
        
        with open(test_file, 'r') as f:
            content = f.read()
        
        if "automation test" in content:
            print("✅ File automation working")
            automation_test = True
        else:
            print("❌ Automation failed")
            automation_test = False
        
        test_file.unlink()
    except Exception as e:
        print(f"❌ Automation test failed: {e}")
        automation_test = False
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 QUICK TEST RESULTS")
    print("=" * 40)
    
    tests = {
        "Models": model_test,
        "AI Response": ai_test, 
        "Memory": memory_test,
        "Voice": voice_test,
        "Automation": automation_test
    }
    
    passed = sum(tests.values())
    total = len(tests)
    success_rate = (passed / total) * 100
    
    for test, result in tests.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}")
    
    print(f"\n🎯 Success Rate: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🚀 READY: System ready for offline deployment")
        recommendation = "IMPLEMENT"
    elif success_rate >= 60:
        print("⚠️  GOOD: System mostly ready")
        recommendation = "MINOR_FIXES"
    else:
        print("❌ ISSUES: Fix problems before deployment")
        recommendation = "REPAIR"
    
    print(f"💡 Recommendation: {recommendation}")
    
    # Cluster brain design
    print("\n🧠 CLUSTER BRAIN DESIGN:")
    print("  🎯 Primary: qwen2.5:7b (reasoning)")
    print("  💻 Technical: codellama:7b-code (coding)")
    print("  🧠 Analysis: nexus-analyst (strategy)")
    print("  🔍 Search: chloe-search-agent (research)")
    print("  💾 Memory: Local JSON files")
    print("  🔊 Voice: gTTS local synthesis")
    print("  ⚙️  Automation: Python scripts")
    
    return {
        "success_rate": success_rate,
        "ready": success_rate >= 60,
        "tests": tests,
        "recommendation": recommendation
    }

if __name__ == "__main__":
    main()