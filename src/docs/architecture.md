# Ultrasonic Agentics Architecture Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagrams](#architecture-diagrams)
3. [Core Components](#core-components)
4. [Ultrasonic Communication Protocol](#ultrasonic-communication-protocol)
5. [Cryptographic Implementation](#cryptographic-implementation)
6. [Signal Processing Architecture](#signal-processing-architecture)
7. [API Design and Patterns](#api-design-and-patterns)
8. [Data Flow and Component Interactions](#data-flow-and-component-interactions)
9. [Performance Characteristics](#performance-characteristics)
10. [Scalability Considerations](#scalability-considerations)
11. [Technology Stack](#technology-stack)
12. [Design Decisions and Trade-offs](#design-decisions-and-trade-offs)
13. [Extension Points](#extension-points)
14. [Mathematical Foundations](#mathematical-foundations)

## System Overview

The Ultrasonic Agentics system is a sophisticated steganographic platform that enables secure, covert communication by embedding encrypted commands within audio and video files using near-ultrasonic frequencies. The system operates in the 17-22 kHz frequency range, leveraging Frequency Shift Keying (FSK) modulation to encode digital data while maintaining imperceptibility to human hearing.

### Key Capabilities

- **Steganographic Embedding**: Hide encrypted commands in audio/video media
- **Real-time Processing**: Live audio stream monitoring and command injection
- **Multi-format Support**: Audio (MP3, WAV, FLAC, OGG, M4A) and Video (MP4, AVI, MOV, MKV)
- **Cryptographic Security**: AES-256-GCM encryption with authenticated encryption
- **Signal Detection**: Automated presence detection and signal strength analysis
- **RESTful API**: FastAPI-based service for integration with external systems

## Architecture Diagrams

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Ultrasonic Agentics System                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐  │
│  │   Client Apps   │    │   Web Frontend  │    │  CLI Tools  │  │
│  └─────────────────┘    └─────────────────┘    └─────────────┘  │
│            │                       │                     │       │
│            └───────────────────────┼─────────────────────┘       │
│                                    │                             │
├─────────────────────────────────────┼─────────────────────────────┤
│                FastAPI Server      │                             │
│  ┌─────────────────────────────────┴─────────────────────────┐   │
│  │            API Layer (server/api.py)                     │   │
│  │  • /embed/audio     • /decode/audio                      │   │
│  │  • /embed/video     • /decode/video                      │   │
│  │  • /analyze/*       • /config/*                          │   │
│  └─────────────────────────────────┬─────────────────────────┘   │
│                                    │                             │
├─────────────────────────────────────┼─────────────────────────────┤
│              Core Services          │                             │
│  ┌─────────────────┐  ┌─────────────┴──┐  ┌─────────────────┐    │
│  │  AudioEmbedder  │  │ VideoEmbedder  │  │  AudioDecoder   │    │
│  │   (embed/)      │  │   (embed/)     │  │   (decode/)     │    │
│  └─────────────────┘  └────────────────┘  └─────────────────┘    │
│           │                     │                   │             │
│           └─────────────────────┼───────────────────┘             │
│                                 │                                 │
│  ┌─────────────────────────────┴─────────────────────────────┐   │
│  │             Ultrasonic Layer                             │   │
│  │  ┌─────────────────┐      ┌─────────────────────────────┐ │   │
│  │  │UltrasonicEncoder│      │    UltrasonicDecoder        │ │   │
│  │  │  • FSK Encoding │      │  • FSK Decoding             │ │   │
│  │  │  • Preamble Gen │      │  • Signal Detection         │ │   │
│  │  │  • Windowing    │      │  • Correlation Analysis     │ │   │
│  │  └─────────────────┘      └─────────────────────────────┘ │   │
│  └─────────────────────────────┬─────────────────────────────┘   │
│                                │                                 │
│  ┌─────────────────────────────┴─────────────────────────────┐   │
│  │             Cryptographic Layer                          │   │
│  │                   CipherService                          │   │
│  │  • AES-256-GCM Encryption    • Obfuscation/Deobfuscation │   │
│  │  • Key Management            • Authenticated Encryption  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Signal Processing Pipeline

```
Input Command → Encryption → Ultrasonic Encoding → Audio Merging → Output Media
     │               │              │                    │             │
     │               │              │                    │             │
     ▼               ▼              ▼                    ▼             ▼
┌─────────┐   ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌──────────┐
│"EXECUTE"│   │ AES-256-GCM │  │ FSK at       │  │ Overlay at  │  │ Audio/   │
│Command  │──▶│ Encrypted   │─▶│ 18.5-19.5kHz │─▶│ Beginning   │─▶│ Video    │
│String   │   │ + Obfusc.   │  │ + Preamble   │  │ of Track    │  │ File     │
└─────────┘   └─────────────┘  └──────────────┘  └─────────────┘  └──────────┘
```

### Decoding Pipeline

```
Input Media → Audio Extract → Signal Detection → Ultrasonic Decode → Decryption → Command
     │             │               │                    │              │           │
     │             │               │                    │              │           │
     ▼             ▼               ▼                    ▼              ▼           ▼
┌──────────┐  ┌──────────┐  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌─────────┐
│Audio/    │  │ Extract  │  │ Band-pass   │  │ Correlation  │  │ AES-256-GCM │  │"EXECUTE"│
│Video     │─▶│ Audio    │─▶│ Filter      │─▶│ Analysis +   │─▶│ Decrypt +   │─▶│Command  │
│File      │  │ Track    │  │ 17-22kHz    │  │ FSK Decode   │  │ Deobfusc.   │  │String   │
└──────────┘  └──────────┘  └─────────────┘  └──────────────┘  └─────────────┘  └─────────┘
```

## Core Components

### 1. Ultrasonic Encoder (`embed/ultrasonic_encoder.py`)

**Purpose**: Converts binary data into ultrasonic audio signals using FSK modulation.

**Key Features**:
- **FSK Modulation**: Uses two carrier frequencies (default: 18.5kHz for '0', 19.5kHz for '1')
- **Preamble Generation**: Creates synchronization pattern for reliable detection
- **Error Correction**: Adds parity bits every 8 data bits
- **Windowing**: Applies gentle transitions to reduce spectral artifacts
- **Configurable Parameters**: Adjustable frequencies, bit duration, amplitude

**Technical Specifications**:
- **Default Frequencies**: 18,500 Hz (bit '0'), 19,500 Hz (bit '1')
- **Sample Rate**: 48,000 Hz (configurable)
- **Bit Duration**: 10ms per bit (configurable)
- **Amplitude**: 10% of full scale (configurable)
- **Preamble Pattern**: "10101010" + "11110000" + "10101010"

### 2. Ultrasonic Decoder (`decode/ultrasonic_decoder.py`)

**Purpose**: Extracts binary data from ultrasonic audio signals using correlation analysis.

**Key Features**:
- **Signal Detection**: Automated presence detection with configurable thresholds
- **Preamble Detection**: Sliding window correlation for synchronization
- **Time-Domain Correlation**: Robust bit detection using reference signals
- **Error Correction**: Parity bit verification with lenient thresholds
- **Adaptive Processing**: Consecutive low-power bit detection for end-of-transmission

**Technical Specifications**:
- **Detection Method**: Cross-correlation with reference sinusoids
- **Minimum Power Difference**: 5% between frequencies for reliable detection
- **Error Tolerance**: Up to 10% parity errors allowed
- **Band-pass Filtering**: 4th-order Butterworth filters for signal isolation

### 3. Cipher Service (`crypto/cipher.py`)

**Purpose**: Provides authenticated encryption/decryption using industry-standard cryptography.

**Key Features**:
- **AES-256-GCM**: Authenticated encryption providing confidentiality and integrity
- **Random IV Generation**: Unique initialization vector for each encryption
- **Obfuscation Support**: Optional padding to obscure payload characteristics
- **Key Management**: Secure key generation and Base64 encoding support

**Security Properties**:
- **Encryption Algorithm**: AES-256 in GCM mode
- **Authentication**: Built-in authentication tag prevents tampering
- **IV Management**: 16-byte random IV per encryption operation
- **Key Sizes**: Support for 128-bit, 192-bit, and 256-bit keys

### 4. Audio/Video Embedders

**AudioEmbedder** (`embed/audio_embedder.py`):
- Combines encryption, ultrasonic encoding, and audio merging
- Maintains original audio quality while adding imperceptible ultrasonic layer
- Supports multiple audio formats with appropriate codec settings

**VideoEmbedder** (`embed/video_embedder.py`):
- Extracts audio track, embeds command, recomposes video
- Preserves video stream while modifying audio component
- Requires MoviePy for video processing

### 5. Audio/Video Decoders

**AudioDecoder** (`decode/audio_decoder.py`):
- Real-time and file-based decoding capabilities
- Signal strength analysis and presence detection
- Optional sounddevice integration for live monitoring

## Ultrasonic Communication Protocol

### Frequency Selection Rationale

The system operates in the 17-22 kHz range for several reasons:

1. **Near-Ultrasonic Range**: Just above typical human hearing (20 Hz - 20 kHz)
2. **Equipment Compatibility**: Most audio equipment can record/reproduce these frequencies
3. **Nyquist Compliance**: Well below the Nyquist frequency for 48 kHz sampling
4. **Environmental Robustness**: Less susceptible to low-frequency noise interference

### FSK Modulation Parameters

```python
# Default Configuration
FREQ_0 = 18500  # Hz - represents binary '0'
FREQ_1 = 19500  # Hz - represents binary '1'
SEPARATION = 1000  # Hz - frequency separation
BIT_DURATION = 0.01  # seconds - 10ms per bit
SAMPLE_RATE = 48000  # Hz - audio sampling rate
```

### Frame Structure

```
┌─────────────┬──────────────┬─────────────┬─────────────┬─────────────┐
│  Preamble   │   Length     │  Payload    │   Parity    │   Silence   │
│  (24 bits)  │  (variable)  │ (variable)  │ (1 per 8)   │  (optional) │
└─────────────┴──────────────┴─────────────┴─────────────┴─────────────┘
```

### Preamble Pattern

The synchronization preamble consists of 24 bits designed for reliable detection:

```
Pattern: 101010101111000010101010
         │      ││      ││      │
         └──────┘└──────┘└──────┘
         Sync    Unique  Sync
         Pattern Marker  Pattern
```

### Error Correction Scheme

Simple parity-based error correction:
- Every 8 data bits followed by 1 parity bit
- Parity bit = XOR of the 8 data bits
- Decoder tolerates up to 10% parity errors
- Failed parity checks logged but don't necessarily abort decoding

## Cryptographic Implementation

### AES-256-GCM Details

**Encryption Process**:
1. Generate 16-byte random IV
2. Create AES-256-GCM cipher with key and IV
3. Encrypt plaintext and generate authentication tag
4. Concatenate: IV || Ciphertext || Auth_Tag

**Decryption Process**:
1. Extract IV (first 16 bytes)
2. Extract authentication tag (last 16 bytes)
3. Extract ciphertext (middle portion)
4. Verify authentication tag and decrypt

### Key Management

```python
# Key Generation
key = CipherService.generate_key(32)  # 256-bit key

# Key Serialization
key_b64 = cipher.get_key_base64()

# Key Restoration
cipher.set_key_from_base64(key_b64)
```

### Obfuscation Layer

Optional obfuscation adds random padding:
```
┌──────────────┬─────────────┬─────────────────────┐
│ Padding Size │   Padding   │   Encrypted Data    │
│   (1 byte)   │ (variable)  │     (variable)      │
└──────────────┴─────────────┴─────────────────────┘
```

## Signal Processing Architecture

### Encoding Signal Generation

The encoding process generates clean sinusoidal tones:

```python
def generate_tone(frequency, duration, sample_rate, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = amplitude * np.sin(2 * np.pi * frequency * t)
    return apply_windowing(tone)
```

### Windowing Function

Gentle windowing reduces spectral artifacts while preserving frequency purity:

```python
def apply_windowing(tone):
    window_size = max(1, len(tone) // 100)  # 1% of tone length
    fade_in = np.linspace(0.9, 1.0, window_size)
    fade_out = np.linspace(1.0, 0.9, window_size)
    
    tone[:window_size] *= fade_in
    tone[-window_size:] *= fade_out
    return tone
```

### Decoding Correlation Analysis

The decoder uses time-domain correlation for robust bit detection:

```python
def decode_bit(segment, freq_0, freq_1, sample_rate):
    t = np.linspace(0, bit_duration, len(segment), endpoint=False)
    ref_0 = np.sin(2 * np.pi * freq_0 * t)
    ref_1 = np.sin(2 * np.pi * freq_1 * t)
    
    power_0 = np.abs(np.dot(segment, ref_0))
    power_1 = np.abs(np.dot(segment, ref_1))
    
    return '0' if power_0 > power_1 else '1'
```

### Band-pass Filtering

Signal isolation using Butterworth filters:

```python
# Design band-pass filter for ultrasonic range
nyquist = sample_rate / 2
low_freq = (min_freq - 1000) / nyquist
high_freq = (max_freq + 1000) / nyquist
bp_filter = signal.butter(4, [low_freq, high_freq], btype='band')
```

## API Design and Patterns

### RESTful API Architecture

The FastAPI server provides clean, RESTful endpoints:

```
POST /embed/audio    - Embed command in audio file
POST /embed/video    - Embed command in video file
POST /decode/audio   - Decode command from audio file
POST /decode/video   - Decode command from video file
POST /analyze/audio  - Analyze audio for steganographic content
POST /analyze/video  - Analyze video for steganographic content
POST /config/frequencies - Configure ultrasonic frequencies
POST /config/key     - Update encryption key
GET  /info          - API information
GET  /health        - Health check
```

### Request/Response Patterns

**Embedding Request**:
```json
{
  "file": "multipart/form-data",
  "command": "EXECUTE: system status",
  "obfuscate": true,
  "bitrate": "192k",
  "ultrasonic_freq": 18500,
  "amplitude": 0.1
}
```

**Analysis Response**:
```json
{
  "file_path": "/path/to/file.mp3",
  "duration_seconds": 120.5,
  "sample_rate": 48000,
  "channels": 2,
  "has_ultrasonic_signal": true,
  "signal_strength": 0.234,
  "frequency_range": [18500, 19500],
  "decoded_command": "EXECUTE: system status",
  "decoding_successful": true
}
```

### Async Processing

FastAPI endpoints use async processing for file operations:

```python
@app.post("/embed/audio")
async def embed_audio_command(file: UploadFile, command: str):
    # Perform embedding in thread to avoid blocking
    result = await asyncio.to_thread(
        audio_embedder.embed_file,
        input_path, output_path, command
    )
    return FileResponse(output_path)
```

## Data Flow and Component Interactions

### Embedding Workflow

1. **Input Processing**: Client uploads media file and command
2. **Media Loading**: File loaded using pydub/moviepy
3. **Encryption**: Command encrypted with AES-256-GCM
4. **Obfuscation**: Optional padding added to encrypted payload
5. **Ultrasonic Encoding**: Binary data converted to FSK signals
6. **Audio Merging**: Ultrasonic signal overlaid on original audio
7. **Export**: Final media exported with appropriate codec settings

### Decoding Workflow

1. **Media Loading**: Input file loaded and audio extracted
2. **Preprocessing**: Audio converted to appropriate sample rate/format
3. **Signal Detection**: Band-pass filtering and presence detection
4. **Synchronization**: Preamble detection using sliding window correlation
5. **Bit Extraction**: FSK demodulation using time-domain correlation
6. **Error Correction**: Parity bit verification and correction
7. **Deobfuscation**: Optional padding removal
8. **Decryption**: AES-256-GCM decryption and verification

### Real-time Processing

For live audio monitoring:

1. **Stream Setup**: Initialize sounddevice input stream
2. **Buffer Management**: Maintain rolling audio buffer
3. **Continuous Analysis**: Periodic signal detection on buffer
4. **Command Detection**: Full decoding pipeline on detected signals
5. **Callback Execution**: User-defined callback for decoded commands

## Performance Characteristics

### Encoding Performance

- **Processing Speed**: ~1-2 seconds for 60-second audio file
- **Memory Usage**: Linear with audio duration (~50MB for 5-minute file)
- **CPU Utilization**: Single-threaded, CPU-bound during signal generation

### Decoding Performance

- **Detection Speed**: ~0.5-1 second for signal presence detection
- **Decoding Speed**: ~2-3 seconds for full command extraction
- **Memory Efficiency**: Streaming processing for large files
- **Accuracy**: >95% success rate under normal conditions

### Bandwidth Efficiency

```
Command Size → Transmission Time (10ms per bit + overhead)
10 bytes    → ~1.0 seconds
50 bytes    → ~4.5 seconds
100 bytes   → ~9.0 seconds
```

### Signal Quality Metrics

- **SNR Requirements**: Minimum 20dB for reliable detection
- **Frequency Stability**: ±50Hz tolerance for carrier frequencies
- **Amplitude Range**: 1-50% of full scale recommended

## Scalability Considerations

### Horizontal Scaling

The FastAPI server can be scaled horizontally:

```yaml
# Docker Compose scaling
services:
  stego-api:
    image: ultrasonic-agentics:latest
    deploy:
      replicas: 3
    ports:
      - "8000-8002:8000"
```

### Load Distribution

- **Stateless Design**: Each request is independent
- **File Isolation**: Temporary files prevent conflicts
- **Async Processing**: Non-blocking I/O for file operations

### Performance Optimization

1. **Caching**: Pre-computed reference signals for common frequencies
2. **Memory Management**: Streaming processing for large files
3. **GPU Acceleration**: Potential CUDA support for FFT operations
4. **Batch Processing**: Multiple files processed simultaneously

### Resource Management

```python
# Resource limits configuration
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_CONCURRENT_REQUESTS = 10
TIMEOUT_SECONDS = 300
TEMP_FILE_CLEANUP_INTERVAL = 3600  # 1 hour
```

## Technology Stack

### Core Dependencies

```
Python 3.8+
├── Signal Processing
│   ├── numpy>=1.21.0           # Numerical computing
│   ├── scipy>=1.7.0            # Signal processing algorithms
│   └── pydub>=0.25.1           # Audio manipulation
├── Cryptography
│   └── pycryptodome>=3.15.0    # AES-GCM implementation
├── Web Framework
│   ├── fastapi>=0.68.0         # Async web framework
│   ├── uvicorn>=0.15.0         # ASGI server
│   └── python-multipart>=0.0.5 # File upload support
├── Media Processing
│   ├── moviepy>=1.0.3          # Video processing
│   └── ffmpeg-python>=0.2.0    # FFmpeg integration
├── Optional
│   └── sounddevice>=0.4.4      # Real-time audio I/O
└── Testing
    ├── pytest>=6.2.4           # Test framework
    ├── pytest-mock>=3.6.1      # Mocking support
    └── pytest-asyncio>=0.15.1  # Async test support
```

### System Requirements

**Minimum**:
- Python 3.8+
- 2GB RAM
- 1GB storage
- Audio device with 48kHz capability

**Recommended**:
- Python 3.9+
- 8GB RAM
- 10GB storage
- High-quality audio interface
- FFmpeg installed system-wide

### Platform Support

- **Linux**: Full support with all features
- **macOS**: Full support with all features
- **Windows**: Core functionality (real-time audio may require configuration)

## Design Decisions and Trade-offs

### Frequency Range Selection

**Decision**: Use 18-20 kHz range
**Trade-offs**:
- ✅ Inaudible to most humans
- ✅ Supported by standard audio equipment
- ❌ May be affected by audio compression
- ❌ Limited by Nyquist frequency

### FSK vs. Other Modulation Schemes

**Decision**: Use binary FSK
**Trade-offs**:
- ✅ Simple implementation
- ✅ Robust to noise
- ✅ Easy frequency detection
- ❌ Lower data rate than QAM/PSK
- ❌ Requires two distinct frequencies

### AES-GCM vs. Other Crypto

**Decision**: Use AES-256-GCM
**Trade-offs**:
- ✅ Authenticated encryption
- ✅ Industry standard
- ✅ Hardware acceleration available
- ❌ Larger ciphertext size
- ❌ IV management complexity

### Time-Domain vs. Frequency-Domain Decoding

**Decision**: Use time-domain correlation
**Trade-offs**:
- ✅ Better performance for short signals
- ✅ Lower computational complexity
- ✅ More robust to windowing artifacts
- ❌ Less frequency resolution
- ❌ May miss weak signals

### Synchronous vs. Asynchronous API

**Decision**: Use FastAPI with async endpoints
**Trade-offs**:
- ✅ Better resource utilization
- ✅ Handles concurrent requests efficiently
- ✅ Non-blocking file I/O
- ❌ More complex error handling
- ❌ Requires async-aware code

## Extension Points

### 1. Modulation Schemes

The system can be extended to support additional modulation schemes:

```python
class ModulationScheme(ABC):
    @abstractmethod
    def encode(self, data: bytes) -> np.ndarray:
        pass
    
    @abstractmethod
    def decode(self, signal: np.ndarray) -> Optional[bytes]:
        pass

# Implement new schemes
class QAMModulation(ModulationScheme):
    def encode(self, data: bytes) -> np.ndarray:
        # QAM implementation
        pass
```

### 2. Encryption Algorithms

Support for additional encryption algorithms:

```python
class EncryptionProvider(ABC):
    @abstractmethod
    def encrypt(self, plaintext: str) -> bytes:
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> Optional[str]:
        pass

class ChaCha20Provider(EncryptionProvider):
    # ChaCha20-Poly1305 implementation
    pass
```

### 3. Transport Protocols

Extension to different media types:

```python
class TransportMedium(ABC):
    @abstractmethod
    def embed(self, medium: Any, signal: np.ndarray) -> Any:
        pass
    
    @abstractmethod
    def extract(self, medium: Any) -> np.ndarray:
        pass

class ImageTransport(TransportMedium):
    # LSB steganography in images
    pass

class NetworkTransport(TransportMedium):
    # Covert channels in network traffic
    pass
```

### 4. Command Processing

Pluggable command processors:

```python
class CommandProcessor(ABC):
    @abstractmethod
    def process(self, command: str) -> Any:
        pass

class ShellCommandProcessor(CommandProcessor):
    def process(self, command: str) -> str:
        return subprocess.run(command, shell=True, capture_output=True)

class AgentCommandProcessor(CommandProcessor):
    def process(self, command: str) -> Dict:
        # Execute agentic commands
        pass
```

### 5. Signal Analysis

Advanced signal analysis capabilities:

```python
class SignalAnalyzer(ABC):
    @abstractmethod
    def analyze(self, signal: np.ndarray) -> Dict:
        pass

class SpectralAnalyzer(SignalAnalyzer):
    def analyze(self, signal: np.ndarray) -> Dict:
        # Spectral analysis, peak detection, etc.
        pass

class StatisticalAnalyzer(SignalAnalyzer):
    def analyze(self, signal: np.ndarray) -> Dict:
        # Statistical analysis for detection
        pass
```

## Mathematical Foundations

### Frequency Shift Keying (FSK)

The FSK modulation scheme represents binary data using two carrier frequencies:

```
s₀(t) = A cos(2πf₀t + φ₀)  for bit '0'
s₁(t) = A cos(2πf₁t + φ₁)  for bit '1'

Where:
- A = amplitude
- f₀, f₁ = carrier frequencies 
- φ₀, φ₁ = phase offsets (typically 0)
- t = time
```

### Correlation Detection

The decoder uses cross-correlation for bit detection:

```
R(τ) = ∫ s(t) × r(t - τ) dt

Where:
- s(t) = received signal
- r(t) = reference signal
- τ = time delay
- R(τ) = correlation coefficient
```

### Band-pass Filter Design

Butterworth filter transfer function:

```
H(ω) = 1 / (1 + (ω/ωc)^(2n))

Where:
- ω = angular frequency
- ωc = cutoff frequency
- n = filter order
```

### Signal-to-Noise Ratio (SNR)

SNR calculation for signal quality assessment:

```
SNR = 10 × log₁₀(Psignal / Pnoise)

Where:
- Psignal = signal power
- Pnoise = noise power
- Result in decibels (dB)
```

### Bit Error Rate (BER)

Theoretical BER for FSK in AWGN:

```
BER ≈ (1/2) × erfc(√(Eb/N₀))

Where:
- Eb = energy per bit
- N₀ = noise power spectral density
- erfc = complementary error function
```

### Nyquist Sampling Criterion

For proper signal reconstruction:

```
fs ≥ 2 × fmax

Where:
- fs = sampling frequency
- fmax = maximum signal frequency
```

### Windowing Functions

Applied windowing function for spectral artifact reduction:

```
w(n) = 0.9 + 0.1 × cos(2πn/N)  for fade regions

Where:
- n = sample index
- N = window length
```

---

This architecture documentation provides a comprehensive technical overview of the Ultrasonic Agentics system, covering all major components, design decisions, and implementation details. The system represents a sophisticated approach to covert communication using steganographic techniques combined with modern cryptography and signal processing.