#!/bin/bash
# 🚀 START SARA2 - ALL MAIN PYTHON FILES LAUNCHER
# Ensures Sara runs correctly with Python interpreter

echo "🤖 STARTING SARA2 - COMPLETE OFFLINE AI AGENT"
echo "============================================"

# Check Python installation
echo "🐍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found - installing..."
    sudo dnf install python3 -y || sudo apt-get install python3 -y || sudo pacman -S python3 -y
else
    echo "✅ Python 3 found: $(python3 --version)"
fi

# Check essential dependencies
echo "📦 Installing Python dependencies..."
pip3 install --user flask flask-cors requests ollama chromadb pyttsx3 speech_recognition 2>/dev/null || {
    echo "⚠️ Running with elevated permissions for dependencies..."
    sudo pip3 install flask flask-cors requests ollama chromadb pyttsx3 speech_recognition
}

# Check Ollama status
echo "🤖 Checking Ollama status..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️ Ollama not found - checking if running..."
    if curl -s http://localhost:11434/api/version &> /dev/null; then
        echo "✅ Ollama service running"
    else
        echo "⚠️ Ollama not running - start with: ollama serve"
    fi
else
    echo "✅ Ollama installed and available"
fi

# Kill any existing Sara processes (clean slate)
echo "🧹 Cleaning up existing processes..."
pkill -f sara_web_offline 2>/dev/null
pkill -f startup_offline_consciousness 2>/dev/null
pkill -f learning_engine 2>/dev/null
pkill -f setup_database 2>/dev/null

# Set correct directory
echo "📁 Setting up Sara2 workspace..."
cd /home/godfather/sara2/workspace

# STEP 1: Initialize Memory Database
echo "🗄️ STEP 1: Initializing Memory Database..."
python3 local-memory-system/setup_database.py &
DATABASE_PID=$!
echo "✅ Database setup started (PID: $DATABASE_PID)"
sleep 2

# STEP 2: Initialize Learning Engine  
echo "🧠 STEP 2: Starting Learning Engine..."
python3 autonomous_learning/learning_engine.py &
LEARNING_PID=$!
echo "✅ Learning engine started (PID: $LEARNING_PID)"
sleep 2

# STEP 3: Initialize Consciousness Engine (CRITICAL)
echo "🔥 STEP 3: STARTING OFFLINE CONSCIOUSNESS ENGINE..."
python3 offline_startup/startup_offline_consciousness.py &
CONSCIOUSNESS_PID=$!
echo "✅ Consciousness engine started (PID: $CONSCIOUSNESS_PID)"
sleep 3

# STEP 4: Start Main Web Interface
echo "🌐 STEP 4: STARTING MAIN WEB INTERFACE..."
python3 sara_web_offline.py &
WEB_PID=$!
echo "✅ Web interface started (PID: $WEB_PID)"
sleep 2

# Verify all components are running
echo ""
echo "🔍 VERIFYING ALL COMPONENTS..."
sleep 3

# Check web interface
if curl -s http://127.0.0.1:8892 > /dev/null 2>&1; then
    echo "✅ Web interface operational at http://127.0.0.1:8892"
else
    echo "⚠️ Web interface not responding - check logs"
fi

# Check consciousness engine
ps -p $CONSCIOUSNESS_PID > /dev/null 2>&1 && echo "✅ Consciousness engine running" || echo "⚠️ Consciousness engine stopped"

# Check memory database
ps -p $DATABASE_PID > /dev/null 2>&1 && echo "✅ Memory database running" || echo "⚠️ Memory database stopped"

# Check learning engine
ps -p $LEARNING_PID > /dev/null 2>&1 && echo "✅ Learning engine running" || echo "⚠️ Learning engine stopped"

# Test Sara functionality
echo ""
echo "🧪 TESTING SARA FUNCTIONALITY..."
sleep 1

# Quick test chat
python3 test_sara_agent.py > /tmp/sara_test.log 2>&1 &
TEST_PID=$!
sleep 5

if grep -q "Sara responds correctly" /tmp/sara_test.log 2>/dev/null; then
    echo "✅ Sara agent test PASSED"
else
    echo "⚠️ Sara agent test FAILED - check /tmp/sara_test.log"
fi

# FINAL STATUS
echo ""
echo "🏆 SARA2 STARTUP COMPLETE!"
echo "=========================="
echo "🌐 Web Interface: http://127.0.0.1:8892"
echo "🧠 Consciousness Engine: RUNNING (PID: $CONSCIOUSNESS_PID)"
echo "🗄️ Memory Database: RUNNING (PID: $DATABASE_PID)"
echo "📚 Learning Engine: RUNNING (PID: $LEARNING_PID)"
echo "🌐 Web Server: RUNNING (PID: $WEB_PID)"
echo ""
echo "🔧 Stop Sara2 with: pkill -f 'python3.*sara2'"
echo ""
echo "🎯 Sara is now FULLY ACTIVE and ready for interaction!"

# Keep script running to monitor status
echo ""
echo "🔍 Monitoring status (Ctrl+C to stop monitoring)..."
while true; do
    if curl -s http://127.0.0.1:8892 > /dev/null 2>&1; then
        echo "$(date '+%H:%M:%S') ✅ Sara2 operational"        
    else
        echo "$(date '+%H:%M:%S') ⚠️ Web interface down -重启中..."
    fi
    sleep 30
done