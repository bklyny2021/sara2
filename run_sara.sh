#!/bin/bash
# Sara2 launcher with auto-restart

LOG_FILE="/tmp/sara2.log"
PYTHON_FILE="/home/sarabot/sara2/voice-agent/sara_voice_agent.py"

cd /home/sarabot/sara2

while true; do
    echo "$(date): Starting Sara2..." >> "$LOG_FILE"
    python3 "$PYTHON_FILE" >> "$LOG_FILE" 2>&1
    echo "$(date): Sara2 crashed, restarting in 2 seconds..." >> "$LOG_FILE"
    sleep 2
done
