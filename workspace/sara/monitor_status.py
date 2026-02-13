#!/usr/bin/env python3
# 📊 Voice System Monitor Status

import subprocess
import json
import time
from datetime import datetime

def check_voice_system_status():
    """Check comprehensive voice system status"""
    print("🔍 CHECKING VOICE SYSTEM STATUS...")
    print("=" * 50)
    
    # Check voice agent
    voice_agent_running = is_process_running("sara_voice_agent.py")
    print(f"🎤 Voice Agent: {'✅ RUNNING' if voice_agent_running else '❌ STOPPED'}")
    
    # Check GUI  
    gui_running = is_process_running("simple_gui.py")
    print(f"🖥️  Monitoring GUI: {'✅ RUNNING' if gui_running else '❌ STOPPED'}")
    
    # Check audio devices
    k66_detected = check_k66_mic()
    print(f"🎙️  K66 Microphone: {'✅ CONNECTED' if k66_detected else '❌ NOT DETECTED'}")
    
    # Check voice recognition components
    sr_available = check语音recognition()
    print(f"🗣️  Speech Recognition: {'✅ AVAILABLE' if sr_available else '⚠️  FALLBACK MODE'}")
    
    # Test audio capture
    audio_working = test_audio_capture()
    print(f"🔊 Audio Capture: {'✅ WORKING' if audio_working else '❌ FAILED'}")
    
    # Current status summary
    status = {
        "voice_agent": voice_agent_running,
        "gui": gui_running,
        "k66_mic": k66_detected,
        "speech_recognition": sr_available,
        "audio_capture": audio_working,
        "system_operational": all([voice_agent_running, k66_detected, audio_working])
    }
    
    print("\n📊 SYSTEM STATUS SUMMARY")
    print("=" * 50)
    if status["system_operational"]:
        print("✅ VOICE SYSTEM FULLY OPERATIONAL")
        print("🎤 Sara is listening for your voice commands")
        print("🎙️  K66 microphone is ready")
        print("🗣️  Voice recognition systems are active")
        print("🖥️  Monitoring ready (GUI can be started if needed)")
    else:
        print("⚠️  SYSTEM HAS ISSUES - CHECK COMPONENTS")
    
    return status

def is_process_running(process_name):
    """Check if process is running"""
    try:
        result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
        return bool(result.stdout.strip())
    except:
        return False

def check_k66_mic():
    """Check if K66 microphone is detected"""
    try:
        result = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
        return "K66" in result.stdout
    except:
        return False

def check语音recognition():
    """Check if speech recognition library is available"""
    try:
        import speech_recognition
        return True
    except:
        try:
            import vosk
            return True
        except:
            return False

def test_audio_capture():
    """Test if audio capture is working"""
    try:
        test_file = "/tmp/audio_test.wav"
        result = subprocess.run(['arecord', '-d', '1', test_file], 
                              capture_output=True, timeout=3)
        
        if os.path.exists(test_file):
            os.remove(test_file)
            return True
        return False
    except:
        return False

def start_monitoring_gui():
    """Start the monitoring GUI if not running"""
    if not is_process_running("simple_gui.py"):
        print("🖥️  Starting monitoring GUI...")
        try:
            subprocess.Popen(['python3', '/home/godfather/local-command-center/simple_gui.py'])
            return True
        except Exception as e:
            print(f"❌ GUI start failed: {e}")
            return False
    else:
        print("✅ GUI already running")
        return True

def main():
    """Main status check"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕐 Voice System Status Check at {now}")
    print()
    
    status = check_voice_system_status()
    
    if status["system_operational"]:
        print("\n🚀 READY FOR VOICE TESTING!")
        print("=" * 50)
        print("💡 HOW TO TEST VOICE RECOGNITION:")
        print("1. Say clearly: 'Sara' (wake word)")
        print("2. Wait for response: 'Yes, I'm listening'")
        print("3. Give voice command: 'Sara, tell me about yourself'")
        print("4. Listen for female voice response")
        print()
        print("🎤 Current Voice Setup:")
        print("  • K66 USB-C microphone (professional quality)")
        print("  • Female voice responses")
        print("  • Local voice recognition (offline)")
        print("  • Complete privacy protection")
        print()
        print("🖥️  Start monitoring GUI for real-time status?")
        start_gui = input("Start GUI? (y/n): ").lower().strip()
        
        if start_gui in ['y', 'yes']:
            if start_monitoring_gui():
                print("✅ Monitoring GUI started")
                time.sleep(2)
        else:
            print("⚡ Continue with voice agent only")
        
        print("\n🎯 VOICE SYSTEM ACTIVE!")
        print("🎤 Sara is listening for your voice commands now!")
        
    else:
        print("\n🔧 SYSTEM NEEDS ATTENTION")
        print("=" * 50)
        if not status["voice_agent"]:
            print("⚠️  Voice agent not running - start with:")
            print("      python3 /home/godfather/local-command-center/agents/sara-voice/sara_voice_agent.py")
        
        if not status["k66_mic"]:
            print("⚠️  K66 microphone not detected - check connection")
        
        if not status["audio_capture"]:
            print("⚠️  Audio capture failing - check permissions")
        
        if not status["speech_recognition"]:
            print("⚠️  Speech recognition components missing - using fallback")

if __name__ == "__main__":
    main()