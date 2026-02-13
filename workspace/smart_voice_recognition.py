#!/usr/bin/env python3
"""
🎤 Voice Recognition with Smart Mic Management
Only activates microphone when listening for commands
"""
import subprocess
import time
import speech_recognition as sr
import sys
import json
import os

class SmartVoiceRecognizer:
    """Speech recognition with intelligent mic control"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.mic_device = "alsa_input.usb-K66_K66_20190805V001-00.analog-stereo"
        self.listening = False
        self.mic_enabled = False
    
    def enable_microphone(self):
        """Enable microphone for listening"""
        if not self.mic_enabled:
            try:
                # Unmute and resume the microphone
                subprocess.run(['pactl', 'set-source-mute', self.mic_device, 'false'], 
                             check=False)
                subprocess.run(['pactl', 'suspend-source', self.mic_device, 'false'], 
                             check=False)
                self.mic_enabled = True
                print("🎤 Microphone activated")
            except Exception as e:
                print(f"⚠️ Mic activation issue: {e}")
    
    def disable_microphone(self):
        """Disable microphone after listening"""
        if self.mic_enabled:
            try:
                # Mute and suspend the microphone to save resources
                subprocess.run(['pactl', 'set-source-mute', self.mic_device, 'true'], 
                             check=False)
                subprocess.run(['pactl', 'suspend-source', self.mic_device, 'true'], 
                             check=False)
                self.mic_enabled = False
                print("🔇 Microphone disabled")
            except Exception as e:
                print(f"⚠️ Mic disable issue: {e}")
    
    def setup_microphone(self):
        """Setup microphone with proper device selection"""
        try:
            # Get microphone with specific device
            mic_list = sr.Microphone.list_microphone_names()
            print(f"🎤 Available microphones: {mic_list}")
            
            # Find our K66 microphone
            k66_index = None
            for i, name in enumerate(mic_list):
                if "K66" in name or "USB" in name:
                    k66_index = i
                    break
            
            if k66_index is not None:
                self.microphone = sr.Microphone(device_index=k66_index)
                print(f"✅ Using K66 microphone (index {k66_index})")
            else:
                # Fall back to default
                self.microphone = sr.Microphone()
                print("⚠️ Using default microphone")
                
        except Exception as e:
            print(f"❌ Microphone setup failed: {e}")
            return False
        
        return True
    
    def listen_for_command(self, timeout=5):
        """Listen for a single command with smart mic management"""
        try:
            print("🎤 Starting to listen...")
            
            # Enable microphone only when needed
            self.enable_microphone()
            self.listening = True
            
            # Adjust for ambient noise quickly
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for command
            with self.microphone as source:
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                    
                    # Immediately disable mic after capturing
                    self.disable_microphone()
                    self.listening = False
                    
                    # Process the audio
                    try:
                        text = self.recognizer.recognize_google(audio)
                        print(f"🗣️ You said: {text}")
                        return text.upper()  # Return uppercase for consistency
                        
                    except sr.UnknownValueError:
                        print("🤷 Sorry, didn't catch that")
                        return None
                        
                    except sr.RequestError as e:
                        print(f"🔌 Speech service error: {e}")
                        return None
                        
                except sr.WaitTimeoutError:
                    print("⏰ Listening timeout")
                    self.disable_microphone()
                    self.listening = False
                    return None
                    
        except Exception as e:
            print(f"❌ Listening error: {e}")
            self.disable_microphone()
            self.listening = False
            return None
        finally:
            # Always ensure mic is disabled
            self.disable_microphone()
            self.listening = False
    
    def cleanup(self):
        """Clean up and ensure mic is disabled"""
        self.disable_microphone()
        print("🔹 Voice recognizer cleaned up")

def test_smart_mic():
    """Test the smart microphone system"""
    print("🎤 Testing Smart Voice Recognition")
    print("=" * 40)
    
    recognizer = SmartVoiceRecognizer()
    
    # Setup microphone
    if not recognizer.setup_microphone():
        print("❌ Failed to setup microphone")
        return False
    
    print("✅ Microphone setup complete")
    print("🎤 Say something (mic will activate only when listening)...")
    
    try:
        # Test listening
        result = recognizer.listen_for_command(timeout=10)
        
        if result:
            print(f"✅ Successfully heard: {result}")
            return True
        else:
            print("⚠️ No speech detected")
            return False
            
    finally:
        recognizer.cleanup()
    
    return True

if __name__ == "__main__":
    success = test_smart_mic()
    if success:
        print("🎉 Smart mic test successful!")
    else:
        print("⚠️ Smart mic test had issues")
    
    sys.exit(0 if success else 1)