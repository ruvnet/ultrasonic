"""MCP tools for embedding commands in media files."""

import os
import time
from typing import Optional
from ..schemas.embed import EmbedAudioRequest, EmbedVideoRequest, EmbedResponse
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from agentic_commands_stego.embed.video_embedder import VideoEmbedder
from agentic_commands_stego.crypto.cipher import CipherService


# Global embedders (will be configured via MCP server)
_audio_embedder: Optional[AudioEmbedder] = None
_video_embedder: Optional[VideoEmbedder] = None
_cipher_key: Optional[bytes] = None


def _ensure_embedders():
    """Ensure embedders are initialized."""
    global _audio_embedder, _video_embedder, _cipher_key
    
    if _cipher_key is None:
        _cipher_key = CipherService.generate_key(32)
    
    if _audio_embedder is None:
        _audio_embedder = AudioEmbedder(key=_cipher_key)
    
    if _video_embedder is None:
        _video_embedder = VideoEmbedder(key=_cipher_key)


def set_cipher_key(key: bytes):
    """Set the encryption key for embedders."""
    global _audio_embedder, _video_embedder, _cipher_key
    
    _cipher_key = key
    
    # Recreate embedders with new key
    _audio_embedder = AudioEmbedder(key=_cipher_key)
    _video_embedder = VideoEmbedder(key=_cipher_key)


def embed_audio_command(request: EmbedAudioRequest) -> EmbedResponse:
    """
    Embed an encrypted command into an audio file using ultrasonic steganography.
    
    This tool takes an audio file and embeds a command into it using high-frequency
    ultrasonic encoding that is inaudible to humans but can be detected by the decoder.
    The command is encrypted before embedding for security.
    
    Args:
        request: Audio embedding parameters including file path, command, and options
        
    Returns:
        EmbedResponse with details about the embedding operation
        
    Raises:
        FileNotFoundError: If the input audio file doesn't exist
        ValueError: If the audio format is not supported
        RuntimeError: If the embedding operation fails
    """
    _ensure_embedders()
    
    start_time = time.time()
    
    try:
        # Validate input file
        if not os.path.exists(request.audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {request.audio_file_path}")
        
        # Generate output path if not specified
        if request.output_path is None:
            base_name = os.path.splitext(request.audio_file_path)[0]
            request.output_path = f"{base_name}_embedded.mp3"
        
        # Configure embedder
        _audio_embedder.set_frequencies(
            request.ultrasonic_freq, 
            request.ultrasonic_freq + 1000
        )
        _audio_embedder.set_amplitude(request.amplitude)
        
        # Perform embedding
        _audio_embedder.embed_file(
            request.audio_file_path,
            request.output_path,
            request.command,
            request.obfuscate,
            request.bitrate
        )
        
        # Get file size
        file_size = os.path.getsize(request.output_path)
        processing_time = (time.time() - start_time) * 1000
        
        return EmbedResponse(
            success=True,
            output_file=request.output_path,
            embedded_command=request.command,
            file_size_bytes=file_size,
            processing_time_ms=processing_time,
            message=f"Successfully embedded command in audio file: {request.output_path}",
            encryption_used=True,
            ultrasonic_freq=request.ultrasonic_freq,
            amplitude=request.amplitude
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        return EmbedResponse(
            success=False,
            output_file="",
            embedded_command=request.command,
            file_size_bytes=0,
            processing_time_ms=processing_time,
            message=f"Embedding failed: {str(e)}",
            encryption_used=True,
            ultrasonic_freq=request.ultrasonic_freq,
            amplitude=request.amplitude
        )


def embed_video_command(request: EmbedVideoRequest) -> EmbedResponse:
    """
    Embed an encrypted command into a video file using ultrasonic steganography.
    
    This tool takes a video file and embeds a command into its audio track using
    high-frequency ultrasonic encoding. The visual content remains unchanged while
    the audio track carries the hidden encrypted command.
    
    Args:
        request: Video embedding parameters including file path, command, and options
        
    Returns:
        EmbedResponse with details about the embedding operation
        
    Raises:
        FileNotFoundError: If the input video file doesn't exist
        ValueError: If the video format is not supported
        RuntimeError: If the embedding operation fails
    """
    _ensure_embedders()
    
    start_time = time.time()
    
    try:
        # Validate input file
        if not os.path.exists(request.video_file_path):
            raise FileNotFoundError(f"Video file not found: {request.video_file_path}")
        
        # Generate output path if not specified
        if request.output_path is None:
            base_name = os.path.splitext(request.video_file_path)[0]
            request.output_path = f"{base_name}_embedded.mp4"
        
        # Configure embedder
        _video_embedder.set_frequencies(
            request.ultrasonic_freq, 
            request.ultrasonic_freq + 1000
        )
        _video_embedder.set_amplitude(request.amplitude)
        
        # Perform embedding
        _video_embedder.embed_file(
            request.video_file_path,
            request.output_path,
            request.command,
            request.obfuscate,
            request.audio_bitrate
        )
        
        # Get file size
        file_size = os.path.getsize(request.output_path)
        processing_time = (time.time() - start_time) * 1000
        
        return EmbedResponse(
            success=True,
            output_file=request.output_path,
            embedded_command=request.command,
            file_size_bytes=file_size,
            processing_time_ms=processing_time,
            message=f"Successfully embedded command in video file: {request.output_path}",
            encryption_used=True,
            ultrasonic_freq=request.ultrasonic_freq,
            amplitude=request.amplitude
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        return EmbedResponse(
            success=False,
            output_file="",
            embedded_command=request.command,
            file_size_bytes=0,
            processing_time_ms=processing_time,
            message=f"Embedding failed: {str(e)}",
            encryption_used=True,
            ultrasonic_freq=request.ultrasonic_freq,
            amplitude=request.amplitude
        )