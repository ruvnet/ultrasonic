# CLI Usage Guide

The Agentic Commands Steganography framework provides a powerful command-line interface for embedding and decoding encrypted commands in media files using ultrasonic steganography.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Quick Start](#quick-start)
3. [CLI Commands Reference](#cli-commands-reference)
4. [Examples](#examples)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

## Installation & Setup

### Install the Package

```bash
# Install from PyPI (when published)
pip install agentic-commands-stego

# Or install from source
git clone https://github.com/yourusername/agentic-commands-stego.git
cd agentic-commands-stego
pip install -e .
```

### Verify Installation

```bash
agentic-stego --version
# Output: 🎵 Agentic Commands Steganography v1.0.0
```

### Install CLI Dependencies

The CLI requires additional dependencies for rich output:

```bash
pip install typer rich click
```

## Quick Start

### 1. Embed a Command

```bash
# Embed a simple command into an audio file
agentic-stego embed input.wav "execute:status_check" --output encoded.wav

# Embed with custom frequency and amplitude
agentic-stego embed input.wav "transmit:sensor_data" \
    --frequency 19500 \
    --amplitude 0.2 \
    --output encoded.wav
```

### 2. Decode a Command

```bash
# Decode a command from an audio file
agentic-stego decode encoded.wav

# Decode with detailed analysis
agentic-stego decode encoded.wav --analysis --verbose
```

### 3. Analyze a File

```bash
# Check if a file contains steganographic content
agentic-stego analyze suspicious.wav
```

### 4. Start MCP Server

```bash
# Start the Model Context Protocol server
agentic-stego server --host 0.0.0.0 --port 3000
```

## CLI Commands Reference

### Global Options

```
--version, -v    Show version and exit
--help          Show help message
```

### `embed` - Embed Commands

Embed encrypted commands into audio or video files.

```bash
agentic-stego embed [OPTIONS] FILE_PATH COMMAND
```

**Arguments:**
- `FILE_PATH`: Input media file path (audio or video)
- `COMMAND`: Command string to embed

**Options:**
- `--output, -o TEXT`: Output file path (default: auto-generated)
- `--frequency, -f FLOAT`: Ultrasonic frequency in Hz (default: 18500.0)
- `--amplitude, -a FLOAT`: Signal amplitude 0.0-1.0 (default: 0.1)
- `--obfuscate/--no-obfuscate`: Enable/disable command obfuscation (default: enabled)
- `--bitrate, -b TEXT`: Audio bitrate (default: 192k)

**Supported Formats:**
- **Audio**: MP3, WAV, FLAC, OGG, M4A
- **Video**: MP4, AVI, MOV, MKV

**Examples:**
```bash
# Basic embedding
agentic-stego embed audio.wav "execute:backup"

# High-frequency embedding with custom amplitude
agentic-stego embed music.mp3 "transmit:logs" \
    --frequency 20000 \
    --amplitude 0.3 \
    --output steganized_music.mp3

# Video embedding
agentic-stego embed video.mp4 "configure:mode=stealth" \
    --output encoded_video.mp4
```

### `decode` - Decode Commands

Extract and decrypt commands from media files.

```bash
agentic-stego decode [OPTIONS] FILE_PATH
```

**Arguments:**
- `FILE_PATH`: Media file path to decode

**Options:**
- `--analysis, -a`: Perform detailed signal analysis
- `--verbose, -v`: Show verbose output including analysis details

**Examples:**
```bash
# Simple decoding
agentic-stego decode encoded.wav

# Detailed analysis
agentic-stego decode encoded.wav --analysis --verbose
```

**Output Format:**
```
✅ Command decoded successfully!
Command: execute:status_check
Processing time: 234.5 ms
Confidence: 0.95
```

### `analyze` - Analyze Media Files

Analyze media files for steganographic content without decoding.

```bash
agentic-stego analyze FILE_PATH
```

**Examples:**
```bash
agentic-stego analyze suspicious_audio.wav
```

**Output:**
```
Media Analysis Results
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property             ┃ Value                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ File                 │ suspicious_audio.wav     │
│ Processing Time      │ 156.2 ms                │
│ Steganographic Content│ ✅ Detected             │
│ Confidence Score     │ 0.87                    │
│ Detected Frequencies │ [18500, 19500]          │
└──────────────────────┴──────────────────────────┘
```

### `server` - Start MCP Server

Start the Model Context Protocol server for integration with AI assistants.

```bash
agentic-stego server [OPTIONS]
```

**Options:**
- `--host, -h TEXT`: Host to bind to (default: localhost)
- `--port, -p INTEGER`: Port to bind to (default: 3000)
- `--log-level, -l TEXT`: Logging level (default: INFO)

**Examples:**
```bash
# Start server on default settings
agentic-stego server

# Start on all interfaces
agentic-stego server --host 0.0.0.0 --port 3000

# Debug mode
agentic-stego server --log-level DEBUG
```

### `config` - Configuration Management

Configure system settings for frequencies and encryption.

```bash
agentic-stego config [OPTIONS]
```

**Options:**
- `--show, -s`: Show current configuration
- `--frequencies, -f`: Configure frequencies
- `--freq-0 FLOAT`: Frequency for binary '0' (Hz)
- `--freq-1 FLOAT`: Frequency for binary '1' (Hz)
- `--encryption, -e`: Configure encryption
- `--key-file TEXT`: Path to encryption key file
- `--key-base64 TEXT`: Base64-encoded encryption key
- `--generate-key`: Generate new encryption key

**Examples:**
```bash
# Show current configuration
agentic-stego config --show

# Configure custom frequencies
agentic-stego config --frequencies --freq-0 18000 --freq-1 19000

# Generate new encryption key
agentic-stego config --encryption --generate-key

# Use custom encryption key
agentic-stego config --encryption --key-file mykey.key
```

### `info` - System Information

Display information about the steganography system.

```bash
agentic-stego info
```

## Examples

### Basic Workflow

```bash
# 1. Start with a clean audio file
cp original.wav input.wav

# 2. Embed a command
agentic-stego embed input.wav "execute:daily_backup" \
    --output encoded.wav \
    --frequency 19000 \
    --amplitude 0.15

# 3. Verify the command was embedded
agentic-stego analyze encoded.wav

# 4. Decode the command
agentic-stego decode encoded.wav --verbose

# 5. Play the file (should sound identical to original)
# The embedded command is inaudible to humans
```

### Batch Processing

```bash
#!/bin/bash
# Batch embed commands into multiple files

commands=(
    "execute:backup"
    "transmit:status"
    "configure:stealth_mode"
)

for i in "${!commands[@]}"; do
    input_file="input_${i}.wav"
    output_file="encoded_${i}.wav"
    command="${commands[$i]}"
    
    echo "Processing $input_file with command: $command"
    agentic-stego embed "$input_file" "$command" \
        --output "$output_file" \
        --frequency $((19000 + i * 100))
done
```

### Video Processing

```bash
# Extract audio from video, embed command, and remux
input_video="presentation.mp4"
temp_audio="temp_audio.wav"
encoded_audio="encoded_audio.wav"
output_video="steganized_presentation.mp4"

# Extract audio
ffmpeg -i "$input_video" -vn -acodec pcm_s16le "$temp_audio"

# Embed command
agentic-stego embed "$temp_audio" "execute:presentation_start" \
    --output "$encoded_audio" \
    --frequency 20000

# Remux with original video
ffmpeg -i "$input_video" -i "$encoded_audio" \
    -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
    "$output_video"
```

### Real-time Monitoring

```bash
#!/bin/bash
# Monitor a directory for new audio files and analyze them

monitor_dir="/path/to/audio/files"

inotifywait -m -r -e create,move "$monitor_dir" \
    --format '%w%f' | while read file; do
    if [[ "$file" =~ \.(wav|mp3|flac)$ ]]; then
        echo "Analyzing new file: $file"
        agentic-stego analyze "$file"
    fi
done
```

## Configuration

### Configuration File

Create `~/.agentic-stego/config.json`:

```json
{
    "frequencies": {
        "freq_0": 18500.0,
        "freq_1": 19500.0,
        "default_amplitude": 0.1
    },
    "encryption": {
        "key_file": "~/.agentic-stego/default.key",
        "algorithm": "AES-256-GCM"
    },
    "server": {
        "default_host": "localhost",
        "default_port": 3000,
        "log_level": "INFO"
    },
    "output": {
        "default_bitrate": "192k",
        "preserve_metadata": true
    }
}
```

### Environment Variables

```bash
# Frequency configuration
export AGENTIC_STEGO_FREQ_0=18500
export AGENTIC_STEGO_FREQ_1=19500

# Encryption key
export AGENTIC_STEGO_KEY="base64-encoded-key-here"

# Server settings
export AGENTIC_STEGO_HOST=localhost
export AGENTIC_STEGO_PORT=3000

# Debug mode
export AGENTIC_STEGO_DEBUG=true
```

## Troubleshooting

### Common Issues

#### Command Not Found
```bash
# Ensure the package is installed and in PATH
pip install -e .
# Or add to PATH manually
export PATH="$PATH:~/.local/bin"
```

#### Permission Denied
```bash
# Check file permissions
chmod +r input.wav
chmod +w output_directory/
```

#### Encoding Failures
```bash
# Test with verbose output
agentic-stego embed input.wav "test" --verbose

# Check file format
file input.wav
ffprobe input.wav

# Try different parameters
agentic-stego embed input.wav "test" \
    --frequency 18000 \
    --amplitude 0.05
```

#### Decoding Failures
```bash
# Analyze the file first
agentic-stego analyze input.wav

# Try with different frequency ranges
for freq in 18000 18500 19000 19500 20000; do
    echo "Trying frequency: $freq"
    agentic-stego decode input.wav --frequency $freq
done
```

### Debug Mode

Enable debug logging for detailed information:

```bash
export AGENTIC_STEGO_DEBUG=true
agentic-stego embed input.wav "test command" --verbose
```

### Performance Issues

```bash
# Check system resources
top
df -h

# Use lower quality for faster processing
agentic-stego embed input.wav "command" \
    --bitrate 128k \
    --amplitude 0.05
```

### Getting Help

```bash
# General help
agentic-stego --help

# Command-specific help
agentic-stego embed --help
agentic-stego decode --help

# System information
agentic-stego info
```

## Integration with Scripts

### Python Script Integration

```python
import subprocess
import json

def embed_command(file_path, command, **kwargs):
    """Embed command using CLI."""
    cmd = ["agentic-stego", "embed", file_path, command]
    
    for key, value in kwargs.items():
        cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def decode_command(file_path):
    """Decode command using CLI."""
    cmd = ["agentic-stego", "decode", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Parse output for command
        return result.stdout
    return None

# Usage
success = embed_command("input.wav", "execute:backup", 
                        frequency=19000, amplitude=0.2)
if success:
    command = decode_command("input.wav")
    print(f"Decoded: {command}")
```

### Shell Script Integration

```bash
#!/bin/bash

# Function to safely embed commands
embed_safely() {
    local input_file="$1"
    local command="$2"
    local output_file="$3"
    
    if [[ ! -f "$input_file" ]]; then
        echo "Error: Input file not found: $input_file"
        return 1
    fi
    
    agentic-stego embed "$input_file" "$command" \
        --output "$output_file" \
        --frequency 19000 \
        --amplitude 0.1
        
    if [[ $? -eq 0 ]]; then
        echo "Successfully embedded command in $output_file"
        return 0
    else
        echo "Failed to embed command"
        return 1
    fi
}

# Usage
embed_safely "audio.wav" "execute:task" "encoded.wav"
```

---

*For complete documentation, see the [main documentation index](index.md).*