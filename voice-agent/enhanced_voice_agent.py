#!/usr/bin/env python3
# 🎤 Enhanced Speech recognition Voice Agent

import subprocess
import sys
import json
import time
import logging
import threading
from datetime import datetime

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️ Speech recognition not available - using keyboard only")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ TTS not available - text responses only")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/local-command-center/logs/enhanced_voice.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedVoiceAgent:
    """Enhanced voice agent with speech recognition"""
    
    def __init__(self):
        logger.info("🎤 Initializing Enhanced Voice Agent...")
        
        # Load configuration
        with open("/home/godfather/local-command-center/config/voice_config.json") as f:
            self.config = json.load(f)
        
        # Setup components
        self.setup_recognizer()
        self.setup_microphone()
        self.setup_tts()
        
        self.wake_word = "sara"
        self.listening = True
        
        logger.info("✅ Enhanced Voice Agent ready!")
        if TTS_AVAILABLE:
            self.speak("Enhanced speech recognition activated. Sara is ready to listen.")
    
    def setup_recognizer(self):
        """Setup speech recognizer"""
        if SPEECH_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.pause_threshold = 0.8  # Pause threshold
                self.recognizer.operation_timeout = None  # No timeout
                self.recognizer.phrase_threshold = 0.3
                self.recognizer.non_speaking_duration = 0.5
                logger.info("✅ Speech recognizer configured")
            except Exception as e:
                logger.error(f"Recognizer setup failed: {e}")
                SPEECH_AVAILABLE = False
        else:
            logger.warning("Speech recognition not available")
    
    def setup_microphone(self):
        """Setup microphone input"""
        if SPEECH_AVAILABLE:
            try:
                mic_index = self.config['audio_settings'].get('microphone_index')
                self.microphone = sr.Microphone(device_index=mic_index)
                logger.info(f"✅ Microphone setup complete (index: {mic_index})")
            except Exception as e:
                logger.error(f"Microphone setup failed: {e}")
                self.microphone = None
        else:
            self.microphone = None
    
    def setup_tts(self):
        """Setup text-to-speech"""
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                
                # Configure female voice
                voice_id = self.config['voice_settings'].get('voice_id')
                if voice_id:
                    voices = self.tts_engine.getProperty('voices')
                    for voice in voices:
                        if voice.id == voice_id:
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                
                # Optimize speech parameters
                speech_params = self.config['voice_settings'].get('speech_params', {})
                self.tts_engine.setProperty('rate', speech_params.get('rate', 140))
                self.tts_engine.setProperty('volume', speech_params.get('volume', 0.85))
                
                logger.info("✅ Female TTS configured")
                
            except Exception as e:
                logger.error(f"TTS setup failed: {e}")
                self.tts_engine = None
        else:
            self.tts_engine = None
    
    def speak(self, text):
        """Speak text using TTS"""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                logger.info(f"🔊 Spoke: {text}")
            except Exception as e:
                logger.error(f"Speech failed: {e}")
                print(f"[TTS] {text}")
        else:
            print(f"[TTS] {text}")
    
    def listen_with_speech(self):
        """Listen using speech recognition"""
        if not SPEECH_AVAILABLE or not self.microphone:
            return None
        
        try:
            with self.microphone as source:
                logger.info("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
            
            try:
                # Google recognition as primary
                text = self.recognizer.recognize_google(audio)
                logger.info(f"🗣️ Recognized: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return None
            except sr.RequestError:
                logger.warning("Speech service error")
                return None
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            logger.error(f"Listening error: {e}")
            return None
    
    def listen_keyboard(self):
        """Keyboard fallback"""
        try:
            user_input = input("Voice (keyboard mode)> ").strip()
            return user_input
        except EOFError:
            return None
        except KeyboardInterrupt:
            self.listening = False
            return None
    
    def process_command(self, command):
        """Process voice command"""
        command = command.lower()
        logger.info(f"🧠 Processing: {command}")
        
        if 'hello' in command or 'hi' in command:
            response = "Hello! I'm Sara, your voice-activated AI assistant. How can I help you today?"
        elif 'tell me about yourself' in command:
            response = "I'm Sara, your AI partner with voice interaction,local processing,and complete privacy protection."
        elif 'status' in command:
            response = "All systems operational. Speech recognition active, and I'm ready to assist with any task."
        elif 'stop' in command or 'quit' in command:
            response = "Goodbye! I'll be here when you need me."
            self.listening = False
        else:
            response = f"I understand you said: '{command}'. Let me help you with that."
        
        if response:
            self.speak(response)
            return response
        
        return None
    
    def listen_for_wake_word(self):
        """Listen for wake word"""
        logger.info("👂 Listening for wake word...")
        
        while self.listening:
            if SPEECH_AVAILABLE:
                user_input = self.listen_with_speech()
            else:
                user_input = self.listen_keyboard()
            
            if not user_input:
                continue
            
            if self.wake_word in user_input.lower():
                logger.info("🎯 Wake word detected!")
                self.speak("Yes, I'm listening. What can I help you with?")
                self.listen_for_command()
    
    def listen_for_command(self):
        """Listen for command after wake word"""
        if SPEECH_AVAILABLE:
            user_input = self.listen_with_speech()
        else:
            user_input = self.listen_keyboard()
        
        if user_input:
            self.process_command(user_input)
    
    def run(self):
        """Main agent loop"""
        logger.info("🚀 Enhanced Voice Agent starting...")
        
        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            logger.info("Shutdown requested")
        finally:
            self.speak("Goodbye!")
            logger.info("🔄 Agent shutdown complete")

if __name__ == "__main__":
    agent = EnhancedVoiceAgent()
    agent.run()
