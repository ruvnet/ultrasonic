# Ultrasonic Agentics Examples

This directory contains practical examples demonstrating various features and use cases of the Ultrasonic Agentics framework.

## Examples Overview

### 1. `basic_encoding.py`
**Purpose**: Fundamental encoding and decoding operations  
**Key Features**:
- Basic command encoding/decoding
- Testing different command types
- Frequency range testing
- Amplitude sensitivity analysis
- Noise resilience testing
- Payload size testing

**Usage**:
```bash
python basic_encoding.py
```

**What you'll learn**:
- How to initialize encoders and decoders
- Basic encoding/decoding workflow
- Parameter optimization techniques
- Signal quality analysis

### 2. `audio_file_processing.py`
**Purpose**: Working with audio files and mixing techniques  
**Key Features**:
- Embedding commands in existing audio files
- Steganographic embedding (hard to detect)
- Batch processing multiple files
- Audio format conversion testing
- Signal mixing techniques

**Usage**:
```bash
python audio_file_processing.py
```

**What you'll learn**:
- How to mix ultrasonic signals with background audio
- Steganographic techniques for covert communication
- Batch processing workflows
- Audio format compatibility

### 3. `api_client.py`
**Purpose**: Interacting with the HTTP API service  
**Key Features**:
- REST API client implementation
- Audio embedding via HTTP endpoints
- Command decoding through API
- Configuration management
- Error handling and performance testing

**Usage**:
```bash
# First, start the API server:
python -m ultrasonic_agentics.server

# Then run the client examples:
python api_client.py
```

**What you'll learn**:
- How to integrate with the HTTP API
- Remote processing capabilities
- API error handling
- Performance considerations for API calls

## Prerequisites

Make sure you have all required dependencies installed:

```bash
pip install -r ../requirements.txt
```

Additional dependencies for examples:
- `matplotlib` (for signal analysis visualizations)
- `requests` (for API client)
- `pydub` (for audio file processing)

## Running Examples

### Quick Start
To run all basic examples:
```bash
python basic_encoding.py
```

### API Examples
1. Start the API server in one terminal:
```bash
cd ..
python -m server.api
```

2. Run the API client examples in another terminal:
```bash
python api_client.py
```

### Individual Example Sections
Each example file contains multiple test functions. You can run specific tests by modifying the `if __name__ == "__main__":` section or importing specific functions:

```python
from basic_encoding import frequency_range_test
frequency_range_test()
```

## Example Outputs

### Successful Encoding/Decoding
```
=== Basic Encoding/Decoding Example ===
Original command: execute:status_check
Encoding command into ultrasonic signal...
Generated signal: 21600 samples
Signal duration: 0.45 seconds
Frequency range: (18500.0, 19500.0) Hz
Saved encoded audio to: encoded_command.wav
Decoding signal...
Decoded command: execute:status_check
✓ Encoding/Decoding successful!
```

### API Success Response
```json
{
  "command": "execute:status_check",
  "analysis": {
    "signal_detected": true,
    "signal_strength": 0.85,
    "frequency_range": [18500, 19500],
    "duration": 0.45
  },
  "success": true
}
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'ultrasonic_agentics'
   ```
   **Solution**: Make sure you're running from the correct directory and the package is properly installed.

2. **Audio Decoding Failures**
   ```
   ✗ Decoding failed - no signal detected
   ```
   **Solutions**:
   - Increase amplitude in encoder
   - Lower detection threshold in decoder
   - Check frequency alignment
   - Reduce background noise

3. **API Connection Errors**
   ```
   ✗ API is not accessible
   ```
   **Solution**: Ensure the API server is running on the correct port (default: 8000).

4. **Audio Format Issues**
   ```
   ✗ MP3 format: Decode failed
   ```
   **Solution**: Some audio formats may introduce compression artifacts. Try using WAV format for best results.

### Performance Optimization

1. **Slow Processing**
   - Use shorter audio files for testing
   - Reduce sample rate if quality permits
   - Enable parallel processing for batch operations

2. **Low Success Rates**
   - Increase signal amplitude
   - Use error correction techniques
   - Test in quieter environments
   - Optimize frequency selection

### Debug Mode

Enable debug logging in any example:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your example code here
```

## Advanced Usage

### Custom Parameter Testing
Create your own parameter combinations:

```python
from basic_encoding import *

# Test custom frequencies
encoder = UltrasonicEncoder(freq_0=20000, freq_1=21000, amplitude=0.3)
decoder = UltrasonicDecoder(freq_0=20000, freq_1=21000, detection_threshold=0.05)

# Test your command
test_command = "custom:test"
signal = encoder.encode_payload(test_command.encode())
result = decoder.decode_payload(signal)
```

### Integration Examples
These examples can be integrated into larger applications:

```python
# Use the UltrasonicAgenticsClient in your application
from api_client import UltrasonicAgenticsClient

client = UltrasonicAgenticsClient("http://your-api-server:8000")

# Embed command in your audio processing pipeline
def process_audio_with_command(audio_file, command):
    embedded_data = client.embed_audio_command(audio_file, command)
    # Process embedded_data further...
    return embedded_data
```

## Next Steps

After running these examples:

1. **Explore Advanced Features**: Check `docs/advanced-usage.md` for complex scenarios
2. **Integration**: Use these patterns in your own applications
3. **Optimization**: Tune parameters for your specific use case
4. **Security**: Implement proper encryption and validation for production use

## Contributing

Found an issue or want to add more examples? Please:

1. Check existing issues in the repository
2. Create a new example following the existing patterns
3. Include proper error handling and documentation
4. Test your example thoroughly before submitting