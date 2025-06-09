# Ultrasonic Agentics User Guide

This guide provides comprehensive instructions for using the Ultrasonic Agentics steganography framework.

## Table of Contents

1. [Installation](#installation)
2. [Basic Concepts](#basic-concepts)
3. [Ultrasonic Audio Processing](#ultrasonic-audio-processing)
4. [Video Steganography](#video-steganography)
5. [Cryptographic Features](#cryptographic-features)
6. [Command Line Interface](#command-line-interface)
7. [API Server Usage](#api-server-usage)
8. [MCP Integration](#mcp-integration)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

Ensure you have Python 3.8 or higher installed on your system.

### Install from PyPI

```bash
pip install ultrasonic-agentics
```

### Development Installation

```bash
git clone https://github.com/yourusername/ultrasonic-agentics.git
cd ultrasonic-agentics
pip install -e .
```

### Verify Installation

```python
import ultrasonic_agentics
print(ultrasonic_agentics.__version__)
```

## Basic Concepts

### Steganography Overview

Steganography is the practice of concealing information within other non-secret data. This framework specializes in:

- **Ultrasonic Audio**: Embedding data in high-frequency audio ranges (typically 18-22 kHz)
- **Video LSB**: Using least significant bit manipulation in video frames
- **Encrypted Payloads**: Securing embedded data with cryptographic protection

### Command Structure

Commands follow a structured format:
```
action:parameter:timestamp
```

Examples:
- `execute:status_check:1640995200`
- `transmit:sensor_data:1640995201`
- `configure:mode=stealth:1640995202`

## Ultrasonic Audio Processing

### Basic Encoding

```python
from ultrasonic_agentics.embed import UltrasonicEncoder

encoder = UltrasonicEncoder(
    frequency=19500,  # Hz
    sample_rate=44100,
    duration=2.0      # seconds
)

# Encode a command
command = "execute:status_check"
audio_data = encoder.encode(command)

# Save to file
encoder.save_audio(audio_data, "encoded_command.wav")
```

### Basic Decoding

```python
from ultrasonic_agentics.decode import UltrasonicDecoder

decoder = UltrasonicDecoder(
    frequency=19500,
    sample_rate=44100
)

# Load and decode audio file
audio_data = decoder.load_audio("encoded_command.wav")
decoded_command = decoder.decode(audio_data)
print(f"Decoded: {decoded_command}")
```

### Advanced Audio Configuration

```python
# Custom frequency calibration
encoder = UltrasonicEncoder()
encoder.calibrate_frequency(target_snr=20.0)

# Multi-frequency encoding for redundancy
encoder.set_frequencies([19000, 19500, 20000])

# Error correction
encoder.enable_error_correction(level=2)
```

## Video Steganography

### Video Encoding

```python
from ultrasonic_agentics.embed import VideoEmbedder

embedder = VideoEmbedder()

# Embed command in video
command = "transmit:sensor_data"
output_video = embedder.embed(
    video_path="input.mp4",
    command=command,
    output_path="encoded_video.mp4"
)
```

### Video Decoding

```python
from ultrasonic_agentics.decode import VideoDecoder

decoder = VideoDecoder()
decoded_command = decoder.decode("encoded_video.mp4")
print(f"Hidden command: {decoded_command}")
```

### Video Processing Options

```python
# Frame selection strategy
embedder.set_frame_strategy("keyframes")  # or "random", "interval"

# Color channel selection
embedder.set_channel("blue")  # or "red", "green", "all"

# Embedding strength
embedder.set_strength(0.1)  # Lower values = more subtle
```

## Cryptographic Features

### Basic Encryption

```python
from ultrasonic_agentics.crypto import Cipher

# Initialize with password
cipher = Cipher("your_secret_password")

# Encrypt before encoding
command = "execute:status_check"
encrypted_command = cipher.encrypt(command)

# Encode encrypted data
encoder = UltrasonicEncoder()
audio_data = encoder.encode(encrypted_command)
```

### Advanced Cryptographic Options

```python
# Custom key derivation
cipher = Cipher()
cipher.set_key_from_password("password", salt=b"custom_salt")

# Multiple encryption layers
cipher.enable_double_encryption()

# Key rotation
cipher.rotate_key(interval=3600)  # seconds
```

## Command Line Interface

The framework provides a comprehensive CLI for all operations. See the [CLI Usage Guide](cli-usage.md) for complete documentation.

### Quick CLI Examples

```bash
# Embed a command
agentic-stego embed audio.wav "execute:backup" --frequency 19000

# Decode a command
agentic-stego decode encoded.wav --verbose

# Analyze a file
agentic-stego analyze suspicious.wav

# Start MCP server
agentic-stego server --port 3000
```

## MCP Integration

For AI assistant integration, the framework provides a Model Context Protocol (MCP) server. See the [MCP Integration Guide](mcp-integration.md) for setup instructions.

### Quick MCP Setup

```bash
# Start the MCP server
agentic-stego server

# The server will be available for AI assistant integration
# Default port: 3000, transport: stdio
```

## API Server Usage

### Starting the Server

```bash
# Default configuration
python -m ultrasonic_agentics.server

# Custom port and host
python -m ultrasonic_agentics.server --host 0.0.0.0 --port 8080
```

### API Endpoints

#### Encode Command

```bash
curl -X POST http://localhost:8000/encode \
  -H "Content-Type: application/json" \
  -d '{
    "command": "execute:status_check",
    "frequency": 19500,
    "duration": 2.0,
    "encrypt": true
  }'
```

#### Decode Audio

```bash
curl -X POST http://localhost:8000/decode \
  -F "audio=@encoded_command.wav" \
  -F "frequency=19500"
```

#### Health Check

```bash
curl http://localhost:8000/health
```

### API Response Format

```json
{
  "status": "success",
  "data": {
    "command": "execute:status_check",
    "timestamp": "2024-01-01T12:00:00Z",
    "metadata": {
      "frequency": 19500,
      "duration": 2.0,
      "encrypted": true
    }
  }
}
```

## Configuration

### Configuration File

Create `config.json` in your project directory:

```json
{
  "ultrasonic": {
    "default_frequency": 19500,
    "sample_rate": 44100,
    "calibration_enabled": true,
    "error_correction": true
  },
  "crypto": {
    "default_algorithm": "AES-256-GCM",
    "key_rotation_interval": 3600
  },
  "server": {
    "host": "localhost",
    "port": 8000,
    "debug": false
  }
}
```

### Environment Variables

```bash
export ULTRASONIC_FREQUENCY=19500
export ULTRASONIC_SAMPLE_RATE=44100
export CRYPTO_PASSWORD=your_secret_password
export API_HOST=localhost
export API_PORT=8000
```

### Programmatic Configuration

```python
from ultrasonic_agentics.config import Config

config = Config()
config.set("ultrasonic.frequency", 20000)
config.set("crypto.algorithm", "ChaCha20-Poly1305")
config.save("my_config.json")
```

## Troubleshooting

### Common Issues

#### Low Detection Rate

```python
# Increase signal strength
encoder.set_amplitude(0.8)

# Use lower frequency for better propagation
encoder.set_frequency(18000)

# Enable error correction
encoder.enable_error_correction()
```

#### Audio Quality Issues

```python
# Use higher sample rate
encoder = UltrasonicEncoder(sample_rate=48000)

# Reduce interference
encoder.apply_noise_filter()

# Calibrate for environment
encoder.auto_calibrate()
```

#### Decoding Failures

```python
# Check frequency alignment
decoder.analyze_spectrum("problem_audio.wav")

# Try frequency sweep
for freq in range(18000, 22000, 500):
    decoder.set_frequency(freq)
    result = decoder.decode(audio_data)
    if result:
        print(f"Success at {freq} Hz")
        break
```

### Performance Optimization

```python
# Use faster processing modes
encoder.set_processing_mode("fast")

# Parallel processing
encoder.enable_multiprocessing(cores=4)

# Memory optimization
encoder.set_buffer_size(1024)
```

### Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug mode
encoder = UltrasonicEncoder(debug=True)
decoder = UltrasonicDecoder(debug=True)

# Analyze signal characteristics
encoder.analyze_output(audio_data)
decoder.plot_spectrum(audio_data)
```

## Best Practices

1. **Frequency Selection**: Use frequencies above 18 kHz for human imperceptibility
2. **Command Length**: Keep commands under 50 characters for reliability
3. **Error Handling**: Always implement try-catch blocks for encoding/decoding
4. **Testing**: Test in your target environment before deployment
5. **Security**: Use encryption for sensitive commands
6. **Performance**: Monitor CPU usage during real-time processing

## Next Steps

- Learn [CLI Usage](cli-usage.md) for command-line operations
- Set up [MCP Integration](mcp-integration.md) for AI assistant workflows
- Explore [Advanced Usage](advanced-usage.md) for complex scenarios
- Review [API Reference](api-reference.md) for complete method documentation
- Check [Examples](../examples/) for practical implementations