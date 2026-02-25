#!/usr/bin/env python3
"""
Sara2 Control Script
Start, stop, restart, and check status of Sara2 voice agent
"""

import subprocess
import sys
import os
import signal
import time
import argparse

SARA_SCRIPT = "/home/sarabot/sara2/workspace/sara/agents/sara-voice/sara_voice_agent.py"
LOG_FILE = "/home/sarabot/.openclaw/workspace/logs/sara2_output.log"
WATCHDOG_LOG = "/home/sarabot/.openclaw/workspace/logs/sara2_watchdog.log"

def get_pid():
    """Get Sara2 process ID"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "sara_voice_agent.py"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            return int(result.stdout.strip().split('\n')[0])
        return None
    except:
        return None

def start():
    """Start Sara2"""
    pid = get_pid()
    if pid:
        print(f"Sara2 is already running (PID: {pid})")
        return
    
    print("Starting Sara2...")
    subprocess.Popen(
        ["nohup", "python3", SARA_SCRIPT],
        stdout=open(LOG_FILE, "w"),
        stderr=subprocess.STDOUT,
        start_new_session=True
    )
    time.sleep(2)
    
    pid = get_pid()
    if pid:
        print(f"✅ Sara2 started (PID: {pid})")
        print(f"   Web UI: http://localhost:8081")
        print(f"   Logs: tail -f {LOG_FILE}")
    else:
        print("❌ Failed to start Sara2")

def stop():
    """Stop Sara2"""
    pid = get_pid()
    if not pid:
        print("Sara2 is not running")
        return
    
    print(f"Stopping Sara2 (PID: {pid})...")
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        
        # Force kill if still running
        if get_pid():
            os.kill(pid, signal.SIGKILL)
            time.sleep(1)
        
        if not get_pid():
            print("✅ Sara2 stopped")
        else:
            print("❌ Failed to stop Sara2")
    except ProcessLookupError:
        print("✅ Sara2 stopped")
    except Exception as e:
        print(f"❌ Error stopping Sara2: {e}")

def restart():
    """Restart Sara2"""
    print("Restarting Sara2...")
    stop()
    time.sleep(2)
    start()

def status():
    """Check Sara2 status"""
    pid = get_pid()
    if pid:
        print(f"✅ Sara2 is running (PID: {pid})")
        print(f"   Web UI: http://localhost:8081")
        
        # Check Web UI
        try:
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:8081/"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip() == "200":
                print("   Web UI: ✅ Responsive")
            else:
                print(f"   Web UI: ⚠️ HTTP {result.stdout.strip()}")
        except Exception:
            print("   Web UI: ❌ Not responding")
    else:
        print("❌ Sara2 is not running")

def logs(lines=20):
    """Show recent logs"""
    try:
        with open(LOG_FILE, "r") as f:
            all_lines = f.readlines()
            for line in all_lines[-lines:]:
                print(line.rstrip())
    except FileNotFoundError:
        print(f"Log file not found: {LOG_FILE}")
    except Exception as e:
        print(f"Error reading logs: {e}")

def main():
    parser = argparse.ArgumentParser(description="Control Sara2 Voice Agent")
    parser.add_argument("command", choices=["start", "stop", "restart", "status", "logs"],
                       help="Command to execute")
    parser.add_argument("-n", "--lines", type=int, default=20,
                       help="Number of log lines to show (for logs command)")
    
    args = parser.parse_args()
    
    if args.command == "start":
        start()
    elif args.command == "stop":
        stop()
    elif args.command == "restart":
        restart()
    elif args.command == "status":
        status()
    elif args.command == "logs":
        logs(args.lines)

if __name__ == "__main__":
    main()
