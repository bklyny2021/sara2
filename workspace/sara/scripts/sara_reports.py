#!/usr/bin/env python3
# Sara Access - Voice Agent Reports

import json
import os
from datetime import datetime

class VoiceAgentReports:
    def get_status_report(self):
        # Check if voice agent is running
        reports = {
            "voice_agent_running": self.is_agent_running(),
            "last_interaction": self.get_last_interaction(),
            "system_status": "operational",
            "sara_access_enabled": True
        }
        
        with open("/home/godfather/local-command-center/sara_voice_report.json", 'w') as f:
            json.dump(reports, f, indent=2)
        
        return reports
    
    def is_agent_running(self):
        # Simple process check
        try:
            import psutil
            for proc in psutil.process_iter(['cmdline']):
                if proc.info['cmdline'] and 'sara_voice_agent.py' in ' '.join(proc.info['cmdline']):
                    return True
        except:
            pass
        return False
    
    def get_last_interaction(self):
        # Get last log entry timestamp
        log_file = "/home/godfather/local-command-center/logs/sara_voice.log"
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    return lines[-1].strip()
        return "No interactions logged yet"

if __name__ == "__main__":
    reports = VoiceAgentReports()
    reports.get_status_report()
    print("Sara voice agent report generated")
