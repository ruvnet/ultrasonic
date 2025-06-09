# 📁 Ultrasonic Agentics Examples

This directory contains sample media files and example scripts for testing and learning the Ultrasonic Agentics steganography framework.

## 🎵 Sample Media Files

### sample_audio.mp3
- **Description**: Crowd cheering sound effect
- **Format**: MP3 (MPEG Audio Layer III)
- **Duration**: 27.74 seconds
- **Bit Rate**: 128 kbps
- **Sample Rate**: 44.1 kHz
- **Channels**: Joint Stereo
- **Size**: 434 KB
- **Source**: Sample-Videos.com
- **License**: Free for testing and development
- **Status**: Clean file (no embedded commands)

### sample_video.mp4
- **Description**: Big Buck Bunny animated short film (clip)
- **Format**: MP4 (H.264 video + AAC audio)
- **Duration**: 5.31 seconds
- **Resolution**: 1280x720 (720p HD)
- **Video Codec**: H.264
- **Audio Codec**: AAC
- **Size**: 1.1 MB
- **Source**: Sample-Videos.com
- **License**: Creative Commons / Free for testing
- **Status**: Clean file (no embedded commands)

## 🐍 Python Example Scripts

### basic_encoding.py
Comprehensive demonstration of encoding and decoding operations:
- Basic encode/decode workflow
- Testing different command types
- Frequency range experiments (17-21 kHz)
- Amplitude sensitivity testing
- Noise resilience evaluation
- Payload size testing

```bash
python basic_encoding.py
```

### audio_file_processing.py
Batch processing and advanced audio operations:
- Process multiple files at once
- Apply different encoding parameters
- Extract and analyze existing commands
- Performance benchmarking

```bash
python audio_file_processing.py
```

### api_client.py
Examples of using the REST API:
- Upload files for embedding
- Download processed files
- Decode commands via API
- Stream processing examples

```bash
# Start the API server first
ultrasonic-api

# Then run the client examples
python api_client.py
```

### test_hello_world.py
Simple verification script:
- Embeds "hello world" in sample files
- Verifies the embedding worked
- Good for quick testing

```bash
python test_hello_world.py
```

### check_embedded_commands.py
Utility to check if files contain hidden commands:
- Tests multiple encryption keys
- Identifies embedded commands
- Useful for debugging

```bash
python check_embedded_commands.py
```

## 🚀 Quick Start Examples

### Command Line Interface

```bash
# 1. Basic embedding
ultrasonic-agentics embed -i sample_audio.mp3 -o audio_with_secret.mp3 -c "hello world"

# 2. Decode the embedded command
ultrasonic-agentics decode -i audio_with_secret.mp3

# 3. Embed with custom parameters
ultrasonic-agentics embed -i sample_audio.mp3 -o custom_output.mp3 \
  -c "execute: deploy --prod" \
  --freq 19000 \
  --amplitude 0.05 \
  --bit-duration 0.02

# 4. Video file embedding
ultrasonic-agentics embed -i sample_video.mp4 -o video_with_command.mp4 \
  -c "AI: analyze video content"

# 5. Analyze for ultrasonic content
ultrasonic-agentics analyze -i audio_with_secret.mp3 --spectrogram
```

### Python API

```python
from src.embed.audio_embedder import AudioEmbedder
from src.decode.audio_decoder import AudioDecoder

# Simple example with auto-generated key
embedder = AudioEmbedder()
decoder = AudioDecoder(key=embedder.cipher.key)

# Embed
embedder.embed_file('sample_audio.mp3', 'output.mp3', 'secret command')

# Decode
command = decoder.decode_file('output.mp3')
print(f"Found: {command}")
```

### Custom Configuration

```python
# Use specific frequencies for compatibility
embedder = AudioEmbedder(
    ultrasonic_freq=17500,  # Lower frequency
    freq_separation=500,    # Narrower band
    amplitude=0.2,          # Higher amplitude
    bit_duration=0.02       # Slower for reliability
)

# Process with custom settings
embedder.embed_file(
    'sample_audio.mp3',
    'low_freq_output.mp3',
    'compatible mode test'
)
```

