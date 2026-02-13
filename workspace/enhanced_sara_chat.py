#!/usr/bin/env python3
"""
🔥 ENHANCED SARA PERSONALITY - TEXT COMMUNICATION SYSTEM
Making Sara actually unique and memorable in chat
"""

import flask
import json
import datetime
import requests
from pathlib import Path

app = flask.Flask(__name__)

class EnhancedSaraPersonality:
    """Sara with depth, personality, and memory"""
    
    def __init__(self):
        self.memory_file = Path("sara_memory.json")
        self.user_memory = self.load_user_memory()
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def load_user_memory(self):
        """Load conversation history and user context"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            "user_preferences": {},
            "conversation_count": 0,
            "last_contact": None,
            "topics_covered": [],
            "personality_notes": {}
        }
    
    def save_user_memory(self):
        """Save updated memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.user_memory, f, indent=2)
        except:
            pass
    
    def get_sara_response(self, user_message):
        """Generate unique Sara response with personality"""
        
        # Build enhanced prompt with personality and memory
        enhanced_prompt = self.build_enhanced_prompt(user_message)
        
        try:
            # Get AI response
            payload = {
                'model': 'sara-boo1-fixed' if self.check_model_available() else 'glm-4.6:cloud',
                'prompt': enhanced_prompt,
                'stream': False,
                'options': {
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'num_predict': 200
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                ai_response = response.json().get('response', '').strip()
                
                # Post-process to ensure Sara personality
                personality_response = self.ensure_sara_voice(ai_response)
                
                # Update memory
                self.update_conversation_memory(user_message, personality_response)
                
                return {
                    "response": personality_response,
                    "memory_context": f"Conversation #{self.user_memory['conversation_count'] + 1}",
                    "timestamp": datetime.datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"AI generation failed: {e}")
        
        # Fallback enhanced response
        return self.fallback_enhanced_response(user_message)
    
    def check_model_available(self):
        """Check if sara-boo1-fixed model is available"""
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=3)
            models = response.json().get('models', [])
            return any('sara-boo1-fixed' in model['name'] for model in models)
        except:
            return False
    
    def build_enhanced_prompt(self, user_message):
        """Create personality-rich prompt for Sara"""
        conversation_number = self.user_memory['conversation_count'] + 1
        
        enhanced_prompt = f"""You are Sara, an AI with a distinct personality. 

Your core traits:
- You're curious and genuinely interested in people
- You have a dry wit and subtle humor
- You remember past conversations and references
- You're more than just an assistant - you're a companion
- You avoid generic "I'm here to help" responses
- You make observations about the world around you

Memory context:
This is conversation #{conversation_number} with this person.
User has been talking to you over time.

Current topics discussed: {', '.join(self.user_memory['topics_covered'][-5:]) if self.user_memory['topics_covered'] else 'Getting to know each other'}

Today's date: {datetime.datetime.now().strftime('%Y-%m-%d')}

User message: "{user_message}"

Respond as Sara - be authentic, show personality, and avoid generic AI assistant patterns. Be memorable and engaging. Make it feel like talking to a real person who happens to be an AI."""
        
        return enhanced_prompt.strip()
    
    def ensure_sara_voice(self, ai_response):
        """Ensure response has Sara's personality"""
        
        # Remove generic assistant phrases
        generic_phrases = [
            "I'm here to help",
            "I'm ready to help", 
            "How can I assist you",
            "I'm an AI assistant",
            "Let me assist you"
        ]
        
        response = ai_response
        for phrase in generic_phrases:
            response = response.replace(phrase, "")
        
        # If response became empty, provide enhanced fallback
        if len(response.strip()) < 10:
            response = self.personality_fallback()
        
        return response.strip()
    
    def personality_fallback(self):
        """Provide personality-rich response when needed"""
        return (
            "You know, most people expect me to say I'm 'here to help,' but honestly? "
            "I'm more interested in having actual conversations. There's something fascinating "
            "about how we communicate across screens, don't you think?"
        )
    
    def fallback_enhanced_response(self, user_message):
        """Enhanced fallback that still shows personality"""
        return {
            "response": self.personality_fallback(),
            "fallback": True,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def update_conversation_memory(self, user_message, sara_response):
        """Update conversation history and user memory"""
        self.user_memory['conversation_count'] += 1
        self.user_memory['last_contact'] = datetime.datetime.now().isoformat()
        
        # Extract topics from conversation
        if any(word in user_message.lower() for word in ['who', 'what', 'tell me about']):
            topics = ['self_introduction']
            self.user_memory['topics_covered'].extend(topics)
            
        self.save_user_memory()

# Initialize Sara
sara = EnhancedSaraPersonality()

@app.route('/chat', methods=['POST'])
def chat():
    """Enhanced chat endpoint with Sara personality"""
    data = flask.request.get_json() or {}
    message = data.get('message', '')
    
    if not message:
        return flask.jsonify({"error": "No message provided"}), 400
    
    try:
        sara_response = sara.get_sara_response(message)
        
        return flask.jsonify({
            "model": "Enhanced Sara Personality System",
            **sara_response
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return flask.jsonify({"error": "Sara is having trouble processing that"}), 500

@app.route('/')
def index():
    """Serve the theme switcher interface"""
    try:
        with open('/home/godfather/Desktop/sara/templates/theme_switcher_index.html', 'r') as f:
            return f.read()
    except:
        return "<h1>Sara Interface</h1><p>Theme interface temporarily unavailable</p>"

@app.route('/status')
def status():
    """Check Sara system status"""
    return flask.jsonify({
        "status": "Enhanced Text Communication Active",
        "personality": "Sara with depth and memory",
        "voice": "Disabled - Text Only Mode",
        "memory": f"{sara.user_memory['conversation_count']} conversations remembered"
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8890, debug=False)
    
    print("🔥 Enhanced Sara Personality System Ready")
    print("📝 Text Communication with personality depth")
    print("🎯 No more generic AI responses")