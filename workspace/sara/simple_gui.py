#!/usr/bin/env python3
# 🖥️ Enhanced Dark Theme Command Center GUI

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import json
import threading
import time
import subprocess
from datetime import datetime
import os
import requests
import hashlib
import fitz  # PyMuPDF for PDF processing
import re
from pathlib import Path

class VoiceCommandCenterGUI:
    """Enhanced Command Center with RAG Memory System"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎤 Sara AI Team Command Center")
        self.root.geometry("1200x800")
        
        # RAG Memory System Setup
        self.rag_memory = {}
        self.memory_file = "/home/godfather/Desktop/sara/RAG_MEMORY.md"
        self.knowledge_base = "/home/godfather/Desktop/sara/knowledge/"
        self.vector_store = {}  # Simple in-memory vector store
        self.processed_files = set()  # Track processed files
        
        # Initialize knowledge directories
        os.makedirs(self.knowledge_base, exist_ok=True)
        os.makedirs(f"{self.knowledge_base}documents/", exist_ok=True)
        os.makedirs(f"{self.knowledge_base}transcripts/", exist_ok=True)
        os.makedirs(f"{self.knowledge_base}pdfs/", exist_ok=True)
        
        # Load existing memory
        self.load_rag_memory()
        
        # Scan for new files and process
        self.scan_and_process_files()
        
        # Dark theme colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#00ff88',
            'warning': '#ff6b6b',
            'info': '#4ecdc4',
            'button': '#2d3748',
            'button_hover': '#4a5568',
            'border': '#374151'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Setup fonts
        self.setup_fonts()
        self.setup_ui()
        self.start_monitoring()
        
    def setup_fonts(self):
        """Setup fonts for the GUI"""
        self.title_font = font.Font(family="Courier", size=14, weight="bold")
        self.label_font = font.Font(family="Courier", size=12)
        self.button_font = font.Font(family="Courier", size=10)
        self.log_font = font.Font(family="Courier", size=9)
        
    def setup_ui(self):
        """Setup the main UI"""
        # Title
        title = tk.Label(self.root, text="🎤 SARA VOICE COMMAND CENTER",
                        font=self.title_font, bg=self.colors['bg'], fg=self.colors['accent'])
        title.pack(pady=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Top section - Status panels
        self.create_status_panels(main_container)
        
        # Middle section - Controls
        self.create_control_panel(main_container)
        
        # Bottom section - Logs
        self.create_log_panel(main_container)
    
    def create_status_panels(self, parent):
        """Create agent status display panels"""
        # Status container
        status_container = tk.Frame(parent, bg=self.colors['bg'])
        status_container.pack(fill=tk.X, pady=(0, 10))
        
        # Agent Status Monitor
        agent_frame = tk.LabelFrame(status_container, text="🤖 Team Status",
                                   bg=self.colors['bg'], fg=self.colors['accent'],
                                   font=self.label_font)
        agent_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.agent_labels = {}
        agents = [
            ("Sara", "🤖 Team Coordinator"),
            ("Chloe", "🔍 Research Expert"), 
            ("Nexus", "📊 Analysis Pro"),
            ("Codi", "💻 Tech Support"),
            ("Vision", "👁️ Visual Data")
        ]
        
        for agent_name, description in agents:
            # Create display frame for each agent
            frame = tk.Frame(agent_frame, bg=self.colors['bg'])
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Agent name and description
            text_frame = tk.Frame(frame, bg=self.colors['bg'])
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            name_label = tk.Label(text_frame, text=f"{agent_name}: {description}",
                                bg=self.colors['bg'], fg=self.colors['fg'], 
                                font=self.label_font, anchor='w')
            name_label.pack(side=tk.LEFT)
            
            # Status indicator
            status_indicator = tk.Label(frame, text="○", fg=self.colors['warning'], 
                                      bg=self.colors['bg'], font=("Courier", 12))
            status_indicator.pack(side=tk.RIGHT, padx=5)
            self.agent_labels[agent_name] = status_indicator
        
        # System Status
        system_frame = tk.LabelFrame(status_container, text="📊 System Status",
                                    bg=self.colors['bg'], fg=self.colors['accent'],
                                    font=self.label_font)
        system_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.system_labels = {}
        metrics = ["CPU", "RAM", "Disk", "Ollama"]
        values = ["0%", "0%", "0%", "Offline"]
        
        for i, (metric, value) in enumerate(zip(metrics, values)):
            frame = tk.Frame(system_frame, bg=self.colors['bg'])
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(frame, text=f"{metric}:", anchor='w', width=8,
                    bg=self.colors['bg'], fg=self.colors['fg'], font=self.label_font).pack(side=tk.LEFT)
            label = tk.Label(frame, text=value, anchor='w',
                          bg=self.colors['bg'], fg=self.colors['info'], 
                          font=self.label_font)
            label.pack(side=tk.LEFT, padx=5)
            self.system_labels[metric] = label
    
    def create_control_panel(self, parent):
        """Create Sara-as-dispatcher control panel"""
        control_frame = tk.LabelFrame(parent, text="🎛️ Talk to Sara (She'll route to best agent)",
                                     bg=self.colors['bg'], fg=self.colors['accent'],
                                     font=self.label_font)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Quick action buttons
        button_container = tk.Frame(control_frame, bg=self.colors['bg'])
        button_container.pack(pady=10)
        
        buttons = [
            ("🤖 Sara Coordination", self.focus_sara, self.colors['accent']),
            ("📢 Team Conference", self.team_chat, self.colors['info']),
            ("📊 Team Health Check", self.test_all_agents, self.colors['fg'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_container, text=text, command=command,
                          bg=self.colors['button'], fg=color,
                          activebackground=self.colors['button_hover'],
                          font=self.button_font, width=15, height=2)
            btn.pack(side=tk.LEFT, padx=5)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors['button']))
        
        # Sara chat interface
        sara_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        sara_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(sara_frame, text="💬 Chat with Sara (routes to best agent):", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=self.label_font).pack(side=tk.LEFT, padx=5)
        
        self.sara_entry = tk.Entry(sara_frame, bg=self.colors['button'], fg=self.colors['fg'],
                                   font=self.label_font, insertbackground=self.colors['fg'])
        self.sara_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.sara_entry.bind("<Return>", lambda e: self.send_to_sara())
        self.sara_entry.focus()
        
        # Status label
        self.status_display = tk.Label(sara_frame, text="🤖 Sara ready - type any question!",
                                      bg=self.colors['bg'], fg=self.colors['accent'], 
                                      font=self.label_font)
        self.status_display.pack(side=tk.RIGHT, padx=5)
    
    def create_log_panel(self, parent):
        """Create enhanced log display panel"""
        log_frame = tk.LabelFrame(parent, text="📝 Agent Communications",
                                 bg=self.colors['bg'], fg=self.colors['accent'],
                                 font=self.label_font)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log controls
        log_controls = tk.Frame(log_frame, bg=self.colors['bg'])
        log_controls.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(log_controls, text="Clear", command=self.clear_logs,
                 bg=self.colors['button'], fg=self.colors['warning'],
                 font=self.button_font).pack(side=tk.LEFT, padx=5)
        
        tk.Label(log_controls, text="Command Center Status:", bg=self.colors['bg'], 
                fg=self.colors['fg'], font=self.label_font).pack(side=tk.LEFT, padx=(20, 5))
        
        self.status_label = tk.Label(log_controls, text="🟢 Online", 
                                    bg=self.colors['bg'], fg=self.colors['accent'],
                                    font=self.label_font)
        self.status_label.pack(side=tk.LEFT)
        
        tk.Button(log_controls, text="Test Ollama", command=self.test_ollama,
                 bg=self.colors['button'], fg=self.colors['info'],
                 font=self.button_font).pack(side=tk.RIGHT, padx=5)
        
        # Log display
        self.log_display = scrolledtext.ScrolledText(
            log_frame, height=15, bg=self.colors['bg'], fg=self.colors['fg'],
            font=self.log_font, wrap=tk.WORD, insertbackground=self.colors['fg']
        )
        self.log_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Configure tags for log levels
        self.log_display.tag_config("INFO", foreground=self.colors['info'])
        self.log_display.tag_config("WARNING", foreground=self.colors['warning'])
        self.log_display.tag_config("ERROR", foreground=self.colors['warning'])
        self.log_display.tag_config("AGENT", foreground=self.colors['accent'])
    
    def add_log(self, message, level="INFO"):
        """Add timestamped log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_line = f"[{timestamp}] {message}\n"
        
        self.log_display.insert(tk.END, formatted_line, level)
        self.log_display.see(tk.END)
        
        # Limit log lines
        lines = self.log_display.get("1.0", tk.END).split('\n')
        if len(lines) > 500:
            self.log_display.delete("1.0", "10.0")
    
    def update_agent_status(self, agent, status):
        """Update agent status indicator"""
        if agent in self.agent_labels:
            color = self.colors['accent'] if status else self.colors['warning']
            symbol = "●" if status else "○"
            self.agent_labels[agent].config(text=symbol, fg=color)
    
    def update_system_metric(self, metric, value, color=None):
        """Update system metric display"""
        if metric in self.system_labels:
            self.system_labels[metric].config(text=str(value))
            if color:
                self.system_labels[metric].config(fg=color)
    
    def start_monitoring(self):
        """Start background monitoring"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # Check if Sara voice agent is running
        self.check_agent_process()
    
    def monitor_loop(self):
        """Background monitoring loop"""
        import psutil
        
        while self.monitoring_active:
            try:
                # Update system metrics
                cpu = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                disk_space = psutil.disk_usage('/').free / (1024**3)  # GB
                
                # Update UI (in main thread)
                self.root.after(0, self.update_system_metrics, cpu, memory, disk, disk_space)
                
                # Check agent processes periodically
                if int(time.time()) % 10 == 0:  # Every 10 seconds
                    self.root.after(0, self.check_agent_process)
                
                time.sleep(2)
                
            except Exception as e:
                self.root.after(0, self.add_log, f"Monitoring error: {e}", "ERROR")
                time.sleep(5)
    
    def update_system_metrics(self, cpu, memory, disk, disk_space):
        """Update system metrics in UI"""
        self.update_system_metric("CPU", f"{cpu}%", 
                                 self.colors['warning'] if cpu > 80 else self.colors['info'])
        self.update_system_metric("RAM", f"{memory}%", 
                                 self.colors['warning'] if memory > 80 else self.colors['info'])
        self.update_system_metric("Disk", f"{disk}%", 
                                 self.colors['warning'] if disk > 90 else self.colors['info'])
        
        # Check Ollama status for final metric
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                models = len(response.json().get('models', []))
                self.update_system_metric("Ollama", f"🟢 {models} models")
            else:
                self.update_system_metric("Ollama", "🔴 Error")
        except:
            self.update_system_metric("Ollama", "🔴 Offline")
    
    def check_agent_process(self):
        """Check Ollama agents status"""
        try:
            # Check Ollama server
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code == 200:
                self.update_agent_status("Ollama", True)
                models = response.json().get('models', [])
                
                # Check individual agents
                agent_models = {
                    "Sara": "sara-ai-partner",
                    "Chloe": "chloe-search-agent", 
                    "Nexus": "nexus-analyst",
                    "Codi": "codi-tech-expert",
                    "Vision": "vision-analyst"
                }
                
                for agent, model_name in agent_models.items():
                    available = any(model_name in model.get('name', '') for model in models)
                    self.update_agent_status(agent, available)
                
                self.status_label.config(text="🟢 Online", fg=self.colors['accent'])
                self.add_log("Ollama agents connected", "INFO")
            else:
                self.status_label.config(text="🔴 Ollama Error", fg=self.colors['warning'])
                # Mark all agents offline
                for agent in ["Sara", "Chloe", "Nexus", "Codi", "Vision"]:
                    self.update_agent_status(agent, False)
                    
        except Exception as e:
            self.status_label.config(text="🔴 Offline", fg=self.colors['warning'])
            self.add_log(f"Connection error: {str(e)}", "ERROR")
            # Mark all agents offline
            for agent in ["Sara", "Chloe", "Nexus", "Codi", "Vision"]:
                self.update_agent_status(agent, False)
    
    def test_ollama(self):
        """Test Ollama connection"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                self.add_log(f"Ollama connected! Found {len(models)} models", "INFO")
                for model in models[:5]:  # Show first 5
                    self.add_log(f"  📦 {model}", "AGENT")
            else:
                self.add_log(f"Ollama error: {response.status_code}", "ERROR")
        except Exception as e:
            self.add_log(f"Ollama connection failed: {e}", "ERROR")
    
    def get_agent_response(self, model_name, prompt):
        """Get response from specific agent"""
        try:
            data = {
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response')
            else:
                return f"Error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def broadcast_message(self):
        """Send message to all agents"""
        message = self.command_entry.get().strip()
        if not message:
            return
            
        self.add_log("📢 BROADCAST: " + message, "AGENT")
        
        agents = [
            ("Sara", "sara-ai-partner"),
            ("Chloe", "chloe-search-agent"),
            ("Nexus", "nexus-analyst")
        ]
        
        for display_name, model_name in agents:
            self.add_log(f"🤖 {display_name}: Processing...", "INFO")
            response = self.get_agent_response(model_name, message)
            self.add_log(f"💬 {display_name}: {response[:100]}...", "AGENT")
        
        self.command_entry.delete(0, tk.END)
    
    def talk_agent(self):
        """Talk to Sara agent"""
        self.send_command_to_agent("sara-ai-partner", "Sara")
    
    def talk_chloe(self):
        """Talk to Chloe agent"""
        self.send_command_to_agent("chloe-search-agent", "Chloe")
    
    def talk_nexus(self):
        """Talk to Nexus agent"""
        self.send_command_to_agent("nexus-analyst", "Nexus")
    
    def send_command_to_agent(self, model_name, agent_name):
        """Setup direct chat with specific agent"""
        message = self.command_entry.get().strip()
        if not message:
            message = "Hello! Can you introduce yourself?"
            
        self.add_log(f"🎯 Direct message to {agent_name}: {message}", "AGENT")
        response = self.get_agent_response(model_name, message)
        self.add_log(f"💬 {agent_name} Response: {response}", "AGENT")
        
        if not message:
            self.command_entry.delete(0, tk.END)
    
    def send_command(self):
        """Redirect to Sara chat"""
        self.send_to_sara()
    
    def focus_sara(self):
        """Focus on Sara chat"""
        self.sara_entry.focus()
        self.status_display.config(text="🤖 Sara ready - type your question!")
        self.add_log("🎯 Focused on Sara - she'll route to the best agent", "INFO")
    
    def team_chat(self):
        """Send message to all team members"""
        self.sara_entry.delete(0, tk.END)
        self.sara_entry.insert(0, "Team, can you all introduce yourselves and your specialties?")
        self.status_display.config(text="📢 Team broadcast ready - press Enter to send")
        self.sara_entry.focus()
    
    def team_chat(self):
        """Initiate team conversation - all agents report to Sara"""
        self.sara_entry.delete(0, tk.END)
        self.sara_entry.insert(0, "Team, can you all introduce yourselves and tell me when you're ready for complex collaboration?")
        self.status_display.config(text="📢 Team coordination - press Enter to start", fg=self.colors['info'])
        self.sara_entry.focus()
        
        # After user sends, trigger team coordination
        self.root.after(2000, self.coordinate_team_collaboration)
    
    def coordinate_team_collaboration(self):
        """Sara coordinates team - asks all agents, compiles responses"""
        self.add_log("🤖 Sara: Team, I need a status update for our human. Please report when ready.", "AGENT")
        
        # Get status from all available agents
        team_reports = {
            "Sara": "🤖 Ready to coordinate and assist",
            "Chloe": "🔍 Research systems online",
            "Nexus": "📊 Analysis capabilities active"
        }
        
        # Actually query each agent
        self.status_display.config(text="🤖 Coordinating team responses...", fg=self.colors['info'])
        
        def get_agent_report(agent_name, model_name):
            try:
                response = self.get_agent_response(model_name, "Quick status report: are you ready to collaborate? Respond in one sentence.")
                return response[:60] if response else "Status unknown"
            except:
                return "暂时无法连接 (Temporarily unavailable)"
        
        # Get actual responses
        import threading
        agent_data = [
            ("Sara", "sara-ai-partner"),
            ("Chloe", "chloe-search-agent"), 
            ("Nexus", "nexus-analyst")
        ]
        
        responses = {}
        for display_name, model_name in agent_data:
            response = get_agent_report(display_name, model_name)
            responses[display_name] = response
            self.add_log(f"💬 {display_name}: {response}", "AGENT")
        
        # Sara compiles summary
        self.add_log("🤖 Sara: Team, I have all your status updates. Here's our current readiness:", "AGENT")
        
        summary = f"📊 TEAM STATUS SUMMARY:\n"
        for agent, status in responses.items():
            if "error" not in status.lower() and "unavailable" not in status.lower():
                summary += f"✅ {agent}: {status}\n"
            else:
                summary += f"⚠️ {agent}: Need attention\n"
        
        self.add_log(summary, "AGENT")
        self.status_display.config(text="🟢 Team coordination complete!", fg=self.colors['accent'])
    
    def test_all_agents(self):
        """Test all agents and have Sara compile results"""
        self.add_log("🤖 Sara: Testing team connectivity, please wait while I check in with each agent...", "AGENT")
        self.status_display.config(text="🤖 Sara coordinating team health check...", fg=self.colors['info'])
        
        agents = [
            ("Sara", "sara-ai-partner"),
            ("Chloe", "chloe-search-agent"), 
            ("Nexus", "nexus-analyst"),
            ("Codi", "codi-tech-expert"),
            ("Vision", "vision-analyst")
        ]
        
        team_status = {}
        
        # Test each agent
        for display_name, model_name in agents:
            self.add_log(f"🤖 Sara: Checking {display_name}...", "AGENT")
            response = self.get_agent_response(model_name, "Connection test: respond with just 'SYSTEM: ONLINE' or 'SYSTEM: OFFLINE'")
            
            if "error" not in response.lower() and "offline" not in response.lower():
                team_status[display_name] = "🟢 Online"
                self.add_log(f"💬 {display_name}: ✅ Connection successful", "AGENT")
            else:
                team_status[display_name] = "🔴 Offline"  
                self.add_log(f"💬 {display_name}: ❌ Connection failed", "ERROR")
        
        # Sara compiles complete report
        self.add_log("🤖 Sara: Team health check complete! Here's the comprehensive status:", "AGENT")
        
        total_agents = len(agents)
        online_count = sum(1 for status in team_status.values() if "🟢" in status)
        
        report = f"📊 TEAM HEALTH REPORT:\n"
        report += f"📈 Overall: {online_count}/{total_agents} agents operational\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for display_name, status in team_status.items():
            report += f"{status:6} {display_name}\n"
        
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if online_count == total_agents:
            report += f"🎉 EXCELLENT: Full team operational!"
            self.status_display.config(text="🟢 Full team online!", fg=self.colors['accent'])
        elif online_count >= 3:
            report += f"✅ GOOD: Core team ready for collaboration"
            self.status_display.config(text="🟡 Core team ready", fg=self.colors['info'])
        else:
            report += f"⚠️ ALERT: Multiple agents need attention"
            self.status_display.config(text="🔴 Team needs support", fg=self.colors['warning'])
        
        self.add_log(report, "AGENT")
    
    def send_to_sara(self):
        """Send message to Sara - she'll coordinate with team and use RAG memory"""
        message = self.sara_entry.get().strip()
        if not message:
            return
            
        self.add_log(f"🗣️ You → Sara: {message}", "INFO")
        self.status_display.config(text="🤖 Sara analyzing with team + memory...", fg=self.colors['info'])
        
        # Check RAG memory for relevant knowledge first
        relevant_knowledge = self.search_rag_memory(message)
        knowledge_context = ""
        if relevant_knowledge:
            knowledge_context = "\n💡 RELEVANT KNOWLEDGE FROM MEMORY:\n"
            for result in relevant_knowledge:
                knowledge_context += f"📄 From {result['file']}: {result['content'][:200]}...\n"
            self.add_log(f"🧠 Found {len(relevant_knowledge)} relevant memories", "INFO")
        
        # Create enhanced prompt with RAG context
        enhanced_prompt = f"""You are Sara with full RAG memory access.

{knowledge_context}

Human request: {message}

Coordinate with your team (Chloe for research, Nexus for analysis, Codi for technical) and provide 
a comprehensive response using both your expertise and the relevant knowledge from your memory 
database above. cite sources when using memory information."""
        
        # Sara analyzes with memory and decides team coordination
        sara_analysis = self.get_agent_response("sara-ai-partner", enhanced_prompt, timeout=20)
        
        self.add_log(f"💬 Sara: {sara_analysis}", "AGENT")
        
        # Determine which agents to involve based on Sara's analysis
        team_members = [("Sara", "sara-ai-partner")]
        
        if any(word in sara_analysis.lower() for word in ["research", "search", "find"]):
            team_members.append(("Chloe", "chloe-search-agent"))
        if any(word in sara_analysis.lower() for word in ["analysis", "market", "trends"]):
            team_members.append(("Nexus", "nexus-analyst"))
        if any(word in sara_analysis.lower() for word in ["technical", "code", "debug"]):
            team_members.append(("Codi", "codi-tech-expert"))
        if any(word in sara_analysis.lower() for word in ["visual", "image", "chart"]):
            team_members.append(("Vision", "vision-analyst"))
        
        # Sara coordinates with each team member
        self.add_log("🤖 Sara: Coordinating with team specialists...", "AGENT")
        
        specialist_responses = {}
        
        for display_name, model_name in team_members:
            if display_name == "Sara":
                # Sara provides her direct response
                response = self.get_agent_response(model_name, message, timeout=20)
                specialist_responses[display_name] = response
                self.add_log(f"💬 {display_name}: {response[:100]}...", "AGENT")
            else:
                # Other specialists provide expertise
                self.add_log(f"🤖 Sara: Consulting {display_name} on this request...", "AGENT")
                response = self.get_agent_response(model_name, 
                    f"Sara asked: '{message}'. Please provide your expert analysis. Keep response focused and valuable.", 
                    timeout=20)
                specialist_responses[display_name] = response
                self.add_log(f"💬 {display_name}: {response[:100]}...", "AGENT")
        
        # Sara compiles and presents the complete team response
        self.add_log("🤖 Sara: Team collaboration complete! Here's our comprehensive response:", "AGENT")
        
        # Create formal team response
        final_response = f"📋 COMPREHENSIVE TEAM RESPONSE:\n"
        final_response += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for display_name, response in specialist_responses.items():
            final_response += f"\n🎯 **{display_name}:**\n"
            final_response += f"{response}\n"
        
        # Sara adds summary and next steps
        summary_prompt = f"Based on these team responses to '{message}', please provide a brief summary and suggest next steps."
        sara_summary = self.get_agent_response("sara-ai-partner", summary_prompt, timeout=15)
        
        final_response += f"\n📊 **Sara's Coordination:**\n{sara_summary}"
        
        # Present final compiled response
        self.add_log(final_response, "AGENT")
        
        # Update status
        self.status_display.config(text="🟢 Team collaboration complete!", fg=self.colors['accent'])
        
        # Clear for next message but focus
        self.sara_entry.delete(0, tk.END)
        self.sara_entry.focus()
    
    def start_sara(self):
        """Start Sara voice agent"""
        try:
            self.add_log("Voice agent features available through console commands", "INFO")
            self.add_log("Run: python3 wake_word_detector.py for voice interaction", "INFO")
        except Exception as e:
            self.add_log(f"Error: {e}", "ERROR")
    
    def stop_agents(self):
        """Stop all voice agents"""
        try:
            import psutil
            stopped = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'sara_voice_agent.py' in cmdline or 'monitor_center.py' in cmdline:
                        proc.terminate()
                        stopped += 1
            
            self.add_log(f"Stopped {stopped} agent processes", "INFO")
        except Exception as e:
            self.add_log(f"Error stopping agents: {e}", "ERROR")
    
    def open_monitor(self):
        """Open detailed monitoring"""
        self.add_log("Opening detailed monitoring...", "INFO")
        # Would open additional monitoring window
    
    def open_settings(self):
        """Open settings dialog"""
        self.add_log("Settings functionality coming soon...", "INFO")
        # Would open settings dialog
    
    def clear_logs(self):
        """Clear log display"""
        self.log_display.delete("1.0", tk.END)
        self.add_log("Logs cleared", "INFO")
    
    def run(self):
        """Run the GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        self.monitoring_active = False
        self.root.destroy()

if __name__ == "__main__":
    app = VoiceCommandCenterGUI()
    app.run()