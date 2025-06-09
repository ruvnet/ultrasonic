"""Schemas for embedding operations."""

from pydantic import BaseModel, Field
from typing import Optional


class EmbedAudioRequest(BaseModel):
    """Request schema for audio embedding."""
    audio_file_path: str = Field(description="Path to the input audio file")
    command: str = Field(description="Command to embed in the audio") 
    output_path: Optional[str] = Field(None, description="Output file path (auto-generated if not specified)")
    obfuscate: bool = Field(True, description="Apply obfuscation to the embedded data")
    bitrate: str = Field("192k", description="Audio bitrate for output")
    ultrasonic_freq: float = Field(18500, description="Ultrasonic carrier frequency")
    amplitude: float = Field(0.1, description="Signal amplitude")


class EmbedVideoRequest(BaseModel):
    """Request schema for video embedding."""
    video_file_path: str = Field(description="Path to the input video file")
    command: str = Field(description="Command to embed in the video")
    output_path: Optional[str] = Field(None, description="Output file path (auto-generated if not specified)")
    obfuscate: bool = Field(True, description="Apply obfuscation to the embedded data")
    audio_bitrate: str = Field("192k", description="Audio bitrate for output")
    ultrasonic_freq: float = Field(18500, description="Ultrasonic carrier frequency")
    amplitude: float = Field(0.1, description="Signal amplitude")


class EmbedResponse(BaseModel):
    """Response schema for embedding operations."""
    success: bool = Field(description="Whether the operation was successful")
    output_file: str = Field(description="Path to the output file")
    embedded_command: str = Field(description="The command that was embedded")
    file_size_bytes: int = Field(description="Size of the output file in bytes")
    processing_time_ms: float = Field(description="Processing time in milliseconds")
    message: str = Field(description="Status message")
    encryption_used: bool = Field(description="Whether encryption was applied")
    ultrasonic_freq: float = Field(description="Ultrasonic frequency used")
    amplitude: float = Field(description="Signal amplitude used")