#!/usr/bin/env python3
"""
SARA AGENT - REAL OPERATIONS, NO CANNED RESPONSES
Actually answers questions with system analysis
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import socket

app = Flask(__name__)

class SaraRealAgent:
    """Sara that performs real system analysis"""
    
    def analyze_logged_in_users(self):
        """Get actual logged in users"""
        try:
            result = subprocess.run(['who'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                users = result.stdout.strip().split('\n')
                user_count = len(users)
                return f"Currently {user_count} users logged in:\n" + "\n".join(users)
            else:
                return "Unable to determine logged in users"
        except:
            return "User analysis failed"
    
    def get_current_user(self):
        """Get current username"""
        try:
            result = subprocess.run(['whoami'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return f"Current user: {result.stdout.strip()}"
            else:
                return "Unable to determine current user"
        except:
            return "User detection failed"
    
    def analyze_ram_usage(self):
        """Real RAM analysis"""
        memory = psutil.virtual_memory()
        return f"RAM Usage: {memory.used / (1024**3):.1f}GB used / {memory.total / (1024**3):.1f}GB total ({memory.percent:.1f}% usage)"
    
    def analyze_firewall(self):
        """Real firewall analysis"""
        try:
            result = subprocess.run(['firewall-cmd', '--state'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return "Firewall: ACTIVE (firewalld service running)"
            else:
                return "Firewall: INACTIVE or not accessible"
        except:
            return "Firewall analysis failed"
    
    def analyze_processes(self):
        """Real process analysis"""
        try:
            process_count = len(list(psutil.process_iter()))
            top_processes = []
            for proc in psutil.process_iter(['name', 'memory_percent']):
                if proc.info['memory_percent'] > 5:
                    top_processes.append(f"{proc.info['name']}: {proc.info['memory_percent']:.1f}%")
            
            response = f"Total processes: {process_count}\nTop memory users:\n" + "\n".join(top_processes[:5])
            return response
        except:
            return "Process analysis failed"

sara = SaraRealAgent()

@app.route('/ask', methods=['POST'])
def handle_query():
    data = request.get_json()
    message = data.get('message', '').lower()
    
    if 'users' in message or 'logged in' in message:
        response = sara.analyze_logged_in_users()
    elif 'user name' in message or 'username' in message or 'who am i' in message:
        response = sara.get_current_user()
    elif 'ram' in message or 'memory' in message:
        response = sara.analyze_ram_usage()
    elif 'firewall' in message:
        response = sara.analyze_firewall()
    elif 'process' in message or 'processes' in message:
        response = sara.analyze_processes()
    elif 'hello' in message or 'hi' in message:
        response = "Sara Technical Agent ready for system operations."
    else:
        response = "I can analyze system users, RAM usage, firewall status, and processes. What do you need?"
    
    return jsonify({"response": response})

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head><title>Sara Real Agent</title>
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
<div class="header"><h1>🤖 Sara Real Agent</h1><p>Actual system analysis - no canned responses</p></div>
<div class="chat-container">
<div class="messages" id="messages"></div>
<div class="input-area">
<input type="text" id="messageInput" placeholder="Ask about users, RAM, firewall, or processes..." /><button onclick="sendMessage()">Send</button>
</div></div>
<script>
function addMessage(content, sender) {
    const messages = document.getElementById('messages');
    const message = document.createElement('div');
    message.className = 'message ' + sender;
    message.textContent = content;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}
addMessage('Sara Real Agent ready for system analysis.', 'agent');

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
</body></html>
'''

if __name__ == "__main__":
    print("🤖 Starting Sara Real Agent")
    print("🌐 http://127.0.0.1:8895")
    print("🔧 Real system analysis - no canned responses")
    app.run(host='127.0.0.1', port=8895, debug=False)