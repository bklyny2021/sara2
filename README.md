# SARA AI Assistant — STANDALONE

**SARA** (Self-Aware Response Agent) — A locally-hosted AI assistant with offline voice, memory, and conversation continuity.

> 🚀 **STANDALONE**: SARA2 is a fully self-contained, offline-capable AI agent. No external dependencies, no cloud APIs required, no OpenClaw integration. Pure local intelligence.

> 📅 **Coming Soon — Stage 2**: Tool-calling architecture (file operations, web search, browser control, shell execution) — bringing OpenClaw-level capabilities directly into SARA2.

## Architecture Philosophy

**SARA2 is STANDALONE** — designed from the ground up to operate independently:
- ✅ **No external services required** after initial setup
- ✅ **Offline-first** — works without internet
- ✅ **Self-hosted** — your data never leaves your machine
- ✅ **Expanding** — Stage 2 will add full tool-calling capability

## What This Repo Contains

| Path | Description | Status |
|------|-------------|--------|
| `voice-agent/sara_voice_agent.py` | Main voice agent (offline + online) | ✅ |
| `voice-agent/models/vosk-model/` | Vosk offline speech model (39MB) | ✅ |
| `voice-agent/config.json` | Voice configuration | ✅ |
| `voice-agent/*.backup` | Previous versions | ✅ |
| `README.md` | This file | ✅ |

### What's in This Repo
- ✅ **Voice agent code** with hybrid online/offline support
- ✅ **Vosk model** for offline speech recognition
- ✅ **Configuration files** for voice settings

### What's NOT in This Repo (Install Separately)
- ❌ `sara_web_offline.py` — Web interface (separate install)
- ❌ Ollama models — Download with `ollama pull sara-v2`
- ❌ Python packages — Install via pip
- ❌ System tools — Install via dnf/apt
- ❌ Logs — Auto-generated locally (not uploaded)

## Features

| Feature | Description | Requires Internet |
|---------|-------------|-------------------|
| **Voice Wake Word** | Say "Sara" to activate | No (Vosk) |
| **Offline Speech Recognition** | Vosk model (local) | No |
| **Online Speech Recognition** | Google Speech API | Yes |
| **Offline Voice** | espeak-ng (female-ish) | No |
| **Online Voice** | gTTS (female Google voice) | Yes |
| **Conversation Memory** | Remembers you (Boo) | No |
| **Hybrid Input** | Speak OR type | Either |
| **Follow-up Mode** | Continue conversation (15s) | Either |

## How It Works

### Online Mode
1. **You speak "Sara"** → Google Speech API hears you
2. **Ask question** → Google Speech transcribes
3. **Ollama (local)** → Processes with sara-v2 model
4. **gTTS responds** → Female voice + text

### Offline Mode
1. **You speak "Sara"** → Vosk (local, from this repo) hears you
2. **Ask question** → Vosk transcribes locally
3. **Ollama (local)** → Same model, no internet needed
4. **espeak-ng responds** → Female-ish voice + text

### Text Input
Always available! Press Enter and type:
- `sara` - Wake up
- `hello` - Ask anything  
- `quit` / `exit` / `stop` - Shutdown
- Type `sara` + Enter when offline

## Installation

### 1. Clone This Repo
```bash
git clone https://github.com/bklyny2021/sara2.git
cd sara2
```

### 2. Install Python Dependencies
```bash
pip3 install flask gtts pyttsx3 vosk requests speech_recognition pyaudio
```

### 3. Install System Tools (Fedora)
```bash
sudo dnf install mpg123 espeak-ng alsa-utils
```

### 4. Install Ollama Models (run these commands)
```bash
ollama pull sara-v2:latest     # Main model
# Or use any available:
ollama pull llama3.2:latest
```

### 5. Verify Vosk Model (should be in this repo)
```bash
ls voice-agent/models/vosk-model/am/final.mdl
# If missing, download from: https://alphacephei.com/vosk/models
```

## Usage

### Start Voice Agent
```bash
cd sara2
python3 voice-agent/sara_voice_agent.py
```

**Then:**
- Online: Say "sara" → speak your question → hear response
- Offline: Turn off WiFi → say "sara" → still works!
- Text: Press Enter → type "sara" → type question

### Web Interface (NOT in this repo - install separately)
To get web interface with code blocks, run:
```bash
# After cloning, also need:
pip3 install flask
python3 /home/sarabot/sara2/workspace/sara_web_offline.py  # From SARA2 main install
```

Then open: http://localhost:8892

## Configuration

