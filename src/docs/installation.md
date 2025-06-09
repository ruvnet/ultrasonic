# Ultrasonic Agentics - Installation & Getting Started Guide

Welcome to Ultrasonic Agentics! This comprehensive guide will help you install and start using the ultrasonic steganography framework for agentic command transmission.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Platform-Specific Instructions](#platform-specific-instructions)
4. [Environment Setup](#environment-setup)
5. [Quick Start Tutorial](#quick-start-tutorial)
6. [Verification Steps](#verification-steps)
7. [Docker Installation](#docker-installation)
8. [Common Issues & Solutions](#common-issues--solutions)
9. [Next Steps](#next-steps)

## 🔧 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Audio**: Sound card capable of 48kHz sampling rate
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

### Audio Hardware Requirements
- Speakers/headphones capable of reproducing 18-22 kHz frequencies
- Microphone with frequency response up to at least 20 kHz (for real-time applications)
- USB audio interfaces recommended for professional applications

### Dependencies Overview
The framework requires these core dependencies:
- **NumPy & SciPy**: Numerical computing and signal processing
- **PyDub**: Audio file manipulation
- **MoviePy**: Video processing capabilities
- **SoundDevice**: Real-time audio I/O
- **FastAPI & Uvicorn**: Web API server
- **FFmpeg**: Media processing backend

## 🚀 Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/ultrasonic-agentics.git
cd ultrasonic-agentics/agentic_commands_stego

# Install with pip
pip install -r requirements.txt

# Verify installation
python -c "from embed.ultrasonic_encoder import UltrasonicEncoder; print('✓ Installation successful!')"
```

### Method 2: Development Install

```bash
# Clone and install in development mode
git clone https://github.com/your-org/ultrasonic-agentics.git
cd ultrasonic-agentics/agentic_commands_stego

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Method 3: Conda Install

```bash
# Create conda environment
conda create -n ultrasonic-agentics python=3.9
conda activate ultrasonic-agentics

# Install core scientific packages via conda
conda install numpy scipy

# Install remaining dependencies via pip
pip install pydub moviepy sounddevice fastapi uvicorn pytest pycryptodome ffmpeg-python python-multipart
```

## 🖥️ Platform-Specific Instructions

### Windows

#### Prerequisites
1. **Install Python 3.8+** from [python.org](https://python.org)
2. **Install FFmpeg**:
   ```powershell
   # Using chocolatey (recommended)
   choco install ffmpeg
   
   # Or download from https://ffmpeg.org/download.html
   # Add FFmpeg to PATH environment variable
   ```

3. **Install Visual C++ Build Tools** (if compilation errors occur):
   ```powershell
   # Download from Microsoft or use:
   choco install visualstudio2019buildtools
   ```

#### Installation
```powershell
# Open PowerShell as Administrator
git clone https://github.com/your-org/ultrasonic-agentics.git
cd ultrasonic-agentics\agentic_commands_stego

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test installation
python examples\basic_encoding.py
```

#### Audio Setup
- Ensure Windows audio is set to 48kHz sample rate:
  1. Right-click sound icon → Sounds → Playback tab
  2. Select default device → Properties → Advanced
  3. Set to "24 bit, 48000 Hz (Studio Quality)"

### macOS

#### Prerequisites
1. **Install Homebrew** (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install dependencies**:
   ```bash
   brew install python@3.9 ffmpeg portaudio
   ```

#### Installation
```bash
# Clone repository
git clone https://github.com/your-org/ultrasonic-agentics.git
cd ultrasonic-agentics/agentic_commands_stego

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Test installation
python examples/basic_encoding.py
```

#### Audio Setup
- Install SoundflowerBed or BlackHole for advanced audio routing
- Ensure Audio MIDI Setup is configured for 48kHz

### Linux (Ubuntu/Debian)

#### Prerequisites
```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install python3 python3-pip python3-venv ffmpeg portaudio19-dev python3-dev

# Install build essentials (if needed)
sudo apt install build-essential
```

#### Installation
```bash
# Clone repository
git clone https://github.com/your-org/ultrasonic-agentics.git
cd ultrasonic-agentics/agentic_commands_stego

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Test installation
python examples/basic_encoding.py
```

#### Audio Setup
```bash
# Install ALSA utilities
sudo apt install alsa-utils

# Test audio capabilities
aplay -l  # List playback devices
arecord -l  # List recording devices

# Set sample rate (if needed)
echo "defaults.pcm.rate_converter \"linear\"" >> ~/.asoundrc
```

### Linux (CentOS/RHEL/Fedora)

```bash
# For CentOS/RHEL
sudo yum install python3 python3-pip python3-devel portaudio-devel ffmpeg

# For Fedora
sudo dnf install python3 python3-pip python3-devel portaudio-devel ffmpeg

# Follow same installation steps as Ubuntu
```

## 🔧 Environment Setup

### Virtual Environment (Highly Recommended)

```bash
# Create isolated environment
python -m venv ultrasonic-env

# Activate environment
source ultrasonic-env/bin/activate  # Linux/macOS
# ultrasonic-env\Scripts\activate  # Windows

# Install framework
pip install -r requirements.txt

# Deactivate when done
deactivate
```

### Environment Variables

Create a `.env` file in your project directory:

```bash
# Audio configuration
AUDIO_SAMPLE_RATE=48000
AUDIO_CHANNELS=1
AUDIO_DEVICE_ID=0

# Ultrasonic settings
DEFAULT_FREQ_0=18500
DEFAULT_FREQ_1=19500
DEFAULT_AMPLITUDE=0.2
DEFAULT_BIT_DURATION=0.01

# API configuration
API_HOST=localhost
API_PORT=8000
API_DEBUG=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=ultrasonic.log
```

### IDE Configuration

#### VS Code
Install recommended extensions:
```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.flake8",
        "ms-toolsai.jupyter"
    ]
}
```

#### PyCharm
1. Set Python interpreter to your virtual environment
2. Configure code style to PEP 8
3. Enable type checking

## 🎯 Quick Start Tutorial

### Step 1: Basic Encoding Example

Create your first ultrasonic encoding script:

```python
# my_first_encoding.py
from embed.ultrasonic_encoder import UltrasonicEncoder
from decode.ultrasonic_decoder import UltrasonicDecoder

# Initialize encoder with default settings
encoder = UltrasonicEncoder(
    freq_0=18500,      # Frequency for bit '0'
    freq_1=19500,      # Frequency for bit '1'
    sample_rate=48000, # Audio sample rate
    amplitude=0.2      # Signal strength (20%)
)

# Initialize decoder with matching settings
decoder = UltrasonicDecoder(
    freq_0=18500,
    freq_1=19500,
    sample_rate=48000
)

# Encode a simple command
command = "execute:status_check"
print(f"Encoding command: {command}")

# Convert to bytes and encode
payload_bytes = command.encode('utf-8')
audio_signal = encoder.encode_payload(payload_bytes)

print(f"Generated {len(audio_signal)} audio samples")
print(f"Duration: {len(audio_signal) / 48000:.2f} seconds")

# Decode the signal
decoded_bytes = decoder.decode_payload(audio_signal)

if decoded_bytes:
    decoded_command = decoded_bytes.decode('utf-8')
    print(f"Decoded command: {decoded_command}")
    
    if decoded_command == command:
        print("✓ Success! Encoding and decoding worked perfectly!")
    else:
        print("✗ Warning: Decoded command doesn't match original")
else:
    print("✗ Error: Failed to decode signal")
```

Run the script:
```bash
python my_first_encoding.py
```

Expected output:
```
Encoding command: execute:status_check
Generated 9216 audio samples
Duration: 0.19 seconds
Decoded command: execute:status_check
✓ Success! Encoding and decoding worked perfectly!
```

### Step 2: Save Audio to File

```python
# save_audio_example.py
from embed.ultrasonic_encoder import UltrasonicEncoder
from pydub import AudioSegment

encoder = UltrasonicEncoder(amplitude=0.3)

# Encode command
command = "transmit:sensor_data"
audio_signal = encoder.encode_payload(command.encode())

# Convert to audio file format
audio_segment = encoder.create_audio_segment(audio_signal)

# Save as WAV file
audio_segment.export("encoded_command.wav", format="wav")
print("✓ Audio saved to encoded_command.wav")

# You can now play this file or transmit it through any audio system
```

### Step 3: Real-time Audio Processing

```python
# realtime_example.py
import sounddevice as sd
import numpy as np
from embed.ultrasonic_encoder import UltrasonicEncoder
from decode.ultrasonic_decoder import UltrasonicDecoder

def real_time_demo():
    """Demonstrate real-time encoding and playback."""
    
    encoder = UltrasonicEncoder(amplitude=0.4)  # Higher amplitude for real-time
    
    # Encode command
    command = "ping"
    audio_signal = encoder.encode_payload(command.encode())
    
    print(f"Playing command: {command}")
    print("Make sure your speakers are on and volume is appropriate")
    
    # Play the encoded signal
    sd.play(audio_signal, samplerate=48000)
    sd.wait()  # Wait for playback to finish
    
    print("✓ Command transmitted!")

if __name__ == "__main__":
    real_time_demo()
```

### Step 4: API Server Example

```python
# api_server_example.py
from server.api import app
import uvicorn

if __name__ == "__main__":
    print("Starting Ultrasonic Agentics API server...")
    print("Access documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )
```

Start the server:
```bash
python api_server_example.py
```

Test the API:
```bash
# Encode a command via API
curl -X POST "http://localhost:8000/encode" \
     -H "Content-Type: application/json" \
     -d '{"command": "execute:status_check", "amplitude": 0.2}'

# Check API health
curl http://localhost:8000/health
```

## ✅ Verification Steps

### Step 1: Basic Installation Test

```bash
python -c "
import numpy as np
import scipy
from pydub import AudioSegment
import sounddevice as sd
print('✓ All core dependencies installed successfully')
"
```

### Step 2: Framework Components Test

```bash
python -c "
from embed.ultrasonic_encoder import UltrasonicEncoder
from decode.ultrasonic_decoder import UltrasonicDecoder
print('✓ Ultrasonic framework components loaded successfully')
"
```

### Step 3: Audio System Test

```bash
python -c "
import sounddevice as sd
print('Available audio devices:')
print(sd.query_devices())
"
```

### Step 4: End-to-End Test

Run the comprehensive test suite:

```bash
# Run basic functionality tests
python examples/basic_encoding.py

# Run unit tests
python -m pytest tests/ -v

# Run specific component tests
python -m pytest tests/test_ultrasonic_encoder.py -v
python -m pytest tests/test_ultrasonic_decoder.py -v
```

Expected test output:
```
=== Basic Encoding/Decoding Example ===
Original command: execute:status_check
Encoding command into ultrasonic signal...
Generated signal: 9216 samples
Signal duration: 0.19 seconds
Frequency range: (18500, 19500) Hz
Saved encoded audio to: encoded_command.wav
Decoding signal...
Decoded command: execute:status_check
✓ Encoding/Decoding successful!
```

### Step 5: Performance Verification

```bash
python -c "
import time
from embed.ultrasonic_encoder import UltrasonicEncoder

encoder = UltrasonicEncoder()
command = 'performance:test' * 10  # Longer payload

start_time = time.time()
signal = encoder.encode_payload(command.encode())
encode_time = time.time() - start_time

print(f'Encoding performance: {len(command)} bytes in {encode_time:.3f}s')
print(f'Throughput: {len(command)/encode_time:.1f} bytes/second')
"
```

## 🐳 Docker Installation

### Using Pre-built Image

```bash
# Pull the image
docker pull ultrasonic-agentics:latest

# Run container with audio support
docker run -it --rm \
  --device /dev/snd \
  -v $(pwd)/output:/app/output \
  ultrasonic-agentics:latest
```

### Building from Source

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose API port
EXPOSE 8000

# Default command
CMD ["python", "examples/basic_encoding.py"]
```

Build and run:

```bash
# Build image
docker build -t ultrasonic-agentics .

# Run with basic example
docker run --rm ultrasonic-agentics

# Run API server
docker run -p 8000:8000 --rm ultrasonic-agentics \
  python -m uvicorn server.api:app --host 0.0.0.0 --port 8000
```

### Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  ultrasonic-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./output:/app/output
    devices:
      - /dev/snd:/dev/snd
    environment:
      - PYTHONPATH=/app
      - LOG_LEVEL=INFO
    command: python -m uvicorn server.api:app --host 0.0.0.0 --port 8000
    
  ultrasonic-worker:
    build: .
    volumes:
      - ./data:/app/data
      - ./output:/app/output
    environment:
      - PYTHONPATH=/app
    command: python examples/basic_encoding.py
```

Run with Docker Compose:

```bash
docker-compose up -d
docker-compose logs -f
```

## 🔧 Common Issues & Solutions

### Issue 1: FFmpeg Not Found

**Problem**: `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solutions**:
```bash
# Windows (using chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

### Issue 2: Audio Device Errors

**Problem**: `sounddevice.PortAudioError: Device unavailable`

**Solutions**:
```bash
# List available audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Test audio system
python -c "
import sounddevice as sd
import numpy as np
sd.play(np.sin(2*np.pi*440*np.linspace(0,1,48000)), samplerate=48000)
sd.wait()
"

# On Linux, check ALSA configuration
aplay -l
cat /proc/asound/cards
```

### Issue 3: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'embed'`

**Solutions**:
```bash
# Ensure you're in the correct directory
cd agentic_commands_stego

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install in development mode
pip install -e .
```

### Issue 4: Poor Decoding Performance

**Problem**: Frequent decoding failures or corrupted data

**Solutions**:
```python
# Increase signal amplitude
encoder = UltrasonicEncoder(amplitude=0.4)

# Lower detection threshold
decoder = UltrasonicDecoder(detection_threshold=0.05)

# Use better frequency separation
encoder = UltrasonicEncoder(freq_0=18000, freq_1=20000)

# Add noise resilience
encoder = UltrasonicEncoder(bit_duration=0.02)  # Longer bits
```

### Issue 5: Frequency Range Issues

**Problem**: `ValueError: Frequencies must be below Nyquist frequency`

**Solutions**:
```python
# Use lower frequencies for 44.1kHz audio
encoder = UltrasonicEncoder(
    freq_0=17000,
    freq_1=18000,
    sample_rate=44100
)

# Or increase sample rate
encoder = UltrasonicEncoder(
    freq_0=18500,
    freq_1=19500,
    sample_rate=48000  # Supports up to 24kHz
)
```

### Issue 6: Permission Errors (Linux)

**Problem**: Permission denied for audio devices

**Solutions**:
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Restart session or run:
newgrp audio

# Set permissions for audio devices
sudo chmod 666 /dev/snd/*
```

### Issue 7: Virtual Environment Issues

**Problem**: Packages not found after installation

**Solutions**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Verify Python location
which python

# Reinstall if needed
pip install --force-reinstall -r requirements.txt
```

## 🎓 Next Steps

### Learning Path

1. **Explore Examples**: Run all examples in `examples/` directory
2. **Read Documentation**: Check `docs/user-guide.md` and `docs/api-reference.md`
3. **Run Tests**: Execute the test suite to understand expected behavior
4. **Experiment**: Try different frequency ranges and encoding parameters
5. **Build Applications**: Start building your own ultrasonic applications

### Advanced Topics

- **Custom Frequency Ranges**: Optimize for your specific hardware
- **Error Correction**: Implement advanced error correction schemes
- **Real-time Processing**: Build streaming audio applications
- **Multi-channel Audio**: Use stereo encoding for increased bandwidth
- **Integration**: Combine with other communication protocols

### Community Resources

- **Documentation**: `/docs/` directory
- **Examples**: `/examples/` directory  
- **Tests**: `/tests/` directory for usage patterns
- **Issues**: GitHub issues for bug reports and feature requests

### Quick Reference Commands

```bash
# Basic encoding test
python examples/basic_encoding.py

# Start API server
python -m uvicorn server.api:app --reload

# Run test suite
python -m pytest tests/ -v

# Interactive frequency testing
python examples/frequency_calibration.py

# Real-time audio demo
python examples/realtime_demo.py
```

## 🎉 Congratulations!

You now have Ultrasonic Agentics installed and working! You can:

- ✅ Encode commands into ultrasonic frequencies
- ✅ Decode ultrasonic signals back to commands  
- ✅ Save and load audio files
- ✅ Use the REST API for integration
- ✅ Run real-time audio processing

Start experimenting with the examples and building your own ultrasonic applications!

---

**Need help?** Check the troubleshooting section above or refer to the detailed documentation in the `docs/` directory.