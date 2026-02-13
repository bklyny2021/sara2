#!/usr/bin/env python3
"""
🔥 KILL CURRENT VOICE AGENT AND RESTART WITH LOCAL AI
"""

import subprocess
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Kill current agent and restart with local AI"""
    logger.info("🔥 Stopping current voice agent...")
    
    # Kill any running voice agents
    subprocess.run(['pkill', '-f', 'sara_voice_agent'], check=False)
    time.sleep(2)  # Wait for cleanup
    
    logger.info("✅ Starting LOCAL-ONLY voice agent (ZERO API KEYS)")
    
    # Launch local-only version
    subprocess.run(['python3', '/home/godfather/.openclaw/workspace/start_local_voice.py'])

if __name__ == "__main__":
    main()