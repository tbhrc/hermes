# Whisper Transcription Benchmarks

## Test Results (2026-05-03)

### Test Clip 1: 9.85s voice note
- **OpenAI API**: 2.848s real time
- **whisper.cpp base.en**: 2.313s real time
- **whisper.cpp tiny.en**: 1.240s real time

### Test Clip 2: 26s voice note (~20s actual speech)
- **whisper.cpp tiny.en**: 1.727s real time
  - Output: "Alright, so this is only a few seconds. It's only like five or six seconds of talking. No, now it's going up to probably fifteen. Now let's test how long it take for this transcription. Total is twenty seconds."
  - Accuracy: Correct transcription
- **OpenAI API**: 2.086s real time
  - Slower than local even for longer clips

## Conclusion
Local whisper.cpp tiny model is faster than OpenAI API for all tested clip lengths (10s to 26s). Network latency makes API slower even when processing longer audio.

## Environment
- Model: ggml-tiny.en.bin (whisper.cpp)
- Conversion: ffmpeg (OGG Opus → 16kHz WAV)
- API Key: OPENAI_API_KEY_AOS from /root/.env
- Note: /root/.env has Windows \r\n line endings; use Python to read: `python3 -c "exec(open('/root/.env').read()); print(OPENAI_API_KEY_AOS)"`
