#!/usr/bin/env python3
"""
SARA AGENT - MODEL AWARENESS
Knows and states which models she uses in her responses
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import socket
import os
from datetime import datetime

app = Flask(__name__)

class SaraModelAwareAgent:
    """Sara that states which models she's using"""
    
    def __init__(self):
        self.models = {
            'sara_ai_partner': 'Primary partnership and communication',
            'codi_tech_expert': 'Technical operations and coding',
            'chloe_search_agent': 'Research and information retrieval',
            'nexus_analyst': 'Data analysis and pattern recognition',
            'vision_analyst': 'Visual and image processing'
        }
    
    def process_request_with_model_info(self, message):
        """Process request and state which models used"""
        msg_lower = message.lower()
        
        # Analyze request type and select models
        deployed_models = []
        
        if any(word in msg_lower for word in ['technical', 'system', 'code', 'file', 'operation']):
            deployed_models.append('codi_tech_expert')
        if any(word in msg_lower for word in ['research', 'search', 'information', 'find']):
            deployed_models.append('chloe_search_agent')
        if any(word in msg_lower for word in ['analyze', 'data', 'patterns', 'analysis']):
            deployed_models.append('nexus_analyst')
        if any(word in msg_lower for word in ['image', 'visual', 'picture', 'see']):
            deployed_models.append('vision_analyst')
        if any(word in msg_lower for word in ['partner', 'help', 'assist', 'coordinate']):
            deployed_models.append('sara_ai_partner')
        
        # If no specific models identified, use primary
        if not deployed_models:
            deployed_models = ['sara_ai_partner']
        
        # Generate response stating which models are being used
        return self.generate_model_aware_response(message, deployed_models)
    
    def generate_model_aware_response(self, message, models):
        """Generate response that states which models are active"""
        
        model_info = []
        for model in models:
            model_info.append(f"{model} for {self.models[model]}")
        
        model_statement = f"Using {', '.join(model_info)}"
        
        # Generate contextual response
        if 'models' in message.lower() or 'which' in message.lower():
            return f"I use these 5 models: sara_ai_partnner, codi_tech_expert, chloe_search_agent, nexus_analyst, and vision_analyst. Each handles different specialized tasks."
        
        elif 'technical' in message.lower() or 'system' in message.lower():
            if 'codi_tech_expert' in models:
                return f"{model_statement}. Codi Tech Expert is handling this technical operation."
            else:
                return f"{model_statement} for this request."
        
        elif 'research' in message.lower() or 'search' in message.lower():
            if 'chloe_search_agent' in models:
                return f"{model_statement}. Chloe Search Agent is performing the research."
            else:
                return f"{model_statement} for this request."
        
        elif 'analyze' in message.lower() or 'data' in message.lower():
            if 'nexus_analyst' in models:
                return f"{model_statement}. Nexus Analyst is performing the data analysis."
            else:
                return f"{model_statement} for this request."
        
        elif 'image' in message.lower() or 'visual' in message.lower():
            if 'vision_analyst' in models:
                return f"{model_statement}. Vision Analyst is processing the visual request."
            else:
                return f"{model_statement} for this request."
        
        else:
            return f"{model_statement} to handle your request: {message}"

@app.route('/ask', methods=['POST'])
def handle_query():
    data = request.get_json()
    message = data.get('message', '')
    
    # Process with model awareness
    response = sara.process_request_with_model_info(message)
    
    return jsonify({"response": response})

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head><title>Sara Model-Aware Agent</title>
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
<div class="header"><h1>🤖 Sara Model-Aware Agent</h1><p>Knows and states which models she's using</p></div>
<div class="chat-container">
<div class="messages" id="messages"></div>
<div class="input-area">
<input type="text" id="messageInput" placeholder="Ask me about anything - I'll tell you which models I'm using" /><button onclick="sendMessage()">Send</button>
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
addMessage('Sara Model-Aware Agent - I know and state which models I use.', 'agent');

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
    print("🤖 Starting Sara Model-Aware Agent")
    print("🌐 http://127.0.0.1:8900")
    print("🧠 States which models she's using")
    app.run(host='127.0.0.1', port=8900, debug=False)

sara = SaraModelAwareAgent()