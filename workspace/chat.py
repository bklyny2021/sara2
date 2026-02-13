#!/usr/bin/env python3
import subprocess
import sys
import json
from datetime import datetime
import argparse
import os
from enhanced_rag_memory_system import EnhancedRAGMemorySystem

def chat_with_memory(model_name="sara-ai-partner", custom_prompt=None):
    """Chat with agent that has full RAG memory context"""
    # Initialize enhanced memory system
    workspace_path = os.path.dirname(os.path.abspath(__file__))
    memory_system = EnhancedRAGMemorySystem(workspace_path)
    
    # Load agent's full memory context
    agent_name = model_name.lower()
    memory_system, context_summary = initialize_agent_with_memory(agent_name, workspace_path)
    
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
        # Search agent memory for relevant context
        memory_results = memory_system.search_agent_memory(agent_name, custom_prompt, top_k=3)
        memory_context = ""
        if memory_results:
            memory_context = "RELEVANT MEMORY:\\n"
            for i, mem in enumerate(memory_results):
                memory_context += f"{i+1}. {mem['chunk'][:150]}... [{mem['timestamp']}][Relevance: {mem['relevance']:.2f}]\\n"
        
        # Create enhanced prompt with memory context
        enhanced_prompt = f"""{context_summary}

{memory_context}

CURRENT CONVERSATION:
User: {custom_prompt}

You are {display_name} with complete memory of all previous conversations since day one. Use your memory context to provide personalized, context-aware responses. Never forget important details from our history.

Response:"""
        
        # Single prompt mode
        cmd = [
            'curl', '-X', 'POST',
            'http://localhost:11434/api/generate',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({
                "model": model_name,
                "prompt": enhanced_prompt,
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
                
                # Store conversation in memory
                memory_system.add_conversation(f"single_prompt_{datetime.now().strftime('%H%M%S')}", custom_prompt, response, agent_name)
                
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"💥 Error: {str(e)}")
        return
    
    # Interactive mode with memory
    print(f"🤖 {display_name} - Interactive Chat with Full Memory")
    print(f"🧠 Memory loaded: {len(context_summary.split())} words of context")
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
            
            # Search memory for relevant context
            memory_results = memory_system.search_agent_memory(agent_name, user_input, top_k=3)
            memory_context = ""
            if memory_results:
                memory_context = "RELEVANT MEMORY:\\n"
                for i, mem in enumerate(memory_results):
                    memory_context += f"{i+1}. {mem['chunk'][:100]}... [{mem['timestamp']}][Relevance: {mem['relevance']:.2f}]\\n"
                
            # Create enhanced prompt with full memory context
            enhanced_prompt = f"""{context_summary}

{memory_context}

CURRENT CONVERSATION:
User: {user_input}

You are {display_name} with complete memory of all previous conversations since day one. Use your memory context to provide personalized, context-aware responses. Never forget important details from our history.

Response:"""
                
            cmd = [
                'curl', '-X', 'POST',
                'http://localhost:11434/api/generate',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "model": model_name,
                    "prompt": enhanced_prompt,
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
                    
                    # Store conversation in memory for future context
                    memory_system.add_conversation(
                        f"interactive_{datetime.now().strftime('%H%M%S')}", 
                        user_input, response, agent_name
                    )
                    
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