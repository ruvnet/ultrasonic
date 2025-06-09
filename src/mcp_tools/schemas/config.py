"""Schemas for configuration operations."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ConfigFrequenciesRequest(BaseModel):
    """Request schema for frequency configuration."""
    freq_0: float = Field(description="Frequency for bit '0' in Hz")
    freq_1: float = Field(description="Frequency for bit '1' in Hz")


class ConfigKeyRequest(BaseModel):
    """Request schema for encryption key configuration."""
    key_base64: Optional[str] = Field(None, description="Base64 encoded encryption key")
    key_file_path: Optional[str] = Field(None, description="Path to file containing encryption key")
    generate_new: bool = Field(False, description="Generate a new random key")


class ConfigResponse(BaseModel):
    """Response schema for configuration operations."""
    success: bool = Field(description="Whether the configuration was successful")
    message: str = Field(description="Status message")
    applied_config: Dict[str, Any] = Field(description="Configuration that was applied")
    previous_config: Optional[Dict[str, Any]] = Field(None, description="Previous configuration values")