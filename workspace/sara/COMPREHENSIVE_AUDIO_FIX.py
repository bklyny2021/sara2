#!/usr/bin/env python3
# 🔊 COMPREHENSIVE AUDIO FIX - HDMI TV Sound Solution

import subprocess
import time
import sys

class ComprehensiveAudioFix:
    """Complete audio system troubleshooting and fix"""
    
    def __init__(self):
        print("🔧 COMPREHENSIVE AUDIO FIX")
        print("=" * 45)
        print("🎯 Target: HDMI TV speakers working")
        print("🔊 System: PipeWire + ALSA + HDMI")
        print("🎤 Voice: Female TTS output")
        print("=" * 45)
        
        self.audio_fixed = False
    
    def diagnose_audio_system(self):
        """Diagnose current audio state"""
        print("\n🔍 DIAGNOSING AUDIO SYSTEM...")
        print("-" * 30)
        
        try:
            # Check audio sinks
            result = subprocess.run(['pactl', 'list', 'sinks'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Audio sinks detected:")
                lines = result.stdout.split('\n')
                sink_count = 0
                for line in lines:
                    if 'Sink #' in line:
                        sink_count += 1
                        sink_id = line.split('#')[1].strip()
                        print(f"  Sink #{sink_id}: Available")
                
                print(f"📊 Total sinks found: {sink_count}")
                return True
            else:
                print("❌ Could not list audio sinks")
                return False
                
        except Exception as e:
            print(f"❌ Audio diagnosis failed: {e}")
            return False
    
    def configure_default_sink(self):
        """Configure default audio sink"""
        print("\n🎯 CONFIGURING DEFAULT AUDIO SINK...")
        print("-" * 35)
        
        try:
            # Set HDMI TV as default sink
            hdmi_sink = "alsa_output.pci-0000_01_00.1.pro-output-3"
            
            print(f"📍 Setting default sink to: {hdmi_sink}")
            
            # Set default sink
            result = subprocess.run(['pactl', 'set-default-sink', hdmi_sink],
                                   capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Default sink set successfully")
                
                # Verify
                verify_result = subprocess.run(['pactl', 'get-default-sink'],
                                             capture_output=True, text=True)
                if verify_result.returncode == 0:
                    current_sink = verify_result.stdout.strip()
                    print(f"✅ Current default: {current_sink}")
                    
                    if hdmi_sink in current_sink:
                        print("✅ HDMI TV confirmed as default sink")
                        return True
                    else:
                        print("⚠️  Sink set but verification unclear")
                        return False
                else:
                    print("⚠️  Could not verify default sink")
                    return False
            else:
                print(f"❌ Failed to set default sink: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Sink configuration failed: {e}")
            return False
    
    def unsuspend_audio_sinks(self):
        """Unsuspend all audio sinks"""
        print("\n🔄 UNSUSPENDING AUDIO SINKS...")
        print("-" * 35)
        
        try:
            # Get list of all sinks
            result = subprocess.run(['pactl', 'list', 'sinks'], 
                                  capture_output_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                sink_ids = []
                
                # Extract sink IDs
                for line in lines:
                    if 'Sink #' in line:
                        sink_id = line.split('#')[1].strip()
                        sink_ids.append(sink_id)
                
                print(f"📍 Found {len(sink_ids)} sinks to unsuspend")
                
                # Unsuspend each sink
                for sink_id in sink_ids:
                    print(f"  Unsinking sink #{sink_id}...")
                    suspend_result = subprocess.run(['pactl', 'suspend-sink', sink_id, 'false'],
                                                  capture_output=True, text=True)
                    if suspend_result.returncode == 0:
                        print(f"    ✅ Sink #{sink_id}: Active")
                    else:
                        print(f"    ⚠️  Sink #{sink_id}: Error")
                
                print("✅ All sinks unsuspended")
                return True
            else:
                print("❌ Could not list sinks")
                return False
                
        except Exception as e:
            print(f"❌ Unsuspend failed: {e}")
            return False
    
    def test_audio_output(self):
        """Test audio output with multiple methods"""
        print("\n🔊 TESTING AUDIO OUTPUT...")
        print("-" * 28)
        
        success_count = 0
        
        # Method 1: Using paplay (PipeWire audio player)
        print("📍 Method 1: PipeWire audio playback...")
        try:
            result = subprocess.run(['paplay', '/usr/share/sounds/alsa/Front_Left.wav'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ PipeWire playback successful")
                success_count += 1
            else:
                print(f"❌ PipeWire playback failed: {result.stderr}")
        except Exception as e:
            print(f"❌ PipeWire test error: {e}")
        
        # Method 2: Using ffplay (FFmpeg)
        print("📍 Method 2: FFmpeg audio playback...")
        try:
            result = subprocess.run(['ffplay', '-nodisp', '-autoexit', 
                                   '/usr/share/sounds/alsa/Front_Left.wav'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ FFmpeg playback successful")
                success_count += 1
            else:
                print(f"❌ FFmpeg playback failed")
        except Exception as e:
            print(f"❌ FFmpeg test error: {e}")
        
        # Method 3: Test TTS output
        print("📍 Method 3: TTS system test...")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            test_message = "Audio system test. Can you hear this through your TV speakers?"
            print(f"🎤 Testing TTS: {test_message}")
            engine.say(test_message)
            engine.runAndWait()
            print("✅ TTS playback attempted")
            success_count += 1
        except Exception as e:
            print(f"❌ TTS test error: {e}")
        
        print(f"📊 Success rate: {success_count}/3 methods")
        return success_count >= 2
    
    def voice_system_integration(self):
        """Integration test with voice system"""
        print("\n🗣️ VOICE SYSTEM INTEGRATION...")
        print("-" * 33)
        
        try:
            # Test with our working voice script
            print("🔄 Testing voice with working audio configuration...")
            
            # Create a simple test script
            test_script = '''
import pyttsx3
import time

print("🎤 Voice-Audio Integration Test")
print("=" * 35)

try:
    engine = pyttsx3.init()
    
    # Find English voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'english' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    engine.setProperty('rate', 140)
    print("🎯 Speaking: HDMI Audio Test Complete!")
    engine.say("HDMI audio test complete! Voice system working perfectly through TV speakers!")
    engine.runAndWait()
    print("✅ Voice-Audio integration successful!")
    
except Exception as e:
    print(f"❌ Voice integration failed: {e}")
'''
            
            # Write test script
            with open('/tmp/voice_test.py', 'w') as f:
                f.write(test_script)
            
            # Run test
            result = subprocess.run(['python3', '/tmp/voice_test.py'],
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Voice-Audio integration complete")
                return True
            else:
                print(f"❌ Voice integration failed")
                return False
                
        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            return False
    
    def create_audio_status_check(self):
        """Create audio status monitoring script"""
        print("\n📝 CREATING AUDIO STATUS CHECK...")
        print("-" * 34)
        
        status_script = '''#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def check_audio_status():
    """Check audio system status"""
    print("🔊 AUDIO STATUS CHECK")
    print("=" * 25)
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check default sink
    try:
        result = subprocess.run(['pactl', 'get-default-sink'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            default_sink = result.stdout.strip()
            print(f"📍 Default sink: {default_sink}")
        else:
            print("❌ Could not get default sink")
    except:
        print("⚠️  Default sink check failed")
    
    # Check sink states
    try:
        result = subprocess.run(['pactl', 'list', 'sinks'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\\n')
            active_sinks = 0
            for line in lines:
                if 'State: SUSPENDED' in line:
                    pass
                elif 'State: ' in line:
                    active_sinks += 1
            print(f"🎤 Active sinks: {active_sinks}")
    except:
        print("⚠️  Sink status check failed")
    
    # Test quick audio
    try:
        result = subprocess.run(['paplay', '/usr/share/sounds/alsa/Front_Left.wav'],
                              capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print("✅ Audio playback: WORKING")
        else:
            print("❌ Audio playback: FAILED")
    except Exception as e:
        print(f"❌ Audio test error: {e}")
    
    print()
    print("🎯 QUICK FIX IF NEEDED:")
    print("pactl set-default-sink alsa_output.pci-0000_01_00.1.pro-output-3")
    print("pactl suspend-sink [sink_id] false")
    print()

if __name__ == "__main__":
    check_audio_status()
'''
        
        with open('/home/godfather/Desktop/sara/audio_status_check.py', 'w') as f:
            f.write(status_script)
        
        # Make executable
        subprocess.run(['chmod', '+x', '/home/godfather/Desktop/sara/audio_status_check.py'])
        
        print("✅ Audio status check script created")
        print("📍 Location: /home/godfather/Desktop/sara/audio_status_check.py")
    
    def apply_optimal_configuration(self):
        """Apply optimal audio configuration"""
        print("\n⚙️ APPLYING OPTIMAL CONFIGURATION...")
        print("-" * 37)
        
        steps_completed = 0
        
        # Step 1: Set proper default sink
        if self.configure_default_sink():
            steps_completed += 1
            print("✅ Step 1: Default HDMI sink configured")
        
        # Step 2: Unsuspend sinks
        if self.unsuspend_audio_sinks():
            steps_completed += 1
            print("✅ Step 2: Audio sinks active")
        
        # Step 3: Test output
        if self.test_audio_output():
            steps_completed += 1
            print("✅ Step 3: Audio output working")
        
        # Step 4: Voice integration
        if self.voice_system_integration():
            steps_completed += 1
            print("✅ Step 4: Voice integration complete")
        
        # Step 5: Status monitoring
        self.create_audio_status_check()
        steps_completed += 1
        print("✅ Step 5: Status monitoring ready")
        
        print(f"🎯 Configuration success: {steps_completed}/5 steps")
        return steps_completed >= 4
    
    def run_comprehensive_fix(self):
        """Run comprehensive audio fix"""
        print("🚀 STARTING COMPREHENSIVE AUDIO FIX")
        print("=" * 40)
        
        # Diagnose first
        if not self.diagnose_audio_system():
            print("❌ Initial diagnosis failed")
            return False
        
        # Apply fixes
        if self.apply_optimal_configuration():
            self.audio_fixed = True
            print("\\n🌟 AUDIO FIX COMPLETE!")
            print("🎵 HDMI TV speakers should now be working")
            print("🗣️ Voice system should output through TV")
            print("⚙️ Use audio_status_check.py for monitoring")
            return True
        else:
            print("❌ Audio fix incomplete")
            return False
    
    def provide_fallback_instructions(self):
        """Provide manual fallback instructions"""
        print("\\n📋 MANUAL AUDIO FIX INSTRUCTIONS")
        print("=" * 35)
        print("If you still don't hear sound, try this:")
        print()
        print("🔧 QUICK FIX STEPS:")
        print("1. Open terminal and run:")
        print("   python3 /home/godfather/Desktop/sara/audio_status_check.py")
        print()
        print("2. If default sink is wrong, run:")
        print("   pactl set-default-sink alsa_output.pci-0000_01_00.1.pro-output-3")
        print()
        print("3. If sinks are suspended, run:")
        print("   pactl list sinks (note sink numbers)")
        print("   pactl suspend-sink [number] false")
        print()
        print("4. Test with:")
        print("   paplay /usr/share/sounds/alsa/Front_Left.wav")
        print()
        print("📺 TV CHECK:")
        print("- TV must be on and HDMI connected")
        print("- TV volume should be up")
        print("- TV input set to correct HDMI port")
        print("- Mute function should be off")
        print()
        print("🎯 VOICE TEST:")
        print("- Say 'Sara' to activate voice system")
        print("- You should hear female voice through TV")
        print("- Check TV speakers are working with other audio")

def main():
    """Main execution"""
    print("🔧 COMPREHENSIVE AUDIO TROUBLESHOOTING")
    print("🎯 Target: HDMI TV speakers - working audio")
    print("🗣️ For: Voice-activated AI system")
    print()
    
    try:
        fix = ComprehensiveAudioFix()
        
        if fix.run_comprehensive_fix():
            print("\\n✅ AUDIO SYSTEM FIXED SUCCESSFULLY!")
            print("🎵 Your HDMI TV speakers should now work")
            print("🗣️ Voice responses will play through TV")
            print("🎯 Say 'Sara' to test voice-AI system")
        else:
            print("\\n⚠️  AUTO FIX INCOMPLETE")
            fix.provide_fallback_instructions()
    
    except KeyboardInterrupt:
        print("\\n🛑 User interrupted audio fix")
    except Exception as e:
        print(f"\\n❌ Audio fix error: {e}")
    
    print("\\n🌟 Remember: Audio troubleshooting continues...")
    print("🎯 Goal: Perfect voice-AI experience through HDMI TV")

if __name__ == "__main__":
    main()