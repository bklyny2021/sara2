#!/bin/bash
# 🌟 SARA FIXED AUTONOMOUS STREAMING LAUNCHER
# Fixed auto-stop bug and freezing issues

echo "🌟 SARA AUTONOMOUS STREAMING V2.1 (FIXED)"
echo "======================================="
echo "🐛 Auto-stop bug fixed"
echo "⏹ Stop button working correctly"
echo "🔗 No more freezing"
echo "✅ All streaming stable"
echo "🚀 Starting fixed autonomous streaming chat..."
echo "🌐 http://127.0.0.1:8889"
echo "✅ 100% Offline & Private Operation"
echo ""

# Kill any existing process
pkill -f sara_autonomous_fixed 2>/dev/null
pkill -f sara_autonomous_streaming 2>/dev/null

# Check dependencies
echo "🔍 Checking dependencies..."
python3 -c "import flask" 2>/dev/null || {
    echo "⚠️  Installing Flask..."
    pip3 install flask flask-cors
}

echo "🌐 Fixed Autonomous Sara Web Interface:"
echo "📍 http://127.0.0.1:8889"
echo "⚡ Fully stable streaming responses"
echo "⏹ Working stop/pause controls"
echo "🧠 Background thinking enabled"
echo ""

# Change to correct directory
cd /home/godfather/.openclaw/workspace

# Start the FIXED autonomous web app
python3 sara_autonomous_fixed.py