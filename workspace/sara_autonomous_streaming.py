#!/usr/bin/env python3
# 🌟 SARA AUTONOMOUS CHAT V2
# Full streaming responses, background thinking, stop controls

from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import json
import time
import os
from pathlib import Path
import threading
import queue
import sys
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration
WORKSPACE_PATH = Path.home() / ".openclaw" / "workspace"
MEMORY_FILE = WORKSPACE_PATH / "simple_memory" / "sara_memory.json"
MEMORY_FILE.parent.mkdir(exist_ok=True)

# Global state for streaming
current_stream = None
stream_queue = queue.Queue()
should_stop = False
background_thinking = False
completion_timer = None

class SaraAutonomousChat:
    def __init__(self):
        self.model = "sara-boo1-fixed"
        self.max_tokens = 2000
        self.temperature = 1.8
        self.active_response = None
        self.response_complete = False
        self.completion_thinking = False
        self.accumulated_response = ""
        self.background_context = {}
        
    def create_streaming_command(self, message, conversation_context):
        """Create command with streaming context"""
        context_lines = []
        self.active_response = None
        self.response_complete = False
        self.accumulated_response = ""
        
        # Add conversation context
        if conversation_context:
            context_lines.append("Recent conversation context:")
            for i, (msg_type, content) in enumerate(conversation_context[-5:]):
                role = "Boo" if msg_type == "user" else "Sara"
                context_lines.append(f"{role}: {content}")
            context_lines.append("")
        
        # Add autonomous instructions
        context_lines.extend([
            "RESPONSE STYLE RULES:",
            "- Respond naturally and conversationally",
            "- Think through your answers completely",
            "- Show your reasoning process step by step",
            "- Use your full capabilities and skills",
            "- NEVER end with questions about what to do next",
            "- Complete your thoughts fully",
            "- Be autonomous: think AND respond completely",
            "- Break down complex topics step by step",
            "- When you think you're done, pause and reconsider if more value can be added",
            "- Continue thinking in the background after main response",
            "",
            f"Task: {message}",
            "",
            "Begin autonomous response now:"
        ])
        
        context_prompt = "\n".join(context_lines)
        
        return [
            "ollama", "run", "sara-exec",
            "--format", "json", 
            "--temperature", str(self.temperature),
            "--num-predict", str(self.max_tokens),
            context_prompt
        ]
    
    def stream_response(self, command, should_continue_streaming):
        """Stream response while monitoring for stop requests"""
        global should_stop, stream_queue
        
        try:
            # Start the process
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            buffer = ""
            thinking_buffer = ""
            in_thinking = False
            
            output_line = process.stdout.readline()
            while output_line and not should_stop:
                buffer += output_line
                
                # Check for thinking indicators
                if "Let me think through this" in buffer or "Actually" in buffer or "Wait" in buffer:
                    if not in_thinking:
                        stream_queue.put({"type": "thinking_start"})
                        in_thinking = True
                    thinking_buffer += output_line
                elif in_thinking:
                    stream_queue.put({"type": "thinking_end", "content": thinking_buffer.strip()})
                    in_thinking = False
                    thinking_buffer = ""
                
                # Send text chunks for display
                if not should_stop:
                    stream_queue.put({
                        "type": "text_chunk",
                        "content": output_line,
                        "is_thinking": in_thinking
                    })
                
                # Check if response is complete
                if len(buffer) > 1000 and any(end_marker in buffer.lower() for end_marker in [".", "!", "?"]):
                    has_final_punctuation = buffer.strip().endswith(('.', '!', '?'))
                    if has_final_punctuation and not self.completion_thinking:
                        self.response_complete = True
                        self.accumulated_response = buffer.strip()
                        stream_queue.put({"type": "response_complete", "content": buffer.strip()})
                
                output_line = process.stdout.readline()
                
                # Brief pause for natural conversation flow
                time.sleep(0.03)
            
            # Process cleanup
            process.terminate()
            
            # Final response accumulation
            if buffer.strip() and not should_stop:
                return buffer.strip()
                
        except Exception as e:
            if not should_stop:
                stream_queue.put({"type": "error", "content": str(e)})
            return None
    
    def initiate_completion_thinking(self, current_response):
        """Start background thinking to augment response"""
        global completion_timer
        
        if self.response_complete and not self.completion_thinking:
            self.completion_thinking = True
            completion_timer = threading.Timer(10.0, self.complete_thinking_check)
            completion_timer.start()
            stream_queue.put({"type": "completion_thinking_start"})
    
    def complete_thinking_check(self):
        """Check if Sara needs to add more to her response"""
        global stream_queue
        
        if self.response_complete and self.accumulated_response:
            # Sara autonomously decides if she needs to add more
            completion_check = f"""
Original response: {self.accumulated_response}

Should I add more details or clarify anything? Consider if important points were missed or if I should expand on my reasoning. 
Think autonomously and respond accordingly."""
            
            try:
                # Autonomous completion thinking
                completion_command = [
                    "ollama", "run", "sara-exec",
                    "--temperature", "1.2",
                    completion_check
                ]
                
                completion_process = subprocess.run(
                    completion_command,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if completion_process.stdout.strip() and "yes" in completion_process.stdout.lower():
                    stream_queue.put({"type": "completion_thinking", "content": completion_process.stdout.strip()})
                
            except Exception as e:
                print(f"Completion thinking error: {e}")
            
            self.completion_thinking = False

# Global Sara instance
sara_chat = SaraAutonomousChat()

def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"conversations": [], "preferences": {}, "tasks": [], "context": {}}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def extract_conversation_context():
    """Extract recent conversation for Sara's context"""
    memory = load_memory()
    conversations = memory.get('conversations', [])
    context = []
    
    for conv in conversations[-8:]:  # Last 8 messages for context
        if 'user' in conv and 'sara' in conv:
            context.append(('user', conv['user']))
            context.append(('sara', conv['sara']))
    
    return context

