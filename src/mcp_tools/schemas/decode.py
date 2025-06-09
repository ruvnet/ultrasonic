"""Schemas for decoding operations."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class DecodeRequest(BaseModel):
    """Request schema for decoding operations."""
    file_path: str = Field(description="Path to the media file to decode")
    detailed_analysis: bool = Field(False, description="Include detailed signal analysis")


class DecodeResponse(BaseModel):
    """Response schema for decoding operations."""
    success: bool = Field(description="Whether decoding was successful")
    command: Optional[str] = Field(None, description="The decoded command (if successful)")
    file_path: str = Field(description="Path to the analyzed file")
    processing_time_ms: float = Field(description="Processing time in milliseconds")
    message: str = Field(description="Status message")
    analysis: Optional[Dict[str, Any]] = Field(None, description="Detailed signal analysis (if requested)")
    confidence_score: Optional[float] = Field(None, description="Confidence in the decoded result (0-1)")
    detected_frequencies: Optional[Dict[str, float]] = Field(None, description="Detected ultrasonic frequencies")
    encryption_detected: Optional[bool] = Field(None, description="Whether encryption was detected")