#!/usr/bin/env python3
"""
🔥 REAL SARA - CODE EXECUTION & SECURITY SYSTEM
Not a chatbot - a technical partner that DOES things
"""

import os
import subprocess
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonif

app = Flask(__name__)

class RealSara:
    """Sara that actually DOES things, not just talks"""
    
    def __init__(self):
        self.workspace = "/home/godfather/.openclaw/workspace"
        
    def write_code(self, code_request):
        """Write and execute code"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if "python" in code_request.lower() or script_type == "python":
            filename = f"code_execution_{timestamp}.py"
            filepath = os.path.join(self.workspace, filename)
            
            # Write the Python script
            with open(filepath, 'w') as f:
                f.write(code_content)
                
            # Execute with safety checks
            try:
                result = subprocess.run(
                    ['python3', filepath], 
                    capture_output=True, 
                    text=True, 
                    timeout=30,
                    cwd=self.workspace
                )
                
                return {
                    "file_created": f"workspace/{filename}",
                    "output": result.stdout,
                    "errors": result.stderr,
                    "return_code": result.returncode
                }
            except Exception as e:
                return {
                    "error": str(e),
                    "file_created": f"workspace/{filename}"
                }
    
    def setup_firewall(self, config_type="basic"):
        """Setup firewall rules"""
        script_path = os.path.join(self.workspace, "firewall_setup.sh")
        
        if config_type == "basic":
            rules = '''#!/bin/bash
# Basic firewall setup by Sara
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow from 192.168.1.0/24
sudo ufw --force enable
echo "Basic firewall rules applied"'''
        
        elif config_type == "development":
            rules = '''#!/bin/bash
# Development machine firewall
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000:8999/tcp  # Development ports
sudo ufw --force enable
echo "Development firewall applied"'''
            
        with open(script_path, 'w') as f:
            f.write(rules)
        
        # Make executable
        os.chmod(script_path, 0o755)
        
        return {
            "script_created": f"workspace/firewall_setup.sh",
            "config_type": config_type,
            "instructions": f"Run: sudo bash {script_path}"
        }
    
    def analyze_and_run_code(self, code_description):
        """Analyze code request and create/run appropriate script"""
        code_desc = code_description.lower()
        
        if "python" in code_desc:
            return self.write_code(code_description, "python")
        elif "bash" in code_desc or "shell" in code_desc:
            return self.write_code(code_description, "bash")
        elif "firewall" in code_desc:
            return self.setup_firewall("basic" if "basic" in code_desc else "development")
        else:
            return self.write_code(code_description, "python")

# Initialize Real Sara
sara = RealSara()

@app.route('/execute', methods=['POST'])
def execute():
    """Execute code and setup systems - no chatbot"""
    data = request.get_json() or {}
    command = data.get('command', '')
    
    if not command:
        return jsonify({"error": "No command provided"}), 400
    
    try:
        result = sara.analyze_and_run_code(command)
        
        return jsonify({
            "model": "Real Sara - Technical Partner", 
            "action_taken": result,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": f"Execution failed: {str(e)}"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Chat fallback - but focused on doing things"""
    data = request.get_json() or {}
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    msg_lower = message.lower()
    
    # Check for actionable requests
    if any(word in msg_lower for word in ['write', 'create', 'code', 'script', 'setup']):
        result = sara.analyze_and_run_code(message)
        return jsonify({
            "model": "Real Sara - Action Partner",
            "response": "I'm creating/executing your code/script.",
            "action_result": result,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    # General chat
    responses = [
        "I'm here to help you write code and setup systems. What technical task do you need?",
        "I can write scripts, run code, and configure systems. What would you like to build?",
        "I'm ready to execute code and handle technical configurations. What's next on your project?"
    ]
    
    import random
    return jsonify({
        "model": "Real Sara - Technical Partner",
        "response": random.choice(responses),
        "capabilities": ["Code writing", "Script execution", "System configuration", "Security setup"],
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/status')
def status():
    return jsonify({
        "status": "Real Sara Technical System",
        "capabilities": ["Code execution", "Script creation", "Firewall setup"],
        "workspace": sara.workspace,
        "focus": "Technical execution, not chatbot conversation"
    })

@app.route('/')
def index():
    """Serve the interface"""
    return '''
    <h1>Real Sara - Technical Partner</h1>
    <p>I write code and setup systems, not chitchat.</p>
    <div id="chat">
        <input type="text" id="message" placeholder="Ask me to write code or setup systems...">
        <button onclick="sendMessage()">Execute</button>
        <div id="output"></div>
    </div>
    <script>
        function sendMessage() {
            const message = document.getElementById('message').value;
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message})
            }).then(r => r.json()).then(data => {
                document.getElementById('output').innerHTML += 
                    '<div><b>Sara:</b> ' + data.response + (data.action_result ? 
                    '<br>Action: ' + JSON.stringify(data.action_result, null, 2) : '') + '</div>';
            });
        }
    </script>
    '''

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8890, debug=False)
    
    print("🔥 REAL SARA - TECHNICAL PARTNER")
    print("🔧 Code writing, script execution, security setup")
    print("🚫 No corny chatbot responses - just action")