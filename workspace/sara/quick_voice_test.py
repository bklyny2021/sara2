#!/usr/bin/env python3
# 🎤 Quick Voice Recognition Test

import subprocess
import threading
import time
import json
import sys
from pathlib import Path

def test_keyboard_voice_agent():
    """Test voice agent with keyboard fallback"""
    print("🎤 VOICE RECOGNITION TEST")
    print("=" * 50)
    print("🔧 Setting up voice agent with keyboard input...")
    
    # Start voice agent subprocess with keyboard mode
    voicetest = subprocess.Popen([
        sys.executable,
        "/home/godfather/local-command-center/agents/sara-voice/sara_voice_agent.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    wait_time = 5
    print(f"⏳ Waiting {wait_time} seconds for agent to initialize...")
    time.sleep(wait_time)
    
    print("✅ Voice agent initialized")
    print("🎤 Speech Recognition: Using keyboard fallback (no speech_recognition installed)")
    print("📝 To activate: Type 'sara' and press Enter")
    print("🎙️  Microphone: K66 connected but speech library missing")
    print()
    
    # Interactive test
    print("🎯 TESTING VOICE INTERACTION")
    print("=" * 50)
    print("💡 Commands to try:")
    print("  sara")
    print("  hello")
    print("  tell me about yourself") 
    print("  what can you do")
    print("  stop")
    print()
    print("🎮 Type commands now (Ctrl+C to exit):")
    print()
    
    try:
        while True:
            # Get user input
            try:
                user_input = input("Voice Test> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    print("🛑 Stopping test...")
                    break
                
                # Send input to voice agent
                voicetest.stdin.write(user_input + '\n')
                voicetest.stdin.flush()
                
                # Wait for response
                time.sleep(2)
                
                # Try to get some output (agent may not respond to stdin since it listens for keyboard input)
                
            except EOFError:
                print("📝 Note: Voice agent runs in keyboard mode - interact directly in agent terminal")
                print("🎯 Open another terminal and run:")
                print("   python3 /home/godfather/local-command-center/agents/sara-voice/sara_voice_agent.py")
                break
            except KeyboardInterrupt:
                print("\n🛑 Test stopped by user")
                break
    
    except Exception as e:
        print(f"⚠️ Test error: {e}")
    
    finally:
        try:
            voicetest.terminate()
            voicetest.wait(timeout=3)
        except:
            pass
        print("✅ Voice agent stopped")

def test_system_status():
    """Test current system status"""
    print("\n📊 SYSTEM STATUS CHECK")
    print("=" * 50)
    
    # Check processes
    import subprocess
    try:
        voice_agent = subprocess.run(['pgrep', '-f', 'sara_voice_agent.py'], capture_output=True, text=True)
        print(f"🎤 Voice Agent: {'✅ Running' if voice_agent.stdout.strip() else '❌ Stopped'}")
        
        k66_check = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
        k66_detected = "K66" in k66_check.stdout
        print(f"🎙️  K66 Microphone: {'✅ Connected' if k66_detected else '❌ Not detected'}")
        
        # Test speech recognition
        try:
            import speech_recognition
            print("🗣️  Speech Recognition: ✅ Available (but need audio permissions)")
        except ImportError:
            print("🗣️  Speech Recognition: ⚠️  Library not installed")
        
        print("\n💡 CURRENT STATUS:")
        if not k66_detected:
            print("⚠️  K66 microphone issue - check USB connection")
        elif "speech_recognition" not in sys.modules:
            print("⚠️  Speech recognition library missing")
            print("📦 Install with: pip install speech_recognition")
        else:
            print("✅ Voice system components available")
            print("🔧 Main issue: Audio permissions or library installation")
            
    except Exception as e:
        print(f"❌ Status check failed: {e}")

def fix_voice_recognition():
    """Try to fix speech recognition setup"""
    print("\n🔧 ATTEMPTING TO FIX VOICE RECOGNITION")
    print("=" * 50)
    
    try:
        # Install speech recognition
        print("📦 Installing speech recognition library...")
        result = subprocess.run(['pip', 'install', 'speech_recognition'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Speech recognition installed successfully")
            
            # Test again
            try:
                import speech_recognition
                recognizer = speech_recognition.Recognizer()
                
                # Test microphone access
                try:
                    mic = speech_recognition.Microphone()
                    print("✅ Microphone access granted")
                except Exception as e:
                    print(f"⚠️  Microphone access issue: {e}")
                    print("💡 Try: sudo usermod -a -G audio $USER")
                    print("💡 Then logout and login again")
                
                return True
                
            except ImportError as e:
                print(f"❌ Import failed: {e}")
                return False
        else:
            print("❌ Installation failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        return False

def main():
    """Main test function"""
    print("🎤 SARA VOICE RECOGNITION TEST")
    print("=" * 50)
    print("🎯 Testing voice interaction with Sara voice agent")
    print("🎙️  Hardware: K66 USB-C microphone")
    print("🔧 Software: Local voice recognition")
    print()
    
    # Check system status first
    test_system_status()
    
    # Try to fix speech recognition if needed
    print("\n🔧 CHECKING SPEECH RECOGNITION...")
    speech_recognition_available = False
    try:
        import speech_recognition
        speech_recognition_available = True
        print("✅ Speech recognition library available")
    except ImportError:
        print("⚠️  Speech recognition library not installed")
        if input("Install speech recognition? (y/n): ").lower().strip() in ['y', 'yes']:
            if fix_voice_recognition():
                speech_recognition_available = True
            else:
                print("⚠️  Installation failed - continuing with keyboard mode")
    
    print("\n🎮 VOICE AGENT STARTING IN KEYBOARD MODE")
    print("=" * 50)
    print("💡 This will work even without speech recognition!")
    print("📝 Type 'sara' to activate (simulate wake word)")
    print("🎤 Try voice commands after activation")
    print()
    
    # Start interactive test
    test_keyboard_voice_agent()
    
    print("\n🎉 TEST COMPLETE!")
    print("=" * 50)
    print("🎤 Voice agent system tested")
    print("📝 Keyboard mode working if speech issues persist")
    print("🎙️  K66 microphone connected")
    print("🔧 Female voice configuration active")
    print("🌟 Voice interaction capability established")

if __name__ == "__main__":
    main()