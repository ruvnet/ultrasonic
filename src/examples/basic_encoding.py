#!/usr/bin/env python3
"""
Basic Encoding Example for Ultrasonic Agentics

This example demonstrates the fundamental encoding and decoding operations
using the Ultrasonic Agentics framework.
"""

import numpy as np
from ultrasonic_agentics.embed.ultrasonic_encoder import UltrasonicEncoder
from ultrasonic_agentics.decode.ultrasonic_decoder import UltrasonicDecoder
from pydub import AudioSegment
import os


def basic_encode_decode_example():
    """Demonstrate basic encoding and decoding of a command."""
    print("=== Basic Encoding/Decoding Example ===")
    
    # 1. Initialize encoder and decoder
    encoder = UltrasonicEncoder(
        freq_0=18500,  # Frequency for bit '0'
        freq_1=19500,  # Frequency for bit '1'
        sample_rate=48000,
        bit_duration=0.01,  # 10ms per bit
        amplitude=0.2       # 20% amplitude
    )
    
    decoder = UltrasonicDecoder(
        freq_0=18500,
        freq_1=19500,
        sample_rate=48000,
        bit_duration=0.01,
        detection_threshold=0.1
    )
    
    # 2. Prepare command to encode
    command = "execute:status_check"
    print(f"Original command: {command}")
    
    # 3. Encode the command
    print("Encoding command into ultrasonic signal...")
    payload_bytes = command.encode('utf-8')
    audio_signal = encoder.encode_payload(payload_bytes)
    
    print(f"Generated signal: {len(audio_signal)} samples")
    print(f"Signal duration: {len(audio_signal) / encoder.sample_rate:.2f} seconds")
    print(f"Frequency range: {encoder.get_frequency_range()} Hz")
    
    # 4. Save encoded audio to file
    audio_segment = encoder.create_audio_segment(audio_signal)
    output_file = "encoded_command.wav"
    audio_segment.export(output_file, format="wav")
    print(f"Saved encoded audio to: {output_file}")
    
    # 5. Decode the signal
    print("Decoding signal...")
    decoded_bytes = decoder.decode_payload(audio_signal)
    
    if decoded_bytes:
        decoded_command = decoded_bytes.decode('utf-8', errors='ignore')
        print(f"Decoded command: {decoded_command}")
        
        # Check if decoding was successful
        if decoded_command == command:
            print("✓ Encoding/Decoding successful!")
        else:
            print(f"✗ Decoding mismatch. Expected: {command}, Got: {decoded_command}")
    else:
        print("✗ Decoding failed - no signal detected")
    
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)


def test_different_commands():
    """Test encoding/decoding with various command types."""
    print("\n=== Testing Different Command Types ===")
    
    encoder = UltrasonicEncoder(amplitude=0.15)
    decoder = UltrasonicDecoder()
    
    test_commands = [
        "execute:status_check",
        "transmit:sensor_data",
        "configure:mode=stealth",
        "status:report",
        "ping",
        "shutdown:graceful"
    ]
    
    success_count = 0
    
    for command in test_commands:
        print(f"\nTesting: {command}")
        
        # Encode
        payload = command.encode('utf-8')
        signal = encoder.encode_payload(payload)
        
        # Decode
        decoded_bytes = decoder.decode_payload(signal)
        
        if decoded_bytes:
            decoded_command = decoded_bytes.decode('utf-8', errors='ignore')
            if decoded_command == command:
                print(f"  ✓ Success")
                success_count += 1
            else:
                print(f"  ✗ Mismatch: {decoded_command}")
        else:
            print(f"  ✗ Decode failed")
    
    print(f"\nSuccess rate: {success_count}/{len(test_commands)} ({100*success_count/len(test_commands):.1f}%)")


def frequency_range_test():
    """Test different frequency ranges for encoding."""
    print("\n=== Frequency Range Testing ===")
    
    frequency_pairs = [
        (17000, 17500),  # Lower ultrasonic
        (18000, 18500),  # Mid-low ultrasonic
        (19000, 19500),  # Mid ultrasonic (default)
        (20000, 20500),  # Mid-high ultrasonic
        (21000, 21500),  # Higher ultrasonic
    ]
    
    test_command = "execute:test"
    
    for freq_0, freq_1 in frequency_pairs:
        print(f"\nTesting frequencies: {freq_0} Hz / {freq_1} Hz")
        
        try:
            encoder = UltrasonicEncoder(freq_0=freq_0, freq_1=freq_1, amplitude=0.2)
            decoder = UltrasonicDecoder(freq_0=freq_0, freq_1=freq_1)
            
            # Encode and decode
            signal = encoder.encode_payload(test_command.encode())
            decoded_bytes = decoder.decode_payload(signal)
            
            if decoded_bytes:
                decoded = decoded_bytes.decode('utf-8', errors='ignore')
                if decoded == test_command:
                    print(f"  ✓ Success at {freq_0}/{freq_1} Hz")
                else:
                    print(f"  ✗ Decode mismatch")
            else:
                print(f"  ✗ Decode failed")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")


