#!/bin/bash
# Sara2 Auto-Restart Watchdog
# Monitors Sara2 voice agent and restarts if not running
# Add to crontab for auto-restart: */1 * * * * /home/sarabot/sara2/auto-restart.sh

LOG_FILE="/home/sarabot/.openclaw/workspace/logs/sara2_watchdog.log"
SARA_SCRIPT="/home/sarabot/sara2/workspace/sara/agents/sara-voice/sara_voice_agent.py"

# Check if Sara2 is running
if ! pgrep -f "sara_voice_agent.py" > /dev/null; then
    echo "[$(date)] Sara2 not running, restarting..." >> "$LOG_FILE"
    nohup python3 "$SARA_SCRIPT" > /home/sarabot/.openclaw/workspace/logs/sara2_output.log 2>&1 &
    echo "[$(date)] Started with PID $!" >> "$LOG_FILE"
else
    # Check if responsive (Web UI)
    if ! curl -s http://localhost:8081/ > /dev/null 2>&1; then
        echo "[$(date)] Sara2 Web UI not responding, restarting..." >> "$LOG_FILE"
        pkill -9 -f "sara_voice_agent.py" 2>/dev/null
        sleep 2
        nohup python3 "$SARA_SCRIPT" > /home/sarabot/.openclaw/workspace/logs/sara2_output.log 2>&1 &
        echo "[$(date)] Restarted with PID $!" >> "$LOG_FILE"
    fi
fi
