#!/bin/bash
# 🚀 SARA WEB INTERFACE LAUNCHER
# Starts beautiful web-based chat interface

echo "🌟 SARA OFFLINE WEB INTERFACE"
echo "=============================="
echo "🚀 Starting web server..."

# Check dependencies
echo "🔍 Checking dependencies..."
python3 -c "import flask" 2>/dev/null || {
    echo "⚠️  Installing Flask..."
    pip3 install flask flask-cors
}

echo "📋 Starting Sara's Web Interface..."
echo "🌐 Opening http://127.0.0.1:8890"
echo "💚 100% Offline & Private Operation"
echo "🤖 SaraBoo1-fixed AI personality"
echo ""

# Change to correct directory
cd /home/godfather/.openclaw/workspace

# Start the web app
python3 sara_web_app.py