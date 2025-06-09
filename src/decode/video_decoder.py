"""
Video decoder for extracting encrypted commands from video files.
Extracts audio and processes it for hidden commands.
"""

import os
import tempfile
from typing import Optional
try:
    from moviepy import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    VideoFileClip = None
from .audio_decoder import AudioDecoder


class VideoDecoder:
    """Service for decoding encrypted commands from video files."""
    
    def __init__(self,
                 key: bytes,
                 ultrasonic_freq: float = 18500,
                 freq_separation: float = 1000,
                 sample_rate: int = 48000,
                 bit_duration: float = 0.01,
                 detection_threshold: float = 0.1):
        """
        Initialize video decoder.
        
        Args:
            key: Decryption key
            ultrasonic_freq: Base frequency for ultrasonic carrier
            freq_separation: Frequency separation for FSK
            sample_rate: Audio sample rate
            bit_duration: Duration per bit in seconds
            detection_threshold: Signal detection threshold
        """
        if not MOVIEPY_AVAILABLE:
            raise ImportError("MoviePy is required for video processing but not available")
            
        self.audio_decoder = AudioDecoder(
            key=key,
            ultrasonic_freq=ultrasonic_freq,
            freq_separation=freq_separation,
            sample_rate=sample_rate,
            bit_duration=bit_duration,
            detection_threshold=detection_threshold
        )
    
    def decode_file(self, video_path: str, temp_dir: str = None) -> Optional[str]:
        """
        Decode command from video file.
        
        Args:
            video_path: Path to video file
            temp_dir: Temporary directory for audio extraction
            
        Returns:
            Decoded command string, or None if decoding fails
        """
        if temp_dir is None:
            temp_dir = tempfile.gettempdir()
        
        # Generate unique temporary file name
        temp_audio = os.path.join(temp_dir, f"temp_video_audio_{os.getpid()}.wav")
        
        try:
            # Load video
            video = VideoFileClip(video_path)
            
            if video.audio is None:
                video.close()
                return None
            
            # Extract audio to temporary file
            video.audio.write_audiofile(
                temp_audio,
                codec='pcm_s16le',  # Uncompressed for quality
                verbose=False,
                logger=None
            )
            
            # Decode command from audio
            command = self.audio_decoder.decode_file(temp_audio)
            
            # Clean up
            video.close()
            
            return command
            
        except Exception as e:
            print(f"Error decoding video: {e}")
            return None
            
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)
            except OSError:
                pass
    
    def decode_video_clip(self, video_clip: VideoFileClip) -> Optional[str]:
        """
        Decode command from video clip object.
        
        Args:
            video_clip: Input video clip
            
        Returns:
            Decoded command string, or None if decoding fails
        """
        if video_clip.audio is None:
            return None
        
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Extract audio
            video_clip.audio.write_audiofile(
                temp_path,
                codec='pcm_s16le',
                verbose=False,
                logger=None
            )
            
            # Decode command
            command = self.audio_decoder.decode_file(temp_path)
            
            return command
            
        except Exception as e:
            print(f"Error decoding video clip: {e}")
            return None
            
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except OSError:
                pass
    
    def detect_signal(self, video_path: str) -> bool:
        """
        Check if ultrasonic signal is present in video.
        
        Args:
            video_path: Path to video file
            
        Returns:
            True if signal detected
        """
        try:
            video = VideoFileClip(video_path)
            
            if video.audio is None:
                video.close()
                return False
            
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix='.wav') as temp_file:
                video.audio.write_audiofile(
                    temp_file.name,
                    codec='pcm_s16le',
                    verbose=False,
                    logger=None
                )
                
                # Check for signal
                has_signal = self.audio_decoder.detect_signal(temp_file.name)
            
            video.close()
            return has_signal
            
        except Exception:
            return False
    
    def get_signal_strength(self, video_path: str) -> float:
        """
        Get signal strength in video audio.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Signal strength (0.0 to 1.0)
        """
        try:
            video = VideoFileClip(video_path)
            
            if video.audio is None:
                video.close()
                return 0.0
            
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix='.wav') as temp_file:
                video.audio.write_audiofile(
                    temp_file.name,
                    codec='pcm_s16le',
                    verbose=False,
                    logger=None
                )
                
                # Get signal strength
                strength = self.audio_decoder.get_signal_strength(temp_file.name)
            
            video.close()
            return strength
            
        except Exception:
            return 0.0
    
    def analyze_video(self, video_path: str) -> dict:
        """
        Analyze video for steganographic content.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Analysis results dictionary
        """
        try:
            video = VideoFileClip(video_path)
            
            if video.audio is None:
                video.close()
                return {
                    'file_path': video_path,
                    'has_audio': False,
                    'error': 'No audio track found',
                    'has_ultrasonic_signal': False,
                    'signal_strength': 0.0,
                    'decoded_command': None,
                    'decoding_successful': False
                }
            
            # Get video info
            video_info = {
                'file_path': video_path,
                'has_audio': True,
                'video_duration': video.duration,
                'video_fps': video.fps,
                'video_size': video.size,
                'audio_fps': video.audio.fps if video.audio else None
            }
            
            # Create temporary audio file for analysis
            with tempfile.NamedTemporaryFile(suffix='.wav') as temp_file:
                video.audio.write_audiofile(
                    temp_file.name,
                    codec='pcm_s16le',
                    verbose=False,
                    logger=None
                )
                
                # Analyze audio
                audio_analysis = self.audio_decoder.analyze_audio(temp_file.name)
            
            # Combine results
            result = {**video_info, **audio_analysis}
            
            video.close()
            return result
            
        except Exception as e:
            return {
                'file_path': video_path,
                'error': str(e),
                'has_audio': False,
                'has_ultrasonic_signal': False,
                'signal_strength': 0.0,
                'decoded_command': None,
                'decoding_successful': False
            }
    
    def get_cipher_key(self) -> bytes:
        """Get the decryption key."""
        return self.audio_decoder.get_cipher_key()
    
    def set_cipher_key(self, key: bytes) -> None:
        """Set new decryption key."""
        self.audio_decoder.set_cipher_key(key)
    
    def get_frequency_range(self) -> tuple:
        """Get ultrasonic frequency range."""
        return self.audio_decoder.get_frequency_range()
    
    def set_frequencies(self, freq_0: float, freq_1: float) -> None:
        """Set new ultrasonic frequencies."""
        self.audio_decoder.set_frequencies(freq_0, freq_1)
    
    def set_detection_threshold(self, threshold: float) -> None:
        """Set signal detection threshold."""
        self.audio_decoder.set_detection_threshold(threshold)