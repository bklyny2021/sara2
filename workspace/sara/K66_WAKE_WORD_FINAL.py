#!/usr/bin/env python3
# 🎯 FINAL K66 WAKE WORD SYSTEM - Working Structure Integration

import speech_recognition as sr
from pyttsx3 import init, speak
import time

print("🎤 K66 WAKE WORD SYSTEM - Your Working Structure Integration")
print("=" * 60)

# ==================== YOUR WORKING SETUP ====================

# Initialize the speech engine and set a female voice
engine = init()
voices = engine.getProperty("voices")

# Find female voice (Your approach)
female_voice_index = None
for i, voice in enumerate(voices):
    if 'female' in voice.name.lower() or 'female' in voice.id.lower():
        female_voice_index = i
        break

# Use female voice if found, otherwise use first available
if female_voice_index is not None:
    engine.setProperty("voice", voices[female_voice_index].id)
    print(f"✅ Female voice: {voices[female_voice_index].name}")
else:
    engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)
    print(f"✅ Voice: {voices[female_voice_index].id if len(voices) > 1 else voices[0].id}")

engine.setProperty("rate", 150)

# ==================== K66 MICROPHONE SETUP ====================

def setup_k66_microphone():
    """Find and setup K66 microphone"""
    recognizer = sr.Recognizer()
    mics = sr.Microphone.list_microphone_names()
    
    print("🔍 Scanning microphones...")
    k66_index = None
    
    for i, mic in enumerate(mics):
        print(f"  {i}: {mic}")
        if "K66" in mic:
            k66_index = i
            print(f"✅ K66 detected at index {i}")
            break
    
    if k66_index is not None:
        return sr.Microphone(device_index=k66_index)
    else:
        print("⚠️  K66 not found, using default microphone")
        return sr.Microphone()

# Test the microphone
def test_microphone(mic, recognizer):
    """Test microphone setup"""
    print("🎤 Testing microphone...")
    print("🎯 Please speak clearly now (testing for 3 seconds)...")
    
    try:
        with mic as source:
            print("🔧 Calibrating...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("🎤 Recording...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
        
        print("🧠 Processing...")
        text = recognizer.recognize_google(audio)
        print(f"✅ Recognized: '{text}'")
        return True, text
        
    except sr.UnknownValueError:
        print("❌ Could not understand speech")
        return False, None
    except sr.WaitTimeoutError:
        print("⏰ No speech detected")
        return False, None
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False, None

# ==================== WAKE WORD SYSTEM ====================

class WakeWordAgent:
    """Wake word detection and command processing"""
    
    def __init__(self, microphone, recognizer):
        self.wake_word = "sara"
        self.microphone = microphone
        self.recognizer = recognizer
        self.listening_for_commands = False
        self.running = True
        
        print(f"🎯 Wake word: '{self.wake_word}'")
        print(f"🎤 Microphone: {'K66' if 'K66' in str(microphone) else 'Default'}")
    
    def listen_for_wake_word(self):
        """Listen specifically for wake word"""
        print("👂 Listening for wake word...")
        
        try:
            with self.microphone as source:
                print("🎤 Speak now...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            user_input = self.recognizer.recognize_google(audio)
            print(f"🗣️ Heard: '{user_input}'")
            
            # Check for wake word
            if self.wake_word.lower() in user_input.lower():
                print("🎯 WAKE WORD DETECTED!")
                return True
                    
        except sr.UnknownValueError:
            print("🔇 Could not understand...")
            return False
        except sr.WaitTimeoutError:
            print("⏰ Timeout...")
            return False
        except Exception as e:
            print(f"❌ Listen error: {e}")
            return False
    
    def activate_command_mode(self):
        """Switch to active command mode"""
        print("🎧 Command mode activated")
        self.listening_for_commands = True
        speak("Yes, I'm listening! What can I help you with?")
        
    def deactivate_command_mode(self):
        """Return to wake word mode"""
        print("🔄 Back to wake word mode")
        self.listening_for_commands = False
        speak("I'll be listening for my wake word.")
    
    def process_command(self, command):
        """Process user command"""
        print(f"🧠 Processing: {command}")
        
        if "hello" in command.lower():
            response = "Hello! I'm Sara with voice recognition using K66 microphone!"
        elif "microphone" in command.lower():
            response = "I'm using the professional K66 USB-C microphone for perfect voice recognition!"
        elif "status" in command.lower():
            response = "K66 microphone working perfectly! Voice recognition active!"
        elif "stop" in command.lower() or "quit" in command.lower():
            response = "Goodbye! I'll be listening for my wake word."
            self.deactivate_command_mode()
            return False
        else:
            response = f"I heard: {command}. Voice recognition working great!"
        
        speak(response)
        return True
    
    def command_loop(self):
        """Process commands when activated"""
        timeout_counter = 0
        max_timeout = 30
        
        while self.listening_for_commands and self.running:
            if timeout_counter >= max_timeout:
                print("⏰ Command timeout")
                self.deactivate_command_mode()
                break
            
            print("🎧 Listening for commands...")
            
            try:
                with self.microphone as source:
                    print("🎤 Say your command...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                command = self.recognizer.recognize_google(audio)
                print(f"📝 Command: {command}")
                
                # Process command
                if command:
                    timeout_counter = 0
                    continue_command = self.process_command(command)
                    if not continue_command:
                        break
                else:
                    timeout_counter += 5
                    
            except sr.UnknownValueError:
                print("🔇 Could not understand command...")
                timeout_counter += 5
            except sr.WaitTimeoutError:
                timeout_counter += 5
            except Exception as e:
                print(f"❌ Command error: {e}")
                timeout_counter += 5

# ==================== MAIN SYSTEM ====================

def main():
    """Main voice system using your working structure"""
    print("=" * 60)
    print("🎤 K66 WAKE WORD SYSTEM")
    print("✅ Using your proven voice recognition structure")
    print("✅ K66 microphone integration")
    print("✅ Wake word detection")
    print("=" * 60)
    
    # Setup recognizer
    recognizer = sr.Recognizer()
    microphone = setup_k66_microphone()
    
    # Test microphone
    success, test_text = test_microphone(microphone, recognizer)
    
    if success:
        print(f"✅ Microphone test successful: '{test_text}'")
    else:
        print("❌ Microphone test failed - continuing anyway")
    
    # Create wake word agent
    agent = WakeWordAgent(microphone, recognizer)
    
    # Initial setup message
    speak("Voice recognition system activated. I'm listening for my wake word.")
    
    try:
        while agent.running:
            if not agent.listening_for_commands:
                # Wake word detection mode
                print("🎯 Wake word mode active")
                
                # Try to detect wake word multiple times
                wake_detected = agent.listen_for_wake_word()
                
                if wake_detected:
                    agent.activate_command_mode()
                    agent.command_loop()
                
            else:
                # Shouldn't happen but safety
                agent.listening_for_commands = False
            
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