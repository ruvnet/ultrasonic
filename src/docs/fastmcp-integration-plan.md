# FastMCP Integration Plan for Agentic Commands Steganography

## Executive Summary

This document outlines the detailed implementation plan for integrating FastMCP with the agentic_commands_stego project to create a comprehensive CLI API that exposes steganography capabilities as MCP tools for AI assistants.

## Current State Analysis

### Existing Architecture
- **Core Modules**: `embed/`, `decode/`, `crypto/`, `server/`
- **API**: FastAPI-based REST API in `server/api.py`
- **Capabilities**: Audio/video steganography, ultrasonic encoding, AES-256-GCM encryption
- **Interface**: HTTP endpoints for embedding, decoding, and analysis

### Current API Endpoints
1. `/embed/audio` - Embed commands in audio files
2. `/embed/video` - Embed commands in video files  
3. `/decode/audio` - Decode commands from audio files
4. `/decode/video` - Decode commands from video files
5. `/analyze/audio` - Analyze audio for steganographic content
6. `/analyze/video` - Analyze video for steganographic content
7. `/config/*` - Configuration endpoints for frequencies and encryption keys

## FastMCP Integration Strategy

### 1. Architecture Design

#### MCP Server Structure
```
agentic_commands_stego/
├── mcp/
│   ├── __init__.py
│   ├── server.py           # Main FastMCP server
│   ├── tools/              # MCP tool implementations
│   │   ├── __init__.py
│   │   ├── embed_tools.py  # Embedding tools
│   │   ├── decode_tools.py # Decoding tools
│   │   ├── analyze_tools.py # Analysis tools
│   │   └── config_tools.py # Configuration tools
│   ├── schemas/            # Pydantic models for MCP
│   │   ├── __init__.py
│   │   ├── embed.py
│   │   ├── decode.py
│   │   └── config.py
│   └── cli.py              # CLI entry point
```

#### Tool Categories
1. **Embedding Tools**
   - `embed_audio_command`
   - `embed_video_command`
   - `embed_text_in_media`

2. **Decoding Tools**  
   - `decode_audio_command`
   - `decode_video_command`
   - `extract_hidden_data`

3. **Analysis Tools**
   - `analyze_audio_steganography`
   - `analyze_video_steganography`
   - `detect_hidden_content`

4. **Configuration Tools**
   - `configure_frequencies`
   - `set_encryption_key`
   - `calibrate_system`

### 2. Implementation Phases

#### Phase 1: Core MCP Server Setup
**Duration**: 2-3 days
**Priority**: High

- Install and configure FastMCP dependency
- Create basic MCP server structure
- Implement core embedding/decoding tools
- Add Pydantic schemas for type safety
- Create CLI entry point

#### Phase 2: Tool Implementation
**Duration**: 3-4 days  
**Priority**: High

- Implement all embedding tools with proper error handling
- Implement all decoding tools with validation
- Add analysis tools for steganographic detection
- Create configuration management tools
- Add comprehensive documentation strings

#### Phase 3: CLI Integration
**Duration**: 2-3 days
**Priority**: Medium

- Create CLI wrapper using Click or Typer
- Add command-line options for all tools
- Implement file handling and batch processing
- Add progress indicators and verbose output
- Create configuration file support

#### Phase 4: Advanced Features
**Duration**: 3-4 days
**Priority**: Medium

- Add streaming support for large files
- Implement batch processing capabilities
- Add real-time audio processing tools
- Create preset configurations
- Add integration tests

#### Phase 5: Documentation & Testing
**Duration**: 2-3 days
**Priority**: Low

- Complete API documentation
- Add usage examples and tutorials
- Create integration tests
- Add performance benchmarks
- Create deployment guides

### 3. Technical Specifications

#### Dependencies
```python
# Add to requirements.txt
fastmcp>=2.0.0
click>=8.0.0
typer>=0.9.0
rich>=13.0.0  # For CLI formatting
```

#### MCP Server Configuration
```python
from fastmcp import FastMCP
from fastmcp.resources import Resource
from fastmcp.utilities.logging import get_logger

mcp = FastMCP(
    name="Agentic Commands Steganography",
    version="1.0.0",
    description="Advanced steganography tools for embedding and extracting agentic commands in multimedia files"
)

# Configure logging
logger = get_logger(__name__)
```

