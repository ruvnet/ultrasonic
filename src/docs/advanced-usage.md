# Advanced Usage Guide

This guide covers advanced features and techniques for the Ultrasonic Agentics framework, including performance optimization, custom configurations, and integration patterns.

## Table of Contents

1. [Advanced Encoding Techniques](#advanced-encoding-techniques)
2. [Performance Optimization](#performance-optimization)
3. [Custom Frequency Schemes](#custom-frequency-schemes)
4. [Error Correction and Redundancy](#error-correction-and-redundancy)
5. [Real-time Processing](#real-time-processing)
6. [Integration Patterns](#integration-patterns)
7. [Security Hardening](#security-hardening)
8. [Troubleshooting and Debugging](#troubleshooting-and-debugging)

## Advanced Encoding Techniques

### Multi-frequency Encoding

Use multiple frequency pairs for increased reliability and data rate:

```python
from ultrasonic_agentics.embed import UltrasonicEncoder
import numpy as np

class MultiFrequencyEncoder:
    def __init__(self):
        self.encoders = [
            UltrasonicEncoder(freq_0=18000, freq_1=18500),
            UltrasonicEncoder(freq_0=19000, freq_1=19500),
            UltrasonicEncoder(freq_0=20000, freq_1=20500)
        ]
    
    def encode_parallel(self, data: bytes) -> np.ndarray:
        """Encode data across multiple frequency bands simultaneously."""
        # Split data across encoders
        chunk_size = len(data) // len(self.encoders)
        signals = []
        
        for i, encoder in enumerate(self.encoders):
            start = i * chunk_size
            end = start + chunk_size if i < len(self.encoders) - 1 else len(data)
            chunk = data[start:end]
            
            signal = encoder.encode_payload(chunk)
            signals.append(signal)
        
        # Combine signals by addition
        max_length = max(len(s) for s in signals)
        combined = np.zeros(max_length)
        
        for signal in signals:
            combined[:len(signal)] += signal
        
        return combined / len(signals)  # Normalize amplitude
```

### Adaptive Amplitude Control

Dynamically adjust amplitude based on background noise:

```python
class AdaptiveEncoder(UltrasonicEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.noise_floor = 0.01
        self.target_snr = 20.0  # dB
    
    def analyze_noise_floor(self, audio_sample: np.ndarray) -> float:
        """Analyze background noise in ultrasonic range."""
        # Apply bandpass filter to isolate target frequencies
        filtered = self._apply_bandpass_filter(audio_sample)
        
        # Calculate RMS of background noise
        noise_rms = np.sqrt(np.mean(filtered ** 2))
        return max(noise_rms, 0.001)  # Minimum noise floor
    
    def set_adaptive_amplitude(self, background_audio: np.ndarray):
        """Set amplitude based on background noise analysis."""
        self.noise_floor = self.analyze_noise_floor(background_audio)
        
        # Calculate required amplitude for target SNR
        target_linear = 10 ** (self.target_snr / 20)
        required_amplitude = self.noise_floor * target_linear
        
        # Clamp to valid range
        self.amplitude = min(required_amplitude, 0.9)
```

### Steganographic Timing

Hide data in natural pauses or specific time windows:

```python
class TimingStegEncoder:
    def __init__(self):
        self.encoder = UltrasonicEncoder()
        self.silence_threshold = 0.01
        self.min_gap_duration = 0.5  # seconds
    
    def embed_in_gaps(self, audio_file: str, command: str) -> np.ndarray:
        """Embed data only in silent gaps of existing audio."""
        # Load and analyze audio
        audio = self._load_audio(audio_file)
        gaps = self._find_silent_gaps(audio)
        
        # Encode command
        encoded_data = self.encoder.encode_payload(command.encode())
        
        # Insert encoded data into gaps
        modified_audio = audio.copy()
        data_pos = 0
        
        for gap_start, gap_end in gaps:
            gap_duration = gap_end - gap_start
            samples_available = int(gap_duration * self.encoder.sample_rate)
            
            if data_pos < len(encoded_data) and samples_available > 0:
                # Insert portion of encoded data
                insert_length = min(len(encoded_data) - data_pos, samples_available)
                
                modified_audio[gap_start:gap_start + insert_length] += \
                    encoded_data[data_pos:data_pos + insert_length]
                
                data_pos += insert_length
        
        return modified_audio
    
    def _find_silent_gaps(self, audio: np.ndarray) -> list:
        """Find silent gaps in audio suitable for data insertion."""
        # Calculate energy in sliding windows
        window_size = int(0.1 * self.encoder.sample_rate)  # 100ms windows
        energy = []
        
        for i in range(0, len(audio) - window_size, window_size // 2):
            window = audio[i:i + window_size]
            energy.append(np.mean(window ** 2))
        
        # Find gaps below silence threshold
        gaps = []
        in_gap = False
        gap_start = 0
        
        for i, e in enumerate(energy):
            pos = i * window_size // 2
            
            if e < self.silence_threshold and not in_gap:
                gap_start = pos
                in_gap = True
            elif e >= self.silence_threshold and in_gap:
                gap_duration = (pos - gap_start) / self.encoder.sample_rate
                if gap_duration >= self.min_gap_duration:
                    gaps.append((gap_start, pos))
                in_gap = False
        
        return gaps
```

## Performance Optimization

### Parallel Processing

Process multiple files or streams simultaneously:

```python
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio

class ParallelProcessor:
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or mp.cpu_count()
        self.encoder = UltrasonicEncoder()
    
    async def process_files_async(self, file_list: list, commands: list):
        """Process multiple files asynchronously."""
        async def process_single(file_path, command):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, self._encode_file, file_path, command
            )
        
        tasks = [
            process_single(file_path, command)
            for file_path, command in zip(file_list, commands)
        ]
        
        return await asyncio.gather(*tasks)
    
    def process_files_parallel(self, file_list: list, commands: list):
        """Process multiple files using process pool."""
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [
                executor.submit(self._encode_file, file_path, command)
                for file_path, command in zip(file_list, commands)
            ]
            
            results = [future.result() for future in futures]
        
        return results
    
    def _encode_file(self, file_path: str, command: str) -> str:
        """Encode single file (worker function)."""
        output_path = file_path.replace('.wav', '_encoded.wav')
        
        # Load audio
        audio_data = self._load_audio(file_path)
        
        # Encode command
        encoded_signal = self.encoder.encode_payload(command.encode())
        
        # Mix with original audio
        combined = self._mix_audio(audio_data, encoded_signal)
        
        # Save result
        self._save_audio(combined, output_path)
        
        return output_path
```

### Memory-efficient Streaming

Process large files without loading entirely into memory:

```python
class StreamingProcessor:
    def __init__(self, chunk_size: int = 1024 * 1024):  # 1MB chunks
        self.chunk_size = chunk_size
        self.encoder = UltrasonicEncoder()
    
    def stream_encode(self, input_file: str, output_file: str, command: str):
        """Encode command into large audio file using streaming."""
        encoded_data = self.encoder.encode_payload(command.encode())
        
        with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
            # Copy header (assuming WAV format)
            header = infile.read(44)
            outfile.write(header)
            
            # Process audio data in chunks
            data_inserted = False
            bytes_processed = 0
            
            while True:
                chunk = infile.read(self.chunk_size)
                if not chunk:
                    break
                
                # Convert to numpy array
                audio_chunk = np.frombuffer(chunk, dtype=np.int16).astype(np.float32)
                
                # Insert encoded data in first suitable chunk
                if not data_inserted and len(audio_chunk) >= len(encoded_data):
                    # Convert encoded data to int16
                    encoded_int16 = (encoded_data * 32767).astype(np.int16)
                    
                    # Mix with original audio
                    audio_chunk[:len(encoded_int16)] += encoded_int16.astype(np.float32)
                    data_inserted = True
                
                # Convert back to bytes and write
                output_chunk = audio_chunk.astype(np.int16).tobytes()
                outfile.write(output_chunk)
                
                bytes_processed += len(chunk)
```

### Caching and Precomputation

Cache frequently used computations:

```python
from functools import lru_cache
import pickle
import hashlib

class OptimizedEncoder:
    def __init__(self):
        self.encoder = UltrasonicEncoder()
        self.filter_cache = {}
        self.pattern_cache = {}
    
    @lru_cache(maxsize=1000)
    def get_frequency_filter(self, freq: float, bandwidth: float):
        """Cache frequency filters for reuse."""
        from scipy import signal
        nyquist = self.encoder.sample_rate / 2
        low = (freq - bandwidth) / nyquist
        high = (freq + bandwidth) / nyquist
        return signal.butter(4, [low, high], btype='band')
    
    def encode_with_cache(self, command: str) -> np.ndarray:
        """Encode command with pattern caching."""
        # Create cache key
        params = (command, self.encoder.freq_0, self.encoder.freq_1, 
                 self.encoder.sample_rate, self.encoder.bit_duration)
        cache_key = hashlib.md5(str(params).encode()).hexdigest()
        
        # Check cache
        if cache_key in self.pattern_cache:
            return self.pattern_cache[cache_key]
        
        # Encode and cache result
        result = self.encoder.encode_payload(command.encode())
        self.pattern_cache[cache_key] = result
        
        return result
    
    def save_cache(self, filename: str):
        """Save cache to disk."""
        with open(filename, 'wb') as f:
            pickle.dump(self.pattern_cache, f)
    
    def load_cache(self, filename: str):
        """Load cache from disk."""
        try:
            with open(filename, 'rb') as f:
                self.pattern_cache = pickle.load(f)
        except FileNotFoundError:
            self.pattern_cache = {}
```

## Custom Frequency Schemes

### Spread Spectrum Encoding

Use multiple frequencies with pseudo-random hopping:

```python
import random

class SpreadSpectrumEncoder:
    def __init__(self, base_freq: float = 18000, bandwidth: float = 4000, 
                 hop_rate: float = 100):  # Hz
        self.base_freq = base_freq
        self.bandwidth = bandwidth
        self.hop_rate = hop_rate
        self.encoder = UltrasonicEncoder()
        
        # Generate frequency sequence
        self.frequencies = self._generate_frequency_sequence()
    
    def _generate_frequency_sequence(self, seed: int = 42) -> list:
        """Generate pseudo-random frequency sequence."""
        random.seed(seed)
        frequencies = []
        
        for _ in range(1000):  # Generate 1000 frequencies
            freq = self.base_freq + random.uniform(0, self.bandwidth)
            frequencies.append(freq)
        
        return frequencies
    
    def encode_spread_spectrum(self, data: bytes) -> np.ndarray:
        """Encode data using frequency hopping."""
        bit_string = ''.join(format(byte, '08b') for byte in data)
        
        total_samples = len(bit_string) * self.encoder.samples_per_bit
        signal = np.zeros(total_samples)
        
        t = np.linspace(0, self.encoder.bit_duration, 
                       self.encoder.samples_per_bit, endpoint=False)
        
        for i, bit in enumerate(bit_string):
            start_idx = i * self.encoder.samples_per_bit
            end_idx = start_idx + self.encoder.samples_per_bit
            
            # Select frequency from hopping sequence
            freq_idx = i % len(self.frequencies)
            base_freq = self.frequencies[freq_idx]
            
            # Use frequency offset for bit encoding
            if bit == '0':
                freq = base_freq
            else:
                freq = base_freq + 500  # 500 Hz offset
            
            # Generate tone
            tone = self.encoder.amplitude * np.sin(2 * np.pi * freq * t)
            signal[start_idx:end_idx] = tone
        
        return signal
```

### Chirp Signal Encoding

Use frequency sweeps for robust transmission:

```python
class ChirpEncoder:
    def __init__(self, start_freq: float = 18000, end_freq: float = 22000,
                 symbol_duration: float = 0.05):
        self.start_freq = start_freq
        self.end_freq = end_freq
        self.symbol_duration = symbol_duration
        self.sample_rate = 48000
        
    def encode_chirp(self, data: bytes) -> np.ndarray:
        """Encode data using chirp signals."""
        symbols = self._data_to_symbols(data)
        
        samples_per_symbol = int(self.symbol_duration * self.sample_rate)
        signal = np.zeros(len(symbols) * samples_per_symbol)
        
        for i, symbol in enumerate(symbols):
            start_idx = i * samples_per_symbol
            end_idx = start_idx + samples_per_symbol
            
            # Generate chirp based on symbol
            chirp = self._generate_chirp(symbol, samples_per_symbol)
            signal[start_idx:end_idx] = chirp
        
        return signal
    
    def _data_to_symbols(self, data: bytes) -> list:
        """Convert bytes to 4-bit symbols."""
        symbols = []
        for byte in data:
            # Split byte into two 4-bit symbols
            symbols.append((byte >> 4) & 0x0F)  # Upper 4 bits
            symbols.append(byte & 0x0F)         # Lower 4 bits
        return symbols
    
    def _generate_chirp(self, symbol: int, num_samples: int) -> np.ndarray:
        """Generate chirp signal for given symbol."""
        t = np.linspace(0, self.symbol_duration, num_samples, endpoint=False)
        
        # Map symbol to frequency range
        freq_range = self.end_freq - self.start_freq
        freq_offset = (symbol / 15.0) * freq_range  # 16 possible symbols (0-15)
        
        symbol_start_freq = self.start_freq + freq_offset
        symbol_end_freq = min(symbol_start_freq + freq_range / 16, self.end_freq)
        
        # Generate linear chirp
        instantaneous_freq = symbol_start_freq + \
                           (symbol_end_freq - symbol_start_freq) * t / self.symbol_duration
        
        phase = 2 * np.pi * np.cumsum(instantaneous_freq) / self.sample_rate
        chirp = 0.1 * np.sin(phase)
        
        return chirp
```

## Error Correction and Redundancy

### Reed-Solomon Error Correction

Implement robust error correction for noisy channels:

```python
try:
    from reedsolo import RSCodec
    HAS_REED_SOLOMON = True
except ImportError:
    HAS_REED_SOLOMON = False

class RobustEncoder:
    def __init__(self, ecc_symbols: int = 10):
        if not HAS_REED_SOLOMON:
            raise ImportError("reedsolo package required for Reed-Solomon encoding")
        
        self.encoder = UltrasonicEncoder()
        self.rs_codec = RSCodec(ecc_symbols)  # Can correct up to 5 errors
    
    def encode_with_ecc(self, data: bytes) -> np.ndarray:
        """Encode data with Reed-Solomon error correction."""
        # Add error correction
        protected_data = self.rs_codec.encode(data)
        
        # Encode with ultrasonic
        return self.encoder.encode_payload(protected_data)
    
    def decode_with_ecc(self, signal: np.ndarray) -> bytes:
        """Decode signal with error correction."""
        decoder = UltrasonicDecoder(
            freq_0=self.encoder.freq_0,
            freq_1=self.encoder.freq_1,
            sample_rate=self.encoder.sample_rate
        )
        
        # Decode ultrasonic signal
        raw_data = decoder.decode_payload(signal)
        if raw_data is None:
            return None
        
        try:
            # Apply error correction
            corrected_data = self.rs_codec.decode(raw_data)[0]
            return corrected_data
        except Exception:
            # Error correction failed
            return None
```

### Redundant Transmission

Send data multiple times with different parameters:

```python
class RedundantEncoder:
    def __init__(self):
        self.encoders = [
            UltrasonicEncoder(freq_0=18000, freq_1=18500, amplitude=0.1),
            UltrasonicEncoder(freq_0=19000, freq_1=19500, amplitude=0.08),
            UltrasonicEncoder(freq_0=20000, freq_1=20500, amplitude=0.12)
        ]
    
    def encode_redundant(self, data: bytes, repetitions: int = 3) -> np.ndarray:
        """Encode data with multiple redundant copies."""
        signals = []
        
        for rep in range(repetitions):
            for encoder in self.encoders:
                # Add timing offset for each repetition
                signal = encoder.encode_payload(data)
                
                # Add random delay between repetitions
                if rep > 0:
                    delay_samples = int(np.random.uniform(0.1, 0.5) * encoder.sample_rate)
                    delayed_signal = np.concatenate([np.zeros(delay_samples), signal])
                    signal = delayed_signal
                
                signals.append(signal)
        
        # Combine all signals
        max_length = max(len(s) for s in signals)
        combined = np.zeros(max_length)
        
        for signal in signals:
            combined[:len(signal)] += signal
        
        # Normalize to prevent clipping
        return combined / len(signals)
```

## Real-time Processing

### Streaming Audio Processing

Process audio streams in real-time:

```python
import threading
import queue
import sounddevice as sd

class RealTimeProcessor:
    def __init__(self, chunk_size: int = 1024):
        self.chunk_size = chunk_size
        self.sample_rate = 48000
        self.encoder = UltrasonicEncoder(sample_rate=self.sample_rate)
        self.decoder = UltrasonicDecoder(sample_rate=self.sample_rate)
        
        self.audio_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.running = False
    
    def start_monitoring(self):
        """Start real-time audio monitoring."""
        self.running = True
        
        # Start audio capture thread
        capture_thread = threading.Thread(target=self._capture_audio)
        capture_thread.start()
        
        # Start processing thread
        process_thread = threading.Thread(target=self._process_audio)
        process_thread.start()
    
    def stop_monitoring(self):
        """Stop real-time monitoring."""
        self.running = False
    
    def _capture_audio(self):
        """Capture audio from microphone."""
        def audio_callback(indata, frames, time, status):
            if self.running:
                self.audio_queue.put(indata.copy())
        
        with sd.InputStream(callback=audio_callback,
                           samplerate=self.sample_rate,
                           channels=1,
                           blocksize=self.chunk_size):
            while self.running:
                sd.sleep(100)
    
    def _process_audio(self):
        """Process captured audio for commands."""
        buffer = np.array([])
        
        while self.running:
            try:
                # Get audio chunk
                chunk = self.audio_queue.get(timeout=0.1)
                chunk = chunk.flatten()
                
                # Add to buffer
                buffer = np.concatenate([buffer, chunk])
                
                # Keep buffer manageable size
                max_buffer_samples = self.sample_rate * 10  # 10 seconds
                if len(buffer) > max_buffer_samples:
                    buffer = buffer[-max_buffer_samples:]
                
                # Try to decode commands
                command = self.decoder.decode_payload(buffer)
                if command:
                    self.command_queue.put(command.decode('utf-8', errors='ignore'))
                    # Clear buffer after successful decode
                    buffer = np.array([])
                    
            except queue.Empty:
                continue
    
    def get_commands(self) -> list:
        """Get any decoded commands."""
        commands = []
        while not self.command_queue.empty():
            try:
                commands.append(self.command_queue.get_nowait())
            except queue.Empty:
                break
        return commands
    
    def transmit_command(self, command: str):
        """Transmit command via speakers."""
        signal = self.encoder.encode_payload(command.encode())
        
        # Play through speakers
        sd.play(signal, samplerate=self.sample_rate)
        sd.wait()  # Wait until playback is finished
```

## Integration Patterns

### Webhook Integration

Integrate with external systems via webhooks:

```python
import requests
import json
from datetime import datetime

class WebhookIntegration:
    def __init__(self, webhook_url: str, secret_key: str = None):
        self.webhook_url = webhook_url
        self.secret_key = secret_key
        self.processor = RealTimeProcessor()
    
    def start_webhook_monitor(self):
        """Start monitoring and send commands via webhook."""
        self.processor.start_monitoring()
        
        monitor_thread = threading.Thread(target=self._webhook_loop)
        monitor_thread.start()
    
    def _webhook_loop(self):
        """Main webhook monitoring loop."""
        while self.processor.running:
            commands = self.processor.get_commands()
            
            for command in commands:
                self._send_webhook(command)
            
            time.sleep(0.1)  # Check every 100ms
    
    def _send_webhook(self, command: str):
        """Send command to webhook endpoint."""
        payload = {
            'timestamp': datetime.utcnow().isoformat(),
            'command': command,
            'source': 'ultrasonic_agentics'
        }
        
        headers = {'Content-Type': 'application/json'}
        
        # Add authentication if secret key provided
        if self.secret_key:
            import hmac
            import hashlib
            
            signature = hmac.new(
                self.secret_key.encode(),
                json.dumps(payload).encode(),
                hashlib.sha256
            ).hexdigest()
            headers['X-Signature'] = f'sha256={signature}'
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Webhook failed: {e}")
```

### Message Queue Integration

Integrate with message queues (RabbitMQ, Redis, etc.):

```python
import pika
import redis
import json

class MessageQueueIntegration:
    def __init__(self, queue_type: str = 'redis', **config):
        self.queue_type = queue_type
        self.config = config
        self.processor = RealTimeProcessor()
        
        if queue_type == 'redis':
            self.redis_client = redis.Redis(**config)
        elif queue_type == 'rabbitmq':
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(**config)
            )
            self.channel = self.connection.channel()
    
    def start_queue_monitor(self, queue_name: str = 'ultrasonic_commands'):
        """Start monitoring and publish to message queue."""
        self.queue_name = queue_name
        self.processor.start_monitoring()
        
        monitor_thread = threading.Thread(target=self._queue_loop)
        monitor_thread.start()
    
    def _queue_loop(self):
        """Main queue monitoring loop."""
        while self.processor.running:
            commands = self.processor.get_commands()
            
            for command in commands:
                self._publish_command(command)
            
            time.sleep(0.1)
    
    def _publish_command(self, command: str):
        """Publish command to message queue."""
        message = {
            'timestamp': datetime.utcnow().isoformat(),
            'command': command,
            'source': 'ultrasonic_agentics'
        }
        
        if self.queue_type == 'redis':
            self.redis_client.lpush(
                self.queue_name,
                json.dumps(message)
            )
        elif self.queue_type == 'rabbitmq':
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message)
            )
```

## Security Hardening

### Key Rotation

Implement automatic key rotation:

```python
import time
import threading
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureProcessor:
    def __init__(self, master_password: str, rotation_interval: int = 3600):
        self.master_password = master_password.encode()
        self.rotation_interval = rotation_interval  # seconds
        self.current_key = None
        self.key_version = 0
        
        self.encoder = UltrasonicEncoder()
        self.decoder = UltrasonicDecoder()
        
        self._generate_key()
        self._start_key_rotation()
    
    def _generate_key(self):
        """Generate new encryption key."""
        # Use timestamp as salt for deterministic key generation
        timestamp = int(time.time() / self.rotation_interval) * self.rotation_interval
        salt = f"ultrasonic_{timestamp}_{self.key_version}".encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        self.current_key = kdf.derive(self.master_password)
        self.key_version += 1
    
    def _start_key_rotation(self):
        """Start automatic key rotation."""
        def rotation_loop():
            while True:
                time.sleep(self.rotation_interval)
                self._generate_key()
        
        rotation_thread = threading.Thread(target=rotation_loop, daemon=True)
        rotation_thread.start()
    
    def encode_secure(self, command: str) -> np.ndarray:
        """Encode command with current key."""
        from ..crypto.cipher import CipherService
        
        cipher = CipherService(self.current_key)
        encrypted_data = cipher.encrypt(command.encode())
        
        # Prepend key version for decoding
        versioned_data = bytes([self.key_version & 0xFF]) + encrypted_data
        
        return self.encoder.encode_payload(versioned_data)
    
    def decode_secure(self, signal: np.ndarray) -> str:
        """Decode command with key version detection."""
        from ..crypto.cipher import CipherService
        
        raw_data = self.decoder.decode_payload(signal)
        if raw_data is None or len(raw_data) < 2:
            return None
        
        # Extract key version
        key_version = raw_data[0]
        encrypted_data = raw_data[1:]
        
        # Generate historical key for this version
        historical_key = self._generate_historical_key(key_version)
        
        try:
            cipher = CipherService(historical_key)
            decrypted_data = cipher.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')
        except Exception:
            return None
    
    def _generate_historical_key(self, version: int) -> bytes:
        """Generate key for specific version."""
        # Calculate timestamp for this key version
        current_period = int(time.time() / self.rotation_interval)
        target_period = current_period - (self.key_version - version)
        timestamp = target_period * self.rotation_interval
        
        salt = f"ultrasonic_{timestamp}_{version}".encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        return kdf.derive(self.master_password)
```

### Command Validation

Implement command structure validation and rate limiting:

```python
import re
from collections import defaultdict
from datetime import datetime, timedelta

class CommandValidator:
    def __init__(self):
        self.allowed_commands = {
            'execute': r'^execute:[a-zA-Z_][a-zA-Z0-9_]*$',
            'status': r'^status:(check|report|update)$',
            'configure': r'^configure:[a-zA-Z_][a-zA-Z0-9_]*=[a-zA-Z0-9_]+$',
            'transmit': r'^transmit:[a-zA-Z0-9_]+$'
        }
        
        # Rate limiting: max 10 commands per minute per command type
        self.rate_limits = defaultdict(lambda: {'count': 0, 'reset_time': datetime.now()})
        self.max_commands_per_minute = 10
    
    def validate_command(self, command: str) -> bool:
        """Validate command format and rate limits."""
        # Basic format check
        if not self._validate_format(command):
            return False
        
        # Rate limiting check
        if not self._check_rate_limit(command):
            return False
        
        return True
    
    def _validate_format(self, command: str) -> bool:
        """Validate command format against allowed patterns."""
        for cmd_type, pattern in self.allowed_commands.items():
            if command.startswith(cmd_type + ':'):
                return bool(re.match(pattern, command))
        
        return False
    
    def _check_rate_limit(self, command: str) -> bool:
        """Check if command exceeds rate limits."""
        cmd_type = command.split(':')[0]
        now = datetime.now()
        
        # Reset counter if a minute has passed
        if now - self.rate_limits[cmd_type]['reset_time'] > timedelta(minutes=1):
            self.rate_limits[cmd_type] = {'count': 0, 'reset_time': now}
        
        # Check rate limit
        if self.rate_limits[cmd_type]['count'] >= self.max_commands_per_minute:
            return False
        
        # Increment counter
        self.rate_limits[cmd_type]['count'] += 1
        return True
```

## Troubleshooting and Debugging

### Signal Analysis Tools

Tools for analyzing and debugging ultrasonic signals:

```python
import matplotlib.pyplot as plt
from scipy import signal as scipy_signal

class SignalAnalyzer:
    def __init__(self):
        self.sample_rate = 48000
    
    def analyze_spectrum(self, audio_data: np.ndarray, title: str = "Spectrum Analysis"):
        """Plot frequency spectrum of audio signal."""
        freqs, psd = scipy_signal.welch(audio_data, self.sample_rate, nperseg=1024)
        
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(np.arange(len(audio_data)) / self.sample_rate, audio_data)
        plt.title(f'{title} - Time Domain')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        
        plt.subplot(2, 1, 2)
        plt.semilogy(freqs, psd)
        plt.title(f'{title} - Frequency Domain')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power Spectral Density')
        plt.xlim(15000, 25000)  # Focus on ultrasonic range
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def compare_signals(self, original: np.ndarray, processed: np.ndarray):
        """Compare original and processed signals."""
        plt.figure(figsize=(15, 10))
        
        # Time domain comparison
        plt.subplot(3, 2, 1)
        plt.plot(original[:min(1000, len(original))])
        plt.title('Original Signal (first 1000 samples)')
        
        plt.subplot(3, 2, 2)
        plt.plot(processed[:min(1000, len(processed))])
        plt.title('Processed Signal (first 1000 samples)')
        
        # Frequency domain comparison
        freqs_orig, psd_orig = scipy_signal.welch(original, self.sample_rate)
        freqs_proc, psd_proc = scipy_signal.welch(processed, self.sample_rate)
        
        plt.subplot(3, 2, 3)
        plt.semilogy(freqs_orig, psd_orig)
        plt.title('Original - Frequency Domain')
        plt.xlim(15000, 25000)
        
        plt.subplot(3, 2, 4)
        plt.semilogy(freqs_proc, psd_proc)
        plt.title('Processed - Frequency Domain')
        plt.xlim(15000, 25000)
        
        # Difference
        min_len = min(len(original), len(processed))
        diff = processed[:min_len] - original[:min_len]
        
        plt.subplot(3, 2, 5)
        plt.plot(diff)
        plt.title('Difference Signal')
        
        freqs_diff, psd_diff = scipy_signal.welch(diff, self.sample_rate)
        plt.subplot(3, 2, 6)
        plt.semilogy(freqs_diff, psd_diff)
        plt.title('Difference - Frequency Domain')
        plt.xlim(15000, 25000)
        
        plt.tight_layout()
        plt.show()
    
    def detect_interference(self, audio_data: np.ndarray) -> dict:
        """Detect potential interference in ultrasonic range."""
        freqs, psd = scipy_signal.welch(audio_data, self.sample_rate, nperseg=2048)
        
        # Focus on ultrasonic range (15-25 kHz)
        ultrasonic_mask = (freqs >= 15000) & (freqs <= 25000)
        ultrasonic_freqs = freqs[ultrasonic_mask]
        ultrasonic_psd = psd[ultrasonic_mask]
        
        # Find peaks in ultrasonic range
        peaks, properties = scipy_signal.find_peaks(
            ultrasonic_psd, 
            height=np.mean(ultrasonic_psd) * 3,  # 3x above average
            distance=50  # Minimum distance between peaks
        )
        
        interference_analysis = {
            'total_power': np.sum(ultrasonic_psd),
            'peak_frequencies': ultrasonic_freqs[peaks].tolist(),
            'peak_powers': ultrasonic_psd[peaks].tolist(),
            'noise_floor': np.median(ultrasonic_psd),
            'snr_estimate': np.max(ultrasonic_psd) / np.median(ultrasonic_psd)
        }
        
        return interference_analysis
```

### Debugging Configuration

Enable detailed logging and debugging:

```python
import logging
import sys
from datetime import datetime

class DebugConfig:
    @staticmethod
    def setup_logging(level: str = 'DEBUG', log_file: str = None):
        """Setup comprehensive logging."""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_file or f'ultrasonic_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
            ]
        )
        
        # Set specific logger levels
        logging.getLogger('ultrasonic_agentics').setLevel(logging.DEBUG)
        logging.getLogger('scipy').setLevel(logging.WARNING)
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    @staticmethod
    def enable_debug_mode():
        """Enable debug mode with enhanced logging."""
        DebugConfig.setup_logging('DEBUG')
        
        # Add debug hooks to key classes
        original_encode = UltrasonicEncoder.encode_payload
        original_decode = UltrasonicDecoder.decode_payload
        
        def debug_encode(self, payload, add_preamble=True):
            logger = logging.getLogger(f'{self.__class__.__name__}')
            logger.debug(f'Encoding payload: {len(payload)} bytes, preamble: {add_preamble}')
            logger.debug(f'Frequencies: {self.freq_0} Hz / {self.freq_1} Hz')
            
            result = original_encode(self, payload, add_preamble)
            
            logger.debug(f'Generated signal: {len(result)} samples, duration: {len(result)/self.sample_rate:.3f}s')
            return result
        
        def debug_decode(self, audio_signal):
            logger = logging.getLogger(f'{self.__class__.__name__}')
            logger.debug(f'Decoding signal: {len(audio_signal)} samples')
            
            # Analyze signal strength
            power = np.mean(np.abs(audio_signal))
            logger.debug(f'Signal power: {power:.6f}')
            
            result = original_decode(self, audio_signal)
            
            if result:
                logger.debug(f'Decoded {len(result)} bytes successfully')
            else:
                logger.debug('Decoding failed')
            
            return result
        
        # Monkey patch for debugging
        UltrasonicEncoder.encode_payload = debug_encode
        UltrasonicDecoder.decode_payload = debug_decode
```

This advanced usage guide provides comprehensive techniques for optimizing and extending the Ultrasonic Agentics framework. Users can combine these approaches based on their specific requirements for performance, security, and reliability.