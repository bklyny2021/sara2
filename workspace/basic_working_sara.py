#!/usr/bin/env python3
"""
🚨 BASIC WORKING SARA - Emergency Restart
Just answer questions - no experiments, no personality attempts
"""

import flask
import json
import datetime
import requests
from pathlib import Path

app = flask.Flask(__name__)

class BasicWorkingSara:
    """Sara that just works - period"""
    
    def __init__(self):
        self.user_name = "Boo"  # From context
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def get_response(self, message):
        """Simple direct responses that actually work"""
        msg_lower = message.lower()
        
        # Direct answers - no personality experiments
        if "user name" in msg_lower or "who am i" in msg_lower:
            return "You're Boo.", "user_identity"
        
        elif "local ip" in msg_lower or "what is my ip" in msg_lower:
            try:
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return f"Your local IP is {ip}.", "technical_info"
            except:
                return "I'm having trouble detecting your local IP.", "technical_error"
        
        elif "hello" in msg_lower or "hi" in msg_lower:
            return "Hi Boo. What do you need?", "greeting"
        
        elif "what are you" in msg_lower or "tell me about yourself" in msg_lower:
            return "I'm Sara, your AI assistant through the OpenClaw system.", "self_info"
        
        else:
            # Simple AI response for everything else
            return self.get_simple_ai_response(message), "ai_response"
    
    def get_simple_ai_response(self, message):
        """Get basic AI response without personality experiments"""
        try:
            payload = {
                'model': 'glm-4.6:cloud',
                'prompt': f"You are Sara, a helpful AI assistant. User message: {message}\n\nRespond helpfully and directly.",
                'stream': False,
                'options': {
                    'temperature': 0.3,  # Low creativity, more focused
                    'top_p': 0.8,
                    'num_predict': 150
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=8)
            
            if response.status_code == 200:
                ai_response = response.json().get('response', '').strip()
                return ai_response
            else:
                return "I'm having trouble with my AI processing."
                
        except Exception as e:
            return "I'm experiencing technical difficulties."

# Initialize basic Sara
sara = BasicWorkingSara()

@app.route('/chat', methods=['POST'])
def chat():
    """Basic working chat endpoint"""
    data = flask.request.get_json() or {}
    message = data.get('message', '')
    
    if not message:
        return flask.jsonify({"error": "No message provided"}), 400
    
    try:
        response, response_type = sara.get_response(message)
        
        return flask.jsonify({
            "model": "Basic Working Sara",
            "response": response,
            "response_type": response_type,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return flask.jsonify({"error": "Sara encountered an error"}), 500

@app.route('/')
def index():
    """Serve theme interface"""
    try:
        with open('/home/godfather/Desktop/sara/templates/theme_switcher_index.html', 'r') as f:
            return f.read()
    except:
        return "<h1>Sara Interface</h1><p>Basic system online</p>"

@app.route('/status')
def status():
    return flask.jsonify({
        "status": "Basic Working System",
        "user_known": sara.user_name,
        "focus": "Direct question answering"
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8890, debug=False)
    
    print("🚨 BASIC SARA SYSTEM STARTING")
    print("🎯 Simple - direct - working")