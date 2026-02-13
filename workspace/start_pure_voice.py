#!/usr/bin/env python3
"""
🚀 Start PURE Sara Voice Agent
NO SCRIPTED RESPONSES - ONLY AI MODEL OUTPUT
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
logger = logging.getLogger(__name__)

def main():
    """Launch PURE voice agent"""
    logger.info("🚀 Starting PURE Sara Voice Agent - NO SCRIPTED RESPONSES")
    
    # Change to local command center
    os.chdir('/home/godfather/.openclaw/workspace')
    
    # Launch pure voice agent
    pure_agent_path = '/home/godfather/.openclaw/workspace/sara_voice_agent_pure.py'
    
    if not os.path.exists(pure_agent_path):
        logger.error(f"❌ Pure agent not found: {pure_agent_path}")
        sys.exit(1)
    
    logger.info("✅ Launching PURE voice agent")
    subprocess.run(['python3', pure_agent_path])

if __name__ == "__main__":
    main()