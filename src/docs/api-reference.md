# Ultrasonic Agentics API Reference

Complete API documentation for all classes, methods, and endpoints in the Ultrasonic Agentics framework.

## Table of Contents

1. [Core Classes](#core-classes)
2. [Ultrasonic Processing](#ultrasonic-processing)
3. [Video Steganography](#video-steganography)
4. [Cryptographic Services](#cryptographic-services)
5. [HTTP API Endpoints](#http-api-endpoints)
6. [Configuration](#configuration)
7. [Error Handling](#error-handling)

## Core Classes

### UltrasonicEncoder

Encodes data into ultrasonic audio frequencies using FSK modulation.

#### Constructor

```python
UltrasonicEncoder(
    freq_0: float = 18500,
    freq_1: float = 19500,
    sample_rate: int = 48000,
    bit_duration: float = 0.01,
    amplitude: float = 0.1
)
```

**Parameters:**
- `freq_0`: Frequency for bit '0' in Hz (default: 18500)
- `freq_1`: Frequency for bit '1' in Hz (default: 19500)
- `sample_rate`: Audio sample rate in Hz (default: 48000)
- `bit_duration`: Duration of each bit in seconds (default: 0.01)
- `amplitude`: Signal amplitude 0.0-1.0 (default: 0.1)

#### Methods

##### `encode_payload(payload: bytes, add_preamble: bool = True) -> np.ndarray`

Encodes payload bytes into ultrasonic audio signal.

**Parameters:**
- `payload`: Binary data to encode
- `add_preamble`: Whether to add synchronization preamble

**Returns:** Audio signal as numpy array

**Example:**
```python
encoder = UltrasonicEncoder()
command = "execute:status_check".encode('utf-8')
audio_data = encoder.encode_payload(command)
```

##### `create_audio_segment(signal: np.ndarray) -> AudioSegment`

Converts numpy signal to AudioSegment for file operations.

**Parameters:**
- `signal`: Audio signal as numpy array

**Returns:** AudioSegment object

##### `estimate_payload_duration(payload_size: int) -> float`

Estimates duration needed for given payload size.

**Parameters:**
- `payload_size`: Size of payload in bytes

**Returns:** Duration in seconds

##### `get_frequency_range() -> Tuple[float, float]`

Returns frequency range used for encoding.

**Returns:** Tuple of (min_freq, max_freq)

##### `set_frequencies(freq_0: float, freq_1: float) -> None`

Sets new frequencies for FSK modulation.

**Parameters:**
- `freq_0`: Frequency for bit '0' in Hz
- `freq_1`: Frequency for bit '1' in Hz

##### `set_amplitude(amplitude: float) -> None`

Sets signal amplitude.

**Parameters:**
- `amplitude`: Signal amplitude (0.0 to 1.0)

### UltrasonicDecoder

Decodes data from ultrasonic audio frequencies using FSK demodulation.

#### Constructor

```python
UltrasonicDecoder(
    freq_0: float = 18500,
    freq_1: float = 19500,
    sample_rate: int = 48000,
    bit_duration: float = 0.01,
    detection_threshold: float = 0.1
)
```

**Parameters:**
- `freq_0`: Frequency for bit '0' in Hz (default: 18500)
- `freq_1`: Frequency for bit '1' in Hz (default: 19500)
- `sample_rate`: Audio sample rate in Hz (default: 48000)
- `bit_duration`: Duration of each bit in seconds (default: 0.01)
- `detection_threshold`: Minimum signal strength for detection (default: 0.1)

#### Methods

##### `decode_payload(audio_signal: np.ndarray) -> Optional[bytes]`

Decodes payload from audio signal.

**Parameters:**
- `audio_signal`: Audio signal as numpy array

**Returns:** Decoded payload bytes, or None if decoding fails

**Example:**
```python
decoder = UltrasonicDecoder()
decoded_data = decoder.decode_payload(audio_signal)
if decoded_data:
    command = decoded_data.decode('utf-8')
```

##### `detect_signal_presence(audio_signal: np.ndarray) -> bool`

Checks if ultrasonic signal is present in audio.

**Parameters:**
- `audio_signal`: Audio signal to analyze

**Returns:** True if ultrasonic signal detected

##### `get_signal_strength(audio_signal: np.ndarray) -> float`

Gets signal strength in ultrasonic range.

**Parameters:**
- `audio_signal`: Audio signal to analyze

**Returns:** Signal strength (0.0 to 1.0)

##### `set_frequencies(freq_0: float, freq_1: float) -> None`

Sets new frequencies for FSK demodulation.

**Parameters:**
- `freq_0`: Frequency for bit '0' in Hz
- `freq_1`: Frequency for bit '1' in Hz

##### `set_detection_threshold(threshold: float) -> None`

Sets signal detection threshold.

**Parameters:**
- `threshold`: New detection threshold

## Ultrasonic Processing

### AudioEmbedder

High-level interface for embedding commands in audio files.

#### Methods

##### `embed_file(input_path: str, output_path: str, command: str, obfuscate: bool = True, bitrate: str = "192k") -> bool`

Embeds command in audio file.

**Parameters:**
- `input_path`: Path to input audio file
- `output_path`: Path for output file
- `command`: Command string to embed
- `obfuscate`: Whether to encrypt the command
- `bitrate`: Output audio bitrate

**Returns:** True if successful

### AudioDecoder

High-level interface for decoding commands from audio files.

#### Methods

##### `decode_file(file_path: str) -> Optional[str]`

Decodes command from audio file.

**Parameters:**
- `file_path`: Path to audio file

**Returns:** Decoded command string, or None if not found

##### `analyze_audio(file_path: str) -> dict`

Analyzes audio file for steganographic content.

**Parameters:**
- `file_path`: Path to audio file

**Returns:** Analysis results dictionary

## Video Steganography

### VideoEmbedder

Interface for embedding commands in video files.

#### Methods

##### `embed_file(input_path: str, output_path: str, command: str, obfuscate: bool = True, audio_bitrate: str = "192k") -> bool`

Embeds command in video file's audio track.

**Parameters:**
- `input_path`: Path to input video file
- `output_path`: Path for output file
- `command`: Command string to embed
- `obfuscate`: Whether to encrypt the command
- `audio_bitrate`: Audio track bitrate

**Returns:** True if successful

### VideoDecoder

Interface for decoding commands from video files.

#### Methods

##### `decode_file(file_path: str) -> Optional[str]`

Decodes command from video file.

**Parameters:**
- `file_path`: Path to video file

**Returns:** Decoded command string, or None if not found

##### `analyze_video(file_path: str) -> dict`

Analyzes video file for steganographic content.

**Parameters:**
- `file_path`: Path to video file

**Returns:** Analysis results dictionary

## Cryptographic Services

### CipherService

Handles encryption and decryption of commands.

#### Static Methods

##### `generate_key(length: int) -> bytes`

Generates cryptographically secure random key.

**Parameters:**
- `length`: Key length in bytes

**Returns:** Random key bytes

#### Constructor

```python
CipherService(key: Optional[bytes] = None)
```

**Parameters:**
- `key`: Encryption key (generates random if None)

#### Methods

##### `encrypt(data: bytes) -> bytes`

Encrypts data using AES-256-GCM.

**Parameters:**
- `data`: Data to encrypt

**Returns:** Encrypted data (includes nonce and tag)

##### `decrypt(encrypted_data: bytes) -> bytes`

Decrypts data using AES-256-GCM.

**Parameters:**
- `encrypted_data`: Encrypted data to decrypt

**Returns:** Decrypted data

**Raises:** `CryptoError` if decryption fails

##### `set_key_from_base64(key_b64: str) -> None`

Sets encryption key from base64 string.

**Parameters:**
- `key_b64`: Base64 encoded key

##### `get_key() -> bytes`

Gets current encryption key.

**Returns:** Encryption key bytes

## HTTP API Endpoints

### Audio Endpoints

#### POST `/embed/audio`

Embeds command into audio file.

**Request:**
- `file`: Audio file (multipart/form-data)
- `command`: Command string (form field)
- `obfuscate`: Whether to encrypt (form field, default: true)
- `bitrate`: Output bitrate (form field, default: "192k")
- `ultrasonic_freq`: Base frequency in Hz (form field, default: 18500)
- `amplitude`: Signal amplitude (form field, default: 0.1)

**Response:** Audio file with embedded command

**Example:**
```bash
curl -X POST http://localhost:8000/embed/audio \
  -F "file=@input.wav" \
  -F "command=execute:status_check" \
  -F "obfuscate=true" \
  -F "ultrasonic_freq=19000"
```

#### POST `/decode/audio`

Decodes command from audio file.

**Request:**
- `file`: Audio file (multipart/form-data)

**Response:**
```json
{
  "command": "execute:status_check",
  "analysis": {
    "signal_detected": true,
    "signal_strength": 0.85,
    "frequency_range": [18500, 19500],
    "duration": 2.5
  },
  "success": true
}
```

#### POST `/analyze/audio`

Analyzes audio file for steganographic content.

**Request:**
- `file`: Audio file (multipart/form-data)

**Response:**
```json
{
  "signal_detected": true,
  "signal_strength": 0.85,
  "frequency_range": [18500, 19500],
  "duration": 2.5,
  "sample_rate": 44100,
  "estimated_payload_size": 32
}
```

### Video Endpoints

#### POST `/embed/video`

Embeds command into video file.

**Request:**
- `file`: Video file (multipart/form-data)
- `command`: Command string (form field)
- `obfuscate`: Whether to encrypt (form field, default: true)
- `audio_bitrate`: Audio bitrate (form field, default: "192k")
- `ultrasonic_freq`: Base frequency in Hz (form field, default: 18500)
- `amplitude`: Signal amplitude (form field, default: 0.1)

**Response:** Video file with embedded command

#### POST `/decode/video`

Decodes command from video file.

**Request:**
- `file`: Video file (multipart/form-data)

**Response:** Same format as audio decode

#### POST `/analyze/video`

Analyzes video file for steganographic content.

**Request:**
- `file`: Video file (multipart/form-data)

**Response:** Same format as audio analysis

### Configuration Endpoints

#### POST `/config/frequencies`

Configures ultrasonic frequencies.

**Request:**
- `freq_0`: Frequency for bit '0' (form field)
- `freq_1`: Frequency for bit '1' (form field)

**Response:**
```json
{
  "success": true,
  "message": "Frequencies updated to 18000 Hz and 19000 Hz",
  "freq_0": 18000,
  "freq_1": 19000
}
```

#### POST `/config/key`

Configures encryption key.

**Request:**
- `key_base64`: Base64 encoded key (form field)

**Response:**
```json
{
  "success": true,
  "message": "Encryption key updated successfully"
}
```

### Information Endpoints

#### GET `/info`

Gets API information.

**Response:**
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

#### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Steganography service is running"
}
```

## Configuration

### Environment Variables

- `ULTRASONIC_FREQUENCY`: Default ultrasonic frequency
- `ULTRASONIC_SAMPLE_RATE`: Default sample rate
- `CRYPTO_PASSWORD`: Default encryption password
- `API_HOST`: API server host
- `API_PORT`: API server port

### Configuration File Format

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

## Error Handling

### Exception Classes

#### `CryptoError`

Raised when cryptographic operations fail.

**Attributes:**
- `message`: Error description

#### `EncodingError`

Raised when audio encoding fails.

**Attributes:**
- `message`: Error description
- `frequency`: Problematic frequency (if applicable)

#### `DecodingError`

Raised when audio decoding fails.

**Attributes:**
- `message`: Error description
- `signal_strength`: Detected signal strength

### HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid parameters, unsupported format)
- `500`: Internal Server Error (processing failure)

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Type Definitions

### Command Format

Commands follow this structure:
```
action:parameter:timestamp
```

**Examples:**
- `execute:status_check:1640995200`
- `transmit:sensor_data:1640995201`
- `configure:mode=stealth:1640995202`

### Analysis Result

```python
{
    "signal_detected": bool,
    "signal_strength": float,  # 0.0 to 1.0
    "frequency_range": List[float],  # [min_freq, max_freq]
    "duration": float,  # seconds
    "sample_rate": int,
    "estimated_payload_size": int  # bytes
}
```

### Frequency Range

Valid ultrasonic frequencies: 16,000 Hz to 24,000 Hz (limited by Nyquist frequency and hardware capabilities)

### Supported File Formats

**Audio:**
- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- OGG (.ogg)
- M4A (.m4a)

**Video:**
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)