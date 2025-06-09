# Ultrasonic Agentics Documentation

Welcome to the comprehensive documentation for **Ultrasonic Agentics**, a cutting-edge steganography framework for embedding and extracting agentic commands in audio and video media using ultrasonic frequencies.

## 🚀 Quick Navigation

### **Getting Started**
- [📦 Installation Guide](installation.md) - Complete setup instructions for all platforms
- [📖 User Guide](user-guide.md) - Comprehensive usage instructions and tutorials
- [⚡ Quick Start Examples](../examples/README.md) - Jump straight into coding

### **API & Integration**
- [💻 CLI Usage Guide](cli-usage.md) - Command-line interface and automation
- [🔌 MCP Integration](mcp-integration.md) - Model Context Protocol for AI assistants
- [🔧 Complete API Reference](api-complete.md) - Full Python and HTTP API documentation
- [🌐 REST API Guide](api-reference.md) - HTTP endpoints and web integration
- [💻 Developer Guide](developer-guide.md) - Contributing and development setup

### **Production & Operations**
- [🚀 Deployment Guide](deployment.md) - Production deployment and scaling
- [🔒 Security Guide](security.md) - Security best practices and compliance
- [🛠 Troubleshooting](troubleshooting.md) - Common issues and solutions

### **Technical Deep Dive**
- [🏗 Architecture Overview](architecture.md) - Technical specifications and design
- [📈 Advanced Usage](advanced-usage.md) - Complex scenarios and optimization
- [📋 Changelog](../../CHANGELOG.md) - Version history and roadmap

---

## 📚 Documentation Overview

### Core Concepts

**Ultrasonic Agentics** uses advanced **Frequency Shift Keying (FSK)** modulation to embed encrypted commands in the near-ultrasonic frequency range (18-22 kHz), making them imperceptible to humans while maintaining high reliability for automated systems.

#### Key Technologies:
- **🎵 Ultrasonic Steganography**: FSK modulation in 18-22 kHz range
- **🔐 AES-256-GCM Encryption**: Military-grade authenticated encryption
- **💻 Command Line Interface**: Full-featured CLI with rich output
- **🤖 MCP Integration**: Native Model Context Protocol support for AI assistants
- **📡 Real-time Processing**: Live audio stream monitoring and encoding
- **🌐 REST API**: FastAPI-based web service with async processing
- **🎬 Multi-format Support**: Audio (MP3, WAV, FLAC) and Video (MP4, AVI, MOV)

---

## 🎯 Quick Start

### Installation
```bash
# Quick install
pip install ultrasonic-agentics

# With all features
pip install ultrasonic-agentics[all]
```

### Basic Usage
```python
from ultrasonic_agentics import UltrasonicEncoder, UltrasonicDecoder

# Encode a command
encoder = UltrasonicEncoder()
command = "execute:status_check"
audio_signal = encoder.encode_payload(command.encode())

# Decode the command
decoder = UltrasonicDecoder()
decoded_bytes = decoder.decode_payload(audio_signal)
print(decoded_bytes.decode('utf-8'))  # "execute:status_check"
```

### MCP Server
```bash
# Start the MCP server for AI assistant integration
agentic-stego server

# Or start HTTP API server (legacy)
python -m agentic_commands_stego.server.api
```

See [MCP Integration Guide](mcp-integration.md) for AI assistant setup.

---

## 📖 Documentation Structure

### 🔰 For New Users
1. **[Installation Guide](installation.md)** - Get up and running quickly
2. **[User Guide](user-guide.md)** - Learn the basics with examples
3. **[Examples](../examples/README.md)** - Hands-on tutorials and code samples

### 👨‍💻 For Developers
1. **[CLI Usage Guide](cli-usage.md)** - Command-line interface and automation
2. **[MCP Integration](mcp-integration.md)** - AI assistant integration setup
3. **[Developer Guide](developer-guide.md)** - Contributing and development setup
4. **[API Reference](api-complete.md)** - Complete API documentation
5. **[Architecture](architecture.md)** - Technical deep dive

### 🚀 For Operations
1. **[Deployment Guide](deployment.md)** - Production deployment strategies
2. **[Security Guide](security.md)** - Security hardening and best practices
3. **[Troubleshooting](troubleshooting.md)** - Issue resolution and debugging

---

## 🎮 Interactive Examples

### Basic Encoding/Decoding
```python
# See: examples/basic_encoding.py
from ultrasonic_agentics.embed import UltrasonicEncoder
from ultrasonic_agentics.decode import UltrasonicDecoder

encoder = UltrasonicEncoder(freq_0=18500, freq_1=19500, amplitude=0.2)
decoder = UltrasonicDecoder(freq_0=18500, freq_1=19500)

command = "execute:system_status"
signal = encoder.encode_payload(command.encode())
result = decoder.decode_payload(signal)
```

### File Processing
```python
# See: examples/audio_file_processing.py
from ultrasonic_agentics.embed import AudioEmbedder
from ultrasonic_agentics.decode import AudioDecoder

embedder = AudioEmbedder()
decoder = AudioDecoder()

# Embed command in audio file
embedder.embed_file("input.wav", "output.wav", "execute:task")

# Decode from file
command = decoder.decode_file("output.wav")
```

