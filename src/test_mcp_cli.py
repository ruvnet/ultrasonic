#!/usr/bin/env python3
"""
Simple CLI test for MCP server functionality.

Tests the MCP server through the CLI interface.
"""

import subprocess
import sys
import json
import tempfile
import os
from pathlib import Path

def run_command(cmd):
    """Run a command and return output."""
    print(f"🏃 Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ Success")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed with exit code {e.returncode}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return None

def test_cli():
    """Test MCP server through CLI."""
    print("🧪 Testing MCP Server CLI Integration")
    print("="*60)
    
    # Get the CLI path
    cli_path = Path(__file__).parent / "mcp_tools" / "cli.py"
    
    # Test 1: Show version
    print("\n📋 Test 1: CLI Version")
    run_command([sys.executable, str(cli_path), "--version"])
    
    # Test 2: Show help
    print("\n📋 Test 2: CLI Help")
    run_command([sys.executable, str(cli_path), "--help"])
    
    # Test 3: Show info
    print("\n📋 Test 3: System Info")
    run_command([sys.executable, str(cli_path), "info"])
    
    # Test 4: Show configuration
    print("\n📋 Test 4: Show Configuration")
    run_command([sys.executable, str(cli_path), "config", "--show"])
    
    # Test 5: Create test audio file and embed command
    print("\n📋 Test 5: Embed Command")
    
    # Create a simple WAV file
    import numpy as np
    from scipy.io import wavfile
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
        
    sample_rate = 44100
    duration = 2  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
    
    wavfile.write(tmp_path, sample_rate, audio_data)
    print(f"Created test audio file: {tmp_path}")
    
    # Embed command
    output_path = tmp_path.replace(".wav", "_embedded.wav")
    result = run_command([
        sys.executable, str(cli_path), "embed",
        tmp_path,
        "test_mcp_command",
        "--output", output_path,
        "--frequency", "18500",
        "--amplitude", "0.1"
    ])
    
    # Test 6: Decode command
    if os.path.exists(output_path):
        print("\n📋 Test 6: Decode Command")
        run_command([
            sys.executable, str(cli_path), "decode",
            output_path,
            "--verbose"
        ])
        
        # Test 7: Analyze file
        print("\n📋 Test 7: Analyze Media")
        run_command([
            sys.executable, str(cli_path), "analyze",
            output_path
        ])
        
        # Clean up
        os.unlink(output_path)
    
    # Clean up
    os.unlink(tmp_path)
    
    print("\n" + "="*60)
    print("✅ CLI tests completed")

def test_mcp_protocol():
    """Test MCP protocol directly."""
    print("\n🧪 Testing MCP Protocol Compliance")
    print("="*60)
    
    # Create a simple test to verify MCP protocol
    test_script = '''
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path

async def test():
    server_path = Path(__file__).parent / "mcp_tools" / "server.py"
    
    server_params = StdioServerParameters(
        command="python",
        args=[str(server_path)],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            print("✅ MCP connection established")
            
            # List tools
            tools_response = await session.list_tools()
            print(f"✅ Found {len(tools_response.tools)} tools")
            
            for tool in tools_response.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Get config
            result = await session.call_tool(
                "get_system_config",
                arguments={}
            )
            
            if result.content:
                config = json.loads(result.content[0].text)
                print("✅ Configuration retrieved successfully")
                print(f"  - Frequencies: {config['frequencies']['freq_0']}Hz, {config['frequencies']['freq_1']}Hz")
                print(f"  - Encryption: {'Configured' if config['encryption']['key_set'] else 'Not configured'}")

asyncio.run(test())
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        test_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ MCP protocol test failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
    finally:
        os.unlink(test_file)

if __name__ == "__main__":
    print("🔧 MCP Server Integration Test")
    print("Version: 1.0.0")
    print("-"*60)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    
    try:
        import numpy
        import scipy
        print("  ✓ NumPy and SciPy found")
    except ImportError:
        print("  ✗ NumPy/SciPy not found. Install with: pip install numpy scipy")
        sys.exit(1)
        
    try:
        import mcp
        print("  ✓ MCP library found")
    except ImportError:
        print("  ✗ MCP library not found. Install with: pip install mcp")
        print("  ℹ️  CLI tests will still run")
    
    # Run CLI tests
    test_cli()
    
    # Run MCP protocol tests if available
    try:
        import mcp
        test_mcp_protocol()
    except ImportError:
        print("\n⚠️  Skipping MCP protocol tests (mcp library not available)")