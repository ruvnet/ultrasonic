"""Pydantic schemas for MCP tool inputs and outputs."""

from .embed import EmbedAudioRequest, EmbedVideoRequest, EmbedResponse
from .decode import DecodeRequest, DecodeResponse
from .config import ConfigFrequenciesRequest, ConfigKeyRequest, ConfigResponse

__all__ = [
    "EmbedAudioRequest",
    "EmbedVideoRequest", 
    "EmbedResponse",
    "DecodeRequest",
    "DecodeResponse",
    "ConfigFrequenciesRequest",
    "ConfigKeyRequest",
    "ConfigResponse"
]