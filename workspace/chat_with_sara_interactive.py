#!/usr/bin/env python3
import subprocess
import sys
import json

def chat_with_sara():
    print("🤖 Sara AI Partner - Interactive Chat Mode")
    print("💬 Type your messages below, 'quit' or 'exit' to stop")
    print("=" * 50)
    
    model_name = "sara-ai-partner"
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye! - Sara")
                break
                
            if not user_input:
                continue
                
            # Call ollama with the user's input
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
            
            # Execute and capture response
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
            
            if result.returncode == 0:
                try:
                    response_data = json.loads(result.stdout)
                    response = response_data.get('response', 'Sorry, I had trouble understanding that.')
                    print(f"\n🤖 Sara: {response}")
                except json.JSONDecodeError:
                    print(f"\n❌ Error parsing response: {result.stdout}")
            else:
                print(f"\n❌ Error: {result.stderr}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! - Sara")
            break
        except subprocess.TimeoutExpired:
            print("\n⏰ Request timed out. Please try again.")
        except Exception as e:
            print(f"\n💥 Error: {str(e)}")

if __name__ == "__main__":
    chat_with_sara()