#!/usr/bin/env python3
import subprocess
import json
import time
import threading
from datetime import datetime
import sys

class AgentCommandCenter:
    def __init__(self):
        self.agents = {
            'sara': {
                'name': 'Sara AI Partner',
                'model': 'sara-ai-partner',
                'role': 'General Conversation & Task Management',
                'status': '🟢 Online',
                'last_response': None,
                'response_time': 0
            },
            'chloe': {
                'name': 'Chloe Rodriguez',
                'model': 'chloe-search-agent', 
                'role': 'Search Intelligence & Research',
                'status': '🟢 Online',
                'last_response': None,
                'response_time': 0
            },
            'nexus': {
                'name': 'Nexus Kumar',
                'model': 'nexus-analyst',
                'role': 'Strategic Analysis & Market Research',
                'status': '🟢 Online', 
                'last_response': None,
                'response_time': 0
            },
            'codi': {
                'name': 'Codi Tech Expert',
                'model': 'codi-tech-expert',
                'role': 'Technical Development & Debugging',
                'status': '🟡 Slow',
                'last_response': None,
                'response_time': 0
            },
            'vision': {
                'name': 'Vision Analyst',
                'model': 'vision-analyst',
                'role': 'Visual Data Analysis',
                'status': '🟡 Slow',
                'last_response': None,
                'response_time': 0
            }
        }
        self.command_log = []
        self.running = True
        
    def get_agent_response(self, agent_key, prompt, timeout=25):
        """Get response from specific agent"""
        start_time = time.time()
        agent = self.agents[agent_key]
        
        try:
            cmd = [
                'curl', '-X', 'POST',
                'http://localhost:11434/api/generate',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "model": agent['model'],
                    "prompt": prompt,
                    "stream": False
                }),
                '--max-time', str(timeout + 5)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=(timeout + 10))
            end_time = time.time()
            
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                response = response_data.get('response', 'Response parsing error')
                response_time = round(end_time - start_time, 2)
                
                # Update agent status
                agent['last_response'] = response[:100] + '...' if len(response) > 100 else response
                agent['response_time'] = response_time
                agent['status'] = '🟢 Online' if response_time < 15 else '🟡 Slow'
                
                return response, response_time
            else:
                agent['status'] = '🔴 Error'
                return f"Agent Error: {result.stderr}", 0
                
        except subprocess.TimeoutExpired:
            agent['status'] = '🔴 Timeout'
            return "Request timeout - agent taking too long to respond", 0
        except Exception as e:
            agent['status'] = '🔴 Error'
            return f"Communication error: {str(e)}", 0
    
    def send_broadcast(self, message):
        """Send message to all agents"""
        print(f"\n📢 BROADCASTING: {message}")
        print("=" * 60)
        results = {}
        
        for agent_key in self.agents.keys():
            agent_name = self.agents[agent_key]['name']
            print(f"\n🤖 {agent_name}:")
            print("⏳ Processing...")
            
            response, response_time = self.get_agent_response(agent_key, message)
            
            print(f"⏱️  Time: {response_time}s")
            print(f"💬 Response: {response}")
            print("-" * 40)
            
            results[agent_key] = {
                'response': response,
                'response_time': response_time,
                'agent': agent_name
            }
            
        # Log the broadcast
        self.command_log.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'type': 'BROADCAST',
            'message': message,
            'results': results
        })
        
        return results
    
    def send_to_agent(self, agent_key, message):
        """Send message to specific agent"""
        agent_key = agent_key.lower()
        if agent_key not in self.agents:
            return f"Agent '{agent_key}' not found. Available: {', '.join(self.agents.keys())}"
        
        agent = self.agents[agent_key]
        print(f"\n🎯 DIRECT MESSAGE TO {agent['name'].upper()}")
        print(f"💬 Message: {message}")
        print("=" * 60)
        
        print(f"🤖 {agent['name']}:")
        print("⏳ Processing...")
        
        response, response_time = self.get_agent_response(agent_key, message)
        
        print(f"⏱️  Time: {response_time}s")
        print(f"💬 Response: {response}")
        
        # Log the direct message
        self.command_log.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'type': 'DIRECT',
            'agent': agent_key,
            'message': message,
            'response': response,
            'response_time': response_time
        })
        
        return response
    
    def show_status(self):
        """Display current agent status"""
        print("\n📊 AGENT COMMAND CENTER STATUS")
        print("=" * 60)
        
        for key, agent in self.agents.items():
            print(f"{agent['status']} {agent['name']}")
            print(f"   🎭 Role: {agent['role']}")
            print(f"   ⏱️  Last Response: {agent['response_time']}s")
            if agent['last_response']:
                print(f"   💭 Last Response: {agent['last_response']}")
            print()
    
    def show_log(self, limit=5):
        """Show recent command log"""
        print(f"\n📜 RECENT COMMANDS (Last {limit})")
        print("=" * 60)
        
        recent_log = self.command_log[-limit:] if len(self.command_log) > limit else self.command_log
        
        for entry in recent_log:
            print(f"⏰ {entry['timestamp']} - {entry['type']}")
            if entry['type'] == 'BROADCAST':
                print(f"   Message: {entry['message'][:50]}...")
                print(f"   Responses: {len(entry['results'])} agents replied")
            else:
                print(f"   Agent: {entry['agent'].upper()}")
                print(f"   Message: {entry['message'][:50]}...")
        print()
    
    def run_interactive(self):
        """Interactive command center"""
        print("🚀 AI AGENT COMMAND CENTER - SPAWNED")
        print("=" * 60)
        print("COMMANDS:")
        print("  broadcast <message>    - Send to ALL agents")
        print("  talk <agent> <message> - Send to specific agent")
        print("  status                 - Show agent status") 
        print("  log                    - Show recent commands")
        print("  agents                 - List available agents")
        print("  quit/exit              - Exit command center")
        print("=" * 60)
        
        while self.running:
            try:
                user_input = input("\n🎯 COMMAND> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Command Center shutting down...")
                    break
                    
                if user_input.lower() == 'status':
                    self.show_status()
                    continue
                    
                if user_input.lower() == 'log':
                    self.show_log()
                    continue
                    
                if user_input.lower() == 'agents':
                    print("\n🤖 AVAILABLE AGENTS:")
                    for key, agent in self.agents.items():
                        print(f"  {key:8} - {agent['name']} ({agent['role']})")
                    continue
                
                # Parse commands
                parts = user_input.split(maxsplit=2)
                command = parts[0].lower()
                
                if command == 'broadcast' and len(parts) >= 2:
                    message = ' '.join(parts[1:])
                    self.send_broadcast(message)
                elif command == 'talk' and len(parts) >= 3:
                    agent_name = parts[1].lower()
                    message = ' '.join(parts[2:])
                    self.send_to_agent(agent_name, message)
                else:
                    print("❌ Invalid command. Type 'agents' to see available agents.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Command Center shutting down...")
                break
            except Exception as e:
                print(f"💥 Command error: {str(e)}")

def main():
    center = AgentCommandCenter()
    center.run_interactive()

if __name__ == "__main__":
    main()