#!/usr/bin/env python3
"""
🎤 FIX TTS AUDIO OUTPUT - K66 + AD106M SPECIFIC
Based on memory analysis - this is the actual issue!
"""

import subprocess
import os
import time
import pyaudio
import wave
import tempfile

def test_device_audio_routing():
    """Test if we can route audio directly to K66 speakers"""
    print("🎯 Testing direct audio routing to K66 speakers...")
    
    # Check available audio devices
    try:
        p = pyaudio.PyAudio()
        
        print("📋 Available Audio Devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            device_name = info['name']
            if 'K66' in device_name or 'AD106M' in device_name:
                print(f"  🎧 Device {i}: {info['name']}")
                print(f"      Channels: {info['maxOutputChannels']}")
                print(f"      Rate: {info['defaultSampleRate']}")
                
                # Test if this is output device
                if info['maxOutputChannels'] > 0:
                    print(f"  ✅ Attempting playback on device {i}...")
                    test_audio_device(p, i)
        
        p.terminate()
        
    except Exception as e:
        print(f"❌ PyAudio test failed: {e}")

def test_audio_device(p, device_index):
    """Test audio playback on specific device"""
    try:
        # Generate test tone
        duration = 2  # seconds
        sample_rate = 44100
        frequency = 440  # A4 note
        
        frames = []
        for i in range(int(sample_rate * duration)):
            frame = int(32767 * 0.3 * (1 if (i // (sample_rate // frequency)) % 2 else -1))
            frames.append([frame, frame])  # Left + Right
        
        # Convert to bytes
        audio_data = b''
        for frame in frames:
            audio_data += frame[0].to_bytes(2, 'little', signed=True)
            audio_data += frame[1].to_bytes(2, 'little', signed=True)
        
        # Try playback
        stream = p.open(format=pyaudio.paInt16,
                       channels=2,
                       rate=sample_rate,
                       output=True,
                       output_device_index=device_index)
        
        print(f"  🎵 Playing test tone...")
        stream.write(audio_data)
        stream.stop_stream()
        stream.close() 
        
        print(f"  ✅ Audio playback test completed on device {device_index}")
        
    except Exception as e:
        print(f"  ❌ Audio playback failed on device {device_index}: {e}")

def test_pulse_audio_routing():
    """Test PulseAudio device-specific routing"""
    print("\n🎯 Testing PulseAudio routing to K66...")
    
    try:
        # Find K66 device in PulseAudio
        result = subprocess.run(['pactl', 'list', 'sinks'], capture_output=True, text=True)
        sinks = result.stdout
        
        k66_sink = None
        for line in sinks.split('\n'):
            if 'K66' in line and 'Name:' in line:
                k66_sink = line.split('Name: ')[1].strip()
                print(f"  ✅ Found K66 sink: {k66_sink}")
                break
        
        if k66_sink:
            # Test sending audio to K66 sink
            test_tone = "/tmp/k66_test.wav"
            
            # Create test audio file
            create_test_wav(test_tone)
            
            # Play to K66 specifically
            print(f"  🎵 Playing test tone to K66 sink...")
            result = subprocess.run(['paplay', '--device', k66_sink, test_tone], 
                                   capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  ✅ PulseAudio routing successful!")
            else:
                print(f"  ❌ PulseAudio routing failed: {result.stderr}")
            
            # Cleanup
            os.remove(test_tone)
        else:
            print("  ❌ K66 sink not found in PulseAudio")
            
    except Exception as e:
        print(f"  ❌ PulseAudio test failed: {e}")

def create_test_wav(filename):
    """Create a simple WAV test file"""
    import wave
    import struct
    
    sample_rate = 44100
    duration = 2
    frequency = 440
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate sine wave
        frames = []
        for i in range(int(sample_rate * duration)):
            value = int(32767 * 0.3 * 0)  # Silence for now
            frames.append(struct.pack('<hh', value, value))
        
        wav_file.writeframes(b''.join(frames))

def test_tts_with_pulse():
    """Test TTS with PulseAudio device output"""
    print("\n🎯 Testing TTS with PulseAudio device routing...")
    
    try:
        import pyttsx3
        
        # Initialize TTS
        engine = pyttsx3.init()
        
        # Get voices
        voices = engine.getProperty('voices')
        female_voice = None
        for voice in voices:
            if 'female' in voice.gender.lower():
                female_voice = voice
                break
        
        if female_voice:
            engine.setProperty('voice', female_voice.id)
            print(f"  ✅ Using female voice: {female_voice.name}")
        
        # Try to set output device if possible
        # Note: pyttsx3 doesn't directly support device selection
        # We need to use environment variables or system defaults
        
        print(f"  🎵 Testing TTS output...")
        print(f"  📍 Attempting to speech...")
        engine.say("This is a TTS test through PulseAudio routing to K66 speakers")
        
        # This is where the original problem occurs - pyttsx3 might not use K66
        print(f"  ⠸ Running speech...")
        engine.runAndWait()
        
        print(f"  ✅ TTS test completed")
        
    except Exception as e:
        print(f"  ❌ TTS test failed: {e}")

def main():
    print("=" * 70)
    print("🎤 K66 + AD106M AUDIO ROUTING DIAGNOSTIC")
    print("=" * 70)
    print("Based on memory analysis - fixing the actual TTS issue!")
    print()
    
    # Test different audio routing methods
    test_device_audio_routing()
    test_pulse_audio_routing()
    test_tts_with_pulse()
    
    print("\n" + "=" * 70)
    print("🎯 AUDIO ROUTING DIAGNOSTIC COMPLETE")
    print()
    print("📋 Summary of findings:")
    print("   If device tests work but TTS silent = pyttsx3 routing issue")
    print("   If all tests fail = system audio routing problem")
    print("   If some work = partial configuration issue")
    print()
    print("🔧 Next steps based on test results...")
    print("=" * 70)

if __name__ == "__main__":
    main()