### Change Path to Vosk Model
Edit `voice-agent/sara_voice_agent.py`:
```python
VOSK_MODEL_PATH = "/path/to/sara2/voice-agent/models/vosk-model"
```

### Change Wake Word
Edit same file:
```python
self.wake_word = "sara"  # Change to any word
```

### Change Voice Speed
```python
engine.setProperty('rate', 150)  # Lower = slower
```

## File Structure

```
sara2/
├── README.md                          # This file
├── voice-agent/
│   ├── sara_voice_agent.py           # ⭐ Main voice agent
│   ├── config.json                   # Voice settings
│   ├── enhanced_voice_agent.py       # Extended features
│   └── models/
│       └── vosk-model/               # ⭐ Offline speech model (39MB)
│           ├── am/final.mdl
│           ├── conf/
│           ├── graph/
│           └── ivector/
└── [other files not in repo]
    # These must be obtained separately:
    # - sara_web_offline.py (web interface)
    # - chat logs (auto-generated)
    # - memory files (auto-generated)
```

### Where Data is Stored (Local Machine Only)
- Conversation memory: `~/.openclaw/workspace/logs/sara_memory.json`
- Chat logs: `~/.openclaw/workspace/logs/sara_chat.log`
- Voice logs: Generated locally (not in repo)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "No TTS available" | `sudo dnf install espeak-ng` |
| "Vosk model not found" | Check `voice-agent/models/vosk-model/` exists, or download from https://alphacephei.com/vosk/models |
| Mic not working | Use keyboard (type instead) or check `alsamixer` |
| ALSA errors | Normal on Fedora, doesn't affect functionality |
| gTTS fails offline | Expected - auto-switches to espeak-ng |
| "Could not connect to Ollama" | Run `ollama serve` in another terminal |

### Offline Mode Not Working?

1. Check Vosk model exists:
```bash
ls voice-agent/models/vosk-model/am/final.mdl
```

2. Install missing packages:
```bash
pip3 install vosk pyaudio
sudo dnf install portaudio-devel
```

3. Test Vosk directly:
```python
from vosk import Model
model = Model("voice-agent/models/vosk-model")
print("Vosk loaded!")
```

## Architecture

```
User Input (Voice/Text)
    ↓
Speech Recognition (Google/Vosk)
    ↓
Ollama LLM (sara-v2) ← Must install separately
    ↓
Text-to-Speech (gTTS/espeak-ng/pyttsx3)
    ↓
User Hears + Sees response
```

## Code Handling

When Sara generates Python code:
- **Voice mode**: Speaks "[Python code shown in chat]", prints full code
- **Web mode** (if installed): Shows in green box with 🐍 border
- **Terminal**: Prints full code with ```python``` markers

## Security & Privacy

- ✅ **100% Local**: No data leaves your machine
- ✅ **No API Keys**: Voice works offline without Google
- ✅ **Private Repo**: Your code, your control
- ✅ **Offline Capable**: Works without internet
- ⚠️ Chat logs stored locally only

## Getting the Full System

This repo = **Voice Agent Only**

For complete system with:
- Web interface
- Memory persistence
- Full SARA2 integration

You need the separate **SARA2 codebase** (not in this repo due to size).

## Commands Cheat Sheet

### Voice Agent
| Command | Action |
|---------|--------|
| Say "sara" | Wake up (online or offline) |
| Speak question | Vosk (offline) or Google (online) transcribes |
| Type "sara" + Enter | Wake up with keyboard |
| Type message + Enter | Send text question |
| "quit" / "exit" | Shutdown gracefully |
| Ctrl+C | Force quit |

## Development

### Modify Voice Agent
1. Edit `voice-agent/sara_voice_agent.py`
2. Test: `python3 voice-agent/sara_voice_agent.py`
3. Backup auto-created: `sara_voice_agent.py.backup`

### Add Features
```python
# In speak() function, add:
if "your_trigger_word" in text:
    # Do something
    pass
```

## Credits

- **Vosk**: Offline speech recognition (alphacephei.com/vosk)
- **Ollama**: Local LLM inference (ollama.ai)
- **gTTS**: Google Text-to-Speech (online only)
- **espeak-ng**: Open source TTS (offline)
- **SARA**: Built by Boo with MAX assistance

## License

MIT License - Your code, your rules.

---

**Voice Agent Only** | **Private Repository** | **Offline Capable** | **☕ Powered**

*Last updated: Feb 12, 2026* - Fixed offline mode, Vosk integration, espeak-ng female voice
