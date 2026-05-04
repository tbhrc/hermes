# Whisper.cpp Setup Recipe
Steps to compile whisper.cpp and download tiny.en model for local transcription.

## Compile from Source
```bash
cd /tmp
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
mkdir build && cd build
cmake ..
make -j$(nproc)
# Binary location: /tmp/whisper.cpp/build/bin/whisper-cli
```

## Download Tiny English Model
```bash
cd /tmp/whisper.cpp/models
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
# Model size: ~142MB
```

## Verify
```bash
/tmp/whisper.cpp/build/bin/whisper-cli -m /tmp/whisper.cpp/models/ggml-tiny.en.bin -f test.wav
```