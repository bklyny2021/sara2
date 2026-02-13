#!/usr/bin/env python3
# 🎤 Quick Voice System Start

import subprocess
import sys
import os

def start_voice_agent():
    """Start Sara voice agent"""
    print("🎤 Starting Sara Voice Agent...")
    try:
        agent = subprocess.Popen([
            sys.executable,
            "/home/godfather/local-command-center/agents/sara-voice/sara_voice_agent.py"
        ])
        print(f"✅ Voice Agent Started (PID: {agent.pid})")
        return agent
    except Exception as e:
        print(f"❌ Voice Agent failed: {e}")
        return None

def start_gui():
    """Start monitoring GUI"""
    print("🖥️ Starting Monitoring GUI...")
    try:
        gui = subprocess.Popen([
            sys.executable,
            "/home/godfather/local-command-center/simple_gui.py"
        ])
        print(f"✅ GUI Started (PID: {gui.pid})")
        return gui
    except Exception as e:
        print(f"❌ GUI failed: {e}")
        return None

def main():
    print("🚀 QUICK VOICE SYSTEM START")
    print("=" * 40)
    
    agent = start_voice_agent()
    gui = start_gui()
    
    if agent and gui:
        print("\n✅ Voice System Active!")
        print("🎤 Sara is listening for 'Sara' wake word")
        print("🖥️ Monitoring GUI is running")
        print("💬 Type 'sara' in terminal if voice doesn't work")
        print("\nPress Ctrl+C to shutdown")
        
        try:
            input()  # Wait for user input
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            if agent: agent.terminate()
            if gui: gui.terminate()
            print("✅ Shutdown complete")
    else:
        print("❌ Failed to start system")

if __name__ == "__main__":
    main()