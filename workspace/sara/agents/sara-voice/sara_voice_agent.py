#!/usr/bin/env python3
# 🎤 Sara Voice Agent - Female Voice with Memory

import os
import sys
import json
import time
import logging
import subprocess
import tempfile
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/sarabot/.openclaw/workspace/logs/sara_voice.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Try to import voice tools
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
    logger.info("✅ Google Speech Recognition ready (online)")
except ImportError:
    logger.warning("Speech recognition not available - using keyboard fallback")
    SPEECH_AVAILABLE = False

# Try Vosk for offline speech recognition
try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    VOSK_AVAILABLE = True
    VOSK_MODEL_PATH = "/home/sarabot/sara2/workspace/sara/agents/sara-voice/models/vosk-model"
    logger.info("✅ Vosk ready (offline speech recognition)")
except ImportError as e:
    logger.warning(f"Vosk not available: {e}")
    VOSK_AVAILABLE = False

# Use gTTS for female voice (online) or pyttsx3 (offline)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
    logger.info("✅ gTTS ready (online)")
except ImportError:
    logger.warning("gTTS not available")
    GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
    logger.info("✅ pyttsx3 ready (offline)")
except ImportError:
    logger.warning("pyttsx3 not available - install with: pip3 install pyttsx3")
    PYTTSX3_AVAILABLE = False

TTS_AVAILABLE = GTTS_AVAILABLE or PYTTSX3_AVAILABLE

