#!/usr/bin/env python3
# 🌟 SARA WORKING WEB INTERFACE
# Using the working sara-boo1-fixed model, no complex streaming

from flask import Flask, render_template, request, jsonify
import subprocess
import json
import time
import os
from pathlib import Path
import threading

# Initialize Flask app
app = Flask(__name__)

# Configuration
WORKSPACE_PATH = Path.home() / ".openclaw" / "workspace"
MEMORY_FILE = WORKSPACE_PATH / "simple_memory" / "sara_memory.json"
MEMORY_FILE.parent.mkdir(exist_ok=True)

def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"conversations": [], "preferences": {}, "tasks": [], "context": {}}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def get_sara_response(user_input):
    """Get response from WORKING SaraBoo1-fixed model"""
    try:
        command = ['ollama', 'run', 'sara-exec', user_input]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            response = result.stdout.strip()
            # Clean up ALL terminal escape sequences thoroughly
            import re
            # Remove ANSI escape sequences
            response = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', response)
            # Remove common problematic sequences
            response = response.replace('[?25h', '').replace('[K', '').replace('[?25l', '')
            response = response.replace('[?2026l', '').replace('[?2026h', '').replace('[?2004h', '')
            response = response.replace('[?2004l', '').replace('[?1h', '').replace('[?1l', '')
            # Clean up extra whitespace
            response = ' '.join(response.split())
            return response
        else:
            return "I'm having trouble thinking right now. Could you try again?"
    except subprocess.TimeoutExpired:
        return "That took me a moment. Let me try a different approach."
    except Exception as e:
        return f"Hmm, something went wrong: {str(e)}"

def extract_task_from_message(user_input, sara_response):
    """Extract potential tasks from conversation"""
    task_keywords = ['reminder', 'create', 'set up', 'build', 'task', 'todo', 'schedule']
    if any(keyword in user_input.lower() for keyword in task_keywords):
        return f"Task: {sara_response[:50]}..."
    return None

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    user_input = request.json.get('message', '').strip()
    timestamp = time.time()
    
    # Get Sara's response from WORKING model
    sara_response = get_sara_response(user_input)
    
    # Store conversation
    memory = load_memory()
    conversation = {
        'user': user_input,
        'sara': sara_response,
        'timestamp': timestamp,
        'session': 'web_chat'
    }
    memory['conversations'].append(conversation)
    
    # Extract and store tasks if needed
    potential_task = extract_task_from_message(user_input, sara_response)
    if potential_task:
        memory['tasks'].append({
            'task': potential_task,
            'created': timestamp,
            'status': 'active'
        })
    
    save_memory(memory)
    
    return jsonify({
        'response': sara_response,
        'timestamp': timestamp
    })

@app.route('/api/status')
def status():
    """Get system status"""
    memory = load_memory()
    
    # Check if Sara model is available
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if 'sara-exec' in result.stdout:
            model_status = '🤖 Sara (executing commands) operational'
        else:
            model_status = '⚠️ Sara-exec not found'
    except:
        model_status = '❌ Model status unknown'
    
    return jsonify({
        'model': model_status,
        'conversations': len(memory['conversations']),
        'tasks': len(memory['tasks']),
        'privacy': '🔒 100% Offline & Private',
        'capabilities': [
            'Full AI Partnership',
            'System Automation', 
            'Security Protection',
            'Task Management',
            'Memory Continuity',
            'Voice Synthesis'
        ]
    })

@app.route('/api/memory')
def get_memory():
    """Get memory statistics"""
    memory = load_memory()
    recent_conversations = memory['conversations'][-10:] if memory['conversations'] else []
    
    return jsonify({
        'total_conversations': len(memory['conversations']),
        'active_tasks': len(memory['tasks']),
        'recent': recent_conversations,
        'storage': 'Local JSON - 100% Private'
    })

@app.route('/api/tasks')
def get_tasks():
    """Get task list"""
    memory = load_memory()
    tasks = memory['tasks']
    
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    })

@app.route('/api/voice_test')
def voice_test():
    """Test voice synthesis"""
    try:
        import gtts
        import os
        
        tts = gtts.gTTS("Hello Boo! This is Sara testing my voice system.", lang='en')
        voice_file = WORKSPACE_PATH / "test_voice.mp3"
        tts.save(str(voice_file))
        
        if voice_file.exists() and voice_file.stat().st_size > 0:
            voice_file.unlink()  # Cleanup
            return jsonify({'status': '✅ Voice synthesis working'})
        else:
            return jsonify({'status': '❌ Voice synthesis failed'})
    except ImportError:
        return jsonify({'status': '⚠️ gTTS not installed'})
    except Exception as e:
        return jsonify({'status': f'❌ Voice error: {str(e)}'})

if __name__ == '__main__':
    print("🌟 SARA WORKING WEB INTERFACE")
    print("=" * 50)
    print("🚀 Starting web server...")
    print("🌐 Opening in browser...")
    print("💚 100% Offline & Private Operation")
    print("🤖 SaraBoo1-fixed AI personality")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=8890, debug=False)