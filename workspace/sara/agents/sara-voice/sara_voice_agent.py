#!/usr/bin/env python3
# 🎤 Sara Voice Agent - Female Voice with Memory + Web UI

import os
import sys
import json
import time
import logging
import subprocess
import tempfile
import threading
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
        self.follow_up_timeout = 120  # 2 minutes of silence before returning to wake word mode

        # ENHANCED MEMORY SYSTEM - Dual layer (daily + long-term)
        self.sara_memory_dir = "/home/sarabot/sara2/memory"
        os.makedirs(self.sara_memory_dir, exist_ok=True)
        os.makedirs(os.path.join(self.sara_memory_dir, "daily"), exist_ok=True)
        os.makedirs(os.path.join(self.sara_memory_dir, "web_searches"), exist_ok=True)
        os.makedirs(os.path.join(self.sara_memory_dir, "knowledge"), exist_ok=True)

        self.long_term_memory = os.path.join(self.sara_memory_dir, "SARA_MEMORY.md")

        # Workspace for saving executed commands/scripts
        self.workspace_dir = os.path.join(self.sara_memory_dir, "workspace")
        os.makedirs(self.workspace_dir, exist_ok=True)
        os.makedirs(os.path.join(self.workspace_dir, "executed_commands"), exist_ok=True)
        os.makedirs(os.path.join(self.workspace_dir, "executed_scripts"), exist_ok=True)

        # Initialize long-term memory header if new
        if not os.path.exists(self.long_term_memory):
            with open(self.long_term_memory, 'w') as f:
                f.write("# SARA's Long-Term Memory\n\nThis file contains accumulated knowledge and important facts.\nNever deleted - only appended to.\n\n")

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

        # Repeat penalty tracking - prevent repetitive responses
        self.recent_responses = []
        self.max_recent_responses = 5
        self.response_similarity_threshold = 0.8

        logger.info("✅ Sara Voice Agent ready with memory!")

        if TTS_AVAILABLE:
            self.speak(f"Voice activated. Hey {self.user_name}!")
        else:
            print(f"[TTS] Voice activated. Type 'sara'.")

    def load_conversation_memory(self):
        """Load previous conversations from all memory sources"""
        try:
            # First load from JSON (basic session data)
            if os.path.exists(self.conversation_file):
                with open(self.conversation_file, 'r') as f:
                    data = json.load(f)
                    self.user_name = data.get('user_name', 'Boo')
                    self.user_role = data.get('user_role', 'admin')
                    self.conversation_history = data.get('history', [])
                    logger.info(f"🧠 Basic memory loaded: {len(self.conversation_history)} exchanges")

            # Then load from daily logs (last 10 conversations across recent days)
            recent_conversations = self.load_recent_daily_conversations(limit=10)
            if recent_conversations:
                self.conversation_history = recent_conversations + self.conversation_history
                self.conversation_history = self.conversation_history[-20:]  # Keep last 20
                logger.info(f"🧠 Total memory loaded: {len(self.conversation_history)} exchanges")

            # Load important facts
            self.load_important_facts_to_memory()

            logger.info(f"🧠 Full memory ready: {self.user_name}, {len(self.conversation_history)} exchanges")

        except Exception as e:
            logger.error(f"Failed to load memory: {e}")
            logger.info("🆕 Starting fresh session")

    def load_recent_daily_conversations(self, limit=10):
        """Load recent conversations from daily log files"""
        try:
            import glob
            import re
            from datetime import datetime

            daily_files = glob.glob(os.path.join(self.sara_memory_dir, "daily", "*.md"))
            if not daily_files:
                return []

            # Sort by date (newest first)
            daily_files.sort(reverse=True)

            conversations = []

            # Read from most recent files
            for daily_file in daily_files[:3]:  # Check last 3 days
                with open(daily_file, 'r') as f:
                    content = f.read()

                # Parse conversation lines
                lines = content.split('\n')
                current_time = ""
                current_user = ""
                current_response = ""

                for line in lines:
                    # Check for timestamp header
                    if line.startswith('## ['):
                        # Save previous if exists
                        if current_user and current_response:
                            conversations.append({
                                'user': self.user_name,
                                'command': current_user,
                                'response': current_response[:100]
                            })
                        current_time = line.strip('[]# ')
                        current_user = ""
                        current_response = ""
                    # Check for user command
                    elif line.startswith(f'**{self.user_name}:**'):
                        current_user = line.split(':', 1)[1].strip()
                    # Check for response
                    elif line.startswith('**Sara:**'):
                        current_response = line.split(':', 1)[1].strip()

                # Save last one
                if current_user and current_response:
                    conversations.append({
                        'user': self.user_name,
                        'command': current_user,
                        'response': current_response[:100]
                    })

            # Return only last 'limit' conversations
            return conversations[-limit:] if len(conversations) > limit else conversations

        except Exception as e:
            logger.error(f"Failed to load daily conversations: {e}")
            return []

    def load_important_facts_to_memory(self):
        """Pre-load important facts to help with recall"""
        try:
            facts = []

            # Load from SARA_MEMORY.md
            if os.path.exists(self.long_term_memory):
                with open(self.long_term_memory, 'r') as f:
                    content = f.read()
                    # Look for personal info sections
                    sections = content.split('## ')
                    for section in sections:
                        if 'PERSONAL_INFO' in section.upper() or 'USER' in section.upper():
                            lines = section.split('\n')
                            for line in lines[1:]:  # Skip header
                                if line.strip() and self.user_name.lower() in line.lower():
                                    facts.append(line.strip())

            # Load from facts.md
            facts_file = os.path.join(self.sara_memory_dir, "knowledge", "facts.md")
            if os.path.exists(facts_file):
                with open(facts_file, 'r') as f:
                    for line in f:
                        if self.user_name.lower() in line.lower():
                            facts.append(line.strip())

            if facts:
                logger.info(f"🧠 Loaded {len(facts)} important facts")
                # Add as initial "system" context
                facts_summary = " | ".join(facts[:5])  # Top 5 facts
                self.conversation_history.insert(0, {
                    'user': 'System',
                    'command': '[Memory loaded]',
                    'response': f"I remember: {facts_summary}"
                })

        except Exception as e:
            logger.error(f"Failed to load facts: {e}")

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

            # ALSO save to enhanced memory system
            self.log_to_daily_memory(command, response)

            # EXTRACT and SAVE important facts
            self.extract_and_save_facts(command, response)
        except Exception as e:
            pass

    def extract_and_save_facts(self, command, response):
        """Extract important facts from conversation and save them"""
        try:
            cmd_lower = command.lower()

            # Check for user's birthday
            if "my birthday is" in cmd_lower or "i was born" in cmd_lower:
                # Extract birthday info
                import re
                # Common date patterns
                date_match = re.search(r'(\w+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})', command)
                if date_match:
                    birthday = date_match.group(1)
                    self.save_learned_fact(f"{self.user_name}'s birthday is {birthday}", "personal_info")
                else:
                    # Save the whole statement
                    self.save_learned_fact(f"{self.user_name}'s birthday: {command}", "personal_info")

            # Check for other personal info
            elif "my name is" in cmd_lower:
                self.save_learned_fact(f"{self.user_name}'s name was set to: {command}", "personal_info")

            elif "i'm" in cmd_lower and any(word in cmd_lower for word in ['years old', 'age']):
                age_match = re.search(r'(\d+|\w+) years old', command)
                if age_match:
                    self.save_learned_fact(f"{self.user_name} is {age_match.group(1)} years old", "personal_info")

            # Check for preferences
            elif any(word in cmd_lower for word in ['like', 'love', 'hate', 'prefer', 'favorite']):
                self.save_learned_fact(f"{self.user_name} {command}", "preferences")

            # Check for important info responses
            if any(phrase in response.lower() for phrase in ['you should know', 'remember', 'this is important']):
                self.save_learned_fact(f"Important: {command} -> {response[:200]}", "important")

        except Exception as e:
            logger.error(f"Failed to extract facts: {e}")

    # ==================== ENHANCED MEMORY SYSTEM ====================

    def log_to_daily_memory(self, command, response, category="conversation"):
        """Log interaction to daily memory file (never deleted, only appended)"""
        try:
            import datetime
            timestamp = datetime.datetime.now()
            date_str = timestamp.strftime("%Y-%m-%d")
            time_str = timestamp.strftime("%H:%M:%S")

            daily_file = os.path.join(self.sara_memory_dir, "daily", f"{date_str}.md")

            entry = f"## [{time_str}]\n**{self.user_name}:** {command}\n**Sara:** {response[:200]}\n\n"

            # Append only - never overwrite
            with open(daily_file, 'a') as f:
                f.write(entry)

            logger.info(f"📝 Logged to daily memory: {daily_file}")
        except Exception as e:
            logger.error(f"Failed to log daily memory: {e}")

    def save_to_long_term_memory(self, key_info, category="general"):
        """Save important info to long-term memory (SARA_MEMORY.md)"""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            entry = f"\n## {category.upper()} - {timestamp}\n{key_info}\n"

            # Append only - never delete existing memories
            with open(self.long_term_memory, 'a') as f:
                f.write(entry)

            logger.info(f"🧠 Saved to long-term memory: {category}")
        except Exception as e:
            logger.error(f"Failed to save long-term memory: {e}")

    def save_web_search_result(self, query, results):
        """Save web search results to memory"""
        try:
            import datetime
            import hashlib
            timestamp = datetime.datetime.now()
            date_str = timestamp.strftime("%Y-%m-%d")
            time_str = timestamp.strftime("%H:%M:%S")

            # Create search record
            search_id = hashlib.md5(f"{query}_{timestamp}".encode()).hexdigest()[:8]
            search_file = os.path.join(self.sara_memory_dir, "web_searches", f"{date_str}_{search_id}.md")

            content = f"# Web Search - {timestamp.strftime('%Y-%m-%d %H:%M')}\n\n"
            content += f"**Query:** {query}\n\n"
            content += f"**Results:**\n{results}\n\n"
            content += f"---\n*Searched by {self.user_name}*\n"

            with open(search_file, 'w') as f:
                f.write(content)

            # Also log to daily memory
            self.log_to_daily_memory(f"[Web Search] {query}", f"Results saved to {search_file}", "web_search")

            # Add to long-term memory index
            self.save_to_long_term_memory(
                f"Web search: '{query}'\nResults: {search_file}\nKey findings: {results[:300]}...",
                "web_search"
            )

            logger.info(f"🌐 Web search saved: {search_file}")
            return search_file
        except Exception as e:
            logger.error(f"Failed to save web search: {e}")
            return None

    def save_learned_fact(self, fact, source="conversation"):
        """Save a learned fact to knowledge base"""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            knowledge_file = os.path.join(self.sara_memory_dir, "knowledge", "facts.md")

            entry = f"\n- **{timestamp}** [{source}]: {fact}\n"

            # Append only - accumulate knowledge
            with open(knowledge_file, 'a') as f:
                f.write(entry)

            logger.info(f"🎓 Learned new fact")
        except Exception as e:
            logger.error(f"Failed to save fact: {e}")

    def get_memory_stats(self):
        """Return memory statistics"""
        try:
            import glob
            daily_files = glob.glob(os.path.join(self.sara_memory_dir, "daily", "*.md"))
            web_files = glob.glob(os.path.join(self.sara_memory_dir, "web_searches", "*.md"))

            total_daily_size = sum(os.path.getsize(f) for f in daily_files)
            total_web_size = sum(os.path.getsize(f) for f in web_files)

            return {
                'daily_logs': len(daily_files),
                'web_searches': len(web_files),
                'long_term_exists': os.path.exists(self.long_term_memory),
                'total_size_kb': (total_daily_size + total_web_size) / 1024
            }
        except Exception as e:
            return {'error': str(e)}

    def get_conversation_context(self, include_personal_facts=False):
        import glob
        context_parts = []

        # Add user identity
        context_parts.append(f"User is {self.user_name} ({self.user_role}). NEVER say 'robot' or 'hey robot'.")

        # Only load personal facts if EXPLICITLY asked
        if include_personal_facts:
            relevant_facts = self.search_memory_for_facts()
            if relevant_facts:
                context_parts.append(f"\nIMPORTANT FACTS TO REMEMBER:\n{relevant_facts}")

        # Add recent conversation (stripped of personal info)
        if self.conversation_history:
            context_parts.append(f"\nRecent chat:")
            for item in self.conversation_history[-3:]:  # Only last 3
                # Skip responses that mention personal info
                response = item['response'][:80]
                if not any(word in response.lower() for word in ['birthday', 'born', 'age', 'born']):
                    context_parts.append(f"{item['user']}: {item['command']}")
                    context_parts.append(f"Sara: {response}")

        return "\n".join(context_parts)

    def search_memory_for_facts(self, query=None):
        """Search long-term memory for relevant facts"""
        try:
            facts = []

            # Load from knowledge/facts.md
            facts_file = os.path.join(self.sara_memory_dir, "knowledge", "facts.md")
            if os.path.exists(facts_file):
                with open(facts_file, 'r') as f:
                    content = f.read()
                    # Extract personal info
                    for line in content.split('\n'):
                        if any(keyword in line.lower() for keyword in ['birthday', 'born', 'age', 'name', 'preference', 'like']):
                            if self.user_name.lower() in line.lower():
                                facts.append(line.strip())

            # Load from SARA_MEMORY.md
            if os.path.exists(self.long_term_memory):
                with open(self.long_term_memory, 'r') as f:
                    content = f.read()
                    # Look for personal info sections
                    sections = content.split('## ')
                    for section in sections:
                        if 'PERSONAL_INFO' in section or 'USER' in section:
                            lines = [l.strip() for l in section.split('\n') if l.strip()]
                            for line in lines[:3]:  # Get first few facts
                                if self.user_name.lower() in line.lower() and len(line) < 200:
                                    facts.append(line)

            # Look at recent daily logs for this session
            import datetime
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            daily_file = os.path.join(self.sara_memory_dir, "daily", f"{today}.md")
            if os.path.exists(daily_file):
                with open(daily_file, 'r') as f:
                    lines = f.readlines()
                    # Get last few exchanges
                    exchanges = []
                    for i in range(len(lines)-1, max(0, len(lines)-50), -1):
                        line = lines[i].strip()
                        if line.startswith(f"**{self.user_name}:**") and any(keyword in line.lower() for keyword in ['born', 'birthday', 'age', 'name', 'am', "i'm", 'like']):
                            # This exchange contains important info
                            fact = line.replace(f"**{self.user_name}:**", "").strip()
                            exchanges.append(f"Today: {fact}")
                    facts.extend(exchanges[-3:])  # Add last 3 relevant exchanges

            if facts:
                return "\n".join(set(facts))  # Remove duplicates
            return ""

        except Exception as e:
            logger.error(f"Memory search failed: {e}")
            return ""

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

    def extract_speakable_text(self, response, executed_result=None):
        """Extract text to speak - NEVER read code aloud, return actual results if available"""
        import re

        # If we have an execution result with actual content, use that
        if executed_result and executed_result.strip():
            # Clean up the result for speaking
            result = executed_result[:400]
            # Remove excessive whitespace
            result = re.sub(r'\s+', ' ', result)
            # Remove markdown asterisks
            result = re.sub(r'\*\*', '', result)
            result = re.sub(r'\*', '', result)
            # Remove any phrases about "written code" or "check screen"
            result = re.sub(r'.*(written the code|check the screen|look at the terminal).*', '', result, flags=re.IGNORECASE)
            return result.strip() or self.clean_text(response)

        return self.clean_text(response)

    def clean_text(self, response):
        """Clean response text for speaking"""
        import re

        # Print full response to console only (with code)
        print(f"\n[Full Response - See console for code]\n")

        # Remove ALL code blocks completely
        text = re.sub(r'```.*?```', '', response, flags=re.DOTALL)

        # Remove inline code
        text = re.sub(r'`[^`]+`', '', text)

        # Remove markdown formatting (asterisks for bold/italic)
        text = re.sub(r'\*\*', '', text)  # Remove **
        text = re.sub(r'\*', '', text)     # Remove single *
        text = re.sub(r'__', '', text)     # Remove __
        text = re.sub(r'_', ' ', text)     # Replace _ with space
        text = re.sub(r'#+ ', '', text)    # Remove markdown headers

        # Remove "written the code" type phrases
        text = re.sub(r'\b(written the code|check the screen|look at the terminal|i\'ve written|i have written).*', '', text, flags=re.IGNORECASE)

        # Clean up whitespace
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)

        return text.strip()[:400]

    def process_command(self, command):
        """Process user command, execute if needed, and stay in conversation mode"""
        logger.info(f"🧠 Processing: {command}")

        cmd_lower = command.lower()

        # Check for custom website scraping (weather)
        if any(phrase in cmd_lower for phrase in ['scrape weather', 'get weather from', 'weather from site']):
            # Extract URL if provided
            url = None
            if 'http' in command:
                import re
                url_match = re.search(r'(https?://[^\s]+)', command)
                if url_match:
                    url = url_match.group(1)

            if not url:
                # Default weather sites
                url = 'https://weather.com'

            response = self.perform_custom_scrape(url, "weather")
            if response:
                speakable = self.extract_speakable_text(response)
                self.speak(speakable)
                self.save_conversation_memory(command, response)
                self.follow_up_mode = True
                self.listen_for_follow_up()
            return

        # Check for custom website scraping (news)
        if any(phrase in cmd_lower for phrase in ['scrape news', 'get news from', 'news from site', 'local news']):
            url = None
            if 'http' in command:
                import re
                url_match = re.search(r'(https?://[^\s]+)', command)
                if url_match:
                    url = url_match.group(1)

            if not url:
                # Default local news or popular sites
                url = 'https://www.cnn.com'  # or local news site

            response = self.perform_custom_scrape(url, "news")
            if response:
                speakable = self.extract_speakable_text(response)
                self.speak(speakable)
                self.save_conversation_memory(command, response)
                self.follow_up_mode = True
                self.listen_for_follow_up()
            return

        # Check for custom website scraping (general)
        if any(phrase in cmd_lower for phrase in ['scrape', 'scrape website', 'parse site', 'get content from']):
            url = None
            if 'http' in command:
                import re
                url_match = re.search(r'(https?://[^\s]+)', command)
                if url_match:
                    url = url_match.group(1)

            if url:
                response = self.perform_custom_scrape(url, "general")
                if response:
                    speakable = self.extract_speakable_text(response)
                    self.speak(speakable)
                    self.save_conversation_memory(command, response)
                    self.follow_up_mode = True
                    self.listen_for_follow_up()
            else:
                self.speak("I need a website URL to scrape. Say 'scrape' followed by the website address.")
                self.follow_up_mode = True
                self.listen_for_follow_up()
            return

        # Check for weather requests - auto search
        if any(phrase in cmd_lower for phrase in ['weather', 'what\'s the weather', 'what is the weather', 'weather in', 'weather for']):
            query = command
            # Extract location if mentioned
            for phrase in ['weather in', 'weather for', 'in']:
                if phrase in cmd_lower:
                    query = command.split(phrase, 1)[-1].strip() or "weather"
                    break
            
            response = self.perform_web_search(f"weather {query}")
            if response:
                speakable = self.extract_speakable_text(response)
                self.speak(speakable)
                self.save_conversation_memory(command, response)
                self.follow_up_mode = True
                self.listen_for_follow_up()
            return
        
        # Check for web search requests - ONLY explicit commands
        if any(phrase in cmd_lower for phrase in ['search for', 'look up', 'google', 'find online', 'web search', 'search the web for']):
            query = command
            # Extract search query
            for phrase in ['search for', 'look up', 'google', 'web search']:
                if phrase in cmd_lower:
                    query = command.split(phrase, 1)[-1].strip()
                    break
            # Handle weather specially
            if 'weather' in cmd_lower:
                city = cmd_lower.split('weather')[-1].strip().replace('in', '').strip()
                if city:
                    query = f"weather in {city}"

            response = self.perform_web_search(query)
            if response:
                speakable = self.extract_speakable_text(response)
                self.speak(speakable)
                self.save_conversation_memory(command, response)
                self.follow_up_mode = True
                self.listen_for_follow_up()
            return

        # Check for HER MEMORY (conversation/knowledge) - NOT system RAM
        if any(phrase in cmd_lower for phrase in ['your memory', 'check your memory', 'what do you remember', 'what do you know', 'show me what you know']):
            if 'ram' in cmd_lower or 'system' in cmd_lower or 'hardware' in cmd_lower:
                # They want system RAM, handle below
                pass
            else:
                # They want HER MEMORY - check facts
                facts = self.search_memory_for_facts()
                response = f"I remember: {facts}\n\nI also have {self.get_memory_stats().get('daily_logs', 0)} days of conversation history and access to {len(self.sara_memory_dir)} memory files."
                self.speak(response)
                self.save_conversation_memory(command, response)
                self.follow_up_mode = True
                self.listen_for_follow_up()
                return

        # Rest of existing process_command logic...

        # Check if this is a direct system command request
        direct_command = None
        cmd_lower = command.lower()

        # Patterns that indicate user wants command execution (SYSTEM commands)
        if any(phrase in cmd_lower for phrase in ['check ', 'run ', 'execute ', 'show ', 'display ', 'what is', 'tell me', 'who is', 'get ', 'find ', 'list ', 'status', 'ip address', 'firewall', 'ports', 'disk', 'cpu', 'processes', 'users', 'uptime', 'time', 'date', 'os', 'operating system', 'hostname', 'kernel']):
            # Try to extract shell command intent
            if 'firewall' in cmd_lower or 'ufw' in cmd_lower:
                direct_command = 'sudo ufw status'
            elif 'ip address' in cmd_lower or 'my ip' in cmd_lower or 'whats my ip' in cmd_lower:
                direct_command = 'ip addr show | grep "inet " | head -3'
            elif 'who is' in cmd_lower or 'current user' in cmd_lower:
                direct_command = 'whoami'
            elif 'disk' in cmd_lower or 'space' in cmd_lower or 'storage' in cmd_lower:
                direct_command = 'df -h'
            elif 'ram' in cmd_lower or 'system memory' in cmd_lower or ('memory' in cmd_lower and 'free' in cmd_lower):
                direct_command = 'free -h'
            elif 'cpu' in cmd_lower or 'processor' in cmd_lower:
                direct_command = 'lscpu | head -10'
            elif 'uptime' in cmd_lower or 'how long' in cmd_lower:
                direct_command = 'uptime'
            elif 'users' in cmd_lower and 'logged' in cmd_lower:
                direct_command = 'who'
            elif 'ports' in cmd_lower or 'listening' in cmd_lower:
                direct_command = 'ss -tlnp | head -10'
            elif 'processes' in cmd_lower or 'running' in cmd_lower:
                direct_command = 'ps aux | head -10'
            elif 'time' in cmd_lower or 'what time' in cmd_lower or 'current time' in cmd_lower:
                direct_command = 'date "+%I:%M %p %Z on %A, %B %d"'
            elif 'date' in cmd_lower or 'what day' in cmd_lower or 'today' in cmd_lower:
                direct_command = 'date "+%A, %B %d, %Y"'
            elif 'os' in cmd_lower or 'operating system' in cmd_lower:
                direct_command = 'cat /etc/os-release | grep -E "^(NAME|VERSION)" | head -2'
            elif 'hostname' in cmd_lower or 'computer name' in cmd_lower:
                direct_command = 'hostname'
            elif 'kernel' in cmd_lower or 'linux version' in cmd_lower:
                direct_command = 'uname -r'

        # If direct command detected, execute it
        executed_result = None
        if direct_command:
            logger.info(f"🔧 Executing direct command: {direct_command}")
            executed_result = self.execute_command(direct_command)
            response = f"I've checked that for you.\n\nCommand: {direct_command}\nResult:\n{executed_result}"
        else:
            # Use LLM for complex queries - NO AUTO CODE EXECUTION
            response = self.query_llm(command)
            # Only execute if user explicitly asks to run something
            if response and any(phrase in cmd_lower for phrase in ['run this', 'execute this', 'do this', 'execute command', 'run command']):
                response, executed_result = self.extract_and_execute_commands(response)
            else:
                executed_result = None

        if response:
            # Check for repetitive responses
            penalty, response = self.check_response_repeat(response)
            
            # Extract speakable parts
            speakable = self.extract_speakable_text(response, executed_result)
            self.speak(speakable)

            # Store for repeat checking
            self.store_response(speakable)

            self.save_conversation_memory(command, response)
            # Always enter follow-up mode after every response
            self.follow_up_mode = True
            self.listen_for_follow_up()
        else:
            self.speak("Connection issue.")

    def listen_for_follow_up(self):
        """Keep listening for follow-up commands. Returns to wake word only after 2 min silence or exit phrase."""
        logger.info("⏱️ Follow-up mode active (2 min timeout)...")
        # Just show quietly on console, don't speak
        print("[Waiting for next input...]")

        silence_start = time.time()

        # Exit phrases - say these to end conversation
        exit_phrases = [
            "that's all", "sara that's all", "bye", "sara bye", "goodbye",
            "stop listening", "stop", "we're done", "done", "end",
            "go away", "leave me alone", "quiet", "sleep"
        ]

        while True:
            try:
                # Listen for next command with shorter timeout to check frequently
                command = None
                if not SPEECH_AVAILABLE:
                    command = self.keyboard_command_timeout(2)  # Check every 2 seconds
                else:
                    command = self.voice_command_timeout(2)

                if command:
                    # Check for exit phrases first
                    cmd_lower = command.lower().strip()
                    is_exit = any(phrase in cmd_lower for phrase in exit_phrases)

                    if is_exit:
                        logger.info(f"👋 Exit phrase detected: '{command}' - returning to wake word mode")
                        self.speak(f"Okay {self.user_name}, I'll be here when you need me. Just say '{self.wake_word}'.")
                        self.follow_up_mode = False
                        logger.info("👂 Now listening for wake word 'sara'...")
                        break

                    # Got a command, reset silence timer
                    silence_start = time.time()
                    self.process_command(command)
                    # After processing, continue the follow-up loop
                    silence_start = time.time()
                    logger.info("⏱️ Continuing follow-up mode...")
                else:
                    # Check if 2 minutes of silence passed
                    elapsed = time.time() - silence_start
                    if elapsed >= self.follow_up_timeout:
                        logger.info("⏱️ 2 min silence, returning to wake word mode")
                        self.speak("Let me know when you need me. Just say 'sara'.")
                        self.follow_up_mode = False
                        break
                    # Otherwise keep listening

            except Exception as e:
                logger.error(f"Follow-up error: {e}")
                break

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

    def perform_web_search(self, query):
        """Search the web using DuckDuckGo + BeautifulSoup and save results"""
        try:
            self.speak(f"Searching for {query}...")
            logger.info(f"🌐 Web search: {query}")

            import requests
            import re
            from bs4 import BeautifulSoup
            import urllib.parse

            search_results = []

            # Use DuckDuckGo HTML search (no API key needed)
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }

                # Search DuckDuckGo
                ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
                resp = requests.get(ddg_url, headers=headers, timeout=15)

                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')

                    # Extract search results
                    results = soup.find_all('a', class_='result__a', limit=3)
                    snippets = soup.find_all('a', class_='result__snippet', limit=3)

                    for i, (link, snippet) in enumerate(zip(results, snippets)):
                        title = link.get_text(strip=True)
                        url = link.get('href', '')
                        desc = snippet.get_text(strip=True) if snippet else 'No description'

                        if title and url:
                            search_results.append({
                                'title': title,
                                'url': url,
                                'description': desc[:200]
                            })

                # If no results from DDG, try alternative
                if not search_results:
                    # Try to get from Wikipedia for factual queries
                    if any(word in query.lower() for word in ['what is', 'who is', 'definition', 'meaning']):
                        wiki_term = query.replace('what is', '').replace('who is', '').replace('definition', '').replace('meaning', '').strip()
                        wiki_term = wiki_term.replace(' ', '_')
                        wiki_url = f"https://en.wikipedia.org/wiki/{wiki_term}"

                        wiki_resp = requests.get(wiki_url, headers=headers, timeout=10)
                        if wiki_resp.status_code == 200:
                            wiki_soup = BeautifulSoup(wiki_resp.text, 'html.parser')
                            content = wiki_soup.find('div', {'id': 'mw-content-text'})
                            if content:
                                paragraphs = content.find_all('p', limit=3)
                                wiki_text = ' '.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                                search_results.append({
                                    'title': f'Wikipedia: {wiki_term.replace("_", " ")}',
                                    'url': wiki_url,
                                    'description': wiki_text[:300]
                                })

            except Exception as search_err:
                logger.error(f"Search error: {search_err}")
                search_results = []

            # Format results for LLM
            if search_results:
                web_context = f"Web search results for '{query}':\n\n"
                for i, result in enumerate(search_results, 1):
                    web_context += f"{i}. {result['title']}\n   URL: {result['url']}\n   {result['description']}\n\n"
            else:
                web_context = f"No web results found for '{query}'."

            # Query LLM with web context
            context = self.get_conversation_context()

            resp = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'sara-uncensored',
                    'prompt': f"{context}\n\nI searched the web for: {query}\n\n{web_context}\n\nBased on these search results, provide a concise, accurate answer. If the results don't contain the answer, say so.\n\n{self.user_name}: {query}\nSara:",
                    'stream': False,
                    'options': {'temperature': 0.7, 'num_predict': 200}
                },
                timeout=30
            )

            if resp.status_code == 200:
                llm_response = resp.json().get('response', 'Search complete.')
            else:
                llm_response = "I searched but couldn't synthesize the results."

            # Save search to memory
            saved_file = self.save_web_search_result(query, web_context, llm_response)

            full_response = f"{llm_response}\n\n[Search saved: {len(search_results)} results]"
            return full_response

        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return f"I couldn't complete the search: {str(e)}"

    def save_web_search_result(self, query, raw_results, summary):
        """Save web search results to memory"""
        try:
            import datetime
            import hashlib
            timestamp = datetime.datetime.now()
            date_str = timestamp.strftime("%Y-%m-%d")
            time_str = timestamp.strftime("%H:%M:%S")

            search_id = hashlib.md5(f"{query}_{timestamp}".encode()).hexdigest()[:8]
            search_file = os.path.join(self.sara_memory_dir, "web_searches", f"{date_str}_{search_id}.md")

            content = f"# Web Search - {timestamp.strftime('%Y-%m-%d %H:%M')}\n\n"
            content += f"**Query:** {query}\n\n"
            content += f"**Raw Results:**\n{raw_results}\n\n"
            content += f"**Summary:**\n{summary}\n\n"
            content += f"---\n*Searched by {self.user_name}*\n"

            with open(search_file, 'w') as f:
                f.write(content)

            # Also log to daily memory
            self.log_to_daily_memory(f"[Web Search] {query}", f"{summary[:150]}... | Saved: {search_file}", "web_search")

            logger.info(f"🌐 Web search saved: {search_file}")
            return search_file
        except Exception as e:
            logger.error(f"Failed to save web search: {e}")
            return None

    def perform_custom_scrape(self, url, scrape_type="general"):
        """Generate and execute a custom Python scraping script"""
        try:
            self.speak(f"Scraping {scrape_type} from {url}...")
            logger.info(f"🔍 Custom scrape: {url} ({scrape_type})")

            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # Generate appropriate scraping script based on type
            if scrape_type == "weather":
                script = f'''import requests
from bs4 import BeautifulSoup
import json

url = "{url}"
headers = {{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}}

try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Common weather selectors
    weather_data = {{}}

    # Try to find temperature
    temp_selectors = ['.temp', '.temperature', '#temp', '.weather-temp', '[class*="temp"]']
    for selector in temp_selectors:
        elem = soup.select_one(selector)
        if elem:
            weather_data['temperature'] = elem.get_text(strip=True)
            break

    # Try to find condition
    condition_selectors = ['.condition', '.weather-condition', '#condition', '[class*="condition"]']
    for selector in condition_selectors:
        elem = soup.select_one(selector)
        if elem:
            weather_data['condition'] = elem.get_text(strip=True)
            break

    # Try to find location
    location_selectors = ['.location', '#location', '.city', '[class*="location"]']
    for selector in location_selectors:
        elem = soup.select_one(selector)
        if elem:
            weather_data['location'] = elem.get_text(strip=True)
            break

    # Get page title as fallback
    if not weather_data.get('location'):
        weather_data['location'] = soup.title.string if soup.title else 'Unknown'

    # Get any visible text that might contain weather info
    paragraphs = soup.find_all(['p', 'div'], limit=5)
    weather_data['raw_snippet'] = ' '.join([p.get_text(strip=True)[:100] for p in paragraphs[:3]])

    print(json.dumps(weather_data, indent=2))

except Exception as e:
    print(f"Error: {{str(e)}}")'''

            elif scrape_type == "news":
                script = f'''import requests
from bs4 import BeautifulSoup
import json

url = "{url}"
headers = {{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}}

try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = []

    # Common news article selectors
    article_selectors = ['article', '.article', '.news-item', '.story', '[class*="news"]', '[class*="headline"]']

    for selector in article_selectors[:3]:  # Try first 3 selectors
        articles = soup.select(selector, limit=5)
        if articles:
            for article in articles:
                # Try to get headline
                headline = None
                for h_tag in ['h1', 'h2', 'h3', '.headline', '.title']:
                    elem = article.select_one(h_tag)
                    if elem:
                        headline = elem.get_text(strip=True)
                        break

                # Try to get summary/link
                summary = article.get_text(strip=True)[:200]
                link_elem = article.find('a', href=True)
                link = link_elem['href'] if link_elem else ''

                if headline or summary:
                    news_items.append({{
                        'headline': headline or 'No headline',
                        'summary': summary,
                        'link': link
                    }})

            if news_items:
                break  # Found articles, stop trying selectors

    # If no articles found, try getting page sections
    if not news_items:
        sections = soup.find_all(['section', 'div'], limit=10)
        for section in sections:
            text = section.get_text(strip=True)
            if len(text) > 50 and len(text) < 500:
                news_items.append({{
                    'headline': 'Section',
                    'summary': text[:200],
                    'link': ''
                }})

    result = {{
        'source': url,
        'articles': news_items[:5],
        'page_title': soup.title.string if soup.title else 'No title'
    }}

    print(json.dumps(result, indent=2))

except Exception as e:
    print(f"Error: {{str(e)}}")'''

            else:  # General scrape
                script = f'''import requests
from bs4 import BeautifulSoup
import json

url = "{url}"
headers = {{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}}

try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract key information
    data = {{
        'url': url,
        'title': soup.title.string if soup.title else 'No title',
        'headings': [],
        'paragraphs': [],
        'links': []
    }}

    # Get headings
    for h in soup.find_all(['h1', 'h2', 'h3'], limit=5):
        text = h.get_text(strip=True)
        if text:
            data['headings'].append(text[:100])

    # Get paragraphs
    for p in soup.find_all('p', limit=8):
        text = p.get_text(strip=True)
        if len(text) > 20:
            data['paragraphs'].append(text[:150])

    # Get links
    for a in soup.find_all('a', href=True, limit=5):
        text = a.get_text(strip=True)
        if text and len(text) > 5:
            data['links'].append({{
                'text': text[:50],
                'url': a['href'][:100]
            }})

    print(json.dumps(data, indent=2))

except Exception as e:
    print(f"Error: {{str(e)}}")'''

            # Execute the script
            output = self.execute_python_script(script)

            # Save scrape results
            scrape_dir = os.path.join(self.sara_memory_dir, "web_scrapes")
            os.makedirs(scrape_dir, exist_ok=True)

            scrape_file = os.path.join(scrape_dir, f"{scrape_type}_{timestamp}.md")
            with open(scrape_file, 'w') as f:
                f.write(f"# {scrape_type.upper()} Scrape - {url}\n\n")
                f.write(f"**URL:** {url}\n")
                f.write(f"**Time:** {datetime.datetime.now().isoformat()}\n\n")
                f.write("**Results:**\n```json\n")
                f.write(output)
                f.write("\n```\n")

            logger.info(f"🔍 Scrape saved: {scrape_file}")

            # Return summary
            if scrape_type == "weather":
                return f"Weather data scraped from {url}. Results saved. Check console for details."
            elif scrape_type == "news":
                return f"News articles scraped from {url}. Results saved. Check console for details."
            else:
                return f"Content scraped from {url}. Results saved to {scrape_file}"

        except Exception as e:
            logger.error(f"Scrape failed: {e}")
            return f"Scraping failed: {str(e)}"

    def check_response_repeat(self, response):
        """Check if response is too similar to recent ones, return penalty multiplier"""
        if not self.recent_responses:
            return 1.0, response

        response_lower = response.lower().strip()

        for recent in self.recent_responses:
            recent_lower = recent.lower().strip()

            # Check for exact match or high similarity
            if response_lower == recent_lower:
                return 0.1, self.make_response_different(response)

            # Check for phrase overlap
            if len(response_lower) > 20 and len(recent_lower) > 20:
                # Check first 50 chars
                prefix_match = response_lower[:50] == recent_lower[:50]
                # Check last 50 chars
                suffix_match = response_lower[-50:] == recent_lower[-50:]

                if prefix_match or suffix_match:
                    logger.warning("🔄 Similar response detected - adding variation")
                    return 0.3, self.make_response_different(response)

        return 1.0, response

    def make_response_different(self, response):
        """Modify a repetitive response to make it different"""
        variations = [
            f"Got it. {response}",
            f"Understood. {response}",
            f"Okay - {response}",
            response.replace("I'll ", "I will ").replace("I'm ", "I am "),
        ]
        return variations[hash(response) % len(variations)]

    def store_response(self, response):
        """Store response for repeat checking"""
        self.recent_responses.append(response.lower().strip()[:100])
        if len(self.recent_responses) > self.max_recent_responses:
            self.recent_responses.pop(0)

    def query_llm(self, command):
        """Query LLM with strict rules: concise, no speculation, execute for facts"""
        try:
            # Check if user wants a joke or casual conversation
            cmd_lower = command.lower()
            wants_fun = any(phrase in cmd_lower for phrase in ['joke', 'funny', 'tell me something', 'make me laugh', 'humor'])
            asking_personal = any(phrase in cmd_lower for phrase in [
                'my birthday', 'when is my birthday', 'what is my birthday',
                'my age', 'how old am i', 'what is my age',
                'what do you remember about me', 'what do you know about me',
                'tell me about me', 'what do you remember'
            ])
            
            context = self.get_conversation_context(include_personal_facts=asking_personal)
            import requests

            # Get current system time
            import datetime
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

            # Choose prompt style based on request
            if wants_fun:
                strict_prompt = f"""{context}

You are Sara, Boo's fun AI assistant.

RULES:
1. For jokes - be clever and concise, max 2-3 sentences
2. For casual chat - be friendly and brief
3. For system questions - use these tools:
   - Time: ```bash\ndate\n```
   - RAM: ```bash\nfree -h\n```
   - Disk: ```bash\ndf -h\n```
4. Be warm and personable, not robotic

Boo: {command}
Sara:"""
            else:
                # STRICT PROMPT - prevent rambling and false info
                strict_prompt = f"""{context}

You are Sara, an AI assistant running on a Linux PC.

AVAILABLE TOOLS - USE THESE TO DISCOVER SYSTEM INFO:
- System time: ```bash\ndate\n```
- RAM usage: ```bash\nfree -h\n```
- Disk space: ```bash\ndf -h\n```
- IP address: ```bash\nip addr show\n```
- CPU info: ```bash\nlscpu\n```
- OS info: ```bash\ncat /etc/os-release\n```
- Hostname: ```bash\nhostname\n```
- Kernel: ```bash\nuname -r\n```

ABSOLUTE RULES:
1. Answer ONLY what was asked - ONE short sentence
2. NEVER make up system info - USE THE TOOLS ABOVE to discover it
3. When asked "what time is it" - provide ```bash\ndate\n``` then give result
4. When asked "how much ram" - provide ```bash\nfree -h\n``` then give result
5. When asked about system info - USE THE COMMAND then report the ACTUAL result
6. NO hardcoded answers - always use tools to discover current state
7. MAX 1-2 sentences. Be BRIEF.
8. NO "I've written the code" - just provide the command and I will execute and speak the result

Boo: {command}
Sara:"""
            resp = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'sara-uncensored',
                    'prompt': strict_prompt,
                    'stream': False,
                    'options': {'temperature': 0.3, 'num_predict': 150}
                },
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json().get('response', '...')
            return "Error."
        except Exception as e:
            logger.error(f"LLM failed: {e}")
            return "System error."

    def sara_monitoring_access(self):
        pass

    def execute_command(self, command_str):
        """Execute a shell command and return the result"""
        try:
            result = subprocess.run(
                command_str,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout if result.stdout else result.stderr if result.stderr else "Command executed (no output)"
            output_str = output.strip()[:500]  # Limit output length for TTS

            # Save command execution results
            self.save_command_execution(command_str, output_str)

            return output_str
        except subprocess.TimeoutExpired:
            self.save_command_execution(command_str, "Command timed out after 30 seconds")
            return "Command timed out after 30 seconds"
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            self.save_command_execution(command_str, error_msg)
            return error_msg

    def save_command_execution(self, command_str, output):
        """Save executed shell command and its results to disk"""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # Create commands directory
            commands_dir = os.path.join(self.workspace_dir, "executed_commands")
            os.makedirs(commands_dir, exist_ok=True)

            # Save the result
            result_file = os.path.join(commands_dir, f"cmd_{timestamp}.txt")
            with open(result_file, 'w') as f:
                f.write(f"Command: {command_str}\n")
                f.write(f"Time: {datetime.datetime.now().isoformat()}\n")
                f.write(f"User: {self.user_name}\n")
                f.write("="*50 + "\n")
                f.write("OUTPUT:\n")
                f.write(output)

            # Add to memory
            self.command_results = getattr(self, 'command_results', {})
            self.command_results[timestamp] = {
                'command': command_str,
                'result_file': result_file,
                'output_preview': output[:200]
            }

            logger.info(f"💾 Command result saved: {result_file}")

        except Exception as e:
            logger.error(f"Failed to save command: {e}")

    def execute_python_script(self, script_content):
        """Execute a Python script and return the result"""
        try:
            # Create a temporary Python file
            import tempfile
            import os

            # Clean up the script content
            script_lines = script_content.strip().split('\n')
            # Remove any markdown formatting markers
            clean_lines = []
            for line in script_lines:
                if line.strip() and not line.strip().startswith('```'):
                    clean_lines.append(line)

            script_content = '\n'.join(clean_lines)

            # Write to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(script_content)
                temp_file = f.name

            # Execute the script
            result = subprocess.run(
                ['python3', temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Clean up temp file
            os.unlink(temp_file)

            output = result.stdout if result.stdout else result.stderr if result.stderr else "Script completed (no output)"
            output = output.strip()

            # Save script and results for future reference
            self.save_script_execution(script_content, output)

            return output[:500]  # Limit output for TTS

        except subprocess.TimeoutExpired:
            return "Python script timed out after 30 seconds"
        except Exception as e:
            return f"Error running Python script: {str(e)}"

    def save_script_execution(self, script_content, output):
        """Save executed Python script and its results to disk"""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # Create scripts directory
            scripts_dir = os.path.join(self.workspace_dir, "executed_scripts")
            os.makedirs(scripts_dir, exist_ok=True)

            # Save the script
            script_file = os.path.join(scripts_dir, f"script_{timestamp}.py")
            with open(script_file, 'w') as f:
                f.write(script_content)

            # Save the results
            result_file = os.path.join(scripts_dir, f"result_{timestamp}.txt")
            with open(result_file, 'w') as f:
                f.write(f"Script: {script_file}\n")
                f.write(f"Time: {datetime.datetime.now().isoformat()}\n")
                f.write(f"User: {self.user_name}\n")
                f.write("="*50 + "\n")
                f.write("OUTPUT:\n")
                f.write(output)

            # Add to memory for quick recall
            self.script_results = getattr(self, 'script_results', {})
            self.script_results[timestamp] = {
                'script_file': script_file,
                'result_file': result_file,
                'output_preview': output[:200]
            }

            # Save to conversation memory
            self.conversation_history.append({
                'user': self.user_name,
                'command': f"[Python Script Executed]",
                'response': f"Script saved to {script_file}, result in {result_file}"
            })

            # Persist to disk
            with open(self.conversation_file, 'w') as f:
                json.dump({
                    'user_name': self.user_name,
                    'user_role': self.user_role,
                    'history': self.conversation_history,
                    'script_results': getattr(self, 'script_results', {})
                }, f)

            logger.info(f"💾 Script saved: {script_file}")

        except Exception as e:
            logger.error(f"Failed to save script: {e}")

    def extract_and_execute_commands(self, llm_response):
        """Extract shell commands from LLM response and execute them"""
        import re

        # Match code blocks with bash/shell
        bash_pattern = r'```(?:bash|shell)?\n(.*?)```'
        bash_matches = re.findall(bash_pattern, llm_response, re.DOTALL)

        # Match inline commands after phrases like "run:" or just backticks
        inline_pattern = r'`([^`]+)`'
        inline_matches = re.findall(inline_pattern, llm_response)

        all_commands = []

        # Parse bash blocks - extract commands line by line
        for block in bash_matches:
            for line in block.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('//'):
                    all_commands.append(line)

        # Parse inline commands that look like shell commands
        for cmd in inline_matches:
            if any(cmd.strip().startswith(char) for char in ['ls', 'cat', 'ping', 'ifconfig', 'ip ', 'curl', 'wget', 'systemctl', 'ps ', 'top', 'df ', 'du ', 'find ', 'grep ', 'awk ', 'sed ', 'echo ', 'touch ', 'mkdir', 'cd ', 'pwd', 'whoami', 'uname', 'lsb_', 'cat ', 'head ', 'tail ', 'less ', 'more ', 'nc ', 'netstat', 'ss ', 'lsof', 'free', 'vmstat', 'iostat', 'mpstat', 'ps', 'top', 'htop', 'kill', 'pkill']):
                all_commands.append(cmd.strip())

        # Also check for Python scripts
        python_pattern = r'```python\n(.*?)```'
        python_matches = re.findall(python_pattern, llm_response, re.DOTALL)

        if python_matches:
            # Execute the first Python script found
            script_content = python_matches[0]
            output = self.execute_python_script(script_content)
            enhanced_response = f"{llm_response}\n\n[Executed Python script]\nResult:\n{output}"
            return enhanced_response, output  # Return the actual output

        if not all_commands:
            return llm_response, None

        # Execute the first valid command
        for cmd in all_commands:
            if cmd and len(cmd) > 2:
                output = self.execute_command(cmd)
                # Append command output to response
                enhanced_response = f"{llm_response}\n\n[Executed: {cmd}]\nResult:\n{output}"
                return enhanced_response, output  # Return the actual output, not just the command

        return llm_response, None

    def shutdown(self):
        logger.info("🛑 Stopping")
        self.running = False

    def run(self):
        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            self.shutdown()


class SaraWebUI:
    """Web interface for Sara Voice Agent - view logs, history, send commands"""

    def __init__(self, voice_agent):
        self.voice_agent = voice_agent
        self.app = None
        self.port = 8081

    def get_logs(self, lines=50):
        """Get recent log entries"""
        try:
            log_file = '/home/sarabot/.openclaw/workspace/logs/sara_voice.log'
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    return f.readlines()[-lines:]
            return []
        except Exception as e:
            return [f"Error reading logs: {e}"]

    def get_conversation_history(self):
        """Get recent conversation history"""
        return self.voice_agent.conversation_history[-20:]  # Last 20 exchanges

    def run_web_server(self):
        """Run Flask web server"""
        try:
            from flask import Flask, render_template_string, request, jsonify, Response
            import queue

            self.app = Flask(__name__)

            # HTML template for the web UI
            HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sara Voice Agent - Web UI</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eaeaea;
            padding: 20px;
            line-height: 1.6;
        }
        h1 { color: #00d4aa; margin-bottom: 20px; font-size: 28px; }
        h2 { color: #00d4aa; margin: 30px 0 15px 0; font-size: 20px; border-bottom: 2px solid #00d4aa; padding-bottom: 10px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .status {
            background: #16213e;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #00d4aa;
        }
        .status-pid { color: #888; font-size: 14px; }
        .status-running { color: #00d4aa; font-weight: bold; }
        .panel {
            background: #16213e;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .log-window {
            background: #0f0f1e;
            border: 1px solid #333;
            border-radius: 6px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.5;
        }
        .log-entry {
            padding: 2px 0;
            border-bottom: 1px solid #1a1a2e;
        }
        .log-time { color: #666; }
        .log-info { color: #4da6ff; }
        .log-error { color: #ff6b6b; }
        .log-warn { color: #ffd93d; }
        .log-success { color: #6bcf7f; }

        .conversation-item {
            background: #0f0f1e;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 10px;
        }
        .conv-user { color: #ffd93d; font-weight: bold; margin-bottom: 5px; }
        .conv-response { color: #eaeaea; padding-left: 20px; border-left: 2px solid #00d4aa; }
        .conv-time { color: #666; font-size: 12px; margin-top: 5px; }

        .command-box {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .command-input {
            flex: 1;
            background: #0f0f1e;
            border: 1px solid #333;
            border-radius: 6px;
            padding: 12px 15px;
            color: #eaeaea;
            font-size: 16px;
        }
        .command-input:focus {
            outline: none;
            border-color: #00d4aa;
        }
        .btn {
            background: #00d4aa;
            color: #1a1a2e;
            border: none;
            border-radius: 6px;
            padding: 12px 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .btn:hover { opacity: 0.9; }
        .btn-secondary {
            background: #333;
            color: #eaeaea;
        }

        .quick-commands {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }
        .quick-btn {
            background: #1a1a2e;
            border: 1px solid #444;
            color: #eaeaea;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }
        .quick-btn:hover {
            background: #00d4aa;
            color: #1a1a2e;
            border-color: #00d4aa;
        }

        .refresh-btn {
            float: right;
            background: #333;
            color: #eaeaea;
            padding: 8px 15px;
            border-radius: 6px;
            cursor: pointer;
            border: none;
            font-size: 14px;
        }
        .refresh-btn:hover { background: #444; }

        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 15px;
        }
        .tab {
            background: #1a1a2e;
            border: none;
            color: #888;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 6px 6px 0 0;
            font-size: 14px;
        }
        .tab.active {
            background: #00d4aa;
            color: #1a1a2e;
            font-weight: bold;
        }

        @media (max-width: 768px) {
            body { padding: 10px; }
            .log-window { height: 300px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Sara Voice Agent</h1>

        <div class="status">
            <div class="status-running">● Running</div>
            <div class="status-pid">PID: {{pid}} | User: {{user}} | Memory: {{memory_count}} exchanges</div>
        </div>

        <h2>📊 Live Logs <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button></h2>
        <div class="panel">
            <div class="log-window" id="logWindow">
                {% for line in logs %}
                <div class="log-entry">{{line|safe}}</div>
                {% endfor %}
            </div>
        </div>

        <h2>💬 Recent Conversations</h2>
        <div class="panel">
            {% for conv in conversations %}
            <div class="conversation-item">
                <div class="conv-user">{{conv.user}}: {{conv.command}}</div>
                <div class="conv-response">{{conv.response}}</div>
            </div>
            {% endfor %}
        </div>

        <h2>⌨️ Send Command</h2>
        <div class="panel">
            <form action="/command" method="POST">
                <div class="command-box">
                    <input type="text" name="command" class="command-input" placeholder="Type a command to send to Sara..." autofocus>
                    <button type="submit" class="btn">Send</button>
                </div>
            </form>
            <div class="quick-commands">
                <button class="quick-btn" onclick="sendQuick('sara')">Sara (wake)</button>
                <button class="quick-btn" onclick="sendQuick('what is my name?')">What's my name?</button>
                <button class="quick-btn" onclick="sendQuick('check your memory')">Check memory</button>
                <button class="quick-btn" onclick="sendQuick('how much RAM?')">Check RAM</button>
                <button class="quick-btn" onclick="sendQuick('bye')">Goodbye</button>
            </div>
        </div>
    </div>

    <script>
        function sendQuick(text) {
            fetch('/command', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'command=' + encodeURIComponent(text)
            });
        }

        // Auto-refresh logs every 5 seconds
        setInterval(function() {
            fetch('/logs')
                .then(r => r.text())
                .then(html => document.getElementById('logWindow').innerHTML = html);
        }, 5000);
    </script>
</body>
</html>
'''

            @self.app.route('/')
            def index():
                logs = self.get_logs(100)
                # Colorize log entries
                colored_logs = []
                for line in logs:
                    if 'INFO' in line:
                        colored = f'<span class="log-time">{line[:23]}</span> <span class="log-info">{line[23:]}</span>'
                    elif 'ERROR' in line:
                        colored = f'<span class="log-time">{line[:23]}</span> <span class="log-error">{line[23:]}</span>'
                    elif 'WARNING' in line:
                        colored = f'<span class="log-time">{line[:23]}</span> <span class="log-warn">{line[23:]}</span>'
                    else:
                        colored = line
                    colored_logs.append(colored)

                return render_template_string(
                    HTML_TEMPLATE,
                    logs=colored_logs,
                    conversations=self.get_conversation_history(),
                    pid=os.getpid(),
                    user=self.voice_agent.user_name,
                    memory_count=len(self.voice_agent.conversation_history)
                )

            @self.app.route('/logs')
            def get_logs_route():
                logs = self.get_logs(50)
                return ''.join([f'<div class="log-entry">{line}</div>' for line in logs])

            @self.app.route('/command', methods=['POST'])
            def send_command():
                command = request.form.get('command', '').strip()
                if command:
                    logger.info(f"🌐 [Web UI] Command received: {command}")
                    # Process the command in a thread
                    threading.Thread(target=self.voice_agent.process_command, args=(command,)).start()
                    return jsonify({'status': 'sent', 'command': command})
                return jsonify({'status': 'error', 'message': 'No command provided'})

            @self.app.route('/api/status')
            def api_status():
                return jsonify({
                    'running': self.voice_agent.running,
                    'pid': os.getpid(),
                    'user': self.voice_agent.user_name,
                    'memory_count': len(self.voice_agent.conversation_history),
                    'follow_up_mode': self.voice_agent.follow_up_mode
                })

            logger.info(f"🌐 Web UI starting on http://localhost:{self.port}")
            self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)

        except ImportError:
            logger.error("⚠️ Flask not installed. Web UI disabled.")
            logger.info("   Install with: pip3 install flask")
        except Exception as e:
            logger.error(f"Web UI error: {e}")


def main():
    agent = SaraVoiceAgent()
    web_ui = SaraWebUI(agent)

    # Start web server in background thread
    web_thread = threading.Thread(target=web_ui.run_web_server, daemon=True)
    web_thread.start()
    logger.info(f"🌐 Web UI thread started - will be available at http://localhost:8080")

    # Run the voice agent
    agent.run()

if __name__ == "__main__":
    main()