#### Tool Schema Example
```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class EmbedAudioRequest(BaseModel):
    """Request schema for audio embedding."""
    audio_file_path: str = Field(description="Path to the input audio file")
    command: str = Field(description="Command to embed in the audio")
    output_path: Optional[str] = Field(None, description="Output file path")
    obfuscate: bool = Field(True, description="Apply obfuscation to the embedded data")
    bitrate: str = Field("192k", description="Audio bitrate for output")
    ultrasonic_freq: float = Field(18500, description="Ultrasonic carrier frequency")
    amplitude: float = Field(0.1, description="Signal amplitude")

class EmbedAudioResponse(BaseModel):
    """Response schema for audio embedding."""
    success: bool
    output_file: str
    embedded_command: str
    file_size_bytes: int
    processing_time_ms: float
    message: str
```

#### CLI Interface Design
```bash
# Main CLI entry point
agentic-stego --help

# Embedding commands
agentic-stego embed audio input.mp3 "execute:status_check" --output embedded.mp3
agentic-stego embed video input.mp4 "run:diagnostics" --freq 19000

# Decoding commands  
agentic-stego decode audio embedded.mp3
agentic-stego decode video embedded.mp4

# Analysis commands
agentic-stego analyze audio suspicious.mp3 --detailed
agentic-stego analyze video suspicious.mp4 --export-report

# Configuration commands
agentic-stego config set-frequencies 18500 19500
agentic-stego config set-key --key-file encryption.key
agentic-stego config calibrate --auto

# MCP server commands
agentic-stego mcp run --port 8080
agentic-stego mcp inspect --debug
```

### 4. Key Implementation Details

#### Error Handling Strategy
- Comprehensive exception handling with user-friendly messages
- Validation of file formats and parameters
- Graceful degradation for missing dependencies
- Detailed logging for debugging

#### Performance Considerations
- Async processing for large files
- Memory-efficient streaming for video files
- Parallel processing for batch operations
- Caching for frequently used configurations

#### Security Features
- Secure key management with environment variables
- Input validation and sanitization
- File type verification
- Access control for sensitive operations

#### Testing Strategy
- Unit tests for all MCP tools
- Integration tests with sample media files
- Performance tests with large files
- CLI integration tests
- MCP protocol compliance tests

### 5. Integration Points

#### Existing Codebase Integration
- Maintain backward compatibility with current FastAPI server
- Reuse existing embedder/decoder classes
- Leverage current crypto implementation
- Preserve existing test suite

#### External Integrations
- Claude Desktop app integration
- VS Code extension compatibility
- Docker containerization
- CI/CD pipeline integration

### 6. Migration Strategy

#### Gradual Migration
1. Add FastMCP alongside existing FastAPI server
2. Create parallel CLI interface
3. Test MCP tools extensively
4. Gradually deprecate REST API (optional)
5. Full migration to MCP-first architecture

#### Compatibility Maintenance
- Keep existing FastAPI endpoints functional
- Provide migration tools for existing users
- Maintain API versioning
- Document migration path

### 7. Success Metrics

#### Functional Metrics
- All existing functionality available via MCP tools
- CLI commands work for all supported file formats
- Integration with Claude Desktop successful
- Performance matches or exceeds current implementation

#### Quality Metrics
- Test coverage > 90%
- Documentation completeness
- User adoption metrics
- Error rate < 1%

### 8. Risk Mitigation

#### Technical Risks
- **FastMCP compatibility issues**: Maintain fallback to REST API
- **Performance degradation**: Implement caching and optimization
- **File handling complexity**: Use robust file validation
- **Memory usage**: Implement streaming for large files

#### User Experience Risks  
- **CLI complexity**: Provide clear documentation and examples
- **Integration difficulty**: Create setup wizards and guides
- **Learning curve**: Provide migration tutorials

### 9. Future Enhancements

#### Planned Features
- Real-time streaming support
- Multi-format batch processing
- Advanced analysis algorithms
- Machine learning detection
- Cloud service integration

#### Extensibility
- Plugin architecture for custom encoders
- Template system for common operations
- API versioning for future compatibility
- Modular tool architecture

## Conclusion

This implementation plan provides a comprehensive roadmap for integrating FastMCP with the agentic_commands_stego project. The phased approach ensures minimal disruption to existing functionality while adding powerful MCP capabilities that enhance usability for AI assistants and command-line users.

The integration will transform the project from a specialized steganography library into a comprehensive, AI-friendly toolkit that can be easily integrated into various workflows and applications.