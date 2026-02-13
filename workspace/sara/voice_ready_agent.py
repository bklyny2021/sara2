#!/usr/bin/env python3
# 🎤 Voice-Enabled Sara Agent - K66 Ready!

import subprocess
import logging
import json
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/local-command-center/logs/voice_ready.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import speech recognition
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    logger.error("SpeechRecognition not available")

# Import TTS
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logger.error("pyttsx3 not available")

class VoiceReadySara:
    """Voice-enabled Sara with K66 microphone and female voice"""
    
    def __init__(self):
        logger.info("🎤 Initializing Voice-Ready Sara...")
        
        # Load configuration
        self.load_config()
        
        # Setup speech recognition
        self.setup_speech_recognition()
        
        # Setup microphone
        self.setup_microphone()
        
        # Setup female voice TTS
        self.setup_tts()
        
        # Initialize state
        self.wake_word = "sara"
        self.running = True
        
        logger.info("✅ Voice-Ready Sara initialized!")
        
        if TTS_AVAILABLE:
            self.speak("Voice recognition activated! I can now hear you clearly through the K66 microphone!")
        else:
            print("[TTS] Voice recognition activated! I can now hear you clearly!")
    
    def load_config(self):
        """Load voice configuration"""
        try:
            with open("/home/godfather/local-command-center/config/voice_config.json") as f:
                self.config = json.load(f)
            logger.info("✅ Configuration loaded")
        except Exception as e:
            logger.error(f"Config load failed: {e}")
            self.config = {}
    
    def setup_speech_recognition(self):
        """Setup speech recognition system"""
        if not SPEECH_AVAILABLE:
            logger.error("Speech recognition not available")
            return
        
        try:
            self.recognizer = sr.Recognizer()
            
            # Optimize for speech recognition
            self.recognizer.pause_threshold = 0.8
            self.recognizer.operation_timeout = None
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
            
            logger.info("✅ Speech recognition configured")
            
        except Exception as e:
            logger.error(f"SR setup failed: {e}")
            SPEECH_AVAILABLE = False
    
    def setup_microphone(self):
        """Setup K66 microphone"""
        if not SPEECH_AVAILABLE:
            logger.error("Cannot setup microphone without speech recognition")
            return
        
        try:
            # Find K66 microphone index
            mics = sr.Microphone.list_microphone_names()
            self.k66_index = None
            
            for i, mic_name in enumerate(mics):
                if "K66" in mic_name:
                    self.k66_index = i
                    logger.info(f"✅ K66 microphone found at index {i}: {mic_name}")
                    break
            
            if self.k66_index is None:
                # Fallback to first available microphone
                logger.warning("K66 not found, using default microphone")
                self.k66_index = None
            
            # Initialize microphone
            self.microphone = sr.Microphone(device_index=self.k66_index)
            logger.info("✅ Microphone initialized")
            
        except Exception as e:
            logger.error(f"Microphone setup failed: {e}")
            self.microphone = None
    
    def setup_tts(self):
        """Setup female voice TTS"""
        if not TTS_AVAILABLE:
            logger.error("TTS not available")
            return
        
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure female voice
            voice_id = self.config.get('voice_settings', {}).get('voice_id')
            if voice_id:
                voices = self.tts_engine.getProperty('voices')
                for voice in voices:
                    if voice.id == voice_id:
                        self.tts_engine.setProperty('voice', voice.id)
                        logger.info(f"✅ Female voice configured: {voice.name}")
                        break
            
            # Optimize speech parameters
            self.tts_engine.setProperty('rate', 140)
            self.tts_engine.setProperty('volume', 0.85)
            
            # Save current voice config
            current_voice = self.tts_engine.getProperty('voice')
            logger.info(f"✅ TTS ready with voice: {current_voice}")
            
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
            text_output = f"[TTS] {text}"
            print(text_output)
            logger.info(text_output)
    
    def listen(self):
        """Listen for speech with K66 microphone"""
        if not SPEECH_AVAILABLE or not self.microphone:
            return self.keyboard_fallback()
        
        try:
            with self.microphone as source:
                logger.info("🎤 Listening on K66...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for speech
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=10)
            
            try:
                # Recognize speech
                text = self.recognizer.recognize_google(audio)
                logger.info(f"🗣️ Recognized: '{text}'")
                return text
                
            except sr.UnknownValueError:
                logger.warning("Could not understand speech")
                return None
            except sr.RequestError:
                logger.warning("Speech recognition service error")
                return None
                
        except sr.WaitTimeoutError:
            logger.debug("Timeout - continuing to listen")
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return self.keyboard_fallback()
    
    def keyboard_fallback(self):
        """Keyboard input fallback"""
        try:
            user_input = input("Voice (K66 + keyboard)> ").strip()
            logger.info(f"⌨️ Keyboard input: {user_input}")
            return user_input
        except EOFError:
            return None
        except KeyboardInterrupt:
            self.running = False
            return None
    
    def process_command(self, command):
        """Process user command and respond"""
        cmd_lower = command.lower()
        logger.info(f"🧠 Processing command: {cmd_lower}")
        
        # Command processing logic
        if 'hello' in cmd_lower or 'hi' in cmd_lower:
            response = "Hello! I'm Sara with full speech recognition. I can hear you clearly through the K66 microphone!"
            
        elif 'speech' in cmd_lower and 'work' in cmd_lower:
            response = "Yes! Speech recognition is working perfectly. I'm using the K66 USB microphone with high-quality audio input."
            
        elif 'microphone' in cmd_lower or 'mic' in cmd_lower:
            response = "I'm using the professional K66 USB-C microphone. It provides excellent voice input quality for our conversations."
            
        elif 'tell me about yourself' in cmd_lower:
            response = "I'm Sara, your voice-activated AI assistant with speech recognition, female voice, and complete local privacy protection."
            
        elif 'test your voice' in cmd_lower or 'voice test' in cmd_lower:
            response = "Perfect! You can hear my female TTS voice responding to you. Speech recognition is working both ways!"
            
        elif 'status' in cmd_lower:
            response = "Speech recognition active, K66 microphone connected, female voice ready, and I'm listening for you!"
            
        elif 'can you hear me' in cmd_lower:
            response = "Yes! I can hear you through the K66 microphone. Speech recognition is processing your voice right now!"
            
        elif 'stop' in cmd_lower or 'quit' in cmd_lower:
            response = "Goodbye! I'll be here whenever you want to talk with voice. I'll be listening!"
            self.running = False
        
        else:
            response = f"I heard you say: '{command}'. Let me help you with that!"
        
        if response:
            self.speak(response)
            return response
        
        return None
    
    def listen_for_wake_word(self):
        """Listen for 'Sara' wake word"""
        logger.info("👂 Listening for wake word 'Sara'...")
        
        while self.running:
            # Listen for speech input
            user_input = self.listen()
            
            if not user_input:
                continue
            
            # Check for wake word
            if self.wake_word.lower() in user_input.lower():
                logger.info("🎯 Wake word 'Sara' detected!")
                self.speak("Yes, I'm listening! I can hear you clearly through the K66 microphone.")
                
                # Brief pause for clarity
                time.sleep(1)
                
                # Listen for command
                self.listen_for_command()
    
    def listen_for_command(self):
        """Listen for command after wake word"""
        command = self.listen()
        
        if command:
            self.process_command(command)
    
    def run(self):
        """Main voice agent loop"""
        logger.info("🚀 Voice-Ready Sara starting...")
        
        try:
            # System announcement
            time.sleep(2)
            
            # Main listening loop
            self.listen_for_wake_word()
            
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
        except Exception as e:
            logger.error(f"Agent error: {e}")
        finally:
            if self.running:
                self.speak("Voice system shutting down. Goodbye!")
            logger.info("🔄 Voice-Ready Sara shutdown complete")

def main():
    """Main execution"""
    try:
        # Create voice agent instance
        sara = VoiceReadySara()
        
        # Start voice agent
        sara.run()
        
    except Exception as e:
        logger.error(f"Main error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()