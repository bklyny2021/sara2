#!/usr/bin/env python3
# 🎧 Linux Voice Final - Use Your Working Script + Linux Audio Chain

import speech_recognition as sr
import pyttsx3
import subprocess
import time
import sqlite3
import json

print("🎤 LINUX VOICE SYSTEM - Final Version")
print("=" * 50)
print("🔧 Using your working script structure")
print("🎤 K66 USB microphone + Linux audio chain")
print("🔊 HDMI TV speakers for output")
print("🎯 Adapting your Windows logic to Linux")
print("=" * 50)

class LinuxVoiceSystem:
    """Your voice recognition system adapted for Linux"""
    
    def __init__(self):
        print("🔄 Initializing Linux voice system...")
        
        # Setup components
        self.setup_speech_recognition()
        self.setup_tts()
        self.setup_database()
        
        # System state
        self.wake_word = "sara"
        self.running = True
        self.recognizer = sr.Recognizer()
        self.k66_index = self.find_k66_microphone()
        
        print("✅ Linux voice system ready!")
        print(f"🎤 Using K66 at index {self.k66_index}")
    
    def setup_speech_recognition(self):
        """Setup speech recognition like your script"""
        try:
            # Initialize recognizer (your approach)
            self.recognizer = sr.Recognizer()
            
            # Find K66 microphone
            mics = sr.Microphone.list_microphone_names()
            print(f"🔍 Found {len(mics)} microphones")
            
            for i, mic in enumerate(mics):
                print(f"  {i}: {mic}")
                if "K66" in mic:
                    self.k66_index = i
                    print(f"✅ K66 found at index {i}")
                    break
            
            if self.k66_index is None:
                print("❌ K66 microphone not found!")
                return False
            
            print("✅ Speech recognition setup complete")
            return True
            
        except Exception as e:
            print(f"❌ SR setup failed: {e}")
            return False
    
    def setup_tts(self):
        """Setup TTS with female voice (your method)"""
        try:
            self.engine = pyttsx3.init()
            
            # Find female voice (your approach)
            voices = self.engine.getProperty('voices')
            female_voice = None
            
            for voice in voices:
                if 'female' in voice.name.lower() or 'female' in voice.id.lower():
                    female_voice = voice
                    break
            
            if female_voice:
                self.engine.setProperty('voice', female_voice.id)
                print(f"✅ Female voice: {female_voice.name}")
            else:
                # Use first available voice
                if len(voices) > 0:
                    self.engine.setProperty('voice', voices[0].id)
                    print(f"✅ Voice: {voices[0].name}")
                else:
                    print("⚠️  No voices available")
                    return False
            
            # Set speaking rate (your settings)
            self.engine.setProperty('rate', 150)
            print("✅ TTS setup complete")
            return True
            
        except Exception as e:
            print(f"❌ TTS setup failed: {e}")
            return False
    
    def setup_database(self):
        """Setup database (your logic)"""
        try:
            db_file = "userlog.db"
            if not db_file in os.listdir('.'):
                conn = sqlite3.connect(db_file)
                conn.execute("""CREATE TABLE log (question text, answer text)""")
                conn.close()
                print("✅ Database created")
            else:
                print("✅ Database exists")
        except Exception as e:
            print(f"⚠️  Database setup: {e}")
    
    def find_k66_microphone(self):
        """Find K66 microphone index"""
        try:
            mics = sr.Microphone.list_microphone_names()
            for i, mic in enumerate(mics):
                if "K66" in mic:
                    return i
            return None
        except:
            return None
    
    def speak(self, text):
        """Speak text with TTS"""
        print(f"🔊 Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            print("✅ Speech completed")
        except Exception as e:
            print(f"❌ TTS failed: {e}")
            print(f"[TTS] {text}")
    
    def listen(self, timeout=5):
        """Listen for speech using K66"""
        if self.k66_index is None:
            print("❌ No microphone available")
            return None
        
        try:
            # Use K66 specifically
            mic = sr.Microphone(device_index=self.k66_index)
            print(f"🎤 Using K66 microphone (index {self.k66_index})")
            
            with mic as source:
                print("🔧 Calibrating...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("🎯 Speak now...")
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
                except sr.WaitTimeoutError:
                    print("⏰ No speech detected")
                    return None
                
                try:
                    text = self.recognize_google(audio)
                    print(f"🗣️ Recognized: '{text}'")
                    return text
                except sr.UnknownValueError:
                    print("❌ Could not understand speech")
                    return None
                except sr.RequestError as e:
                    print(f"❌ Recognition error: {e}")
                    return None
                    
        except Exception as e:
            print(f"❌ Listen error: {e}")
            return None
    
    def save_to_database(self, question, answer):
        """Save to database (your method)"""
        try:
            conn = sqlite3.connect("userlog.db")
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS log (question text, answer text)""")
            c.execute("INSERT INTO log VALUES (?, ?)", (question, answer))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database save failed: {e}")
    
    def process_command(self, user_input):
        """Process command (your logic adapted for Linux)"""
        print(f"🧠 Processing: {user_input}")
        
        # Save to database
        self.save_to_database(user_input, "processed")
        
        user_lower = user_input.lower()
        
        # Your command logic + Linux adaptations
        if "hello" in user_lower or "hi" in user_lower:
            response = "Hello! I'm Sara running on Linux with K66 microphone and HDMI TV speakers!"
        elif "microphone" in user_lower:
            response = "I'm using the professional K66 USB-C microphone, working perfectly on Linux!"
        elif "status" in user_lower:
            response = "Linux voice system active: K66 recording, HDMI speakers, wake word ready!"
        elif "linux" in user_lower:
            response = "I've adapted your Windows voice script to work perfectly on Linux with K66!"
        elif "sara" in user_lower and len(user_input.split()) == 1:
            response = "You activated me! I'm Sara, your voice-activated AI assistant on Linux!"
        elif "stop" in user_lower or "quit" in user_lower:
            response = "Goodbye! I'll be listening for my wake word!"
            return response, True
        else:
            response = f"I heard: {user_input}. Linux voice recognition working great!"
        
        return response, False
    
    def main_loop(self):
        """Main loop using your script structure"""
        print("🚀 Starting Linux voice system...")
        print("🎯 Wake word: 'sara'")
        print("🎤 K66 microphone input")
        print("🔊 HDMI TV speaker output")
        print("=" * 50)
        
        # Initial greeting
        self.speak("Linux voice recognition system activated! I'm using K66 microphone with HDMI TV speakers. Say 'sara' to activate!")
        
        try:
            while self.running:
                print("👂 Listening continuously...")
                user_input = self.listen(timeout=10)
                
                if not user_input:
                    print("🔄 Continuing to listen...")
                    time.sleep(2)
                    continue
                
                print(f"You said: {user_input}")
                
                # Check for wake word (like your script)
                if self.wake_word.lower() in user_input.lower():
                    print("🎯 Wake word detected!")
                    self.speak("Yes, I'm listening! What can I help you with?")
                    
                    # Command mode (your structure)
                    command_timeout = 0
                    while command_timeout < 30:
                        print("🎧 Command mode active...")
                        command = self.listen(timeout=5)
                        
                        if not command:
                            command_timeout += 5
                            continue
                        
                        print(f"Command: {command}")
                        
                        # Process command
                        response, should_exit = self.process_command(command)
                        
                        # Speak response
                        self.speak(response)
                        
                        if should_exit:
                            print("Exiting command mode")
                            break
                        
                        command_timeout = 0  # Reset timeout
                
                elif "hello" in user_input.lower():
                    response, _ = self.process_command(user_input)
                    self.speak(response)
                
                # Brief pause
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested")
            self.speak("Linux voice system shutting down. Goodbye!")
        except Exception as e:
            print(f"❌ System error: {e}")
            self.speak("Voice system error. Shutting down.")

def main():
    """Main execution"""
    print("🎤 LINUX VOICE SYSTEM")
    print("🔧 Your Windows voice script adapted for Linux")
    print("🎤 K66 USB-C professional microphone")
    print("🔊 HDMI TV speaker output")
    print("=" * 45)
    
    try:
        system = LinuxVoiceSystem()
        system.main_loop()
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()