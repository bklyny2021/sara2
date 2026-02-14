# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## TTS / Voice Configuration

### ElevenLabs Setup (Active)
- **API Key**: Configured
- **Voice**: Caribbean female (XB0fDUnXU5powFXDhCwa)
- **Model**: eleven_multilingual_v2
- **Auto-delete**: Enabled (10 seconds after playback)
- **Status**: Ready for voice replies

### Voice Agent
- **Name**: SARA Voice
- **Type**: Real-time voice conversation
- **TTS**: ElevenLabs Caribbean female
- **STT**: Whisper/Vosk local
- **Note**: Separate from this text chat agent
