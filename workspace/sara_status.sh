#!/bin/bash
# 🎯 QUICK SARA STATUS CHECK
echo "🔍 SARA STATUS REPORT"
echo "===================="

# Check if Sara is running
if curl -s http://127.0.0.1:8890/api/status > /dev/null 2>&1; then
    echo "✅ Sara is RUNNING at http://127.0.0.1:8890"
    
    # Get current status
    status=$(curl -s http://127.0.0.1:8890/api/status)
    echo "📊 Status: $(echo $status | grep -o '"model":"[^"]*"' | cut -d'"' -f4)"
    echo "💬 Conversations: $(echo $status | grep -o '"conversations":[0-9]*' | cut -d':' -f2)"
    
    # Test command execution
    echo ""
    echo "🧪 Command Execution Test:"
    response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"message":"whoami"}' http://127.0.0.1:8890/api/chat | grep -o '"response":"[^"]*"' | cut -d'"' -f4)
    echo "whoami → $response"
    
    if [ "$response" = "godfather" ]; then
        echo "✅ COMMAND EXECUTION: WORKING!"
        echo "🏆 Sara is FULLY OPERATIONAL!"
    else
        echo "❌ Command execution failed - needs fix"
    fi
else
    echo "❌ Sara is NOT running"
    echo "🚨 Start with: ./start_working_sara.sh"
fi

echo ""
echo "🌐 Access at: http://127.0.0.1:8890"