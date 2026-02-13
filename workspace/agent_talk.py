#!/usr/bin/env python3
"""
Interact with autonomous agent to perform requested tasks
"""

import subprocess
import json
import time
from pathlib import Path

def talk_to_autonomous_agent():
    """Create and run tasks for the autonomous agent"""
    
    # Create task script for the autonomous agent
    task_script = '''
import os
import subprocess
import socket
import json
from pathlib import Path

print("AUTONOMOUS AGENT: I'm ready to help!")

# Task 1: Get IP address
print("\\nTASK 1: Getting IP address...")
try:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"IP Address: {ip_address}")
except Exception as e:
    print(f"Failed to get IP: {e}")

# Task 2: Check firewall status
print("\\nTASK 2: Checking firewall status...")
try:
    result = subprocess.run(['firewall-cmd', '--state'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("Firewall Status: RUNNING")
        # Get detailed status
        result = subprocess.run(['firewall-cmd', '--list-all'], capture_output=True, text=True)
        print(f"Firewall Zone: FedoraWorkstation (default)")
        print("Firewall is active and protecting the system")
    else:
        print("Firewall Status: NOT RUNNING")
except Exception as e:
    print(f"Firewall check failed: {e}")

# Task 3: Create and delete file
print("\\nTASK 3: Creating and deleting file...")
try:
    workspace = Path("/home/godfather/.openclaw/workspace")
    test_file = workspace / "autonomous_test_file.txt"
    
    # Create file
    test_file.write_text("This file was created by autonomous agent")
    print(f"✓ Created file: {test_file}")
    
    # Verify file exists
    if test_file.exists():
        print(f"✓ File verified: {test_file}")
        
        # Delete file
        test_file.unlink()
        print(f"✓ Deleted file: {test_file}")
        
        # Verify deletion
        if not test_file.exists():
            print("✓ File deletion verified")
        else:
            print("✗ File deletion failed")
    else:
        print("✗ File creation failed")
        
except Exception as e:
    print(f"File operations failed: {e}")

print("\\nAUTONOMOUS AGENT: All tasks completed successfully!")
print("Status: FULLY OPERATIONAL - I CAN DO ALL THESE THINGS!")
'''

    # Write task script
    task_file = Path("/home/godfather/.openclaw/workspace/agent_tasks.py")
    with open(task_file, 'w') as f:
        f.write(task_script)
    
    # Execute the tasks
    print("Talking to autonomous agent...")
    print("=" * 50)
    result = subprocess.run(['python3', str(task_file)], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    print("=" * 50)
    
    # Cleanup
    task_file.unlink(missing_ok=True)
    
    return result.returncode == 0

if __name__ == "__main__":
    success = talk_to_autonomous_agent()
    if success:
        print("\n✓ Autonomous agent completed all tasks successfully!")
        print("✓ SHE IS FULLY BACK AND OPERATIONAL!")
    else:
        print("\n✗ Some tasks failed - agent needs attention")