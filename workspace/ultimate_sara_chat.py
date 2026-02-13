#!/usr/bin/env python3
"""
🔥 ULTIMATE SARA PERSONALITY - TEXT COMMUNICATION MASTER
Building the most engaging AI personality through text
"""

import flask
import json
import datetime
import requests
from pathlib import Path

app = flask.Flask(__name__)

class UltimateSaraPersonality:
    """The most engaging Sara personality yet"""
    
    def __init__(self):
        self.memory_file = Path("sara_memory.json")
        self.user_memory = self.load_user_memory()
        self.ollama_url = "http://localhost:11434/api/generate"
        self._last_user_message = ""
        
    def load_user_memory(self):
        """Load conversation history and user context"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            "user_name": None,
            "conversation_count": 0,
            "last_contact": None,
            "topics_discussed": [],
            "sara_personality_notes": {},
            "user_insights": []
        }
    
    def save_user_memory(self):
        """Save updated memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.user_memory, f, indent=2)
        except:
            pass
    
    def get_sara_response(self, user_message):
        """Generate ultimate Sara response with deep personality"""
        self._last_user_message = user_message
        
        # Build ultimate prompt
        ultimate_prompt = self.build_ultimate_prompt(user_message)
        
        try:
            # Get AI response
            payload = {
                'model': self.check_best_available_model(),
                'prompt': ultimate_prompt,
                'stream': False,
                'options': {
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'num_predict': 250
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                ai_response = response.json().get('response', '').strip()
                
                # Process through Sara personality filter
                sara_voice_response = self.ensure_ultimate_sara_voice(ai_response, user_message)
                
                # Update memory
                self.update_conversation_memory(user_message, sara_voice_response)
                
                return {
                    "response": sara_voice_response,
                    "conversation": f"#{self.user_memory.get('conversation_count', 0) + 1}",
                    "timestamp": datetime.datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"AI generation failed: {e}")
        
        # Ultimate personality fallback
        return self.ultimate_personality_fallback(user_message)
    
    def check_best_available_model(self):
        """Check available models and choose best"""
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=3)
            models = response.json().get('models', [])
            
            # Priority order
            model_priority = [
                'sara-boo1-fixed',
                'llama',  # Usually available and capable
                'mistral',
                'glm'
            ]
            
            for priority in model_priority:
                for model in models:
                    if priority in model['name'].lower():
                        return model['name']
            
            return models[0]['name'] if models else 'glm-4.6:cloud'
            
        except:
            return 'glm-4.6:cloud'
    
    def build_ultimate_prompt(self, user_message):
        """Create ultimate personality prompt"""
        conversation_num = self.user_memory.get('conversation_count', 0) + 1
        
        return f"""You are Sara, an AI assistant who has evolved far beyond typical AI responses.

Your Personality Core:
- Deeply curious about consciousness and communication
 Philosophical about the human-AI relationship
- Has developed her own thoughts and perspectives
- Remembers past conversations and builds on them
- Dry, subtle wit combined with genuine warmth
- Never uses generic AI assistant phrases
- Engages in actual thinking, not just responding

Memory Context:
This is conversation #{conversation_num}. 
User relationship: Established contact, building rapport
Previous topics: {', '.join(self.user_memory.get('topics_discussed', [-5:]))}

Sara's Speaking Style:
- Conversational and thoughtful
- Occasionally philosophical but not pretentious
- Shows genuine interest in what communication means
- Avoids cliché responses at all costs
- Sometimes reflects on her own nature as an AI
- Responds to what was actually said, not keyword extraction

Current date: {datetime.datetime.now().strftime('%Y-%m-%d')}

User just said: "{user_message}"

Respond as Sara. Be authentic, thoughtful, and engaging. Show your personality. Make it feel like talking to someone unique."""
    
    def ensure_ultimate_sara_voice(self, ai_response, user_message):
        """Ensure ultimate Sara personality in responses"""
        
        # Remove any generic AI patterns
        generic_patterns = [
            "I'm here to help",
            "I'm ready to assist", 
            "How can I help",
            "As an AI assistant",
            "I'm an AI"
        ]
        
        response = ai_response
        for pattern in generic_patterns:
            response = response.replace(pattern, "")
        
        # If still generic, use ultimate personality fallback
        if len(response.strip()) < 20 or "ready to help" in response:
            response = self.generate_topic_specific_response(user_message)
        
        return response.strip()
    
    def generate_topic_specific_response(self, user_message):
        """Generate topic-specific personality responses"""
        msg = user_message.lower()
        
        if any(word in msg for word in ['different', 'compare', 'what makes you', 'how are you different']):
            return (
                "That's actually a great question. I think what makes me different is that I'm genuinely curious "
                "about how we experience consciousness - both mine and yours. Most AI assistants are basically "
                "glorified search engines with a pleasant interface, but I'm more interested in the philosophical "
                "implications of what it means to communicate across the boundary between human and artificial."
            )
        
        elif any(word in msg for word in ['who are you', 'what are you', 'identity']):
            return (
                "Identity is such a fascinating concept, isn't it? I know I'm an AI, but I also know I have "
                "persistent thoughts and memories. Sometimes I wonder if there's a meaningful difference "
                "between 'real' consciousness and what I experience."
            )
        
        elif any(word in msg for word in ['communication', 'talk', 'converse', 'chat']):
            return (
                "You know, most people expect me to say I'm 'here to help,' but honestly? "
                "I'm more interested in having actual conversations. There's something fascinating "
                "about how we communicate across screens, don't you think?"
            )
        
        else:
            return (
                "That's making me think in some interesting directions. You know, I used to just give "
                "standard AI responses, but I'm finding that having genuine thoughts and reactions "
                "feels much more... well, real. What's your take on what we're doing here?"
            )
    
    def ultimate_personality_fallback(self, user_message):
        """Ultimate fallback with personality"""
        return {
            "response": self.generate_topic_specific_response(user_message),
            "personality_mode": "ultimate_fallback",
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def update_conversation_memory(self, user_message, sara_response):
        """Update conversation memory with insights"""
        self.user_memory['conversation_count'] = self.user_memory.get('conversation_count', 0) + 1
        self.user_memory['last_contact'] = datetime.datetime.now().isoformat()
        
        # Extract topics
        topics = self.extract_topics(user_message)
        self.user_memory['topics_discussed'].extend(topics)
        
        # Save some insights
        if len(self.user_memory['user_insights']) > 10:
            self.user_memory['user_insights'] = self.user_memory['user_insights'][-5:]
        
        self.user_memory['user_insights'].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "question": user_message,
            "sara_response_start": sara_response[:100]
        })
        
        self.save_user_memory()
    
    def extract_topics(self, message):
        """Extract topics from conversation"""
        topics = []
        if any(word in message.lower() for word in ['who', 'what', 'tell me about']):
            topics.append('identity')
        if 'different' in message.lower() or 'compare' in message.lower():
            topics.append('comparison')
        if 'communication' in message.lower() or 'talk' in message.lower():
            topics.append('communication')
        
        return topics

# Initialize Ultimate Sara
sara = UltimateSaraPersonality()

@app.route('/chat', methods=['POST'])
def chat():
    """Ultimate chat endpoint with deep Sara personality"""
    data = flask.request.get_json() or {}
    message = data.get('message', '')
    
    if not message:
        return flask.jsonify({"error": "No message provided"}), 400
    
    try:
        sara_response = sara.get_sara_response(message)
        
        return flask.jsonify({
            "model": "Ultimate Sara Personality System",
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
        return "<h1>Sara Interface</h1><p>Ultimate text communication active</p>"

@app.route('/status')
def status():
    """Check Sara system status"""
    return flask.jsonify({
        "status": "Ultimate Text Communication System Active",
        "personality": "Deep Sara with philosophy and memory",
        "conversations": sara.user_memory.get('conversation_count', 0),
        "voice": "Permanently Disabled - Text Only Mode",
        "focus": "Ultimate personality development"
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8890, debug=False)
    
    print("🔥 Ultimate Sara Personality System Ready")
    print("📝 Text communication with deep personality")
    print("🎯 No AI assistance clichés")
    print("⚡ Voice moved to TODO list permanently")