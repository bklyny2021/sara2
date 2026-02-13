#!/usr/bin/env python3
"""
🤖 PURE LOCAL VOICE AGENT - ZERO API KEYS
Ollama integration only - no external services
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

class LocalOnlySaraVoiceAgent:
    """LOCAL-ONLY voice agent - pure Ollama integration"""
    
    def __init__(self):
        logger.info("🚀 Starting LOCAL-ONLY Sara Voice Agent - ZERO API KEYS")
        
        # Configuration  
        self.wake_word = "sara"
        self.running = True
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Setup voice components
        self.setup_voice_components()
        
        # Test local AI
        self.test_ollama_connection()
        
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
    
    def test_ollama_connection(self):
        """Test local Ollama availability"""
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                logger.info(f"✅ Ollama connected, models: {[m['name'] for m in models]}")
                
                # Check if sara-boo1-fixed is available
                for model in models:
                    if 'sara-boo1-fixed' in model['name']:
                        logger.info("✅ sara-boo1-fixed model available")
                        return True
                        
                # Fallback to glm-4.6 if sara-boo1-fixed not found
                for model in models:
                    if 'glm-4.6' in model['name'] or 'glm' in model['name']:
                        self.ollama_model = model['name']
                        logger.info(f"⚠️ Using fallback model: {model['name']}")
                        return True
                        
                logger.warning("⚠️ No suitable model found, using default")
                self.ollama_model = "glm-4.6:cloud"
                return True
            else:
                raise Exception(f"Ollama returned {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Ollama connection failed: {e}")
            logger.error("📍 Ollama must be running: 'ollama serve'")
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
            logger.info(f"🔊 Spoke LOCAL AI model response")
        except Exception as e:
            logger.error(f"TTS failed: {e}")
    
    def get_local_ai_response(self, user_input):
        """Get response from LOCAL Ollama model - ZERO API KEYS"""
        try:
            payload = {
                'model': getattr(self, 'ollama_model', 'glm-4.6:cloud'),
                'prompt': user_input,
                'stream': False,
                'options': {
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'num_predict': 150
                }
            }
            
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                ai_response = response.json().get('response', '')
                logger.info(f"🧠 LOCAL AI Model Response: {ai_response}")
                return ai_response.strip()
            else:
                logger.warning(f"Local Ollama failed: {response.status_code}")
                return "I'm having trouble with my local AI processing. Can you try again?"
                
        except Exception as e:
            logger.error(f"Local AI processing failed: {e}")
            return "My local AI system needs attention. Let me check my configuration."
    
    def wait_for_wake_word(self):
        """Wait for wake word - NO spoken confirmation"""
        logger.info("👂 Listening for wake word...")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
        while self.running:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                # Try speech recognition
                text = self.recognizer.recognize_google(audio).lower()
                
                if self.wake_word in text:
                    logger.info(f"🎯 Wake word detected: '{text}'")
                    return
                    
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
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
        """Main loop - LOCAL AI only"""
        logger.info("🚀 LOCAL-ONLY voice agent starting - ZERO API KEYS")
        
        while self.running:
            try:
                # Wait for wake word silently
                self.wait_for_wake_word()
                
                if not self.running:
                    break
                
                # Get user command
                command = self.get_user_command()
                
                if command:
                    # Get LOCAL AI model response ONLY
                    ai_response = self.get_local_ai_response(command)
                    
                    if ai_response:
                        # Speak ONLY what LOCAL AI model generated
                        self.speak_model_response(ai_response)
                    else:
                        logger.warning("No LOCAL AI response received")
                
            except KeyboardInterrupt:
                logger.info("🛑 Shutdown requested")
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                time.sleep(1)
        
        logger.info("🔚 LOCAL-ONLY voice agent shutdown")

def main():
    """Launch local-only voice agent"""
    agent = LocalOnlySaraVoiceAgent()
    agent.run()

if __name__ == "__main__":
    main()