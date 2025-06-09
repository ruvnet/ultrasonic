"""MCP tools for decoding commands from media files."""

import os
import time
from typing import Optional, Dict, Any
from ..schemas.decode import DecodeRequest, DecodeResponse
from agentic_commands_stego.decode.audio_decoder import AudioDecoder
from agentic_commands_stego.decode.video_decoder import VideoDecoder
from agentic_commands_stego.crypto.cipher import CipherService


# Global decoders (will be configured via MCP server)
_audio_decoder: Optional[AudioDecoder] = None
_video_decoder: Optional[VideoDecoder] = None
_cipher_key: Optional[bytes] = None


def _ensure_decoders():
    """Ensure decoders are initialized."""
    global _audio_decoder, _video_decoder, _cipher_key
    
    if _cipher_key is None:
        _cipher_key = CipherService.generate_key(32)
    
    if _audio_decoder is None:
        _audio_decoder = AudioDecoder(key=_cipher_key)
    
    if _video_decoder is None:
        _video_decoder = VideoDecoder(key=_cipher_key)


def set_cipher_key(key: bytes):
    """Set the encryption key for decoders."""
    global _audio_decoder, _video_decoder, _cipher_key
    
    _cipher_key = key
    
    # Recreate decoders with new key
    _audio_decoder = AudioDecoder(key=_cipher_key)
    _video_decoder = VideoDecoder(key=_cipher_key)


def decode_audio_command(request: DecodeRequest) -> DecodeResponse:
    """
    Decode an encrypted command from an audio file using ultrasonic steganography.
    
    This tool analyzes an audio file to detect and decode hidden commands that were
    embedded using ultrasonic frequencies. It automatically detects the presence of
    steganographic content and attempts to decrypt any found commands.
    
    Args:
        request: Decoding parameters including file path and analysis options
        
    Returns:
        DecodeResponse with the decoded command and analysis details
        
    Raises:
        FileNotFoundError: If the input audio file doesn't exist
        ValueError: If the audio format is not supported
    """
    _ensure_decoders()
    
    start_time = time.time()
    
    try:
        # Validate input file
        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"Audio file not found: {request.file_path}")
        
        # Check file extension
        if not request.file_path.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a')):
            raise ValueError(f"Unsupported audio format: {request.file_path}")
        
        # Perform decoding
        command = _audio_decoder.decode_file(request.file_path)
        
        # Get analysis if requested
        analysis = None
        confidence_score = None
        detected_frequencies = None
        
        if request.detailed_analysis:
            analysis = _audio_decoder.analyze_audio(request.file_path)
            # Extract confidence and frequency info from analysis
            if analysis:
                confidence_score = analysis.get('confidence', None)
                detected_frequencies = analysis.get('detected_frequencies', None)
        
        processing_time = (time.time() - start_time) * 1000
        
        if command:
            return DecodeResponse(
                success=True,
                command=command,
                file_path=request.file_path,
                processing_time_ms=processing_time,
                message=f"Successfully decoded command from audio file",
                analysis=analysis,
                confidence_score=confidence_score,
                detected_frequencies=detected_frequencies,
                encryption_detected=True
            )
        else:
            return DecodeResponse(
                success=False,
                command=None,
                file_path=request.file_path,
                processing_time_ms=processing_time,
                message="No hidden command detected in audio file",
                analysis=analysis,
                confidence_score=0.0,
                detected_frequencies=detected_frequencies,
                encryption_detected=False
            )
            
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        return DecodeResponse(
            success=False,
            command=None,
            file_path=request.file_path,
            processing_time_ms=processing_time,
            message=f"Decoding failed: {str(e)}",
            analysis=None,
            confidence_score=None,
            detected_frequencies=None,
            encryption_detected=None
        )


