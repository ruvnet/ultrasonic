# Ultrasonic Agentics

A comprehensive steganography framework for embedding and extracting agentic commands in audio and video media using ultrasonic frequencies. This project provides tools for covert communication and command transmission through multimedia channels.

## Features

- **Ultrasonic Audio Encoding/Decoding**: Embed and extract commands in high-frequency audio ranges
- **Video Steganography**: Hide data in video frames using LSB techniques
- **Cryptographic Security**: Built-in encryption for secure command transmission
- **RESTful API**: HTTP server for remote encoding/decoding operations
- **Calibration System**: Automatic frequency calibration for optimal transmission
- **Comprehensive Testing**: Full test suite with pytest framework

## Installation

### From PyPI (Recommended)

```bash
pip install ultrasonic-agentics
```

### From Source

```bash
git clone https://github.com/yourusername/ultrasonic-agentics.git
cd ultrasonic-agentics
pip install -e .
```

## Quick Start

### Basic Usage

```python
from ultrasonic_agentics import UltrasonicEncoder, UltrasonicDecoder

# Encode a command
encoder = UltrasonicEncoder()
audio_data = encoder.encode("execute:status_check")

# Decode the command
decoder = UltrasonicDecoder()
command = decoder.decode(audio_data)
print(f"Decoded: {command}")
```

### API Server

```bash
# Start the API server
python -m ultrasonic_agentics.server

# Encode via API
curl -X POST http://localhost:8000/encode \
  -H "Content-Type: application/json" \
  -d '{"command": "execute:status_check"}'
```

## Documentation

- [User Guide](docs/user-guide.md) - Comprehensive usage instructions
- [API Reference](docs/api-reference.md) - Complete API documentation
- [Advanced Usage](docs/advanced-usage.md) - Advanced features and configurations
- [Examples](examples/) - Code examples and tutorials

## Project Structure

```
ultrasonic_agentics/
├── crypto/           # Encryption and security modules
├── embed/            # Encoding implementations
├── decode/           # Decoding implementations
├── server/           # HTTP API server
├── tests/            # Test suite
├── docs/             # Documentation
└── examples/         # Usage examples
```

## Requirements

- Python 3.8+
- NumPy
- SciPy
- librosa
- opencv-python
- cryptography
- fastapi
- uvicorn

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ultrasonic_agentics

# Run specific test categories
pytest tests/test_ultrasonic_encoder.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Notice

This tool is designed for legitimate research and authorized testing purposes. Users are responsible for complying with applicable laws and regulations regarding steganography and covert communications.

## Acknowledgments

- Built using modern Python steganography techniques
- Inspired by research in ultrasonic communication systems
- Designed for integration with agentic AI systems