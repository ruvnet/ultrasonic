#!/usr/bin/env python3
"""
Test script to embed and verify "hello world" in sample media files.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.embed.video_embedder import VideoEmbedder
from src.decode.audio_decoder import AudioDecoder
from src.decode.video_decoder import VideoDecoder

def main():
    # Use a consistent key
    test_key = b'HelloWorldDemoKey' + b'0' * 15  # Pad to 32 bytes
    
    print("=" * 60)
    print("HELLO WORLD EMBEDDING TEST")
    print("=" * 60)
    
    # Test 1: Check original files (should have no embedded commands)
    print("\n1. CHECKING ORIGINAL FILES")
    print("-" * 40)
    
    audio_decoder = AudioDecoder(key=test_key)
    video_decoder = VideoDecoder(key=test_key)
    
    print("Checking sample_audio.mp3...")
    result = audio_decoder.decode_file('sample_audio.mp3')
    print(f"  Result: {result if result else 'No embedded command (clean file)'}")
    
    print("\nChecking sample_video.mp4...")
    result = video_decoder.decode_file('sample_video.mp4')
    print(f"  Result: {result if result else 'No embedded command (clean file)'}")
    
    # Test 2: Embed "hello world"
    print("\n\n2. EMBEDDING 'HELLO WORLD'")
    print("-" * 40)
    
    audio_embedder = AudioEmbedder(key=test_key)
    video_embedder = VideoEmbedder(key=test_key)
    
    print("Embedding in audio file...")
    try:
        # First embed in WAV to preserve ultrasonic frequencies
        success = audio_embedder.embed_file(
            'sample_audio.mp3',
            'sample_audio_hello_world.wav',
            'hello world'
        )
        print(f"  Audio embedding (WAV): {'SUCCESS' if success else 'FAILED'}")
        
        # Also try MP3 with high bitrate (will likely fail decoding)
        if success:
            print("\n  Also creating MP3 version (for comparison)...")
            success_mp3 = audio_embedder.embed_file(
                'sample_audio.mp3',
                'sample_audio_hello_world.mp3',
                'hello world',
                bitrate='320k'
            )
            print(f"  Audio embedding (MP3): {'SUCCESS' if success_mp3 else 'FAILED'}")
            
    except Exception as e:
        print(f"  Audio embedding FAILED: {e}")
    
    print("\nEmbedding in video file...")
    try:
        # Embed with ultrasonic preservation enabled
        success = video_embedder.embed_file(
            'sample_video.mp4',
            'sample_video_hello_world.mp4',
            'hello world',
            preserve_ultrasonic=True  # Use PCM audio codec
        )
        print(f"  Video embedding: {'SUCCESS' if success else 'FAILED'}")
    except Exception as e:
        print(f"  Video embedding FAILED: {e}")
    
    # Test 3: Verify embedded commands
    print("\n\n3. VERIFYING EMBEDDED COMMANDS")
    print("-" * 40)
    
    # Test WAV file first
    if os.path.exists('sample_audio_hello_world.wav'):
        print("Decoding sample_audio_hello_world.wav...")
        result = audio_decoder.decode_file('sample_audio_hello_world.wav')
        if result == 'hello world':
            print(f"  ✓ SUCCESS: Found '{result}' in WAV file")
        else:
            print(f"  ✗ FAILED: Expected 'hello world', got '{result}' in WAV file")
    else:
        print("  ✗ WAV file with embedded command not found")
    
    # Test MP3 file (may fail due to compression)
    if os.path.exists('sample_audio_hello_world.mp3'):
        print("\nDecoding sample_audio_hello_world.mp3...")
        result = audio_decoder.decode_file('sample_audio_hello_world.mp3')
        if result == 'hello world':
            print(f"  ✓ SUCCESS: Found '{result}' in MP3 file")
        else:
            print(f"  ✗ WARNING: MP3 compression affected ultrasonic signal")
            print(f"    (This is expected - MP3 compression removes ultrasonic frequencies)")
    else:
        print("  ✗ MP3 file with embedded command not found")
    
    if os.path.exists('sample_video_hello_world.mp4'):
        print("\nDecoding sample_video_hello_world.mp4...")
        result = video_decoder.decode_file('sample_video_hello_world.mp4')
        if result == 'hello world':
            print(f"  ✓ SUCCESS: Found '{result}'")
        else:
            print(f"  ✗ FAILED: Expected 'hello world', got '{result}'")
    else:
        print("  ✗ Video file with embedded command not found")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Original files: Clean (no embedded commands)")
    print("Target command: 'hello world'")
    print("Encryption key: First 17 chars = 'HelloWorldDemoKey'")
    
    print("\nFORMAT RECOMMENDATIONS:")
    print("- WAV: Best format for ultrasonic embedding (uncompressed)")
    print("- FLAC: Good lossless alternative to WAV")
    print("- MP3: Poor ultrasonic preservation (cuts frequencies >16kHz)")
    print("- Video: Use preserve_ultrasonic=True for PCM audio codec")
    
    # List all files
    print("\nFiles created:")
    os.system('ls -la sample_*hello_world*')
    
    # Run frequency analysis if available
    if os.path.exists('check_ultrasonic_frequencies.py'):
        print("\n" + "=" * 60)
        print("FREQUENCY ANALYSIS")
        print("=" * 60)
        if os.path.exists('sample_audio_hello_world.wav'):
            print("\nAnalyzing WAV file:")
            os.system('python check_ultrasonic_frequencies.py sample_audio_hello_world.wav')
        if os.path.exists('sample_audio_hello_world.mp3'):
            print("\nAnalyzing MP3 file:")
            os.system('python check_ultrasonic_frequencies.py sample_audio_hello_world.mp3')

if __name__ == "__main__":
    main()