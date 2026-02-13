#!/usr/bin/env python3
"""
SARA AGENT TECHNICAL OPERATIONS
Actually performs system analysis - no chatbot behavior
"""

import subprocess
import json
import time
import psutil
import socket

class SaraAgentTechnical:
    """Sara that performs actual technical operations"""
    
    def __init__(self):
        print("🤖 Sara Technical Agent - Ready for operations")
        
    def get_ram_usage(self):
        """Check actual RAM usage"""
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024**3), 1),
            "used_gb": round(memory.used / (1024**3), 1),
            "available_gb": round(memory.available / (1024**3), 1),
            "percent_used": round(memory.percent, 1)
        }
    
    def check_firewall(self):
        """Check firewall status"""
        try:
            # Try firewalld
            result = subprocess.run(['firewall-cmd', '--state'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return {"status": "ACTIVE", "service": "firewalld", "details": "firewall running"}
            else:
                return {"status": "INACTIVE", "service": "firewalld", "details": "service stopped"}
        except:
            try:
                # Try ufw
                result = subprocess.run(['sudo', 'ufw', 'status'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return {"status": "ACTIVE", "service": "ufw", "details": result.stdout.strip()}
                else:
                    return {"status": "INACTIVE", "service": "ufw", "details": "firewall not configured"}
            except:
                return {"status": "UNKNOWN", "service": "none", "details": "unable to access firewall"}
    
    def analyze_processes(self):
        """Get top memory processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                if proc.info['memory_percent'] > 2:
                    processes.append({
                        "name": proc.info['name'],
                        "memory_percent": round(proc.info['memory_percent'], 1),
                        "pid": proc.info['pid']
                    })
            except:
                pass
        
        return sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    
    def technical_response(self, query):
        """Respond with actual technical data"""
        query_lower = query.lower()
        
        if "ram" in query_lower or "memory" in query_lower:
            data = self.get_ram_usage()
            return f"System RAM: {data['used_gb']}GB used / {data['total_gb']}GB total ({data['percent_used']}% usage). {data['available_gb']}GB available."
            
        elif "firewall" in query_lower:
            fw = self.check_firewall()
            return f"Firewall Status: {fw['status']} - {fw['service']} service. {fw['details']}."
            
        elif "process" in query_lower:
            procs = self.analyze_processes()
            proc_list = "\n".join([f"- {p['name']}: {p['memory_percent']}% RAM (PID {p['pid']})" for p in procs])
            return f"Top memory processes:\n{proc_list}"
            
        else:
            return "Technical query received. Specify RAM, firewall, or process analysis."

def talk_to_sara():
    """Actually communicate with Sara agent"""
    print("🤖 TALKING TO SARA - AGENT MODE")
    print("=" * 30)
    
    sara = SaraAgentTechnical()
    
    # The exact questions user asked
    questions = [
        "how much ram on this system is in use",
        "what is the firewall status on this system is it setup ?", 
        "analyze the system memory for me"
    ]
    
    for question in questions:
        print(f"\n👤 User: {question}")
        print("-" * 25)
        
        # Sara responds with actual technical analysis
        time.sleep(1)
        response = sara.technical_response(question)
        
        print(f"🤖 Sara: {response}")
        print()
    
    print("✅ Agent communication complete")

if __name__ == "__main__":
    talk_to_sara()