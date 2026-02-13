#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def check_audio_status():
    """Check audio system status"""
    print("🔊 AUDIO STATUS CHECK")
    print("=" * 25)
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check default sink
    try:
        result = subprocess.run(['pactl', 'get-default-sink'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            default_sink = result.stdout.strip()
            print(f"📍 Default sink: {default_sink}")
        else:
            print("❌ Could not get default sink")
    except:
        print("⚠️  Default sink check failed")
    
    # Check sink states
    try:
        result = subprocess.run(['pactl', 'list', 'sinks'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            active_sinks = 0
            for line in lines:
                if 'State: SUSPENDED' in line:
                    pass
                elif 'State: ' in line:
                    active_sinks += 1
            print(f"🎤 Active sinks: {active_sinks}")
    except:
        print("⚠️  Sink status check failed")
    
    # Test quick audio
    try:
        result = subprocess.run(['paplay', '/usr/share/sounds/alsa/Front_Left.wav'],
                              capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print("✅ Audio playback: WORKING")
        else:
            print("❌ Audio playback: FAILED")
    except Exception as e:
        print(f"❌ Audio test error: {e}")
    
    print()
    print("🎯 QUICK FIX IF NEEDED:")
    print("pactl set-default-sink alsa_output.pci-0000_01_00.1.pro-output-3")
    print("pactl suspend-sink [sink_id] false")
    print()

if __name__ == "__main__":
    check_audio_status()
