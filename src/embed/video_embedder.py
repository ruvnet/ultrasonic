"""
Video embedder for embedding encrypted commands into video files.
Extracts audio, embeds command, then recombines with video.
"""

import os
import tempfile
from typing import Optional
try:
    from moviepy import VideoFileClip, AudioFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    VideoFileClip = None
    AudioFileClip = None
from .audio_embedder import AudioEmbedder


class VideoEmbedder:
    """Service for embedding encrypted commands into video files."""
    
    def __init__(self,
                 key: bytes = None,
                 ultrasonic_freq: float = 18500,
                 freq_separation: float = 1000,
                 sample_rate: int = 48000,
                 bit_duration: float = 0.01,
                 amplitude: float = 0.1):
        """
        Initialize video embedder.
        
        Args:
            key: Encryption key (if None, random key generated)
            ultrasonic_freq: Base frequency for ultrasonic carrier
            freq_separation: Frequency separation for FSK
            sample_rate: Audio sample rate
            bit_duration: Duration per bit in seconds
            amplitude: Ultrasonic signal amplitude
        """
        if not MOVIEPY_AVAILABLE:
            raise ImportError("MoviePy is required for video processing but not available")
        
        self.audio_embedder = AudioEmbedder(
            key=key,
            ultrasonic_freq=ultrasonic_freq,
            freq_separation=freq_separation,
            sample_rate=sample_rate,
            bit_duration=bit_duration,
            amplitude=amplitude
        )
    
    def embed_file(self,
                   input_path: str,
                   output_path: str,
                   command: str,
                   obfuscate: bool = True,
                   audio_bitrate: str = "192k",
                   video_bitrate: str = None,
                   temp_dir: str = None) -> None:
        """
        Embed command into video file.
        
        Args:
            input_path: Path to input video file
            output_path: Path to output video file
            command: Command string to embed
            obfuscate: Whether to add obfuscation
            audio_bitrate: Audio bitrate for output
            video_bitrate: Video bitrate for output (None for auto)
            temp_dir: Temporary directory for intermediate files
        """
        if temp_dir is None:
            temp_dir = tempfile.gettempdir()
        
        # Generate unique temporary file names
        temp_audio_input = os.path.join(temp_dir, f"temp_audio_input_{os.getpid()}.wav")
        temp_audio_output = os.path.join(temp_dir, f"temp_audio_output_{os.getpid()}.wav")
        
        try:
            # Load video
            video = VideoFileClip(input_path)
            
            if video.audio is None:
                raise ValueError("Input video has no audio track")
            
            # Extract audio to temporary file
            try:
                # Try MoviePy 2.x syntax first
                video.audio.write_audiofile(
                    temp_audio_input,
                    codec='pcm_s16le'  # Uncompressed for quality
                )
            except TypeError:
                # Fall back to older syntax if needed
                video.audio.write_audiofile(
                    temp_audio_input,
                    codec='pcm_s16le',
                    verbose=False,
                    logger=None
                )
            
            # Embed command in audio
            self.audio_embedder.embed_file(
                input_path=temp_audio_input,
                output_path=temp_audio_output,
                command=command,
                obfuscate=obfuscate,
                bitrate=audio_bitrate
            )
            
            # Load modified audio
            new_audio = AudioFileClip(temp_audio_output)
            
            # Replace audio in video
            try:
                # Try MoviePy 2.x syntax first
                final_video = video.with_audio(new_audio)
            except AttributeError:
                # Fall back to older syntax if needed
                final_video = video.set_audio(new_audio)
            
            # Prepare output parameters
            output_params = {
                'codec': 'libx264',
                'audio_codec': 'aac',
                'temp_audiofile': os.path.join(temp_dir, f"temp_audiofile_{os.getpid()}.m4a"),
                'remove_temp': True
            }
            
            if video_bitrate:
                output_params['bitrate'] = video_bitrate
            
            # Export final video
            try:
                # Try MoviePy 2.x syntax first
                final_video.write_videofile(output_path, **output_params)
            except TypeError:
                # Fall back to older syntax if needed
                output_params['verbose'] = False
                output_params['logger'] = None
                final_video.write_videofile(output_path, **output_params)
            
            # Clean up
            video.close()
            new_audio.close()
            final_video.close()
            
        finally:
            # Clean up temporary files
            for temp_file in [temp_audio_input, temp_audio_output]:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except OSError:
                    pass  # Ignore cleanup errors
    
    def embed_video_clip(self,
                         video_clip: VideoFileClip,
                         command: str,
                         obfuscate: bool = True) -> VideoFileClip:
        """
        Embed command into video clip object.
        
        Args:
            video_clip: Input video clip
            command: Command to embed
            obfuscate: Whether to add obfuscation
            
        Returns:
            New video clip with embedded command
        """
        if video_clip.audio is None:
            raise ValueError("Video clip has no audio track")
        
        # Create temporary file for audio processing
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_input:
            temp_input_path = temp_input.name
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_output:
            temp_output_path = temp_output.name
        
        try:
            # Extract audio
            video_clip.audio.write_audiofile(
                temp_input_path,
                codec='pcm_s16le',
                verbose=False,
                logger=None
            )
            
            # Embed command
            self.audio_embedder.embed_file(
                input_path=temp_input_path,
                output_path=temp_output_path,
                command=command,
                obfuscate=obfuscate
            )
            
            # Load modified audio
            new_audio = AudioFileClip(temp_output_path)
            
            # Create new video with modified audio
            result_video = video_clip.set_audio(new_audio)
            
            return result_video
            
        finally:
            # Clean up temporary files
            for temp_file in [temp_input_path, temp_output_path]:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except OSError:
                    pass
    
    def validate_video_compatibility(self, video_path: str) -> dict:
        """
        Check if video is compatible for embedding.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with compatibility info
        """
        try:
            video = VideoFileClip(video_path)
            
            if video.audio is None:
                return {
                    'compatible': False,
                    'error': 'No audio track found',
                    'has_audio': False
                }
            
            # Create temporary audio file for analysis
            with tempfile.NamedTemporaryFile(suffix='.wav') as temp_audio:
                video.audio.write_audiofile(
                    temp_audio.name,
                    codec='pcm_s16le',
                    verbose=False,
                    logger=None
                )
                
                # Load as AudioSegment for analysis
                from pydub import AudioSegment
                audio = AudioSegment.from_file(temp_audio.name)
                
                # Check audio compatibility
                audio_compat = self.audio_embedder.validate_audio_compatibility(audio)
                
                result = {
                    'compatible': audio_compat['compatible'],
                    'has_audio': True,
                    'video_duration': video.duration,
                    'video_fps': video.fps,
                    'video_size': video.size,
                    'audio_info': audio_compat
                }
                
                video.close()
                return result
                
        except Exception as e:
            return {
                'compatible': False,
                'error': str(e),
                'has_audio': False
            }
    
    def get_cipher_key(self) -> bytes:
        """Get the encryption key."""
        return self.audio_embedder.get_cipher_key()
    
    def set_cipher_key(self, key: bytes) -> None:
        """Set new encryption key."""
        self.audio_embedder.set_cipher_key(key)
    
    def get_frequency_range(self) -> tuple:
        """Get ultrasonic frequency range."""
        return self.audio_embedder.get_frequency_range()
    
    def set_frequencies(self, freq_0: float, freq_1: float) -> None:
        """Set new ultrasonic frequencies."""
        self.audio_embedder.set_frequencies(freq_0, freq_1)
    
    def set_amplitude(self, amplitude: float) -> None:
        """Set ultrasonic signal amplitude."""
        self.audio_embedder.set_amplitude(amplitude)
    
    def estimate_embedding_duration(self, command: str) -> float:
        """
        Estimate duration needed for embedding command.
        
        Args:
            command: Command to embed
            
        Returns:
            Duration in seconds
        """
        return self.audio_embedder.estimate_embedding_duration(command)