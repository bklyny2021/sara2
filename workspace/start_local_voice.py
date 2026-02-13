#!/usr/bin/env python3
"""
🚀 Start LOCAL-ONLY Sara Voice Agent
ZERO API KEYS - PURE OLLAMA INTEGRATION
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

# Setup logs
os.makedirs('/home/godfather/local-command-center/logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/local-command-center/logs/sara_voice.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name())

def main():
    """Launch local-only voice agent"""
    logger.info("🚀 Starting LOCAL-ONLY Sara Voice Agent - ZERO API KEYS")
    
    # Change to local command center
    os.chdir('/home/godfather/.openclaw/workspace')
    
    # Launch local-only voice agent
    local_agent_path = '/home/godfather/.openclaw/workspace/sara_voice_local_only.py'
    
    if not os.path.exists(local_agent_path):
        logger.error(f"❌ Local-only agent not found: {local_agent_path}")
        sys.exit(1)
    
    logger.info("✅ Launching LOCAL-ONLY voice agent")
    subprocess.run(['python3', local_agent_path])

if __name__ == "__main__":
    main()