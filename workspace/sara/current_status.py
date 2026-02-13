#!/usr/bin/env python3
# 📊 Current Voice System Status Report

import os
import json
import subprocess
from datetime import datetime

def get_voice_system_status():
    """Get comprehensive voice system status"""
    status = {
        "timestamp": datetime.now().isoformat(),
        "voice_system": {
            "voice_agent_running": is_process_running("sara_voice_agent.py"),
            "gui_running": is_process_running("simple_gui.py"),
            "speech_recognition": check_component_available("speech_recognition"),
            "tts_available": check_component_available("pyttsx3"),
            "vosk_available": check_component_available("vosk"),
            "wake_word_configured": "Sara",
            "operation_mode": "keyboard_fallback" if not check_component_available("speech_recognition") else "_voice_active"
        },
        "system_resources": get_system_resources(),
        "monitoring": {
            "sara_access_enabled": True,
            "log_files_available": check_log_files(),
            "running_processes": get_running_processes(),
            "health_status": "HEALTHY" if check_system_health() else "DEGRADED"
        },
        "interaction_counts": {
            "voice_agent_log_entries": count_log_entries(),
            "system_uptime": get_process_uptime(),
            "last_interaction": get_last_interaction()
        }
    }
    
    return status

def is_process_running(process_name):
    """Check if process is running"""
    try:
        result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_component_available(component):
    """Check if Python component is available"""
    try:
        __import__(component)
        return True
    except ImportError:
        return False

def get_system_resources():
    """Get current system resource usage"""
    try:
        import psutil
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "network_active": bool(len(psutil.net_if_addrs()) > 1)
        }
    except:
        return {"error": "psutil not available"}

def check_log_files():
    """Check if log files exist and are accessible"""
    log_files = [
        "/home/godfather/local-command-center/logs/sara_voice.log",
        "/home/godfather/local-command-center/logs/voice_system.log"
    ]
    
    available = {}
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                size = os.path.getsize(log_file)
                available[os.path.basename(log_file)] = {
                    "exists": True,
                    "size_bytes": size,
                    "readable": os.access(log_file, os.R_OK)
                }
            except:
                available[os.path.basename(log_file)] = {"exists": True, "error": "access_error"}
        else:
            available[os.path.basename(log_file)] = {"exists": False}
    
    return available

def get_running_processes():
    """Get count of running voice system processes"""
    processes = ["sara_voice_agent.py", "simple_gui.py", "start_voice_system.py"]
    running = 0
    
    for proc in processes:
        if is_process_running(proc):
            running += 1
    
    return {"total_processes": running, "expected_processes": 2, "details": processes}

def check_system_health():
    """Check overall system health"""
    checks = [
        is_process_running("sara_voice_agent.py"),
        os.path.exists("/home/godfather/local-command-center/logs/sara_voice.log"),
        check_component_available("pyttsx3")
    ]
    
    return sum(checks) >= 2  # At least 2/3 checks pass

def count_log_entries():
    """Count entries in voice agent log"""
    log_file = "/home/godfather/local-command-center/logs/sara_voice.log"
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                return len(f.readlines())
        except:
            return 0
    else:
        return 0

def get_process_uptime():
    """Get process uptime info"""
    try:
        result = subprocess.run(['ps', '-o', 'etime=', '-p', str(get_pid("sara_voice_agent.py"))], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            return result.stdout.strip()
        else:
            return "unknown"
    except:
        return "unknown"

def get_pid(process_name):
    """Get process ID"""
    try:
        result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
        if result.stdout.strip():
            return int(result.stdout.strip().split()[0])
        else:
            return None
    except:
        return None

def get_last_interaction():
    """Get last interaction from logs"""
    log_file = "/home/godfather/local-command-center/logs/sara_voice.log"
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    return lines[-1].strip()
        except:
            pass
    
    return "No interactions logged"

def save_status_report(status):
    """Save status report for Sara access"""
    report_file = "/home/godfather/local-command-center/current_status.json"
    
    with open(report_file, 'w') as f:
        json.dump(status, f, indent=2)
    
    return report_file

def main():
    """Generate and display status report"""
    print("🔍 Checking Voice System Status...")
    
    status = get_voice_system_status()
    
    print("\n📊 VOICE SYSTEM STATUS REPORT")
    print("=" * 50)
    
    # Voice System Status
    voice = status["voice_system"]
    print(f"🎤 Voice Agent: {'✅ RUNNING' if voice['voice_agent_running'] else '❌ STOPPED'}")
    print(f"🖥️  Monitoring GUI: {'✅ RUNNING' if voice['gui_running'] else '❌ STOPPED'}")
    print(f"🗣️  Speech Recognition: {'✅ AVAILABLE' if voice['speech_recognition'] else '⚠️  KEYBOARD FALLBACK'}")
    print(f"🔊 Text-to-Speech: {'✅ AVAILABLE' if voice['tts_available'] else '❌ UNAVAILABLE'}")
    print(f"🔧 Operating Mode: {voice['operation_mode']}")
    
    # System Resources
    resources = status["system_resources"]
    if "error" not in resources:
        print(f"\n📊 System Resources:")
        print(f"   CPU Usage: {resources['cpu_percent']}%")
        print(f"   Memory Usage: {resources['memory_percent']}%")
        print(f"   Disk Usage: {resources['disk_percent']}%")
        print(f"   Network: {'🔗 Connected' if resources['network_active'] else '❌ Offline'}")
    
    # Monitoring 
    monitoring = status["monitoring"]
    print(f"\n📈 Monitoring Status:")
    print(f"   Sara Access: {'✅ ENABLED' if monitoring['sara_access_enabled'] else '❌ DISABLED'}")
    print(f"   System Health: {monitoring['health_status']}")
    print(f"   Running Processes: {monitoring['running_processes']['total_running']}/{monitoring['running_processes']['total_processes']}")
    
    # Recent Activity
    interactions = status["interaction_counts"]
    print(f"\n💬 Recent Activity:")
    print(f"   Log Entries: {interactions['voice_agent_log_entries']}")
    print(f"   Process Uptime: {interactions['system_uptime']}")
    print(f"   Last Interaction: {interactions['last_interaction']}")
    
    # Save for Sara access
    report_file = save_status_report(status)
    print(f"\n💾 Status report saved: {report_file}")
    print("🔗 Sara can access this report at any time")
    
    print("\n🎉 Voice System Status Check Complete!")
    
    return status

if __name__ == "__main__":
    main()