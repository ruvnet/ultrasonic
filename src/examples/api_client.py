#!/usr/bin/env python3
"""
API Client Example for Ultrasonic Agentics

This example demonstrates how to interact with the Ultrasonic Agentics HTTP API
for encoding and decoding operations via REST endpoints.
"""

import requests
import json
import os
import time
from io import BytesIO
import numpy as np
from pydub import AudioSegment


class UltrasonicAgenticsClient:
    """Client for interacting with the Ultrasonic Agentics API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> dict:
        """Check if the API service is running."""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def get_api_info(self) -> dict:
        """Get API information and capabilities."""
        try:
            response = self.session.get(f"{self.base_url}/info", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def embed_audio_command(self, audio_file_path: str, command: str, 
                          obfuscate: bool = True, bitrate: str = "192k",
                          ultrasonic_freq: float = 18500, amplitude: float = 0.1) -> bytes:
        """Embed command into audio file via API."""
        with open(audio_file_path, 'rb') as f:
            files = {'file': (os.path.basename(audio_file_path), f, 'audio/wav')}
            data = {
                'command': command,
                'obfuscate': obfuscate,
                'bitrate': bitrate,
                'ultrasonic_freq': ultrasonic_freq,
                'amplitude': amplitude
            }
            
            response = self.session.post(
                f"{self.base_url}/embed/audio",
                files=files,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            return response.content
    
    def decode_audio_command(self, audio_file_path: str) -> dict:
        """Decode command from audio file via API."""
        with open(audio_file_path, 'rb') as f:
            files = {'file': (os.path.basename(audio_file_path), f, 'audio/wav')}
            
            response = self.session.post(
                f"{self.base_url}/decode/audio",
                files=files,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
    
    def analyze_audio(self, audio_file_path: str) -> dict:
        """Analyze audio file for steganographic content."""
        with open(audio_file_path, 'rb') as f:
            files = {'file': (os.path.basename(audio_file_path), f, 'audio/wav')}
            
            response = self.session.post(
                f"{self.base_url}/analyze/audio",
                files=files,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
    
    def configure_frequencies(self, freq_0: float, freq_1: float) -> dict:
        """Configure ultrasonic frequencies."""
        data = {
            'freq_0': freq_0,
            'freq_1': freq_1
        }
        
        response = self.session.post(
            f"{self.base_url}/config/frequencies",
            data=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def configure_encryption_key(self, key_base64: str) -> dict:
        """Configure encryption key."""
        data = {'key_base64': key_base64}
        
        response = self.session.post(
            f"{self.base_url}/config/key",
            data=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()


def create_test_audio_file(filename: str = "test_audio.wav") -> str:
    """Create a test audio file for API demonstrations."""
    duration = 5.0
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a simple musical phrase
    audio = (
        0.3 * np.sin(2 * np.pi * 261.63 * t) +  # C note
        0.2 * np.sin(2 * np.pi * 329.63 * t) +  # E note
        0.1 * np.random.normal(0, 0.02, len(t))  # Background noise
    )
    
    # Convert to AudioSegment and save
    audio_int16 = (audio * 32767).astype(np.int16)
    audio_segment = AudioSegment(
        audio_int16.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )
    
    audio_segment.export(filename, format="wav")
    print(f"Created test audio file: {filename}")
    return filename


def test_api_connection():
    """Test basic API connectivity."""
    print("=== Testing API Connection ===")
    
    client = UltrasonicAgenticsClient()
    
    # Health check
    health = client.health_check()
    print(f"Health check: {health}")
    
    if health.get("status") == "healthy":
        print("✓ API is running and accessible")
        
        # Get API info
        info = client.get_api_info()
        print(f"API Info: {json.dumps(info, indent=2)}")
        return True
    else:
        print("✗ API is not accessible")
        print("Make sure the API server is running with: python -m ultrasonic_agentics.server")
        return False


def test_audio_embedding_api():
    """Test audio embedding via API."""
    print("\n=== Testing Audio Embedding API ===")
    
    client = UltrasonicAgenticsClient()
    
    # Create test audio
    test_file = create_test_audio_file("api_test_input.wav")
    
    try:
        # Embed command
        command = "api:test_embedding"
        print(f"Embedding command: {command}")
        
        embedded_audio_data = client.embed_audio_command(
            test_file, 
            command,
            obfuscate=True,
            ultrasonic_freq=19000,
            amplitude=0.15
        )
        
        # Save embedded audio
        output_file = "api_test_embedded.wav"
        with open(output_file, 'wb') as f:
            f.write(embedded_audio_data)
        
        print(f"✓ Command embedded successfully")
        print(f"Saved embedded audio: {output_file}")
        
        # Test decoding
        decode_result = client.decode_audio_command(output_file)
        print(f"Decode result: {json.dumps(decode_result, indent=2)}")
        
        if decode_result.get("success") and decode_result.get("command") == command:
            print("✓ Command decoded successfully via API")
        else:
            print("✗ Command decoding failed")
        
        # Clean up
        cleanup_files([test_file, output_file])
        
    except requests.RequestException as e:
        print(f"✗ API request failed: {e}")
        cleanup_files([test_file])


def test_audio_analysis_api():
    """Test audio analysis via API."""
    print("\n=== Testing Audio Analysis API ===")
    
    client = UltrasonicAgenticsClient()
    
    # Create test audio with embedded command
    test_file = create_test_audio_file("analysis_test.wav")
    
    try:
        # First embed a command
        embedded_data = client.embed_audio_command(
            test_file,
            "analysis:test_signal",
            amplitude=0.2
        )
        
        embedded_file = "analysis_embedded.wav"
        with open(embedded_file, 'wb') as f:
            f.write(embedded_data)
        
        # Analyze the embedded audio
        analysis_result = client.analyze_audio(embedded_file)
        print(f"Analysis result: {json.dumps(analysis_result, indent=2)}")
        
        # Check analysis results
        if "signal_detected" in analysis_result:
            print(f"Signal detected: {analysis_result['signal_detected']}")
            if "signal_strength" in analysis_result:
                print(f"Signal strength: {analysis_result['signal_strength']:.4f}")
            print("✓ Audio analysis completed successfully")
        else:
            print("✗ Audio analysis failed")
        
        # Clean up
        cleanup_files([test_file, embedded_file])
        
    except requests.RequestException as e:
        print(f"✗ API request failed: {e}")
        cleanup_files([test_file])


def test_configuration_api():
    """Test API configuration endpoints."""
    print("\n=== Testing Configuration API ===")
    
    client = UltrasonicAgenticsClient()
    
    try:
        # Test frequency configuration
        print("Testing frequency configuration...")
        freq_result = client.configure_frequencies(20000, 21000)
        print(f"Frequency config result: {json.dumps(freq_result, indent=2)}")
        
        if freq_result.get("success"):
            print("✓ Frequency configuration successful")
        else:
            print("✗ Frequency configuration failed")
        
        # Test with the new frequencies
        test_file = create_test_audio_file("freq_test.wav")
        
        embedded_data = client.embed_audio_command(
            test_file,
            "freq:test_20k",
            ultrasonic_freq=20000
        )
        
        embedded_file = "freq_test_embedded.wav"
        with open(embedded_file, 'wb') as f:
            f.write(embedded_data)
        
        decode_result = client.decode_audio_command(embedded_file)
        
        if decode_result.get("success"):
            print("✓ New frequency configuration works correctly")
        else:
            print("✗ New frequency configuration test failed")
        
        # Reset to default frequencies
        client.configure_frequencies(18500, 19500)
        
        # Clean up
        cleanup_files([test_file, embedded_file])
        
    except requests.RequestException as e:
        print(f"✗ Configuration API request failed: {e}")


def test_batch_api_operations():
    """Test batch operations via API."""
    print("\n=== Testing Batch API Operations ===")
    
    client = UltrasonicAgenticsClient()
    
    # Create multiple test files
    test_files = []
    commands = ["batch:cmd1", "batch:cmd2", "batch:cmd3"]
    
    try:
        print("Creating batch test files...")
        for i, command in enumerate(commands):
            input_file = f"batch_input_{i+1}.wav"
            test_files.append(input_file)
            create_test_audio_file(input_file)
        
        # Process each file
        embedded_files = []
        for i, (input_file, command) in enumerate(zip(test_files, commands)):
            print(f"Processing {input_file} with command: {command}")
            
            # Embed command
            embedded_data = client.embed_audio_command(
                input_file,
                command,
                amplitude=0.18
            )
            
            # Save embedded file
            embedded_file = f"batch_embedded_{i+1}.wav"
            embedded_files.append(embedded_file)
            with open(embedded_file, 'wb') as f:
                f.write(embedded_data)
        
        # Decode all files
        print("Decoding batch files...")
        success_count = 0
        for i, (embedded_file, expected_command) in enumerate(zip(embedded_files, commands)):
            decode_result = client.decode_audio_command(embedded_file)
            
            if decode_result.get("success") and decode_result.get("command") == expected_command:
                print(f"  ✓ {embedded_file}: {decode_result['command']}")
                success_count += 1
            else:
                print(f"  ✗ {embedded_file}: Failed or mismatched")
        
        print(f"Batch processing results: {success_count}/{len(commands)} successful")
        
        # Clean up
        cleanup_files(test_files + embedded_files)
        
    except requests.RequestException as e:
        print(f"✗ Batch API operations failed: {e}")
        cleanup_files(test_files)


def test_error_handling():
    """Test API error handling with invalid inputs."""
    print("\n=== Testing API Error Handling ===")
    
    client = UltrasonicAgenticsClient()
    
    # Test invalid file upload
    try:
        # Create a text file instead of audio
        invalid_file = "invalid_audio.txt"
        with open(invalid_file, 'w') as f:
            f.write("This is not an audio file")
        
        print("Testing invalid file format...")
        try:
            client.embed_audio_command(invalid_file, "test:invalid")
            print("✗ Should have failed with invalid file format")
        except requests.HTTPError as e:
            print(f"✓ Correctly rejected invalid file: {e.response.status_code}")
        
        os.remove(invalid_file)
        
    except Exception as e:
        print(f"Error in invalid file test: {e}")
    
    # Test invalid frequency configuration
    print("Testing invalid frequency configuration...")
    try:
        result = client.configure_frequencies(-1000, 50000)  # Invalid frequencies
        print("✗ Should have failed with invalid frequencies")
    except requests.HTTPError as e:
        print(f"✓ Correctly rejected invalid frequencies: {e.response.status_code}")
    
    # Test non-existent endpoint
    print("Testing non-existent endpoint...")
    try:
        response = client.session.get(f"{client.base_url}/nonexistent")
        response.raise_for_status()
        print("✗ Should have failed with 404")
    except requests.HTTPError as e:
        print(f"✓ Correctly returned 404 for non-existent endpoint: {e.response.status_code}")


def performance_test():
    """Test API performance with various file sizes."""
    print("\n=== Testing API Performance ===")
    
    client = UltrasonicAgenticsClient()
    
    durations = [1, 3, 5, 10]  # seconds
    
    for duration in durations:
        print(f"\nTesting with {duration}s audio file...")
        
        # Create test audio of specific duration
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = 0.3 * np.sin(2 * np.pi * 440 * t)
        
        audio_int16 = (audio * 32767).astype(np.int16)
        audio_segment = AudioSegment(
            audio_int16.tobytes(),
            frame_rate=sample_rate,
            sample_width=2,
            channels=1
        )
        
        test_file = f"perf_test_{duration}s.wav"
        audio_segment.export(test_file, format="wav")
        
        try:
            # Measure embedding time
            start_time = time.time()
            embedded_data = client.embed_audio_command(
                test_file,
                f"perf:test_{duration}s"
            )
            embed_time = time.time() - start_time
            
            # Save and measure decoding time
            embedded_file = f"perf_embedded_{duration}s.wav"
            with open(embedded_file, 'wb') as f:
                f.write(embedded_data)
            
            start_time = time.time()
            decode_result = client.decode_audio_command(embedded_file)
            decode_time = time.time() - start_time
            
            print(f"  File size: {os.path.getsize(test_file) / 1024:.1f} KB")
            print(f"  Embed time: {embed_time:.2f}s")
            print(f"  Decode time: {decode_time:.2f}s")
            print(f"  Success: {decode_result.get('success', False)}")
            
            # Clean up
            cleanup_files([test_file, embedded_file])
            
        except Exception as e:
            print(f"  ✗ Performance test failed: {e}")
            cleanup_files([test_file])


def cleanup_files(file_list):
    """Clean up temporary files."""
    for file_path in file_list:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            pass


if __name__ == "__main__":
    print("Ultrasonic Agentics - API Client Examples")
    print("=" * 50)
    print("Note: Make sure the API server is running:")
    print("  python -m ultrasonic_agentics.server")
    print("=" * 50)
    
    # Test API connectivity first
    if test_api_connection():
        # Run all API tests
        test_audio_embedding_api()
        test_audio_analysis_api()
        test_configuration_api()
        test_batch_api_operations()
        test_error_handling()
        performance_test()
        
        print("\n" + "=" * 50)
        print("API client examples completed!")
    else:
        print("\nSkipping tests - API server is not accessible")
        print("Start the server with: python -m ultrasonic_agentics.server")