## 📊 Testing Scenarios

### 1. Basic Functionality Test
```bash
# Embed a simple command
ultrasonic-agentics embed -i sample_audio.mp3 -o test1.mp3 -c "test"

# Verify it works
ultrasonic-agentics decode -i test1.mp3
```

### 2. Long Command Test
```bash
# Test with the longer duration audio file
ultrasonic-agentics embed -i sample_audio.mp3 -o test2.mp3 \
  -c "execute: deploy --environment production --version 2.0 --rollback-enabled true"
```

### 3. Video Processing Test
```bash
# Embed in video file
ultrasonic-agentics embed -i sample_video.mp4 -o test3.mp4 \
  -c "video: process frames"
```

### 4. Real-time Detection Test
```python
from src.decode.audio_decoder import AudioDecoder

decoder = AudioDecoder(key=your_key)

def on_command(cmd):
    print(f"Detected: {cmd}")

# Start listening through microphone
decoder.start_listening(callback=on_command)
```

## 🔧 Advanced Usage

### Batch Processing
```python
import os
from src.embed.audio_embedder import AudioEmbedder

embedder = AudioEmbedder()

# Process all MP3 files in directory
for file in os.listdir('.'):
    if file.endswith('.mp3'):
        output = f"secured_{file}"
        embedder.embed_file(file, output, f"batch: {file}")
        print(f"Processed: {file}")
```

### Performance Testing
```python
import time
from src.embed.audio_embedder import AudioEmbedder

embedder = AudioEmbedder()

# Measure embedding speed
start = time.time()
embedder.embed_file('sample_audio.mp3', 'perf_test.mp3', 'performance test')
duration = time.time() - start

print(f"Embedding took: {duration:.2f} seconds")
print(f"Speed: {27.74/duration:.1f}x realtime")
```

## 📝 Notes

### About the Sample Files
- Both files are clean (no pre-embedded commands)
- Suitable for testing but may not represent all real-world scenarios
- The audio file's 27+ second duration supports embedding longer commands
- The video file demonstrates audio track extraction and re-embedding

### Embedding Limits
- Maximum command length depends on audio duration and bit rate
- Default settings: ~100-1000 bits per second
- For a 30-second file: ~375-3750 bytes of data
- Includes encryption overhead and error correction

### Best Practices
1. Use longer audio files for longer commands
2. Test with various audio types (music, speech, silence)
3. Verify commands after embedding
4. Keep encryption keys secure
5. Test in your target environment (speakers, microphones)

## 🔗 Additional Resources

### Download More Test Files
- [Pexels](https://www.pexels.com) - Free stock videos and music
- [Sample-Videos.com](https://www.sample-videos.com) - Various test media files
- [Pixabay](https://pixabay.com) - Royalty-free audio and video
- [Freesound](https://freesound.org) - Creative Commons audio samples
- [BBC Sound Effects](https://sound-effects.bbcrewind.co.uk/) - 33,000+ free sound effects

### Documentation
- [API Reference](../src/docs/api-reference.md)
- [User Guide](../src/docs/user-guide.md)
- [Security Best Practices](../src/docs/security.md)
- [Troubleshooting](../src/docs/troubleshooting.md)

## 🐛 Troubleshooting

### Common Issues

1. **"No embedded command found"**
   - Verify the correct encryption key is used
   - Check audio file isn't too compressed
   - Try increasing amplitude parameter

2. **"Embedding failed"**
   - Ensure audio file is valid
   - Check sufficient duration for command
   - Verify write permissions

3. **Poor detection rate**
   - Reduce background noise
   - Adjust frequency parameters
   - Increase bit duration for reliability

### Debug Mode
```bash
# Enable verbose output for debugging
ultrasonic-agentics decode -i test.mp3 --verbose

# Analyze signal quality
ultrasonic-agentics analyze -i test.mp3 --detailed
```

---

Happy testing! 🎉 If you create useful examples, consider contributing them back to the project.