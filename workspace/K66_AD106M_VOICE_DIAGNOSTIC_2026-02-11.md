# 🎤 K66 MICROPHONE & AD106M AUDIO DIAGNOSTIC

## 🔊 HARDWARE SPECIFICATIONS:

### 📱 **INPUT DEVICE**: K66 USB-C Microphone
- **Type**: USB-C professional microphone
- **Interface**: Direct USB-C connection
- **Purpose**: High-quality voice input

### 🔊 **OUTPUT SPEAKER**: AD106M Pro
- **Type**: Professional speaker system
- **Designation**: AD106M Pro
- **Purpose**: Audio output/Sara voice

---

## ⚠️ **ISSUE IDENTIFIED**:
**Command center starts but Sara not talking**

### 🎯 **DIAGNOSTIC PRIORITIES**:
1. **K66 microphone input detection**
2. **AD106M speaker output configuration**  
3. **Audio routing and device mapping**
4. **Voice system process status**

---

## 🔍 **IMMEDIATE DIAGNOSTIC STEPS**:

### Step 1: **Hardware Detection Check**
```bash
# Find K66 microphone
arecord -l | grep -i k66

# Find AD106M speaker
aplay -l | grep -i ad106

# List all audio devices
cat /proc/asound/cards
```

### Step 2: **Audio Configuration Verify**
```bash
# Check default audio settings
pactl info | grep -E "(Default Sink|Default Source)"

# Check available devices
pactl list sources | grep -i k66
pactl list sinks | grep -i ad106
```

### Step 3: **Voice Process Status**
```bash
# Check if voice agent is running
ps aux | grep voice

# Check audio processes running
ps aux | grep -E "(pulse|alsa|audio)"
```

---

## 🛠️ **EXPECTED FIXES NEEDED**:

### Fix A: **Device-Specific Audio Routing**
- Map K66 as default input source
- Route AD106M as default output sink
- Configure pulseaudio for USB devices
- Set up proper audio routing

### Fix B: **Voice System Configuration**
- Update voice config for K66/AD106M hardware
- Test audio pipeline with these devices
- Verify wake word detection with K66
- Test TTS output to AD106M

### Fix C: **Process Management**
- Ensure voice agent process starts correctly
- Verify audio device initialization
- Test wake word activation loop
- Confirm TTS voice output

---

## 🚀 **QUICK LAUNCH TEST**:
```bash
# Test K66 microphone
arecord -D plughw:2,0 -d 5 -f cd /tmp/test_k66.wav
aplay /tmp/test_k66.wav

# Test AD106M speaker  
echo "Testing AD106M speaker" | espeak --stdout | aplay -D plughw:1,0

# Launch voice system with device hint
cd /home/godfather/.openclaw/workspace/sara
python3 start_voice_system.py
```

---

## 📊 **COMPATIBILITY ASSESSMENT**:
- **K66 USB-C**: Should work as USB audio input device
- **AD106M Pro**: Professional speaker system compatibility
- **Linux Support**: USB audio class compatible
- **Voice Integration**: Standard ALSA/PulseAudio support

---

## 🔍 **DEBUGGING FOCUS**:
1. **System recognizes devices?**
2. **Voice system starts but no sound?** 
3. **Audio routing misconfiguration?**
4. **Hardware-specific drivers needed?**

---
*Created: 2026-02-11 09:02 EST*
*Hardware: K66 USB-C mic + AD106M Pro speaker*
*Issue: Voice system silent operation*