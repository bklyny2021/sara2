#!/usr/bin/env python3
# 🎤 WORKING VOICE INTEGRATION - Your Code + K66 + Wake Word

import sys
import time
import speech_recognition as sr
from pyttsx3 import init, speak
import os
import sqlite3
import datetime

# ==================== YOUR WORKING SETUP ====================

# Initialize the speech engine and set a female voice
engine = init()
voices = engine.getProperty("voices")

# Try to find a female voice (Your approach)
female_voice_index = None
for i, voice in enumerate(voices):
    if 'female' in voice.name.lower() or 'female' in voice.id.lower():
        female_voice_index = i
        break

# Use female voice if found, otherwise use first available
if female_voice_index is not None:
    engine.setProperty("voice", voices[female_voice_index].id)
    print(f"✅ Female voice selected: {voices[female_voice_index].name}")
else:
    engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)
    print(f"✅ Using voice: {voices[1].id if len(voices) > 1 else voices[0].id}")

engine.setProperty("rate", 150)  # Adjust this value as needed

# Database setup (Your approach)
if not os.path.exists("userlog.db"):
    conn = sqlite3.connect("userlog.db")
    conn.close()
    print("✅ userlog.db created")

def save_to_database(question, answer):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("userlog.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS log (question text, answer text)""")
    c.execute("INSERT INTO log VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

# ==================== K66 INTEGRATION ====================

def get_k66_microphone():
    """Find K66 microphone specifically"""
    recognizer = sr.Recognizer()
    mics = sr.Microphone.list_microphone_names()
    
    print("🔍 Scanning microphones...")
    k66_index = None
    
    for i, mic in enumerate(mics):
        print(f"  {i}: {mic}")
        if "K66" in mic:
            k66_index = i
            print(f"✅ K66 found at index {i}")
            break
    
    if k66_index is not None:
        return sr.Microphone(device_index=k66_index)
    else:
        print("⚠️  K66 not found, using default microphone")
        return sr.Microphone()

# Test K66 connection
def test_k66_connection():
    """Test if K66 microphone is working"""
    print("🎤 Testing K66 microphone...")
    k66_mic = get_k66_microphone()
    recognizer = sr.Recognizer()
    
    try:
        with k66_mic as source:
            print("🔧 Calibrating...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("🎯 Say something to test K66 (3 seconds)...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
        print("🧠 Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ K66 recognized: '{text}'")
        return True
        
    except sr.UnknownValueError:
        print("❌ K66 couldn't understand speech")
        return False
    except sr.RequestError as e:
        print(f"❌ Recognition error: {e}")
        return False
    except Exception as e:
        print(f"❌ K66 test failed: {e}")
        return False

# ==================== WAKE WORD SYSTEM ====================

class WakeWordSystem:
    """Wake word detection using your working structure"""
    
    def __init__(self):
        self.wake_word = "sara"
        self.activated = False
        self.recognizer = sr.Recognizer()
        self.microphone = get_k66_microphone()
        
        print(f"🎯 Wake word system initialized")
        print(f"👂 Listening for: '{self.wake_word}'")
        print(f"🎤 Using microphone: {'K66' if 'K66' in str(self.microphone) else 'Default'}")
    
    def detect_wake_word(self):
        """Detect wake word in speech input"""
        print("👂 Listening for wake word...")
        
        try:
            with self.microphone as source:
                print("🎤 Wake word mode - speak now...")
                _audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            user_input = self.recognizer.recognize_google(_audio)
            print(f"🗣️ Heard: '{user_input}'")
            
            # Check for wake word
            if self.wake_word.lower() in user_input.lower():
                print("🎯 WAKE WORD DETECTED!")
                return True
            else:
                print(f"⚠️  Not wake word - waiting for '{self.wake_word}'")
                return False
                
        except sr.UnknownValueError:
            print("🔇 Could not understand - continuing...")
            return False
        except sr.RequestError as e:
            print(f"❌ Recognition error: {e}")
            return False
        except Exception as e:
            print(f"❌ Wake word error: {e}")
            return False
    
    def activate_command_mode(self):
        """Switch to active command processing"""
        print("🎧 Activating command mode...")
        self.activated = True
        speak("Yes, I'm listening! What can I help you with?")
        
    def deactivate_command_mode(self):
        """Return to wake word listening"""
        print("🔄 Returning to wake word mode...")
        self.activated = False
        speak("I'll be listening for my wake word.")
    
    def process_command(self, command):
        """Process user command using your structure"""
        print(f"🧠 Processing command: {command}")
        
        # Save to database (Your approach)
        save_to_database(command, "processed")
        
        # Command processing (Your logic)
        if "hello" in command.lower():
            response = "Hello! I'm Sara with voice recognition powered by K66 microphone!"
        elif "microphone" in command.lower():
            response = "I'm using the professional K66 USB-C microphone for perfect voice recognition!"
        elif "status" in command.lower():
            response = "Voice system K66 microphone is working perfectly! Wake word detection active!"
        elif "stop" in command.lower() or "quit" in command.lower():
            response = "Goodbye! I'll be listening for my wake word!"
            self.deactivate_command_mode()
            return False  # Signal to exit command mode
        else:
            response = f"I heard you say: {command}. K66 microphone is working great!"
        
        # Speak response
        speak(response)
        return True  # Continue command mode

# ==================== MAIN INTEGRATION ====================

def main():
    """Main voice system using your working structure + K66 + Wake word"""
    print("=" * 60)
    print("🎤 WORKING VOICE INTEGRATION SYSTEM")
    print("=" * 60)
    print("🎯 Wake word: 'sara'")
    print("🎙️  K66 microphone: Professional grade")
    print("🔊 Female voice: Active")
    print("🌐 Your recognition structure: Working")
    print("=" * 60)
    
    # Test K66 first
    print("🔍 Testing K66 microphone system...")
    if not test_k66_connection():
        print("❌ K66 test failed - trying default microphone")
        speak("K66 microphone test failed. Using default microphone.")
    else:
        print("✅ K66 microphone test passed!")
        speak("K66 microphone system operational.")
    
    # Initialize wake word system
    wake_system = WakeWordSystem()
    
    # Initial greeting
    speak("Voice recognition system activated. I'm listening for my wake word.")
    
    try:
        while True:
            if not wake_system.activated:
                # Wake word detection mode
                if wake_system.detect_wake_word():
                    wake_system.activate_command_mode()
                    
                    # Command processing loop
                    timeout_counter = 0
                    max_timeout = 30  # 30 seconds
                    
                    while wake_system.activated and timeout_counter < max_timeout:
                        print("🎧 Command mode - listening...")
                        
                        # Use same recognition structure as your code
                        try:
                            with wake_system.microphone as source:
                                print("🎤 Say your command...")
                                audio = wake_system.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                            
                            command = wake_system.recognizer.recognize_google(audio)
                            print(f"📝 Command: {command}")
                            
                            # Process command
                            continue_command = wake_system.process_command(command)
                            if not continue_command:
                                break  # Exit command mode
                            
                            timeout_counter = 0  # Reset timeout
                            
                        except sr.UnknownValueError:
                            print("🔇 Could not understand command...")
                            timeout_counter += 5
                        except sr.RequestError as e:
                            print(f"❌ Command recognition error: {e}")
                            timeout_counter += 5
                        except Exception as e:
                            print(f"❌ Command error: {e}")
                            timeout_counter += 5
                        
                        # Check timeout
                        if timeout_counter >= max_timeout:
                            print("⏰ Command timeout - returning to wake word mode")
                            wake_system.deactivate_command_mode()
                            break
                            
            else:
                # Brief pause
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
        speak("Voice system shutting down. Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        speak("Voice system error. Shutting down.")

if __name__ == "__main__":
    main()