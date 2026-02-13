#!/bin/bash
# SARA SPEED DEPLOYMENT - Complete in < 30 seconds

echo "🚀 SARA SPEED AGENT DEPLOYMENT"
echo "================================"

# Kill existing agents
pkill -f "sara.*agent.py" 2>/dev/null

# Start speed agent
cd /home/godfather/sara2
echo "🌐 Starting Sara Speed Agent..."
python3 sara_speed_agent.py &

# Test connectivity
sleep 3
echo "🔍 Testing deployment..."
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"message":"test"}' http://127.0.0.1:8902/ask | jq -r .response 2>/dev/null)

if [[ "$response" == *"Speed Agent"* ]]; then
    echo "✅ DEPLOYMENT SUCCESS"
    echo "🌐 http://127.0.0.1:8902"
    echo "🚀 Speed Agent ready - 2 models, optimized for rapid operations"
    echo "💪 Ready for task completion acceleration"
else
    echo "❌ Deployment failed"
fi