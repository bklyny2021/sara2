#!/bin/bash
# 🌟 SARA AUTONOMOUS STREAMING LAUNCHER
# Full streaming responses with stop controls

echo "🌟 SARA AUTONOMOUS STREAMING V2"
echo "================================="
echo "🚀 Starting autonomous streaming chat..."
echo "⏹ Stop/Pause controls available"
echo "🧠 Background thinking enabled"
echo "✅ 100% Offline & Private Operation"
echo ""

# Check dependencies
echo "🔍 Checking dependencies..."
python3 -c "import flask" 2>/dev/null || {
    echo "⚠️  Installing Flask..."
    pip3 install flask flask-cors
}

echo "🌐 Autonomous Sara Web Interface:"
echo "📍 http://127.0.0.1:8889"
echo "⚡ Full streaming responses"
echo "⏹ Stop button for interruption"
echo "🧠 Background thinking"
echo ""

# Change to correct directory
cd /home/godfather/.openclaw/workspace

# Start the autonomous web app
python3 sara_autonomous_streaming.py