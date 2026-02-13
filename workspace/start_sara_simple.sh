#!/bin/bash
# 🌟 SARA SIMPLE ROCK-SOLID LAUNCHER
# No streaming, no auto-stop, just reliable chat

echo "🌟 SARA SIMPLE AUTONOMOUS CHAT"
echo "============================="
echo "🔧 No streaming complexity"
echo "⏹ Stop controls working properly"
echo "✅ Rock solid responses"
echo "🚀 Starting simple chat..."
echo "🌐 http://127.0.0.1:8890"
echo "✅ 100% Offline & Private Operation"
echo ""

# Kill any existing Sara processes
pkill -f sara_simple 2>/dev/null
pkill -f sara_autonomous 2>/dev/null

# Check dependencies
echo "🔍 Checking dependencies..."
python3 -c "import flask" 2>/dev/null || {
    echo "⚠️  Installing Flask..."
    pip3 install flask flask-cors
}

echo "🌐 Simple Sara Web Interface:"
echo "📍 http://127.0.0.1:8890"
echo "⚡ Reliable responses (no streaming issues)"
echo "⏹ Working stop controls
echo "🧠 Direct command execution"
echo ""

# Change to correct directory
cd /home/godfather/.openclaw/workspace

# Start the SIMPLE web app
python3 sara_simple.py