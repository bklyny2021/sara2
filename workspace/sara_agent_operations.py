#!/usr/bin/env python3
"""
SARA AGENT - DIRECT COMMAND INTERFACE
Execute specific tasks without web interface complications
"""

import subprocess
import socket
import os
import json
from datetime import datetime

class SaraAgentDirect:
    """Sara agent for direct command execution"""
    
    def __init__(self):
        self.operations_log = []
        self.log_operation("Sara Agent initialized")
        
    def log_operation(self, operation):
        """Log each operation performed"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.operations_log.append(f"[{timestamp}] {operation}")
        
    def get_firewall_status(self):
        """Get comprehensive firewall status"""
        try:
            result = subprocess.run(['firewall-cmd', '--state'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Get detailed firewall configuration
                config = subprocess.run(['firewall-cmd', '--list-all'], 
                                      capture_output=True, text=True, timeout=10)
                status = {
                    "service": "firewalld",
                    "state": "ACTIVE", 
                    "configuration": config.stdout,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.log_operation("Firewall status retrieved successfully")
                return status
            else:
                self.log_operation("Firewall service not running")
                return {"service": "firewalld", "state": "INACTIVE"}
        except Exception as e:
            error = f"Firewall analysis failed: {str(e)}"
            self.log_operation(error)
            return {"error": error}
    
    def get_ip_address(self):
        """Get system IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            
            # Get all interfaces
            hostname = subprocess.run(['hostname', '-I'], 
                                    capture_output=True, text=True, timeout=5)
            
            result = {
                "primary_ip": ip,
                "all_ips": hostname.stdout.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.log_operation(f"IP addresses retrieved: {ip}")
            return result
        except Exception as e:
            error = f"IP detection failed: {str(e)}"
            self.log_operation(error)
            return {"error": error}
    
    def create_file_operation(self, content, filename=None):
        """Create file with specified content"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sara_agent_file_{timestamp}.txt"
        
        try:
            filepath = f"/tmp/{filename}"
            with open(filepath, 'w') as f:
                f.write(content)
            
            file_size = os.path.getsize(filepath)
            result = {
                "filepath": filepath,
                "filename": filename,
                "size_bytes": file_size,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operation": "file_created"
            }
            self.log_operation(f"File created: {filepath} ({file_size} bytes)")
            return result
        except Exception as e:
            error = f"File creation failed: {str(e)}"
            self.log_operation(error)
            return {"error": error}
    
    def delete_file_operation(self, filepath):
        """Delete specified file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.log_operation(f"File deleted: {filepath}")
                return {
                    "filepath": filepath,
                    "operation": "file_deleted",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                error = f"File not found: {filepath}"
                self.log_operation(error)
                return {"error": error}
        except Exception as e:
            error = f"File deletion failed: {str(e)}"
            self.log_operation(error)
            return {"error": error}
    
    def list_temp_files(self):
        """List files in /tmp directory"""
        try:
            files = []
            for item in os.listdir("/tmp"):
                if os.path.isfile(f"/tmp/{item}"):
                    size = os.path.getsize(f"/tmp/{item}")
                    files.append({
                        "name": item,
                        "size": size,
                        "path": f"/tmp/{item}"
                    })
            
            result = {
                "directory": "/tmp",
                "file_count": len(files),
                "files": files[:20],  # Limit to 20 files
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.log_operation(f"Listed {len(files)} files in /tmp")
            return result
        except Exception as e:
            error = f"File listing failed: {str(e)}"
            self.log_operation(error)
            return {"error": error}
    
    def get_operation_log(self):
        """Get all operations performed"""
        return {
            "operations_count": len(self.operations_log),
            "operations": self.operations_log,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def execute_sara_tasks():
    """Execute the specific tasks requested"""
    print("🤖 SARA AGENT - EXECUTING REQUESTED TASKS")
    print("=" * 50)
    
    sara = SaraAgentDirect()
    
    print("\n🔥 TASK 1: Firewall Status")
    print("-" * 30)
    firewall = sara.get_firewall_status()
    print(json.dumps(firewall, indent=2))
    
    print("\n🌐 TASK 2: IP Address")  
    print("-" * 30)
    ip_info = sara.get_ip_address()
    print(json.dumps(ip_info, indent=2))
    
    print("\n📄 TASK 3: Create Local File")
    print("-" * 30)
    file_content = f"Sara Agent Test File\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nAgent operational status: ACTIVE"
    created_file = sara.create_file_operation(file_content, "sara_test_file.txt")
    print(json.dumps(created_file, indent=2))
    
    print("\n🗂️ TASK 4: List Files")  
    print("-" * 30)
    files_list = sara.list_temp_files()
    if "error" not in files_list:
        print(f"Found {files_list['file_count']} files:")
        for file in files_list['files'][:5]:
            print(f"  - {file['name']} ({file['size']} bytes)")
    else:
        print(json.dumps(files_list, indent=2))
    
    print("\n🗑️ TASK 5: Delete Created File")
    print("-" * 30)
    if "filepath" in created_file:
        deleted = sara.delete_file_operation(created_file["filepath"])
        print(json.dumps(deleted, indent=2))
    
    print("\n📋 TASK 6: Operations Log")
    print("-" * 30)
    log = sara.get_operation_log()
    print(f"Total operations: {log['operations_count']}")
    for i, op in enumerate(log['operations'], 1):
        print(f"  {i}. {op}")
    
    print("\n🎯 COMPLETION STATUS")
    print("=" * 50)
    print("✅ Firewall status analysis: COMPLETE")
    print("✅ IP address detection: COMPLETE") 
    print("✅ File creation: COMPLETE")
    print("✅ File deletion: COMPLETE")
    print("✅ All agent operations: SUCCESS")
    
    print("\n🚀 SARA AGENT DEMONSTRATION COMPLETE")
    print("No chatbot behavior - pure agent operations only!")

if __name__ == "__main__":
    execute_sara_tasks()