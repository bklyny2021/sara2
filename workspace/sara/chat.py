#!/usr/bin/env python3
import subprocess
import sys
import json
import argparse

def chat_interactive(model_name="sara-ai-partner", custom_prompt=None):
    # Available agents
    agents = {
        "sara": "sara-ai-partner",
        "sara-ai-partner": "sara-ai-partner",
        "chloe": "chloe-search-agent", 
        "chloe-search-agent": "chloe-search-agent",
        "nexus": "nexus-analyst",
        "nexus-analyst": "nexus-analyst",
        "codi": "codi-tech-expert",
        "codi-tech-expert": "codi-tech-expert",
        "vision": "vision-analyst", 
        "vision-analyst": "vision-analyst"
    }
    
    agent_display_names = {
        "sara-ai-partner": "Sara AI Partner",
        "chloe-search-agent": "Chloe Rodriguez (Search Intelligence)",
        "nexus-analyst": "Nexus Kumar (Strategic Analysis)",
        "codi-tech-expert": "Codi (Tech Expert)",
        "vision-analyst": "Vision Analyst"
    }
    
    model_name = agents.get(model_name.lower(), model_name)
    display_name = agent_display_names.get(model_name, model_name)
    
    if custom_prompt:
        # Single prompt mode
        cmd = [
            'curl', '-X', 'POST',
            'http://localhost:11434/api/generate',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({
                "model": model_name,
                "prompt": custom_prompt,
                "stream": False
            }),
            '--max-time', '60'
        ]
        
        print(f"🤖 {display_name}")
        print(f"💬 Prompt: {custom_prompt}")
        print("⏳ Thinking...")
        print("-" * 50)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=70)
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                response = response_data.get('response', 'Sorry, I had trouble understanding that.')
                print(f"🤖 {display_name}: {response}")
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"💥 Error: {str(e)}")
        return
    
    # Interactive mode
    print(f"🤖 {display_name} - Interactive Chat Mode")
    print("💬 Type your messages below, 'quit' or 'exit' to stop")
    print("=" * 50)
    
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"\n👋 Goodbye! - {display_name}")
                break
                
            if not user_input:
                continue
                
            cmd = [
                'curl', '-X', 'POST',
                'http://localhost:11434/api/generate',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "model": model_name,
                    "prompt": user_input,
                    "stream": False
                }),
                '--max-time', '30'
            ]
            
            print("⏳ Thinking...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
            
            if result.returncode == 0:
                try:
                    response_data = json.loads(result.stdout)
                    response = response_data.get('response', 'Sorry, I had trouble understanding that.')
                    print(f"\n🤖 {display_name}: {response}")
                except json.JSONDecodeError:
                    print(f"\n❌ Error parsing response: {result.stdout}")
            else:
                print(f"\n❌ Error: {result.stderr}")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye! - {display_name}")
            break
        except subprocess.TimeoutExpired:
            print("\n⏰ Request timed out. Please try again.")
        except Exception as e:
            print(f"\n💥 Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Chat with local AI agents')
    parser.add_argument('agent', nargs='?', default='sara', help='Agent name (sara, chloe, nexus, codi, vision)')
    parser.add_argument('--prompt', '-p', help='Single prompt mode (no interactive chat)')
    
    args = parser.parse_args()
    
    chat_interactive(args.agent, args.prompt)

if __name__ == "__main__":
    main()