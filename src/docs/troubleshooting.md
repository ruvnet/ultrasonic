# Ultrasonic Agentics - Troubleshooting Guide

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Audio Encoding/Decoding Problems](#audio-encodingdecoding-problems)
3. [Frequency Detection Issues](#frequency-detection-issues)
4. [Performance and Optimization](#performance-and-optimization)
5. [API Server Issues](#api-server-issues)
6. [Platform-Specific Problems](#platform-specific-problems)
7. [Dependency Conflicts](#dependency-conflicts)
8. [Error Messages Explained](#error-messages-explained)
9. [Debug Mode and Logging](#debug-mode-and-logging)
10. [Memory and CPU Optimization](#memory-and-cpu-optimization)
11. [Audio Format Compatibility](#audio-format-compatibility)
12. [Network and Firewall Configuration](#network-and-firewall-configuration)
13. [Version Compatibility Matrix](#version-compatibility-matrix)
14. [Community Support Resources](#community-support-resources)

---

## Installation Issues

### Problem: FFmpeg Not Found
**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**Solution:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg

# macOS
brew install ffmpeg

# Windows (using chocolatey)
choco install ffmpeg

# Verify installation
ffmpeg -version
```

**Diagnostic Commands:**
```bash
which ffmpeg
ffmpeg -codecs | grep aac
ffmpeg -formats | grep mp3
```

### Problem: Python Dependencies Fail to Install
**Symptoms:**
```
ERROR: Failed building wheel for numpy
ERROR: Could not build wheels for scipy
```

**Solution:**
```bash
# Install system dependencies first
sudo apt install python3-dev build-essential libffi-dev

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install dependencies in order
pip install numpy>=1.21.0
pip install scipy>=1.7.0
pip install -r requirements.txt
```

### Problem: SoundDevice Backend Issues
**Symptoms:**
```
PortAudioError: Error querying device
```

**Solution:**
```bash
# Linux - install ALSA/PulseAudio development headers
sudo apt install libasound2-dev portaudio19-dev

# macOS - install PortAudio
brew install portaudio

# Test audio backend
python -c "import sounddevice; print(sounddevice.query_devices())"
```

---

## Audio Encoding/Decoding Problems

### Problem: Embedded Command Not Detected
**Symptoms:**
- `decoded_command` returns `None`
- Signal detection fails despite successful embedding

**Diagnostic Steps:**
```python
# Check signal strength
from agentic_commands_stego.decode.audio_decoder import AudioDecoder
decoder = AudioDecoder()
strength = decoder.get_signal_strength(audio_segment)
print(f"Signal strength: {strength}")

# Analyze audio for debugging
analysis = decoder.analyze_audio(audio_segment)
print(f"Analysis: {analysis}")
```

**Common Solutions:**
1. **Lower detection threshold:**
   ```python
   decoder = AudioDecoder(detection_threshold=0.001)  # Default: 0.01
   ```

2. **Increase embedding amplitude:**
   ```python
   embedder = AudioEmbedder(amplitude=0.8)  # Default: 0.1
   ```

3. **Extend bit duration:**
   ```python
   embedder = AudioEmbedder(bit_duration=0.05)  # Default: 0.01
   decoder = AudioDecoder(bit_duration=0.05)
   ```

### Problem: Preamble Detection Failures
**Symptoms:**
- `_detect_preamble()` returns None
- Signal present but synchronization fails

**Solution:**
```python
# Debug preamble detection
from agentic_commands_stego.decode.ultrasonic_decoder import UltrasonicDecoder
decoder = UltrasonicDecoder()

# Enable verbose preamble detection
def debug_correlate_with_pattern(self, segment, freq_sequence):
    correlation = self._correlate_with_pattern(segment, freq_sequence)
    print(f"Correlation: {correlation}, Threshold: {self.detection_threshold}")
    return correlation
```

**Configuration Fixes:**
```python
# Use more robust preamble pattern
embedder = AudioEmbedder()
embedder._generate_preamble = lambda: "10101010" * 3  # Longer pattern

# Adjust correlation threshold
decoder = UltrasonicDecoder(detection_threshold=0.005)
```

### Problem: Unicode Command Corruption
**Symptoms:**
- Non-ASCII characters fail to decode
- Encoded commands return garbled text

**Solution:**
```python
# Ensure proper UTF-8 encoding
command = "CMD αβγ 日本"
command_bytes = command.encode('utf-8')

# Verify encoding/decoding chain
from agentic_commands_stego.crypto.cipher import CipherService
cipher = CipherService()
encrypted = cipher.encrypt(command_bytes)
decrypted = cipher.decrypt(encrypted)
decoded_command = decrypted.decode('utf-8')
assert decoded_command == command
```

---

## Frequency Detection Issues

### Problem: Wrong Frequencies Detected
**Symptoms:**
- FSK demodulation produces incorrect bits
- High bit error rate

**Diagnostic Commands:**
```python
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Analyze frequency spectrum
def analyze_spectrum(audio_segment, sample_rate=48000):
    samples = np.array(audio_segment.get_array_of_samples())
    
    # Calculate FFT
    fft = np.fft.fft(samples)
    freqs = np.fft.fftfreq(len(samples), 1/sample_rate)
    
    # Find peaks in ultrasonic range
    ultrasonic_mask = (freqs >= 17000) & (freqs <= 22000)
    ultrasonic_fft = np.abs(fft[ultrasonic_mask])
    ultrasonic_freqs = freqs[ultrasonic_mask]
    
    peaks, _ = find_peaks(ultrasonic_fft, height=np.max(ultrasonic_fft) * 0.1)
    detected_freqs = ultrasonic_freqs[peaks]
    
    print(f"Detected frequencies: {detected_freqs}")
    return detected_freqs
```

**Solutions:**
1. **Calibrate frequency detection:**
   ```python
   # Use frequency calibration tool
   from agentic_commands_stego.tests.test_calibration import FrequencyCalibrator
   calibrator = FrequencyCalibrator()
   optimal_freqs = calibrator.find_optimal_frequencies()
   
   embedder.set_frequencies(optimal_freqs[0], optimal_freqs[1])
   decoder.set_frequencies(optimal_freqs[0], optimal_freqs[1])
   ```

2. **Increase frequency separation:**
   ```python
   # Use wider frequency gap
   embedder.set_frequencies(18000, 20000)  # 2kHz separation
   decoder.set_frequencies(18000, 20000)
   ```

### Problem: Nyquist Frequency Violations
**Symptoms:**
```
ValueError: Frequencies must be below Nyquist frequency (24000 Hz)
```

**Solution:**
```python
# Check sample rate compatibility
def validate_frequencies(freq_0, freq_1, sample_rate):
    nyquist = sample_rate / 2
    if freq_0 >= nyquist or freq_1 >= nyquist:
        print(f"Error: Frequencies {freq_0}, {freq_1} exceed Nyquist {nyquist}")
        return False
    return True

# Use appropriate sample rate
embedder = AudioEmbedder(sample_rate=48000)  # Supports up to 24kHz
decoder = AudioDecoder(sample_rate=48000)
```

---

## Performance and Optimization

### Problem: Slow Encoding/Decoding
**Symptoms:**
- Operations take more than 10 seconds
- High CPU usage during processing

**Optimization Strategies:**

1. **Reduce bit duration for faster processing:**
   ```python
   # Faster but less robust
   embedder = AudioEmbedder(bit_duration=0.005)  # 5ms per bit
   decoder = AudioDecoder(bit_duration=0.005)
   ```

2. **Use vectorized operations:**
   ```python
   # Enable numpy optimizations
   import os
   os.environ['OMP_NUM_THREADS'] = '4'  # Use 4 CPU cores
   ```

3. **Batch processing for multiple files:**
   ```python
   def batch_embed_files(file_paths, commands):
       results = []
       for path, cmd in zip(file_paths, commands):
           result = embedder.embed_file(path, f"{path}_embedded.mp3", cmd)
           results.append(result)
       return results
   ```

**Performance Monitoring:**
```python
import time
import psutil

def monitor_performance(func, *args, **kwargs):
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024
    
    result = func(*args, **kwargs)
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024
    
    print(f"Execution time: {end_time - start_time:.2f}s")
    print(f"Memory usage: {end_memory - start_memory:.2f}MB")
    
    return result
```

### Problem: Memory Usage Too High
**Symptoms:**
- Process killed due to OOM
- System becomes unresponsive

**Solutions:**
```python
# Process audio in chunks
def process_large_audio(audio_segment, chunk_size_seconds=30):
    chunk_size_samples = chunk_size_seconds * audio_segment.frame_rate
    results = []
    
    for i in range(0, len(audio_segment), chunk_size_samples):
        chunk = audio_segment[i:i + chunk_size_samples]
        result = decoder.decode_audio_segment(chunk)
        if result:
            results.append(result)
    
    return results

# Clear audio data after processing
def safe_decode(audio_path):
    audio = AudioSegment.from_file(audio_path)
    result = decoder.decode_audio_segment(audio)
    del audio  # Free memory immediately
    return result
```

---

## API Server Issues

### Problem: Server Won't Start
**Symptoms:**
```
OSError: [Errno 98] Address already in use
```

**Solutions:**
```bash
# Check what's using port 8000
lsof -i :8000
netstat -tulpn | grep :8000

# Kill existing process
sudo kill -9 $(lsof -t -i:8000)

# Start server on different port
uvicorn agentic_commands_stego.server.api:app --port 8001
```

### Problem: File Upload Fails
**Symptoms:**
```
413 Request Entity Too Large
422 Unprocessable Entity
```

**Server Configuration:**
```python
# api.py - Increase file size limits
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/embed/audio")
async def embed_audio_command(
    file: UploadFile = File(..., max_size=100_000_000)  # 100MB limit
):
    # Validate file size
    if file.size > 50_000_000:  # 50MB
        raise HTTPException(status_code=413, detail="File too large")
    
    # Validate file type
    allowed_types = ['audio/mpeg', 'audio/wav', 'audio/flac']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=422, detail="Unsupported audio format")
```

### Problem: CORS Issues
**Symptoms:**
- Cross-origin requests blocked
- Browser console shows CORS errors

**Solution:**
```python
# api.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Platform-Specific Problems

### Windows Issues

**Problem: FFmpeg path not found**
```bash
# Add FFmpeg to PATH
set PATH=%PATH%;C:\ffmpeg\bin

# Or specify full path in code
import os
os.environ['FFMPEG_BINARY'] = r'C:\ffmpeg\bin\ffmpeg.exe'
```

**Problem: Audio device access**
```python
# Use specific audio backend
import sounddevice as sd
sd.default.device = 'WASAPI'  # Windows Audio Session API
```

### macOS Issues

**Problem: Permission denied for audio access**
```bash
# Grant microphone permissions in System Preferences > Security & Privacy
# Or run with elevated permissions
sudo python your_script.py
```

**Problem: M1/M2 compatibility**
```bash
# Install native ARM64 packages
arch -arm64 pip install numpy scipy
# Or use Rosetta 2
arch -x86_64 pip install requirements.txt
```

### Linux Issues

**Problem: No audio output device**
```bash
# Install and configure PulseAudio
sudo apt install pulseaudio pulseaudio-utils
pulseaudio --start

# Test audio
aplay /usr/share/sounds/alsa/Front_Left.wav
```

---

## Dependency Conflicts

### Problem: NumPy Version Conflicts
**Symptoms:**
```
ImportError: numpy.core.multiarray failed to import
AttributeError: module 'numpy' has no attribute 'bool'
```

**Resolution:**
```bash
# Uninstall conflicting versions
pip uninstall numpy -y
pip uninstall scipy -y

# Reinstall compatible versions
pip install "numpy>=1.21.0,<1.25.0"
pip install "scipy>=1.7.0,<1.12.0"
```

### Problem: Pydub/FFmpeg Integration
**Symptoms:**
```
CouldntDecodeError: Decoding failed. ffmpeg returned error code 1
```

**Solution:**
```python
# Configure pydub to use system FFmpeg
from pydub import AudioSegment
from pydub.utils import which

# Check FFmpeg availability
ffmpeg_path = which("ffmpeg")
if not ffmpeg_path:
    raise RuntimeError("FFmpeg not found in PATH")

AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = which("ffprobe")
```

---

## Error Messages Explained

### `decoded_command = None`
**Meaning:** Signal was not detected or demodulation failed
**Causes:**
- Signal amplitude too low
- Detection threshold too high  
- Frequency mismatch between encoder/decoder
- Audio corruption during transmission

**Debug Steps:**
```python
# Step-by-step debugging
audio_segment = AudioSegment.from_file("test.mp3")

# 1. Check signal presence
has_signal = decoder.detect_signal(audio_segment)
print(f"Signal detected: {has_signal}")

# 2. Check signal strength
strength = decoder.get_signal_strength(audio_segment)
print(f"Signal strength: {strength}")

# 3. Get detailed analysis
analysis = decoder.analyze_audio(audio_segment)
print(f"Full analysis: {analysis}")
```

### `ValueError: Frequencies must be below Nyquist frequency`
**Meaning:** Ultrasonic frequencies exceed half the sample rate
**Solution:** Use higher sample rate or lower frequencies
```python
# Fix: Use 48kHz sample rate for 20kHz+ frequencies
embedder = AudioEmbedder(
    freq_0=18500, 
    freq_1=19500, 
    sample_rate=48000  # Nyquist = 24000
)
```

### `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`
**Meaning:** FFmpeg binary not found in system PATH
**Solution:** Install FFmpeg or specify path manually
```python
import os
os.environ['FFMPEG_BINARY'] = '/usr/local/bin/ffmpeg'
```

### `PortAudioError: Error querying device`
**Meaning:** Audio system not properly configured
**Solution:** Install audio system libraries
```bash
# Linux
sudo apt install libasound2-dev

# Test configuration
python -c "import sounddevice; print(sounddevice.query_devices())"
```

---

## Debug Mode and Logging

### Enabling Debug Logging
```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ultrasonic_debug.log'),
        logging.StreamHandler()
    ]
)

# Component-specific logging
logger = logging.getLogger('ultrasonic_encoder')
logger.setLevel(logging.DEBUG)
```

### Custom Debug Tools
```python
# Debug encoder output
def debug_encoder_output(encoder, payload):
    signal = encoder.encode_payload(payload)
    
    # Save raw signal for analysis
    np.save('debug_signal.npy', signal)
    
    # Plot frequency spectrum
    import matplotlib.pyplot as plt
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1/encoder.sample_rate)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(signal[:1000])  # Time domain
    plt.title('Time Domain Signal')
    
    plt.subplot(1, 2, 2)
    plt.plot(freqs[:len(freqs)//2], np.abs(fft[:len(fft)//2]))
    plt.title('Frequency Domain')
    plt.xlabel('Frequency (Hz)')
    plt.axvline(encoder.freq_0, color='red', label='Freq 0')
    plt.axvline(encoder.freq_1, color='blue', label='Freq 1')
    plt.legend()
    plt.savefig('debug_spectrum.png')
    plt.show()

# Debug decoder correlation
def debug_decoder_correlation(decoder, audio_signal):
    filtered = decoder._apply_bandpass_filter(audio_signal)
    
    # Visualize correlation over time
    correlations = []
    positions = range(0, len(filtered) - decoder.samples_per_bit, 
                     decoder.samples_per_bit // 4)
    
    for pos in positions:
        segment = filtered[pos:pos + decoder.samples_per_bit]
        corr_0 = decoder._calculate_frequency_power(segment, decoder.freq_0)
        corr_1 = decoder._calculate_frequency_power(segment, decoder.freq_1)
        correlations.append((corr_0, corr_1))
    
    import matplotlib.pyplot as plt
    corr_0_vals, corr_1_vals = zip(*correlations)
    plt.figure(figsize=(12, 4))
    plt.plot(corr_0_vals, label='Freq 0 Power')
    plt.plot(corr_1_vals, label='Freq 1 Power')
    plt.axhline(decoder.detection_threshold, color='red', 
                linestyle='--', label='Threshold')
    plt.legend()
    plt.title('Frequency Power Over Time')
    plt.xlabel('Time (bit periods)')
    plt.ylabel('Normalized Power')
    plt.savefig('debug_correlation.png')
    plt.show()
```

### Signal Analysis Tools
```python
# Complete signal analysis
def analyze_signal_quality(audio_segment, embedder, decoder):
    print("=== Signal Quality Analysis ===")
    
    # Basic properties
    print(f"Duration: {len(audio_segment)}ms")
    print(f"Sample rate: {audio_segment.frame_rate}Hz")
    print(f"Channels: {audio_segment.channels}")
    
    # Convert to numpy
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2)).mean(axis=1)
    
    # Signal statistics
    print(f"RMS level: {np.sqrt(np.mean(samples**2)):.6f}")
    print(f"Peak level: {np.max(np.abs(samples)):.6f}")
    print(f"Dynamic range: {20*np.log10(np.max(np.abs(samples))/np.sqrt(np.mean(samples**2))):.1f} dB")
    
    # Frequency analysis
    fft = np.fft.fft(samples)
    freqs = np.fft.fftfreq(len(samples), 1/audio_segment.frame_rate)
    
    # Ultrasonic band analysis
    ultrasonic_mask = (freqs >= 17000) & (freqs <= 22000)
    ultrasonic_power = np.sum(np.abs(fft[ultrasonic_mask])**2)
    total_power = np.sum(np.abs(fft)**2)
    
    print(f"Ultrasonic power ratio: {ultrasonic_power/total_power:.6f}")
    
    # Signal detection test
    has_signal = decoder.detect_signal(audio_segment)
    strength = decoder.get_signal_strength(audio_segment)
    print(f"Signal detected: {has_signal}")
    print(f"Signal strength: {strength:.6f}")
    
    return {
        'has_signal': has_signal,
        'strength': strength,
        'ultrasonic_ratio': ultrasonic_power/total_power
    }
```

---

## Memory and CPU Optimization

### Memory Management
```python
# Efficient audio processing
class OptimizedAudioProcessor:
    def __init__(self, chunk_size_mb=10):
        self.chunk_size_bytes = chunk_size_mb * 1024 * 1024
    
    def process_large_file(self, filepath):
        # Process in chunks to avoid memory issues
        audio = AudioSegment.from_file(filepath)
        chunk_duration_ms = (self.chunk_size_bytes // 
                           (audio.frame_rate * audio.sample_width)) * 1000
        
        results = []
        for start_ms in range(0, len(audio), chunk_duration_ms):
            chunk = audio[start_ms:start_ms + chunk_duration_ms]
            result = self.process_chunk(chunk)
            results.append(result)
            del chunk  # Free memory immediately
        
        del audio
        return results
    
    def process_chunk(self, chunk):
        # Process individual chunk
        return decoder.decode_audio_segment(chunk)

# Memory-mapped file processing for very large files
def process_with_mmap(filepath):
    import mmap
    
    with open(filepath, 'rb') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            # Process without loading entire file into memory
            # Implementation depends on specific audio format
            pass
```

### CPU Optimization
```python
# Parallel processing for multiple files
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

def parallel_decode(file_paths, max_workers=None):
    if max_workers is None:
        max_workers = mp.cpu_count()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(decoder.decode_file, path) 
                  for path in file_paths]
        results = [future.result() for future in futures]
    
    return results

# Optimize numpy operations
import os
os.environ['OPENBLAS_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'

# Use faster FFT implementations
try:
    import scipy.fftpack
    np.fft = scipy.fftpack  # May be faster for some operations
except ImportError:
    pass
```

---

## Audio Format Compatibility

### Supported Formats and Codecs
```python
# Check format support
def check_format_support():
    supported_formats = {
        'input': ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac'],
        'output': ['.mp3', '.wav', '.flac', '.ogg']
    }
    
    # Test FFmpeg codec availability
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-codecs'], 
                              capture_output=True, text=True)
        codecs = result.stdout
        
        codec_support = {
            'mp3': 'mp3' in codecs,
            'aac': 'aac' in codecs,
            'flac': 'flac' in codecs,
            'ogg': 'vorbis' in codecs
        }
        
        return supported_formats, codec_support
    except FileNotFoundError:
        return supported_formats, {}

# Format-specific handling
def load_audio_robust(filepath):
    """Load audio with fallback for problematic formats."""
    try:
        # Try direct loading
        return AudioSegment.from_file(filepath)
    except Exception as e:
        print(f"Direct load failed: {e}")
        
        # Try format-specific loading
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.mp3':
            return AudioSegment.from_mp3(filepath)
        elif ext == '.wav':
            return AudioSegment.from_wav(filepath)
        elif ext == '.flac':
            return AudioSegment.from_file(filepath, format='flac')
        elif ext == '.ogg':
            return AudioSegment.from_ogg(filepath)
        else:
            # Last resort: convert via FFmpeg
            temp_wav = filepath.replace(ext, '_temp.wav')
            subprocess.run(['ffmpeg', '-i', filepath, temp_wav])
            audio = AudioSegment.from_wav(temp_wav)
            os.unlink(temp_wav)
            return audio
```

### Sample Rate Compatibility
```python
# Handle different sample rates
def ensure_compatible_sample_rate(audio_segment, target_rate=48000):
    """Resample audio to compatible sample rate."""
    if audio_segment.frame_rate != target_rate:
        print(f"Resampling from {audio_segment.frame_rate}Hz to {target_rate}Hz")
        audio_segment = audio_segment.set_frame_rate(target_rate)
    
    return audio_segment

# Validate audio compatibility
def validate_audio_for_steganography(audio_segment):
    """Check if audio is suitable for ultrasonic steganography."""
    issues = []
    
    # Check sample rate
    if audio_segment.frame_rate < 44100:
        issues.append(f"Sample rate too low: {audio_segment.frame_rate}Hz (need ≥44100Hz)")
    
    # Check duration
    if len(audio_segment) < 1000:  # 1 second
        issues.append(f"Audio too short: {len(audio_segment)}ms (need ≥1000ms)")
    
    # Check if stereo
    if audio_segment.channels > 1:
        issues.append("Stereo audio detected (will be converted to mono)")
    
    # Check bit depth
    if audio_segment.sample_width < 2:
        issues.append(f"Low bit depth: {audio_segment.sample_width*8}bit (prefer 16bit+)")
    
    return {
        'compatible': len(issues) == 0,
        'issues': issues,
        'recommendations': [
            "Use 48kHz sample rate for best results",
            "Ensure audio is at least 5 seconds long",
            "Use 16-bit or 24-bit audio",
            "Mono audio is preferred"
        ]
    }
```

---

## Network and Firewall Configuration

### API Server Configuration
```python
# Production server configuration
def create_production_app():
    app = FastAPI(
        title="Ultrasonic Steganography API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Security headers
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
    
    # Rate limiting
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    @app.post("/embed/audio")
    @limiter.limit("10/minute")  # Rate limit
    async def embed_audio(request: Request, ...):
        pass
    
    return app

# SSL/TLS configuration
def run_secure_server():
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="private_key.pem",
        ssl_certfile="certificate.pem",
        ssl_ca_certs="ca_cert.pem"
    )
```

### Firewall Rules
```bash
# Allow API server port
sudo ufw allow 8000/tcp
sudo ufw allow 8443/tcp  # HTTPS

# For development only - restrict to localhost
sudo ufw allow from 127.0.0.1 to any port 8000

# Check current rules
sudo ufw status verbose
```

### Client Configuration
```python
# HTTP client with proper error handling
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_robust_client(base_url="http://localhost:8000"):
    session = requests.Session()
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# Example usage
client = create_robust_client()

def upload_for_embedding(audio_file_path, command):
    try:
        with open(audio_file_path, 'rb') as f:
            files = {'file': f}
            data = {'command': command}
            
            response = client.post(
                "http://localhost:8000/embed/audio",
                files=files,
                data=data,
                timeout=60
            )
            
            response.raise_for_status()
            return response.content
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

---

## Version Compatibility Matrix

| Component | Minimum Version | Recommended | Maximum Tested |
|-----------|----------------|-------------|----------------|
| Python | 3.7 | 3.9+ | 3.11 |
| NumPy | 1.21.0 | 1.23.0 | 1.24.4 |
| SciPy | 1.7.0 | 1.9.0 | 1.11.4 |
| Pydub | 0.25.1 | 0.25.1 | 0.25.1 |
| FFmpeg | 4.0 | 5.0+ | 6.0 |
| FastAPI | 0.68.0 | 0.100+ | 0.104.1 |
| MoviePy | 1.0.3 | 1.0.3 | 1.0.3 |

### Known Compatibility Issues

**Python 3.12+:**
- NumPy compatibility issues with some versions
- Use NumPy 1.24+ for Python 3.12

**NumPy 1.25+:**
- Breaking changes in numpy.bool
- Pin to `numpy<1.25` if encountering issues

**FFmpeg 6.0+:**
- New default settings may affect output quality
- Use explicit codec parameters for consistency

### Version Checking Script
```python
def check_version_compatibility():
    """Check if all dependencies meet version requirements."""
    import sys
    import pkg_resources
    
    requirements = {
        'python': ('3.7', sys.version_info[:2]),
        'numpy': ('1.21.0', '1.24.4'),
        'scipy': ('1.7.0', '1.11.4'),
        'pydub': ('0.25.1', '0.25.1'),
        'fastapi': ('0.68.0', '0.104.1')
    }
    
    results = {}
    
    for package, (min_ver, max_ver) in requirements.items():
        if package == 'python':
            current = f"{sys.version_info.major}.{sys.version_info.minor}"
            results[package] = {
                'current': current,
                'compatible': current >= min_ver
            }
        else:
            try:
                current = pkg_resources.get_distribution(package).version
                results[package] = {
                    'current': current,
                    'compatible': min_ver <= current <= max_ver
                }
            except pkg_resources.DistributionNotFound:
                results[package] = {
                    'current': 'NOT INSTALLED',
                    'compatible': False
                }
    
    # Check FFmpeg
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            ffmpeg_version = version_line.split(' ')[2]
            results['ffmpeg'] = {
                'current': ffmpeg_version,
                'compatible': True  # Assume compatible if runs
            }
        else:
            results['ffmpeg'] = {'current': 'ERROR', 'compatible': False}
    except FileNotFoundError:
        results['ffmpeg'] = {'current': 'NOT INSTALLED', 'compatible': False}
    
    return results

# Run compatibility check
compatibility = check_version_compatibility()
for package, info in compatibility.items():
    status = "✓" if info['compatible'] else "✗"
    print(f"{status} {package}: {info['current']}")
```

---

## Community Support Resources

### Documentation and Guides
- **Main Documentation**: `/docs/user-guide.md`
- **API Reference**: `/docs/api-reference.md`
- **Advanced Usage**: `/docs/advanced-usage.md`
- **Examples**: `/examples/README.md`

### Issue Reporting
When reporting issues, please include:

1. **System Information:**
   ```bash
   python --version
   pip list | grep -E "(numpy|scipy|pydub|fastapi)"
   ffmpeg -version
   uname -a  # Linux/macOS
   ```

2. **Audio File Information:**
   ```python
   from pydub import AudioSegment
   audio = AudioSegment.from_file("problem_file.mp3")
   print(f"Duration: {len(audio)}ms")
   print(f"Sample rate: {audio.frame_rate}Hz")
   print(f"Channels: {audio.channels}")
   print(f"Sample width: {audio.sample_width} bytes")
   ```

3. **Minimal Reproduction Case:**
   ```python
   # Provide minimal code that reproduces the issue
   from agentic_commands_stego import AudioEmbedder, AudioDecoder
   
   embedder = AudioEmbedder()
   decoder = AudioDecoder()
   
   # Steps to reproduce...
   ```

4. **Error Logs:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   # Include full stack trace
   ```

### Testing Your Setup

**Quick System Test:**
```python
def run_system_test():
    """Run comprehensive system test."""
    print("=== Ultrasonic Steganography System Test ===")
    
    # 1. Check dependencies
    print("\n1. Checking dependencies...")
    compatibility = check_version_compatibility()
    all_compatible = all(info['compatible'] for info in compatibility.values())
    print(f"Dependencies: {'✓ PASS' if all_compatible else '✗ FAIL'}")
    
    # 2. Test basic encoding/decoding
    print("\n2. Testing basic functionality...")
    try:
        from agentic_commands_stego import AudioEmbedder, AudioDecoder
        from pydub import AudioSegment
        
        # Create test audio
        test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        
        # Test embedding
        embedder = AudioEmbedder(amplitude=0.8, bit_duration=0.05)
        stego_audio = embedder.embed(test_audio, "TEST_COMMAND")
        
        # Test decoding
        decoder = AudioDecoder(detection_threshold=0.001, bit_duration=0.05)
        result = decoder.decode_audio_segment(stego_audio)
        
        if result == "TEST_COMMAND":
            print("Basic functionality: ✓ PASS")
        else:
            print(f"Basic functionality: ✗ FAIL (got: {result})")
            
    except Exception as e:
        print(f"Basic functionality: ✗ FAIL ({e})")
    
    # 3. Test file operations
    print("\n3. Testing file operations...")
    try:
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            test_audio.export(tmp.name, format='wav')
            
            # Test file embedding
            output_path = tmp.name.replace('.wav', '_embedded.mp3')
            embedder.embed_file(tmp.name, output_path, "FILE_TEST")
            
            # Test file decoding
            result = decoder.decode_file(output_path)
            
            if result == "FILE_TEST":
                print("File operations: ✓ PASS")
            else:
                print(f"File operations: ✗ FAIL (got: {result})")
            
            # Cleanup
            os.unlink(tmp.name)
            os.unlink(output_path)
            
    except Exception as e:
        print(f"File operations: ✗ FAIL ({e})")
    
    # 4. Test API server (if running)
    print("\n4. Testing API server...")
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("API server: ✓ PASS")
        else:
            print(f"API server: ✗ FAIL (status: {response.status_code})")
    except Exception:
        print("API server: - SKIP (not running)")
    
    print("\n=== Test Complete ===")

# Run the test
if __name__ == "__main__":
    run_system_test()
```

### Performance Benchmarks

**Benchmark Script:**
```python
def run_performance_benchmark():
    """Run performance benchmark."""
    import time
    from agentic_commands_stego import AudioEmbedder, AudioDecoder
    from pydub import AudioSegment
    
    print("=== Performance Benchmark ===")
    
    # Test parameters
    durations = [5000, 10000, 30000]  # 5s, 10s, 30s
    commands = ["SHORT", "MEDIUM_LENGTH_COMMAND", "VERY_LONG_COMMAND_" + "X" * 50]
    
    embedder = AudioEmbedder(amplitude=0.8, bit_duration=0.05)
    decoder = AudioDecoder(detection_threshold=0.001, bit_duration=0.05)
    
    results = []
    
    for duration in durations:
        for command in commands:
            test_audio = AudioSegment.silent(duration=duration, frame_rate=48000)
            
            # Measure embedding time
            start_time = time.time()
            stego_audio = embedder.embed(test_audio, command)
            embed_time = time.time() - start_time
            
            # Measure decoding time
            start_time = time.time()
            result = decoder.decode_audio_segment(stego_audio)
            decode_time = time.time() - start_time
            
            success = result == command
            
            results.append({
                'duration_ms': duration,
                'command_length': len(command),
                'embed_time': embed_time,
                'decode_time': decode_time,
                'total_time': embed_time + decode_time,
                'success': success
            })
            
            print(f"Audio: {duration}ms, Command: {len(command)} chars, "
                  f"Embed: {embed_time:.2f}s, Decode: {decode_time:.2f}s, "
                  f"Success: {success}")
    
    # Summary statistics
    successful_results = [r for r in results if r['success']]
    if successful_results:
        avg_embed = sum(r['embed_time'] for r in successful_results) / len(successful_results)
        avg_decode = sum(r['decode_time'] for r in successful_results) / len(successful_results)
        
        print(f"\nAverage times (successful operations):")
        print(f"Embedding: {avg_embed:.2f}s")
        print(f"Decoding: {avg_decode:.2f}s")
        print(f"Success rate: {len(successful_results)}/{len(results)} ({100*len(successful_results)/len(results):.1f}%)")
    
    return results

# Run benchmark
if __name__ == "__main__":
    benchmark_results = run_performance_benchmark()
```

This comprehensive troubleshooting guide covers the most common issues and their solutions for the Ultrasonic Agentics project. Use the diagnostic commands and debug tools to identify specific problems, and refer to the appropriate sections for detailed resolution steps.