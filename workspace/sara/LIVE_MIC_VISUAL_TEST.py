#!/usr/bin/env python3
# 🔴 LIVE MIC VISUAL TEST - WATCH THE MIC ICON!

import speech_recognition as sr
import time
import os

def live_mic_test():
    print("🔴 LIVE MICROPHONE VISUAL TEST")
    print("=============================")
    print("👀 WATCH YOUR DESKTOP TASKBAR NOW!")
    print("🎤 Looking for microphone activity icon...")
    print()
    
    recognizer = sr.Recognizer()
    
    # Try to find K66
    try:
        mics = sr.Microphone.list_microphone_names()
        k66_index = None
        
        for i, mic in enumerate(mics):
            print(f"  🔍 {i}: {mic}")
            if "K66" in mic:
                k66_index = i
                print(f"✅ K66 found at index {i}")
                break
        
        if k66_index is None:
            print("❌ K66 NOT FOUND - trying default mic")
            microphone = sr.Microphone()
        else:
            microphone = sr.Microphone(device_index=k66_index)
        
        print()
        print("🔴 STARTING LIVE TEST - WATCH MIC ICON!")
        print("🎤 I will activate microphone for 3 seconds...")
        print("📱 Do you see activity icon on desktop?")
        
        with microphone as source:
            print("\n🔥 MIC ACTIVATING NOW - WATCH!")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Keep mic active for visual test
            print("⏰ MIC ACTIVE FOR 3 SECONDS...")
            time.sleep(1)
            print("⏰ 2 seconds...")
            time.sleep(1)
            print("⏰ 3 seconds...")
            time.sleep(1)
            
            print("\n🔥 CAPTURING AUDIO NOW...")
            # Try to capture
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                print("✅ Audio captured!")
                
                print("\n🔥 SPEAKING NOW - WATCH MIC ICON!")
                # Visual test - just speak and see if icon shows
                print("📢 SPEAKING TEST PHRASE...")
                
                # Try recognition
                text = recognizer.recognize_google(audio)
                print(f"🗣️ I heard: {text}")
                
            except:
                print("⚠️  Recognition failed but mic should have shown activity")
        
        print("\n🎯 VISUAL TEST COMPLETE")
        print("❓ DID YOU SEE MICROPHONE ACTIVITY ICON?")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    live_mic_test()