#!/usr/bin/env python3
# TTS Initialization and Voice Setup

import pyttsx3
import json

def setup_female_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Find female voice
    female_voice = None
    for voice in voices:
        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
            female_voice = voice
            break
    
    if female_voice:
        engine.setProperty('voice', female_voice.id)
        print(f"Using female voice: {female_voice.name}")
    else:
        # Use first available voice as fallback
        engine.setProperty('voice', voices[0].id)
        print(f"Using default voice: {voices[0].name}")
    
    # Configure voice properties
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    
    return engine

if __name__ == "__main__":
    engine = setup_female_voice()
    engine.say("Voice system initialized. Hello, I am Sara.")
    engine.runAndWait()
