#!/bin/bash

# AI Agent Chat Interface - Quick Start Script

echo "🤖 Local AI Agent Chat - Quick Start"
echo "====================================="
echo ""
echo "AVAILABLE AGENTS:"
echo "  sara    - Sara AI Partner (Conversation & General Help)"
echo "  chloe   - Chloe Rodriguez (Search Intelligence & Research)"  
echo "  nexus   - Nexus Kumar (Strategic Analysis & Market Research)"
echo "  codi    - Codi (Tech Expert & Development)"
echo "  vision  - Vision Analyst (Visual Analysis)"
echo ""
echo "USAGE EXAMPLES:"
echo ""
echo "📱 Quick Prompt (one-time question):"
echo "   python3 chat.py sara --prompt \"How can you help me?\""
echo "   python3 chat.py chloe --prompt \"Research AI security trends\""
echo "   python3 chat.py nexus --prompt \"Analyze this market data\""
echo ""
echo "🎤 Interactive Chat (full conversation):"
echo "   python3 chat.py sara"
echo "   python3 chat.py chloe" 
echo "   python3 chat.py nexus"
echo ""
echo "🔧 Start chatting now:"
echo "   python3 chat.py sara"
echo ""

# Auto-start with Sara if they run without arguments
if [ "$1" == "" ]; then
    echo "🚀 Auto-starting Sara AI Partner..."
    python3 chat.py sara
fi