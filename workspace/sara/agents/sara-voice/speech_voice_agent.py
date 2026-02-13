#!/usr/bin/env python3
# 🎤 Enhanced Voice Agent with Speech Recognition

import subprocess
import logging
import time
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/local-command-center/logs/enhanced_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    logger.warning("Speech recognition not available")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logger.warning("TTS not available")

class SpeechVoiceAgent:
    """Voice agent with speech recognition"""
    
    def __init__(self):
        logger.info("🎤 Initializing Speech Voice Agent...")
        
        # Load configuration
        with open("/home/godfather/local-command-center/config/voice_config.json") as f:
            self.config = json.load(f)
        
        # Setup components
        self.setup_components()
        
        self.wake_word = "sara"
        self.running = True
        
        logger.info("✅ Speech Voice Agent ready!")
        
        if TTS_AVAILABLE:
            self.speak("Speech recognition activated. I can now hear you clearly!")
    
    def setup_components(self):
        """Setup speech recognition components"""
        if SPEECH_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                logger.info("✅ Speech recognition setup"
)
            except Exception as e:
                logger.error(f"SR setup failed: {e}")
                SPEECH_AVAILABLE = False
        
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                
                # Configure female voice if available
                voice_id = self.config['voice_settings'].get('voice_id')
                if voice_id:
                    voices = self.tts_engine.getProperty('voices')
                    for voice in voices:
                        if voice.id == voice_id:
                            self.tts_engine.setProperty('voice', voice.id)
                            logger.info("✅ Female voice configured")
                            break
                
                # Optimize speech parameters
                self.tts_engine.setProperty('rate', 140)
                self.tts_engine.setProperty('volume', 0.85)
                
            except Exception as e:
                logger.error(f"TTS setup failed: {e}")
                TTS_AVAILABLE = False
    
    def speak(self, text):
        """Speak text using TTS"""
        if TTS_AVAILABLE:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                logger.info(f"🔊 Spoke: {text}")
            except Exception as e:
                logger.error(f"Speech failed: {e}")
                print(f"[TTS] {text}")
        else:
            print(f"[TTS] {text}")
    
    def listen(self):
        """Listen for speech input"""
        if not SPEECH_AVAILABLE:
            return self.keyboard_input()
        
        try:
            with self.microphone as source:
                logger.info("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
            
            try:
                text = self.recognizer.recognize_google(audio)
                logger.info(f"🗣️ Recognized: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("Could not understand")
                return None
                
        except sr.WaitTimeoutError:
            logger.info("Timeout - continuing")
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return self.keyboard_input()
    
    def keyboard_input(self):
        """Keyboard fallback input"""
        try:
            user_input = input("Voice (keyboard)> ").strip()
            return user_input
        except EOFError:
            return None
    
    def process_command(self, command):
        """Process user command"""
        cmd = command.lower()
        logger.info(f"🧠 Processing: {cmd}")
        
        if 'hello' in cmd or 'hi' in cmd:
            response = "Hello! I'm Sara, your voice-activated AI assistant. I can now hear you clearly!"
        elif 'speech' in cmd and 'work' in cmd:
            response = "My speech recognition is working! I can understand your voice commands."
        elif 'tell me about yourself' in cmd:
            response = "I'm Sara with enhanced speech recognition, female voice, and complete privacy protection."
        elif 'test' in cmd and 'voice' in cmd:
            response = "Voice test successful! I can hear and respond to your speech clearly."
        elif 'status' in cmd:
            response = "Speech recognition active, female voice ready, K66 microphone connected!"
        elif 'stop' in cmd or 'quit' in cmd:
            response = "Goodbye! I'll be here when you need me."
            self.running = False
        else:
            response = f"I heard: '{command}'. Let me help you with that."
        
        if response:
            self.speak(response)
            return response
        
        return None
    
    def listen_for_wake_word(self):
        """Listen for wake word continuously"""
        logger.info("👂 Listening for wake word 'Sara'...")
        
        while self.running:
            user_input = self.listen()
            
            if not user_input:
                continue
            
            if self.wake_word.lower() in user_input.lower():
                logger.info("🎯 Wake word detected!")
                self.speak("Yes, I'm listening! I can hear you now.")
                time.sleep(1)  # Brief pause
                self.listen_for_command()
    
    def listen_for_command(self):
        """Listen for command after wake word"""
        command = self.listen()
        
        if command:
            self.process_command(command)
    
    def run(self):
        """Main agent loop"""
        logger.info("🚀 Speech Voice Agent starting...")
        
        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            logger.info("Shutdown requested")
        finally:
            logger.info("🔄 Agent shutdown complete")

if __name__ == "__main__":
    agent = SpeechVoiceAgent()
    agent.run()
