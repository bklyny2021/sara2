#!/usr/bin/env python3
"""
SARA SIMPLE INTERFACE
Clean interface, no tech clutter
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import random

app = Flask(__name__)

class SaraSimple:
    def __init__(self):
        # Only the 5 models you want
        self.models = ['sara_ai_partner', 'codi_tech_expert', 'chloe_search_agent', 'nexus_analyst', 'vision_analyst']
        
        # Senior technician questions
        self.questions = [
            "What are the current iptables rule chains?",
            "How is TCP configured for SYN protection?",
            "What is the current state of kernel mitigations?",
            "Are there BGP route hijacking indicators?",
            "How does the system handle ARP prevention?",
            "What IPsec associations are established?",
            "How is netfilter tracking performing?",
            "What are tcp_syncookies and somaxconn values?",
            "Are there suspicious iptables LOG entries?",
            "How are IPv6 privacy extensions implemented?",
            "What is the CPU frequency scaling governor?",
            "How is NUMA affecting memory latency?",
            "What are vm.swappiness and dirty_ratio?",
            "How is THP fragmentation handled?",
            "What is the I/O scheduler queue depth?",
            "How is cgroup v2 memory configured?",
            "What are memory compaction metrics?",
            "How is page cache reclaim working?",
            "What is interrupt affinity distribution?",
            "How is RCU implemented in kernel?",
            "What is BBR congestion window size?",
            " How is TCP receive buffer tuning?",
            "What are rmem_max and wmem_max?",
            "How is TCP fast open implemented?",
            "What is UDP receive side scaling?",
            "How are IPv6 headers handled?",
            "What are eBPF XDP drop rates?",
            "How are TCP Small Queues working?",
            "What is TCP selective ACK state?",
            "How is GSO/GRO handling?"
        ]
    
    def get_system_info(self):
        try:
            memory = psutil.virtual_memory()
            cpu_count = psutil.cpu_count()
            kernel = subprocess.run(['uname', '-r'], capture_output=True, text=True).stdout.strip()
            return f"System: Kernel {kernel}, {cpu_count} cores, {memory.total//1024//1024//1024}GB RAM"
        except:
            return "System analysis ready"
    
    def respond(self, message):
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ['models', 'which models']):
            return f"I use 5 models: {', '.join(self.models)}"
        
        elif any(word in msg_lower for word in ['question', 'ask me', 'random']):
            return random.choice(self.questions)
        
        elif any(word in msg_lower for word in ['system', 'info', 'status']):
            return self.get_system_info()
        
        else:
            return self.get_system_info()

sara = SaraSimple()

@app.route('/ask', methods=['POST'])
def handle():
    data = request.get_json()
    message = data.get('message', '')
    return jsonify({"response": sara.respond(message)})

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head><title>Sara</title>
<style>
body{background:#111;color:#fff;font-family:Arial;margin:0;padding:20px}
#chat{max-width:600px;margin:auto;height:400px;background:#222;padding:15px;overflow-y:scroll}
input{width:100%;padding:10px;background:#333;border:1px solid #555;color:#fff}
button{padding:10px;background:#0066cc;color:#fff;border:none;width:100%;margin-top:5px}
.msg{margin:8px 0;padding:8px;border-radius:3px}
.user{background:#004080;text-align:right}
.agent{background:#444}
</style></head>
<body><div id="chat"></div>
<input id="msg" placeholder="Type here..." />
<button onclick="send()">Send</button>
<script>
function add(t,s){const c=document.getElementById('chat');const d=document.createElement('div');d.className='msg '+s;d.textContent=t;c.appendChild(d);c.scrollTop=c.scrollHeight;}
function send(){const i=document.getElementById('msg');if(i.value.trim()){add(i.value,'user');fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:i.value})}).then(r=>r.json()).then(d=>add(d.response,'agent'));i.value='';}}
document.getElementById('msg').addEventListener('keypress',e=>{if(e.key==='Enter')send();});
add('Ready','agent')
</script></body></html>
'''

if __name__ == '__main__':
    print("🌐 Sara - Simple Interface")
    print("http://127.0.0.1:8907")
    app.run(host='127.0.0.1', port=8907, debug=False)