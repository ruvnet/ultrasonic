# 🔊 Ultrasonic Agentics

**Hide AI Secret Commands & Data in Plain Sound** • Secure steganographic framework for embedding invisible commands in audio and video

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
- **🎯 High Reliability**: Advanced error correction ensures accurate decoding

## 🎯 Use Cases

- **AI Agent Coordination**: Transmit commands between AI systems covertly
- **Digital Watermarking**: Protect your audio/video content with invisible signatures
- **Secure Communications**: Send encrypted messages through public audio channels
- **IoT Command & Control**: Control smart devices using inaudible sound
- **Interactive Media**: Create audio/video content with hidden interactive elements

## 🛠️ Quick Start

### Installation

```bash
# Install from PyPI
pip install ultrasonic-agentics

# With all features
pip install ultrasonic-agentics[all]
```

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

## 📚 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Security Best Practices](docs/security.md)
- [MCP Integration](docs/mcp-integration.md)
- [Examples & Tutorials](agentic_commands_stego/examples/)

## 🏗️ Architecture

Ultrasonic Agentics uses a sophisticated signal processing pipeline:

1. **Command Encryption**: AES-256-GCM with key derivation
2. **Binary Encoding**: Efficient bit packing with error correction
3. **FSK Modulation**: Frequency-shift keying at 18.5-19.5 kHz
4. **Signal Injection**: Psychoacoustic masking for seamless integration
5. **Adaptive Decoding**: ML-enhanced signal detection and extraction

## 🔒 Security Features

- **End-to-End Encryption**: Commands are never transmitted in plaintext
- **Authentication**: HMAC prevents tampering and ensures message integrity
- **Key Management**: Secure key generation and optional key rotation
- **Obfuscation**: Multiple encoding layers prevent casual detection

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

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
  <a href="https://github.com/ultrasonic-agentics/ultrasonic-agentics/docs">Read Docs</a> •
  <a href="https://github.com/ultrasonic-agentics/ultrasonic-agentics/issues">Report Bug</a>
</p>
