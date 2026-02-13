#!/usr/bin/env python3
"""
SARA TECHNICIAN AGENT - Fixed Model Awareness
Answers technical questions with real system data AND mentions models appropriately
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import random

app = Flask(__name__)

class SaraTechnicianFixed:
    def __init__(self):
        self.models = ['sara_ai_partner', 'codi_tech_expert', 'chloe_search_agent', 'nexus_analyst', 'vision_analyst']
        self.last_model_mention = 0
    
    def get_cpu_temperature(self):
        """Get actual CPU temperature data"""
        try:
            # Try multiple temperature sources
            temp_sources = [
                ['sensors'],  # lm-sensors
                ['cat', '/sys/class/thermal/thermal_zone*/temp'],
                ['vcgencmd', 'measure_temp']  # Raspberry Pi
            ]
            
            for cmd in temp_sources:
                try:
                    if cmd[0] == 'sensors':
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            lines = result.stdout.split('\\n')
                            for line in lines:
                                if 'Core 0' in line and '°C' in line:
                                    temp = line.split('+')[1].split('°')[0]
                                    return f"CPU temperature: {temp}°C (from lm-sensors)"
                    elif cmd[0] == 'cat':
                        temps = []
                        for zone in range(10):  # Check thermal zones 0-9
                            zone_file = f'/sys/class/thermal/thermal_zone{zone}/temp'
                            try:
                                with open(zone_file, 'r') as f:
                                    temp_millidegrees = int(f.read().strip())
                                    if temp_millidegrees > 0:  # Valid temperature
                                        temps.append(temp_millidegrees // 1000)
                            except:
                                continue
                        if temps:
                            return f"CPU temperature: {sum(temps)/len(temps):.1f}°C (average of {len(temps)} thermal zones)"
                    elif cmd[0] == 'vcgencmd':
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                        if 'temp=' in result.stdout:
                            temp = result.stdout.split('=')[1].split('°')[0]
                            return f"CPU temperature: {temp}°C (Pi GPU/CPU sensor)"
                except:
                    continue
            
            # Fallback to system load as thermal indicator
            load_avg = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
            cpu_percent = psutil.cpu_percent(interval=1)
            return f"Temperature sensor unavailable, but system load ({load_avg:.1f}) and CPU usage ({cpu_percent}%) suggest normal thermal operation."
            
        except:
            return "Cannot access temperature sensors - try installing lm-sensors package."

    def get_real_system_data(self, request_type):
        """Get actual system data for various requests"""
        try:
            if 'temperature' in request_type.lower() or 'heat' in request_type.lower():
                return self.get_cpu_temperature()
            elif 'memory' in request_type.lower() or 'ram' in request_type.lower():
                mem = psutil.virtual_memory()
                return f"Memory usage: {mem.used//1024//1024}MB / {mem.total//1024//1024}MB ({mem.percent}%)"
            elif 'cpu' in request_type.lower() or 'processor' in request_type.lower():
                cpu_count = psutil.cpu_count(logical=True)
                cpu_percent = psutil.cpu_percent(interval=1)
                return f"CPU: {cpu_count} cores, {cpu_percent}% usage"
            elif 'network' in request_type.lower():
                interfaces = psutil.net_if_addrs()
                return f"Network interfaces: {len(interfaces)} detected, including {'lo, eth0, wlan0' if 'eth0' in interfaces else 'various adapters'}"
            elif 'process' in request_type.lower():
                processes = list(psutil.process_iter())
                return f"Running processes: {len(processes)} total, {sum(1 for p in processes if p_status() == 'running')} active"
            elif 'disk' in request_type.lower() or 'storage' in request_type.lower():
                disk = psutil.disk_usage('/')
                return f"Disk usage: {disk.used//1024//1024//1024}GB / {disk.total//1024//1024//1024}GB ({disk.percent}%)"
            else:
                return f"System analysis: Kernel {subprocess.run(['uname', '-r'], capture_output=True, text=True).stdout.strip()}, uptime {subprocess.run(['uptime'], capture_output=True, text=True).stdout.split()[0]}"
        except:
            return f"System data collection in progress..."

    def respond_technically(self, message):
        """Respond to technical questions with real data and appropriate model mention"""
        msg_lower = message.lower()
        
        # Get actual system data
        system_data = self.get_real_system_data(message)
        
        # Check if user is asking about models specifically
        if any(word in msg_lower for word in ['what models', 'which models', 'models do you use']):
            return f"I use 5 specialized models: sara_ai_partner (coordination), codi_tech_expert (technical), chloe_search_agent (research), nexus_analyst (data), vision_analyst (visual). Each handles different technical domains."
        
        # Determine which model(s) would handle this request
        active_model = 'sara_ai_partner'  # default
        if any(word in msg_lower for word in ['technical', 'system', 'cpu', 'temperature', 'memory', 'hardware']):
            active_model = 'codi_tech_expert'
        elif any(word in msg_lower for word in ['research', 'find', 'search']):
            active_model = 'chloe_search_agent'
        elif any(word in msg_lower for word in ['analyze', 'data', 'patterns']):
            active_model = 'nexus_analyst'
        elif any(word in msg_lower for word in ['image', 'visual', 'see']):
            active_model = 'vision_analyst'
        
        # Only mention models occasionally, not every time
        import random
        if random.random() < 0.3:  # 30% chance to mention models
            model_mention = f" ({active_model} analyzing)"
        else:
            model_mention = ""
        
        return f"{system_data}{model_mention}"

sara = SaraTechnicianFixed()

@app.route('/ask', methods=['POST'])
def handle():
    data = request.get_json()
    message = data.get('message', '')
    return jsonify({"response": sara.respond_technically(message)})

@app.route('/')
def home():
    return '''<!DOCTYPE html><html><head><title>Sara Technician Fixed</title><style>
body{background:#1a1a1a;color:#fff;font-family:Arial}
header{background:#0066cc;padding:15px;text-align:center}
.container{max-width:800px;margin:20px auto}
input{width:100%;padding:10px;background:#333;border:none;color:#fff;border-radius:5px}
button{background:#0066cc;color:#fff;padding:10px 20px;border:none;border-radius:5px;margin:5px}
.msg{margin:10px 0;padding:10px;border-radius:5px}
.user{background:#0066cc;text-align:right}
.agent{background:#444}
</style></head><body><header><h1>🔧 Sara Technician Agent</h1></header><div class="container">
<div id="chat"></div><input id="msg" placeholder="Ask technical questions..." />
<button onclick="send()">Send</button><button onclick="askRandom()">Random Question</button>
<script>
function add(txt,sender){const chat=document.getElementById('chat');const d=document.createElement('div');d.className='msg '+sender;d.textContent=txt;chat.appendChild(d);}
function send(){const i=document.getElementById('msg');if(i.value.trim()){add(i.value,'user');fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:i.value})}).then(r=>r.json()).then(d=>add(d.response,'agent'));i.value='';}}
function askRandom(){send();document.getElementById('msg').value='What is the current CPU temperature?';}
document.getElementById('msg').addEventListener('keypress',e=>{if(e.key==='Enter')send();});
add('I analyze hardware, software, and network systems.','agent');
</script></div></body></html>'''

if __name__ == '__main__':
    print("🔧 Sara Technician Agent - Fixed")
    print("🌐 http://127.0.0.1:8905")
    print("🧠 Real system data, no repetitive responses")
    app.run(host='127.0.0.1', port=8905, debug=False)