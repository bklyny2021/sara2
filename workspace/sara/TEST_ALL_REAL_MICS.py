#!/usr/bin/env python3
# 🎤 TEST ALL REAL MICROPHONES (not ghost detections)

import speech_recognition as sr
import time

def test_specific_microphone(mic_index, mic_name):
    """Test a specific microphone by index"""
    print(f"\n🎤 Testing: {mic_name} (index {mic_index})")
    print("=" * 50)
    
    recognizer = sr.Recognizer()
    
    try:
        microphone = sr.Microphone(device_index=mic_index)
        
        with microphone as source:
            print(f"🔧 Calibrating {mic_name}...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print(f"🎤 SPEAK NOW - Testing {mic_name}")
            print("📢 Say something clearly for 5 seconds...")
            
            # Listen for audio
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("✅ Audio captured - processing...")
            
            try:
                text = recognizer.recognize_google(audio)
                print(f"🗣️ RECOGNIZED: '{text}'")
                print(f"✅ {mic_name}: WORKING!")
                return True
            except:
                print(f"⚠️  Recognition failed but audio captured")
                print(f"❓ {mic_name}: Partially working")
                return True
                
    except Exception as e:
        print(f"❌ {mic_name}: FAILED - {e}")
        return False

def main():
    print("🎤 TESTING ALL REAL MICROPHONES")
    print("============================")
    
    # Real microphones found
    real_mics = [
        (4, "HD-Audio Generic ALC897 Analog (motherboard)"),
        (5, "HD-Audio Generic ALC897 Alt (motherboard)"), 
        (6, "K66 USB Audio"),
        (11, "K66 Analog Stereo")
    ]
    
    results = {}
    
    for index, name in real_mics:
        print(f"\n{'='*60}")
        print(f"🎯 MICROPHONE {len(results)+1}/{len(real_mics)}")
        success = test_specific_microphone(index, name)
        results[f"mic_{index}"] = success
        time.sleep(2)  # Brief pause between tests
    
    # Summary
    print(f"\n{'='*60}")
    print("🎯 MICROPHONE TEST SUMMARY")
    print("=" * 30)
    
    working = []
    failed = []
    
    for key, success in results.items():
        for index, name in real_mics:
            if f"mic_{index}" == key:
                if success:
                    working.append(name)
                else:
                    failed.append(name)
                break
    
    print(f"✅ WORKING microphones ({len(working)}):")
    for mic in working:
        print(f"   🎤 {mic}")
    
    if failed:
        print(f"❌ FAILED microphones ({len(failed)}):")
        for mic in failed:
            print(f"   🎤 {mic}")
    
    print(f"\n🎯 TOTAL: {len(working)}/{len(real_mics)} microphones working!")

if __name__ == "__main__":
    main()