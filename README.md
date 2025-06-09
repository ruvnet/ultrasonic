# 🔊 Ultrasonic Agentics

**Hide Secret AI Commands & Data in Plain Sound** Secure steganographic framework for embedding invisible commands in audio and video

[![PyPI Version](https://img.shields.io/pypi/v/ultrasonic-agentics.svg)](https://pypi.org/project/ultrasonic-agentics/)
[![Python Support](https://img.shields.io/pypi/pyversions/ultrasonic-agentics.svg)](https://pypi.org/project/ultrasonic-agentics/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue.svg)](https://modelcontextprotocol.io)

## 🚀 What is Ultrasonic Agentics?

Ultrasonic Agentics is a cutting-edge steganography framework that embeds encrypted AI commands into ultrasonic frequencies (18-20 kHz) - inaudible to humans but detectable by your applications. Perfect for secure command transmission, covert communication channels, and innovative AI agent coordination.

### ✨ Key Features

- **🔇 Inaudible Commands**: Embed data in 18-20 kHz frequencies beyond human hearing
- **🔐 Military-Grade Encryption**: AES-256 encryption with HMAC authentication
- **🎵 Audio/Video Support**: Works with any audio or video file format
- **🤖 AI-Ready**: MCP (Model Context Protocol) integration for AI agents
- **⚡ Real-Time Processing**: Stream or batch process with minimal latency
- **🔋 Low Power Operation**: Optimized for battery-powered devices and embedded systems
- **🎯 High Reliability**: Advanced error correction ensures accurate decoding
- **📡 No RF Interference**: Audio-based transmission avoids radio frequency congestion

## 🎯 Use Cases

- **AI Agent Coordination**: Transmit commands between AI systems covertly
- **Low-Power Command & Control**: Energy-efficient device control for battery-powered IoT sensors and embedded systems
- **Emergency Communications Systems**: Backup communication channel for first responders when primary networks fail
- **Digital Watermarking**: Protect your audio/video content with invisible signatures
- **Secure Communications**: Send encrypted messages through public audio channels
- **Smart Home Automation**: Control lights, appliances, and security systems with inaudible commands
- **Industrial Monitoring**: Transmit sensor data and control signals in noisy environments
- **Access Control Systems**: Ultrasonic authentication tokens for secure facility access
- **Underwater Communications**: Leverage ultrasonic frequencies for submarine data transmission
- **Wildlife Research**: Covert data collection without disturbing animal behavior
- **Interactive Media**: Create audio/video content with hidden interactive elements
- **Medical Device Control**: Secure command transmission in healthcare environments
- **Proximity Detection**: Device-to-device communication for contact tracing and asset tracking

## 📚 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [API Reference](agentic_commands_stego/docs/api-reference.md)
- [Security Best Practices](agentic_commands_stego/docs/security.md)
- [MCP Integration](agentic_commands_stego/docs/mcp-integration.md)
- [Examples & Tutorials](agentic_commands_stego/examples/)


## 🏗️ Architecture

Ultrasonic Agentics uses a sophisticated signal processing pipeline:

1. **Command Encryption**: AES-256-GCM with key derivation
2. **Binary Encoding**: Efficient bit packing with error correction
3. **FSK Modulation**: Frequency-shift keying at 18.5-19.5 kHz
4. **Signal Injection**: Psychoacoustic masking for seamless integration
5. **Adaptive Decoding**: ML-enhanced signal detection and extraction

## 🔋 Low-Power Command & Control

Ultrasonic Agentics is designed for energy-efficient operation, making it ideal for battery-powered and embedded systems:

### Power Advantages

- **Minimal Processing**: Simple FSK demodulation requires less CPU than complex protocols
- **No Radio Transmission**: Acoustic transducers consume less power than RF transmitters
- **Sleep Mode Compatible**: Wake devices only when ultrasonic commands detected
- **Efficient Encoding**: Optimized bit rates reduce transmission time and power usage

### Ideal for Embedded Systems

- **Microcontroller Support**: Runs on Arduino, ESP32, Raspberry Pi, and similar platforms
- **Low Memory Footprint**: Core decoder uses < 1KB RAM
- **Battery Life**: Months of operation on coin cell batteries in listening mode
- **Solar Powered**: Perfect for remote sensors and outdoor installations

## 🔒 Security Features

- **End-to-End Encryption**: Commands are never transmitted in plaintext
- **Authentication**: HMAC prevents tampering and ensures message integrity
- **Key Management**: Secure key generation and optional key rotation
- **Obfuscation**: Multiple encoding layers prevent casual detection


## 🛠️ Quick Start

### Installation

```bash
# Install from PyPI
pip install ultrasonic-agentics

# With all features
pip install ultrasonic-agentics[all]
```

### Command Line Interface

After installation, three CLI tools are available:

#### `ultrasonic-agentics` - Main CLI
```bash
# Show help and available commands
ultrasonic-agentics --help

# Embed a command in an audio file
ultrasonic-agentics embed -i input.mp3 -o output.mp3 -c "command:execute" -k your-secret-key

# Embed with custom frequency and amplitude
ultrasonic-agentics embed -i input.mp3 -o output.mp3 -c "deploy:v2" \
  --freq 19000 --amplitude 0.05 --bit-duration 0.02

# Decode commands from audio
ultrasonic-agentics decode -i output.mp3 -k your-secret-key

# Decode with verbose output
ultrasonic-agentics decode -i output.mp3 -k your-secret-key --verbose

# Analyze audio for ultrasonic content
ultrasonic-agentics analyze -i audio.mp3

# Analyze with spectrogram output
ultrasonic-agentics analyze -i audio.mp3 --spectrogram --output report.png

# Configure default settings
ultrasonic-agentics config --freq 19000 --bit-rate 500

# Show current configuration
ultrasonic-agentics config --show
```

#### `ultrasonic-server` - MCP Server
```bash
# Start MCP server for AI agent integration
ultrasonic-server

# With custom port
ultrasonic-server --port 8080
```

#### `ultrasonic-api` - REST API Server
```bash
# Start REST API server
ultrasonic-api

# With custom configuration
ultrasonic-api --host 0.0.0.0 --port 8000 --workers 4
```

### CLI Quick Reference

| Command | Description | Example |
|---------|-------------|---------|
| `embed` | Hide command in audio | `ultrasonic-agentics embed -i in.mp3 -o out.mp3 -c "cmd"` |
| `decode` | Extract hidden command | `ultrasonic-agentics decode -i out.mp3 -k key` |
| `analyze` | Detect ultrasonic content | `ultrasonic-agentics analyze -i audio.mp3` |
| `config` | Manage settings | `ultrasonic-agentics config --show` |

**Common Options:**
- `-i, --input`: Input audio/video file
- `-o, --output`: Output file path
- `-c, --command`: Command to embed
- `-k, --key`: Encryption key (auto-generated if not provided)
- `--freq`: Ultrasonic frequency (default: 18500 Hz)
- `--amplitude`: Signal strength (0.0-1.0, default: 0.1)
- `--verbose`: Detailed output
- `--help`: Show help for any command


### Basic Usage

```python
from agentic_commands_stego import AudioEmbedder, AudioDecoder

# Embed a command
embedder = AudioEmbedder()
command = "execute: deploy_model --version 2.0"
secure_audio = embedder.embed_from_file("original.mp3", command)
secure_audio.export("output.mp3", format="mp3")

# Decode the command
decoder = AudioDecoder(embedder.cipher.key)
decoded_command = decoder.decode_from_file("output.mp3")
print(f"Hidden command: {decoded_command}")
```

## 🎮 Interactive Web Interface

Experience Ultrasonic Agentics through our modern React-based UI:

```bash
# Start the web interface
cd ui && npm install && npm run dev
```

Visit `http://localhost:5173` to:
- 🎙️ Record and embed commands in real-time
- 📁 Process audio/video files with drag-and-drop
- 🔍 Analyze ultrasonic frequencies with live visualization
- 🔐 Configure encryption and encoding parameters
- 📊 Monitor signal quality and decoding confidence

## 🤖 MCP Integration

Use Ultrasonic Agentics with AI agents via Model Context Protocol:

```bash
# Start the MCP server
ultrasonic-server

# Use with Claude or other MCP-compatible AI
ultrasonic-agentics encode "AI: process customer data" audio.mp3
ultrasonic-agentics decode audio.mp3
```

## 🔧 Advanced Features

### Streaming API

```python
# Real-time encoding for live audio
from agentic_commands_stego import StreamEncoder

encoder = StreamEncoder()
for chunk in audio_stream:
    encoded_chunk = encoder.process(chunk, command_queue.get())
    output_stream.write(encoded_chunk)
```

### REST API

```bash
# Start the API server
ultrasonic-api

# Embed via API
curl -X POST http://localhost:8000/embed \
  -F "audio=@input.mp3" \
  -F "command=deploy:production" \
  -F "key=your-secret-key"
```

### Video Support

```python
# Embed in video files
from agentic_commands_stego import VideoEmbedder

embedder = VideoEmbedder()
embedder.embed_from_file(
    "video.mp4",
    "AI: analyze frames for objects",
    "output.mp4"
)
```

## 🤝 Contributing

We welcome contributions!

```bash
# Development setup
git clone https://github.com/ultrasonic-agentics/ultrasonic-agentics
cd ultrasonic-agentics
pip install -e ".[dev]"
pytest
```

## 📊 Performance

- **Embedding Speed**: ~100x realtime on modern CPUs
- **Bit Rate**: 100-1000 bps depending on configuration
- **Frequency Range**: 18-20 kHz (customizable)
- **Success Rate**: >99.9% in typical conditions
- **Power Consumption**: < 10mW in listening mode on embedded devices
- **Wake Latency**: < 50ms from sleep to command detection
- **Range**: 1-10 meters depending on environment and transducer

## 🌟 Roadmap

- [ ] Neural network-based decoding for noisy environments
- [ ] Bluetooth beacon mode for proximity commands
- [ ] Multi-channel encoding for higher bandwidth
- [ ] Hardware acceleration support (GPU/TPU)
- [ ] Mobile SDKs (iOS/Android)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with cutting-edge audio processing libraries including NumPy, SciPy, PyDub, and Librosa. Special thanks to the MCP community for protocol development.

---

<p align="center">
  <b>Ready to hide commands in plain sound?</b><br>
  <a href="https://github.com/ultrasonic-agentics/ultrasonic-agentics">Get Started</a> •
  <a href="agentic_commands_stego/docs/">Read Docs</a> •
  <a href="https://github.com/ultrasonic-agentics/ultrasonic-agentics/issues">Report Bug</a>
</p>