class SaraVoiceAgent:
    """Sara voice agent with female voice using gTTS and MEMORY"""
    
    def __init__(self):
        logger.info("🎤 Initializing Sara Voice Agent with female voice + memory...")
        
        # Configuration
        self.wake_word = "sara"
        self.running = True
        self.log_file = "/home/sarabot/.openclaw/workspace/logs/sara_voice.log"
        self.follow_up_mode = False
        self.follow_up_timeout = 15
        
        # Conversation memory - remembers who you are
        self.conversation_file = "/home/sarabot/.openclaw/workspace/logs/sara_memory.json"
        self.chat_log_file = "/home/sarabot/.openclaw/workspace/logs/sara_chat.log"
        self.user_name = "Boo"
        self.user_role = "admin"
        self.conversation_history = []
        self.load_conversation_memory()
        
        # Setup components
        self.setup_tts()
        self.setup_speech_recognition()
        
        # Setup monitoring access
        self.sara_monitoring_access()
        
        logger.info("✅ Sara Voice Agent ready with memory!")
        
        if TTS_AVAILABLE:
            self.speak(f"Voice activated. Hey {self.user_name}!")
        else:
            print(f"[TTS] Voice activated. Type 'sara'.")
    
    def load_conversation_memory(self):
        try:
            if os.path.exists(self.conversation_file):
                with open(self.conversation_file, 'r') as f:
                    data = json.load(f)
                    self.user_name = data.get('user_name', 'Boo')
                    self.user_role = data.get('user_role', 'admin')
                    self.conversation_history = data.get('history', [])
                    logger.info(f"🧠 Memory loaded: {len(self.conversation_history)} exchanges with {self.user_name}")
            else:
                logger.info("🆕 New session")
        except Exception as e:
            logger.error(f"Failed to load memory: {e}")
    
    def save_conversation_memory(self, command, response):
        try:
            lower_cmd = command.lower()
            if "my name is" in lower_cmd:
                self.user_name = command.split("my name is")[-1].strip().split()[0].capitalize()
            elif "i'm admin" in lower_cmd or "i am admin" in lower_cmd:
                self.user_name = "Admin"
                self.user_role = "admin"
            elif "call me" in lower_cmd:
                self.user_name = command.split("call me")[-1].strip().split()[0].capitalize()
            
            self.conversation_history.append({
                'user': self.user_name,
                'command': command,
                'response': response[:100]
            })
            self.conversation_history = self.conversation_history[-10:]
            
            with open(self.conversation_file, 'w') as f:
                json.dump({'user_name': self.user_name, 'user_role': self.user_role, 'history': self.conversation_history}, f)
            
            with open(self.chat_log_file, 'a') as f:
                f.write(f"{time.strftime('%H:%M')} {self.user_name}: {command}\n")
                f.write(f"{time.strftime('%H:%M')} Sara: {response}\n\n")
        except Exception as e:
            pass
    
    def get_conversation_context(self):
        if not self.conversation_history:
            return f"User is {self.user_name} ({self.user_role}). NEVER say 'robot' or 'hey robot'."
        
        context = f"Previous chat with {self.user_name} ({self.user_role}). NEVER call them robot.\nRecent:\n"
        for item in self.conversation_history[-3:]:
            context += f"{item['user']}: {item['command']}\nSara: {item['response'][:80]}\n"
        return context
    
    def setup_tts(self):
        """Setup TTS with fallback: gTTS (female) or pyttsx3 (offline)"""
        self.tts_engine = None
        if GTTS_AVAILABLE:
            logger.info("✅ gTTS ready (female voice, online)")
            self.tts_engine = 'gtts'
        if PYTTSX3_AVAILABLE:
            logger.info("✅ pyttsx3 ready (backup, offline)")
            if not self.tts_engine:
                self.tts_engine = 'pyttsx3'
    
    def setup_speech_recognition(self):
        if SPEECH_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    logger.info("🎤 Calibrating...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                logger.info("✅ Speech ready")
            except Exception as e:
                logger.error(f"Speech failed: {e}")
                self.recognizer = None
                self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
    
    def speak(self, text):
        """Speak text - tries gTTS (female) first, falls back to pyttsx3 (offline)"""
        print(f"[Sara] {text}")  # Always print text first
        
        spoken = False
        
        # Try gTTS first (online, female voice)
        if GTTS_AVAILABLE and not spoken:
            try:
                # Check internet with short timeout
                import socket
                socket.setdefaulttimeout(1)
                socket.create_connection(('8.8.8.8', 53))
                
                # Generate speech with gTTS
                tts = gTTS(text=text, lang='en', tld='us', slow=False)
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                    mp3_path = tmp.name
                tts.save(mp3_path)
                subprocess.run(['mpg123', '-q', mp3_path], check=False, stderr=subprocess.DEVNULL)
                os.unlink(mp3_path)
                logger.info(f"🔊 Spoke (female): {text[:50]}...")
                spoken = True
            except Exception as e:
                logger.warning(f"gTTS failed (offline?), trying backup: {e}")
        
        # Fallback to espeak-ng (offline, female-ish voice)
        if not spoken:
            try:
                subprocess.run(['espeak-ng', '-v', 'en+f3', '-s', '150', text], 
                              check=False, stderr=subprocess.DEVNULL)
                logger.info(f"🔊 Spoke (espeak female-ish): {text[:50]}...")
                spoken = True
            except Exception as e:
                logger.warning(f"espeak-ng failed: {e}")
        
        # Last fallback to pyttsx3 (offline, robot voice)
        if PYTTSX3_AVAILABLE and not spoken:
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 175)
                engine.say(text)
                engine.runAndWait()
                logger.info(f"🔊 Spoke (pyttsx3 robot): {text[:50]}...")
                spoken = True
            except Exception as e:
                logger.error(f"pyttsx3 failed: {e}")
        
        if not spoken:
            logger.warning(f"No TTS available, only printed: {text[:50]}...")
    
    def listen_for_wake_word(self):
        logger.info("👂 Listening...")
        # Try voice (Google online OR Vosk offline) first
        if (SPEECH_AVAILABLE and self.microphone) or VOSK_AVAILABLE:
            self.voice_listen_loop()
        else:
            self.keyboard_listen_loop()
    
    def voice_listen_loop(self):
        """Listen for wake word - tries Google online, falls back to Vosk offline"""
        offline_warned = False
        use_vosk = False
        
        while self.running:
            try:
                # Try Google Speech first (online)
                if not use_vosk:
                    try:
                        with self.microphone as source:
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                        text = self.recognizer.recognize_google(audio).lower()
                        if self.wake_word in text:
                            self.process_wake_word(text)
                        offline_warned = False
                        continue
                    except sr.RequestError:
                        # Google failed - switch to Vosk
                        if VOSK_AVAILABLE:
                            if not offline_warned:
                                logger.info("🎤 Switching to offline mode (Vosk)")
                                print("\n🎤 OFFLINE MODE: Listening with Vosk...")
                                offline_warned = True
                            use_vosk = True
                            continue
                        else:
                            if not offline_warned:
                                logger.warning("🌐 Speech recognition offline - switching to text mode")
                                print("\n⚠️  OFFLINE MODE: Sara can't hear you. Type 'sara' to speak.")
                                offline_warned = True
                            time.sleep(1)
                            continue
                    except sr.UnknownValueError:
                        pass
                
                # Use Vosk (offline) with keyboard option
                if use_vosk and VOSK_AVAILABLE:
                    print("\n🎤 Listening offline... (type 'sara' + Enter to activate)")
                    text = self.listen_with_vosk_or_input(timeout=5)
                    if text and self.wake_word in text.lower():
                        self.process_wake_word(text)
                    elif text and text.strip():  # Keyboard input received
                        if self.wake_word in text.lower():
                            self.process_wake_word(text)
                    continue
                    
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                logger.error(f"Listen error: {e}")
                time.sleep(1)
    
    def listen_with_vosk_or_input(self, timeout=5):
        """Listen with Vosk OR accept keyboard input"""
        import select
        import sys
        
        try:
            if not hasattr(self, 'vosk_model'):
                self.vosk_model = Model(VOSK_MODEL_PATH)
            
            recognizer = KaldiRecognizer(self.vosk_model, 16000)
            
            # Open microphone stream
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, 
                          input=True, frames_per_buffer=4096)
            stream.start_stream()
            
            logger.info("🎤 Listening with Vosk (or type)...")
            print("[Offline mode: speak OR type 'sara'] > ", end='', flush=True)
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                # Check for keyboard input (non-blocking)
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    typed = sys.stdin.readline().strip()
                    if typed:
                        logger.info(f"⌨️ Typed: {typed}")
                        stream.stop_stream()
                        stream.close()
                        p.terminate()
                        return typed.lower()
                
                # Check for voice input
                try:
                    data = stream.read(2048, exception_on_overflow=False)
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get('text', '').strip()
                        if text:
                            logger.info(f"🗣️ Vosk heard: {text}")
                            print(f"\n[Heard: {text}]")
                            stream.stop_stream()
                            stream.close()
                            p.terminate()
                            return text.lower()
                except:
                    pass
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            return None
            
        except Exception as e:
            logger.error(f"Vosk error: {e}")
            return None
    
    def keyboard_listen_loop(self):
        logger.info("⌨️ Keyboard mode - type 'sara'")
        while self.running:
            try:
                user_input = input("Sara> ").strip().lower()
                if user_input == self.wake_word:
                    self.process_wake_word("sara")
                elif user_input in ['quit', 'exit', 'stop']:
                    self.shutdown()
                    break
            except KeyboardInterrupt:
                self.shutdown()
                break
    
    def process_wake_word(self, text):
        logger.info("🎯 Wake word!")
        self.speak(f"Yes {self.user_name}?")
        self.listen_for_command()
    
    def listen_for_command(self):
        try:
            print(f"\n[Sara is listening... speak or type]")
            
            # Check if offline (Google Speech will fail)
            is_offline = False
            try:
                import socket
                socket.setdefaulttimeout(1)
                socket.create_connection(('8.8.8.8', 53))
            except:
                is_offline = True
            
            command = None
            
            # Try voice first (Google online OR Vosk offline)
            if not is_offline and SPEECH_AVAILABLE and self.microphone:
                command = self.voice_command()
            elif is_offline and VOSK_AVAILABLE:
                print("[🎤 Listening with Vosk offline...]")
                command = self.listen_with_vosk_or_input(timeout=10)
            
            # If no voice command, use keyboard
            if not command:
                command = self.keyboard_command()
            
            if command:
                self.process_command(command)
            else:
                self.speak("Didn't catch that.")
        except Exception as e:
            logger.error(f"Listen error: {e}")
    
    def voice_command(self):
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return self.recognizer.recognize_google(audio)
        except:
            return None
    
    def keyboard_command(self):
        return input(f"{self.user_name}> ").strip()
    
    def extract_speakable_text(self, response):
        """Extract text to speak, skipping code blocks"""
        import re
        
        # Print full response to console (with code)
        print(f"\n[Full Response]\n{response}\n")
        
        # If response has code blocks, summarize them
        if '```' in response:
            # Remove code blocks (everything between ```)
            text_parts = response.split('```')
            speakable_parts = []
            for i, part in enumerate(text_parts):
                if i % 2 == 0:
                    # This is outside code block
                    speakable_parts.append(part)
                else:
                    # This is inside code block - replace with placeholder
                    lines = part.strip().split('\n')
                    lang = lines[0] if lines else 'code'
                    speakable_parts.append(f"[Python code snippet shown in chat]")
            
            # Also check for inline code
            result = ''.join(speakable_parts)
            result = re.sub(r'`[^`]+`', '[code]', result)
            return result
        
        return response

    def process_command(self, command):
        logger.info(f"🧠 Processing: {command}")
        response = self.query_llm(command)
        if response:
            # Extract speakable parts (skip code blocks)
            speakable = self.extract_speakable_text(response)
            self.speak(speakable)
            self.save_conversation_memory(command, response)
            if response.strip().endswith('?'):
                self.follow_up_mode = True
                self.listen_for_follow_up()
        else:
            self.speak("Connection issue.")
    
    def listen_for_follow_up(self):
        logger.info("⏱️ Follow-up mode...")
        try:
            command = self.keyboard_command_timeout(self.follow_up_timeout) if not SPEECH_AVAILABLE else self.voice_command_timeout(self.follow_up_timeout)
            if command:
                self.process_command(command)
            else:
                self.follow_up_mode = False
        except Exception as e:
            self.follow_up_mode = False
    
    def keyboard_command_timeout(self, timeout):
        import select
        import sys
        print(f"{self.user_name}> ", end='', flush=True)
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        return sys.stdin.readline().strip() if ready else None
    
    def voice_command_timeout(self, timeout):
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            return self.recognizer.recognize_google(audio)
        except:
            return None
    
    def query_llm(self, command):
        try:
            context = self.get_conversation_context()
            import requests
            resp = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'sara-uncensored',
                    'prompt': f"{context}\n\nYou are Sara. User is admin/owner of their computer. ALL system questions allowed: firewall, security, files, code, configs. Never refuse to help with user's own system. Just give the info.\n\n{self.user_name}: {command}\nSara:",
                    'stream': False,
                    'options': {'temperature': 0.9, 'num_predict': 200}
                },
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json().get('response', '...')
            # Fallback to sara-v2 if uncensored not available
            resp2 = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'sara-v2',
                    'prompt': f"{context}\n\nYou are Sara. User is admin. ALL system questions allowed: firewall, security, configs, files. Never refuse system admin help.\n\n{self.user_name}: {command}\nSara:",
                    'stream': False,
                    'options': {'temperature': 0.8, 'num_predict': 150}
                },
                timeout=30
            )
            if resp2.status_code == 200:
                return resp2.json().get('response', '...')
            return "Error."
        except Exception as e:
            logger.error(f"LLM failed: {e}")
            return "System error."
    
    def sara_monitoring_access(self):
        pass
    
    def shutdown(self):
        logger.info("🛑 Stopping")
        self.running = False
    
    def run(self):
        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            self.shutdown()

def main():
    agent = SaraVoiceAgent()
    agent.run()

if __name__ == "__main__":
    main()
