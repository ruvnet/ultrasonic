#!/usr/bin/env python3
"""
Debug script to understand why embedding fails.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.decode.audio_decoder import AudioDecoder
from src.embed.ultrasonic_encoder import UltrasonicEncoder
from src.decode.ultrasonic_decoder import UltrasonicDecoder
from pydub import AudioSegment
import numpy as np

def test_basic_encoding_decoding():
    """Test the basic encoding and decoding pipeline."""
    print("=== BASIC ENCODING/DECODING TEST ===\n")
    
    # Create encoder and decoder with matching parameters
    encoder = UltrasonicEncoder(amplitude=0.8, bit_duration=0.05)
    decoder = UltrasonicDecoder(detection_threshold=0.001, bit_duration=0.05)
    
    # Test with a simple payload
    test_payload = b"TEST"
    print(f"Test payload: {test_payload}")
    
    # Encode the payload
    signal = encoder.encode_payload(test_payload)
    print(f"Encoded signal length: {len(signal)} samples")
    print(f"Signal duration: {len(signal) / encoder.sample_rate:.2f} seconds")
    print(f"Signal amplitude range: {np.min(signal):.3f} to {np.max(signal):.3f}")
    
    # Try to decode
    decoded_payload = decoder.decode_payload(signal)
    print(f"Decoded payload: {decoded_payload}")
    
    if decoded_payload == test_payload:
        print("✅ SUCCESS: Direct encoding/decoding works!")
    else:
        print("❌ FAILED: Direct encoding/decoding failed")
    
    return decoded_payload == test_payload

def test_with_audio_segment():
    """Test with AudioSegment conversion."""
    print("\n=== AUDIO SEGMENT CONVERSION TEST ===\n")
    
    encoder = UltrasonicEncoder(amplitude=0.8, bit_duration=0.05)
    decoder = UltrasonicDecoder(detection_threshold=0.001, bit_duration=0.05)
    
    test_payload = b"TEST"
    
    # Encode and create audio segment
    signal = encoder.encode_payload(test_payload)
    audio_segment = encoder.create_audio_segment(signal)
    
    print(f"AudioSegment duration: {len(audio_segment)} ms")
    print(f"AudioSegment sample rate: {audio_segment.frame_rate} Hz")
    
    # Convert back to numpy for decoding
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
    samples_norm = samples / np.max(np.abs(samples))
    
    print(f"Normalized samples range: {np.min(samples_norm):.3f} to {np.max(samples_norm):.3f}")
    
    # Try to decode
    decoded_payload = decoder.decode_payload(samples_norm)
    print(f"Decoded payload: {decoded_payload}")
    
    if decoded_payload == test_payload:
        print("✅ SUCCESS: AudioSegment conversion works!")
    else:
        print("❌ FAILED: AudioSegment conversion failed")
    
    return decoded_payload == test_payload

def test_full_pipeline():
    """Test the full embedding/decoding pipeline."""
    print("\n=== FULL PIPELINE TEST ===\n")
    
    # Use a consistent key
    test_key = b'TestKey1234567890123456789012345'  # 32 bytes
    
    embedder = AudioEmbedder(key=test_key, amplitude=0.8, bit_duration=0.05)
    decoder = AudioDecoder(key=test_key, detection_threshold=0.001, bit_duration=0.05)
    
    # Create silent audio
    test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
    
    # Test command
    command = "hello world"
    print(f"Test command: '{command}'")
    
    # Embed command
    stego_audio = embedder.embed(test_audio, command)
    print(f"Stego audio duration: {len(stego_audio)} ms")
    
    # Try to decode
    decoded_command = decoder.decode_audio_segment(stego_audio)
    print(f"Decoded command: '{decoded_command}'")
    
    if decoded_command == command:
        print("✅ SUCCESS: Full pipeline works!")
    else:
        print("❌ FAILED: Full pipeline failed")
        
        # Debug: Check if signal is present
        print("\nDEBUG: Checking signal presence...")
        is_present = decoder.detect_signal(stego_audio)
        print(f"Signal detected: {is_present}")
        
        if is_present:
            strength = decoder.get_signal_strength(stego_audio)
            print(f"Signal strength: {strength:.3f}")
    
    return decoded_command == command

def main():
    """Run all tests."""
    print("Debugging ultrasonic embedding system...\n")
    
    test1 = test_basic_encoding_decoding()
    test2 = test_with_audio_segment()
    test3 = test_full_pipeline()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Basic encoding/decoding: {'PASS' if test1 else 'FAIL'}")
    print(f"AudioSegment conversion: {'PASS' if test2 else 'FAIL'}")
    print(f"Full pipeline: {'PASS' if test3 else 'FAIL'}")
    print("=" * 50)

if __name__ == "__main__":
    main()