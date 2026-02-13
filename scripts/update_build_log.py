#!/usr/bin/env python3
"""
Build Log Updater - Updates BUILD_LOG.json with current timestamp and component status
"""
import json
import os
from datetime import datetime

def update_build_log():
    workspace = "/home/sarabot/.openclaw/workspace"
    log_path = os.path.join(workspace, "BUILD_LOG.json")
    
    # Load existing log
    with open(log_path, 'r') as f:
        log = json.load(f)
    
    # Update timestamp
    now = datetime.now().isoformat()
    log['last_updated'] = now
    
    # Update component timestamps
    for component in log.get('components', []):
        component['last_built'] = now
    
    # Save back
    with open(log_path, 'w') as f:
        json.dump(log, f, indent=2)
    
    print(f"BUILD_LOG.json updated: {now}")
    return True

if __name__ == "__main__":
    update_build_log()
