#!/usr/bin/env python3
import requests
import json
import sys

def chat_with_model(model_name, prompt, timeout=30):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=timeout)
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'No response')
        else:
            return f"Error: HTTP {response.status_code} - {response.text}"
    except requests.exceptions.Timeout:
        return f"Error: Request timed out after {timeout}s"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 chat.py <model_name> <prompt>")
        sys.exit(1)
    
    model_name = sys.argv[1]
    prompt = " ".join(sys.argv[2:])
    
    print(f"\n🤖 Talking to: {model_name}")
    print(f"📝 Prompt: {prompt}")
    print("⏳ Response:")
    print("-" * 50)
    
    response = chat_with_model(model_name, prompt, timeout=30)
    print(response)
    print("-" * 50)

if __name__ == "__main__":
    main()