def amplitude_sensitivity_test():
    """Test how amplitude affects encoding/decoding reliability."""
    print("\n=== Amplitude Sensitivity Testing ===")
    
    amplitudes = [0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
    test_command = "test:amplitude"
    
    decoder = UltrasonicDecoder(detection_threshold=0.05)
    
    for amplitude in amplitudes:
        print(f"\nTesting amplitude: {amplitude}")
        
        encoder = UltrasonicEncoder(amplitude=amplitude)
        signal = encoder.encode_payload(test_command.encode())
        
        # Check signal strength
        signal_power = np.sqrt(np.mean(signal ** 2))
        print(f"  Signal RMS: {signal_power:.4f}")
        
        # Test decoding
        decoded_bytes = decoder.decode_payload(signal)
        
        if decoded_bytes:
            decoded = decoded_bytes.decode('utf-8', errors='ignore')
            if decoded == test_command:
                print(f"  ✓ Decode success")
            else:
                print(f"  ✗ Decode mismatch")
        else:
            print(f"  ✗ Decode failed")


def noise_resilience_test():
    """Test encoding/decoding with added noise."""
    print("\n=== Noise Resilience Testing ===")
    
    encoder = UltrasonicEncoder(amplitude=0.3)  # Higher amplitude for noise resilience
    decoder = UltrasonicDecoder(detection_threshold=0.1)
    
    test_command = "test:noise_resilience"
    clean_signal = encoder.encode_payload(test_command.encode())
    
    noise_levels = [0.01, 0.02, 0.05, 0.1, 0.2]
    
    for noise_level in noise_levels:
        print(f"\nTesting with noise level: {noise_level}")
        
        # Add random noise
        noise = np.random.normal(0, noise_level, len(clean_signal))
        noisy_signal = clean_signal + noise
        
        # Calculate SNR
        signal_power = np.mean(clean_signal ** 2)
        noise_power = np.mean(noise ** 2)
        snr_db = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
        print(f"  SNR: {snr_db:.1f} dB")
        
        # Test decoding
        decoded_bytes = decoder.decode_payload(noisy_signal)
        
        if decoded_bytes:
            decoded = decoded_bytes.decode('utf-8', errors='ignore')
            if decoded == test_command:
                print(f"  ✓ Decode success despite noise")
            else:
                print(f"  ✗ Decode corrupted: {decoded}")
        else:
            print(f"  ✗ Decode failed due to noise")


def payload_size_test():
    """Test encoding/decoding with different payload sizes."""
    print("\n=== Payload Size Testing ===")
    
    encoder = UltrasonicEncoder(amplitude=0.2)
    decoder = UltrasonicDecoder()
    
    # Test different payload sizes
    test_sizes = [5, 10, 20, 50, 100, 200]
    
    for size in test_sizes:
        # Create test payload of specified size
        payload = f"test:{'x' * (size - 5)}"  # 5 chars for "test:"
        payload = payload[:size]  # Truncate to exact size
        
        print(f"\nTesting payload size: {len(payload)} bytes")
        print(f"  Payload: {payload[:30]}{'...' if len(payload) > 30 else ''}")
        
        # Estimate encoding time
        duration = encoder.estimate_payload_duration(len(payload))
        print(f"  Estimated duration: {duration:.2f} seconds")
        
        # Encode and decode
        signal = encoder.encode_payload(payload.encode())
        actual_duration = len(signal) / encoder.sample_rate
        print(f"  Actual duration: {actual_duration:.2f} seconds")
        
        decoded_bytes = decoder.decode_payload(signal)
        
        if decoded_bytes:
            decoded = decoded_bytes.decode('utf-8', errors='ignore')
            if decoded == payload:
                print(f"  ✓ Success")
            else:
                print(f"  ✗ Mismatch (got {len(decoded)} bytes)")
        else:
            print(f"  ✗ Decode failed")


if __name__ == "__main__":
    print("Ultrasonic Agentics - Basic Encoding Examples")
    print("=" * 50)
    
    # Run all examples
    basic_encode_decode_example()
    test_different_commands()
    frequency_range_test()
    amplitude_sensitivity_test()
    noise_resilience_test()
    payload_size_test()
    
    print("\n" + "=" * 50)
    print("Examples completed!")