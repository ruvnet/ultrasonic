"""
MCP server for Agentic Commands Steganography.

This module provides the MCP (Model Context Protocol) server implementation
for embedding and extracting agentic commands in multimedia files.
"""

import asyncio
import logging
import json
from typing import Any, Dict, List, Optional
from pathlib import Path

from mcp.server import Server
from mcp.types import Tool, TextContent

from .tools.embed_tools import embed_audio_command, embed_video_command
from .tools.decode_tools import decode_audio_command, decode_video_command, analyze_media_file
from .tools.config_tools import configure_frequencies, configure_encryption_key, get_current_config
from .schemas.embed import EmbedAudioRequest, EmbedVideoRequest
from .schemas.decode import DecodeRequest
from .schemas.config import ConfigFrequenciesRequest, ConfigKeyRequest


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("agentic-commands-steganography")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="embed_audio",
            description="Embed an encrypted command into an audio file using ultrasonic steganography",
            inputSchema={
                "type": "object",
                "properties": {
                    "audio_file_path": {"type": "string", "description": "Path to the input audio file"},
                    "command": {"type": "string", "description": "The command to embed"},
                    "output_path": {"type": "string", "description": "Path for output file (optional)"},
                    "ultrasonic_freq": {"type": "number", "default": 18500.0, "description": "Frequency for binary '0' in Hz"},
                    "amplitude": {"type": "number", "default": 0.1, "description": "Signal amplitude 0.0-1.0"},
                    "obfuscate": {"type": "boolean", "default": True, "description": "Whether to obfuscate the command"},
                    "bitrate": {"type": "string", "default": "192k", "description": "Audio bitrate for output"}
                },
                "required": ["audio_file_path", "command"]
            }
        ),
        Tool(
            name="embed_video",
            description="Embed an encrypted command into a video file using ultrasonic steganography",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_file_path": {"type": "string", "description": "Path to the input video file"},
                    "command": {"type": "string", "description": "The command to embed"},
                    "output_path": {"type": "string", "description": "Path for output file (optional)"},
                    "ultrasonic_freq": {"type": "number", "default": 18500.0, "description": "Frequency for binary '0' in Hz"},
                    "amplitude": {"type": "number", "default": 0.1, "description": "Signal amplitude 0.0-1.0"},
                    "obfuscate": {"type": "boolean", "default": True, "description": "Whether to obfuscate the command"},
                    "audio_bitrate": {"type": "string", "default": "192k", "description": "Audio bitrate for output"}
                },
                "required": ["video_file_path", "command"]
            }
        ),
        Tool(
            name="decode_audio",
            description="Decode an encrypted command from an audio file using ultrasonic steganography",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the audio file to analyze"},
                    "detailed_analysis": {"type": "boolean", "default": False, "description": "Perform detailed signal analysis"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="decode_video",
            description="Decode an encrypted command from a video file using ultrasonic steganography",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the video file to analyze"},
                    "detailed_analysis": {"type": "boolean", "default": False, "description": "Perform detailed signal analysis"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="analyze_media",
            description="Analyze a media file for steganographic content without attempting to decode",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the media file to analyze"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="configure_system_frequencies",
            description="Configure the ultrasonic frequencies used for FSK modulation",
            inputSchema={
                "type": "object",
                "properties": {
                    "freq_0": {"type": "number", "description": "Frequency for binary '0' in Hz"},
                    "freq_1": {"type": "number", "description": "Frequency for binary '1' in Hz"}
                },
                "required": ["freq_0", "freq_1"]
            }
        ),
        Tool(
            name="configure_encryption",
            description="Configure the encryption key used for command encryption",
            inputSchema={
                "type": "object",
                "properties": {
                    "key_base64": {"type": "string", "description": "Base64-encoded encryption key (optional)"},
                    "key_file_path": {"type": "string", "description": "Path to key file (optional)"},
                    "generate_new": {"type": "boolean", "default": False, "description": "Generate new random key"}
                },
                "required": []
            }
        ),
        Tool(
            name="get_system_config",
            description="Get the current system configuration",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "embed_audio":
            return await embed_audio_tool(arguments)
        elif name == "embed_video":
            return await embed_video_tool(arguments)
        elif name == "decode_audio":
            return await decode_audio_tool(arguments)
        elif name == "decode_video":
            return await decode_video_tool(arguments)
        elif name == "analyze_media":
            return await analyze_media_tool(arguments)
        elif name == "configure_system_frequencies":
            return await configure_frequencies_tool(arguments)
        elif name == "configure_encryption":
            return await configure_encryption_tool(arguments)
        elif name == "get_system_config":
            return await get_config_tool(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Tool {name} failed: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def embed_audio_tool(arguments: Dict[str, Any]) -> list[TextContent]:
    """Embed audio tool implementation."""
    try:
        request = EmbedAudioRequest(
            audio_file_path=arguments["audio_file_path"],
            command=arguments["command"],
            output_path=arguments.get("output_path"),
            ultrasonic_freq=arguments.get("ultrasonic_freq", 18500.0),
            amplitude=arguments.get("amplitude", 0.1),
            obfuscate=arguments.get("obfuscate", True),
            bitrate=arguments.get("bitrate", "192k")
        )
        
        result = embed_audio_command(request)
        return [TextContent(type="text", text=json.dumps(result.dict(), indent=2))]
        
    except Exception as e:
        logger.error(f"Audio embedding failed: {str(e)}")
        return [TextContent(type="text", text=f"Audio embedding failed: {str(e)}")]


async def embed_video_tool(arguments: Dict[str, Any]) -> list[TextContent]:
    """Embed video tool implementation."""
    try:
        request = EmbedVideoRequest(
            video_file_path=arguments["video_file_path"],
            command=arguments["command"],
            output_path=arguments.get("output_path"),
            ultrasonic_freq=arguments.get("ultrasonic_freq", 18500.0),
            amplitude=arguments.get("amplitude", 0.1),
            obfuscate=arguments.get("obfuscate", True),
            audio_bitrate=arguments.get("audio_bitrate", "192k")
        )
        
        result = embed_video_command(request)
        return [TextContent(type="text", text=json.dumps(result.dict(), indent=2))]
        
    except Exception as e:
        logger.error(f"Video embedding failed: {str(e)}")
        return [TextContent(type="text", text=f"Video embedding failed: {str(e)}")]


async def decode_audio_tool(arguments: Dict[str, Any]) -> list[TextContent]:
    """Decode audio tool implementation."""
    try:
        request = DecodeRequest(
            file_path=arguments["file_path"],
            detailed_analysis=arguments.get("detailed_analysis", False)
        )
        
        result = decode_audio_command(request)
        return [TextContent(type="text", text=json.dumps(result.dict(), indent=2))]
        
    except Exception as e:
        logger.error(f"Audio decoding failed: {str(e)}")
        return [TextContent(type="text", text=f"Audio decoding failed: {str(e)}")]


async def decode_video_tool(arguments: Dict[str, Any]) -> list[TextContent]:
    """Decode video tool implementation."""
    try:
        request = DecodeRequest(
            file_path=arguments["file_path"],
            detailed_analysis=arguments.get("detailed_analysis", False)
        )
        
        result = decode_video_command(request)
        return [TextContent(type="text", text=json.dumps(result.dict(), indent=2))]
        
    except Exception as e:
        logger.error(f"Video decoding failed: {str(e)}")
        return [TextContent(type="text", text=f"Video decoding failed: {str(e)}")]


async def analyze_media_tool(arguments: Dict[str, Any]) -> list[TextContent]:
    """Analyze media tool implementation."""
    try:
        request = DecodeRequest(
            file_path=arguments["file_path"],
            detailed_analysis=True
        )
        
        result = analyze_media_file(request)
        return [TextContent(type="text", text=json.dumps(result.dict(), indent=2))]
        
    except Exception as e:
        logger.error(f"Media analysis failed: {str(e)}")
        return [TextContent(type="text", text=f"Media analysis failed: {str(e)}")]


async def configure_frequencies_tool(arguments: Dict[str, Any]) -> list[TextContent]:
    """Configure frequencies tool implementation."""
    try:
        request = ConfigFrequenciesRequest(
            freq_0=arguments["freq_0"],
            freq_1=arguments["freq_1"]
        )
        
        result = configure_frequencies(request)
        return [TextContent(type="text", text=json.dumps(result.dict(), indent=2))]
        
    except Exception as e:
        logger.error(f"Frequency configuration failed: {str(e)}")
        return [TextContent(type="text", text=f"Frequency configuration failed: {str(e)}")]


async def configure_encryption_tool(arguments: Dict[str, Any]) -> list[TextContent]:
    """Configure encryption tool implementation."""
    try:
        request = ConfigKeyRequest(
            key_base64=arguments.get("key_base64"),
            key_file_path=arguments.get("key_file_path"),
            generate_new=arguments.get("generate_new", False)
        )
        
        result = configure_encryption_key(request)
        return [TextContent(type="text", text=json.dumps(result.dict(), indent=2))]
        
    except Exception as e:
        logger.error(f"Encryption configuration failed: {str(e)}")
        return [TextContent(type="text", text=f"Encryption configuration failed: {str(e)}")]


async def get_config_tool(arguments: Dict[str, Any]) -> list[TextContent]:
    """Get config tool implementation."""
    try:
        config = get_current_config()
        return [TextContent(type="text", text=json.dumps(config, indent=2))]
        
    except Exception as e:
        logger.error(f"Failed to get configuration: {str(e)}")
        return [TextContent(type="text", text=f"Failed to get configuration: {str(e)}")]


def run_server():
    """Run the MCP server using stdio transport."""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Agentic Commands Steganography MCP server")
    logger.info("Available tools:")
    logger.info("  - embed_audio: Embed commands in audio files")
    logger.info("  - embed_video: Embed commands in video files")
    logger.info("  - decode_audio: Decode commands from audio files")
    logger.info("  - decode_video: Decode commands from video files")
    logger.info("  - analyze_media: Analyze files for steganographic content")
    logger.info("  - configure_system_frequencies: Set FSK frequencies")
    logger.info("  - configure_encryption: Set encryption key")
    logger.info("  - get_system_config: Get current configuration")
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    asyncio.run(main())


if __name__ == "__main__":
    run_server()