# Sara2 Voice Agent - Changelog

## Version 2.1.0 - 2026-02-25

### Core Features Added

#### 1. System Discovery Tools (Auto-detect any PC)
Sara2 now can discover system information dynamically on ANY PC she runs on:
- **Time**: `date "+%I:%M %p %Z on %A, %B %d"` → "12:49 PM EST on Wednesday, February 25"
- **Date**: `date "+%A, %B %d, %Y"` → "Wednesday, February 25, 2026"
- **RAM**: `free -h` → "Total: 31Gi, Used: 8.2Gi, Free: 22Gi"
- **Disk Space**: `df -h` → Shows all mounted filesystems
- **IP Address**: `ip addr show | grep "inet " | head -3` → Shows network interfaces
- **CPU Info**: `lscpu | head -10` → CPU model, cores, architecture
- **OS Info**: `cat /etc/os-release | grep -E "^(NAME|VERSION)"` → Fedora Linux 43
- **Hostname**: `hostname` → Any PC name she's on
- **Kernel**: `uname -r` → Linux kernel version

**How it works**: When you ask "what time is it", Sara generates a bash command, executes it, and speaks the ACTUAL result. No hardcoded info.

#### 2. Weather Auto-Search
- "What's the weather?" → Automatically searches web for weather
- "Weather in [city]" → Searches for specific city weather
- No longer says "Let me check the web" - actually does it

#### 3. Ultra-Concise Response Mode
- MAX 1-2 sentences per response
- NO volunteering personal information unless explicitly asked
- NO "I remember..." unless you ask what she remembers
- Answer's ONLY what was asked, then stops

#### 4. Personal Info Protection
- `get_conversation_context()` now defaults to NOT including personal facts
- Only includes birthday/age when you say "when is my birthday" or "what do you remember about me"
- Stops randomly mentioning age/birthday from memory

#### 5. Speech Formatting Cleanup
- Removes markdown asterisks (`**bold**` → "bold")
- Removes underscores (`_italic_` → "italic")
- Removes headers (`# Title` → "Title")
- Stops saying "astride" from markdown

#### 6. Joke/Casual Mode
- Detects: "joke", "funny", "make me laugh", "tell me something"
- Switches to relaxed, personable prompt for humor
- Warm, friendly responses instead of rigid system mode

#### 7. Repeat Penalty System
- Tracks last 5 responses
- Detects similar responses (prefix/suffix matching)
- Adds variation prefixes: "Got it.", "Understood."
- Prevents robotic repetition

### Control & Monitoring

#### 8. Web UI (Port 8081)
- Access at: `http://localhost:8081`
- View conversation history
- View live logs
- Send commands (no voice needed)
- Changed from 8080 → 8081 to avoid conflicts

#### 9. Control Script (`sara2-control.py`)
```bash
python3 /home/sarabot/sara2/sara2-control.py start    # Start
python3 /home/sarabot/sara2/sara2-control.py stop     # Stop
python3 /home/sarabot/sara2/sara2-control.py restart  # Restart
python3 /home/sarabot/sara2/sara2-control.py status   # Status + Web UI check
python3 /home/sarabot/sara2/sara2-control.py logs     # Show last 20 lines
```

#### 10. Auto-Restart Watchdog
- Cron job: `*/1 * * * * /home/sarabot/sara2/auto-restart.sh`
- Monitors every 60 seconds
- Restarts if process not found
- Restarts if Web UI not responding
- Logs to: `/home/sarabot/.openclaw/workspace/logs/sara2_watchdog.log`

#### 11. Conversation Mode
- After response, stays listening for 2 minutes
- No need to repeat wake word "Sara" 
- Exit phrases: "that's all", "bye", "stop listening", "done", "end"
- Automatically returns to wake-word mode after timeout

### Bug Fixes

#### 12. Missing Attribute Error
- Fixed: `'SaraVoiceAgent' object has no attribute 'workspace_dir'`
- Added in `__init__`: `self.workspace_dir = os.path.join(self.sara_memory_dir, "workspace")`
- Creates subdirectories: `executed_commands/`, `executed_scripts/`

#### 13. Duplicate Code Removal
- Fixed duplicate `requests.post` block in `query_llm()` causing syntax errors

#### 14. Code Execution Results
- `extract_speakable_text()` now accepts `executed_result` parameter
- `extract_and_execute_commands()` returns actual output, not just command name
- Execution results are now spoken (not "I've written the code")

#### 15. Time Awareness
- Current timestamp injected into LLM prompt automatically
- Knows local time without running commands

### LLM Prompt Updates

#### System Prompt Structure:
```
You are Sara, an AI assistant running on a Linux PC.

AVAILABLE TOOLS:
- System time: ```bash
date
```
- RAM usage: ```bash
free -h
```
... (etc)

ABSOLUTE RULES:
1. Answer ONLY what was asked - ONE short sentence
2. NEVER make up system info - USE THE TOOLS ABOVE to discover it
...
```

#### For Jokes/Casual Chat:
```
You are Sara, Boo's fun AI assistant.

RULES:
1. For jokes - be clever and concise, max 2-3 sentences
2. For casual chat - be friendly and brief
...
```

### Files Created/Modified

**New Files:**
- `/home/sarabot/sara2/sara2-control.py` - Control script
- `/home/sarabot/sara2/auto-restart.sh` - Watchdog script
- `/home/sarabot/sara2/UPDATES.md` - This changelog

**Modified:**
- `/home/sarabot/sara2/workspace/sara/agents/sara-voice/sara_voice_agent.py` - Core agent

### Usage Examples

| You Say | Sara Does |
|---------|-----------|
| "Sara, what's the time?" | Executes `date`, speaks actual time |
| "How much RAM do I have?" | Runs `free -h`, tells you exact usage |
| "What's my IP?" | Checks `ip addr`, reports interfaces |
| "Tell me a joke" | Switches to fun mode, tells joke |
| "What's the weather?" | Searches web, reports weather |
| "What's my birthday?" | Only THEN tells you October 8th, 1968 |
| "How are you?" | Brief answer, NO age/birthday mention |

### Technical Architecture

```
┌─────────────────────────────────────────┐
│           Voice Input (Vosk)            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Command Processing               │
│  (Direct commands → Shell execution)    │
│  (Complex queries → LLM)                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         LLM (Ollama/sara-uncensored)   │
│         Query with system tools prompt  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│    Execute Commands → Get Real Results  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      TTS (ElevenLabs) + Output        │
└─────────────────────────────────────────┘
         │
    ┌────▼────┐
    │ Web UI  │ ← Flask on port 8081
    └─────────┘
```

---
**Last Updated:** 2026-02-25 01:03 EST
**Version:** 2.1.0
**Status:** Stable, running with auto-restart
