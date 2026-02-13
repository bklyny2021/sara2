#!/usr/bin/env python3

import subprocess
import json
import time
from datetime import datetime

def quick_spawn():
    """Quick test spawn to verify agents are ready"""
    print("⚡ QUICK SPAWN TEST")
    print("=" * 40)
    
    agents = {
        'sara': 'Sara AI Partner',
        'chloe': 'Chloe Rodriguez', 
        'nexus': 'Nexus Kumar'
    }
    
    all_responding = True
    
    for key, name in agents.items():
        print(f"🔌 Pinging {name}...")
        
        start_time = time.time()
        try:
            cmd = [
                'curl', '-X', 'POST',
                'http://localhost:11434/api/generate',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "model": f"{key}-ai-partner" if key == 'sara' else f"{key}-search-agent" if key == 'chloe' else f"{key}-analyst",
                    "prompt": "Respond with just: Online and ready",
                    "stream": False
                }),
                '--max-time', '10'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            end_time = time.time()
            
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                response = response_data.get('response', 'Error parsing')
                response_time = round(end_time - start_time, 2)
                
                if "error" not in response.lower():
                    print(f"✅ {name} - {response_time}s - {response}")
                else:
                    print(f"❌ {name} - Error in response")
                    all_responding = False
            else:
                print(f"❌ {name} - Communication error")
                all_responding = False
                
        except Exception as e:
            print(f"❌ {name} - {str(e)}")
            all_responding = False
    
    print(f"\n{'✅ ALL SYSTEMS GO' if all_responding else '⚠️ SOME ISSUES DETECTED'}")
    return all_responding

if __name__ == "__main__":
    quick_spawn()