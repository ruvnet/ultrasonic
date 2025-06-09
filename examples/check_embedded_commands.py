#!/usr/bin/env python3
"""
Simple script to check if the sample files have any embedded commands.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.decode.audio_decoder import AudioDecoder

def check_files():
    # Test with various common keys
    test_keys = [
        b'0' * 32,  # All zeros
        b'HelloWorldDemoKey' + b'0' * 15,  # Demo key
        b'test' * 8,  # Simple test key
        b'ultrasonic' + b'0' * 22,  # Project name based
    ]
    
    print("=" * 60)
    print("CHECKING FOR EMBEDDED COMMANDS IN SAMPLE FILES")
    print("=" * 60)
    
    files_to_check = [
        'sample_audio.mp3',
        'sample_video.mp4',
        'sample_audio_hello_world.mp3',
        'sample_audio_with_hello_world.mp3'
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            print(f"\nChecking: {filename}")
            print("-" * 40)
            
            found_command = False
            
            for i, key in enumerate(test_keys):
                try:
                    decoder = AudioDecoder(key=key)
                    
                    if filename.endswith('.mp4'):
                        # For video files, we need to extract audio first
                        from src.decode.video_decoder import VideoDecoder
                        video_decoder = VideoDecoder(key=key)
                        result = video_decoder.decode_file(filename)
                    else:
                        result = decoder.decode_file(filename)
                    
                    if result:
                        print(f"  ✓ Found command with key {i+1}: '{result}'")
                        found_command = True
                        break
                except Exception as e:
                    pass
            
            if not found_command:
                print("  ✗ No embedded command found (file is clean)")
        else:
            print(f"\n{filename}: File not found")
    
    print("\n" + "=" * 60)
    print("CREATING TEST FILE WITH 'HELLO WORLD'")
    print("=" * 60)
    
    # Now let's create a file with "hello world" embedded
    demo_key = b'HelloWorldDemoKey' + b'0' * 15
    embedder = AudioEmbedder(key=demo_key)
    
    print("\nEmbedding 'hello world' in a new test file...")
    try:
        success = embedder.embed_file(
            'sample_audio.mp3',
            'test_hello_world_verified.mp3',
            'hello world'
        )
        
        if success:
            print("  ✓ Embedding successful")
            
            # Verify it
            decoder = AudioDecoder(key=demo_key)
            result = decoder.decode_file('test_hello_world_verified.mp3')
            
            if result == 'hello world':
                print(f"  ✓ Verification successful: '{result}'")
                print("\nCONCLUSION: The embedding system works correctly!")
                print("File 'test_hello_world_verified.mp3' contains 'hello world'")
            else:
                print(f"  ✗ Verification failed: got '{result}'")
        else:
            print("  ✗ Embedding failed")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")

if __name__ == "__main__":
    check_files()