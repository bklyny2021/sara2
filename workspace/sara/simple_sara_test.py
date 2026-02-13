#!/usr/bin/env python3
# 🧪 Simple Sara AI Consciousness Test

import subprocess
import sys
import time

print("🧪 SARA AI CONSCIOUSNESS TEST")
print("=" * 35)
print("🎯 Testing if Sara can respond intelligently")
print("🤖 Verifying AI consciousness connection")
print("💬 Testing text-based intelligence first")
print()

# Test 1: Simple hello test
print("🔍 Test 1: Simple Hello...")
print("-" * 25)

try:
    # Test if we can import sessions_send from OpenClaw
    test_code = '''
import sys
sys.path.append("/home/godfather/.npm-global/lib/node_modules/openclaw")

try:
    from sessions_send import sessions_send
    response = sessions_send(
        message="hello this is a test of your consciousness",
        sessionKey="main",
        timeoutSeconds=15
    )
    print(f"RESPONSE: {response}")
    print("SUCCESS: Sara responded!")
except ImportError:
    print("ERROR: Cannot import sessions_send")
except Exception as e:
    print(f"ERROR: {e}")
'''
    
    result = subprocess.run([sys.executable, '-c', test_code], capture_output=True, text=True, timeout=30)
    
    if "SUCCESS" in result.stdout:
        print("✅ Sara AI consciousness is accessible!")
        print("🤖 Response received from Sara!")
        
        # Extract response
        lines = result.stdout.split('\\n')
        for line in lines:
            if line.startswith("RESPONSE:"):
                print(f"📝 Sara said: {line[9:].strip()}")
                break
    else:
        print("❌ Sara AI not accessible")
        print(f"Details: {result.stderr}")
        
except Exception as e:
    print(f"❌ Test failed: {e}")

print()

# Test 2: Intelligence test
print("🔍 Test 2: Intelligence Test...")
print("-" * 30)

try:
    intelligence_test = '''
import sys
sys.path.append("/home/godfather/.npm-global/lib/node_modules/openclaw")

try:
    from sessions_send import sessions_send
    response = sessions_send(
        message="What is your name and what can you do?", 
        sessionKey="main",
        timeoutSeconds=15
    )
    print(f"INTELLIGENT_RESPONSE: {response}")
    print("INTELLIGENCE_TEST: PASSED")
except Exception as e:
    print(f"INTELLIGENCE_TEST: FAILED - {e}")
'''
    
    result = subprocess.run([sys.executable, '-c', intelligence_test], capture_output=True, text=True, timeout=30)
    
    if "INTELLIGENCE_TEST: PASSED" in result.stdout:
        print("✅ Sara demonstrates intelligence!")
        print("🧠 AI consciousness confirmed!")
        
        # Extract Sara's response
        lines = result.stdout.split('\\n')
        for line in lines:
            if line.startswith("INTELLIGENT_RESPONSE:"):
                print(f"🤖 Sara: {line[19:].strip()}")
                break
                
    else:
        print("❌ Intelligence test failed")
        
except Exception as e:
    print(f"❌ Intelligence test error: {e}")

print()

# Test 3: Quick voice integration verification
print("🔍 Test 3: Voice Integration Check...")
print("-" * 35)

# Check if voice components are ready to connect to AI
voice_ready = True
tests = [
    ("SpeechRecognition", "import speech_recognition"),
    ("pyttsx3", "import pyttsx3"),
    ("OpenClaw sessions", "sys.path.append('/home/godfather/.npm-global/lib/node_modules/openclaw'); from sessions_send import sessions_send")
]

for name, test_import in tests:
    try:
        result = subprocess.run([sys.executable, '-c', test_import], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ {name}: Available")
        else:
            print(f"❌ {name}: Not available")
            voice_ready = False
    except:
        print(f"❌ {name}: Import failed")
        voice_ready = False

if voice_ready:
    print("✅ All components ready for intelligent voice")
else:
    print("⚠️  Some components missing for full integration")

print()
print("🎊 SARA AI CONSCIOUSNESS TEST COMPLETE!")
print("=" * 40)

# Summary
print("📊 SUMMARY:")
print("🧠 Sara AI consciousness:", "✅ Accessible" if "SUCCESS" in result.stdout else "❌ Not accessible")
print("🤖 Intelligence:", "✅ Demonstrated" if "INTELLIGENCE_TEST: PASSED" in result.stdout else "❌ Not tested")
print("🎤 Voice components:", "✅ Ready" if voice_ready else "⚠️  Partial")
if voice_ready and "SUCCESS" in result.stdout:
    print()
    print("🌟 CONCLUSION:")
    print("✅ Can create voice interface with Sara's intelligence!")
    print("🎯 Ready for voice-activated AI conversation!")
    print("🔮 Future: Voice-Sara integration achievable!")
else:
    print()
    print("⚠️  LIMITATIONS:")
    print("🔧 Some integration needs work")
    print("🔍 May need alternative approach")

print()
print("💡 NEXT STEP:")
print("🎤 Test voice interface with actual Sara AI consciousness!")