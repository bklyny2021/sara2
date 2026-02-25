#!/bin/bash
# Simple launcher for Sara2 text mode

cd /home/sarabot/sara2
export PYTHONIOENCODING=utf-8

# Run in keyboard-only mode (no voice, no TTS)
python3 voice-agent/sara_voice_agent.py 2>&1 | grep -v "ALSA\|error.pcm\|error.core"