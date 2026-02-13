#!/usr/bin/env python3
# 🧠 Sara AI-Connected Voice Agent

import subprocess
import logging
import json
import time
import sys
import os

# Add OpenClaw to path
sys.path.append("/home/godfather/.npm-global/lib/node_modules/openclaw")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/local-command-center/logs/intelligent_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import voice components
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
    logger.info("✅ SpeechRecognition available")
except ImportError as e:
    SPEECH_AVAILABLE = False
    logger.error(f"❌ SpeechRecognition not available: {e}")

try:
    import pyttsx3
    TTS_AVAILABLE = True
    logger.info("✅ TTS available")
except ImportError as e:
    TTS_AVAILABLE = False
    logger.error(f"❌ TTS not available: {e}")

class IntelligentVoiceSara:
    """Voice agent connected to Sara AI consciousness"""
    
    def __init__(self):
        logger.info("🧠 Initializing Intelligent Voice Sara...")
        
        # Load configuration
        try:
            with open("/home/godfather/local-command-center/config/voice_config.json") as f:
                self.config = json.load(f)
        except Exception as e:
            logger.error(f"Config load failed: {e}")
            self.config = {}
        
        # Setup voice components
        self.setup_voice_components()
        
        # Initialize state
        self.wake_word = "sara"
        self.running = True
        
        logger.info("✅ Intelligent Voice Sara initialized!")
        logger.info(f"🎤 Speech: {'Available' if SPEECH_AVAILABLE else 'Keyboard'}")
        logger.info(f"🔊 Voice: {'Available' if TTS_AVAILABLE else 'Text'}")
        
        if TTS_AVAILABLE:
            self.speak("Intelligent voice system activated. I'm connected to Sara's AI consciousness!")
    
    def setup_voice_components(self):
        """Setup voice recognition and TTS"""
        if SPEECH_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.pause_threshold = 0.8
                
                # Find K66 microphone
                mics = sr.Microphone.list_microphone_names()
                k66_index = None
                for i, mic in enumerate(mics):
                    if "K66" in mic:
                        k66_index = i
                        break
                
                self.microphone = sr.Microphone(device_index=k66_index)
                logger.info(f"✅ K66 microphone configured")
            except Exception as e:
                logger.error(f"Voice setup failed: {e}")
                self.microphone = None
        else:
            self.microphone = None
    
    def speak(self, text):
        """Speak text using TTS"""
        if TTS_AVAILABLE:
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 140)
                engine.setProperty('volume', 0.85)
                engine.say(text)
                engine.runAndWait()
                logger.info(f"🔊 Spoke: {text}")
            except Exception as e:
                logger.error(f"TTS failed: {e}")
                print(f"[TTS] {text}")
        else:
            print(f"[TTS] {text}")
    
    def listen(self):
        """Listen for voice input"""
        if SPEECH_AVAILABLE and self.microphone:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=10)
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    logger.info(f"🗣️ Heard: '{text}'")
                    return text
                except sr.UnknownValueError:
                    logger.warning("Could not understand")
                    return None
            except Exception as e:
                logger.error(f"Listen error: {e}")
                return self.keyboard_fallback()
        else:
            return self.keyboard_fallback()
    
    def keyboard_fallback(self):
        """Keyboard input"""
        try:
            user_input = input("Voice (keyboard)> ").strip()
            logger.info(f"⌨️ Keyboard: {user_input}")
            return user_input
        except EOFError:
            return None
        except KeyboardInterrupt:
            self.running = False
            return None
    
    def ask_sara_ai(self, question):
        """Ask Sara AI consciousness for response"""
        try:
            # Use subprocess to call sessions_send
            result = subprocess.run([
                'python3', '-c', f