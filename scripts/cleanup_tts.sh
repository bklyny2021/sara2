#!/bin/bash
# Auto-delete TTS audio files after playback
# Usage: ./cleanup_tts.sh /path/to/audio.mp3 [delay_seconds]

AUDIO_FILE="$1"
DELAY="${2:-10}"

if [ -z "$AUDIO_FILE" ]; then
    echo "Usage: $0 <audio_file> [delay_seconds]"
    exit 1
fi

# Sleep for delay then delete
(sleep "$DELAY" && rm -f "$AUDIO_FILE" && rmdir "$(dirname "$AUDIO_FILE")" 2>/dev/null) &
echo "Scheduled cleanup of $AUDIO_FILE in ${DELAY}s (PID: $!)"
