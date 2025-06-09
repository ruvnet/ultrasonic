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
        success = audio_embedder.embed_file(
            'sample_audio.mp3',
            'sample_audio_hello_world.mp3',
            'hello world'
        )
        print(f"  Audio embedding: {'SUCCESS' if success else 'FAILED'}")
    except Exception as e:
        print(f"  Audio embedding FAILED: {e}")
    
    print("\nEmbedding in video file...")
    try:
        success = video_embedder.embed_file(
            'sample_video.mp4',
            'sample_video_hello_world.mp4',
            'hello world'
        )
        print(f"  Video embedding: {'SUCCESS' if success else 'FAILED'}")
    except Exception as e:
        print(f"  Video embedding FAILED: {e}")
    
    # Test 3: Verify embedded commands
    print("\n\n3. VERIFYING EMBEDDED COMMANDS")
    print("-" * 40)
    
    if os.path.exists('sample_audio_hello_world.mp3'):
        print("Decoding sample_audio_hello_world.mp3...")
        result = audio_decoder.decode_file('sample_audio_hello_world.mp3')
        if result == 'hello world':
            print(f"  ✓ SUCCESS: Found '{result}'")
        else:
            print(f"  ✗ FAILED: Expected 'hello world', got '{result}'")
    else:
        print("  ✗ Audio file with embedded command not found")
    
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
    
    # List all files
    print("\nFiles in examples directory:")
    os.system('ls -la *.mp*')

if __name__ == "__main__":
    main()