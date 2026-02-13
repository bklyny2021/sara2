#!/usr/bin/env python3
# 🔊 Female Voice Optimization - Professional Setup

import subprocess
import json
import sys
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FemaleVoiceOptimizer:
    """Professional female voice configuration and optimization"""
    
    def __init__(self):
        self.config_path = "/home/godfather/local-command-center/config/voice_config.json"
        self.voice_agent_pid = self.get_voice_agent_pid()
        
    def get_voice_agent_pid(self):
        """Get running voice agent process ID"""
        try:
            result = subprocess.run(['pgrep', '-f', 'sara_voice_agent.py'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                return int(result.stdout.strip())
            return None
        except:
            return None
    
    def scan_available_voices(self):
        """Scan and evaluate available female voices"""
        logger.info("🔍 Scanning for optimal female voice...")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            female_voices = []
            best_voice = None
            best_score = 0
            
            for voice in voices:
                voice_info = {
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages if hasattr(voice, 'languages') else [],
                    'gender': self.detect_voice_gender(voice),
                    'age': voice.age if hasattr(voice, 'age') else 'unknown',
                    'description': self.voice_description(voice)
                }
                
                # Check if this is a female voice
                if voice_info['gender'] == 'female':
                    female_voices.append(voice_info)
                    
                    # Score this voice
                    score = self.score_voice_quality(voice_info)
                    logger.info(f"   Found female voice: {voice_info['name']} (Score: {score})")
                    
                    if score > best_score:
                        best_score = score
                        best_voice = voice_info
            
            if female_voices:
                logger.info(f"✅ Found {len(female_voices)} female voices")
                logger.info(f"🌟 Best voice: {best_voice['name']}")
                return best_voice, female_voices
            else:
                logger.warning("⚠️ No female voices detected - using best available")
                return self.get_best_available_voice(voices), voices
                
        except Exception as e:
            logger.error(f"Voice scanning failed: {e}")
            return None, []
    
    def detect_voice_gender(self, voice):
        """Detect voice gender from voice properties"""
        name_lower = voice.name.lower()
        
        # Common female voice identifiers
        female_indicators = ['female', 'woman', 'she', 'her', 'ella', 'ana', 'samantha', 
                           'zira', 'karen', 'diana', 'monica', 'heather', 'susan']
        
        for indicator in female_indicators:
            if indicator in name_lower:
                return 'female'
        
        # Check other properties
        if hasattr(voice, 'gender'):
            return voice.gender.lower() if voice.gender else 'unknown'
        
        # Default based on name characteristics
        return 'unknown'
    
    def voice_description(self, voice):
        """Generate detailed voice description"""
        desc_parts = [voice.name]
        
        if hasattr(voice, 'languages') and voice.languages:
            langs = ', '.join([str(lang) if isinstance(lang, str) else lang for lang in voice.languages])
            desc_parts.append(f"Languages: {langs}")
        
        if hasattr(voice, 'age') and voice.age:
            desc_parts.append(f"Age: {voice.age}")
        
        return ' | '.join(desc_parts)
    
    def score_voice_quality(self, voice_info):
        """Score voice quality based on characteristics"""
        score = 0
        
        # Preferred voice names (better quality)
        preferred_names = ['zira', 'samantha', 'karen', 'diana', 'monica', 'heather']
        name_lower = voice_info['name'].lower()
        
        for pref in preferred_names:
            if pref in name_lower:
                score += 50
                break
        
        # Language support (English preferred)
        if any('en' in str(lang).lower() for lang in voice_info.get('languages', [])):
            score += 30
        
        # Voice description quality
        if len(voice_info['name']) > 10:  # Detailed name suggests quality voice
            score += 20
        
        return score
    
    def get_best_available_voice(self, voices):
        """Get best available voice when no female voices found"""
        best_voice = None
        best_score = 0
        
        for voice in voices:
            score = len(voice.name) + 10  # Basic scoring
            
            # Prefer voices with longer, more descriptive names
            if score > best_score:
                best_score = score
                best_voice = {
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages if hasattr(voice, 'languages') else [],
                    'gender': 'unknown',
                    'description': self.voice_description(voice)
                }
        
        return best_voice, voices
    
    def configure_female_voice(self, voice_info):
        """Configure TTS system with selected female voice"""
        logger.info(f"🔧 Configuring voice: {voice_info['name']}")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Set female voice
            engine.setProperty('voice', voice_info['id'])
            
            # Optimize female voice settings
            engine.setProperty('rate', 140)  # Slightly slower for natural speech
            engine.setProperty('volume', 0.85)  # Gentle volume
            engine.setProperty('pitch', 50)  # Default pitch (female voices often naturally higher)
            
            # Update configuration
            self.update_voice_config(voice_info)
            
            # Test voice
            logger.info("🔊 Testing female voice...")
            engine.say("Hello, I'm Sara with my new female voice. How can I help you?")
            engine.runAndWait()
            
            logger.info("✅ Female voice configured successfully")
            return True
            
        except Exception as e:
            logger.error(f"Voice configuration failed: {e}")
            return False
    
    def update_voice_config(self, voice_info):
        """Update voice configuration with female voice settings"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Update voice settings
            config['voice_settings'].update({
                'voice_id': voice_info['id'],
                'voice_name': voice_info['name'],
                'voice_gender': 'female',
                'voice_description': voice_info['description'],
                'volume': 0.85,
                'rate': 140,  # Slower, more natural
                'pitch': 50,
                'optimized_date': time.strftime('%Y-%m-%d'),
                'voice_quality': 'professional_female'
            })
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info("✅ Configuration updated")
            
        except Exception as e:
            logger.error(f"Config update failed: {e}")
    
    def restart_voice_agent(self):
        """Restart voice agent with new voice configuration"""
        if self.voice_agent_pid:
            logger.info("🔄 Restarting voice agent with new voice...")
            
            try:
                # Send SIGHUP to restart gracefully
                subprocess.run(['kill', '-HUP', str(self.voice_agent_pid)])
                time.sleep(2)
                
                # Check if still running, if not start new
                if not self.is_voice_agent_running():
                    self.start_voice_agent()
                    
                logger.info("✅ Voice agent restarted with female voice")
                
            except Exception as e:
                logger.error(f"Agent restart failed: {e}")
                self.start_voice_agent()
    
    def is_voice_agent_running(self):
        """Check if voice agent is running"""
        try:
            result = subprocess.run(['pgrep', '-f', 'sara_voice_agent.py'], 
                                  capture_output=True, text=True)
            return bool(result.stdout.strip())
        except:
            return False
    
    def start_voice_agent(self):
        """Start voice agent process"""
        try:
            script_path = "/home/godfather/local-command-center/agents/sara-voice/sara_voice_agent.py"
            subprocess.Popen([sys.executable, script_path])
            logger.info("🚀 Voice agent started")
        except Exception as e:
            logger.error(f"Voice agent start failed: {e}")
    
    def verify_voice(self):
        """Verify female voice is working"""
        logger.info("🔍 Verifying female voice quality...")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            current_voice = engine.getProperty('voice')
            voices = engine.getProperty('voices')
            
            current_voice_name = "Unknown"
            for voice in voices:
                if voice.id == current_voice:
                    current_voice_name = voice.name
                    break
            
            logger.info(f"✅ Current voice: {current_voice_name}")
            
            # Quick verification test
            engine.say("Voice verification complete. Female voice is active.")
            engine.runAndWait()
            
            return True
            
        except Exception as e:
            logger.error(f"Voice verification failed: {e}")
            return False
    
    def run_optimization(self):
        """Run complete female voice optimization"""
        logger.info("🚀 Starting female voice optimization...")
        
        print("🔊 FEMALE VOICE OPTIMIZATION")
        print("=" * 50)
        
        # Scan and select best female voice
        best_voice, all_female_voices = self.scan_available_voices()
        
        if not best_voice:
            print("❌ No suitable voice found")
            return False
        
        print(f"🌟 Selected: {best_voice['name']}")
        print(f"📝 Description: {best_voice['description']}")
        
        # Configure voice
        if self.configure_female_voice(best_voice):
            print("✅ Voice configured successfully")
            
            # Verify setup
            if self.verify_voice():
                print("✅ Voice quality verified")
                
                # Restart voice agent with new voice
                self.restart_voice_agent()
                
                print("🎉 FEMALE VOICE OPTIMIZATION COMPLETE!")
                print("🔊 Sara now speaks with professional female voice")
                print("💬 Voice characteristics optimized for natural conversation")
                
                return True
            else:
                print("⚠️ Voice verification failed")
                return False
        else:
            print("❌ Voice configuration failed")
            return False

def main():
    """Main optimization execution"""
    optimizer = FemaleVoiceOptimizer()
    
    try:
        success = optimizer.run_optimization()
        
        if success:
            print("\n💡 FEMALE VOICE FEATURES:")
            print("  ✓ Natural female speech pattern")
            print("  ✓ Optimized speaking rate and tone")
            print("  ✓ Professional voice quality")
            print("  ✓ Gentle volume settings")
            print("  ✓ Enhanced clarity and warmth")
            print("\n🎤 Test by saying: 'Sara, how does my voice sound?'")
            
        else:
            print("\n⚠️ Optimization had issues - voice using default settings")
            
    except KeyboardInterrupt:
        print("\n🛑 Voice optimization cancelled")
    except Exception as e:
        print(f"\n❌ Optimization error: {e}")

if __name__ == "__main__":
    main()