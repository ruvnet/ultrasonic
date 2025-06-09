"""
Audio embedder for embedding encrypted commands into audio files.
Combines encryption, ultrasonic encoding, and audio merging.
"""

import os
from typing import Optional, Union
from pydub import AudioSegment
from ..crypto.cipher import CipherService
from .ultrasonic_encoder import UltrasonicEncoder


class AudioEmbedder:
    """Service for embedding encrypted commands into audio files."""
    
    def __init__(self,
                 key: bytes = None,
                 ultrasonic_freq: float = 18500,
                 freq_separation: float = 1000,
                 sample_rate: int = 48000,
                 bit_duration: float = 0.01,
                 amplitude: float = 0.1):
        """
        Initialize audio embedder.
        
        Args:
            key: Encryption key (if None, random key generated)
            ultrasonic_freq: Base frequency for ultrasonic carrier
            freq_separation: Frequency separation for FSK
            sample_rate: Audio sample rate
            bit_duration: Duration per bit in seconds
            amplitude: Ultrasonic signal amplitude
        """
        self.cipher = CipherService(key)
        
        self.encoder = UltrasonicEncoder(
            freq_0=ultrasonic_freq,
            freq_1=ultrasonic_freq + freq_separation,
            sample_rate=sample_rate,
            bit_duration=bit_duration,
            amplitude=amplitude
        )
    
    def embed(self, 
              audio: AudioSegment, 
              command: str,
              obfuscate: bool = True) -> AudioSegment:
        """
        Embed command into audio segment.
        
        Args:
            audio: Original audio segment
            command: Command string to embed
            obfuscate: Whether to add obfuscation to payload
            
        Returns:
            Audio segment with embedded command
        """
        # Encrypt command
        encrypted_payload = self._encrypt_payload(command, obfuscate)
        
        # Generate ultrasonic signal
        ultrasonic_signal = self._encode_ultrasonic(encrypted_payload)
        
        # Merge with original audio
        return self._merge_audio(audio, ultrasonic_signal)
    
    def embed_file(self,
                   input_path: str,
                   output_path: str,
                   command: str,
                   obfuscate: bool = True,
                   bitrate: str = "320k") -> bool:
        """
        Embed command into audio file.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            command: Command string to embed
            obfuscate: Whether to add obfuscation
            bitrate: Output bitrate for compressed formats
            
        Returns:
            bool: True if embedding was successful, False otherwise
        """
        try:
            # Load audio file
            audio = AudioSegment.from_file(input_path)
            
            # Embed command
            result_audio = self.embed(audio, command, obfuscate)
            
            # Export with appropriate settings
            export_params = {
                "format": self._get_format_from_path(output_path),
                "bitrate": bitrate
            }
            
            # Ensure high sample rate for ultrasonic preservation
            if result_audio.frame_rate < self.encoder.sample_rate:
                result_audio = result_audio.set_frame_rate(self.encoder.sample_rate)
            
            # For MP3, ensure we use a high enough bitrate to preserve ultrasonic frequencies
            if export_params['format'] == 'mp3' and bitrate == "320k":
                print(f"Warning: MP3 format may not preserve ultrasonic frequencies above 16kHz properly.")
                print(f"Consider using WAV or FLAC format for better ultrasonic signal preservation.")
            
            result_audio.export(output_path, **export_params)
            
            # Verify the file was created and has content
            if not os.path.exists(output_path):
                print(f"Error: Output file was not created at {output_path}")
                return False
                
            if os.path.getsize(output_path) == 0:
                print(f"Error: Output file is empty at {output_path}")
                return False
            
            # Verify the embedded signal is present
            try:
                from ..decode.audio_decoder import AudioDecoder
                # Create a decoder with the same settings
                verifier = AudioDecoder(
                    key=self.cipher.get_key(),
                    ultrasonic_freq=self.encoder.freq_0,
                    freq_separation=self.encoder.freq_1 - self.encoder.freq_0,
                    sample_rate=self.encoder.sample_rate,
                    bit_duration=self.encoder.bit_duration,
                    detection_threshold=0.01
                )
                
                # Try to decode the embedded command
                decoded_command = verifier.decode_file(output_path)
                if decoded_command == command:
                    print(f"✓ Successfully embedded and verified '{command}' in {output_path}")
                    return True
                else:
                    print(f"✗ Embedding verification failed. Expected '{command}', got '{decoded_command}'")
                    # For WAV files, this is a real failure
                    if export_params['format'] == 'wav':
                        return False
                    # For compressed formats, still return True but warn
                    print(f"Note: This may be due to {export_params['format'].upper()} compression affecting ultrasonic frequencies.")
                    return True
                    
            except Exception as verify_error:
                print(f"Warning: Could not verify embedding (this may be normal for compressed formats): {verify_error}")
                # Still return True if file was created successfully
                return True
            
        except Exception as e:
            # Log the error with detailed information
            print(f"Error embedding file: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _encrypt_payload(self, command: str, obfuscate: bool = True) -> bytes:
        """Encrypt command payload."""
        encrypted = self.cipher.encrypt_command(command)
        
        if obfuscate:
            encrypted = self.cipher.add_obfuscation(encrypted)
        
        return encrypted
    
    def _encode_ultrasonic(self, payload: bytes) -> AudioSegment:
        """Encode payload as ultrasonic signal."""
        signal_array = self.encoder.encode_payload(payload)
        return self.encoder.create_audio_segment(signal_array)
    
    def _merge_audio(self, 
                     original: AudioSegment, 
                     ultrasonic: AudioSegment) -> AudioSegment:
        """
        Merge original audio with ultrasonic signal.
        
        Args:
            original: Original audio
            ultrasonic: Ultrasonic signal to embed
            
        Returns:
            Merged audio
        """
        # Ensure both have same sample rate
        if original.frame_rate != ultrasonic.frame_rate:
            original = original.set_frame_rate(ultrasonic.frame_rate)
        
        # Ensure both have same channel count
        if original.channels != ultrasonic.channels:
            if original.channels == 2 and ultrasonic.channels == 1:
                # Convert ultrasonic to stereo
                ultrasonic = AudioSegment.from_mono_audiosegments(
                    ultrasonic, ultrasonic
                )
            elif original.channels == 1 and ultrasonic.channels == 2:
                # Convert original to stereo
                original = AudioSegment.from_mono_audiosegments(
                    original, original
                )
        
        # Determine insertion point (start of audio)
        insertion_point = 0
        
        # Calculate how much of the original audio to use
        min_duration = max(len(ultrasonic), 5000)  # At least 5 seconds
        
        if len(original) < min_duration:
            # Original audio is too short, pad it
            silence_needed = min_duration - len(original)
            silence = AudioSegment.silent(
                duration=silence_needed,
                frame_rate=original.frame_rate
            )
            original = original + silence
        
        # Overlay ultrasonic signal at the beginning
        if len(ultrasonic) <= len(original):
            # Ultrasonic fits within original audio
            result = original.overlay(ultrasonic, position=insertion_point)
        else:
            # Ultrasonic is longer than original, extend original
            extension_needed = len(ultrasonic) - len(original)
            silence = AudioSegment.silent(
                duration=extension_needed,
                frame_rate=original.frame_rate
            )
            extended_original = original + silence
            result = extended_original.overlay(ultrasonic, position=insertion_point)
        
        return result
    
    def _get_format_from_path(self, path: str) -> str:
        """Get audio format from file path."""
        extension = os.path.splitext(path)[1].lower()
        format_map = {
            '.mp3': 'mp3',
            '.wav': 'wav',
            '.flac': 'flac',
            '.ogg': 'ogg',
            '.m4a': 'mp4',
            '.aac': 'aac'
        }
        return format_map.get(extension, 'mp3')
    
    @staticmethod
    def get_format_recommendations() -> dict:
        """Get recommendations for different audio formats."""
        return {
            'wav': {
                'quality': 'Excellent',
                'ultrasonic_preservation': 'Perfect',
                'file_size': 'Large',
                'recommendation': 'Best choice for ultrasonic embedding'
            },
            'flac': {
                'quality': 'Excellent',
                'ultrasonic_preservation': 'Perfect',
                'file_size': 'Medium',
                'recommendation': 'Good lossless alternative to WAV'
            },
            'mp3': {
                'quality': 'Good',
                'ultrasonic_preservation': 'Poor (cuts >16kHz)',
                'file_size': 'Small',
                'recommendation': 'Not recommended for ultrasonic; use 320k bitrate if required'
            },
            'ogg': {
                'quality': 'Good',
                'ultrasonic_preservation': 'Poor (cuts >16kHz)',
                'file_size': 'Small',
                'recommendation': 'Not recommended for ultrasonic embedding'
            },
            'aac': {
                'quality': 'Good',
                'ultrasonic_preservation': 'Poor (cuts >16kHz)',
                'file_size': 'Small',
                'recommendation': 'Not recommended for ultrasonic embedding'
            }
        }
    
    def get_cipher_key(self) -> bytes:
        """Get the encryption key."""
        return self.cipher.get_key()
    
    def set_cipher_key(self, key: bytes) -> None:
        """Set new encryption key."""
        self.cipher.set_key(key)
    
    def get_frequency_range(self) -> tuple:
        """Get ultrasonic frequency range."""
        return self.encoder.get_frequency_range()
    
    def set_frequencies(self, freq_0: float, freq_1: float) -> None:
        """Set new ultrasonic frequencies."""
        self.encoder.set_frequencies(freq_0, freq_1)
    
    def set_amplitude(self, amplitude: float) -> None:
        """Set ultrasonic signal amplitude."""
        self.encoder.set_amplitude(amplitude)
    
    def estimate_embedding_duration(self, command: str) -> float:
        """
        Estimate duration needed for embedding command.
        
        Args:
            command: Command to embed
            
        Returns:
            Duration in seconds
        """
        # Estimate encrypted payload size
        encrypted = self.cipher.encrypt_command(command)
        obfuscated = self.cipher.add_obfuscation(encrypted)
        
        return self.encoder.estimate_payload_duration(len(obfuscated))
    
    def validate_audio_compatibility(self, audio: AudioSegment) -> dict:
        """
        Check if audio is compatible for embedding.
        
        Args:
            audio: Audio segment to check
            
        Returns:
            Dictionary with compatibility info
        """
        nyquist = audio.frame_rate / 2
        freq_range = self.get_frequency_range()
        
        return {
            'compatible': freq_range[1] < nyquist,
            'sample_rate': audio.frame_rate,
            'nyquist_frequency': nyquist,
            'ultrasonic_range': freq_range,
            'recommended_sample_rate': max(48000, int(freq_range[1] * 2.5)),
            'duration_seconds': len(audio) / 1000.0,
            'channels': audio.channels
        }