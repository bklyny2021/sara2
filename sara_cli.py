#!/usr/bin/env python3
# Sara text-only mode for headless systems

import sys
sys.path.insert(0, '/home/sarabot/sara2/voice-agent')

# Mock audio before importing
import speech_recognition as sr
sr.Microphone = lambda: None

from sara_voice_agent import SaraVoiceAgent

# Disable voice/TTS
agent = SaraVoiceAgent()
agent.recognizer = None
agent.microphone = None

print("="*50)
print("SARA TEXT MODE")
print("="*50)
print("Type your message, or 'sara' to activate\n")

while True:
    try:
        cmd = input("You> ").strip()
        if cmd.lower() == 'quit':
            break
        if cmd:
            print(f"\n[Sara] ", end='')
            agent.process_command(cmd)
            print()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")

print("\nGoodbye!")
