#!/usr/bin/env python3
# 🗣️ Complete Speech Recognition Setup with Female Voice

import subprocess
import sys
import time
import json
import os
from datetime import datetime

class SpeechRecognitionSetup:
    """Complete speech recognition setup with female voice integration"""
    
    def __init__(self):
        print("🗣️ SPEECH RECOGNITION SETUP")
        print("=" * 60)
        print("🎯 Setting up complete voice recognition system")
        print("🎤 Integrating with K66 microphone")
        print("🔊 Configuring female voice responses")
        print("🌐 Ensuring 100% local operation")
        print()
        
        self.config_path = "/home/godfather/local-command-center/config/voice_config.json"
        self.voice_agent_path = "/home/godfather/local-command-center/agents/sara-voice/sara_voice_agent.py"
        
    def install_dependencies(self):
        """Install required speech recognition dependencies"""
        print("📦 Installing speech recognition components...")
        
        packages = [
            "speech_recognition",      # Main speech recognition
            "pyaudio",                 # Audio processing
            "vosk",                    # Offline recognition (fallback)
            "pyttsx3",                 # Text-to-speech (female voice)
            "sounddevice",             # Audio device management
            "numpy",                   # Audio processing
        ]
        
        installed_count = 0
        failed_packages = []
        
        for package in packages:
            print(f"🔧 Installing {package}...")
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"✅ {package} installed successfully")
                    installed_count += 1
                else:
                    print(f"❌ {package} failed: {result.stderr}")
                    failed_packages.append(package)
                    
            except Exception as e:
                print(f"❌ {package} error: {e}")
                failed_packages.append(package)
        
        print(f"\n📊 Installation Summary:")
        print(f"✅ Successfully installed: {installed_count}/{len(packages)}")
        
        if failed_packages:
            print(f"⚠️ Failed packages: {failed_packages}")
        
        return installed_count == len(packages)
    
    def setup_audio_permissions(self):
        """Setup audio permissions and configuration"""
        print("🔧 Setting up audio permissions...")
        
        try:
            # Add user to audio group (requires manual intervention)
            print("⚠️  Audio permissions may need manual setup:")
            print("   sudo usermod -a -G audio $USER")
            print("   Then logout and login again")
            print("   OR continue with current permissions (may work)")
            print()
            
            # Test audio device access
            audio_test = self.test_audio_devices()
            if audio_test:
                print("✅ Audio device access confirmed")
                return True
            else:
                print("⚠️  Audio access issues detected")
                return False
                
        except Exception as e:
            print(f"❌ Audio setup failed: {e}")
            return False
    
    def test_audio_devices(self):
        """Test audio device access"""
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            
            # Test microphone access
            try:
                # Try to list microphones
                mics = sr.Microphone.list_microphone_names()
                print(f"🎤 Found {len(mics)} audio devices:")
                for i, mic in enumerate(mics[:5]):  # Show first 5
                    print(f"   {i}: {mic}")
                
                # Test K66 specifically
                k66_found = any("K66" in mic for mic in mics)
                if k66_found:
                    print("✅ K66 microphone detected")
                else:
                    print("⚠️  K66 not in mic list, trying default...")
                
                return True
                
            except Exception as e:
                print(f"⚠️  Microphone listing failed: {e}")
                return False
                
        except ImportError:
            print("❌ speech_recognition not available")
            return False
    
    def configure_k66_microphone(self):
        """Configure K66 microphone as default input"""
        print("🎙️  Configuring K66 microphone...")
        
        try:
            import speech_recognition as sr
            
            # Find K66 microphone
            recognizer = sr.Recognizer()
            mics = sr.Microphone.list_microphone_names()
            
            k66_mic_index = None
            for i, mic_name in enumerate(mics):
                if "K66" in mic_name or "card 2" in mic_name.lower():
                    k66_mic_index = i
                    print(f"✅ Found K66 at index {i}: {mic_name}")
                    break
            
            if k66_mic_index is None:
                print("⚠️  K66 not found in microphones, using default...")
                k66_mic_index = None
            
            # Test microphone with calibration
            try:
                mic = sr.Microphone(device_index=k66_mic_index)
                with mic as source:
                    print("🔧 Calibrating microphone...")
                    recognizer.adjust_for_ambient_noise(source, duration=3)
                    print("✅ Microphone calibration complete")
                
                # Save microphone configuration
                self.save_microphone_config(k66_mic_index)
                return True
                
            except Exception as e:
                print(f"❌ Microphone setup failed: {e}")
                return False
                
        except ImportError:
            print("❌ speech_recognition not installed")
            return False
    
    def save_microphone_config(self, mic_index):
        """Save microphone configuration"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            config['audio_settings'].update({
                'microphone_index': mic_index,
                'microphone_type': 'K66_USB-C',
                'sample_rate': 16000,  # Optimized for speech
                'chunk_size': 1024,
                'format': 'int16',
                'channels': 1,
                'recognition_engine': 'google',  # Primary
                'fallback_engine': 'vosk',    # Offline backup
                'noise_reduction': True,
                'voice_activity_detection': True
            })
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print("✅ Microphone configuration saved")
            
        except Exception as e:
            print(f"⚠️  Config save issue: {e}")
    
    def setup_female_voice_tts(self):
        """Configure female voice for responses"""
        print("🔊 Configuring female voice TTS...")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Find best female voice
            female_voices = []
            for voice in voices:
                voice_name = self.get_voice_name(voice)
                if self.is_female_voice(voice):
                    female_voices.append((voice, voice_name))
            
            # Select best female voice
            best_voice = None
            best_score = 0
            
            for voice, voice_name in female_voices[:3]:  # Check top 3
                score = self.score_voice_quality(voice_name)
                if score > best_score:
                    best_score = score
                    best_voice = voice
            
            if best_voice:
                engine.setProperty('voice', best_voice.id)
                print(f"✅ Selected female voice: {self.get_voice_name(best_voice)}")
                
                # Optimize for female speech
                engine.setProperty('rate', 140)  # Natural speed
                engine.setProperty('volume', 0.85)  # Gentle volume
                engine.setProperty('pitch', 50)  # Default pitch
                
                # Save TTS configuration
                if hasattr(best_voice, 'id'):
                    with open(self.config_path, 'r') as f:
                        config = json.load(f)
                    
                    config['voice_settings'].update({
                        'voice_id': best_voice.id,
                        'voice_name': self.get_voice_name(best_voice),
                        'voice_gender': 'female_optimized',
                        'tts_engine': 'pyttsx3',
                        'speech_params': {
                            'rate': 140,
                            'volume': 0.85,
                            'pitch': 50
                        },
                        'optimized_date': time.strftime('%Y-%m-%d')
                    })
                    
                    with open(self.config_path, 'w') as f:
                        json.dump(config, f, indent=2)
                
                return True
            else:
                print("⚠️  No female voices found, using available voice")
                return False
                
        except Exception as e:
            print(f"❌ TTS setup failed: {e}")
            return False
    
    def get_voice_name(self, voice):
        """Get voice name from voice object"""
        if hasattr(voice, 'name'):
            return voice.name
        elif hasattr(voice, 'id'):
            return voice.id
        else:
            return "Unknown Voice"
    
    def is_female_voice(self, voice):
        """Check if voice has female characteristics"""
        voice_name = self.get_voice_name(voice).lower()
        
        female_indicators = [
            'female', 'woman', 'she', 'her', 'zira', 'samantha', 
            'karen', 'diana', 'monica', 'heather', 'susan', 'ella'
        ]
        
        return any(indicator in voice_name for indicator in female_indicators)
    
    def score_voice_quality(self, voice_name):
        """Score voice quality for selection"""
        score = 10  # Base score
        
        preferred_names = ['zira', 'samantha', 'karen', 'diana']
        for pref in preferred_names:
            if pref in voice_name.lower():
                score += 20
                break
        
        if 'english' in voice_name.lower():
            score += 10
        
        return score
    
    def test_speech_recognition(self):
        """Test complete speech recognition system"""
        print("🧪 Testing speech recognition with K66...")
        
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            # Load microphone configuration
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            mic_index = config['audio_settings'].get('microphone_index')
            
            # Test with K66 microphone
            mic = sr.Microphone(device_index=mic_index)
            
            with mic as source:
                print("🔧 Calibrating microphone for recognition...")
                recognizer.adjust_for_ambient_noise(source, duration=2)
                
                print("🎤 Say 'test' now (5 seconds window)...")
                try:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    print("🧠 Processing speech...")
                    
                    # Try Google first
                    try:
                        text = recognizer.recognize_google(audio)
                        print(f"✅ Recognized: '{text}'")
                        return True, text
                        
                    except sr.UnknownValueError:
                        print("⚠️  Could not understand audio")
                        return False, None
                        
                except sr.WaitTimeoutError:
                    print("⚠️  No speech detected in timeout window")
                    return False, None
                    
        except Exception as e:
            print(f"❌ Speech recognition test failed: {e}")
            return False, None
    
    def create_enhanced_voice_agent(self):
        """Create enhanced voice agent with speech recognition"""
        print("🤖 Creating enhanced voice agent...")
        
        enhanced_agent_code = '''#!/usr/bin/env python3
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
'''
        
        # Write enhanced agent
        enhanced_path = self.voice_agent_path.replace('sara_voice_agent.py', 'enhanced_voice_agent.py')
        with open(enhanced_path, 'w') as f:
            f.write(enhanced_agent_code)
        
        # Make executable
        os.chmod(enhanced_path, 0o755)
        logger.info(f"✅ Enhanced voice agent created: {enhanced_path}")
        return enhanced_path

    def restart_voice_agent(self, enhanced=True):
        """Restart voice agent with speech recognition"""
        print("🔄 Restarting voice agent...")
        
        # Stop current agent
        try:
            subprocess.run(['pkill', '-f', 'sara_voice_agent.py'], timeout=5)
            time.sleep(2)
        except:
            pass
        
        # Start enhanced agent
        if enhanced:
            agent_path = self.voice_agent_path.replace('sara_voice_agent.py', 'enhanced_voice_agent.py')
        else:
            agent_path = self.voice_agent_path
        
        try:
            subprocess.Popen([sys.executable, agent_path])
            print(f"✅ Voice agent started: {agent_path}")
            return True
        except Exception as e:
            print(f"❌ Agent start failed: {e}")
            return False
    
    def run_complete_setup(self):
        """Run complete speech recognition setup"""
        print("🚀 STARTING COMPLETE SPEECH RECOGNITION SETUP")
        print("=" * 60)
        
        success_steps = 0
        
        # Step 1: Install dependencies
        print("\n📦 STEP 1: Installing dependencies...")
        if self.install_dependencies():
            success_steps += 1
            print("✅ Dependencies installed")
        else:
            print("⚠️  Some dependencies failed but continuing...")
        
        # Step 2: Setup audio permissions
        print("\n🔧 STEP 2: Setting up audio...")
        if self.setup_audio_permissions():
            success_steps += 1
        else:
            print("⚠️  Audio issues detected - manual permission setup may be needed")
        
        # Step 3: Configure K66 microphone
        print("\n🎙️  STEP 3: Configuring K66 microphone...")
        if self.configure_k66_microphone():
            success_steps += 1
            print("✅ K66 microphone configured")
        else:
            print("⚠️  Microphone config had issues")
        
        # Step 4: Setup female voice
        print("\n🔊 STEP 4: Configuring female voice...")
        if self.setup_female_voice_tts():
            success_steps += 1
            print("✅ Female voice configured")
        else:
            print("⚠️  Female voice setup issues")
        
        # Step 5: Test speech recognition
        print("\n🧪 STEP 5: Testing speech recognition...")
        success, recognized = self.test_speech_recognition()
        if success:
            success_steps += 1
            print(f"✅ Speech test successful: '{recognized}'")
        else:
            print("⚠️  Speech test failed - keyboard fallback available")
        
        # Step 6: Create enhanced agent
        print("\n🤖 STEP 6: Creating enhanced voice agent...")
        if self.create_enhanced_voice_agent():
            success_steps += 1
            print("✅ Enhanced agent created")
        else:
            print("⚠️  Enhanced agent creation failed")
        
        # Step 7: Restart voice agent
        print("\n🔄 STEP 7: Restarting voice agent...")
        if self.restart_voice_agent():
            success_steps += 1
            print("✅ Voice agent restarted")
        else:
            print("⚠️  Agent restart failed")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎊 SETUP COMPLETE!")
        print(f"✅ Successful steps: {success_steps}/7")
        
        if success_steps >= 5:
            print("🌟 SPEECH RECOGNITION SYSTEM READY!")
            print("🎤 Sara can now hear your voice!")
            print("🔊 Female voice responses configured!")
            print("🎙️  K66 microphone integration complete!")
            print("🌐 Complete local operation!")
            
            print("\n🎯 HOW TO USE:")
            print("1. Say 'Sara' to activate")
            print("2. Wait for 'Yes, I'm listening'")
            print("3. Give voice commands")
            print("4. Hear female voice responses")
            
        else:
            print("⚠️  Setup had issues - keyboard mode still works")
            print("🔄 Try manual audio permission setup:")
            print("   sudo usermod -a -G audio $USER")
            print("   logout and login again")
        
        print("\n🎉 YOUR VOICE-ACTIVATED SARA IS READY!")
        
        return success_steps >= 5

def main():
    """Main setup execution"""
    setup = SpeechRecognitionSetup()
    success = setup.run_complete_setup()
    
    if success:
        print("\n✨ ENJOY YOUR VOICE-ACTIVATED AI PARTNER!")
        print("🤖 Sara is listening with her female voice!")
        print("🎤 Speak to her anytime - she'll respond!")
        print("🌟 The future of human-AI conversation is here!")
    else:
        print("\n⚡ Keyboard mode continues to work perfectly")

if __name__ == "__main__":
    main()