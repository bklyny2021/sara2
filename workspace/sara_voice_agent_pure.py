#!/usr/bin/env python3
"""
🤖 PURE SARA VOICE AGENT - NO SCRIPTED RESPONSES
SPEAKS ONLY WHAT AI MODEL GENERATES - ZERO CANNED CONTENT
"""

import os
import sys
import json
import time
import logging
import subprocess
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/local-command-center/logs/sara_voice.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PureSaraVoiceAgent:
    """PURE voice agent - only AI model responses"""
    
    def __init__(self):
        logger.info("🚀 StartingPURE Sara Voice Agent - NO SCRIPTED RESPONSES")
        
        # Configuration  
        self.wake_word = "sara"
        self.running = True
        
        # Setup voice components
        self.setup_voice_components()
        
        # Welcome message? NO! User said NO!
        # Just start listening silently
        
    def setup_voice_components(self):
        """Setup voice recognition and TTS"""
        try:
            import speech_recognition as sr
            import pyttsx3
            
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone(device_index=self.get_k66_device_index())
            self.tts_engine = pyttsx3.init()
            
            # Setup TTS voice properties
            voices = self.tts_engine.getProperty('voices')
            female_voice = None
            for voice in voices:
                if hasattr(voice, 'gender') and 'female' in voice.gender.lower():
                    female_voice = voice
                    break
            
            if female_voice:
                self.tts_engine.setProperty('voice', female_voice.id)
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.9)
                
            logger.info("✅ Voice components setup complete")
            
        except Exception as e:
            logger.error(f"Voice setup failed: {e}")
            sys.exit(1)
    
    def get_k66_device_index(self):
        """Find K66 microphone device index"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            for i, mic in enumerate(mic_list):
                if 'K66' in mic:
                    logger.info(f"🎤 Found K66 at index {i}")
                    return i
            return None
        except:
            return None
    
    def speak_model_response(self, text):
        """Speak ONLY AI model-generated text"""
        try:
            # ONLY speak what the model generates - no modifications
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            logger.info(f"🔊 Spoke AI model response")
        except Exception as e:
            logger.error(f"TTS failed: {e}")
    
    def get_ai_model_response(self, user_input):
        """Get response from actual AI model - NO SCRIPTS"""
        try:
            # Try to connect to main Sara AI via REST API
            response = requests.post(
                'http://127.0.0.1:8890/chat',
                json={'message': user_input},
                timeout=10
            )
            
            if response.status_code == 200:
                ai_response = response.json().get('response', '')
                logger.info(f"🧠 AI Model Response: {ai_response}")
                return ai_response.strip()
            else:
                logger.warning(f"API failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"AI model connection failed: {e}")
            return None
    
    def wait_for_wake_word(self):
        """Wait for wake word - NO spoken confirmation"""
        logger.info("👂 Listening for wake word...")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
        while self.running:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                # Try to recognize speech
                text = self.recognizer.recognize_google(audio).lower()
                
                if self.wake_word in text:
                    logger.info(f"🎯 Wake word detected: '{text}'")
                    return
                    
            except sr.UnknownValueError:
                # No speech detected
                pass
            except sr.RequestError:
                # Service error, continue
                pass
            except Exception as e:
                logger.error(f"Wake word error: {e}")
                pass
    
    def get_user_command(self):
        """Get user command after wake word"""
        logger.info("🎤 Listening for command...")
        
        with self.microphone as source:
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
        
        try:
            command = self.recognizer.recognize_google(audio)
            logger.info(f"🗣️ Command: {command}")
            return command.strip()
            
        except sr.UnknownValueError:
            logger.info("❌ Could not understand command")
            return None
        except Exception as e:
            logger.error(f"Command recognition failed: {e}")
            return None
    
    def run(self):
        """Main loop - PURE AI responses only"""
        logger.info("🚀 PURE voice agent starting - NO SCRIPTED RESPONSES")
        
        while self.running:
            try:
                # Wait for wake word silently
                self.wait_for_wake_word()
                
                if not self.running:
                    break
                
                # Get user command
                command = self.get_user_command()
                
                if command:
                    # Get AI model response ONLY
                    ai_response = self.get_ai_model_response(command)
                    
                    if ai_response:
                        # Speak ONLY what AI model generated
                        self.speak_model_response(ai_response)
                    else:
                        logger.warning("No AI response received")
                
            except KeyboardInterrupt:
                logger.info("🛑 Shutdown requested")
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                time.sleep(1)
        
        logger.info("🔚 PURE voice agent shutdown")

def main():
    """Launch pure voice agent"""
    agent = PureSaraVoiceAgent()
    agent.run()

if __name__ == "__main__":
    main()