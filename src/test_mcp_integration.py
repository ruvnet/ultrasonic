#!/usr/bin/env python3
"""
Comprehensive test script for MCP server integration.

This script verifies:
1. MCP server startup and protocol compliance
2. Tool registration and discovery
3. Tool execution through MCP protocol
4. Error handling in MCP context
5. Integration with fastmcp library
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional
import tempfile
import os

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("ERROR: MCP client libraries not found. Install with: pip install mcp")
    sys.exit(1)


class MCPServerTester:
    """Test harness for MCP server integration."""
    
    def __init__(self):
        self.server_path = Path(__file__).parent / "mcp_tools" / "server.py"
        self.test_results = []
        self.client: Optional[ClientSession] = None
        
    async def start_server_and_connect(self):
        """Start the MCP server and establish connection."""
        print("🚀 Starting MCP server...")
        
        # Create server parameters
        server_params = StdioServerParameters(
            command="python",
            args=[str(self.server_path)],
            env=None
        )
        
        # Connect to the server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.client = session
                
                # Initialize the connection
                await session.initialize()
                
                # Run all tests
                await self.run_all_tests()
                
    async def run_all_tests(self):
        """Run all MCP integration tests."""
        print("\n" + "="*60)
        print("🧪 Running MCP Server Integration Tests")
        print("="*60 + "\n")
        
        # Test 1: Server startup and protocol compliance
        await self.test_server_startup()
        
        # Test 2: Tool registration and discovery
        await self.test_tool_registration()
        
        # Test 3: Tool execution - embed audio
        await self.test_embed_audio()
        
        # Test 4: Tool execution - decode audio
        await self.test_decode_audio()
        
        # Test 5: Configuration tools
        await self.test_configuration_tools()
        
        # Test 6: Error handling
        await self.test_error_handling()
        
        # Test 7: Analyze media
        await self.test_analyze_media()
        
        # Print results
        self.print_results()
        
    async def test_server_startup(self):
        """Test 1: Server startup and protocol compliance."""
        print("📋 Test 1: Server Startup and Protocol Compliance")
        
        try:
            # Check if client is connected
            if self.client is not None:
                self.test_results.append({
                    "test": "Server Startup",
                    "status": "✅ PASSED",
                    "details": "Server started successfully and MCP protocol connection established"
                })
            else:
                self.test_results.append({
                    "test": "Server Startup",
                    "status": "❌ FAILED",
                    "details": "Failed to establish MCP connection"
                })
        except Exception as e:
            self.test_results.append({
                "test": "Server Startup",
                "status": "❌ FAILED",
                "details": f"Error: {str(e)}"
            })
            
    async def test_tool_registration(self):
        """Test 2: Tool registration and discovery."""
        print("📋 Test 2: Tool Registration and Discovery")
        
        try:
            # List available tools
            tools_response = await self.client.list_tools()
            tools = tools_response.tools
            
            expected_tools = [
                "embed_audio", "embed_video", "decode_audio", "decode_video",
                "analyze_media", "configure_system_frequencies", 
                "configure_encryption", "get_system_config"
            ]
            
            registered_tools = [tool.name for tool in tools]
            
            # Check if all expected tools are registered
            missing_tools = set(expected_tools) - set(registered_tools)
            extra_tools = set(registered_tools) - set(expected_tools)
            
            if not missing_tools and not extra_tools:
                self.test_results.append({
                    "test": "Tool Registration",
                    "status": "✅ PASSED",
                    "details": f"All {len(expected_tools)} tools registered correctly"
                })
            else:
                details = []
                if missing_tools:
                    details.append(f"Missing: {missing_tools}")
                if extra_tools:
                    details.append(f"Extra: {extra_tools}")
                self.test_results.append({
                    "test": "Tool Registration",
                    "status": "❌ FAILED",
                    "details": "; ".join(details)
                })
                
            # Verify tool schemas
            for tool in tools:
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    print(f"  ✓ Tool '{tool.name}' has valid input schema")
                    
        except Exception as e:
            self.test_results.append({
                "test": "Tool Registration",
                "status": "❌ FAILED",
                "details": f"Error: {str(e)}"
            })
            
    async def test_embed_audio(self):
        """Test 3: Tool execution - embed audio."""
        print("📋 Test 3: Tool Execution - Embed Audio")
        
        try:
            # Create a temporary audio file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name
                
            # Create a simple WAV file using numpy/scipy
            import numpy as np
            from scipy.io import wavfile
            
            sample_rate = 44100
            duration = 2  # seconds
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
            
            wavfile.write(tmp_path, sample_rate, audio_data)
            
            # Call embed_audio tool
            result = await self.client.call_tool(
                "embed_audio",
                arguments={
                    "audio_file_path": tmp_path,
                    "command": "test_command_123",
                    "ultrasonic_freq": 18500.0,
                    "amplitude": 0.1,
                    "obfuscate": True
                }
            )
            
            # Parse result
            if result.content and len(result.content) > 0:
                result_text = result.content[0].text
                result_data = json.loads(result_text)
                
                if result_data.get("success"):
                    self.test_results.append({
                        "test": "Embed Audio",
                        "status": "✅ PASSED",
                        "details": f"Command embedded successfully. Output: {result_data.get('output_file')}"
                    })
                    
                    # Store output file for decode test
                    self.embedded_audio_file = result_data.get("output_file")
                else:
                    self.test_results.append({
                        "test": "Embed Audio",
                        "status": "❌ FAILED",
                        "details": f"Embedding failed: {result_data.get('message')}"
                    })
            else:
                self.test_results.append({
                    "test": "Embed Audio",
                    "status": "❌ FAILED",
                    "details": "No result returned from tool"
                })
                
            # Clean up
            os.unlink(tmp_path)
            
        except Exception as e:
            self.test_results.append({
                "test": "Embed Audio",
                "status": "❌ FAILED",
                "details": f"Error: {str(e)}"
            })
            
    async def test_decode_audio(self):
        """Test 4: Tool execution - decode audio."""
        print("📋 Test 4: Tool Execution - Decode Audio")
        
        try:
            if hasattr(self, 'embedded_audio_file') and self.embedded_audio_file:
                # Call decode_audio tool
                result = await self.client.call_tool(
                    "decode_audio",
                    arguments={
                        "file_path": self.embedded_audio_file,
                        "detailed_analysis": True
                    }
                )
                
                # Parse result
                if result.content and len(result.content) > 0:
                    result_text = result.content[0].text
                    result_data = json.loads(result_text)
                    
                    if result_data.get("success") and result_data.get("command") == "test_command_123":
                        self.test_results.append({
                            "test": "Decode Audio",
                            "status": "✅ PASSED",
                            "details": f"Command decoded correctly: '{result_data.get('command')}'"
                        })
                    else:
                        self.test_results.append({
                            "test": "Decode Audio",
                            "status": "❌ FAILED",
                            "details": f"Decoding failed or incorrect command: {result_data}"
                        })
                else:
                    self.test_results.append({
                        "test": "Decode Audio",
                        "status": "❌ FAILED",
                        "details": "No result returned from tool"
                    })
                    
                # Clean up
                if os.path.exists(self.embedded_audio_file):
                    os.unlink(self.embedded_audio_file)
            else:
                self.test_results.append({
                    "test": "Decode Audio",
                    "status": "⚠️ SKIPPED",
                    "details": "No embedded audio file available from previous test"
                })
                
        except Exception as e:
            self.test_results.append({
                "test": "Decode Audio",
                "status": "❌ FAILED",
                "details": f"Error: {str(e)}"
            })
            
    async def test_configuration_tools(self):
        """Test 5: Configuration tools."""
        print("📋 Test 5: Configuration Tools")
        
        try:
            # Test get_system_config
            result = await self.client.call_tool(
                "get_system_config",
                arguments={}
            )
            
            if result.content and len(result.content) > 0:
                result_text = result.content[0].text
                config_data = json.loads(result_text)
                
                if "frequencies" in config_data and "encryption" in config_data:
                    self.test_results.append({
                        "test": "Get System Config",
                        "status": "✅ PASSED",
                        "details": "Configuration retrieved successfully"
                    })
                else:
                    self.test_results.append({
                        "test": "Get System Config",
                        "status": "❌ FAILED",
                        "details": "Invalid configuration structure"
                    })
            
            # Test configure_system_frequencies
            result = await self.client.call_tool(
                "configure_system_frequencies",
                arguments={
                    "freq_0": 18000.0,
                    "freq_1": 19000.0
                }
            )
            
            if result.content and len(result.content) > 0:
                result_text = result.content[0].text
                result_data = json.loads(result_text)
                
                if result_data.get("success"):
                    self.test_results.append({
                        "test": "Configure Frequencies",
                        "status": "✅ PASSED",
                        "details": "Frequencies configured successfully"
                    })
                else:
                    self.test_results.append({
                        "test": "Configure Frequencies",
                        "status": "❌ FAILED",
                        "details": result_data.get("message", "Unknown error")
                    })
                    
        except Exception as e:
            self.test_results.append({
                "test": "Configuration Tools",
                "status": "❌ FAILED",
                "details": f"Error: {str(e)}"
            })
            
    async def test_error_handling(self):
        """Test 6: Error handling in MCP context."""
        print("📋 Test 6: Error Handling")
        
        try:
            # Test with invalid file path
            result = await self.client.call_tool(
                "decode_audio",
                arguments={
                    "file_path": "/nonexistent/file.wav"
                }
            )
            
            if result.content and len(result.content) > 0:
                result_text = result.content[0].text
                
                # Should contain error message
                if "Error" in result_text or "error" in result_text.lower():
                    self.test_results.append({
                        "test": "Error Handling - Invalid File",
                        "status": "✅ PASSED",
                        "details": "Error handled gracefully"
                    })
                else:
                    self.test_results.append({
                        "test": "Error Handling - Invalid File",
                        "status": "❌ FAILED",
                        "details": "Error not properly reported"
                    })
                    
            # Test with invalid tool name
            try:
                await self.client.call_tool(
                    "nonexistent_tool",
                    arguments={}
                )
                self.test_results.append({
                    "test": "Error Handling - Invalid Tool",
                    "status": "❌ FAILED",
                    "details": "Should have raised an error"
                })
            except Exception:
                self.test_results.append({
                    "test": "Error Handling - Invalid Tool",
                    "status": "✅ PASSED",
                    "details": "Invalid tool error handled correctly"
                })
                
        except Exception as e:
            self.test_results.append({
                "test": "Error Handling",
                "status": "❌ FAILED",
                "details": f"Error: {str(e)}"
            })
            
    async def test_analyze_media(self):
        """Test 7: Analyze media tool."""
        print("📋 Test 7: Analyze Media Tool")
        
        try:
            # Create a test audio file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name
                
            import numpy as np
            from scipy.io import wavfile
            
            sample_rate = 44100
            duration = 1
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
            
            wavfile.write(tmp_path, sample_rate, audio_data)
            
            # Call analyze_media tool
            result = await self.client.call_tool(
                "analyze_media",
                arguments={
                    "file_path": tmp_path
                }
            )
            
            if result.content and len(result.content) > 0:
                result_text = result.content[0].text
                result_data = json.loads(result_text)
                
                if "success" in result_data:
                    self.test_results.append({
                        "test": "Analyze Media",
                        "status": "✅ PASSED",
                        "details": "Media analysis completed successfully"
                    })
                else:
                    self.test_results.append({
                        "test": "Analyze Media",
                        "status": "❌ FAILED",
                        "details": "Analysis failed"
                    })
                    
            # Clean up
            os.unlink(tmp_path)
            
        except Exception as e:
            self.test_results.append({
                "test": "Analyze Media",
                "status": "❌ FAILED",
                "details": f"Error: {str(e)}"
            })
            
    def print_results(self):
        """Print test results summary."""
        print("\n" + "="*60)
        print("📊 Test Results Summary")
        print("="*60 + "\n")
        
        passed = sum(1 for r in self.test_results if "PASSED" in r["status"])
        failed = sum(1 for r in self.test_results if "FAILED" in r["status"])
        skipped = sum(1 for r in self.test_results if "SKIPPED" in r["status"])
        
        for result in self.test_results:
            print(f"{result['status']} {result['test']}")
            if result['details']:
                print(f"    → {result['details']}")
            print()
            
        print("-"*60)
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Skipped: {skipped}")
        print("-"*60)
        
        if failed == 0:
            print("\n🎉 All tests passed! MCP server integration is working correctly.")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please check the details above.")
            

async def main():
    """Main entry point."""
    print("🔧 MCP Server Integration Test Suite")
    print("Version: 1.0.0")
    print("-"*60)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    
    try:
        import mcp
        print("  ✓ MCP library found")
    except ImportError:
        print("  ✗ MCP library not found. Install with: pip install mcp")
        return
        
    try:
        import numpy
        import scipy
        print("  ✓ NumPy and SciPy found")
    except ImportError:
        print("  ✗ NumPy/SciPy not found. Install with: pip install numpy scipy")
        return
        
    # Run tests
    tester = MCPServerTester()
    try:
        await tester.start_server_and_connect()
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())