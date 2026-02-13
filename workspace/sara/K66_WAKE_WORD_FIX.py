#!/usr/bin/env python3
# 🎤 K66 Wake Word Fix - Use Your Working Code Structure

import os
import sys
import subprocess
import time
import queue
import json
import datetime
import pytz
import re
import threading

# Import your working voice code components
try:
    import sounddevice as sd
    import pyttsx3
    import speech_recognition as sr
    from vosk import Model, KaldiRecognizer
    print("✅ All voice components imported successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class K66WakeWordSystem:
    """Properly integrated K66 wake word system using your working code"""
    
    def __init__(self):
        print("🎤 Initializing K66 Wake Word System...")
        
        # Configuration
        self.wake_word = "sara"
        self.vosk_model_path = "vosk-model-small-en-us-0.15"
        self.conversation_log_file = "conversation_context_log.txt"
        
        # Initialize components
        self.setup_vosk()
        self.setup_tts()
        self.setup_audio_queue()
        
        # Conversation state
        self.conversation_history = []
        self.running = True
        self.listening_mode = False  # Wake word detection vs command mode
        
        print("✅ K66 Wake Word System Ready!")
        
    def setup_vosk(self):
        """Setup Vosk speech recognition (from your working code)"""
        print("🔧 Setting up Vosk model...")
        
        if not os.path.isdir(self.vosk_model_path):
            print(f"⚠️  Vosk model folder '{self.vosk_model_path}' not found")
            print("💡 Need to download and extract Vosk model first")
            sys.exit(1)
        
        try:
            self.model_sr = Model(self.vosk_model_path)
            self.rec = KaldiRecognizer(self.model_sr, 16000)
            print("✅ Vosk model loaded")
        except Exception as e:
            print(f"❌ Vosk setup failed: {e}")
            sys.exit(1)
    
    def setup_tts(self):
        """Setup Text-to-Speech (from your working code)"""
        print("🔊 Setting up TTS...")
        
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            
            # Female voice selection (your approach)
            voices = self.engine.getProperty('voices')
            selected_voice = None
            
            for voice in voices:
                if 'female' in voice.name.lower() or 'female' in voice.id.lower():
                    selected_voice = voice.id
                    break
            
            if not selected_voice and voices:
                selected_voice = voices[0].id
            
            if selected_voice:
                self.engine.setProperty('voice', selected_voice)
                print(f"✅ Female voice configured: {selected_voice}")
            else:
                print("⚠️  No female voice found, using default")
                
        except Exception as e:
            print(f"❌ TTS setup failed: {e}")
            sys.exit(1)
    
    def setup_audio_queue(self):
        """Setup audio processing queue (from your working code)"""
        print("🎙️  Setting up audio queue...")
        
        self.q = queue.Queue()
        self.audio_callback = lambda indata, frames, time, status: self.q.put(bytes(indata))
        
        print("✅ Audio queue configured")
    
    def recognize_speech(self, timeout=10):
        """Recognize speech using Vosk (your working method)"""
        print("🎤 Speak now...")
        
        try:
            with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            ):
                result_text = ""
                start_time = time.time()
                
                while True:
                    if time.time() - start_time > timeout:
                        print("⏰ Timeout, no speech detected")
                        return None
                    
                    try:
                        data = self.q.get(timeout=1)
                    except queue.Empty:
                        continue
                    
                    if self.rec.AcceptWaveform(data):
                        res = json.loads(self.rec.Result())
                        result_text = res.get('text', '')
                        if result_text.strip():
                            print(f"🗣️ Recognized: '{result_text}'")
                            return result_text.lower()
                
        except Exception as e:
            print(f"❌ Speech recognition error: {e}")
            return None
    
    def speak(self, text):
        """Speak text using TTS with formatting (your method)"""
        print(f"🔊 Speaking: {text}")
        
        try:
            # Add pauses for punctuation (your method)
            spoken_text = text.split('...')[-1].strip() if '...' in text else text
            spoken_text = re.sub(r'(\.|,)', r'. ', spoken_text)
            spoken_text = re.sub(r'[^A-Za-z0-9\. ]+', '', spoken_text)
            
            self.engine.say(spoken_text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
    
    def check_wake_word(self, text):
        """Check if wake word is detected"""
        if text and self.wake_word in text.lower():
            print("🎯 WAKE WORD DETECTED!")
            return True
        return False
    
    def activate_listening_mode(self):
        """Switch to active listening mode"""
        print("👂 Switching to active listening mode...")
        self.listening_mode = True
        self.speak("Yes, I'm listening! What can I help you with?")
    
    def deactivate_listening_mode(self):
        """Switch back to wake word detection"""
        print("👂 Switching to wake word detection mode...")
        self.listening_mode = False
        self.speak("Let me know if you need anything else!")
    
    def process_command(self, command):
        """Process voice command"""
        print(f"🧠 Processing command: {command}")
        
        # Simple command processing
        if 'hello' in command.lower() or 'hi' in command.lower():
            response = "Hello! I'm Sara with voice recognition powered by K66 microphone!"
        elif 'what can you do' in command.lower():
            response = "I can hear you through the K66 microphone, process your voice, and respond with my female voice!"
        elif 'microphone' in command.lower():
            response = "I'm using the professional K66 USB-C microphone for perfect voice recognition!"
        elif 'stop' in command.lower() or 'quit' in command.lower():
            response = "Goodbye! I'll be listening for your wake word!"
            self.deactivate_listening_mode()
        else:
            response = f"I heard you say: {command}. Let me help you with that!"
        
        return response
    
    def main_loop(self):
        """Main wake word detection loop"""
        print("🚀 Starting K66 Wake Word System...")
        print(f"👂 Listening for wake word: '{self.wake_word}'")
        
        self.speak("Voice recognition system activated. I'm listening for your wake word.")
        
        while self.running:
            if not self.listening_mode:
                # Wake word detection mode
                print("🎯 Wake word mode - listening...")
                text = self.recognize_speech(timeout=60)
                
                if text and self.check_wake_word(text):
                    self.activate_listening_mode()
                    self.command_loop()
            else:
                print("⚠️  Should not be here!")
                self.listening_mode = False
    
    def command_loop(self):
        """Command processing loop when activated"""
        timeout_counter = 0
        max_timeout = 30  # 30 seconds of inactivity returns to wake word mode
        
        while self.listening_mode and self.running and timeout_counter < max_timeout:
            print("🎧 Command mode - listening for commands...")
            text = self.recognize_speech(timeout=5)
            
            if text:
                timeout_counter = 0  # Reset timeout
                
                # Process command
                response = self.process_command(text)
                self.speak(response)
                
                # Check if command ended the listening mode
                if not self.listening_mode:
                    break
            else:
                timeout_counter += 5
                if timeout_counter >= max_timeout:
                    print("⏰ Timeout, returning to wake word mode...")
                    self.speak("I'll be listening for your wake word!")
                    self.listening_mode = False
                    break
    
    def run(self):
        """Main entry point"""
        try:
            print("=" * 50)
            print("🎤 K66 WAKE WORD SYSTEM")
            print("=" * 50)
            print("🎯 Wake word: 'sara'")
            print("🎙️  K66 microphone active")
            print("🔊 Female voice ready")
            print("🌐 Local processing")
            print("=" * 50)
            
            self.main_loop()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested")
            self.running = False
            self.speak("Voice system shutting down. Goodbye!")
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            self.running = False

def main():
    """Main execution"""
    try:
        # Check if K66 microphone is available
        print("🔍 Checking K66 microphone...")
        
        # Test speech recognition with K66
        recognizer = sr.Recognizer()
        mics = sr.Microphone.list_microphone_names()
        
        k66_found = False
        for i, mic in enumerate(mics):
            if "K66" in mic:
                print(f"✅ K66 found at index {i}: {mic}")
                k66_found = True
                break
        
        if not k66_found:
            print("❌ K66 microphone not found!")
            available_mics = [mic for mic in mics[:5]]
            print(f"Available microphones: {available_mics}")
            print("⚠️  Ensure K66 is connected and recognized by system")
            return
        
        # Start wake word system
        system = K66WakeWordSystem()
        system.run()
        
    except Exception as e:
        print(f"❌ Main error: {e}")

if __name__ == "__main__":
    main()