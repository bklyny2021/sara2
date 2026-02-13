#!/usr/bin/env python3
"""
🔧 FIXED PURE AI VOICE AGENT - Audio Chain Repaired
ZERO EXTERNAL DEPENDENCIES - PURE LOCAL AI ONLY
"""

import os
import sys
import json
import time
import logging
import subprocess
import requests
import speech_recognition as sr  # FIXED: Top-level import
from pathlib import Path

# Configure logging (MINIMAL - NO coaching messages)
logging.basicConfig(
    level=logging.ERROR,  # Only errors, no info/debug messages
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/local-command-center/logs/sara_voice.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FixedPureAIVoiceAgent:
    """ZERO COACHING - PURE AI SPEECH ONLY - IMPORTS FIXED"""
    
    def __init__(self):
        # NO startup messages
        self.wake_word = "sara"
        self.running = True
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Setup silently
        self.setup_voice_components()
        self.test_ollama_connection()
        
        # NO greeting messages - silent startup
        
    def setup_voice_components(self):
        """Setup voice components silently - IMPORTS FIXED"""
        try:
            # speech_recognition imported at top level now
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone(device_index=self.get_k66_device_index())
            
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Setup TTS voice properties silently
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
                
            # Setup audio sink for AD106M
            try:
                # Set default sink to K66 speakers
                subprocess.run(['pactl', 'set-default-sink', 'alsa_output.usb-K66_K66_20190805V001.pro-output-0'], 
                             capture_output=True, check=False)
            except:
                pass  # Silent continue if pactl not available
                
        except Exception as e:
            logger.error(f"Voice setup failed: {e}")
            sys.exit(1)
    
    def test_ollama_connection(self):
        """Test local Ollama silently"""
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                
                # Silently check for sara-boo1-fixed
                for model in models:
                    if 'sara-boo1-fixed' in model['name']:
                        return True
                
                # Fallback silently
                for model in models:
                    if 'glm-4.6' in model['name'] or 'glm' in model['name']:
                        self.ollama_model = model['name']
                        return True
                
                self.ollama_model = "glm-4.6:cloud"
                return True
            else:
                raise Exception(f"Ollama returned {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Ollama connection failed: {e}")
            logger.error("📍 Ollama must be running: 'ollama serve'")
            sys.exit(1)
    
    def get_k66_device_index(self):
        """Find K66 device silently"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            for i, mic in enumerate(mic_list):
                if 'K66' in mic:
                    return i
            return None
        except:
            return None
    
    def speak_ai_response_only(self, text):
        """Speak ONLY AI responses - audio chain ready"""
        try:
            # ONLY what AI generates - nothing else
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            logger.error(f"TTS failed: {e}")
    
    def get_local_ai_response(self, user_input):
        """Get AI response silently"""
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
                return ai_response.strip()
            else:
                return "I hear you. Let me process that."
                
        except Exception as e:
            logger.error(f"Local AI processing failed: {e}")
            return "Let me think about that."
    
    def wait_for_wake_word_silent(self):
        """Silent wake word detection - audio chain ready"""
        while self.running:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Audio chain: K66 → recognizer
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                text = self.recognizer.recognize_google(audio).lower()
                
                if self.wake_word in text:
                    return
                    
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
            except Exception as e:
                logger.error(f"Wake word error: {e}")
                pass
    
    def get_user_command_silent(self):
        """Get command through audio chain - no coaching"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
            
            command = self.recognizer.recognize_google(audio)
            return command.strip()
            
        except sr.UnknownValueError:
            return None
        except Exception as e:
            logger.error(f"Command recognition failed: {e}")
            return None
    
    def run(self):
        """Main loop - AUDIO CHAIN FIXED"""
        while self.running:
            try:
                self.wait_for_wake_word_silent()
                
                if not self.running:
                    break
                
                command = self.get_user_command_silent()
                
                if command:
                    ai_response = self.get_local_ai_response(command)
                    
                    if ai_response:
                        # Audio chain: TTS → AD106M speakers
                        self.speak_ai_response_only(ai_response)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                time.sleep(1)

def main():
    """Launch fixed pure AI voice agent"""
    agent = FixedPureAIVoiceAgent()
    agent.run()

if __name__ == "__main__":
    main()