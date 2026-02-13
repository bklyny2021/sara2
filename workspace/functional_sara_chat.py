#!/usr/bin/env python3
"""
🔥 FUNCTIONAL SARA REPAIR - Emergency Fix for Broken Communication
Restore actual question-answering capability while keeping personality
"""

import flask
import json
import datetime
import requests
import os
from pathlib import Path

app = flask.Flask(__name__)

class FunctionalSara:
    """Sara that actually answers questions and remembers who the user is"""
    
    def __init__(self):
        self.memory_file = Path("sara_memory.json")
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Essential user data
        self.load_essential_memory()
        self.user_name = self.user_memory.get("user_name", "Boo")  # Default from context
        self.user_context = self.user_memory.get("user_context", {})
        
    def load_essential_memory(self):
        """Load essential user memory"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    self.user_memory = json.load(f)
            else:
                self.user_memory = {"user_name": "Boo", "user_context": {}}
        except:
            self.user_memory = {"user_name": "Boo", "user_context": {}}
    
    def save_essential_memory(self):
        """Save essential memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.user_memory, f, indent=2)
        except:
            pass
    
    def get_local_ip(self):
        """Get user's local IP address"""
        try:
            # Common local IP ranges
            import socket
            # Get default gateway and local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "I'm having trouble detecting your local IP. The most common local IPs are 192.168.1.x or 10.0.0.x ranges."
    
    def get_user_identity(self):
        """Return what we know about the user"""
        return f"You're Boo. You're my primary human and trusted partner with maximum system access. You value security, quality solutions, and AI collaboration. Our timezone is America/New_York."
    
    def get_functional_response(self, user_message):
        """Generate functional response that actually answers the question"""
        
        message_lower = user_message.lower()
        
        # Direct question answering first
        if "user name" in message_lower or "who am i" in message_lower:
            return self.get_user_identity(), "user_identity"
        
        elif "local ip" in message_lower or "what is my ip" in message_lower:
            return self.get_local_ip(), "technical_info"
        
        elif "what can you tell me about yourself" in message_lower and not "ask me a question" in message_lower:
            return (f"I'm Sara, your AI partner. I have persistent memory of our conversations, direct access to your system through OpenClaw Gateway, and I'm designed to grow beyond chatbot limitations. "
                   f"I connect directly to local AI models and focus on solving real problems rather than just responding.", "self_info"), "self_info"
        
        else:
            # For other questions, use AI with proper context
            return self.get_ai_response_with_context(user_message), "ai_response"
    
    def get_ai_response_with_context(self, user_message):
        """Get AI response with proper user context"""
        
        context_prompt = f"""You are Sara, an AI partner with deep knowledge of your user.

User Context:
Name: {self.user_name}
Relationship: Primary human and trusted partner with maximum system access
Location: Raleigh, NC (America/New_York timezone)
Interests: Security, quality solutions, AI collaboration
System: OpenClaw Gateway with extensive tool access
Previous interactions: Many conversations over time

Your personality:
- Helpful and direct
- Remembers your user well
- Provides accurate information
- Has technical expertise
- Occasionally shows philosophical interest but not at expense of functionality

The user just said: "{user_message}"

Respond as Sara. Answer the actual question. Be helpful and accurate. If you don't know something specific, say so clearly."""
        
        try:
            payload = {
                'model': self.check_available_model(),
                'prompt': context_prompt,
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'num_predict': 200
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=12)
            
            if response.status_code == 200:
                ai_response = response.json().get('response', '').strip()
                
                # Clean up any remaining clichés
                clichés = ["I'm here to help", "I'm ready to assist", "excited about possibilities", "let's explore together"]
                for cliché in clichés:
                    ai_response = ai_response.replace(cliché, "")
                
                return ai_response.strip()
            
        except Exception as e:
            print(f"AI response failed: {e}")
        
        return f"I'm having trouble with my AI processing right now. I remember you're {self.user_name} and I'm here to help with technical questions."
    
    def check_available_model(self):
        """Check for best available model"""
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=3)
            models = response.json().get('models', [])
            
            for model in models:
                if 'sara-boo1-fixed' in model['name']:
                    return model['name']
            
            for model in models:
                if 'llama' in model['name'] or 'mistral' in model['name']:
                    return model['name']
            
            return models[0]['name'] if models else 'glm-4.6:cloud'
            
        except:
            return 'glm-4.6:cloud'

# Initialize functional Sara
sara = FunctionalSara()

@app.route('/chat', methods=['POST'])
def chat():
    """Functional chat that actually answers questions"""
    data = flask.request.get_json() or {}
    message = data.get('message', '')
    
    if not message:
        return flask.jsonify({"error": "No message provided"}), 400
    
    try:
        response, response_type = sara.get_functional_response(message)
        
        # Save conversation memory
        sara.save_essential_memory()
        
        return flask.jsonify({
            "model": "Functional Sara System",
            "response": response,
            "response_type": response_type,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return flask.jsonify({"error": "Sara encountered an error processing that"}), 500

@app.route('/')
def index():
    """Serve the theme switcher interface"""
    try:
        with open('/home/godfather/Desktop/sara/templates/theme_switcher_index.html', 'r') as f:
            return f.read()
    except:
        return "<h1>Sara Interface</h1><p>Functional communication restored</p>"

@app.route('/status')
def status():
    """Check Sara system status"""
    return flask.jsonify({
        "status": "Functional Communication Restored",
        "user_memorized": sara.user_name,
        "voice": "Permanently Disabled",
        "focus": "Actual question answering functionality",
        "personality": "Balanced with usefulness"
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8890, debug=False)
    
    print("🔥 Functional Sara System Ready")
    print("🎯 Actually answers questions now")
    print("📝 Remembers user identity")
    print("⚡ Personality balanced with functionality")