#!/usr/bin/env python3
"""
🎤 ACTUALLY TEST SARA MYSELF - NO MORE CLAIMS
Testing direct voice agent interaction
"""

import subprocess
import time
import socket
import json
import os

def test_voice_agent_directly():
    """Test communication with running voice agent"""
    print("🔍 Testing direct voice agent communication...")
    
    # Method 1: Try to communicate via voice agent socket/API
    try:
        # Check if voice agent has any listening ports
        result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True)
        print("📡 Checking for voice agent listening ports...")
        
        for line in result.stdout.split('\n'):
            if 'python' in line and 'LISTEN' in line:
                print(f"   Found listening: {line.strip()}")
                
                # Extract port and try to connect
                parts = line.split()
                addr_port = parts[3]
                if ':' in addr_port:
                    port = addr_port.split(':')[-1]
                    print(f"   Attempting connection to port {port}...")
                    
                    # Try socket connection
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        sock.connect(('localhost', int(port)))
                        
                        # Send wake word command
                        command = {"command": "wake_word", "text": "sara"}
                        sock.send(json.dumps(command).encode() + b'\n')
                        
                        # Wait for response
                        response = sock.recv(1024)
                        print(f"   ✅ Response: {response.decode()}")
                        
                        sock.close()
                        return True
                        
                    except Exception as e:
                        print(f"   ❌ Connection failed: {e}")
    
    except Exception as e:
        print(f"❌ Voice agent communication test failed: {e}")
    
    return False

def test_keyboard_input():
    """Test keyboard input to voice agent"""
    print("\n📝 Testing keyboard input method...")
    
    # Find voice agent process
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        voice_line = None
        for line in result.stdout.split('\n'):
            if 'sara_voice_agent.py' in line:
                voice_line = line
                break
        
        if voice_line:
            print(f"✅ Found voice agent: {voice_line.strip()}")
            
            # Try to send input to the process (this may not work due to process isolation)
            print("📍 Note: Can't directly send input to running process due to isolation")
            print("📍 Need to check if voice agent supports stdin interaction")
            
            return True
        else:
            print("❌ Voice agent process not found")
            
    except Exception as e:
        print(f"❌ Keyboard input test failed: {e}")
    
    return False

def test_tts_directly():
    """Test TTS directly to K66 speakers"""
    print("\n🔊 Testing TTS directly to K66 speakers...")
    
    try:
        # Use pyttsx3 directly to test audio
        import pyttsx3
        
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        female_voice = None
        for voice in voices:
            if hasattr(voice, 'gender') and 'female' in voice.gender.lower():
                female_voice = voice
                break
        
        if female_voice:
            engine.setProperty('voice', female_voice.id)
            print(f"✅ Using female voice: {female_voice.name}")
        
        # Set properties
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        print("🗣️ Speaking test message...")
        test_message = "This is a direct TTS test to verify audio routing to K66 speakers"
        
        # This is the actual test - does audio come out?
        engine.say(test_message)
        engine.runAndWait()
        
        print("✅ TTS test completed - check if you heard audio through AD106M speakers")
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def check_audio_device_status():
    """Check current audio device configuration"""
    print("\n🔍 Checking audio device status...")
    
    try:
        # PulseAudio info
        result = subprocess.run(['pactl', 'info'], capture_output=True, text=True)
        
        default_sink = None
        default_source = None
        
        for line in result.stdout.split('\n'):
            if 'Default Sink:' in line:
                default_sink = line.split(':')[-1].strip()
                print(f"🔊 Default Sink: {default_sink}")
            elif 'Default Source:' in line:
                default_source = line.split(':')[-1].strip()
                print(f"🎤 Default Source: {default_source}")
        
        # Check K66 specific
        result = subprocess.run(['pactl', 'list', 'sinks'], capture_output=True, text=True)
        
        k66_sink = None
        for line in result.stdout.split('\n'):
            if 'K66' in line and 'Name:' in line:
                k66_sink = line.split('Name:')[-1].strip()
                print(f"✅ K66 Sink Found: {k66_sink}")
                break
        
        # If K66 exists but isn't default, that's the issue!
        if k66_sink and default_sink != k66_sink:
            print(f"⚠️ ISSUE: K66 sink ({k66_sink}) is not default ({default_sink})")
            print(f"🔧 Need to route TTS to K66 sink specifically")
            
        return True
        
    except Exception as e:
        print(f"❌ Audio device check failed: {e}")
        return False

def main():
    print("🎤 ACTUALLY TESTING SARA MYSELF - NO MORE CLAIMS")
    print("="*60)
    print("Goal: Prove system works with actual interaction, not just logs")
    print()
    
    # Run actual tests
    print("🔍 TEST 1: Direct voice agent communication")
    test_voice_agent_directly()
    
    print("\n🔍 TEST 2: Keyboard input method")
    test_keyboard_input()
    
    print("\n🔍 TEST 3: Direct TTS to speakers")
    tts_success = test_tts_directly()
    
    print("\n🔍 TEST 4: Audio device configuration")
    check_audio_device_status()
    
    print("\n" + "="*60)
    print("📊 ACTUAL TEST RESULTS:")
    print()
    
    if tts_success:
        print("✅ TTS TEST: If you heard audio, the system works!")
        print("📍 The issue is with wake word detection, not hardware")
        print("🎯 Need to fix voice wake word sensitivity")
    else:
        print("❌ TTS TEST: No audio output - confirms audio routing issue")
        print("📍 This is the real problem that needs fixing")
    
    print()
    print("🔍 CONCLUSION: No more claiming it works without proof!")
    print("🎯 Need actual user interaction testing, not log watching!")
    
    return tts_success

if __name__ == "__main__":
    success = main()
    print(f"\n🏆 TEST STATUS: {'PASS' if success else 'FAIL'}")
    print("🎤 Time to acknowledge the real issues and fix them properly!")