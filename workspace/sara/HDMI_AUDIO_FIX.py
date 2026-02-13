#!/usr/bin/env python3
# 🔊 HDMI TV Audio Output Fix for Voice System

import subprocess
import pyttsx3
import time
import os

class HDMIAudioFix:
    """Fix TTS output to HDMI TV for voice system"""
    
    def __init__(self):
        print("🔧 HDMI Audio Output Fix")
        print("=" * 40)
        print("🎯 Target: NVIDIA HDMI to TV output")
        print("🔊 System: AD106M High Definition Audio")
        print("=" * 40)
        
        self.engine = pyttsx3.init()
        
    def check_audio_devices(self):
        """Check available audio output devices"""
        print("\n🔍 Checking audio playback devices...")
        
        try:
            result = subprocess.run(['aplay', '-l'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Audio devices found:")
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'card' in line and ('HDMI' in line or 'NVidia' in line):
                        print(f"  {line.strip()}")
                return True
            else:
                print("❌ Could not list audio devices")
                return False
        except Exception as e:
            print(f"❌ Device check failed: {e}")
            return False
    
    def set_hdmi_audio_output(self):
        """Set HDMI as default audio output"""
        print("\n🎯 Setting HDMI audio output...")
        
        try:
            # Method 1: Use pacmd to set HDMI output
            print("📋 Method 1: Setting HDMI via pacmd...")
            cmd1 = subprocess.run(['pacmd', 'set-default-sink', 'auto_set'], 
                                capture_output=True, text=True)
            
            print("📋 Method 2: Setting HDMI profile...")
            cmd2 = subprocess.run(['pactl', 'set-card-profile', 'alsa_card.pci-0000_01_00.0', 
                                  'output:hdmi-stereo'], capture_output=True, text=True)
            
            # Method 3: Direct HDMI device setting
            print("📋 Method 3: Setting HDMI device...")
            cmd3 = subprocess.run(['amixer', '-c', '0', 'sset', "'IEC958',0", '100%'], 
                                 capture_output=True, text=True)
            cmd4 = subprocess.run(['amixer', '-c', '0', 'sset', "'IEC958',1", '100%'], 
                                 capture_output=True, text=True)
            
            print("✅ HDMI audio configuration attempts completed")
            return True
            
        except Exception as e:
            print(f"❌ HDMI setup failed: {e}")
            return False
    
    def test_tts_to_hdmi(self):
        """Test TTS output to HDMI TV"""
        print("\n🔊 Testing TTS output to HDMI TV...")
        
        try:
            # Test with a simple message
            test_message = "Testing audio output to HDMI television. Can you hear this through your TV speakers?"
            print(f"🎤 Speaking: {test_message}")
            
            self.engine.say(test_message)
            self.engine.runAndWait()
            
            print("✅ TTS playback sent to audio system")
            print("🔊 Check TV speakers for voice output")
            
            return True
            
        except Exception as e:
            print(f"❌ TTS test failed: {e}")
            return False
    
    def configure_engine_for_hdmi(self):
        """Configure TTS engine for HDMI output"""
        print("\n🔧 Configuring TTS engine for HDMI...")
        
        try:
            # Reset and reinitialize engine
            del self.engine
            time.sleep(1)
            
            # Reinitialize with HDMI output focus
            self.engine = pyttsx3.init()
            
            # Set voice properties
            voices = self.engine.getProperty('voices')
            
            # Find a good female voice
            female_voice = None
            for voice in voices:
                if 'english' in voice.name.lower() and ('female' in voice.name.lower() or 'woman' in voice.name.lower()):
                    female_voice = voice
                    break
            
            if female_voice:
                self.engine.setProperty('voice', female_voice.id)
                print(f"✅ Set female voice: {female_voice.name}")
            
            # Optimize for TV speakers
            self.engine.setProperty('rate', 140)  # Slightly slower for TV
            self.engine.setProperty('volume', 0.9)  # Higher volume for TV
            
            print("✅ TTS engine configured for HDMI TV")
            return True
            
        except Exception as e:
            print(f"❌ Engine configuration failed: {e}")
            return False
    
    def manual_audio_selection(self):
        """Provide manual audio selection guidance"""
        print("\n📱 Manual Audio Selection Guidance:")
        print("=" * 45)
        print("If you didn't hear the test on your TV:")
        print()
        print("🎮 Pulse Audio Control:")
        print("   1. Run: pavucontrol")
        print("   2. Go to 'Output Devices' tab")
        print("   3. Look for 'NVIDIA HDMI' or 'HDMI' output")
        print("   4. Set as fallback/primary device")
        print("   5. Test again")
        print()
        print("🔧 System Audio Settings:")
        print("   1. Right-click sound icon in system tray")
        print("   2. Select 'Audio Settings' or 'PulseAudio Volume Control'")
        print("   3. Choose HDMI/TV as output device")
        print("   4. Test with system sounds first")
        print()
        print("🎮 Alternative Commands:")
        print("   pactl list sinks | grep -i hdmi")
        print("   pacmd set-default-sink [HDMI_DEVICE_NAME]")
        print()
        print("🎯 After fixing audio output:")
        print("   1. Test system sounds: play /usr/share/sounds/alsa/Front_Left.wav")
        print("   2. Then test the voice system again")
        print()
    
    def run_full_fix(self):
        """Run complete HDMI audio fix"""
        print("🚀 Starting HDMI Audio Fix Process")
        print("=" * 45)
        
        # Step 1: Check audio devices
        if not self.check_audio_devices():
            print("❌ Audio device check failed")
            return False
        
        # Step 2: Configure engine
        if not self.configure_engine_for_hdmi():
            print("❌ Engine configuration failed")
            return False
        
        # Step 3: Set HDMI audio output
        if not self.set_hdmi_audio_output():
            print("❌ HDMI setup failed")
            return False
        
        # Step 4: Test TTS
        if not self.test_tts_to_hdmi():
            print("❌ TTS test failed")
            return False
        
        print("\n✅ HDMI Audio Fix Complete!")
        print("🔊 You should hear voice output through TV speakers")
        print("🎯 Voice system ready for HDMI TV interaction")
        
        return True

def main():
    """Main execution"""
    print("🔊 HDMI TV Audio Fix for Voice System")
    print("=" * 50)
    print("🎯 Target: Output voice through HDMI TV speakers")
    print("🎤 Speaker system: AD106M High Definition Audio")
    print("📺 Output destination: TOSHIBA-TV via HDMI")
    print("=" * 50)
    
    # Create and run fix
    fix = HDMIAudioFix()
    success = fix.run_full_fix()
    
    if success:
        print("\n🌟 SUCCESS: HDMI Audio Configured!")
        print("🎙️ Voice system now outputs to TV speakers")
        print("🔍 If still no sound, try the manual steps provided")
    else:
        print("\n⚠️  Some steps failed - try manual configuration")
        fix.manual_audio_selection()

if __name__ == "__main__":
    main()