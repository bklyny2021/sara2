#!/usr/bin/env python3
# 🎤 MINIMAL VOICE TEST - Check if system can work

import speech_recognition as sr
import pyttsx3

def test_voice_system():
    print("🎤 MINIMAL VOICE SYSTEM TEST")
    print("=" * 30)
    
    # Test TTS first
    try:
        engine = pyttsx3.init()
        engine.say("Voice test starting")
        engine.runAndWait()
        print("✅ TTS system working")
    except Exception as e:
        print(f"❌ TTS failed: {e}")
        return False
    
    # Test microphone
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            print("🎧 Testing microphone...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("📢 Say something...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
        
        text = recognizer.recognize_google(audio)
        print(f"✅ Speech recognized: '{text}")
        
        # Test full loop
        response = f"I heard you say: {text}"
        engine.say(response)
        engine.runAndWait()
        print("✅ Full voice loop working!")
        return True
        
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

if __name__ == "__main__":
    test_voice_system()