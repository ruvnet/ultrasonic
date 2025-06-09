#!/usr/bin/env python3
"""
Robust test script for ultrasonic embedding and decoding.
Uses appropriate audio formats to preserve ultrasonic frequencies.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.embed.video_embedder import VideoEmbedder
from src.decode.audio_decoder import AudioDecoder
from src.decode.video_decoder import VideoDecoder

def test_audio_formats():
    """Test different audio formats for ultrasonic preservation."""
    test_key = b'TestKey1234567890' + b'0' * 15  # Pad to 32 bytes
    command = "hello ultrasonic world"
    
    print("=" * 70)
    print("AUDIO FORMAT ULTRASONIC PRESERVATION TEST")
    print("=" * 70)
    
    embedder = AudioEmbedder(key=test_key)
    decoder = AudioDecoder(key=test_key)
    
    # Test different audio formats
    formats = [
        ('wav', 'WAV (Uncompressed)', None),
        ('flac', 'FLAC (Lossless)', None),
        ('mp3', 'MP3 320k', '320k'),
        ('mp3', 'MP3 192k', '192k'),
        ('ogg', 'OGG Vorbis', '320k'),
    ]
    
    results = []
    
    for fmt, description, bitrate in formats:
        print(f"\nTesting {description}...")
        print("-" * 50)
        
        output_file = f"test_ultrasonic.{fmt}"
        
        try:
            # Create a test audio file if sample doesn't exist
            if not os.path.exists('sample_audio.mp3'):
                print("Creating sample audio file...")
                from pydub import AudioSegment
                from pydub.generators import Sine
                # Create 10 seconds of 440 Hz tone
                tone = Sine(440).to_audio_segment(duration=10000)
                tone.export('sample_audio.mp3', format='mp3')
            
            # Embed the command
            kwargs = {'bitrate': bitrate} if bitrate else {}
            success = embedder.embed_file(
                'sample_audio.mp3',
                output_file,
                command,
                **kwargs
            )
            
            if success:
                # Try to decode
                decoded = decoder.decode_file(output_file)
                
                if decoded == command:
                    print(f"✓ SUCCESS: Embedded and decoded '{command}'")
                    results.append((description, "SUCCESS", "Full recovery"))
                else:
                    print(f"✗ PARTIAL: Embedded but decoded as '{decoded}'")
                    results.append((description, "PARTIAL", f"Got: {decoded}"))
            else:
                print(f"✗ FAILED: Could not embed command")
                results.append((description, "FAILED", "Embedding failed"))
                
            # Clean up test file
            if os.path.exists(output_file):
                os.remove(output_file)
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
            results.append((description, "ERROR", str(e)))
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY OF RESULTS")
    print("=" * 70)
    print(f"{'Format':<20} {'Result':<10} {'Details'}")
    print("-" * 70)
    for fmt, result, details in results:
        print(f"{fmt:<20} {result:<10} {details}")
    
    print("\nRECOMMENDATIONS:")
    print("- Use WAV format for best ultrasonic signal preservation")
    print("- FLAC is a good lossless compressed alternative")
    print("- Avoid MP3/OGG for ultrasonic frequencies above 16kHz")
    print("- If using MP3, use highest bitrate (320k) and expect signal loss")


def test_video_embedding():
    """Test video embedding with proper audio codec."""
    test_key = b'VideoTestKey12345' + b'0' * 15  # Pad to 32 bytes
    command = "video command test"
    
    print("\n\n" + "=" * 70)
    print("VIDEO EMBEDDING TEST")
    print("=" * 70)
    
    embedder = VideoEmbedder(key=test_key)
    decoder = VideoDecoder(key=test_key)
    
    # Check if sample video exists
    if not os.path.exists('sample_video.mp4'):
        print("✗ No sample_video.mp4 found. Skipping video test.")
        return
    
    print("\nEmbedding command in video...")
    output_file = "test_video_ultrasonic.mp4"
    
    try:
        success = embedder.embed_file(
            'sample_video.mp4',
            output_file,
            command
        )
        
        if success:
            print("✓ Video file created successfully")
            
            # Try to decode
            decoded = decoder.decode_file(output_file)
            
            if decoded == command:
                print(f"✓ SUCCESS: Decoded '{command}' from video")
            else:
                print(f"✗ PARTIAL: Expected '{command}', got '{decoded}'")
        else:
            print("✗ FAILED: Could not create video with embedded command")
            
        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


def test_amplitude_adjustment():
    """Test different amplitude levels for embedding."""
    test_key = b'AmplitudeTest123' + b'0' * 16  # Pad to 32 bytes
    command = "amplitude test"
    
    print("\n\n" + "=" * 70)
    print("AMPLITUDE ADJUSTMENT TEST")
    print("=" * 70)
    
    decoder = AudioDecoder(key=test_key)
    
    amplitudes = [0.05, 0.1, 0.2, 0.3, 0.5]
    results = []
    
    for amp in amplitudes:
        print(f"\nTesting amplitude: {amp}")
        print("-" * 30)
        
        embedder = AudioEmbedder(key=test_key, amplitude=amp)
        output_file = f"test_amp_{amp}.wav"
        
        try:
            success = embedder.embed_file(
                'sample_audio.mp3',
                output_file,
                command
            )
            
            if success:
                decoded = decoder.decode_file(output_file)
                if decoded == command:
                    print(f"✓ SUCCESS at amplitude {amp}")
                    results.append((amp, "SUCCESS"))
                else:
                    print(f"✗ FAILED: Got '{decoded}' instead of '{command}'")
                    results.append((amp, "FAILED"))
            else:
                print(f"✗ Embedding failed")
                results.append((amp, "EMBED_FAIL"))
                
            # Clean up
            if os.path.exists(output_file):
                os.remove(output_file)
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
            results.append((amp, "ERROR"))
    
    print("\n" + "=" * 50)
    print("AMPLITUDE TEST SUMMARY")
    print("=" * 50)
    for amp, result in results:
        print(f"Amplitude {amp}: {result}")
    
    print("\nRECOMMENDATION:")
    print("- Use amplitude between 0.1 and 0.3 for best results")
    print("- Higher amplitudes may be audible")
    print("- Lower amplitudes may not decode reliably")


def main():
    """Run all tests."""
    print("ULTRASONIC EMBEDDING COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    # Run tests
    test_audio_formats()
    test_video_embedding()
    test_amplitude_adjustment()
    
    print("\n\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()