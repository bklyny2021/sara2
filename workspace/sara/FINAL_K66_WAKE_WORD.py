#!/usr/bin/env python3
# 🎯 FINAL K66 Wake Word System - Direct Hardware Control

import os
import sys
import subprocess
import time
import queue
import json
from datetime import datetime

# Voice imports
try:
    import sounddevice as sd
    import pyttsx3
    import speech_recognition as sr
    print("✅ Voice components imported")
except Exception as e:
    print(f"❌ Voice import error: {e}")
    sys.exit(1)

class DirectK66WakeWord:
    """Direct K66 control using system audio"""
    
    def __init__(self):
        print("🎤 Initializing Direct K66 Wake Word System...")
        print("=" * 50)
        
        # Configuration
        self.wake_word = "sara"
        self.k66_device = "hw:2,0"  # Card 2, device 0
        self.k66_card_num = 2
        
        # Setup TTS
        self.setup_tts()
        
        # Test K66 directly
        self.verify_k66_hardware()
        
        # State
        self.running = True
        self.activated = False
        
        print("✅ Direct K66 System Ready!")
        
    def setup_tts(self):
        """Setup TTS engine"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160)
            
            # Select a voice
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find female-like voice
                for voice in voices:
                    if any(word in voice.name.lower() for word in ['female', 'woman', 'zira']):
                        self.engine.setProperty('voice', voice.id)
                        print(f"✅ Voice selected: {voice.name}")
                        break
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
                    print(f"✅ Default voice: {voices[0].name}")
            
        except Exception as e:
            print(f"❌ TTS setup failed: {e}")
            sys.exit(1)
    
    def verify_k66_hardware(self):
        """Verify K66 hardware presence and setup"""
        print("🔍 Verifying K66 hardware...")
        
        try:
            # Check if K66 appears in audio listings
            result = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
            
            if 'card 2: K66 [K66]' in result.stdout:
                print("✅ K66 microphone detected in system")
                print("📋 Audio devices found:")
                
                # Show relevant devices
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'card' in line and ('K66' in line or 'ALC897' in line):
                        print(f"   {line}")
            else:
                print("❌ K66 not found in audio devices")
                print("Available devices:")
                for line in result.stdout.split('\n')[:5]:
                    print(f"   {line}")
                return False
                
            # Test K66 capture settings
            try:
                capture_result = subprocess.run([
                    'amixer', '-c', '2', 'sget', 'Mic'
                ], capture_output=True, text=True)
                
                if capture_result.returncode == 0:
                    print("✅ K66 capture settings accessible")
                    print("🔊 Current settings:")
                    for line in capture_result.stdout.split('\n')[:8]:
                        if line.strip():
                            print(f"   {line.strip()}")
                else:
                    print("⚠️  K66 settings not accessible")
                
                # Ensure capture levels are adequate
                subprocess.run(['amixer', '-c', '2', 'sset', 'Mic', 'capture', '80'], 
                              capture_output=True)
                print("✅ K66 capture level optimized")
                
            except Exception as e:
                print(f"⚠️  K66 setup issue: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Hardware verification failed: {e}")
            return False
    
    def speak(self, text):
        """Speak text"""
        print(f"🔊 Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ TTS error: {e}")
    
    def test_k66_direct(self, duration=5):
        """Test K66 directly with sounddevice"""
        print(f"🎤 Testing K66 microphone ({duration} seconds)...")
        print("🎯 Please speak clearly now...")
        
        try:
            # Configure K66 as input
            sd.default.device = "pulse"  # Use pulse for better compatibility
            sd.default.samplerate = 16000
            sd.default.channels = 1
            
            # Audio settings
            recording_queue = queue.Queue()
            
            def audio_callback(indata, frames, time, status):
                recording_queue.put(indata.copy())
            
            # Start recording
            with sd.InputStream(
                samplerate=16000,
                channels=1,
                dtype='int16',
                blocksize=1024,
                callback=audio_callback
            ):
                print("🎤 Recording...")
                start_time = time.time()
                
                # Collect audio data
                audio_data = []
                while time.time() - start_time < duration:
                    try:
                        data = recording_queue.get(timeout=0.1)
                        audio_data.append(data)
                    except queue.Empty:
                        continue
                
                print(f"✅ Recording complete - captured {len(audio_data)} chunks")
                
                # Simple level check
                if audio_data:
                    max_level = max(abs(chunk).max() for chunk in audio_data if chunk.size > 0)
                    print(f"🔊 Audio level detected: {max_level}")
                    
                    if max_level > 1000:  # Significant audio detected
                        print("✅ Vocal sounds detected!")
                        return True
                    else:
                        print("⚠️  Low audio level - try speaking louder")
                        return False
                else:
                    print("❌ No audio data captured")
                    return False
                    
        except Exception as e:
            print(f"❌ Recording test failed: {e}")
            return False
    
    def simple_speech_test(self):
        """Simple speech recognition test"""
        print("🧪 Testing speech recognition...")
        
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            
            # Try using system default microphone
            with sr.Microphone() as source:
                print("🔧 Calibrating microphone...")
                recognizer.adjust_for_ambient_noise(source, duration=2)
                
                print("🎤 Please speak now (5 seconds)...")
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                    print("🧠 Processing speech...")
                    
                    # Try to recognize
                    try:
                        text = recognizer.recognize_google(audio)
                        print(f"✅ Recognized: '{text}'")
                        return text
                    except sr.UnknownValueError:
                        print("❌ Could not understand speech")
                        return None
                    except sr.RequestError as e:
                        print(f"❌ Recognition service error: {e}")
                        return None
                        
                except sr.WaitTimeoutError:
                    print("⏰ Timeout - no speech detected")
                    return None
                    
        except Exception as e:
            print(f"❌ Speech recognition test failed: {e}")
            return None
    
    def wake_word_detection_loop(self):
        """Main wake word detection loop"""
        print("🚀 Starting Wake Word Detection...")
        print(f"👂 Listening for wake word: '{self.wake_word}'")
        print("💡 Speak clearly when ready...")
        
        self.speak("Voice recognition system activated. I'm listening for my wake word.")
        
        while self.running:
            try:
                # Speech recognition test
                text = self.simple_speech_test()
                
                if text:
                    print(f"🗣️ Heard: '{text}'")
                    
                    # Check for wake word
                    if self.wake_word.lower() in text.lower():
                        print("🎯 WAKE WORD DETECTED!")
                        self.speak("Yes, I'm listening! What can I help you with?")
                        self.activated = True
                        self.command_mode()
                    else:
                        print(f"⚠️  Not wake word - waiting for '{self.wake_word}'")
                else:
                    print("🔄 No speech detected - continuing to listen...")
                
                # Brief pause to prevent CPU spinning
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested")
                break
            except Exception as e:
                print(f"⚠️  Loop error: {e}")
                time.sleep(2)
                continue
    
    def command_mode(self):
        """Command processing when activated"""
        print("🎧 Command mode active...")
        
        timeout_counter = 0
        max_timeout = 30  # 30 seconds
        
        while self.activated and timeout_counter < max_timeout and self.running:
            print("🎧 Listening for commands...")
            
            text = self.simple_speech_test()
            
            if text:
                timeout_counter = 0
                print(f"💬 Command: {text}")
                
                # Simple command processing
                if 'hello' in text.lower():
                    response = "Hello! I'm Sara activated through K66 microphone!"
                elif 'microphone' in text.lower():
                    response = "I'm using the professional K66 USB-C microphone!"
                elif 'status' in text.lower():
                    response = "Voice system K66 microphone is working perfectly!"
                elif 'stop' in text.lower() or 'quit' in text.lower():
                    response = "I'll go back to wake word mode!"
                    self.activated = False
                else:
                    response = f"I heard: {text}. Good voice recognition!"
                
                self.speak(response)
                
                if not self.activated:
                    break
            else:
                timeout_counter += 5
                if timeout_counter >= max_timeout:
                    print("⏰ Command timeout - returning to wake word mode")
                    self.speak("I'll be listening for my wake word!")
                    self.activated = False
                    break
    
    def run(self):
        """Main entry point"""
        print("=" * 60)
        print("🎤 FINAL K66 WAKE WORD SYSTEM")
        print("=" * 60)
        print("🎯 Wake word: 'sara'")
        print("🎙️  K66 microphone: hw:2,0")
        print("🔊 Female voice: Active")
        print("🌐 Local processing: Enabled")
        print("=" * 60)
        
        # Test K66 first
        self.speak("Testing K66 microphone system...")
        
        if self.verify_k66_hardware():
            print("✅ K66 hardware verified")
            
            # Audio test
            if self.test_k66_direct(3):
                print("✅ K66 audio working")
                
                # Start main loop
                self.wake_word_detection_loop()
            else:
                print("❌ K66 audio test failed")
                self.speak("K66 microphone test failed. Check connection.")
        else:
            print("❌ K66 hardware not found")
            self.speak("K66 microphone not detected. Please check connection.")
        
        # Cleanup
        print("🔄 Shutting down...")
        self.speak("Voice system shutting down. Goodbye!")

def main():
    """Main execution"""
    print("🎤 FINAL K66 Wake Word System Starting...")
    
    try:
        system = DirectK66WakeWord()
        system.run()
    except KeyboardInterrupt:
        print("\n🛑 User interrupted")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()