### API Integration
```python
# See: examples/api_client.py
import requests

# Embed command via API
files = {'file': open('audio.wav', 'rb')}
data = {'command': 'execute:status', 'frequency': 19000}
response = requests.post('http://localhost:8000/embed/audio', 
                        files=files, data=data)
```

---

## 🎯 Use Cases & Applications

### 🤖 Agentic Systems
- **Command Distribution**: Securely distribute commands to distributed agents
- **Covert Operations**: Embed instructions in media for stealth operations
- **IoT Device Management**: Control devices through audio/video channels

### 🎵 Media Applications
- **Audio Watermarking**: Embed metadata in audio content
- **Content Authentication**: Verify media authenticity
- **Smart Broadcasting**: Trigger actions in smart devices via broadcast media

### 🔒 Security Applications
- **Covert Communication**: Secure communication through public channels
- **Digital Forensics**: Embed tracking information in media files
- **Anti-Tampering**: Detect unauthorized modifications to audio/video

---

## 🛠 Command Line Tools

After installation, the CLI is available as `agentic-stego`:

```bash
# Embed commands into media files
agentic-stego embed audio.wav "execute:task" --output encoded.wav

# Decode commands from media files
agentic-stego decode encoded.wav

# Start the MCP server for AI assistant integration
agentic-stego server --port 3000

# Analyze media files for embedded content
agentic-stego analyze suspicious.wav

# Configure system settings
agentic-stego config --show
```

See the [CLI Usage Guide](cli-usage.md) for complete documentation.

---

## 🔬 Technical Specifications

| Feature | Specification |
|---------|---------------|
| **Frequency Range** | 17-22 kHz (near-ultrasonic) |
| **Modulation** | Binary FSK (Frequency Shift Keying) |
| **Data Rate** | ~100 bps (configurable) |
| **Encryption** | AES-256-GCM authenticated encryption |
| **Error Correction** | Parity-based with 10% tolerance |
| **Audio Formats** | MP3, WAV, FLAC, OGG, M4A |
| **Video Formats** | MP4, AVI, MOV, MKV |
| **Sample Rates** | 44.1 kHz, 48 kHz (others supported) |

---

## 🌟 Key Features

### 🎵 Advanced Audio Processing
- **Near-ultrasonic frequencies** (18-22 kHz) for human imperceptibility
- **Adaptive amplitude control** based on background noise
- **Real-time audio monitoring** with live processing
- **Multi-format support** for audio and video files

### 🔐 Military-Grade Security
- **AES-256-GCM encryption** with authenticated encryption
- **Key rotation and lifecycle management**
- **Input validation and sanitization**
- **Secure key derivation** from passwords

### 🚀 Production-Ready Infrastructure
- **FastAPI-based REST API** with async processing
- **Docker containerization** for easy deployment
- **Kubernetes manifests** for scalable orchestration
- **Comprehensive monitoring** and logging

### 🧪 Robust Testing & Quality
- **TDD methodology** with comprehensive test coverage
- **Performance benchmarking** and optimization
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Continuous integration** with automated testing

---

## 📞 Support & Community

### 📖 Documentation
- **[User Guide](user-guide.md)** - Comprehensive usage instructions
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[FAQ](troubleshooting.md#frequently-asked-questions)** - Frequently asked questions

### 🐛 Issue Reporting
- **[GitHub Issues](https://github.com/ultrasonic-agentics/ultrasonic-agentics/issues)** - Bug reports and feature requests
- **[Security Issues](security.md#vulnerability-disclosure)** - Responsible disclosure process

### 💬 Community
- **[Discussions](https://github.com/ultrasonic-agentics/ultrasonic-agentics/discussions)** - Community forum
- **[Discord](https://discord.gg/ultrasonic-agentics)** - Real-time chat support
- **[Stack Overflow](https://stackoverflow.com/questions/tagged/ultrasonic-agentics)** - Technical Q&A

---

## 📋 Contributing

We welcome contributions! See the **[Developer Guide](developer-guide.md)** for:

- **Development environment setup**
- **Code style and conventions**
- **Testing requirements**
- **Pull request process**
- **Community guidelines**

### Quick Contribution Setup
```bash
# Clone the repository
git clone https://github.com/ultrasonic-agentics/ultrasonic-agentics.git
cd ultrasonic-agentics

# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]

# Run tests
pytest

# Format code
black .
isort .
```

---

## 📜 License & Legal

- **License**: MIT License (see [LICENSE](../../LICENSE))
- **Copyright**: © 2024 Ultrasonic Agentics Team
- **Export Control**: Review export regulations for cryptographic software
- **Compliance**: See [Security Guide](security.md) for regulatory considerations

---

## 🗺 Roadmap

### Version 1.1 (Q2 2024)
- Enhanced error correction algorithms
- WebSocket real-time streaming
- Mobile SDK (iOS/Android)

### Version 1.2 (Q3 2024)
- Machine learning-based signal detection
- Hardware acceleration support
- Advanced steganographic techniques

### Version 2.0 (Q1 2025)
- Multi-channel encoding
- Blockchain integration
- Enterprise management console

See the complete roadmap in our **[Changelog](../../CHANGELOG.md)**.

---

*Last updated: January 2024 | Version 1.0.0*