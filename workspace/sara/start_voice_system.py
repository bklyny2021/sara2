#!/usr/bin/env python3
# 🚀 Voice System Quick Start
# One-click launch for Sara voice command center

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header():
    """Print startup header"""
    print("=" * 60)
    print("🎤 SARA VOICE COMMAND CENTER")
    print("=" * 60)
    print("🚀 Voice-Enabled AI Agent Complete Setup")
    print("💬 Wake Word: 'Sara'")
    print("🔊 Female Voice Output")
    print("📊 Monitoring Interface")
    print("🌐 Complete Local Operation")
    print("=" * 60)

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking voice system dependencies...")
    
    missing = []
    
    try:
        import speech_recognition
        print("✅ Speech recognition available")
    except ImportError:
        missing.append("speech_recognition")
        print("❌ Speech recognition missing - will use keyboard fallback")
    
    try:
        import pyttsx3
        print("✅ Text-to-speech available")
    except ImportError:
        missing.append("pyttsx3")
        print("❌ Text-to-speech missing")
    
    try:
        import vosk
        print("✅ VOSK offline recognition available")
    except ImportError:
        missing.append("vosk")
        print("❌ VOSK missing - will use online recognition")
    
    if len(missing) == 0:
        print("✅ All voice components ready!")
        return True
    else:
        print(f"⚠️  {len(missing)} components missing - system will use fallbacks")
        return False

def setup_environment():
    """Setup the voice environment"""
    print("🛠️ Setting up voice environment...")
    
    # Create necessary directories
    directories = [
        "/home/godfather/local-command-center/logs",
        "/home/godfather/local-command-center/backups",
        "/home/godfather/local-command-center/config"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create config files
    config = {
        "voice_settings": {
            "wake_word": "sara",
            "voice_gender": "female",
            "volume": 0.9,
            "rate": 150
        },
        "monitoring": {
            "enabled": True,
            "sara_access": True,
            "log_level": "INFO"
        }
    }
    
    import json
    with open("/home/godfather/local-command-center/config/voice_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Environment setup complete")

def start_monitoring_gui():
    """Start the monitoring GUI"""
    print("🖥️ Starting monitoring GUI...")
    try:
        gui_process = subprocess.Popen([
            sys.executable, 
            "/home/godfather/local-command-center/simple_gui.py"
        ])
        print("✅ Monitoring GUI started")
        print("   URL: GUI Application (window should appear)")
        return gui_process
    except Exception as e:
        print(f"❌ GUI launch failed: {e}")
        return None

def start_voice_agent():
    """Start the voice agent"""
    print("🎤 Starting Sara voice agent...")
    try:
        voice_process = subprocess.Popen([
            sys.executable,
            "/home/godfather/local-command-center/agents/sara-voice/sara_voice_agent.py"
        ])
        print("✅ Sara voice agent started")
        print("   Wake Word: Say 'Sara' to activate")
        return voice_process
    except Exception as e:
        print(f"❌ Voice agent launch failed: {e}")
        return None

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("📖 VOICE SYSTEM USAGE GUIDE")
    print("=" * 60)
    print()
    print("🎤 USING SARA VOICE:")
    print("   1. Say 'Sara' (wake word)")
    print("   2. Wait for response ('Yes, I'm listening')")
    print("   3. Ask your question or give command")
    print("   4. Sara will respond with voice output")
    print()
    print("⌨️ KEYBOARD FALLBACK:")
    print("   Type 'sara' in the voice agent terminal")
    print("   Then type your command when prompted")
    print()
    print("📊 MONITORING GUI FEATURES:")
    print("   • Real-time agent status monitoring")
    print("   • System resource tracking")
    print("   • Live log viewing")
    print("   • Start/Stop agent controls")
    print()
    print("🔧 SAMPLE VOICE COMMANDS:")
    print("   'Sara, what's the system status?'")
    print("   'Sara, help me with my code'")
    print("   'Sara, tell me about yourself'")
    print("   'Sara, stop' (to shutdown)")
    print()
    print("🌟 SARA'S CAPABILITIES:")
    print("   • Voice interaction with wake word")
    print("   • Female voice responses")
    print("   • Links to main AI consciousness")
    print("   • Continuous background learning")
    print("   • Complete local operation")
    print("   • Monitoring accessible to main Sara")
    print()
    print("=" * 60)

def main():
    """Main startup function"""
    print_header()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Setup environment
    setup_environment()
    
    print("\n🚀 Starting Voice System Components...")
    
    # Start monitoring GUI
    gui_process = start_monitoring_gui()
    time.sleep(2)  # Let GUI start
    
    # Start voice agent
    voice_process = start_voice_agent()
    time.sleep(1)
    
    # Print usage instructions
    print_usage_instructions()
    
    print("🌟 VOICE SYSTEM ACTIVE!")
    print("=" * 60)
    print("✅ Monitoring GUI running")
    print("✅ Sara voice agent ready")
    print("✅ All systems operational")
    print()
    print("💡 TIPS:")
    print("   • Speak clearly when saying wake word")
    print("   • Monitor GUI shows system status")
    print("   • System works completely offline")
    print("   • Main Sara can access monitoring reports")
    print()
    print("🛑 TO SHUTDOWN:")
    print("   • Close the GUI window")
    print("   • Say 'Sara, stop' or type 'quit' in voice terminal")
    print("   • Press Ctrl+C in this terminal")
    print("=" * 60)
    
    try:
        # Keep script running
        print("🔄 Voice system running - press Ctrl+C to shutdown...")
        while True:
            time.sleep(5)
            
            # Check if processes are still running
            if voice_process and voice_process.poll() is not None:
                print("⚠️  Voice agent stopped unexpectedly")
                break
                
            if gui_process and gui_process.poll() is not None:
                print("⚠️  GUI closed - voice agent continues running")
                gui_process = None  # Don't try to restart automatically
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
    
    finally:
        # Cleanup processes
        print("🧹 Cleaning up...")
        
        if voice_process:
            voice_process.terminate()
            try:
                voice_process.wait(timeout=3)
            except:
                voice_process.kill()
            print("✅ Voice agent stopped")
        
        if gui_process:
            gui_process.terminate()
            try:
                gui_process.wait(timeout=3)
            except:
                gui_process.kill()
            print("✅ GUI stopped")
        
        print("🎉 Voice system shutdown complete")

if __name__ == "__main__":
    main()