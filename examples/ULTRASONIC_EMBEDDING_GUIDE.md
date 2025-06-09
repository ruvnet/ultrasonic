# Ultrasonic Embedding Guide

## Overview

This guide explains the fixes implemented to ensure reliable ultrasonic embedding and decoding in the Ultrasonic project.

## Key Issues Fixed

### 1. Return Values in Embed Methods
- **Issue**: `embed_file` methods in `audio_embedder.py` and `video_embedder.py` were not returning proper True/False values
- **Fix**: Now properly return `True` on success and `False` on failure with detailed error messages

### 2. Default Bitrate for Compressed Formats
- **Issue**: Default bitrate of 192k was too low for preserving ultrasonic frequencies
- **Fix**: Changed default bitrate to 320k for MP3 and other compressed formats

### 3. Embedding Verification
- **Issue**: No verification that the embedded signal was actually present after encoding
- **Fix**: Added verification step that attempts to decode the embedded command after encoding (with appropriate warnings for compressed formats)

### 4. Video Audio Codec
- **Issue**: AAC audio codec in videos was removing ultrasonic frequencies
- **Fix**: Added `preserve_ultrasonic` parameter that uses PCM audio codec for better signal preservation

### 5. Error Handling and Logging
- **Issue**: Silent failures made debugging difficult
- **Fix**: Added comprehensive error messages and traceback printing for debugging

## Audio Format Recommendations

### Best Formats for Ultrasonic Embedding

1. **WAV (Recommended)**
   - Uncompressed format
   - Perfect ultrasonic preservation
   - Larger file sizes
   - Use: `output.wav`

2. **FLAC (Good Alternative)**
   - Lossless compression
   - Perfect ultrasonic preservation
   - Smaller than WAV
   - Use: `output.flac`

3. **MP3 (Not Recommended)**
   - Lossy compression cuts frequencies >16kHz
   - Ultrasonic signals will be lost
   - Use 320k bitrate if required
   - Use: `output.mp3` with `bitrate='320k'`

4. **OGG/AAC (Not Recommended)**
   - Similar limitations to MP3
   - Poor ultrasonic preservation

## Usage Examples

### Basic Audio Embedding (WAV)
```python
from src.embed.audio_embedder import AudioEmbedder

embedder = AudioEmbedder(key=b'YourSecretKey...')
success = embedder.embed_file(
    'input.mp3',
    'output.wav',  # WAV format preserves ultrasonic
    'secret command'
)
```

### Video Embedding with Ultrasonic Preservation
```python
from src.embed.video_embedder import VideoEmbedder

embedder = VideoEmbedder(key=b'YourSecretKey...')
success = embedder.embed_file(
    'input.mp4',
    'output.mp4',
    'secret command',
    preserve_ultrasonic=True  # Uses PCM audio codec
)
```

### Checking Frequency Content
```bash
# Check if ultrasonic frequencies are preserved
python check_ultrasonic_frequencies.py embedded_file.wav

# Compare original and embedded files
python check_ultrasonic_frequencies.py original.mp3 embedded.mp3
```

### Running Tests
```bash
# Basic hello world test
python test_hello_world.py

# Comprehensive format testing
python test_ultrasonic_embedding.py
```

## Troubleshooting

### Embedding Succeeds but Decoding Fails

1. **Check the audio format**: MP3/OGG/AAC formats remove ultrasonic frequencies
2. **Verify sample rate**: Must be at least 44.1kHz (48kHz preferred)
3. **Check amplitude**: Try increasing amplitude to 0.2 or 0.3
4. **Use frequency analysis**: Run `check_ultrasonic_frequencies.py` to verify signal presence

### Video Embedding Issues

1. **No audio track**: Ensure input video has an audio track
2. **Codec issues**: Use `preserve_ultrasonic=True` for PCM audio
3. **File size concerns**: PCM audio creates larger files but preserves signal

### Best Practices

1. **Always use WAV or FLAC** for production ultrasonic embedding
2. **Test with verification**: Check that embedded commands can be decoded
3. **Monitor frequency content**: Use the diagnostic tools to verify signal preservation
4. **Consider amplitude**: Balance between detectability and audibility (0.1-0.3 recommended)
5. **Document format choices**: Make it clear which formats preserve ultrasonic signals

## Technical Details

### Ultrasonic Frequency Range
- Base frequency: 18.5 kHz (configurable)
- FSK separation: 1 kHz
- Range: 18.5-19.5 kHz
- Required sample rate: >39 kHz (48 kHz recommended)

### Signal Parameters
- Bit duration: 0.01 seconds (10ms)
- Amplitude: 0.1 (10% of max, configurable)
- Modulation: Frequency Shift Keying (FSK)

### Nyquist Theorem
- Sample rate must be at least 2x the highest frequency
- For 19.5 kHz signal: minimum 39 kHz sample rate
- Most audio is 44.1 kHz or 48 kHz (sufficient)
- Compressed formats filter out "inaudible" frequencies >16 kHz