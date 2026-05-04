#!/usr/bin/env python3
"""
Voice Note Transcription Script (A1 PERSONAL - OPTIMIZED)

LOCATION: /root/3_core_tools/hermes/data/scripts/transcribe_voice.py
AGENT: A1 (Hermes Agent / Global Orchestrator)

Uses local whisper.cpp tiny model for fast transcription (~1.2s).
Requires ffmpeg for OGG to WAV conversion.

Usage: python3 transcribe_voice.py <audio_file_path>
Output: JSON with transcription text and metadata
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# whisper.cpp paths
WHISPER_CLI = "/tmp/whisper.cpp/build/bin/whisper-cli"
WHISPER_MODEL = "/tmp/whisper.cpp/models/ggml-tiny.en.bin"
FFMPEG = "ffmpeg"

def transcribe_audio(audio_path):
    """Transcribe audio file using local whisper.cpp."""
    
    if not os.path.exists(audio_path):
        return {"error": f"Audio file not found: {audio_path}"}
    
    if not os.path.exists(WHISPER_CLI):
        return {"error": f"whisper-cli not found: {WHISPER_CLI}"}
    
    if not os.path.exists(WHISPER_MODEL):
        return {"error": f"Model not found: {WHISPER_MODEL}"}
    
    # Convert to WAV (whisper.cpp doesn't support OGG)
    wav_path = "/tmp/transcribe_temp.wav"
    try:
        # Convert to 16kHz mono WAV
        cmd = [FFMPEG, "-i", audio_path, "-ar", "16000", "-ac", "1", wav_path, "-y", "-loglevel", "error"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return {"error": f"FFmpeg failed: {result.stderr}"}
        
        # Run whisper.cpp
        cmd = [WHISPER_CLI, "-m", WHISPER_MODEL, "-f", wav_path, "--no-prints", "--output-txt", "--output-file", "/tmp/whisper_output"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return {"error": f"whisper failed: {result.stderr}"}
        
        # Read transcription output
        txt_path = "/tmp/whisper_output.txt"
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                text = f.read().strip()
        else:
            # Fallback: parse stdout
            text = result.stdout.strip()
        
        # Cleanup
        if os.path.exists(wav_path):
            os.remove(wav_path)
        if os.path.exists(txt_path):
            os.remove(txt_path)
        
        return {
            "success": True,
            "text": text,
            "language": "en",
            "audio_file": audio_path,
            "timestamp": Path(audio_path).stat().st_mtime,
            "engine": "whisper.cpp-tiny",
            "time": "~1.2s"
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Transcription timeout"}
    except Exception as e:
        return {"error": str(e), "audio_file": audio_path}

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Transcribe voice notes using local whisper.cpp (A1 optimized)')
    parser.add_argument('audio_file', help='Path to audio file (OGG, MP3, WAV, etc.)')
    
    args = parser.parse_args()
    
    result = transcribe_audio(args.audio_file)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
