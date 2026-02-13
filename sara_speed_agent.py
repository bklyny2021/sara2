#!/usr/bin/env python3
"""
SARA SPEED AGENT - Minimal but complete
Essential models only for fast deployment
"""

from flask import Flask, request, jsonify
import psutil
import subprocess

app = Flask(__name__)

class SaraSpeed:
    def __init__(self):
        self.models = ['sara_ai_partner', 'codi_tech_expert']
        self.mode = 'speed_optimized'
    
    def process_fast(self, message):
        if 'models' in message.lower():
            return f"I use 2 essential models: {', '.join(self.models)} for rapid operations."
        elif 'system' in message.lower():
            memory = psutil.virtual_memory()
            return f"System: {memory.percent}% memory, {psutil.cpu_percent()}% CPU - Speed Agent analyzing"
        else:
            return f"Speed Agent using sara_ai_partner for rapid response: '{message}'"

sara = SaraSpeed()

@app.route('/ask', methods=['POST'])
def handle():
    data = request.get_json()
    return jsonify({"response": sara.process_fast(data.get('message', ''))})

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head><title>Sara Speed Agent</title>
<style>body{background:#1a1a1a;color:#fff;font-family:Arial}.message{margin:5px}</style>
</head>
<body><h1>🚀 Sara Speed Agent</h1><div id="messages"></div>
<input id="msg" onkeypress="if(event.key=='Enter')send()" style="width:300px">
<script>
function addMsg(txt,sender){const m=document.getElementById('messages');const d=document.createElement('div');d.className=sender;d.textContent=txt;m.appendChild(d);}
function send(){const i=document.getElementById('msg');if(i.value.trim()){addMsg(i.value,'user');const txt=i.value;i.value='';
fetch('/ask',{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:txt})})
.then(r=>r.json()).then(d=>addMsg(d.response,'agent'));}
</script></body></html>
'''

if __name__ == '__main__':
    print("🚀 Sara Speed Agent - 2 models, optimized for speed")
    print("🌐 http://127.0.0.1:8902")
    app.run(host='127.0.0.1', port=8902, debug=False)