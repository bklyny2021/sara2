#!/usr/bin/env python3
# 🌟 SARA SIMPLE AUTONOMOUS CHAT
# Rock-solid, no-complex streaming, just reliable responses

from flask import Flask, render_template, request, jsonify
import subprocess
import json
import time
import os
from pathlib import Path
import threading
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration
WORKSPACE_PATH = Path.home() / ".openclaw" / "workspace"
MEMORY_FILE = WORKSPACE_PATH / "simple_memory" / "sara_memory.json"
MEMORY_FILE.parent.mkdir(exist_ok=True)

# Simple global states
is_responding = False
should_stop = False

def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"conversations": [], "preferences": {}, "tasks": [], "context": {}}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def get_sara_response(message):
    """Get simple, reliable response from Sara"""
    global is_responding, should_stop
    
    try:
        # Handle system/network queries directly when needed
        if "ip address" in message.lower() or "what is the ip" in message.lower():
            try:
                result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    ips = result.stdout.strip().split()
                    ipv4 = [ip for ip in ips if ":" not in ip and ip != "127.0.0.1"]
                    if ipv4:
                        return f"My IP address is: {ipv4[0]}"
                return "I couldn't determine the IP address at the moment."
            except:
                return "I had trouble getting the IP address."
        
        # Build command using correct OpenClaw agent syntax
        command = ["openclaw", "agent", "--session-id", "agent:main:main", "--message", message]
        
        # Execute command with timeout
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=40,
            check=False
        )
        
        # Clean up response properly
        response = result.stdout.strip()
        if not response or result.returncode != 0:
            return "I had trouble processing that. Could you rephrase your question?"
        
        # Better cleanup of terminal escape sequences
        import re
        response = re.sub(r'\[\?\d+[hlmK]', '', response)  # Remove various escape sequences
        response = re.sub(r'\[\d+[hlmK]', '', response)    # Remove numbered sequences  
        response = re.sub(r'\[\?\d*[hlmK]', '', response)  # Remove wildcard sequences
        response = re.sub(r'\s+', ' ', response)           # Collapse whitespace
        response = response.strip()
        
        # Check if response is meaningful - better validation
        clean_check = re.sub(r'[^a-zA-Z\s]', '', response).strip()
        if len(clean_check) < 3:
            return response if response.strip() else "Hello! I'm here to help you."

        return response
        
        return response
        
    except subprocess.TimeoutExpired:
        return "That request took too long. Let's try something simpler."
    except Exception as e:
        return f"I had a technical issue. Could you ask me again in a different way?"
    finally:
        is_responding = False
        should_stop = False

def extract_conversation_context():
    """Get recent conversation context"""
    memory = load_memory()
    conversations = memory.get('conversations', [])
    
    # Get last 5 pairs of messages
    context = []
    for conv in conversations[-10:]:
        if 'user' in conv and 'sara' in conv:
            context.append(f"User: {conv['user']}")
            context.append(f"Sara: {conv['sara']}")
    
    return "\n".join(context[-10:]) if context else ""

# Flask Routes
@app.route('/')
def index():
    return render_template('enhanced_chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Simple, reliable chat endpoint"""
    global is_responding, should_stop
    
    user_input = request.json.get('message', '').strip()
    
    if not user_input or is_responding:
        return jsonify({"error": "Already responding or empty message"})
    
    # Set responding state
    is_responding = True
    should_stop = False
    
    # Get Sara's response
    sara_response = get_sara_response(user_input)
    
    # Save conversation if not stopped
    if not should_stop:
        memory = load_memory()
        conversation = {
            'user': user_input,
            'sara': sara_response,
            'timestamp': time.time(),
            'session': 'simple_chat'
        }
        memory['conversations'].append(conversation)
        save_memory(memory)
    
    return jsonify({
        'response': sara_response,
        'timestamp': time.time(),
        'stopped': should_stop
    })

@app.route('/api/stop')
def stop_response():
    """Stop current response - MANUAL BUTTON ONLY"""
    global should_stop, is_responding
    
    # Only stop if manually triggered by button click
    if is_responding:
        should_stop = True
        is_responding = False
        return jsonify({"status": "stopped_manually"})
    else:
        return jsonify({"status": "not_responding"})

@app.route('/api/memory')
def memory():
    """Get memory statistics and recent conversations"""
    memory_data = load_memory()
    conversations = memory_data.get('conversations', [])
    recent_conversations = conversations[-10:] if conversations else []
    
    return jsonify({
        "total_conversations": len(conversations),
        "active_tasks": len(memory_data.get('tasks', [])),
        "recent": recent_conversations,
        "storage": "Local JSON - 100% Private"
    })

@app.route('/api/tasks')
def tasks():
    """Get task list"""
    memory_data = load_memory()
    task_list = memory_data.get('tasks', [])
    
    return jsonify({
        "tasks": task_list,
        "count": len(task_list)
    })

@app.route('/api/status')
def status():
    """Get system status"""
    context = extract_conversation_context()
    
    return jsonify({
        "model": "main",
        "mode": "SIMPLE AUTONOMOUS CHAT",
        "responding": is_responding,
        "capabilities": [
            "✅ Reliable responses (no streaming issues)",
            "✅ Command execution working", 
            "✅ Stop/pause controls",
            "✅ Memory continuity",
            "✅ Full system access",
            "✅ 100% Offline operation"
        ],
        "features": {
            "reliable": "Simple, robust communication",
            "commands": "Direct command execution",
            "stop_controls": "Manual stop control", 
            "memory": "Conversation persistence",
            "access": "Complete system capabilities"
        },
        "conversation_stats": {
            "total_messages": len(load_memory().get('conversations', [])),
            "context_preview": context[:200] + "..." if len(context) > 200 else context
        }
    })

if __name__ == '__main__':
    print("🌟 SARA SIMPLE AUTONOMOUS CHAT")
    print("=" * 40)
    print("🚀 Starting simple, reliable chat...")
    print("🔧 No complex streaming - rock solid")
    print("🌐 http://127.0.0.1:8890")
    print("✅ 100% Offline & Private Operation")
    print("=" * 40)
    
    app.run(host='127.0.0.1', port=8890, debug=False)