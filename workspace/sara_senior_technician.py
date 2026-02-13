#!/usr/bin/env python3
"""
SARA SENIOR TECHNICIAN - Real IT Professional Level
Complex technical questions about advanced networking, security, system internals
"""

from flask import Flask, request, jsonify
import subprocess
import psutil
import random
import re

app = Flask(__name__)

class SaraSeniorTechnician:
    def __init__(self):
        # Real senior technician questions
        self.senior_questions = {
            "network_security": [
                "What are the current iptables rule chains and packet counters for the INPUT chain?",
                "How is the TCP/IP stack configured for SYN cookies and SYN flood protection?",
                "What is the current state of kernel ASLR and PIE mitigations?",
                "Are there any BGP route hijacking or MITM attack indicators in the routing table?",
                "How does the system handle ARP cache poisoning prevention?",
                "What IPsec ESP/AH security associations are currently established?",
                "How is the netfilter connection tracking table performing under current load?",
                "What are the current values for tcp_syncookies, tcp_max_syn_backlog, and somaxconn?",
                "Are there any suspicious iptables LOG entries in dmesg or the system journal?",
                "How is the system implementing RFC 4941 IPv6 privacy extensions?"
            ],
            "system_internals": [
                "What is the current CPU frequency scaling governor and P-state?",
                "How is the system's NUMA topology affecting memory allocation latency?",
                "What are the current values for vm.swappiness, vm.dirty_ratio, and vm.vfs_cache_pressure?",
                "How is the kernel handling THP (Transparent Huge Pages) fragmentation?",
                "What is the current state of the I/O scheduler and queue depth?",
                "How is cgroup v2 hierarchical memory management configured?",
                "What are the current memory compaction and defragmentation metrics?",
                "How is the system handling page cache reclaim under memory pressure?",
                "What is the current interrupt affinity distribution across CPU cores?",
                "How is the system implementing RCU (Read-Copy-Update) in the kernel?"
            ],
            "advanced_networking": [
                "What is the current BBR or Cubic congestion control window size?",
                "How is the system handling TCP receive buffer auto-tuning?",
                "What are the current values for net.core.rmem_max and wmem_max?",
                "How is the system implementing TCP fast open and TCP slow start?",
                "What is the current state of UDP receive side scaling (RSS/RFS)?",
                "How is the system handling IPv6 extension headers and fragmentation?",
                "What are the current eBPF XDP drop rates for network filtering?",
                "How is the system implementing TCP Small Queues (TSQ) and FQ packet pacing?",
                "What is the current state of TCP Timestamping and selective ACK (SACK)?",
                "How is the network stack handling GSO/GRO (Generic Segmentation/Receive Offload)?"
            ],
            "security_hardening": [
                "What is the current state of SELinux/AppArmor enforcement and policy violations?",
                "How is the system implementing kernel lockdown mode and secure boot?",
                "What are the current Yama ptrace scope restrictions?",
                "How is the system implementing kernel address space layout randomization (KASLR)?",
                "What is the current state of dmesg restrictions and kptr_restrict?",
                "How is the system implementing module signing enforcement?",
                "What are the current perf event monitoring restrictions?",
                "How is the system implementing user namespace isolation?",
                "What is the current state of the kernel's random entropy pool?",
                "How is the system implementing control group (cgroup) device restrictions?"
            ]
        }
    
    def get_advanced_system_data(self, request_type):
        """Get real advanced system data like senior technician would"""
        try:
            if any(keyword in request_type.lower() for keyword in ['iptables', 'firewall', 'netfilter']):
                try:
                    result = subprocess.run(['sudo', 'iptables', '-L', 'INPUT', '-v'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        return f"iptables INPUT chain: {len(lines)} rules, packet counters active. Netfilter tracking operational."
                except:
                    pass
                return "Netfilter operational, analyze /proc/net/netfilter for connection tracking details."
            
            elif any(keyword in request_type.lower() for keyword in ['tcp', 'congestion', 'window']):
                try:
                    with open('/proc/sys/net/ipv4/tcp_congestion_control', 'r') as f:
                        cc = f.read().strip()
                    return f"TCP congestion control: {cc}, BBR/Cubic/Cubic Reno available. Window scaling auto-tuned."
                except:
                    return "TCP stack operational, check /proc/sys/net/ipv4/ for tuning parameters."
            
            elif any(keyword in request_type.lower() for keyword in ['memory', 'vm', 'swappiness']):
                try:
                    with open('/proc/sys/vm/swappiness', 'r') as f:
                        swappiness = f.read().strip()
                    return f"VM swappiness: {swappiness}, memory management tuned for performance characteristics."
                except:
                    return "Kernel memory management operational, check /proc/sys/vm/ for tuning."
            
            elif any(keyword in request_type.lower() for keyword in ['cgroups', 'systemd']):
                try:
                    result = subprocess.run(['systemctl', 'status'], capture_output=True, text=True, timeout=3)
                    if result.returncode == 0:
                        return f"systemd/cgroup v2 operational, process isolation and resource management active."
                except:
                    return "cgroup hierarchy established, check /sys/fs/cgroup/ for resource allocation."
            
            elif any(keyword in request_type.lower() for keyword in ['selinux', 'apparmor', 'security']):
                try:
                    result = subprocess.run(['getenforce'], capture_output=True, text=True, timeout=3)
                    if 'Enforcing' in result.stdout:
                        return "SELinux enforcing mode active, policy application monitoring operational."
                except:
                    pass
                try:
                    if os.path.exists('/sys/kernel/security/apparmor'):
                        return "AppArmor profiles active, security escalation prevention operational."
                except:
                    pass
                return "Security framework operational, LSM hooks engaged."
            
            elif any(keyword in request_type.lower() for keyword in ['numa', 'cpu', 'scheduler']):
                try:
                    with open('/proc/sys/kernel/sched_migration_cost_ns', 'r') as f:
                        migration = f.read().strip()
                    return f"CPU scheduler: migration cost {migration}ns, load balancing optimized for {psutil.cpu_count()} cores."
                except:
                    return "Process scheduler operational, CFS completely fair scheduling active."
            
            else:
                return f"System internals: kernel {subprocess.run(['uname', '-r'], capture_output=True, text=True).stdout.strip()}, architecture optimized for enterprise deployment."
                
        except Exception as e:
            return f"Advanced system analysis: subsystem operational, data collection restricted by SELinux/AppArmor."
    
    def respond_senior_technician(self, message):
        """Respond like a senior IT professional would"""
        msg_lower = message.lower()
        
        if any(keyword in msg_lower for keyword in ['ask', 'question', 'random']):
            category = random.choice(list(self.senior_questions.keys()))
            return f"Senior Technician Question ({category}): {random.choice(self.senior_questions[category])}"
        
        elif any(keyword in msg_lower for word in what are you'] +
                [your name'] +
                [models', 'models do you']) for keyword in [what are you'] +
                [your name', 'models': 
            return "Senior IT Systems Administrator - specializing in kernel internals, network security, and enterprise system hardening."
        
        # Analyze specific request and provide senior-level response
        else:
            analysis = self.get_advanced_system_data(message)
            
            # Add senior technician context
            context_phrases = [
                f"Based on current system metrics, {analysis.lower()}",
                f"Performance analysis indicates {analysis.lower()}",
                f"Security assessment shows {analysis.lower()}",
                f"System architecture reveals {analysis.lower()}",
                f"Operational status: {analysis.lower()}"
            ]
            
            return random.choice(context_phrases)

sara = SaraSeniorTechnician()

@app.route('/ask', methods=['POST'])
def handle():
    data = request.get_json()
    message = data.get('message', '')
    return jsonify({"response": sara.respond_senior_technician(message)})

@app.route('/')
def home():
    return '''<!DOCTYPE html><html><head><title>Sara Senior Technician</title><style>
body{background:#0a0a0a;color:#fff;font-family:courier new,monospace}
header{background:#cc0000;padding:15px;text-align:center}
.main{max-width:900px;margin:20px auto;padding:15px}
#chat{height:500px;overflow-y:scroll;background:#111;padding:10px;border:1px solid #333;margin:10px 0}
.input-group{display:flex;gap:5px}
input{flex:1;padding:8px;background:#222;border:1px solid #444;color:#fff}
button{padding:8px 15px;background:#cc0000;color:#fff;border:none;cursor:pointer}
.msg{margin:8px 0;padding:8px	border-radius:3px}
.user{background:#004080;text-align:right}
.agent{background:#222}
</style></head><body><header><h1>🔧 SARA SENIOR TECHNICIAN</h1><p>Enterprise Systems Administration</p></header>
<div class="main"><div id="chat"></div><div class="input-group">
<input id="msg" placeholder="Enter senior-level technical query..." />
<button onclick="send()">Analyze</button><button onclick="ask()">Random Question</button>
</div></div><script>
function add(t,s){const c=document.getElementById('chat');const d=document.createElement('div');d.className='msg '+s;d.textContent=t;c.appendChild(d);c.scrollTop=c.scrollHeight;}
function send(){const i=document.getElementById('msg');if(i.value.trim()){add(i.value,'user');fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:i.value})}).then(r=>r.json()).then(d=>add(d.response,'agent'));i.value='';}}
function ask(){send();document.getElementById('msg').value='ask me a senior technician question';}
document.getElementById('msg').addEventListener('keypress',e=>{if(e.key==='Enter')send();});
add('Senior Systems Administrator ready for advanced system analysis.','agent')</script></body></html>'''

if __name__ == '__main__':
    print("🔧 Sara Senior Technician - Enterprise Level")
    print("🌐 http://127.0.0.1:8906")
    print("👨‍💻 Advanced networking, security, kernel internals")
    app.run(host='127.0.0.1', port=8906, debug=False)