# Flask Routes

@app.route('/')
def index():
    return render_template('autonomous_chat.html')

@app.route('/api/chat_stream', methods=['POST'])
def chat_stream():
    """Handle streaming chat with autonomous Sara"""
    global current_stream, should_stop, stream_queue
    
    user_input = request.json.get('message', '').strip()
    
    # Reset stream state
    should_stop = False
    stream_queue = queue.Queue()
    current_stream = threading.current_thread()
    
    # Get conversation context
    conversation_context = extract_conversation_context()
    
    # Create streaming command in background
    def run_sara_stream():
        global should_stop
        
        # Build streaming command
        command = sara_chat.create_streaming_command(user_input, conversation_context)
        
        # Start streaming
        result = sara_chat.stream_response(command, lambda: not should_stop)
        
        # If not stopped, save conversation
        if not should_stop and result:
            memory = load_memory()
            conversation = {
                'user': user_input,
                'sara': '',
                'timestamp': time.time(),
                'session': 'autonomous_chat'
            }
            memory['conversations'].append(conversation)
            save_memory(memory)
    
    # Start streaming in background thread
    stream_thread = threading.Thread(target=run_sara_stream)
    stream_thread.daemon = True
    stream_thread.start()
    
    return jsonify({"status": "streaming_started"})

@app.route('/api/chat/stream')
def stream_endpoint():
    """Server-Sent Events for streaming responses"""
    def generate():
        global stream_queue, should_stop
        
        while True:
            try:
                # Get message from queue (with timeout)
                try:
                    message = stream_queue.get(timeout=0.5)
                    yield f"data: {json.dumps(message)}\n\n"
                    
                    if message.get("type") == "response_complete":
                        # Start completion thinking
                        sara_chat.initiate_completion_thinking(message.get("content", ""))
                        
                except queue.Empty:
                    # Send keepalive if still streaming
                    if current_stream and current_stream.is_alive():
                        yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
                    else:
                        break
                        
                # Check if should stop
                if should_stop:
                    yield f"data: {json.dumps({'type': 'stopped'})}\n\n"
                    break
                    
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
                break
    
    return app.response_class(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
        }
    )

@app.route('/api/stop_response')
def stop_response():
    """Stop current Sara response"""
    global should_stop
    should_stop = True
    return jsonify({"status": "stop_initiated"})

@app.route('/api/status')
def status():
    """Get system status"""
    return jsonify({
        "model": "sara-boo1-fixed",
        "mode": "AUTONOMOUS STREAMING",
        "capabilities": [
            "✅ Full streaming responses",
            "✅ Background thinking",
            "✅ Autonomous completion",
            "✅ Stop/pause controls",
            "✅ Context awareness",
            "✅ 100% Offline operation"
        ],
        "features": {
            "streaming": "Real-time response streaming",
            "stop_controls": "Interrupt Sara anytime",
            "background_thinking": "Continues thinking after response",
            "autonomous_completion": "Self-ensures complete answers",
            "context_awareness": "Remembers conversation flow",
            "full_access": "Complete system capabilities"
        }
    })

if __name__ == '__main__':
    print("🌟 SARA AUTONOMOUS CHAT V2")
    print("=" * 50)
    print("🚀 Starting autonomous streaming chat...")
    print("🌐 Opening http://127.0.0.1:8889")
    print("🤖 Sara with full streaming and stop controls")
    print("🧠 Background thinking capabilities")
    print("✅ 100% Offline & Private Operation")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=8889, debug=False)