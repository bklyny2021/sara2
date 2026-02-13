#!/bin/bash
# 🏆 START WORKING SARA - WINNER'S EDITION
# This script starts the proven working Sara setup

echo "🌟 STARTING WORKING SARA - WINNER'S EDITION"
echo "=========================================="

# Kill any existing Sara processes
echo "🧹 Cleaning up previous instances..."
pkill -f sara_working_web 2>/dev/null

# Wait for cleanup
sleep 2

# Start the working Sara
echo "🚀 Starting Sara at port 8890..."
cd /home/godfather/.openclaw/workspace
python3 sara_working_web.py > /tmp/sara_winner.log 2>&1 &

# Wait for startup
sleep 3

# Test if it's working
echo "🎯 Testing command execution..."
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"message":"whoami"}' http://127.0.0.1:8890/api/chat | grep -o '"response":"[^"]*"' | cut -d'"' -f4)

if [ "$response" = "godfather" ]; then
    echo "✅ SUCCESS! Sara is working perfectly!"
    echo "📍 URL: http://127.0.0.1:8890"
    echo "🎯 Status: Executing commands like a champ!"
    echo "💚 Winner confirmed! 🏆"
else
    echo "❌ Something went wrong. Check /tmp/sara_winner.log"
    echo "🔧 Emergency recovery needed..."
fi

echo ""
echo "🎉 Ready to use your working Sara!"
echo "=================================="