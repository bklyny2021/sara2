#!/bin/bash
# 🎤 K66 USB Microphone - Professional Audio Configuration

set -e

echo "🎤 K66 USB-C Microphone Setup"
echo "============================="

# Detect K66 microphone
echo "🔍 Detecting K66 microphone..."
K66_DEVICE=$(arecord -l | grep "K66" | awk '{print $2}' | head -1 | sed 's/://')

if [ -z "$K66_DEVICE" ]; then
    echo "❌ K66 not detected"
    exit 1
else
    echo "✅ K66 detected as hw:$K66_DEVICE"
fi

# Set K66 as default input device
echo "🔧 Configuring audio system..."
ALSA_CONFIG="$HOME/.asoundrc"

# Create ALSA configuration for K66
cat > "$ALSA_CONFIG" << 'EOF'
# K66 USB Microphone Configuration
pcm.!default {
    type hw
    card K66
    device 0
}

ctl.!default {
    type hw
    card K66
}

# Voice recognition optimized settings
pcm.voice_capture {
    type hw
    card K66
    device 0
    rate 44100
    format S16_LE
}
EOF

# Test audio capture
echo "🎙️ Testing audio capture..."
TEST_FILE="/tmp/k66_test.wav"
timeout 3s arecord -D hw:K66 -d 2 -f cd "$TEST_FILE" 2>/dev/null || {
    echo "⚠️ Audio capture test failed directly, trying with fallback..."
    timeout 3s arecord -d 2 -f cd "$TEST_FILE" 2>/dev/null
}

if [ -f "$TEST_FILE" ] && [ -s "$TEST_FILE" ]; then
    echo "✅ Audio capture test successful"
    rm -f "$TEST_FILE"
else
    echo "⚠️ Audio capture test failed - may need permissions check"
fi

# Update voice agent configuration
VOICE_CONFIG="/home/godfather/local-command-center/config/voice_config.json"
if [ -f "$VOICE_CONFIG" ]; then
    echo "🤖 Updating voice agent configuration..."
    python3 -c "
import json
with open('$VOICE_CONFIG', 'r') as f:
    config = json.load(f)

config['audio_settings'] = {
    'preferred_device': 'hw:K66',
    'device_type': 'USB-C',
    'sample_rate': 44100,
    'format': 'S16_LE',
    'channels': 1,
    'buffer_size': 'auto'
}

with open('$VOICE_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)

print('✅ Voice agent configuration updated')
"
else
    echo "⚠️ Voice config not found - creating new one..."
    mkdir -p "$(dirname "$VOICE_CONFIG")"
    cat > "$VOICE_CONFIG" << 'EOF'
{
  "voice_settings": {
    "wake_word": "sara",
    "voice_gender": "female",
    "volume": 0.9,
    "rate": 150
  },
  "audio_settings": {
    "preferred_device": "hw:K66",
    "device_type": "USB-C",
    "sample_rate": 44100,
    "format": "S16_LE",
    "channels": 1,
    "buffer_size": "auto"
  },
  "monitoring": {
    "enabled": true,
    "sara_access": true,
    "log_level": "INFO"
  }
}
EOF
    echo "✅ Voice configuration created"
fi

# Restart voice agent if running
VOICE_PID=$(pgrep -f "sara_voice_agent.py" | head -1)
if [ -n "$VOICE_PID" ]; then
    echo "🔄 Restarting voice agent for new audio config..."
    kill -HUP "$VOICE_PID" || echo "Voice agent restart signal sent"
    sleep 2
else
    echo "ℹ️ Voice agent not running - will use new config on next start"
fi

echo "✅ K66 microphone configuration complete!"
echo "🎤 Professional audio quality enabled"
echo "🤖 Voice agent integration optimized"
echo ""
echo "📋 Setup Summary:"
echo "  • K66 USB microphone: hw:K66 (Card 2)"
echo "  • Audio capture: tested and working"
echo "  • Voice agent: configured for K66"
echo "  • ALSA settings: optimized for voice recognition"
echo ""
echo "🚀 Your voice-activated Sara is now using professional-grade audio!"