#!/usr/bin/env python3
# 🎯 Linux Voice Fix - Use ALSA + Your Working Windows Script Logic

import subprocess
import time
import sys
import os
from datetime import datetime
import sqlite3

# Note: On Linux, we'll use your speech logic but switch to ALSA + simpleaudio for audio
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
    print("✅ Speech recognition library available")
except ImportError:
    SPEECH_AVAILABLE = False
    print("❌ Speech recognition not available")

# For Linux audio output
try:
    import simpleaudio as sa
    SIMPLE_AUDIO_AVAILABLE = True
    print("✅ Simple audio playback available")
except ImportError:
    SIMPLE_AUDIO_AVAILABLE = False
    print("⚠️  Simple audio not available, using system tools")

# Fallback to system audio if needed
print("🔍 Setting up Linux voice system...")

class LinuxVoiceSystem:
    """Linux voice system using your working script structure"""
    
    def __init__(self):
        print("🎤 Initializing Linux Voice System...")
        print("=" * 50)
        print("🔧 Adapting your Windows script for Linux")
        print("🎯 Using K66 microphone + ALSA audio")
        print("🔊 Output to HDMI TV speakers")
        print("=" * 50)
        
        # Initialize components
        self.setup_speech_recognition()
        self.setup_audio_output()
        self.setup_database()
        
        # Wake word system
        self.wake_word = "sara"
        self.recognizer = None
        
        print("✅ Linux Voice System Ready!")
    
    def setup_speech_recognition(self):
        """Setup speech recognition using your Windows logic"""
        if not SPEECH_AVAILABLE:
            print("❌ Speech recognition not available")
            return False
        
        try:
            self.recognizer = sr.Recognizer()
            print("✅ Speech recognizer initialized")
            
            # Find K66 microphone using Linux approach
            mics = sr.Microphone.list_microphone_names()
            self.k66_index = None
            
            for i, mic in enumerate(mics):
                print(f"  {i}: {mic}")
                if "K66" in mic:
                    self.k66_index = i
                    print(f"✅ K66 found at index {i}")
                    break
            
            if self.k66_index is None:
                print("❌ K66 microphone not found")
                return False
            
            print("✅ K66 microphone location identified")
            return True
            
        except Exception as e:
            print(f"❌ Speech recognition setup failed: {e}")
            return False
    
    def setup_audio_output(self):
        """Setup audio output for Linux"""
        try:
            # Test HDMI audio output
            print("🔊 Testing HDMI audio output...")
            
            # Use ALSA to test audio
            test_result = self.test_hdmi_audio()
            if test_result:
                print("✅ HDMI audio working")
                self.audio_method = "alsa"
            else:
                print("⚠️  HDMI audio issue, will use fallback")
                self.audio_method = "system"
            
            return True
            
        except Exception as e:
            print(f"❌ Audio setup failed: {e}")
            return False
    
    def setup_database(self):
        """Setup database like your Windows script"""
        try:
            database_file = "userlog.db"
            
            if not os.path.exists(database_file):
                conn = sqlite3.connect(database_file)
                conn.execute("""CREATE TABLE log (question text, answer text)""")
                conn.close()
                print(f"✅ Created {database_file}")
            else:
                print(f"✅ {database_file} exists")
                
        except Exception as e:
            print(f"⚠️  Database setup issue: {e}")
    
    def test_hdmi_audio(self):
        """Test HDMI audio playback"""
        try:
            # Create a simple test tone or use system beep
            print("🎵 Testing audio playback...")
            
            # Test with system beep
            result = subprocess.run(['beep'], capture_output=True, timeout=3)
            if result.returncode == 0:
                print("✅ System audio working")
                return True
            
            # Alternative: Use aplay if available
            test_file = "/tmp/test_audio.wav"
            if not os.path.exists(test_file):
                # Create a simple test audio script
                subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1', 
                               test_file], capture_output=True, timeout=10)
            
            result = subprocess.run(['aplay', '-D', 'hw:0,3', test_file], 
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                print("✅ HDMI audio playback successful")
                return True
            
            return False
            
        except Exception as e:
            print(f"Audio test failed: {e}")
            return False
    
    def speak_with_alsa(self, text):
        """Speak using Linux audio system"""
        print(f"🔊 Speaking: {text}")
        
        try:
            # Method 1: Try system TTS + ALSA
            print("🎤 Using TTS + ALSA audio output...")
            
            # Create speech using system TTS
            temp_file = "/tmp/speech.wav"
            
            # Try festival if available
            festival_result = subprocess.run(['festival', '--tts'], 
                                         input=text, capture_output=True, text=True, timeout=10)
            if festival_result.returncode == 0:
                # Convert to WAV and play
                with open(temp_file, 'wb') as f:
                    f.write(festival_result.stdout)
                
                # Play through HDMI
                subprocess.run(['aplay', '-D', 'hw:0,3', temp_file], 
                             capture_output=True, timeout=10)
                print("✅ Festival + ALSA playback successful")
                return True
            
            # Method 2: Use pyttsx3 with ALSA
            import pyttsx3
            engine = pyttsx3.init()
            
            # Find female voice
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
            print("✅ pyttsx3 playback attempted")
            return True
            
        except Exception as e:
            print(f"❌ TTS playback failed: {e}")
            return False
    
    def speak_fallback(self, text):
        """Fallback speech method"""
        print(f"[SPEECH] {text}")
    
    def listen_with_k66(self, timeout=5):
        """Listen using K66 microphone on Linux"""
        if not SPEECH_AVAILABLE or self.recognizer is None:
            print("❌ Speech recognition not available")
            return None
        
        try:
            if self.k66_index is not None:
                mic = sr.Microphone(device_index=self.k66_index)
                print(f"🎤 Using K66 microphone at index {self.k66_index}")
            else:
                mic = sr.Microphone()
                print("🎤 Using default microphone")
            
            with mic as source:
                print("🔧 Calibrating...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                print(f"🎯 Say something (timeout {timeout}s)...")
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    print("⏰ No speech detected")
                    return None
                
                print("🧠 Processing speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"🗣️ Recognized: '{text}'")
                return text
                
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Listen error: {e}")
            return None
    
    def process_like_your_script(self, user_input):
        """Process using your Windows script logic"""
        print(f"🧠 Processing: {user_input}")
        
        # Save to database (your logic)
        try:
            self.save_to_database(user_input, "processed")
        except:
            pass
        
        # Command processing (your logic)
        user_input_lower = user_input.lower()
        
        if "hello" in user_input_lower or "hi" in user_input_lower:
            response = "Hello! I'm Sara running on Linux with K66 microphone and HDMI TV speakers!"
        elif "microphone" in user_input_lower:
            response = "I'm using the professional K66 USB-C microphone for perfect voice recognition on Linux!"
        elif "status" in user_input_lower:
            response = "Linux voice system: K66 microphone active, HDMI audio configured, wake word ready!"
        elif "linux" in user_input_lower:
            response = "I'm now running on Linux with your voice recognition logic adapted for K66 microphone!"
        elif "stop" in user_input_lower or "quit" in user_input_lower:
            response = "Goodbye! I'll be listening for my wake word on Linux!"
            return response, True  # Signal to exit command mode
        else:
            response = f"I heard: {user_input}. Linux voice recognition is working great with K66!"
        
        return response, False
    
    def save_to_database(self, question, answer):
        """Your database saving logic"""
        try:
            conn = sqlite3.connect("userlog.db")
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS log (question text, answer text)""")
            c.execute("INSERT INTO log VALUES (?, ?)", (question, answer))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database save failed: {e}")
    
    def run_your_script_structure(self):
        """Main loop using your Windows script structure for Linux"""
        print("🚀 Starting Linux Voice System")
        print("🔧 Using your working script structure adapted for Linux")
        print("=" * 60)
        
        # Initial greeting
        self.speak_with_alsa("Linux voice control system activated! I'm using K66 microphone with HDMI speakers. Say 'sara' to activate!")
        
        try:
            while True:
                # Listen continuously like your script
                user_input = self.listen_with_k66(timeout=10)
                
                if not user_input:
                    print("🔄 Continuing to listen...")
                    time.sleep(2)
                    continue
                
                print(f"You said: {user_input}")
                
                # Check for wake word (like your script logic)
                if self.wake_word.lower() in user_input.lower():
                    print("🎯 Wake word detected!")
                    self.speak_with_alsa("Yes, I'm listening! What can I help you with on Linux?")
                    
                    # Command mode (like your script)
                    command_timeout = 0
                    while command_timeout < 30:
                        print("🎧 Command mode active...")
                        command = self.listen_with_k66(timeout=5)
                        
                        if not command:
                            command_timeout += 5
                            continue
                        
                        print(f"Command: {command}")
                        
                        # Process command
                        response, should_exit = self.process_like_your_script(command)
                        
                        # Speak response
                        self.speak_with_alsa(response)
                        
                        if should_exit:
                            break
                        
                        command_timeout = 0  # Reset timeout
                
                elif "hello" in user_input.lower():
                    response, _ = self.process_like_your_script(user_input)
                    self.speak_with_alsa(response)
                
                # Brief pause to prevent CPU spinning
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested")
            self.speak_with_alsa("Linux voice system shutting down. Goodbye!")
        except Exception as e:
            print(f"❌ System error: {e}")

def main():
    """Main execution"""
    print("🎤 Linux Voice System (Adapted from Your Windows Script)")
    print("=" * 55)
    print("🔧 Your working voice recognition logic + Linux audio")
    print("🎯 K66 microphone + HDMI TV speakers")
    print("🌐 Local processing with your chat database")
    print("=" * 55)
    
    try:
        system = LinuxVoiceSystem()
        system.run_your_script_structure()
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()