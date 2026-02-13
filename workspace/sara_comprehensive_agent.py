#!/usr/bin/env python3
"""
SARA AGENT TECHNICAL OPERATIONS - EXTENDED
File operations, IP analysis, comprehensive system tasks
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import socket
import os
import json
from datetime import datetime

app = Flask(__name__)

class SaraTechnicalAgent:
    """Sara with comprehensive technical capabilities"""
    
    def __init__(self):
        self.operations_log = []
        
    def get_ip_address(self):
        """Get actual IP address"""
        try:
            # Get primary IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return f"Primary IP address: {ip}"
        except:
            # Fallback to hostname check
            try:
                result = subprocess.run(['hostname', '-I'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    ips = result.stdout.strip().split()
                    return f"System IP addresses: {', '.join(ips)}"
                else:
                    return "Unable to determine IP address"
            except:
                return "IP address detection failed"
    
    def check_firewall_status(self):
        """Comprehensive firewall analysis"""
        try:
            # Check firewalld
            result = subprocess.run(['firewall-cmd', '--state'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # Get firewall rules
                rules = subprocess.run(['firewall-cmd', '--list-all'], 
                                     capture_output=True, text=True, timeout=5)
                return f"Firewall: ACTIVE (firewalld)\nConfiguration:\n{rules.stdout}"
            else:
                # Check UFW
                ufw_result = subprocess.run(['ufw', 'status'], 
                                           capture_output=True, text=True, timeout=5)
                if ufw_result.returncode == 0:
                    return f"Firewall: ACTIVE (UFW)\n{ufw_result.stdout}"
                else:
                    return "Firewall: INACTIVE or not accessible"
        except Exception as e:
            return f"Firewall analysis failed: {str(e)}"
    
    def create_file(self, content, filename=None):
        """Create file with content"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sara_file_{timestamp}.txt"
        
        try:
            filepath = f"/tmp/{filename}"
            with open(filepath, 'w') as f:
                f.write(content)
            
            file_size = os.path.getsize(filepath)
            self.operations_log.append(f"Created file: {filepath} ({file_size} bytes)")
            return f"File created: {filepath} ({file_size} bytes)"
        except Exception as e:
            return f"File creation failed: {str(e)}"
    
    def delete_file(self, filepath):
        """Delete specified file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.operations_log.append(f"Deleted: {filepath}")
                return f"File deleted: {filepath}"
            else:
                return f"File not found: {filepath}"
        except Exception as e:
            return f"Deletion failed: {str(e)}"
    
    def list_files(self, directory="/tmp"):
        """List files in directory"""
        try:
            files = []
            for item in os.listdir(directory):
                path = os.path.join(directory, item)
                if os.path.isfile(path):
                    size = os.path.getsize(path)
                    files.append(f"{item} ({size} bytes)")
            return "Files:\n" + "\n".join(files)
        except Exception as e:
            return f"File listing failed: {str(e)}"

sara = SaraTechnicalAgent()

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Sara Technical Agent</title>
    <style>
        body { font-family: Arial; background: #1a1a1a; color: #fff; margin: 0; }
        .header { background: #ff6b6b; padding: 15px; text-align: center; }
        .chat-container { max-width: 800px; margin: 20px auto; height: 600px; display: flex; flex-direction: column; }
        .messages { flex: 1; overflow-y: auto; border: 1px solid #444; padding: 15px; background: #2a2a2a; }
        .message { margin: 10px 0; }
        .user { text-align: right; color: #007bff; }
        .agent { text-align: left; color: #4CAF50; }
        .input-area { display: flex; gap: 10px; padding: 10px; background: #333; }
        input { flex: 1; padding: 10px; border: none; background: #444; color: #fff; border-radius: 5px; }
        button { padding: 10px 20px; background: #ff6b6b; border: none; color: #fff; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Sara Technical Agent</h1>
        <p>File operations, IP analysis, system monitoring</p>
    </div>
    <div class="chat-container">
        <div class="messages" id="messages"></div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Ask about firewall, IP, create files, delete files..." />
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
<script>
function addMessage(content, sender) {
    const messages = document.getElementById('messages');
    const message = document.createElement('div');
    message.className = 'message ' + sender;
    message.textContent = content;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}
addMessage('Sara Technical Agent ready. IP analysis, firewall status, file operations available.', 'agent');

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    if (!message) return;
    
    addMessage(message, 'user');
    input.value = '';
    
    fetch('/ask', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message})})
        .then(r => r.json())
        .then(data => addMessage(data.response, 'agent'));
}
document.getElementById('messageInput').addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });
</script>
</body>
</html>
'''

@app.route('/ask', methods=['POST'])
def handle_query():
    data = request.get_json()
    message = data.get('message', '').lower()
    
    if 'firewall' in message or 'firewall status' in message:
        response = sara.check_firewall_status()
        
    elif 'ip' in message or 'ip address' in message:
        response = sara.get_ip_address()
        
    elif 'create file' in message and 'content' in message.lower():
        # Extract content and filename from request
        try:
            request_data = json.loads(data.get('message', '{}'))
            content = request_data.get('content', 'Default file content')
            filename = request_data.get('filename', None)
            response = sara.create_file(content, filename)
        except:
            response = "Format: create file with content 'your content' name 'filename.ext'"
            
    elif 'create file' in message:
        content = message.split('content')[-1].strip() if 'content' in message else "Default file created by Sara"
        response = sara.create_file(content)
        
    elif 'delete file' in message or 'remove file' in message:
        # Extract filepath from message
        if '/tmp/' in message:
            filepath = message.split('/tmp/')[-1].split()[0]
            filepath = f"/tmp/{filepath}"
            response = sara.delete_file(filepath)
        else:
            response = "Specify file path (e.g., /tmp/filename.txt)"
            
    elif 'list files' in message:
        response = sara.list_files()
        
    elif 'ram' in message or 'memory' in message:
        import psutil
        memory = psutil.virtual_memory()
        response = f"RAM: {memory.used / (1024**3):.1f}GB used / {memory.total / (1024**3):.1f}GB total ({memory.percent:.1f}%)"
        
    else:
        response = "Specify: firewall status, IP address, create file, delete file, list files"
    
    return jsonify({"response": response})

@app.route('/status')
def status():
    return jsonify({
        "agent_mode": "comprehensive_technical_operations",
        "operations": len(sara.operations_log),
        "last_operations": sara.operations_log[-5:] if sara.operations_log else []
    })

if __name__ == "__main__":
    print("🤖 Starting Sara Technical Agent - Extended Operations")
    print("🌐 http://127.0.0.1:8894")
    print("🔧 File operations, IP analysis, system tools")
    app.run(host='127.0.0.1', port=8894, debug=False)