def decode_video_command(request: DecodeRequest) -> DecodeResponse:
    """
    Decode an encrypted command from a video file using ultrasonic steganography.
    
    This tool analyzes the audio track of a video file to detect and decode hidden
    commands that were embedded using ultrasonic frequencies. The visual content
    is ignored while the audio track is processed for steganographic content.
    
    Args:
        request: Decoding parameters including file path and analysis options
        
    Returns:
        DecodeResponse with the decoded command and analysis details
        
    Raises:
        FileNotFoundError: If the input video file doesn't exist
        ValueError: If the video format is not supported
    """
    _ensure_decoders()
    
    start_time = time.time()
    
    try:
        # Validate input file
        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"Video file not found: {request.file_path}")
        
        # Check file extension
        if not request.file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            raise ValueError(f"Unsupported video format: {request.file_path}")
        
        # Perform decoding
        command = _video_decoder.decode_file(request.file_path)
        
        # Get analysis if requested
        analysis = None
        confidence_score = None
        detected_frequencies = None
        
        if request.detailed_analysis:
            analysis = _video_decoder.analyze_video(request.file_path)
            # Extract confidence and frequency info from analysis
            if analysis:
                confidence_score = analysis.get('confidence', None)
                detected_frequencies = analysis.get('detected_frequencies', None)
        
        processing_time = (time.time() - start_time) * 1000
        
        if command:
            return DecodeResponse(
                success=True,
                command=command,
                file_path=request.file_path,
                processing_time_ms=processing_time,
                message=f"Successfully decoded command from video file",
                analysis=analysis,
                confidence_score=confidence_score,
                detected_frequencies=detected_frequencies,
                encryption_detected=True
            )
        else:
            return DecodeResponse(
                success=False,
                command=None,
                file_path=request.file_path,
                processing_time_ms=processing_time,
                message="No hidden command detected in video file",
                analysis=analysis,
                confidence_score=0.0,
                detected_frequencies=detected_frequencies,
                encryption_detected=False
            )
            
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        return DecodeResponse(
            success=False,
            command=None,
            file_path=request.file_path,
            processing_time_ms=processing_time,
            message=f"Decoding failed: {str(e)}",
            analysis=None,
            confidence_score=None,
            detected_frequencies=None,
            encryption_detected=None
        )


def analyze_media_file(request: DecodeRequest) -> DecodeResponse:
    """
    Analyze a media file for steganographic content without attempting to decode.
    
    This tool performs detailed analysis of audio or video files to detect the
    presence of ultrasonic steganographic signals without attempting to decrypt
    them. Useful for forensic analysis or content verification.
    
    Args:
        request: Analysis parameters including file path
        
    Returns:
        DecodeResponse with detailed analysis but no decoded command
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file format is not supported
    """
    _ensure_decoders()
    
    start_time = time.time()
    
    try:
        # Validate input file
        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"Media file not found: {request.file_path}")
        
        # Determine file type and perform analysis
        file_ext = request.file_path.lower()
        analysis = None
        
        if file_ext.endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a')):
            analysis = _audio_decoder.analyze_audio(request.file_path)
        elif file_ext.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            analysis = _video_decoder.analyze_video(request.file_path)
        else:
            raise ValueError(f"Unsupported media format: {request.file_path}")
        
        processing_time = (time.time() - start_time) * 1000
        
        # Extract analysis details
        confidence_score = analysis.get('confidence', 0.0) if analysis else 0.0
        detected_frequencies = analysis.get('detected_frequencies', None) if analysis else None
        has_steganographic_content = confidence_score > 0.1
        
        return DecodeResponse(
            success=True,
            command=None,  # Analysis only, no decoding
            file_path=request.file_path,
            processing_time_ms=processing_time,
            message=f"Media analysis complete. Steganographic content {'detected' if has_steganographic_content else 'not detected'}",
            analysis=analysis,
            confidence_score=confidence_score,
            detected_frequencies=detected_frequencies,
            encryption_detected=has_steganographic_content
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        return DecodeResponse(
            success=False,
            command=None,
            file_path=request.file_path,
            processing_time_ms=processing_time,
            message=f"Analysis failed: {str(e)}",
            analysis=None,
            confidence_score=None,
            detected_frequencies=None,
            encryption_detected=None
        )