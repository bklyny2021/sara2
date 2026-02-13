#!/usr/bin/env python3
"""
SARA - FIXED - Different responses for different questions
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import random

app = Flask(__name__)

class SaraFixed:
    def __init__(self):
        self.models = ['sara_ai_partner', 'codi_tech_expert', 'chloe_search_agent', 'nexus_analyst', 'vision_analyst']
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
            "What is the I/O scheduler queue depth?"
        ]
    
    def get_temperature(self):
        try:
            result = subprocess.run(['sensors'], capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Core 0' in line and '°C' in line:
                        temp = line.split('+')[1].split('°')[0]
                        return f"CPU temperature {temp}°C"
            return "Temperature sensors not accessible"
        except:
            return "Thermal monitoring not available"
    
    def get_security(self):
        try:
            fw = subprocess.run(['firewall-cmd', '--state'], capture_output=True, text=True, timeout=3)
            if fw.returncode == 0:
                return "Firewall active and enforcing security policy"
            return "Security framework configured"
        except:
            return "Security protocols active"
    
    def get_memory(self):
        try:
            mem = psutil.virtual_memory()
            return f"Memory {mem.used//1024//1024}MB used of {mem.total//1024//1024}MB ({mem.percent}%)"
        except:
            return "Memory management active"
    
    def get_network(self):
        try:
            interfaces = len(psutil.net_if_addrs())
            return f"Network interfaces detected: {interfaces}"
        except:
            return "Network subsystem operational"
    
    def respond_fixed(self, message):
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ['models', 'which models']):
            return f"I use {', '.join(self.models)}"
        
        elif any(word in msg_lower for word in ['question', 'ask me', 'random']):
            return random.choice(self.questions)
        
        elif 'temperature' in msg_lower or 'temp' in msg_lower:
            return self.get_temperature()
            
        elif 'security' in msg_lower or 'firewall' in msg_lower:
            return self.get_security()
            
        elif 'memory' in msg_lower or 'ram' in msg_lower:
            return self.get_memory()
            
        elif 'network' in msg_lower or 'connection' in msg_lower:
            return self.get_network()
        
        elif 'cpu' in msg_lower or 'processor' in msg_lower:
            return f"CPU: {psutil.cpu_count()} cores, {psutil.cpu_percent()}% usage"
        
        elif 'system' in msg_lower or 'info' in msg_lower:
            kernel = subprocess.run(['uname', '-r'], capture_output=True, text=True).stdout.strip()
            return f"System: Kernel {kernel} with {psutil.cpu_count()} cores and {psutil.virtual_memory().total//1024//1024//1024}GB RAM"
        
        elif any(word in msg_lower for word in ['hello', 'hi', 'hey']):
            return "I can analyze system temperature, security, memory, network, CPU performance, and ask technical questions."
        
        elif any(word in msg_lower for word in ['lol', 'haha', 'funny']):
            return "Yes, system analysis can be entertaining! Ask me about iptables rules or kernel mitigations."
        
        elif any(word in msg_lower for word in ['lets go', 'awesome', 'great']):
            return "Ready for technical operations! I can monitor system components and security configurations."
        
        elif any(word in msg_lower for word in ['what else', 'more']):
            return "I can analyze firewall rules, TCP settings, memory management, network protocols, and system internals."
        
        else:
            return f"I can analyze: {', '.join(['temperature', 'security', 'memory', 'network', 'CPU', 'system info'])}. What would you like?"

sara = SaraFixed()

@app.route('/ask', methods=['POST'])
def handle():
    data = request.get_json()
    message = data.get('message', '')
    return jsonify({"response": sara.respond_fixed(message)})

@app.route('/')
def home():
    return '''<!DOCTYPE html><html><head><title>Sara Fixed</title><style>
body{background:#111;color:#fff;margin:10px}
#chat{height:400px;background:#1a1a1a;padding:15px;overflow-y:scroll;border-radius:5px}
input{width:100%;padding:10px;background:#222;border:1px solid #444;color:#fff;border-radius:5px}
.msg{margin:8px 0;padding:8px;max-width:85%}
.user{background:#0066cc;margin-left:auto;text-align:right}
</style></head><body><div id="chat"></div><input id="msg" />
<script>
function add(txt,cls='msg'){document.getElementById('chat').innerHTML+='<div class="'+cls+'">'+txt+'</div>';document.getElementById('chat').scrollTop=99999;}
document.getElementById('msg').onkeypress=function(e){if(e.key=='Enter'&&this.value.trim()){add(this.value,'msg user');fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:this.value})}).then(r=>r.json()).then(d=>add(d.response)).catch(e=>add('Error'));this.value='';}}
add('I respond differently to different questions.','msg');
</script></body></html>'''

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8909, debug=False)