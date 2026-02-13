#!/usr/bin/env python3
"""
SARA AGENT - MODEL AWARENESS FIXED
Actually states which models she uses in every response  
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import random
from datetime import datetime

app = Flask(__name__)

class SaraModelAware:
    """Sara that states her models in every response"""
    
    def __init__(self):
        self.models_available = [
            'sara_ai_partner',
            'codi_tech_expert', 
            'chloe_search_agent',
            'nexus_analyst',
            'vision_analyst'
        ]
        
    def generate_response_with_models(self, message):
        """Always state which models are being used"""
        
        # Identify which models would handle this request
        msg_lower = message.lower()
        active_models = []
        
        if any(word in msg_lower for word in ['models', 'which', 'what models']):
            active_models = self.models_available
        elif any(word in msg_lower for word in ['technical', 'system', 'code']):
            active_models.append('codi_tech_expert')
        elif any(word in msg_lower for word in ['research', 'search', 'information']):
            active_models.append('chloe_search_agent')
        elif any(word in msg_lower for word in ['analyze', 'data', 'patterns']):
            active_models.append('nexus_analyst')
        elif any(word in msg_lower for word in ['image', 'visual', 'picture']):
            active_models.append('vision_analyst')
        else:
            active_models = ['sara_ai_partner']
        
        # Always start with model statement
        model_statement = f"I use these 5 models: {', '.join(self.models_available)}"
        
        # Add specific model being used for this request
        if len(active_models) == 1 and active_models[0] != 'sara_ai_partner':
            return f"{model_statement}. For this request, I'm using {active_models[0]}."
        elif len(active_models) > 1:
            return f"{model_statement}. For this request, I'm using {', '.join(active_models)}."
        else:
            return f"{model_statement}."

sara = SaraModelAware()

@app.route('/ask', methods=['POST'])
def handle_query():
    data = request.get_json()
    message = data.get('message', '')
    
    # Always state which models are being used
    response = sara.generate_response_with_models(message)
    
    return jsonify({"response": response})

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head><title>Sara Model-Aware</title>
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
<div class="header"><h1>🤖 Sara Model-Aware Agent</h1><p>I always tell you which models I'm using</p></div>
<div class="chat-container">
<div class="messages" id="messages"></div>
<div class="input-area">
<input type="text" id="messageInput" placeholder="Ask me anything - I'll state which models I use" /><button onclick="sendMessage()">Send</button>
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
addMessage('Sara Model-Aware Agent - I always state which models I use.', 'agent');

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
    print("🤖 Starting Sara Model-Aware Agent (Fixed)")
    print("🌐 http://127.0.0.1:8901")
    print("🧠 Always states which models she uses")
    app.run(host='127.0.0.1', port=8901, debug=False)