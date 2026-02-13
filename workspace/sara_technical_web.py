#!/usr/bin/env python3
"""
SARA AGENT TECHNICAL OPERATIONS WEB SERVER
Real agent interface - no chatbot behavior
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import json

app = Flask(__name__)

class SaraWebAgent:
    """Sara web agent with actual technical capabilities"""
    
    def __init__(self):
        self.operations_performed = 0
        
    def analyze_ram_usage(self):
        """Actual RAM analysis"""
        memory = psutil.virtual_memory()
        total_gb = round(memory.total / (1024**3), 1)
        used_gb = round(memory.used / (1024**3), 1)
        percent = round(memory.percent, 1)
        available_gb = round(memory.available / (1024**3), 1)
        
        self.operations_performed += 1
        return f"System RAM Status: {used_gb}GB used from {total_gb}GB total ({percent}% utilization). {available_gb}GB memory remaining."
    
    def check_firewall_status(self):
        """Actual firewall status"""
        try:
            result = subprocess.run(['firewall-cmd', '--state'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return "Firewall is ACTIVE and running (firewalld service operational)."
            else:
                return "Firewall service is not running."
        except:
            return "Unable to access firewall status - insufficient permissions."
    
    def analyze_system_processes(self):
        """Process analysis with memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['name', 'memory_percent']):
                if proc.info['memory_percent'] > 3:
                    processes.append(f"{proc.info['name']}: {proc.info['memory_percent']:.1f}%")
            
            top_processes = "\n".join(processes[:5])
            self.operations_performed += 1
            return f"High memory usage processes:\n{top_processes}"
        except:
            return "Process analysis failed"

sara = SaraWebAgent()

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
        .status { position: fixed; top: 10px; right: 10px; background: #28a745; padding: 5px 10px; border-radius: 5px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="status">Technical Agent Active</div>
    <div class="header">
        <h1>🤖 Sara Technical Agent</h1>
        <p>Actual system analysis and operations</p>
    </div>
    <div class="chat-container">
        <div class="messages" id="messages"></div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Ask about RAM, firewall, or system analysis..." />
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
addMessage('Sara Technical Agent ready for operations. Ask about system resources.', 'agent');

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
    
    if 'ram' in message or 'memory' in message:
        response = sara.analyze_ram_usage()
    elif 'firewall' in message:
        response = sara.check_firewall_status()
    elif 'process' in message or 'system' in message:
        response = sara.analyze_system_processes()
    else:
        response = "Specify RAM analysis, firewall status, or process monitoring."
    
    return jsonify({"response": response})

@app.route('/status')
def status():
    return jsonify({
        "agent_mode": "technical_operations",
        "operations": sara.operations_performed,
        "status": "active"
    })

if __name__ == "__main__":
    print("🤖 Starting Sara Technical Agent Web Interface")
    print("🌐 http://127.0.0.1:8893")
    print("🔧 Real technical operations only - no chatbot behavior")
    app.run(host='127.0.0.1', port=8893, debug=False)