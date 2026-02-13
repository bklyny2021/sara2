# SARA AI Assistant

**SARA** (Self-Aware Response Agent) — A locally-hosted AI assistant with offline voice, memory, and conversation continuity.

## What SARA Does

SARA is your personal AI assistant that runs **entirely on your machine** — no cloud dependencies, no API keys needed, complete privacy.

### Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Voice Wake Word** | Say "Sara" to activate | ✅ Working |
| **Offline Speech Recognition** | Vosk model (local) | ✅ Working |
| **Online Speech Recognition** | Google Speech API | ✅ Working |
| **Offline Voice** | espeak-ng (female-ish) | ✅ Working |
| **Online Voice** | gTTS (female Google voice) | ✅ Working |
| **Conversation Memory** | Remembers you (Boo) across sessions | ✅ Working |
| **Follow-up Mode** | Continue conversation without wake word (15s) | ✅ Working |
| **Hybrid Input** | Speak OR type in any mode | ✅ Working |
| **Web Interface** | Chat via browser (port 8892) | ✅ Working |
| **Voice Agent** | Terminal-based voice control | ✅ Working |
| **Auto Offline Switch** | Seamlessly switches when internet drops | ✅ Working |
| **Code Handling** | Shows Python in boxes, doesn't speak code | ✅ Working |

## How It Works

### Online Mode
1. **You speak "Sara"** → Google Speech API hears you
2. **Ask question** → Google Speech transcribes
3. **Ollama (local)** → Processes with sara-v2 model
4. **gTTS responds** → Female voice + text

### Offline Mode
1. **You speak "Sara"** → Vosk (local) hears you
2. **Ask question** → Vosk transcribes locally
3. **Ollama (local)** → Same model, no internet needed
4. **espeak-ng responds** → Female-ish voice + text

### Text Input
Always available! Press Enter and type:
- `sara` - Wake up
- `hello` - Ask anything
- `quit` / `exit` / `stop` - Shutdown

## Installation

### Requirements
```bash
# Python packages
pip3 install flask gtts pyttsx3 vosk requests speech_recognition

# System tools (Fedora)
sudo dnf install mpg123 espeak-ng

# Ollama models
ollama pull sara-v2:latest
```

### Setup
```bash
# Clone this repo
git clone https://github.com/bklyny2021/sara2.git
cd sara2

# Start SARA
python3 workspace/sara_web_offline.py  # Web interface
python3 workspace/sara/agents/sara-voice/sara_voice_agent.py  # Voice agent
```

## Usage

### Web Interface
- Open: http://localhost:8892
- Type or speak (with mic)
- See conversation history
- Python code shown in green boxes

### Voice Agent
```bash
python3 workspace/sara/agents/sara-voice/sara_voice_agent.py
```
- Say "Sara" to wake
- Speak your question
- Listen to response
- Or type instead

### Files
| File | Purpose |
|------|---------|
| `sara_voice_agent.py` | Main voice agent with offline/online support |
| `sara_web_offline.py` | Web interface with memory |
| `sara_memory.json` | Conversation history (auto-saved) |
| `sara_chat.log` | Text log of conversations |

## Memory System

SARA remembers:
- Your name (Boo)
- Your role (admin)
- Last 10 conversations
- Context between sessions

Stored locally in:
- `/logs/sara_memory.json`
- `/logs/sara_chat.log`

## Architecture

```
User Input (Voice/Text)
    ↓
Speech Recognition (Google/Vosk)
    ↓
Ollama LLM (sara-v2)
    ↓
Text-to-Speech (gTTS/espeak-ng/pyttsx3)
    ↓
User Hears + Sees in Web
```

## Configuration

### Change Wake Word
Edit `sara_voice_agent.py`:
```python
self.wake_word = "sara"  # Change to any word
```

### Change Voice Speed
```python
# In speak() function
engine.setProperty('rate', 150)  # Lower = slower
```

### Add More Offline Languages
Download Vosk models from:
https://alphacephei.com/vosk/models

Extract to:
`workspace/sara/agents/sara-voice/models/`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "No TTS available" | Install espeak-ng: `sudo dnf install espeak-ng` |
| "Vosk not available" | Download model: see Installation |
| Mic not working | Use keyboard input instead |
| ALSA errors | Normal on Fedora, doesn't affect functionality |
| gTTS fails | Offline mode activated, espeak used instead |

## Security & Privacy

- **100% Local**: No data leaves your machine
- **No API Keys**: All services run locally
- **Private Repo**: Your code, your control
- **Offline Capable**: Works without internet

## Commands Cheat Sheet

### Voice Agent
| Command | Action |
|---------|--------|
| Say "sara" | Wake up |
| Say "hello how are you" | Ask anything |
| Type "sara" + Enter | Wake up (offline) |
| Type message + Enter | Send text |
| "quit" / "exit" | Shutdown |

### Web Chat
| Command | Action |
|---------|--------|
| Type in box | Send message |
| Enter key | Submit |
| "save this" | SARA remembers |
| "who am i" | SARA recalls you're Boo |

## Development

### Adding Features
1. Edit `sara_voice_agent.py`
2. Test locally
3. Commit: `git commit -am "New feature"`
4. Push: `git push origin master`

### Modifying Responses
Edit the LLM prompt in `query_llm()`:
```python
prompt = f"You are Sara... {context}\nUser: {command}\nSara:"
```

## License

MIT - Your code, your rules.

## Credits

- Vosk: Offline speech recognition
- Ollama: Local LLM inference
- gTTS: Google Text-to-Speech
- espeak-ng: Open source TTS

---

**Private Repository** | **Created by Boo** | **Powered by Coffee ☕**
