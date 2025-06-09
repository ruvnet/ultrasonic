# MCP Integration Guide

The Agentic Commands Steganography framework provides a Model Context Protocol (MCP) server for seamless integration with AI assistants like Claude, ChatGPT, and other compatible systems.

## Table of Contents

1. [MCP Overview](#mcp-overview)
2. [Installation & Setup](#installation--setup)
3. [Server Configuration](#server-configuration)
4. [MCP Tools Reference](#mcp-tools-reference)
5. [Integration Examples](#integration-examples)
6. [Claude Code Integration](#claude-code-integration)
7. [Troubleshooting](#troubleshooting)

## MCP Overview

### What is MCP?

The Model Context Protocol (MCP) enables AI assistants to interact with external tools and services. This steganography framework provides an MCP server that allows AI assistants to:

- Embed encrypted commands into audio and video files
- Decode commands from media files  
- Analyze media for steganographic content
- Configure system parameters
- Manage encryption keys

### Architecture

```
AI Assistant (Claude)
        ↓
    MCP Client
        ↓
MCP Server (agentic-stego)
        ↓
Steganography Framework
        ↓
    Media Files
```

## Installation & Setup

### Prerequisites

```bash
# Ensure Python 3.8+ is installed
python --version

# Install the framework
pip install agentic-commands-stego

# Install MCP server dependencies
pip install mcp fastapi uvicorn
```

### Quick Setup

1. **Start the MCP Server:**
```bash
agentic-stego server --host 0.0.0.0 --port 3000
```

2. **Configure AI Assistant:**
   - Add the MCP server to your AI assistant's configuration
   - Server URL: `http://localhost:3000`
   - Protocol: MCP v1.0

## Server Configuration

### Basic Configuration

```bash
# Start with default settings
agentic-stego server

# Custom host and port
agentic-stego server --host 127.0.0.1 --port 3000

# Enable debug logging
agentic-stego server --log-level DEBUG
```

### Configuration File

Create `mcp-server-config.json`:

```json
{
    "server": {
        "host": "0.0.0.0",
        "port": 3000,
        "log_level": "INFO",
        "cors_enabled": true,
        "allowed_origins": ["*"]
    },
    "steganography": {
        "default_frequency": 19000,
        "default_amplitude": 0.1,
        "max_file_size_mb": 100,
        "allowed_formats": ["wav", "mp3", "mp4", "avi"]
    },
    "security": {
        "encryption_required": true,
        "key_rotation_hours": 24,
        "max_command_length": 256
    }
}
```

### Environment Variables

```bash
# Server settings
export MCP_HOST=0.0.0.0
export MCP_PORT=3000
export MCP_LOG_LEVEL=INFO

# Security settings
export STEGO_ENCRYPTION_KEY="your-base64-encoded-key"
export STEGO_MAX_FILE_SIZE=104857600  # 100MB in bytes

# Feature flags
export STEGO_ENABLE_VIDEO=true
export STEGO_ENABLE_ANALYSIS=true
```

## MCP Tools Reference

The MCP server exposes several tools that AI assistants can use:

### 1. `embed_audio_command`

Embed an encrypted command into an audio file.

**Schema:**
```json
{
    "name": "embed_audio_command",
    "description": "Embed an encrypted command into an audio file using ultrasonic steganography",
    "inputSchema": {
        "type": "object",
        "properties": {
            "audio_file_path": {"type": "string"},
            "command": {"type": "string"},
            "output_path": {"type": "string", "optional": true},
            "ultrasonic_freq": {"type": "number", "default": 19000},
            "amplitude": {"type": "number", "default": 0.1},
            "obfuscate": {"type": "boolean", "default": true},
            "bitrate": {"type": "string", "default": "192k"}
        },
        "required": ["audio_file_path", "command"]
    }
}
```

**Example Usage:**
```json
{
    "tool": "embed_audio_command",
    "arguments": {
        "audio_file_path": "/path/to/input.wav",
        "command": "execute:backup_database",
        "output_path": "/path/to/encoded.wav",
        "ultrasonic_freq": 19500,
        "amplitude": 0.15
    }
}
```

### 2. `embed_video_command`

Embed an encrypted command into a video file's audio track.

**Schema:**
```json
{
    "name": "embed_video_command",
    "description": "Embed an encrypted command into a video file's audio track",
    "inputSchema": {
        "type": "object",
        "properties": {
            "video_file_path": {"type": "string"},
            "command": {"type": "string"},
            "output_path": {"type": "string", "optional": true},
            "ultrasonic_freq": {"type": "number", "default": 19000},
            "amplitude": {"type": "number", "default": 0.1},
            "obfuscate": {"type": "boolean", "default": true},
            "audio_bitrate": {"type": "string", "default": "192k"}
        },
        "required": ["video_file_path", "command"]
    }
}
```

### 3. `decode_audio_command`

Decode an encrypted command from an audio file.

**Schema:**
```json
{
    "name": "decode_audio_command",
    "description": "Decode an encrypted command from an audio file",
    "inputSchema": {
        "type": "object",
        "properties": {
            "file_path": {"type": "string"},
            "detailed_analysis": {"type": "boolean", "default": false}
        },
        "required": ["file_path"]
    }
}
```

### 4. `decode_video_command`

Decode an encrypted command from a video file's audio track.

**Schema:**
```json
{
    "name": "decode_video_command",
    "description": "Decode an encrypted command from a video file's audio track",
    "inputSchema": {
        "type": "object",
        "properties": {
            "file_path": {"type": "string"},
            "detailed_analysis": {"type": "boolean", "default": false}
        },
        "required": ["file_path"]
    }
}
```

### 5. `analyze_media_file`

Analyze a media file for steganographic content.

**Schema:**
```json
{
    "name": "analyze_media_file",
    "description": "Analyze a media file for steganographic content without decoding",
    "inputSchema": {
        "type": "object",
        "properties": {
            "file_path": {"type": "string"},
            "detailed_analysis": {"type": "boolean", "default": true}
        },
        "required": ["file_path"]
    }
}
```

### 6. `configure_frequencies`

Configure the ultrasonic frequencies used for encoding.

**Schema:**
```json
{
    "name": "configure_frequencies",
    "description": "Configure the ultrasonic frequencies for FSK modulation",
    "inputSchema": {
        "type": "object",
        "properties": {
            "freq_0": {"type": "number"},
            "freq_1": {"type": "number"}
        },
        "required": ["freq_0", "freq_1"]
    }
}
```

### 7. `configure_encryption_key`

Configure the encryption key for securing commands.

**Schema:**
```json
{
    "name": "configure_encryption_key",
    "description": "Configure the encryption key for command security",
    "inputSchema": {
        "type": "object",
        "properties": {
            "key_base64": {"type": "string", "optional": true},
            "key_file_path": {"type": "string", "optional": true},
            "generate_new": {"type": "boolean", "default": false}
        }
    }
}
```

## Integration Examples

### Basic Embedding with Claude

**User Prompt:**
```
Please embed the command "execute:daily_backup" into the audio file "morning_briefing.wav" using ultrasonic steganography at 19.5 kHz frequency.
```

**Claude's MCP Tool Call:**
```json
{
    "tool": "embed_audio_command",
    "arguments": {
        "audio_file_path": "morning_briefing.wav",
        "command": "execute:daily_backup",
        "ultrasonic_freq": 19500,
        "amplitude": 0.1,
        "output_path": "encoded_morning_briefing.wav"
    }
}
```

**Response:**
```json
{
    "success": true,
    "message": "Command successfully embedded",
    "output_file": "encoded_morning_briefing.wav",
    "file_size_bytes": 2456789,
    "processing_time_ms": 234.5,
    "ultrasonic_freq": 19500,
    "amplitude": 0.1
}
```

### Batch Processing Multiple Files

**User Prompt:**
```
I have a list of audio files that need steganographic analysis. Can you check each one and report if they contain hidden commands?
```

**Claude's Response:**
Claude would iterate through each file using the `analyze_media_file` tool:

```json
{
    "tool": "analyze_media_file",
    "arguments": {
        "file_path": "file1.wav",
        "detailed_analysis": true
    }
}
```

### Video Processing

**User Prompt:**
```
Embed a stealth mode activation command into this presentation video, but make sure it's completely inaudible.
```

**Claude's MCP Tool Call:**
```json
{
    "tool": "embed_video_command",
    "arguments": {
        "video_file_path": "presentation.mp4",
        "command": "configure:stealth_mode=enabled",
        "ultrasonic_freq": 20000,
        "amplitude": 0.05,
        "output_path": "steganized_presentation.mp4"
    }
}
```

## Claude Code Integration

### Setup for Claude Code

1. **Start MCP Server:**
```bash
agentic-stego server --host localhost --port 3000
```

2. **Configure Claude Code:**
Add to your Claude Code configuration:
```json
{
    "mcp": {
        "servers": {
            "steganography": {
                "command": "agentic-stego",
                "args": ["server", "--port", "3000"],
                "env": {
                    "STEGO_ENCRYPTION_KEY": "your-key-here"
                }
            }
        }
    }
}
```

### Example Claude Code Workflows

#### Workflow 1: Secure Command Distribution

```typescript
// Claude Code workflow for secure command distribution
export async function distributeCommands(
    audioFiles: string[],
    commands: string[]
) {
    const results = [];
    
    for (let i = 0; i < audioFiles.length; i++) {
        const result = await mcp.callTool('embed_audio_command', {
            audio_file_path: audioFiles[i],
            command: commands[i],
            ultrasonic_freq: 19000 + (i * 100), // Vary frequency
            amplitude: 0.1
        });
        results.push(result);
    }
    
    return results;
}
```

#### Workflow 2: Media Surveillance

```typescript
// Monitor directory for new media files and analyze them
export async function monitorMediaFiles(directory: string) {
    const files = await fs.readdir(directory);
    const mediaFiles = files.filter(file => 
        /\.(wav|mp3|mp4|avi)$/i.test(file)
    );
    
    const analysisResults = [];
    
    for (const file of mediaFiles) {
        const result = await mcp.callTool('analyze_media_file', {
            file_path: path.join(directory, file),
            detailed_analysis: true
        });
        
        if (result.encryption_detected) {
            console.log(`Steganographic content detected in: ${file}`);
            analysisResults.push({
                file,
                detected: true,
                confidence: result.confidence_score
            });
        }
    }
    
    return analysisResults;
}
```

### Error Handling

```typescript
export async function safeEmbedCommand(
    filePath: string,
    command: string
) {
    try {
        const result = await mcp.callTool('embed_audio_command', {
            audio_file_path: filePath,
            command: command
        });
        
        if (!result.success) {
            throw new Error(`Embedding failed: ${result.message}`);
        }
        
        return result;
    } catch (error) {
        console.error('MCP tool call failed:', error);
        // Fallback to CLI if MCP fails
        return await fallbackToCLI(filePath, command);
    }
}

async function fallbackToCLI(filePath: string, command: string) {
    const { exec } = require('child_process');
    return new Promise((resolve, reject) => {
        exec(`agentic-stego embed "${filePath}" "${command}"`, 
            (error, stdout, stderr) => {
                if (error) reject(error);
                else resolve({ success: true, output: stdout });
            }
        );
    });
}
```

## Troubleshooting

### Common Issues

#### MCP Server Won't Start

```bash
# Check if port is in use
netstat -an | grep 3000

# Try different port
agentic-stego server --port 3001

# Check logs
agentic-stego server --log-level DEBUG
```

#### Connection Refused

```bash
# Verify server is running
curl http://localhost:3000/health

# Check firewall settings
sudo ufw status

# Test with telnet
telnet localhost 3000
```

#### Tool Call Failures

```json
// Common error response
{
    "error": {
        "code": "TOOL_EXECUTION_FAILED",
        "message": "File not found: input.wav",
        "details": {
            "tool": "embed_audio_command",
            "file_path": "input.wav"
        }
    }
}
```

**Solutions:**
- Verify file paths are absolute
- Check file permissions
- Ensure file formats are supported
- Validate command length limits

#### Performance Issues

```bash
# Monitor server performance
top -p $(pgrep -f "agentic-stego server")

# Increase server resources
agentic-stego server --workers 4

# Use faster encoding parameters
# Lower amplitude and shorter bit duration
```

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
export MCP_DEBUG=true
export STEGO_DEBUG=true
agentic-stego server --log-level DEBUG
```

### Health Checks

```bash
# Basic health check
curl http://localhost:3000/health

# Detailed status
curl http://localhost:3000/status

# Tool availability
curl http://localhost:3000/tools
```

### Testing MCP Integration

```python
#!/usr/bin/env python3
"""Test script for MCP integration."""

import requests
import json

def test_mcp_server():
    base_url = "http://localhost:3000"
    
    # Test health endpoint
    response = requests.get(f"{base_url}/health")
    print(f"Health check: {response.status_code}")
    
    # Test tool availability
    response = requests.get(f"{base_url}/tools")
    tools = response.json()
    print(f"Available tools: {len(tools)}")
    
    # Test embed tool
    payload = {
        "tool": "embed_audio_command",
        "arguments": {
            "audio_file_path": "test.wav",
            "command": "test:command"
        }
    }
    
    response = requests.post(f"{base_url}/execute", json=payload)
    print(f"Tool execution: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    test_mcp_server()
```

## Best Practices

### Security

1. **Use HTTPS in production:**
```bash
agentic-stego server --ssl-cert cert.pem --ssl-key key.pem
```

2. **Restrict access:**
```bash
# Only allow specific IPs
agentic-stego server --allowed-ips 192.168.1.100,10.0.0.5
```

3. **Regular key rotation:**
```bash
# Rotate encryption keys daily
agentic-stego config --encryption --generate-key
```

### Performance

1. **Resource monitoring:**
```bash
# Monitor memory usage
ps aux | grep agentic-stego

# Check disk space
df -h
```

2. **Batch operations:**
```python
# Process multiple files efficiently
async def batch_embed(file_command_pairs):
    tasks = []
    for file_path, command in file_command_pairs:
        task = mcp.callTool('embed_audio_command', {
            'audio_file_path': file_path,
            'command': command
        })
        tasks.append(task)
    
    return await asyncio.gather(*tasks)
```

3. **Caching:**
```bash
# Enable result caching
export MCP_ENABLE_CACHE=true
export MCP_CACHE_TTL=3600  # 1 hour
```

---

*For complete documentation, see the [main documentation index](index.md).*