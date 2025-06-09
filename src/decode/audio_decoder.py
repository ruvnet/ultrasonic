"""
Audio decoder for extracting encrypted commands from audio files.
Combines ultrasonic decoding, decryption, and real-time processing.
"""

import threading
import time
from typing import Optional, Callable, Union
import numpy as np
from pydub import AudioSegment
try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except (ImportError, OSError):
    SOUNDDEVICE_AVAILABLE = False
    sd = None
from ..crypto.cipher import CipherService
from .ultrasonic_decoder import UltrasonicDecoder


class AudioDecoder:
    """Service for decoding encrypted commands from audio files."""
    
    def __init__(self,
                 key: bytes,
                 ultrasonic_freq: float = 18500,
                 freq_separation: float = 1000,
                 sample_rate: int = 48000,
                 bit_duration: float = 0.01,
                 detection_threshold: float = 0.01):
        """
        Initialize audio decoder.
        
        Args:
            key: Decryption key
            ultrasonic_freq: Base frequency for ultrasonic carrier
            freq_separation: Frequency separation for FSK
            sample_rate: Audio sample rate
            bit_duration: Duration per bit in seconds
            detection_threshold: Signal detection threshold
        """
        self.cipher = CipherService(key)
        
        self.decoder = UltrasonicDecoder(
            freq_0=ultrasonic_freq,
            freq_1=ultrasonic_freq + freq_separation,
            sample_rate=sample_rate,
            bit_duration=bit_duration,
            detection_threshold=detection_threshold
        )
        
        # Real-time processing state
        self._listening = False
        self._listen_thread = None
        self._callback = None
        self._stream = None
        self._buffer = np.array([])
        self._buffer_size = sample_rate * 2  # 2 second buffer
    
    def decode_file(self, file_path: str) -> Optional[str]:
        """
        Decode command from audio file.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Decoded command string, or None if decoding fails
        """
        try:
            # Load audio file
            audio = AudioSegment.from_file(file_path)
            
            # Convert to appropriate format
            audio = self._prepare_audio(audio)
            
            # Convert to numpy array
            audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
            
            # Normalize
            if len(audio_data) > 0:
                max_val = np.max(np.abs(audio_data))
                if max_val > 0:
                    audio_data = audio_data / max_val
            
            # Decode payload
            payload = self._decode_audio_data(audio_data)
            
            return payload
            
        except Exception as e:
            print(f"Error decoding file: {e}")
            return None
    
    def decode_audio_segment(self, audio: AudioSegment) -> Optional[str]:
        """
        Decode command from AudioSegment.
        
        Args:
            audio: AudioSegment to decode
            
        Returns:
            Decoded command string, or None if decoding fails
        """
        try:
            # Prepare audio
            audio = self._prepare_audio(audio)
            
            # Convert to numpy array
            audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
            
            # Normalize
            if len(audio_data) > 0:
                max_val = np.max(np.abs(audio_data))
                if max_val > 0:
                    audio_data = audio_data / max_val
            
            # Decode payload
            return self._decode_audio_data(audio_data)
            
        except Exception as e:
            print(f"Error decoding audio segment: {e}")
            return None
    
    def start_listening(self,
                       input_device: Optional[int] = None,
                       callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Start real-time listening for commands.
        
        Args:
            input_device: Audio input device ID (None for default)
            callback: Function to call when command is detected
            
        Returns:
            True if listening started successfully
        """
        if not SOUNDDEVICE_AVAILABLE:
            print("Real-time listening not available: sounddevice library not found")
            return False
            
        if self._listening:
            return False
        
        try:
            self._callback = callback
            self._listening = True
            
            # Start audio stream
            self._stream = sd.InputStream(
                device=input_device,
                channels=1,
                samplerate=self.decoder.sample_rate,
                dtype='float32',
                blocksize=1024,
                callback=self._audio_callback
            )
            
            self._stream.start()
            
            # Start processing thread
            self._listen_thread = threading.Thread(target=self._process_buffer)
            self._listen_thread.daemon = True
            self._listen_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error starting listening: {e}")
            self._listening = False
            return False
    
    def stop_listening(self) -> None:
        """Stop real-time listening."""
        self._listening = False
        
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        
        if self._listen_thread:
            self._listen_thread.join(timeout=1.0)
            self._listen_thread = None
        
        self._buffer = np.array([])
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback for real-time audio processing."""
        if status:
            print(f"Audio callback status: {status}")
        
        if self._listening:
            # Add new data to buffer
            new_data = indata[:, 0]  # Take first channel
            self._buffer = np.append(self._buffer, new_data)
            
            # Keep buffer size reasonable
            if len(self._buffer) > self._buffer_size:
                self._buffer = self._buffer[-self._buffer_size:]
    
    def _process_buffer(self) -> None:
        """Process audio buffer for commands."""
        while self._listening:
            if len(self._buffer) >= self._buffer_size // 2:
                # Try to decode from current buffer
                command = self._decode_audio_data(self._buffer.copy())
                
                if command and self._callback:
                    try:
                        self._callback(command)
                    except Exception as e:
                        print(f"Error in callback: {e}")
            
            time.sleep(0.1)  # Check every 100ms
    
    def _prepare_audio(self, audio: AudioSegment) -> AudioSegment:
        """Prepare audio for decoding."""
        # Convert to mono if stereo
        if audio.channels > 1:
            audio = audio.set_channels(1)
        
        # Set appropriate sample rate
        if audio.frame_rate != self.decoder.sample_rate:
            audio = audio.set_frame_rate(self.decoder.sample_rate)
        
        return audio
    
    def _decode_audio_data(self, audio_data: np.ndarray) -> Optional[str]:
        """
        Decode command from audio data.
        
        Args:
            audio_data: Audio signal as numpy array
            
        Returns:
            Decoded command string, or None if decoding fails
        """
        # Extract payload using ultrasonic decoder
        payload = self.decoder.decode_payload(audio_data)
        
        if payload is None:
            return None
        
        # Remove obfuscation if present
        deobfuscated = self._remove_obfuscation(payload)
        if deobfuscated is None:
            return None
        
        # Decrypt command
        command = self._decrypt_payload(deobfuscated)
        
        return command
    
    def _remove_obfuscation(self, payload: bytes) -> Optional[bytes]:
        """Remove obfuscation from payload."""
        # Try to remove obfuscation first
        deobfuscated = self.cipher.remove_obfuscation(payload)
        if deobfuscated is not None:
            return deobfuscated
        
        # If that fails, assume payload is not obfuscated
        return payload
    
    def _decrypt_payload(self, payload: bytes) -> Optional[str]:
        """Decrypt payload to get command."""
        return self.cipher.decrypt_command(payload)
    
    def detect_signal(self, audio: Union[str, AudioSegment]) -> bool:
        """
        Check if ultrasonic signal is present.
        
        Args:
            audio: Audio file path or AudioSegment
            
        Returns:
            True if signal detected
        """
        try:
            if isinstance(audio, str):
                audio = AudioSegment.from_file(audio)
            
            audio = self._prepare_audio(audio)
            audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
            
            if len(audio_data) > 0:
                max_val = np.max(np.abs(audio_data))
                if max_val > 0:
                    audio_data = audio_data / max_val
            
            return self.decoder.detect_signal_presence(audio_data)
            
        except Exception:
            return False
    
    def get_signal_strength(self, audio: Union[str, AudioSegment]) -> float:
        """
        Get signal strength in audio.
        
        Args:
            audio: Audio file path or AudioSegment
            
        Returns:
            Signal strength (0.0 to 1.0)
        """
        try:
            if isinstance(audio, str):
                audio = AudioSegment.from_file(audio)
            
            audio = self._prepare_audio(audio)
            audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
            
            if len(audio_data) > 0:
                max_val = np.max(np.abs(audio_data))
                if max_val > 0:
                    audio_data = audio_data / max_val
            
            return self.decoder.get_signal_strength(audio_data)
            
        except Exception:
            return 0.0
    
    def is_listening(self) -> bool:
        """Check if currently listening for commands."""
        return self._listening
    
    def get_cipher_key(self) -> bytes:
        """Get the decryption key."""
        return self.cipher.get_key()
    
    def set_cipher_key(self, key: bytes) -> None:
        """Set new decryption key."""
        self.cipher.set_key(key)
    
    def get_frequency_range(self) -> tuple:
        """Get ultrasonic frequency range."""
        return (self.decoder.freq_0, self.decoder.freq_1)
    
    def set_frequencies(self, freq_0: float, freq_1: float) -> None:
        """Set new ultrasonic frequencies."""
        self.decoder.set_frequencies(freq_0, freq_1)
    
    def set_detection_threshold(self, threshold: float) -> None:
        """Set signal detection threshold."""
        self.decoder.set_detection_threshold(threshold)
    
    def analyze_audio(self, audio: Union[str, AudioSegment]) -> dict:
        """
        Analyze audio for steganographic content.
        
        Args:
            audio: Audio file path or AudioSegment
            
        Returns:
            Analysis results dictionary
        """
        try:
            if isinstance(audio, str):
                audio_segment = AudioSegment.from_file(audio)
                file_path = audio
            else:
                audio_segment = audio
                file_path = None
            
            audio_segment = self._prepare_audio(audio_segment)
            audio_data = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
            
            if len(audio_data) > 0:
                max_val = np.max(np.abs(audio_data))
                if max_val > 0:
                    audio_data = audio_data / max_val
            
            # Analyze signal
            has_signal = self.decoder.detect_signal_presence(audio_data)
            signal_strength = self.decoder.get_signal_strength(audio_data)
            
            # Try to decode
            decoded_command = None
            if has_signal:
                decoded_command = self._decode_audio_data(audio_data)
            
            return {
                'file_path': file_path,
                'duration_seconds': len(audio_segment) / 1000.0,
                'sample_rate': audio_segment.frame_rate,
                'channels': audio_segment.channels,
                'has_ultrasonic_signal': has_signal,
                'signal_strength': signal_strength,
                'frequency_range': self.get_frequency_range(),
                'decoded_command': decoded_command,
                'decoding_successful': decoded_command is not None
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'has_ultrasonic_signal': False,
                'signal_strength': 0.0,
                'decoded_command': None,
                'decoding_successful': False
            }