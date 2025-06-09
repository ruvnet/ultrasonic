"""
Command-line interface for Agentic Commands Steganography MCP server.

This module provides a CLI for starting the MCP server and managing
steganography operations from the command line.
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import track
    import click
except ImportError:
    print("Missing CLI dependencies. Install with: pip install typer rich click")
    sys.exit(1)

from .server import run_server
from .tools.embed_tools import embed_audio_command, embed_video_command
from .tools.decode_tools import decode_audio_command, decode_video_command, analyze_media_file
from .tools.config_tools import configure_frequencies, configure_encryption_key, get_current_config
from .schemas.embed import EmbedAudioRequest, EmbedVideoRequest
from .schemas.decode import DecodeRequest
from .schemas.config import ConfigFrequenciesRequest, ConfigKeyRequest


# Initialize Typer app and Rich console
app = typer.Typer(
    name="agentic-stego",
    help="Agentic Commands Steganography - Embed and decode commands in media files",
    add_completion=False,
    no_args_is_help=True
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print("🎵 Agentic Commands Steganography v1.0.0")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", callback=version_callback, help="Show version and exit")
):
    """
    🎵 Agentic Commands Steganography
    
    Embed and decode encrypted commands in audio and video files using 
    ultrasonic steganography. Commands are embedded using inaudible 
    high-frequency FSK modulation with AES-256-GCM encryption.
    
    Available commands:
    • server    - Start the MCP server
    • embed     - Embed a command into a media file
    • decode    - Decode a command from a media file
    • analyze   - Analyze a media file for steganographic content
    • config    - Configure system settings
    • info      - Show system information
    """
    pass


@app.command("server")
def start_server(
    log_level: str = typer.Option("INFO", "--log-level", "-l", help="Logging level")
):
    """Start the MCP server (uses stdio transport)."""
    console.print(Panel.fit(
        f"🚀 Starting Agentic Commands Steganography MCP Server\n"
        f"Transport: stdio\n"
        f"Log Level: {log_level}\n\n"
        f"This server uses stdio transport for MCP communication.\n"
        f"Connect your MCP client to this server's stdin/stdout.",
        title="MCP Server Startup",
        border_style="green"
    ))
    
    # Configure logging
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    
    try:
        run_server()
    except KeyboardInterrupt:
        console.print("\n[yellow]MCP server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Server error: {str(e)}[/red]")
        sys.exit(1)


@app.command("embed")
def embed_command(
    file_path: str = typer.Argument(..., help="Input media file path"),
    command: str = typer.Argument(..., help="Command to embed"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    freq: float = typer.Option(18500.0, "--frequency", "-f", help="Ultrasonic frequency (Hz)"),
    amplitude: float = typer.Option(0.1, "--amplitude", "-a", help="Signal amplitude (0.0-1.0)"),
    obfuscate: bool = typer.Option(True, "--obfuscate/--no-obfuscate", help="Obfuscate command"),
    bitrate: str = typer.Option("192k", "--bitrate", "-b", help="Audio bitrate")
):
    """Embed a command into a media file."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        sys.exit(1)
    
    console.print(f"[blue]Embedding command into {file_path.name}...[/blue]")
    
    try:
        # Determine file type
        if file_path.suffix.lower() in ['.mp3', '.wav', '.flac', '.ogg', '.m4a']:
            request = EmbedAudioRequest(
                audio_file_path=str(file_path),
                command=command,
                output_path=output,
                ultrasonic_freq=freq,
                amplitude=amplitude,
                obfuscate=obfuscate,
                bitrate=bitrate
            )
            result = embed_audio_command(request)
        elif file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
            request = EmbedVideoRequest(
                video_file_path=str(file_path),
                command=command,
                output_path=output,
                ultrasonic_freq=freq,
                amplitude=amplitude,
                obfuscate=obfuscate,
                audio_bitrate=bitrate
            )
            result = embed_video_command(request)
        else:
            console.print(f"[red]Error: Unsupported file format: {file_path.suffix}[/red]")
            sys.exit(1)
        
        if result.success:
            console.print(Panel.fit(
                f"✅ Command embedded successfully!\n"
                f"Output file: {result.output_file}\n"
                f"File size: {result.file_size_bytes:,} bytes\n"
                f"Processing time: {result.processing_time_ms:.1f} ms\n"
                f"Frequency: {result.ultrasonic_freq} Hz\n"
                f"Amplitude: {result.amplitude}",
                title="Embedding Complete",
                border_style="green"
            ))
        else:
            console.print(f"[red]Embedding failed: {result.message}[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@app.command("decode")
def decode_command(
    file_path: str = typer.Argument(..., help="Media file path to decode"),
    analysis: bool = typer.Option(False, "--analysis", "-a", help="Perform detailed analysis"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Decode a command from a media file."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        sys.exit(1)
    
    console.print(f"[blue]Decoding command from {file_path.name}...[/blue]")
    
    try:
        request = DecodeRequest(
            file_path=str(file_path),
            detailed_analysis=analysis
        )
        
        # Determine file type and decode
        if file_path.suffix.lower() in ['.mp3', '.wav', '.flac', '.ogg', '.m4a']:
            result = decode_audio_command(request)
        elif file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
            result = decode_video_command(request)
        else:
            console.print(f"[red]Error: Unsupported file format: {file_path.suffix}[/red]")
            sys.exit(1)
        
        if result.success and result.command:
            console.print(Panel.fit(
                f"✅ Command decoded successfully!\n"
                f"Command: {result.command}\n"
                f"Processing time: {result.processing_time_ms:.1f} ms\n"
                f"Confidence: {result.confidence_score:.2f}" if result.confidence_score else "",
                title="Decoding Complete",
                border_style="green"
            ))
            
            if verbose and result.analysis:
                console.print("\n[bold]Detailed Analysis:[/bold]")
                console.print(result.analysis)
                
        else:
            console.print(Panel.fit(
                f"❌ No command found\n"
                f"Message: {result.message}\n"
                f"Processing time: {result.processing_time_ms:.1f} ms",
                title="Decoding Result",
                border_style="red"
            ))
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@app.command("analyze")
def analyze_command(
    file_path: str = typer.Argument(..., help="Media file path to analyze")
):
    """Analyze a media file for steganographic content."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        sys.exit(1)
    
    console.print(f"[blue]Analyzing {file_path.name} for steganographic content...[/blue]")
    
    try:
        request = DecodeRequest(
            file_path=str(file_path),
            detailed_analysis=True
        )
        
        result = analyze_media_file(request)
        
        if result.success:
            has_content = result.encryption_detected
            
            table = Table(title="Media Analysis Results")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="magenta")
            
            table.add_row("File", str(file_path))
            table.add_row("Processing Time", f"{result.processing_time_ms:.1f} ms")
            table.add_row("Steganographic Content", "✅ Detected" if has_content else "❌ Not Detected")
            table.add_row("Confidence Score", f"{result.confidence_score:.2f}" if result.confidence_score else "N/A")
            
            if result.detected_frequencies:
                table.add_row("Detected Frequencies", str(result.detected_frequencies))
            
            console.print(table)
            
            if result.analysis:
                console.print(f"\n[bold]Detailed Analysis:[/bold]")
                console.print(result.analysis)
                
        else:
            console.print(f"[red]Analysis failed: {result.message}[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@app.command("config")
def config_command(
    frequencies: bool = typer.Option(False, "--frequencies", "-f", help="Configure frequencies"),
    freq_0: Optional[float] = typer.Option(None, "--freq-0", help="Frequency for binary '0' (Hz)"),
    freq_1: Optional[float] = typer.Option(None, "--freq-1", help="Frequency for binary '1' (Hz)"),
    encryption: bool = typer.Option(False, "--encryption", "-e", help="Configure encryption"),
    key_file: Optional[str] = typer.Option(None, "--key-file", help="Path to encryption key file"),
    key_base64: Optional[str] = typer.Option(None, "--key-base64", help="Base64-encoded encryption key"),
    generate_key: bool = typer.Option(False, "--generate-key", help="Generate new encryption key"),
    show: bool = typer.Option(False, "--show", "-s", help="Show current configuration")
):
    """Configure system settings."""
    
    if show:
        config = get_current_config()
        
        table = Table(title="System Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Frequency 0", f"{config['frequencies']['freq_0']} Hz")
        table.add_row("Frequency 1", f"{config['frequencies']['freq_1']} Hz")
        table.add_row("Frequency Separation", f"{config['frequencies']['separation_hz']} Hz")
        table.add_row("Encryption Configured", "✅ Yes" if config['encryption']['key_set'] else "❌ No")
        table.add_row("Encryption Algorithm", config['encryption']['algorithm'])
        table.add_row("Signal Amplitude", str(config['signal']['amplitude']))
        table.add_row("Bit Duration", f"{config['signal']['bit_duration']} s")
        table.add_row("Sample Rate", f"{config['signal']['sample_rate']} Hz")
        
        console.print(table)
        return
    
    if frequencies:
        if freq_0 is None or freq_1 is None:
            console.print("[red]Error: Both --freq-0 and --freq-1 are required[/red]")
            sys.exit(1)
        
        try:
            request = ConfigFrequenciesRequest(freq_0=freq_0, freq_1=freq_1)
            result = configure_frequencies(request)
            
            if result.success:
                console.print(f"[green]✅ {result.message}[/green]")
            else:
                console.print(f"[red]❌ {result.message}[/red]")
                sys.exit(1)
                
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)
    
    if encryption:
        try:
            request = ConfigKeyRequest(
                key_base64=key_base64,
                key_file_path=key_file,
                generate_new=generate_key
            )
            result = configure_encryption_key(request)
            
            if result.success:
                console.print(f"[green]✅ {result.message}[/green]")
            else:
                console.print(f"[red]❌ {result.message}[/red]")
                sys.exit(1)
                
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)
    
    if not (frequencies or encryption or show):
        console.print("[yellow]No configuration action specified. Use --help for options.[/yellow]")


@app.command("info")
def info_command():
    """Show information about the steganography system."""
    info_panel = Panel.fit(
        "🎵 Agentic Commands Steganography System\n\n"
        "This system uses ultrasonic frequency-shift keying (FSK) to embed\n"
        "encrypted commands into audio and video files. The commands are\n"
        "inaudible to humans but can be decoded by compatible systems.\n\n"
        "Supported formats:\n"
        "  Audio: MP3, WAV, FLAC, OGG, M4A\n"
        "  Video: MP4, AVI, MOV, MKV\n\n"
        "Security features:\n"
        "  • AES-256-GCM encryption\n"
        "  • Command obfuscation\n"
        "  • Ultrasonic frequency range (>17kHz)\n"
        "  • FSK modulation for reliability",
        title="System Information",
        border_style="blue"
    )
    console.print(info_panel)


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()