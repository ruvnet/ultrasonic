#!/usr/bin/env python3
"""
Test to compare WAV vs MP3 encoding/decoding.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.decode.audio_decoder import AudioDecoder

def main():
    # Use the same key as in test_hello_world.py
    test_key = b'HelloWorldDemoKey' + b'0' * 15  # Pad to 32 bytes
    
    print("=" * 60)
    print("WAV vs MP3 ENCODING TEST")
    print("=" * 60)
    
    embedder = AudioEmbedder(key=test_key)
    decoder = AudioDecoder(key=test_key)
    
    command = "hello world"
    
    # Test 1: Embed in WAV format
    print("\n1. Testing with WAV format")
    print("-" * 40)
    
    try:
        success = embedder.embed_file(
            'sample_audio.mp3',
            'test_hello_world.wav',
            command
        )
        print(f"WAV embedding: {'SUCCESS' if success else 'FAILED'}")
        
        if success:
            result = decoder.decode_file('test_hello_world.wav')
            print(f"WAV decoding result: '{result}'")
            print(f"WAV test: {'PASS' if result == command else 'FAIL'}")
    except Exception as e:
        print(f"WAV test error: {e}")
    
    # Test 2: Embed in MP3 format with higher bitrate
    print("\n2. Testing with MP3 format (320k bitrate)")
    print("-" * 40)
    
    try:
        success = embedder.embed_file(
            'sample_audio.mp3',
            'test_hello_world_320k.mp3',
            command,
            bitrate="320k"
        )
        print(f"MP3 (320k) embedding: {'SUCCESS' if success else 'FAILED'}")
        
        if success:
            result = decoder.decode_file('test_hello_world_320k.mp3')
            print(f"MP3 (320k) decoding result: '{result}'")
            print(f"MP3 (320k) test: {'PASS' if result == command else 'FAIL'}")
    except Exception as e:
        print(f"MP3 (320k) test error: {e}")
    
    # Test 3: Check frequency spectrum
    print("\n3. Checking frequency preservation")
    print("-" * 40)
    
    from pydub import AudioSegment
    import numpy as np
    
    if os.path.exists('test_hello_world.wav'):
        wav_audio = AudioSegment.from_file('test_hello_world.wav')
        wav_samples = np.array(wav_audio.get_array_of_samples(), dtype=np.float32)
        
        # Check frequency content
        fft = np.fft.fft(wav_samples[:48000])  # First second
        freqs = np.fft.fftfreq(48000, 1/48000)
        magnitude = np.abs(fft)
        
        # Find peaks around our ultrasonic frequencies
        freq_range = (freqs > 17000) & (freqs < 21000)
        ultrasonic_power = np.sum(magnitude[freq_range])
        total_power = np.sum(magnitude)
        
        print(f"WAV ultrasonic power ratio: {ultrasonic_power/total_power:.4f}")
    
    if os.path.exists('test_hello_world_320k.mp3'):
        mp3_audio = AudioSegment.from_file('test_hello_world_320k.mp3')
        mp3_samples = np.array(mp3_audio.get_array_of_samples(), dtype=np.float32)
        
        # Check frequency content
        fft = np.fft.fft(mp3_samples[:48000])  # First second
        freqs = np.fft.fftfreq(48000, 1/48000)
        magnitude = np.abs(fft)
        
        # Find peaks around our ultrasonic frequencies
        freq_range = (freqs > 17000) & (freqs < 21000)
        ultrasonic_power = np.sum(magnitude[freq_range])
        total_power = np.sum(magnitude)
        
        print(f"MP3 ultrasonic power ratio: {ultrasonic_power/total_power:.4f}")
    
    # Clean up test files
    for f in ['test_hello_world.wav', 'test_hello_world_320k.mp3']:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    main()